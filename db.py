import PyInstaller.__main__

PyInstaller.__main__.run([
    "main.py",
    "--onefile",          # 打包成单个exe
    "--windowed",         # 不显示黑窗口
    "--collect-all", "streamlit",  # 关键！必须分开写
    "--collect-all", "cv2",
    "--collect-all", "mediapipe",
    "--collect-all", "numpy",
])