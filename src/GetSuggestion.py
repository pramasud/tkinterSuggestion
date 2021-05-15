from tkinter import *
import time
import threading


class GetSuggestion:
    bg = 'grey17'

    def __init__(self, master, widget, x, y, l, b, populateSuggestionList, selectTextDataVar):
        self.baseWindow = master
        self.suggestionList = ''
        self.selectTextDataVar = selectTextDataVar
        self.widget = widget
        self.listBox = None
        self.l = l
        self.b = b
        self.x = x
        self.y = y
        self.populateListOptions = populateSuggestionList
        self.checkEntryFocus = 0
        self.checkListFocus = 0
        self.listCurrPos = -1
        self.BaseWindowClose = 0
        self.getThreadLock = 0
        self.threadExecuting = 0
        self.dbConnectionOpen = 0
        self.updateListBox = 1
        self.threadHandlerLwClose = None
        self.threadHandlerDbConn = None
        self.dbConnection = None
        self.connectString = None
        self.con = None
        self.cur = None
        self.curText = ''
        self.prevText = ''
        self.keyCodeSkipList = [9, 16, 17, 18, 19, 20, 33, 34, 35, 36, 45, 91, 93, 112, 113, 114, 115, 116, 117, 118,
                                119, 120, 121, 122, 123, 144, 145]
        self.entryCursorPos = 0
        self.alreadyProcessing = 0
        self.selectionDone = 0
        self.sw = None
        self.swMainFrame = None
        self.baseWindow.bind('<Configure>', self.baseWindowConfigure)
        self.widget.bind('<Key>', self.button_key)
        self.widget.bind('<FocusOut>', self.focusOut)
        self.widget.bind('<FocusIn>', self.focusIn)

    def refreshWinPos(self, x, y, l, b):
        self.l = l
        self.b = b
        self.x = x
        self.y = y

    def setSuggestionList(self, suggestionListUpd):
        print('In setSuggestionList...')
        if not suggestionListUpd:
            if self.alreadyProcessing == 1:
                self.closeWindow()
        else:
            if self.alreadyProcessing == 0:
                self.alreadyProcessing = 1
                self.sw = Toplevel(self.baseWindow, bg=self.bg)
                self.sw.overrideredirect(True)
                self.sw.geometry('%dx%d+%d+%d' % (self.l, self.b, self.x, self.y))
                self.sw.protocol('WM_DELETE_WINDOW', self.closeWindow)
                self.sw.attributes('-topmost', 'true')
                self.swMainFrame = Frame(self.sw)
                self.swMainFrame.pack(anchor='w', fill=BOTH, expand=YES)
                self.listBox = Listbox(self.swMainFrame, selectmode=SINGLE)
                self.listBox.bind('<<ListboxSelect>>', self.on_selection)
                self.listBox.bind('<FocusIn>', self.listFocusIn)
                self.listBox.pack(anchor='w', side=LEFT, fill=BOTH, expand=YES)

            self.suggestionList = suggestionListUpd
            for data in self.suggestionList:
                print(data)
            if self.listBox is None:
                pass
            else:
                self.listBox.delete(0, END)
                for data in self.suggestionList:
                    self.listBox.insert(END, data)

    def button_key(self, event):
        print('In button_key...')
        print('button_key ===> ' + str(event.char) + ' ' + str(event.keycode) + ' ' + str(event.keysym))
        prevStr = self.selectTextDataVar.get()
        stringLen = len(prevStr)
        print('prevStr = ' + prevStr)
        prevCursorPos = self.widget.index(INSERT)
        self.updateListBox = 1
        # Right Arrow
        if event.keycode == 39:
            self.updateListBox = 0
            if prevCursorPos < stringLen:
                self.entryCursorPos = prevCursorPos + 1
            else:
                self.entryCursorPos = prevCursorPos
            print(str(stringLen) + ' ----- ' + str(prevCursorPos) + '-------' + str(self.entryCursorPos))
        # Left Arrow
        elif event.keycode == 37:
            self.updateListBox = 0
            if prevCursorPos > 0:
                self.entryCursorPos = prevCursorPos - 1
            else:
                self.entryCursorPos = prevCursorPos
            print(str(stringLen) + ' ----- ' + str(prevCursorPos) + '-------' + str(self.entryCursorPos))
        # Shift and Escape Key
        elif event.keycode in self.keyCodeSkipList:
            self.updateListBox = 0
        # Enter Key Pressed in Widget
        elif event.keycode == 13:
            if self.listCurrPos == -1:
                self.updateListBox = 0
                value = self.curText
                print('On Enter Key self.listCurrPos : ' + str(self.listCurrPos))
                print('On Enter Key : ' + self.curText)
                self.selectTextDataVar.set(value)
                self.populateListOptions(value, 1)
                self.widget.icursor(END)
                self.closeWindow()
        # BackSpace
        elif event.keycode == 8:
            print('Backspace ==> prevCursorPos, stringLen = ' + str(prevCursorPos) + ',' + str(stringLen))
            if stringLen == 0:
                self.updateListBox = 0
                self.closeWindow()
            else:
                # string length = Cursor Pos, Cursor at the End - Max for prevCursorPos
                if stringLen == prevCursorPos:
                    self.curText = prevStr[:-1:]
                    print('=========== ' + self.curText)
                    self.entryCursorPos = prevCursorPos - 1
                    if len(self.curText) == 0:
                        self.updateListBox = 0
                        self.closeWindow()
                # Cursor Pos > 1, but not equal to string length, Cursor at in middle
                elif prevCursorPos > 1:
                    self.curText = prevStr[0:prevCursorPos - 1:] + prevStr[prevCursorPos::]
                    print('=========== ' + self.curText)
                    self.entryCursorPos = prevCursorPos - 1
                elif prevCursorPos == 1:
                    self.curText = prevStr[1::]
                    print('=========== ' + self.curText)
                    self.entryCursorPos = prevCursorPos - 1
                else:
                    self.entryCursorPos = prevCursorPos
        # Delete
        elif event.keycode == 46:
            print('Delete ==> prevCursorPos, stringLen = ' + str(prevCursorPos) + ',' + str(stringLen))
            self.entryCursorPos = prevCursorPos
            if stringLen == 0:
                self.updateListBox = 0
                self.closeWindow()
            # string length = Cursor Pos, Cursor at the End, Nothing to Delete
            elif 0 <= prevCursorPos < stringLen:
                self.curText = prevStr[0:prevCursorPos:] + prevStr[prevCursorPos + 1::]
                print('=========== ' + self.curText)
                self.entryCursorPos = prevCursorPos - 1
        else:
            self.curText = prevStr + str(event.char)
            print('self.curText =========================> ' + self.curText)
            print(' ==================== ' + self.curText + ' ==================== ')

        if self.updateListBox == 1:
            if self.alreadyProcessing == 1:
                # Down Arrow
                if event.keycode == 40:
                    if self.listBox.size() > self.listCurrPos + 1:
                        self.listCurrPos = self.listCurrPos + 1
                    print(str(self.listCurrPos) + ' ' + str(self.listBox.size()))
                    self.listBox.selection_clear(0, END)
                    self.listBox.select_set(self.listCurrPos)
                # Escape Key
                elif event.keycode == 27:
                    self.closeWindow()
                # Up Arrow
                elif event.keycode == 38:
                    if self.listCurrPos > 0:
                        self.listCurrPos = self.listCurrPos - 1
                        self.listBox.selection_clear(0, END)
                        self.listBox.select_set(self.listCurrPos)
                    else:
                        if self.listCurrPos == 0:
                            self.listCurrPos = self.listCurrPos - 1
                            self.listBox.selection_clear(0, END)
                    print(str(self.listCurrPos) + ' ' + str(self.listBox.size()))
                # Enter Key in the List Options
                elif event.keycode == 13:
                    now = self.listBox.curselection()
                    print(now)
                    value = str(self.listBox.get(now))
                    print('On Enter Key self.listBox.get(now) : ' + str(self.listBox.get(now)))
                    print('On Enter Key : ' + self.curText)
                    self.curText = value
                    self.selectTextDataVar.set(value)
                    self.populateListOptions(value, 1)
                    self.widget.icursor(END)
                    self.closeWindow()
                else:
                    self.populateListOptions(self.curText, 0)
            else:
                if self.alreadyProcessing == 0:
                    self.populateListOptions(self.curText, 0)

    def focusIn(self, event):
        print('In focusIn...')
        print('Entry focusIn : ' + str(event))
        self.checkEntryFocus = 1

    def focusOut(self, event):
        print('In focusOut...')
        print('Entry focusOut : ' + str(event))
        self.checkEntryFocus = 0
        t1 = threading.Thread(target=self.suggestionWindowFocus)
        t1.start()
        # self.closeWindow()

    def listFocusIn(self, event):
        print('In List focusIn...')
        print('List focusIn : ' + str(event))
        print(self.selectionDone)
        self.checkListFocus = 1
        self.closeWindow()
        self.checkListFocus = 0

    def on_selection(self, event):
        print('In on_selection...')
        now = self.listBox.curselection()
        value = str(self.listBox.get(now))
        print('on_selection : ' + str(event) + str(self.listBox.get(now)))
        self.selectTextDataVar.set(value)
        self.populateListOptions(value, 1)
        self.widget.icursor(END)
        self.selectionDone = 1
        # self.closeWindow()

    def suggestionWindowFocus(self):
        print('In suggestionWindowFocus...')
        time.sleep(0.05)
        if self.checkEntryFocus == 0:
            if self.checkListFocus == 1:
                time.sleep(0.05)
            self.closeWindow()
        print('suggestionWindowFocus Exiting....')

    def baseWindowConfigure(self, event):
        print('In baseWindowConfigure...')
        self.closeWindow()

    def closeWindow(self):
        print('In closeWindow...')
        print('self.alreadyProcessing = ' + str(self.alreadyProcessing))
        if self.alreadyProcessing == 1:
            self.alreadyProcessing = 0
            self.listCurrPos = -1
            self.sw.destroy()
