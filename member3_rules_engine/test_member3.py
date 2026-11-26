"""
test_member3.py - Standalone test script (network-free mock) to validate all Member 3 modules.
Run with: python test_member3.py
"""
import json
from rules_engine import GameRulesEngine
from scoring import EndGameConsensusManager


def run_simulation():
    print("=== STARTING 7 WONDERS SIMULATION (MEMBER 3) ===\n")

    # 1. Initialize a 3-player game
    peers = ["peer_alice", "peer_bob", "peer_charlie"]
    wonders = {
        "peer_alice": ("babylon", "A"),     # Starting resource: CLAY
        "peer_bob": ("rhodos", "A"),        # Starting resource: ORE
        "peer_charlie": ("olympia", "A")    # Starting resource: WOOD
    }

    engine = GameRulesEngine(ordered_peer_ids=peers, player_wonders=wonders)

    # 2. Turn 1: Basic building construction + neighbor resource checks
    # Alice tries to build "baths" (cost: 1 STONE), but no one produces Stone yet -> must fail
    ok, reason, _ = engine.validate_action("peer_alice", "BUILD_CARD", "baths")
    print(f"[Illegal Move Test] Alice builds Baths without Stone -> Valid={ok} | Reason: {reason}")
    assert not ok

    # Bob builds "barracks" (cost: 1 ORE -> produced by Rhodos Wonder)
    # Charlie builds "stone_pit" (free -> produces 1 STONE)
    # Alice builds "altar" (free -> 2 VP, chains to Temple)
    engine.apply_turn_actions([
        {"peer_id": "peer_alice", "action": "BUILD_CARD", "card_id": "altar"},
        {"peer_id": "peer_bob", "action": "BUILD_CARD", "card_id": "barracks"},
        {"peer_id": "peer_charlie", "action": "BUILD_CARD", "card_id": "stone_pit"},
    ])
    print("[Turn 1] Actions applied successfully.")

    # 3. Turn 2: Buying a resource from a neighbor (Alice buys 1 STONE from Charlie for 2 coins)
    engine.apply_turn_actions([
        {"peer_id": "peer_alice", "action": "BUILD_CARD", "card_id": "baths"},
        {"peer_id": "peer_bob", "action": "BUILD_CARD", "card_id": "guard_tower"},
        {"peer_id": "peer_charlie", "action": "DISCARD", "card_id": "loom_1"},
    ])
    print(
        f"[Turn 2] Alice coins (expected 3): {engine.players['peer_alice'].coins} | "
        f"Charlie coins (expected 8): {engine.players['peer_charlie'].coins}"
    )
    assert engine.players["peer_alice"].coins == 3
    assert engine.players["peer_charlie"].coins == 8

    # 4. End of Age 1 Military Resolution
    # Alice: 0 shields | Bob: 2 shields | Charlie: 0 shields
    age1_res = engine.resolve_age_end()
    print(f"\n[End of Age 1 - Military] JSON Payload:\n{json.dumps(age1_res, indent=2)}")
    assert engine.players["peer_bob"].military_tokens == [1, 1]
    assert engine.players["peer_alice"].military_tokens == [-1]

    # 5. Free Chaining Test + Scientific Structures (Ages 2 & 3)
    # Alice owns "altar", so she can build "temple" (normal cost 1W 1C 1G) FOR FREE!
    engine.apply_turn_actions([
        {"peer_id": "peer_alice", "action": "BUILD_CARD", "card_id": "temple"},
        {"peer_id": "peer_bob", "action": "BUILD_CARD", "card_id": "loom_1"},
        {"peer_id": "peer_charlie", "action": "BUILD_CARD", "card_id": "glassworks_1"},
    ])
    engine.apply_turn_actions([
        {"peer_id": "peer_alice", "action": "DISCARD", "card_id": "pawnshop"},
        {"peer_id": "peer_bob", "action": "BUILD_CARD", "card_id": "apothecary"},
        {"peer_id": "peer_charlie", "action": "BUILD_CARD", "card_id": "workshop"},
    ])
    print("\n[Free Chaining] Alice built Temple for free via Altar!")

    # Add scientific cards + Scientists Guild (Wild) to Bob
    engine.players["peer_bob"].built_cards.extend(["workshop", "scriptorium", "scientists_guild"])
    # Bob has: apothecary (COMPASS), workshop (GEAR), scriptorium (TABLET) + 1 WILD
    # With 1 wild -> 2 COMPASS, 1 GEAR, 1 TABLET = 4 + 1 + 1 + 7 = 13 science points!

    # 6. End-of-Game Consensus (SCORE_REPORT -> GAME_END)
    consensus_alice = EndGameConsensusManager(engine, "peer_alice")
    consensus_bob = EndGameConsensusManager(engine, "peer_bob")
    consensus_charlie = EndGameConsensusManager(engine, "peer_charlie")

    rep_alice = consensus_alice.generate_local_score_report()
    rep_bob = consensus_bob.generate_local_score_report()
    rep_charlie = consensus_charlie.generate_local_score_report()

    # Simulate network reception at Alice's node
    consensus_alice.register_peer_score_report("peer_bob", rep_bob["scores"])
    consensus_alice.register_peer_score_report("peer_charlie", rep_charlie["scores"])

    ok_consensus, msg, game_end = consensus_alice.check_consensus()
    print(f"\n[Final Consensus] Status: {msg}")
    assert ok_consensus
    assert game_end["standings"][0]["breakdown"]["science"] == 13
    print(json.dumps(game_end, indent=2))
    print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")


if __name__ == "__main__":
    run_simulation()
