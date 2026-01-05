NUM_MAP = {
    0: " ",
    1: ":green[1]",
    2: ":blue[2]",
    3: ":orange[3]",
    4: ":red[4]",
    5: ":red[5]",
    6: ":red[6]",
    7: ":red[7]",
    8: ":red[8]"

}

class uiCont:

    langcaption = {
        'English': "You could select the language in the **side bar**.",
        '正體中文': "你可以在**側邊欄**中選擇語言。"
    }

    tabs = {
        'game': {
            'English': "Game",
            '正體中文': "遊戲畫面"
        },
        'rule': {
            'English': "Rule",
            '正體中文': "規則"
        }
    }

    metrics = {
        'score': {
            'English': "Score",
            '正體中文': "分數"
        }, 
        'lucky_stars': {
            'English': "Lucky stars",
            '正體中文': "幸運星星 :material/star:"
        }
    }

    btns = {
        'restart': {
            'English': "Restart",
            '正體中文': "重新開始"
        },
        'remove_a_mine': {
            'English': "Remove a mine",
            '正體中文': "掃雷"
        },
        'dig_a_safe_cell': {
            'English': "Dig a safe cell",
            '正體中文': "安全牌"
        },
        'mark_mine': {
            'English': ":material/flag: Mark Flag",
            '正體中文': ":material/flag: 標記旗子"
        },
        'mark_question': {
            'English': ":material/help: Mark Question",
            '正體中文': ":material/help: 標記問號"
        },
        'return_to_play': {
            'English': "cancel",
            '正體中文': "取消"
        } 
    }

    with open("rules/zhtw.md") as f:
        rule_zhtw = f.read()
    with open("rules/eng.md") as f:
        rule_en = f.read()
