import argparse
import pickle

from gamesrc.episode import run_episode
from gamesrc.render import init_display, make_step_callback

MODEL_BY_MODE = {
    "legacy": "best_model.pickle",
    "raycast": "best_model_raycast.pickle",
}

PLAY_FPS = 17


def parse_args():
    parser = argparse.ArgumentParser(description="Watch a trained network play snake.")
    parser.add_argument("--model", default=None,
                         help="Overrides the model file resolved from --input-mode.")
    parser.add_argument("--input-mode", choices=["legacy", "raycast"], default="legacy",
                         help="Must match the mode the model was trained with.")
    return parser.parse_args()


def main():
    """This function runs the game with the given trained network in control."""
    args = parse_args()
    model_path = args.model or MODEL_BY_MODE[args.input_mode]

    with open(model_path, "rb") as model_file:
        net = pickle.load(model_file)

    display = init_display()
    on_step = make_step_callback(display, PLAY_FPS)
    run_episode(net, input_mode=args.input_mode, on_step=on_step)


if __name__ == "__main__":
    main()
