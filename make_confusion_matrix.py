from __future__ import division
import sys
import json
import collections
import cli.app
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from tabulate import tabulate
import json

ner_res = [

    {u'ORGANIZATION': [u'Red Bull', u'Red Bull', u'Red Bull', u'McLaren', u'McLarens', u'McLaren', u'Red Bull',
                       u'Ferrari', u'McLaren', u'McLarens', u'Vettel', u'Button', u'McLarens', u'Red Bull',
                       u'Ferrari',
                       u'Red Bull', u'McLaren', u'Ferrari', u'McLaren', u'McLaren', u'Monaco', u'McLaren',
                       u'Red Bull',
                       u'Red Bull', u'Spa', u'Ferrari or McLaren', u'McLaren', u'Ferrari', u'Ferrari', u'Ferrari'],
     u'MISC': [u'German', u'Button'],
     u'LOCATION': [u'Hungary', u'Nurburgring', u'Hungaroring', u'Germany', u'Hungary', u'Germany', u'Hungary',
                   u'Germany', u'Valencia', u'Spain', u'Nurburgring', u'Monza', u'Singapore', u'Japan', u'Korea',
                   u'India', u'Brazil', u'Suzuka', u'Suzuka'],
     u'PERSON': [u'Mark HughesBBC', u'Bull', u'Sebastian Vettel', u'Mark Webber', u'Jenson', u'Webber', u'Jenson',
                 u'Jaguar', u'Jenson', u'Lewis Hamilton', u'Hamilton', u'Vettel', u'Vettel', u'Hamilton', u'Button',
                 u'Vettel', u'Vettel', u'Silverstone', u'Pat Fry', u'Silverstone', u'Christian Horner',
                 u'Paddy Lowe',
                 u'Abu Dhabi', u'Vettel']}
    ,
    {u'ORGANIZATION': [u'Toyota', u'disruptionToyota Motor', u'Toyota', u'Toyota', u'Toyota', u'Toyota',
                       u'Toyota Motor'], u'LOCATION': [u'Japan', u'Japan', u'US', u'Japan'],
     u'PERSON': [u'Takahiko Ijichi']},

    {u'ORGANIZATION': [u'Lancet', u'British Heart Foundation', u'University of Birmingham',
                       u'UK National Screening Committee', u'British Heart Foundation',
                       u'Emory University School of Medicine', u"Cohen Children's Medical Center"],
     u'LOCATION': [u'UK', u'UK', u'US', u'Atlanta', u'New York'],
     u'PERSON': [u'Andrew Ewer', u'David Elliman', u'Amy Thompson', u'William Mahle', u'Robert Koppel']},

    {u'ORGANIZATION': [u'Nashville', u'SautoyYou'],
     u'LOCATION': [u'Tennessee', u'Nashville', u'North America', u'America', u'North America', u'Tennessee'],
     u'PERSON': [u'Marcus']},

    {u'ORGANIZATION': [u'Congress', u'Congress', u'House of Representatives', u'Senate', u'BBC', u'House',
                       u'Democratic House', u'Republican Tea Party', u'Republican House', u'New Congressional',
                       u'NovemberImage', u'Congress', u'Congress', u'House of Representatives', u'Senate'],
     u'MISC': [u'Republican', u'Democratic', u'Republicans', u'Democrats', u'Republicans', u'Democratic', u'Democrats',
               u'Democrats', u'Republicans', u'Republicans', u'Democrats'],
     u'LOCATION': [u'US', u'US', u'US', u'US', u'US', u'US', u'US', u'US', u'Washington', u'Tokyo', u'London',
                   u'Paris', u'US', u'Japan'],
     u'PERSON': [u'Obama', u"Jane O'Brienbbc News", u'Barack Obama', u"Jane O'Brien", u'Nancy Pelosi', u'Obama',
                 u'Obama', u'Yukio Edano', u'John Boehner', u'Obama', u'Boehner']},

    {u'ORGANIZATION': [u'Syrians Strike Restive Cities', u'Local Coordination Committees'],
     u'MISC': [u'Syrian', u'American', u'European', u'Syrian', u'Syrian', u'Syrian', u'Syrian', u'Syrian', u'Syrian',
               u'Islamist', u'Internet'],
     u'LOCATION': [u'Lebanon', u'Ramadan', u'Hama', u'United States', u'Hama', u'Libya', u'United States', u'Hama',
                   u'Hama', u'Hama', u'Syria', u'Syria', u'Syria', u'Hama'],
     u'PERSON': [u'Raidsby Nada Bakri', u'Anthony Shadid', u'Hama', u'Bashar al-Assad', u'Deir al-Zour', u'Assad',
                 u'Obama', u'Assad', u'Muammar el-Qaddafi', u'Assad', u'Obama', u'Assad', u'Deir al-Zour',
                 u'Omar Habbal', u'Hama', u'Hama', u'Assad', u'Hafez', u'Obada Arwany']},

    {u'ORGANIZATION': [u'Focus Turns Back', u'Fed', u'Congress', u'Federal Reserve', u'Senate', u'House', u'Congress',
                       u'Federal Reserve', u'Fed', u'Fed', u'Mesirow Financial', u'Fed', u'Treasuries', u'Fed',
                       u'Treasury', u'Fed', u'Fed', u'Federal Reserve Bank of Richmond', u'Fed', u'Fed', u'Congress',
                       u'Congress', u'Standard & Poor', u'Treasury', u'Fed', u'Fed', u'Treasuries',
                       u'Chase and Bank of New York', u'Princeton', u'Treasury', u'Fed', u'Treasury',
                       u'Brookings Institution'], u'MISC': [u'American', u'American', u'American'],
     u'LOCATION': [u'U.S.', u'New York', u'China', u'China', u'U.S.'],
     u'PERSON': [u'Binyamin Appelbaum', u'Catherine Rampell', u'S. Bernanke', u'Diane Swonk', u'Bernanke',
                 u'Jeffrey M. Lacker', u'Bernanke', u'Obama', u'Donald L. Kohn', u'Alan Blinder', u'Blinder',
                 u'Kohn']},
    {
        u'ORGANIZATION': [u'Associated Press', u'Rutgers', u'Atlantic Coast Conference', u'ESPN',
                          u'NBC Sports and Versus',
                          u'Fox Sports', u'ESPN', u'ESPN', u'ESPN', u'ESPN', u'Comcast', u'NBC', u'Longhorn Network',
                          u'South Florida Coach Skip Holtz'],
        u'MISC': [u'East Is Still Big Deal', u'Bowl Championship Series', u'Rose Bowl', u'Texas Christian', u'A-list',
                  u'Cadillac', u'Big East', u'Big East'],
        u'LOCATION': [u'Big East', u'Rutgers', u'Big East', u'Newport', u'ESPN', u'Big East', u'Big East', u'Sanu',
                      u'Big East', u'Big East', u'Big East', u'Big East', u'Big East', u'Big East', u'Big East',
                      u'Big East', u'Big East', u'Central Florida', u'Kansas', u'Kansas State', u'Missouri',
                      u'Big East',
                      u'Big East', u'Big East'],
        u'PERSON': [u'Pete Thamel', u'Greg Schiano', u'Fox', u'John Marinatto', u'Fox', u'Marinatto', u'Marinatto',
                    u'Jon Miller', u'Larry Jones', u'Burke', u'Marinatto', u'Marinatto', u'Marinatto', u'Dave Gavitt',
                    u'Mike Tranghese', u'Marinatto', u'Marinatto', u'Magnus', u'Nick Carparelli', u'Tom Odjakjian',
                    u'Schiano']},
    {u'ORGANIZATION': [u'Medtronic Giving Yale Grant', u'Review Infuse Researchby Barry Meier', u'Medtronic', u'Yale',
                       u'Medtronic', u'Infuse', u'The Spine Journal', u'Medtronic', u'Spine Journal', u'Yale',
                       u'Medtronic', u'Yale', u'Medtronic', u'The Spine Journal', u'Medtronic', u'Yale', u'Medtronic',
                       u'Food and Drug', u'Spine Journal', u'Justice Department', u'Medtronic', u'Senate'],
     u'MISC': [u'Infuse-related', u'Infuse', u'Infuse'],
     u'LOCATION': [u'Infuse', u'United States', u'Stanford', u'Infuse'],
     u'PERSON': [u'Harlan Krumholz', u'Krumholz', u'Eugene Carragee', u'Carragee']},
    {u'ORGANIZATION': [u'ExxonMobil', u'Environmental Protection Agency', u'E.P.A.', u'American Petroleum Institute',
                       u'Kaiser Exploration and Mining Company', u'Congress'],
     u'LOCATION': [u'Jackson County', u'Kaiser', u'Texas'],
     u'PERSON': [u'IAN URBINAAUG', u'Rex W. Tillerson', u'Carla Greathouse', u'Eric Wohlschlegel', u'Wohlschlegel',
                 u'James Parsons', u'Parson', u'James Parson', u'Parson', u'Parson', u'Mr. Wohlschlegel', u'Parsons',
                 u'Wohlschlegel', u'Parsons']}
]


