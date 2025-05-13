import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
url = input("请输入网址：")
a = int(input("请输入使用的线程数："))
def download_chapter(chapter_url):
    try:
        response = requests.get(chapter_url, headers=header)
        response.encoding = 'utf-8'
        name = etree.HTML(response.text).xpath('//h1/text()')
        noteText = etree.HTML(response.text).xpath('//div[@id="chaptercontent"]/text()')
        with open("小说.txt", 'a', encoding='utf-8') as file:
            for t in name:
                file.write(t + '\n')
            for t in noteText:
                file.write(t + '\n')
        print(f"章节 {name} 下载完成")
    except Exception as e:
        print(f"章节 {name} 下载失败：{e}")

if __name__ == "__main__":
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    webCode = response.text
    en = etree.HTML(webCode)
    li = en.xpath('//div[@class = "listmain"]//dl//dd')

    chapter_urls = ["https://www.bie5.cc" + item.xpath("./a/@href")[0] for item in li]

    with ThreadPoolExecutor(max_workers=a) as executor:
        executor.map(download_chapter, chapter_urls)

