import streamlit as st
from datetime import datetime, timezone, timedelta
import pandas as pd
import re

# 日本時間（JST: UTC+9）に設定
JST = timezone(timedelta(hours=9))
start_time = datetime(2025, 7, 7, 11, 00, tzinfo=JST)
end_time = datetime(2025, 11, 14, 10, 00, tzinfo=JST)
now = datetime.now(JST)

st.set_page_config(page_title="船橋習志野エリア入塾テスト合否結果", page_icon="🔢")
st.title("📈 船橋習志野エリア入塾テスト合否結果")

# 公開期間チェック
if now < start_time:
    st.warning(f"このページは {start_time.strftime('%Y/%m/%d %H:%M')}から公開されます。")
    st.stop()
elif now > end_time:
    st.warning(f"このページの公開期間は終了しました（{end_time.strftime('%Y/%m/%d %H:%M')} まで）。")
    st.stop()
else:
    st.markdown("""
    受験番号とIDを入力してください。
    （※ 半角英数字のみ、有効な入力は自動的に大文字に変換されます）
    """)

    # CSVファイルの読み込み
    try:
        df = pd.read_csv("入塾テスト合否掲示用.csv", dtype=str)
        df = df.fillna('')
    except Exception as e:
        st.error(f"データファイルの読み込みに失敗しました: {e}")
        st.stop()

    # 合否マークをメッセージに変換
    def get_message(mark):
        if mark == "〇":
            return "合格です。"
        elif mark == "×":
            return "残念ながら、ご希望に添うことが出来ませんでした。"
        elif mark == "△":
            return "新津田沼教室で合格です。"
        else:
            return None

    # 入力欄
    exam_id_input = st.text_input("受験番号")
    id_input = st.text_input("PW", type="password")

    # 入力を大文字化・半角英数字のみに制限
    def sanitize_input(text):
        return re.sub(r'[^A-Za-z0-9]', '', text.upper())

    exam_id = sanitize_input(exam_id_input)
    user_id = sanitize_input(id_input)

    # ボタン押下で確認
    if st.button("確認する"):
        if not exam_id or not user_id:
            st.error("⚠️ 半角英数字で受験番号とPWを入力してください。")
        else:
            # 入力一致データ検索
            row = df[(df["受験番号"] == exam_pw) & (df["PW"] == user_pw)]
            if not row.empty:
                mark = row.iloc[0]["合否結果"]
                message = get_message(mark)
                if message:
                    st.success(f"✅ 【結果】{message}")
                else:
                    st.error("⚠️ 合否結果の形式が不明です。")
            else:
                st.error("⚠️ 受験番号あるいはPWが一致しません。")
