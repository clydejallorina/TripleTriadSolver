# TripleTriadSolver

This repository is a hobby project to create a solver for [Triple Triad](https://ffxiv.consolegameswiki.com/wiki/Triple_Triad) in Final Fantasy XIV.

Currently, the project is only built to solve the Open ruleset with no additional modifiers. This means that the game gives out perfect information for both sides, and that both sides would have all the information required to create the best moves.

The solver works through [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) the game tree and attempts to calculate the best move for Player 1. The solver assumes that Player 1 is always the user of the program.

As for the game implementation, the card parser assumes that the data is received from [Raelys's Triple Triad Tracker API](https://triad.raelys.com/). This repository will NOT come with their data, and the user must download the card data themselves using their API.

Yes, I do hate myself for putting as much effort into this as I have.

---

### Requirements

This project requires [Pillow](https://pillow.readthedocs.io/en/stable/index.html) to draw the board. The appropriate `requirements.txt` file has been provided in this repository for the install.

---

### To-Do

As it is, this repository is very barebones and can barely solve the game in some depths. Calculating the best first move is still a massive struggle for the system as it tries to build the full game tree from scratch. This needs to be optimized, but I'm not particularly sure how.
