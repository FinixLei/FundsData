# gen\_all\_funds\_report.py
gen\_all\_funds\_report.py implements the function that reads and analyzes all the html files at /tmp/FundsData/web_pages, and output to a json style file. If specify an existing report, it can merge the existing report to the analyzed result to be a bigger report. See the sample style below.  
<pre><code>	
{
"000001": {
    "title": "华夏成长",
    "2015-08-28": 3.5750,
    "2015-10-23": 3.6120,
    "2015-11-03": 3.5910,
    "2015-11-05": 3.6260,
    "2015-11-06": 3.65,
    "2015-11-10": 3.6580,
    "2015-11-17": 3.6550,
    "2015-11-20": 3.6970,
    "2015-11-26": 3.7110,
    "2015-12-01": 3.6420
},
......
}
</code></pre>  

The settings are in the script itself. 

# executor.py  
This script is to implement a trading algorithm. It also reports the money gain or lose.   

**Usage:**  
python executor.py  
