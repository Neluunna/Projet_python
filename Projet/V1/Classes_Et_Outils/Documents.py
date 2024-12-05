class Document:
    # Init
    def __init__(self, titre="", auteur="", date="", url="", texte="", type=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = type

    # Getters
    def __getTitre__(self):
        return self.titre
    def __getAuteur__(self):
        return self.auteur
    def __getDate__(self):
        return self.date
    def __getUrl__(self):
        return self.url
    def __getTexte__(self):
        return self.texte
    def __getType__(self):
        return self.type
    
    # Setters
    def __setTitre__(self, newTitre):
        self.titre=newTitre
    def __setAuteur__(self, newAuteur):
        self.auteur=newAuteur
    def __setDate__(self, newDate):
        self.date=newDate
    def __setUrl__(self, newUrl):
        self.url=newUrl
    def __setTexte__(self, newTexte):
        self.texte=newTexte
    
    # ToString()
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"

# héritage pour les deux catégories : Reddit et Arxiv

class RedditDocument(Document):
    def __init__ (self, titre="", auteur="", date="", url="", texte="", subreddit=""):
        super().__init__(titre, auteur, date, url, texte, "Reddit")
        self.subreddit = subreddit      # Reddit possède des subReddit 
                                        #  comme particularités
    
    # Getters
    def __getSub__(self):
        return self.subreddit
    def __getType__(self):
        return self.source

    # Setter
    def __setSub__(self, newSub):
        self.subreddit = newSub

    # ToString()
    def __str__(self):
        return f"{super().__str__()}; trouvé sur {self.source} dans le sub : {self.subreddit}"
    def __repr__(self):
        return f"{super().__repr__()}\tSource : {self.source}\tSubReddit : {self.subreddit}"

class ArxivDocument(Document):
    def __init__ (self, titre="", auteur="", date="", url="", texte="", coAuteurs=""):
        super().__init__(titre, auteur, date, url, texte, "Arxiv")
        self.coAuteurs = coAuteurs      # Arxiv possède des co-auteurs/trices
                                        #  comme particularités
    
    # Getters
    def __getCoAut__(self):
        return self.coAuteurs
    def __getType__(self):
        return self.source
    
    # Setters (ou adders)
    def __setCoAut__(self, newCoAut):
        self.coAuteurs = newCoAut
    def __addCoAut__(self, newCoAut):
        self.coAuteurs += f", {newCoAut}"

    # ToString()
    def __str__(self):
        return f"{super().__str__()} aidé par {self.coAuteurs}; trouvé sur {self.source} "
    def __repr__(self):
        return f"{super().__repr__()}\tSource: {self.source}\tCo-Auteurs: {self.coAuteurs} "
    
# =======================================================================
