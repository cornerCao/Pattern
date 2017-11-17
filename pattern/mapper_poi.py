"""
mapper for ssid pattern
"""
#coding=utf-8
import sys
for line in sys.stdin:
    line = line.strip()
    content = line.split('\t')
    print('%s\t%s\t%s\t%s' % (content[1], content[0], content[3], content[-1]))
