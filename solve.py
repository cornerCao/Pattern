#coding=utf-8
"""
reducer for poi pattern
"""
import traceback
import ctypes
import sys
import numpy as np
import codecs
import itertools
import operator
so = ctypes.cdll.LoadLibrary
lib = so("./suffixarray.so")

class RetRes(ctypes.Structure):
    """
    return value structure
    """
    _fields_ = [("len", ctypes.c_int), ("covernum", ctypes.c_int), ("pos", ctypes.c_int)]


def get_data(lines):
    """
    get data
    """
    for line in lines:
        line = line.strip().split('\t')
        yield line


def getLCS(ssidlist, flag, laststr, labelnum, poiid):
    """
    get logest common string
    """
    strarr = []
    for ssid in ssidlist:
        strarr.append(len(ssid))
        for w in ssid:
            if ord(w) > 0xff00:
                strarr.append(ord('?'))
            else:
                if w >= 'A' and w <= 'Z':
                    w = w.lower()
                strarr.append(ord(w))
    strarr = np.array(strarr, dtype='int32')
    c_func = lib.solve
    c_func.restype = RetRes
    retres = c_func(len(ssidlist), strarr.ctypes.data)
    reslen = retres.len
    covernum = retres.covernum
    idx = retres.pos - 1
    if flag == 2:
        if reslen <= 3:
            return
    if reslen < 2:
        return
    cnt = 0
    resstr = ''
    for ssid in ssidlist:
        if idx >= cnt and idx < cnt + len(ssid):
            idx -= cnt
            for i in range(0, reslen):
                if i + idx < len(ssid):
                    resstr += ssid[i + idx]
            break
        cnt += len(ssid) + 1
    if flag == 2:
        #flag表示找的是第几个最多的公共字符串，当剩下的字符串还有较多的公共子串时，则再调用一次getLCS来获取公共子串
        if resstr in laststr:
            return
    whole = 0
    ssidlist_comple = []
    for ssid in ssidlist:
        whole += 1
        if resstr not in ssid:
            ssidlist_comple.append(ssid)
    print poi + '\t' + resstr.encode('utf-8') + '\t' + str(reslen) + \
    '\t' + str((covernum)) + '\t' + str((whole + labelnum)) + '\t' + \
    str(float((covernum)) / (whole + labelnum))
    if flag == 1:
        if len(ssidlist_comple) >= 3:
            getLCS(ssidlist_comple, 2, resstr, labellist, poiid)
    return


for poi, data in itertools.groupby(get_data(sys.stdin), operator.itemgetter(0)):
    try:
        poicnt = 0
        poiidx = 0
        poilist = []
        labellist = set([])
        poidata = []
        for g in data:
            if g[1] == 'none':
                #说明没有join上poi
                labellist.add(int(g[2]))
            else:
                #join上了poi，于是把poi放到放到poi data中
                poidata.append(g)
        labelnum = len(labellist)
        poiid = ''
        if len(poidata) < 2:
            if len(poidata[0]) < 2:
                continue
            if len(poidata) == 1:
                print poidata[0][0] + '\t' + poidata[0][1] + '\t' + \
                str(len(poidata[0][1].decode('utf-8'))) + '\t1\t1\t1.0\t' + poidata[0][-1]
                continue
        for g in poidata:
            poiidx += 1
            if len(g) < 3:
                continue
            if g[1] == 'none':
                continue
            poicnt += 1
            poiid = g[-1]
            poilist.append(g[1].decode('utf-8'))
            if poiidx == len(poidata) or poicnt >= 2500:
                #内存限制，无法处理超过2500条数据
                if len(poilist) > 0:
                    getLCS(poilist, 1, '', labelnum, poiid)
                poicnt = 0
                poilist = []
    except:
     #   pass
        traceback.print_exc() 
