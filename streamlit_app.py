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

    for dr, dc in directions:
        r, c = row + dr, col + dc
        flip_positions = []

        while 0 <= r < 8 and 0 <= c < 8 and board[r, c] == opponent:
            flip_positions.append((r, c))
            r += dr
            c += dc
        
        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] == player:
            for fr, fc in flip_positions:
                board[fr, fc] = player

# 空きマスに合法的に置けるか確認する関数
def is_valid_move(board, row, col, player):
    if board[row, col] is not None:
        return False
    opponent = '黒' if player == '白' else '白'
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    valid = False

    for dr, dc in directions:
        r, c = row + dr, col + dc
        flip_positions = []

        while 0 <= r < 8 and 0 <= c < 8 and board[r, c] == opponent:
            flip_positions.append((r, c))
            r += dr
            c += dc
        
        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] == player and flip_positions:
            valid = True

    return valid

# プレイヤーが置ける場所をリストアップ
def get_valid_moves(board, player):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, row, col, player):
                valid_moves.append((row, col))
    return valid_moves

# ゲームの進行
def play_game():
    board = initialize_board()
    player = '黒'  # 黒が先手
    turn = 1

    # StreamlitのUI部分
    st.title("オセロ（リバーシ）")

    # ボードの表示
    st.write(f"現在のターン: {player}の番")
    board_display = np.copy(board)
    for i in range(8):
        for j in range(8):
            if board_display[i, j] is None:
                board_display[i, j] = "空"
            st.text(board_display[i, j], width=3)

    # ユーザー入力（プレイヤーが駒を置く位置を選択）
    valid_moves = get_valid_moves(board, player)
    if valid_moves:
        st.write("以下の空いている場所に駒を置いてください:")
        for move in valid_moves:
            st.button(f"{move}", on_click=handle_move, args=(move,))

# 駒を置く処理
def handle_move(move):
    row, col = move
    if is_valid_move(board, row, col, player):
        board[row, col] = player
        flip_pieces(board, row, col, player)
        # プレイヤー交代
        player = '白' if player == '黒' else '黒'
