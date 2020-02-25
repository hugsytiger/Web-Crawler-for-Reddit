#!/usr/bin/env python
# coding: utf-8

# # CompLing Final Project- Automated Web Crawling

# ### In this notebook, we will learn a concept of the package-BeautifulSoup and its implementation

# ## Outline:

# <img src="img/outline.png" alt="Outline" style="width:800px;"/>

# ## HTTP Protocol

# <img src="img/http.png" alt="Http" style="width:600px;"/>

# HTTP functions as a request-response protocol in the client-server computing model. The **client** submits an HTTP _request_ message to the server. The **server**, which provides resources such as HTML files and other contents, returns a _response_ message to the client.

# ## Scrape the titles and comments from the website-Reddit:
# 

# In[25]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import schedule
import time

'''url=the url of the website that I want to scrape,
html=use the urlopen function to fetch URLs
soup=use the beautifulsoup to parse the response from the server'''

url = "https://www.reddit.com/"
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")

reddit_text = soup.find_all("h3",class_="_eYtD2XCVieq6emjKBH3m")
reddit_texts = [e.text for e in reddit_text]

reddit_comment = soup.find_all("span",class_= "FHCV02u6Cp2zYL0fhQPsO")
reddit_comments = [f.text for f in reddit_comment]

print(reddit_text)
print(reddit_comment)


# In[26]:


print(reddit_texts)
print(reddit_comments)


# In[27]:


'''clear all the punctuations and lowercase the texts in the title'''
   
a=0
for a in range(len(reddit_texts)):
   for b in '!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~':
       reddit_texts[a] = reddit_texts[a].replace(b, "")
       reddit_texts[a] = reddit_texts[a].lower()

print(reddit_texts)


# In[28]:


'''check if there is a repeated title'''
print(len(reddit_texts))
print(len(reddit_comments))


# In[29]:


'''delete the repeated title if there is one'''
c=0
reddit_texts1=[]
for c in range(len(reddit_texts)):
    if reddit_texts[c] not in reddit_texts1:
        reddit_texts1.append(reddit_texts[c])

print(reddit_texts1)


# In[30]:


'''check again'''
print(len(reddit_texts1))
print(len(reddit_comments))


# In[31]:


'''delete the word "comments"'''
d=0
for d in range(len(reddit_comments)):
    reddit_comments[d]=reddit_comments[d].replace("comments","")
    
print(reddit_comments)


# In[33]:


'''search word from the titles, if it matches, append the titles that contain the search word into the 
new list reddit_search, and also append the corresponding comments to the new list reddit_comments'''
    
search_word=["history","development"]
e=0
reddit_search=[]
reddit_search_comment=[]
for e in range(len(reddit_texts1)):
    words = reddit_texts1[e].split()
    for word in words:
        if word in search_word and reddit_texts1[e] not in reddit_search:
            reddit_search.append(reddit_texts1[e])
            reddit_search_comment.append(reddit_comments[e])
    
print(reddit_search)
print(reddit_search_comment)


# In[34]:


'''delete the ".","k","", plus 2 zeros and convert the list to interger
if the number is too large, the format will become BLOB when storing in the database which is hard to read
so I divide the number by 10 to get the numeric format'''

f=0
for f in range(len(reddit_search_comment)):
    if "k" in reddit_search_comment[f]:
        reddit_search_comment[f]=reddit_search_comment[f].replace(".","")
        reddit_search_comment[f]=reddit_search_comment[f].replace("k","")
        reddit_search_comment[f]=reddit_search_comment[f].replace(" ","")
        reddit_search_comment[f]=reddit_search_comment[f]+"00"
        reddit_search_comment[f]=(int(reddit_search_comment[f])/10)
    else:
        reddit_search_comment[f]=(int(reddit_search_comment[f])/10)
        
        
print(reddit_search)
print(reddit_search_comment)


# In[35]:


'''use the panda package to convert to dataframe(table) format'''

df = pd.DataFrame(
    {"reddit_search":reddit_search, "reddit_search_comment":reddit_search_comment
    })
df.head()


# In[36]:


''' A new file called test.db is created where the database will be stored,
    connect Python to database, create the table in database'''

conn = sqlite3.connect('test.db')
c = conn.cursor()
#c.execute("CREATE TABLE COMPLING1206 (TITLE TEXT, COMMENTS INTEGER);"
    #)


# <img src="img/cursor1.png" alt="cursor" style="width:600px;"/>

# In[37]:


'''insert the data into the table'''

g=0
for g in range(len(df)):
    c.execute("INSERT INTO COMPLING1206 VALUES (?,?)", (df["reddit_search"][g],df["reddit_search_comment"][g],))
    conn.commit()


# ## Scheduler

# In[18]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import URLError
import pandas as pd
import sqlite3
import schedule
import time

