# Choreograph (beta) v0.9

<a id="up"></a>

[![Video Presentation](docs/video_presentation.png)](https://youtu.be/9EAe0ReYfHI)

[English Version](./README.md)  

[Démarrage Rapide](#demarrage-rapide)  

---

Environnement logiciel permettant le paramétrage de robots à base de servo-moteur.  

## Choreograph vous permet

<a id="format-skeleton"></a>

- Une **Description structurée** de vos robots  
Sur la base d'un fichier JSON, vous allez pouvoir décrire chaque contrôleur, chaque servo moteur et les regrouper pour former les membres de votre robot.

<div align="center"><img alt="skeleton.json" width="50%" src="docs/skeleton/img_skeleton_json.png" />&nbsp;<img alt="skeleton.screen" width="40%" src="docs/skeleton/img_skeleton_screen.png" /></div>  

[=> en savoir +](docs/skeleton/file_format_skeleton_fr.md)  

---
<a id="desc-trim"></a>

- Déterminer la **position neutre (trim)** de chaque servo.  
Une fois le fichier de squelette chargé, vous pourrez rechercher la position initiale de chaque servo-moteur et recalculer leur offset.  

<div align="center"><img alt="recalculate.trim" width="100%" src="docs/trim/img_recalculate_trim.png" /></div>  

[=> en savoir +](docs/trim/desc_trim_fr.md)  

---
<a id="position"></a>

- Commander en **temps réel** chaque servo moteur indépendamment et enregistrer des **SnapShot** de position.  

<div align="center"><img alt="position.screen" width="60%" src="docs/position/img_position_screen.png" />&nbsp;<img alt="position.screen" width="30%" src="docs/position/img_position_screen2.png" /></div>  

[=> en savoir +](docs/position/desc_position_fr.md)  

---
<a id="movement"></a>

- **Créer des mouvements** en enchainant des positions préalablement enregistrées, grâce à des transitions paramétrables.  

<div align="center"><img alt="movement.screen" width="90%" src="docs/movement/img_movement.png" /></div>  

[=> en savoir +](docs/movement/desc_movement_fr.md)  

---
<a id="export-c"></a>

- **Exporter en langage C** la description du squelette et des mouvements pour une intégration directe dans vos codes sources.

<div align="center"><img alt="skeleton.json" width="49%" src="docs/skeleton/img_skeleton_json.png" />&nbsp;<img alt="export_c.screen" width="49%" src="docs/export_c/img_export_c.png" /></div>  

[=> en savoir +](docs/export_c/desc_export_c_fr.md)  

---
<a id="multi-type"></a>

- Prise en charge de **plusieurs types** de contrôleurs (Arduino Uno, Nano, Mega, Raspberry) et de servo-moteurs (pwm, série). Il suffit de les déclarer dans la description du squelette.

<div align="center"><img alt="multi_type.screen" width="75%" src="docs/multi_type/img_multi_type.png" /></div>  

[=> en savoir +](docs/multi_type/desc_multi_type_fr.md)  

---
<a id="controller"></a>

- **Piloter votre robot** en attachant les mouvements paramétrés aux touches du clavier ou de votre manette Bluetooth.

<div align="center"><img alt="controller.screen" width="75%" src="docs/controller/img_controller.png" /></div>  

[=> en savoir +](docs/controller/desc_controller_fr.md)  

---
<a id="firmware"></a>

- Le **Firmware** est à charger dans votre robot.  
Disponible pour les cartes Arduino, il est à charger depuis l'IDE Arduino.  
Le support VSCode PIO est en cours de développement ainsi que d'autres cartes Micro Contrôleur.

<div align="center"><img alt="lang.screen" width="75%" src="docs/firmware/img_doc1_firmware_arduino.png" /></div>  

[=> en savoir +](docs/firmware/desc_firmware_fr.md)  

---
<a id="multi-lang"></a>

- **Multi langues**, disponible en Anglais et Français, les langues sont stockées sous forme de dictionnaire facilement modifiable.

<div align="center"><img alt="lang.screen" width="50%" src="docs/lang/img_lang.png" /></div>  

---
<a id="file-format"></a>

- L'ensemble des formats de paramétrage sont décrits dans le lien suivant.  

[=> en savoir +](docs/file_format_fr.md)  

---

## Démarrage Rapide

<a id="demarrage-rapide"></a>

OK, vous avez monté votre robot et effectué quelques tests de bon fonctionnement sur les différents servo-moteurs, place maintenant aux Mouvements !!!

**Tout se passe dans le dossier *./data***

- dupliquer le dossier *.data/_default_project*
  - le renommer du nom de votre projet
- dupliquer le fichier *./data/_defaut_project.pjt
  - le renommer du nom de votre projet
  - l'ouvrir est modifier les balises suivantes à minima
    - **description**: avec la précédemment de votre robot
    - **filepath**: modifier le chemin avec le nom du dossier precedement renommé
    - [=> format complet du fichier projet](docs/projet/file_format_project_fr.md)
- dans le dossier de votre projet, remplacer le fichier **view.jpg** par une image de votre robot, elle sera affichée à chaque chargement de votre projet.

---

Modifions maintenant le fichier de description de votre robot en ouvrant le fichier *skeleton.skt*

- A minima, il convient de modifier
  - sur le noeud *controller*
    - le type de votre carte
    - la connexion et le port
  - décrire chaque servo-moteur
  - vous pouvez maintenant regrouper les servo-moteurs de chaque membre dans le noeud *motorgroups*
  - et enfin attacher ces *motorgroups* au bon contrôleur
- Tous les détails se trouvent dans la documentation [=> format complet squeleton.skt](docs/skeleton/file_format_skeleton_fr.md)

---

Charger le firmware *Choreograph* dans votre carte [=> documentation firmware](docs/firmware/desc_firmware_fr.md)

---

- Vous pouvez maintenant enregistrer vos propres positions
  - [=> documentation sur les positions](docs/position/desc_position_fr.md)
- Puis les enchainer sous forme de mouvements
  - [=> documentation sur les mouvements](docs/movement/desc_movement_fr.md)
- Piloter votre robot à partir de votre clavier ou manette BT
  - [=> documentation sur les contrôleurs](docs/controller/desc_controller_fr.md)

---

[=> Haut](#up)
