# Kaitlyn Randolph
# HW3 Part 2
# 3/4/2020

import json
import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def jm(query, doc, coll, lmbd):
    result = 0
    for word in set(query['query'].split()) & set(doc['body'].split()):
        cq = query['query'].count(word)
        cd = doc['body'].count(word)
        found = False
        for line in coll:
            if line['query_num'] == query['query number']:
                if line['id'] == doc['id']:
                    found = True
                    pref = line['position']
            if found:
                break
        if not found:
            pref = 5
        if lmbd != 0:
            result += cq * math.log2(1 + ((1 - lmbd) * cd / (lmbd * pref * len(doc['body'].split()))))
        else:
            result += cq * math.log2(1 + cd)
    return result


def dp(query, doc, coll, mu):
    result = 0
    for word in set(query['query'].split()) & set(doc['body'].split()):
        cq = query['query'].count(word)
        cd = doc['body'].count(word)
        found = False
        for line in coll:
            if line['query_num'] == query['query number']:
                if line['id'] == doc['id']:
                    found = True
                    pref = line['position']
            if found:
                break
        if not found:
            pref = 5
        if mu != 0:
            result += cq * math.log2(1 + (cd / (mu * pref))) - len(query['query'].split()) * math.log2(len(doc['body'].split()) + mu)
        else:
            result += cq * math.log2(cd) - len(query['query'].split()) * math.log2(len(doc['body'].split()) + mu)
    return result




def main():
    jmscore = {}
    dpscore = {}
    with open('Cranfield/cranqrel.json') as rel:
        relList = json.loads(rel.read())
    with open('Cranfield/cran.qry.json') as qry:
        qryList = json.loads(qry.read())
    with open('Cranfield/cranfield_data.json') as docs:
        dataList = json.loads(docs.read())

    perfScore = {}
    avgsets = {}
    # JM
    for lmbdval in [0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        lmbd = lmbdval
        for item in relList:
            jmscore[(item['query_num'], item['id'])] = jm(qryList[int(item['query_num'])-1], dataList[int(item['id'])-1], relList, lmbd)
        count = 0
        avg = 0
        for val in range(1, 256):
            perfScore[(lmbd,val)] = 0
            for k in sorted(jmscore, key=jmscore.get, reverse=True):
                if int(k[0]) == val:
                    perfScore[(lmbd,val)] += jmscore[k]
                    count += 1
                    if count == 5:
                        perfScore[(lmbd,val)] /= 5
                        print(val, perfScore[(lmbd,val)])
                        avg += perfScore[(lmbd,val)]
                        count = 0
                        break
        avg /= 255
        avgsets[lmbd] = avg
        print("Average Performance Score: ", avg)
        plt.hist(list(perfScore.values()), bins=[0,1,2,3,4,5])
        plt.savefig('jmgraph' + str(lmbd) + '.png')
        plt.clf()
    plt.plot(list(avgsets.keys()), list(avgsets.values()))
    plt.savefig('jmlineplot.png')

    #DP
    for muval in [0, 100, 500, 1000, 2000, 4000, 8000, 10000]:
        mu = muval
        for item in relList:
            dpscore[(item['query_num'], item['id'])] = dp(qryList[int(item['query_num'])-1], dataList[int(item['id'])-1], relList, mu)
        count = 0
        avg = 0
        for val in range(1, 256):
            perfScore[(mu,val)] = 0
            for k in sorted(jmscore, key=jmscore.get, reverse=True):
                if int(k[0]) == val:
                    perfScore[(mu,val)] += dpscore[k]
                    count += 1
                    if count == 5:
                        perfScore[(mu,val)] /= 5
                        print(val, perfScore[(mu,val)])
                        avg += perfScore[(mu,val)]
                        count = 0
                        break
        avg /= 255
        avgsets[mu] = avg
        print("Average Performance Score: ", avg)
        plt.hist(list(perfScore.values()), bins=[0,1,2,3,4,5])
        plt.savefig('dpgraph' + str(mu) + '.png')
        plt.clf()
    plt.plot(list(avgsets.keys()), list(avgsets.values()))
    plt.savefig('dplineplot.png')


main()

