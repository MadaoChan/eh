from json_util import *
from util import *


base_url = "https://e-hentai.org/"
cookies = read_file("cookies.txt")

eh = get_bs(base_url, cookies)
print(get_page_count(eh))
book_list = get_all_books(eh)
book_list2 = get_all_torrent_url(book_list, cookies)
book_list3 = get_book_detail(book_list2, cookies)

json = list_to_json(book_list3)
print(json)
save_json(json)

# html_file = open("test.html", 'r', encoding='utf-8')
# html_handle = html_file.read()
# eh = BeautifulSoup(html_handle, 'html5lib')


# url = "https://e-hentai.org/archiver.php?gid=1457480&token=01058a136d&or=43469" \
#       "3--e83dc95cb90c5bfa3c0bce88b1ea848d3884644e"
# params = {"dltype": "org", "dlcheck": "Download Original Archive"}
# bs = post_bs(url, cookies, params)
# print(bs)

