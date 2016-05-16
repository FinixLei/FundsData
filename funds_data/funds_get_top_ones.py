import string
import os
from funds_gen_sorting_files import FundsSorter
from settings import TODAY, RESULT_DIR, top_100_cfg, top_50_cfg


ALL_FUNDS = []

def _gen_set(order, Top):
    global ALL_FUNDS
    funds = []
    for rec in ALL_FUNDS:
        if rec[order].find('%') != -1:
            funds.append(rec)
    
    count = 0
    my_list = []
    for rec in sorted(funds, key=lambda record: string.atof(record[order].split("%")[0]), reverse=True):
        my_list.append('\t'.join([rec["Code"], rec["Title"]]))
        count += 1
        if count >= Top:
            break
    
    my_set = set(my_list)
    return my_set


def get_intersection(WriteFile, Top=100,
                     Inc3Years=False, Inc2Years=False, Inc1Year=False,
                     Inc6Months=False, Inc3Months=False, Inc1Month=False):
    set_3years = _gen_set("Inc3Years", Top) if Inc3Years else set()
    set_2years = _gen_set("Inc2Years", Top) if Inc2Years else set()
    set_1year = _gen_set("Inc1Year", Top) if Inc1Year else set()
    set_6months = _gen_set("Inc6Months", Top) if Inc6Months else set()
    set_3months = _gen_set("Inc3Months", Top) if Inc3Months else set()
    set_1month = _gen_set("Inc1Month", Top) if Inc1Month else set()

    rating_set = ""
    final_set = None

    if Inc3Years:
        rating_set += "3 years "
        final_set = set_3years

    if Inc2Years:
        rating_set += "2 years "
        if final_set is not None:
            final_set = final_set & set_2years
        else:
            final_set = set_2years

    if Inc1Year:
        rating_set += "1 year "
        if final_set is not None:
            final_set = final_set & set_1year
        else:
            final_set = set_1year

    if Inc6Months:
        rating_set += "6 months "
        if final_set is not None:
            final_set = final_set & set_6months
        else:
            final_set = set_6months

    if Inc3Months:
        rating_set += "3 months "
        if final_set is not None:
            final_set = final_set & set_3months
        else:
            final_set = set_3months

    if Inc1Month:
        rating_set += "1 month "
        if final_set is not None:
            final_set = final_set & set_1month
        else:
            final_set = set_1month

    print "The following funds belong to top %d funds in recent %s" % (Top, rating_set)

    with open(WriteFile, "w") as wf:
        for item in final_set:
            line = item + '\n'
            wf.write(line)
            print line


def main():
    global ALL_FUNDS
    funds_sorter = FundsSorter()
    ALL_FUNDS = funds_sorter.get_all_funds()
    get_intersection(os.path.join(RESULT_DIR, "all_100_%s.txt" % TODAY), **top_100_cfg)
    get_intersection(os.path.join(RESULT_DIR, "all_50_%s.txt" % TODAY), **top_50_cfg)


if __name__ == "__main__":
    main()
