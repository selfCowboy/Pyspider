import requests
from selenium import webdriver
from lxml import etree
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
}
DRIVER = webdriver.Chrome(executable_path=r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")

def main():
    url = 'https://tuchong.com/tags/%E5%9F%8E%E5%B8%82/'
    DRIVER.get(url)
    html = etree.HTML(DRIVER.page_source)
    lis = html.xpath("//ul[@class='pagelist-wrapper']//li")
    for li in lis:
        print('-------------------------------------')
        url = li.xpath(".//div[contains(@class,'post-image')]//@style")
        print(url)


if __name__ == '__main__':
    main()