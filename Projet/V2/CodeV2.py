from Classes_Et_Outils.Corpus import Corpus
from Classes_Et_Outils.Documents import Document, RedditDocument, ArxivDocument
from Classes_Et_Outils import Importation as dl

# ATTENTION : Il faut se positionner dans le répertoire "Projet"

# Tests généraux de Documents et Corpus

# AI generated exemples
Doc1 = Document("Climate Change Impacts", "Alice Martin", "2022-11-20", "https://example.com/climate-change-impacts", "This document explores the various impacts of climate change on ecosystems, economy, and human societies worldwide.")
Doc2 = ArxivDocument("Quantum Computing Basics", "Robert Brown", "2023-03-05", "https://example.com/quantum-computing", "An introduction to quantum computing, explaining fundamental principles like qubits, superposition, and entanglement.")
Doc3 = RedditDocument("Renewable Energy Innovations", "Alice Martin", "2023-08-30", "https://example.com/renewable-energy-innovations", "This document examines the latest innovations in renewable energy technologies, including advancements in solar, wind, and geothermal energy solutions.")

CorpusV2 = Corpus("NomV1")

CorpusV2.add(Doc1)
CorpusV2.add(Doc2)
CorpusV2.add(Doc3)

CorpusV2.search("quantum")
print(CorpusV2.concorde("and"))
CorpusV2.stats(10)

print(CorpusV2.tf())
print(CorpusV2.idf())
print(CorpusV2.tfidf())

print(CorpusV2.searchEngine(2,"quantum computing"))