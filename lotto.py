import requests
import re
import time
import datetime
import locale
locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')


res = []
param = { 'drwNo':[i for i in range(1, 1073)] for i in range(1, 1073)}
param_values = list(param.values())   # 딕셔너리의 값을 리스트로 만들기
param_values = param_values[0]
print(param_values)  # [ [1, 2, 3, 4 ....] ]



for i in range(len(param_values)):
    param = {'drwNo' : param_values[i]}
    res.insert(i, requests.post(
        'https://www.dhlottery.co.kr/gameResult.do?method=byWin', params=param))  # params는 위에서 만든 param을 넣어주기
    text = res[i].text

    p = re.compile('ball_645 lrg ball\d">(\d+)<')
    win_num = p.findall(text)

    sidx = text.find('"desc">')
    eidx = text.find('추첨)<', sidx)
    result2 = text[sidx:eidx]

    p2 = re.compile('([0-9]{4}[가-힣]{1}\s*[0-9]{2}[가-힣]{1}\s*[0-9]{2}[가-힣]{1})')
    drawdate = "".join(map(str, p2.findall(result2)))
    drawdate = datetime.datetime.strptime(drawdate, '%Y년 %m월 %d일')
    
    
    import pymysql
    conn = pymysql.connect(
        host='', user='', password='', 
        db='', charset='utf8' 
    )
    cursor = conn.cursor()


    sql = '''
    INSERT INTO lotto645 (drwNo, num1, num2, num3, num4, num5, num6, bonus, drawdate)
    VALUES (%s, %s, %s, %s,%s, %s,%s, %s,%s)
    '''
    cursor.execute(sql, (param_values[i], win_num[0], win_num[1], win_num[2], win_num[3], win_num[4], win_num[5], win_num[6], drawdate))
    conn.commit()
    cursor.close()
    conn.close()
