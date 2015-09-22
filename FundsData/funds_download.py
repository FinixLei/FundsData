import urllib2
from settings import WEB_PAGES


def download_all_webpages():
    for i in sorted(WEB_PAGES.keys()):
        try:
            url = WEB_PAGES[i]["url"]
            target_file = WEB_PAGES[i]["file"]

            print "Downloading %s......" % url
            f = urllib2.urlopen(url)
            with open(target_file, 'w') as tf:
                tf.write(f.read())

        except Exception as ex:
            print str(ex)
            break

def main():
    download_all_webpages()

if __name__ == "__main__":
    main()
