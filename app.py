import streamlit as st
import numpy as np

from utils_st import render_sidebar, render_global_memory
from minesweeper import initialize_session_state, MineSweeper

st.divider()
st.title("Minesweeper")

st.set_page_config(page_title = "Minesweeper", 
                   page_icon = ":material/chess_king:", 
                   layout="centered", 
                   initial_sidebar_state = "auto", 
                   menu_items={
        'Get Help': None,
        'Report a bug': "mailto:huang0jin@gmail.com",
        'About': """
- Developed by - **[Wally, Huang Lin Chun](https://antique-turn-ad4.notion.site/Wally-Huang-Lin-Chun-182965318fa7804c86bdde557fa376f4)**"""
    })


# --------------------------------------------------------------------
# * Style setting
with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
# --------------------------------------------------------------------
# * Tabs
TAB_GAME, TAB_RULE = st.tabs(["遊戲畫面", "規則"])


# --------------------------------------------------------------------
# * Rule Description

with open("rules/zhtw.md") as f:
    zhtw = f.read()
with open("rules/eng.md") as f:
    en = f.read()

with TAB_RULE:
    st.subheader("**Rule Description 規則說明**")
    lang = st.pills("Language", ["English", "繁體中文"], default = '繁體中文')
    if lang == "English":
        st.markdown(en)
    else:
        st.markdown(zhtw)

# --------------------------------------------------------------------
# * Initialize game
initialize_session_state()
minesweeper = MineSweeper()


# --------------------------------------------------------------------
# * Get score and lucky stars, and check game status whenever the app is rerun
if st.session_state['status'] is None:
    minesweeper.get_score()
    minesweeper.get_lucky_stars()
    minesweeper.check_game_status()

with TAB_GAME:
# --------------------------------------------------------------------
# * Render core metrices
    C1, C2, C3, C4 = st.columns(4)
    with C1:
        st.metric("Score", int(st.session_state['score']), help = 'The number of safe cells that have been dug.')
    with C2:
        with st.container(key = "lucky_stars_container"):
        
            st.metric("Lucky stars", f"{int(st.session_state['lucky_stars'])}", help = 'The number of lucky stars that have not been used. You can use the lucky stars to remove a mine or dig a safe cell. You earn one lucky star whenever you earn 10 points.')
    with C3:
        st.metric("Safe Cells", len(st.session_state['safe_coord']), help = 'The number of safe cells that have not been dug.')
    with C4:
        st.metric("Left Mines", len(st.session_state['mine_coord']), help = 'The number of mines that have not been revealed.')

# --------------------------------------------------------------------
# * Render game board
    minesweeper.board()


# --------------------------------------------------------------------
# * Check game status 
    if st.session_state['status'] is None:
        L2, R2 = st.columns(2)
        with L2:
            if st.button(":material/cleaning_services: Remove a mine", type = "primary", width = "stretch", 
                        help = "Consume a lucky star and randomly reveal a mine and remove it."):
                minesweeper.remove_a_mine()
        with R2:
            if st.button(":material/adjust: Dig a safe cell", type = "primary", width = "stretch", 
                        help = "Consume a lucky star and randomly dig a safe cell."):
                minesweeper.open_a_safe_cell()


    elif st.session_state['status'] == False:
        if st.button("Restart", type = "primary", width = "stretch"):
            for _ in st.session_state:
                del st.session_state[_]
            st.rerun()
        st.error("**Game Over!**")

    elif st.session_state['status'] == True:
        
        if st.button("Restart", type = "primary", width = "stretch"):
            for _ in st.session_state:
                del st.session_state[_]
            st.rerun()
        st.success("You Sweeped All Mines!")
    
