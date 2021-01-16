# fichier: Position

Ce fichier permet de décrire une position du robot, c'est à dire la position de certains ou tous les moteurs du robot.  
Le nom du fichier proposé est une concaténation de la catégorie et du nom.  

format: **json**  
Extension: **.pos**  

```JSON
    {
     "category": "default",
     "name": "init",
     "description": "Initial position.\n The robot is standing.",
     "motors":
        {
         "YL": "90",
         "YR": "90",
         "RL": "90",
         "RR": "90"
        }
    }
```

* **category**: famille de la position
* **name**: nom de la position
* **description**: description de la position. Les retours à la ligne se font par "\n"
* **motors**: liste des moteurs avec:  
"nom" : "position"

---

[<= Retour](../..README_fr.md)  
[=> Tous les formats de fichiers](../file_format_fr.md)  
