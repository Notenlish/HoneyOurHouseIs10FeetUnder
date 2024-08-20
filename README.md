# HoneyOurHouseIs10FeetUnder
source code for: https://notenlish.itch.io/honey-our-house-is-10-feet-deep
gmtk 2024 entry
## run instructions:

Install Python 3.11/3.12

https://www.python.org/downloads/release/python-3119/ and choose add to path in py installer 

Open up cmd prompt, type:

pip install pygame-ce 

And 

pip install pymunk

pip install numpy

then do:

py main.py

## Game idea

highscore based game
you need to build an apartment that needs to house increasingly more amount of people
and you need it to be able to resist earthquakes/wind etc.

The game randomly gives blocks to you and you must expand

Blocks:
steel
wood
plastic
rope

Wood Square
Wood long Rect
Plastic Circle
Steel Frame
Rope

Some guy named Jimmy and his wife
They live in the apartment, and they just come
and after every tour, they come and have some small talk or something

Also add people as entities in the game
like they have special sprites etc.

Man, Child(male or female), Woman, Cat, Dog, Hamster, Bird, fish in a bowl

İf they die they say "oof" sound(custom made)

for every alive people you get one more extra card

# Particles

dust fx for when buildings collapse. maybe some fire as well

oh wait what if there was chaos happening. like children crying and whatnot. meh idk

either I make a goofy game with 'bla bla' as dialog with building
or make a goofy game where theres chaos every time you mess something up

https://www.youtube.com/watch?v=QUpUWL7xw5g
https://discord.com/channels/772505616680878080/822265298085347368/1274696375841460234
https://discord.com/channels/772505616680878080/772507247540437032/1142477416158220358

use pygame_ecs :eyes: ?

https://discord.com/channels/554137097229959188/772557289416163329/1274803091258212363
https://discord.com/channels/554137097229959188/772557289416163329/1274798148585390235

amsaa's particle system code: https://discord.com/channels/554137097229959188/772557289416163329/1274797886856757340

# todo

add apartments to cards
add apartment spawning, score
make some fx
sfx?
main menu & dialog(if possible)
windows build(with pyinstaller and exe to msi) also warn people to disable their windows defender before running
add requirements.txt
steps on how to run the source code
link to the source code in itch.io description

camera moving to keep up with the building height

# performance

test on family laptop
If possible let objects fall asleep with Space.sleep_time_threshold.
Tweak the Space.iterations property.


wood
metal
ice
plastic

maybe add ropes???

# credits
Building crumble Sound Effect by <a href="https://pixabay.com/users/floraphonic-38928062/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=185114">floraphonic</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=185114">Pixabay</a>

Ice sound effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=33654">Pixabay</a>

Metal Sound Effect by <a href="https://pixabay.com/users/floraphonic-38928062/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=202176">floraphonic</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=202176">Pixabay</a>
and <a href="https://pixabay.com/users/ribhavagrawal-39286533/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=230501">Ribhav Agrawal</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=230501">Pixabay</a>
and <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=6765">Pixabay</a>
