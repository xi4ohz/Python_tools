#!/usr/bin/env python
# encoding: utf-8

import sys,httplib, urllib,json,optparse,socket,urlparse
import platform
reload(sys)
sys.setdefaultencoding('utf-8')
if platform.system() == 'Windows':
    sys.setdefaultencoding('gbk')
key = ['xxx','xxx'] #插入你自己的bing key
def GetKey(Del = ''):
    return list.pop(key)
def GetUrl(domainip,nuMpage,key):
    # print ('当前key:'+key)
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': key,
    }

    params = urllib.urlencode({
        # Request parameters
        'q': domainip,
        'count': '50',
        'offset': nuMpage,
        'mkt': 'en-us',
        'safesearch': 'Moderate',
    })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    if response.status == 401:
        print '当前key失效:'+key
        key = GetKey('d')
        print "更换下一个key:"+key
        return GetUrl(domainip,nuMpage,key)
    else:
        return data

def bing(ip):
    pagenum = 0
    i = 0
    try:
        while(1):
            data = GetUrl('ip:{}'.format(ip),pagenum,GetKey())
            hjson = json.loads(data)
            for result in hjson['webPages']['value']:
                i=i+1
                resulturl = result['displayUrl']
                if resulturl.startswith("https://"):
                    resulturl
                else:
                    resulturl =  "http://" + resulturl
                print '[{}] ip:{}  title:{}'.format(i,resulturl,result['name'])
            if len(hjson['webPages']['value'])== 50:
                pagenum=pagenum+50
            else:
                break
    except Exception as e:
        print "NULL"
def getips(host):   #获取C段IP
    ips = []
    ip_pre = ""
    for pre in host.split('.')[0:3]:
        ip_pre = ip_pre + pre + '.'
    for i in range(1, 255):
        ips.append(ip_pre + str(i))
    return ips
def www_ip(name):  #域名转IP
    try:
        result = socket.getaddrinfo(name, None)
        print 'ip:{}'.format(result)
        return result[0][4][0]
    except:
        return 0
if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-u", dest="url", help="Target URL (e.g. \"http://www.baidu.com\" or \"8.8.8.8\")")
    parser.add_option("-c", dest="c",action="store_true", help="C段查询")
    (options, args) = parser.parse_args()
    if options.url:
        if not options.url.startswith('http'):
            options.url = 'http://%s' % options.url
        host = urlparse.urlparse(options.url, 'http').hostname
        ip = www_ip(host)
        if options.c:
            for ip in getips(ip):
                print ip
                bing(ip)
        else:
            bing(ip)
    else:
        parser.print_help()
