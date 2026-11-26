"""
cards_db.py - Complete Card and Wonder Database for 7 Wonders (RFC 7WD-1)
Contains definitions for all cards (Ages I, II, III, and Guilds) with costs, chaining rules,
and effects, as well as all 7 Wonder boards (Sides A and B).
"""

# Resource types: "WOOD", "STONE", "CLAY", "ORE", "GLASS", "LOOM", "PAPYRUS"
# Card colors: "BROWN", "GREY", "BLUE", "YELLOW", "RED", "GREEN", "PURPLE"
# Science symbols: "COMPASS", "GEAR", "TABLET"

CARDS = {
    # ==================== AGE I ====================
    "lumber_yard": {
        "name": "Lumber Yard", "age": 1, "color": "BROWN", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"WOOD": 1}]}
    },
    "stone_pit": {
        "name": "Stone Pit", "age": 1, "color": "BROWN", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"STONE": 1}]}
    },
    "clay_pool": {
        "name": "Clay Pool", "age": 1, "color": "BROWN", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"CLAY": 1}]}
    },
    "ore_vein": {
        "name": "Ore Vein", "age": 1, "color": "BROWN", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"ORE": 1}]}
    },
    "tree_farm": {
        "name": "Tree Farm", "age": 1, "color": "BROWN", "min_players": 6,
        "cost": {"coins": 1, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"WOOD": 1}, {"CLAY": 1}]}
    },
    "excavation": {
        "name": "Excavation", "age": 1, "color": "BROWN", "min_players": 4,
        "cost": {"coins": 1, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"STONE": 1}, {"CLAY": 1}]}
    },
    "clay_pit": {
        "name": "Clay Pit", "age": 1, "color": "BROWN", "min_players": 3,
        "cost": {"coins": 1, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"CLAY": 1}, {"ORE": 1}]}
    },
    "timber_yard": {
        "name": "Timber Yard", "age": 1, "color": "BROWN", "min_players": 3,
        "cost": {"coins": 1, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"STONE": 1}, {"WOOD": 1}]}
    },
    "forest_cave": {
        "name": "Forest Cave", "age": 1, "color": "BROWN", "min_players": 5,
        "cost": {"coins": 1, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"WOOD": 1}, {"ORE": 1}]}
    },
    "mine": {
        "name": "Mine", "age": 1, "color": "BROWN", "min_players": 6,
        "cost": {"coins": 1, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"ORE": 1}, {"STONE": 1}]}
    },
    "loom_1": {
        "name": "Loom", "age": 1, "color": "GREY", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"LOOM": 1}]}
    },
    "glassworks_1": {
        "name": "Glassworks", "age": 1, "color": "GREY", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"GLASS": 1}]}
    },
    "press_1": {
        "name": "Press", "age": 1, "color": "GREY", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"PAPYRUS": 1}]}
    },
    "pawnshop": {
        "name": "Pawnshop", "age": 1, "color": "BLUE", "min_players": 4,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "VP", "points": 3}
    },
    "baths": {
        "name": "Baths", "age": 1, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"STONE": 1}},
        "chains_from": [], "chains_to": ["aqueduct"],
        "effect": {"type": "VP", "points": 3}
    },
    "altar": {
        "name": "Altar", "age": 1, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": ["temple"],
        "effect": {"type": "VP", "points": 2}
    },
    "theater": {
        "name": "Theater", "age": 1, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": ["statue"],
        "effect": {"type": "VP", "points": 2}
    },
    "tavern": {
        "name": "Tavern", "age": 1, "color": "YELLOW", "min_players": 4,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "COINS", "coins": 5}
    },
    "east_trading_post": {
        "name": "East Trading Post", "age": 1, "color": "YELLOW", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": ["forum"],
        "effect": {"type": "TRADE_DISCOUNT", "direction": "RIGHT", "resources": ["WOOD", "STONE", "CLAY", "ORE"]}
    },
    "west_trading_post": {
        "name": "West Trading Post", "age": 1, "color": "YELLOW", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": ["forum"],
        "effect": {"type": "TRADE_DISCOUNT", "direction": "LEFT", "resources": ["WOOD", "STONE", "CLAY", "ORE"]}
    },
    "marketplace": {
        "name": "Marketplace", "age": 1, "color": "YELLOW", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": ["caravansery"],
        "effect": {"type": "TRADE_DISCOUNT", "direction": "BOTH", "resources": ["GLASS", "LOOM", "PAPYRUS"]}
    },
    "stockade": {
        "name": "Stockade", "age": 1, "color": "RED", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "MILITARY", "shields": 1}
    },
    "barracks": {
        "name": "Barracks", "age": 1, "color": "RED", "min_players": 3,
        "cost": {"coins": 0, "resources": {"ORE": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "MILITARY", "shields": 1}
    },
    "guard_tower": {
        "name": "Guard Tower", "age": 1, "color": "RED", "min_players": 3,
        "cost": {"coins": 0, "resources": {"CLAY": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "MILITARY", "shields": 1}
    },
    "apothecary": {
        "name": "Apothecary", "age": 1, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"LOOM": 1}},
        "chains_from": [], "chains_to": ["stables", "dispensary"],
        "effect": {"type": "SCIENCE", "symbol": "COMPASS"}
    },
    "workshop": {
        "name": "Workshop", "age": 1, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"GLASS": 1}},
        "chains_from": [], "chains_to": ["laboratory", "archery_range"],
        "effect": {"type": "SCIENCE", "symbol": "GEAR"}
    },
    "scriptorium": {
        "name": "Scriptorium", "age": 1, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"PAPYRUS": 1}},
        "chains_from": [], "chains_to": ["courthouse", "library"],
        "effect": {"type": "SCIENCE", "symbol": "TABLET"}
    },

    # ==================== AGE II ====================
    "sawmill": {
        "name": "Sawmill", "age": 2, "color": "BROWN", "min_players": 3,
        "cost": {"coins": 1, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"WOOD": 2}]}
    },
    "quarry": {
        "name": "Quarry", "age": 2, "color": "BROWN", "min_players": 3,
        "cost": {"coins": 1, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"STONE": 2}]}
    },
    "brickyard": {
        "name": "Brickyard", "age": 2, "color": "BROWN", "min_players": 3,
        "cost": {"coins": 1, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"CLAY": 2}]}
    },
    "foundry": {
        "name": "Foundry", "age": 2, "color": "BROWN", "min_players": 3,
        "cost": {"coins": 1, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"ORE": 2}]}
    },
    "loom_2": {
        "name": "Loom", "age": 2, "color": "GREY", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"LOOM": 1}]}
    },
    "glassworks_2": {
        "name": "Glassworks", "age": 2, "color": "GREY", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"GLASS": 1}]}
    },
    "press_2": {
        "name": "Press", "age": 2, "color": "GREY", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "RESOURCE", "options": [{"PAPYRUS": 1}]}
    },
    "aqueduct": {
        "name": "Aqueduct", "age": 2, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"STONE": 3}},
        "chains_from": ["baths"], "chains_to": [],
        "effect": {"type": "VP", "points": 5}
    },
    "temple": {
        "name": "Temple", "age": 2, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 1, "CLAY": 1, "GLASS": 1}},
        "chains_from": ["altar"], "chains_to": ["pantheon"],
        "effect": {"type": "VP", "points": 3}
    },
    "statue": {
        "name": "Statue", "age": 2, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"ORE": 2, "WOOD": 1}},
        "chains_from": ["theater"], "chains_to": ["gardens"],
        "effect": {"type": "VP", "points": 4}
    },
    "courthouse": {
        "name": "Courthouse", "age": 2, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"CLAY": 2, "LOOM": 1}},
        "chains_from": ["scriptorium"], "chains_to": [],
        "effect": {"type": "VP", "points": 4}
    },
    "forum": {
        "name": "Forum", "age": 2, "color": "YELLOW", "min_players": 3,
        "cost": {"coins": 0, "resources": {"CLAY": 2}},
        "chains_from": ["east_trading_post", "west_trading_post"], "chains_to": ["haven"],
        "effect": {"type": "RESOURCE", "options": [{"GLASS": 1}, {"LOOM": 1}, {"PAPYRUS": 1}], "tradable": False}
    },
    "caravansery": {
        "name": "Caravansery", "age": 2, "color": "YELLOW", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 2}},
        "chains_from": ["marketplace"], "chains_to": ["lighthouse"],
        "effect": {"type": "RESOURCE", "options": [{"WOOD": 1}, {"STONE": 1}, {"CLAY": 1}, {"ORE": 1}], "tradable": False}
    },
    "vineyard": {
        "name": "Vineyard", "age": 2, "color": "YELLOW", "min_players": 3,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "COINS_PER_COLOR", "color": "BROWN", "coins": 1, "targets": ["SELF", "LEFT", "RIGHT"]}
    },
    "bazar": {
        "name": "Bazar", "age": 2, "color": "YELLOW", "min_players": 4,
        "cost": {"coins": 0, "resources": {}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "COINS_PER_COLOR", "color": "GREY", "coins": 2, "targets": ["SELF", "LEFT", "RIGHT"]}
    },
    "walls": {
        "name": "Walls", "age": 2, "color": "RED", "min_players": 3,
        "cost": {"coins": 0, "resources": {"STONE": 3}},
        "chains_from": [], "chains_to": ["fortifications"],
        "effect": {"type": "MILITARY", "shields": 2}
    },
    "training_ground": {
        "name": "Training Ground", "age": 2, "color": "RED", "min_players": 4,
        "cost": {"coins": 0, "resources": {"ORE": 2, "WOOD": 1}},
        "chains_from": [], "chains_to": ["circus"],
        "effect": {"type": "MILITARY", "shields": 2}
    },
    "stables": {
        "name": "Stables", "age": 2, "color": "RED", "min_players": 3,
        "cost": {"coins": 0, "resources": {"CLAY": 1, "WOOD": 1, "ORE": 1}},
        "chains_from": ["apothecary"], "chains_to": [],
        "effect": {"type": "MILITARY", "shields": 2}
    },
    "archery_range": {
        "name": "Archery Range", "age": 2, "color": "RED", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 2, "ORE": 1}},
        "chains_from": ["workshop"], "chains_to": [],
        "effect": {"type": "MILITARY", "shields": 2}
    },
    "dispensary": {
        "name": "Dispensary", "age": 2, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"ORE": 2, "GLASS": 1}},
        "chains_from": ["apothecary"], "chains_to": ["lodge", "arena"],
        "effect": {"type": "SCIENCE", "symbol": "COMPASS"}
    },
    "laboratory": {
        "name": "Laboratory", "age": 2, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"CLAY": 2, "PAPYRUS": 1}},
        "chains_from": ["workshop"], "chains_to": ["observatory", "siege_workshop"],
        "effect": {"type": "SCIENCE", "symbol": "GEAR"}
    },
    "library": {
        "name": "Library", "age": 2, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"STONE": 2, "LOOM": 1}},
        "chains_from": ["scriptorium"], "chains_to": ["senate", "university"],
        "effect": {"type": "SCIENCE", "symbol": "TABLET"}
    },
    "school": {
        "name": "School", "age": 2, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 1, "PAPYRUS": 1}},
        "chains_from": [], "chains_to": ["academy", "study"],
        "effect": {"type": "SCIENCE", "symbol": "TABLET"}
    },

    # ==================== AGE III ====================
    "pantheon": {
        "name": "Pantheon", "age": 3, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"CLAY": 2, "ORE": 1, "GLASS": 1, "PAPYRUS": 1, "LOOM": 1}},
        "chains_from": ["temple"], "chains_to": [],
        "effect": {"type": "VP", "points": 7}
    },
    "gardens": {
        "name": "Gardens", "age": 3, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"CLAY": 2, "WOOD": 1}},
        "chains_from": ["statue"], "chains_to": [],
        "effect": {"type": "VP", "points": 5}
    },
    "town_hall": {
        "name": "Town Hall", "age": 3, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"STONE": 2, "ORE": 1, "GLASS": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "VP", "points": 6}
    },
    "palace": {
        "name": "Palace", "age": 3, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"STONE": 1, "ORE": 1, "WOOD": 1, "CLAY": 1, "GLASS": 1, "PAPYRUS": 1, "LOOM": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "VP", "points": 8}
    },
    "senate": {
        "name": "Senate", "age": 3, "color": "BLUE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 2, "STONE": 1, "ORE": 1}},
        "chains_from": ["library"], "chains_to": [],
        "effect": {"type": "VP", "points": 6}
    },
    "haven": {
        "name": "Haven", "age": 3, "color": "YELLOW", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 1, "ORE": 1, "LOOM": 1}},
        "chains_from": ["forum"], "chains_to": [],
        "effect": {"type": "DYNAMIC_VP_COINS", "target_color": "BROWN", "coins": 1, "vp": 1, "targets": ["SELF"]}
    },
    "lighthouse": {
        "name": "Lighthouse", "age": 3, "color": "YELLOW", "min_players": 3,
        "cost": {"coins": 0, "resources": {"STONE": 1, "GLASS": 1}},
        "chains_from": ["caravansery"], "chains_to": [],
        "effect": {"type": "DYNAMIC_VP_COINS", "target_color": "YELLOW", "coins": 1, "vp": 1, "targets": ["SELF"]}
    },
    "chamber_of_commerce": {
        "name": "Chamber of Commerce", "age": 3, "color": "YELLOW", "min_players": 4,
        "cost": {"coins": 0, "resources": {"CLAY": 2, "PAPYRUS": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "DYNAMIC_VP_COINS", "target_color": "GREY", "coins": 2, "vp": 2, "targets": ["SELF"]}
    },
    "arena": {
        "name": "Arena", "age": 3, "color": "YELLOW", "min_players": 3,
        "cost": {"coins": 0, "resources": {"STONE": 2, "ORE": 1}},
        "chains_from": ["dispensary"], "chains_to": [],
        "effect": {"type": "DYNAMIC_WONDER", "coins": 3, "vp": 1}
    },
    "fortifications": {
        "name": "Fortifications", "age": 3, "color": "RED", "min_players": 3,
        "cost": {"coins": 0, "resources": {"ORE": 3, "STONE": 1}},
        "chains_from": ["walls"], "chains_to": [],
        "effect": {"type": "MILITARY", "shields": 3}
    },
    "circus": {
        "name": "Circus", "age": 3, "color": "RED", "min_players": 4,
        "cost": {"coins": 0, "resources": {"STONE": 3, "ORE": 1}},
        "chains_from": ["training_ground"], "chains_to": [],
        "effect": {"type": "MILITARY", "shields": 3}
    },
    "arsenal": {
        "name": "Arsenal", "age": 3, "color": "RED", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 2, "ORE": 1, "LOOM": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "MILITARY", "shields": 3}
    },
    "siege_workshop": {
        "name": "Siege Workshop", "age": 3, "color": "RED", "min_players": 3,
        "cost": {"coins": 0, "resources": {"CLAY": 3, "WOOD": 1}},
        "chains_from": ["laboratory"], "chains_to": [],
        "effect": {"type": "MILITARY", "shields": 3}
    },
    "lodge": {
        "name": "Lodge", "age": 3, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"CLAY": 2, "PAPYRUS": 1, "LOOM": 1}},
        "chains_from": ["dispensary"], "chains_to": [],
        "effect": {"type": "SCIENCE", "symbol": "COMPASS"}
    },
    "observatory": {
        "name": "Observatory", "age": 3, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"ORE": 2, "GLASS": 1, "LOOM": 1}},
        "chains_from": ["laboratory"], "chains_to": [],
        "effect": {"type": "SCIENCE", "symbol": "GEAR"}
    },
    "university": {
        "name": "University", "age": 3, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 2, "PAPYRUS": 1, "GLASS": 1}},
        "chains_from": ["library"], "chains_to": [],
        "effect": {"type": "SCIENCE", "symbol": "TABLET"}
    },
    "academy": {
        "name": "Academy", "age": 3, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"STONE": 3, "GLASS": 1}},
        "chains_from": ["school"], "chains_to": [],
        "effect": {"type": "SCIENCE", "symbol": "COMPASS"}
    },
    "study": {
        "name": "Study", "age": 3, "color": "GREEN", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 1, "PAPYRUS": 1, "LOOM": 1}},
        "chains_from": ["school"], "chains_to": [],
        "effect": {"type": "SCIENCE", "symbol": "GEAR"}
    },

    # ==================== GUILDS (AGE III - PURPLE) ====================
    "workers_guild": {
        "name": "Workers Guild", "age": 3, "color": "PURPLE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"ORE": 2, "CLAY": 1, "STONE": 1, "WOOD": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "GUILD_COLOR", "target_color": "BROWN", "vp": 1, "targets": ["LEFT", "RIGHT"]}
    },
    "craftsmens_guild": {
        "name": "Craftsmens Guild", "age": 3, "color": "PURPLE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"ORE": 2, "STONE": 2}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "GUILD_COLOR", "target_color": "GREY", "vp": 2, "targets": ["LEFT", "RIGHT"]}
    },
    "traders_guild": {
        "name": "Traders Guild", "age": 3, "color": "PURPLE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"GLASS": 1, "LOOM": 1, "PAPYRUS": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "GUILD_COLOR", "target_color": "YELLOW", "vp": 1, "targets": ["LEFT", "RIGHT"]}
    },
    "philosophers_guild": {
        "name": "Philosophers Guild", "age": 3, "color": "PURPLE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"CLAY": 3, "PAPYRUS": 1, "LOOM": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "GUILD_COLOR", "target_color": "GREEN", "vp": 1, "targets": ["LEFT", "RIGHT"]}
    },
    "spies_guild": {
        "name": "Spies Guild", "age": 3, "color": "PURPLE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"CLAY": 3, "GLASS": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "GUILD_COLOR", "target_color": "RED", "vp": 1, "targets": ["LEFT", "RIGHT"]}
    },
    "strategists_guild": {
        "name": "Strategists Guild", "age": 3, "color": "PURPLE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"ORE": 2, "STONE": 1, "LOOM": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "GUILD_DEFEAT_TOKENS", "vp": 1, "targets": ["LEFT", "RIGHT"]}
    },
    "shipowners_guild": {
        "name": "Shipowners Guild", "age": 3, "color": "PURPLE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 3, "GLASS": 1, "PAPYRUS": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "GUILD_MULTI_COLOR", "target_colors": ["BROWN", "GREY", "PURPLE"], "vp": 1, "targets": ["SELF"]}
    },
    "scientists_guild": {
        "name": "Scientists Guild", "age": 3, "color": "PURPLE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 2, "ORE": 2, "PAPYRUS": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "SCIENCE_WILD"}
    },
    "magistrates_guild": {
        "name": "Magistrates Guild", "age": 3, "color": "PURPLE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"WOOD": 3, "STONE": 1, "LOOM": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "GUILD_COLOR", "target_color": "BLUE", "vp": 1, "targets": ["LEFT", "RIGHT"]}
    },
    "builders_guild": {
        "name": "Builders Guild", "age": 3, "color": "PURPLE", "min_players": 3,
        "cost": {"coins": 0, "resources": {"STONE": 2, "CLAY": 2, "GLASS": 1}},
        "chains_from": [], "chains_to": [],
        "effect": {"type": "GUILD_WONDERS", "vp": 1, "targets": ["SELF", "LEFT", "RIGHT"]}
    }
}

