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
# Subset of well-known count-based deviations (dealer Ace coded as 11)
DEVIATIONS = [
    (16, False, False, 10, 0, "STAND"),        # 16 vs 10: stand at TC >= 0
    (15, False, False, 10, 4, "STAND"),        # 15 vs 10: stand at TC >= +4
    (12, False, False,  3, 2, "STAND"),        # 12 vs 3:  stand at TC >= +2
    (12, False, False,  2, 3, "STAND"),        # 12 vs 2:  stand at TC >= +3
    (10, False, False, 10, 4, "DOUBLE DOWN"),  # 10 vs 10: double at TC >= +4
    (11, False, False, 11, 1, "DOUBLE DOWN"),  # 11 vs A:  double at TC >= +1 (H17)
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
