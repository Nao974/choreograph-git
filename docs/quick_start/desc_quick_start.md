# Démarrage Rapide

OK, vous avez monté votre robot et effectué quelques tests de bon fonctionnement sur les différents servo-moteurs, place maintenant aux Mouvements !!!

**Tout se passe dans le dossier *./data***

* dupliquer le dossier *.data/_default_project*
  * le renommer du nom de votre projet
* dupliquer le fichier *./data/_defaut_project.pjt
  * le renommer du nom de votre projet
  * l'ouvrir est modifier les balises suivantes à minima
    * **description**: avec la précédemment de votre robot
    * **filepath**: modifier le chemin avec le nom du dossier precedement renommé
    * [=> format complet du fichier projet](../projet/file_format_project_fr.md)
* dans le dossier de votre projet, remplacer le fichier **view.jpg** par une image de votre robot, elle sera affichée à chaque chargement de votre projet.

---

Modifions maintenant le fichier de description de votre robot en ouvrant le fichier *skeleton.skt*

* A minima, il convient de modifier
  * sur le noeud *controller*
    * le type de votre carte
    * la connexion et le port
  * décrire chaque servo-moteur
  * vous pouvez maintenant regrouper les servo-moteurs de chaque membre dans le noeud *motorgroups*
  * et enfin attacher ces *motorgroups* au bon contrôleur
* Tous les détails se trouvent dans la documentation [=> format complet squeleton.skt](../skeleton/file_format_skeleton_fr.md)

---

Charger le firmware *Choreograph* dans votre carte [=> documentation firmware](../firmware/desc_firmware_fr.md)

---

* Vous pouvez maintenant enregistrer vos propres positions
  * [=> documentation sur les positions](../position/desc_position_fr.md)
* Puis les enchainer sous forme de mouvements
  * [=> documentation sur les mouvements](../movement/desc_movement_fr.md)
* Piloter votre robot à partir de votre clavier ou manette BT
  * [=> documentation sur les contrôleurs](../controller/desc_controller_fr.md)

---

[<= Retour](../../README_fr.md#controller)
