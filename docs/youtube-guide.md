# YouTube App 使用教程

本文面向第一次使用设备的新用户，目标是帮助你从 0 开始配置 `YouTube` app，让设备显示公开频道的数据卡片。

---

## 一、这个 app 能显示什么

`YouTube` app 显示的是公开频道数据。当前包括：

1. 频道标题
2. 头像
3. 订阅数
4. 总观看数
5. 视频总数

注意：

1. 它读取的是公开数据
2. 不会登录你的 YouTube 账号
3. 如果频道拥有者隐藏了订阅数，设备会显示 `Hidden`

---

## 二、开始前你需要准备什么

开始前需要准备两项：

1. `Channel Ref`
2. `YouTube Data API v3` 的 API Key

同时请确认：

1. 设备已经联网
2. 你能打开设备网页 `ii.html`
3. 设备和 Google API 之间的网络是通的

---

## 三、什么是 Channel Ref

设备支持三种写法：

1. `Channel ID`
2. `@handle`
3. `username`

例如：

```text
UCxxxxxxxxxxxxxxxxxxxxxx
@openai
some_channel_name
```

如果你不确定，最推荐填：

1. `UC...` 开头的频道 ID
2. 或者 `@handle`

这两种通常比旧式 username 更稳定。

---

## 四、如何获取 YouTube API Key

你需要在 Google Cloud Console 中完成下面几步：

1. 登录 Google Cloud Console
2. 新建一个项目，或者选择已有项目
3. 启用 `YouTube Data API v3`
4. 创建一个 API Key
5. 把生成的 key 复制出来

建议：

1. 先保证能跑通
2. 跑通后再给 key 加上配额和来源限制

---

## 五、在设备网页中配置 YouTube

进入 `YouTube` 页面后，依次填写：

### Channel Ref

填写你的频道标识，例如：

```text
@yourhandle
```

或者：

```text
UCxxxxxxxxxxxxxxxxxxxxxx
```

### API Key

填写你刚刚创建的 YouTube Data API v3 key。

### Refresh Interval

建议先用默认值：

```text
60
```

表示每 60 秒刷新一次。

---

## 六、保存并验证

推荐按这个顺序操作：

1. 点击 `Open This App`
2. 填写 `Channel Ref`
3. 填写 `API Key`
4. 点击 `Save YouTube`
5. 点击 `Reload YouTube`

如果配置正确，设备会开始显示频道数据。

---

## 七、缓存行为说明

现在 `YouTube` app 已经支持缓存。

这意味着：

1. 如果你以前成功拉取过频道数据
2. 重新进入 `YouTube` app 时
3. 设备会先显示上一次缓存的数据
4. 后台再异步联网刷新

所以刚进入 app 时，如果先看到旧数据，不是异常，是正常设计。

常见状态包括：

1. `Cached just now`
2. `Cached · updated 25s ago`
3. `Live`
4. `Live · updated 25s ago`

---

## 八、常见问题

### 问题 1：显示 `Set channel and API key`

说明当前还没有配置完整：

1. `Channel Ref` 为空
2. `API Key` 为空
3. 保存没有成功

### 问题 2：显示 `Wi-Fi offline`

说明设备当前没有联网。先检查设备的 Wi-Fi 配置。

### 问题 3：显示 `HTTP xxx`

常见原因：

1. API Key 无效
2. API 没有启用
3. Google Cloud 项目配额不足
4. 频道标识写错

### 问题 4：订阅数显示 `Hidden`

这不是错误，而是频道拥有者隐藏了公开订阅数。

### 问题 5：刚进 app 时显示的是旧数据

这是正常现象。设备会先显示缓存，再异步联网刷新。

---

## 九、推荐的首次上手顺序

如果你是第一次配置，建议按这个顺序来：

1. 先确认设备联网
2. 再确认你能打开设备网页
3. 准备好频道 `Channel Ref`
4. 在 Google Cloud 中准备好 `YouTube Data API v3` 的 API Key
5. 填入网页并保存
6. 点击 `Reload YouTube`
7. 观察设备是否显示频道数据