def load_data(file):
    with open(file) as f:
        data = json.load(f)
        return data


def get_tags(file):
    data = load_data(file)
    total_tags = []

    for story in data:
        person = []
        location = []
        organization = []
        miscellaneous = []
        no_ent = []

        for item in story:
            if item["FIELD3"] == "PER":
                person.append(item["FIELD2"])
            elif item["FIELD3"] == "LOC":
                location.append(item["FIELD2"])
            elif item["FIELD3"] == "ORG":
                organization.append(item["FIELD2"])
            elif item["FIELD3"] == "MISC":
                miscellaneous.append(item["FIELD2"])
            else:
                no_ent.append(item["FIELD2"])

        total_tags.append({'PER': person, 'LOC': location, "ORG": organization, "MISC": miscellaneous, 'O': no_ent})

    # if story["FIELD1"] == "http://news.bbc.co.uk/sport2/hi/formula_one/14363956.stm":
    #
    #         if story["FIELD3"] == "PER":
    #             person.append(story["FIELD2"])
    #         elif story["FIELD3"] == "LOC":
    #             location.append(story["FIELD2"])
    #         elif story["FIELD3"] == "ORG":
    #             organization.append(story["FIELD2"])
    #         elif story["FIELD3"] == "MISC":
    #             miscellaneous.append(story["FIELD2"])
    #         else:
    #             no_ent.append(story["FIELD2"])
    #
    return total_tags


