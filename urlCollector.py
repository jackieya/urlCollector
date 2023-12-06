# coding=utf-8
import argparse
import pyfiglet
import urllib3
from colorama import Fore
urllib3.disable_warnings()
import os
from GoogleSpider import GoogleSpider
from BingSpider import BingSpider

resultUrlList = []


def main():
    banner = "urlCollector"
    print(pyfiglet.figlet_format(banner))
    parser = argparse.ArgumentParser(prog="urlCollector", description="a url Collector for major search engines.",
                                     epilog="author:Anch0r")
    parser.add_argument("-q", "--query", default="hack", help="the query keyWorld")  # 要检索的关键字
    parser.add_argument("-e", "--engine", type=str, choices=["google", "bing"], default="google",
                        help="the engine, the value is restricted to google and bing")  # 指定搜索引擎
    args = parser.parse_args()
    if args.engine == "google":  # 搜索引擎为google
        url = f"https://www.google.com/search?q={args.query}"
        re_str = '<a jsname=.*?href="(http.*?)".*?>'
        googleSpider = GoogleSpider(url)
        resultUrlList = googleSpider.getResultList()
    elif args.engine == "bing":  # 搜索引擎为 bing
        url = f"https://cn.bing.com/search?q={args.query}"
        re_str = '<a target="_blank" href="(.*?)".*?>'
        bingSpider = BingSpider(url)
        resultUrlList = bingSpider.getResultList()
    else:
        print(Fore.RED + "[-] 请在['google', 'bing']中选择！")
        exit()
    resultUrlList = list(set(resultUrlList))  # 结果去重
    num = len(resultUrlList)
    if num:
        print(Fore.GREEN + f"[+] 一共爬取{num}个结果, 爬取结果如下：")
        print(resultUrlList)
        while True:  # 将结果保存
            ifSave = input(Fore.BLUE + "[*] 请问是否保存爬取的结果? y or n:").strip()
            if ifSave == "y":
                fileName = input(Fore.BLUE + "[*] 请输入您要保存的文件名(默认回车以检索关键字为文件名):")
                fileName = fileName.strip()
                fileName = fileName + ".xlsx" if fileName else f"\"{args.query}\".xlsx"
                if args.engine == "google":
                    fileName = f'./google/{fileName}'
                    googleSpider.saveUrls(fileName)
                elif args.engine == "bing":
                    fileName = f'./bing/{fileName}'
                    bingSpider.saveUrls(fileName)
                break
            elif ifSave == "n":
                break
            else:
                print(Fore.RED + "[-] 输入格式错误，只能输入 y or n,请重新输入。")
    else:
        print(Fore.RED + "[-] 爬取 0 个结果！请尝试换个关键词！")


if __name__ == '__main__':
    main()
