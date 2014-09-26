import os
import time

TODAY = time.strftime("%Y-%m-%d")
ROOT_DIR = "C:/Users/leile/funds_collection/basic_data"

if not os.path.exists(ROOT_DIR):
    ROOT_DIR = "./funds_collection/basic_data"

TARGET_DIR = os.path.join(ROOT_DIR, TODAY)
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)
    
URL = "http://huobijijin.com/jijin?order_by=5"

PAGE_NUM = 12
UF = {}
for i in range(PAGE_NUM):
    url = URL + "&page=" + str(i+1)
    target_file = os.path.join(TARGET_DIR, TODAY + "_by_6_months_page_" + str(i+1) + ".html")
    UF[i] = {'url' : url, 'file' : target_file}
    
# Below are analysis result files
RES_ROOT_DIR = "C:/Users/leile/funds_collection/result_data"
RES_DIR      = os.path.join(RES_ROOT_DIR, TODAY)

if not os.path.exists(RES_DIR):
    RES_ROOT_DIR = "./funds_collection/result_data"
    os.makedirs(RES_DIR)
    
RES_FILES = {
    "Inc1Month"  : os.path.join(RES_DIR, TODAY + "_by_1_month"  + ".txt"), 
    "Inc3Months" : os.path.join(RES_DIR, TODAY + "_by_3_months" + ".txt"), 
    "Inc6Months" : os.path.join(RES_DIR, TODAY + "_by_6_months" + ".txt"), 
    "Inc1Year"   : os.path.join(RES_DIR, TODAY + "_by_1_year"   + ".txt"), 
    "Inc2Years"  : os.path.join(RES_DIR, TODAY + "_by_2_years"  + ".txt"), 
    "Inc3Years"  : os.path.join(RES_DIR, TODAY + "_by_3_years"  + ".txt"), 
}