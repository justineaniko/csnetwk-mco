"""
scoring.py - Calculation of all 7 scoring categories in 7 Wonders and end-of-game consensus
(`SCORE_REPORT` and `GAME_END` per RFC 7WD-1).
"""
import itertools
from typing import Dict, Tuple
from cards_db import get_card
from player_state import PlayerState
from rules_engine import GameRulesEngine


def compute_science_points(compass: int, gear: int, tablet: int, wilds: int) -> int:
    """
    Computes the optimal score for Scientific structures (Green) + wild symbols
    (Scientists Guild, Babylon).
    Formula: a^2 + b^2 + c^2 + 7 * min(a, b, c)
    Evaluates all possible wild symbol assignments to maximize total points.
    """
    if wilds == 0:
        sets = min(compass, gear, tablet)
        return (compass ** 2) + (gear ** 2) + (tablet ** 2) + (7 * sets)

    best_score = 0
    for assignment in itertools.product(["COMPASS", "GEAR", "TABLET"], repeat=wilds):
        c = compass + assignment.count("COMPASS")
        g = gear + assignment.count("GEAR")
        t = tablet + assignment.count("TABLET")
        sets = min(c, g, t)
        score = (c ** 2) + (g ** 2) + (t ** 2) + (7 * sets)
        if score > best_score:
            best_score = score
    return best_score


def calculate_player_score(
    player: PlayerState, left_neighbor: PlayerState, right_neighbor: PlayerState
) -> Dict[str, int]:
    """
    Calculates the full 7-category score breakdown for a player at the end of the game.
    """
    # 1. Military Conflicts
    military_pts = sum(player.military_tokens)

    # 2. Treasury (1 VP per full set of 3 coins)
    treasury_pts = player.coins // 3

    # 3. Wonder
    wonder_pts = 0
    for i in range(player.wonder_stages_built):
        for eff in player.wonder_data["stages"][i]["effects"]:
            if eff["type"] == "VP":
                wonder_pts += eff["points"]

    # 4. Civilian Structures (Blue)
    civilian_pts = 0
    for cid in player.built_cards:
        card = get_card(cid)
        if card["color"] == "BLUE" and card["effect"]["type"] == "VP":
            civilian_pts += card["effect"]["points"]

    # 5. Commercial Structures (Yellow)
    commercial_pts = 0
    for cid in player.built_cards:
        card = get_card(cid)
        if card["color"] == "YELLOW":
            eff = card["effect"]
            if eff["type"] == "DYNAMIC_VP_COINS":
                count = len(player.get_cards_by_color(eff["target_color"]))
                commercial_pts += count * eff["vp"]
            elif eff["type"] == "DYNAMIC_WONDER":
                commercial_pts += player.wonder_stages_built * eff["vp"]

    # 6. Guilds (Purple) - including Olympia Side B Stage 3 (copy neighbor guild)
    guilds_pts = _compute_guilds_points(player, left_neighbor, right_neighbor)

    # 7. Scientific Structures (Green + Wilds)
    compass, gear, tablet, wilds = 0, 0, 0, 0
    for cid in player.built_cards:
        eff = get_card(cid)["effect"]
        if eff["type"] == "SCIENCE":
            sym = eff["symbol"]
            if sym == "COMPASS":
                compass += 1
            elif sym == "GEAR":
                gear += 1
            elif sym == "TABLET":
                tablet += 1
        elif eff["type"] == "SCIENCE_WILD":
            wilds += 1

    for i in range(player.wonder_stages_built):
        for eff in player.wonder_data["stages"][i]["effects"]:
            if eff["type"] == "SCIENCE_WILD":
                wilds += 1

    science_pts = compute_science_points(compass, gear, tablet, wilds)

    total = (
        military_pts
        + treasury_pts
        + wonder_pts
        + civilian_pts
        + commercial_pts
        + guilds_pts
        + science_pts
    )

    return {
        "military": military_pts,
        "treasury": treasury_pts,
        "wonder": wonder_pts,
        "civilian": civilian_pts,
        "commercial": commercial_pts,
        "guilds": guilds_pts,
        "science": science_pts,
        "total": total,
        "coins_tiebreaker": player.coins
    }


def _evaluate_single_guild_effect(
    eff: dict, player: PlayerState, left_neighbor: PlayerState, right_neighbor: PlayerState
) -> int:
    """Evaluates victory points yielded by a specific Guild effect."""
    etype = eff["type"]
    target_map = {"SELF": player, "LEFT": left_neighbor, "RIGHT": right_neighbor}

    if etype == "GUILD_COLOR":
        count = sum(
            len(target_map[t].get_cards_by_color(eff["target_color"]))
            for t in eff["targets"]
        )
        return count * eff["vp"]

    elif etype == "GUILD_MULTI_COLOR":
        count = 0
        for t in eff["targets"]:
            for col in eff["target_colors"]:
                count += len(target_map[t].get_cards_by_color(col))
        return count * eff["vp"]

    elif etype == "GUILD_DEFEAT_TOKENS":
        defeats = 0
        for t in eff["targets"]:
            defeats += sum(1 for tok in target_map[t].military_tokens if tok == -1)
        return defeats * eff["vp"]

    elif etype == "GUILD_WONDERS":
        stages = sum(target_map[t].wonder_stages_built for t in eff["targets"])
        return stages * eff["vp"]

    return 0


