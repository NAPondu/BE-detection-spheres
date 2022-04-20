from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import pathlib
import ntpath

global inputFilePath
global outputDirectoryPath 
outputDirectoryPath = pathlib.Path().resolve()

#Découpe un chemin pour n'avoir que le dernier élément
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

#Permet d'ouvrir une ou plusieurs images et conserve le chemin dans inputFilePath
def openInputFile():
    global inputFilePath
    inputFilePath = filedialog.askopenfilenames(initialdir=pathlib.Path().resolve(),title="Sélectionnez image(s)",filetypes=(("JPG","*.jpg"),("JPEG","*.jpeg"),("PNG","*.png"),("Autres","*.*")))
    if not inputFilePath:
        entryInputText.set("Aucune image sélectionnée!")
    if len(inputFilePath)==1:
        entryInputText.set(path_leaf(inputFilePath[0]))
    if len(inputFilePath)>1:
        entryInputText.set(path_leaf(inputFilePath[0]) + " + " + str(len(inputFilePath)-1) + " autre(s)")

#Permet d'ouvrir un répertoire et conserve le chemin dans outputDirectoryPath
def openOutputDirectory():
    global outputDirectoryPath 
    outputDirectoryPath = filedialog.askdirectory(title="Sélectionnez un répertoire")
    if not outputDirectoryPath:
        entryOutputText.set("Aucun répertoire sélectionné!")
    if outputDirectoryPath:
        entryOutputText.set(outputDirectoryPath)

#Permet d'executer notre programme (WIP)
def run():
    #Gestion d'erreurs
    try: inputFilePath
    except NameError:
        messagebox.showerror("Erreur", "Vous n'avez pas sélectionné d'image!")
        return
    else:
        if not inputFilePath:
            messagebox.showerror("Erreur", "Vous n'avez pas sélectionné d'image!")
            return
    try: outputDirectoryPath
    except NameError:
        messagebox.showerror("Erreur", "Vous n'avez pas sélectionné de répertoire!")
        return
    else: 
        if not outputDirectoryPath:
            messagebox.showerror("Erreur", "Vous n'avez pas sélectionné de répertoire!")
            return

#Initialisation
root = Tk()
root.wm_title("Sphere Detection")
entryInputText = StringVar()
entryOutputText = StringVar()

#Label Frame 1
etapeUne = LabelFrame(root, text= " 1. Fichiers entrée / sortie: ")
etapeUne.grid(row=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
fileInputLabel = Label(etapeUne, text="Sélectionnez image(s)")
fileInputLabel.grid(row=0, column=0, sticky='E', padx=5, pady=2)
fileInputEntry = Entry(etapeUne, state="readonly", fg="#007BFF", textvariable=entryInputText,width=42)
fileInputEntry.grid(row=0, column=1, columnspan=7, sticky="WE", pady=3)
fileInputButton = Button(etapeUne, text = "Modifier ...", command=openInputFile)
fileInputButton.grid(row=0, column=8, sticky='W', padx=5, pady=2)
outputFileLabel = Label(etapeUne, text="Sauvegarder résultat dans:")
outputFileLabel.grid(row=1, column=0, sticky='E', padx=5, pady=2)
entryOutputText.set(pathlib.Path().resolve())
outputFileEntry = Entry(etapeUne, state="readonly", fg="#007BFF", textvariable=entryOutputText,width=42)
outputFileEntry.grid(row=1, column=1, columnspan=7, sticky="WE", pady=2)
outputFileButton = Button(etapeUne, text="Modifier ...",command=openOutputDirectory)
outputFileButton.grid(row=1, column=8, sticky='W', padx=5, pady=2)

#Label Frame Aide
aideFrame = LabelFrame(root, text=" Aide rapide")
aideFrame.grid(row=0, column=9, columnspan=2, rowspan=8, sticky='NS', padx=5, pady=5)
aideLabel1 = Label(aideFrame, text= "Veuillez sélectionner des images avant de lancer le programme")
aideLabel1.grid(row=0, sticky=W)
aideLabel2 = Label(aideFrame, text= "Le répertoire d'enregistrement par défaut est:")
aideLabel2.grid(row=1, sticky=W)
aideLabel3 = Label(aideFrame, text= pathlib.Path().resolve(), fg="#007BFF")
aideLabel3.grid(row=2, sticky=W)
aideLabel4 = Label(aideFrame, text= "Vous pouvez choisir de modifier ce répertoire")
aideLabel4.grid(row=3, sticky=W)

#Label Frame 2
etapeDeux = LabelFrame(root, text=" 2. Configuration: ")
etapeDeux.grid(row=2, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
labelWIP2 = Label(etapeDeux, text= "WIP")
labelWIP2.grid(row=0)

#Label Frame 3
etapeTrois = LabelFrame(root, text= " 3. Données générées: ")
etapeTrois.grid(row=3, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
labelWIP3 = Label(etapeTrois, text= "WIP")
labelWIP3.grid(row=0)

#Launch frame
launchFrame = Frame(root)
launchFrame.grid(row=4, columnspan=7, padx=5, pady=5, ipadx=5, ipady=5)
launchButton = Button(launchFrame, text="Executer le programme",command=run)
launchButton.grid(row=1, column=8, padx=5, pady=2)

root.mainloop()