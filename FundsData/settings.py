import os
import time

BASEDIR = "/tmp/FundsData"

if not os.path.exists(BASEDIR):
    try:
        os.makedirs(BASEDIR)
    except Exception as ex:
        OLD_BASEDIR = BASEDIR
        BASEDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        print "Cannot create %s, will choose another folder for data: %s" % (OLD_BASEDIR, BASEDIR)

TODAY = time.strftime("%Y-%m-%d")

# settings for temporary downloaded web pages
TODAY_WEB_PAGE_DIR = os.path.join(os.path.join(BASEDIR, "web_pages"), TODAY)

if not os.path.exists(TODAY_WEB_PAGE_DIR):
    os.makedirs(TODAY_WEB_PAGE_DIR)

# settings for downloading web pages
URL = "http://huobijijin.com/jijin?order_by=5"  # 5 means "order by latest 6 months"
PAGE_NUM = 12

WEB_PAGES = {}
for i in range(PAGE_NUM):
    url = URL + "&page=" + str(i+1)
    target_file = os.path.join(TODAY_WEB_PAGE_DIR, TODAY + "_by_6_months_page_" + str(i+1) + ".html")
    WEB_PAGES[i] = {'url': url, 'file': target_file}

# settings for result files
RESULT_DIR = os.path.join(BASEDIR, "result")

# settings for sorting files
TODAY_SORTING_DIR = os.path.join(RESULT_DIR, "sorting_%s" % TODAY)

if not os.path.exists(TODAY_SORTING_DIR):
    os.makedirs(TODAY_SORTING_DIR)

# settings for sorting files
SORTING_FILES = {
    "Inc1Month": os.path.join(TODAY_SORTING_DIR, TODAY + "_by_1_month" + ".txt"),
    "Inc3Months": os.path.join(TODAY_SORTING_DIR, TODAY + "_by_3_months" + ".txt"),
    "Inc6Months": os.path.join(TODAY_SORTING_DIR, TODAY + "_by_6_months" + ".txt"),
    "Inc1Year": os.path.join(TODAY_SORTING_DIR, TODAY + "_by_1_year" + ".txt"),
    "Inc2Years": os.path.join(TODAY_SORTING_DIR, TODAY + "_by_2_years" + ".txt"),
    "Inc3Years": os.path.join(TODAY_SORTING_DIR, TODAY + "_by_3_years" + ".txt"),
}

# settings for get top N
# Each line below represents one set which matches all the orders listed
# Thus the following part can be designated by the user
top_100_cfg = {'Top': 100,
               'Inc3Years':  True,
               'Inc2Years':  True,
               'Inc1Year':   True,
               'Inc6Months': True,
               'Inc3Months': True,
               'Inc1Month':  True
               }
top_50_cfg = {'Top': 50,
              'Inc3Years':  True,
              'Inc2Years':  True,
              'Inc1Year':   True,
              'Inc6Months': True,
              'Inc3Months': True,
              'Inc1Month':  True
              }
