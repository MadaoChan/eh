import random
import re

from bs4 import BeautifulSoup
import requests

from BookInfo import BookInfo

my_headers = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]


def get_bs(url, cookies):
    random_header = random.choice(my_headers)
    headers = {"User-Agent": random_header, "Cookie": cookies}
    content = requests.get(url, headers=headers).text
    bs = BeautifulSoup(content, 'html5lib')
    return bs


def post_bs(url, cookies, params):
    random_header = random.choice(my_headers)
    headers = {"User-Agent": random_header, "Cookie": cookies}
    content = requests.post(url, headers=headers, data=params).text
    bs = BeautifulSoup(content, 'html5lib')
    return bs


def get_page_count(bs_obj):
    ptt = bs_obj.find("table", {"class": "ptt"})
    tds = ptt.find_all("td")
    index = len(tds) - 2
    count_td = tds[index]
    count = count_td.find("a").get_text()
    return count


def get_all_books(bs):
    list_table = bs.find("table", {"class": "itg gltc"})
    trs = list_table.find_all("tr")
    # 过滤头部标题
    trs_without_header = trs[1:]
    # 过滤广告
    book_info_list = []
    for tr in trs_without_header:
        gl1c_td = tr.find("td", {"class": "gl1c glcat"})
        if gl1c_td is None:
            continue
        else:
            book_info = get_book_info(tr)
            book_info_list.append(book_info)
    print(len(book_info_list))
    return book_info_list


def get_book_info(bs):
    info = BookInfo()
    gl2c = bs.find("td", {"class": "gl2c"})
    if gl2c is not None:
        date_div = gl2c.find("div", id=re.compile("posted"))
        if date_div is not None:
            info.publish_date = date_div.get_text()

    glname = bs.find("td", {"class": "gl3c glname"})
    if glname is not None:
        url_a = glname.find("a")

        if url_a is not None:
            info.book_url = url_a["href"]

        glink = glname.find("div", {"class": "glink"})
        if glink is not None:
            info.title = glink.get_text()

    gldown = gl2c.find("div", {"class": "gldown"})
    if gldown is not None:
        gldown_a = gldown.find("a")
        if gldown_a is not None:
            info.torrent_page = gldown_a["href"]

    cn = bs.find("div", {"class", "cn"})
    if cn is not None:
        info.category = cn.get_text()
    return info


def get_all_torrent_url(book_list, cookie_dict):
    for book_info in book_list:
        if book_info.torrent_page.__contains__("http"):
            bs = get_bs(book_info.torrent_page, cookie_dict)
            torrent_table = bs.find_all("table")
            if len(torrent_table) > 0:
                torrent_tr = torrent_table[0].find_all("tr")
                if len(torrent_tr) > 2:
                    torrent_td = torrent_tr[2].find("td")
                    if torrent_td is not None:
                        href = torrent_td.find("a")["href"]
                        book_info.torrent = href
    return book_list


def get_book_detail(books, cookies):
    for book in books:
        if book.book_url.__contains__("http"):
            bs = get_bs(book.book_url, cookies)
            # 获取下载链接
            gd5 = bs.find("div", {"id": "gd5"})
            if gd5 is not None:
                p_buttons = gd5.find_all("p", {"class": "g2"})
                if p_buttons is not None:
                    archive_p = p_buttons[0]
                    if archive_p is not None:
                        onclick = archive_p.find("a")["onclick"]
                        if onclick is not None:
                            splits = onclick.split("'")
                            if len(splits) >= 2:
                                book.archive_page = splits[1]
            # 获取tag list
            taglist = bs.find("div", {"id": "taglist"})
            if taglist is not None:
                tag_trs = taglist.find_all("tr")
                if tag_trs is not None:
                    tag_cat = ""
                    tag_dict = {}
                    for tag_tr in tag_trs:
                        tag_tds = tag_tr.find_all("td")

                        if tag_tds is not None:
                            for tag_td in tag_tds:
                                tags_div = tag_td.find_all("div")
                                if len(tags_div) > 0:
                                    for tag_div in tags_div:
                                        tag = tag_div.find("a")
                                        if tag is not None:
                                            name = tag.get_text()
                                            tag_dict.setdefault(tag_cat, list()).append(name)
                                else:
                                    tag_cat = tag_td.get_text().replace(":", "")
                    book.tag = tag_dict
                    # print(book.title + " " + json.dumps(book.tag))
            # 获取file_size
            gdd = bs.find("div", {"id": "gdd"})
            if gdd is not None:
                gdt2_tds = gdd.find_all("td", {"class": "gdt2"})
                if gdt2_tds is not None:
                    for gdt2 in gdt2_tds:
                        if gdt2.get_text().__contains__(" MB"):
                            book.size = gdt2.get_text()
    return books


def read_file(file):
    file_object = open(file, 'r')
    all_the_text = ""
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()
        return all_the_text


def cookie_to_dict(cookie):
    cookie_dict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        cookie_dict[key] = value
    return cookie_dict


