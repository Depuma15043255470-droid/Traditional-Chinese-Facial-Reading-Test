import sys
from threading import Timer
import streamlit.web.cli as st_cli
import webbrowser

def open_browser():
    url = "http://localhost:8501"  # Streamlit默认地址
    webbrowser.open(url)
if __name__ == '__main__':
    Timer(1.5, open_browser).start()
    sys.argv = ["streamlit", "run", "app.py", "--server.headless", "true", "--global.developmentMode", "false"]
    st_cli.main()
