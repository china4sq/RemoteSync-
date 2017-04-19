#coding=utf-8
import os
import time
import threading
import sys



#时间戳转日期字符串
def todatestr(timeStamp):
    import datetime
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    return dateArray.strftime("%Y%m%d")

#时间字符串转时间戳
def timestr2timestamp(timestr):
    #中间过程，一般都需要将字符串转化为时间数组,再转时间戳
    return int(time.mktime(time.strptime(timestr,'%Y-%m-%d %H:%M:%S')))

#时间戳转时间字符串
def todatetimestr(timeStamp,offset):
    import datetime
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp+offset)
    return dateArray.strftime("%Y-%m-%d %H:%M:%S")


#追加写入文件，模拟动态写入
def appendwrite(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    while (True):
        timestamp=int(time.time())
        date=todatestr(timestamp)
        path=folder+date
        file = open(path, 'a')
        line='ABCD12345678|-70|'+str(timestamp)
        line=line+'\n'
        file.write(line)
        print(line)
        file.close()
        time.sleep(2)

if __name__ == "__main__":
    threads=[]
    rootpath=sys.argv[1]
    threads.append(threading.Thread(target=appendwrite,args=(rootpath+'4860BC6C077E/',)))
    threads.append(threading.Thread(target=appendwrite,args=(rootpath+'4860BC6C077B/',)))
    for t in threads:
        t.start()