from tkinter import *
from GetSuggestion import GetSuggestion
import fnmatch

class MainProcess:
    bg = "grey17"
    hbg = "gray60"
    hcol = "gray60"
    fg = "azure"
    objBg = "grey24"
    txtBg = "grey17"
    
    def __init__(self, master):
        # Base Window
        self.baseWindow = master
        master.title("Master Window")
        master.configure(background=self.bg)
        
        self.selectTextDataVar = StringVar()
        self.anotherTextDataVar = StringVar()
        self.getSuggestion = None
        
        # One Frame
        self.firstFrame = Frame(master)
        self.firstFrame.configure(background=self.bg, highlightbackground=self.hbg, highlightcolor=self.hcol,
                             highlightthickness=2, bd=0)
        self.firstFrame.pack(side=TOP, anchor='w', fill=X)
        # One Label
        self.textFieldLabel = Label(self.firstFrame, text="Type Something", width=12, borderwidth=2,
                                relief="flat", bg=self.bg,
                                fg=self.fg)
        self.textFieldLabel.pack(side=LEFT, padx=5, pady=15)
        #Sample Text Field
        self.sampleText = Entry(self.firstFrame, width=50, borderwidth=2, relief="groove", bg=self.objBg, textvariable=self.selectTextDataVar, fg=self.fg)
        self.sampleText.pack(side=LEFT, padx=5, pady=(15), anchor=W, fill=X, expand=YES)
        self.sampleText.bind("<FocusIn>", self.funInitGetSuggestion)
        # self.sampleText.bind("<Button-1>", self.funInitGetSuggestion)
        # self.sampleText.bind("<Key>", self.funGetSuggestion)
        self.sampleText2 = Entry(self.firstFrame, width=50, borderwidth=2, relief="groove", bg=self.objBg, textvariable=self.anotherTextDataVar, fg=self.fg)
        self.sampleText2.pack(side=LEFT, padx=5, pady=(15), anchor=W, fill=X, expand=YES)
        self.listItems = ["Aare", "Abacus", "Abbey", "Access", "Activity", "Adapter", "Addition", "Adam", "Adobe", "Aegis"]
    
    def funInitGetSuggestion(self, event):
        self.baseWindow.update()
        windowX = self.baseWindow.winfo_x()
        windowY = self.baseWindow.winfo_y()
        sampleTextX = self.sampleText.winfo_x()
        sampleTextY = self.sampleText.winfo_y()
        print("x,y" + str(sampleTextX) + "," + str(sampleTextY))
        if self.getSuggestion is None:
            self.getSuggestion = GetSuggestion(self.baseWindow, self.sampleText, windowX + sampleTextX + 9, windowY + sampleTextY + 52, 305, 130, self.populateSuggestionList, self.selectTextDataVar)
        else:
            self.getSuggestion.refreshWinPos(windowX + sampleTextX + 9, windowY + sampleTextY + 52, 305, 130)
    
    
    def populateSuggestionList(self, char, selected):
        print("populateListOptions..." + char)
        pattern = char + "*"
        matching = fnmatch.filter(self.listItems, pattern)
        print(matching)
        if selected == 0:
            suggestion = matching
            self.funInitGetSuggestion("UpdateWinPos")
            self.getSuggestion.setSuggestionList(suggestion)
        else :
            print("Got the Selected Value. Next operation can proceed => " + char)
            print("self.sampleText.get() = " + self.sampleText.get())


root = Tk()

m = MainProcess(root)

root.mainloop()