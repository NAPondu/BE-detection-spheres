from re import I
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from numba import cuda
from PIL import Image
import pathlib
import os
import ntpath
import tensorflow as tf
import numpy as np

#Variables globales
global inputFilePath
global outputDirectoryPath 
global comboBox
comboBox = "Crop"
model = None
outputDirectoryPath = pathlib.Path().resolve()
IMAGE_SIZE = 128

#Clear la mémoire lorsque le logiciel est éteint
def on_closing():
    tf.keras.backend.clear_session()
    cuda.select_device(0)
    cuda.close()
    root.destroy()

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

#Coupe une image en plusieurs sous-images de taille IMAGE_SIZE*IMAGE_SIZE
def crop(input_file):
    img = Image.open(input_file)
    img_width, img_height = img.size
    for i in range(img_height//IMAGE_SIZE):
        for j in range(img_width//IMAGE_SIZE):
            box = (j*IMAGE_SIZE, i*IMAGE_SIZE, (j+1)*IMAGE_SIZE, (i+1)*IMAGE_SIZE)
            yield img.crop(box)

#Coupe l'ensemble des images passées en paramètre en plusieurs sous-images de taille IMAGE_SIZE*IMAGE_SIZE
#return un tableau contenant l'ensemble des images crop
def split(imagePath):
    nbSousImages = 0
    for infile in imagePath:
        img = Image.open(infile)
        nbSousImages = nbSousImages + int((img.width/IMAGE_SIZE)*(img.height/IMAGE_SIZE))
    imgArray = np.zeros((nbSousImages, IMAGE_SIZE, IMAGE_SIZE, 3))
    i = 0
    for infile in imagePath:
        for k, piece in enumerate(crop(infile), 1):
            img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), 255)
            img.paste(piece)
            imgArray[i] = np.asarray(img)
            i = i+1
    return imgArray

#Recombine les masques entre eux pour qu'ils correspondent à l'image originale 
def combineMask(imagePath, imgArrayMask, out_dir):
    nbSousImages = 0
    i = 0
    k = 0
    for infile in imagePath:
        img = Image.open(infile)
        new_im = Image.new('RGB', (img.width, img.height))
        nbSousImages = nbSousImages + int((img.width/IMAGE_SIZE)*(img.height/IMAGE_SIZE))
        for y in range(0, int(img.height/IMAGE_SIZE)):
            for x in range(0, int(img.width/IMAGE_SIZE)):
                imgMask = Image.fromarray((imgArrayMask[i]*255).astype(np.uint8))
                new_im.paste(imgMask, (x*IMAGE_SIZE,y*IMAGE_SIZE))
                i = i+1
        img_path = os.path.join(out_dir, 
                                    path_leaf(infile).split('.')[0]+ '_'
                                    + str(k).zfill(5) + '.png')
        new_im.save(img_path)
        k = k+1

#Resize les images en entrées en taille IMAGE_SIZE*IMAGE_SIZE
#Return un tableau des images resize
def resizeImg(imagePath):
    images = np.zeros((len(imagePath), IMAGE_SIZE, IMAGE_SIZE, 3))
    i = 0
    for img_name in imagePath:
        img = Image.open(img_name)
        img = img.resize((IMAGE_SIZE,IMAGE_SIZE), Image.ANTIALIAS)
        images[i] = np.asarray(img)
        i = i+1 
    return images

#Execute le modèle en effectuant un cropping des images
def launchModelCrop(imgArray, imagePath, out_dir):
    #Lancement de la progressBar
    popup = Toplevel()
    textPourcentage = StringVar()
    textImages = StringVar()
    textImages.set("Lancement du modèle...")
    Label(popup, textvariable=textPourcentage).grid(row=1,column=0)
    Label(popup, textvariable=textImages).grid(row=2,column=0)
    progress = 0
    progress_var = DoubleVar()
    progress_var.set(0.0)
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
    progress_bar.grid(row=0, column=0)
    popup.update()
    progress_step = float(100.0/len(imgArray))
    #Lancement du modèle
    predictions = model.predict(imgArray)
    imgArrayMask = np.zeros((len(predictions), IMAGE_SIZE, IMAGE_SIZE, 3))
    i = 0
    for img in predictions:
        popup.update()
        textImages.set("Enregistrement des images... ("+str(i)+"/"+str(len(predictions))+" images)")
        textPourcentage.set(str(int((i/len(predictions)*100)))+"%")
        imgArrayMask[i] = np.asarray(img)
        progress += progress_step
        progress_var.set(progress)
        i = i+1
    textImages.set("Création des masques...")
    textPourcentage.set("")
    combineMask(imagePath, imgArrayMask, out_dir)
    popup.destroy()

