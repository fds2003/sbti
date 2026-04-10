# SBTI 测试项目 - 部署与运维指南

## 部署选项

### 1. Cloudflare Pages（推荐 - 当前使用）

**优势**
- 免费托管
- 全球 CDN 加速
- 自动 HTTPS
- 极快的部署速度

**部署步骤**
```bash
# 1. 安装 Wrangler CLI
npm install -g wrangler

# 2. 登录 Cloudflare
wrangler login

# 3. 初始化项目
wrangler pages project create sbti-test

# 4. 部署
wrangler pages deploy . --project-name=sbti-test
```

**配置文件 `wrangler.toml`**
```toml
name = "sbti-test"
compatibility_date = "2024-01-01"

[build]
command = ""

[build.upload]
format = "directory"
directory = "."
```

### 2. GitHub Pages

**优势**
- 完全免费
- 与 GitHub 仓库集成
- 自动部署

**部署步骤**
1. 在 GitHub 仓库设置中启用 GitHub Pages
2. 选择 `main` 分支作为源
3. 访问 `https://yourusername.github.io/SBTI-test/`

**注意**：需要更新图片路径为绝对路径

### 3. Vercel

**优势**
- 极快的构建速度
- 自动 HTTPS
- 全球 CDN
- 支持自定义域名

**部署步骤**
```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 部署
vercel
```

### 4. Netlify

**优势**
- 免费托管
- 持续部署
- 自动 HTTPS
- 表单处理

**部署步骤**
```bash
# 1. 安装 Netlify CLI
npm install -g netlify-cli

# 2. 登录
netlify login

# 3. 部署
netlify deploy --prod
```

## 性能优化配置

### 1. 缓存策略

**Cloudflare 缓存规则**
```javascript
// Cache Everything
https://sbti.unun.dev/*
Cache Level: Everything
Edge Cache TTL: 1 day
Browser Cache TTL: 4 hours
```

### 2. 图片优化

**使用 Cloudflare Images**
```html
<!-- 优化后的图片标签 -->
<img 
  src="https://images.unsplash.com/photo-xxx?w=800&q=80&f=webp" 
  alt="描述"
  loading="lazy"
  decoding="async"
>
```

**本地图片优化**
```bash
# 安装 sharp
npm install sharp

# 优化图片脚本
# compress-images.js
```

### 3. CDN 配置

**Cloudflare 配置**
- 启用 Brotli 压缩
- 启用 HTTP/3
- 启用 0-RTT Connection Resumption
- 设置适当的缓存头

### 4. 预加载关键资源

```html
<head>
  <!-- 预加载字体 -->
  <link rel="preload" href="path/to/font.woff2" as="font" type="font/woff2" crossorigin>
  
  <!-- 预加载关键图片 -->
  <link rel="preload" href="image/CTRL.png" as="image">
</head>
```

## 安全配置

### 1. 安全头设置

**Cloudflare Workers**
```javascript
// workers.js
export default {
  async fetch(request) {
    const response = await fetch(request);
    
    // 添加安全头
    const newResponse = new Response(response.body, response);
    newResponse.headers.set('X-Frame-Options', 'DENY');
    newResponse.headers.set('X-Content-Type-Options', 'nosniff');
    newResponse.headers.set('X-XSS-Protection', '1; mode=block');
    newResponse.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    newResponse.headers.set('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
    
    return newResponse;
  }
};
```

### 2. HTTPS 强制跳转

**Cloudflare 设置**
- SSL/TLS: Full
- Always Use HTTPS: On
- Automatic HTTPS Rewrites: On

### 3. 防火墙规则

**Cloudflare WAF**
```
# 阻止恶意爬虫
(http.user_agent contains "bot" and cf.bot_management.score < 30) -> Block

# 速率限制
(cf.threat_score > 10) -> Rate Limit: 100 req/min
```

## 监控和分析

### 1. Cloudflare Analytics

**关键指标**
- 页面浏览量
- 独立访客
- 平均加载时间
- 地理分布
- 设备类型

### 2. Google Analytics

**集成代码**
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### 3. 错误监控

**Sentry 集成**
```html
<script src="https://cdn.jsdelivr.net/npm/@sentry/browser@7.64.0/build/sentry.min.js"></script>
<script>
  Sentry.init({
    dsn: 'YOUR_DSN',
    environment: 'production',
    tracesSampleRate: 0.1
  });
</script>
```

## CI/CD 配置

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy . --project-name=sbti-test
```

## 备份和恢复

### 1. 数据备份

```bash
# 备份脚本
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR="/path/to/backups"
tar -czf $BACKUP_DIR/sbti-test-$DATE.tar.gz .
```

### 2. 自动备份

**Cron Job**
```bash
# 每天凌晨 2 点备份
0 2 * * * /path/to/backup-script.sh
```

## 故障排除

### 常见问题

**1. 图片加载失败**
- 检查图片路径是否正确
- 验证图片文件是否存在
- 检查 CDN 缓存

**2. 性能问题**
- 使用 Chrome DevTools 分析
- 检查网络请求
- 优化图片大小

**3. 跨域问题**
- 配置 CORS 头
- 检查 API 端点设置

### 调试工具

**浏览器控制台**
```javascript
// 检查本地存储
console.log(localStorage.getItem('sbti_test_result'));

// 清除缓存
localStorage.clear();

// 检查应用状态
console.log(app);
```

## 维护建议

### 定期任务

**每周**
- 检查性能指标
- 查看错误日志
- 更新依赖项

**每月**
- 分析用户行为
- 优化 SEO
- 备份数据

**每季度**
- 安全审计
- 性能优化
- 功能更新

### 版本更新

**更新流程**
1. 创建新分支
2. 进行更改
3. 测试更改
4. 合并到主分支
5. 部署到生产环境

## 联系和支持

- 项目主页：https://github.com/UnluckyNinja/SBTI-test
- 问题反馈：https://github.com/UnluckyNinja/SBTI-test/issues
- 在线演示：https://sbti.unun.dev

## 许可证

本项目仅供学习和娱乐使用，请勿用于商业用途。