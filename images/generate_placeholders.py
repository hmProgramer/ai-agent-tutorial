#!/usr/bin/env python3
"""
Generate placeholder illustration images with Chinese text.
These are functional placeholders - replace with AI-generated handdrawn images.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = '/System/Library/Fonts/STHeiti Medium.ttc'
FONT_SMALL = '/System/Library/Fonts/PingFang.ttc'

# Colors matching the handdrawn theme
PAPER = '#FBFAF5'
INK = '#333333'
BLUE = '#D9E8F6'
GREEN = '#DCEAD6'
PEACH = '#F5DEB8'
LAVENDER = '#E4DCF4'
ACCENT = '#D66F4D'
LIGHT_LINE = '#CCCCCC'

def get_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def draw_corner_marks(draw, w, h):
    """Faint corner marks"""
    for x, y in [(40, 40), (w-40, 40), (40, h-40), (w-40, h-40)]:
        draw.line([(x, y), (x+15, y)], fill=LIGHT_LINE, width=1)
        draw.line([(x, y), (x, y+15)], fill=LIGHT_LINE, width=1)

def draw_page_number(draw, text, w):
    font = ImageFont.truetype(FONT_SMALL, 18)
    draw.text((36, 28), text, fill=LIGHT_LINE, font=font)

def draw_title(draw, title, subtitle, w):
    """Centered title with blue underline"""
    title_font = get_font(36)
    sub_font = get_font(18)

    # Title
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    tx = (w - tw) // 2
    draw.text((tx, 60), title, fill=INK, font=title_font)

    # Underline
    ul_y = 108
    draw.line([(tx, ul_y), (tx + tw, ul_y)], fill=BLUE, width=2)

    # Subtitle
    if subtitle:
        bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        sw = bbox[2] - bbox[0]
        sx = (w - sw) // 2
        draw.text((sx, 120), subtitle, fill='#666666', font=sub_font)

def draw_pastel_label(draw, x, y, text, color, font=None):
    """Draw a pastel rounded label"""
    if font is None:
        font = get_font(16)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    padding = 8
    draw.rounded_rectangle(
        [x - padding, y - padding, x + tw + padding, y + th + padding],
        radius=6, fill=color, outline=INK, width=1
    )
    draw.text((x, y), text, fill=INK, font=font)

def draw_arrow(draw, x1, y1, x2, y2):
    """Simple arrow"""
    draw.line([(x1, y1), (x2, y2)], fill=INK, width=1)
    # small arrowhead
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    al = 8
    ax = x2 - al * math.cos(angle - 0.4)
    ay = y2 - al * math.sin(angle - 0.4)
    draw.line([(ax, ay), (x2, y2)], fill=INK, width=1)
    ax = x2 - al * math.cos(angle + 0.4)
    ay = y2 - al * math.sin(angle + 0.4)
    draw.line([(ax, ay), (x2, y2)], fill=INK, width=1)

# ========== Image 1: Cover (21:9) ==========
def create_cover():
    w, h = 2520, 1080
    img = Image.new('RGB', (w, h), PAPER)
    draw = ImageDraw.Draw(img)
    draw_corner_marks(draw, w, h)

    # Large title
    title_font = get_font(72)
    sub_font = get_font(32)
    label_font = get_font(28)

    title = 'AI Agent 智能体教程'
    subtitle = '从基础理论到 Python 实战'

    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 180), title, fill=INK, font=title_font)
    draw.line([((w - tw) // 2, 270), ((w + tw) // 2, 270)], fill=BLUE, width=3)
    draw.text(((w - draw.textbbox((0, 0), subtitle, font=sub_font)[2] + draw.textbbox((0, 0), subtitle, font=sub_font)[0]) // 2, 300), subtitle, fill='#555555', font=sub_font)

    # Central diagram - Agent core with 4 orbiting modules
    cx, cy = w // 2, 580
    # Central circle
    r = 60
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2, fill=PEACH)
    draw.text((cx - 36, cy - 18), 'Agent', fill=INK, font=get_font(24))

    # Orbiting labels with dotted lines
    modules = [
        (cx, cy - 160, 'LLM 大脑', BLUE),
        (cx + 180, cy - 20, '规划', GREEN),
        (cx, cy + 120, '工具', PEACH),
        (cx - 180, cy - 20, '记忆', LAVENDER),
    ]
    for mx, my, mtext, mcolor in modules:
        # Dashed line from center
        for i in range(0, int(((mx-cx)**2 + (my-cy)**2)**0.5 - r), 12):
            ratio = i / ((mx-cx)**2 + (my-cy)**2)**0.5
            px = cx + (mx - cx) * ratio / ((mx-cx)**2 + (my-cy)**2)**0.5 * i if mx != cx else cx
            py = cy + (my - cy) * ratio / ((mx-cx)**2 + (my-cy)**2)**0.5 * i if my != cy else cy
            if mx != cx:
                px = cx + (mx - cx) * i / max(1, ((mx-cx)**2 + (my-cy)**2)**0.5)
            if my != cy:
                py = cy + (my - cy) * i / max(1, ((mx-cx)**2 + (my-cy)**2)**0.5)
            draw.point((int(px), int(py)), fill=LIGHT_LINE)

        draw_pastel_label(draw, mx - 36, my - 12, mtext, mcolor, font=label_font)

    img.save(os.path.join(OUTPUT_DIR, '01-cover-ai-agent-tutorial.png'))
    print(f'Cover: {w}x{h}')

# ========== Body illustration base ==========
def create_body_base(title, subtitle, page_num, w=1920, h=1080):
    img = Image.new('RGB', (w, h), PAPER)
    draw = ImageDraw.Draw(img)
    draw_corner_marks(draw, w, h)
    draw_page_number(draw, page_num, w)
    draw_title(draw, title, subtitle, w)
    return img, draw

# ========== Image 2: 基础与原理 - Classification Map ==========
def create_fundamentals():
    img, draw = create_body_base('基础与原理', '理解 AI Agent 的核心概念', '01 / 12')
    w, h = 1920, 1080

    # Tree diagram
    nodes = [
        # (x, y, text, color, parent_idx)
        (960, 700, '大语言模型 LLM', BLUE, -1),  # root
        (400, 500, '推理与规划', GREEN, 0),
        (700, 450, '提示词工程', BLUE, 0),
        (1000, 400, 'Token 词元', PEACH, 0),
        (1200, 500, '向量数据库', LAVENDER, 0),
        (1500, 450, 'RAG 知识检索', GREEN, 0),
        (800, 300, 'Agent 架构', BLUE, 2),
        (1100, 270, 'Harness Eng.', PEACH, 2),
        (1400, 300, 'Hermes Agent', LAVENDER, 2),
    ]

    font = get_font(15)
    for i, (nx, ny, ntext, ncolor, parent) in enumerate(nodes):
        draw_pastel_label(draw, nx - 40, ny - 10, ntext, ncolor, font=font)
        if parent >= 0:
            px, py = nodes[parent][0], nodes[parent][1] + 15
            draw.line([(px, py), (nx, ny)], fill=LIGHT_LINE, width=1)

    img.save(os.path.join(OUTPUT_DIR, '02-category-fundamentals.png'))

# ========== Image 3: 智能体工具 ==========
def create_tools():
    img, draw = create_body_base('智能体工具', '从第一个 Agent 到生产级部署', '02 / 12')
    w, h = 1920, 1080

    font = get_font(15)
    # Cabinet with 3 drawers
    sections = [
        ('入门上手', 350, [('第一个 AI Agent', BLUE), ('AI 开发平台', GREEN), ('OpenClaw 快速上手', PEACH), ('QoderWork', LAVENDER)]),
        ('IM 接入', 520, [('微信接入', BLUE), ('飞书接入', GREEN), ('Skills 配置', PEACH)]),
        ('工作流与框架', 690, [('CrewAI', BLUE), ('LangChain', GREEN), ('LangGraph', PEACH), ('AI Workflow', LAVENDER)]),
    ]

    for sec_title, sy, items in sections:
        # Drawer background
        draw.rounded_rectangle([400, sy, 1520, sy + 140], radius=8, outline=INK, width=1, fill=None)
        draw_pastel_label(draw, 420, sy - 8, sec_title, PEACH, font=get_font(18))

        # Items as cards
        for j, (item_text, item_color) in enumerate(items):
            ix = 500 + j * 240
            draw_pastel_label(draw, ix, sy + 55, item_text, item_color, font=font)

    # Top card
    draw_pastel_label(draw, 860, 260, '一键部署', GREEN, font=get_font(20))

    img.save(os.path.join(OUTPUT_DIR, '03-category-tools.png'))

# ========== Image 4: Vibe Coding ==========
def create_vibecoding():
    img, draw = create_body_base('Vibe Coding', 'AI 驱动的自然语言编程范式', '03 / 12')
    w, h = 1920, 1080

    font = get_font(16)
    # Three panels
    panels = [
        (350, '终端 CLI', [('Claude Code', BLUE), ('OpenCode', GREEN)]),
        (800, 'IDE 集成', [('Qoder', PEACH), ('Trae', LAVENDER)]),
        (1250, '高级特性', [('Coding Plan', BLUE), ('Quest 模式', GREEN), ('Skills', PEACH)]),
    ]

    for px, ptitle, items in panels:
        draw.rounded_rectangle([px - 150, 350, px + 150, 620], radius=8, outline=INK, width=1, fill=None)
        draw_pastel_label(draw, px - 40, 320, ptitle, PEACH, font=get_font(18))
        for j, (item_text, item_color) in enumerate(items):
            iy = 400 + j * 80
            draw_pastel_label(draw, px - 60, iy, item_text, item_color, font=font)

    img.save(os.path.join(OUTPUT_DIR, '04-category-vibecoding.png'))

# ========== Image 5: Python ==========
def create_python():
    img, draw = create_body_base('Python 实现智能体', '环境配置 · 工具调用 · 记忆系统 · 多智能体 · 生产部署', '04 / 12')
    w, h = 1920, 1080

    font = get_font(14)
    steps = [
        (120, '环境配置', BLUE),
        (400, '工具调用', GREEN),
        (680, '记忆系统', PEACH),
        (960, 'RAG 检索', LAVENDER),
        (1240, '多智能体', BLUE),
        (1520, '生产部署', GREEN),
    ]

    for i, (sx, stext, scolor) in enumerate(steps):
        draw.ellipse([sx, 520, sx + 110, 630], outline=INK, width=1, fill=scolor)
        draw.text((sx + 20, 555), stext, fill=INK, font=get_font(13))
        if i < len(steps) - 1:
            draw_arrow(draw, sx + 115, 575, steps[i+1][0] - 5, 575)

    # Foundation strip at bottom
    draw_pastel_label(draw, 750, 740, 'Hugging Face Transformers 基础', LAVENDER, font=get_font(18))

    img.save(os.path.join(OUTPUT_DIR, '05-category-python.png'))

# ========== Image 6: Agent Core Formula ==========
def create_agent_core():
    img, draw = create_body_base('Agent 核心公式', 'LLM 大脑 · 规划 · 工具 · 记忆', '05 / 12')
    w, h = 1920, 1080

    # Center gear
    cx, cy = w // 2, 560
    draw.ellipse([cx - 55, cy - 55, cx + 55, cy + 55], outline=INK, width=2, fill=PEACH)
    draw.text((cx - 28, cy - 16), 'Agent', fill=INK, font=get_font(22))

    # Four satellites
    sats = [
        (cx, cy - 170, 'LLM 大脑', '思考', BLUE),
        (cx + 200, cy, '规划', '拆解', GREEN),
        (cx, cy + 170, '工具', '执行', PEACH),
        (cx - 200, cy, '记忆', '存取', LAVENDER),
    ]

    for sx, sy, sname, ssub, scolor in sats:
        draw.ellipse([sx - 50, sy - 30, sx + 50, sy + 30], outline=INK, width=1, fill=scolor)
        draw.text((sx - 36, sy - 22), sname, fill=INK, font=get_font(15))
        draw.text((sx - 16, sy + 2), ssub, fill='#666666', font=get_font(11))
        # Dashed connection
        for i in range(0, 40, 10):
            ratio = i / 40.0
            dx = int(cx + (sx - cx) * ratio)
            dy = int(cy + (sy - cy) * ratio)
            draw.point((dx, dy), fill=LIGHT_LINE)

    img.save(os.path.join(OUTPUT_DIR, '06-agent-core-formula.png'))

# ========== Image 7: AI Architecture ==========
def create_architecture():
    img, draw = create_body_base('AI 底层架构', '从基础模型到智能体应用的五层体系', '06 / 12')
    w, h = 1920, 1080

    layers = [
        ('应用层', '自动化工作流 · AI 助手 · 企业系统', GREEN, 200),
        ('智能体层', '感知 → 规划 → 行动', PEACH, 330),
        ('能力扩展层', 'MCP · 工具调用 · API 连接', LAVENDER, 460),
        ('上下文层', 'Prompt · Memory · RAG', BLUE, 590),
        ('基础层', 'Transformer · Token化 · 注意力机制', PEACH, 720),
    ]

    font = get_font(16)
    small_font = get_font(14)
    lx = 300
    lw = 1320

    for lname, ldetail, lcolor, ly in layers:
        draw.rounded_rectangle([lx, ly, lx + lw, ly + 100], radius=6, outline=INK, width=1, fill=lcolor)
        draw.text((lx + 20, ly + 15), lname, fill=INK, font=font)
        draw.text((lx + 180, ly + 40), ldetail, fill='#555555', font=small_font)

    # Vertical arrows
    for y in range(300, 800, 25):
        if y % 50 == 0:
            draw.point((lx + lw // 2, y), fill=INK)

    img.save(os.path.join(OUTPUT_DIR, '07-ai-architecture-layers.png'))

# ========== Image 8: Agent Loop ==========
def create_agent_loop():
    img, draw = create_body_base('Agent 运行循环', 'ReAct 框架：推理与行动交替进行', '07 / 12')
    w, h = 1920, 1080

    cx, cy = w // 2, 580
    r = 140

    stations = [
        (cx, cy - r, '感知', 'Observe', BLUE),
        (cx + r, cy, '思考', 'Reason', GREEN),
        (cx, cy + r, '行动', 'Act', PEACH),
        (cx - r, cy, '反馈', 'Feedback', LAVENDER),
    ]

    # Circle
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=1)

    for sx, sy, sname, seng, scolor in stations:
        draw.ellipse([sx - 38, sy - 22, sx + 38, sy + 22], outline=INK, width=1, fill=scolor)
        draw.text((sx - 26, sy - 18), sname, fill=INK, font=get_font(15))

    # Arrows (approximate with curves)
    import math
    for i in range(4):
        a1 = -math.pi/2 + i * math.pi/2
        a2 = a1 + math.pi/2
        steps = 10
        for j in range(steps):
            a = a1 + (a2 - a1) * j / steps
            x = cx + (r + 46) * math.cos(a)
            y = cy + (r + 22) * math.sin(a)
            if j % 2 == 0:
                draw.point((int(x), int(y)), fill=INK)

    # Center label
    draw.text((cx - 40, cy - 12), 'ReAct', fill=INK, font=get_font(18))

    # Annotations
    draw.text((cx + r + 80, cy - 30), '环境输入', fill='#666666', font=get_font(14))
    draw.text((cx - r - 120, cy + 160), '结果输出', fill='#666666', font=get_font(14))

    img.save(os.path.join(OUTPUT_DIR, '08-agent-loop-react.png'))

# ========== Image 9: RAG ==========
def create_rag():
    img, draw = create_body_base('RAG 工作流程', '检索增强生成：离线索引 + 在线查询', '08 / 12')
    w, h = 1920, 1080

    font = get_font(14)
    # Upper pipeline (offline)
    upper = [('文档', 120), ('分块', 420), ('向量化', 700), ('向量库', 980), (None, 1260)]
    lower = [('问题', 200), ('向量化', 500), ('检索', 780), ('增强提示', 1060), ('LLM 生成', 1320), ('答案', 1580)]

    for i, (uname, ux) in enumerate(upper):
        if uname:
            draw.rounded_rectangle([ux, 280, ux + 100, 320], radius=4, outline=INK, width=1, fill=BLUE)
            draw.text((ux + 15, 290), uname, fill=INK, font=font)
            if i < len(upper) - 2:
                draw_arrow(draw, ux + 105, 300, upper[i+1][1] - 5, 300)

    draw.text((60, 285), '离线索引', fill='#666666', font=get_font(16))

    # Divider
    draw.line([(80, 450), (1840, 450)], fill=LIGHT_LINE, width=1)

    draw.text((60, 500), '在线查询', fill='#666666', font=get_font(16))

    for i, (lname, lx) in enumerate(lower):
        if lname:
            draw.rounded_rectangle([lx, 520, lx + 100, 560], radius=4, outline=INK, width=1, fill=GREEN)
            draw.text((lx + 12, 530), lname, fill=INK, font=font)
            if i < len(lower) - 1:
                draw_arrow(draw, lx + 105, 540, lower[i+1][1] - 5, 540)

    img.save(os.path.join(OUTPUT_DIR, '09-rag-workflow.png'))

# ========== Image 10: Function Calling ==========
def create_function_calling():
    img, draw = create_body_base('Function Calling 机制', '工具调用：让 LLM 连接真实世界', '09 / 12')
    w, h = 1920, 1080

    font = get_font(14)
    steps = [
        (120, 550, '工具定义', BLUE),
        (420, 480, '模型判断', GREEN),
        (720, 550, '参数提取', PEACH),
        (1020, 480, '函数执行', LAVENDER),
        (1320, 550, '结果返回', BLUE),
    ]
    arrow_texts = ['发送工具列表', '选择工具+参数', '执行命令', '处理结果']

    for i, (sx, sy, sname, scolor) in enumerate(steps):
        draw.rounded_rectangle([sx, sy, sx + 110, sy + 60], radius=6, outline=INK, width=1, fill=scolor)
        draw.text((sx + 10, sy + 22), sname, fill=INK, font=font)
        if i < len(steps) - 1:
            draw_arrow(draw, sx + 115, sy + 30, steps[i+1][0] - 5, steps[i+1][1] + 30)
            # Arrow text
            at = arrow_texts[i]
            mid_x = (sx + 115 + steps[i+1][0]) // 2
            draw.text((mid_x - 30, steps[i+1][1] + 5), at, fill='#666666', font=get_font(12))

    img.save(os.path.join(OUTPUT_DIR, '10-function-calling.png'))

# ========== Image 11: Memory System ==========
def create_memory_system():
    img, draw = create_body_base('记忆系统架构', '短期记忆与长期记忆协同工作', '10 / 12')
    w, h = 1920, 1080

    font = get_font(15)

    # Left: Short-term
    draw.text((350, 450), '短期记忆', fill=INK, font=get_font(22))
    draw.rounded_rectangle([300, 500, 750, 650], radius=8, outline=INK, width=1, fill=BLUE)
    draw.text((380, 540), 'Context Window', fill=INK, font=font)
    draw.text((380, 570), '容量有限 · 即时访问', fill='#666666', font=get_font(14))

    # Right: Long-term
    draw.text((1150, 450), '长期记忆', fill=INK, font=get_font(22))
    draw.rounded_rectangle([1050, 500, 1650, 650], radius=8, outline=INK, width=1, fill=LAVENDER)
    draw.text((1120, 540), 'Vector DB', fill=INK, font=font)
    draw.text((1120, 570), '持久存储 · 需检索获取', fill='#666666', font=get_font(14))

    # Bridge
    draw.text((870, 530), '记忆管理器', fill=INK, font=get_font(16))
    draw_arrow(draw, 760, 570, 1040, 570)
    draw_arrow(draw, 1040, 600, 760, 600)
    draw.text((820, 555), '存储 →', fill='#666666', font=get_font(12))
    draw.text((830, 615), '← 检索', fill='#666666', font=get_font(12))

    img.save(os.path.join(OUTPUT_DIR, '11-memory-system.png'))

# ========== Image 12: Multi-Agent ==========
def create_multi_agent():
    img, draw = create_body_base('多智能体系统', '层次架构与平级架构两种协作模式', '11 / 12')
    w, h = 1920, 1080

    font = get_font(15)

    # Left: Hierarchical
    draw.text((400, 400), '层次架构', fill=INK, font=get_font(22))
    # Orchestrator
    draw.ellipse([430, 480, 530, 540], outline=INK, width=1, fill=BLUE)
    draw.text((450, 498), 'Orchestrator', fill=INK, font=get_font(13))
    # Sub-agents
    for i, (sname, sx) in enumerate([('搜索 Agent', 370), ('计算 Agent', 510), ('写作 Agent', 650)]):
        draw.ellipse([sx, 600, sx + 80, 640], outline=INK, width=1, fill=GREEN)
        draw.text((sx + 8, 612), sname.split(' ')[0], fill=INK, font=get_font(12))
        draw.line([(480, 545), (sx + 40, 610)], fill=LIGHT_LINE, width=1)

    # Divider
    draw.line([(960, 400), (960, 700)], fill=LIGHT_LINE, width=1)

    # Right: Peer-to-peer
    draw.text((1150, 400), '平级架构', fill=INK, font=get_font(22))
    peers = [(1050, 520), (1220, 470), (1390, 520)]
    for px, py in peers:
        draw.ellipse([px, py, px + 80, py + 50], outline=INK, width=1, fill=PEACH)
    draw.text((1070, 535), 'Agent A', fill=INK, font=get_font(13))
    draw.text((1240, 485), 'Agent B', fill=INK, font=get_font(13))
    draw.text((1410, 535), 'Agent C', fill=INK, font=get_font(13))
    # Mesh lines
    draw.line([(1090, 545), (1260, 510)], fill=LIGHT_LINE, width=1)
    draw.line([(1260, 520), (1430, 545)], fill=LIGHT_LINE, width=1)
    draw.line([(1090, 555), (1430, 555)], fill=LIGHT_LINE, width=1)

    # Foundation
    draw.rounded_rectangle([600, 730, 1320, 780], radius=6, outline=INK, width=1, fill=LAVENDER)
    draw.text((750, 745), 'A2A 协议 · MCP 协议', fill=INK, font=get_font(18))

    img.save(os.path.join(OUTPUT_DIR, '12-multi-agent-system.png'))

# ========== Image 13: Learning Path ==========
def create_learning_path():
    img, draw = create_body_base('AI Agent 学习路径', '四阶段掌握智能体开发', '12 / 12')
    w, h = 1920, 1080

    font = get_font(17)
    steps = [
        (180, 700, '理解原理', BLUE),
        (580, 550, '上手工具', GREEN),
        (980, 420, 'Vibe Coding', PEACH),
        (1380, 300, 'Python 实战', LAVENDER),
    ]

    for i, (sx, sy, sname, scolor) in enumerate(steps):
        draw.ellipse([sx, sy, sx + 150, sy + 80], outline=INK, width=1, fill=scolor)
        draw.text((sx + 25, sy + 28), sname, fill=INK, font=font)
        if i < len(steps) - 1:
            draw_arrow(draw, sx + 155, sy + 40, steps[i+1][0] - 5, steps[i+1][1] + 40)

    # Flag at top right
    draw.polygon([(1500, 240), (1580, 260), (1500, 280)], fill=ACCENT)
    draw.text((1510, 250), '学成', fill='#FFFFFF', font=get_font(14))

    # Tiny learner figure (abstract)
    draw.ellipse([120, 740, 145, 765], outline=INK, width=1)
    draw.line([(132, 765), (132, 790)], fill=INK, width=1)

    img.save(os.path.join(OUTPUT_DIR, '13-learning-path.png'))

# ========== Main ==========
if __name__ == '__main__':
    print("Generating illustration images...")
    create_cover()
    create_fundamentals()
    create_tools()
    create_vibecoding()
    create_python()
    create_agent_core()
    create_architecture()
    create_agent_loop()
    create_rag()
    create_function_calling()
    create_memory_system()
    create_multi_agent()
    create_learning_path()
    print("\nDone! 13 images generated in:", OUTPUT_DIR)
    print("\nNOTE: These are functional placeholder images.")
    print("Replace with AI-generated handdrawn images using the prompts in images/prompts/")
