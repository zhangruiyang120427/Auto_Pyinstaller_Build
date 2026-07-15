# Auto_Pyinstaller_Build

把 `files/` 下的 Python 脚本一键打包成 Windows 单 exe，**全部在 GitHub Actions 云端跑**，本地零环境依赖。

## 一、用法

1. 把你的 Python 源码放到 `files/` 目录下
   - 如果是单个文件，**推荐重命名为 `main.py`**（工作流会优先用它作为入口）
   - 也支持任意文件名 —— 工作流会按 `main.py` → 字典序第一个 `.py` 的顺序自动找入口
2. （可选）把项目依赖写到 `files/requirements.txt`
3. 进 Actions 页 → 选 `Python打包-自带样例-缓存依赖-安全打包` → Run workflow，按需调参数
4. 跑完后在 Artifacts 区域下载 `Windows-<exe名>.zip`

## 二、工作流会自动做的事

| 步骤 | 说明 |
| --- | --- |
| 拉取仓库 | 含 `files/` 下所有源文件 |
| 配置 Python | 装指定版本（3.8~3.11），**pip 缓存** 复用上次下载的依赖包 |
| 装依赖 | 优先读 `files/requirements.txt`，再叠加 UI 里"额外依赖"输入框 |
| 找入口 | `main.py` 优先；否则取 `files/` 下第一个 `.py` |
| 决定 EXE 名 | 留空则与入口 `.py` 同名；填了就用填的 |
| 跑 PyInstaller | 拼好 `-F/-w/-c/-n` 参数执行 |
| 搬产物 | 把 `dist/*.exe` 移到 `build/` |
| 上传 Artifacts | 提供 zip 下载 |

## 三、目录约定

```
Auto_Pyinstaller_Build/
├── .github/workflows/build.yml    # 打包工作流
├── files/
│   ├── main.py                    # ⭐ 入口：替换成你自己的脚本
│   ├── requirements.txt           # ⭐ 依赖：填你项目用到的 pip 包
│   └── readme.txt
├── build/
│   └── readme.txt                 # 打包后 exe 会出现在这里（已在 .gitignore 忽略 .exe）
└── README.md
```

## 四、参数说明

| 参数 | 含义 | 推荐 |
| --- | --- | --- |
| `console_mode` | 是否保留黑色控制台窗口 | GUI 选 `-w`；带 print 选 `-c` |
| `build_mode` | 单 exe 还是文件夹 | 选 `-F`（单文件，分发方便） |
| `exe_name` | 产物名 | 留空默认与源码同名 |
| `python_ver` | 打包用 Python | **必须和你本地解释器版本一致** |
| `py_deps` | 临时补的依赖 | 常规依赖请改 `requirements.txt` |

## 五、常见问题

**Q：为什么 exe 体积很大？**
A：PyInstaller 默认会把 Python 解释器和所有依赖一起打进 exe，几十 MB 是正常的。可以用 UPX 或 `--exclude-module` 瘦身。

**Q：本地能跑，打出来的 exe 闪退？**
A：八成是少了依赖 / 数据文件。优先：
1. 把缺的所有包都写进 `files/requirements.txt`
2. 资源文件用 `--add-data "src;."` 加到工作流（需要小改 build.yml）

**Q：能不能指定图标？**
A：放一个 `files/icon.ico`，在 build.yml 的 `pyinstaller` 命令里加 `--icon files/icon.ico`。

**Q：为什么不再删除源码了？**
A：旧版本会跑完删 `files/*.py`，导致下次打包失败。新版本只把 `dist/*.exe` 搬到 `build/`，**源文件一律保留**。
