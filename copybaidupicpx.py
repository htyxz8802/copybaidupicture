#coding=utf-8
import requests
import os
import re
import time
import optparse
# 获取页面的json
def getManyPages(keyword,pages,width,height):
    print '[*] getManypages'
    param=[]
    for i in range(0,30*pages+30,30):
        param.append({
            'tn':'resultjson_com',
            'ipn':'rj',
            'ct':201326592,
            'is':'',
            'fp':'result',
            'queryWord':keyword,
            'cl':'',
            'lm':-1,
            'ie':'utf-8',
            'oe':'urf-8',
            'adpiicid':'',
            'st':-1,
            'z':'',
            'ic':0,
            'word':keyword,
            's':'',
            'se':'',
            'tab':'',
            'width':width,
            'height':height,
            'face':0,
            'istype':2,
            'qc':'',
            'nc':1,
            'fr':'',
            'pn':i,
            'rn':30,
            'gsm':'96',
            '1498206977355':''
            })

    urls = []
    url = 'https://image.baidu.com/search/acjson'
    for i in param:
        try:
            urls.append(requests.get(url,params=i).json().get('data'))
        except Exception, e:
            print '[*] getmanypages exception %s' %str(e)
            pass
    return urls

#解析每个json数据
def parseJson(keyword,datalist, localpath):
    print '[*] parseJson'
    if not os.path.exists(localpath):
        os.mkdir(localpath)
    url = 'https://image.baidu.com/search/detail'
    x = 0
    for list in datalist:
        for s in list:
            spn = s.get('spn')
            p = {
                    'ct':0,
                    'z':0,
                    'ipn':'false',
                    'word':keyword,
                    'step_word':'',
                    'hs':0,
                    'pn':0,
                    'spn':spn,
                    'di':s.get('di'),
                    'pi':s.get('pi'),
                    'rn':1,
                    'tn':'baiduimagedetail',
                    'is':s.get('is'),
                    'istype':2,
                    'ie':'utf-8',
                    'oe':'utf-8',
                    'in':'',
                    'cl':'',
                    'lm':-1,
                    'st':'-1',
                    'cs':s.get('cs'),
                    'os':s.get('os'),
                    'simid':s.get('simid'),
                    'adpicid':s.get('adpicid'),
                    'lpn':0,
                    'ln':'',
                    'fr':'',
                    'fmq':'',
                    'fm':'result',
                    'ic':0,
                    's':'undefined',
                    'se':'',
                    'sme':'',
                    'tab':0,
                    'width':s.get('width'),
                    'height':s.get('height'),
                    'face':'undefined',
                    'ist':'',
                    'jit':'',
                    'cg':'girl',
                    'bdtype':0,
                    'oriquery':'',
                    'objurl':'',
                    'fromurl':'',
                    'gsm':0,
                    'rpstart':0,
                    'rpnum':0
            }
            imgType = s.get('type')

            result = requests.get(url,params=p).text
            imgsrc = re.compile(r'src="(.+?\.%s)"' %imgType)
            imglist = re.findall(imgsrc,result)
            getImg(imglist,localpath,imgType,x)
            x += 1 




def getImg(imglist, localPath, imgType, count):
    print '[*] getimg '

    pattern = re.compile(r'.*/(.*?)\.%s'%imgType,re.S)
    m = 0
    for imgsrc in imglist:
        try:
            print '[++] %s ' %str(imgsrc) 
    
            ir = requests.get(imgsrc)
            # item = re.findall(pattern,imgsrc)  
            # FileName = item[0]+str('.%s'%imgType)
            content = ir.content
            print '[=============] %s'%content.find('JFIF')
            if content.find('JFIF') == 6 :
                FileName = str('%d%d.%s' %(count,m,imgType))
                with open(localPath + FileName,'wb') as f:
                    f.write(content)
                    f.close()
            m += 1
        except Exception, e:
            print '[**] exception: e %s' %str(e)  
            pass 



def main():
    parser = optparse.OptionParser('usage%prog -c <content not null> -i <pages> -w <width> --hg <height> -d <savepath not null>')
    parser.add_option('-c', dest='content',type='string', help='search content')
    parser.add_option('-i',dest='pages',type='long', help='pages')
    parser.add_option('-w',dest='width',type='long',help='width')
    parser.add_option('--hg',dest='height',type='long',help='height')
    parser.add_option('-d',dest='savepath',type='string',help='save path dir')
    (options,args) = parser.parse_args()
   
    if options.content == None or options.savepath == None:
        print '[*] ' + parser.usage
        exit(0)

    c = options.content
    i = options.pages
    w = options.width
    h = options.height
    d = options.savepath
    print '[c] ' + str(c)  
    if options.pages == None:
        i = 30
    if options.width == None:
        w = 1920
    if options.height == None:
        h = 1080
#    if options.savepath == None:
 #       d = '~/Pictures/testpic/'

    datalist = getManyPages(c, i, w, h)
    parseJson(c, datalist, d)



if __name__ == '__main__':
#    dataList = getManyPages('美女',10,1920,1080)  
 #   parseJson('美女',dataList,'/home/yangqiang/Pictures/testpic/') 
    main()





