# Choreogrpah (beta) v0.9

[English Version](./README.md)  

Environement logiciel permettant le paramétrage de robots à base de servo-moteur.  

## Choreograph vous permet

- Une **Description structurée** de vos robots  
Sur la base d'un fichier JSON, vous allez pouvoir décrire chaque controleur, chaque servo moteur et les regrouper pour former chaque membre de votre robot.

<div align="center"><img alt="skeleton.json" width="50%" src="docs/skeleton/img_skeleton_json.png" />&nbsp;<img alt="skeleton.screen" width="40%" src="docs/skeleton/img_skeleton_screen.png" /></div>  

[=> Détail sur le format du fichier](docs/skeleton/desc_skeleton.md)  

---

- Déterminer la **position neutre (trim)** de chaque servo.  
Une fois le fichier de squelette chargé, vous pourrez rechercher la position initiale de chaque servo-moteur de manière interactive et mettre à jour votre fichier JSON.  

<div align="center"><img alt="recalculate.trim" width="100%" src="docs/trim/img_recalculate_trim.png" /></div>  

[=> en savoir +](docs/skeleton/desc_trim.md)  

---

- Commander en **temps réel** chaque servo moteur indépendament et enregistrer des "**SnapShoot**" de position.  

<div align="center"><img alt="position.screen" width="60%" src="docs/position/img_position_screen.png" />&nbsp;<img alt="position.screen" width="30%" src="docs/position/img_position_screen2.png" /></div>  

[=> en savoir +](docs/position/desc_position.md)  

---

- **Créer des mouvements** en enchainant des positions préalablement enregistréess, grâce à des transistions paramétrables.  

<div align="center"><img alt="movement.screen" width="90%" src="docs/movement/img_movement.png" /></div>  

[=> en savoir +](docs/position/desc_movement.md)  

---

- **Exporter en langage C** la description du squelette et des mouvements pour une intégration directe dans vos codes sources.

<div align="center"><img alt="skeleton.json" width="49%" src="docs/skeleton/img_skeleton_json.png" />&nbsp;<img alt="export_c.screen" width="49%" src="docs/export_c/img_export_c.png" /></div>  

[=> en savoir +](docs/export_c/desc_export_c.md)  

---

- Prise en charge de **plusieurs types** de controleurs (Arduino Uno, Nano, Mega, Raspberry) et de servo-moteurs (pwm, serie). Il suffit de les déclarer dans la description du squelette.

<div align="center"><img alt="multi_type.screen" width="100%" src="docs/multi_type/img_multi_type.png" /></div>  

[=> en savoir +](docs/multi_type/desc_multi_type.md)  

---

- **Piloter votre robot** en attachant des mouvements paramétrés aux touches du clavier ou de votre manette bluetooth.

<div align="center"><img alt="controller.screen" width="100%" src="docs/controller/img_controller.png" /></div>  

[=> en savoir +](docs/controller/desc_controller.md)  

---

- **Multi langues** actuellement disponibles: Anglais et Français. Stockées sous forme de dictionnaire facilement modifiable.

<div align="center"><img alt="lang.screen" width="50%" src="docs/lang/img_lang.png" /></div>  

[=> en savoir +](docs/lang/desc_lang.md)  
