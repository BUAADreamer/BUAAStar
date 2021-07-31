import requests
from lxml import etree
from bs4 import BeautifulSoup

inLs = [{"webname": "Tmall", "url": "https://list.tmall.com/search_product.htm?q=%s",
         "store": "//*[@id=\"J_ItemList\"]/div/div/div[3]/a/text()",
         "price": "//*[@id=\"J_ItemList\"]/div/div/p[1]/em/@title",
         "productName": "//*[@id=\"J_ItemList\"]/div/div/p[2]/a/@title",
         "detailUrl": "//*[@id=\"J_ItemList\"]/div/div/div[1]/a/@href",
         "headers": {
             'authority': 'list.tmall.com',
             'cache-control': 'max-age=0',
             'upgrade-insecure-requests': '1',
             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3872.400 QQBrowser/10.8.4455.400',
             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'accept-encoding': 'gzip, deflate, br',
             'accept-language': 'zh-CN,zh;q=0.9',
             'cookie': 'cna=QM6MFzgD7VECAZb/DiexI4BO; lid=tb9980523643; enc=mgTD%2FDmAl9K5m1wGwF7coyGEuDQ48Xz8fphWuVwDPZhUFfCJKZrEPDTSeRscSFnhPFzrCwxg7PxiWBiRYySs1GKlEeM%2FCvY%2Bk9zFpjYQY%2BM%3D; _med=dw:1536&dh:864&pw:2016&ph:1134&ist:0; hng=CN%7Czh-CN%7CCNY%7C156; miid=261268894721064690; xlly_s=1; t=a4009dd173096c118669a215179ab6bd; tracknick=tb9980523643; lgc=tb9980523643; _tb_token_=7bb316b15861b; cookie2=28d04242d578d755fb2f62d8574dc0a6; _uab_collina=162752929426879351572555; dnk=tb9980523643; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie14=Uoe2ytBH07LtSQ%3D%3D&existShop=false&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0&cookie21=URm48syIYn73; uc3=lg2=URm48syIIVrSKA%3D%3D&vt3=F8dCujP1zJObcI%2Fwc3c%3D&nk2=F5RMECdSQc4WHviG&id2=UUphzOZ5JytEo%2FCYLw%3D%3D; _l_g_=Ug%3D%3D; uc4=id4=0%40U2grF837HRBJ%2FSrrOEyqKoE5HKMeODjL&nk4=0%40FY4HVZV6cwwgv%2BpzLOA88OUn0nxfFt0%3D; unb=2206470308284; cookie1=AVcXXKQqFCIZqjJ%2BfGHCSNMNueRmjf67O3MPdGygg0A%3D; login=true; cookie17=UUphzOZ5JytEo%2FCYLw%3D%3D; _nk_=tb9980523643; sgcookie=E100QN7Szk9siOyeTM3LbHkYsjhXyG7byoo71N2mshD1p07a%2FYizwKm4eNaOyGQF8bb1%2BNGABAR8FAiOjFstpkocTQ%3D%3D; cancelledSubSites=empty; sg=347; csg=b4948694; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zfvmw%2Fq5v1XFTvxMCE8clTlW3bfDCGE1vtmMMS5%2FOUdt%2Bk9SiPDDVcYHpvE249YAFKjUf2Utdvp72YIw9XDyDnAyw3zLGG4%2B6GY8aeFMg4be%2FgF8cDXozr2TJtoAAGIAeA3sEugt4EFJ8utJnp%2Bx6RKt%2FIuce4Nue7gMO85av1YCQEcHvR0BFFjBXqMd7oORCTtygxOnHGYzM6tcJOm8376YfmWERiqG1G5NIgTklEyd99duP69kji6CO7iPQWbg%3D%3D; x5sec=7b22746d616c6c7365617263683b32223a223365373131313662656166353937636165373434623537383561626135376164434c764e6949674745492f70735a50572b2b722b36674561447a49794d4459304e7a417a4d4467794f4451374d54446a316f536d2b662f2f2f2f3842227d; res=scroll%3A1812*6037-client%3A1812*899-offset%3A1812*6037-screen%3A1920*1080; cq=ccp%3D1; pnm_cku822=098%23E1hvepvUvbpvUvCkvvvvvjiWPFSZsjrmRFLv0jYHPmPwQjDbRFs9Qjrbn2Mp6jYUi9hvCvvv9UUgvpvhvvvvvvgCvvpvvPMMvvhvC9vhvvCvpb9Cvm9vvvvQphvvvvvv9tEvpvQRvvm2phCvhRvvvUnvphvppvvv96CvpvsmkvhvC99vvOCzBT9Cvv9vvUvY%2BnNACv9CvhQZRPZvC0Er6jc6%2Bul684AUyf00h7QEfJBlY84QnH1rD7zpdutIpfmxfaAK5kx%2F0j7%2BD40wjLjaYWL9HF%2BSBiVvQP7%2FHmHL5a7lDLwT; l=eBSwuOngjq6Is5_CBOfCnurza77TcLA0SuPzaNbMiOCPO519u391W6hq2-YpCnGVnsmJR3yYsZa3BS8xgy4eCN0MZRMztuixXdLh.; tfstk=c5CcBu0C8tJbU7pldSOfoVSvL2aRZQlwx155a1ic1v314hCPiSHrBqOQrnmErA1..; isg=BOnpwnnCrBqRhJFW0vy-GP467ZVDtt3oarGfIIveCVAfUgpk0wBQubNIFPbkT3Ug',
         }},
        {"webname": "TaoBao", "url": "https://uland.taobao.com/sem/tbsearch?keyword=%s",
         "store": "//*[@id=\"mx_5\"]/ul/li/a/div[3]/div/text()",
         "price": "//*[@id=\"mx_5\"]/ul/li/a/div[2]/span[2]/text()",
         "productName": "//*[@id=\"mx_5\"]/ul/li/a/div[1]/span/text()",
         "detailUrl": "//*[@id=\"mx_5\"]/ul/li/a/@href",
         "headers": {
             'authority': 'uland.taobao.com',
             'cache-control': 'max-age=0',
             'upgrade-insecure-requests': '1',
             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3872.400 QQBrowser/10.8.4455.400',
             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'accept-encoding': 'gzip, deflate, br',
             'accept-language': 'zh-CN,zh;q=0.9',
             'cookie': '__wpkreporterwid_=bd095931-b888-4801-b8a9-f0ae5ca868c1; mt=ci%3D-1_0; miid=261268894721064690; UM_distinctid=17acd4d6993d5-061c5dccd1db47-33554779-144000-17acd4d699514a; t=a4009dd173096c118669a215179ab6bd; lego2_cna=05DR58C54PEMX5CPYMMWMK8E; cna=QM6MFzgD7VECAZb/DiexI4BO; lgc=tb9980523643; tracknick=tb9980523643; enc=mgTD%2FDmAl9K5m1wGwF7coyGEuDQ48Xz8fphWuVwDPZhUFfCJKZrEPDTSeRscSFnhPFzrCwxg7PxiWBiRYySs1GKlEeM%2FCvY%2Bk9zFpjYQY%2BM%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci=1_1; cookie2=28d04242d578d755fb2f62d8574dc0a6; _tb_token_=7bb316b15861b; lLtC1_=1; v=0; _samesite_flag_=true; xlly_s=1; unb=2206470308284; uc3=lg2=URm48syIIVrSKA%3D%3D&vt3=F8dCujP1zJObcI%2Fwc3c%3D&nk2=F5RMECdSQc4WHviG&id2=UUphzOZ5JytEo%2FCYLw%3D%3D; csg=b4948694; cancelledSubSites=empty; cookie17=UUphzOZ5JytEo%2FCYLw%3D%3D; sgcookie=E100QN7Szk9siOyeTM3LbHkYsjhXyG7byoo71N2mshD1p07a%2FYizwKm4eNaOyGQF8bb1%2BNGABAR8FAiOjFstpkocTQ%3D%3D; dnk=tb9980523643; skt=562ca0f322c86023; existShop=MTYyNzUyOTUzMQ%3D%3D; uc4=id4=0%40U2grF837HRBJ%2FSrrOEyqKoE5HKMeODjL&nk4=0%40FY4HVZV6cwwgv%2BpzLOA88OUn0nxfFt0%3D; _cc_=UtASsssmfA%3D%3D; _l_g_=Ug%3D%3D; sg=347; _nk_=tb9980523643; cookie1=AVcXXKQqFCIZqjJ%2BfGHCSNMNueRmjf67O3MPdGygg0A%3D; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zfvmw%2Fq5v1XFTvxMCE8clTlW3bfDCGE1vtmMMS5%2FOUdt%2Bk9SiPDDVcYHpvE249YAFKjUf2Utdvp72YIw9XDyDnAyw3zLGG4%2B6GY8aeFMg4be%2FgF8cDXozr2TJtoAAGIAeA3sEugt4EFJ8utJnp%2Bx6RKt%2FIuce4Nue7gMO85av1YCQEcHvR0BFFjBXqMd7oORCTtygxOnHGYzM6tcJOm8376YfmWERiqG1G5NIgTklEyd99duP69kji6CO7iPQWbg%3D%3D; ctoken=Dczqn-Gc_1RWCNvGpscFuQNm; _m_h5_tk=c05e7ad3a8b24cc98864b6b624e80dc1_1627542179315; _m_h5_tk_enc=4a949a304b49ac9de16e63d7a6893c9d; CNZZDATA1272960300=1710712994-1627005146-https%253A%252F%252Fwww.baidu.com%252F%7C1627528836; uc1=cookie15=UIHiLt3xD8xYTw%3D%3D&cookie21=U%2BGCWk%2F7pY%2FF&cookie14=Uoe2ytBGpwumZw%3D%3D&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&pas=0; l=eBg_LxPHOLaCMWVbBO5CPurza77O0Qv84PVzaNbMiInca6Nl6FgCrNCKgq2MJdtjgt1XjUKzH5bb-RLHR3fDr1OV-bN0140Znxf..; tfstk=c7oCBRc0M6fQzZLPYv9NzoJoXAZfa_BbFeNndq2JBYnDFih76scd0S0Zg4f-VSy1.; isg=BJSURgxfiUWb1yOb_MkZ1dAmcNIG7bjX1wrSRy53P5-iGTRjX_ykZ1vbGRGB5PAv',
         }},
        {"webname": "JD", "url": "https://search.jd.com/Search?keyword=%s",
         "store": "//*[@id=\"J_goodsList\"]/ul/li/div/div[7]/span/a/text()",
         "price": "//*[@id=\"J_goodsList\"]/ul/li/div/div[3]/strong/i/text()",
         "productName": "//*[@id=\"J_goodsList\"]/ul/li/div/div[4]/a/em/text()",
         "detailUrl": "//*[@id=\"J_goodsList\"]/ul/li/div/div[4]/a/@href",
         "headers": {
             'authority': 'search.jd.com',
             'upgrade-insecure-requests': '1',
             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3872.400 QQBrowser/10.8.4455.400',
             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'accept-encoding': 'gzip, deflate, br',
             'accept-language': 'zh-CN,zh;q=0.9',
             'cookie': '__jdu=16240300343501469942217; areaId=23; ipLoc-djd=23-2121-22469-0; unpl=V2_ZzNtbUZfQ0Z0C0NTchoIDWJUQA4RABAXdA5GUC4bX1BjChEOclRCFnUUR1JnGlQUZwAZWUdcQB1FCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHseXwBmARNcQFJBEXQIQ1NzEVkGZAMUbXJQcyVFDEBVfxhfNWYzE20AAx8VcgxOUn9UXAJkBhNfQ1ZBEHcMR1R%2bHlQNYgARXURnQiV2; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_591b024682e94fcbbfb30715d32d582b|1627534471012; PCSYCityID=CN_460000_460100_460107; __jda=122270672.16240300343501469942217.1624030034.1627007222.1627534471.2; __jdc=122270672; shshshfpa=98baf211-2649-632e-3402-0ce566eda9d7-1627534476; __jdb=122270672.4.16240300343501469942217|2.1627534471; shshshfp=1a261e3fd2158637b42c5dc5bd275e4f; shshshsID=9490d2c337699ce2edd7b0178289313b_2_1627534484544; shshshfpb=tZX1iS%209icBWhdHFqsEIoMA%3D%3D; qrsc=1; rkv=1.0; 3AB9D23F7A4B3C9B=XUZOPZV4JMYL2SUIGP6PRMB4PM53IDOSGYPKAMIQAXZ7SJ3JHML6IJ3DB4PKAUZYIPNW5ANIEZ74MCKTDTFDXZNRD4',
         }},
        {"webname": "suning", "url": "https://search.suning.com/%s/",
         "store": "//*[@id=\"product-list\"]/ul/li/div/div/div[2]/div[4]/a/text()",
         "price": "//*[@id=\"product-list\"]/ul/li/div/div/div[2]/div[1]/span/text()",
         "productName": "//*[@id=\"product-list\"]/ul/li/div/div/div[2]/div[2]/a/text()",
         "detailUrl": "//*[@id=\"product-list\"]/ul/li/div/div/div[2]/div[2]/a/@href",
         "headers": {
             'authority': 'search.suning.com',
             'cache-control': 'max-age=0',
             'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
             'sec-ch-ua-mobile': '?0',
             'upgrade-insecure-requests': '1',
             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
             'sec-fetch-site': 'none',
             'sec-fetch-mode': 'navigate',
             'sec-fetch-user': '?1',
             'sec-fetch-dest': 'document',
             'accept-language': 'zh-CN,zh;q=0.9',
             'cookie': 'tradeLdc=NJGX_YG; SN_SESSION_ID=cc557f4c-83df-4fe2-a95b-076c198e6c1e; _snmc=1; _snsr=direct%7Cdirect%7C%7C%7C; _snma=1%7C162753548537960026%7C1627535485379%7C1627535485379%7C1627535485901%7C1%7C1; _snmp=162753548539655052; _snmb=16275354859142432%7C1627535485931%7C1627535485914%7C1; _snms=162753548593252267; sesab=BCAABBABCAAA; sesabv=23%2C12%2C7%2C1%2C27%2C8%2C3%2C18%2C3%2C4%2C6%2C1; _snvd=1627535488733xaxWQDnOP6H; tradeMA=187; authId=si0vlzypQfH5tUSobM5LfdMPAgSpuYSnm1; cityId=9085; districtId=10598; SN_CITY=200_898_1000085_9085_01_10598_2_0; token=1a9f4c2c-9c93-4401-b25c-a3bc49ad78ea; secureToken=77157C015F0CADE2713F0002102F91CF; totalProdQty=0; hm_guid=b84a0402-94d6-4bfa-91a0-e9dc18b3a31f; isScale=false',
         }},
        {"webname": "pinduoduo", "url": "http://mobile.pinduoduo.com/search_result.html?search_key=%s",
         "store": "//*[@id=\"main\"]/div/div[2]/div/div[3]/div[1]/div/div/div/div[2]/div[3]/div[1]/div[1]/span[2]",
         "price": "//*[@id=\"main\"]/div/div[2]/div/div[3]/div[1]/div/div/div/div[2]/div[3]/div[1]/div[1]/span[2]",
         "productName": "//*[@id=\"main\"]/div/div[2]/div/div[3]/div[1]/div/div/div/div[2]/div[1]/text()",
         "detailUrl": "//*[@id=\"main\"]/div/div[2]/div/div[3]/div[1]/div/div/div/div[2]/div[3]/div[1]/div[1]/span[2]",
         "headers": {'User-Agent': 'Mozilla/5.0'}}
        ]


