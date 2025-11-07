# 数据库信息

## 当前数据存储位置

**数据库类型**: PostgreSQL (Neon DB - 云端托管)

**连接信息**:
- **提供商**: Neon (neon.tech)
- **数据库名**: `neondb`
- **连接字符串**: 存储在 `backend/.env` 文件中的 `DATABASE_URL`

## 数据库连接详情

你的数据存储在 **Neon DB** 云端 PostgreSQL 数据库中。

Neon 是一个 Serverless PostgreSQL 服务，特点：
- ✅ 云端托管，无需本地安装
- ✅ 自动备份
- ✅ 高可用性
- ✅ 免费 tier 可用

## 数据库表结构

当前数据库包含以下表：

1. **users** - 用户信息
   - 邮箱、密码哈希、姓名、学校、年级等
   - 兴趣爱好、身高、体重、国籍、人种
   - 照片、头像、验证状态等

2. **date_requests** - 约会邀请
   - 发送者、接收者、状态、消息等

3. **events** - 校园活动
   - 标题、描述、地点、时间、标签等

4. **event_attendees** - 活动参与者
   - 用户ID、活动ID、RSVP状态

5. **messages** - 消息
   - 发送者、接收者、内容、时间戳

6. **matches** - 匹配记录
   - 用户ID、匹配用户ID、匹配分数

## 查看数据库

### 方式 1: 使用 Neon Dashboard
1. 访问 [Neon Console](https://console.neon.tech/)
2. 登录你的账户
3. 选择项目
4. 可以查看数据库、运行 SQL 查询等

### 方式 2: 使用 psql 命令行
```bash
psql 'postgresql://neondb_owner:npg_0UiRFOK1qGml@ep-plain-leaf-a4h7kg5v-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
```

### 方式 3: 使用数据库管理工具
- **pgAdmin**: 图形化 PostgreSQL 管理工具
- **DBeaver**: 通用数据库管理工具
- **TablePlus**: macOS 数据库管理工具

使用上面的连接字符串连接即可。

## 数据安全

- ✅ 密码使用 bcrypt 加密存储
- ✅ 数据库连接使用 SSL
- ✅ 敏感信息不会在日志中暴露

## 备份

Neon DB 提供自动备份功能。你也可以：
1. 在 Neon Console 中创建手动备份
2. 使用 `pg_dump` 导出数据

## 迁移到其他数据库

如果需要迁移到其他数据库（如本地 PostgreSQL、Supabase 等），可以：
1. 导出当前数据
2. 更新 `DATABASE_URL` 在 `.env` 文件中
3. 运行数据库迁移脚本

