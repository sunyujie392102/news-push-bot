# 每日新闻简报推送 Bot

每天早上 **北京时间 07:00**，自动抓取前一天《新闻联播》要闻，通过 **PushPlus** 推送到你的微信。

## 功能

- 自动抓取 [timelines.cn](https://www.timelines.cn) 新闻联播要闻
- 格式化为简报（12条新闻 + 心语）
- 通过 PushPlus 免费推送到微信通知

## 部署步骤

### 1. 创建 GitHub 仓库

```bash
# 在 GitHub 上创建一个名为 news-push-bot 的公开仓库
# 然后本地执行：
git init
git add .
git commit -m "init: 新闻简报推送bot"
git remote add origin https://github.com/你的用户名/news-push-bot.git
git push -u origin main
```

### 2. 配置 PushPlus Token（Secret）

1. 打开你的 GitHub 仓库页面
2. **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. Name 填：`PUSHPLUS_TOKEN`
5. Value 填：`d5c5c541e5634ce7b46ac62406b51dbc`
6. 点击 **Add secret**

### 3. 启用 GitHub Actions

1. 进入仓库 **Actions** 标签页
2. 点击 **"每日新闻简报推送"** workflow
3. 点击 **Enable workflow**

### 4. 手动测试

进入 **Actions** → 选择 workflow → **Run workflow** → 点击 **Run**

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `.github/workflows/push.yml` | GitHub Actions 定时任务配置 |
| `news_push.py` | 主脚本：抓取 → 格式化 → 推送 |
| `README.md` | 本文件 |

## 定时说明

- **Cron 表达式**：`0 23 * * *`（UTC 时间）
- **对应北京时间**：每天 **07:00**
- 可在 Actions 页面手动触发测试

## 常见问题

**Q：收不到推送？**
A：检查 PushPlus Token 是否正确、是否已完成实名认证。

**Q：GitHub Actions 免费额度够用吗？**
A：完全够用，每月 2000 分钟，这个脚本每次运行 < 1 分钟。

**Q：如何修改推送时间？**
A：修改 `.github/workflows/push.yml` 中的 cron 表达式，北京时间 = UTC + 8 小时。
