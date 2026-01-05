import streamlit as st
import numpy as np
import random

from constants import NUM_MAP


def initialize_session_state():

    if "status" not in st.session_state:
        st.session_state['status'] = None
    if "mine_coord" and "safe_coord" not in st.session_state:
        coords = [(i, j) for i in range(12) for j in range(12)]
        random.shuffle(coords)
        st.session_state['mine_coord'] = coords[:20]
        st.session_state['safe_coord'] = coords[20:]
    if "mines" not in st.session_state:
        st.session_state['mines'] = np.zeros((12, 12))
        for coord in st.session_state['mine_coord']:
            st.session_state['mines'][coord] = 1
    if "game_state" not in st.session_state:
        st.session_state['game_state']= np.zeros((12, 12))
    if "mark_state" not in st.session_state:
        st.session_state['mark_state'] = np.zeros((12, 12))     # 1 -> mine mark; 2 -> question mark
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
    if "mode" not in st.session_state:
        st.session_state['mode'] = 'play'


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



# initialize_session_state()


class MineSweeper:
    def __init__(self):
        pass

    def show_cell(self, row, col):
        """
        Docstring for show_cell

        :param row: row index
        :param col: column index
        """
        
        if st.session_state['game_state'][row, col] == 1:
            # * dug cells

            if st.session_state['mines'][row, col] == 0:
                # if not mine -> return the mine count in the proximity
                val = round(st.session_state['prox_mine_count'][row, col])
                return NUM_MAP[val]
            
            if st.session_state['mines'][row, col] == 1:
                return "💣"
        
        elif st.session_state['game_state'][row, col] == 2:
            # * sweeped mines
            return "✨"
        
        else:
            # * not dug cells
            if st.session_state['mark_state'][row, col] == 2:
                return "❓"
            elif st.session_state['mark_state'][row, col] == 1:
                return "🚩"
            else:
                return " "
            
        
        
    

    
        
    def dig_session_handle(self, row, col):
        # * reveal dug cell
        st.session_state['game_state'][row, col] = 1

        # * pop safe coordinates
        if (row, col) in st.session_state['safe_coord']:
            st.session_state['safe_coord'].remove((row, col))

        # * disable revealed cell
        st.session_state['disabled'][row, col] = True
    
    def dig(self, row, col):
        self.dig_session_handle(row, col)

        self.check_game_status()

        if st.session_state['status'] == False:
            # * if any mine is dug
            return
        if st.session_state['prox_mine_count'][row, col] > 0:
            # * if there is any mine in the proximity -> stop dig recursion
            return
        
        # * define the proximity indices
        prox_h, prox_v = [row-1, row, row+1], [col-1, col, col+1]

        # * check whether to dig the cells in the proximity
        for i in prox_h:
            if i < 0 or i > 11:                  # if index out of bound -> continue
                continue
            for j in prox_v:
                if j < 0 or j > 11:
                    continue

                # continue rules
                if ((st.session_state['mines'][i, j] == 1)            # if mine -> do not dig
                    or (st.session_state['game_state'][i, j] == 1)    # if already dug -> continue
                    or ((i != row) and (j != col))                    # only dig cells in thetop, buttom, left, and right
                    ):
                    continue

                if (st.session_state['prox_mine_count'][i, j] == 0):  # if there is no mine in the proximity -> recursion
                    self.dig(i, j)

                else:                                                 # otherwise, only dig the cell itself but not dig further
                    self.dig_session_handle(i, j)


    def mark_question(self, row, col):
        if st.session_state['mark_state'][row, col] == 0:
            st.session_state['mark_state'][row, col] = 2
        else:
            st.session_state['mark_state'][row, col] = 0
        st.session_state['mode'] = 'play'

    def mark_mine(self, row, col):
        if st.session_state['mark_state'][row, col] == 0:
            st.session_state['mark_state'][row, col] = 1
        else:
            st.session_state['mark_state'][row, col] = 0
        st.session_state['mode'] = 'play'


    def dig_or_mark_handler(self, row, col):
        if st.session_state['mode'] == 'play':
            self.dig(row, col)
        elif st.session_state['mode'] == 'mark_question':
            self.mark_question(row, col)
        elif st.session_state['mode'] == 'mark_mine':
            self.mark_mine(row, col)

    


    def check_game_status(self):
        # the condition means a mine has been revealed
        if any((st.session_state['game_state'] + st.session_state['mines'] == 2).flatten()):

            st.session_state['status'] = False        # * -> game over
            st.session_state['disabled'] = np.array([[True for _ in range(12)] for _ in range(12)]) # disable all cells

            # render all mines
            for i in range(12):
                for j in range(12):
                    if st.session_state['mines'][i, j] == 1:
                        st.session_state['game_state'][i, j] = 1
            st.snow()

        if st.session_state['score'] >= 124:          # * full score
            st.session_state['status'] = True
            st.balloons()



    def get_score(self): 
        # * score: the number of cells that are safely dug
        prev_score = st.session_state['score']
        new_score = np.sum(st.session_state['game_state'] * (1 - st.session_state['mines']))
        added_score = new_score - prev_score

        st.session_state['score'] = new_score
        st.session_state['score_bonus'] += added_score 

    def get_lucky_stars(self):
        # * every 10 point gain earns a lucky star
        if st.session_state['score_bonus'] >= 10:
            st.session_state['lucky_stars'] +=  min(st.session_state['score_bonus'] // 10, 5)
            st.session_state['score_bonus'] = st.session_state['score_bonus'] % 10

    def remove_a_mine(self):
        """
        consume a lucky star to randomly reveal a mine and disable it
        """
        if st.session_state['lucky_stars'] <= 0:
            st.toast("No lucky star left!", icon = '‼️')

        elif st.session_state['lucky_stars'] > 0:
            to_remove = random.randint(0, len(st.session_state['mine_coord']) - 1)   # get a random mine
            popped = st.session_state['mine_coord'].pop(to_remove)                   # pop the coordinate
            st.session_state['disabled'][popped] = True        # -> disable the mine
            st.session_state['game_state'][popped] = 2         # -> means 'shown' but 'not clicked'
            st.session_state['lucky_stars'] -= 1               # -> remove one lucky star
            st.rerun()

    # TODO Open save cell
    def open_a_safe_cell(self):
        """
        consume a lucky star to randomly dig a safe cell
        """
        if st.session_state['lucky_stars'] <= 0:
            st.toast("No lucky star left!", icon = '‼️')

        elif st.session_state['lucky_stars'] > 0:
            to_open = random.randint(0, len(st.session_state['safe_coord']) - 1)
            popped = st.session_state['safe_coord'].pop(to_open)
            self.dig(*popped)
            st.session_state['lucky_stars'] -= 1
            st.rerun()

    def board(self):
        """
        Render game board
        """
        for i in range(12):
            with st.container():
                COLS = st.columns(12, gap = 'small')
            for j in range(12):
                with COLS[j]:
                    st.button(f"{self.show_cell(i, j)}", 
                            key = f"{i}_{j}", 
                            disabled = st.session_state['disabled'][i, j], 
                            on_click = self.dig_or_mark_handler, args = (i, j),
                            type = 'secondary')
    
    
    



    
