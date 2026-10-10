# 新闻聚合系统（Django + Vue + 爬虫）

基于 Python Django 与 Vue2 实现的新闻聚合系统。系统通过自建爬虫模块定时采集多个主流新闻源的文章数据，经清洗、分类后统一入库，再由前后端分离的 Web 应用对外提供新闻浏览、检索、评论互动等聚合服务。

## 技术栈

| 层次 | 技术 |
| --- | --- |
| 后端 | Python 3 / Django 3.x（自定义 Router/CTX 路由封装、Token 鉴权、CORS 中间件） |
| 数据库 | MySQL（`project_db`） |
| 用户端前端 | Vue 2 + Element UI + Bootstrap Vue（`static/home`） |
| 管理端前端 | Vue 2 + Element UI（`static/admin`） |
| 爬虫模块 | requests + pandas，threading 定时调度（`spider/`） |

## 功能模块

- **新闻聚合采集**：爬虫支持中新网、人民网、腾讯新闻、新华网等多个新闻源，支持 CSV 导出与 MySQL 落库，含去重（unique_id）、清洗、分类与定时调度
- **新闻浏览**：首页轮播、导航分类、新闻列表 / 详情、关键词搜索、浏览历史
- **用户体系**：注册登录、找回密码（邮箱验证码）、用户中心、个人资料、用户分组
- **互动功能**：评论、点赞、收藏、关注、私信、消息通知
- **内容管理（管理端）**：新闻 / 文章管理、栏目分类、新闻来源与资源管理、轮播图、公告管理
- **运营支撑**：敏感词过滤、点击量统计、操作日志、视频 / 媒体资源管理

## 目录结构

```
project/
├── app/                 # Django 后端
│   ├── core/            # 控制器与 MySQL 封装
│   ├── services/        # 业务逻辑层
│   ├── views/           # 视图层
│   ├── settings.py      # 配置（数据库、邮箱等）
│   └── router.py        # 路由封装
├── spider/              # 新闻爬虫模块（采集/清洗/分类/调度/入库）
├── static/
│   ├── home/            # 用户端 Vue 前端
│   └── admin/           # 管理端 Vue 前端
├── project.sql          # 数据库初始化脚本
├── 安装.bat / 运行.bat    # 依赖安装与启动脚本
└── 数据库设计文档.doc
```

## 快速开始

### 1. 环境准备

- Python 3.8+、MySQL 5.7+、Node.js（如需二次开发前端）

### 2. 初始化数据库

```bash
# 创建数据库并导入
mysql -u root -p -e "CREATE DATABASE project_db DEFAULT CHARACTER SET utf8mb4;"
mysql -u root -p project_db < project.sql
```

### 3. 配置后端

修改 `app/settings.py` 中的数据库连接（默认 `root/root@127.0.0.1:3306`），以及邮箱 SMTP 授权码（用于注册 / 找回密码验证码发送）。

### 4. 安装依赖并启动

```bash
pip install django pymysql pillow

# 启动后端（或直接双击 运行.bat）
python manage.py runserver 0.0.0.0:5000
```

前端已包含构建产物（`static/home/dist`、`static/admin/dist`），由 Django 静态文件直接提供服务，克隆后启动后端即可访问。

### 5. 启动爬虫（可选）

```bash
cd spider
# 按 spider/说明.txt 配置 config/config.ini 后启动
python app.py        # 手动采集
python scheduler.py  # 定时调度采集
```

## 说明

- 本仓库仅包含系统源码与数据库脚本，供学习交流使用。
- 爬虫仅用于学习目的，请合理控制采集频率并遵守目标站点相关条款。
