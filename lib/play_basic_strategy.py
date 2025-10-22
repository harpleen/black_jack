from basic_strategy import BasicStrategy
from counting_cards import CardCounter
from deviations import DeviationAdvisor

def observe_cards(counter: CardCounter):
    raw = input("Enter visible cards this round (e.g. '10, 6, A, 9') or just press Enter to skip: ").strip()
    if not raw:
        return
    for token in raw.split(','):
        card = token.strip()
        if card:
            counter.observe(card)

def main():
    print("🎴 Welcome to Blackjack Basic Strategy Advisor 🎴")
    
    # Choose game mode
    mode = input("Are you on a CSM (continuous shuffle) table? (y/n): ").strip().lower()
    is_csm = (mode == 'y')

    if is_csm:
        counter = CardCounter(total_decks=8, mode="csm", rolling_window=78)  # ~1.5 decks window
    else:
        counter = CardCounter(total_decks=8, mode="shoe")
        # Optional warm-start if joining mid-shoe
        warm = input("Joining mid-shoe? Estimate decks already gone (0–8), or press Enter: ").strip()
        if warm:
            try:
                decks_gone = float(warm)
                counter.warm_start(int(decks_gone * 52))
            except ValueError:
                print("Ignoring invalid warm-start input.")

    advisor = DeviationAdvisor(counter, cautious=is_csm)
    
    while True:
        try:
            # Ask the player for their total
            player_total = int(input("Enter your hand total (2–21): "))

            # Ask if the hand is soft (contains an Ace counted as 11)
            is_soft_input = input("Is it a soft hand? (y/n): ").strip().lower()
            is_soft = is_soft_input == 'y'

            # Ask if the hand is a pair
            is_pair_input = input("Is it a pair? (y/n): ").strip().lower()
            is_pair = is_pair_input == 'y'

            # Ask for the dealer's upcard
            dealer_upcard = input("Enter dealer's upcard (2–10, J, Q, K, A): ").strip()

            # Create a BasicStrategy instance
            strategy = BasicStrategy(player_total, is_soft, dealer_upcard, is_pair)

            # Get and print the recommendation
            action = strategy.get_action()

            # Update the counter with visible cards from this round
            observe_cards(counter)

            # Apply count-based deviations if warranted
            final_action, tc, changed = advisor.advise(
                action,
                player_total=strategy.player_total,
                dealer_upcard=strategy.dealer_upcard,
                is_soft=strategy.is_soft,
                is_pair=strategy.is_pair,
            )

            if counter.mode == "csm":
                tc_label = f"Rolling TC: {tc:+d}"
            else:
                tc_label = f"True Count: {tc:+d}"

            if changed:
                print(f"\n👉 Basic: {action}  |  {tc_label}  →  Deviation applied: {final_action}\n")
            else:
                print(f"\n👉 Recommended action: {final_action}  |  {tc_label}\n")

        except ValueError:
            print("❌ Invalid input! Please enter numeric values where required.\n")
            continue

        # Ask if they want to check another hand
        again = input("Check another hand? (y/n): ").strip().lower()
        if again != 'y':
            print("\nThanks for using the Blackjack Strategy Advisor! 👋")
            break

if __name__ == "__main__":
    main()