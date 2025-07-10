import streamlit as st
import numpy as np

# 初期のオセロボード設定
def initialize_board():
    board = np.full((8, 8), None)
    # 初期配置
    board[3, 3] = '白'
    board[3, 4] = '黒'
    board[4, 3] = '黒'
    board[4, 4] = '白'
    return board

# 駒をひっくり返す関数
def flip_pieces(board, row, col, player):
    opponent = '黒' if player == '白' else '白'
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
