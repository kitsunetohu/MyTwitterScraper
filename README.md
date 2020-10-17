

## 实现功能
能够爬取推特搜索内容、用户主页。通过selenium实现，适用于小规模（3000条以下）项目。
与推特高级搜索相结合能达成筛选特定语言、特定时间段等推特内容的目的

目前github的爬虫大多专用性强，虽然高效但配置复杂,需要linux或远程服务器。
本项目旨在通过selenium和推特高级搜索结合，能方便地进行配置和数据爬取，适用于小型或前期测试。

## 使用方法

1. 更改main.py中的，url、pagenum、lang变量
2. 运行
3. 爬取后会生成excel文档，可直接另存为

可以获取搜索页或用户页的所有Tweet的用户名、内容、时间、点赞数、转发数



## 使用环境
anaconda
BeautifulSoup
selenium
python 3.6
chrome

anaconda安装：
https://www.anaconda.com/products/individual

selenium安装：
https://selenium-python.readthedocs.io/installation.html

BeautifulSoup安装：
``` pip install beautifulsoup4 ```
