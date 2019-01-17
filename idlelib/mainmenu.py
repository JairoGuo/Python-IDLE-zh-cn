"""Define the menu contents, hotkeys, and event bindings.

There is additional configuration information in the EditorWindow class (and
subclasses): the menus are created there based on the menu_specs (class)
variable, and menus not created are silently skipped in the code here.  This
makes it possible, for example, to define a Debug menu which is only present in
the PythonShell window, and a Format menu which is only present in the Editor
windows.

"""
from importlib.util import find_spec

from idlelib.config import idleConf

#   Warning: menudefs is altered in macosx.overrideRootMenu()
#   after it is determined that an OS X Aqua Tk is in use,
#   which cannot be done until after Tk() is first called.
#   Do not alter the 'file', 'options', or 'help' cascades here
#   without altering overrideRootMenu() as well.
#       TODO: Make this more robust

menudefs = [
 # underscore prefixes character to underscore
 ('file', [
   ('_新建文件', '<<open-new-window>>'),
   ('_打开文件...', '<<open-window-from-file>>'),
   ('打开模块...', '<<open-module>>'),
   ('模块浏览器', '<<open-class-browser>>'),
   ('_路径浏览器', '<<open-path-browser>>'),
   None,
   ('_保存', '<<save-window>>'),
   ('另存为...', '<<save-window-as-file>>'),
   ('将副本另存为...', '<<save-copy-of-window-as-file>>'),
   None,
   ('打印', '<<print-window>>'),
   None,
   ('_关闭', '<<close-window>>'),
   ('退出', '<<close-all-windows>>'),
  ]),
 ('edit', [
   ('_撤销', '<<undo>>'),
   ('_重做', '<<redo>>'),
   None,
   ('剪切', '<<cut>>'),
   ('_复制', '<<copy>>'),
   ('_粘贴', '<<paste>>'),
   ('全选', '<<select-all>>'),
   None,
   ('_查找...', '<<find>>'),
   ('再次查找', '<<find-again>>'),
   ('查找选择', '<<find-selection>>'),
   ('在文件中查找...', '<<find-in-files>>'),
   ('替换...', '<<replace>>'),
   ('跳转', '<<goto-line>>'),
   ('显示补全', '<<force-open-completions>>'),
   ('扩展单词', '<<expand-word>>'),
   ('参数提示', '<<force-open-calltip>>'),
   ('突出括号', '<<flash-paren>>'),

  ]),
('format', [
   ('_增加缩进', '<<indent-region>>'),
   ('_减少缩进', '<<dedent-region>>'),
   ('注释', '<<comment-region>>'),
   ('取消注释', '<<uncomment-region>>'),
   ('缩进区域', '<<tabify-region>>'),
   ('取消区域', '<<untabify-region>>'),
   ('切换标签', '<<toggle-tabs>>'),
   ('设置制表位', '<<change-indentwidth>>'),
   ('格式段落', '<<format-paragraph>>'),
   ('删除尾随空格', '<<do-rstrip>>'),
   ]),
 ('run', [
   ('Python Shell', '<<open-python-shell>>'),
   ('检查模块', '<<check-module>>'),
   ('运行模块', '<<run-module>>'),
   ]),
 ('shell', [
   ('_查看上次重启', '<<view-restart>>'),
   ('_重启 Shell', '<<restart-shell>>'),
   None,
   ('_中断执行', '<<interrupt-execution>>'),
   ]),
 ('debug', [
   ('_转到文件/行', '<<goto-file-line>>'),
   ('!_调试器', '<<toggle-debugger>>'),
   ('_栈查看器', '<<open-stack-viewer>>'),
   ('!_自动打开栈查看器', '<<toggle-jit-stack-viewer>>'),
   ]),
 ('options', [
   ('配置 _IDLE', '<<open-config-dialog>>'),
   ('_代码上下文', '<<toggle-code-context>>'),
   ]),
 ('windows', [
   ('变焦高度', '<<zoom-height>>'),
   ]),
 ('help', [
   ('_关于 IDLE', '<<about-idle>>'),
   None,
   ('_IDLE 帮助', '<<help>>'),
   ('Python _文档', '<<python-docs>>'),
   ]),
]

if find_spec('turtledemo'):
    menudefs[-1][1].append(('Turtle 演示', '<<open-turtle-demo>>'))

default_keydefs = idleConf.GetCurrentKeySet()
