import sys
import zipfile
import os
import tkinter
import tkinter.messagebox


# DIR = getattr(sys, '_MEIPASS', '')
DIR = sys._MEIPASS
os.system('python '+ DIR + '\\res\\' + 'get_py_dir.py')
with open(DIR + '\\res\\' +'py_path.ini','r') as f:
	PY_DIR = f.read()
 
# PY_DIR = sys.executable
PY_DIR = '\\'.join(PY_DIR.split('\\')[:-1])+'\\Lib'
SEC_DIR = DIR + '\\res\\'

def hh():
	z = zipfile.ZipFile(SEC_DIR + 'idlelib.zip', 'r')
	z.extractall(path=PY_DIR)
	z.close()

def hy():
	z = zipfile.ZipFile(PY_DIR+'\\idlelib.zip', 'r')
	z.extractall(path=PY_DIR+'\\idlelib')
	z.close()

def bf():
	ls = os.walk(PY_DIR+'\\idlelib')
	z = zipfile.ZipFile(PY_DIR + '\\idlelib.zip', 'w', zipfile.ZIP_DEFLATED)
	for i in ls:
		for n in i[2]:
			z.write(''.join((i[0],'\\',n)),''.join((i[0].split('\\idlelib')[-1][1:],'\\',n)))
	z.close()

def init():
	dir_ls = os.listdir(PY_DIR)
	if 'py_zh.ini' in dir_ls:
		with open(PY_DIR+'\\py_zh.ini','r') as f:
			flag = f.read()
			if '0' in flag :
				text = '汉化'
			else:
				text = '还原'
	else:
		with open(PY_DIR+'\\py_zh.ini','w') as f:
			f.write("0")
		text = '汉化'
		bf()

	return text

def but():
	with open(PY_DIR+'\\py_zh.ini','r') as f:
		flag = f.read()
	with open(PY_DIR+'\\py_zh.ini','w') as f:
		if '0' in flag:
			hh()
			tkinter.messagebox.showinfo('提示',bt['text']+'成功')
			bt['text'] = '还原'
			f.write('1')
		else:
			hy()
			tkinter.messagebox.showinfo('提示',bt['text']+'成功')
			bt['text'] = '汉化'
			f.write('0')	


text = init()
mainp = tkinter.Tk()
mainp.title('Python汉化助手')
mainp.iconbitmap(SEC_DIR+ "ico.ico")
ws = mainp.winfo_screenwidth()
hs = mainp.winfo_screenheight()
w = ws//4
h = hs//4
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
mainp.geometry('%dx%d+%d+%d' % (w, h, x, y))
mainp.resizable(width=False, height=False)
mainp.update()
bt = tkinter.Button(mainp, text=text, width=w//15, height=h//55,command=but)
bt.place(relx=0.5, rely=0.2, anchor='center')
lab_text = '\
说明:\n\
(1)本软件为简化汉化IDLE操作\n\
(2)请确保Python IDLE为英文版本\n\
(2)程序会为您备份文件以便恢复\n\
作者：Jairo\n\
邮箱：jairoguo@126.com\n'
tkinter.Label(mainp, text=lab_text, justify='left').place(relx=0.5, rely=0.7, anchor='center')
mainp.mainloop()
