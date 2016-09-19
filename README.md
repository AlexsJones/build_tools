##build tools
===========

Python based dynamic service loading build system

For use in CI build steps to do actual complex tasks that CI usually wont do (Or do badly)

###Usage

```
./build_service.py --service shell --optargs echo "Hello World!"
./build_service.py --service build --build_number 09130 --create_chain true
```
