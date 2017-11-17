#encoding=utf-8
"""
check if is normal ssid and extract ssid pattern
"""
import sys
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


pat_5g = re.compile("[_-]5g", re.IGNORECASE)
pat_25g = re.compile("[_-]2.5g", re.IGNORECASE)
pat_digit = re.compile("[0-9]", re.IGNORECASE)
pat_digit2 = re.compile("[0-9]*$", re.IGNORECASE)
pat_none = re.compile("(mobile|wifi|backup|network|wlan|tplink|dlink|tenda|mercury|netcore|netgear\
|cmcc|i-shanghai|i-hangzhou|i-shenyang|i-yangzhou|chinanet|android|chinaunicom|fast|ffan\
|mylgnet|test|mywifi|chinanet|@wanhe|@ffan|-wifi|-free|tp-link|SK_WiFi|U+Net|macAt|\
logitecuser|logitecgameuser|iPhone|ap|_web|PHICOMM|LieBao|xfinity|midea_ac\
|and-Business|Free_secure|D-Link_DIR-|ASUS|midea_db_|midea_da_|Hotspot|xiaomi|mate|\
Vodafone-|R9s|gehua|Telecom-|红米手机|ssid|行车记录仪|WirelessNet|home|-WEB|DIRECT-\
|iptime|HUAWEI|Yunos|midea_ca_|BT-with-FON|BT-X|免费|HP|Cable|WOW|小米手机\
|redmi|fiber|i-LiaoNing|Linksys|魅蓝|TelenetWiFree|HiTV_|Samsung|HP-Print-|-LaserJet|\
D-Link|Movistar|TPGuest|HyFi|Buffalo|JCG捷稀智能无线路由器|智能家居专用接入号|Galaxy|\
moto|htc|TELENETSPOT|olleh|U+Net|SFR|orange|free|Lenovo|Note|midea_e|小米共享|Honor|\
DIR|my|-pptv|pptv)", re.IGNORECASE)
pat_device = re.compile("(backup|^cu_|^Boai-|iphone|tplink|dlink|tenda|mercury|netcore|\
netgear|cmcc|i-shanghai|i-hangzhou|i-shenyang|i-yangzhou|chinanet|android|chinaunicom|\
fast|ffan|mylgnet|test|mywifi|chinanet|@wanhe|@ffan|tp-link|SK_WiFi|U+Net|macAt|\
logitecuser|logitecgameuser|iPhone|PHICOMM|LieBao|xfinity|midea_ac|\
and-Business|Free_secure|D-Link_DIR-|ASUS|midea_db_|midea_da_|Hotspot|xiaomi|mate|\
Vodafone-|R9s|gehua|Telecom-|红米手机|ssid|行车记录仪|WirelessNet|-WEB|DIRECT-|\
iptime|HUAWEI|Yunos|midea_ca_|BT-with-FON|BT-X|HP|Cable|WOW|小米手机|\
redmi|fiber|i-LiaoNing|Linksys|魅蓝|TelenetWiFree|HiTV_|Samsung|HP-Print-|-LaserJet|\
D-Link|Movistar|TPGuest|HyFi|Buffalo|JCG捷稀智能无线路由器|智能家居专用接入号|Galaxy|\
moto|htc|TELENETSPOT|olleh|U+Net|SFR|orange|Lenovo|Note|midea_e|小米共享|Honor|DIR|\
-pptv|pptv|荣耀V)", re.IGNORECASE)


def normal_ssid(ssid):
    """
    get ssid pattern,and check if is a meanningful ssid
    """
    orig_len = len(ssid)
    ssid = pat_device.sub('', ssid)
    orig_len2 = len(ssid)
    ssid = pat_5g.sub('', ssid)
    ssid = pat_25g.sub('', ssid)
    ssid = pat_digit2.sub('', ssid)
    ssid = pat_digit.sub('#', ssid)
    ssid = pat_none.sub('', ssid)
    ssid = ssid.replace('#', '')
    ssid = ssid.replace('_', '')
    ssid = ssid.replace('-', '')
    ssid = ssid.lower()
    valid_len = len(filter(lambda x: x != '#' and x != '_' and x != '-', ssid))
    return ssid, valid_len > 1 and len(ssid) > 2 and orig_len2 == orig_len


def ismobile(ssid):
    """
    check if is a mobile ssid
    """
    ssid2 = pat_device.sub('', ssid)
    if len(ssid2) == len(ssid):
        return False
    return True


def test():
    """
    simple test case
    """
    print normal_ssid("asdfasf1G")
    print normal_ssid("asdfasf_5G")
    print normal_ssid("asdfasf_2.5G")
    print normal_ssid("asdfasf-2.5G")
    print normal_ssid("a1sd22fasf-2.5G")
    print normal_ssid("tp-link-wifi")
    print normal_ssid("tplink-free")
    print normal_ssid('iPhone')
    print normal_ssid('cu_aaa')
    print normal_ssid('bcu_aaa')
    print normal_ssid('Baidu_Friend')
    print normal_ssid('BNU-mobile')


def main():
    """
    main
    """
    for line in sys.stdin:
        g = line.strip().split('\t')
        print normal_ssid(g[0])

if __name__ == '__main__':
    main()
    #test()
