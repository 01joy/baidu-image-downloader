#百度图片批量下载器
![](https://raw.githubusercontent.com/Beeder/BaiduImageDownloader/master/BaiduImageDownloader.png)

使用python3 + pyqt5 + eric6 + cx_Freeze4完成，详细内容请看[我的博客](http://www.bitjoy.net/2015/08/13/baidu-image-downloader-python3-pyqt5-eric6-cx_freeze4/)

目前已知bug有：
1. 如果存储目录设置为某个根目录，图片写入失败，因为根目录是c:/的形式，会导致生成c://a.jpg这样的文件，但是写入失败，多了个斜杠/；如果是其他目录c:/img，则拼接为c:/img/a.jpg正确。
2. 关键词为`校花`，图片尺寸为`特大`时，程序崩溃，[好像是JSON decode的某个问题](http://stackoverflow.com/questions/15198426/fixing-invalid-json-escape)。