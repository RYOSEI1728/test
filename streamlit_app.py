import streamlit as st
import numpy as np
import random

# ゲームの初期設定
def initialize_game():
    # カードのペアを用意する（2つずつ同じ数字を持つ）
    cards = [i for i in range(1, 9)] * 2  # 1~8のペア
    random.shuffle(cards)  # シャッフルしてランダム化
    board = np.array(cards).reshape(4, 4)  # 4x4のボードにする
    return board

# ゲームの状態をリセット
def reset_game():
    st.session_state.board = initialize_game()  # 新しいボードを初期化
    st.session_state.flipped = np.full((4, 4), False)  # 全てのカードは裏向き
    st.session_state.matched = []  # 一度ペアになったカードの位置
    st.session_state.turns = 0  # ターン数
    st.session_state.first_card = None  # 最初にめくったカード
    st.session_state.is_game_over = False  # ゲームオーバーかどうか

# カードをめくった後の処理
def flip_card(row, col):
    # 最初のカードをめくる
    if st.session_state.first_card is None:
        st.session_state.first_card = (row, col)
        st.session_state.flipped[row, col] = True
        return
    
    # 2枚目のカードをめくる
    first_row, first_col = st.session_state.first_card
    if st.session_state.board[first_row, first_col] == st.session_state.board[row, col]:
        st.session_state.matched.append((first_row, first_col, row, col))  # ペアが合ったカード
        st.session_state.flipped[row, col] = True
        st.session_state.first_card = None
    else:
        st.session_state.flipped[first_row, first_col] = False
        st.session_state.flipped[row, col] = True
        st.session_state.first_card = None

    st.session_state.turns += 1

    # ゲームオーバー条件を確認
    if len(st.session_state.matched) == 8:
        st.session_state.is_game_over = True

# ゲームを再開する処理
def game_ui():
    if 'board' not in st.session_state:
        reset_game()

    board = st.session_state.board
    flipped = st.session_state.flipped

    st.title("真剣衰弱 (Memory Game)")

    # ゲーム終了時の表示
    if st.session_state.is_game_over:
        st.success(f"ゲーム終了！ターン数: {st.session_state.turns}回")
        if st.button("もう一度遊ぶ"):
            reset_game()
        return

    st.write(f"ターン: {st.session_state.turns}回")

    # ボードの表示
    for i in range(4):
        cols = st.columns(4)
        for j in range(4):
            if flipped[i, j]:
                # 裏向きではなく、カードが表になっているとき
                cols[j].button(f'{board[i, j]}', key=f"{i}_{j}")
            else:
                # 裏向きカード
                cols[j].button('?', key=f"{i}_{j}_hidden", on_click=flip_card, args=(i, j))

# ゲーム開始
game_ui()