def _compute_guilds_points(
    player: PlayerState, left_neighbor: PlayerState, right_neighbor: PlayerState
) -> int:
    pts = 0
    for cid in player.built_cards:
        card = get_card(cid)
        if card["color"] == "PURPLE":
            pts += _evaluate_single_guild_effect(card["effect"], player, left_neighbor, right_neighbor)

    # Olympia Side B Stage 3 special ability: Copy the highest-scoring Guild of a neighbor
    has_olympia_copy = (
        player.wonder_id == "olympia"
        and player.wonder_side == "B"
        and player.wonder_stages_built >= 3
    )
    if has_olympia_copy:
        best_copied_pts = 0
        neighbor_guilds = left_neighbor.get_cards_by_color("PURPLE") + right_neighbor.get_cards_by_color("PURPLE")
        for g_id in neighbor_guilds:
            eff = get_card(g_id)["effect"]
            if eff["type"] != "SCIENCE_WILD":  # Wild science symbols are handled in science scoring
                val = _evaluate_single_guild_effect(eff, player, left_neighbor, right_neighbor)
                if val > best_copied_pts:
                    best_copied_pts = val
        pts += best_copied_pts

    return pts


class EndGameConsensusManager:
    """
    Manages generation of the `SCORE_REPORT` message, cross-peer consensus verification,
    and production of the final `GAME_END` payload.
    """

    def __init__(self, engine: GameRulesEngine, local_peer_id: str):
        self.engine = engine
        self.local_peer_id = local_peer_id
        self.received_reports: Dict[str, dict] = {}

    def generate_local_score_report(self) -> dict:
        """
        Computes the complete score table for all players and formats
        the dictionary ready to be serialized as JSON in a `SCORE_REPORT` packet.
        """
        scores_by_peer = {}
        for pid in self.engine.seat_order:
            player = self.engine.players[pid]
            left_n, right_n = self.engine.get_neighbors(pid)
            scores_by_peer[pid] = calculate_player_score(player, left_n, right_n)

        report = {
            "type": "SCORE_REPORT",
            "sender_id": self.local_peer_id,
            "scores": scores_by_peer
        }
        self.received_reports[self.local_peer_id] = scores_by_peer
        return report

    def register_peer_score_report(self, sender_id: str, peer_scores: dict):
        """Registers a score report received from another peer over UDP."""
        self.received_reports[sender_id] = peer_scores

    def check_consensus(self) -> Tuple[bool, str, dict]:
        """
        Verifies whether all peers have submitted their `SCORE_REPORT` and whether
        all calculations match identically across peers.
        Returns: (consensus_reached: bool, status_msg: str, game_end_payload: dict)
        """
        expected_peers = set(self.engine.seat_order)
        received_peers = set(self.received_reports.keys())

        if received_peers != expected_peers:
            missing = expected_peers - received_peers
            return False, f"Waiting for score reports from: {sorted(list(missing))}", {}

        reference_scores = self.received_reports[self.local_peer_id]
        mismatched_peers = []

        for pid, scores in self.received_reports.items():
            if scores != reference_scores:
                mismatched_peers.append(pid)

        if mismatched_peers:
            return False, f"Score mismatch detected with peers: {mismatched_peers}", {}

        # Final ranking: Total VP descending, then remaining treasury coins as tiebreaker
        ranking = sorted(
            reference_scores.items(),
            key=lambda item: (item[1]["total"], item[1]["coins_tiebreaker"]),
            reverse=True
        )

        # Determine winner(s) (shared victory only if both total VP and coins are tied)
        top_total = ranking[0][1]["total"]
        top_coins = ranking[0][1]["coins_tiebreaker"]
        winners = [
            pid for pid, sc in ranking
            if sc["total"] == top_total and sc["coins_tiebreaker"] == top_coins
        ]

        game_end_payload = {
            "type": "GAME_END",
            "consensus": True,
            "winners": winners,
            "standings": [
                {
                    "rank": idx + 1,
                    "peer_id": pid,
                    "total_points": sc["total"],
                    "coins": sc["coins_tiebreaker"],
                    "breakdown": sc
                }
                for idx, (pid, sc) in enumerate(ranking)
            ]
        }
        return True, "Consensus reached! Game finished.", game_end_payload
