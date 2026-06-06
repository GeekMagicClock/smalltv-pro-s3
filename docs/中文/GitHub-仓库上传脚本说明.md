# GitHub 仓库上传脚本说明

脚本路径：

```text
tools/github_repo_uploader.py
```

默认目标仓库：

```text
GeekMagicClock/smalltv-pro-s3
```

## 一、HTTPS 或 SSH

脚本支持两种方式：

1. `https`
2. `ssh`

默认是：

```text
https
```

如果你已经配置好 GitHub SSH key，建议使用：

```text
--transport ssh
```

## 二、上传整个 docs 目录

```bash
python3 tools/github_repo_uploader.py \
  --transport ssh \
  --message "Upload multilingual docs" \
  --item docs=docs
```

## 三、上传单个文件

例如上传中文 AI Usage 教程：

```bash
python3 tools/github_repo_uploader.py \
  --transport ssh \
  --message "Upload Chinese AI Usage guide" \
  --item docs/中文/AI-Usage-使用教程.md=docs/中文/AI-Usage-使用教程.md
```

## 四、上传固件

```bash
python3 tools/github_repo_uploader.py \
  --transport ssh \
  --message "Upload firmware build" \
  --item .pio/build/smalltv-pro-s3/firmware.bin=firmware/firmware.bin
```

## 五、预演但不上传

```bash
python3 tools/github_repo_uploader.py \
  --transport ssh \
  --dry-run \
  --item docs=docs
```

## 六、使用前确认

请先确认：

1. 已安装 `git`
2. 已安装 Python 3
3. 你对目标仓库有写权限
4. 如果走 SSH，`ssh -T git@github.com` 能正常通过
