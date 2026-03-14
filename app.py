import cv2
import numpy as np
import cameradetection
import facialkeypoints
import bizi
import santing
import yanjing
import zuiba
import streamlit as st
st.set_page_config(
    page_title="智能面相分析系统",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 侧边栏
st.sidebar.title("📋 操作菜单")
menu_option = st.sidebar.radio(
    "选择功能",
    ["系统介绍", "摄像头标定", "面相检测分析", "结果展示"]
)

# 初始化会话状态
if "calibration_done" not in st.session_state:
    st.session_state.calibration_done = False
if "mtx" not in st.session_state:
    st.session_state.mtx = None
if "dist" not in st.session_state:
    st.session_state.dist = None
if "face_data" not in st.session_state:
    st.session_state.face_data = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# 主页面内容
if menu_option == "系统介绍":
    st.title("👤 智能面相分析系统")
    st.markdown("""
    ### 系统简介
    本系统基于计算机视觉技术，通过摄像头采集面部图像，结合相机标定技术校正畸变，
    提取面部关键点并计算三庭、五官等特征参数，最终完成面相分析。

    ### 操作流程
    1. **摄像头标定**：使用棋盘格完成相机参数标定（需准备9×6棋盘格）
    2. **面相检测分析**：实时采集面部图像，提取关键点
    3. **结果展示**：查看详细的面相分析报告

    ### 技术说明
    - 相机标定：基于OpenCV实现，校正镜头畸变
    - 面部关键点：使用MediaPipe Face Mesh提取468个面部关键点
    - 尺寸转换：像素坐标转换为实际毫米尺寸
    - 面相分析：基于传统面相学的三庭五眼理论
    """)

    st.warning("⚠️ 开始分析前请先完成摄像头标定！")

elif menu_option == "摄像头标定":
    st.title("📷 摄像头标定")
    st.markdown("### 请准备9×6棋盘格，按以下步骤操作：")
    st.markdown("""
    1. 点击「开始标定」按钮启动摄像头
    2. 将棋盘格对准摄像头，按空格键采集标定图像（建议采集10-20张）
    3. 按ESC键结束采集并开始标定计算
    """)

    if st.button("🚀 开始标定", type="primary"):
        try:
            # 创建临时视频捕获对象
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("❌ 无法打开摄像头，请检查设备连接！")
            else:
                with st.spinner("正在采集标定图像...（按空格采集，ESC结束）"):
                    # 调用标定函数
                    mtx_list, dist_list = cameradetection.cameradetection(cap)

                    if len(mtx_list) > 0:
                        # 计算平均标定参数
                        st.session_state.mtx = np.mean(mtx_list, axis=0)
                        st.session_state.dist = np.mean(dist_list, axis=0)
                        st.session_state.calibration_done = True

                        st.success("✅ 摄像头标定完成！")
                        st.subheader("标定参数：")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("📐 相机内参矩阵：")
                            st.write(st.session_state.mtx)
                        with col2:
                            st.write("🔧 畸变系数：")
                            st.write(st.session_state.dist)
                    else:
                        st.error("❌ 未采集到有效标定图像，请重新尝试！")

                    cap.release()
                    cv2.destroyAllWindows()
        except Exception as e:
            st.error(f"❌ 标定过程出错：{str(e)}")

    if st.session_state.calibration_done:
        st.success("✅ 已完成摄像头标定，可以进入下一步面相检测！")

elif menu_option == "面相检测分析":
    st.title("👤 面部关键点检测与分析")

    if not st.session_state.calibration_done:
        st.error("❌ 请先完成摄像头标定！")
    else:
        st.markdown("### 检测步骤：")
        st.markdown("""
        1. 点击「开始检测」按钮启动摄像头
        2. 面对摄像头，保持面部清晰可见
        3. 按ESC键结束检测并开始分析
        """)

        if st.button("🎯 开始检测", type="primary"):
            try:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    st.error("❌ 无法打开摄像头，请检查设备连接！")
                else:
                    with st.spinner("正在检测面部关键点...（按ESC结束）"):
                        # 调用面部关键点检测函数
                        px_list, py_list, frame = facialkeypoints.facialkeypoints(
                            cap, st.session_state.mtx, st.session_state.dist
                        )

                        # 计算面相参数
                        bigao, biyi_kuan = bizi.bizi(px_list, py_list, st.session_state.mtx)
                        shangting, zhongting, xiating = santing.santing(px_list, py_list, st.session_state.mtx)
                        zuoyan_chang, yanju = yanjing.yanjing(px_list, py_list, st.session_state.mtx)
                        zuikuan = zuiba.zuiba(px_list, py_list, st.session_state.mtx)

                        # 保存数据到会话状态
                        st.session_state.face_data = {
                            "px_list": px_list,
                            "py_list": py_list,
                            "frame": frame,
                            "bigao": bigao,
                            "biyi_kuan": biyi_kuan,
                            "shangting": shangting,
                            "zhongting": zhongting,
                            "xiating": xiating,
                            "zuoyan_chang": zuoyan_chang,
                            "yanju": yanju,
                            "zuikuan": zuikuan
                        }

                        # 生成分析结果
                        result = ""
                        score = 0

                        # 1. 三庭判断
                        total = shangting + zhongting + xiating
                        avg = total / 3
                        shangting_judge = abs(shangting - avg) < 2
                        zhongting_judge = abs(zhongting - avg) < 2
                        xiating_judge = abs(xiating - avg) < 2

                        if shangting_judge and zhongting_judge and xiating_judge:
                            result += "三庭均衡：一生平稳，福禄双全，贵人运旺。\n"
                            score += 30
                        elif zhongting > shangting and zhongting > xiating:
                            result += "中庭偏长：中年事业发达，财运旺盛。\n"
                            score += 25
                        elif xiating > shangting and xiating > zhongting:
                            result += "下庭偏长：晚年享福，子女孝顺，家庭和睦。\n"
                            score += 23
                        elif shangting > zhongting and shangting > xiating:
                            result += "上庭偏长：天资聪明，早年运势佳，学业顺利。\n"
                            score += 20
                        else:
                            result += "三庭不均：运势起伏，需靠努力调整。\n"
                            score += 10

                        # 2. 鼻子判断
                        if 40 <= bigao <= 55 and 35 <= biyi_kuan <= 45:
                            result += "鼻子：财运极佳，聚财能力强，事业顺利。\n"
                            score += 30
                        elif 35 <= bigao <= 60:
                            result += "鼻子：财运平稳，正财稳定，努力可得财。\n"
                            score += 20
                        else:
                            result += "鼻子：财运波动，守财较难，需谨慎理财。\n"
                            score += 10

                        # 3. 眼睛判断
                        if 28 <= zuoyan_chang <= 35:
                            result += "眼睛：聪慧敏锐，洞察力强，人缘好。\n"
                            score += 15
                        else:
                            result += "眼睛：心性单纯，情绪较直接。\n"
                            score += 8

                        yanju_ideal = zuoyan_chang
                        if abs(yanju - yanju_ideal) < 3:
                            result += "眼距适中：心胸开阔，一生贵人多。\n"
                            score += 10
                        elif yanju > yanju_ideal + 3:
                            result += "眼距偏宽：性格温和，待人宽厚。\n"
                            score += 5
                        else:
                            result += "眼距偏窄：心思细腻，做事专注。\n"
                            score += 5

                        # 4. 嘴巴判断
                        if 40 <= zuikuan <= 55:
                            result += "嘴巴：口才好，有福气，人缘极佳。\n"
                            score += 15
                        else:
                            result += "嘴巴：情感内敛，不喜多言，心思重。\n"
                            score += 8

                        # 最终分数
                        score = max(0, min(100, score))

                        # 总结评语
                        if score >= 85:
                            summary = "综合评级：上上吉 → 富贵双全，人缘极佳，一生平顺，事业财运双旺！"
                        elif score >= 70:
                            summary = "综合评级：吉 → 运势良好，聪明稳重，努力即可成就一番事业。"
                        elif score >= 55:
                            summary = "综合评级：中平 → 一生平稳，无大风大浪，家庭安稳，知足常乐。"
                        elif score >= 40:
                            summary = "综合评级：普通 → 运势一般，需靠自身努力，踏实进取可保平安。"
                        else:
                            summary = "综合评级：偏弱 → 早年多波折，中年后转稳，心善则福至。"

                        st.session_state.analysis_result = {
                            "detail": result,
                            "score": score,
                            "summary": summary
                        }

                        st.success("✅ 面部检测与分析完成！")
                        cap.release()
                        cv2.destroyAllWindows()

                        # 跳转到结果展示
                        st.sidebar.radio(
                            "选择功能",
                            ["系统介绍", "摄像头标定", "面相检测分析", "结果展示"],
                            index=3
                        )

            except Exception as e:
                st.error(f"❌ 检测过程出错：{str(e)}")

elif menu_option == "结果展示":
    st.title("📊 面相分析结果")

    if st.session_state.face_data is None or st.session_state.analysis_result is None:
        st.error("❌ 暂无分析结果，请先完成面相检测！")
    else:
        # 提取数据
        face_data = st.session_state.face_data
        analysis_result = st.session_state.analysis_result

        # 分栏展示
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("📸 检测图像")
            # 转换图像格式
            frame = face_data["frame"]
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame_rgb, caption="面部关键点检测图像", use_column_width=True)

            st.subheader("📏 面部参数")
            st.write(f"鼻梁高度：{face_data['bigao']:.2f} mm")
            st.write(f"鼻翼宽度：{face_data['biyi_kuan']:.2f} mm")
            st.write(f"左眼长度：{face_data['zuoyan_chang']:.2f} mm")
            st.write(f"眼间距：{face_data['yanju']:.2f} mm")
            st.write(f"嘴宽：{face_data['zuikuan']:.2f} mm")
            st.write(f"上庭长度：{face_data['shangting']:.2f} mm")
            st.write(f"中庭长度：{face_data['zhongting']:.2f} mm")
            st.write(f"下庭长度：{face_data['xiating']:.2f} mm")

        with col2:
            st.subheader("📝 详细分析结果")
            st.text_area("分析详情", analysis_result["detail"], height=300)

            st.subheader("⭐ 综合评分")
            st.markdown(f"<h1 style='color: #1f77b4;'>{analysis_result['score']} 分</h1>", unsafe_allow_html=True)

            st.subheader("📜 综合评语")
            st.success(analysis_result["summary"])

            # 下载结果
            result_text = f"""
====== 智能面相分析报告 ======

【面部参数】
鼻梁高度：{face_data['bigao']:.2f} mm
鼻翼宽度：{face_data['biyi_kuan']:.2f} mm
左眼长度：{face_data['zuoyan_chang']:.2f} mm
眼间距：{face_data['yanju']:.2f} mm
嘴宽：{face_data['zuikuan']:.2f} mm
上庭长度：{face_data['shangting']:.2f} mm
中庭长度：{face_data['zhongting']:.2f} mm
下庭长度：{face_data['xiating']:.2f} mm

【详细分析】
{analysis_result['detail']}

【综合评分】：{analysis_result['score']} 分
【综合评语】：{analysis_result['summary']}
            """

            st.download_button(
                label="📥 下载分析报告",
                data=result_text,
                file_name="面相分析报告.txt",
                mime="text/plain"
            )
