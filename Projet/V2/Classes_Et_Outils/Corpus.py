from .Author import Author
from .Documents import Document, ArxivDocument, RedditDocument
import re
import pandas as pd
import scipy as sp
import numpy as np

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
    
    def search(self, mot):
        try:
            texte = self.textes_all
        except:
            self.textes_all = " ".join([doc.__getTexte__() for doc in [*self.id2doc.values()]])
            texte = self.textes_all
        pattern = re.compile(mot,re.IGNORECASE)
        res = pattern.finditer(texte)
        start_pattern = [m.start() for m in res]
        print(f'{len(start_pattern)} occurences found')
        return(texte[i-20:i+20] for i in start_pattern)
    
    def concorde(self, mot, taille_contexte=20):
        # Utiliser une expression régulière pour trouver le motif
        pattern = re.compile(mot, re.IGNORECASE)
        res = pattern.finditer(self.textes_all)
            
        # Stocker les résultats dans une liste
        concordance = []
        for m in res:
            start, end = m.start(), m.end()
            contexte_gauche = self.textes_all[max(0, start-taille_contexte):start]
            motif_trouve = self.textes_all[start:end]
            contexte_droit = self.textes_all[end:end+taille_contexte]
            
            concordance.append({
                "contexte gauche": contexte_gauche.strip(),
                "motif trouvé": motif_trouve,
                "contexte droit": contexte_droit.strip()
            })
            
        # Créer un DataFrame pandas
        df = pd.DataFrame(concordance)
        print(f'{len(df)} occurrences trouvées.')
        return df
    
    def nettoyer_texte(self, str):
        resultat = str.lower()
        resultat = resultat.replace('\n', ' ')
        chiffres = {
            "0": "zéro", "1": "un", "2": "deux", "3": "trois", "4": "quatre",
            "5": "cinq", "6": "six", "7": "sept", "8": "huit", "9": "neuf"
        }
        pattern = re.compile(r'\b\d+\b')
        matches = pattern.findall(resultat)
        for match in matches:
            lettres = " ".join(chiffres[ch] for ch in match)
            resultat = resultat.replace(match, lettres, 1)
        return resultat
    
    def construire_vocabulaire(self):
        vocabulaire_set = set()
        freq = {}  # Dictionnaire pour compter les occurrences des mots
        df = {}    # Dictionnaire pour compter les documents contenant chaque mot
        
        # Parcourir les documents du corpus
        for doc_id, doc in self.id2doc.items():
            texte = doc.__getTexte__().lower()  # Convertir le texte en minuscules
            mots = set(re.findall(r"\b\w[\w']*\b", texte))  # Utiliser un set pour ne pas compter plusieurs fois le même mot dans un même document
            
            # Mettre à jour le vocabulaire et compter les occurrences
            for mot in mots:                
                # Compter l'occurrence du mot dans tous les documents (TF)
                if mot in freq:
                    freq[mot] += 1
                else:
                    freq[mot] = 1
                
                # Compter le nombre de documents où le mot apparaît (DF)
                if mot in df:
                    df[mot] += 1
                else:
                    df[mot] = 1
        
        # Créer un DataFrame pandas avec les fréquences des mots et la document frequency
        df_freq = pd.DataFrame(list(freq.items()), columns=['Mot', 'Fréquence'])
        df_df = pd.DataFrame(list(df.items()), columns=['Mot', 'Document Frequency'])
        
        # Fusionner les deux DataFrames (fréquence et document frequency)
        df_final = pd.merge(df_freq, df_df, on='Mot', how='left')
        
        # Trier le DataFrame par fréquence décroissante
        df_final = df_final.sort_values(by='Fréquence', ascending=True).reset_index(drop=True)
        
        # Retourner le tableau des fréquences et des document frequencies
        return df_final
    
    def stats(self, n=10):
        # Construire les fréquences si elles n'ont pas été calculées
        cache= self.construire_vocabulaire()
        
        print("Statistiques du corpus :")
        # Nombre de mots différents
        nb_mots_differents = len(cache)
        print(f"Nombre de mots différents dans le corpus : {nb_mots_differents}")
        
        # Les n mots les plus fréquents
        print(f"\nLes {n} mots les plus fréquents :")
        print(cache.head(n))

    def tf(self):
        # Initialiser un vocabulaire pour les mots
        vocab = {}
        unique_id = 0
    
        # Parcourir les documents pour construire le vocabulaire
        for word in sorted(self.textes_all.lower().split()):
            if word not in vocab:
                # Si le mot n'est pas dans le vocabulaire, lui attribuer un nouvel ID
                vocab[word] = {
                    'unique_id': unique_id,
                    'total_occurrence': 1
                }
                unique_id += 1
            else:
                # Si le mot est déjà dans le vocabulaire, incrémenter son compteur d'occurrences
                vocab[word]['total_occurrence'] += 1
        
        # Préparer les données pour la matrice TF
        rows = []
        cols = []
        data = []
        
        # Parcourir les documents pour remplir les lignes et colonnes
        for i, doc in enumerate(self.id2doc.values()):
            for word in doc.__getTexte__().lower().split():
                if word in vocab:
                    rows.append(i)  
                    cols.append(vocab[word]['unique_id']) 
                    data.append(1) 
        
        tf_matrix = sp.sparse.csr_matrix((data, (rows, cols)), shape=(self.ndoc, len(vocab)))
    
        return tf_matrix
        
    def idf(self):
        n_docs= self.ndoc
        # Nombre de documents contenant chaque terme
        df = np.array((self.tf() > 0).sum(axis=0)).flatten()
        
        # Calcul de l'IDF
        idf_values = np.log((n_docs + 1) / (df + 1)) + 1  # Évite log(0) avec le +1
        
        return idf_values
    
    def tfidf(self):
        
        # Normaliser la matrice TF par les poids IDF
        tf_idf_matrix= self.tf().multiply(self.idf())

        return sp.sparse.csr_matrix(tf_idf_matrix)