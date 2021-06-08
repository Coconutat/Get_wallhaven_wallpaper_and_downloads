# https://wallhaven.cc/
# 实现对此页面的爬取图片地址
import requests
import json
from bs4 import BeautifulSoup
from genericpath import exists


url = "https://wallhaven.cc/search?q=id:25046" # 页面地址

print("开始解析页面，地址是：",url,"\n")

user_agent = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"} # 设置User-Agent，以便访问一些限制网站
r = requests.get(url,headers=user_agent)
r.encoding = "UTF-8"
watchdog = r.status_code

print("输出状态码：",watchdog,"(200为访问成功)")

demo = r.text
soup = BeautifulSoup(demo,"html5lib") # html5lib / html.parser


# a = soup.find_all("a")
find_class = soup.find_all(attrs = {"class":"preview"}) # 寻找标签为class，class属性为preview的页面
# find_class = soup.find(attrs={'class':'item-1'})

imgstore = dict() # 存储包含真正指向图片地址的地址的字典

i = 0 # 序数变量1

tmp = "0"

for img in find_class:
    for dictplus in range(1):
        i += 1
        tmp = str(i)
        imgstore[tmp] = img.attrs["href"]



# 开始访问拥有真正图片的页面，并解析真实的地址

real_imgstore = dict() # 存储包含真正图片地址的字典

loga = 0 # 序数变量2
logb = 0 # 序数变量3


lenforurls = len(imgstore)

tmp2 = "0"
tmp3 = "0"


for govistimg in range(lenforurls):
    loga += 1
    tmp2 = str(loga)
    img_url = imgstore[tmp2]
    r2 = requests.get(img_url,headers=user_agent)
    r2.encoding = "UTF-8"
    watchdog2 = r2.status_code
    if watchdog2 == 200:
        print("正在解析，请稍后。")
        demo2 = r2.text
        soup2 = BeautifulSoup(demo2,"html5lib")
        find_class2 = soup2.find_all(attrs = {"id":"wallpaper"}) # 寻找标签为id，id属性为wallpaper的页面
        for img_url in find_class2:
          print(img_url.attrs["src"])
          for dictplus2 in range(1):
               logb += 1
               tmp3 = str(logb)
               real_imgstore[tmp3] = img_url.attrs["src"]

print("输出地址的JSON文件。请稍后......")
print("预计img数量：",lenforurls)
with open("输出json.json","a",encoding="UTF-8") as f: # 自己定义输出json文件的位置
    f.write(json.dumps(real_imgstore,ensure_ascii=False,indent=2))