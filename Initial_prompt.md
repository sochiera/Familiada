This is new project.
I would like to implement Polish version of "Family Feud" television game show. The polish version is named "Familiada".

The project should be written in python and possible to run on Ubuntu and Mac.

The game needs a json file with data input. Each json will contain question with answers and scores for a single round.

The program should be graphical (can be windowed or full screen) and only input would be using a mouse clicking on certain fields on the board.

Feature 1)
It should implement only inputs from game controller. 
Game controller will just click using a mouse on a selected area that would show actions.
The board should look like this:
1 ...................................... --
2 ...................................... --
3 ...................................... --
4 ...................................... --
5 ...................................... --
6 ...................................... --

                                 SUMA 0

Suma is polish for sum/total count.
It can be simple green on black with every letter having the same width. Use some old fasioned czcionka. 
When game controller clicks on a row, it should show anser and points
for example it click on 2 and in the json 2 was mapping to Dawid and 20.
After that, the screen should show something like this:
1 ...................................... --
2 Dawid  .......................... 20
3 ...................................... --
4 ...................................... --
5 ...................................... --
6 ...................................... --

The question (in this case "Give a nice name in Polish) is not visible to the system, only the master tells it to the players.
Players don't interact with the system, they just see the board and tell answers to game master.

Feature 2)
Another action is to click on empty field on the right or left
This would cause to create an X on that side.
There is place for 3 X on the side
For example it can look like this:
1 ...................................... --
2 Dawid  .......................... 20    X
3 ...................................... --
4 ...................................... --      X
5 ...................................... --    
6 ...................................... --      X

The same on the other side.

Feature 3)
There should be also 2 score counters - on the left bottom corner and on the right bottom corner.
When game master clicks on that counter, the current total is transferred to that counter.
Single counter means current score for one playing team.
After sum is assigned to selected team score, the round is finished and another round should start, if there are not used jsons.

Feature 4) 
Add sounds for actions. 
Use sounds from that site: https://www.myinstants.com/en/search/?name=Familiada

Right now analyze it all and ask me questions. 
If you don't have any questions, prepare memory bank or some specification or just a plan so that I can use AI tools to generate code. Do it in a way that this will be easy to implement by AI. Use good practices of working with AI for code generation.