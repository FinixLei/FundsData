# -*- coding: UTF-8 -*-

import re
import os
import time
import string
import funds_name


FieldsList = [
    "Num", "Date", "Code", "Title", "Value", 
    "IncToday", "IncWeek", "Inc1Month", "Inc3Months", "Inc6Months", 
    "Inc1Year", "Inc2Years", "Inc3Years", "IncThisYear", "IncSinceCreated", 
    "Birthday", 
]

ALL_FUNDS = []

def gen_all_sec_list(specific_file):
    str_tbody_start = "<tbody>"
    str_tbody_end   = "</tbody>"
    
    pt_tbody_start = re.compile(r'\s*<tbody>\s*')
    pt_tbody_end   = re.compile(r'\s*</tbody>\s*')
    
    pt_sec_start = re.compile(r'\s*<tr>\s*')
    pt_sec_end   = re.compile(r'\s*</tr>\s*')
    
    
    with open(specific_file, "r") as file:
        s = file.read()
        mylist = s.split('\n')
        
    if (s.count(str_tbody_start) != 1 or s.count(str_tbody_end) != 1):
        print("Unrecoginized tables: There are more than 1 pair of 'tbody' tags.")
        return
        
    bInTable   = False
    bInSection = False
    line_num   = 0
    
    all_sec_list = []
    
    while line_num < len(mylist):
        line = mylist[line_num]
        
        if bInTable:
            if pt_tbody_end.match(line):
                bInTable = False
                break
                
            elif not bInSection:
                if pt_sec_start.match(line):
                    bInSection = True
                    
                    sec_list = []
                    while bInSection:
                        line_num += 1
                        
                        if not pt_sec_end.match(mylist[line_num]) and line_num < len(mylist):
                            sec_list.append(mylist[line_num])
                        else:
                            bInSection = False
                            all_sec_list.append(sec_list)
                            break
                
        else: # not in table
            if pt_tbody_start.match(line):
                bInTable = True
                
        line_num += 1
        
    return all_sec_list
    
    
def _fetch_field(line, mode, InfoList, field):
    try:
        pattern = re.compile(mode)
        res = pattern.search(line).groups()
        InfoList[field] = res[0] if res else "None"
    except Exception as ex:
        InfoList[field] = "None"
        print("Exception is %s: Wrong line is %s" % (str(ex), line))

def analyze(all_sec_list):
    for tr in all_sec_list:
        InfoList = {}
        for key in FieldsList:
            InfoList[key] = "None" 
        
        count = 0
        for td in tr:
            if count == 0:      # Num
                _fetch_field(td, '\s+<td>(\d+)</td>\s*', InfoList, FieldsList[count])
            elif count == 1:    # Date
                _fetch_field(td, '<td .+>(.+)</td>', InfoList, FieldsList[count])
            elif count == 2:    # Code
                _fetch_field(td, '<td class=".+">(\d+)</td>', InfoList, FieldsList[count])
            elif count == 3:    # Title
                _fetch_field(td, '<td><a href.+>(.+)</a></td>', InfoList, "Title")
            elif count == 4:    # Value
                _fetch_field(td, '<td class=".+">(.+)</td>', InfoList, FieldsList[count])
            elif 5 <= count <= 14: 
                _fetch_field(td, '<td class=".+"><span.*>(.+)</span></td>', InfoList, FieldsList[count])
            elif count == 15:   # Birthday
                _fetch_field(td, '<td class=.+>(.+)</td>', InfoList, FieldsList[count])
            else:
                pass
                
            count += 1
        
        if len(ALL_FUNDS) == 0 or ALL_FUNDS[len(ALL_FUNDS)-1]["Code"] != InfoList["Code"]:
            ALL_FUNDS.append(InfoList) 
        


