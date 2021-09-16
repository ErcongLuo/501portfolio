### Author : Ercong Luo
### The aim of this document is to source articles that mention 
### the environmental costs of recyling batteries


import requests
import json
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

### my API key: fea5c56a315742a8bcc16a4c19a1b31e
from newsapi import NewsApiClient

# Init
# newsapi = NewsApiClient(api_key='fea5c56a315742a8bcc16a4c19a1b31e')

# /v2/everything
url = ('https://newsapi.org/v2/everything?'
       #'q=university&'
       'q=electric vehicle AND environment&'
       #'from=2021-02-06&'
       #'to=2020-03-07&'
       #'sources=fox-news&'
       
    #   'sources=bbc-news&'
      #'sources=google-news&'
      #'sources=wired&'
     # 'sources=fox-news&'
      #'sources=business-insider&'

       
       'pageSize=100&'
       'apiKey=fea5c56a315742a8bcc16a4c19a1b31e'
       #'qInTitle=Georgetown&'
       #'country=us'

)
print(url)
response2 = requests.get(url)
jsontxt2 = response2.json()
print(jsontxt2, "\n")

filename = "batteryNewsArticles"

MyFILE=open(filename,"w")
### Place the column names in - write to the first row
WriteThis="Date,Source,Title,Headline\n"
MyFILE.write(WriteThis)
MyFILE.close()


## Open the file for append
MyFILE=open(filename, "a")

for items in jsontxt2["articles"]:
    print(items, "\n\n\n")
              
    #Author=items["author"]
    #Author=str(Author)
    #Author=Author.replace(',', '')
    
    Source=items["source"]["id"]
    print(Source)
    
    Date=items["publishedAt"]
    ##clean up the date
    NewDate=Date.split("T")
    Date=NewDate[0]
    print(Date)
    
    ## CLEAN the Title
    ##----------------------------------------------------------
    ##Replace punctuation with space
    # Accept one or more copies of punctuation         
    # plus zero or more copies of a space
    # and replace it with a single space
    Title=items["title"]
    Title=re.sub(r'[,.;@#?!&$\-\']+', ' ', Title, flags=re.IGNORECASE)
    Title=re.sub(' +', ' ', Title, flags=re.IGNORECASE)
    Title=re.sub(r'\"', ' ', Title, flags=re.IGNORECASE)
    
    # and replace it with a single space
    ## NOTE: Using the "^" on the inside of the [] means
    ## we want to look for any chars NOT a-z or A-Z and replace
    ## them with blank. This removes chars that should not be there.
    Title=re.sub(r'[^a-zA-Z]', " ", Title, flags=re.VERBOSE)
    Title=Title.replace(',', '')
    Title=' '.join(Title.split())
    Title=re.sub("\n|\r", "", Title)
    ##----------------------------------------------------------
    
    Headline=items["description"]
    Headline=re.sub(r'[,.;@#?!&$\-\']+', ' ', Headline, flags=re.IGNORECASE)
    Headline=re.sub(' +', ' ', Headline, flags=re.IGNORECASE)
    Headline=re.sub(r'\"', ' ', Headline, flags=re.IGNORECASE)
    Headline=re.sub(r'[^a-zA-Z]', " ", Headline, flags=re.VERBOSE)
    ## Be sure there are no commas in the headlines or it will
    ## write poorly to a csv file....
    Headline=Headline.replace(',', '')
    Headline=' '.join(Headline.split())
    Headline=re.sub("\n|\r", "", Headline)
    
    ### AS AN OPTION - remove words of a given length............
    Headline = ' '.join([wd for wd in Headline.split() if len(wd)>3])

    #print("Author: ", Author, "\n")
    #print("Title: ", Title, "\n")
    #print("Headline News Item: ", Headline, "\n\n")
    
    #print(Author)
    print(Title)
    print(Headline)
    
    WriteThis=str(Date)+","+str(Source)+","+ str(Title) + "," + str(Headline) + "\n"
    
    MyFILE.write(WriteThis)
    
## CLOSE THE FILE
MyFILE.close()