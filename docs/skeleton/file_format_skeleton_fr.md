# fichier: Squelette  

Ce fichier permet de décrire l'ensemble du paramétrage du robot.  
Les servo moteurs sont définis puis intégrés à des "motorgroups", eux même rattachés à un controleur.  
Un robot peut comporter plusieurs controleurs.

format: **json**  
Extension: **.skt**  

```json
{
 "controller":
   {
    "Name_of_controller 1":
        {
         "type": "arduino_nano",
         "connection": "serial",
         "address": ["COM5",500000],
         "port": "pin",
         "sync_read": true,
         "attached_motorgroups": ["left_leg", "right_leg"]
         "mg_alignment" : "h"
        }
    },
 "motorgroups":
    {
     "left_leg": ["YL", "RL"],
     "right_leg": ["YR", "RR"]
    },
 "motors":
    {
     "YL":
        {
         "id": 5,
         "type": "servo_pwm",
         "orientation" : "direct",
         "offset" : 19,
         "angle_limit": [0, 180],
         "default_position": 90,
         "skeleton_position": [2, 1, 1]
        },
     "YR":
        {
         "id": 10,
         "type": "servo_pwm",
         "orientation" : "indirect",
         "offset" : -15,
         "angle_limit": [0, 180],
         "default_position": 90,
         "skeleton_position": [0, 1, -1]
        },
     "RL":
        {
         "id": 6,
         "type": "servo_pwm",
         "orientation" : "direct",
         "offset" : -18,
         "angle_limit": [0, 180],
         "default_position": 90,
         "skeleton_position": [2, 2, 1]
        },
     "RR":
        {
         "id": 11,
         "type": "servo_pwm",
         "orientation" : "indirect",
         "offset" : 5,
         "angle_limit": [0, 180],
         "default_position": 90,
         "skeleton_position": [0, 2, -1]
        }
    }
}
```

## "controller"

Permet de paramétrer la ou les carte(s) controleurs des servo-moteurs.  
Cette section peut comporter plusieurs objet correspondant à différentes cartes controleurs de servo-moteurs.  

* **type**: type de carte entre:  
arduino, arduino_uno, arduino_nano, arduino_mega, pi, pi_b, pi_3, pi_4
* **connection**: type de connexion à la carte:  
serial, lan, onboard
* **address**: liste avec les informations necessaire à la connexion
  * **serial**: [port_com, baudrate]
  * **lan**: [@_ip, port_ip]
  * **onboard**: [nop]
* **sync_read**: non implémenté
* **attached_motorgroups**: Liste des "motorgroup" attachés à ce controleur
* **mg_alignment**: alignement des moteurs par "motorgroup" dans l'onglet "Squelette":  
"h" pour horizontal, "v" pour vertical

## "motorgroups"

Un "motorgroup" est un regroupement logique de servo-moteurs correspondant par exmple à une articulation ou un membre.  
Cette section permet de lister les "motorgroups" et définir pour chacun les servo-moteurs qui le compose.  

* **"nom_du_motorgroup1"**: ["servo1", "servo2"]
* **"nom_du_motorgroup2"**: ["servo3", "servo24]

## motors

Permet de définir l'ensemble des servo-moteurs du robot. Ceci seront dispatchés dans les "motorgroups".

* **id**: GPIO sur la carte controleur
* **type**: type du moteur entre:  
servo_pwm, servo_serial, mboxe_a, mboxe_b  
* **orientation**: permet de définir le sens de rotation du moteur:  
direct, indirect
* **offset**: décalage au démarrage afin d'ajuster la position par défaut
* **angle_limit**: limite en position min et max du moteur à ne pas dépasser: [pos_min, pos_max]
* **default_position**: position au démarrage
* **skeleton_position**: permet de définir dans l'onglet interatif, la position du moteur:  
[colonne, ligne, alignement] à noter que les N° de colonne et de ligne commencent à 0  

---

[=> Tous les formats de fichiers](../file_format_fr.md)  

---

[<= Retour](../../README_fr.md#description_strcuturee)  
