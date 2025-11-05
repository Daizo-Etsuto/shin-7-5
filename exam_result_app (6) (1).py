import streamlit as st
from datetime import datetime, timezone, timedelta
import pandas as pd
import re

# 日本時間設定
JST = timezone(timedelta(hours=9))
start_time = datetime(2026, 1, 26, 14, 0, tzinfo=JST)
end_time = datetime(2026, 1, 31, 10, 0, tzinfo=JST)
now = datetime.now(JST)

st.set_page_config(page_title="船橋習志野エリア入塾テスト合否結果", page_icon="🔢")
st.markdown(
    "<h1 style='font-size:22px;'>📈 船橋習志野エリア入塾テスト合否結果</h1>",
    unsafe_allow_html=True
)
# 公開期間チェック
if now < start_time:
    st.warning(f"このページは {start_time.strftime('%Y/%m/%d %H:%M')} から公開されます。")
    st.stop()
elif now > end_time:
    st.warning(f"このページの公開期間は終了しました（{end_time.strftime('%Y/%m/%d %H:%M')} まで）。")
    st.stop()
else:
    st.markdown("""
    受験番号とパスワードを入力してください。  
    （※ 半角英数字のみ。有効な入力は自動的に大文字に変換されます）
    """)

    # CSV読み込み
    try:
        df = pd.read_csv("入塾テスト合否掲示用.csv", dtype=str)
        df = df.fillna('')
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"データファイルの読み込みに失敗しました: {e}")
        st.stop()

    # 必須列チェック
    required_cols = {"受験番号", "PW", "合否結果"}
    if not required_cols.issubset(set(df.columns)):
        st.error(f"CSVに必要な列が見つかりません。列名を確認してください。\n現在の列: {list(df.columns)}")
        st.stop()

    # 合否マークを柔軟に判定
    def get_message(mark):
        mark = str(mark).strip().replace("○", "〇")  # Unicode違いを吸収
        if mark in ["〇", "合格", "合"]:
            return "合格です。"
        elif mark in ["×", "不合格", "否"]:
            return "残念ながら、ご希望に添うことが出来ませんでした。"
        elif mark in ["△", "新津田沼", "津田沼"]:
            return "新津田沼教室で合格です。"
        else:
            return None

    # 入力欄
    exam_id_input = st.text_input("受験番号")
    pw_input = st.text_input("パスワード (PW)", type="password")

    def sanitize_input(text):
        return re.sub(r'[^A-Za-z0-9]', '', text.upper())

    exam_id = sanitize_input(exam_id_input)
    pw = sanitize_input(pw_input)

    if st.button("確認する"):
        if not exam_id or not pw:
            st.error("⚠️ 半角英数字で受験番号とパスワードを入力してください。")
        else:
            row = df[(df["受験番号"] == exam_id) & (df["PW"] == pw)]
            if not row.empty:
                mark = row.iloc[0]["合否結果"]
                message = get_message(mark)
                if message:
                    st.success(f"✅ 【結果】{message}")
                else:
                    st.error(f"⚠️ 合否結果の形式が不明です（値: {mark}）")
            else:
                st.error("⚠️ 受験番号あるいはパスワードが一致しません。")
