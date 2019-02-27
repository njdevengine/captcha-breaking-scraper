import requests
import pandas as pd
import re

with requests.Session() as s:
    url = "search page of the site to visit"
    headers = {"user-agent" : "your browser headers"}
    r = s.get(url, headers=headers)
soup = []
for i in r:
    i = i.decode("utf-8") 
    soup.append(i)

soup = "".join(soup)

captcha_base = "the static part of the captcha image url"
num = soup.find('src="')+5
finnum = soup[num:].find('"')
captcha = (soup[num:num+finnum])
captcha_url = captcha_base + captcha

#this part retrieves a dynamic key from the starting search page
num2 = soup.find('name="dynamic_key"')+20
finnum2 = soup[num2:].find('">')
pkey = (soup[num2:num2+finnum2])

print(captcha_url)
code = input(" whats the captcha? ")

queries = ["put","your","query","terms","here"]

table = {}
for i in queries:
    try:
        search_data = {
        "query goes here" : i,
        "query options can go here" : "PARTIAL",
        "captcha can go here" : code,
        "dynamic key can go here" : pkey,
        "something static can go here" : 1
        }
        url2 = "the post url goes here"
        r = s.post(url2, data =search_data, headers=headers)
        print(i)
        result = r.content.decode("utf-8")
        start = result.find('query returns ')+14
        fin = result[start:].find(' names')
        count = int(result[start:start+fin])
        table[i] = count
    except:
        print(i+ " error")
        
out = pd.Series(table, name='retrieved_data')
out.index.name = 'query_term'
out.reset_index()
out.to_csv('file_output.csv')
