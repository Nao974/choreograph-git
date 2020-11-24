# Choreogrpah (beta) v0.9

Environement logiciel permettant le paramétrage de robots à base de servo-moteur.  
[English Version](https://github.com/Nao974/M-BOXE_MANAGER_TK/blob/master/README.md)  

## Choreograph vous permet

- Une **Description structurée** de vos robots  
Sur la base d'un fichier JSON, vous allez pouvoir décrire chaque controleur, chaque servo moteur et les regrouper pour former chaque membre de votre robot.

<div align="center"><img alt="skeleton.json" width="60%" src="docs/skeleton/img_skeleton_json.png" />&nbsp;<img alt="skeleton.screen" width="30%" src="docs/skeleton/img_skeleton_screen.png" /></div>  

[=> Détail sur le format du fichier](docs/skeleton/desc_skeleton.md)  

---

- Déterminer la **position neutre (trim)** de chaque servo.  
Une fois le fichier de squelette chargé, vous pourrez rechercher la position initiale de chaque servo-moteur de manière interactive et mettre à jour votre fichier JSON.  

<div align="center"><img alt="recalculate.trim" width="100%" src="docs/trim/img_recalculate_trim.png" /></div>  

[=> en savoir +](docs/skeleton/desc_trim.md)  

---

- Piloter en **temps réel** chaque servo moteur indépendament et enregistrer des "**SnapShoot**" de position.  

<div align="center"><img alt="position.screen" width="60%" src="docs/position/img_position_screen.png" />&nbsp;<img alt="position.screen" width="30%" src="docs/position/img_position_screen2.png" /></div>  

[=> en savoir +](docs/position/desc_position.md)  

---

- **Créer des mouvements** en enchainant des positions préalablement enregistréess, grâce à des transistions paramétrables.  

<div align="center"><img alt="movement.screen" width="90%" src="docs/movement/img_movement.png" /></div>  

[=> en savoir +](docs/position/desc_movement.md)  

---

- **Exporter en langage C** la description du squelette et des mouvements pour une intégration directe dans vos codes sources.

<div align="center"><img alt="skeleton.json" width="49%" src="docs/skeleton/img_skeleton_json.png" />&nbsp;<img alt="skeleton.screen" width="49%" src="docs/export_c/img_export_c.png" /></div>  

[=> en savoir +](docs/export_c/desc_export_c.md)  

---

- **Pilotage du robot** par le clavier ou manette Bluetooth  
blablabal  

<div align="center"><img alt="skeleton.json" width="40%" src="docs/skeleton/img_recalculate_trim.png" /></div>  

[Recalcule Trim](https://github.com/Nao974/choreograph-git/blob/Update-Docs/docs/trim/trim_fr.md)  

- Prise en charge de **plusieurs types** de servo-moteurs (pwm, serie, autres)  
blabal  

<div align="center"><img alt="skeleton.json" width="40%" src="docs/skeleton/img_recalculate_trim.png" /></div>  

[Recalcule Trim](https://github.com/Nao974/choreograph-git/blob/Update-Docs/docs/trim/trim_fr.md)  

- **Multi langues**  
blablabal  

<div align="center"><img alt="skeleton.json" width="40%" src="docs/skeleton/img_recalculate_trim.png" /></div>  

[Recalcule Trim](https://github.com/Nao974/choreograph-git/blob/Update-Docs/docs/trim/trim_fr.md)  
