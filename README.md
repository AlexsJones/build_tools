![buildIcon](http://i.imgur.com/xzrllfC.png)
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
###Usage

For help please see module arguments with 

```
./build_tools.py [module_name] --help

```