def evaluate_results(correct_labels, generated_labels, s):
    e = correct_labels  # e represents the true entity resolution result
    m = generated_labels  # m represents the matching results
    # print e
    # print m
    true_positive = m.intersection(e)
    false_positive = m.difference(e)
    false_negative = e.difference(m)
    true_negative = s.difference(e.union(m))

    # print "True positive:", true_positive, len(true_positive)
    # print "False positive:", false_positive, len(false_positive)
    # print "False negative:", false_negative, len(false_negative)
    # print "True negative:", true_negative, len(true_negative)

    return {'tp': true_positive, 'fp': false_positive, 'fn': false_negative, 'tn': true_negative}


def evaluate_microavg(measurements):
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

    # print "Precision is TP/(TP+FP):", precision
    # print "Recall is TP/(TP+FN):", recall
    # print "The F-Measure is (2*Precision*Recall)/(Precision+Recall):", f

    results = [recall, precision, f]

    return results


def data_cleaning(ner_results):
    # print "Cleaning data..."
    # print "Organization size:", len(ner_results[u'ORGANIZATION'])
    # print "Person size:", len(ner_results[u'PERSON'])
    # print "Location size:", len(ner_results[u'LOCATION'])
    # print "Miscellaneous size:", len(ner_results[u'MISC'])
    generated_labels_ls = []
    for item in ner_results:

        org_set = set(item[u'ORGANIZATION'])
        per_set = set(item[u'PERSON'])
        loc_set = set(item[u'LOCATION'])
        if u'MISC' in item:
            misc_set = set(item[u'MISC'])
        else:
            misc_set = set()
        generated_labels_ls.append({'org': org_set, 'per': per_set, 'loc': loc_set, 'misc': misc_set})
    # print "---------"
    # print "Set organization size:", len(org_set)
    # print "Set person size:", len(per_set)
    # print "Set location size:", len(loc_set)
    # print "Set miscellaneous size:", len(misc_set)

    return generated_labels_ls


def get_f_measure(measurements):
    if (len(measurements['tp']) + len(measurements['fp'])) != 0:

        precision = len(measurements['tp']) / (len(measurements['tp']) + len(measurements['fp']))
    else:
        precision = 0

    if (len(measurements['tp']) + len(measurements['fn'])) != 0:
        recall = len(measurements['tp']) / (len(measurements['tp']) + len(measurements['fn']))
    else:
        recall = 0

    if (precision + recall) != 0:
        f = 2 * precision * recall / (precision + recall)
    else:
        f = 0

    # print "Precision is TP/(TP+FP):", precision
    # print "Recall is TP/(TP+FN):", recall
    # print "The F-Measure is (2*Precision*Recall)/(Precision+Recall):", f

    results = [recall, precision, f]

    return results


