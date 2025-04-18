import streamlit as st
import random

st.title("🟢 워크숍 팀 랜덤 배정기 + 점수판")

# 초기 상태 설정
if "team_fixed" not in st.session_state:
    st.session_state.team_fixed = False
if "team1" not in st.session_state:
    st.session_state.team1 = []
if "team2" not in st.session_state:
    st.session_state.team2 = []

# 🎲 팀 랜덤 배정
if st.button("🎲 팀 랜덤 배정하기", disabled=st.session_state.team_fixed):
    team1 = ["신문철"]
    team2 = ["장용석"]
    women = ["정아라", "박민영", "강성희", "이다빈"]
    all_members = [
        "신문철", "장용석", "이주용", "정아라", "강희철", "김문규",
        "조운호", "김원래", "오종민", "박민영", "강성희", "이다빈",
        "최정우", "박준섭"
    ]
    others = [m for m in all_members if m not in women + ["신문철", "장용석"]]
    random.shuffle(women)
    team1 += women[:2]
    team2 += women[2:]
    random.shuffle(others)
    team1 += others[:4]
    team2 += others[4:]
    st.session_state.team1 = team1
    st.session_state.team2 = team2

# ✅ 팀 확정 버튼
if st.button("✅ 팀 확정하기") and not st.session_state.team_fixed:
    st.session_state.team_fixed = True

# 📌 팀 출력
if st.session_state.team1 and st.session_state.team2:
    st.subheader("📌 이사님 팀")
    st.write(st.session_state.team1)

    st.subheader("📌 실장님 팀")
    st.write(st.session_state.team2)

    if st.session_state.team_fixed:
        st.success("✔ 팀이 확정되었습니다. 점수 입력이 가능합니다.")
    else:
        st.warning("⏳ 팀이 아직 확정되지 않았습니다.")

# 🏆 점수판 (확정 후에만 표시)
# 점수판 상태 저장용 초기화
if "result_shown" not in st.session_state:
    st.session_state.result_shown = False

# 점수판 (팀 확정 후에만 표시)
if st.session_state.team_fixed:
    st.markdown("---")
    st.header("🏆 게임 점수판")

    game_names = ["제기차기", "릴레이 달리기", "퀴즈쇼"]
    team1_total = 0
    team2_total = 0

    # 점수 입력
    for game in game_names:
        st.markdown(f"**🎮 {game}**")
        col1, col2 = st.columns(2)
        with col1:
            score1 = st.number_input(f"{game} - 이사님 팀", min_value=0, step=1, key=f"{game}_team1")
        with col2:
            score2 = st.number_input(f"{game} - 실장님 팀", min_value=0, step=1, key=f"{game}_team2")

        team1_total += score1
        team2_total += score2

    st.markdown("---")
    st.subheader("📣 총점 결과")
    st.write(f"🟢 이사님 팀 총점: **{team1_total}점**")
    st.write(f"🔵 실장님 팀 총점: **{team2_total}점**")

    # 🎯 결과 확정 버튼
    if st.button("🎯 최종 결과 확정하기"):
        st.session_state.result_shown = True

    # 우승 메시지 출력 (확정 시점에만)
    if st.session_state.result_shown:
        if team1_total > team2_total:
            st.success("🎉 **이사님 팀 우승!** 🥇")
        elif team2_total > team1_total:
            st.success("🎉 **실장님 팀 우승!** 🥇")
        else:
            st.info("🤝 **무승부입니다!**")
