import requests
import json
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

### my API key: fea5c56a315742a8bcc16a4c19a1b31e
from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='fea5c56a315742a8bcc16a4c19a1b31e')

# /v2/everything
all_articles = newsapi.get_everything(q='electric vehicles AND carbon emissions',
                                      domains='techcrunch.com', 'nytimes.com', 'technologyreview.com', 'cnbn.com', 
                                      from_param='2018-01-01',
                                      to='2021-09-15',
                                      language='en',
                                      sort_by='relevancy',
                                      page=100)
