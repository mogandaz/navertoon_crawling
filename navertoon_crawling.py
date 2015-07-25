import lxml.html
import requests

def crawl_main_page():

    titleIDs = []
    pageID = 1

    while True:
        end = False
        base_url = "http://comic.naver.com/genre/bestChallenge.nhn?&page="

        response = requests.get(base_url + str(pageID))
        html_string = response.text
        dom = lxml.html.fromstring(html_string)

        webtoon_url = dom.cssselect("h6[class='challengeTitle'] a")

        for url in webtoon_url:
            if url.get('href')[32:] in titleIDs:
                end = True
                break
            else:
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


        stars = ep_dom.cssselect("span[id='topPointTotalNumber']")[0].text_content()
        stars_join = ep_dom.cssselect("span[class='pointTotalPerson'] em")[0].text_content()
        reg_date = ep_dom.cssselect("dd[class='date']")[0].text_content()
        view_cnt = ep_dom.cssselect("dd[class='date']")[1].text_content()

        record["stars"] = stars
        record["stars_join"] = stars_join
        record["reg_date"] = reg_date
        record["view_cnt"] = view_cnt

        cm_url = "http://comic.naver.com/ncomment/ncomment.nhn?titleId="+ str(toon_id) + "&no=" + str(idx) + "&levelName=BEST_CHALLENGE"
        cm_response = requests.get(cm_url)
        cm_html_string = cm_response.text
        cm_dom = lxml.html.fromstring(cm_html_string)

        data_table.append(record)

#    for i in data_table:
#        for key, value in i.iteritems():
#            print key + " " , value

    return data_table
