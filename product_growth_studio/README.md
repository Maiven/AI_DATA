# Product Growth Studio (실행형 제품)

단순 아이디어 문서가 아니라, **바로 실행해서 성장 실험을 운영할 수 있는 제품**입니다.

## 제공 기능
- 실시간 퍼널 계산 (방문→가입→활성화→결제)
- 병목 단계 자동 진단
- CSV 업로드 기반 주차별 추이 시각화
- 온보딩 건강도 점검 (가치제안/TTV/마찰)
- ICE 우선순위 기반 실험 백로그
- 1주 실행 플랜 자동 생성
- 지표 CSV 다운로드

## 빠른 실행
```bash
cd /workspace/AI_DATA
pip install -r product_growth_studio/requirements.txt
streamlit run product_growth_studio/app.py
```

## 데이터 포맷
`sample_funnel.csv`와 동일한 컬럼을 사용합니다.
- `date`
- `visitors`
- `signup`
- `activated`
- `paid`

## 실제 운영 방법
1. 지난 4~8주의 퍼널 데이터를 CSV로 업로드
2. 병목 단계 확인
3. 온보딩 점수가 낮은 항목 1~2개 선택
4. ICE 상위 실험 1개를 1주 동안 실행
5. 다음 주 동일 대시보드에서 개선폭 재측정
