# Girls Front Line AVG

Parse GFL avg to Ren'Py Script format

## How to use

1. Clone repository
2. Extract latest gfl avg text from gamedata or just use current avg resources
3. Create a renpy project
4. Refer to `tool/config.example.py`, save your config to `tool/config.py`
5. Run `avg_parser.py`, renpy script(*.rpy) will save to rpy folder
6. You can copy rpy files to renpy manually or use powershell script `deploy.ps1`, require powershell-7
7. Launch your renpy project

> renpy will load script.rpy first, then auto generated script.rpy will call other rpy script

## Parse Flow

`GameData` -> `x-x-x.bytes` -> `s_x_x_x.rpy` -> `Ren'Py`

### Unpacked text

`avgtxt_main`

### **Parser**

`avg_parser.py`

## Requirements

[cvtool](https://github.com/qzlin/cvtool)

## Ren'Py

[Ren'Py](https://renpy.org/)