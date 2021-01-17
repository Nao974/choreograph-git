# file: project

This file is used to load all the configuration files at once.

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

- **description**: used to describe the project
- **filepath**: base path of the project from the Choregraph application
- **view**: path / name of the image.jpg, robot image in jpeg format
- **skeleton**: skeleton description file in json format
- **position**: sub folder from the project folder *filepath* containing the positions in json format
- **movement**: sub-folder from the project folder *filepath* containing the movements in json format
- **controller**: path + description file of the controller in json format

---

[=> All file formats](../file_format.md)

---

[<= Return](../../README.md#file-format)
