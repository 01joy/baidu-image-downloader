# -*- coding: utf-8 -*-
import urllib.request
import json
import socket
#from urllib.error import  HTTPError
#import threading
import queue
#import http.client
from PyQt5.QtCore import * 

global dict_arr
dict_arr = {'w': 'a', 'k': 'b', 'v': 'c', '1': 'd', 'j': 'e', 'u': 'f', '2': 'g', 'i': 'h', 't': 'i', '3': 'j', 'h': 'k', 's': 'l', '4': 'm', 'g': 'n', '5': 'o', 'r': 'p', 'q': 'q', '6': 'r', 'f': 's', 'p': 't', '7': 'u', 'e': 'v', 'o': 'w', '8': '1', 'd': '2', 'n': '3', '9': '4', 'c': '5', 'm': '6', '0': '7', 'b': '8', 'l': '9', 'a': '0', '_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/' }
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
        
    def DecodeURL(self, src):
        dest = ''
        i = 0
        length = len(src)
        while i < length:
            if src[i] == '_' or src[i] == 'A':
                if src[i:i+6] in dict_arr:
                    dest += dict_arr[src[i:i+6]]
                    i += 6
                else:
                    dest += src[i]
                    i += 1
            elif src[i] in dict_arr:
                dest += dict_arr[src[i]]
                i +=1
            else:
                dest += src[i]
                i += 1
        return dest
    
    def ParseJSON(self, pn, rn, st):
        url = 'http://image.baidu.com/i?tn=resultjson_com&ie=utf-8&word=%s&pn=%d&rn=%d&z=%d'%(self.word, pn, rn, self.size)
        #print(url)
        request = urllib.request.Request(url = url,  headers = my_header)
        html = urllib.request.urlopen(request).read()
        hjson = json.loads(html.decode('gbk'))
        for i in range(0, len(hjson['data'])-1):#最后一个数据为空
            img_url = self.DecodeURL(hjson['data'][i]['objURL'])
            if img_url not in st:
                st.add(img_url)#去重
                self.progressBar_updated_signal.emit()#更新进度条
            
    def GetImgUrlSet(self):
        img_url_set = set()
        if self.num <= 60:
            self.ParseJSON(0, self.num, img_url_set)
        else:
            i = 0
            while len(img_url_set) < self.num:
                self.ParseJSON(i, 60, img_url_set)
                i += 1
        return img_url_set
    
    def sub_update_progressBar(self):
        self.progressBar_updated_signal.emit()
        
    def run(self):
        global bad
        bad = 0
        self.status_changed_signal.emit('获取URL')
        img_url_queue = queue.Queue(0)
        img_url_set = self.GetImgUrlSet()
        n = 0
        for i in img_url_set:
            img_url_queue.put(i)
            n += 1
            if n == self.num:
                break
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
        
