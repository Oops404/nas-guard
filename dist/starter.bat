if "%1"=="hide" goto CmdBegin
start mshta vbscript:createobject("wscript.shell").run("""%~0"" hide",0)(window.close)&&exit
:CmdBegin
nas-guard-py3.exe -r 192.168.199.1 -p 80 -t 3 -a 1 > log.txt