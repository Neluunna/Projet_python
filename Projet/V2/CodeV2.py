from Classes_Et_Outils.Corpus import Corpus
from Classes_Et_Outils.Documents import Document, RedditDocument, ArxivDocument
from Classes_Et_Outils import Importation as dl

# ATTENTION : Il faut se positionner dans le répertoire "Projet"

# Tests généraux de Documents et Corpus

# AI generated exemples
Doc1 = Document("Climate Change Impacts", "Alice Martin", "2022-11-20", "https://example.com/climate-change-impacts", "This document explores the various impacts of climate change on ecosystems, economies, and human societies worldwide.")
Doc2 = ArxivDocument("Quantum Computing Basics", "Robert Brown", "2023-03-05", "https://example.com/quantum-computing", "An introduction to quantum computing, explaining fundamental principles like qubits, superposition, and entanglement.")
Doc3 = RedditDocument("Renewable Energy Innovations", "Alice Martin", "2023-08-30", "https://example.com/renewable-energy-innovations", "This document examines the latest innovations in renewable energy technologies, including advancements in solar, wind, and geothermal energy solutions.")

CorpusV1 = Corpus("NomV1")

CorpusV1.add(Doc1)
CorpusV1.add(Doc2)
CorpusV1.add(Doc3)

CorpusV1.search("quantum")
print(CorpusV1.concorde("and"))
CorpusV1.stats()

# Tests pour importations

