# Copyright (c) 2025 김트리0516
# This software is licensed under the MIT License.


import sys
import os
import subprocess
import tempfile
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton,
    QTabWidget, QFileDialog, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QTextCursor

keyword_map = {
    "만일": "if", "이라면": "then", "아니면": "else", "그렇지않으면": "elseif", "끝": "end",
    "반복": "for", "동안": "while", "반복하기": "repeat", "까지": "until", "반복멈추기": "break",
    "돌려주기": "return", "하기": "do", "함수": "function", "지역": "local",
    "출력": "print", "숫자로": "tonumber", "문자열로": "tostring", "자료형": "type",
    "요구": "require", "오류": "error", "확인": "assert",
    "추가": "table.insert", "제거": "table.remove", "정렬": "table.sort", "다음": "next",
    "길이": "string.len", "부분문자열": "string.sub", "찾기": "string.find", "대체": "string.gsub", "형식": "string.format",
    "절댓값": "math.abs", "올림": "math.ceil", "버림": "math.floor", "최댓값": "math.max",
    "최솟값": "math.min", "거듭제곱": "math.pow", "무작위": "math.random", "제곱근": "math.sqrt",
    "코루틴_만들기": "coroutine.create", "코루틴_시작": "coroutine.resume", "코루틴_일시중지": "coroutine.yield", "코루틴_상태": "coroutine.status",
    "메타설정": "setmetatable", "메타가져오기": "getmetatable",
    "파일실행": "dofile", "파일읽기": "loadfile", "반복자_인덱스": "ipairs", "반복자_모두": "pairs",
    "참": "true", "거짓": "false",
    "또는": "or",
    "그리고": "and",
    "아니다": "not",
}

def preprocess_korean_lua(code: str) -> str:
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, keyword_map.keys())) + r')\b')
    return pattern.sub(lambda m: keyword_map[m.group(0)], code)

class KoreanSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyword_groups = {
            "conditional": {"keywords": ["만일", "이라면", "아니면", "그렇지않으면", "끝"], "format": QTextCharFormat()},
            "loop": {"keywords": ["반복", "동안", "반복하기", "끝", "까지"], "format": QTextCharFormat()},
            "function": {"keywords": ["함수", "지역", "돌려주기"], "format": QTextCharFormat()},
            "standard_func": {"keywords": ["출력", "숫자로", "문자열로", "자료형", "요구", "오류", "확인"], "format": QTextCharFormat()},
            "table": {"keywords": ["추가", "제거", "정렬", "다음"], "format": QTextCharFormat()},
            "string_func": {"keywords": ["길이", "부분문자열", "찾기", "대체", "형식"], "format": QTextCharFormat()},
            "math_func": {"keywords": ["절댓값", "올림", "버림", "최댓값", "최솟값", "거듭제곱", "무작위", "제곱근"], "format": QTextCharFormat()},
            "coroutine": {"keywords": ["코루틴_만들기", "코루틴_시작", "코루틴_일시중지", "코루틴_상태"], "format": QTextCharFormat()},
            "metatable": {"keywords": ["메타설정", "메타가져오기"], "format": QTextCharFormat()},
            "boolean": {"keywords": ["참", "거짓"], "format": QTextCharFormat()},
            "etc": {"keywords": ["파일실행", "파일읽기", "반복자_인덱스", "반복자_모두", "하기", "반복멈추기"], "format": QTextCharFormat()},
            "logic": {"keywords": ["또는", "그리고", "아니다"], "format": QTextCharFormat()},
        }

        color_map = {
            "conditional": "#569CD6", "loop": "#4EC9B0", "function": "#C586C0",
            "standard_func": "#D7BA7D", "table": "#9CDCFE", "string_func": "#CE9178",
            "math_func": "#B5CEA8", "coroutine": "#D16969", "metatable": "#61AFEF",
            "boolean": "#D16969",
            "etc": "#8FBCBB",
            "logic": "#dcdcaa",
        }

        for group, color in color_map.items():
            fmt = self.keyword_groups[group]["format"]
            fmt.setForeground(QColor(color))
            fmt.setFontWeight(QFont.Bold)
            pattern = r'\b(' + '|'.join(map(re.escape, self.keyword_groups[group]["keywords"])) + r')\b'
            self.keyword_groups[group]["compiled"] = re.compile(pattern)

    def highlightBlock(self, text):
        for group in self.keyword_groups.values():
            for match in group["compiled"].finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), group["format"])

