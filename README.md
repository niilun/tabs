![TABS (logo font is Null)](img/logo.20.png)

**TABS** is a simulation game, where you pit various units against eachother to fight! It's highly customizable, allowing anyone to add their own units and abilities which interact easily with the game.

## Getting started

1. Clone this repository ```git clone https://github.com/Leowondeh/tabs.git```.

2. Run main.py with Python ```py```/```python3```/```python``` ```main.py```.

## Modding

For a new unit to be considered valid, it needs only **3 things**:

1. It should be a class and imported to ```unit_management.py``` with an elif statement under ```create_unit()```, it's name (as defined in the class) added to ```unit_list``` and era added to ```eras_list```.

2. It should have ```current_health```, ```max_health```, ```armor``` and ```attack_damage``` attributes.

3. It should define a ```take_turn```  method, which defines what that unit does on it's turn. This is called on that unit's turn.

Functions described as ```Internal function``` are generally not to be modified if all you need is a new unit.

**For more info on modding, check the code documentation.**

## To-do list

- [ ] UI overhaul
- [ ] More units

## License

This software is licensed under the [MIT License](https://en.wikipedia.org/wiki/MIT_License).
