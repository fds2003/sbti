#!/usr/bin/env python3
"""从 data/personality-source.json 生成人格骨架页（利于 SEO 与内链）。

默认输出到 personality-skel/，避免 personality/ 为 root 属主时无法写入。
合并到站点：见 personality-skel/README.txt
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "data", "personality-source.json")

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{code} {cn} - SBTI 人格类型</title>
  <meta name="description" content="{tagline} SBTI 趣味人格测试，{cn} 类型一句话画像。" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{domain}/personality/{slug}.html" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{domain}/personality/{slug}.html" />
  <meta property="og:title" content="{code} {cn} - SBTI" />
  <meta property="og:description" content="{tagline}" />
  <meta property="og:image" content="{domain}/image/{image}" />
  <style>
    :root {{
      --bg: #f6faf6;
      --text: #1e2a22;
      --muted: #6a786f;
      --line: #dbe8dd;
      --accent: #6c8d71;
      --accent-strong: #4d6a53;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.75;
      min-height: 100vh;
    }}
    .wrap {{ max-width: 720px; margin: 0 auto; padding: 28px 18px 48px; }}
    a {{ color: var(--accent-strong); }}
    .nav {{ margin-bottom: 20px; font-size: 14px; }}
    .nav a {{ margin-right: 14px; }}
    .card {{
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 28px;
      box-shadow: 0 12px 36px rgba(47, 73, 55, 0.06);
    }}
    h1 {{ font-size: clamp(26px, 5vw, 36px); margin: 0 0 8px; color: var(--accent-strong); }}
    .tagline {{ color: var(--muted); font-size: 17px; margin: 0 0 20px; }}
    .hero-img {{
      width: 100%;
      max-width: 320px;
      height: auto;
      border-radius: 16px;
      display: block;
      margin: 0 auto 24px;
    }}
    .lead {{ font-size: 16px; margin: 0 0 20px; }}
    .cta {{
      display: inline-block;
      background: var(--accent-strong);
      color: #fff !important;
      text-decoration: none;
      padding: 12px 22px;
      border-radius: 12px;
      font-weight: 700;
      margin-top: 8px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <nav class="nav" aria-label="面包屑">
      <a href="../index.html">SBTI 测试</a>
      <a href="index.html">人格图鉴</a>
    </nav>
    <article class="card">
      <h1>{code} · {cn}</h1>
      <p class="tagline">{tagline}</p>
      <img class="hero-img" src="../image/{image}" width="320" height="320" alt="{code} {cn}" loading="lazy" decoding="async" />
      <p class="lead">
        在 SBTI 中，<strong>{code}</strong> 对应「{cn}」人格画像。完整长文解读与十五维度评分请在完成测试后的结果页查看；本页为独立收录的一句话介绍与入口。
      </p>
      <a class="cta" href="../index.html">去做测试</a>
    </article>
  </div>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        default="personality-skel",
        help="输出目录（默认 personality-skel；合并到站点时用 personality）",
    )
    args = parser.parse_args()
    out_dir = os.path.join(ROOT, args.out)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    domain = data.get("canonicalDomain", "https://sbti.oucloud.top").rstrip("/")
    os.makedirs(out_dir, exist_ok=True)
    skip = {"ctrl", "boss"}  # 保留原有较详版页面（若已存在）
    for t in data["types"]:
        slug = t["slug"]
        if slug in skip:
            continue
        path = os.path.join(out_dir, f"{slug}.html")
        html = TEMPLATE.format(
            domain=domain,
            code=t["code"],
            cn=t["cn"],
            tagline=t["tagline"].replace("&", "&amp;").replace("<", "&lt;"),
            slug=slug,
            image=t["image"],
        )
        with open(path, "w", encoding="utf-8") as out:
            out.write(html)
        print("wrote", path)

    hub_lines = [
        '            <li><a href="{slug}.html">{code} {cn}</a> — <span class="tag">{tagline}</span></li>'.format(
            slug=t["slug"],
            code=t["code"],
            cn=t["cn"],
            tagline=t["tagline"],
        )
        for t in data["types"]
    ]
    hub_body = "\n".join(hub_lines)
    hub_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SBTI 27 种人格图鉴</title>
  <meta name="description" content="SBTI 趣味人格测试全部人格类型一览：一句话画像与入口。" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{domain}/personality/index.html" />
  <style>
    :root {{ --bg: #f6faf6; --text: #1e2a22; --muted: #6a786f; --line: #dbe8dd; --accent-strong: #4d6a53; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; min-height: 100vh; }}
    .wrap {{ max-width: 900px; margin: 0 auto; padding: 28px 18px 48px; }}
    a {{ color: var(--accent-strong); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    h1 {{ font-size: clamp(24px, 4vw, 34px); color: var(--accent-strong); margin: 0 0 12px; }}
    .lead {{ color: var(--muted); margin: 0 0 24px; }}
    ul {{ list-style: none; padding: 0; margin: 0; }}
    li {{ padding: 12px 14px; border-bottom: 1px solid var(--line); }}
    li:hover {{ background: rgba(108, 141, 113, 0.06); }}
    .tag {{ color: var(--muted); font-size: 14px; }}
    .topnav {{ margin-bottom: 20px; font-size: 15px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <nav class="topnav"><a href="../index.html">← 返回测试首页</a></nav>
    <h1>SBTI 27 种人格图鉴</h1>
    <p class="lead">每种类型独立成页，便于检索与分享；完整解读以答题后的结果页为准。</p>
    <ul>
{hub_body}
    </ul>
  </div>
</body>
</html>
"""
    hub_path = os.path.join(out_dir, "index.html")
    with open(hub_path, "w", encoding="utf-8") as out:
        out.write(hub_html)
    print("wrote", hub_path)


if __name__ == "__main__":
    main()
