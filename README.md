# Battleship
One player version of battleship that allows the user to play against an AI. In this version, it is announced when a ship is destroyed, the board size is configurable, and the number and size of the ships is variable.

Gameplay:
1. Each turn either the player or the AI selects a location to fire upon
  - if the location does not contain the opposing ship a miss is announced
    - misses are marked with O
  - if the location does contain an opposing ship a hit is announced unless that is the last hit on the ship and then it is announced that you destroyed that ship
    - hits are marked with X
2. The player and the AI alternate taking turns until one of them has destroyed all of their opponents ships
3. the player will input thir choice as a row column pair on one line separated by a space.