#Execute le modèle en resizant les images 
def launchModelResize(images, out_dir):
    #Lancement de la progressBar
    popup = Toplevel()
    textPourcentage = StringVar()
    textPourcentage.set("0%")
    textImages = StringVar()
    textImages.set("Lancement du modèle...")
    Label(popup, textvariable=textPourcentage).grid(row=1,column=0)
    Label(popup, textvariable=textImages).grid(row=2,column=0)
    progress = 0
    progress_var = DoubleVar()
    progress_var.set(0.0)
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
    progress_bar.grid(row=0, column=0)
    popup.update()
    progress_step = float(100.0/len(images))
    #Lancement du modèle
    predictions = model.predict(images)
    i = 1
    for img in predictions:
        popup.update()
        textImages.set("Enregistrement des images... ("+str(i)+"/"+str(len(images))+" images)")
        textPourcentage.set(str(int((i/len(images)*100)))+"%")
        new_im = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE))
        imgMask = Image.fromarray((np.squeeze(img, axis=2)*255).astype(np.uint8))
        new_im.paste(imgMask, (0,0))
        img_path = os.path.join(out_dir, 
                                    "Resize"+ '_'
                                    + str(i).zfill(5) + '.png')
        new_im.save(img_path)
        i = i+1
        progress += progress_step
        progress_var.set(progress)
    popup.destroy()

#Gestion d'erreurs lors de l'execution du programme
def gestionErreurs():
    try: inputFilePath
    except NameError:
        messagebox.showerror("Erreur", "Vous n'avez pas sélectionné d'image!")
        return True
    else:
        if not inputFilePath:
            messagebox.showerror("Erreur", "Vous n'avez pas sélectionné d'image!")
            return True
    try: outputDirectoryPath
    except NameError:
        messagebox.showerror("Erreur", "Vous n'avez pas sélectionné de répertoire!")
        return True
    else: 
        if not outputDirectoryPath:
            messagebox.showerror("Erreur", "Vous n'avez pas sélectionné de répertoire!")
            return True
    try: int(intensiteLumineuse.get())
    except ValueError:
        messagebox.showerror("Erreur", "Vous devez entrer un nombre entier pour l'intensité!")
        return True
    else: 
        if int(intensiteLumineuse.get())<0 or int(intensiteLumineuse.get())>255:
            messagebox.showerror("Erreur", "L'intensité lumineuse doit être comprise entre 0 et 255!")
            return True
    try: float(rayonSphere.get())
    except ValueError:
        messagebox.showerror("Erreur", "Vous devez entrer un nombre pour le rayon de la sphère!")
        return True
    else: 
        if (float(rayonSphere.get()))<0:
            rayonSphere.set(abs(float(rayonSphere.get())))
    return False

#Permet d'executer notre programme
def run():
    #Gestion d'erreurs
    if gestionErreurs():
        return
    #Load modele
    global model
    if model is None:
        model = tf.keras.models.load_model("model.h5")
    #Observe la valeur dans la comboBox
    global comboBox
    if not comboBox or comboBox is None:
        messagebox.showerror("Erreur", "Vous n'avez pas sélectionné de valeur dans la configuration!")
        return
    if comboBox=="Crop":
        #Conserve les sous-images (de taille IMAGE_SIZE*IMAGE_SIZE) dans le tableau imgArray
        imgArray = split(inputFilePath)
        #Execute le modele
        launchModelCrop(imgArray, inputFilePath, outputDirectoryPath)
    if comboBox=="Resize":
        #Resize tout les images
        imgArray = resizeImg(inputFilePath)    
        #Execute le modele
        launchModelResize(imgArray, outputDirectoryPath)
    
    boolDetaille = rapportDetaille.get()
    boolSimple = rapportSimple.get()
    intIntensite = int(intensiteLumineuse.get())
    floatRayon = float(rayonSphere.get())
    cheminsFichiers = inputFilePath
    print(str(boolSimple)+" "+str(boolDetaille)+" "+str(intIntensite)+" "+str(floatRayon)+" "+str(cheminsFichiers))

