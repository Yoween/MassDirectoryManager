#imports
from tkinter import ttk, filedialog
import tkinter as tk
import multiprocessing, os, time, subprocess

class Execution():
    def changeFolder(self):
        """Simply changes the current working directory
        """
        os.chdir(filedialog.askdirectory() + "/")


    def createFolders(self, inputString: str, timeSleep: int, numIterations=0, startPos=0):
        """Create folders named after the names specified

        Args:
            inputString (str): Folders names
            timeSleep (int): Pause time between folder creation
            numIterations (int): Number of iterations; 0 means it's disabled and >0 create the amount of folders and increments the value of '{inc}' from <startPos> to it. Defaults to 0.
            startPos (int, optional): pos to start from if iteration mode selcted. Defaults to 0.
        """
        self.functionsOutput = ""
        inputList = inputString.split("\n")
        if numIterations == 0:
            for item in inputList:
                try:
                    os.mkdir(item)
                    time.sleep(timeSleep)
                    self.functionsOutput = "Done!\n"
                except Exception as error:
                    if str(error).startswith("[WinError 183]"):
                        self.functionsOutput = f"'{item}' already exist (skipping)\n"
                    elif str(error).startswith("[WinError 123]"):
                        self.functionsOutput = f"'{item}' has invalid name (skipping)\n"
                    else:
                        self.functionsOutput = str(error) + "\n"
        else:
            for iteration in range(numIterations):
                for item in inputList:
                    try:
                        for j in range(len(item)):
                            marker = item[j:j+5]
                            if marker == "{inc}":
                                os.mkdir(f"{item[0:j]}{iteration+startPos}{item[j+5:len(item)]}")
                                time.sleep(timeSleep)
                                self.functionsOutput = "Done!\n"
                    except Exception as error:
                        if str(error).startswith("[WinError 183]"):
                            self.functionsOutput = f"'{item}' already exist (skipping)\n"
                        elif str(error).startswith("[WinError 123]"):
                            self.functionsOutput = f"'{item}' has invalid name (skipping)\n"
                        else:
                            self.functionsOutput = str(error) + "\n"


    def removeFolders(self, inputString:int, modeSelected:int, startsEndsWith:str, numIterations=0, startPos=0):
        """Remove folders named after the specified names
        
        Args:
            inputString (int): Folders names
            modeSelected (int): 1 is 'starts with', 2 is 'ends with' and 0 is normal/iteration
            startsEndsWith (str): Charactes passed as params is modeSelected is 1 or 2
            numIterations (int, optional): 0 is no iteration and >0 loops replacing '{inc}' by the loop index. Defaults to 0.
            startPos (int, optional): pos to start from if iteration mode selcted. Defaults to 0.
        """
        self.functionsOutput = ""
        inputList = inputString.split("\n")
        if modeSelected == 0:
            self.functionsOutput = ""
            inputList = inputString.split("\n")
            if numIterations == 0:
                for folder in inputList:
                    try:
                        os.rmdir(folder)
                        self.functionsOutput = "Done!\n"
                    except Exception as error:
                        if str(error).startswith("[WinError 2]"):
                            self.functionsOutput = f"'{folder}' doesn't exist (skipping)\n"
                        elif str(error).startswith("[WinError 3]"):
                            pass
                        else:
                            self.functionsOutput = str(error) + "\n"
            else:
                for iteration in range(numIterations):
                    for folder in inputList:
                        try:
                            for j in range(len(folder)):
                                marker = folder[j:j+5]
                                if marker == "{inc}":
                                    os.rmdir(f"{folder[0:j]}{iteration+startPos}{folder[j+5:len(folder)]}")
                                    self.functionsOutput = "Done!\n"
                        except Exception as error:
                            if str(error).startswith("[WinError 2]"):
                                self.functionsOutput = f"'{folder}' doesn't exist (skipping)\n"
                            elif str(error).startswith("[WinError 3]"):
                                pass
                            else:
                                self.functionsOutput = str(error) + "\n"
                        
        elif modeSelected == 1:
            if startsEndsWith == "":
                return
            for it in os.listdir(os.getcwd()):
                if os.path.isdir(it) and it.startswith(startsEndsWith):
                    print(it)
                    os.rmdir(it)
                    self.functionsOutput = "Done!\n"
        elif modeSelected == 2:
            if startsEndsWith == "":
                return
            for it in os.listdir(os.getcwd()):
                if os.path.isdir(it) and it.endswith(startsEndsWith):
                    os.rmdir(it)
                    self.functionsOutput = "Done!\n"


    def modifyFolders(self, inputString:str, modeSelected:int, replaceWith:str, timeSleep:int):
        for it in os.listdir(os.getcwd()):
            if os.path.isdir(it):
                try:
                    time.sleep(timeSleep)
                    if it.startswith(inputString) and modeSelected == 1:
                        prefix = it[:len(inputString)]
                        suffix = it[len(inputString):]
                        os.rename(it, prefix.replace(inputString, replaceWith) + suffix)
                    elif it.endswith(inputString) and modeSelected == 2:
                        if inputString == "":
                            os.rename(it, it + replaceWith)
                        elif replaceWith == "":
                            os.rename(it, it[:-len(inputString)])
                        else:
                            prefix = it[:-len(inputString)]
                            suffix = it[-len(inputString)]
                            os.rename(it, prefix + suffix.replace(inputString, replaceWith))
                    self.functionsOutput = "Done!\n"
                except Exception as error:
                    self.functionsOutput = str(error) + "\n"


    def getFolderList(self):
        self.foldersList = ""
        for it in os.listdir(os.getcwd()+"/"):
            if os.path.isdir(it):
                self.foldersList = self.foldersList + it +"\n"



