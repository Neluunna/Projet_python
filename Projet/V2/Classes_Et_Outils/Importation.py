import urllib
import urllib.request
import praw

import xmltodict
import datetime
import pandas as panda

from .Documents import RedditDocument, ArxivDocument
from .Corpus import Corpus

c_id= 'BYxnYk3vn0M4mnQ7RYMyhA'
c_secret= 'oXb1p2xrJW3a6Yd-_cc72tXPeOHdsQ'
u_agent= 'TVLyon2'

reddittxt=[]
arxivtxt=[]

def sauvegarder(Query,name="Imported"):
    textes_Reddit, textes_Arxiv = []

    i = praw.Reddit(client_id=c_id,client_secret=c_secret,user_agent=u_agent)
    RedditDocs = i.subreddit(Query).hot(limit=50)

    for DocR in RedditDocs :
        textes_Reddit.append(DocR)

    url= 'http://export.arxiv.org/api/query?search_query=all:'+ Query +'&start=0&max_results=50'
    RawArxivRes = xmltodict.parse(urllib.request.urlopen(url).read().decode('utf-8'))
    ArxivDocs=RawArxivRes['feed']['entry']

    for article in ArxivDocs :
        textes_Arxiv.append(article)
            
    corpus = textes_Reddit + textes_Arxiv
    print("import: done")
    
    corpus_df = panda.DataFrame.from_dict({
        'ID': range(1, len(corpus)+1),
        'data': [i for i in corpus],
        'Source': ['Reddit' if i< len(textes_Reddit) else 'Arxiv' for i in range(len(corpus))]
    })
    print("processing: done")
    corpus_df.to_csv(name+'.csv', sep='\t')

# cette fonction ne fonctionne qu'avec 

def corpusAddAll(Corpus, path="Imported"): 
    docs = panda.read_csv(path+'.csv', sep='\t', encoding='utf-8')
    
    for doc in range(len(docs)):
        row = docs.iloc[i]

        if row['Source'] == 'Reddit':
            text = doc.replace("\n"," ")
            if text.len()>25:
                # Documents making
                Corpus.add(RedditDocument( doc.title, 
                        doc.author, 
                        doc.date.fromtimestamp(doc.created).strftime("%d/%m/%Y"), 
                        doc.url, 
                        text,
                        doc.subreddit))
                
        elif row['Source'] == 'Arxiv':
            text = doc['summary'].replace("\n"," ")
            if text.len()>25:
                # Document making
                coAuthors = []
                for i in doc['author']:
                    if i!=doc['author'][1]: coAuthors.append(i)

                Corpus.add(ArxivDocument(doc['title'],
                        doc['author'][1],
                        datetime.datetime.strptime(doc['published'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y"),
                        doc['id'],
                        text,
                        coAuthors))
        else :
            None