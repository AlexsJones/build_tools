##build tools
===========

Python based dynamic service loading build system

For use in CI build steps to do actual complex tasks that CI usually wont do (Or do badly)

###Usage


####teamcity service

```
./build_tools.py --service teamcity --teamcity_server 10.188.108.40 --teamcity_port 80 --teamcity_user admin --teamcity_password admin --teamcity_command trigger --teamcity_command_arg ExampleProject_DemoBuild
```

####shell service
```
./build_tools.py --service shell --optargs echo "Hello World!"
```
