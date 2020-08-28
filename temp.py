import requests
from bs4 import BeautifulSoup
import json
import ast
import sys

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
        final = soup.find_all('div', attrs={'class' : 'col col-xs-12 col-sm-12 col-md-8 comments search-results border-style white p-t-20'})[-1]

        return (cleaning(final))

    except:
        return 'error'
lst = []
for i in getbox('arbeiten').split('\n'):
    if i != ' ' and i != '':
        lst.append(i)
print(lst)
#    except:
#        ...
#    try:
#        final2 = (tra.text.split("var c1Arr = new Array")[1]).split(';\nvar c2Arr')[0]
#        lst1 = ast.literal_eval(final2.replace('(','[').replace(")",']'))[1:]
#
#        final3 = (tra.text.split("var c2Arr = new Array")[1]).split(';')[0]
#        lst2 = ast.literal_eval(final3.replace('(','[').replace(")",']'))[1:]
#
#        final4 = dict(zip(lst1, lst2))
#        return [text, final4]
#    except:
#        return 'error'
#
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