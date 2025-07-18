import json
import requests
import datetime

# 读取鼓励语库
with open("praise_library.json", "r", encoding="utf-8") as f:
    praise_data = json.load(f)

# 读取任务日志
with open("task_log.json", "r", encoding="utf-8") as f:
    task_log = json.load(f)

# Webhook 设置
WEBHOOK_URL = "https://discord.com/api/webhooks/1395086102133735624/o_Ty8X_6hOl9MDlZVkeHb9M-oTEiaOApB4ovGATenj49toWV84o-UzX1gYsjpOS0jcGc"

# 获取今天日期字符串
today_str = datetime.datetime.now().strftime("%Y-%m-%d")

# 记录已处理的用户-任务
already_rewarded = set()

# 遍历日志并找出今天完成的任务
for entry in task_log:
    if entry["date"] != today_str:
        continue

    user = entry["user"]
    task = entry["task"]
    key = f"{user}-{task}"

    if key in already_rewarded:
        continue
    already_rewarded.add(key)

    # 获取一条对应任务的夸奖语
    praise_list = praise_data.get(task, praise_data.get("默认", []))
    praise = praise_list[hash(key) % len(praise_list)] if praise_list else "干得不错！"

    # 构造消息
    message = {
        "username": "结算小账房",
        "avatar_url": "https://cdn.discordapp.com/embed/avatars/4.png",
        "content": f"🎉 <@{user}> 完成了任务【{task}】\n🧙 NPC评语：「{praise}」"
    }

    # 发送 webhook 消息
    response = requests.post(WEBHOOK_URL, json=message)
    if response.status_code != 204:
        print(f"发送失败：{response.status_code}, {response.text}")
