from __future__ import print_function
import semantria
import uuid
import time
import requests
import os
import json


# data_dir = os.getcwd() + '/docs'
data_dir = os.getcwd() + '/n_semantria_labels'
initialTexts = [None] * 947


def load_data_2(file_name):
    with open(file_name) as f:
        dat = json.load(f)
    return dat


def load_data(file_name):
    with open(file_name) as f:
        data2 = f.read()
    return data2


def get_res():
    serializer = semantria.JsonSerializer()
    session = semantria.Session("59e4e96b-f19b-48b5-910a-a2b5d9d2bfc7", "0cee133a-889e-4d1f-9d99-2749677bcfdd",
                                serializer,
                                use_compression=True)

    for fi in os.listdir(data_dir):
        print(fi)
        data = load_data((data_dir + '/%s' % fi))
        # initialTexts.append(data)
        initialTexts[int(fi)] = data

    del initialTexts[0]
    for i, text in enumerate(initialTexts):
        doc = {"id": str(i + 1), "text": text}
        status = session.queueDocument(doc)
        if status == 202:
            print("\"", doc["id"], "\" document queued successfully.", "\r\n")

    length = len(initialTexts)
    results = []

    while len(results) < length:
        print("Retrieving your processed results...", "\r\n")
        time.sleep(2)
        # get processed documents
        status = session.getProcessedDocuments()
        results.extend(status)

    for data in results:
        if "entities" in data:
            print("Entities:", "\r\n")
            if len(data["entities"]) == 20:

                with open('n_semantria_labels/%s' % data["id"] + 'limit', 'w') as fb:
                    json.dump(data["entities"], fb)
            else:
                with open('n_semantria_labels/%s' % data["id"], 'w') as fb:
                    json.dump(data["entities"], fb)


def clean_results():
    for f in os.listdir(data_dir):

        dic = {}
        dic['PERSON'] = []
        dic['LOCATION'] = []
        dic['ORGANIZATION'] = []
        data = load_data_2(data_dir + '/' + f)
        for entity in data:
            if entity["entity_type"] == 'Person':
                dic['PERSON'].append(entity["title"])
            if entity["entity_type"] == 'Place':
                dic['LOCATION'].append(entity["title"])
            if entity["entity_type"] == 'Company':
                dic['ORGANIZATION'].append(entity["title"])

        with open('semantria_clean_labels_2/%d' % int(f), 'w') as fb:
            json.dump(dic, fb)


def main():
    clean_results()
    # get_res()


if __name__ == "__main__":
    main()
