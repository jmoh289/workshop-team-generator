import streamlit as st
import random
import os
import json

st.set_page_config(page_title="워크숍 팀 배정기", page_icon="🎯")

st.title("🟢 워크숍 팀 랜덤 배정기 + 점수판")

TEAM_FILE = "teams.json"
GAME_LIST = ["제기차기", "릴레이 달리기", "퀴즈쇼"]

# 🧩 초기 세션 상태 설정
if "team_fixed" not in st.session_state:
    st.session_state.team_fixed = False
if "result_shown" not in st.session_state:
    st.session_state.result_shown = False
if "team1" not in st.session_state:
    st.session_state.team1 = []
if "team2" not in st.session_state:
    st.session_state.team2 = []

# 🧩 저장된 팀 구성 불러오기
if os.path.exists(TEAM_FILE) and not st.session_state.team_fixed:
    with open(TEAM_FILE, "r", encoding="utf-8") as f:
        saved = json.load(f)
        st.session_state.team1 = saved.get("team1", [])
        st.session_state.team2 = saved.get("team2", [])
        st.session_state.team_fixed = True
        st.session_state.result_shown = saved.get("result_shown", False)

# 🎲 랜덤 배정 (확정 전만 가능)
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

# ✅ 팀 확정
if st.button("✅ 팀 확정하기", disabled=st.session_state.team_fixed):
    st.session_state.team_fixed = True
    with open(TEAM_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "team1": st.session_state.team1,
            "team2": st.session_state.team2,
            "result_shown": False
        }, f, ensure_ascii=False, indent=2)

# 🔄 팀 구성 초기화 버튼 (언제든지 누를 수 있음)
if st.button("🔄 팀 구성 초기화"):
    # 세션 상태 초기화
    st.session_state.team_fixed = False
    st.session_state.result_shown = False
    st.session_state.team1 = []
    st.session_state.team2 = []

    # 저장된 파일 삭제
    if os.path.exists(TEAM_FILE):
        os.remove(TEAM_FILE)

    st.experimental_rerun()  # 전체 앱 재실행 (초기 상태로)

# 📌 팀 표시
if st.session_state.team1 and st.session_state.team2:
    st.subheader("📌 이사님 팀")
    st.write(st.session_state.team1)
    st.subheader("📌 실장님 팀")
    st.write(st.session_state.team2)

    if st.session_state.team_fixed:
        st.success("✔ 팀이 확정되었습니다. 점수 입력이 가능합니다.")
    else:
        st.warning("⏳ 팀이 아직 확정되지 않았습니다.")

# 🏆 점수 입력 (팀 확정 후에만)
if st.session_state.team_fixed:
    st.markdown("---")
    st.header("🏆 게임 점수판")

    team1_total = 0
    team2_total = 0

    for game in GAME_LIST:
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

    # 🎯 최종 결과 확정 버튼
    if st.button("🎯 최종 결과 확정하기"):
        st.session_state.result_shown = True
        # 결과 표시 여부도 파일에 저장
        with open(TEAM_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "team1": st.session_state.team1,
                "team2": st.session_state.team2,
                "result_shown": True
            }, f, ensure_ascii=False, indent=2)

    # 🏁 우승 결과 메시지
    if st.session_state.result_shown:
        if team1_total > team2_total:
            st.success("🎉 **이사님 팀 우승!** 🥇")
        elif team2_total > team1_total:
            st.success("🎉 **실장님 팀 우승!** 🥇")
        else:
            st.info("🤝 **무승부입니다!**")
