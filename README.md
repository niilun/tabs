![TABS (TABS logo, font is Null)](img/logo.20.png)

**TABS** is a simulation game, where you pit various units against eachother to fight! It's highly customizable, allowing anyone to add their own units and abilities which interact easily with the game.

## Getting started

1. **Clone** this repository ```git clone https://github.com/Leowondeh/tabs.git``` or download it as ZIP.

2. Enter the **TABS root folder** and run TABS with Python ```py```/```python3```/```python``` ```main.py```.

## Adding your own units

You need just a *couple* things to create a working, shiny new unit:

1. To be considered valid, a unit needs to have ```current_health```, ```max_health```, ```armor``` and ```attack_damage``` in it's ```__init__``` method. 

> **Note**: The ```armor``` and ```max_health``` values are optional to use. Also, units can have ```attributes``` like *cavalry* or *melee* that other units can check against for special effects (stuff like anti-cavalry dealing more damage)

2. Check if the unit is imported to ```unit_management.py```.

3. Add the unit's user-friendly name to ```all_units_map```.

**For more info on modding, check the code documentation.**

## Building an executable

You can package up the code into **executable form** using ```pyinstaller```.

1. If you don't have them installed already, run ```pip install -r requirements.txt``` to install all requirements.

2. Run the build scripts from ```build_scripts/```. Use ```build.sh``` on Linux or ```build.bat``` on Windows. 

## Extra info / Acknowledgments

Logo was made using the [Null](https://www.fontfabric.com/fonts/null/#font-styles) font (Made by Svetoslav Simov).

## To-do list

- [ ] UI overhaul
- [ ] More units
- [ ] More interactions between units
- [ ] More types of fights

## License

This software is licensed under the [MIT License](https://en.wikipedia.org/wiki/MIT_License).