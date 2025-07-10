import streamlit as st
import numpy as np

# チェスボードの初期設定
def initialize_board():
    board = np.array([
        ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
        ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
        ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
    ])
    return board

# 駒を移動する関数
def move_piece(board, start_row, start_col, end_row, end_col):
    board[end_row, end_col] = board[start_row, start_col]
    board[start_row, start_col] = ' '

# UIの表示
def display_board(board):
    st.write("### チェスボード")
    for row in range(8):
        cols = st.columns(8)
        for col in range(8):
            piece = board[row, col]
            cols[col].button(piece, key=f"{row}_{col}", on_click=select_piece, args=(row, col))

# 駒の選択と移動処理
def select_piece(row, col):
    if 'selected_piece' not in st.session_state:
        st.session_state.selected_piece = (row, col)
    else:
        start_row, start_col = st.session_state.selected_piece
        # 移動する
        move_piece(st.session_state.board, start_row, start_col, row, col)
        # 選択を解除
        del st.session_state.selected_piece
        # ターンを更新
        st.session_state.turn = '黒' if st.session_state.turn == '白' else '白'
        st.session_state.turns += 1

# ゲーム進行
def play_game():
    # セッション状態の確認・初期化
    if 'board' not in st.session_state:
        st.session_state.board = initialize_board()
        st.session_state.turn = '白'  # 最初のプレイヤー
        st.session_state.turns = 0  # ターン数

    # ゲームタイトル
    st.title(f"チェスゲーム: {st.session_state.turn}の番")
    st.write(f"ターン数: {st.session_state.turns}")

    # チェスボードの表示
    display_board(st.session_state.board)

    # ゲームが進行中の場合
    st.write(f"現在のターン: {st.session_state.turn}")

# ゲーム開始
play_game()
