# Emotion Diary 🎭

基于 FastAPI + Streamlit 的心情日记应用，支持用户注册登录、树洞对话（未来接入大模型 API）、情绪日记管理，以及情绪数据可视化仪表盘。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 前端框架 | Streamlit |
| 数据库 | SQLite（开发）/ PostgreSQL（生产） |
| ORM | SQLAlchemy 2.0 |
| 认证 | JWT (python-jose + passlib) |

## 项目结构

```
emotion-diary/
├── backend/
│   ├── main.py              # FastAPI 入口，注册路由 & 初始化数据库
│   ├── config.py            # 环境变量配置（DB URL / JWT）
│   ├── database.py          # SQLAlchemy engine & session
│   ├── auth.py              # JWT 工具：hash、token 签发/校验
│   ├── models/              # SQLAlchemy ORM 模型
│   │   ├── user.py          # 用户表
│   │   ├── conversation.py  # 对话记录表
│   │   └── diary.py         # 日记表
│   ├── schemas/             # Pydantic 请求/响应模型
│   ├── routers/             # API 路由
│   │   ├── auth.py          # 注册 & 登录
│   │   ├── conversation.py  # 树洞对话
│   │   ├── diary.py         # 日记 CRUD
│   │   └── dashboard.py     # 情绪统计 & 时间线
│   └── requirements.txt
├── frontend/
│   ├── app.py               # Streamlit 主页（导航）
│   ├── api.py               # 后端 API 封装
│   ├── pages/
│   │   ├── login.py         # 登录 / 注册页
│   │   ├── chat.py          # 树洞对话页
│   │   ├── diary.py         # 日记列表 & 撰写
│   │   └── dashboard.py     # 情绪仪表盘
│   └── requirements.txt
├── .env.example             # 环境变量模板
├── requirements.txt         # 共享依赖
├── .gitignore
└── README.md
```

## 快速开始

### 1. 环境准备

- Python 3.10+

### 2. 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 3. 配置环境变量（可选）

```bash
copy .env.example .env
# 默认使用 SQLite，无需额外配置
# 切换到 PostgreSQL 时取消 .env 中 DATABASE_URL 的注释并修改
```

### 4. 启动后端

```bash
cd emotion-diary
python -m uvicorn backend.main:app --reload --port 8000
```

后端运行在 http://localhost:8000 ，访问 /docs 可查看 Swagger 接口文档。

### 5. 启动前端

```bash
cd emotion-diary
python -m streamlit run frontend/app.py
```

前端运行在 http://localhost:8501 。

## API 概览

| 模块 | 端点 | 说明 |
|------|------|------|
| Auth | POST `/auth/register` | 用户注册 |
| Auth | POST `/auth/login` | 用户登录，返回 JWT |
| Chat | POST `/chat/` | 发送消息（需认证） |
| Chat | GET `/chat/history` | 获取对话历史 |
| Diary | POST `/diary/` | 创建日记 |
| Diary | GET `/diary/` | 日记列表 |
| Diary | GET `/diary/{id}` | 日记详情 |
| Diary | DELETE `/diary/{id}` | 删除日记 |
| Dashboard | GET `/dashboard/mood-timeline` | 情绪时间线数据 |
| Dashboard | GET `/dashboard/stats` | 心情分布统计 |

## 未来计划

- [ ] 接入大模型 API（OpenAI / 本地模型）实现智能对话
- [ ] 对话结束后自动生成情绪日记
- [ ] 情绪评分模型（NLP 分析对话内容）
- [ ] 更丰富的图表（折线图、热力图、词云）
- [ ] 数据导出（PDF / Markdown）
