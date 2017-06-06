from __future__ import division
import sys
import json
import collections
import cli.app
from sklearn.metrics import confusion_matrix

from tabulate import tabulate
import re
import json
import os
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt


def load_data(file_name):
    with open(file_name) as f:
        data = json.load(f)
        return data


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


def pre_measuring(ger_doc):
    s = set()
    s.update(ger_doc['per'], ger_doc['org'], ger_doc['loc'])
    return s


def conf(generated_labels, correct_labels, s):
    e = correct_labels  # e represents the true entity resolution result
    m = generated_labels  # m represents the matching results

    true_positive = m.intersection(e)
    false_positive = m.difference(e)
    false_negative = e.difference(m)
    true_negative = s.difference(e.union(m))
    return {'tp': true_positive, 'fp': false_positive, 'fn': false_negative, 'tn': true_negative}


def get_accuracy(y_true, y_pred):
    y_pred = list(y_pred)
    y_true = list(y_true)

    return f1_score(y_true, y_pred, average='binary')


def get_metrics(measurements):

    if (measurements['tp'] + measurements['fp']) != 0:

        precision = measurements['tp'] / (measurements['tp'] + measurements['fp'])

    else:
        precision = 0

    if (measurements['tp'] + measurements['fn']) != 0:
        recall = measurements['tp'] / (measurements['tp'] + measurements['fn'])
    else:
        recall = 0

    if (precision + recall) != 0:
        f = 2 * precision * recall / (precision + recall)
    else:
        f = 0

    results = [recall, precision, f]

    return results


def main(gen, cor):
    gen_dir = os.getcwd() + '/' + gen
    cor_dir = os.getcwd() + '/' + cor

    generated_label_ls = [None] * 11
    correct_label_ls = [None] * 11

    stat = {
        'per': {'tp': 0, 'fp': 0, 'fn': 0, 'tn': 0}}

    for f in os.listdir(gen_dir):
        generated_label = load_data(gen_dir + '/' + f)
        generated_label_ls[int(f)] = pre_processing(generated_label)

    for f in os.listdir(cor_dir):
        correct_label = load_data(cor_dir + '/' + f)
        correct_label_ls[int(f)] = pre_processing(correct_label)

    s = pre_measuring(generated_label_ls[3])  # print generated_label_ls[1]
    statistical_measures = conf(generated_label_ls[3]['per'], correct_label_ls[3]['per'], s)
    print "tp", len(statistical_measures['tp'])
    print "fp", len(statistical_measures['fp'])
    print "fn", len(statistical_measures['fn'])
    print "tn", len(statistical_measures['tn'])

    stat['per']['tp'] = len(statistical_measures['tp'])
    stat['per']['fp'] = len(statistical_measures['fp'])
    stat['per']['fn'] = len(statistical_measures['fn'])
    stat['per']['tn'] = len(statistical_measures['tn'])

    print get_metrics(stat['per'])
    print list(generated_label_ls[3]['per'])
    print ""
    print list(correct_label_ls[3]['per'])
    print get_accuracy(correct_label_ls[3]['per'], generated_label_ls[3]['per'])
    cm = confusion_matrix(list(correct_label_ls[1]['per']), list(generated_label_ls[1]['per']))
    print(cm)
    plt.matshow(cm)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

if __name__ == "__main__":
    main('stanford_labels', 'gold_labels')
