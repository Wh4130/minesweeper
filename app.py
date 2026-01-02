import streamlit as st
import numpy as np

from utils_st import render_sidebar, render_global_memory
from minesweeper import initialize_session_state, board, get_score, get_lucky_stars, remove_a_mine

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

with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

initialize_session_state()


if st.session_state['status'] is None:
    get_score()   
    get_lucky_stars()

L, R = st.columns(2)
with L:
    st.metric("Score", st.session_state['score'])
with R:
    st.metric("Lucky stars", st.session_state['lucky_stars'])


board()

if st.session_state['status'] is None:
    if st.button(":material/cleaning_services: Remove a mine", type = "primary", width = "stretch", 
                help = "Consume a sweeper and randomly reveal a mine and remove it."):
        remove_a_mine()

elif st.session_state['status'] == False:
    if st.button("Restart", type = "primary", width = "stretch"):
        for _ in st.session_state:
            del st.session_state[_]
        st.rerun()
    st.error("**Game Over!**")

elif st.session_state['status'] == True:
    st.success("You Sweeped All Mines!")
    
