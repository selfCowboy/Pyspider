from lxml import etree
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'cookie':'RECOMMEND_TIP=true; user_trace_token=20211029150640-f6292e25-1d2e-49c3-9df5-c1f12eef5dad; LGUID=20211029150640-63f59066-2ded-47d5-8818-e1ac9e14449b; _ga=GA1.2.343371776.1635491201; JSESSIONID=ABAAABAABEIABCI05AC1D9BB7F45FBA149ABB0556FFEF76; WEBTJ-ID=03122021%2C161251-17d7f5a68fc186-04919c1946db67-b7a1a38-1327104-17d7f5a68fd166; privacyPolicyPopup=false; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1638519172; _gid=GA1.2.1424249324.1638519172; sensorsdata2015session=%7B%7D; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=0977480691b2bc624719158361c0b6bf9c9acd802f; TG-TRACK-CODE=index_search; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1638519236; LGRID=20211203161500-37dae636-2813-4732-9a53-81331bbb4a63; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217ccadf3fd245b-0808c93b42fd39-b7a1a38-1327104-17ccadf3fd3e21%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2294.0.4606.61%22%7D%2C%22%24device_id%22%3A%2217ccadf3fd245b-0808c93b42fd39-b7a1a38-1327104-17ccadf3fd3e21%22%7D',
}
DRIVER = webdriver.Chrome(executable_path=r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
position = []
def main():
    url = "https://www.lagou.com/wn/jobs?labelWords=&fromSearch=true&suginput=&kd=python"
    DRIVER.get(url)
    response = DRIVER.page_source
    parse_list_page(response)
    print("------------------------------")
    next = DRIVER.find_element(By.XPATH,"//li[@class='lg-pagination-next']/a")
    while next:
        if "lg-pagination-disabled" in DRIVER.find_element(By.XPATH,"//li[contains(@class,'lg-pagination-next')]").get_attribute('class'):
            print("最后一页爬取完成！")
            break
        else:
            print("开始爬取下一页--------》》》》》")
            next.click()
            time.sleep(1)
    DRIVER.quit()


def parse_list_page(response):
    html = etree.HTML(response)
    divs = html.xpath("//div[@class='list__YibNq']/div")
    for div in divs:
        data = {}
        title = div.xpath(".//div[@class='p-top__1F7CL']/a/text()")[0]
        name = re.match(r"(.*)\[(.*)\]",title).group(1)
        address = re.match(r"(.*)\[(.*)\]",title).group(2)
        money = div.xpath(".//span[@class='money__3Lkgq']/text()")[0]
        experience = div.xpath(".//div[@class='p-bom__JlNur']/text()")[0]
        company = div.xpath(".//div[@class='company-name__2-SjF']/a/text()")[0]
        company_info = div.xpath(".//div[@class='industry__1HBkr']/text()")
        if company_info:
            data['company_info'] = company_info[0]
        data['name'] = name
        data['address'] = address
        data['money'] = money
        data['experience'] = experience
        data['company'] = company
        DRIVER.find_element(By.XPATH, ".//div[@class='p-top__1F7CL']/a").click()
        windows = DRIVER.window_handles
        DRIVER.switch_to.window(windows[1])
        time.sleep(1)
        response = DRIVER.page_source
        description = parse_detail_page(response)
        data['description'] = description
        DRIVER.close()
        DRIVER.switch_to.window(windows[0])
        time.sleep(1)
        position.append(data)
        break

    with open('position.json', 'w', encoding='utf-8') as fp:
        for i in range(len(position)):
            json.dump(position[i], fp, ensure_ascii=False)
            fp.write("\n")


def parse_detail_page(response):
    html = etree.HTML(response)
    time.sleep(1)
    description = "".join(html.xpath("//div[@class='job-detail']//text()"))
    return description.replace(" ","")


if __name__ == '__main__':
    main()