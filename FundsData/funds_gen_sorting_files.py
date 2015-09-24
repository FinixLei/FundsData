# coding=utf-8

import re
import os
import string
from settings import WEB_PAGES, SORTING_FILES


class FundsSorter(object):
    def __init__(self):
        self.ALL_FUNDS = []
        self.all_sec_list = []
        self.FieldsList = [
            "Num", "Date", "Code", "Title", "Value",
            "IncToday", "IncWeek", "Inc1Month", "Inc3Months", "Inc6Months",
            "Inc1Year", "Inc2Years", "Inc3Years", "IncThisYear", "IncSinceCreated",
            "Birthday"
        ]

    def _gen_all_sec_list(self, specific_file):
        str_tbody_start = "<tbody>"
        str_tbody_end = "</tbody>"

        pt_tbody_start = re.compile(r'\s*<tbody>\s*')
        pt_tbody_end = re.compile(r'\s*</tbody>\s*')

        pt_sec_start = re.compile(r'\s*<tr>\s*')
        pt_sec_end = re.compile(r'\s*</tr>\s*')

        with open(specific_file, "r") as sf:
            s = sf.read()
            mylist = s.split('\n')

        if s.count(str_tbody_start) != 1 or s.count(str_tbody_end) != 1:
            print "Unrecognized tables: There are more than 1 pair of 'tbody' tags."
            return

        bInTable = False
        bInSection = False
        line_num = 0

        self.all_sec_list = []

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
                                self.all_sec_list.append(sec_list)
                                break

            else:  # not in table
                if pt_tbody_start.match(line):
                    bInTable = True

            line_num += 1

    def _fetch_field(self, line, mode, InfoList, field):
        try:
            pattern = re.compile(mode)
            res = pattern.search(line).groups()
            InfoList[field] = res[0] if res else "None"
        except Exception as ex:
            InfoList[field] = "None"
            if line.find('<td class="hide-col"></td>') == -1:
                print "Exception is %s: Wrong line is %s" % (str(ex), line)


    def analyze(self, file):
        self._gen_all_sec_list(file)

        for tr in self.all_sec_list:
            InfoList = {}

            count = 0
            for td in tr:
                if count == 0:      # Num
                    self._fetch_field(td, '\s+<td>(\d+)</td>\s*', InfoList, self.FieldsList[count])
                elif count == 1:    # Date
                    self._fetch_field(td, '<td .+>(.+)</td>', InfoList, self.FieldsList[count])
                elif count == 2:    # Code
                    self._fetch_field(td, '<td class=".+">(\d+)</td>', InfoList, self.FieldsList[count])
                elif count == 3:    # Title
                    self._fetch_field(td, '<td><a href.+>(.+)</a></td>', InfoList, "Title")
                elif count == 4:    # Value
                    self._fetch_field(td, '<td class=".+">(.+)</td>', InfoList, self.FieldsList[count])
                elif 5 <= count <= 14:
                    self._fetch_field(td, '<td class=".+"><span.*>(.+)</span></td>', InfoList, self.FieldsList[count])
                elif count == 15:   # Birthday
                    self._fetch_field(td, '<td class=.+>(.+)</td>', InfoList, self.FieldsList[count])
                else:
                    pass

                count += 1

            # Due to some kind of error in the web page downloaded, use the following validation
            if len(self.ALL_FUNDS) == 0 or self.ALL_FUNDS[len(self.ALL_FUNDS)-1]["Code"] != InfoList["Code"]:
                self.ALL_FUNDS.append(InfoList)

    def write_to_sorting_file(self, order):
        with open(SORTING_FILES[order], "w") as out_file:
            count = 1
            funds = []
            for rec in self.ALL_FUNDS:
                if rec[order].find('%') != -1:
                    funds.append(rec)

            for rec in sorted(funds, key=lambda record: string.atof(record[order].split("%")[0]), reverse=True):
                # line = '\t'.join([str(count), rec["Date"], rec["Code"], rec["Title"], rec["IncToday"], \
                #        rec["Inc1Month"], rec["Inc3Months"], rec["Inc6Months"], rec["Inc1Year"], rec["Inc2Years"], rec["Inc3Years"]]) + '\n'
                line = '\t'.join([str(count), rec["Date"], rec["Code"], rec["Title"], rec[order]]) + '\n'
                out_file.write(line)
                count += 1

    def get_all_funds(self):
        for i in sorted(WEB_PAGES.keys()):
            f = WEB_PAGES[i]['file']
            if os.path.exists(f):
                self.analyze(f)
            else:
                print "File %s does not exist!" % f

        return self.ALL_FUNDS

    def do_work(self):
        self.get_all_funds()

        self.write_to_sorting_file("Inc1Month")
        self.write_to_sorting_file("Inc3Months")
        self.write_to_sorting_file("Inc6Months")
        self.write_to_sorting_file("Inc1Year")
        self.write_to_sorting_file("Inc2Years")
        self.write_to_sorting_file("Inc3Years")


funds_sorter = FundsSorter()
