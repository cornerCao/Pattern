"""
mapper for ssid
"""
import sys
import util
def coordinateConvert(x, y):
    """
    coordinate convert
    """
    try:
        float_x = float(x)
        float_y = float(y)
        if float_x <= 0 or float_y <= 0:
            return (0, 0)
        return map(int, util.coordtrans('wgs84', 'bd09mc', float_x, float_y))
    except:
        return (0, 0)

for line in sys.stdin:
    line = line.strip()
    content = line.split('\t')
    if float(content[2]) == 0 or float(content[3]) == 0:
        continue
    coord = coordinateConvert(float(content[2]), float(content[3]))
    if coord[0] == 0 or coord[0] == 0:
        continue
    print('%s\t0\t%s\t%s\t%s' % (content[0], str(coord[0]), str(coord[1]), content[1]))
