# VIS-group-C
__Vialis Intersection Simulation__ 

![](https://www.vrsrail.nl/dynamics/modules/SFIL0200/view.php?fil_Id=5534&thumb_nr=108)


## Setup

### Dataset
Create in `intersections/` a folder for each intersection with the name of the intersection,  
All files relevant of the intersection should be in that folder.
Create a folder 'extern_data' where the external dataset will be placed.
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
    * You will have 3 options. We will recommend chosing 4 for the first time:
         * Compress csv
         * Process extern data
         * Process spawn points
         * All of the aboven
2. Process simulation
    * Insert desired timeframe in miliseconds
3. Start webserver

The next time(s) you can just
- Start webserver
