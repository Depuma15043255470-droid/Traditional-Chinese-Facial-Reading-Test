import streamlit as st
import webbrowser
from threading import Timer
import subprocess
import sys

# 只打开一次浏览器
if __name__ == "__main__":
    if not st.session_state.get('browser_opened', False):
        def open_browser():
            webbrowser.open("http://localhost:8501")
            st.session_state.browser_opened = True

        Timer(1, open_browser).start()

    # 启动 streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", __file__])