# analyze\_htmls.pl & analyze\_htmls.py
Both analzye\_htmls.pl and analyze\_htmls.py implements the same function. It is to read and analyze all the html files at /tmp/FundsData/web_pages, and print out a json style output. See the sample below.  
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
analyze\_htmls.pl has been deprecated, as it's just a reference object for analyze\_htmls.py and its output format has been different from the latest output format of the python script.   
