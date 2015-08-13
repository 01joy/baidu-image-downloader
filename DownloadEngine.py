# -*- coding: utf-8 -*-
import urllib.request
import json
import socket
import queue
from PyQt5.QtCore import * 

global my_header
my_header = {'User-Agent':'Mozilla/5.0'}  
global bad
bad = 0

class ImageDownloadThread(QThread):
    sub_progressBar_updated_signal = pyqtSignal()
    def __init__(self,queue_in, dir_in):        #进程间通过队列通信，所以每个进程需要用到同一个队列初始化
        super(ImageDownloadThread,self).__init__()
        self.my_queue=queue_in
        self.dir = dir_in
        #self.setDaemon(True)         #守护线程
        self.start()                 #启动线程
     
    #使用队列实现进程间通信
    def run(self):
        while (True):
            global bad
            img_url = self.my_queue.get()
            socket.setdefaulttimeout(5)#这里对整个socket层设置超时时间。后续连接中如果再使用到socket，不必再设置  
            try:
                urllib.request.urlretrieve(img_url, self.dir + '/' + img_url.split('/')[-1])
            except Exception as e:
                print("-----%s: %s-----\n"%(type(e), img_url))
                bad  += 1
            
            self.sub_progressBar_updated_signal.emit()
            if self.my_queue.empty():
                break
            self.my_queue.task_done()  #当使用者线程调用 task_done() 以表示检索了该项目、并完成了所有的工作时，那么未完成的任务的总数就会减少。


class DownloadEngine(QThread):
    download_done_signal = pyqtSignal(int)
    status_changed_signal = pyqtSignal(str)
    progressBar_updated_signal = pyqtSignal()
    def __init__(self, word_in, size_in, num_in, dir_in, thread_num_in):
        super(DownloadEngine,self).__init__()
        self.word = urllib.parse.quote(word_in)
        self.size = size_in
        self.num = num_in
        self.dir = dir_in
        self.thread_num = thread_num_in
        
    
    def ParseJSON(self, pn, rn, qe):
        url = 'http://image.baidu.com/i?tn=resultjson&ie=utf-8&word=%s&pn=%d&rn=%d&z=%d'%(self.word, pn, rn, self.size)
        #print(url)
        request = urllib.request.Request(url = url,  headers = my_header)
        html = urllib.request.urlopen(request).read()
        hjson = json.loads(html.decode('gbk'))
        for i in range(0, len(hjson['data'])-1):#最后一个数据为空
            qe.put(hjson['data'][i]['objURL'])
            self.progressBar_updated_signal.emit()#更新进度条
            
    def GetImgUrlQueue(self):
        img_url_queue = queue.Queue(0)
        if self.num <= 60:
            self.ParseJSON(0, self.num, img_url_queue)
        else:
            n = self.num / 60
            n = int(n)
            for i in range(n):
                self.ParseJSON(i * 60, 60, img_url_queue)
            self.ParseJSON(n * 60, self.num - n * 60, img_url_queue)
        return img_url_queue
    
    def sub_update_progressBar(self):
        self.progressBar_updated_signal.emit()
        
    def run(self):
        global bad
        bad = 0
        self.status_changed_signal.emit('获取URL')
        img_url_queue = self.GetImgUrlQueue()
        threads = []
        self.status_changed_signal.emit('下载图片')
        #多线程爬去图片
        for i in range(self.thread_num):
            thread=ImageDownloadThread(img_url_queue, self.dir)
            thread.sub_progressBar_updated_signal.connect(self.sub_update_progressBar)
            threads.append(thread)
        #合并进程，当子进程结束时，主进程才可以执行
        for thread in threads:
            thread.wait()
        self.status_changed_signal.emit('下载完成')
        self.download_done_signal.emit(bad)
        
