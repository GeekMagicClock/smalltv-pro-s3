# AI Usage 使用教程

本文面向第一次使用设备的新用户，目标是帮助你从 0 开始配置 `AI Usage`，让设备显示 Claude 或 Codex 的使用情况。

## 一、开始前先确认

请先确认下面几项：

1. 设备已经开机
2. 设备和电脑在同一个局域网
3. 你能打开设备网页 `settings.html`
4. 你知道设备的 IP 地址
5. 电脑已经安装 Python 3

检查 Python：

```bash
python3 --version
```

Windows 也可以用：

```bash
py --version
```

## 二、AI Usage 是怎么工作的

`AI Usage` 用来把电脑上的 AI 使用数据显示到设备上。

当前支持：

1. Claude
2. Codex

你需要在电脑上运行一个 Python 脚本：

1. 脚本读取本地使用数据
2. 脚本通过 HTTP 把数据发给设备
3. 设备更新 `AI Usage` 页面

Claude 和 Codex 最终都发到这个接口：

```text
/api/claude_usage
```

## 三、Claude 使用步骤

### 第 1 步

先在设备上打开 `AI Usage` app。

### 第 2 步

下载：

```text
claude_usage.py
```

直接下载：

<https://raw.githubusercontent.com/GeekMagicClock/smalltv-pro-s3/main/tools/claude_usage.py>

### 第 3 步

运行：

```bash
python3 claude_usage.py 192.168.1.123
```

把 `192.168.1.123` 换成你的真实设备 IP。

Windows 也可以用：

```bash
py claude_usage.py 192.168.1.123
```

### 第 4 步

保持脚本运行，并让设备停留在 `AI Usage` 页面。

## 四、Codex 使用步骤

### 第 1 步

先打开设备上的 `AI Usage`。

### 第 2 步

下载：

```text
codex_usage.py
```

直接下载：

<https://raw.githubusercontent.com/GeekMagicClock/smalltv-pro-s3/main/tools/codex_usage.py>

### 第 3 步

运行：

```bash
python3 codex_usage.py 192.168.1.123
```

Windows 也可以用：

```bash
py codex_usage.py 192.168.1.123
```

### 第 4 步

确认本地有 Codex session 数据。

常见路径：

```text
~/.codex/sessions
```

Windows 原生环境一般是：

```text
C:\Users\你的用户名\.codex\sessions
```

如果还没有任何会话记录，先用一次 Codex，再重新运行脚本。

## 五、常见问题

### 设备没有更新

请检查：

1. IP 是否正确
2. 设备和电脑是否同网
3. 设备是否停留在 `AI Usage`
4. 脚本是否还在运行
5. 本地是否真的有 Claude 或 Codex 数据

### 脚本提示网络错误

一般是：

1. IP 写错
2. 设备离线
3. 电脑和设备不在同一个网络
4. 路由器做了隔离

### Windows 能运行但没有数据

请检查：

1. 你是不是在原生 Windows 环境，不是 WSL
2. `.codex/sessions` 是否存在
3. Codex 是否已经产生过至少一次会话
