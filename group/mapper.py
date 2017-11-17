#coding = utf-8
"""
mapper for group
"""
import sys
import re
import ssid as ss
pat_kuohao = re.compile("\(.*\)")
pat_kuohao2 = re.compile("\（.*\）")
for line in sys.stdin:
    line = line.strip().split('\t')
    sid, res = ss.normal_ssid(line[1])
    ssid = line[1]
    if res == True:
        ssid = sid
    if res == False:
        continue
    if ssid == '':
        continue
    if '$' in ssid:
        ssid = ssid.split('$')[0]
    line[3] = pat_kuohao.sub('', line[3])
    line[3] = pat_kuohao2.sub('', line[3])
    print('%s\t%s\t%s\t%s\t%s' % (ssid, line[0], line[2], line[3], line[4]))
