import requests
from lxml import etree


def fetch_stocks_from_hgtz() -> list:
    response = requests.get('http://www.haiguitouzi.com/doc/intro_stock_list.php')
    html_content = response.text
    root = etree.HTML(html_content)
    nodes = root.xpath('//table/tbody/tr/td')
    result = []
    for item in nodes:
        title = item.xpath('./a')[0]
        print(f"{item.text} - {title.text}")
        code = item.text.strip()
        title = title.text.strip()
        result.append({"code": code, "title": title})
    return result


if __name__ == '__main__':
    item = fetch_stocks_from_hgtz()
