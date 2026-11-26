"""
rules_engine.py - Core game rules validation, neighbor resource trading, and military resolution.
Handles actions: BUILD_CARD, BUILD_WONDER, DISCARD, and AGE_END.
"""
from typing import Dict, List, Tuple
from cards_db import get_card
from player_state import PlayerState


def _can_satisfy_resources(required: Dict[str, int], providers: List[List[Dict[str, int]]]) -> bool:
    """
    Uses recursive backtracking to check if the player's resource producers (including
    choice cards like Timber Yard or Caravansery) can cover the required resources.
    """
    rem = {res: qty for res, qty in required.items() if qty > 0}
    if not rem:
        return True
    if not providers:
        return False

    current_provider = providers[0]
    rest_providers = providers[1:]

    for option in current_provider:
        useful = any(rem.get(r, 0) > 0 for r in option)
        if useful:
            new_rem = dict(rem)
            for r, qty in option.items():
                if r in new_rem:
                    new_rem[r] = max(0, new_rem[r] - qty)
            if _can_satisfy_resources(new_rem, rest_providers):
                return True

    return _can_satisfy_resources(rem, rest_providers)


def _find_cheapest_trade(
    required_resources: Dict[str, int],
    player: PlayerState,
    left_neighbor: PlayerState,
    right_neighbor: PlayerState
) -> Tuple[bool, int, int, int]:
    """
    Finds the cheapest way for a player to pay `required_resources` by combining
    their own production and purchasing missing resources from `left_neighbor` and `right_neighbor`.
    Returns: (is_possible: bool, total_coins_needed: int, pay_left: int, pay_right: int)
    """
    own_providers = player.get_resource_providers(only_tradable=False)
    if _can_satisfy_resources(required_resources, own_providers):
        return True, 0, 0, 0

    discounts = player.get_trade_discounts()
    left_cost_per_res = {r: (1 if r in discounts["LEFT"] else 2) for r in required_resources}
    right_cost_per_res = {r: (1 if r in discounts["RIGHT"] else 2) for r in required_resources}

    left_providers = left_neighbor.get_resource_providers(only_tradable=True)
    right_providers = right_neighbor.get_resource_providers(only_tradable=True)

    res_keys = [r for r, q in required_resources.items() if q > 0]
    best_solution = None  # (total_cost, pay_left, pay_right)

    def search_splits(idx: int, self_req: dict, left_req: dict, right_req: dict):
        nonlocal best_solution
        if idx == len(res_keys):
            pay_l = sum(left_req.get(r, 0) * left_cost_per_res[r] for r in res_keys)
            pay_r = sum(right_req.get(r, 0) * right_cost_per_res[r] for r in res_keys)
            total = pay_l + pay_r
            if best_solution is not None and total >= best_solution[0]:
                return
            if (
                _can_satisfy_resources(self_req, own_providers)
                and _can_satisfy_resources(left_req, left_providers)
                and _can_satisfy_resources(right_req, right_providers)
            ):
                best_solution = (total, pay_l, pay_r)
            return

        r = res_keys[idx]
        total_q = required_resources[r]
        for q_self in range(total_q + 1):
            for q_left in range(total_q - q_self + 1):
                q_right = total_q - q_self - q_left
                self_req[r] = q_self
                left_req[r] = q_left
                right_req[r] = q_right
                search_splits(idx + 1, self_req, left_req, right_req)

    search_splits(0, {}, {}, {})

    if best_solution is None:
        return False, 0, 0, 0
    return True, best_solution[0], best_solution[1], best_solution[2]


