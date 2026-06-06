# YouTube 使用教程

本文帮助第一次使用设备的新用户，从 0 开始配置 `YouTube` app。

## 一、这个 app 会显示什么

它会显示公开频道数据：

1. 频道标题
2. 头像
3. 订阅数
4. 总观看数
5. 视频总数

它只读取公开数据，不会登录你的 YouTube 账号。

## 二、开始前需要准备什么

请准备两项：

1. `Channel Ref`
2. `YouTube Data API v3` 的 API Key

同时确认：

1. 设备已经联网
2. 你能打开 `settings.html`

## 三、什么是 Channel Ref

设备支持三种写法：

1. Channel ID
2. `@handle`
3. username

例如：

```text
UCxxxxxxxxxxxxxxxxxxxxxx
@openai
some_channel_name
```

最推荐填写：

1. `UC...` 开头的频道 ID
2. `@handle`

## 四、如何获取 API Key

在 Google Cloud Console 中：

1. 登录账号
2. 新建或选择项目
3. 启用 `YouTube Data API v3`
4. 创建 API Key
5. 复制这个 key

常用链接：

1. 创建 API Key：<https://console.cloud.google.com/apis/credentials>
2. 官方说明：<https://developers.google.com/youtube/registering_an_application>

## 五、如何在设备网页里配置

打开 `YouTube` 页面后，依次填写：

### Channel Ref

例如：

```text
@yourhandle
```

或者：

```text
UCxxxxxxxxxxxxxxxxxxxxxx
```

### API Key

填入你的 YouTube Data API v3 key。

### Refresh Interval

建议先用默认值：

```text
60
```

## 六、保存并验证

建议按这个顺序：

1. 点击 `Open This App`
2. 填写 `Channel Ref`
3. 填写 `API Key`
4. 点击 `Save YouTube`
5. 点击 `Reload YouTube`

如果都正确，设备会开始显示频道数据。

## 七、缓存说明

现在这个 app 支持缓存。

意思是：

1. 如果之前成功拉取过数据
2. 再次进入 app 时
3. 设备会先显示缓存
4. 后台再联网刷新

常见状态：

1. `Cached just now`
2. `Cached · updated 25s ago`
3. `Live`
4. `Live · updated 25s ago`

## 八、常见问题

### 显示 `Set channel and API key`

说明配置还不完整。

### 显示 `Wi-Fi offline`

说明设备当前没联网。

### 显示 `HTTP xxx`

一般是：

1. API Key 无效
2. API 没启用
3. 项目配额有问题
4. 频道标识写错

### 订阅数显示 `Hidden`

这是正常情况，说明频道拥有者隐藏了订阅数。
