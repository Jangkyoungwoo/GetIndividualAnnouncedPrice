from bs4 import BeautifulSoup
import requests
import pandas as pd

xmlUrl = 'http://apis.data.go.kr/1611000/nsdi/IndvdLandPriceService/attr/getIndvdLandPriceAttr'
df = pd.read_excel("C:/Users/COMTREE/Desktop/공시지가요청조회요청변수.xlsx")  # dgnb.csv는 등기번호가 있는 엑셀 데이터 #파일 경로는 바꾸시면 됩니다!!
df_list = df.values.tolist()

#2차원 배열 초기화
rows = []
columns = ['jibeon', 'dong', 'year']
for pnu in df_list:
    pnu = str(pnu)[1:-24]    # []형식으로 불러와져서 앞뒤 분리
    print(pnu)
    payload = '?' +'ServiceKey=' + 'RQMiAIqHCNN20vD5mOZQ8tkirErTnCbqPGs0Y%2FVfRJzB31o1WNbpod0tTMjpL0JoToP%2FVWTB6MnLvnWDhpXKJA%3D%3D' +"&" + "pnu="+pnu + '&stdrYear=2023&format=xml&numOfRows=10&pageNo=1' # 요청변수 설정 부분
    apiurl=xmlUrl+payload
    print(apiurl)
    res = requests.get(apiurl)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml-xml') #웹 크롤링
    it = soup.select('fields')
    print(it)
    columns = ['jibeon', 'dong', 'year']
    for node in it:
        try:
            receiveData = node.find('field').text
        except:
            receiveData = ' '
        pnu = node.find('pnu').get_text()
        dong = node.find('ldCodeNm').get_text()
        year = node.find('stdrYear').get_text()

        rows.append({'jibeon': pnu,
                    'dong': dong,
                    'year': year,
                    })
        print(rows)
df = pd.DataFrame(rows, columns=columns)
df.to_excel("성공_230825.xlsx")