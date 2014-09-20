import urllib2
import funds_name

for key in sorted(funds_name.UF.keys()):
    try:
        url         = funds_name.UF[key]["url"]
        target_file = funds_name.UF[key]["file"]
        
        print("Downloading %s" % url)
        f = urllib2.urlopen(url)
        with open(target_file, 'w') as file:
            file.write(f.read())
    
    except Exception as ex:
        print(str(ex))
        break
