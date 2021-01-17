# fichier: projet

Ce fichier permet de charger en une seule fois, l'ensemble des fichiers de paramétrage.

format: **json**  
Extension: **.pjt**  

```json
{
 "detail":
  {
   "description": "My project from OttO robot.",
   "filepath": "./data/otto/",
   "view": "view.jpg",
   "skeleton": "otto.skt",
   "position": "positions",
   "movement": "movements",
   "controller": "./_controllers/controller_ps3.ctl"
  }
}
```

- **description**: permet de décrire le projet
- **filepath**: chemin de base du projet à partir de l'application Choregraph
- **view**: chemin/nom de l'image.jpg, image du robot au format jpeg
- **skeleton**: fichier de description du squelette au format json
- **position**: sous dossier à partir du dossier du projet *filepath* contenant les positions au format json
- **movement**: sous dossier à partir du dossier du projet *filepath* contenant les mouvements au format json
- **controller**: chemin + fichier de description du contrôleur au format json

---

[=> Tous les formats de fichiers](../file_format_fr.md)

---

[<= Retour](../../README_fr.md#file-format)
