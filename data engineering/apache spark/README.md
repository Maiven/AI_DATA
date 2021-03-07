주제 : 아파치 스파크 입문과 활용 
참조 : https://tacademy.skplanet.com/live/player/onlineLectureDetail.action?seq=193

<토크 ON 세미나 가이드>

주제 : 아파치 스파크 입문과 활용
▣ T 아카데미 토크 ON 세미나는 현업 전문가 GURU 와 더불어 참석자가 적극적으로
“질의토론 (또는 실습)” 에 참여하는 Interactive Learning 을 지향합니다.
▣ 사전학습 자료의 내용을 충분히 숙지하신 후 세미나에 참석하시면, 일방적인 지식전달이 아닌
질의/토론/실습 중심으로 세미나를 보다 유익하게 만들어 갈 수 있습니다.
▣ 실습환경 셋팅은 별도로 진행되지 않으니, 아래 실습을 위한 SW 를 반드시 준비하신 후 참석해 주세요.

--

1. 사전학습 자료
사전학습 내용 참고 자료
하둡 / 카프카
※ 아래 내용을 사전에 살펴보고 오시면 좋습니다.
▶ T 아카데미 온라인 강의 (아파치 하둡 입문):
https://tacademy.skplanet.com/live/player/onlineLectureDetail.action?seq=188
▶ T 아카데미 온라인 강의 (아파치 카프카 입문):
https://tacademy.skplanet.com/live/player/onlineLectureDetail.action?seq=183
스파크 기본개념
Scala 기본 문법
※ 아래 내용을 사전에 살펴보고 오시면 좋습니다.
▶ 스파크 완벽 가이드 : 1 장(빅데이터와 스파크 간단히 살펴보기)
https://issuu.com/hanbit.co.kr/docs/____________________
▶ Scala 5 분만에 배우기
http://learnxinyminutes.com/docs/scala/
▶ Coursera Scala 강의
https://www.coursera.org/course/progfun

--

2. 실습을 위한 SW 설치 방법
사전준비 항목 참고 자료
 실습 진행을 위해서 노트북 (Mac os 또는 리눅스) 을 지참해 주세요.
※ Window OS 의 경우 개별적으로 VM 기반으로 리눅스 환경을 띄우시는 것은
무방하나 실습시 발생하는 문제에 대해서는 지원이 어렵습니다.
 (*필수) docker
설치
※ 아래 사이트를 참고하여 운영 OS 에 docker 가 구동될 수 있도록 사전
설치합니다.
▶ Mac : https://docs.docker.com/docker-for-mac/
▶ Windows : https://docs.docker.com/docker-for-windows/
▶ Linux : https://docs.docker.com/engine/install/ubuntu/
(*필수) docker 를
통해 zeppelin
이미지 가져오기
※ docker 명령어를 실행하여 아래와 같이 구동 directory 내에 logs 폴더와
notebook 폴더를 생성하고 docker path 에 마운트 합니다.

--

docker run -p 4040:4040 -p 8081:8081 --privileged=true -v $PWD/logs:/logs
-v $PWD/notebook:/notebook -e ZEPPELIN_NOTEBOOK_DIR='/notebook' -e
ZEPPELIN_LOG_DIR='/logs' -d apache/zeppelin:0.8.1 /zeppelin/bin/zeppelin.sh
(*필수) zepplin
구동 확인
cmd>docker-machine ip
192.168.99.100
※ 인터넷 브라우져로 아래 처럼 확인된 ip 로 접속을 해봅니다.
http://192.168.99.100:8080
(*필수) 실습 코드
확인
※ 브라우저로 아래 사이트에서 코드를 확인합니다.
▶ https://github.com/databricks/Spark-The-Definitive-Guide
• 관련 도서(번역서): 스파크 완벽 가이드 : 스파크를 활용한 빅데이터 처리와 분석의
모든 것(한빛 미디어)
