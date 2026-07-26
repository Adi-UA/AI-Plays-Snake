# AI Plays Snake

[![CI](https://github.com/Adi-UA/AI-Plays-Snake/actions/workflows/ci.yml/badge.svg)](https://github.com/Adi-UA/AI-Plays-Snake/actions/workflows/ci.yml)

<table>
  <tr>
    <th>Legacy (binary adjacency)</th>
    <th>Raycast (NERO-style sensors)</th>
  </tr>
  <tr>
    <td><video src="https://github.com/Adi-UA/AI-Plays-Snake/raw/master/assets/legacy-demo.mp4" controls muted loop width="380"></video></td>
    <td><video src="https://github.com/Adi-UA/AI-Plays-Snake/raw/master/assets/raycast-demo.mp4" controls muted loop width="380"></video></td>
  </tr>
</table>

This project uses [`NEAT`](https://neat-python.readthedocs.io/en/latest/neat_overview.html) and [`Pygame`](https://www.pygame.org/news) to create a variation of Snake and beat it using NEAT's neural networks.

I wanted to see if the classic game Snake could be beaten with NEAT and didn't find any examples, so I made one myself. Two input encodings are available (pick with `--input-mode`): the original "legacy" mode uses binary values for whether the 8 blocks adjacent to the snake's head are free, plus 3 values for whether to go ahead, left, or right based on the food's relative position; the newer "raycast" mode replaces this with 16 continuous distance-sensor values, described below.

# The Game

For context, it is good to understand what the game is so you understand what the neural network is trying to do.

In Snake, at each game tick you can choose to make the snake turn left or turn right. If you choose neither, the snake will continue moving forward until you either issue a command or it fails after hitting a wall or itself.

The objective of turning is to guide the snake towards food blocks for it to eat while making sure the snake doesn't crash into the wall or itself. If you successfully get the snake to consume a block of food, it will grow a little (makes the game harder) and you will get a point.

There is no endpoint for my variation of the game and the objective is simply to survive for as long as possible while eating food.

For a touch of fanciness, in my version of the game the food changes color and eating the food changes the color of the snake to the food's color.

If you're not interested in the AI stuff and just want to play the game, run `snake_game.py` with the arrow keys.

## Layout

```
gamesrc/
  constants.py  - grid size and window dimensions, no pygame dependency
  grid.py       - the 30x30 occupancy grid
  snake.py      - snake state: position, orientation, movement
  food.py       - food state
  decision.py   - builds the network's input vector (legacy or raycast mode)
  sensors.py    - the raycast distance-sensor math
  rules.py      - pure win/fail condition checks
  episode.py    - runs one full game episode headlessly, used by both
                  training and inference
  render.py     - the only pygame-dependent module; draws a game to screen
resources/
  config-feedforward.txt          - NEAT config for legacy mode (11 inputs)
  config-feedforward-raycast.txt  - NEAT config for raycast mode (16 inputs)
tests/          - pytest suite for everything under gamesrc/, no display
                  or pygame dependency
trainAI.py      - entrypoint: train a network       (python trainAI.py)
testAI.py       - entrypoint: watch a trained model  (python testAI.py)
snake_game.py   - entrypoint: play it yourself        (python snake_game.py)
```

The core design principle is that `episode.py` has zero pygame dependency, so training can run headless across multiple CPU cores; `render.py` is the only place pygame is imported and used, and only entry points that actually want visuals (`snake_game.py`, `testAI.py`, or `trainAI.py --render`) create a window.

# Setup

Assuming you have pip, git, and Python 3.10+:

```
git clone https://github.com/Adi-UA/AI-Plays-Snake.git
cd AI-Plays-Snake
python -m venv venv
```

macOS/Linux:
```
source venv/bin/activate
```

Windows (PowerShell):
```
venv\Scripts\Activate.ps1
```

Then, on either machine:
```
pip install -r requirements.txt
```

For running the tests and linter too:
```
pip install -r requirements-dev.txt
```

# Running

## Training

If you don't want to use the trained models that come with this repository (`best_model.pickle` for legacy mode, `best_model_raycast.pickle` for raycast mode), run `trainAI.py`. By default it trains for 50 generations with a population of 1000, evaluating the population in parallel across your CPU cores.

```
python trainAI.py
```

Useful flags:

| Flag | Default | Description |
|---|---|---|
| `--generations` | 50 | Number of generations to run |
| `--pop-size` | (from config) | Overrides the config file's population size |
| `--workers` | all CPU cores | Worker processes for parallel evaluation |
| `--render` | off | Watch training in a single process instead of running headless in parallel |
| `--input-mode` | `legacy` | `legacy` or `raycast`, see below |
| `--seed` | none | Base seed for reproducible runs |
| `--checkpoint-dir` | `checkpoints` | Where to write periodic checkpoints |
| `--checkpoint-every` | 10 | Generations between checkpoints |
| `--resume` | none | Resume from a checkpoint file |
| `--config` | (resolved from `--input-mode`) | Override the NEAT config file path |

Training can take a while. To watch it happen instead of running headless:

```
python trainAI.py --render --workers 1
```

## Testing

To see a trained AI controlling the snake:

```
python testAI.py --input-mode legacy    # or --input-mode raycast
```

## Playing it yourself

```
python snake_game.py
```

Use the arrow keys to turn; the snake keeps going straight otherwise.

# Input modes

**Legacy** (default, `resources/config-feedforward.txt`, 11 inputs): 8 binary values for whether each of the 8 cells adjacent to the head is free, plus 3 binary values for whether the food is ahead, to the left, or to the right.

**Raycast** (`resources/config-feedforward-raycast.txt`, 16 inputs): 8 directional distance sensors to the nearest obstacle (wall or own body) and 8 directional distance sensors to food, one pair per 45-degree direction around the snake's head. This follows the sensor design used for NEAT-controlled game agents in Stanley, K.O., Bryant, B.D., & Miikkulainen, R. (2005), ["Real-Time Neuroevolution in the NERO Video Game"](https://ieeexplore.ieee.org/document/1545941), *IEEE Transactions on Evolutionary Computation*, 9(6), 653-668, which uses continuous, normalized distance sensors instead of raw occupancy.

The two modes use separate config files (input counts differ) and separate model files, so training one never overwrites the other.

# Modifying Neural Net Parameters

If you want to experiment with your own NEAT parameters, the config files are in the `resources` directory: `config-feedforward.txt` for legacy mode, `config-feedforward-raycast.txt` for raycast mode. You can change any of the parameters in these files and see how that affects model training and accuracy; just keep `num_inputs` matching whichever mode you're using.

The code in `trainAI.py` and `gamesrc/episode.py` is documented where the logic isn't self-explanatory, so if you're familiar with NEAT it should be straightforward to follow where genome fitness is being incremented and decremented.
