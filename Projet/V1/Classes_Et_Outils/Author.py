class Author:
    def __init__(self, name, production):
        self.__name = name
        self.__ndoc = 1
        self.__production =[production]
    
    def __str__(self):
        return self.__name
    
    def addDoc(self, document):
        if (document.__getAuteur__()==self.__str__()):
            self.__production.append(document)
            self.__ndoc=self.__ndoc+1
        else :
            print("Ceci n'est pas votre document")

    def addListDoc(self, documents):
        for i in documents:
            self.addDoc(i)

    def printAut(self):
       print("Informations complètes de l'auteur :")
       print(f"Nom : {self.__name}")
       print(f"Nombre de documents : {self.__ndoc}")
       for i in self.__production:
           print("\t" + i.__str__())