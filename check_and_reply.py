import os
import json
import random
import requests
from datetime import datetime

# 加载环境变量
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
TASK_KEYWORDS = os.getenv("TASK_KEYWORDS", "").split(",")

# 加载语录库
with open("praise_library.json", "r", encoding="utf-8") as f:
    praise_pool = json.load(f)

# 示例模拟数据：任务记录
# 实际使用时应该由其他模块写入，如领取/完成日志
task_log = {
    "2025-07-16": {
        "用户A": {
            "写作1000字": "完成",
            "番茄钟": "未完成"
        },
        "用户B": {
            "写作1000字": "完成"
        },
        "用户C": {
            "音乐": "未完成"
        }
    }
}

# 获取当天日期
today = datetime.now().strftime("%Y-%m-%d")

# 构造消息列表
messages = []

if today in task_log:
    for user, tasks in task_log[today].items():
        for task, status in tasks.items():
            if task not in TASK_KEYWORDS:
                continue
            if status == "完成":
                style = random.choice(list(praise_pool.keys()))
                quote = random.choice(praise_pool[style])
                messages.append(f"🎉 **{user}** 完成了任务【{task}】\n🧙 NPC评价：“{quote}”")
            else:
                messages.append(f"🕓 **{user}** 今天领取了【{task}】，但还未完成。继续加油，明天再战！")

# 发送到 Discord Webhook
if messages:
    content = "\n\n".join(messages)
    payload = { "content": content }
    response = requests.post(DISCORD_WEBHOOK, json=payload)
    print("发送结果：", response.status_code)
else:
    print("今日无结算内容。")