import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Product Growth Studio", page_icon="🚀", layout="wide")

st.title("🚀 Product Growth Studio")
st.caption("실제 제품 운영을 위한 UX · 온보딩 · 전환율 개선 워크벤치")


def pct(n: float, d: float) -> float:
    return (n / d * 100) if d > 0 else 0.0


def funnel_metrics(visitors: int, signup: int, activated: int, paid: int) -> dict:
    return {
        "signup_rate": pct(signup, visitors),
        "activation_rate": pct(activated, signup),
        "payment_rate": pct(paid, activated),
        "full_cvr": pct(paid, visitors),
    }


st.sidebar.header("입력 방식")
mode = st.sidebar.radio("데이터 소스", ["수동 입력", "CSV 업로드", "샘플 데이터 사용"], index=2)

if mode == "수동 입력":
    visitors = st.sidebar.number_input("방문자 수", 0, value=5000, step=100)
    signup = st.sidebar.number_input("회원가입 수", 0, value=900, step=10)
    activated = st.sidebar.number_input("활성화 수", 0, value=350, step=10)
    paid = st.sidebar.number_input("결제 수", 0, value=70, step=1)
    current = pd.DataFrame([{"date": "today", "visitors": visitors, "signup": signup, "activated": activated, "paid": paid}])
elif mode == "CSV 업로드":
    up = st.sidebar.file_uploader("퍼널 CSV 업로드", type=["csv"])
    if up is None:
        st.info("CSV를 업로드하거나 샘플 데이터 모드로 전환하세요.")
        st.stop()
    current = pd.read_csv(up)
else:
    current = pd.read_csv("product_growth_studio/sample_funnel.csv")

for c in ["visitors", "signup", "activated", "paid"]:
    current[c] = pd.to_numeric(current[c], errors="coerce").fillna(0).astype(int)

latest = current.iloc[-1]
m = funnel_metrics(latest["visitors"], latest["signup"], latest["activated"], latest["paid"])

tab1, tab2, tab3, tab4 = st.tabs(["실시간 퍼널", "온보딩 진단", "실험 우선순위", "주간 실행 플랜"])

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("방문→가입", f"{m['signup_rate']:.1f}%")
    c2.metric("가입→활성화", f"{m['activation_rate']:.1f}%")
    c3.metric("활성화→결제", f"{m['payment_rate']:.1f}%")
    c4.metric("전체 CVR", f"{m['full_cvr']:.2f}%")

    steps = pd.DataFrame(
        {
            "단계": ["방문", "가입", "활성화", "결제"],
            "사용자수": [latest["visitors"], latest["signup"], latest["activated"], latest["paid"]],
            "전환율": [100.0, m["signup_rate"], m["activation_rate"], m["payment_rate"]],
        }
    )
    bottleneck = steps.iloc[1:].sort_values("전환율").iloc[0]["단계"]
    st.warning(f"현재 병목 단계: **{bottleneck}**")
    st.dataframe(steps, use_container_width=True)

    if "date" in current.columns and len(current) > 1:
        trend = current.copy()
        trend["full_cvr"] = trend.apply(lambda r: pct(r["paid"], r["visitors"]), axis=1)
        fig = px.line(trend, x="date", y=["visitors", "signup", "activated", "paid"], markers=True, title="주차별 퍼널 추이")
        st.plotly_chart(fig, use_container_width=True)
        fig2 = px.line(trend, x="date", y="full_cvr", markers=True, title="전체 CVR 추이")
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("온보딩 체크")
    checks = [
        "첫 화면에서 가치 제안이 5초 내 이해된다",
        "회원가입 전 체험(샘플/미리보기) 가능",
        "첫 성공 경험(TTV)이 10분 이내 발생",
        "불필요한 입력/권한 요청이 없다",
        "초기 가이드(툴팁/체크리스트)가 있다",
    ]
    score_map = {}
    cols = st.columns(len(checks))
    for i, q in enumerate(checks):
        score_map[q] = cols[i].slider(q, 1, 5, 3)

    health = sum(score_map.values()) / (5 * len(checks)) * 100
    st.progress(int(health))
    st.write(f"온보딩 건강도: **{health:.1f}/100**")

    if health < 60:
        st.error("우선 과제: 가치 제안 문구 개선 + 가입 전 체험 제공")
    elif health < 80:
        st.info("개선 과제: TTV 단축 + 가이드 강화")
    else:
        st.success("좋습니다. 다음 단계로 개인화 온보딩 A/B 테스트를 추천합니다.")

with tab3:
    st.subheader("ICE 실험 백로그")
    rows = []
    defaults = ["소셜 로그인 도입", "가입 폼 7개→3개 필드 축소", "첫 실행 튜토리얼 자동 시작"]
    for i in range(3):
        name = st.text_input(f"실험 아이디어 {i+1}", value=defaults[i])
        a, b, c = st.columns(3)
        impact = a.slider(f"Impact {i+1}", 1, 10, 7)
        confidence = b.slider(f"Confidence {i+1}", 1, 10, 6)
        ease = c.slider(f"Ease {i+1}", 1, 10, 5)
        ice = round((impact * confidence * ease) / 100, 2)
        rows.append({"아이디어": name, "Impact": impact, "Confidence": confidence, "Ease": ease, "ICE": ice})

    backlog = pd.DataFrame(rows).sort_values("ICE", ascending=False)
    st.dataframe(backlog, use_container_width=True)
    top = backlog.iloc[0]
    st.success(f"이번 주 1순위: **{top['아이디어']}** (ICE {top['ICE']})")

with tab4:
    st.subheader("1주 실행 계획 자동 생성")
    target = st.selectbox("집중 퍼널 단계", ["방문→가입", "가입→활성화", "활성화→결제"])
    improve_goal = st.slider("목표 상대 개선율(%)", 5, 50, 15)

    st.markdown(
        f"""
### 실행 템플릿
1. **월요일**: 현재 `{target}` 기준선 지표 확정
2. **화~수요일**: 1순위 실험 구현 및 QA
3. **목요일**: 실험 오픈(트래픽 50%)
4. **금요일**: 중간 점검 및 롤백 기준 확인
5. **다음 주 월요일**: 결과 분석 (목표: 상대 {improve_goal}% 개선)

### 성공 조건
- 주 지표: `{target}` 전환율
- 보조 지표: 이탈률, CS 문의량, 활성 사용자 비율
"""
    )

st.download_button(
    "현재 지표 CSV 다운로드",
    data=current.to_csv(index=False).encode("utf-8"),
    file_name="growth_metrics_export.csv",
    mime="text/csv",
)
