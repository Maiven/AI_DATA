import pandas as pd
import plotly.express as px
import streamlit as st

from product_growth_studio.engine import FunnelSnapshot, detect_bottleneck, funnel_metrics, projected_paid_users

st.set_page_config(page_title="Product Growth Studio", page_icon="🚀", layout="wide")

st.title("🚀 Product Growth Studio")
st.caption("실제 제품 운영을 위한 UX · 온보딩 · 전환율 개선 워크벤치")

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
snapshot = FunnelSnapshot(
    visitors=int(latest["visitors"]),
    signup=int(latest["signup"]),
    activated=int(latest["activated"]),
    paid=int(latest["paid"]),
)
m = funnel_metrics(snapshot)


tab1, tab2, tab3, tab4, tab5 = st.tabs(["실시간 퍼널", "온보딩 진단", "실험 우선순위", "주간 실행 플랜", "임팩트 시뮬레이터"])

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("방문→가입", f"{m['signup_rate']:.1f}%")
    c2.metric("가입→활성화", f"{m['activation_rate']:.1f}%")
    c3.metric("활성화→결제", f"{m['payment_rate']:.1f}%")
    c4.metric("전체 CVR", f"{m['full_cvr']:.2f}%")

    bottleneck = detect_bottleneck(snapshot)
    st.warning(f"현재 병목 단계: **{bottleneck}**")

    steps = pd.DataFrame(
        {
            "단계": ["방문", "가입", "활성화", "결제"],
            "사용자수": [snapshot.visitors, snapshot.signup, snapshot.activated, snapshot.paid],
            "전환율": [100.0, m["signup_rate"], m["activation_rate"], m["payment_rate"]],
        }
    )
    st.dataframe(steps, use_container_width=True)

    if "date" in current.columns and len(current) > 1:
        trend = current.copy()
        trend["full_cvr"] = trend.apply(lambda r: (r["paid"] / r["visitors"] * 100) if r["visitors"] > 0 else 0.0, axis=1)
        st.plotly_chart(px.line(trend, x="date", y=["visitors", "signup", "activated", "paid"], markers=True, title="주차별 퍼널 추이"), use_container_width=True)
        st.plotly_chart(px.line(trend, x="date", y="full_cvr", markers=True, title="전체 CVR 추이"), use_container_width=True)

with tab2:
    checks = [
        "첫 화면에서 가치 제안이 5초 내 이해된다",
        "회원가입 전 체험(샘플/미리보기) 가능",
        "첫 성공 경험(TTV)이 10분 이내 발생",
        "불필요한 입력/권한 요청이 없다",
        "초기 가이드(툴팁/체크리스트)가 있다",
    ]
    cols = st.columns(len(checks))
    score_map = {q: cols[i].slider(q, 1, 5, 3) for i, q in enumerate(checks)}
    health = sum(score_map.values()) / (5 * len(checks)) * 100
    st.progress(int(health))
    st.write(f"온보딩 건강도: **{health:.1f}/100**")

with tab3:
    rows = []
    defaults = ["소셜 로그인 도입", "가입 폼 축소", "첫 실행 튜토리얼 자동 시작"]
    for i in range(3):
        name = st.text_input(f"실험 아이디어 {i+1}", value=defaults[i])
        a, b, c = st.columns(3)
        impact = a.slider(f"Impact {i+1}", 1, 10, 7)
        confidence = b.slider(f"Confidence {i+1}", 1, 10, 6)
        ease = c.slider(f"Ease {i+1}", 1, 10, 5)
        rows.append({"아이디어": name, "ICE": round((impact * confidence * ease) / 100, 2)})
    backlog = pd.DataFrame(rows).sort_values("ICE", ascending=False)
    st.dataframe(backlog, use_container_width=True)

with tab4:
    target = st.selectbox("집중 퍼널 단계", ["가입", "활성화", "결제"])
    improve_goal = st.slider("목표 상대 개선율(%)", 5, 50, 15)
    st.markdown(f"이번 스프린트 목표: **{target} 단계 전환율 상대 {improve_goal}% 개선**")

with tab5:
    st.subheader("개선 효과 시뮬레이션")
    improve_step = st.selectbox("개선 단계", ["가입", "활성화", "결제"])
    improve_pct = st.slider("개선율(상대, %)", 1, 100, 20)
    arppu = st.number_input("결제 사용자당 평균 매출(원)", min_value=0, value=30000, step=1000)

    baseline_paid = snapshot.paid
    projected_paid = projected_paid_users(snapshot, improve_step, improve_pct)
    delta_paid = projected_paid - baseline_paid
    delta_revenue = delta_paid * arppu

    a, b, c = st.columns(3)
    a.metric("현재 결제 사용자", baseline_paid)
    b.metric("예상 결제 사용자", projected_paid, delta=delta_paid)
    c.metric("예상 매출 증분", f"₩{delta_revenue:,.0f}")

st.download_button(
    "현재 지표 CSV 다운로드",
    data=current.to_csv(index=False).encode("utf-8"),
    file_name="growth_metrics_export.csv",
    mime="text/csv",
)
