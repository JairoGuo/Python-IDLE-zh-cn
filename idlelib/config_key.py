"""
Dialog for building Tkinter accelerator key bindings
"""
from tkinter import *
from tkinter.ttk import Scrollbar
from tkinter import messagebox
import string
import sys


class GetKeysDialog(Toplevel):

    # Dialog title for invalid key sequence
    keyerror_title = 'Key Sequence Error'

    def __init__(self, parent, title, action, currentKeySequences,
                 *, _htest=False, _utest=False):
        """
        action - string, the name of the virtual event these keys will be
                 mapped to
        currentKeys - list, a list of all key sequence lists currently mapped
                 to virtual events, for overlap checking
        _utest - bool, do not wait when running unittest
        _htest - bool, change box location when running htest
        """
        Toplevel.__init__(self, parent)
        self.withdraw() #hide while setting geometry
        self.configure(borderwidth=5)
        self.resizable(height=FALSE, width=FALSE)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.Cancel)
        self.parent = parent
        self.action=action
        self.currentKeySequences = currentKeySequences
        self.result = ''
        self.keyString = StringVar(self)
        self.keyString.set('')
        self.SetModifiersForPlatform() # set self.modifiers, self.modifier_label
        self.modifier_vars = []
        for modifier in self.modifiers:
            variable = StringVar(self)
            variable.set('')
            self.modifier_vars.append(variable)
        self.advanced = False
        self.CreateWidgets()
        self.LoadFinalKeyList()
        self.update_idletasks()
        self.geometry(
                "+%d+%d" % (
                    parent.winfo_rootx() +
                    (parent.winfo_width()/2 - self.winfo_reqwidth()/2),
                    parent.winfo_rooty() +
                    ((parent.winfo_height()/2 - self.winfo_reqheight()/2)
                    if not _htest else 150)
                ) )  #centre dialog over parent (or below htest box)
        if not _utest:
            self.deiconify() #geometry set, unhide
            self.wait_window()

    def showerror(self, *args, **kwargs):
        # Make testing easier.  Replace in #30751.
        messagebox.showerror(*args, **kwargs)

    def CreateWidgets(self):
        frameMain = Frame(self,borderwidth=2,relief=SUNKEN)
        frameMain.pack(side=TOP,expand=TRUE,fill=BOTH)
        frameButtons=Frame(self)
        frameButtons.pack(side=BOTTOM,fill=X)
        self.buttonOK = Button(frameButtons,text='OK',
                width=8,command=self.OK)
        self.buttonOK.grid(row=0,column=0,padx=5,pady=5)
        self.buttonCancel = Button(frameButtons,text='取消',
                width=8,command=self.Cancel)
        self.buttonCancel.grid(row=0,column=1,padx=5,pady=5)
        self.frameKeySeqBasic = Frame(frameMain)
        self.frameKeySeqAdvanced = Frame(frameMain)
        self.frameControlsBasic = Frame(frameMain)
        self.frameHelpAdvanced = Frame(frameMain)
        self.frameKeySeqAdvanced.grid(row=0,column=0,sticky=NSEW,padx=5,pady=5)
        self.frameKeySeqBasic.grid(row=0,column=0,sticky=NSEW,padx=5,pady=5)
        self.frameKeySeqBasic.lift()
        self.frameHelpAdvanced.grid(row=1,column=0,sticky=NSEW,padx=5)
        self.frameControlsBasic.grid(row=1,column=0,sticky=NSEW,padx=5)
        self.frameControlsBasic.lift()
        self.buttonLevel = Button(frameMain,command=self.ToggleLevel,
                text='高级键位绑定 >>')
        self.buttonLevel.grid(row=2,column=0,stick=EW,padx=5,pady=5)
        labelTitleBasic = Label(self.frameKeySeqBasic,
                text="新按键  '"+self.action+"' :")
        labelTitleBasic.pack(anchor=W)
        labelKeysBasic = Label(self.frameKeySeqBasic,justify=LEFT,
                textvariable=self.keyString,relief=GROOVE,borderwidth=2)
        labelKeysBasic.pack(ipadx=5,ipady=5,fill=X)
        self.modifier_checkbuttons = {}
        column = 0
        for modifier, variable in zip(self.modifiers, self.modifier_vars):
            label = self.modifier_label.get(modifier, modifier)
            check=Checkbutton(self.frameControlsBasic,
                command=self.BuildKeyString,
                text=label,variable=variable,onvalue=modifier,offvalue='')
            check.grid(row=0,column=column,padx=2,sticky=W)
            self.modifier_checkbuttons[modifier] = check
            column += 1
        labelFnAdvice=Label(self.frameControlsBasic,justify=LEFT,
                            text=\
                            "选择上面所需的需改键位\n"+
                            "并从右侧列表选择一个键位\n\n"+
                            "使用上面选择符号,使用 Shift 修饰\n" +
                            "(字母自动转化)")
        labelFnAdvice.grid(row=1,column=0,columnspan=4,padx=2,sticky=W)
        self.listKeysFinal=Listbox(self.frameControlsBasic,width=15,height=10,
                selectmode=SINGLE)
        self.listKeysFinal.bind('<ButtonRelease-1>',self.FinalKeySelected)
        self.listKeysFinal.grid(row=0,column=4,rowspan=4,sticky=NS)
        scrollKeysFinal=Scrollbar(self.frameControlsBasic,orient=VERTICAL,
                command=self.listKeysFinal.yview)
        self.listKeysFinal.config(yscrollcommand=scrollKeysFinal.set)
        scrollKeysFinal.grid(row=0,column=5,rowspan=4,sticky=NS)
        self.buttonClear=Button(self.frameControlsBasic,
                text='清除键位',command=self.ClearKeySeq)
        self.buttonClear.grid(row=2,column=0,columnspan=4)
        labelTitleAdvanced = Label(self.frameKeySeqAdvanced,justify=LEFT,
                text="输入新的绑定为  '"+self.action+"' :\n"+
                "(不检查有效性!)")
        labelTitleAdvanced.pack(anchor=W)
        self.entryKeysAdvanced=Entry(self.frameKeySeqAdvanced,
                textvariable=self.keyString)
        self.entryKeysAdvanced.pack(fill=X)
        labelHelpAdvanced=Label(self.frameHelpAdvanced,justify=LEFT,
            text="键位绑定使用 Tkinter keysyms\n"+
                 "如以下示例中所示: <Control-f>, <Shift-F2>, <F12>,\n"
                 "<Control-space>, <Meta-less>, <Control-Alt-Shift-X>.\n"
                 "大写字母使用 Shift 修饰!\n\n" +
                 "'Emacs 风格' 多个键位绑定指定如下:\n" +
                 " <Control-x><Control-y>\n" +
                 "其中第一个键是不执行任何操作的键绑定.\n\n" +
                 "个操作的多个单独绑定应该是用空格分隔\n"+
                 "例如, <Alt-v> <Meta-v>." )
        labelHelpAdvanced.grid(row=0,column=0,sticky=NSEW)

    def SetModifiersForPlatform(self):
        """Determine list of names of key modifiers for this platform.

        The names are used to build Tk bindings -- it doesn't matter if the
        keyboard has these keys, it matters if Tk understands them. The
        order is also important: key binding equality depends on it, so
        config-keys.def must use the same ordering.
        """
        if sys.platform == "darwin":
            self.modifiers = ['Shift', 'Control', 'Option', 'Command']
        else:
            self.modifiers = ['Control', 'Alt', 'Shift']
        self.modifier_label = {'Control': 'Ctrl'} # short name

    def ToggleLevel(self):
        if  self.buttonLevel.cget('text')[:4]=='高级键位':
            self.ClearKeySeq()
            self.buttonLevel.config(text='<< 基本键位绑定')
            self.frameKeySeqAdvanced.lift()
            self.frameHelpAdvanced.lift()
            self.entryKeysAdvanced.focus_set()
            self.advanced = True
        else:
            self.ClearKeySeq()
            self.buttonLevel.config(text='高级键位绑定 >>')
            self.frameKeySeqBasic.lift()
            self.frameControlsBasic.lift()
            self.advanced = False

    def FinalKeySelected(self,event):
        self.BuildKeyString()

    def BuildKeyString(self):
        keyList = modifiers = self.GetModifiers()
        finalKey = self.listKeysFinal.get(ANCHOR)
        if finalKey:
            finalKey = self.TranslateKey(finalKey, modifiers)
            keyList.append(finalKey)
        self.keyString.set('<' + '-'.join(keyList) + '>')

    def GetModifiers(self):
        modList = [variable.get() for variable in self.modifier_vars]
        return [mod for mod in modList if mod]

    def ClearKeySeq(self):
        self.listKeysFinal.select_clear(0,END)
        self.listKeysFinal.yview(MOVETO, '0.0')
        for variable in self.modifier_vars:
            variable.set('')
        self.keyString.set('')

    def LoadFinalKeyList(self):
        #these tuples are also available for use in validity checks
        self.functionKeys=('F1','F2','F3','F4','F5','F6','F7','F8','F9',
                'F10','F11','F12')
        self.alphanumKeys=tuple(string.ascii_lowercase+string.digits)
        self.punctuationKeys=tuple('~!@#%^&*()_-+={}[]|;:,.<>/?')
        self.whitespaceKeys=('Tab','Space','Return')
        self.editKeys=('BackSpace','Delete','Insert')
        self.moveKeys=('Home','End','Page Up','Page Down','Left Arrow',
                'Right Arrow','Up Arrow','Down Arrow')
        #make a tuple of most of the useful common 'final' keys
        keys=(self.alphanumKeys+self.punctuationKeys+self.functionKeys+
                self.whitespaceKeys+self.editKeys+self.moveKeys)
        self.listKeysFinal.insert(END, *keys)

    def TranslateKey(self, key, modifiers):
        "Translate from keycap symbol to the Tkinter keysym"
        translateDict = {'Space':'space',
                '~':'asciitilde','!':'exclam','@':'at','#':'numbersign',
                '%':'percent','^':'asciicircum','&':'ampersand','*':'asterisk',
                '(':'parenleft',')':'parenright','_':'underscore','-':'minus',
                '+':'plus','=':'equal','{':'braceleft','}':'braceright',
                '[':'bracketleft',']':'bracketright','|':'bar',';':'semicolon',
                ':':'colon',',':'comma','.':'period','<':'less','>':'greater',
                '/':'slash','?':'question','Page Up':'Prior','Page Down':'Next',
                'Left Arrow':'Left','Right Arrow':'Right','Up Arrow':'Up',
                'Down Arrow': 'Down', 'Tab':'Tab'}
        if key in translateDict:
            key = translateDict[key]
        if 'Shift' in modifiers and key in string.ascii_lowercase:
            key = key.upper()
        key = 'Key-' + key
        return key

    def OK(self, event=None):
        keys = self.keyString.get().strip()
        if not keys:
            self.showerror(title=self.keyerror_title, parent=self,
                           message="No key specified.")
            return
        if (self.advanced or self.KeysOK(keys)) and self.bind_ok(keys):
            self.result = keys
        self.destroy()

    def Cancel(self, event=None):
        self.result=''
        self.destroy()

    def KeysOK(self, keys):
        '''Validity check on user's 'basic' keybinding selection.

        Doesn't check the string produced by the advanced dialog because
        'modifiers' isn't set.

        '''
        finalKey = self.listKeysFinal.get(ANCHOR)
        modifiers = self.GetModifiers()
        keysOK = False
        title = self.keyerror_title
        key_sequences = [key for keylist in self.currentKeySequences
                             for key in keylist]
        if not keys.endswith('>'):
            self.showerror(title, parent=self,
                           message='Missing the final Key')
        elif (not modifiers
              and finalKey not in self.functionKeys + self.moveKeys):
            self.showerror(title=title, parent=self,
                           message='No modifier key(s) specified.')
        elif (modifiers == ['Shift']) \
                 and (finalKey not in
                      self.functionKeys + self.moveKeys + ('Tab', 'Space')):
            msg = 'The shift modifier by itself may not be used with'\
                  ' this key symbol.'
            self.showerror(title=title, parent=self, message=msg)
        elif keys in key_sequences:
            msg = 'This key combination is already in use.'
            self.showerror(title=title, parent=self, message=msg)
        else:
            keysOK = True
        return keysOK

    def bind_ok(self, keys):
        "Return True if Tcl accepts the new keys else show message."

        try:
            binding = self.bind(keys, lambda: None)
        except TclError as err:
            self.showerror(
                    title=self.keyerror_title, parent=self,
                    message=(f'The entered key sequence is not accepted.\n\n'
                             f'Error: {err}'))
            return False
        else:
            self.unbind(keys, binding)
            return True


if __name__ == '__main__':
    import unittest
    unittest.main('idlelib.idle_test.test_config_key', verbosity=2, exit=False)

    from idlelib.idle_test.htest import run
    run(GetKeysDialog)
