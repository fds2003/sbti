/**
 * 一次性冒烟：本地需已启动 static server，例如:
 *   python3 -m http.server 8765 --bind 127.0.0.1
 * 运行: node e2e-smoke.mjs
 *
 * 浏览器启动顺序（与 tests/playwright.config.js 对齐）：
 * 1) 环境变量 CHROME_FOR_TESTING 指向 Chrome/Chromium 可执行文件或 .app
 * 2) 默认尝试 ~/Downloads/chrome-mac-x64/Google Chrome for Testing.app
 * 3) Playwright 自带的 Chromium（需 npx playwright install）
 * 4) 本机已安装的 Google Chrome（channel: chrome）
 */
import fs from "fs";
import path from "path";
import { chromium } from "playwright";

const BASE = process.env.SBTI_BASE || "http://127.0.0.1:8765/index.html";

/** @param {string | undefined} userPath */
function resolveChromeExecutable(userPath) {
  if (!userPath || !fs.existsSync(userPath)) return undefined;
  if (userPath.endsWith(".app")) {
    const bin = path.join(
      userPath,
      "Contents/MacOS/Google Chrome for Testing",
    );
    return fs.existsSync(bin) ? bin : undefined;
  }
  return userPath;
}

function chromeForTestingPath() {
  const fromEnv = resolveChromeExecutable(process.env.CHROME_FOR_TESTING);
  if (fromEnv) return fromEnv;
  const defaultApp = path.join(
    process.env.HOME || "",
    "Downloads/chrome-mac-x64/Google Chrome for Testing.app",
  );
  return resolveChromeExecutable(defaultApp);
}

async function launchChromium() {
  const executablePath = chromeForTestingPath();
  const opts = executablePath ? { executablePath } : {};
  try {
    return await chromium.launch(opts);
  } catch (e) {
    console.warn(
      "[e2e-smoke] 默认 Chromium 启动失败，尝试系统 Chrome：",
      /** @type {Error} */ (e).message || e,
    );
    return await chromium.launch({ channel: "chrome" });
  }
}

async function answerUntilSubmit(page, { drunk }) {
  let iter = 0;
  while (iter++ < 150) {
    if (await page.locator("#submitBtn").isEnabled()) return;

    const unanswered = page.locator("#questionList .question").filter({
      hasNot: page.locator("input:checked"),
    });
    if ((await unanswered.count()) === 0) {
      await page.waitForTimeout(80);
      continue;
    }
    const card = unanswered.first();
    const title = await card.locator(".question-title").innerText();

    if (drunk && title.includes("爱好")) {
      await card.locator('input[value="3"]').check();
    } else if (drunk && title.includes("饮酒的态度")) {
      await card.locator('input[value="2"]').check();
    } else {
      await card.locator('input[type="radio"]').first().check();
    }
  }
  throw new Error("答题未完成：提交按钮始终未启用");
}

async function runScenario(page, label, drunk) {
  const consoleErrors = [];
  const pageErrors = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });
  page.on("pageerror", (e) => pageErrors.push(e.message));

  await page.goto(BASE, { waitUntil: "domcontentloaded" });
  await page.click("#startBtn");
  await page.waitForSelector("#questionList .question");

  await answerUntilSubmit(page, { drunk });
  await page.locator("#submitBtn").click();
  await page.waitForSelector("#result.screen.active", { timeout: 20000 });

  const typeName = await page.locator("#resultTypeName").innerText();
  const modeKicker = await page.locator("#resultModeKicker").innerText();
  const badge = await page.locator("#matchBadge").innerText();
  const dimCount = await page.locator("#dimList .dim-item").count();
  const posterSrc = await page.locator("#posterImage").getAttribute("src");

  return {
    label,
    drunk,
    typeName,
    modeKicker,
    badge,
    dimCount,
    posterSrc,
    consoleErrors,
    pageErrors,
  };
}

async function main() {
  const browser = await launchChromium();
  const context = await browser.newContext({
    acceptDownloads: true,
    permissions: ["clipboard-read", "clipboard-write"],
  });
  const page = await context.newPage();

  const results = [];

  // 1) 常规路径（首选项含「吃喝拉撒」非饮酒）
  results.push(await runScenario(page, "常规路径", false));

  // 结果页：分享 / 复制 / 下载
  await page.click("#shareBtn");
  await page.waitForTimeout(400);
  const shareToast = (await page.locator("#toast").textContent()) || "";

  await page.click("#copyLinkBtn");
  await page.waitForTimeout(400);
  const copyToast = (await page.locator("#toast").textContent()) || "";

  const [download] = await Promise.all([
    page.waitForEvent("download", { timeout: 15000 }),
    page.click("#downloadBtn"),
  ]);
  const downloadName = download.suggestedFilename();

  // 重新测试 → 酒鬼分支
  await page.click("#restartBtn");
  await page.waitForSelector("#test.screen.active");
  results.push(await runScenario(page, "酒鬼分支", true));

  // 回到首页
  await page.click("#toTopBtn");
  await page.waitForSelector("#intro.screen.active");

  // 测试页返回首页
  await page.click("#startBtn");
  await page.waitForSelector("#test.screen.active");
  await page.keyboard.press("Escape");
  await page.waitForSelector("#intro.screen.active");

  await browser.close();

  console.log(JSON.stringify({ results, shareToast, copyToast, downloadName }, null, 2));

  const failed = results.filter(
    (r) => r.consoleErrors.length || r.pageErrors.length || r.dimCount !== 15
  );
  if (failed.length) {
    console.error("失败项:", failed);
    process.exit(1);
  }
  if (!downloadName || !downloadName.endsWith(".html")) {
    console.error("下载异常:", downloadName);
    process.exit(1);
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
