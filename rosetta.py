from __future__ import division

import os
import re
import json

docs = []


def load_data(file_name):
    with open(file_name) as f:
        data = f.read()
        # for line in f:
        #     data = line
        #     print repr(data)
        return data

def dump_data(file_name, dic):
    with open('rosetta_clean/%s' % file_name, 'w') as fb:
            json.dump(dic, fb)


def pre_processing(item):
    unique_labels = {}

    if 'ORGANIZATION' in item:
        org_set = set(item['ORGANIZATION'])
        unique_labels['org'] = org_set
    else:
        unique_labels['org'] = set([])

    if 'PERSON' in item:
        per_set = set(item['PERSON'])
        unique_labels['per'] = per_set
    else:
        unique_labels['per'] = set([])

    if 'LOCATION' in item:
        loc_set = set(item['LOCATION'])
        unique_labels['loc'] = loc_set
    else:
        unique_labels['loc'] = set([])

    return unique_labels


def create_tags(doc):
    dic = {}
    re_org = re.compile(".*?ORGANIZATION")
    re_loc = re.compile(".*?LOCATION")
    re_per = re.compile(".*?PERSON")
    org = re_org.findall(doc)
    loc = re_loc.findall(doc)
    per = re_per.findall(doc)

    if per:
        for idx, p in enumerate(per):
            per[idx] = p.replace('PERSON', '')
            per[idx] = per[idx].replace('\t', '')
        dic['PERSON'] = per
    if loc:
        for idx, l in enumerate(loc):
            loc[idx] = l.replace('LOCATION', '')
            loc[idx] = loc[idx].replace('\t', '')
        dic['LOCATION'] = loc
    if org:
        for idx, o in enumerate(org):
            org[idx] = o.replace('ORGANIZATION', '')
            org[idx] = org[idx].replace('\t', '')
        dic['ORGANIZATION'] = org
    return dic


def main(gen):
    raw_tags = os.getcwd() + '/' + gen

    for f in os.listdir(raw_tags):
        generated_label = load_data(raw_tags + '/' + f)
        data_tags = create_tags(generated_label)
        file_name = f[:-4]
        dump_data(file_name, data_tags)

        # for line in generated_label.splitlines():
        #     label_ls = [x for x in line.split('\t')]
        #     if len(label_ls) == 2 and not (label_ls[0] == 'Entity' and label_ls[1]):
        #         pre_processing(label_ls)


if __name__ == "__main__":
    main('rosetta_tags')
