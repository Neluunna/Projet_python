from .Author import Author
from .Documents import Document, ArxivDocument, RedditDocument

class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur,doc)
            self.aut2id[doc.auteur] = self.naut
        else :
            self.authors[self.aut2id[doc.auteur]].addDoc(doc)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
    
    def __str__(self):
        print(self.nom + ": ")
        for i in self.id2doc.values():
            print(i)