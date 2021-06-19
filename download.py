import os
import  json as js
import requests
from genericpath import exists


json_path = "imglist.json" # parsingurl.py得到的json文件路径，如：D:\\url.json
file = open(json_path)
images_urls=js.load(file)
images_nums = len(images_urls)
user_agent = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
lognum = 0
tmp = "0"

for downloadimg in range(images_nums):
    lognum += 1
    tmp = str(lognum)
    res = requests.get(images_urls[tmp],headers=user_agent)
    save_path = "" + images_urls[tmp].split("/")[-1]  # 定义图片保存位置
    print("开始下载第",lognum,"张图片")
    with open(save_path, 'wb') as f:
      f.write(res.content)
      f.close()
      print("图片 ",lognum,"已经保存！")

# 清除JSON文件
file.close() # 关闭打开的JSON文件
os.remove(json_path)