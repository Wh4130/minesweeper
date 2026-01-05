import streamlit as st
import numpy as np

from utils_st import render_sidebar
from constants import uiCont
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
    
render_sidebar()


# --------------------------------------------------------------------
# * Initialize game
if "lang" not in st.session_state:
    st.session_state['lang'] = "正體中文"
initialize_session_state()
minesweeper = MineSweeper()

if st.session_state['mode'] != 'play':
    st.markdown("""<style>[data-testid="stBaseButton-secondary"] {
    background-color: #edf8ef !important; /* Red background */
}
[data-testid="stBaseButton-secondary"]:disabled {
    background-color: #dbf2dd !important; /* Red background */
}</style>""", unsafe_allow_html = True)

# --------------------------------------------------------------------
# * Tabs
TAB_GAME, TAB_RULE = st.tabs([
    uiCont.tabs['game'][st.session_state['lang']], 
    uiCont.tabs['rule'][st.session_state['lang']]
    ])


# --------------------------------------------------------------------
# * Rule Description

with open("rules/zhtw.md") as f:
    zhtw = f.read()
with open("rules/eng.md") as f:
    en = f.read()

with TAB_RULE:
    st.subheader("**Rule Description 規則說明**")
    if st.session_state['lang'] == "English":
        st.markdown(uiCont.rule_en)
    else:
        st.markdown(uiCont.rule_zhtw)

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
        st.metric(uiCont.metrics['score'][st.session_state['lang']], int(st.session_state['score']))
    with C2:
        with st.container(key = "lucky_stars_container"):
        
            st.metric(uiCont.metrics['lucky_stars'][st.session_state['lang']], f"{int(st.session_state['lucky_stars'])}")
    

# --------------------------------------------------------------------
# * Render game board
    minesweeper.board()


# --------------------------------------------------------------------
# * Check game status 
    if st.session_state['status'] is None:
        with C3:

            # * 掃雷按鈕
            if st.button(":material/cleaning_services: " + uiCont.btns['remove_a_mine'][st.session_state['lang']],
                type = "primary", 
                width = "stretch"):
                    minesweeper.remove_a_mine()
            
            if st.session_state['mode'] == 'play':
                if st.button(uiCont.btns['mark_mine'][st.session_state['lang']],
                    type = 'tertiary', width = 'stretch'):
                    st.session_state['mode'] = 'mark_mine'
                    st.rerun()
            elif st.session_state['mode'] == 'mark_mine':
                if st.button(uiCont.btns['return_to_play'][st.session_state['lang']],
                    type = 'tertiary', width = 'stretch'):
                    st.session_state['mode'] = 'play'
                    st.rerun()
            st.space()


        with C4:

            # * 安全牌按鈕
            if st.button(":material/right_click: " + uiCont.btns['dig_a_safe_cell'][st.session_state['lang']],
                    type = "primary", 
                    width = "stretch"):
                    minesweeper.open_a_safe_cell()

            if st.session_state['mode'] == 'play':
                if st.button(uiCont.btns['mark_question'][st.session_state['lang']],
                    type = 'tertiary', width = 'stretch'):
                    st.session_state['mode'] = 'mark_question'
                    st.rerun()
            elif st.session_state['mode'] == 'mark_question':
                if st.button(uiCont.btns['return_to_play'][st.session_state['lang']],
                    type = 'tertiary', width = 'stretch', key = 'return_to_play_q'):
                    st.session_state['mode'] = 'play'
                    st.rerun()

            # if st.button(uiCont.btns['mark_question'][st.session_state['lang']],
            #      type = 'tertiary', width = 'stretch'):
            #     pass

    elif st.session_state['status'] == False:
        if st.button(":material/restart_alt: " + uiCont.btns['restart'][st.session_state['lang']],
                      type = "primary", 
                      width = "stretch"):
            for _ in st.session_state:
                del st.session_state[_]
            st.rerun()
        st.error("**Game Over!**")

    elif st.session_state['status'] == True:
        
        if st.button(":material/restart_alt: " + uiCont.btns['restart'][st.session_state['lang']],
                      type = "primary", 
                      width = "stretch"):
            for _ in st.session_state:
                del st.session_state[_]
            st.rerun()
        st.success("You Sweeped All Mines!")
    
