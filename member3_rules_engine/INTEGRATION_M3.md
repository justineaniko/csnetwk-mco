# Member 3 - Rules Engine & End-of-Game Scoring (7 Wonders P2P)

## Included Files
1. `cards_db.py`: Complete database of all cards (Ages I, II, III, Guilds) and all 7 Wonders (Sides A & B).
2. `player_state.py`: Individual player board state management (built structures, coins, Wonder stages, shields, trade discounts).
3. `rules_engine.py`: Move validation (`BUILD_CARD`, `BUILD_WONDER`, `DISCARD`), cheapest neighbor trade solver (left/right backtracking), free chaining, simultaneous turn execution, and end-of-Age military resolution (`AGE_END`).
4. `scoring.py`: Final 7-category scoring calculation (including combinatorial optimization for science symbols and wildcards) + network consensus manager (`SCORE_REPORT` -> `GAME_END`).
5. `test_member3.py`: Standalone mock test script (no network dependencies).

## Integration Guide for Teammates (M1, M2, M4)

```python
from rules_engine import GameRulesEngine
from scoring import EndGameConsensusManager

# 1. At game initialization (after M4's Randomness Ceremony):
# ordered_peers = ["peer_1", "peer_2", "peer_3"]
# wonders = {"peer_1": ("rhodos", "A"), "peer_2": ("babylon", "B"), "peer_3": ("gizah", "A")}
engine = GameRulesEngine(ordered_peers, wonders)

# 2. During the Draft phase (M4), validate a player's move before committing:
is_valid, error_msg, payment = engine.validate_action(peer_id, "BUILD_CARD", card_id)

# 3. Once all cards for the turn are revealed (M4):
turn_events = engine.apply_turn_actions([
    {"peer_id": "peer_1", "action": "BUILD_CARD", "card_id": "lumber_yard"},
    {"peer_id": "peer_2", "action": "DISCARD", "card_id": "altar"},
    {"peer_id": "peer_3", "action": "BUILD_WONDER", "card_id": "baths"},
])

# 4. At the end of each Age (after Turn 6):
age_end_json = engine.resolve_age_end()  # Broadcast via UDP (M1)

# 5. At the end of Age 3 (Score Consensus):
consensus = EndGameConsensusManager(engine, local_peer_id="peer_1")
my_report_json = consensus.generate_local_score_report()  # Send SCORE_REPORT to all peers

# Upon receiving a SCORE_REPORT message from another peer:
consensus.register_peer_score_report(sender_id, received_payload["scores"])
reached, status, game_end_json = consensus.check_consensus()
```
