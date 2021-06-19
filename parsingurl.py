# https://wallhaven.cc/
# 实现对此站点的多数页面爬取真实图片的下载地址
import os
import requests
import json
from bs4 import BeautifulSoup
from genericpath import exists

locate_path = os.getcwd()  # 脚本运行目录
img_save_path = locate_path + "//img//"  # 图片保存位置
json_save_patch = img_save_path + "imglist.json"  # json保存位置

print("欢迎！正在检测一些基础...")

if os.path.exists(img_save_path):
  print("img目录存在。将继续。")
else:
  os.mkdir(img_save_path,755)
  print("img目录被创建。将继续。")


url = input("请输入Wallhaven.cc网站您具体要爬取的页面：")  # 让用户输入页面地址
print("开始解析页面，地址是：", url, "\n")

# 设置User-Agent，以便访问一些限制非浏览器的网站
user_agent = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}


def multipleimgpage():  # 多图片页面解析
    r = requests.get(url, headers=user_agent)
    r.encoding = "UTF-8"
    watchdog = r.status_code

    print("输出状态码：", watchdog, "(200为访问成功)")
    demo = r.text
    soup = BeautifulSoup(demo, "html5lib")  # html5lib / html.parser

    # a = soup.find_all("a")
    # 寻找标签为class，class属性为preview的页面
    find_class = soup.find_all(attrs={"class": "preview"})
    # find_class = soup.find(attrs={'class':'item-1'})

    imgstore = dict()  # 存储包含真正指向图片地址的地址的字典

    i = 0  # 序数变量1

    tmp = "0"

    for img in find_class:
        for dictplus in range(1):
            i += 1
            tmp = str(i)
            imgstore[tmp] = img.attrs["href"]

    # 开始访问拥有真正图片的页面，并解析真实的地址

    real_imgstore = dict()  # 存储包含真正图片地址的字典

    loga = 0  # 序数变量2
    logb = 0  # 序数变量3

    lenforurls = len(imgstore)

    tmp2 = "0"
    tmp3 = "0"

    for govistimg in range(lenforurls):
        loga += 1
        tmp2 = str(loga)
        img_url = imgstore[tmp2]
        r2 = requests.get(img_url, headers=user_agent)
        r2.encoding = "UTF-8"
        watchdog2 = r2.status_code
        if watchdog2 == 200:
            print("正在解析，请稍后。")
            demo2 = r2.text
            soup2 = BeautifulSoup(demo2, "html5lib")
            # 寻找标签为id，id属性为wallpaper的页面
            find_class2 = soup2.find_all(attrs={"id": "wallpaper"})
            for img_url in find_class2:
                print(img_url.attrs["src"])
                for dictplus2 in range(1):
                    logb += 1
                    tmp3 = str(logb)
                    real_imgstore[tmp3] = img_url.attrs["src"]

    print("输出地址的JSON文件。请稍后......")
    print("预计img数量：", lenforurls)
    with open(json_save_patch, "a", encoding="UTF-8") as f:  # 自己定义输出json文件的位置
        f.write(json.dumps(real_imgstore, ensure_ascii=False, indent=2))


def singleimgpage():  # 单图片页面解析
    rs = requests.get(url, headers=user_agent)
    rs.encoding = "UTF-8"
    watchdog2 = rs.status_code

    print("输出状态码：", watchdog2, "(200为访问成功)")

    singledemo = rs.text
    # html5lib / html.parser
    singlesoup = BeautifulSoup(singledemo, "html5lib")

    find_single_class = singlesoup.find_all(attrs={"id": "wallpaper"})
    for img_urls in find_single_class:
        print(img_urls.attrs["src"])

    real_single_img_url = dict()
    real_single_img_url["1"] = img_urls.attrs["src"]

    lenforsingle = len(real_single_img_url)
    print("输出地址的JSON文件。请稍后......")
    print("预计img数量：", lenforsingle)
    with open(json_save_patch, "a", encoding="UTF-8") as f:  # 自己定义输出json文件的位置
        f.write(json.dumps(real_single_img_url, ensure_ascii=False, indent=2))

# https://wallhaven.cc/w/xxxxx 这种格式的是单图片页面
# https://wallhaven.cc/toplist or https://wallhaven.cc/search... 等都是多图片页面


lenurlsingle = len("https://wallhaven.cc/w/")

if url.find("https://wallhaven.cc/w/", 0, lenurlsingle) == 0:
    singleimgpage()
else:
    multipleimgpage()
