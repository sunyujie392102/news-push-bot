#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新闻简报推送脚本
从 GitHub Actions 定时运行，通过 PushPlus 推送到微信
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sys

# ========== 配置 ==========
PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN", "d5c5c541e5634ce7b46ac62406b51dbc")
PUSHPLUS_API = "http://www.pushplus.plus/send"

# 农历映射（每年初补充）
LUNAR_MAP = {
    "0101": "腊月初二", "0517": "四月初一", "0518": "四月初二",
    "0519": "四月初三", "0520": "四月初四", "0521": "四月初五",
    "0601": "四月十六", "0616": "五月初一", "0617": "五月初二",
    "0618": "五月初三", "0619": "五月初四", "0620": "五月初五",
    "0701": "五月十六", "0715": "五月三十", "0716": "六月初一",
}
WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


# ========== 日期 ==========
def get_yesterday_info():
    yesterday = datetime.now() - timedelta(days=1)
    return {
        "date_str": yesterday.strftime("%Y年%m月%d日"),
        "date_compact": yesterday.strftime("%Y%m%d"),
        "weekday": WEEKDAYS[yesterday.weekday()],
        "lunar": LUNAR_MAP.get(yesterday.strftime("%m%d"), ""),
    }


# ========== 抓取 ==========
def fetch_xwlb(date_compact):
    url = f"https://www.timelines.cn/xwlb/{date_compact}/"
    try:
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        if resp.status_code == 200:
            return resp.text
        print(f"[WARN] HTTP {resp.status_code}")
    except Exception as e:
        print(f"[WARN] 抓取失败: {e}")
    return None


def parse_html(html):
    soup = BeautifulSoup(html, "lxml")
    items = []
    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        if text and 10 < len(text) < 200:
            if "时间轴" not in text and "综合自" not in text:
                items.append(text)
    seen = set()
    unique = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique[:12]


# ========== 简报 ==========
def build_bulletin(info, news):
    lines = []
    lunar = f"，农历{info['lunar']}" if info["lunar"] else ""
    lines.append(f"{info['date_str']}简报，{info['weekday']}{lunar}，早安！")
    lines.append("")
    if news:
        for i, item in enumerate(news, 1):
            lines.append(f"{i}. {item.rstrip('；;')}")
    else:
        lines.append("（今日新闻联播内容暂未更新，请稍后查看。）")
    lines.append("")
    lines.append("【心语】生活的意义不在于拿到一副好牌，"
                "而在于怎样将坏牌打得精彩。"
                "每一个不曾起舞的日子，都是对生命的辜负。——尼采")
    return "\n".join(lines)


# ========== 推送 ==========
def send_pushplus(title, content):
    payload = {"token": PUSHPLUS_TOKEN, "title": title, "content": content, "channel": "wechat"}
    try:
        resp = requests.post(PUSHPLUS_API, json=payload, timeout=15)
        result = resp.json()
        if result.get("code") == 200:
            print(f"[OK] 推送成功！message_id={result.get('data','')}")
            return True
        print(f"[ERR] 推送失败: {result}")
    except Exception as e:
        print(f"[ERR] 推送异常: {e}")
    return False


# ========== 主流程 ==========
def main():
    print(f"=== 开始推送 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    info = get_yesterday_info()
    print(f"[INFO] 目标日期: {info['date_str']}")

    html = fetch_xwlb(info["date_compact"])
    news = parse_html(html) if html else []
    print(f"[INFO] 解析到 {len(news)} 条新闻")

    bulletin = build_bulletin(info, news)
    ok = send_pushplus(f"{info['date_str']} 新闻简报", bulletin)

    print(f"=== {'完成' if ok else '失败'} ===")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
