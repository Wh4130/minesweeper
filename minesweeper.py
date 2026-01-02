import streamlit as st
import numpy as np
import random

NUM_MAP = {
    0: " ",
    1: ":green[1]",
    2: ":blue[2]",
    3: ":orange[3]",
    4: ":red[4]"

}

def initialize_session_state():

    if "status" not in st.session_state:
        st.session_state['status'] = None
    if "mine_coord" not in st.session_state:
        coords = [(i, j) for i in range(12) for j in range(12)]
        random.shuffle(coords)
        st.session_state['mine_coord'] = coords[:20]
    if "mines" not in st.session_state:
        st.session_state['mines'] = np.zeros((12, 12))
        for coord in st.session_state['mine_coord']:
            st.session_state['mines'][coord] = 1
    if "game_state" not in st.session_state:
        st.session_state['game_state']= np.zeros((12, 12))
    if "disabled" not in st.session_state:
        st.session_state['disabled'] = np.array([[False for _ in range(12)] for _ in range(12)])
    if "prox_mine_count" not in st.session_state:
        st.session_state['prox_mine_count']= np.zeros((12, 12))
    if "score" not in st.session_state:
        st.session_state['score'] = 0
    if "score_bonus" not in st.session_state:
        st.session_state['score_bonus'] = 0
    if "lucky_stars" not in st.session_state:
        st.session_state['lucky_stars'] = 0


    # * update prox_mine_count
    for r in range(12):
        for c in range(12):
            count = 0
            prox_h, prox_v = [r-1, r, r+1], [c-1, c, c+1]

            for i in prox_h:
                if i < 0 or i > 11:
                    continue
                for j in prox_v:
                    if j < 0 or j > 11:
                        continue

                    if st.session_state['mines'][i, j] == 1:
                        count += 1
            
            st.session_state['prox_mine_count'][r, c] = count
            if st.session_state['mines'][r, c] == 1: 
                # * if there's mine on the coordinate, do not calculate the mine counts in the proximity
                st.session_state['prox_mine_count'][r, c] = 0



initialize_session_state()

def show_cell(row, col):
    if st.session_state['game_state'][row, col] == 1:

        if st.session_state['mines'][row, col] == 0:
            val = round(st.session_state['prox_mine_count'][row, col])
            return NUM_MAP[val]
        
        if st.session_state['mines'][row, col] == 1:
            return "💣"
    
    elif st.session_state['game_state'][row, col] == 2:
        return "✨"
    else:
        return " "
    
def dig(row, col):
    st.session_state['game_state'][row, col] = 1
    st.session_state['disabled'][row, col] = True
    check_game_status()

    if st.session_state['status'] == False:
        return
    if st.session_state['prox_mine_count'][row, col] > 0:
        return
        
    prox_h, prox_v = [row-1, row, row+1], [col-1, col, col+1]


    for i in prox_h:
        if i < 0 or i > 11:
            continue
        for j in prox_v:
            if j < 0 or j > 11:
                continue

            # continue rules
            if ((st.session_state['mines'][i, j] == 1)
                or (st.session_state['game_state'][i, j] == 1)
                or ((i != row) and (j != col))
                ):
                continue

            if (st.session_state['prox_mine_count'][i, j] == 0):
                # ** Recursion
                dig(i, j)

            else:
                st.session_state['game_state'][i, j] = 1
                st.session_state['disabled'][i, j] = True

def check_game_status():
    # the condition means a mine has been revealed
    if any((st.session_state['game_state'] + st.session_state['mines'] == 2).flatten()):
        st.session_state['status'] = False
        st.session_state['disabled'] = np.array([[True for _ in range(12)] for _ in range(12)])

        # render all mines
        for i in range(12):
            for j in range(12):
                if st.session_state['mines'][i, j] == 1:
                    st.session_state['game_state'][i, j] = 1
        st.snow()
    if st.session_state['score'] == 124:
        st.balloons()
        st.session_state['status'] = True


def get_score(): 
    prev_score = st.session_state['score']
    new_score = np.sum(st.session_state['game_state'] * (1 - st.session_state['mines']))
    added_score = new_score - prev_score

    st.session_state['score'] = new_score
    st.session_state['score_bonus'] += added_score 

def get_lucky_stars():
    if st.session_state['score_bonus'] >= 10:
        st.session_state['lucky_stars'] +=  min(st.session_state['score_bonus'] // 10, 5)
        st.session_state['score_bonus'] = st.session_state['score_bonus'] % 10

def remove_a_mine():
    if st.session_state['lucky_stars'] <= 0:
        st.error("No lucky star left!")

    elif st.session_state['lucky_stars'] > 0:
        to_remove = random.randint(0, len(st.session_state['mine_coord']) - 1)
        popped = st.session_state['mine_coord'].pop(to_remove)
        st.session_state['disabled'][popped] = True        # -> disable the mine
        st.session_state['game_state'][popped] = 2         # -> means 'shown' but 'not clicked'
        st.session_state['lucky_stars'] -= 1               # -> remove one lucky star
        st.rerun()

# TODO Open save cell

def board():
    for i in range(12):
        with st.container():
            COLS = st.columns(12, gap = 'small')
        for j in range(12):
            with COLS[j]:
                st.button(f"{show_cell(i, j)}", 
                        key = f"{i}_{j}", 
                        disabled = st.session_state['disabled'][i, j], 
                        on_click = dig, args = (i, j))
    
    
    



    