def write_to_res_file(order):
    with open(funds_name.RES_FILES[order], "w") as file:
        count = 1
        FUNDS = []
        for rec in ALL_FUNDS:
            if rec[order].find('%') != -1:
                FUNDS.append(rec)
                
        for rec in sorted(FUNDS, key=lambda record: string.atof(record[order].split("%")[0]), reverse=True):
            # line = '\t'.join([str(count), rec["Date"], rec["Code"], rec["Title"], rec["IncToday"], \
            #        rec["Inc1Month"], rec["Inc3Months"], rec["Inc6Months"], rec["Inc1Year"], rec["Inc2Years"], rec["Inc3Years"]]) + '\n'
            line = '\t'.join([str(count), rec["Date"], rec["Code"], rec["Title"], rec[order]]) + '\n'
            file.write(line)
            count += 1
                   

def _gen_set(order, Top):
    TODAY = time.strftime("%m-%d")
    FUNDS = []
    for rec in ALL_FUNDS:
        if rec[order].find('%') != -1 and rec["Date"] == TODAY:
            FUNDS.append(rec)
    
    count = 0
    my_list = []
    for rec in sorted(FUNDS, key=lambda record: string.atof(record[order].split("%")[0]), reverse=True):
        my_list.append('\t'.join([rec["Code"], rec["Title"]]))
        count += 1
        if count >= Top:
            break

    my_set = set(my_list)
    return my_set

def get_intersection(WriteFile, Top = 100, 
                     Inc3Years  = True, Inc2Years  = True, Inc1Year  = True,
                     Inc6Months = True, Inc3Months = True, Inc1Month = True):
    
    set_3years  = _gen_set("Inc3Years",  Top) if Inc3Years  else set()
    set_2years  = _gen_set("Inc2Years",  Top) if Inc2Years  else set()
    set_1year   = _gen_set("Inc1Year",   Top) if Inc1Year   else set()
    set_6months = _gen_set("Inc6Months", Top) if Inc6Months else set()
    set_3months = _gen_set("Inc3Months", Top) if Inc3Months else set()
    set_1month  = _gen_set("Inc1Month",  Top) if Inc1Month  else set()
    
    final_set = set_3years if Inc3Years else None
    if Inc2Years:
        final_set = final_set & set_2years  if final_set else set_2years
    if Inc1Year:
        final_set = final_set & set_1year   if final_set else set_1year
    if Inc6Months:
        final_set = final_set & set_6months if final_set else set_6months
    if Inc3Months:
        final_set = final_set & set_3months if final_set else set_3months
    if Inc1Month:
        final_set = final_set & set_1month  if final_set else set_1month
    
    with open(WriteFile, "w") as wfile:
        for item in final_set:
            wfile.write(item + '\n')


def main():
    for i in sorted(funds_name.UF.keys()):
        url  = funds_name.UF[i]['url']
        file = funds_name.UF[i]['file']
        if os.path.exists(file):
            all_sec_list = gen_all_sec_list(file)
            analyze(all_sec_list)
        else:
            print("File %s does not exist!" % file)
            
        write_to_res_file("Inc1Month")
        write_to_res_file("Inc3Months")
        write_to_res_file("Inc6Months")
        write_to_res_file("Inc1Year")
        write_to_res_file("Inc2Years")
        write_to_res_file("Inc3Years")
        
        cfg_100_all = {'Top':100, 'Inc3Years':True, 'Inc2Years':True, 'Inc1Year':True, 'Inc6Months':True, 'Inc3Months':True, 'Inc1Month':True}
        cfg_50_all  = {'Top':50,  'Inc3Years':True, 'Inc2Years':True, 'Inc1Year':True, 'Inc6Months':True, 'Inc3Months':True, 'Inc1Month':True}
        
        TODAY = time.strftime("%Y-%m-%d")
        get_intersection("./cfg_100_all" + TODAY +".txt", **cfg_100_all)
        get_intersection("./cfg_50_all" + TODAY +".txt",  **cfg_50_all)
        
    
if __name__:
    main()
    