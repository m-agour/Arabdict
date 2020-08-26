import requests
from bs4 import BeautifulSoup
import json
import ast
import sys
import re

inp = 'data.txt'#sys.argv[1]


def cleaning(soup):
    import urllib
    from bs4 import BeautifulSoup

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()
    return text

class StreamArray(list):

    def __init__(self, generator):
        self.generator = generator
        self._len = 1

    def __iter__(self):
        self._len = 0
        for item in self.generator:
            yield item
            self._len += 1

    def __len__(self):
        return self._len

def getbox(word):
 #input("Enter a word: ")
    headers = {
        'User-Agent': '007',
        'From': 'sss'
    }

    url = "https://www.arabdict.com/en/deutsch-arabisch/"+word
    params = {'s':word}
    tra = requests.get(url, headers= headers)


    soup = BeautifulSoup(tra.text, features="html.parser")

    try:
        terms = soup.findAll('ol', {'class': 'rec-list results-items'})
        all = soup.find_all('ol', attrs={'class' : 'rec-list results-items'})

        return all,terms

    except:
        return 'error'
def sim(html):
    similar = []
    for i in cleaning(html[-1]).split('\n\n\n \n'):

        if i == '' or i == ' ':
            continue
        temp = i.split('\n\n\n')
        similar.append([temp[0].replace("\n", "").strip(), temp[1].replace("\n", "").strip()])
    return similar
def verb(html):
    for j in html:
        if cleaning(j).strip()[0:4] == 'Verb':
            verb = []
            print(repr(cleaning(j)))
            for i in cleaning(j)[11:].split('\n\n\n \n'):
                if i == '' or i == ' ':
                    continue
                temp = i.split('\n\n\n')
                verb.append([temp[0].replace("\n", "").strip(), temp[1].replace("\n", "").strip()])
            return verb
def pron(html):
    for j in html.s:
        if cleaning(j)[0:4].strip() == '...' or cleaning(j)[0:5].strip() == 'Noun':
            pron = []
            print(j)
            for i in cleaning(j.split('</span></h5>')[1]).split('\n\n\n \n'):
                if i == '' or i == ' ':
                    continue
                temp = i.split('\n\n\n')
                pron.append([temp[0].replace("\n", "").strip(), temp[1].replace("\n", "").strip()])
            return pron
def ex2(html):
    temp = []
    for i in cleaning(html).split('\n'):
        i = i.strip()
        if i == '' or i == ' 'or i == '...' or i == 'Noun, neutral':
            continue
        else :
            temp.append(i)
    it = iter(temp)
    return list(zip(it, it))

def ad(html):
    for j in html:
        print(cleaning(j)[0:4].strip())
        if cleaning(j)[0:4].strip() == 'Adj' or cleaning(j)[0:4].strip()=='Adv':
            adj = []
            print(repr(cleaning(j)[11:]))
            for i in cleaning(j)[11:].split('\n\n\n \n'):
                if i == '' or i == ' ':
                    continue
                temp = i.split('\n\n\n')
                adj.append([temp[0].replace("\n", "").strip(), temp[1].replace("\n", "").strip()])
            return adj

html = getbox('ich')
all = html[0]
terms = html[1]
upterms = str(all)
print(ex2(terms[0]))
#print((ex2(html)))

#print(repr(getbox('arbeiten').split('\n\n\n \n')))
#def large_list_generator_func():
#    c = 0
#    with open(inp, "r", encoding='utf8') as myfile:
#        for line in myfile.readlines():
#            line = line.replace("\n", "")
#            chunk = {line: getbox(line)}
#            c += 1
#            print(c)
#            yield chunk
#
#
#with open(inp+'.json', 'w') as outfile:
#    large_generator_handle = large_list_generator_func()
#    stream_array = StreamArray(large_generator_handle)
#
#    for chunk in json.JSONEncoder().iterencode(stream_array):
#
#        outfile.write(chunk)