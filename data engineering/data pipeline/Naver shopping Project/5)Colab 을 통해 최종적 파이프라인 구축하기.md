이제 마지막으로 colab 을 통해서 aws RDS 에 있는 데이터를 

추출하여 데이터 분석에 쓰일 수 있게 가공하려고 한다.

 

Colab 을 사용한 이유는 구글 드라이브를 통해 쉽게 공유를 할 수 있을 뿐만 아니라

다른 직원들이 사용하는 컴퓨터에 파이썬, 아나콘다 등을 깔지 않아도 되기 때문이다.

즉, 클라우드 시스템인 Colab 을 통해서 인터넷만 되고 노트북만 있으면 어느 장소에서든

접속을 하여 데이터 분석을 진행할 수 있기 때문이다.


mysql 에 축적해놓은 데이터들을 colab을 통해 가져와 데이터 분석에 주로 사용되는 라이브러리인

판다스 데이터프레임으로 변환하는 함수를 만들었다.

```python
import pandas as pd
import numpy as np
import pymysql
import logging

# AWS mysql 연결하기 

host = "database-4.castm60mjxbf.ap-northeast-2.rds.amazonaws.com"
username = "code_cho2"
password = "eogml5132"
database = "codechodb"

def get_data(host,username,database,password):
    try:
      conn  = pymysql.connect(host = host, user=username, db=database, passwd=password, use_unicode=True, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
      cursor = conn.cursor()
    except Exception as e:
      print(e)
      logging.error("could not connect to AWS RDS mysql. Please to let engineers know that!")
      sys.exit(1)
    
    # rds -  데이터를 가져온다
    cursor.execute("select * from shop_20;")
    result = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(result)
    return df

hah = get_data(host,username,database,password)
hah

```

get_data 형태로 mysql에서 데이터를 가져오고 난 후에 데이터 프레임으로 변환시키는 함수를 만들었다.

작은 스타트업에서는 코딩 지식이 없는 사람들이 많기 때문에 비교적 교육하기 쉬운 

파이썬의 판다스를 위주로 활용하여 데이터 분석을 할 수 있는 환경을 구축해보고자 했다. 

위 함수를 통해서 판다스의 데이터 프레임으로 변환을 하면, 그 데이터 프레임을 바탕으로 

데이터 분석을 할 수 있을 것으로 생각한다.


위 결과를 통해서 나온 최종적인 결과물이다.

 

이를 통해 작은 스타트업에서도 AWS와 colab 을 통해 간단하게 데이터 파이프라인을 구축하고

이를 통해 데이터 분석을 할 수 있는 환경을 구축해 보았다.

이번 프로젝트에서는 파이프 라인을 구축하는 것에 중점을 주었기 때문에 어떤 데이터를 활용할 것인지에

대해서는 크게 고려하진 않았다.

 

이를 끝으로 5월 초부터 약 3주간의 기간에 걸쳐 진행해본 작은 사이드 프로젝트를 

마무리 짓고자 한다.

 

처음 이 프로젝트를 기획하고 만든 이유는, 데이터 엔지니어가 하는 업무의 프로세스를

큰 범위 내에서 이해를 하고 싶었기 때문이었다.

해당 프로젝트를 하는 동안, 좀더 수집 프로세스를 고도화 시켜야 되나라고 하는 고민도 많았지만

 

타겟으로 설정한 기업에게는 맞지 않은 프로세스가 될 것이기에 과감히 포기하고 라이트하게

기획을 했다.

 

마지막 기록으로는 이 프로젝트를 하면서 배운 점과 부족했던 점 그리고 

기획한 파이프라인 프로세스와 왜 이 서비스를 선택했는지에 대해서 

간단하게 적고자 한다.

 


출처:  [기록습관]
