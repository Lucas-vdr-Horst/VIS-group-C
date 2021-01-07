# VIS-group-C
__Vialis Intersection Simulation__

## Setup

### Dataset
Create in `intersections/` a foler for each intersection with the name of the intersection,  
All files relevant of the intersection should be in that folder.  
For example: 
```
intersections
├── Original
│   ├── BOS211.csv
│   └── BOS210.csv
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
Run `app.py`