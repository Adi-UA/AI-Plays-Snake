# Overview
This project uses [`NEAT`](https://neat-python.readthedocs.io/en/latest/neat_overview.html) and [`Pygame`](https://www.pygame.org/news) to create a variation of Snake and beat it using NEAT's Neural Networks. 

I wanted to see if the classic game Snake could be beaten with NEAT and didn't find any examples, so I made one myself! My model uses "shortsighted" decision-making to figure out where to go next. The inputs include binary values to indicate if the 8 blocks adjacent to the snake's head are free or not as well as values to indicate wheter the snake should go ahead, left or right based on the food's relative position. The number of adjacent blocks given as input can be increased or decreased but 8 felt like the sweet spot between short training times and a consistent model. 

# The Game
For context, it is good to understand what the game is so you understand what the neural network is trying to do. 

In Snake, at each game tick you can choose to make the snake turn left or turn right. If you choose neither, the snake will continue moving forward until you either issue a command or it fails after hitting a wall/itself.

The objective of turning, is to guide the snake towards food blocks for it to eat while making sure the snake doesn't crash into the wall or itself. If you successfully get the snake to consume a block of food, it will grow a little (makes the game harder) and you will get a point. 

There is no endpoint for my variation of the game and the objective is simply to survive for as long as possible while eating food.

For a touch of fanciness, in my version of the game the food changes colour and eating the food changes the colour of the snake to the food's color.

If you're not intersted in the AI stuff and just want to play the game, then (assuming you've cloned the repo) you can simply run `snake_game.py`

All the modules used to create the game can be found in `gamesrc`

# Using
### Before Running (Assuming you have pip, git and an appropriate version of python)

* If you're not worried about breaking anything in your environment:
    
    * Run `pip install -r requirements.txt`

* Otherwise, if you're trying to install the dependencies individually:
    * Run `pip install pygame`
    * Run `pip install neat-python`
    * Run `pip install numpy`

Then, clone the repo with: `git clone https://github.com/Adi-UA/AI-Plays-Snake.git`.

**Note:** I am using `python 3.7.x`, `pygame 1.9.6`, `neat-python 0.92`, `numpy 1.19.0`.

## Running
### Training (Optional)
If you don't want to use the trained model that comes with this repository in `best_model.pickle`, simply run the `trainAI.py` module. Running the module will train the model for upto 50 generations with a population size of 1000 in each generation; when it finds a satisfactory model, it will store it inside `best_model.pickle`.

Training can take a while! I got a great model in around 34 generation (roughly 2.5 hours) but your mileage may vary based on initial conditions. It is, however, pretty rewarding to see a snake zooming and changing colors at 1000fps.

### Testing
When you're ready to see a trained AI controlling the snake, simply run the `testAI.py` module. Running the module will fire up a game of Snake in which the snake is controlled by the neural net stored in `best_model.pickle`. See how far it gets!

## Modifying Neural Net Parameters
Chances are you don't just want to train the AI on my category values and are looking to spice things up with some of your own. In that case, I will assume you are at least somewhat familiar with `NEAT`, so I won't explain in detail below.

### Modify the config file for the NN
The config file can be found in the `resources` directory as `config-feedforward.txt`
You can change any or all of the parameters in this file and see how that affects model training and accuracy.

### Modify the code in trainAI.py
I've documented each step of the code fairly well, so if you're familiar with `NEAT` it should be easy to follow the code and figure out where genome fitness values are being incremented and decremented.
