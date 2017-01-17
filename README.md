```
.______    __    __   __   __       _______
|   _  \  |  |  |  | |  | |  |     |       \
|  |_)  | |  |  |  | |  | |  |     |  .--.  |
|   _  <  |  |  |  | |  | |  |     |  |  |  |
|  |_)  | |  `--'  | |  | |  `----.|  '--'  |
|______/   \______/  |__| |_______||_______/

.___________.  ______     ______    __          _______.
|           | /  __  \   /  __  \  |  |        /       |
`---|  |----`|  |  |  | |  |  |  | |  |       |   (----`
    |  |     |  |  |  | |  |  |  | |  |        \   \
    |  |     |  `--'  | |  `--'  | |  `----.----)   |
    |__|      \______/   \______/  |_______|_______/
```  

[![Build Status](https://travis-ci.org/AlexsJones/build_tools.svg?branch=master)](https://travis-ci.org/AlexsJones/build_tools)

##build tools
===========

Python based dynamic service loading build system

For use in CI build steps to do actual complex tasks that CI usually wont do (Or do badly)

| Service | Purpose |
|---------|-----------------------------------------------|
| Teamcity| Start remote builds & download logs           |
| Jenkins | Start remote builds & download logs           |
| Build   | Increment build  number files                 |
| Shell   | Runs shell commands                           |
| Nexus   | Create, Delete, Download nexus repo artefacts |
| Gitlab  | Start remote build & download logs            |
---
###Version

Python 3.5

###Usage

For help please see module arguments with 

```
source env/bin/activate
install -r requirements
python ./build_tools.py [module_name] --help

```

###Requirements
```
libffi 
nmap
```
