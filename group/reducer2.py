"""
reducer for group
"""
import sys
import operator
import itertools
import traceback
import numpy as np
from sklearn.cluster import DBSCAN
def get_data(lines):
    """
    get data
    """
    for line in lines:
        line = line.strip().split('\t')
       # res = [line[0],int(line[1]),int(line[2])]
        yield line


def getlabel(data, info):
    """
    get group label
    """
    data = np.array(data)
    #x = data[:,1:3].astype(int)
    db = DBSCAN(eps=200, min_samples=1).fit(data)
    labels = db.labels_
    for i in range(0, len(info)):
        info[i].append(str(labels[i]))
        print '\t'.join(info[i])


for ssid, data in itertools.groupby(get_data(sys.stdin), operator.itemgetter(0)):
    try:
        d = []
        info = []
        cnt = 0
        idlist = set([])
        for g in data:
            if len(g) < 5:
                continue
            if g[2] != 'None':
                if g[2] not in idlist:
                    idlist.add(g[2])
                    g.append('-1')
                    print '\t'.join(g)
                    continue
            else:
                cnt += 1
                d.append([int(g[4].split(',')[0]), int(g[4].split(',')[1])])
                info.append(g)
                if cnt >= 2500:
                    getlabel(d, info)
                    info = []
                    d = []
                    cnt = 0
        if len(d) > 0:
            getlabel(d, info)
    except Exception as e:
        sys.stderr.write(str(e) + '\r\n')
