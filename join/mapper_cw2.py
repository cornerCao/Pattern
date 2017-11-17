"""
mapper for cw data
"""
import sys
import pinyin as py
import ssid as ss
import match_reducer as mt
py.load_pinyin_data("pinyin35w")
for line in sys.stdin:
    try:
        line = line.strip()
        content = line.split('\t')
        ssid = content[3]
        name = content[2]
        if '$' in content[2]:
            name = content[2].split('$')[0]
        score = 0
        if '$' in content[3]:
            ssid = ''
            ssidlist = content[3].split('$')
            for s in ssidlist:
                s_tmp, res = ss.normal_ssid(s)
                if res == False:
                    continue
                reslist = py.get_pinyin_with_words(name).split('\001')
                meigezi = reslist[0].split('-')
                quanpin = reslist[0].replace('-', '')
                shouzimu = reslist[2]
                percent = 0
                if (s_tmp in quanpin) or (s_tmp in shouzimu) or (shouzimu in s_tmp)\
                 or (s_tmp in name) or (name in s_tmp) or (quanpin in s_tmp):
                    percent = 1
                if s_tmp in meigezi:
                    continue
                if percent == 0:
                    lcs1, lon = mt.Longest_common_string(quanpin, s_tmp)
                    lcs2, lon = mt.Longest_common_string(name, s_tmp)
                    lcs = max(lcs1, lcs2)
                    percent = float(lcs) / len(s_tmp)
                if percent > score:
                    score = percent
                    ssid = s
        if ssid == '':
            continue
        print('%s\t1\t%s\t%s\t%s' % (content[1], ssid, content[0], name))
    except:
        pass
