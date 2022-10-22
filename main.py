#imports
from tkinter import ttk, filedialog
from tkinter import *
import multiprocessing, os, time, subprocess


#functions
def changeFolder():
    os.chdir(filedialog.askdirectory() + "/")


functionsOutput = ""
def createFolders(inputString, timeSleep):
    global functionsOutput
    inputList = inputString.split("\n")
    for i in inputList :
        try:
            os.mkdir(i)
            time.sleep(timeSleep)
            functionsOutput = "Done!\n"
        except Exception as error:
            if str(error).startswith("[WinError 183]") :
                functionsOutput = f"'{i}' already exist (skipping)\n"
            elif str(error).startswith("[WinError 123]") :
                functionsOutput = f"'{i}' has invalid name (skipping)\n"
            else :
                functionsOutput = str(error) + "\n"


def removeFolders(inputString, modeSelected, startsEndsWith) :
    global functionsOutput
    inputList = inputString.split("\n")
    if modeSelected == 0:
        for folder in inputList :
            try :
                os.rmdir(folder)
                functionsOutput = "Done!\n"
            except Exception as error:
                if str(error).startswith("[WinError 2]") :
                    functionsOutput = f"'{folder}' doesn't exist (skipping)\n"
                elif str(error).startswith("[WinError 3]") :
                    pass
                else :
                    functionsOutput = str(error) + "\n"
    elif modeSelected == 1 :
        for it in os.listdir(os.getcwd()+"\\") :
            if os.path.isdir(it) and it.startswith(startsEndsWith) :
                os.rmdir(it)
    elif modeSelected == 2 :
        for it in os.listdir(os.getcwd()+"\\") :
            if os.path.isdir(it) and it.endswith(startsEndsWith) :
                os.rmdir(it)


def modifyFolders(inputString, modeSelected, replaceWith, timeSleep) :
    global functionsOutput
    for it in os.listdir(os.getcwd()+"\\") :
        if os.path.isdir(it):
            try :
                time.sleep(timeSleep)
                if it.startswith(inputString) and modeSelected == 1 :
                    prefix = it[:len(inputString)]
                    suffix = it[len(inputString):]
                    os.rename(it, prefix.replace(inputString, replaceWith) + suffix)
                elif it.endswith(inputString) and modeSelected == 2 :
                    if inputString == "" :
                        os.rename(it, it + replaceWith)
                    elif replaceWith == "" :
                        os.rename(it, it[:-len(inputString)])
                    else :
                        prefix = it[:-len(inputString)]
                        suffix = it[-len(inputString)]
                        os.rename(it, prefix + suffix.replace(inputString, replaceWith))
                functionsOutput = "Done!\n"
            except Exception as error :
                functionsOutput = str(error) + "\n"


foldersList = ""
def getFolderList():
    global foldersList
    foldersList = ""
    for it in os.listdir(os.getcwd()+"\\") :
        if os.path.isdir(it):
            foldersList = foldersList + it +"\n"



