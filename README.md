Ce script vise à la création via le logiciel Blender:
	-d'images contenant une paroi de grotte ainsi que des sphères de couleur et tailles variables devant cette même paroi 
	-du masque binaire contenant les sphères associé à chaque image


Utilisation:

Ouvrir Blender (2.8+).
La scène par défaut comporte un cube, une caméra et une lumière.
Supprimer la lumière (si possible supprimer les données de lumières associées, si vous savez pas où c'est, c'est pas grave).

Le script peut fonctionner à partir de ces deux éléments (Cube et Caméra).
Si vous souhaitez changer d'objet de référence (ici Cube), supprimez le (de même, supprimer les données associées si possible) et créez ou importez un nouvel objet (par exemple une paroi de grotte).
Assurez vous que l'objet de référence est bien centré sur son origine (clic gauche sur l'objet pour le sélectionner -> clic droit -> Set Origin -> Geometry to Origin).

Ensuite, rendez vous dans l'onglet Scripting et ouvrez ce script.
Il y plusieurs paramètres changeables, tous au début.
Configurez les différents paramètres.
Configurez le placement de votre caméra en fonction des images désirées.
Lancez le script.
Les images et masques créés sont automatiquement enregistrées dans le dossier renseigné.


/!\ Précautions d'utilisation:

L'exécution du script étant assez lourde, Blender est inaccessible durant l'exécution.
Pour suivre l'exécution, il est conseillé d'ouvrir le dossier d'enregistrement ou la console (Window -> Toggle System Console) en parallèle.
Pour les mêmes raisons, il est conseillé de tester votre paramétrage sur une seule ou deux images plutôt que sur 100.

Attention à la numérotation, si dans le dossier d'enregistrement, il existe déjà des images ou masques du même nom (numéro), ils seront écrasés sans autre forme de procès.

Attention au placement et au paramétrage de votre caméra:
-si la caméra est trop près de l'objet de référence, il se peut que les sphères soient générées derrière l'objet
-si vous augmentez la distance focale de la caméra, il se peut que les sphères soient générées derrière la caméra (en fait devant la position absolue de la caméra mais derrière la "lentille")
Pour ces deux raisons, privilégiez l'agrandissement de votre objet de référence à un rapprochement ou un changement de focale de la caméra.

Les paramètres non explicitement mentionnés ci-dessous (et l'entièreté du script par ailleurs) sont modifiables à vos risques et périls si vous le souhaitez.


Paramètres:

Hauteur de l'image
Largeur de l'image
Format de l'image

Taille des sphères
Variation maximale de la taille des sphères
Nombre maximum de sphères à afficher
Choix du mode de coloration des sphères
Choix du nombre de sphères à afficher

Nom de la caméra à utiliser
Nom de l'objet à utiliser

Chemin d'enregistrement des images et des masques
Nombre d'images à créer par lancement de script
Nombre maximal d'images que l'on souhaite créer
Numéro de la première image
