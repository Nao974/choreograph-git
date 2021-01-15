# fichier: Controller

Ce fichier permet d'attacher vos mouvements aux touches de votre manette bluetooch ou de votre clavier.

* Attacher vos mouvements aux boutons de la manette
* Lier les touches de votre clavier aux boutons de la manette

format: **json**  
Extension: **.ctl**  

```json
{
 "controller_name": 
    {
     "model": "Dualshock 3 Wireless",
     "picture": "controller_ps3.jpg",
     "adress": "localhost",
     "port": "auto",
     "sync_read": true
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
    }
}
```

* **model**: modèle du controleur
* **picture**: image du controleur au format jpeg
* **adress**: non implémenté
* **port**: non implémenté
* **sync_read**: non implémenté
* **movements**: liste des boutons du controleur avec le mouvement associé:
  * "bouton": "mouvement"  
* **keys**: liste des boutons du controleur avec la touche clavier associée:  
  * "bouton": "touche_clavier"

ATTENTION, les mouvements doivent être chargés dans la liste de l'onglet "Mouvement".

---

[=> Tous les formats de fichiers](../file_format_fr.md)

---

[<= Retour](../../README_fr.md#controller)  
