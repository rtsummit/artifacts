pyinstaller -F -n csv2tableloader main.py

copy /Y .\dist\csv2tableloader.exe ..\..\bin
copy /Y .\dist\csv2tableloader.exe "..\..\..\Client\Assets\Standard Assets\Game\Script\generated"

copy /Y .\template\*.* ..\..\bin\template
copy /Y .\template\*.* "..\..\..\Client\Assets\Standard Assets\Game\Script\generated\template"
