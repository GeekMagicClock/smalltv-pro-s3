# YouTube Guide

This guide helps new users set up the `YouTube` app from zero.

## 1. What the app shows

The app shows public channel data:

1. Channel title
2. Avatar
3. Subscriber count
4. Total views
5. Total videos

It only uses public data. It does not sign in to your YouTube account.

## 2. What you need

Prepare these two items:

1. `Channel Ref`
2. A `YouTube Data API v3` key

Also make sure:

1. The device is online
2. You can open `ii.html`

## 3. What is Channel Ref

The device supports:

1. Channel ID
2. `@handle`
3. username

Examples:

```text
UCxxxxxxxxxxxxxxxxxxxxxx
@openai
some_channel_name
```

Best choice:

1. `UC...` channel ID
2. `@handle`

## 4. How to get an API key

In Google Cloud Console:

1. Sign in
2. Create or select a project
3. Enable `YouTube Data API v3`
4. Create an API key
5. Copy the key

## 5. Configure the device

Open the `YouTube` page and fill in:

### Channel Ref

Example:

```text
@yourhandle
```

or

```text
UCxxxxxxxxxxxxxxxxxxxxxx
```

### API Key

Paste your YouTube Data API v3 key.

### Refresh Interval

Recommended default:

```text
60
```

## 6. Save and test

Recommended order:

1. Click `Open This App`
2. Fill `Channel Ref`
3. Fill `API Key`
4. Click `Save YouTube`
5. Click `Reload YouTube`

If everything is correct, the device will show your channel data.

## 7. Cache behavior

The app supports cache now.

That means:

1. If data was loaded before
2. The app can show cached data first
3. Then it refreshes in the background

Common status text:

1. `Cached just now`
2. `Cached · updated 25s ago`
3. `Live`
4. `Live · updated 25s ago`

## 8. Common problems

### `Set channel and API key`

This means the setup is incomplete.

### `Wi-Fi offline`

The device is not online.

### `HTTP xxx`

Usually one of these:

1. Invalid API key
2. API not enabled
3. Project quota problem
4. Wrong channel reference

### Subscriber count is `Hidden`

This is normal if the channel owner hides subscriber count.
