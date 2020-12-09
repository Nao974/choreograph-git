# fichier: Controller
Ce fichier permet de décrire et d'associer chaque bouton du controleur à une touche du clavier pour simulation ainsi qu'à un mouvement.  
ATTENTION la liste des touches associées au clavier doit être strictement la meme que l'association avec les mouvements.

format: **json**  
Extension: **.ctl**  


	{
	  "controller_name": 
		{
		 "model": "Dualshock 3 Wireless",
		 "picture": "controller_ps3.jpg",
		 "adress": "localhost",
		 "port": "auto",
		 "sync_read": true
		},
	  "keys":
		{
		 "L1": "&",
		 "L2": "é",
		 "R1": ")",
		 "R2": "=",
		 "LF": "q",
		 "RG": "d",
		 "UP": "z",
		 "DW": "s",
		 "S" : "k",
		 "O" : "m",
		 "T" : "o",
		 "X" : "l"
		},
	  "movements":
		{
		 "L1": "jump",
		 "L2": "shake_leg",
		 "R1": "flapping",
		 "R2": "moonwalker",
		 "LF": "turn_left_key",
		 "RG": "turn_right_key",
		 "UP": "walk_fd_key",
		 "DW": "walk_bd_key",
		 "S" : "",
		 "O" : "",
		 "T" : "crusaito",
		 "X" : "Swing"
		}  
	}

* **model**: modèle du controleur
* **picture**: image du controleur au format jpeg
* **adress**: non implémenté
* **port**: non implémenté
* **sync_read**: non implémenté
* **keys**: liste des boutons du controleur avec la touche clavier associée:  
"bouton": "touche_clavier"
* **movements**: liste des boutons du controleur avec le mouvement associé:  
"bouton": "mouvement"  
ATTENTION, le mouvement doit être chargé dans la liste de l'onglet "Mouvement".

---

[<= Retour](../../README_fr.md)  
[=> Tous les formats de fichiers](../file_format_fr.md)  