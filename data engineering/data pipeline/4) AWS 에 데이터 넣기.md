# AWS 에 데이터 넣기

저번까지 해서 원하는 데이터들을 긁어오는 데에는 성공했다.

이제 이를 AWS 에 넣어보고자 한다..

 

우선, AWS 의 RDS 에 들어가서 새로운 데이터베이스를 생성해준다. 이때 데이터 베이스의 선정 기준은 아래와 같다

 

1. 나에게 익숙한가

2. 현업에서 많이 사용하고 있는가

3. 저장하고자 하는 데이터의 형태는 무엇인가

 

총 3가지 이다. 이에 대한 답변은 우선 MYSQL 은 현재 회사에서도 사용하고 있기에 익숙한 DB이며, 현업에서도 가장 많이 사용하기 시작한 DB 이다. 그리고 무엇보다도 저장하고자 하는 데이터는 RDS 형태이므로 RDS 에서 빠른 처리속도를 보여주는 MYSQL 을 선택했다.


![image](https://user-images.githubusercontent.com/10266436/111027498-0a3f0480-8434-11eb-8085-65c841522d8f.png)

그리고 난 후에는 mysql 의 워크벤치에 aws 와 연결을 해주어 mysql 을 활성화 시켰다.
![image](https://user-images.githubusercontent.com/10266436/111027869-4ffccc80-8436-11eb-83a8-de82e5702a4b.png)

```sql
  show databases;
 create database codechodb;

use codechodb;
create table shop_20(dates timestamp,
					ratios int,
                    primary key(dates))
                    engine=InnoDB default charset = 'utf8';
             
             
select * from shop_20;
```


그리고 mysql 워크벤치에 들어가서, 네이버 api 를 통해 수집한 데이터를 담을 데이터 베이스와 테이블을 생성해 준다.


![image](https://user-images.githubusercontent.com/10266436/111027505-12973f80-8434-11eb-9005-739e2c8d3aa5.png)

그러고 난 뒤에는 파이썬을 통해 mysql을 조작하기 위해서 파이썬 패키지인 pymysql 을 활용하여 

파이썬 내에서 mysql을 조작했다.

```python
# aws mysql 연결

def main():
    
    # aws 의 mysql 과 직접 연결
    try:
        # mysql 과 직접 연결
        conn = pymysql.connect(host, user=username, passwd=password, db=database, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
    except:
        logging.error("could not connect to RDS")
        sys.exit(1)

    shops = get_shop(client_id,client_secret)

    # json 으로 변환하기
    raw = json.loads(shops)

    # date, ratio 를 추출
    datas = raw['results'][0]['data']

    # date 와 ratio 를 aws에 넣기 전, 리스트에 담기
    shop_content = []
    for data in datas:
        shop_content.append(
            {
                'dates' : data['period'],
                'ratios' : data['ratio']
            }
        )
    print(shop_content)

```

맨 위에 hostd와 유저 네임등을 변수에 담은 다음에, connect 를 통해 연결했다. 
그리고 미리 만들어둔 get_shop 함수를 통해 naver 에서 데이터를 불러 온 다음에, 필요한 데이터만 추출하여 리스트 내의 딕셔너리 형태로 필요한 데이터들을 담아두었다.


```
{"startDate":"2020-01-01","endDate":"2020-01-10","timeUnit":"date","results":[{"title":"패션의류","category":["50000000"],"data":[{"period":"2020-01-01","ratio":89.00652},{"period":"2020-01-02","ratio":87.14725},{"period":"2020-01-03","ratio":80.25985},{"period":"2020-01-04","ratio":88.98288},{"period":"2020-01-05","ratio":100},{"period":"2020-01-06","ratio":90.04795},{"period":"2020-01-07","ratio":89.18886},{"period":"2020-01-08","ratio":85.80307},{"period":"2020-01-09","ratio":82.07851},{"period":"2020-01-10","ratio":73.47124}]}]}

```
리스트 내에는 딕셔너리 형태로 데이터를 저장했다.

딕셔너리 형태로 저장한 이유는, 추후 이를 aws 의 mysql 로 옮길 때, colum 값을 key, 들어가는 row 값을 value 로 쉽게

추출하기 위해서이다.




aws 에 쿼리문을 날려서 넣어주려고 하면, 한개씩 밖에 들어가지 않고 또 이를 단순하게 쿼리문을 날리면

마지막에 들어간 값만 최종적으로 mysql 에 담기기 때문에 insert_row 라는 함수를 만들고,

이 함수를 for문을 통해 반복하기로 했다. 

 

최종적으로 mysql 에 담긴 결과는 아래와 같다



처음에는 그저 넣는 것이 어려워보였는데 몇개의 조건만 이용하면 aws 의 DB 와 연결이 가능하다는 것이 매우 놀라웠었다. 사람은 일단 해보아야 한다는 것이 새삼 느껴진다..

 

물론, 자신의 컴퓨터에 테이블을 생성하고 거기에 변수들을 넣을 수 있을 것이다. 하지만, 실무에서의 데이터들은 양이 매우 많기 때문에, 이 모든 데이터를 한꺼번에 처리하는 데는 효율이 매우 적다.. 그러기 때문에 많은 양의 데이터를 효율적으로 적재할 수 있는 클라우드 서비스를 사용하는 것이다..라는 생각이 든다.

 

RDB 에 넣기까지의 프로세스를 구현했으니, 다음에는 어떤 데이터를 넣을지 그리고 어떤 분석을 할 것인지에 대해서 

간단하게 기획을 해야겠다.

 


출처:  [기록습관]

