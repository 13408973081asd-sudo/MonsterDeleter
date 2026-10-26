#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MonsterDeleter —— 大将怪兽摧毁文件桌宠
=====================================
Windows 桌面趣味桌宠：
  1. 通过右键菜单【召唤大将怪兽摧毁文件】呼出
  2. 弹出透明、置顶、无边框的怪兽动画窗口
  3. 确认后把文件/文件夹【移入回收站】（可恢复，不做永久粉碎）
  4. 玩法是整活动画，不是数据销毁工具

用法（通过右键菜单调用，把目标路径作为第一个参数传入）：
    MonsterDeleter.exe  "C:\\path\\to\\target.txt"
也可以命令行直接运行： python main.py "C:\\path\\to\\target.txt"
"""

import os
import sys
import platform

try:
    import send2trash
except ImportError:  # pragma: no cover
    send2trash = None

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QMessageBox, QPushButton, QVBoxLayout, QHBoxLayout,
)

APP_TITLE = "MonsterDeleter · 大将怪兽摧毁文件"

ANIM_DURATION_MS = 4200      # 怪兽动画总时长
GIF = "assets/monster.gif"   # 动画素材，打包后需与 exe 同层或位于 assets 目录


def resource_path(rel: str) -> str:
    """兼容 PyInstaller 打包（--onefile 时资源在临时解包目录）与源码直接运行。"""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


class MonsterWindow(QWidget):
    """透明、无边框、置顶的怪兽动画窗口。

    流程：确认框(Yes) -> 播放怪兽吞噬动画 -> send2trash 移入回收站 -> 完成提示。
    """

    def __init__(self, target_path: str, parent=None):
        super().__init__(parent)
        self.target_path = target_path
        self.trashed_ok = False

        flags = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        if platform.system() == "Windows":
            flags |= Qt.WindowTransparentForInput | Qt.WindowDoesNotAcceptFocus
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle(APP_TITLE)
        self.resize(340, 340)

        self._label = QLabel("", self)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setStyleSheet("background: transparent;")

        self._btn = QPushButton("放它一马", self)
        self._btn.setFixedWidth(110)
        self._btn.setStyleSheet(
            "QPushButton { background:#ffe08a; color:#5b3a00; border:2px solid #c9852b;"
            " border-radius:14px; font-size:14px; font-weight:bold; padding:6px 10px;}"
            "QPushButton:hover { background:#ffd06a; }"
        )
        self._btn.hide()
        self._btn.clicked.connect(self._cancel)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._label, 1)
        hb = QHBoxLayout()
        hb.addStretch()
        hb.addWidget(self._btn)
        hb.addStretch()
        lay.addLayout(hb)
        lay.setAlignment(hb, Qt.AlignBottom)

        gif_path = resource_path(GIF)
        if os.path.isfile(gif_path):
            self._movie = QMovie(gif_path)
            self._label.setMovie(self._movie)
            self._movie.start()
        else:
            self._label.setText("（未找到 monster.gif 动画素材）\n即将把文件移入回收站…")

        self._place_near_cursor()

        QTimer.singleShot(300, self._ask_confirm)

    def _place_near_cursor(self) -> None:
        cursor = QCursorPos()
        self.move(cursor.x() - self.width() // 2, cursor.y() - self.height() // 2)

    def _ask_confirm(self) -> None:
        if send2trash is None:
            QMessageBox.critical(
                self, APP_TITLE,
                "缺少依赖库 send2trash。\n请先执行：\n    pip install send2trash\n"
                "装好后重新运行。",
            )
            self.close()
            return

        name = os.path.basename(self.target_path) or self.target_path
        ret = QMessageBox.question(
            self,
            APP_TITLE,
            f"怪兽要把「{name}」吃掉啦！\n\n"
            "吃进肚子后会【移入回收站】，可以随时恢复，\n不会永久粉碎文件。\n\n"
            "确定要召唤大将怪兽吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if ret != QMessageBox.Yes:
            self.close()
            return

        self._btn.show()
        QTimer.singleShot(ANIM_DURATION_MS, self._do_trash)

    def _cancel(self) -> None:
        """动画播放中点击“放它一马”，放弃删除。"""
        self.close()

    def _do_trash(self) -> None:
        if self.trashed_ok:
            return
        self.trashed_ok = True
        try:
            send2trash.send2trash(self.target_path)
            QMessageBox.information(
                self, APP_TITLE,
                "嗷呜～ 怪兽已经把文件丢进回收站了！\n\n"
                "想找回的话，去回收站里翻一翻就行～",
            )
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(
                self, APP_TITLE,
                "怪兽打了个嗝，删除失败了：\n\n" + str(exc),
            )
        self.close()


def QCursorPos() -> QPoint:
    """返回当前鼠标所在的屏幕坐标（兼容多显示器）。"""
    from PySide6.QtGui import QCursor
    return QCursor.pos()


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)

    if len(sys.argv) < 2:
        QMessageBox.information(
            None, APP_TITLE,
            "请通过文件右键菜单【召唤大将怪兽摧毁文件】来使用本程序。\n"
            "用法：MonsterDeleter.exe \"文件或文件夹路径\"",
        )
        return 0

    target = sys.argv[1].strip('"')
    if not os.path.exists(target):
        QMessageBox.warning(None, APP_TITLE, f"找不到目标：{target}")
        return 1

    win = MonsterWindow(target)
    win.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
