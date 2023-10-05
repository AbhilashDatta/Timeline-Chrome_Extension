import requests
from numpy.testing._private.utils import temppath
from bs4 import BeautifulSoup
import numpy as np
import GoogleNews
from GoogleNews import GoogleNews
from sentence_transformers import SentenceTransformer
import re
from flask import jsonify

model = SentenceTransformer('sentence-transformers/paraphrase-distilroberta-base-v2')

##test comment
def main(mainUrl): 
    mainHead,mainContent = getInfo(mainUrl)
    if not mainHead:
        badRequest = {1:'Bad Request'}
        return jsonify(badRequest)
    return getNews(mainHead,mainContent)


def getInfo(url):  # Return the headline and content of the p tags in the htmls
    try:
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        ReqJson = []
        headline = ''
        for title in soup.find_all('title'):   # headline
            headline += title.get_text()

        for _ in soup.find_all('p'):   # p tags
            if len(_.get_text()):
                ReqJson.append(_.get_text())

        content = ''.join(ReqJson)
        return headline,content
    except:
        return None,None

def areSimilar(v1,v2): # vector 1, vextor 2 , should be encoded 
    cos_sim = np.dot(v1.T, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))        
    if cos_sim[0]>0.3 and cos_sim[0]<0.97:
        return True
    return False



def getNews(headline , content):
    content = re.sub(r'[^\w\s]', '', str(content))   # removing all the punctutations
    mainPageEncodng = model.encode(content).reshape(-1,1)
    googlenews = GoogleNews()  # google news api object
    googlenews.set_lang('en')
    googlenews.set_period('7d')   # '7d' represents 7 days ,change the number to get lesser or more days' news
    googlenews.set_encode('utf-8')
    googlenews.get_news(headline) # query using the headline
    
    res = googlenews.result() #put indexing here to restrict the number of news you want to check 
    print("Articles Found:",len(res)) # Only for debugging
    similarNewsIndex = [] #[index of the news , similarity with our main content]
    for i in range(len(res)):
        print('Processing news number',i+1) #Only for debugging
        url = 'https://'+res[i]['link'] #res[i]['link'] has the link, but we have to add the https://
        _,tempContent = getInfo(url) 
        if not tempContent: # if url is not accesible
            continue

        tempContent = re.sub(r'[^\w\s]', '', tempContent) #removing punctutations
        tempContentEncoding = model.encode(tempContent)
    
        if areSimilar(mainPageEncodng,tempContentEncoding):
            similarNewsIndex.append(i)  #index of the news that are similar
    reqJson = {i:res[i] for i in similarNewsIndex} #jsonifying the similar news

    reqJson = jsonify(reqJson)
    return reqJson