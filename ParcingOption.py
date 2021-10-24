import requests
from bs4 import BeautifulSoup


def search():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

    url = 'https://market.yandex.ru/product--videokarta-gigabyte-geforce-gtx-1650-d6-windforce-oc-4g-rev-' \
          '2-0/765618626?cpc=aX2qLpu8DLIVFxpq7Jf4yQS-wkHgCdENRSxt4LdoG7o5ZPN3bomSF6-5oJknxuX6CyuACQprr-F49kv' \
          'ceMx9RFA0Qzhfj-AFQaSiR8vVPnxVdFetzilzsldRoIRoe_5Gi48oHGESGYfTEpMVcjZ8oRKXeK6Y-Pe7JSJftmOL9Olk9wpVRB7' \
          'iEw%2C%2C&sku=101114697010&do-waremd5=7WFuq9eSaT-GTo1-G4guoQ&cpa=1&nid=22488691'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    with open('Parc.html', 'w', encoding="utf-8") as output_file:
        output_file.write(str(soup))


def parc():
    with open('Parc.html', 'r', encoding='utf-8') as input_file:
        contents = input_file.read()
        soup1 = BeautifulSoup(contents, 'lxml')
        quotes = soup1.find_all('h1')
        quotes1 = soup1.find_all('span')
        for i in quotes:
            f = open('Parc.txt', 'w', encoding='utf-8')
            i = str(i.text)
            f.write(i + '\n')
            print(i)
        flag = True
        for j in quotes1:
            if j.text != '':
                if j.text[len(j.text) - 1] == '₽' and flag:
                    j = str(j.text)
                    j = j[:len(j) - 2:] + j[len(j) - 1]
                    f.write(j)
                    print(j)
                    flag = False


# search()
parc()

# /html/body/div[1]/div[5]/div/div[4]/div/div[2]/div/div/div[1]/h1/text()
# 'https://market.yandex.ru/product--elektricheskii-stabilizator-feiyutech-g6-plus/203000324?cpc=' \
#           'A2awI69IJW9_YoFvhhUf-XSvVRrCb3FgCdb-_5t6d7RHKRJdm7KgLlc7pYkF6qWGbPmNKgLRWZPvNWaWxyRrZ5pd-GMixQP' \
#           'QFQWyM1bvOtbvGs9yo6DKMTfMhS7GacXf_CldG_jC3QYosJyNOkW8be2okyAJfAp8E8TBYC6G2CnkKEXWvEfKVg%2C%2C&sku' \
#           '=203000324&do-waremd5=AXj-DDtb7zlhhrCJw3IjMg&cpa=1&nid=22490890'
