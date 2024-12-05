import urllib
import urllib.request
import praw
import json
from datetime import date

import xmltodict
import datetime
import pandas as panda

from .Documents import Document, RedditDocument, ArxivDocument
from .Corpus import Corpus

c_id= 'BYxnYk3vn0M4mnQ7RYMyhA'
c_secret= 'oXb1p2xrJW3a6Yd-_cc72tXPeOHdsQ'
u_agent= 'TVLyon2'

reddittxt=[]
arxivtxt=[]

def sauvegarder(Query,name="Imported", number= 50):
    textes_Reddit, textes_Arxiv = [], []

    i = praw.Reddit(client_id=c_id,client_secret=c_secret,user_agent=u_agent)
    RedditDocs = i.subreddit(Query).hot(limit=number)

    for doc in RedditDocs :
        docR= [doc.title, 
                        doc.author.name, 
                        date.fromtimestamp(doc.created).strftime("%d/%m/%Y"), 
                        doc.url, 
                        doc.selftext.replace("\n",""),
                        "r/"+doc.subreddit.display_name]
        textes_Reddit.append(docR)
        

    url= 'http://export.arxiv.org/api/query?search_query=all:'+ Query +'&start=0&max_results='+number
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
    
    corpus_df['data']= corpus_df['data'].apply(lambda x: json.dumps(x))
    corpus_df.to_csv('V1/Classes_Et_Outils/'+name+'.csv', sep='\t', index=False)
    print("save : done")

def corpusAddAll(Corpus, path="V1/Classes_Et_Outils/Imported"): 
    docs = panda.read_csv(path+'.csv', sep='\t', encoding='utf-8')
    docs['data'] = docs['data'].apply(lambda x: json.loads(x))
    
    for i in range(len(docs)):
        row = docs.iloc[i]
        doc= row['data']
        if row['Source'] == 'Reddit':
            if len(doc[4])>25:
                # Documents making
                Corpus.add(RedditDocument(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
                
        elif row['Source'] == 'Arxiv':
            text = doc.get('summary').replace("\n"," ")
            if len(text)>25:
                # Document making
                coAuthors = []
                if len(doc['author'])>1:
                    for i in doc['author']:
                        if i!=doc['author'][0]: coAuthors.append(i['name'])

                    Corpus.add(ArxivDocument(doc['title'],
                            doc['author'][0]['name'],
                            datetime.datetime.strptime(doc['published'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y"),
                            doc['id'],
                            text,
                            coAuthors))
                else :
                    Corpus.add(ArxivDocument(doc['title'],
                            doc['author']['name'],
                            datetime.datetime.strptime(doc['published'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y"),
                            doc['id'],
                            text,
                            coAuthors))
        else :
            None