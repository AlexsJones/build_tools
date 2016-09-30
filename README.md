![buildIcon](/res/hammer.png)
##build tools
===========

Python based dynamic service loading build system

For use in CI build steps to do actual complex tasks that CI usually wont do (Or do badly)

| Service | Purpose |
|---------|-------------------------------------|
| Teamcity| Start remote builds & download logs |
| Jenkins | Start remote builds & download logs |
| Version | Increment version number files      |
| Shell   | Runs shell commands                 |


###Usage


####teamcity service

Build triggering: Useful when you need to kick off a non-directly chained build in a command step
```
./build_tools.py --service teamcity --teamcity_server 10.188.108.40 --teamcity_port 80 --teamcity_user admin --teamcity_password admin --teamcity_command trigger --teamcity_build_id ExampleProject_DemoBuild
```

####shell service

Shell commands on the agent
```
./build_tools.py --service shell --shell_command echo  --shell_command_args "Hello World!"
```

####version service

Lets you increment a version file (creates one if it doesnt exist)

```
./build_tools.py --service version --version_increment VERSION
```
####Example of CI integration

![ciintegration](/res/ci_integration.png)
