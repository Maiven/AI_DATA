# Product Growth Studio (실행형 제품)

실행 가능한 성장 분석/실험 도구입니다.

## 기능
- 퍼널 지표 계산 및 병목 자동 탐지
- 온보딩 건강도 진단
- ICE 실험 우선순위
- 1주 실행 계획
- 개선 효과/매출 임팩트 시뮬레이터

## 실행
```bash
cd /workspace/AI_DATA
pip install -r product_growth_studio/requirements.txt
streamlit run product_growth_studio/app.py
```

## 테스트
```bash
python -m py_compile product_growth_studio/app.py
pytest product_growth_studio/tests -q
```
