import requests
from bs4 import BeautifulSoup
import json
import ast
import sys
import re

none = open('exceptions', 'r')
none = json.load(none)

inp = "data.txt"  # sys.argv[1]


def cleaning(soup):
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
    # input("Enter a word: ")
    headers = {"User-Agent": "007", "From": "sss"}

    url = "https://www.arabdict.com/en/deutsch-arabisch/" + word
    params = {"s": word}
    tra = requests.get(url, headers=headers)

    soup = BeautifulSoup(tra.text, features="html.parser")

    try:
        terms = soup.findAll("ol", {"class": "rec-list results-items"})
        all = soup.find_all("ol", attrs={"class": "rec-list results-items"})

        return all, terms
    except:
        return "error"


def sim(html):
    similar = []
    for i in cleaning(html[-1]).split("\n\n\n \n"):

        if i == "" or i == " ":
            continue
        temp = i.split("\n\n\n")
        similar.append(
            [temp[0].replace("\n", "").strip(), temp[1].replace("\n", "").strip()]
        )
    return similar


def verb(html):
    for j in html:
        if cleaning(j).strip()[0:4] == "Verb":
            verb = []
            print(repr(cleaning(j)))
            for i in cleaning(j)[11:].split("\n\n\n \n"):
                if i == "" or i == " ":
                    continue
                temp = i.split("\n\n\n")
                verb.append(
                    [
                        temp[0].replace("\n", "").strip(),
                        temp[1].replace("\n", "").strip(),
                    ]
                )
            return verb


def pron(html):
    for j in html.s:
        if cleaning(j)[0:4].strip() == "..." or cleaning(j)[0:5].strip() == "Noun":
            pron = []
            print(j)
            for i in cleaning(j.split("</span></h5>")[1]).split("\n\n\n \n"):
                if i == "" or i == " ":
                    continue
                temp = i.split("\n\n\n")
                pron.append(
                    [
                        temp[0].replace("\n", "").strip(),
                        temp[1].replace("\n", "").strip(),
                    ]
                )
            return pron


def ex1(terms):
    try:
        html = terms[0]
        temp = []
        for i in cleaning(html).split("\n"):
            i = i.strip()
            if i in none :
                continue
            else:
                temp.append(i)
        it = iter(temp)
        it = list(zip(it, it))
        temp = []
        for i in it:
            op = []
            if len(i[0].split("(", 1)) > 1:
                op = i[0].split("(", 1)
                op[1] = "(" + op[1]
            elif len(i[0].split("[", 1)) > 1:
                op = i[0].split("[", 1)
                op[1] = "[" + op[1]
            else:
                op = [i[0], ""]
            temp.append([op[0].strip(), i[1].strip(), op[1].strip()])
        return temp
    except:
        return None


def ad(html):
    for j in html:
        print(cleaning(j)[0:4].strip())
        if cleaning(j)[0:4].strip() == "Adj" or cleaning(j)[0:4].strip() == "Adv":
            adj = []
            print(repr(cleaning(j)[11:]))
            for i in cleaning(j)[11:].split("\n\n\n \n"):
                if i == "" or i == " ":
                    continue
                temp = i.split("\n\n\n")
                adj.append(
                    [
                        temp[0].replace("\n", "").strip(),
                        temp[1].replace("\n", "").strip(),
                    ]
                )
            return adj


def ex2(terms):
    try:
        html = terms[1]
        temp = []
        for i in cleaning(html).split("\n"):
            i = i.strip()
            if i in none:
                continue
            else:
                temp.append(i)
        it = iter(temp)
        it = list(zip(it, it))
        temp = []
        for i in it:
            op = []
            if len(i[0].split("(", 1)) > 1:
                op = i[0].split("(", 1)
                op[1] = "(" + op[1]
            elif len(i[0].split("[", 1)) > 1:
                op = i[0].split("[", 1)
                op[1] = "[" + op[1]
            else:
                op = [i[0], ""]
            temp.append([[op[0].strip(), i[1].strip(), op[1].strip()]])
        return temp
    except:
        return None


def final(word):
    html = getbox(word)
    terms = html[1]
    main = ex1(terms)
    similar = ex2(terms)
    if similar == None:
        return {"main": similar, "similar": main}
    else:
        return {"main": main, "similar": similar}

# print(ex1(terms))



def large_list_generator_func():
    c = 0
    with open(inp, "r", encoding='utf8') as myfile:
        for line in myfile.readlines():
            line = line.replace("\n", "")
            temp = final(line)
            chunk = {line: temp}
            c += 1
            if c%1000 == 0:
                print(temp)
            yield chunk
#
#
with open(inp+'.json', 'w') as outfile:
    large_generator_handle = large_list_generator_func()
    stream_array = StreamArray(large_generator_handle)
    for chunk in json.JSONEncoder().iterencode(stream_array):
        outfile.write(chunk)
