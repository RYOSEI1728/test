import streamlit as st
import numpy as np

# ゲームの初期設定
def initialize_board():
    board = np.full((8, 8), None)
    # 初期配置
    board[3, 3] = '白'
    board[3, 4] = '黒'
    board[4, 3] = '黒'
    board[4, 4] = '白'
    return board

# 駒をひっくり返す処理
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

# 空きマスに合法的に置けるか確認する処理
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

# ゲームの進行とUI
def play_game():
    # セッション状態の確認・初期化
    if 'board' not in st.session_state:
        st.session_state.board = initialize_board()
        st.session_state.current_player = '黒'  # 最初のプレイヤー
        st.session_state.turns = 0  # ターン数
        st.session_state.is_game_over = False  # ゲームオーバーのフラグ

    # ターン表示
    st.title(f"オセロ: {st.session_state.current_player}の番")
    st.write(f"ターン数: {st.session_state.turns}")

    # ボードの表示
    board_display = np.copy(st.session_state.board)
    for i in range(8):
        cols = st.columns(8)
        for j in range(8):
            if board_display[i, j] is None:
                cols[j].button(' ', key=f'{i}_{j}', disabled=True)  # 空白のセル
            else:
                cols[j].button(board_display[i, j], key=f'{i}_{j}', on_click=make_move, args=(i, j))

    # 勝敗の判定
    if st.session_state.is_game_over:
        st.write("ゲーム終了！")
        black_count = np.sum(st.session_state.board == '黒')
        white_count = np.sum(st.session_state.board == '白')
        if black_count > white_count:
            st.write(f"黒の勝ち！ {black_count} 対 {white_count}")
        elif black_count < white_count:
            st.write(f"白の勝ち！ {white_count} 対 {black_count}")
        else:
            st.write(f"引き分け！ {black_count} 対 {white_count}")
        if st.button("もう一度遊ぶ"):
            st.session_state.board = initialize_board()
            st.session_state.current_player = '黒'
            st.session_state.turns = 0
            st.session_state.is_game_over = False

# プレイヤーの手を処理する関数
def make_move(row, col):
    # 現在のプレイヤーの手を置ける場合
    if is_valid_move(st.session_state.board, row, col, st.session_state.current_player):
        st.session_state.board[row, col] = st.session_state.current_player
        flip_pieces(st.session_state.board, row, col, st.session_state.current_player)
        
        # 次のプレイヤーに交代
        st.session_state.current_player = '白' if st.session_state.current_player == '黒' else '黒'
        st.session_state.turns += 1

        # 勝利条件のチェック
        valid_moves = get_valid_moves(st.session_state.board, st.session_state.current_player)
        if not valid_moves:
            # 次のプレイヤーが置ける場所がなければゲーム終了
            st.session_state.is_game_over = True

# ゲームの開始
play_game()