def redditsqlitegogo():
    try:
        url = "https://www.reddit.com/"
        html = urlopen(url)
        soup = BeautifulSoup(html, "html.parser")

        reddit_text = soup.find_all("h3",class_="_eYtD2XCVieq6emjKBH3m")
        reddit_texts = [e.text for e in reddit_text]

        reddit_comment = soup.find_all("span",class_= "FHCV02u6Cp2zYL0fhQPsO")
        reddit_comments = [f.text for f in reddit_comment]
    
        #print(reddit_comments)

       
        a=0
        for a in range(len(reddit_texts)):
            for b in '!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~':
                reddit_texts[a] = reddit_texts[a].replace(b, " ")
                reddit_texts[a] = reddit_texts[a].lower()
    
        #print(reddit_texts)   
        
        c=0
        reddit_texts1=[]
        for c in range(len(reddit_texts)):
            if reddit_texts[c] not in reddit_texts1:
                reddit_texts1.append(reddit_texts[c])
    
        print(reddit_texts)
        # When encountering more than two repeated titles, it's hard to match the titles and comments,
        #so I abandon the repeated titles for this time period (this happens rarely)
        h=0
        if len(reddit_texts1) != len(reddit_comments):
            reddit_texts1=[]
            while h < len(reddit_comments):
                reddit_texts1.append("No Value")
                h=h+1
        
        d=0
        for d in range(len(reddit_comments)):
            reddit_comments[d]=reddit_comments[d].replace("comments","")
        
        e=0
        for e in range(len(reddit_comments)):
            if "k" in reddit_comments[e]:
                reddit_comments[e]=reddit_comments[e].replace(".","")
                reddit_comments[e]=reddit_comments[e].replace("k","")
                reddit_comments[e]=reddit_comments[e].replace(" ","")
                reddit_comments[e]=reddit_comments[e]+"000"
                reddit_comments[e]=(int(reddit_comments[e])/100)
            else:
                reddit_comments[e]=(int(reddit_comments[e])/10)
            
       
        df = pd.DataFrame(
            {"reddit_texts1":reddit_texts1, "reddit_comments":reddit_comments
        })
        df.head()

        
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        #c.execute("CREATE TABLE REDDITTILECOMMENTS11145 (TITLE TEXT, COMMENTS INTEGER);"
        #)



        f=0
        for f in range(len(df)):
            c.execute("INSERT INTO COMPLING1206 VALUES (?,?)", (df["reddit_texts1"][f],df["reddit_comments"][f],))
            conn.commit()
            
    except URLError:
        print("Be patient~let's try again")


# In[19]:


import schedule
import time

schedule.every(10).seconds.do(redditsqlitegogo)

while 1:
    schedule.run_pending()
    time.sleep(1)


# ## Google Blog

# In[31]:


'''scrape articles from GoogleBlog,'''
'''fetch google blog article, enter the next page and fetch the content of the article'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import sqlite3

url = "https://www.blog.google/outreach-initiatives/arts-culture/"
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")

'''scrape the title of the next page (because the connection between the main page's url and the next page's url
is main page's url + names of the titles of the next page)'''

google_text = soup.find_all("h4",class_="uni-blog-nup__header h-has-bottom-margin h-u-font-weight-medium uni-click-tracker")
google_texts = [e.text for e in google_text]

'''lowercase the title of the article and join the "-" to become the part that comes at the very end of a URL'''
a=0
google_url=[]
for a in range(len(google_texts)):
    google_texts[a]=google_texts[a].lower()
    url=google_texts[a].split()
    google_url.append("-".join(url))
    

    

'''connect the main page's url and the next page'''

web="https://www.blog.google/outreach-initiatives/arts-culture/"
b=0
total_url=[]
for b in range(len(google_url)):
    total_url.append(web+google_url[b]+"/")
    
    
'''enter the next page to fetch the content of the article'''  

url = total_url[0]
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")

google_new=soup.find_all("div",class_="rich-text")
google_news=[f.text for f in google_new]

print(google_news)


# ## Twitter BBC

# In[25]:


'''enter the next page to fetch the content of the article'''  

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import sqlite3


url = "https://twitter.com/BBCWorld"
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")

tweet_text = soup.find_all("p",class_="tweet-text")
tweet_texts = [e.text for e in tweet_text]

'''the titles that I scraped have the url and some symbols after the titles, so here I delete them'''

new_tweet=[]
new_tweet2=[]
a=0
for a in range(len(tweet_texts)):
    tweet_texts[a] = tweet_texts[a].replace('"', " ")
    tweet_texts[a] = tweet_texts[a].replace("\n","")
    tweet_texts[a] = tweet_texts[a].replace("#","")
    new_tweet = re.split("https://",tweet_texts[a])
    del new_tweet[len(new_tweet)-1]
    new_tweet2.extend(new_tweet)
    
        
print(tweet_texts)
print(new_tweet2)


# ## BBC News

# In[26]:


'''Scrape titles from BBC news'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import sqlite3

url = "http://www.bbc.co.uk/news"
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")

bbc_text = soup.find_all("a",class_="gs-c-promo-heading")
bbc_texts = [e.text for e in bbc_text]
print(bbc_texts)


# ## Table

# In[27]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

'''Scrape a table(countries) from the wikipedia'''

url = "https://zh.wikipedia.org/zh-tw/ISO_3166-1"
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")

table = soup.find("table", class_="wikitable sortable")

tableheader = [th.text.replace("\n","") for th in table.find_all("th")]

'''find the data of each country'''

trs = table.find_all("tr")[1:]
rows = []
for tr in trs:
    rows.append([td.text.replace("\n","").replace("\xa0","") for td in tr.find_all('td')])

#print(trs)
#print(rows)


df = pd.DataFrame(data=rows, columns=tableheader)
df.head()


# In[ ]:




