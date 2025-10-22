class BasicStrategy:
    """Returns actions based on blackjack basic strategy."""
    def __init__(self, player_total, is_soft, dealer_upcard, is_pair=False):
        # Store the inputs
        self.player_total = int(player_total)
        self.is_soft = bool(is_soft)
        self.is_pair = bool(is_pair)
        # Normalize dealer upcard (accepts '2'-'10', 'J','Q','K','A' or ints)
        if isinstance(dealer_upcard, str):
            up = dealer_upcard.upper()
            if up in {"J", "Q", "K"}:
                self.dealer_upcard = 10
            elif up == "A":
                self.dealer_upcard = 11
            else:
                self.dealer_upcard = int(up)
        else:
            # assume int already
            self.dealer_upcard = int(dealer_upcard)
        self.actions = {'H': 'HIT', 'S': 'STAND', 'D': 'DOUBLE DOWN', 'P': 'SPLIT'}
        self.strategy_table_hard_totals = {
            # Player Total : {Dealer Upcard : Action}
            8:  {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            9:  {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            10: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'H', 11: 'H'},
            11: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'D', 11: 'H'},
            12: {2: 'H', 3: 'H', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            13: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            14: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            15: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            16: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            17: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            18: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            19: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            20: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            21: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
        }
        self.strategy_table_soft_totals = {
            # Player Total : {Dealer Upcard : Action}
            13: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            14: {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            15: {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            16: {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            17: {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            18: {2: 'S', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'S', 8: 'S', 9: 'H', 10: 'H', 11: 'H'},
            19: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            20: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            21: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
        }
        self.strategy_table_pairs = {
            # Player Pair : {Dealer Upcard : Action}
            2:  {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            3:  {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            4:  {2: 'H', 3: 'H', 4: 'H', 5: 'P', 6: 'P', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            5:  {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'H', 11: 'H'},
            6:  {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            7:  {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
            8:  {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'P', 9: 'P', 10: 'P', 11: 'P'},
            9:  {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'S', 8: 'P', 9: 'P', 10: 'S', 11: 'S'},
            10: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
            11: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'P', 9: 'P', 10: 'P', 11: 'P'},
        }

    def get_action(self):
        """
        Return the recommended action for the instance's
        (player_total, dealer_upcard, is_pair, is_soft).
        """
        if self.is_pair:
            strategy_table = self.strategy_table_pairs
        elif self.is_soft:
            strategy_table = self.strategy_table_soft_totals
        else:
            strategy_table = self.strategy_table_hard_totals

        pt = self.player_total
        du = self.dealer_upcard

        if pt in strategy_table and du in strategy_table[pt]:
            action_code = strategy_table[pt][du]
            return self.actions[action_code]
        else:
            return 'No action found for the given totals.'


from typing import Optional, List

class CardCounter:
    """Hi-Lo card counter with modes for normal shoe and CSM.

    mode: "shoe" (classic true-count) or "csm" (rolling/decaying count).
    total_decks: number of decks in shoe (default 8).
    initial_cards_seen: warm-start estimate if you join mid-shoe.
    rolling_window: window size in cards for rolling count (CSM mode).
    decay_lambda: optional exponential decay factor per card (CSM mode).
    """
    HI_LO = {
        **{str(n): 1 for n in range(2, 7)},   # 2-6 → +1
        **{str(n): 0 for n in range(7, 10)},  # 7-9 → 0
        "10": -1, "J": -1, "Q": -1, "K": -1, "A": -1,
    }

    def __init__(self, *, total_decks: int = 8, mode: str = "shoe",
                 initial_cards_seen: int = 0, initial_running_count: int = 0,
                 rolling_window: Optional[int] = None, decay_lambda: Optional[float] = None):
        self.total_decks = float(total_decks)
        self.mode = mode  # "shoe" or "csm"
        self.initial_cards_seen = int(initial_cards_seen)
        self.running_count = int(initial_running_count)
        self.cards_seen_now = 0
        # Rolling/decay state for CSM mode
        self.rolling_window = int(rolling_window) if rolling_window else None
        self.decay_lambda = float(decay_lambda) if decay_lambda else None
        self._window: List[float] = []  # store tags for last W cards (or one rolling value if decay)

    def reset(self):
        self.running_count = 0
        self.cards_seen_now = 0
        self._window.clear()

    def warm_start(self, cards_seen_estimate: int, rc_estimate: int = 0):
        """Set a mid-shoe baseline when joining part-way through a shoe."""
        self.initial_cards_seen = int(max(cards_seen_estimate, 0))
        self.running_count = int(rc_estimate)
        self.cards_seen_now = 0
        self._window.clear()

    def _norm(self, card):
        c = str(card).upper().strip()
        if c in {"J", "Q", "K"}:
            return "10"
        return c  # "2"-"10" or "A"

    def _tag(self, card):
        return self.HI_LO.get(self._norm(card), 0)

    def observe(self, card):
        """Observe a single visible card and update counts."""
        tag = self._tag(card)
        # classic RC always updates
        self.running_count += tag
        self.cards_seen_now += 1
        # Update rolling window / decay if configured (for CSM)
        if self.rolling_window:
            self._window.append(tag)
            if len(self._window) > self.rolling_window:
                self._window.pop(0)
        elif self.decay_lambda:
            # store a single rolling value in _window[0]
            if not self._window:
                self._window = [0.0]
            self._window[0] = self._window[0] * self.decay_lambda + tag

    def decks_remaining(self) -> float:
        cards_total = self.total_decks * 52.0
        remaining_cards = max(cards_total - (self.initial_cards_seen + self.cards_seen_now), 1.0)
        return remaining_cards / 52.0

    def true_count(self) -> float:
        dr = self.decks_remaining()
        return self.running_count / dr if dr > 0 else float(self.running_count)

    def rolling_true_count(self) -> float:
        if not self._window:
            return 0.0
        if self.rolling_window:
            rc_roll = sum(self._window)
            decks_equiv = max(self.rolling_window / 52.0, 0.25)
            return rc_roll / decks_equiv
        if self.decay_lambda:
            rc_roll = float(self._window[0])
            # approximate effective deck span from decay
            decks_equiv = 1.0  # simple default
            return rc_roll / decks_equiv
        return 0.0


DEVIATIONS = [
    # Example deviation tuples for illustration:
    # (player_total, is_soft, is_pair, dealer_upcard, true_count_threshold, action)
    (16, False, False, 10, 0, 'S'),
    (15, False, False, 10, 4, 'S'),
    # Add more deviations as needed...
]

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from counting_cards import CardCounter

class DeviationAdvisor:
    """Applies count-based deviations to a basic-strategy recommendation."""
    def __init__(self, counter: 'CardCounter', cautious: bool = True):
        self.counter = counter
        self.cautious = cautious

    def advise(self, basic_action: str, *, player_total: int, dealer_upcard: int,
               is_soft: bool, is_pair: bool):
        # choose which TC to use
        if getattr(self.counter, 'mode', 'shoe') == "csm":
            tc = int(round(self.counter.rolling_true_count()))
            buffer = 1 if self.cautious else 0
        else:
            tc = int(round(self.counter.true_count()))
            buffer = 0

        for (pt, soft, pair, du, thr, action) in DEVIATIONS:
            if (pt, soft, pair, du) == (player_total, is_soft, is_pair, dealer_upcard):
                if tc >= thr + buffer and basic_action != action:
                    return action, tc, True
        return basic_action, tc, False


from basic_strategy import BasicStrategy
from counting_cards import CardCounter
from deviations import DeviationAdvisor
