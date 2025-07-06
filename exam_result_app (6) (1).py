# app.py（合否データ + 公開期間 + 入力制限 + 図版 + 合格者GIF表示 + 日本時間対応）
import streamlit as st
from datetime import datetime, timezone, timedelta
import re

# 日本時間（JST: UTC+9）に設定
JST = timezone(timedelta(hours=9))
start_time = datetime(2025, 7, 7, 14, 00, tzinfo=JST)
end_time = datetime(2025, 7, 14, 10, 00, tzinfo=JST)
now = datetime.now(JST)

st.set_page_config(page_title="新津田沼教室入塾テスト合否結果", page_icon="🔢")
st.title("📈 新津田沼教室入塾テスト合否結果")

# 公開期間チェック
if now < start_time:
    st.warning(f"このページは {start_time.strftime('%Y/%m/%d %H:%M')}から公開されます。")
    st.stop()
elif now > end_time:
    st.warning(f"このページの公開期間は終了しました（{end_time.strftime('%Y/%m/%d %H:%M')} まで）。")
    st.stop()
else:
    st.markdown("""
    受験番号とパスワードを入力してください。
    （※ 半角英数字のみ、有効な入力は自動的に大文字に変換されます）
    """)

    # 合否データ（受験番号, パスワード） → 結果
    data = {
        ('9S601', '81070'): '合格です。',
        ('9C101', '25243'): '合格です',
        ('9C102', '77162'): '合格です。',
        ('9C201', '30555'): '合格です。',
        ('9C202', '16248'): '合格です。',
        ('9C06', '1239'): '残念ながら、ご希望に添うことが出来ませんでした。',
        ('9C07', '1240'): '合格です。',
        ('9C08', '1241'): '残念ながら、ご希望に添うことが出来ませんでした。',
    }

    # 入力欄
    exam_id_input = st.text_input("受験番号")
    password_input = st.text_input("パスワード", type="password")

    # 入力を大文字化・半角英数字のみに制限
    def sanitize_input(text):
        return re.sub(r'[^A-Za-z0-9]', '', text.upper())

    exam_id = sanitize_input(exam_id_input)
    password = sanitize_input(password_input)

    # ボタン押下で確認
    if st.button("確認する"):
        if not exam_id or not password:
            st.error("⚠️ 半角英数字で受験番号とパスワードを入力してください。")
        else:
            result = data.get((exam_id, password))
            if result:
                st.success(f"\u2705 【結果】{result}")
            else:
                st.error("⚠️ 受験番号あるいはパスワードが一致しません。")
