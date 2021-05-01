
from Everest_Downloader import db

class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable =False)
    link = db.Column(db.String, nullable = False)

    def __init__(self,title, link):
        self.title = title
        self.link = link






