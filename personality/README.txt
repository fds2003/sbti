人格静态页生成结果（与 data/personality-source.json 同步）

合并到线上目录 personality/ 的方法：
1. 若 personality/ 无法写入，先修正属主：
   sudo chown -R "$(whoami)" personality
2. 将本目录全部文件复制到 personality/（与现有 ctrl.html、boss.html 合并共存）：
   cp -r personality-skel/* personality/

重新生成骨架页：
  python3 scripts/generate-personality-pages.py
默认输出到 personality-skel/；输出到 personality/ 时请加：
  python3 scripts/generate-personality-pages.py --out personality
