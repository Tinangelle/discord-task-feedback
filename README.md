# 🎯 Discord 任务反馈系统（Task Feedback System）

> 自动读取 Discord 频道消息，识别任务完成内容并生成 JSON 日志，支持后续扩展为奖励机制、NPC夸奖、称号系统等。

---

## 📌 项目功能概述

- 每小时自动运行脚本
- 读取 Discord 指定频道中用户发言
- 检测是否包含任务关键词（如“完成 写作1000字”）
- 写入 `task_log.json` 作为任务完成记录
- 自动推送 commit 到 GitHub 仓库

---

## ⚙️ 使用的技术与工具

- GitHub Actions：定时运行任务
- Python：处理消息与生成 JSON 文件
- Discord Bot Token（后台读取消息）
- GitHub Personal Access Token（写入仓库）

---

## 🗂️ 项目结构说明