class IndentTextEdit(QTextEdit):
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            cursor = self.textCursor()
            cursor.beginEditBlock()
            cursor.movePosition(cursor.StartOfLine, cursor.KeepAnchor)
            current_line_text = cursor.selectedText()
            indent = ""
            for ch in current_line_text:
                if ch in (" ", "\t"):
                    indent += ch
                else:
                    break
            super().keyPressEvent(event)
            self.insertPlainText(indent)
            cursor.endEditBlock()
        else:
            super().keyPressEvent(event)

dark_style = """
QWidget {
    background-color: #121212;
    color: #e0e0e0;
    font-family: '맑은 고딕', 'Malgun Gothic', sans-serif;
    font-size: 12pt;
}
QTextEdit, QPlainTextEdit {
    background-color: #1e1e1e;
    color: #e0e0e0;
    border: 1px solid #333333;
    padding: 6px;
    border-radius: 4px;
    selection-background-color: #3a5fcd;
    selection-color: #ffffff;
    scrollbar-width: thin;
    scrollbar-color: #3a5fcd #1e1e1e;
}
QScrollBar:vertical {
    background: #1e1e1e;
    width: 10px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: #3a5fcd;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QPushButton {
    background-color: #333333;
    color: #e0e0e0;
    border: 1px solid #444444;
    border-radius: 6px;
    padding: 8px 16px;
}
QPushButton:hover {
    background-color: #3a5fcd;
    border: 1px solid #3a5fcd;
}
QPushButton:pressed {
    background-color: #2a3f9d;
}
QTabWidget::pane {
    border: 1px solid #444444;
    background-color: #1e1e1e;
    border-radius: 6px;
}
QTabBar::tab {
    background: #2a2a2a;
    color: #ccc;
    padding: 8px 15px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background: #3a5fcd;
    color: #fff;
}
QTabBar::tab:hover {
    background: #4a70dd;
    color: #fff;
}
"""

