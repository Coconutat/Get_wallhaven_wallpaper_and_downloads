import os
import json as js
import requests
from genericpath import exists

locate_path = os.getcwd()  # 脚本运行目录
img_save_path = locate_path + "//img//"  # 图片保存位置
# json保存位置，parsingurl.py得到的json文件路径
json_save_patch = img_save_path + "imglist.json"

file = open(json_save_patch)
images_urls = js.load(file)
images_nums = len(images_urls)
user_agent = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
lognum = 0
tmp = "0"

for downloadimg in range(images_nums):
    lognum += 1
    tmp = str(lognum)
    res = requests.get(images_urls[tmp], headers=user_agent)
    save_path = img_save_path + images_urls[tmp].split("/")[-1]  # 定义图片保存位置
    print("开始下载第", lognum, "张图片")
    with open(save_path, 'wb') as f:
        f.write(res.content)
        f.close()
        print("图片 ", lognum, " 已经保存！")

# 清除JSON文件
file.close()  # 关闭打开的JSON文件
os.remove(json_save_patch)
