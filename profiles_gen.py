with open('profiles', 'r', encoding='utf-8') as file:
    string = file.read()

profiles_module = '# Warning! This file is auto generated\nIMG = %s\n'
with open('profiles.py', 'w', encoding='utf-8') as file:
    file.write(profiles_module % [x.lower() for x in string.split('\n')])