#UI class
class WindowUI: 
    def __init__(self):
        self.execution = Execution()

        #global
        self.root = tk.Tk()
        self.root.geometry("600x600")
        self.root.title("Mass Directory Manager")

        tabControl = ttk.Notebook(self.root)
        anotherTabControl = ttk.Notebook(self.root)

        self.tab1 = tk.Frame(tabControl)
        self.tab2 = tk.Frame(tabControl)
        self.tab3 = tk.Frame(tabControl)
        self.tab4 = tk.Frame(anotherTabControl)

        tabControl.add(self.tab1, text = " Create folders ")
        tabControl.add(self.tab2, text = " Remove folders ")
        tabControl.add(self.tab3, text = " Modify folders ")
        tabControl.place(x=0, y=0)
        anotherTabControl.add(self.tab4, text = "Output")
        anotherTabControl.place(x=328, y=0)

        buttonQuit = tk.Button(self.root, text = "Quit!", command = self.root.destroy)
        buttonQuit.pack(side = "bottom",  anchor = "se", pady = 20, padx = 20)

        self.root.bind("<Escape>", lambda y: self.root.destroy())
        self.root.bind("<F1>", lambda z: tabControl.select(self.tab1))
        self.root.bind("<F2>", lambda z: tabControl.select(self.tab2))
        self.root.bind("<F3>", lambda z: tabControl.select(self.tab3))

        #tab1 - create folders

        textBox1 = tk.Text(self.tab1, height = 27, width = 40)
        textBox1.pack()

        buttonGo1 = tk.Button(self.tab1, text = "Go!", command = lambda: [self.newCreateFolders(textBox1.get("1.0",'end-1c'), v1.get())])
        buttonGo1.pack(side = "bottom", pady = 10)

        v1 = tk.DoubleVar()

        timeoutText = tk.Label(self.tab1, text = "Time to pause between actions (in seconds)")
        timeoutText.pack()
        timeoutSlider = tk.Scale(self.tab1, variable = v1, from_ = 0, to = 60, orient = tk.HORIZONTAL)   
        timeoutSlider.pack(anchor = "center")
        
        self.incrementVariable = tk.IntVar()
        
        incrementButton1 = tk.Checkbutton(self.tab1, text = "Increment mode", variable = self.incrementVariable, onvalue = 1, offvalue = 0, command = lambda: [self.incrementSelector(self.tab1)])
        incrementButton1.pack(side = "left", anchor = "sw")

        #tab2 - remove folders

        testBox2 = tk.Text(self.tab2, height = 27, width = 40)
        testBox2.pack()

        v4 = tk.IntVar()

        startsWith1 = tk.Checkbutton(self.tab2, text = "Starts with", variable=v4, onvalue=1, offvalue=0)
        startsWith1.pack()
        endsWith1 = tk.Checkbutton(self.tab2, text = "Ends with", variable=v4, onvalue=2, offvalue=0)
        endsWith1.pack()

        entryBox1 = tk.Entry(self.tab2)
        entryBox1.pack()

        buttonGo2 = tk.Button(self.tab2, text = "Go!", command = lambda: [self.newRemoveFolders(testBox2.get("1.0",'end-1c'), v4.get(), entryBox1.get())])
        buttonGo2.pack(side = "bottom", pady = 10)
        
        incrementButton2 = tk.Checkbutton(self.tab2, text = "Increment mode", variable = self.incrementVariable, onvalue = 1, offvalue = 0, command = lambda: [self.incrementSelector(self.tab2)])
        incrementButton2.pack(side = "left", anchor = "sw")

        
        #tab3 - modify folders

        v2 = tk.IntVar()

        startsWith = tk.Radiobutton(self.tab3, text = "Starts with", variable=v2, value=1)
        startsWith.pack()
        endsWith = tk.Radiobutton(self.tab3, text = "Ends with", variable=v2, value=2)
        endsWith.pack()

        entryBox2 = tk.Entry(self.tab3)
        entryBox2.pack()

        replaceLabel = tk.Label(self.tab3, text = "Replace with:")
        replaceLabel.pack()
        entryBox3 = tk.Entry(self.tab3)
        entryBox3.pack()

        v3 = tk.DoubleVar()

        timeoutText2 = tk.Label(self.tab3, text = "Time to pause between actions (in seconds)")
        timeoutText2.pack()
        timeoutSlider = tk.Scale(self.tab3, variable = v3, from_ = 0, to = 60, orient = tk.HORIZONTAL)   
        timeoutSlider.pack(anchor = tk.CENTER)

        buttonGo3 = tk.Button(self.tab3, text = "Go!", command = lambda: [self.newModifyFolders(entryBox2.get(), v2.get(), entryBox3.get(), v3.get())])
        buttonGo3.pack(side = "bottom", pady = 10)

        #tab4 - output

        self.log = tk.Text(self.tab4, state = 'normal', wrap = 'none', width = 33)
        self.log.pack()
        self.log.configure(state = "disabled")

        buttonFolderList = tk.Button(self.tab4, text = "Get folders list", command = self.newFoldersList)
        buttonFolderList.pack(padx = 10, pady = 10)

        buttonSelectFolder = tk.Button(self.tab4, text = "Change working folder", command = self.newChangeFolder)
        buttonSelectFolder.pack(padx = 10, pady = 10)

        buttonOpenFolder = tk.Button(self.tab4, text = "Explore working folder", command = self.newOpenCurrentFolder)
        buttonOpenFolder.pack(padx = 10, pady = 10)


        self.root.mainloop()


    def incrementSelector(self, selectedTab):
        variable = self.incrementVariable.get()
        if variable == 1:
            self.label2 = tk.Label(selectedTab, text= "Pos to start")
            self.label2.pack(side="right", padx = 2)
            self.incrementStart = tk.Text(selectedTab, height = 1, width = 2)
            self.incrementStart.pack(side = "right", padx = 2)

            self.label1 = tk.Label(selectedTab, text= "Num to loop")
            self.label1.pack(side="right", padx = 2)
            self.incrementValue = tk.Text(selectedTab, height = 1, width = 3)
            self.incrementValue.pack(side = "right", padx = 2)
        elif variable == 0:
            try:
                self.label1.destroy()
                self.incrementValue.destroy()
                self.label2.destroy()
                self.incrementStart.destroy()
            except:
                pass


    def newCreateFolders(self, entryGet = "", sleepValue = 0):
        try:
            incrementValue = self.incrementValue.get(1.0, "end-1c")
            incrementStart = self.incrementStart.get(1.0, "end-1c")
        except:
            incrementValue = 0
            incrementStart = 0
        if incrementStart == "":
            incrementStart = 1
        if incrementValue == "":
            incrementValue = 0
        if str(incrementValue).isdigit():
            incrementValue = int(incrementValue)
        if str(incrementStart).isdigit():
            incrementStart = int(incrementStart)

        p = multiprocessing.Process(target = self.execution.createFolders(entryGet, sleepValue, incrementValue, incrementStart))
        p.start()
        self.log.configure(state = "normal")
        self.log.insert("1.0", f"---------------------------------\n{self.execution.functionsOutput}")
        self.log.configure(state = "disabled")

    def newRemoveFolders(self, entryGet = "", modeSelected = 0, startsEndsWith = ""):
        try:
            incrementValue = self.incrementValue.get(1.0, "end-1c")
            incrementStart = self.incrementStart.get(1.0, "end-1c")
        except:
            incrementValue = 0
            incrementStart = 0
        if incrementStart == "":
            incrementStart = 1
        if incrementValue == "":
            incrementValue = 0
        if str(incrementValue).isdigit():
            incrementValue = int(incrementValue)
        if str(incrementStart).isdigit():
            incrementStart = int(incrementStart)

        p = multiprocessing.Process(target = self.execution.removeFolders(entryGet, modeSelected, startsEndsWith, incrementValue, incrementStart))
        p.start()
        self.log.configure(state = "normal")
        self.log.insert("1.0", f"---------------------------------\n{self.execution.functionsOutput}")
        self.log.configure(state = "disabled")

    def newModifyFolders(self, entryGet = "",  modeSelected = 0, replaceWith = "", sleepValue = 0):
        p = multiprocessing.Process(target = self.execution.modifyFolders(entryGet, modeSelected, replaceWith, sleepValue))
        p.start()
        self.log.configure(state = "normal")
        self.log.insert("1.0", f"---------------------------------\n{self.execution.functionsOutput}")
        self.log.configure(state = "disabled")

    def newFoldersList(self):
        p = multiprocessing.Process(target = self.execution.getFolderList())
        p.start()
        self.log.configure(state = "normal")
        self.log.insert("1.0", f"---------------------------------\nCurrently working on:\n{os.getcwd()}.\nFolders list:\n{self.execution.foldersList}")
        self.log.configure(state = "disabled")

    def newChangeFolder(self):
        p = multiprocessing.Process(target = self.execution.changeFolder())
        p.start()

    def newOpenCurrentFolder(self): 
        subprocess.Popen(f'explorer "{os.getcwd()}"')

if __name__ == '__main__':
    startUI = WindowUI()