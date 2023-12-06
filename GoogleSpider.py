import openpyxl
import requests
from fake_useragent import UserAgent
import time
from colorama import Fore
from lxml import etree
import pandas as pd
import os


class GoogleSpider:
    def __init__(self, url):
        self.url = url
        self.resultList = []

    def saveUrls(self, fileName):
        title_li = []  # 网站标题
        url_li = []  # 网站url
        link_li = []  # 超链接

        for title, url in self.resultList:
            title_li.append(title)
            url_li.append(url)
            link = f'=HYPERLINK("{url}","点击查看")'
            link_li.append(link)
        save_df = pd.DataFrame({'网站标题': title_li, 'url': url_li, '链接': link_li})
        if os.path.exists(fileName):  # 如何文件存在，则追加
            print(Fore.BLUE + "[*] 文件已存在！与之前得到的结果合并中")
            workbook = openpyxl.load_workbook(fileName, data_only=False)
            sheet = workbook.active
            original_pd = pd.DataFrame(sheet.values, columns=["网站标题", "url", "链接"])
            save_df = pd.concat([original_pd, save_df], axis=0)
            save_df = save_df.drop_duplicates()  # 删除重复行
        num = save_df.shape[0]
        save_df.to_excel(fileName, index=None)
        print(Fore.GREEN + f"[+] 保存成功!一共保存{num}条资产数据!请检查{fileName}!")

    def getResultList(self):
        num = 100
        try:
            for start in range(101, 200, num):
                req_url = self.url + f"&num={num}&start={start}"  # google 检索的 url 参数需要控制 num和 start
                print(Fore.BLUE + f"[*] 爬取{req_url}中")
                req = requests.get(url=req_url, headers={"User-Agent": UserAgent().random}, verify=False)
                content = req.content.decode()
                html = etree.HTML(content)
                resultOneList = []
                for link in html.xpath('//a[@jsname="UWckNb"]'):
                    title = link.xpath('h3[@class]/text()')[0].lstrip(
                        "=").strip()  # 将标题的左边的等于号删除，防止写入excel文件中被当成公式,有一些标题会前面带=号
                    title = title if title else "此网站没有标题"
                    href = link.xpath('@href')[0].strip()
                    resultOneList.append((title, href))
                if len(resultOneList) == 0:
                    print(Fore.RED + f"[-] 可能受到限制了！如果想要更多结果，请更换关键词!")
                    return self.resultList
                print(Fore.GREEN + f"[+] 在{req_url}页面中一共爬取{len(resultOneList)}个结果")
                self.resultList.extend(resultOneList)
                self.resultList = list(set(self.resultList))
                time.sleep(3)  # 防止请求频繁，停顿 3 秒
            return self.resultList
        except requests.exceptions.ProxyError:
            print(Fore.RED + '[-] 请求被拦截，可能需要进行人机验证!')
            return self.resultList
        except IndexError:
            print(Fore.RED + '[-] 可能没爬取到内容，请再重试一遍!')
