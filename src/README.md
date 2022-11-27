# SpiderMan 爬虫类

## __init__()

```python
def __init__(self, choice_num, interval=100)
self.type_list	# 豆瓣电影排行榜页面列出的所有类型
```

choice_num：选择爬去的类型列表，从0开始对应

type_list中的类型

interval排名区间，点进去某个类型时会有超过xx%-xx%的电影，这里默认interval=100 <=> 100%-90%，也就是设定左边界(豆瓣url左边大于右边)，整5或整10设定（还没测试过）

### 需要自己改的参数

```python
headers
```

## get_html()

```python
def get_html(self, url)
```

获取html内容

### 需要自己改的参数

无

## grab_urls()

```python
def grab_urls(self)->list:url_list
```

这个函数用来获取在type_list中选中的类型的url，返回的url列表用在最后爬取，每个类型建一个csv文件

现在可以确定暂时还没有加上interval的选择，后续数据量不够再加上

### 需要自己改的参数

目前无

## get_movie_detail()

```python
def get_movie_detail(self, url, center=True)->list:info_list
```

点进去一个电影的详细信息页面，获取这个电影的详细信息

返回一个根据这个电影相关的「信息列表」，里面是字典元素，后续直接改成python的字典，能提高很多效率，现在因为是列表所以爬得慢

url：电影独立页面的链接

center：默认为True，意思是这个电影不是在底下那被推荐十个电影里面的，然后要把底下推荐的电影名字和链接记录下来；如果为False，那就只记录自己的详细信息，不记录底下的十个电影

说明：为了提高一点复用性，因为如果底下记录的十个电影起初没有被爬取，那么在用到的时候需要爬取它的详细信息，但是并不需要爬取关于它的那底下被推荐的十个电影。

### 需要自己改的参数

目前无

### 注意

```
别改参数！

别改参数！

别改参数！
```

因为用来写文件的函数需要和这个函数的参数对应，数量对不上的话应该是写不进去，暂时还没有在写文件中提供try-except这个机制，所以会导致程序直接退出QAQ

## grab_movies()

```python
def grab_movies(self, url)->list:top100
```

从那个类型的页面上爬电影的链接，返回一个存电影链接的列表，top100是因为开始我爬前一百个电影，发现数据不够，里面的「grab_num」变量才是本体

```python
browser = webdriver.Chrome()
        browser.get(_url)
        for i in range(10):
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)

        validHtml = browser.page_source
```

这一段代码，相当于操控了chrome浏览器，然后模拟鼠标往下滚动，因为有一些元素是在javascript里面动态加载的，所以要用这个。

### 需要自己改的参数

```python
grab_num
for i in range(10):	# range里面的数字，一次滚动加载的元素个数可能应该取决于你的屏幕高度，但是我感觉大一点无非就是滚到底下滚不动然后没有元素可供加载，所以问题也不大
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
```

	### 注意

```python
# 改「grab_num」之前注意一下，尽量别超过那个类型中最大电影数，因为我还没写保护机制，所以爬起来可能导致下标越界
from selenium import webdriver
# 用Chrome，其他的我不知道这个包里有没有
```

## store()

写入文件，建议列名直接看文件第一行，更清晰一些

设计是每一个类型的「grab_num」个电影存到一个csv文件里面

没有的信息就是「unknown」

### 需要自己改的参数

目前无，这个应该是可以直接用的，建的csv文件就放在代码那个文件夹里面

### 注意

现在还是没有try-except保护，后续添加

## 注意

```python
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import time
import csv
```

这些包目前足够

## 「sleep」问题

```python
browser = webdriver.Chrome()
        browser.get(_url)
        for i in range(10):
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)

        validHtml = browser.page_source
```

这里要sleep一下，给浏览器一点时间响应

在爬单个电影页面的信息的时候也可以sleep，我测试的时候没有sleep也可以都爬下来，但是防止加载的慢还是建议sleep，尤其是在后面利用爬到的推荐电影的信息间接爬这个电影的详细信息的时候，网页加载会很慢。
