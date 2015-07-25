import lxml.html
import requests

def crawl_main_page():

    titleIDs = []
    pageID = 1

    while True:
        end = False
        base_url = "http://comic.naver.com/genre/bestChallenge.nhn?&page="
        print "***********" + str(pageID) + "*************"

        response = requests.get(base_url + str(pageID))
        html_string = response.text
        dom = lxml.html.fromstring(html_string)

        webtoon_url = dom.cssselect("h6[class='challengeTitle'] a")

        for url in webtoon_url:
            if url.get('href')[32:] in titleIDs:
                end = True
                break
            else:
                print type(url.get('href')[32:])
                titleIDs.append(url.get('href')[32:])

        if end:
            break

        pageID += 1

    return titleIDs
