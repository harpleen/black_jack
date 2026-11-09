# Blackjack strategy advisor

A small Python tool that tells you the basic-strategy play for a blackjack hand, keeps a Hi-Lo count as cards are seen, and adjusts the advice with count-based deviations.

| File | What it does |
| --- | --- |
| `lib/basic_strategy.py` | `BasicStrategy`: hard, soft and pair tables mapping player total and dealer up-card to hit, stand, double or split |
| `lib/counting_cards.py` | `CardCounter`: Hi-Lo running and true count, with modes for a normal shoe and a continuous-shuffle machine |
| `lib/deviations.py` | `DeviationAdvisor`: a subset of the well-known count-based deviations from basic strategy |
| `lib/play_basic_strategy.py` | A command-line advisor that asks for the visible cards and your hand and prints the play |
| `tests/` | pytest tests for the basic-strategy tables |

```sh
python3 -m pytest                       # run the tests
python3 lib/play_basic_strategy.py      # run the advisor
```
