class User:
    def __init__(self, username: str, genre: str, artist: str, id: int = None):  # type: ignore
        self.id = id
        self.username = username
        self.preferredGenre = genre
        self.preferredArtist = artist
