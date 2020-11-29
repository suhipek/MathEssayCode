import requests
from bs4 import BeautifulSoup

cookie = """_EDGE_V=1; MUID=0F19052E3F59653D272C0B6D3E77644E; SRCHD=AF=MOZLBR; SRCHUID=V=2&GUID=28DD87C55CE34750B0FBFA19B686F8F2&dmnchg=1; SRCHUSR=DOB=20191231&T=1606036086000; MUIDB=0F19052E3F59653D272C0B6D3E77644E; SRCHHPGUSR=WTS=63741632886&CW=1274&CH=615&DPR=1.3333333333333333&UTC=480&HV=1606036092&DM=0; ABDEF=MRNB=1582286974066&MRB=0; _BEC=PLTL=422&PLTA=607&PLTN=4; _tarLang=default=en; _TTSS_IN=hist=WyJ6aC1IYW5zIiwiYXV0by1kZXRlY3QiXQ==; _TTSS_OUT=hist=WyJlbiJd; MUIDB=0F19052E3F59653D272C0B6D3E77644E; _EDGE_S=SID=0BB0C1E8144161F80FBACE621589607B&mkt=zh-cn; _SS=SID=0BB0C1E8144161F80FBACE621589607B&bIm=90:; ipv6=hit=1606039691796&t=4"""

def get_sentences(wordEn, wordCh, num):
    sentences = []
    for i in range(1, num+1):
        print('正在爬取{}作为{}的句子,爬取进度{}/{}'.format(wordEn,wordCh,i,num))
        r = requests.get('https://cn.bing.com/dict/service?q= \
            {}%20{}&offset={}&dtype=sen'.format(wordEn, wordCh, i * 10),headers = {"cookie": cookie})
        if r.status_code == 200: soup = BeautifulSoup(r.text, features="html.parser")
        else:
            i -= 1
            continue
        for j in soup.find_all('div', attrs = {'class': 'sen_en b_regtxt'}):
            sentences.append(j.get_text())
    return sentences

if __name__ == "__main__":
    with open('words.csv') as f:
        for i in f.readlines():
            data = i.split(',')
            with open('{}_{}.txt'.format(data[0],data[1]),mode='w') as dataFile:
                dataFile.writelines(map(lambda x: x + '\n', \
                    get_sentences(data[0], data[1], int(data[2]))))
                dataFile.close()
