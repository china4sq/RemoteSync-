#coding=utf-8
import time

#读文件，从上一次读到的地方继续读
def readfile(path,label):
    fd=open(path,'r') #获得一个句柄
    fd.seek(label)# 把文件读取指针移动到之前记录的位置
    content=fd.readlines() #接着上次的位置继续向下读取
    currentlabel=fd.tell()-1#记录读取到的位置
    if currentlabel<0:
        currentlabel=0
    #将更新的内容逐行放进一个字符串里
    contentstr=''
    for line in content:
        contentstr=contentstr+line
    fd.close()#关闭文件
    #返回最后的标记位置和数据内容
    return currentlabel,contentstr

#追加读取文件内容
def ApendRead(path):
    label=0
    while(True):
        label,contentstr=readfile(path,label)
        print(contentstr)
        time.sleep(2)

#测试追加读
if __name__ == "__main__":
    path="P:/wifi/4860BC6C077E/20170406"
    ApendRead(path)