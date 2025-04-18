# team_generator.py
import streamlit as st
import random

st.title("🟢 워크숍 팀 랜덤 배정기 + 점수판")

if st.button("🎲 팀 조합 추첨하기"):
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

    st.session_state['team1'] = team1
    st.session_state['team2'] = team2

if 'team1' in st.session_state and 'team2' in st.session_state:
    st.subheader("📌 이사님 팀")
    st.write(st.session_state['team1'])

    st.subheader("📌 실장님 팀")
    st.write(st.session_state['team2'])

    st.markdown("---")
    st.header("🏆 게임 점수 입력")

    game_names = ["제기차기", "릴레이 달리기", "퀴즈쇼"]
    team1_total = 0
    team2_total = 0

    for game in game_names:
        st.markdown(f"**🎮 {game}**")
        col1, col2 = st.columns(2)
        with col1:
            score1 = st.number_input(f"{game} - 이사님 팀 점수", min_value=0, step=1, key=f"{game}_team1")
        with col2:
            score2 = st.number_input(f"{game} - 실장님 팀 점수", min_value=0, step=1, key=f"{game}_team2")

        team1_total += score1
        team2_total += score2

    st.markdown("---")
    st.subheader("📣 총점 결과")

    st.write(f"🟢 이사님 팀 총점: **{team1_total}점**")
    st.write(f"🔵 실장님 팀 총점: **{team2_total}점**")

    if team1_total > team2_total:
        st.success("🎉 **이사님 팀 우승!** 🥇")
    elif team2_total > team1_total:
