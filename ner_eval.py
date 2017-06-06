from __future__ import division
import sys
import json
import collections
import cli.app
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from tabulate import tabulate
import re
import json
import os


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


def get_measures(correct_labels, generated_labels, s):
    e = correct_labels  # e represents the true entity resolution result
    m = generated_labels  # m represents the matching results

    true_positive = m.intersection(e)
    false_positive = m.difference(e)
    false_negative = e.difference(m)
    true_negative = s.difference(e.union(m))
    return {'tp': true_positive, 'fp': false_positive, 'fn': false_negative, 'tn': true_negative}


def get_metrics(measurements):
    if (measurements['ttp'] + measurements['tfp']) != 0:

        precision = measurements['ttp'] / (measurements['ttp'] + measurements['tfp'])
    else:
        precision = 0

    if (measurements['ttp'] + measurements['tfn']) != 0:
        recall = measurements['ttp'] / (measurements['ttp'] + measurements['tfn'])
    else:
        recall = 0

    if (precision + recall) != 0:
        f = 2 * precision * recall / (precision + recall)
    else:
        f = 0

    results = [recall, precision, f]

    return results


def main(gen, cor):
    entity_type = ['per', 'org', 'loc']
    gen_dataset_tags = [None] * 947
    cor_dataset_tags = [None] * 947
    headers = ["Recall", "Precision", "F1"]
    gen_dir = os.getcwd() + '/' + gen
    cor_dir = os.getcwd() + '/' + cor

    total_stat = {
        'per': {'ttp': 0, 'tfp': 0, 'tfn': 0, 'ttn': 0},
        'org': {'ttp': 0, 'tfp': 0, 'tfn': 0, 'ttn': 0},
        'loc': {'ttp': 0, 'tfp': 0, 'tfn': 0, 'ttn': 0}
    }

    for f in os.listdir(gen_dir):
        generated_label = load_data(gen_dir + '/' + f)
        gen_dataset_tags[int(f)] = pre_processing(generated_label)
    del gen_dataset_tags[0]

    for f in os.listdir(cor_dir):
        correct_label = load_data(cor_dir + '/' + f)
        cor_dataset_tags[int(f)] = pre_processing(correct_label)
    del cor_dataset_tags[0]

    for i in range(946):

        if gen_dataset_tags[i] is not None:

            s = pre_measuring(gen_dataset_tags[i])
            for t in entity_type:
                print i, t
                print '----'
                print gen_dataset_tags[i][t], cor_dataset_tags[i][t]

                statistical_measures = get_measures(cor_dataset_tags[i][t], gen_dataset_tags[i][t], s)
                print statistical_measures
                total_stat[t]['ttp'] += len(statistical_measures['tp'])
                total_stat[t]['tfp'] += len(statistical_measures['fp'])
                total_stat[t]['tfn'] += len(statistical_measures['fn'])
                total_stat[t]['ttn'] += len(statistical_measures['tn'])

    for t in entity_type:
        print t
        print total_stat[t]

        table = [get_metrics(total_stat[t])]
        print tabulate(table, headers)



if __name__ == "__main__":
    main('stanford_entities', 'conll_gold')
    #main('semantria_entities', 'conll_gold')
    # main('rosetta_entities', 'correct_labels')
    # main('ie_crf_entities', 'conll_gold')
