"""
mapper for poi pattern
"""
import sys
for line in sys.stdin:
    line = line.strip().split('\t')
    ssid = line[0]
    line[3] = line[3].lower()
    if '$' in line[3]:
        line[3] = line[3].split('$')[0]
    print('%s\t%s\t%s\t%s' % (ssid, line[3], line[5], line[2]))
