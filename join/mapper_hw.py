"""
mapper for hw data
"""
import sys
for line in sys.stdin:
    line = line.strip()
    content = line.split('\t')
    print("%s\t1\t%s\t%s\t%s\t%s" % (content[0], content[3], content[5], content[6], content[2]))
