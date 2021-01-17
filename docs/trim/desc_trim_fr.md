# Déterminer la position neutre (trim)  

Lorsque vous montez votre robot, vous allez certainement positionner vos servo-moteurs sur leur valeur médiane puis monter le palonnier. Mais celui-ci ne sera peut être pas exactement orienté comme vous le souhaitez.  
Vous allez pour cela pouvoir incrémenter ou décrémenter la position neutre de vos servo-moteurs afin de le placer dans la position souhaitée.

1. Avant le montage, positionner vos servo-moteurs **sur la position neutre** (90° entre [0;180]) à partir d'un petit script Arduino (disponible sur internet)  

2. Effectuer le montage de votre robot en plaçant chaque palonnier en position médiane

3. Paramétrer votre fichier de squelette JSON comme ci-dessous pour chaque servo-moteur puis lancer ***Choreograph***:  

    - "offset" : 0
    - "default_position": 90  

    <img alt="json_init.trim" width="50%" src="./img_doc1_pos_init.png" />  

4. Charger le firmware dans votre carte contrôleur [=> firmware](../firmware/desc_firmware_fr.md)

5. Pour chaque servo-moteurs, affiner la position avec les flèches haut/bas de chaque servo-moteur
    <img alt="change_position.trim" width="50%" src="./img_doc2_pos_revised.png" />

6. Lancer le recalcule du décalage  

    <div align="center"><img alt="recalculate.menu" width="29%" src="./img_doc3_menu_recalculate.png" />&nbsp;<img alt="recalculed.screen" width="70%" src="./img_doc4_win_recalculate.png" /></div>  

7. Mettre à jour votre fichier JSON en modifiant le paramètre "offset" de vos servo-moteurs avec la valeur indiquée dans le recalcule  

    ```json
    "YL":
        {
         ...
         "offset" : 6,
         "angle_limit": [0, 180],
         "default_position": 90,
         ...
        }
    ```

8. Recharger votre fichier de squelette par le menu Squelette-> MAJ

    <img alt="updated.trim" width="50%" src="./img_doc5_updated.png" />

---
[<= Retour](../../README_fr.md#desc-trim)
