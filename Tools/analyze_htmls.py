# coding=utf-8

import re
import os

file_path_mode = re.compile(r'.*?(\d{4})-\d{2}-\d{2}')
tr_mode = re.compile(r'\s*<tr>\s*')
date_mode = re.compile(r'\s*<td.*?>(.+)\</td>')
id_mode = re.compile(r'\s*<td.*?>(\d+)</td>')
title_mode = re.compile(r'\s*<td.*?>.*title="(.+?)的历史收益情况".+</td>')
value_mode = re.compile(r'\s*<td.*?>(.+)</td>')

total_hash = {}

def analyze_file(file_path):
    try:
        year = '????'
        if file_path_mode.match(file_path):
            res = file_path_mode.search(file_path).groups()
            if res and res[0]:
                year = res[0] 
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
                    date = "%s-%s" % (year, res[0])
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
            

def print_total_hash():
    print "{"
    all_keys = sorted(total_hash.keys())
    last_key = all_keys[-1]
    
    for id in all_keys:
        print '    "%s": {' % id
        print '        "title": "%s",' % total_hash[id]['title']
        
        all_id_keys = sorted(total_hash[id].keys())
        last_id_key = all_id_keys[-1] if all_id_keys[-1] != 'title' else all_id_keys[-2]
        
        for date in all_id_keys:
            if date != 'title':
                if date != last_id_key:
                    print '        "%s": %s,' % (date, total_hash[id][date])
                else:
                    print '        "%s": %s' % (date, total_hash[id][date])
                
        if id != last_key:
            print "    },"
        else:
            print "    }"
    print "}"


if __name__ == "__main__":
    list_files('/tmp/FundsData/web_pages')
    print_total_hash()
