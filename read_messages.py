import os
import requests
import json
from datetime import datetime

# 读取必要变量
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("SUBMISSION_CHANNEL_ID")
TASK_KEYWORDS = os.getenv("TASK_KEYWORDS", "").split(",")

HEADERS = {
    "Authorization": f"Bot {BOT_TOKEN}"
}

# 获取最近 100 条消息
def fetch_messages(channel_id):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=100"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"获取消息失败: {response.status_code}")
        return []

# 分析消息内容并更新日志
def update_task_log(messages, keywords):
    today = datetime.now().strftime("%Y-%m-%d")
    task_log = {}
    log_file = "task_log.json"

    # 加载旧记录
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            task_log = json.load(f)

    if today not in task_log:
        task_log[today] = {}

    for msg in messages:
        content = msg["content"]
        username = msg["author"]["username"]

        for keyword in keywords:
            if f"领取 {keyword}" in content:
                task_log[today].setdefault(username, {})[keyword] = "已领取"
            elif f"完成 {keyword}" in content:
                task_log[today].setdefault(username, {})[keyword] = "完成"

    # 保存更新
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(task_log, f, ensure_ascii=False, indent=2)

# 主流程
msgs = fetch_messages(CHANNEL_ID)
update_task_log(msgs, TASK_KEYWORDS)