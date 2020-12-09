# fichier: projet

Ce fichier permet de charger en une seule fois, l'ensemble des autres fichiers de paramétrage.

format: **json**  
Extension: **.pjt**  

	{
	 "detail":
		{
		"description": "My project from OttO robot.",
		"filepath": "../_projects/otto/",
		"view": "view.jpg",
		"skeleton": "otto.skt",
		"position": "positions",
		"movement": "movements",
		"controller": "../../_controllers/controller_ps3.ctl"
		}
	}

- **description**:  permet de décrire le projet
- **filepath**:     chemin de base du projet à partir de l'application Choregraph
- **view**:         chemin/nom de l'image.jpg, image du robot au format jpeg
- **skeleton**:     fichier de description du squelette au format json
- **position**:		sous dossier à partir du dossier du projet *filepath* contenant les positions au format json
- **movement**:		sous dossier à partir du dossier du projet *filepath* contenant les mouvements au format json
- **controller**:	chemin+fichier de description du controleur au format json

---

[<= Retour](../../README_fr.md)  
[=> Tous les formats de fichiers](../file_format_fr.md)  