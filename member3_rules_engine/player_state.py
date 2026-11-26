"""
player_state.py - Representation of an individual player's board state.
"""
from typing import List, Dict
from cards_db import get_card, get_wonder


class PlayerState:
    def __init__(self, peer_id: str, wonder_id: str, wonder_side: str = "A", starting_coins: int = 3):
        self.peer_id = peer_id
        self.wonder_id = wonder_id
        self.wonder_side = wonder_side
        self.wonder_data = get_wonder(wonder_id, wonder_side)

        self.coins: int = starting_coins
        self.built_cards: List[str] = []           # List of built card_ids
        self.wonder_stages_built: int = 0           # Number of completed Wonder stages
        self.military_tokens: List[int] = []        # Military conflict tokens (+1, +3, +5, -1)
        self.used_olympia_free_build: bool = False  # Olympia Side A ability (once per Age)

    def reset_age_flags(self):
        """Resets abilities that can be used once per Age."""
        self.used_olympia_free_build = False

    def has_card(self, card_id: str) -> bool:
        """Checks if the player already owns a card (by ID or identical building name)."""
        if card_id in self.built_cards:
            return True
        target_name = get_card(card_id)["name"]
        for built_id in self.built_cards:
            if get_card(built_id)["name"] == target_name:
                return True
        return False

    def get_cards_by_color(self, color: str) -> List[str]:
        return [cid for cid in self.built_cards if get_card(cid)["color"] == color]

    def get_total_shields(self) -> int:
        shields = 0
        for cid in self.built_cards:
            eff = get_card(cid)["effect"]
            if eff["type"] == "MILITARY":
                shields += eff["shields"]
        for i in range(self.wonder_stages_built):
            for eff in self.wonder_data["stages"][i]["effects"]:
                if eff["type"] == "MILITARY":
                    shields += eff["shields"]
        return shields

    def get_trade_discounts(self) -> Dict[str, set]:
        """Returns resources with a trade discount (1 coin instead of 2) for LEFT and RIGHT neighbors."""
        discounts = {"LEFT": set(), "RIGHT": set()}
        for cid in self.built_cards:
            eff = get_card(cid)["effect"]
            if eff["type"] == "TRADE_DISCOUNT":
                self._apply_discount_effect(discounts, eff)
        for i in range(self.wonder_stages_built):
            for eff in self.wonder_data["stages"][i]["effects"]:
                if eff["type"] == "TRADE_DISCOUNT":
                    self._apply_discount_effect(discounts, eff)
        return discounts

    def _apply_discount_effect(self, discounts: Dict[str, set], eff: dict):
        direction = eff["direction"]
        res_list = eff["resources"]
        if direction in ("LEFT", "BOTH"):
            discounts["LEFT"].update(res_list)
        if direction in ("RIGHT", "BOTH"):
            discounts["RIGHT"].update(res_list)

    def get_resource_providers(self, only_tradable: bool = False) -> List[List[Dict[str, int]]]:
        """
        Returns the list of resource producers owned by the player.
        Each item is a list of alternative options (e.g., [{"WOOD": 1}, {"CLAY": 1}] for dual-choice cards).
        If only_tradable=True, excludes yellow cards (Forum, Caravansery) and Wonder stages,
        which cannot be purchased by neighbors according to 7 Wonders rules.
        """
        providers = []
        # Starting resource of the Wonder (tradable with neighbors)
        start_res = self.wonder_data["starting_resource"]
        if start_res:
            providers.append([{start_res: 1}])

        # Built cards
        for cid in self.built_cards:
            card = get_card(cid)
            eff = card["effect"]
            if eff["type"] == "RESOURCE":
                if only_tradable and eff.get("tradable") is False:
                    continue
                providers.append(eff["options"])

        # Built Wonder stages (not tradable with neighbors)
        if not only_tradable:
            for i in range(self.wonder_stages_built):
                for eff in self.wonder_data["stages"][i]["effects"]:
                    if eff["type"] == "RESOURCE":
                        providers.append(eff["options"])

        return providers

    def to_dict(self) -> dict:
        return {
            "peer_id": self.peer_id,
            "wonder_id": self.wonder_id,
            "wonder_side": self.wonder_side,
            "coins": self.coins,
            "built_cards": list(self.built_cards),
            "wonder_stages_built": self.wonder_stages_built,
            "military_tokens": list(self.military_tokens),
            "shields": self.get_total_shields()
        }
