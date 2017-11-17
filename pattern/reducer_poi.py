"""
reducer for ssid pattern
"""
import traceback
import ctypes
import sys
import codecs
import itertools
import operator
#so = ctypes.cdll.LoadLibrary
#lib = so("./suffixarray.so")
def get_data(lines):
    """
    get data
    """
    for line in lines:
        line = line.strip().split('\t')
        yield line

for poi, data in itertools.groupby(get_data(sys.stdin), operator.itemgetter(0)):
    try:
        ssid = {}
        whole = 0
        poiid = ''
        for g in data:
            poiid = g[-1]
            whole += int(g[2])
            if g[1] not in ssid:
                ssid[g[1]] = int(g[2])
            else:
                ssid[g[1]] += int(g[2])
        ssid = sorted(ssid.items(), key = lambda d:d[1], reverse = True)
        for s in ssid:
            print('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (poi, s[0], str(len(s[0].decode('utf-8'))), \
                str(s[1]), str(whole), str(float(s[1]) / whole), poiid))
    except:
       # pass
        traceback.print_exc() 
