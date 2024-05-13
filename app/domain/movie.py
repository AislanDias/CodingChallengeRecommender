class Movie:
    def __init__(self, title: str, content: str, genres: str, artist: str, id=None):  # type: ignore
        self.id = id
        self.title = title
        self.content = content
        self.genres = genres
        self.artist = artist
