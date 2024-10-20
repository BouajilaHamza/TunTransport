import requests


def translate(text):
    text = text.replace(" ", "%20")
    url = "https://www.bing.com/ttranslatev3?isVertical=1&&IG=E5ABD1443BC14A54A229F0F73D81BFEA&IID=translator.5026"
    payload = f"fromLang=en&to=ar&token=lmLu1_AfspdfcU_VYKkzjH_d5FgcpT52&key=1719150633739&text={text}&tryFetchingGenderDebiasedTranslations=true"
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,ar;q=0.5",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "MUID=0554DE9777946C5F156CCAEB767A6D33; MUIDB=0554DE9777946C5F156CCAEB767A6D33; _EDGE_V=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=5403C447EB9940CF967B860FE3BCCA14&dmnchg=1; MUIDB=0554DE9777946C5F156CCAEB767A6D33; _UR=QS=0&TQS=0; MicrosoftApplicationsTelemetryDeviceId=ccb32325-a7fd-4bdb-afbc-d5fe19911de8; MSPTC=asWpbxckIIbY1FHvy5toJziZd_xCrab0zVjcF-oAgWE; mapc=rm=0; ANIMIA=FRE=1; MMCASM=ID=2D033DDDF6914F4A832F32C80CA78DA6; ABDEF=V=13&ABDV=13&MRNB=1719078075972&MRB=0; _EDGE_S=SID=063FE72F6C406D343CB9F3896D466C1E; _Rwho=u=d&ts=2024-06-22; _HPVN=CS=eyJQbiI6eyJDbiI6MTUsIlN0IjowLCJRcyI6MCwiUHJvZCI6IlAifSwiU2MiOnsiQ24iOjE1LCJTdCI6MCwiUXMiOjAsIlByb2QiOiJIIn0sIlF6Ijp7IkNuIjoxNSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNC0wNi0yM1QwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjoxMjksIlRvYm4iOjB9; _SS=SID=063FE72F6C406D343CB9F3896D466C1E&R=200&RB=0&GB=0&RG=200&RP=200&PC=U316; SRCHS=PC=U316; ak_bmsc=6D0A22B917E3DEB892FE19CCB55C230F~000000000000000000000000000000~YAAQ9Ia6XYnDhUSQAQAACRpTRRh+4/bwJFUOtASic3IPAfjsA90WU1fChuZ5YwxRWURsMyYwI9bG4jwxcmQYG2xFM3v8QynXb30pJmvQeiLn9EictLWUIvc1aYKFiiX7aEvH8FMOpPP3yDvxZ3j9PIxVCURkh39SbSQdwyXuoN809DEIf/aQ3s3/3TAvClQLaDNNtRAnjTr8jngQMiaENJMbcSG1Qp2R9PJEeVPiZI/Hi8FkMp8on6B1h84Ox8nVFNtMAfyNg2HO5Nrp/UtzCWxsT5uNU3WQVIXZXEI6ihoWS/JdORnm/ZVL6OcsJdOdj/KNmEFZo7HFrBYxTQVWtvhwWgMKQNsdxEm7a1Yhme4SNdyX/vQyMVHsWP+j900V0Nnoqhg=; USRLOC=HS=1&ELOC=LAT=36.81328582763672|LON=10.211057662963867|N=Tunis%2C%20Tunis|ELT=1|; SRCHUSR=DOB=20240511&T=1719149992000; _tarLang=default=ar; _TTSS_IN=hist=WyJlbiIsImF1dG8tZGV0ZWN0Il0=&isADRU=0; _TTSS_OUT=hist=WyJhciJd; bm_sv=AA137A58538291B798093E5CA225BD19~YAAQAoa6XUvCjTaQAQAAn65cRRituKLFTmhACIQGLZovwWnAaOv+n0YFXAK+TrH3AcGc939CayTUFB8FhgEuiI8nWga2l5xD4yAPl3YiQBb8FsjQTHZrMOOx0UEgVFu/bwLMuYEutviAPeTiqqW/4sfXDZHqmHGv8qsKS3vEtro+nFPyF+UoHtdsafLyu4M88+PznL/oo/yn+i7aiKDVhVsxDNYvkHBBndHMvpDd26ePtrTwyclDPcfMhRfsBA==~1; ipv6=hit=1719154225934; _RwBf=wls=&r=0&ilt=185&ihpd=0&ispd=1&rc=200&rb=0&gb=0&rg=200&pc=200&mtu=0&rbb=0&g=0&cid=&clo=0&v=1&l=2024-06-23T07%3A00%3A00.0000000Z&lft=0001-01-01T00%3A00%3A00.0000000&aof=0&ard=0001-01-01T00%3A00%3A00.0000000&rwdbt=0001-01-01T00%3A00%3A00.0000000&rwflt=0001-01-01T00%3A00%3A00.0000000&o=2&p=&c=&t=0&s=0001-01-01T00%3A00%3A00.0000000+00%3A00&ts=2024-06-23T13%3A50%3A22.8202579+00%3A00&rwred=0&wlb=&wle=&ccp=&cpt=&lka=0&lkt=0&aad=0&TH=; SRCHHPGUSR=SRCHLANG=en&IG=A5A26F83CC9B4A788CC71ACB6F72AE1A&PV=10.0.0&BRW=W&BRH=S&CW=1396&CH=663&SCW=1381&SCH=3543&DPR=1.4&UTC=60&DM=1&EXLTT=31&CIBV=1.1779.0&HV=1719150635&WTS=63854746792&PRVCW=1396&PRVCH=663; btstkn=DO2HlU9246AKd4bpr%252Fb4raNIbTkOdXP%252F36xRmRvAbHVGugAvYZlssJEJtuHb4tro39KqNqObrW2SNd3BNGQKruXVTawoHSblxUyi%252Fx26RPU%253D; SNRHOP=I=8; SNRHOP=I=&TS=; MUIDB=0554DE9777946C5F156CCAEB767A6D33",
        "origin": "https://www.bing.com",
        "priority": "u=1, i",
        "referer": "https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx",
        "sec-ch-ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version": '"121.0.2277.106"',
        "sec-ch-ua-full-version-list": '"Not A(Brand";v="99.0.0.0", "Microsoft Edge";v="121.0.2277.106", "Chromium";v="121.0.6167.140"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"10.0.0"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-ms-gec-version": "1-121.0.2277.106",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    translated = response.json()[0]["translations"][0]["text"]
    return translated


# @st.cache_resource(show_spinner=False)
def clean_filter(_collection, filter):
    raw_data = list(_collection.find(filter))
    clean_data = [i["Name"] for i in raw_data]
    return raw_data, clean_data
