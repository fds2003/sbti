# SBTI 测试项目 - 代理上下文

## 项目概述

SBTI 是一个娱乐性质的人格测试网页应用，类似于 MBTI 但更具趣味性。项目采用纯前端技术实现，无需后端支持。

**项目信息**
- 项目名称：SBTI 测试（镜像）
- 原作者：B站 @蛆肉儿串儿
- 线上地址：https://sbti.unun.dev
- 项目类型：静态网页 / 前端应用

## 技术栈

- **HTML5** - 页面结构
- **CSS3** - 样式设计（包含 CSS 变量、Flexbox、Grid 布局）
- **原生 JavaScript** - 测试逻辑和交互（无框架）
- **无构建工具** - 单文件应用，无需编译
- **无外部依赖** - 纯原生实现

## 项目结构

```
SBTI-test/
├── index.html          # 主应用文件（包含 HTML/CSS/JS）
├── README.md           # 项目说明文档
├── AGENTS.md           # 本文件（代理上下文）
└── image/              # 人格类型结果图片
    ├── ATM-er.png
    ├── BOSS.png
    ├── CTRL.png
    ├── DEAD.png
    ├── Dior-s.jpg
    ├── DRUNK.png
    ├── FAKE.png
    ├── FUCK.png
    ├── GOGO.png
    ├── HHHH.png
    ├── IMFW.png
    ├── IMSB.png
    ├── JOKE-R.jpg
    ├── LOVE-R.png
    ├── MALO.png
    ├── MONK.png
    ├── MUM.png
    ├── OH-NO.png
    ├── OJBK.png
    ├── POOR.png
    ├── SEXY.png
    ├── SHIT.png
    ├── SOLO.png
    ├── THAN-K.png
    ├── THIN-K.png
    ├── WOC.png
    └── ZZZZ.png
```

## 核心功能

### 测试系统
- **30道常规题目**：覆盖15个心理维度
- **2道特殊题目**：用于触发隐藏人格（酒鬼人格）
- **题目随机排序**：每次测试题目顺序不同
- **进度跟踪**：实时显示答题进度

### 评分机制
- **十五维度系统**：
  - **自我模型** (S1-S3)：自尊自信、自我清晰度、核心价值
  - **情感模型** (E1-E3)：依恋安全感、情感投入度、边界与依赖
  - **态度模型** (A1-A3)：世界观倾向、规则与灵活度、人生意义感
  - **行动驱力模型** (Ac1-Ac3)：动机导向、决策风格、执行模式
  - **社交模型** (So1-So3)：社交主动性、人际边界感、表达与真实度

- **评分等级**：L (Low) = 1, M (Medium) = 2, H (High) = 3
- **人格匹配算法**：基于欧氏距离计算与预定义人格模式的相似度

### 人格类型
共 **26种人格类型**，包括：

- **24种常规人格**：CTRL、ATM-er、BOSS、Dior-s、THAN-K、OH-NO、GOGO、SEXY、LOVE-R、MUM、FAKE、OJBK、MALO、JOKE-R、WOC!、THIN-K、SHIT、ZZZZ、POOR、MONK、IMSB、SOLO、FUCK、DEAD、IMFW
- **1种隐藏人格**：DRUNK（酒鬼）- 通过特殊题目触发
- **1种兜底人格**：HHHH（傻乐者）- 当标准人格库匹配度低于 60% 时分配

## 运行和测试

### 本地运行
```bash
# 直接用浏览器打开
open index.html

# 或使用简单的静态服务器
python -m http.server 8000
# 然后访问 http://localhost:8000
```

### 部署
- Cloudflare Pages（当前使用）
- GitHub Pages
- Vercel
- Netlify
- 任何支持静态文件托管的服务

## 代码约定

### 文件结构
- 所有代码集中在 `index.html` 文件中
- HTML 结构在 `<body>` 中
- CSS 样式在 `<head>` 的 `<style>` 标签中
- JavaScript 逻辑在 `<body>` 末尾的 `<script>` 标签中

### 命名规范
- 使用驼峰命名法（camelCase）
- CSS 变量使用连字符命名法（kebab-case）
- 常量使用大写字母（如 `TYPE_LIBRARY`, `DIM_EXPLANATIONS`）

### 关键数据结构
- `questions`: 常规题目数组
- `specialQuestions`: 特殊题目数组
- `TYPE_LIBRARY`: 人格类型定义
- `TYPE_IMAGES`: 人格类型图片映射
- `NORMAL_TYPES`: 常规人格类型及其匹配模式
- `DIM_EXPLANATIONS`: 维度评分解释

### 主要函数
- `startTest()`: 初始化测试
- `renderQuestions()`: 渲染题目列表
- `updateProgress()`: 更新进度条
- `computeResult()`: 计算测试结果
- `renderResult()`: 渲染结果页面

## 开发注意事项

### 修改题目
- 题目定义在 `questions` 和 `specialQuestions` 数组中
- 每道题需包含 `id`、`dim`（维度）、`text`（题干）、`options`（选项）
- 选项需包含 `label`（显示文本）和 `value`（分值）

### 修改人格类型
- 人格定义在 `TYPE_LIBRARY` 对象中
- 每种人格需包含 `code`、`cn`（中文名）、`intro`（开场白）、`desc`（描述）
- 匹配模式在 `NORMAL_TYPES` 数组中定义（15个字母的模式字符串）

### 添加图片
- 新人格图片需放置在 `image/` 目录
- 在 `TYPE_IMAGES` 对象中添加映射关系
- 支持 PNG 和 JPG 格式

### 测试模式
- 可调用 `startTest(true)` 启用预览模式，显示维度信息
- 正式测试时调用 `startTest(false)` 隐藏维度信息

## 浏览器兼容性

- 使用现代 CSS 特性（CSS 变量、Grid、Flexbox）
- 使用 ES6+ JavaScript 特性
- 建议使用现代浏览器（Chrome、Firefox、Safari、Edge 最新版本）

## 性能优化

- 所有内联代码，减少 HTTP 请求
- 图片按需加载
- 使用 CSS 过渡效果而非 JavaScript 动画
- 无外部资源依赖

## 已知特性

1. **酒鬼人格触发机制**：当用户在补充题中选择"饮酒"作为爱好，且对饮酒态度选择"酒精令我信服"时，强制触发 DRUNK 人格

2. **兜底机制**：当标准人格库最高匹配度低于 60% 时，系统强制分配 HHHH 人格

3. **题目动态插入**：第一道特殊题目（爱好选择）会随机插入到常规题目中，第二道特殊题目（饮酒态度）仅在满足条件时动态插入

4. **结果匹配算法**：综合考虑距离（欧氏距离）、精确匹配数和相似度百分比进行排序

## 维护和更新

- 修改题目或人格类型后需测试所有可能的路径
- 确保新增图片已正确映射到 `TYPE_IMAGES`
- 测试隐藏人格和兜底人格的触发逻辑
- 验证所有维度评分和解释文本的正确性