![TABS (TABS logo, font is Null)](img/logo.20.png)

**TABS** is a simulation game, where you pit various units against eachother to fight! It's highly customizable, allowing anyone to add their own units and abilities which interact easily with the game.

## Getting started

1. **Clone** this repository ```git clone https://github.com/Leowondeh/tabs.git``` or download it.

2. Enter the **TABS root folder** and run TABS with Python ```py```/```python3```/```python``` ```main.py```.

## Adding your own units

You need just a *couple* things to create a working, shiny new unit:

1. To be considered valid, a unit needs to have ```current_health```, ```max_health```, ```armor``` and ```attack_damage``` in it's ```__init__``` method. 

> **Note**: A unit does not necessarily have to interact with it's ```armor``` or ```max_health``` value (though other units may), but the variable **needs** to exist for unit combat to take place correctly, even if it's at 0.

2. If the unit is in a different file, make sure to import it in ```unit_management.py```.

3. Add a new ```elif``` statement with the unit's user-friendly name and instantiate that unit to the ```created_unit``` variable.

> **Note**: Functions described as ```Internal function``` are generally not to be modified if all you need is a new unit.

**For more info on modding, check the code documentation.**

## Extra info / Acknowledgments

The logo was made using the [Null](https://www.fontfabric.com/fonts/null/#font-styles) font (Made by Svetoslav Simov), adding a 15px outline to the glyphs.

## To-do list

- [ ] UI overhaul
- [ ] More units

## License

This software is licensed under the [MIT License](https://en.wikipedia.org/wiki/MIT_License).