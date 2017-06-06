__author__ = 'shadowtrader'
import json
from bs4 import BeautifulSoup
import re


docs = []

def load_data(file_name):
    doc = str()
    with open(file_name) as f:
        for l in f:
            if '<DOCUMENT>' in l.strip():
                doc += ''
            elif '</DOCUMENT>' in l.strip():
                doc += ''
                docs.append(doc)
                doc = ''
            else:
                doc += l
    return docs

def create_no_tags_doc(ls_docs):
    counter = 0
    for doc in ls_docs:
        counter += 1
        rep = ['<PERSON>', '</PERSON>', '<LOCATION>', '</LOCATION>', '<ORGANIZATION>', '</ORGANIZATION>', '<S>',
               '</S>']
        for i in rep:
            doc = doc.replace(i, '')

        with open('docs/%d' % counter, 'w') as fb:
            fb.write(doc)

def create_tags(ls_docs):
    counter = 0
    for doc in ls_docs:
        dic = {}
        counter += 1
        re_org = re.compile("<ORGANIZATION>.*?</ORGANIZATION>")
        re_loc = re.compile("<LOCATION>.*?</LOCATION>")
        re_per = re.compile("<PERSON>.*?</PERSON>")
        org = re_org.findall(doc)
        loc = re_loc.findall(doc)
        per = re_per.findall(doc)

        if per:
            for idx, p in enumerate(per):
                per[idx] = p.replace('<PERSON>', '')
                per[idx] = per[idx].replace('</PERSON>', '')
            dic['PERSON'] = per
        if loc:
            for idx, l in enumerate(loc):
                loc[idx] = l.replace('<LOCATION>', '')
                loc[idx] = loc[idx].replace('</LOCATION>', '')
            dic['LOCATION'] = loc
        if org:
            for idx, o in enumerate(org):
                org[idx] = o.replace('<ORGANIZATION>', '')
                org[idx] = org[idx].replace('</ORGANIZATION>', '')
            dic['ORGANIZATION'] = org

        with open('correct_labels/%d' % counter, 'w') as fb:
            json.dump(dic, fb)


data = load_data('conll.txt')

create_tags(data)
