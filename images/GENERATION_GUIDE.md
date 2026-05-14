# AI Agent 教程 - 手绘插图生成指南

## 已完成的准备工作

1. **13 组详细 Prompts** 已写好，存放在 `images/prompts/` 目录
2. **风格锁定文本** 已写好: `images/deck-style-lock.txt`
3. **图片映射配置** 已写好: `js/images.json`
4. **网站集成代码** 已更新: `js/app.js`, `css/style.css` 均已支持插图加载

## 产出清单

| # | 文件名 | 类型 | 尺寸 |
|---|---|---|---|
| 1 | 01-cover-ai-agent-tutorial.png | 封面图 | 21:9 (2520x1080) |
| 2 | 02-category-fundamentals.png | 分类概览 | 16:9 (1920x1080) |
| 3 | 03-category-tools.png | 分类概览 | 16:9 (1920x1080) |
| 4 | 04-category-vibecoding.png | 分类概览 | 16:9 (1920x1080) |
| 5 | 05-category-python.png | 分类概览 | 16:9 (1920x1080) |
| 6 | 06-agent-core-formula.png | 核心概念 | 16:9 (1920x1080) |
| 7 | 07-ai-architecture-layers.png | 核心概念 | 16:9 (1920x1080) |
| 8 | 08-agent-loop-react.png | 核心概念 | 16:9 (1920x1080) |
| 9 | 09-rag-workflow.png | 核心概念 | 16:9 (1920x1080) |
| 10 | 10-function-calling.png | 核心概念 | 16:9 (1920x1080) |
| 11 | 11-memory-system.png | 核心概念 | 16:9 (1920x1080) |
| 12 | 12-multi-agent-system.png | 核心概念 | 16:9 (1920x1080) |
| 13 | 13-learning-path.png | 学习路径 | 16:9 (1920x1080) |

## 生成方式

### 方式一：使用 OpenAI DALL-E 3 / GPT-4o 图片生成

每个 prompt 文件可以直接作为图片生成的输入。推荐使用 GPT-4o 的图片生成能力，它对中文文字渲染较好。

步骤：
1. 打开 ChatGPT 或 API
2. 使用 `images/prompts/01-cover-ai-agent-tutorial.md` 中的完整描述
3. 生成图片并保存到 `images/` 目录
4. 重复以上步骤生成全部 13 张图

### 方式二：使用 Stable Diffusion + ControlNet

适合本地部署，可以使用 Flux 等模型。

### 方式三：使用 Midjourney

需要将中文 prompt 翻译为英文，文字渲染可能不如 DALL-E。

## 网站图片显示逻辑

- **封面图**: 仅在首页 `ai-agent-tutorial` 顶部显示 (21:9)
- **分类图**: 在每个分类的第一篇文章顶部显示 (16:9)
- **概念图**: 在对应文章内容中显示 (16:9)
- **学习路径图**: 在首页底部显示 (16:9)

所有图片通过 `js/images.json` 配置映射关系，代码会自动根据当前页面 ID 加载对应图片。
