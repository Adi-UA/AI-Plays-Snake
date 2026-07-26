import argparse
import functools
import os
import pickle

import neat

from gamesrc.episode import WIN_SCORE, run_episode
from gamesrc.render import init_display, make_step_callback

CONFIG_BY_MODE = {
    "legacy": os.path.join("resources", "config-feedforward.txt"),
    "raycast": os.path.join("resources", "config-feedforward-raycast.txt"),
}

MODEL_BY_MODE = {
    "legacy": "best_model.pickle",
    "raycast": "best_model_raycast.pickle",
}

RENDER_FPS = 1000  # matches the original "zooming" training visuals


def eval_genome(genome, config, input_mode, on_step=None):
    """
    Evaluates a single genome and returns its fitness. Once a genome plays
    well enough to reach `episode.WIN_SCORE`, its network is saved to the
    model file for this input mode.

    Arguments:
        genome -- The genome to evaluate.
        config -- The NEAT config the genome was created under.
        input_mode {str} -- "legacy" or "raycast".
        on_step -- Optional render callback. Only used in single-process
        `--render` mode; never passed under `ParallelEvaluator`.

    Returns:
        float -- The genome's fitness.
    """
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    result = run_episode(net, input_mode=input_mode, on_step=on_step)

    if result["score"] >= WIN_SCORE:
        with open(MODEL_BY_MODE[input_mode], "wb") as model_file:
            pickle.dump(net, model_file)

    return result["fitness"]


def eval_genomes_with_render(genomes, config, input_mode, on_step):
    """
    Sequential fitness function used only for `--render`, since a shared
    pygame display can only be drawn to from a single process.
    """
    for _, genome in genomes:
        genome.fitness = eval_genome(genome, config, input_mode, on_step)


def build_config(args):
    config_path = args.config or CONFIG_BY_MODE[args.input_mode]
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    if args.pop_size is not None:
        config.pop_size = args.pop_size
    return config


def build_population(args, config):
    if args.resume:
        return neat.Checkpointer.restore_checkpoint(args.resume, new_config=config)
    return neat.Population(config, seed=args.seed)


def run(args):
    config = build_config(args)
    population = build_population(args, config)

    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    os.makedirs(args.checkpoint_dir, exist_ok=True)
    population.add_reporter(neat.Checkpointer(
        generation_interval=args.checkpoint_every,
        filename_prefix=os.path.join(args.checkpoint_dir, "neat-checkpoint-"),
    ))

    try:
        if args.render:
            display = init_display()
            on_step = make_step_callback(display, RENDER_FPS)
            fitness_function = functools.partial(
                eval_genomes_with_render, input_mode=args.input_mode, on_step=on_step,
            )
            population.run(fitness_function, args.generations)
        else:
            evaluator = neat.ParallelEvaluator(
                args.workers,
                functools.partial(eval_genome, input_mode=args.input_mode),
                seed=args.seed,
            )
            population.run(evaluator.evaluate, args.generations)
    finally:
        # Save whatever the best genome is so far, even if training raises
        # partway through (e.g. a crash during reproduction) -- otherwise a
        # failure this late would lose everything the run had achieved.
        save_best_genome(population, config, args.input_mode)


def save_best_genome(population, config, input_mode):
    """
    Saves the best genome seen across the whole run. `eval_genome` already
    saves a genome as soon as it reaches WIN_SCORE mid-training, but a run
    that never crosses that bar would otherwise end with nothing on disk.
    """
    if population.best_genome is None:
        return
    net = neat.nn.FeedForwardNetwork.create(population.best_genome, config)
    with open(MODEL_BY_MODE[input_mode], "wb") as model_file:
        pickle.dump(net, model_file)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train a NEAT-evolved snake-playing network.")
    parser.add_argument("--generations", type=int, default=150)
    parser.add_argument("--pop-size", type=int, default=None,
                         help="Overrides pop_size in the config file.")
    parser.add_argument("--workers", type=int, default=os.cpu_count(),
                         help="Worker processes for parallel evaluation. Ignored with --render.")
    parser.add_argument("--render", action="store_true",
                         help="Watch training in a single process instead of running headless "
                              "in parallel.")
    parser.add_argument("--input-mode", choices=["legacy", "raycast"], default="legacy")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--checkpoint-dir", default="checkpoints")
    parser.add_argument("--checkpoint-every", type=int, default=10)
    parser.add_argument("--resume", default=None,
                         help="Path to a checkpoint file to resume training from.")
    parser.add_argument("--config", default=None,
                         help="Overrides the config file resolved from --input-mode.")
    return parser.parse_args()


def main():
    args = parse_args()
    run(args)


if __name__ == "__main__":
    main()
