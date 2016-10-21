############################################################
#                    Google Downloader                     #
# Creator: Tyler Moon                                      #
# Contributors:                                            #
# Purpose: This script uses the most common keywords in    #
# the keywordsCondensed.txt file and scrapes Google Images #
# webpage. Once an image has been found it downloads it    #
# into the createdMemes directory                          #
############################################################
from icrawler.examples import GoogleImageCrawler

kwd = ""
with open('keywordsCondensed.txt') as my_file:
    kwd = my_file.readline()
    kwd = kwd.replace('FIRSTCOMMON=','')
    print kwd

google_crawler = GoogleImageCrawler('createdMemes')
google_crawler.crawl(keyword=kwd, offset=0, max_num=1,
                     date_min=None, date_max=None, feeder_thr_num=1,
                     parser_thr_num=1, downloader_thr_num=4,
                     min_size=(200,200), max_size=None)
