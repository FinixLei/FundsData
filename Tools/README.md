# analyze\_htmls.py
analyze\_htmls.py implements the function that reads and analyzes all the html files at /tmp/FundsData/web_pages, and print out a json style output. See the sample below.  
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

**Usage:**  
python analyze\_htmls.py  
The result file "/tmp/FundsData/result/all_data.txt" will be generated. It is a file containing a pure big json. 
