# fichier: Mouvement
Ce fichier permet de décrire une position du robot, c'est à dire la position de certains ou tous les moteurs du robot.   
Le nom du fichier proposé est une concaténation de la catégorie et du nom.  

format: **json**  
Extension: **.mov**  


	{
	  "name": "shake_leg",
	  "duration": 500,
	  "functions": {
		"I001": {
		  "function": "Linear",
		  "position": "shakeleg_1",
		  "duration": 500,
		  "nb_step": 0
		},
		"I002": {
		  "function": "Linear",
		  "position": "shakeleg_2",
		  "duration": 500,
		  "nb_step": 0
		}
	  },
	  "id": "I007",
	  "file": "C:/Choregrpah_TK/PROJECTS/otto/movements/shake_leg.mov"
	}

* **name**: nom du mouvement
* **duration**: unité de temps du mouvement
* **functions**: liste des positions sous forme d'objet
* * **function**: fonction de mouvement
* * **position**: nom de la position    
ATTENTION, la poistion doit être chargée et disponible dans la liste des positions
* * **duration**: durée du mouvement
* * **nb_step**: nombre d'étape en fonction de la durée de la position et de l'unité de temps du mouvement (duration)
* **id**: id du mouvement dans la liste des mouvements
* **file**: chemin/nom_du_fichier.mov

---

[<= Retour](../../README_fr.md)  
[=> Tous les formats de fichiers](../file_format_fr.md)  