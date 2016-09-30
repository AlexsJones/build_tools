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

---
###Usage

Most services are fairly self explantory from running `--describe SERVICE` or `--help` to see all options. 
But here are some examples of service use:

Starting a teamcity build.
```
./build_tools.py --service teamcity --teamcity_server 10.188.108.40 --teamcity_port 80 --teamcity_user admin --teamcity_password admin --teamcity_command trigger --teamcity_build_id ExampleProject_DemoBuild
```

Shell commands on the agent.
```
./build_tools.py --service shell --shell_command echo  --shell_command_args "Hello World!"
```
Increment a version number
```
./build_tools.py --service version --version_increment VERSION
```

---
####Example of CI integration

![ciintegration](/res/ci_integration.png)
