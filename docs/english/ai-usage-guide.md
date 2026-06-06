# AI Usage Guide

This guide is for new users. It helps you set up `AI Usage` from zero so the device can show Claude or Codex usage.

## 1. Before you start

Please check these items first:

1. The device is powered on.
2. The device and your computer are on the same local network.
3. You can open the device web page `settings.html`.
4. You know the device IP address.
5. Python 3 is installed on your computer.

Check Python:

```bash
python3 --version
```

On Windows you can also use:

```bash
py --version
```

## 2. How AI Usage works

`AI Usage` shows local AI usage data on the device.

Supported sources:

1. Claude
2. Codex

You run a Python script on your computer:

1. The script reads local usage data.
2. The script sends data to the device by HTTP.
3. The device updates the `AI Usage` app.

Both Claude and Codex send data to:

```text
/api/claude_usage
```

## 3. Claude setup

### Step 1

Open `AI Usage` on the device.

### Step 2

Download:

```text
claude_usage.py
```

Direct download:

<https://raw.githubusercontent.com/GeekMagicClock/smalltv-pro-s3/main/tools/claude_usage.py>

### Step 3

Run:

```bash
python3 claude_usage.py 192.168.1.123
```

Replace `192.168.1.123` with your real device IP.

Windows:

```bash
py claude_usage.py 192.168.1.123
```

### Step 4

Keep the script running and keep the device on the `AI Usage` page.

## 4. Codex setup

### Step 1

Open `AI Usage` on the device.

### Step 2

Download:

```text
codex_usage.py
```

Direct download:

<https://raw.githubusercontent.com/GeekMagicClock/smalltv-pro-s3/main/tools/codex_usage.py>

### Step 3

Run:

```bash
python3 codex_usage.py 192.168.1.123
```

Windows:

```bash
py codex_usage.py 192.168.1.123
```

### Step 4

Make sure local Codex session data exists.

Typical path:

```text
~/.codex/sessions
```

Windows native path is usually:

```text
C:\Users\YourName\.codex\sessions
```

If there is no session yet, use Codex once first, then run the script again.

## 5. Common problems

### No update on the device

Check these items:

1. Correct device IP
2. Same local network
3. Device is on `AI Usage`
4. The script is still running
5. Claude or Codex has local usage data

### Network error

Usually this means:

1. Wrong IP
2. Device offline
3. Different network
4. Router isolation

### Windows script starts but no data

Check:

1. You are using native Windows, not WSL
2. `.codex/sessions` exists
3. Codex already created at least one session
