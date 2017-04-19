#coding=utf-8
import urllib.parse
import urllib.request
from readFile import readfile
import time,threading,sys,os


#源数据服务器作为客户端，每隔20秒向server端（备份端）发送最新的数据

#时间戳转日期字符串
def todatestr(timeStamp):
    datestr=time.strftime('%Y%m%d',time.localtime(timeStamp))
    return datestr
#时间字符串转时间戳
def timestr2timestamp(timestr):
    #中间过程，一般都需要将字符串转化为时间数组,再转时间戳
    return int(time.mktime(time.strptime(timestr,'%Y%m%d %H:%M:%S')))
#时间戳转时间字符串
def todatetimestr(timeStamp,offset):
    import datetime
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp+offset)
    return dateArray.strftime("%Y%m%d %H:%M:%S")

def getDateList(begindate):
    dates=[]
    timestamp=timestr2timestamp(begindate+' 00:00:00')
    currenttime=timestr2timestamp(todatestr(time.time())+' 00:00:00')
    while timestamp<currenttime:
        dates.append(todatestr(timestamp))
        timestamp=timestamp+3600*24
    return dates



def post2server(currentlabel,mac,date):
    rootpath=sys.argv[1]
    label=0
    try:
        #备份服务器地址与端口
        #host='139.129.110.99'
        #host='10.108.166.201'
        host=sys.argv[2]
        port='8080'
        #源数据路径
        path=rootpath+mac+'/'+date
        #print('从第'+str(currentlabel)+'字节处开始同步本地文件：'+path)
        #从本地读取更新的数据与及获得更新后的标志
        label,contentstr=readfile(path=path,label=currentlabel)
        #print(contentstr)
        #构造post数据
        post_data = {'mac':mac,'date':date,'contentstr':contentstr}
        #post数据编码
        post_data_urlencode = urllib.parse.urlencode(post_data).encode(encoding='UTF8')
        #备份服务器url
        requrl = "http://"+host+":"+port+"/wifitraffic/datasync"
        #把数据post到备份服务器
        req=urllib.request.Request(requrl, post_data_urlencode)
        res=urllib.request.urlopen(req)
        status=res.code
        #print(status)
        #如果状态吗不为200，备份端上传备份端失败，则标记不往前走
        if not status==200:
            label=currentlabel

    except:
        print('error')
        label=currentlabel
    finally:
        #返回最新标志
        return label

#获得指定目录下的所有文件夹列表
def getAPlist(APfolder):
    APlist=[]
    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent,dirnames,filenames in os.walk(APfolder):
        for dirname in  dirnames:
            path=dirname
            APlist.append(path)
    return APlist

#发送对应AP的数据到服务器
def topost(mac):
     #标记代表从文件开头数起几个字节处
    #初始label为0，表示从文件开头读起。
    #以后每次拷贝会更新该标记。
    initlabel=0
    label=initlabel
    #指定要备份的mac
    lastdate=todatestr(time.time())
    while(True):
        #print('###############################################################')
        #获得当前日期，与上一次的日期比较
        date=todatestr(time.time())
        #零点处理：日期一变，则标志置零，新建新的备份文件
        if not date==lastdate:
            #先把旧的一天剩下的所有记录同步
            post2server(label,mac,lastdate)
            #再从头开始同步新的一天数据
            label=0
            lastdate=date
        label=post2server(label,mac,date)
        time.sleep(2)

if __name__=='__main__':

    dates=getDateList(sys.argv[3])

    #获得指定目录下的所有文件夹列表
    APlist=getAPlist(sys.argv[1])
    for d in dates:
        for AP in APlist:
            print(AP+':'+d)
            post2server(0,AP,d)
    print('history finish')
    threads = []
    #遍历AP列表
    for AP in APlist:
        threads.append(threading.Thread(target=topost,args=(AP,)))
    #开启多线程
    for t in threads:
        t.start()


