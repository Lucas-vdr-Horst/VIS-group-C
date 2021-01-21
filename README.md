# VIS-group-C
__Vialis Intersection Simulation__ 

![](https://www.vrsrail.nl/dynamics/modules/SFIL0200/view.php?fil_Id=5534&thumb_nr=108)


## Setup

### Dataset
Create in `intersections/` a folder for each intersection with the name of the intersection,  
All files relevant of the intersection should be in that folder.  
For example: 
```
intersections
├── BOS210
│   ├── 79190154_BOS210_ITF_COMPLETE.xml
│   └── new_BOS210.csv
└── BOS211
    ├── 7919015E_BOS211_ITF_COMPLETE.xml
    └── new_BOS211.csv
```

### Dependencies
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

On the first time (or when something has changed), the options should be run in order:
1. Preprocess
2. Process simulation
3. Start webserver

The next time(s) you can just
- Start webserver