#UI class
class WindowUI : 
    def __init__(self):
        #global
        self.root = Tk()
        self.root.geometry("600x600")
        self.root.title("Mass Directory Manager")

        tabControl = ttk.Notebook(self.root)
        anotherTabControl = ttk.Notebook(self.root)

        self.tab1 = Frame(tabControl)
        self.tab2 = Frame(tabControl)
        self.tab3 = Frame(tabControl)
        self.tab4 = Frame(anotherTabControl)

        tabControl.add(self.tab1, text = " Create folders ")
        tabControl.add(self.tab2, text = " Remove folders ")
        tabControl.add(self.tab3, text = " Modify folders ")
        tabControl.place(x=0, y=0)
        anotherTabControl.add(self.tab4, text = "Output")
        anotherTabControl.place(x=328, y=0)

        buttonQuit = Button(self.root, text = "Quit!", command = self.root.destroy)
        buttonQuit.pack(side = "bottom",  anchor = "se", pady = 20, padx = 20)

        self.root.bind("<Escape>", lambda y: self.root.destroy())
        self.root.bind("<F1>", lambda z: tabControl.select(self.tab1))
        self.root.bind("<F2>", lambda z: tabControl.select(self.tab2))
        self.root.bind("<F3>", lambda z: tabControl.select(self.tab3))

        #tab1 - create folders

        textBox1 = Text(self.tab1, height = 29, width = 40)
        textBox1.pack()

        buttonGo1 = Button(self.tab1, text = "Go!", command = lambda: [self.newCreateFolders(textBox1.get("1.0",'end-1c'), v1.get())])
        buttonGo1.pack(side = "bottom", pady = 10)

        v1 = DoubleVar()

        timeoutText = Label(self.tab1, text = "Time to pause between actions (in seconds)")
        timeoutText.pack()
        timeoutSlider = Scale(self.tab1, variable = v1, from_ = 0, to = 60, orient = HORIZONTAL)   
        timeoutSlider.pack(anchor = "center")

        #tab2 - remove folders

        testBox2 = Text(self.tab2, height = 27, width = 40)
        testBox2.pack()

        v4 = IntVar()

        noSelect = Radiobutton(self.tab2, text = "None", variable=v4, value=0)
        noSelect.pack()
        startsWith1 = Radiobutton(self.tab2, text = "Starts with", variable=v4, value=1)
        startsWith1.pack()
        endsWith1 = Radiobutton(self.tab2, text = "Ends with", variable=v4, value=2)
        endsWith1.pack()

        entryBox1 = Entry(self.tab2)
        entryBox1.pack()

        buttonGo2 = Button(self.tab2, text = "Go!", command = lambda: [self.newRemoveFolders(testBox2.get("1.0",'end-1c'), v4.get(), entryBox1.get())])
        buttonGo2.pack(side = "bottom", pady = 10)

        
        #tab3 - modify folders

        v2 = IntVar()

        startsWith = Radiobutton(self.tab3, text = "Starts with", variable=v2, value=1)
        startsWith.pack()
        endsWith = Radiobutton(self.tab3, text = "Ends with", variable=v2, value=2)
        endsWith.pack()

        entryBox2 = Entry(self.tab3)
        entryBox2.pack()

        replaceLabel = Label(self.tab3, text = "Replace with :")
        replaceLabel.pack()
        entryBox3 = Entry(self.tab3)
        entryBox3.pack()

        v3 = DoubleVar()

        timeoutText2 = Label(self.tab3, text = "Time to pause between actions (in seconds)")
        timeoutText2.pack()
        timeoutSlider = Scale(self.tab3, variable = v3, from_ = 0, to = 60, orient = HORIZONTAL)   
        timeoutSlider.pack(anchor = CENTER)

        buttonGo3 = Button(self.tab3, text = "Go!", command = lambda: [self.newModifyFolders(entryBox2.get(), v2.get(), entryBox3.get(), v3.get())])
        buttonGo3.pack(side = "bottom", pady = 10)

        #tab4 - output

        self.log = Text(self.tab4, state = 'normal', wrap = 'none', width = 33)
        self.log.pack()
        self.log.configure(state = "disabled")

        buttonFolderList = Button(self.tab4, text = "Get folders list", command = self.newFoldersList)
        buttonFolderList.pack(padx = 10, pady = 10)

        buttonSelectFolder = Button(self.tab4, text = "Change working folder", command = self.newChangeFolder)
        buttonSelectFolder.pack(padx = 10, pady = 10)

        buttonOpenFolder = Button(self.tab4, text = "Explore working folder", command = self.newOpenCurrentFolder)
        buttonOpenFolder.pack(padx = 10, pady = 10)




        self.root.mainloop()


    def newCreateFolders(self, entryGet = "", sleepValue = 0) :
        p = multiprocessing.Process(target = createFolders(entryGet, sleepValue))
        p.start()
        global functionsOutput
        self.log.configure(state = "normal")
        self.log.insert("1.0", f"---------------------------------\n{functionsOutput}")
        self.log.configure(state = "disabled")

    def newRemoveFolders(self, entryGet = "", modeSelected = 0, startsEndsWith = "") :
        p = multiprocessing.Process(target = removeFolders(entryGet, modeSelected, startsEndsWith))
        p.start()
        global functionsOutput
        self.log.configure(state = "normal")
        self.log.insert("1.0", f"---------------------------------\n{functionsOutput}")
        self.log.configure(state = "disabled")

    def newModifyFolders(self, entryGet = "",  modeSelected = 0, replaceWith = "", sleepValue = 0) :
        p = multiprocessing.Process(target = modifyFolders(entryGet, modeSelected, replaceWith, sleepValue))
        p.start()
        global functionsOutput
        self.log.configure(state = "normal")
        self.log.insert("1.0", f"---------------------------------\n{functionsOutput}")
        self.log.configure(state = "disabled")

    def newFoldersList(self) :
        p = multiprocessing.Process(target = getFolderList())
        p.start()
        global foldersList
        self.log.configure(state = "normal")
        self.log.insert("1.0", f"---------------------------------\nCurrently working on :\n{os.getcwd()}.\nFolders list :\n{foldersList}")
        self.log.configure(state = "disabled")

    def newChangeFolder(self) :
        p = multiprocessing.Process(target = changeFolder())
        p.start()

    def newOpenCurrentFolder(self) : 
        subprocess.Popen(f'explorer "{os.getcwd()}"')

if __name__ == '__main__' :
    startUI = WindowUI()