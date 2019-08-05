import json


class BookInfo:

    book_id = ""
    title = ""
    category = ""
    publish_date = ""
    book_url = ""
    torrent = ""
    torrent_page = ""
    tag = {}
    size = ""
    archive_page = ""

    def to_json(self):
        json_str = '{"book_id":"' + self.book_id + \
                   '", "title":"' + self.title + \
                   '", "category":"' + self.category + \
                   '", "publish_date":"' + self.publish_date + \
                   '", "book_url":"' + self.book_url + \
                   '", "torrent":"' + self.torrent + \
                   '", "torrent_page":"' + self.torrent_page + \
                   '", "tag":' + json.dumps(self.tag) + \
                   ', "archive_page":"' + self.archive_page + \
                   '", "size":"' + self.size + '"}'
        return json_str
