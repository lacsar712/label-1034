# 学生成绩管理系统

基于 Vue3 + Element Plus 与 FastAPI + SQLAlchemy 的简易学生成绩管理系统，支持班级管理、学生管理、课程管理、成绩录入与查询，**一键 Docker 部署**，无需本地安装 Node.js 或 Python。

---

## 功能概览

| 模块       | 说明 |
|------------|------|
| **成绩查询** | 按学生、课程筛选，查看成绩列表（含学生姓名、学号、课程、学分、成绩、考试时间） |
| **成绩录入** | 为学生选择课程并录入/修改成绩，支持按学生、课程筛选列表 |
| **学生管理** | 学生增删改查，按班级筛选；新增/编辑时从班级表选择班级 |
| **班级管理** | 班级增删改查；删除前校验该班下是否还有学生 |
| **课程管理** | 课程增删改查（课程名称、学分） |

---

## 技术栈

| 层级     | 技术 |
|----------|------|
| Frontend | Vue 3、Vite、Element Plus、Vue Router、Axios |
| Backend  | FastAPI、SQLAlchemy 2.0（异步）、Pydantic |
| Database| MySQL 8.0 |
| 部署     | Docker、Docker Compose、Nginx |

---

## 环境要求

- **Docker**（建议 20.10+）
- **Docker Compose**（建议 v2+）

无需在本机安装 Node.js、Python 或 MySQL。

---

## 快速部署（三步启动）

### 1. 克隆或解压项目

```bash
# 若从 Git 克隆
git clone <仓库地址>
cd 根目录


### 2. 一键构建并启动

在项目**根目录**（与 `docker-compose.yml` 同级）执行：

```bash
docker compose up -d --build
```

- 首次运行会拉取镜像、安装依赖、构建前后端，约需 **2～5 分钟**（视网络而定）。
- 后端会等待 MySQL 健康后再启动，并自动建表、执行 Seed 填充演示数据。

### 3. 访问系统

浏览器打开：

- **前端（系统入口）**：<http://localhost:31034>
- **后端 API 文档**：<http://localhost:8103/docs>

使用前端页面即可进行成绩查询、成绩录入、学生管理、班级管理、课程管理。

---

## 服务与端口

| 服务   | 地址 | 说明 |
|--------|------|------|
| 前端   | http://localhost:31034 | 用户操作界面，Nginx 提供静态资源并代理 `/api` 到后端 |
| 后端 API | http://localhost:8103 | FastAPI 服务；Swagger 文档：http://localhost:8103/docs |
| MySQL | localhost:3306 | 用户：`root`，密码：`root`，数据库：`student_grade` |

端口可在 `docker-compose.yml` 中修改（如宿主机端口冲突时）。

---

## 演示数据

首次启动后会自动执行 **Seed**，包含：

- **班级**：计算机1班、计算机2班、软件1班
- **学生**：5 名示例学生（张三、李四、王五、赵六、钱七），已关联上述班级
- **课程**：高等数学、大学英语、程序设计基础、数据结构（含学分）
- **成绩**：多条学生-课程成绩记录

打开前端即可直接查看与操作，无需手动建库或导入数据。

---

## 常用 Docker 命令

```bash
# 启动（后台）
docker compose up -d --build

# 查看运行状态
docker compose ps

# 查看日志（所有服务）
docker compose logs -f

# 仅查看后端日志
docker compose logs -f backend

# 停止并删除容器（不删数据卷）
docker compose down

# 停止并删除容器及数据卷（清空数据库）
docker compose down -v
```

---

## 数据持久化

- MySQL 数据保存在 Docker 卷 **`mysql_data`** 中。
- 执行 `docker compose down` 不会删除该卷，再次 `docker compose up -d` 时数据仍在。
- 需要**清空数据库**时，使用：`docker compose down -v`，下次启动会重新建表并再次执行 Seed。

---

## 项目结构（简要）

```
/
├── docker-compose.yml    # 编排：db、backend、frontend
├── backend/              # FastAPI 后端
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py       # 入口、CORS、生命周期（建表+Seed）
│       ├── config.py     # 配置（数据库等）
│       ├── database.py   # SQLAlchemy 异步引擎与会话
│       ├── seed.py       # 初始化演示数据
│       ├── models/       # 班级、学生、课程、成绩
│       ├── schemas/      # Pydantic 校验与响应
│       └── api/          # 班级、学生、课程、成绩 接口
└── frontend/             # Vue3 前端
    ├── Dockerfile        # 多阶段：Node 构建 + Nginx 运行
    ├── nginx.conf        # 静态资源 + /api 反向代理到后端
    ├── package.json
    └── src/
        ├── main.js
        ├── App.vue
        ├── router/
        ├── api/          # 请求封装与各模块 API
        └── views/        # 成绩查询、成绩录入、学生、班级、课程 页面
```

---

## 故障排查

### 1. 端口被占用

若 31034、8103 或 3306 已被占用，可修改 `docker-compose.yml` 中对应服务的 `ports`，例如：

```yaml
frontend:
  ports:
    - "31035:80"   # 将宿主机端口改为 31035
```

### 2. 后端启动失败或接口报错

- 查看后端日志：`docker compose logs -f backend`
- 确认 MySQL 已就绪：`docker compose ps` 中 `grade-db` 为 healthy 后再看 backend 是否启动成功。
- 后端会重试连接数据库约 30 次，若仍失败请检查本机防火墙或 Docker 网络。

### 3. 前端能打开但接口 404 / 502

- 确认后端已正常启动：访问 http://localhost:8103/docs 能打开 Swagger。
- 前端通过 Nginx 将 `/api` 代理到后端，请勿直接改前端里的 `localhost` 为宿主机 IP（容器内应使用服务名 `backend`）。

### 4. 重新构建某一服务

```bash
docker compose up -d --build backend   # 仅重建后端
docker compose up -d --build frontend  # 仅重建前端
```

### 5. 清空数据库并重新初始化

```bash
docker compose down -v
docker compose up -d --build
```

---

## 使用流程建议

1. 打开 http://localhost:31034，进入系统。
2. **班级管理**：先维护班级（如已有 Seed 数据可直接用）。
3. **学生管理**：按班级筛选、新增/编辑学生时选择班级。
4. **课程管理**：维护课程及学分。
5. **成绩录入**：选择学生、课程，录入或修改成绩。
6. **成绩查询**：按学生、课程筛选查看成绩列表。

---

## 许可证与说明

本项目为简易教学/示例项目。生产环境使用请自行加强鉴权、输入校验与安全配置。
