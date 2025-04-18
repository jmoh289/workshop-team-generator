import streamlit as st
import random
import os
import json

st.set_page_config(page_title="워크숍 팀 배정기", page_icon="🎯")

st.title("🟢 워크숍 팀 랜덤 배정기 + 점수판")

TEAM_FILE = "teams.json"

# 🔄 세션 상태 초기화
if "team_fixed" not in st.session_state:
    st.session_state.team_fixed = False
if "result_shown" not in st.session_state:
    st.session_state.result_shown = False
if "team1" not in st.session_state:
    st.session_state.team1 = []
if "team2" not in st.session_state:
    st.session_state.team2 = []
if "game_names" not in st.session_state:
    st.session_state.game_names = ["제기차기", "릴레이 달리기", "퀴즈쇼"]
if "games_fixed" not in st.session_state:
    st.session_state.games_fixed = False

# 📥 teams.json 불러오기
if os.path.exists(TEAM_FILE):
    with open(TEAM_FILE, "r", encoding="utf-8") as f:
        saved = json.load(f)
        st.session_state.team1 = saved.get("team1", [])
        st.session_state.team2 = saved.get("team2", [])
        st.session_state.team_fixed = saved.get("team_fixed", False)
        st.session_state.result_shown = saved.get("result_shown", False)
        st.session_state.game_names = saved.get("game_names", st.session_state.game_names)
        st.session_state.games_fixed = saved.get("games_fixed", False)

# 🎮 게임명 입력 UI
st.markdown("---")
st.subheader("🎮 참가 게임명 설정")

game_input = st.text_input(
    "게임명을 쉼표로 구분하여 입력하세요",
    ", ".join(st.session_state.game_names),
    disabled=st.session_state.games_fixed
)

col_fix, col_edit = st.columns([1, 1])

with col_fix:
    if st.button("✅ 게임명 확정", disabled=st.session_state.games_fixed):
        st.session_state.game_names = [g.strip() for g in game_input.split(",") if g.strip()]
        st.session_state.games_fixed = True

        saved_data = {}
        if os.path.exists(TEAM_FILE):
            with open(TEAM_FILE, "r", encoding="utf-8") as f:
                saved_data = json.load(f)

        saved_data["game_names"] = st.session_state.game_names
        saved_data["games_fixed"] = True

        with open(TEAM_FILE, "w", encoding="utf-8") as f:
            json.dump(saved_data, f, ensure_ascii=False, indent=2)

        st.rerun()

with col_edit:
    if st.button("✏️ 수정하기", disabled=not st.session_state.games_fixed):
        st.session_state.games_fixed = False

        # teams.json 파일도 수정
        if os.path.exists(TEAM_FILE):
            with open(TEAM_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["games_fixed"] = False
            with open(TEAM_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        st.rerun()


# 🎲 랜덤 팀 배정
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
            "result_shown": False,
            "team_fixed": True,
            "game_names": st.session_state.game_names,
            "games_fixed": st.session_state.games_fixed
        }, f, ensure_ascii=False, indent=2)
    st.rerun()

# 🔄 초기화
if st.button("🔄 팀 구성 초기화"):
    st.session_state.team_fixed = False
    st.session_state.result_shown = False
    st.session_state.games_fixed = False
    st.session_state.team1 = []
    st.session_state.team2 = []
    st.session_state.game_names = ["제기차기", "릴레이 달리기", "퀴즈쇼"]

    if os.path.exists(TEAM_FILE):
        os.remove(TEAM_FILE)

    st.rerun()

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

# 🏆 점수판 (게임 확정 후에만)
if st.session_state.games_fixed:
    st.header("🏆 게임 점수판")
    team1_total = 0
    team2_total = 0

    for game in st.session_state.game_names:
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

    if st.button("🎯 최종 결과 확정하기"):
        st.session_state.result_shown = True
        with open(TEAM_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "team1": st.session_state.team1,
                "team2": st.session_state.team2,
                "result_shown": True,
                "team_fixed": st.session_state.team_fixed,
                "game_names": st.session_state.game_names,
                "games_fixed": st.session_state.games_fixed
            }, f, ensure_ascii=False, indent=2)
        st.rerun()

    if st.session_state.result_shown:
        if team1_total > team2_total:
            st.success("🎉 **이사님 팀 우승!** 🥇")
        elif team2_total > team1_total:
            st.success("🎉 **실장님 팀 우승!** 🥇")
        else:
            st.info("🤝 **무승부입니다!**")
