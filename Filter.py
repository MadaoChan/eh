class Filter:

    language = ""
    category = []

    def __init__(self, language, category) -> None:
        super().__init__()
        self.language = language
        self.category = category
