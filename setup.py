from cx_Freeze import setup,Executable
setup(name="My game",
         version="1.0",
         options={"build_exe":{"packages":["pygame"],"include_files":["archer.png","dragonblue.png"]}},
         description="My game!",
         executables=[Executable("Dragonborn.py")])
