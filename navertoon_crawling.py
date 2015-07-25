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

def crawl_toon_page(toon_id):

    data_table = []
    url = "http://comic.naver.com/bestChallenge/list.nhn?titleId=" + str(toon_id)
    response = requests.get(url)
    html_string = response.text
    dom = lxml.html.fromstring(html_string)

    author = dom.cssselect("div[class='detail'] h2 span")[0].text_content()
    title = dom.cssselect("div[class='detail'] h2")[0].text_content()[:-len(author)]
    ep_cnt = int(dom.cssselect("td[class='title'] a")[0].get('href')[44:])

    for idx in range(2,ep_cnt):
        record = {}

        ep_url = "http://comic.naver.com/bestChallenge/detail.nhn?titleId=" + str(toon_id) + "&no=" + str(idx)
        ep_response = requests.get(ep_url)
        ep_html_string = ep_response.text
        ep_dom = lxml.html.fromstring(ep_html_string)

        record["webtoon_id"] = toon_id
        record["title"] = title
        record["author"] = author
        record["ep_id"] = idx

        data_table.append(record)

    return data_table
