@ECHO OFF
copy python-3.9.12-amd64.exe C:\Users\Administrator\Downloads
CD /D "C:\Users\Administrator\Downloads"
python-3.9.12-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
CMD