def getSpecTree(url, headers):
    html = None
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()  # 状态不是200则发生HTTPError异常
        r.encoding = r.apparent_encoding
        html = r.text
    except Exception as e:
        print(e)
        print("产生了HTTPError异常")
    tree = etree.HTML(html)
    # print(html)
    return tree


def Printnode(node):
    if node.text is not None:
        print(node.text)
    if (list(node)):
        for child in node:
            Printnode(child)


def getSpecContent(product, webname=None):
    ans = {}
    ans1 = []
    for info in inLs:
        if webname != None:
            if info['webname'] != webname:
                continue
        try:
            tree = getSpecTree(info["url"] % product, info["headers"])
            stores = tree.xpath(info["store"])
            prices = tree.xpath(info["price"])
            productNames = tree.xpath(info["productName"])
            urls = tree.xpath(info["detailUrl"])
            n = 5 if len(stores) >= 5 else len(stores)
            storeLs = stores[:n]
            priceLs = prices[:n]
            productNameLs = productNames[:n]
            urlLs = urls[:n]
            ret = []
            print(n)
            # print(priceLs)
            # print(productNameLs)
            for i in range(n):
                dic = {}
                dic['webname'] = info['webname']
                if len(storeLs) > 0:
                    dic['store'] = storeLs[i].strip()
                else:
                    dic['store'] = ''
                if len(priceLs) > 0:
                    dic['price'] = float(priceLs[i].strip()) if priceLs[i].strip() != '' else 0
                else:
                    dic['price'] = 0
                if len(productNameLs) > 0:
                    dic['productName'] = productNameLs[i].strip()
                else:
                    dic['productName'] = ''
                if len(urlLs) > 0:
                    dic['detailUrl'] = urlLs[i].strip()
                else:
                    dic['detailUrl'] = ''
                ret.append(dic)
                ans1.append(dic)
            ans[info['webname']] = ret
        except:
            continue
    return ans, ans1


if __name__ == '__main__':
    product = "足球鞋"
    print(getSpecContent(product))
