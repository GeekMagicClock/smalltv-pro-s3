# AI Usage 使用教程

本文面向第一次使用设备的新用户，目标是帮助你从 0 开始配置 `AI Usage`，让设备显示 Claude 或 Codex 的使用情况。

---

## 一、准备工作

开始前，请先确认下面几项：

1. 设备已经开机，并连接到和电脑同一个局域网
2. 你能打开设备网页 `ii.html`
3. 你知道设备当前的局域网 IP
4. 电脑已经安装 Python 3

### 如何确认 Python 3

在终端或命令行里执行：

```bash
python3 --version
```

如果是 Windows，也可以试：

```bash
py --version
```

看到 `Python 3.x.x` 就可以继续。

### 如何确认设备 IP

最简单的方法：

1. 打开设备网页
2. 看浏览器地址栏
3. 如果地址像 `http://192.168.1.123/...`，那么 `192.168.1.123` 就是设备 IP

如果你是通过热点名称、局域网域名或别的方式访问设备，请到路由器后台或设备网络页确认它的真实 IP。

---

## 二、AI Usage 的工作原理

`AI Usage` 用来显示桌面端 AI 工具的使用状态。当前支持：

1. Claude
2. Codex

你需要在电脑上运行一个 Python 脚本：

1. 脚本从本地 AI 客户端目录读取使用数据
2. 脚本定时把数据通过 HTTP 发送到设备
3. 设备上的 `AI Usage` app 接收后更新显示

Claude 和 Codex 最终都会把数据发送到设备的同一个接口：

```text
/api/claude_usage
```

设备会根据 payload 自动区分来源。

所以必须同时满足：

1. 电脑本地有可读取的使用记录
2. 电脑能访问设备 IP
3. 设备当前能联网并正常运行 `AI Usage`

---

## 三、Claude 使用步骤

### 步骤 1：打开设备上的 AI Usage

在设备网页中进入 `AI Usage` 页面，点击：

```text
Open This App
```

保持设备停留在 `AI Usage` app，方便立即看到更新结果。

### 步骤 2：下载 Claude 脚本

在网页中下载：

```text
claude_usage.py
```

建议把它放在一个容易找到的目录，比如：

1. 桌面
2. 下载目录
3. 你自己的脚本工具目录

### 步骤 3：运行脚本

在脚本所在目录打开终端，执行：

```bash
python3 claude_usage.py 192.168.1.123
```

把 `192.168.1.123` 替换成你的真实设备 IP。

如果是 Windows，也可以用：

```bash
py claude_usage.py 192.168.1.123
```

### 步骤 4：观察输出

脚本正常运行时，通常会周期性打印：

1. 当前读取到的数据
2. 向设备 POST 的结果

如果设备端收到数据，`AI Usage` 页面会出现更新。

---

## 四、Codex 使用步骤

### 步骤 1：打开设备上的 AI Usage

和 Claude 一样，先在网页中点击：

```text
Open This App
```

### 步骤 2：下载 Codex 脚本

在网页中下载：

```text
codex_usage.py
```

### 步骤 3：运行脚本

在脚本所在目录打开终端，执行：

```bash
python3 codex_usage.py 192.168.1.123
```

Windows 也可以用：

```bash
py codex_usage.py 192.168.1.123
```

### 步骤 4：确认本地有 Codex 使用数据

`codex_usage.py` 需要读取本地 Codex session 数据。标准路径通常是：

```text
~/.codex/sessions
```

Windows 原生环境下通常对应：

```text
C:\Users\你的用户名\.codex\sessions
```

如果你的 Codex 还没有产生任何会话记录，脚本可能会提示没有找到数据。此时先在 Codex 中进行一次实际对话，再重新运行脚本。

---

## 五、常见问题

### 问题 1：设备没有任何更新

按顺序检查：

1. 设备和电脑是否在同一个局域网
2. 命令里的 IP 是否正确
3. 设备当前是否停留在 `AI Usage`
4. 本地脚本是否真的在持续运行
5. Claude / Codex 本地是否已经产生可读的使用记录

### 问题 2：脚本提示网络错误

通常是这些原因：

1. IP 写错
2. 设备离线
3. 电脑和设备不在同一网络
4. 路由器隔离了客户端之间的访问

### 问题 3：Windows 上脚本能启动，但没有数据

先确认：

1. 你是在 Windows 原生 Codex 环境里使用，不是 WSL
2. 本地存在 `.codex/sessions`
3. Codex 已经实际产生过会话记录

如果你是 WSL 中运行 Codex、Windows 中运行脚本，路径可能不一致，需要按实际环境调整脚本扫描目录。

---

## 六、推荐的首次上手顺序

建议按下面顺序操作：

1. 先确认设备网页可打开
2. 先确认设备 IP
3. 再确认 Python 3 可用
4. 然后先跑 Claude 或 Codex 其中一个脚本
5. 最后观察 `AI Usage` 页面是否稳定更新