class LuaRunnerThread(QThread):
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, lua_code, lua_exec="lua"):
        super().__init__()
        self.lua_code = lua_code
        self.lua_exec = lua_exec
        self._process = None
        self._running = True

    def run(self):
        with tempfile.NamedTemporaryFile("w", suffix=".lua", delete=False, encoding="utf-8") as tmp_file:
            tmp_file.write(self.lua_code)
            tmp_path = tmp_file.name

        try:
            self._process = subprocess.Popen(
                [self.lua_exec, tmp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                text=True,
                encoding="utf-8",
                errors='replace'
            )

            while self._running:
                out_line = self._process.stdout.readline()
                if out_line:
                    self.output_signal.emit(out_line)
                elif self._process.poll() is not None:
                    break

            # stderr도 읽음
            err = self._process.stderr.read()
            if err:
                self.error_signal.emit(err)

            self._process.wait()

        except Exception as e:
            self.error_signal.emit(str(e))

        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass

        self.finished_signal.emit()

    def stop(self):
        self._running = False
        if self._process:
            try:
                self._process.terminate()
            except Exception:
                pass

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("한글 Lua 변환기 + 실행기")
        self.resize(900, 700)

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # 입력 탭 (한글 Lua 코드)
        self.tab_input = QWidget()
        self.tab_input_layout = QVBoxLayout(self.tab_input)
        self.input_text = IndentTextEdit()
        self.tab_input_layout.addWidget(self.input_text)
        self.highlighter_input = KoreanSyntaxHighlighter(self.input_text.document())
        self.tabs.addTab(self.tab_input, "한글 Lua 코드")

        # 번역된 Lua 코드 탭
        self.tab_translated = QWidget()
        self.tab_translated_layout = QVBoxLayout(self.tab_translated)
        self.translated_code_text = QTextEdit()
        self.translated_code_text.setReadOnly(True)
        self.tab_translated_layout.addWidget(self.translated_code_text)
        self.tabs.addTab(self.tab_translated, "번역된 Lua 코드")

        # 결과 출력 탭
        self.tab_result = QWidget()
        self.tab_result_layout = QVBoxLayout(self.tab_result)
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.tab_result_layout.addWidget(self.result_text)
        self.tabs.addTab(self.tab_result, "실행 결과")

        # 버튼 레이아웃
        self.btn_layout = QHBoxLayout()
        self.btn_translate = QPushButton("번역")
        self.btn_run = QPushButton("실행")
        self.btn_stop = QPushButton("중지")
        self.btn_save = QPushButton("저장")
        self.btn_load = QPushButton("불러오기")
        self.btn_layout.addWidget(self.btn_translate)
        self.btn_layout.addWidget(self.btn_run)
        self.btn_layout.addWidget(self.btn_stop)
        self.btn_layout.addWidget(self.btn_save)
        self.btn_layout.addWidget(self.btn_load)
        self.layout.addLayout(self.btn_layout)

        # 버튼 이벤트
        self.btn_translate.clicked.connect(self.translate_code)
        self.btn_run.clicked.connect(self.run_code)
        self.btn_stop.clicked.connect(self.stop_code)
        self.btn_save.clicked.connect(self.save_code)
        self.btn_load.clicked.connect(self.load_code)

        self.lua_thread = None

        self.setStyleSheet(dark_style)

    def translate_code(self):
        korean_code = self.input_text.toPlainText()
        translated = preprocess_korean_lua(korean_code)
        self.translated_code_text.setPlainText(translated)
        self.tabs.setCurrentWidget(self.tab_translated)

    def run_code(self):
        if self.lua_thread and self.lua_thread.isRunning():
            QMessageBox.warning(self, "경고", "이미 실행 중인 코드가 있습니다. 먼저 중지하세요.")
            return

        lua_code = self.translated_code_text.toPlainText()
        if not lua_code.strip():
            QMessageBox.warning(self, "경고", "번역된 Lua 코드가 없습니다. 먼저 번역하세요.")
            return

        self.result_text.clear()
        self.lua_thread = LuaRunnerThread(lua_code)
        self.lua_thread.output_signal.connect(self.append_output)
        self.lua_thread.error_signal.connect(self.append_error)
        self.lua_thread.finished_signal.connect(self.run_finished)
        self.lua_thread.start()
        self.tabs.setCurrentWidget(self.tab_result)

    def stop_code(self):
        if self.lua_thread and self.lua_thread.isRunning():
            self.lua_thread.stop()
        else:
            QMessageBox.information(self, "정보", "실행 중인 코드가 없습니다.")

    def append_output(self, text):
        self.result_text.moveCursor(QTextCursor.End)
        self.result_text.insertPlainText(text)
        self.result_text.moveCursor(QTextCursor.End)

    def append_error(self, text):
        self.result_text.moveCursor(QTextCursor.End)
        self.result_text.insertHtml(f'<span style="color:red;">{text}</span>')
        self.result_text.moveCursor(QTextCursor.End)

    def run_finished(self):
        self.append_output("\n-- 실행 종료 --\n")

    def save_code(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "코드 저장", "", "Lua Files (*.lua);;All Files (*)", options=options)
        if fileName:
            try:
                with open(fileName, "w", encoding="utf-8") as f:
                    f.write(self.input_text.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, "오류", f"저장 실패: {e}")

    def load_code(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "코드 불러오기", "", "Lua Files (*.lua);;All Files (*)", options=options)
        if fileName:
            try:
                with open(fileName, "r", encoding="utf-8") as f:
                    code = f.read()
                self.input_text.setPlainText(code)
            except Exception as e:
                QMessageBox.critical(self, "오류", f"불러오기 실패: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
