# Multi-Types

Dans votre fichier de description de votre robot *(squelette.skt)*, vous allez définir le type de vos contrôleurs ainsi que ceux de vos servo-moteurs.  
[=> format squelette.skt](../skeleton/file_format_skeleton_fr.md)

## **Les Contrôleurs**

Les contrôleurs pour le moment supportés sont les cartes:

- arduino, arduino_uno, arduino_nano, arduino_mega
  - Seul le firmware pour les cartes Arduino est pour le moment développé

- Raspberry Pi, Pi_b, Pi 3, Pi 4
  - Choreograph pilote directement les servo-moteurs par les GPIOs de celle-ci.
  - il conviendra donc de décrire votre contrôleur avec *connection: onboard*

---

## **Les Servo-moteurs**

Les actionneurs actuellement supportés sont les servo-moteurs:

- les servo-moteurs standard PWM (pour modélisme)

- M-Boxe, uniquement par Raspbery Pi  
[=> GutHub: projet M-Boxe](https://github.com/Nao974/M-BOXE)

- Les servo-moteurs séries peuvent être déclarés dans le squelette.skt mais ne sont pas pour le moment pris en charge par le firmware.

---

[<= Retour](../../README_fr.md#multi-type)
