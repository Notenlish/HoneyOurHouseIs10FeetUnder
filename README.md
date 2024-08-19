# HoneyOurHouseIs10FeetUnder

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

add some guy named jim and his wife
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

Do scrollbar for camera

implement the spawning effect for spawning blocks(size starts small, then goes a bit overflow(size_mul is bigger than 1) then size_mul becomes 1)
move block spawning logic to cards
add apartments to cards
add apartment spawning, score
make some fx
sfx?
main menu & dialog(if possible)

# performance

test on family laptop
If possible let objects fall asleep with Space.sleep_time_threshold.
Tweak the Space.iterations property.
