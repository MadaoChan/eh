from datetime import datetime


def list_to_json(book_list):
    size = len(book_list)
    json = '{"book_list": {'
    for index, book in enumerate(book_list):
        if index == size - 1:
            book_json = '"book": ' + book.to_json()
        else:
            book_json = '"book": ' + book.to_json() + ', '
        json = json + book_json
    json = json + "}}"
    return json


def save_json(json):
    dt = datetime.now()
    dt_str = dt.strftime("%Y-%m-%d_%H%M%S")
    path = "result\\" + dt_str + ".json"
    with open(path, 'w', encoding='utf-8', newline='') as f:
        try:
            f.write(json)
        finally:
            f.close()
