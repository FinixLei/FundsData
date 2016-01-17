# coding=utf-8

######################################################################################################
# Usage: python gen_all_funds_report.py
#    This script parses all the htmls at the specified foler and generate one dict called total_hash, 
#    and merge the current report (if there is) into total_hash, and output total_hash to one file. 
######################################################################################################

import re
import os
import simplejson
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Settings
current_report_file = "./all_data.txt"
root_dir = '/tmp/FundsData'
web_pages_dir = os.path.join(root_dir, 'web_pages')
result_file = "./all_data_new.txt"


# pattern for parsing html files
file_path_mode = re.compile(r'.*?(\d{4})-(\d{2})-\d{2}')
tr_mode = re.compile(r'\s*<tr>\s*')
date_mode = re.compile(r'\s*<td.*?>(.+)\</td>')
id_mode = re.compile(r'\s*<td.*?>(\d+)</td>')
title_mode = re.compile(r'\s*<td.*?>.*title="(.+?)的历史收益情况".+</td>')
value_mode = re.compile(r'\s*<td.*?>(.+)</td>')

total_hash = {}

def analyze_file(file_path):
    try:
        year = '????'
        month = '??'
        if file_path_mode.match(file_path):
            res = file_path_mode.search(file_path).groups()
            if res and res[0] and res[1]:
                year = res[0] 
                month = res[1]
    except Exception as ex:
        print "Error happened when parsing file path: %s" % str(ex)
    
    try:
        with open(file_path, "r") as infile:
            lines =  infile.read().split('\n')
    except Exception as ex:
        print "Error happened when open file: " + str(ex)
        raise
            
    hit_flag = 0
    i = 0
    while i < len(lines):
        date, id, title, value = '????', 'id', 'title', 0
        
        try:
            if tr_mode.match(lines[i]):
                res = date_mode.search(lines[i+2]).groups()
                if res and res[0]:
                    month_value = res[0][0] + res[0][1]
                    year_value = int(year)
                    if month == '01' and month_value == '12':  # this is a potential bug, will fix it as below
                        year_value -= 1
                    date = "%d-%s" % (year_value, res[0])
                else:
                    i += 2
                    continue
                
                res = id_mode.search(lines[i+3]).groups()
                if res and res[0]:
                    id = res[0]
                else:
                    i += 3
                    continue
                
                res = title_mode.search(lines[i+4]).groups()
                if res and res[0]:
                    title = res[0]
                else:
                    i += 4
                    continue
                
                res = value_mode.search(lines[i+5]).groups()
                if res and res[0]:
                    value = res[0]                    
                else:
                    i += 5
                    continue
                    
                hit_flag = 1
                i += 6
            else:
                i += 1
                hit_flag = 0
                
        except Exception as ex:
            # print "Error happened in one loop: " + str(ex)
            i += 1
            
        if hit_flag:
            if total_hash.get(id) is None:
                total_hash[id] = {}
            total_hash[id]['title'] = title
            if total_hash[id].get(date) is None:
                total_hash[id][date] = value


def list_files(target_dir):
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            analyze_file(file_path)
            
        for dir in dirs:
            list_files(dir)
            

def output_total_hash(result_file):
    try:
        with open(result_file, 'w') as outfile:
            outfile.write("{\n")
            
            all_keys = sorted(total_hash.keys())
            last_key = all_keys[-1]
            
            indent = "    "  # 4 spaces
            for id in all_keys:
                outfile.write(indent + '"%s": {\n' % id)
                outfile.write(indent + indent + '"title": "%s",\n' % total_hash[id]['title'])
                
                all_id_keys = sorted(total_hash[id].keys())
                last_id_key = all_id_keys[-1] if all_id_keys[-1] != 'title' else all_id_keys[-2]
                
                for date in all_id_keys:
                    if date != 'title':
                        if date != last_id_key:
                            outfile.write(indent + indent + '"%s": %s,\n' % (date, total_hash[id][date]))
                        else:
                            outfile.write(indent + indent + '"%s": %s\n' % (date, total_hash[id][date]))
                        
                if id != last_key:
                    outfile.write(indent + "},\n")
                else:
                    outfile.write(indent + "}\n")
                    
            outfile.write("}\n")
        
    except Exception as ex:
        print "Error happened when output total_hash: %s" % str(ex)


def execute():
    # Step 1. Get current report
    try:
        with open(current_report_file, "r") as INFILE:
            content = INFILE.read()
        current_report = simplejson.loads(content)
    except Exception as ex:
        print "One exception: %s" % str(ex)
    
    # Step 2. Get report from web pages folder
    list_files(web_pages_dir)
    
    # Step 3. Merge current report into total_hash which represents information of latest web pages
    if current_report is not None:
        for id, info in current_report.iteritems():
            if total_hash.get(id) is not None:
                for date, value in current_report[id].iteritems():
                    if date != "title" and total_hash[id].get(date) is None:
                        total_hash[id][date] = value
            else:
                total_hash[id] = {}
                for k,v in current_report[id].iteritems():
                    total_hash[id][k] = v
        
    # Step 4. Output latest report of all funds
    output_total_hash(result_file)
        
if __name__ == "__main__":
    execute()
    