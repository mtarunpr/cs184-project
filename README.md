# CS 184 Final Project: RL for Coq

## Setup

```bash
pip install -r requirements.txt
```

## Usage

To train a model on the Coq files listed in `src/data/parser.py`:

```bash
python src/reinforce.py [args]
```

Alternatively, use one of the pre-trained models in `models`. To test a model (also on the same Coq files; feel free to modify as necessary):

```bash
python src/test.py --model "path/to/model.pkl" [args]
```

In both training and testing, setting the `--render` flag displays every attempted proof step during the search process along with corresponding rewards.
