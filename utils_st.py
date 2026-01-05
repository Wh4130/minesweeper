import streamlit as st
import pandas as pd
import time
import datetime as dt
import json
from typing import List, Callable, Dict, Any, Tuple, Optional


def render_sidebar():
    """
    Render a streamlit sidebar

    """
    with st.sidebar:
        st.header("Minesweeper 踩地雷")
        st.caption("升級版踩地雷！")
        # st.logo("assets/icon.png", size = 'large')

        with st.container():
            st.subheader(":material/settings: **Setting**")
            st.session_state['lang'] = st.pills("Language", ["English", "正體中文"], default = "正體中文")
            

       