#Est appellé quand la valeur "resize" ou "crop" de la comboBox est modifiée
def comboBoxChange(event):
    global comboBox
    comboBox = SelectLaunchOption.get()

#Initialisation
root = Tk()
root.wm_title("Sphere Detection")
entryInputText = StringVar()
entryOutputText = StringVar()
rapportDetaille = IntVar()
rapportSimple = IntVar()
intensiteLumineuse = StringVar()
intensiteLumineuse.set(str(255))
rayonSphere = StringVar()
rayonSphere.set(str(1))

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
aideEtapeUne = LabelFrame(aideFrame, text=" 1. Entrees/sorties")
aideEtapeUne.grid(row=1, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
aideLabel1 = Label(aideEtapeUne, text= "Veuillez sélectionner des images avant de lancer le programme")
aideLabel1.grid(row=0, sticky=W)
aideLabel2 = Label(aideEtapeUne, text= "Le répertoire d'enregistrement par défaut est:")
aideLabel2.grid(row=1, sticky=W)
aideLabel3 = Label(aideEtapeUne, text= pathlib.Path().resolve(), fg="#007BFF")
aideLabel3.grid(row=2, sticky=W)
aideLabel4 = Label(aideEtapeUne, text= "Vous pouvez choisir de modifier ce répertoire")
aideLabel4.grid(row=3, sticky=W)
aideEtapeDeux = LabelFrame(aideFrame, text=" 2. Configuration")
aideEtapeDeux.grid(row=2, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
aideLabel5 = Label(aideEtapeDeux, text= "Crop donnera des résultats précis mais est plus lent à éxecuter")
aideLabel5.grid(row=0, sticky=W)
aideLabel6 = Label(aideEtapeDeux, text= "Resize est plus rapide mais moins précis")
aideLabel6.grid(row=1, sticky=W)
aideLabel7 = Label(aideEtapeDeux, text= "Rapport simple = données en moyenne sur une image")
aideLabel7.grid(row=2, sticky=W)
aideLabel8 = Label(aideEtapeDeux, text= "Rapport detaille = données de chaque sphère sur chaque image")
aideLabel8.grid(row=3, sticky=W)
aideLabel9 = Label(aideEtapeDeux, text= "Changer l'intensité max si les sphères sont de couleurs spécifiques")
aideLabel9.grid(row=4, sticky=W)

#Label Frame 2
etapeDeux = LabelFrame(root, text=" 2. Configuration: ")
etapeDeux.grid(row=2, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
SelectLaunchOption = ttk.Combobox(etapeDeux, values=["Crop",  "Resize"], state="readonly")
SelectLaunchOption.grid(row=0, sticky='W')
SelectLaunchOption.current(0)
SelectLaunchOption.bind('<<ComboboxSelected>>', comboBoxChange)
CheckboxSimple = Checkbutton(etapeDeux, text='Rapport simple', variable=rapportSimple)
CheckboxSimple.grid(row=1, column=0 ,sticky='W')
CheckboxDetaille = Checkbutton(etapeDeux, text='Rapport detaille', variable=rapportDetaille)
CheckboxDetaille.grid(row=1, column=1, sticky='W')
LabelIntensiteLumineuse = Label(etapeDeux, text= "Intensité la plus élevée en RGB: ")
LabelIntensiteLumineuse.grid(row=6, column=0, sticky='W', columnspan=7)
EntryIntensiteLumineuse = Entry(etapeDeux, textvariable=intensiteLumineuse)
EntryIntensiteLumineuse.grid(row=6, column=7, sticky='W')
LabelRayonSphere = Label(etapeDeux, text= "Taille prévue des sphères en unité arbitraire: ")
LabelRayonSphere.grid(row=7, column=0, sticky='W', columnspan=7)
EntryRayonSphere = Entry(etapeDeux, textvariable=rayonSphere)
EntryRayonSphere.grid(row=7, column=7, sticky='W')

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

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()