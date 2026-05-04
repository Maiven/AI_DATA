import streamlit as st
import pandas as pd

st.set_page_config(page_title="Product Growth Studio", page_icon="🚀", layout="wide")

st.title("🚀 Product Growth Studio")
st.caption("UX · 온보딩 · 전환율을 함께 개선하는 실전 대시보드")

with st.sidebar:
    st.header("1) 퍼널 입력")
    visitors = st.number_input("방문자 수", min_value=0, value=5000, step=100)
    signup = st.number_input("회원가입 수", min_value=0, value=900, step=10)
    activated = st.number_input("핵심행동 완료 수", min_value=0, value=350, step=10)
    paid = st.number_input("결제 사용자 수", min_value=0, value=70, step=1)


def pct(n, d):
    return (n / d * 100) if d > 0 else 0.0


signup_rate = pct(signup, visitors)
activation_rate = pct(activated, signup)
payment_rate = pct(paid, activated)
full_cvr = pct(paid, visitors)

col1, col2, col3, col4 = st.columns(4)
col1.metric("방문→가입", f"{signup_rate:.1f}%")
col2.metric("가입→활성화", f"{activation_rate:.1f}%")
col3.metric("활성화→결제", f"{payment_rate:.1f}%")
col4.metric("전체 CVR", f"{full_cvr:.2f}%")

st.subheader("2) 퍼널 병목 진단")
steps = pd.DataFrame(
    {
        "단계": ["방문", "가입", "활성화", "결제"],
        "사용자수": [visitors, signup, activated, paid],
    }
)
steps["이전 단계 대비 전환율(%)"] = [100.0, signup_rate, activation_rate, payment_rate]
steps["이탈률(%)"] = [0.0, 100 - signup_rate, 100 - activation_rate, 100 - payment_rate]
st.dataframe(steps, use_container_width=True)

bottleneck_row = steps.iloc[1:].sort_values("이전 단계 대비 전환율(%)").iloc[0]
st.warning(f"현재 최우선 병목: **{bottleneck_row['단계']} 단계**")

st.subheader("3) 온보딩 건강도 체크")
checks = {
    "첫 화면에서 가치 제안이 5초 내 이해된다": 3,
    "회원가입 전 체험(샘플/미리보기) 가능": 2,
    "첫 성공 경험(TTV)이 10분 이내 발생": 2,
    "불필요한 입력 필드/권한 요청이 없다": 3,
    "초기 사용자 가이드(툴팁/체크리스트)가 있다": 2,
}

scores = {}
cols = st.columns(len(checks))
for i, (item, default) in enumerate(checks.items()):
    scores[item] = cols[i].slider(item, 1, 5, default)

health = sum(scores.values()) / (5 * len(scores)) * 100
st.progress(int(health))
st.write(f"온보딩 건강도: **{health:.1f}/100**")

if health < 60:
    st.error("온보딩 재설계 필요: 첫 가치 제시와 TTV 단축부터 개선하세요.")
elif health < 80:
    st.info("중간 수준: 마찰 제거와 안내 강화로 빠른 개선이 가능합니다.")
else:
    st.success("양호: 개인화/추천/리텐션 루프로 확장해보세요.")

st.subheader("4) 실험 백로그 (ICE 우선순위)")
st.caption("아이디어를 입력하고 Impact/Confidence/Ease(1~10)를 평가하세요.")

ideas = []
for idx in range(1, 4):
    st.markdown(f"**실험 {idx}**")
    name = st.text_input(f"아이디어 {idx}", value="" if idx != 1 else "가입 단계 소셜 로그인 추가")
    c1, c2, c3 = st.columns(3)
    impact = c1.slider(f"Impact {idx}", 1, 10, 7)
    confidence = c2.slider(f"Confidence {idx}", 1, 10, 6)
    ease = c3.slider(f"Ease {idx}", 1, 10, 5)
    ice = (impact * confidence * ease) / 100
    ideas.append({"아이디어": name or f"실험 {idx}", "Impact": impact, "Confidence": confidence, "Ease": ease, "ICE": round(ice, 2)})

idea_df = pd.DataFrame(ideas).sort_values("ICE", ascending=False)
st.dataframe(idea_df, use_container_width=True)

best = idea_df.iloc[0]
st.success(f"이번 주 1순위 실험: **{best['아이디어']}** (ICE {best['ICE']})")

st.subheader("5) 다음 액션")
st.markdown(
    """
- 상위 실험 1~2개만 선택해 1주 내 릴리즈
- 성공 지표: 해당 병목 단계 전환율 +10% 상대 개선
- 실험 종료 후 동일 화면에서 재측정하고 학습을 기록
"""
)
