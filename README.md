# CS440-A1

## Instruction for Running Program:
The program uses the pygame Python module for the interface. 
Please run `pip install pygame` before trying to test the code.
The main file that is used to run the program is Grid.py. 

It is configured to accept 2 command line arguments. First is ‘astar’ or ‘thetastar’ which is used to determine which algorithm will be executed. 

The second argument (optional) is the name of the text file that contains the instructions for the grid size and structure. 
If no name for text file is given, a 100x50 grid with randomly picked 10% of the cells are set to be blocked is used.

Example 1: no text file and you want to run A*
	`python Grid.py astar`
Example 2: text file called test.txt and you want to run theta*
	`python Grid.py thetastar test.txt`

Note that if you use a text file with the program, you will have to terminate the process on the terminal to exit
Press ctrl-c to terminate the program.
