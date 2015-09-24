# FundsData
----------------------------------------------------------
## Introduction
These scripts are downloading funds data from <http://huobijijin.com/>.  
Then analyze the downloaded data to generate 6 sorting files, which are the sorting funds based on 6 kinds of orders, e.g. last month, last 3 months, last 6 months, last year, last 2 years and last 3 years.  
At last, this script can give all the funds that are in the top 100 of the above 6 kinds of orders, and all the funds that are in the top 50 of the above 6 kinds of orders.
Generally speaking, the report will be under */tmp/FundsData/result* for Unix, and for Windows, the report will be under the *"data/result"* folder which is under the installation directory.  

<pre><code>
usage: python scripts/funds_data.py [-h] [-d] [-a] [-g] [-r] [-v]

optional arguments:
  -h, --help      show this help message and exit
  -d, --download  Only download the latest web pages from
                  http://huobijijin.com to data/webpages/<date>
  -a, --analyze   Analyze the downloaded web pages and generate the files
                  containing sorted funds. These files locate at
                  data/result/<sorting_<date>
  -g, --generate  Generate all the funds that are in the top 100 of all kinds
                  of orders, also generate all the funds that are in the top
                  50 of all kinds of orders.
  -r, --run       Dry run, including download the web pages, do analysis, and
                  generate the top 100 and top 50 funds matching all kinds of
                  orders. If don't specify any option, the effect is the same
                  as specifying this option.
  -v, --version   Show the version


</code></pre>

-----------------------------
## Distribution

Run the following commands to register, build and upload the package to PYPI.  

	python setup.py register sdist upload

The home page on PYPI is: <https://pypi.python.org/pypi/FundsData/0.90/>

-----------------------------
## Install

    sudo pip install FundsData

-----------------------------
## Usage

After installation, run the following command:

    python -mFundsData.funds_data -h

    python -mFundsData.funds_data
