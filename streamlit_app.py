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
