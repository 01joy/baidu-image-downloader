# 百度图片批量下载器
![](https://raw.githubusercontent.com/Beeder/BaiduImageDownloader/master/BaiduImageDownloader.png)

使用python3 + pyqt5 + eric6 + cx_Freeze4完成，详细内容请看[我的博客](http://www.bitjoy.net/2015/08/13/baidu-image-downloader-python3-pyqt5-eric6-cx_freeze4/)

# 文件含义
```
|--__pycache__：python缓存文件内容
|
|--_eric6project：eric6项目文件内容
|
|--build：cx_Freeze4打包内容
|
|--dist：cx_Freeze4打包生成的可执行文件
|
|--BaiduImageDownloader.e4p：eric6项目文件
|
|--BaiduImageDownloader.png：界面截图
|
|--DownloadEngine.py：python3多线程下载类
|
|--Ui_main.py：qt5界面布局代码
|
|--__init__.py：自动生成的文件，空
|
|--main.py：项目主流程
|
|--main.ui：qt gui界面文件
|
|--setup.py：cx_Freeze4打包脚本
```
重要文件是main.py和DownloadEngine.py

# 使用方法
#### 程序猿：

依次安装[python-3.4.3.amd64.msi](https://www.python.org/ftp/python/3.4.3/python-3.4.3.amd64.msi)、[PyQt5-5.5-gpl-Py3.4-Qt5.5.0-x64.exe](http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5/PyQt5-5.5-gpl-Py3.4-Qt5.5.0-x64.exe)、[eric6-6.0.8.zip](http://downloads.sourceforge.net/project/eric-ide/eric6/stable/6.0.8/eric6-6.0.8.zip?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Feric-ide%2Ffiles%2Feric6%2Fstable%2F&ts=1439435222&use_mirror=nchc)。

1. 下载该项目所有代码，在当前路径执行`python main.py`
2. 下载该项目所有代码，导入eric6，选中main.py，按F2执行

#### 人类：

WIN7 64位用户直接下载[BaiduImageDownloader-0.2-amd64.msi](https://github.com/01joy/BaiduImageDownloader/blob/master/dist/BaiduImageDownloader-0.2-amd64.msi?raw=true)安装，在安装目录，双击main.exe运行。

# 已知bug

1. 如果存储目录设置为某个根目录，图片写入失败，因为根目录是c:/的形式，会导致生成c://a.jpg这样的文件，但是写入失败，多了个斜杠/；如果是其他目录c:/img，则拼接为c:/img/a.jpg正确。
2. ~~关键词为`校花`，图片尺寸为`特大`时，程序崩溃，[好像是JSON decode的某个问题](http://stackoverflow.com/questions/15198426/fixing-invalid-json-escape)。~~
3. http://image.baidu.com/i?tn=resultjson&ie=utf-8&word=%s 百度图片取json的API失效，[请另寻他法](http://blog.csdn.net/ttdevs/article/details/13768421)。