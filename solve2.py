import traceback
import sys
import codecs
import itertools
import LCS
import operator
def get_data(lines):
	for line in lines:
		line = line.strip().split('\t')
		yield line
def getLCS(ssidlist,flag,laststr,labelnum,poi,ssidwholenum):
        strarr = []
        for ssid in ssidlist:
            ssid = ssid[0]
            strarr.append(len(ssid))
         #   f.write(str(len(ssid)) + ' ')
	    for w in ssid:
                if ord(w)>0xff00:
                    strarr.append(ord('?'))
                   # f.write(str(ord('?'))+' ')
                else:
                    if w>='A' and w<='Z':
                        w = w.lower()
                    strarr.append(ord(w))
		   # f.write(str(ord(w))+' ')
        strarr = tuple(strarr)
        reslen, covernum, idx = LCS.solve(len(ssidlist), len(strarr), strarr)
        if covernum <1:
            return
        if flag==2:
            if reslen<=3:
                return
            if covernum<10 and covernum/len(ssidlist)<2/3:
                return
        if reslen<2:
            return
        cnt = 0
        resstr = ''
        for ssidinfo in ssidlist:
            ssid = ssidinfo[0]
            if idx>=cnt and idx < cnt+len(ssid):
                idx -=cnt
                for i in range(0,reslen):
                    if i+idx<len(ssid):
                        resstr += ssid[i+idx]
                break
            cnt += len(ssid)+1
        if flag ==2:
            if resstr in laststr:
                return
        whole = 0
        ssidlist_comple = []
        poiid = ''
        poitype = {}
        poitype1 = {}
        for ssidinfo in ssidlist:
            whole += 1
            ssid = ssidinfo[0]
            if ssidinfo[2] not in poitype:
                poitype[ssidinfo[2]] = 1
            else:
                poitype[ssidinfo[2]] += 1
            tmp1 = ssidinfo[2].split(';')[0]
            if tmp1 not in poitype1:
                poitype1[tmp1] = 1
            else:
                poitype1[tmp1] += 1
            if resstr in ssid:
                poiid = ssidinfo[1]
            if resstr not in ssid:
                ssidlist_comple.append(ssidinfo)
        tp = ''
        maxtpnum = -1
        poitype['none'] = 0
        poitype1['none'] = 0
        tp1 = ''
        maxtpnum1 = -1
        wholetype = 0
        wholetype1 = 0
        for t in poitype:
            wholetype += poitype[t]
            if poitype[t]>maxtpnum:
                tp = t
                maxtpnum = poitype[t]
        for t in poitype1:
            wholetype1 += poitype1[t]
            if poitype1[t] > maxtpnum1:
                tp1 = t
                maxtpnum1 = poitype1[t]
        if flag == 2:
            whole = ssidwholenum
        print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%(poi,resstr.encode('utf-8'),str(reslen),str(covernum),str(whole+labelnum),str(whole),str(float(covernum)/(whole+labelnum)),str(float(covernum)/whole),poiid,tp+'|'+str(float(maxtpnum)/wholetype)\
                ,tp1 +'|'+str(float(maxtpnum1)/wholetype1)))
        if flag == 1:
            if len(ssidlist_comple)>=3:
                getLCS(ssidlist_comple,2,resstr,labelnum,poi,ssidwholenum)
        return

for poi,data in itertools.groupby(get_data(sys.stdin),operator.itemgetter(0)):
    try:
        ssidcnt = 0
        ssididx = 0
        ssidlist = []
        labellist = set([])
        ssiddata = []
        for g in data:
            if g[1] == 'none':
                labellist.add(int(g[-1]))
            else:
                ssiddata.append(g)
        labelnum = len(labellist)
        poiid = ''
        if len(ssiddata) < 2:
            if len(ssiddata)==1 and len(ssiddata[0])<2:
                continue
            if len(ssiddata) == 1:
                print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%(ssiddata[0][0],ssiddata[0][1],str(len(ssiddata[0][1].decode('utf-8'))),'1',str(1+labelnum),'1',str(float(1)/(1+labelnum)),'1.0',ssiddata[0][-2],ssiddata[0][-3]+'|1.0'\
                        ,ssiddata[0][-3].split(';')[0]+'|1.0'))
             #   print ssiddata[0][0]+'\t'+ssiddata[0][1]+'\t'+str(len(ssiddata[0][1].decode('utf-8')))+'\t1\t'+str(1+labelnum)+'\t1.0\t'+ssiddata[0][-1]
                continue
        for g in ssiddata:
            ssididx += 1
            if len(g) < 3:
                continue
            if g[1] == 'none':
                continue
            ssidcnt += 1
            poiid = g[-1]
            ssidlist.append((g[1].decode('utf-8'),g[-2],g[-3]))
          #  labellist.append(int(g[2]))
            if ssididx == len(ssiddata) or ssidcnt>=2500:
                if len(ssidlist)>0:
                    getLCS(ssidlist,1,'',labelnum,poi,len(ssidlist))
                ssidcnt = 0
                ssidlist = []
            #    labellist = set([])
    except:
 #        pass
         traceback.print_exc() 
