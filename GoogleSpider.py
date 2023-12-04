import requests
import re
from fake_useragent import UserAgent
import time
import os


class GoogleSpider:
    def __init__(self, url, re_str):
        self.url = url
        self.re_str = re_str
        self.url_li = []

    def saveUrls(self, fileName):
        if os.path.exists(f"./google/{fileName}"):
            mode = "a+"
        else:
            mode = "w"
            print(f"[*]写入到google/{fileName}中")
        with open(file="./google/" + fileName, mode=mode) as f:
            try:
                for url in self.url_li:
                    f.write(url + "\n")
                print(f"[+] 结果保存成功!请检查google/{fileName}")
                return True
            except:
                print(f"[-] 出现异常！结果保存失败！")
                return False

    def getResultUrlList(self):
        num = 100
        try:
            for start in range(1, 1000, num):
                req_url = self.url + f"&num={num}&start={start}"  # google 检索的 url 参数需要控制 num和 start
                print(f"[*] 爬取{req_url}中")
                req = requests.get(url=req_url, headers={"User-Agent": UserAgent().random}, verify=False)
                content = req.content.decode()
                re_compile = re.compile(self.re_str)
                urlOneList = re_compile.findall(content)
                if len(urlOneList) == 0:
                    print(f"[-] 该关键词的所有相关 url 爬取结束！如果想要更多结果，请更换关键词!")
                    return self.url_li
                print(f"[+] 在{req_url}页面中一共爬取{len(urlOneList)}个结果")
                self.url_li.extend(re_compile.findall(content))
                self.url_li = [x.strip() for x in self.url_li if "google.com" not in x]
                time.sleep(3)  # 防止请求频繁，停顿 3 秒
            return self.url_li
        except requests.exceptions.ProxyError:
            print('[-] 请求被拦截，可能需要进行人机验证')
            return self.url_li
