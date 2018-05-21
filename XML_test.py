# -*- coding:utf-8 -*-
from xml.parsers.expat import ParserCreate
from urllib import request
class DefaultSaxHandler(object):
    def __init__(self):
        self.city = ''
        self.forecast = []

    def start_element(self, name, attrs):
        if name == 'yweather:location':
            self.city = attrs['city']
        if name == 'yweather:forecast':
            self.forecast.append(
                {'date': attrs['day'], 'text': attrs['text'], 'high': (int(
                    attrs['high'])-32)/1.8, 'low': (int(attrs['low'])-32)/1.8})
def parseXml(xml_str):
    # print(xml_str)
    handler = DefaultSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.Parse(xml_str)
    print('%s weather forecast:' % handler.city)
    for x in handler.forecast:
        print('%s:  %s  high:%0.1f°C   low:%0.1f°C' % (x['date'], x['text'], x['high'], x['low']))
    return {
        'city': handler.city,
        'forecast': handler.forecast
    }


# 测试:
URL = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=xml'

with request.urlopen(URL, timeout=4) as f:
    data = f.read()

result = parseXml(data.decode('utf-8'))
assert result['city'] == 'Beijing'
