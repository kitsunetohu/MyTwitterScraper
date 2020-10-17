from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import xlwings as xw



#**************#
url="https://twitter.com/search?q=lang%3Aja%20mihoyo&src=typed_query&f=live"#想爬推文的搜索界面。配合推特高级搜索可搜索特定语言、时间段,也可以直接爬用户界面
pagenum=3    #想爬多少页（当总页数不足想要爬取页数时，在到达低端时会自动终止）,建议限制在150以下
lang='ja'    #想抓取的语言

#**************#

name_out=[]#名字
comment_out=[]#内容
like_out=[]#点赞
retweet_out=[]#转发
date_out=[]#时间

df=pd.DataFrame({"name":[],
                  "date":[],
                  "comment": [],
                  "like": [],
                  "retweet": []})

tw_timeList=[]



def get_tweets_name(star_bs):
    name = star_bs.find('div', attrs={'dir': "auto"}).text
    return name

def get_tweets_comment(star_bs):
    str=''
    tmp = star_bs.find('div', attrs={'lang':lang,'dir': "auto"})
    if tmp is not None:
        for child in tmp.contents:
            if child.string is not None:
                str=str+child.string

    return str


def get_tweets_like_retweet(star_bs):
    pingjia = star_bs.find_all('div', attrs={'class': "css-1dbjc4n r-xoduu5 r-1udh08x"})
    if len(pingjia)==0:
        return [0,0]
    return [moji2count(pingjia[1]),moji2count(pingjia[2])]

def get_tweets_date(star_bs):
    str=""
    datetime=star_bs.select('time')
    try:
        str = datetime[0]['datetime'][0:19]
    except:
        str="推广"

    return  str

def moji2count(crd):
    if "千" in crd.text:
        comment_number = int(float((crd.text)[:-1].replace(',','')) * 1000)  # 将带有千字的数据转化为整数,并剔除掉‘,’
    elif "万" in crd.text:
        comment_number = int(float((crd.text)[:-1].replace(',','')) * 10000)  # 将带有万字的数据转化为整数
    else:  # 没有带千字或万字
        if crd.text:
            comment_number = int(crd.text.replace(',',''))
        else:  # 若不存在数据，则设为0
            comment_number = 0
    return comment_number



def main():
    pageCount = 0
    browser = webdriver.Chrome()#准备浏览器
    browser.get(url)
    time.sleep(2)
    pageTxt=""

    old_scroll_height = 0  # 表明页面在最上端
    js1 = 'return document.body.scrollHeight'  # 获取页面高度的javascript语句
    js2 = 'window.scrollTo(0, document.body.scrollHeight)'  # 将页面下拉的Javascript语句


    for i in range(pagenum):
        if i >0 :
            if browser.execute_script(js1) > old_scroll_height:
                old_scroll_height = browser.execute_script(js1)#获取到当前页面高度
                browser.execute_script(js2)  # 操控浏览器进行下拉
                time.sleep(1.5)
            else:
                break

        soup = BeautifulSoup(browser.page_source, 'html.parser')#拉取网页内容
        tweets_bs = soup.find_all(attrs={"data-testid": "tweet"})#找到每条推特


        for tweet in tweets_bs:
            try:
                tw_time = tweet.select('time')[0]['datetime']
            except:
                continue
            print(tw_time)
            if tw_time not in tw_timeList:
                tw_timeList.extend(tw_time)  # 把时间戳添加到列表中

                name_out.extend([get_tweets_name(tweet)])
                comment_out.extend([get_tweets_comment(tweet)])
                like_out.extend([get_tweets_like_retweet(tweet)[0]])
                retweet_out.extend([get_tweets_like_retweet(tweet)[1]])
                date_out.extend([get_tweets_date(tweet)])

        pageCount = pageCount + 1
        print(str(pageCount) + "/" + str(pagenum))

    result = {"name": name_out,
              "date": date_out,
              "comment": comment_out,
              "like": like_out,
              "retweet": retweet_out}

    df=pd.DataFrame(result)

    wb=xw.Book()
    wb.sheets[0].range('A1').value=df
    print('成功完成爬取，共爬取了'+str(pageCount)+'页')
    input()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

