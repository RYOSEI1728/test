import streamlit as st
import random

# ジャンケンの手を定義
hands = ["グー", "チョキ", "パー"]

# ストリームリットアプリのタイトル
st.title("ジャンケンゲーム")

# ユーザーが選ぶ手を選択するためのボタン
user_choice = st.radio("あなたの手を選んでください:", hands)

# コンピュータの手をランダムに選ぶ
computer_choice = random.choice(hands)

# ゲームの進行ボタン
if st.button("ジャンケン！"):
    # 結果を表示
    st.write(f"あなたの手: {user_choice}")
    st.write(f"コンピュータの手: {computer_choice}")
    
    # 勝敗を判定
    if user_choice == computer_choice:
        result = "引き分け"
    elif (user_choice == "グー" and computer_choice == "チョキ") or \
         (user_choice == "チョキ" and computer_choice == "パー") or \
         (user_choice == "パー" and computer_choice == "グー"):
        result = "あなたの勝ち！"
    else:
        result = "コンピュータの勝ち！"

    st.write(f"結果: {result}")