WONDERS = {
    "rhodos": {
        "name": "The Colossus of Rhodes",
        "A": {
            "starting_resource": "ORE",
            "stages": [
                {"cost": {"WOOD": 2}, "effects": [{"type": "VP", "points": 3}]},
                {"cost": {"CLAY": 3}, "effects": [{"type": "MILITARY", "shields": 2}]},
                {"cost": {"ORE": 4}, "effects": [{"type": "VP", "points": 7}]}
            ]
        },
        "B": {
            "starting_resource": "ORE",
            "stages": [
                {"cost": {"STONE": 3}, "effects": [{"type": "MILITARY", "shields": 1}, {"type": "VP", "points": 3}, {"type": "COINS", "coins": 3}]},
                {"cost": {"ORE": 4}, "effects": [{"type": "MILITARY", "shields": 1}, {"type": "VP", "points": 4}, {"type": "COINS", "coins": 4}]}
            ]
        }
    },
    "alexandria": {
        "name": "The Lighthouse of Alexandria",
        "A": {
            "starting_resource": "GLASS",
            "stages": [
                {"cost": {"STONE": 2}, "effects": [{"type": "VP", "points": 3}]},
                {"cost": {"ORE": 2}, "effects": [{"type": "RESOURCE", "options": [{"WOOD": 1}, {"STONE": 1}, {"CLAY": 1}, {"ORE": 1}], "tradable": False}]},
                {"cost": {"GLASS": 2}, "effects": [{"type": "VP", "points": 7}]}
            ]
        },
        "B": {
            "starting_resource": "GLASS",
            "stages": [
                {"cost": {"CLAY": 2}, "effects": [{"type": "RESOURCE", "options": [{"WOOD": 1}, {"STONE": 1}, {"CLAY": 1}, {"ORE": 1}], "tradable": False}]},
                {"cost": {"WOOD": 2}, "effects": [{"type": "RESOURCE", "options": [{"GLASS": 1}, {"LOOM": 1}, {"PAPYRUS": 1}], "tradable": False}]},
                {"cost": {"STONE": 3}, "effects": [{"type": "VP", "points": 7}]}
            ]
        }
    },
    "ephesos": {
        "name": "The Temple of Artemis in Ephesus",
        "A": {
            "starting_resource": "PAPYRUS",
            "stages": [
                {"cost": {"STONE": 2}, "effects": [{"type": "VP", "points": 3}]},
                {"cost": {"WOOD": 2}, "effects": [{"type": "COINS", "coins": 9}]},
                {"cost": {"PAPYRUS": 2}, "effects": [{"type": "VP", "points": 7}]}
            ]
        },
        "B": {
            "starting_resource": "PAPYRUS",
            "stages": [
                {"cost": {"STONE": 2}, "effects": [{"type": "VP", "points": 2}, {"type": "COINS", "coins": 4}]},
                {"cost": {"WOOD": 2}, "effects": [{"type": "VP", "points": 3}, {"type": "COINS", "coins": 4}]},
                {"cost": {"PAPYRUS": 1, "LOOM": 1, "GLASS": 1}, "effects": [{"type": "VP", "points": 5}, {"type": "COINS", "coins": 4}]}
            ]
        }
    },
    "babylon": {
        "name": "The Hanging Gardens of Babylon",
        "A": {
            "starting_resource": "CLAY",
            "stages": [
                {"cost": {"CLAY": 2}, "effects": [{"type": "VP", "points": 3}]},
                {"cost": {"WOOD": 3}, "effects": [{"type": "SCIENCE_WILD"}]},
                {"cost": {"CLAY": 4}, "effects": [{"type": "VP", "points": 7}]}
            ]
        },
        "B": {
            "starting_resource": "CLAY",
            "stages": [
                {"cost": {"CLAY": 1, "LOOM": 1}, "effects": [{"type": "VP", "points": 3}]},
                {"cost": {"WOOD": 2, "GLASS": 1}, "effects": [{"type": "SPECIAL", "ability": "PLAY_LAST_CARD"}]},
                {"cost": {"CLAY": 3, "PAPYRUS": 1}, "effects": [{"type": "SCIENCE_WILD"}]}
            ]
        }
    },
    "olympia": {
        "name": "The Statue of Zeus in Olympia",
        "A": {
            "starting_resource": "WOOD",
            "stages": [
                {"cost": {"WOOD": 2}, "effects": [{"type": "VP", "points": 3}]},
                {"cost": {"STONE": 2}, "effects": [{"type": "SPECIAL", "ability": "FREE_BUILD_ONCE_PER_AGE"}]},
                {"cost": {"ORE": 2}, "effects": [{"type": "VP", "points": 7}]}
            ]
        },
        "B": {
            "starting_resource": "WOOD",
            "stages": [
                {"cost": {"WOOD": 2}, "effects": [{"type": "TRADE_DISCOUNT", "direction": "BOTH", "resources": ["WOOD", "STONE", "CLAY", "ORE"]}]},
                {"cost": {"STONE": 2}, "effects": [{"type": "VP", "points": 5}]},
                {"cost": {"ORE": 2, "LOOM": 1}, "effects": [{"type": "SPECIAL", "ability": "COPY_NEIGHBOR_GUILD"}]}
            ]
        }
    },
    "halikarnassos": {
        "name": "The Mausoleum of Halicarnassus",
        "A": {
            "starting_resource": "LOOM",
            "stages": [
                {"cost": {"CLAY": 2}, "effects": [{"type": "VP", "points": 3}]},
                {"cost": {"ORE": 3}, "effects": [{"type": "SPECIAL", "ability": "BUILD_FROM_DISCARD"}]},
                {"cost": {"LOOM": 2}, "effects": [{"type": "VP", "points": 7}]}
            ]
        },
        "B": {
            "starting_resource": "LOOM",
            "stages": [
                {"cost": {"ORE": 2}, "effects": [{"type": "VP", "points": 2}, {"type": "SPECIAL", "ability": "BUILD_FROM_DISCARD"}]},
                {"cost": {"CLAY": 3}, "effects": [{"type": "VP", "points": 1}, {"type": "SPECIAL", "ability": "BUILD_FROM_DISCARD"}]},
                {"cost": {"GLASS": 1, "PAPYRUS": 1, "LOOM": 1}, "effects": [{"type": "SPECIAL", "ability": "BUILD_FROM_DISCARD"}]}
            ]
        }
    },
    "gizah": {
        "name": "The Pyramids of Giza",
        "A": {
            "starting_resource": "STONE",
            "stages": [
                {"cost": {"STONE": 2}, "effects": [{"type": "VP", "points": 3}]},
                {"cost": {"WOOD": 3}, "effects": [{"type": "VP", "points": 5}]},
                {"cost": {"STONE": 4}, "effects": [{"type": "VP", "points": 7}]}
            ]
        },
        "B": {
            "starting_resource": "STONE",
            "stages": [
                {"cost": {"WOOD": 2}, "effects": [{"type": "VP", "points": 3}]},
                {"cost": {"STONE": 3}, "effects": [{"type": "VP", "points": 5}]},
                {"cost": {"CLAY": 3}, "effects": [{"type": "VP", "points": 5}]},
                {"cost": {"STONE": 4, "PAPYRUS": 1}, "effects": [{"type": "VP", "points": 7}]}
            ]
        }
    }
}


def get_card(card_id: str) -> dict:
    if card_id not in CARDS:
        raise ValueError(f"Unknown card in database: {card_id}")
    return CARDS[card_id]


def get_wonder(wonder_id: str, side: str = "A") -> dict:
    if wonder_id not in WONDERS or side not in WONDERS[wonder_id]:
        raise ValueError(f"Unknown wonder: {wonder_id} (side {side})")
    return WONDERS[wonder_id][side]
