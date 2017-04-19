#coding=utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import os,sys


#备份端作为server，接收源数据服务器（客户端）post来的数据，并在本地备份，客户端每20秒向server发送一次最新的数据

define("port", default=8080, help="run on the given port", type=int)
class SyncHandler(tornado.web.RequestHandler):
    def post(self):
        mac=self.get_argument('mac')
        date = self.get_argument('date')
        contentstr=self.get_argument('contentstr')
        #print ('同步'+mac+'的数据')
        #备份目标文件夹地址
        backuprootpath=sys.argv[1]
        targetfolder=backuprootpath+mac #argv[0]为备份数据文件夹路径，以‘/’结尾
        path=targetfolder+'/'+date
        #如果目录不存在则新建目录
        if not os.path.exists(targetfolder):
            os.makedirs(targetfolder)
        #以追加方式写入拷贝文件，如果文件不存在则自动新建
        copyfile=open(path,'a')
        #将从服务器返回的数据追加写入拷贝文件
        if not contentstr=='':
            if not os.stat(path).st_size==0:
                copyfile.write('\n'+contentstr)
            else:
                #print('新建文件')
                copyfile.write(contentstr)

        #print(contentstr)
        copyfile.close()



if __name__ == "__main__":
    print('start backup..')
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        #配置urL与数据的映射句柄
        handlers=[
            (r"/wifitraffic/datasync",SyncHandler),
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    #配置监听端口
    http_server.listen(options.port)
    #服务启动
    tornado.ioloop.IOLoop.instance().start()