class GameRulesEngine:
    """
    Core 7 Wonders rules engine for Member 3.
    Handles move validation, immediate card/wonder effect application,
    Public Log recording, and end-of-Age military resolution.
    """

    def __init__(self, ordered_peer_ids: List[str], player_wonders: Dict[str, Tuple[str, str]]):
        """
        ordered_peer_ids: Clockwise ordered list of peer_ids around the table.
        player_wonders: {peer_id: (wonder_id, side)}
        """
        self.seat_order: List[str] = list(ordered_peer_ids)
        self.players: Dict[str, PlayerState] = {}
        for pid in self.seat_order:
            w_id, side = player_wonders[pid]
            self.players[pid] = PlayerState(pid, w_id, side)

        self.current_age: int = 1
        self.current_turn: int = 1
        self.discard_pile: List[str] = []
        self.public_log: List[dict] = []

    def get_neighbors(self, peer_id: str) -> Tuple[PlayerState, PlayerState]:
        """Returns (left_neighbor, right_neighbor) based on seating order."""
        idx = self.seat_order.index(peer_id)
        n = len(self.seat_order)
        left_id = self.seat_order[(idx - 1) % n]
        right_id = self.seat_order[(idx + 1) % n]
        return self.players[left_id], self.players[right_id]

    def validate_action(
        self,
        peer_id: str,
        action_type: str,
        card_id: str,
        use_free_olympia: bool = False
    ) -> Tuple[bool, str, dict]:
        """
        Validates whether a player can perform `action_type` ("BUILD_CARD", "BUILD_WONDER", "DISCARD").
        Returns: (is_valid, reason_message, payment_details)
        payment_details = {"bank_cost": int, "pay_left": int, "pay_right": int, "free_via_chain": bool}
        """
        if peer_id not in self.players:
            return False, f"Unknown player: {peer_id}", {}

        player = self.players[peer_id]
        left_neighbor, right_neighbor = self.get_neighbors(peer_id)

        try:
            card = get_card(card_id)
        except ValueError as e:
            return False, str(e), {}

        # 1. Discarding a card for 3 coins is always legal
        if action_type == "DISCARD":
            return True, "OK", {"bank_cost": 0, "pay_left": 0, "pay_right": 0, "free_via_chain": False}

        # 2. Building a structure
        if action_type == "BUILD_CARD":
            if player.has_card(card_id):
                return False, f"You already own the building {card['name']}.", {}

            # Check free chaining prerequisite
            for prereq_id in card.get("chains_from", []):
                if player.has_card(prereq_id):
                    return True, "OK (Free chain)", {
                        "bank_cost": 0, "pay_left": 0, "pay_right": 0, "free_via_chain": True
                    }

            # Check Olympia Side A special ability (1 free build per Age)
            if use_free_olympia:
                has_olympia_ability = (
                    player.wonder_id == "olympia"
                    and player.wonder_side == "A"
                    and player.wonder_stages_built >= 2
                )
                if not has_olympia_ability:
                    return False, "You do not have the Olympia free-build ability.", {}
                if player.used_olympia_free_build:
                    return False, "Olympia free-build ability already used during this Age.", {}
                return True, "OK (Olympia ability)", {
                    "bank_cost": 0, "pay_left": 0, "pay_right": 0, "free_via_chain": True
                }

            # Check coin + resource cost
            bank_cost = card["cost"].get("coins", 0)
            res_cost = card["cost"].get("resources", {})

            possible, trade_coins, pay_l, pay_r = _find_cheapest_trade(
                res_cost, player, left_neighbor, right_neighbor
            )
            if not possible:
                return False, f"Insufficient resources to build {card['name']}.", {}

            total_coins_needed = bank_cost + trade_coins
            if player.coins < total_coins_needed:
                return False, f"Insufficient coins ({player.coins}/{total_coins_needed} required).", {}

            return True, "OK", {
                "bank_cost": bank_cost, "pay_left": pay_l, "pay_right": pay_r, "free_via_chain": False
            }

        # 3. Building a Wonder stage
        if action_type == "BUILD_WONDER":
            stages = player.wonder_data["stages"]
            if player.wonder_stages_built >= len(stages):
                return False, "All Wonder stages have already been built.", {}

            next_stage = stages[player.wonder_stages_built]
            res_cost = next_stage["cost"]
            possible, trade_coins, pay_l, pay_r = _find_cheapest_trade(
                res_cost, player, left_neighbor, right_neighbor
            )
            if not possible:
                return False, "Insufficient resources to build the next Wonder stage.", {}
            if player.coins < trade_coins:
                return False, f"Insufficient coins to buy missing resources ({player.coins}/{trade_coins}).", {}

            return True, "OK", {
                "bank_cost": 0, "pay_left": pay_l, "pay_right": pay_r, "free_via_chain": False
            }

        return False, f"Invalid action type: {action_type}", {}

    def apply_turn_actions(self, actions: List[dict]) -> List[dict]:
        """
        Simultaneously applies validated actions of all players for a single turn.
        `actions`: list of dicts {"peer_id": str, "action": str, "card_id": str, "use_olympia": bool}
        """
        # Step 1: Validate all actions and compute payments before modifying any state (simultaneity)
        validated_batch = []
        for act in actions:
            pid = act["peer_id"]
            atype = act["action"]
            cid = act["card_id"]
            use_oly = act.get("use_olympia", False)
            ok, msg, pay = self.validate_action(pid, atype, cid, use_oly)
            if not ok:
                raise ValueError(f"Illegal action by {pid} ({atype} {cid}): {msg}")
            validated_batch.append((pid, atype, cid, use_oly, pay))

        # Step 2: Deduct costs and credit neighbors (simultaneous commerce)
        for pid, atype, cid, use_oly, pay in validated_batch:
            player = self.players[pid]
            left_n, right_n = self.get_neighbors(pid)

            total_spent = pay["bank_cost"] + pay["pay_left"] + pay["pay_right"]
            player.coins -= total_spent
            left_n.coins += pay["pay_left"]
            right_n.coins += pay["pay_right"]

            if use_oly and atype == "BUILD_CARD":
                player.used_olympia_free_build = True

        # Step 3: Build cards / Wonder stages and apply immediate coin rewards
        turn_events = []
        for pid, atype, cid, _, pay in validated_batch:
            player = self.players[pid]
            left_n, right_n = self.get_neighbors(pid)

            if atype == "DISCARD":
                self.discard_pile.append(cid)
                player.coins += 3
            elif atype == "BUILD_CARD":
                player.built_cards.append(cid)
                self._apply_immediate_card_effects(player, get_card(cid)["effect"], left_n, right_n)
            elif atype == "BUILD_WONDER":
                stage_idx = player.wonder_stages_built
                player.wonder_stages_built += 1
                stage_effects = player.wonder_data["stages"][stage_idx]["effects"]
                for eff in stage_effects:
                    self._apply_immediate_card_effects(player, eff, left_n, right_n)

            log_entry = {
                "age": self.current_age,
                "turn": self.current_turn,
                "peer_id": pid,
                "action": atype,
                "card_id": cid if atype != "BUILD_WONDER" else "HIDDEN_WONDER_STAGE",
                "payment": pay
            }
            self.public_log.append(log_entry)
            turn_events.append(log_entry)

        self.current_turn += 1
        return turn_events

    def _apply_immediate_card_effects(
        self, player: PlayerState, eff: dict, left_n: PlayerState, right_n: PlayerState
    ):
        """Applies immediate coin gains from Yellow cards or Wonder stages."""
        etype = eff["type"]
        if etype == "COINS":
            player.coins += eff["coins"]

        elif etype == "COINS_PER_COLOR":
            target_color = eff["color"]
            coins_per = eff["coins"]
            count = 0
            if "SELF" in eff["targets"]:
                count += len(player.get_cards_by_color(target_color))
            if "LEFT" in eff["targets"]:
                count += len(left_n.get_cards_by_color(target_color))
            if "RIGHT" in eff["targets"]:
                count += len(right_n.get_cards_by_color(target_color))
            player.coins += count * coins_per

        elif etype == "DYNAMIC_VP_COINS":
            target_color = eff["target_color"]
            coins_per = eff["coins"]
            count = len(player.get_cards_by_color(target_color))
            player.coins += count * coins_per

        elif etype == "DYNAMIC_WONDER":
            player.coins += player.wonder_stages_built * eff["coins"]

    def resolve_age_end(self) -> dict:
        """
        Resolves military conflicts at the end of the current Age (1, 2, or 3)
        and returns the payload ready for the `AGE_END` network message.
        """
        victory_points_by_age = {1: 1, 2: 3, 3: 5}
        win_pts = victory_points_by_age[self.current_age]

        shields_map = {pid: p.get_total_shields() for pid, p in self.players.items()}
        conflicts_result = {}

        for pid in self.seat_order:
            player = self.players[pid]
            left_n, right_n = self.get_neighbors(pid)
            my_shields = shields_map[pid]

            tokens_gained = []
            # Conflict with left neighbor
            if my_shields > shields_map[left_n.peer_id]:
                tokens_gained.append(win_pts)
            elif my_shields < shields_map[left_n.peer_id]:
                tokens_gained.append(-1)

            # Conflict with right neighbor
            if my_shields > shields_map[right_n.peer_id]:
                tokens_gained.append(win_pts)
            elif my_shields < shields_map[right_n.peer_id]:
                tokens_gained.append(-1)

            player.military_tokens.extend(tokens_gained)
            conflicts_result[pid] = {
                "shields": my_shields,
                "tokens_gained": tokens_gained,
                "total_military_score": sum(player.military_tokens)
            }

        age_end_payload = {
            "type": "AGE_END",
            "age": self.current_age,
            "military_results": conflicts_result
        }
        self.public_log.append(age_end_payload)

        # Advance to next Age if applicable
        if self.current_age < 3:
            self.current_age += 1
            self.current_turn = 1
            for p in self.players.values():
                p.reset_age_flags()

        return age_end_payload
