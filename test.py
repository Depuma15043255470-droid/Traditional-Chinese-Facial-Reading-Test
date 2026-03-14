import cameradetection
import numpy as np
import facialkeypoints
import cv2
import bizi
import santing
import yanjing
import zuiba
cap = cv2.VideoCapture(0)
mtx_list=[]
dist_list=[]
mt_list,dis_list, = cameradetection.cameradetection(cap)
final_mtx = np.mean(mt_list, axis=0)
final_dist = np.mean(dis_list, axis=0)
cap = cv2.VideoCapture(0)
px_list,py_list,frame=facialkeypoints.facialkeypoints(cap,final_mtx,final_dist)
cv2.imshow("处理后的图像", frame)
bigao, biyi_kuan=bizi.bizi(px_list,py_list,final_mtx)
shangting, zhongting, xiating=santing.santing(px_list,py_list,final_mtx)
zuoyan_chang, yanju=yanjing.yanjing(px_list,py_list,final_mtx)
zuikuan=zuiba.zuiba(px_list,py_list,final_mtx)
# ==========================
# 面相自动判断逻辑（if 完整版）
# ==========================
result = ""

# ----------------------
# 1. 三庭判断（一生运势）
# ----------------------
total = shangting + zhongting + xiating
avg = total / 3

shangting_judge = abs(shangting - avg) < 2
zhongting_judge = abs(zhongting - avg) < 2
xiating_judge = abs(xiating - avg) < 2

if shangting_judge and zhongting_judge and xiating_judge:
    result += "三庭均衡：一生平稳，福禄双全，贵人运旺。\n"
elif zhongting > shangting and zhongting > xiating:
    result += "中庭偏长：中年事业发达，财运旺盛。\n"
elif xiating > shangting and xiating > zhongting:
    result += "下庭偏长：晚年享福，子女孝顺，家庭和睦。\n"
elif shangting > zhongting and shangting > xiating:
    result += "上庭偏长：天资聪明，早年运势佳，学业顺利。\n"
else:
    result += "三庭不均：运势起伏，需靠努力调整。\n"

# ----------------------
# 2. 鼻子判断（财运）
# ----------------------
if 40 <= bigao <= 55 and 35 <= biyi_kuan <= 45:
    result += "鼻子：财运极佳，聚财能力强，事业顺利。\n"
elif 35 <= bigao <= 60:
    result += "鼻子：财运平稳，正财稳定，努力可得财。\n"
else:
    result += "鼻子：财运波动，守财较难，需谨慎理财。\n"

# ----------------------
# 3. 眼睛判断（智慧、人缘）
# ----------------------
if 28 <= zuoyan_chang <= 35:
    result += "眼睛：聪慧敏锐，洞察力强，人缘好。\n"
else:
    result += "眼睛：心性单纯，情绪较直接。\n"

yanju_ideal = zuoyan_chang
if abs(yanju - yanju_ideal) < 3:
    result += "眼距适中：心胸开阔，一生贵人多。\n"
elif yanju > yanju_ideal + 3:
    result += "眼距偏宽：性格温和，待人宽厚。\n"
else:
    result += "眼距偏窄：心思细腻，做事专注。\n"

# ----------------------
# 4. 嘴巴判断（食禄、情感）
# ----------------------
if 40 <= zuikuan <= 55:
    result += "嘴巴：口才好，有福气，人缘极佳。\n"
else:
    result += "嘴巴：情感内敛，不喜多言，心思重。\n"
# ==========================
# 面相综合评分 0-100分 + 总结
# ==========================
score = 0

# 1. 三庭打分 (最高30分)
total = shangting + zhongting + xiating
avg = total / 3
if abs(shangting-avg)<2 and abs(zhongting-avg)<2 and abs(xiating-avg)<2:
    score += 30
elif zhongting > shangting and zhongting > xiating:
    score += 25
elif xiating > shangting and xiating > zhongting:
    score += 23
elif shangting > zhongting and shangting > xiating:
    score += 20
else:
    score += 10

# 2. 鼻子打分 (最高30分)
if 40 <= bigao <=55 and 35 <= biyi_kuan <=45:
    score +=30
elif 35<=bigao<=60:
    score +=20
else:
    score +=10

# 3. 眼睛打分 (最高25分)
if 28<=zuoyan_chang<=35:
    score +=15
else:
    score +=8

yanju_ideal = zuoyan_chang
if abs(yanju - yanju_ideal) <3:
    score +=10
else:
    score +=5

# 4. 嘴巴打分 (最高15分)
if 40<=zuikuan<=55:
    score +=15
else:
    score +=8

# 最终分数（限制0-100）
score = max(0, min(100, score))

# ==========================
# 自动生成总结评语
# ==========================
if score >= 85:
    summary = "综合评级：上上吉 → 富贵双全，人缘极佳，一生平顺，事业财运双旺！"
elif score >=70:
    summary = "综合评级：吉 → 运势良好，聪明稳重，努力即可成就一番事业。"
elif score >=55:
    summary = "综合评级：中平 → 一生平稳，无大风大浪，家庭安稳，知足常乐。"
elif score >=40:
    summary = "综合评级：普通 → 运势一般，需靠自身努力，踏实进取可保平安。"
else:
    summary = "综合评级：偏弱 → 早年多波折，中年后转稳，心善则福至。"
print("\n====== 面相分析结果 ======\n")
print(result)
print(f"最终面相评分：{score} 分")
print(summary)