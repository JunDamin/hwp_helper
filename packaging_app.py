import subprocess

# Define the PowerShell command as a string
command = 'pip show customtkinter'

# Run the command using subprocess
result = subprocess.run(["powershell", "-Command", command], capture_output=True)

# The output is returned as bytes, so it needs to be decoded
info = {}
for line in result.stdout.decode('utf-8').splitlines():
    key, value = line.split(": ")
    info[key] = value

info["Location"]
ctk_path = info["Location"].replace("\\", "/")
command = f'pyinstaller --noconfirm --onefile --windowed --add-data "{ctk_path}/customtkinter;customtkinter" --add-data "src;src" --icon=src/ai.ico main.py'

print(command)
result = subprocess.run(["powershell", "-Command", command], capture_output=True)

print(result.stdout.decode('utf-8'))