# streamlit_app/app.py

import streamlit as st
import requests

st.set_page_config(page_title="PDF要約アプリ", layout="centered")

st.title("📄 PDF要約アプリ")
st.write("PDFファイルをアップロードすると、その内容を要約します。")

# アップロード
uploaded_file = st.file_uploader("PDFファイルを選択してください", type="pdf")

# APIのURL（ngrokなどで公開されたFastAPIのURLに変更してください）
API_URL = "https://your-ngrok-url.ngrok.io/summarize"  # ★ここを実行時に貼り替える

if uploaded_file is not None:
    if st.button("要約する"):
        with st.spinner("要約中...お待ちください"):
            try:
                # FastAPIへリクエスト
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(API_URL, files={"file": uploaded_file})

                if response.status_code == 200:
                    summary = response.json().get("summary", "")
                    st.subheader("📝 要約結果")
                    st.write(summary)
                else:
                    st.error(f"エラーが発生しました: {response.status_code}")
                    st.json(response.json())

            except Exception as e:
                st.error(f"通信エラー: {e}")