def main(file_name):
    generated_labels_list = []
    correct_labels_list = []
    correct_labels_list = get_tags(file_name)
    s = set()
    per_total_stat = {'ttp': 0, 'tfp': 0, 'tfn': 0, 'ttn': 0}
    org_total_stat = {'ttp': 0, 'tfp': 0, 'tfn': 0, 'ttn': 0}
    loc_total_stat = {'ttp': 0, 'tfp': 0, 'tfn': 0, 'ttn': 0}
    misc_total_stat = {'ttp': 0, 'tfp': 0, 'tfn': 0, 'ttn': 0}
    generated_labels_list = data_cleaning(ner_res)

    for i in range(10):
        s = set()
        s.update(generated_labels_list[i]['per'], generated_labels_list[i]['org'], generated_labels_list[i]['loc'],
                 generated_labels_list[i]['misc'])
        headers = ["Recall", "Precision", "F1"]

        # F1 measure for Person
        print "Person Statistical measures"
        statistical_measures = evaluate_results(generated_labels_list[i]['per'], set(correct_labels_list[i]['PER']), s)
        per_total_stat['ttp'] += len(statistical_measures['tp'])
        per_total_stat['tfp'] += len(statistical_measures['fp'])
        per_total_stat['tfn'] += len(statistical_measures['fn'])
        per_total_stat['ttn'] += len(statistical_measures['tn'])
        table = [get_f_measure(statistical_measures)]
        print ""
        print tabulate(table, headers)
        print ""

        # F1 measure for Organization
        print "Organization statistical measures"
        statistical_measures = evaluate_results(generated_labels_list[i]['org'], set(correct_labels_list[i]['ORG']), s)
        org_total_stat['ttp'] += len(statistical_measures['tp'])
        org_total_stat['tfp'] += len(statistical_measures['fp'])
        org_total_stat['tfn'] += len(statistical_measures['fn'])
        org_total_stat['ttn'] += len(statistical_measures['tn'])
        table = [get_f_measure(statistical_measures)]
        print tabulate(table, headers)
        print ""

        # F1 measure for Location
        print "Location statistical measures"
        statistical_measures = evaluate_results(generated_labels_list[i]['loc'], set(correct_labels_list[i]['LOC']), s)
        loc_total_stat['ttp'] += len(statistical_measures['tp'])
        loc_total_stat['tfp'] += len(statistical_measures['fp'])
        loc_total_stat['tfn'] += len(statistical_measures['fn'])
        loc_total_stat['ttn'] += len(statistical_measures['tn'])
        table = [get_f_measure(statistical_measures)]
        print tabulate(table, headers)
        print ""

        # F1 measure for Misc
        print "Misc statistical measures"
        statistical_measures = evaluate_results(generated_labels_list[i]['misc'],
                                                set(correct_labels_list[i]['MISC']), s)
        misc_total_stat['ttp'] += len(statistical_measures['tp'])
        misc_total_stat['tfp'] += len(statistical_measures['fp'])
        misc_total_stat['tfn'] += len(statistical_measures['fn'])
        misc_total_stat['ttn'] += len(statistical_measures['tn'])
        table = [get_f_measure(statistical_measures)]

        print tabulate(table, headers)
        print ""

        print evaluate_microavg(per_total_stat)
        print evaluate_microavg(org_total_stat)
        print evaluate_microavg(loc_total_stat)
        print evaluate_microavg(misc_total_stat)
        print ""
        print 'Macroaveraged'
        print [(x + y + z + t) / 4 for x, y, z, t in zip(evaluate_microavg(per_total_stat),
                                                         evaluate_microavg(org_total_stat),
                                                         evaluate_microavg(loc_total_stat),
                                                         evaluate_microavg(misc_total_stat))]

        mic = {
            'tfn': per_total_stat['tfn'] + org_total_stat['tfn'] + loc_total_stat['tfn'] + misc_total_stat['tfn'],
            'ttp': per_total_stat['ttp'] + org_total_stat['ttp'] + loc_total_stat['ttp'] + misc_total_stat['ttp'],
            'tfp': per_total_stat['tfp'] + org_total_stat['tfp'] + loc_total_stat['tfp'] + misc_total_stat['tfp'],
            'ttn': per_total_stat['ttn'] + org_total_stat['ttn'] + loc_total_stat['ttn'] + misc_total_stat['ttn']}
        print ''
        print 'Microaveraged'
        print evaluate_microavg(mic)
        print ''


if __name__ == "__main__":
    main('newgold.json')
