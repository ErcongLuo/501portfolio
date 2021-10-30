################################################ 
######### Author: Ercong Luo  ##################
######### Last Updated: 10/28/21 ###############
#########    ARM    ############################
################################################


# Setting up libraries 
library(arules)
library(arulesViz)
library(igraph)
library(networkD3)
library(visNetwork)
library(tidyverse)
library(tokenizers, stopwords)
library(rtweet)
#library(dployr)

############### GATHERING TWEETS ###############
tweet_df1 = search_tweets(q = "#EV lang:en", n = 1000, type = "mixed", include_rts = F)
tweet_df2 = search_tweets(q = "electric cars lang:en", n = 1000, type = "mixed", include_rts = F)
tweet_df3 = search_tweets(q = "environment AND EV lang:en", n = 1000, type = "mixed", include_rts = F)
tweet_df4 = search_tweets(q = "#EV lang:en", n = 100, type = "popular", include_rts = F)
tweet_df5 = search_tweets(q = "electric cars lang:en", n = 100, type = "popular", include_rts = F)
tweet_df6 = search_tweets(q = "environment AND EV lang:en", n = 100, type = "popular", include_rts = F)

df = rbind(tweet_df1, tweet_df2)
df = rbind(df, tweet_df3)
df = rbind(df, tweet_df4)
df = rbind(df, tweet_df5)
df = rbind(df, tweet_df6)
write.csv(df, file = "rawtweets.csv")
df = df['text']



############### TOKENIZING ###############
############### {STOP WORDS, PUNCTUATION, NUMERIC CHARS} REMOVED ###############
for (row in c(1:nrow(df))){
  df$text[row] = tokenize_words(df$text[row], strip_numeric = T, strip_punct = T, stopwords = c(stopwords::stopwords("en", source = "nltk"), c("https", "t.co")))
}

############### APPLYING APRIORI ###############
a_list = as.list(df$text)
names(a_list) <- paste("Tr",c(1:length(a_list)), sep = "")
transaction = transactions(a_list)
rules = apriori(transaction, parameter = list(supp = 50/length(a_list), conf = 0.1, target = "rules", minlen=1, maxlen=3))

############### WRITE RULES, TOP RULES TO .CSV FILES ###############
write.csv(DATAFRAME(rules), "rules.csv")
write.csv(DATAFRAME(head(rules, by = "support", n = 15)), "15supp.csv")
write.csv(DATAFRAME(head(rules, by = "confidence", n = 15)), "15conf.csv")
write.csv(DATAFRAME(head(rules, by = "lift", n = 15)), "15lift.csv")


############### Networking using igraph ############### 
vis1 = plot(head(rules, by = "confidence", n = 100), method = "graph", control = list(verbose = FALSE),
                   measure = "confidence", shading = "confidence", engine = "htmlwidget")
vis2 = plot(head(rules, by = "lift", n = 100), method = "graph", control = list(verbose = FALSE),
            measure = "lift", shading = "lift", engine = "htmlwidget")
vis3 = plot(head(rules, by = "support", n = 100), method = "graph", control = list(verbose = FALSE),
             measure = "support", shading = "support", engine = "htmlwidget")



htmlwidgets::saveWidget(vis1, "conf.html", selfcontained = TRUE)
htmlwidgets::saveWidget(vis2, "lift.html", selfcontained = TRUE)
htmlwidgets::saveWidget(vis3, "supp.html", selfcontained = TRUE)







