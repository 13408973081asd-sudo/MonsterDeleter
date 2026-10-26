# MonsterDeleter 🐉 大将怪兽摧毁文件

> 一只可爱又凶悍的大将怪兽，帮你把文件"吃掉"——其实只是**移入回收站**，随时可以恢复！

Windows 桌面趣味桌宠。右键任意文件 → 【召唤大将怪兽摧毁文件】→ 怪兽张嘴把文件吞掉 → 文件被安全地移入回收站。

⚠️ **它是个好玩的活动动画，不是数据销毁工具。** 它不会永久粉碎文件，删除方式是可恢复的回收站。请不要用它处理涉密、重要文件，也不要指望它帮你"彻底删除"数据。

---

## ✨ 功能特性

| 特性 | 说明 |
|------|------|
| 🖱 右键菜单 | 文件右键菜单新增【召唤大将怪兽摧毁文件】，一键呼出 |
| 🎞 动画特效 | 怪兽张嘴 → 张大 → 猛吞 → 咀嚼 → 喘气，全程透明背景循环动画 |
| ♻️ 安全删除 | 通过 `send2trash` **移入回收站**，可随时恢复，绝不永久删除 |
| 🪟 窗口风格 | 透明背景、无边框、置顶、不进任务栏（工具窗口） |
| 📦 单文件打包 | PyInstaller 打包为单个 exe，绿色免安装 |
| 🔓 开源 | MIT License，素材全部程序化生成，无版权问题 |

---

## 📁 工程结构

```
MonsterDeleter/
├── main.py                    # 主程序（PySide6 桌宠窗口）
├── build.bat                  # PyInstaller 打包脚本
├── requirements.txt           # 依赖清单
├── install_menu.reg           # 右键菜单安装注册表
├── uninstall_menu.reg         # 右键菜单卸载注册表
├── README.md
├── LICENSE
├── .gitignore
├── assets/
│   ├── monster.gif            # 怪兽动画素材（程序化生成）
│   └── monster.ico            # 应用/菜单图标
└── scripts/
    ├── generate_monster.py    # 生成怪兽动画 GIF（PIL）
    └── make_icon.py           # 从 GIF 首帧生成 .ico 图标
```

---

## 🚀 快速开始

### 方式一：源码直接运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. （可选）重新生成动画素材
python scripts\generate_monster.py
python scripts\make_icon.py

# 3. 直接调用（把目标文件/文件夹路径作为参数传入）
python main.py "C:\Users\me\Desktop\demo.txt"
```

### 方式二：打包成 exe + 注册右键菜单（推荐）

```bash
# 1. 打包（产物：dist\MonsterDeleter.exe）
build.bat

# 2. 编辑 install_menu.reg，把里面的 EXE_PATH 替换为真实路径
#    例如：  "D:\Tools\MonsterDeleter\MonsterDeleter.exe"

# 3. 双击 install_menu.reg 导入注册表
# 4. 右键任意文件 → 【召唤大将怪兽摧毁文件】🎉
```

---

## 🖱 使用说明

1. **呼出**：右键任意文件（或文件夹），选择【召唤大将怪兽摧毁文件】。
2. **确认**：弹出确认框，点「Yes」后怪兽开始动画；播放中可点「放它一马」取消。
3. **删除**：动画结束后，目标被移入回收站并弹窗提示。
4. **恢复**：打开回收站，找到文件还原即可（等同普通删除）。

> 命令行也可直接带路径运行：`MonsterDeleter.exe "目标路径"`。

---

## 🔧 自定义怪兽

想换颜色、体型？直接改 `scripts/generate_monster.py` 里的 `BODY`、`BELLY`、`MOUTH_IN` 等颜色常量，或调整 `FRAMES` / `FPS`，然后重新运行脚本即可重新生成 `monster.gif`。

---

## 🧯 卸载

- 双击 `uninstall_menu.reg` 移除右键菜单。
- 删除 `dist\MonsterDeleter.exe` 及整个工程目录即可（无后台服务、无开机自启）。

---

## ⚠️ 免责声明

- 本项目是趣味玩具，**不保证数据安全**，请勿用于删除任何你不愿失去的文件。
- 杀毒软件可能对 PyInstaller 打包的单文件 exe 误报，属于正常现象；介意可改用源码运行。
- 你对自己电脑上执行的任何删除操作负责。

---

## 📄 License

[MIT](./LICENSE) © MonsterDeleter contributors
