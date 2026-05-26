"""
Matchup Guide: runas, builds y consejos de matchup por campeón/rol/rival.
Los builds usan nombres de objetos (resolución dinámica via Data Dragon) para
no depender de IDs que cambian con cada parche.
"""

# ── RUNAS ────────────────────────────────────────────────────────────────────
# Formato: keystone, primary_tree, primary_slots (3), secondary_tree, secondary_slots (2), shards (3)
# Las claves son los "key" de runesReforged.json de Data Dragon.

RUNE_PAGES: dict[str, dict[str, dict]] = {
    # TOP
    "Darius": {"TOP": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendTenacity", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Overgrowth"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Aatrox": {"TOP": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendBloodline", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Unflinching"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Garen": {"TOP": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendTenacity", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["Demolish", "Overgrowth"],
        "shards": ["Adaptive Force", "Armor", "Health Scaling"],
    }},
    "Jax": {"TOP": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendAlacrity", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Overgrowth"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Irelia": {"TOP": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendAlacrity", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Unflinching"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Camille": {"TOP": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendAlacrity", "CoupDeGrace"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Overgrowth"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Malphite": {"TOP": {
        "keystone": "Arcane Comet", "primary_tree": "Sorcery",
        "primary_slots": ["ManaflowBand", "Transcendence", "GatheringStorm"],
        "secondary_tree": "Resolve", "secondary_slots": ["Demolish", "BonePlating"],
        "shards": ["Adaptive Force", "Armor", "Health Scaling"],
    }},
    "Renekton": {"TOP": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendTenacity", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Unflinching"],
        "shards": ["Adaptive Force", "Adaptive Force", "Armor"],
    }},
    # JUNGLE
    "LeeSin": {"JUNGLE": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendTenacity", "CoupDeGrace"],
        "secondary_tree": "Domination", "secondary_slots": ["TasteOfBlood", "TreasureHunter"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Viego": {"JUNGLE": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendAlacrity", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Overgrowth"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Kayn": {"JUNGLE": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendAlacrity", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Overgrowth"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "JarvanIV": {"JUNGLE": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendTenacity", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Overgrowth"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Vi": {"JUNGLE": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendTenacity", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Overgrowth"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Warwick": {"JUNGLE": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendBloodline", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Overgrowth"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Graves": {"JUNGLE": {
        "keystone": "Conqueror", "primary_tree": "Precision",
        "primary_slots": ["Triumph", "LegendAlacrity", "LastStand"],
        "secondary_tree": "Domination", "secondary_slots": ["TasteOfBlood", "TreasureHunter"],
        "shards": ["Adaptive Force", "Adaptive Force", "Armor"],
    }},
    # MIDDLE
    "Ahri": {"MIDDLE": {
        "keystone": "Electrocute", "primary_tree": "Domination",
        "primary_slots": ["TasteOfBlood", "EyeballCollection", "TreasureHunter"],
        "secondary_tree": "Sorcery", "secondary_slots": ["Transcendence", "GatheringStorm"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Zed": {"MIDDLE": {
        "keystone": "Electrocute", "primary_tree": "Domination",
        "primary_slots": ["TasteOfBlood", "ZombieWard", "TreasureHunter"],
        "secondary_tree": "Sorcery", "secondary_slots": ["AbsoluteFocus", "GatheringStorm"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Syndra": {"MIDDLE": {
        "keystone": "Electrocute", "primary_tree": "Domination",
        "primary_slots": ["TasteOfBlood", "EyeballCollection", "TreasureHunter"],
        "secondary_tree": "Sorcery", "secondary_slots": ["Transcendence", "GatheringStorm"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Viktor": {"MIDDLE": {
        "keystone": "Arcane Comet", "primary_tree": "Sorcery",
        "primary_slots": ["ManaflowBand", "Transcendence", "GatheringStorm"],
        "secondary_tree": "Domination", "secondary_slots": ["TasteOfBlood", "TreasureHunter"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Leblanc": {"MIDDLE": {
        "keystone": "Electrocute", "primary_tree": "Domination",
        "primary_slots": ["TasteOfBlood", "ZombieWard", "TreasureHunter"],
        "secondary_tree": "Sorcery", "secondary_slots": ["Transcendence", "GatheringStorm"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Orianna": {"MIDDLE": {
        "keystone": "Arcane Comet", "primary_tree": "Sorcery",
        "primary_slots": ["ManaflowBand", "Transcendence", "GatheringStorm"],
        "secondary_tree": "Inspiration", "secondary_slots": ["BiscuitDelivery", "CosmicInsight"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Fizz": {"MIDDLE": {
        "keystone": "Electrocute", "primary_tree": "Domination",
        "primary_slots": ["TasteOfBlood", "EyeballCollection", "TreasureHunter"],
        "secondary_tree": "Sorcery", "secondary_slots": ["AbsoluteFocus", "GatheringStorm"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Yasuo": {"MIDDLE": {
        "keystone": "LethalTempo", "primary_tree": "Precision",
        "primary_slots": ["PresenceOfMind", "LegendAlacrity", "LastStand"],
        "secondary_tree": "Resolve", "secondary_slots": ["BonePlating", "Overgrowth"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    # ADC
    "Jinx": {"BOTTOM": {
        "keystone": "LethalTempo", "primary_tree": "Precision",
        "primary_slots": ["PresenceOfMind", "LegendAlacrity", "CoupDeGrace"],
        "secondary_tree": "Domination", "secondary_slots": ["TasteOfBlood", "TreasureHunter"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Caitlyn": {"BOTTOM": {
        "keystone": "FleetFootwork", "primary_tree": "Precision",
        "primary_slots": ["PresenceOfMind", "LegendAlacrity", "CoupDeGrace"],
        "secondary_tree": "Domination", "secondary_slots": ["TasteOfBlood", "TreasureHunter"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Jhin": {"BOTTOM": {
        "keystone": "FleetFootwork", "primary_tree": "Precision",
        "primary_slots": ["PresenceOfMind", "LegendAlacrity", "CoupDeGrace"],
        "secondary_tree": "Sorcery", "secondary_slots": ["AbsoluteFocus", "GatheringStorm"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "MissFortune": {"BOTTOM": {
        "keystone": "LethalTempo", "primary_tree": "Precision",
        "primary_slots": ["PresenceOfMind", "LegendBloodline", "CoupDeGrace"],
        "secondary_tree": "Domination", "secondary_slots": ["TasteOfBlood", "TreasureHunter"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Kaisa": {"BOTTOM": {
        "keystone": "PressTheAttack", "primary_tree": "Precision",
        "primary_slots": ["PresenceOfMind", "LegendAlacrity", "CoupDeGrace"],
        "secondary_tree": "Domination", "secondary_slots": ["TasteOfBlood", "TreasureHunter"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Ashe": {"BOTTOM": {
        "keystone": "FleetFootwork", "primary_tree": "Precision",
        "primary_slots": ["PresenceOfMind", "LegendAlacrity", "CoupDeGrace"],
        "secondary_tree": "Domination", "secondary_slots": ["TasteOfBlood", "TreasureHunter"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    "Ezreal": {"BOTTOM": {
        "keystone": "Arcane Comet", "primary_tree": "Sorcery",
        "primary_slots": ["ManaflowBand", "Transcendence", "GatheringStorm"],
        "secondary_tree": "Inspiration", "secondary_slots": ["BiscuitDelivery", "CosmicInsight"],
        "shards": ["Adaptive Force", "Adaptive Force", "Health Scaling"],
    }},
    # SUPPORT
    "Thresh": {"UTILITY": {
        "keystone": "Aftershock", "primary_tree": "Resolve",
        "primary_slots": ["FontOfLife", "BonePlating", "Overgrowth"],
        "secondary_tree": "Inspiration", "secondary_slots": ["BiscuitDelivery", "CosmicInsight"],
        "shards": ["Armor", "Armor", "Health Scaling"],
    }},
    "Nautilus": {"UTILITY": {
        "keystone": "Aftershock", "primary_tree": "Resolve",
        "primary_slots": ["FontOfLife", "BonePlating", "Overgrowth"],
        "secondary_tree": "Inspiration", "secondary_slots": ["BiscuitDelivery", "CosmicInsight"],
        "shards": ["Armor", "Armor", "Health Scaling"],
    }},
    "Lulu": {"UTILITY": {
        "keystone": "SummonAery", "primary_tree": "Sorcery",
        "primary_slots": ["ManaflowBand", "Transcendence", "Revitalize"],
        "secondary_tree": "Inspiration", "secondary_slots": ["BiscuitDelivery", "CosmicInsight"],
        "shards": ["Adaptive Force", "Armor", "Health Scaling"],
    }},
    "Janna": {"UTILITY": {
        "keystone": "SummonAery", "primary_tree": "Sorcery",
        "primary_slots": ["ManaflowBand", "Transcendence", "Revitalize"],
        "secondary_tree": "Inspiration", "secondary_slots": ["BiscuitDelivery", "CosmicInsight"],
        "shards": ["Adaptive Force", "Armor", "Health Scaling"],
    }},
    "Blitzcrank": {"UTILITY": {
        "keystone": "Aftershock", "primary_tree": "Resolve",
        "primary_slots": ["FontOfLife", "BonePlating", "Overgrowth"],
        "secondary_tree": "Inspiration", "secondary_slots": ["BiscuitDelivery", "CosmicInsight"],
        "shards": ["Armor", "Armor", "Health Scaling"],
    }},
    "Morgana": {"UTILITY": {
        "keystone": "Arcane Comet", "primary_tree": "Sorcery",
        "primary_slots": ["ManaflowBand", "Transcendence", "Revitalize"],
        "secondary_tree": "Inspiration", "secondary_slots": ["BiscuitDelivery", "CosmicInsight"],
        "shards": ["Adaptive Force", "Armor", "Health Scaling"],
    }},
    "Leona": {"UTILITY": {
        "keystone": "Aftershock", "primary_tree": "Resolve",
        "primary_slots": ["FontOfLife", "BonePlating", "Overgrowth"],
        "secondary_tree": "Inspiration", "secondary_slots": ["BiscuitDelivery", "CosmicInsight"],
        "shards": ["Armor", "Armor", "Health Scaling"],
    }},
    "Soraka": {"UTILITY": {
        "keystone": "SummonAery", "primary_tree": "Sorcery",
        "primary_slots": ["ManaflowBand", "Transcendence", "Revitalize"],
        "secondary_tree": "Resolve", "secondary_slots": ["FontOfLife", "Revitalize"],
        "shards": ["Adaptive Force", "Armor", "Health Scaling"],
    }},
}

# ── BUILDS ────────────────────────────────────────────────────────────────────
# Los nombres de objetos se resuelven dinámicamente con Data Dragon.
# Formato: start (items iniciales), boots, core (3 objetos principales), situational (opciones)

BUILDS: dict[str, dict[str, dict]] = {
    # TOP
    "Darius": {"TOP": {
        "start": ["Doran's Shield", "Health Potion"],
        "boots": "Plated Steelcaps",
        "core": ["Trinity Force", "Sterak's Gage", "Death's Dance"],
        "situational": ["Spirit Visage", "Warmog's Armor", "Randuin's Omen"],
        "note": "Trinity Force es tu primer spike. Peleas cortas y agresivas ganan el laning.",
    }},
    "Aatrox": {"TOP": {
        "start": ["Doran's Shield", "Health Potion"],
        "boots": "Plated Steelcaps",
        "core": ["Goredrinker", "Death's Dance", "Sterak's Gage"],
        "situational": ["Spirit Visage", "Frozen Heart", "Black Cleaver"],
        "note": "Goredrinker te da sustain en pelea. Espera a nivel 9 para empezar a dominar.",
    }},
    "Garen": {"TOP": {
        "start": ["Doran's Shield", "Health Potion"],
        "boots": "Plated Steelcaps",
        "core": ["Trinity Force", "Warmog's Armor", "Sunfire Aegis"],
        "situational": ["Wit's End", "Force of Nature", "Mortal Reminder"],
        "note": "Warmog's te permite ignorar mana y regenerar vida entre peleas.",
    }},
    "Jax": {"TOP": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Plated Steelcaps",
        "core": ["Trinity Force", "Blade of the Ruined King", "Sterak's Gage"],
        "situational": ["Death's Dance", "Wit's End", "Spear of Shojin"],
        "note": "Con Trinity Force eres una amenaza enorme. Tradea siempre con E activa.",
    }},
    "Irelia": {"TOP": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Plated Steelcaps",
        "core": ["Trinity Force", "Blade of the Ruined King", "Sterak's Gage"],
        "situational": ["Death's Dance", "Wit's End", "Spear of Shojin"],
        "note": "Rush Trinity Force. Necesitas 2 stacks de Q para iniciar tradeos.",
    }},
    "Camille": {"TOP": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["Trinity Force", "Spear of Shojin", "Death's Dance"],
        "situational": ["Sterak's Gage", "Ravenous Hydra", "Frozen Heart"],
        "note": "E-W-Q-AA es tu combo de daño. Usa la ult para aislar carries.",
    }},
    "Malphite": {"TOP": {
        "start": ["Doran's Ring", "Health Potion"],
        "boots": "Sorcerer's Shoes",
        "core": ["Sunfire Aegis", "Zhonya's Hourglass", "Shadowflame"],
        "situational": ["Rabadon's Deathcap", "Void Staff", "Frozen Heart"],
        "note": "AP Malphite hace daño enorme con ult. Pokea con Q y conserva mana.",
    }},
    "Renekton": {"TOP": {
        "start": ["Doran's Shield", "Health Potion"],
        "boots": "Plated Steelcaps",
        "core": ["Sunfire Aegis", "Black Cleaver", "Sterak's Gage"],
        "situational": ["Death's Dance", "Spirit Visage", "Frozen Heart"],
        "note": "Dominas el early game. Cierra la partida antes del late (caes en escala).",
    }},
    # JUNGLE
    "LeeSin": {"JUNGLE": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["Black Cleaver", "Sterak's Gage", "Death's Dance"],
        "situational": ["Serylda's Grudge", "Ravenous Hydra", "Guardian Angel"],
        "note": "Tu poder está en el early. Q-W-Insec-R es el combo que decide las peleas.",
    }},
    "Viego": {"JUNGLE": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Plated Steelcaps",
        "core": ["Blade of the Ruined King", "Kraken Slayer", "Infinity Edge"],
        "situational": ["Wit's End", "Ravenous Hydra", "Sterak's Gage"],
        "note": "Farm eficientemente hasta poseer a alguien con R. Tu passive te regenera vida.",
    }},
    "Kayn": {"JUNGLE": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Plated Steelcaps",
        "core": ["Goredrinker", "Sterak's Gage", "Death's Dance"],
        "situational": ["Spirit Visage", "Ravenous Hydra", "Black Cleaver"],
        "note": "Rhaast (rojo) contra equipo con muchos tanques; Shadow Assassin (azul) contra squishies.",
    }},
    "Warwick": {"JUNGLE": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Plated Steelcaps",
        "core": ["Trinity Force", "Sterak's Gage", "Wit's End"],
        "situational": ["Spirit Visage", "Warmog's Armor", "Frozen Heart"],
        "note": "Tu W marca objetivos con poca vida. Gankea carriles cuando los enemigos están debilitados.",
    }},
    "Graves": {"JUNGLE": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Plated Steelcaps",
        "core": ["Trinity Force", "Kraken Slayer", "Death's Dance"],
        "situational": ["Sterak's Gage", "Guardian Angel", "Serylda's Grudge"],
        "note": "Juega como carry de jungla. Farmea eficientemente y entra a peleas desde flancos.",
    }},
    # MIDDLE
    "Ahri": {"MIDDLE": {
        "start": ["Doran's Ring", "Health Potion"],
        "boots": "Sorcerer's Shoes",
        "core": ["Luden's Echo", "Shadowflame", "Rabadon's Deathcap"],
        "situational": ["Zhonya's Hourglass", "Void Staff", "Cosmic Drive"],
        "note": "E-Q combo para all-in. Usa R para perseguir o escapar. Rota a carriles tras first blood.",
    }},
    "Zed": {"MIDDLE": {
        "start": ["Long Sword", "Long Sword", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["The Collector", "Serpent's Fang", "Serylda's Grudge"],
        "situational": ["Edge of Night", "Guardian Angel", "Death's Dance"],
        "note": "W-E-Q-AA-R-AA-E-Q es tu combo completo. Mata antes que el Zhonya's tenga efecto.",
    }},
    "Syndra": {"MIDDLE": {
        "start": ["Doran's Ring", "Health Potion"],
        "boots": "Sorcerer's Shoes",
        "core": ["Luden's Echo", "Shadowflame", "Rabadon's Deathcap"],
        "situational": ["Void Staff", "Zhonya's Hourglass", "Horizon Focus"],
        "note": "Q-E-R para instakill squishies. Acumula esferas con Q antes de usar ult.",
    }},
    "Viktor": {"MIDDLE": {
        "start": ["Doran's Ring", "Health Potion"],
        "boots": "Sorcerer's Shoes",
        "core": ["Luden's Echo", "Cosmic Drive", "Rabadon's Deathcap"],
        "situational": ["Void Staff", "Zhonya's Hourglass", "Shadowflame"],
        "note": "Mejora habilidades en orden: E-Q-W. Tu E amplificada con lag es devastadora.",
    }},
    "Leblanc": {"MIDDLE": {
        "start": ["Doran's Ring", "Health Potion"],
        "boots": "Sorcerer's Shoes",
        "core": ["Luden's Echo", "Shadowflame", "Rabadon's Deathcap"],
        "situational": ["Zhonya's Hourglass", "Void Staff", "Horizon Focus"],
        "note": "W-Q-E-R es tu combo estándar. Nunca te comprometas sin poder escapar con W.",
    }},
    "Orianna": {"MIDDLE": {
        "start": ["Doran's Ring", "Health Potion"],
        "boots": "Sorcerer's Shoes",
        "core": ["Luden's Echo", "Shadowflame", "Rabadon's Deathcap"],
        "situational": ["Zhonya's Hourglass", "Void Staff", "Cosmic Drive"],
        "note": "Tu ult es el teamfight más poderoso del juego. Posiciona la bola para maximizar hits.",
    }},
    "Yasuo": {"MIDDLE": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Berserker's Greaves",
        "core": ["Infinity Edge", "Kraken Slayer", "Immortal Shieldbow"],
        "situational": ["Wit's End", "Guardian Angel", "Death's Dance"],
        "note": "Necesitas un CC aéreo aliado para usar E-R. Farmea bajo torre si estás perdiendo.",
    }},
    # ADC
    "Jinx": {"BOTTOM": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Berserker's Greaves",
        "core": ["Kraken Slayer", "Runaan's Hurricane", "Infinity Edge"],
        "situational": ["Lord Dominik's Regards", "Mortal Reminder", "Guardian Angel"],
        "note": "Eres la carry de late game más fuerte. Farm hasta 3 items y entonces dominas.",
    }},
    "Caitlyn": {"BOTTOM": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Berserker's Greaves",
        "core": ["Kraken Slayer", "Galeforce", "Infinity Edge"],
        "situational": ["Lord Dominik's Regards", "Mortal Reminder", "Rapid Firecannon"],
        "note": "Dominas el early con tu rango. Coloca trampas bajo estructuras enemigas.",
    }},
    "Jhin": {"BOTTOM": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Galeforce",
        "core": ["Galeforce", "Rapid Firecannon", "Infinity Edge"],
        "situational": ["Mortal Reminder", "Lord Dominik's Regards", "Collector"],
        "note": "La cuarta bala hace crítico y ralentiza. Sinergiza con supports con CC para W.",
    }},
    "MissFortune": {"BOTTOM": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Berserker's Greaves",
        "core": ["Kraken Slayer", "Runaan's Hurricane", "Infinity Edge"],
        "situational": ["Mortal Reminder", "Lord Dominik's Regards", "Serylda's Grudge"],
        "note": "R en choke points con tu support es devastador. Úsala tras un engage masivo.",
    }},
    "Kaisa": {"BOTTOM": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Berserker's Greaves",
        "core": ["Kraken Slayer", "Rabadon's Deathcap", "Guinsoo's Rageblade"],
        "situational": ["Void Staff", "Nashor's Tooth", "Immortal Shieldbow"],
        "note": "Mejora W para AP burst, Q para AD bruiser. Entra en peleas con E tras un CC aliado.",
    }},
    "Ashe": {"BOTTOM": {
        "start": ["Doran's Blade", "Health Potion"],
        "boots": "Berserker's Greaves",
        "core": ["Kraken Slayer", "Runaan's Hurricane", "Infinity Edge"],
        "situational": ["Lord Dominik's Regards", "Mortal Reminder", "Wit's End"],
        "note": "Tu R es un CC global. Úsala para iniciar o para detener fugas. Kita siempre.",
    }},
    "Ezreal": {"BOTTOM": {
        "start": ["Tear of the Goddess", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["Trinity Force", "Manamune", "Serylda's Grudge"],
        "situational": ["Death's Dance", "Guardian Angel", "Ravenous Hydra"],
        "note": "No te pelees en el early. Farmea con Q y crece con Manamune para mid/late.",
    }},
    # SUPPORT
    "Thresh": {"UTILITY": {
        "start": ["Relic Shield", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["Locket of the Iron Solari", "Shurelya's Battlesong", "Redemption"],
        "situational": ["Frozen Heart", "Knight's Vow", "Staff of Flowing Water"],
        "note": "Q es tu mejor herramienta. Usa el farol (E) para salvar carries en situaciones difíciles.",
    }},
    "Nautilus": {"UTILITY": {
        "start": ["Relic Shield", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["Locket of the Iron Solari", "Shurelya's Battlesong", "Redemption"],
        "situational": ["Knight's Vow", "Frozen Heart", "Warmog's Armor"],
        "note": "Q-AA-E-R es tu combo de CC en cadena. Casi nadie escapa. Inicia peleas con confianza.",
    }},
    "Lulu": {"UTILITY": {
        "start": ["Spellthief's Edge", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["Shurelya's Battlesong", "Staff of Flowing Water", "Redemption"],
        "situational": ["Moonstone Renewer", "Ardent Censer", "Chemtech Putrifier"],
        "note": "R es el escudo más poderoso del juego para carries. W convierte amenazas en ardillas.",
    }},
    "Janna": {"UTILITY": {
        "start": ["Spellthief's Edge", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["Shurelya's Battlesong", "Staff of Flowing Water", "Redemption"],
        "situational": ["Ardent Censer", "Moonstone Renewer", "Chemtech Putrifier"],
        "note": "R desengaja peleas y cura al equipo. Usa Q para interrumpir carreras enemigas.",
    }},
    "Blitzcrank": {"UTILITY": {
        "start": ["Relic Shield", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["Locket of the Iron Solari", "Shurelya's Battlesong", "Knight's Vow"],
        "situational": ["Frozen Heart", "Zeke's Convergence", "Redemption"],
        "note": "Una Q que conecta = kill casi garantizado. Pega a los flancos para sorprender.",
    }},
    "Morgana": {"UTILITY": {
        "start": ["Spellthief's Edge", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["Chemtech Putrifier", "Zhonya's Hourglass", "Shadowflame"],
        "situational": ["Void Staff", "Rabadon's Deathcap", "Shurelya's Battlesong"],
        "note": "E cancela cualquier CC enemigo. Usa Q para hacer pelar a tu ADC libremente.",
    }},
    "Leona": {"UTILITY": {
        "start": ["Relic Shield", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["Locket of the Iron Solari", "Shurelya's Battlesong", "Knight's Vow"],
        "situational": ["Frozen Heart", "Zeke's Convergence", "Redemption"],
        "note": "E-Q-AA-R es tu combo. Eres el initiator más agresivo del juego. Atrévete a entrar.",
    }},
    "Soraka": {"UTILITY": {
        "start": ["Spellthief's Edge", "Health Potion"],
        "boots": "Ionian Boots of Lucidity",
        "core": ["Moonstone Renewer", "Staff of Flowing Water", "Redemption"],
        "situational": ["Chemtech Putrifier", "Ardent Censer", "Mikael's Blessing"],
        "note": "R cura a todo el equipo globalmente. Úsala cuando alguien baje del 30-40% de vida.",
    }},
}

# ── CONSEJOS POR ARQUETIPO ────────────────────────────────────────────────────
# Clave: (tipo_jugador, tipo_rival)
# Tipos de Data Dragon: Fighter, Tank, Mage, Assassin, Marksman, Support

ARCHETYPE_ADVICE: dict[tuple, dict] = {
    ("Fighter", "Fighter"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "Matchup de tradeos cortos y agresivos. Gana quien tenga mejor timing.",
        "tips": [
            "Pelea cuando tengas E o habilidad de CC activa — evita tradeos cuando tus CDs están en espera.",
            "El primer objeto de poder determina quién gana el nivel 9+. Rush tu item core.",
            "Si pierdes el nivel 1-3, juega en wave management defensivo hasta tu primer back.",
        ],
        "items_note": "Considera Sterak's Gage para la resistencia en tradeos extendidos.",
    },
    ("Fighter", "Tank"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "Los tanks aguantan bien pero tú escalaS mejor. Tradeos cortos frecuentes.",
        "tips": [
            "Tradea rápido y retírate antes que puedan usar su CC principal.",
            "Conqueror / Black Cleaver son esenciales para romper su armadura.",
            "Empuja oleadas y busca el 1v1 — tienes más daño pero ellos duran más.",
        ],
        "items_note": "Black Cleaver o Serylda's Grudge para penetrar su resistencia física.",
    },
    ("Fighter", "Mage"): {
        "difficulty": "Favorable",
        "color": "#10b981",
        "overview": "Puedes cerrar la distancia fácilmente. Su daño es más intenso pero tienes sustain.",
        "tips": [
            "Acercarte es tu condición de victoria. Una vez en melee, controlan poco.",
            "Esquiva el skillshot principal antes de entrar — es su única defensa real.",
            "Mercury's Treads o Spirit Visage si tienen mucho AP.",
        ],
        "items_note": "Spirit Visage / Wit's End para reducir su daño mágico y ganar sustain.",
    },
    ("Fighter", "Assassin"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "Ambos pueden all-in. El asesino tiene más burst, tú tienes más sustain.",
        "tips": [
            "No te dejes burstar con los CDs disponibles. Tradeala cuando use una habilidad.",
            "Sterak's Gage te salva de la mayoría de combos de asesino.",
            "Pelea dentro de la minion wave — su movilidad se limita en espacios reducidos.",
        ],
        "items_note": "Sterak's Gage y Death's Dance reducen el burst de asesinos enormemente.",
    },
    ("Fighter", "Marksman"): {
        "difficulty": "Favorable",
        "color": "#10b981",
        "overview": "Si llegas hasta ellos, es un kill casi garantizado. Tu trabajo es cerrar la distancia.",
        "tips": [
            "Evita su kiting. Usa tus habilidades de gap-close para pegarte a ellos.",
            "Nunca entres en su rango sin plan de escape — la distancia es su ventaja.",
            "Flanquea en teamfights para llegar a ellos por sorpresa.",
        ],
        "items_note": "Galeforce o Stridebreaker para reducir la distancia rápidamente.",
    },
    ("Tank", "Tank"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "Matchup largo y lento de farmeo. Quien tenga mejor macro gana.",
        "tips": [
            "No te arriesgues a peleas 1v1 largas. Ninguno de los dos suele ganar limpiamente.",
            "Prioriza TP-ganks a otros carriles si tu carril está equilibrado.",
            "Empuja oleadas y busca objetivos globales.",
        ],
        "items_note": "Heartsteel escala bien en matchups de tank vs tank.",
    },
    ("Tank", "Fighter"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "Los luchadores tienen más daño pero tú aguantas más. Tradeos largos te benefician.",
        "tips": [
            "Aguanta sus tradeos cortos y responde con CC cuando ataquen.",
            "Tendrás más utilidad en teamfights que en el 1v1 de línea.",
            "CC de bajo cooldown = tu mejor arma.",
        ],
        "items_note": "Frozen Heart contra carries AD. Hollow Radiance contra múltiples amenazas.",
    },
    ("Tank", "Mage"): {
        "difficulty": "Favorable",
        "color": "#10b981",
        "overview": "Tu resistencia mágica te protege de su daño. Cierra la distancia y domina.",
        "tips": [
            "Corre hacia ellos después de su habilidad principal — están en cooldown.",
            "Force of Nature te convierte en inmune a su poke AP.",
            "En teamfights, engánchate al carry AP enemigo para eliminar su amenaza.",
        ],
        "items_note": "Force of Nature / Abyssal Mask para maximizar resistencia mágica.",
    },
    ("Tank", "Assassin"): {
        "difficulty": "Muy Favorable",
        "color": "#34d399",
        "overview": "Los asesinos no pueden matar a un tank bien construido. Sé muy agresivo.",
        "tips": [
            "Entra en ellos con confianza — su burst no te eliminará con la build correcta.",
            "CC constante cuando entren — no pueden escapar fácilmente.",
            "Itemiza Warmog's para regenerar entre peleas.",
        ],
        "items_note": "Warmog's Armor para regenerar en retorno. Randuin's Omen contra crit.",
    },
    ("Tank", "Marksman"): {
        "difficulty": "Desfavorable",
        "color": "#ef4444",
        "overview": "Raro en laning phase. Su daño sostenido eventualmente atraviesa tu armadura.",
        "tips": [
            "Cierra la distancia constantemente — en melee, no pueden hacer nada.",
            "Randuin's Omen reduce su critical strike damage.",
            "Inicia peleas desde ángulos inesperados para que no puedan kitearte.",
        ],
        "items_note": "Randuin's Omen y Thornmail limitan su efectividad en peleas largas.",
    },
    ("Mage", "Fighter"): {
        "difficulty": "Desfavorable",
        "color": "#ef4444",
        "overview": "Pueden cerrarte la distancia. Juega seguro y castiga desde lejos cuando puedas.",
        "tips": [
            "Usa las minions como barrera. Nunca iguales su posición.",
            "Zhonya's Hourglass es obligatorio si pueden engancharte.",
            "Pokea con habilidades de largo alcance sin entrar en su zona de peligro.",
        ],
        "items_note": "Zhonya's Hourglass salva de cualquier engage. Arrastrable para todos los matchups de fighter.",
    },
    ("Mage", "Tank"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "La resistencia mágica los protege pero tu poke los desgasta a largo plazo.",
        "tips": [
            "Void Staff al 3er item para romper su MR acumulada.",
            "Pokea constantemente pero gestiona tu mana — los tankeos duran mucho.",
            "Usa CC para forzarles a gastar dinero en Tenacity.",
        ],
        "items_note": "Void Staff es imprescindible. Horizon Focus para amplificar el daño en CC.",
    },
    ("Mage", "Mage"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "Quien acierte primero los skillshots suele ganar. Gestión de wave y poke son clave.",
        "tips": [
            "Conserva mana para tradeos — lanzar todo sin ton ni son te deja indefenso.",
            "Aprende el patrón de movimiento enemigo para acertar tus CC.",
            "El primero en conseguir Luden's / Shadowflame suele llevar el control.",
        ],
        "items_note": "Shadowflame da ventaja en burst en matchups de mago vs mago.",
    },
    ("Mage", "Assassin"): {
        "difficulty": "Muy Desfavorable",
        "color": "#dc2626",
        "overview": "Te matan antes de que puedas hacer nada. Zhonya's y positioning son tu vida.",
        "tips": [
            "Zhonya's Hourglass es tu primer item obligatorio en este matchup.",
            "Juega detrás de minions y nunca uses tus habilidades predeciblemente.",
            "Pide ganks al jungla — si el asesino se snowballea, la partida se acaba.",
        ],
        "items_note": "Zhonya's Hourglass SIEMPRE. Crown of the Shattered Queen da otro escudo de vida.",
    },
    ("Mage", "Marksman"): {
        "difficulty": "Favorable",
        "color": "#10b981",
        "overview": "Tu CC les impide kitearte. Un combo completo los elimina si conectas.",
        "tips": [
            "Entra cuando hayan usado su habilidad de escape (Ezreal E, etc.).",
            "Tu CC de ráfaga es más impactante que su DPS sostenido.",
            "Pokea de forma segura y espera el momento para el all-in.",
        ],
        "items_note": "Build estándar. Morellonomicon si tienen mucho healing.",
    },
    ("Assassin", "Mage"): {
        "difficulty": "Favorable",
        "color": "#10b981",
        "overview": "Son tu presa natural. Espera nivel 6, baitea sus CDs y mata.",
        "tips": [
            "Farmea seguro antes del 6. Nunca entres si tienen CC disponible.",
            "Baitea su habilidad principal (Flash/CC) antes del all-in.",
            "Si compran Zhonya's, espera a que expire para continuar el combo.",
        ],
        "items_note": "Serpent's Fang contra escudos. The Collector para ejecutar con poca vida.",
    },
    ("Assassin", "Tank"): {
        "difficulty": "Muy Desfavorable",
        "color": "#dc2626",
        "overview": "Tu daño de burst no sirve contra tanks. Ignóralo y rota a otros carriles.",
        "tips": [
            "No pierdas el tiempo intentando matarle. Roam a mid/bot.",
            "Concéntrate en los carries enemigos en teamfights.",
            "Itemiza Armor Pen si es indispensable dañarle.",
        ],
        "items_note": "Serylda's Grudge o Lord Dominik's si necesitas dañar tanques.",
    },
    ("Assassin", "Fighter"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "Ellos pueden aguantar tu burst. Necesitas el combo perfecto para ganar.",
        "tips": [
            "Espera a que usen Sterak's o su sustain antes de comprometerte.",
            "Flanquea desde ángulos inesperados en teamfights.",
            "Edge of Night o Serpent's Fang contrarrestan sus escudos.",
        ],
        "items_note": "Serpent's Fang si tienen escudos. Edge of Night contra Sterak's.",
    },
    ("Assassin", "Assassin"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "El primero en atacar suele ganar. Paciencia y posicionamiento son clave.",
        "tips": [
            "Nunca inicies hasta tener ventaja clara (habilidades disponibles, nivel).",
            "Usa el control de oleadas para crear rangos de seguridad.",
            "Quien domina la wave tiene el control del matchup.",
        ],
        "items_note": "Stopwatch o Zhonya's como first spike defensivo si va mal.",
    },
    ("Assassin", "Marksman"): {
        "difficulty": "Favorable",
        "color": "#10b981",
        "overview": "Tu objetivo prioritario. Mátalos en 0.5 segundos antes de que puedan reaccionar.",
        "tips": [
            "Espera que usen su Galeforce o escape antes del all-in.",
            "En teamfights, siempre busca al carry físico. No te distraigas.",
            "Flanquea por los bordes del mapa para maximizar el elemento sorpresa.",
        ],
        "items_note": "The Collector para ejecuciones. Serpent's Fang contra Immortal Shieldbow.",
    },
    ("Marksman", "Tank"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "Con el tiempo y los objetos correctos, atraviesas cualquier tank.",
        "tips": [
            "Lord Dominik's o Kraken Slayer son obligatorios contra tanks.",
            "Nunca te acerques — kita constantemente mientras dispara.",
            "En teamfights, si el tank engaña, cambia de target al carry.",
        ],
        "items_note": "Lord Dominik's Regards + Kraken Slayer para penetración de armadura.",
    },
    ("Marksman", "Fighter"): {
        "difficulty": "Desfavorable",
        "color": "#ef4444",
        "overview": "Si llegan a ti, mueres. Necesitas support y posicionamiento para sobrevivir.",
        "tips": [
            "Juega detrás del support. Nunca seas el más adelantado.",
            "Kita constantemente — Galeforce o Flash para escapar de su engage.",
            "En teamfights, dispara desde atrás. Si alguien te engacha, usa tu escape.",
        ],
        "items_note": "Galeforce para escape o reposicionamiento. Phantom Dancer da un escudo de vida.",
    },
    ("Marksman", "Assassin"): {
        "difficulty": "Muy Desfavorable",
        "color": "#dc2626",
        "overview": "Morirás instantáneamente si te alcanzan. Nunca estés solo.",
        "tips": [
            "Nunca te separes del support o del equipo.",
            "Pide al jungla que wardee los flancos.",
            "Immortal Shieldbow puede salvarte de un burst completo de asesino.",
        ],
        "items_note": "Immortal Shieldbow SIEMPRE contra asesinos. Phantom Dancer da escudo extra.",
    },
    ("Marksman", "Marksman"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "Depende del alcance, kiting y la sinergia con el support.",
        "tips": [
            "El que llega primero al spike de Kraken/IE + segundo item generalmente gana.",
            "Prioriza farmeo sobre pokes inútiles — la economía decide este matchup.",
            "El support con más CC gana el 2v2.",
        ],
        "items_note": "Build estándar. Mortal Reminder si tienen healing.",
    },
    ("Support", "Support"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "El matchup de soporte lo decide la sinergia con el ADC y el control de visión.",
        "tips": [
            "Wardea el tribush y el río desde el inicio. La visión determina los ganks.",
            "Si tienes más CC, sé agresivo. Si tienes más sustain, juega conservador.",
            "Busca al support enemigo en teamfights para negarle sus habilidades.",
        ],
        "items_note": "Chemtech Putrifier contra apoyo de healing. Mikael's contra un CC crítico.",
    },
    ("Support", "Fighter"): {
        "difficulty": "Desfavorable",
        "color": "#ef4444",
        "overview": "Los fighters son duros y difíciles de CC. Protege a tu ADC.",
        "tips": [
            "No inicies 1v1 contra el soporte rival que vaya de fighter.",
            "Juega para tu ADC — shields y heals en lugar de initiation.",
            "Pide al jungla que vigile el bot lane.",
        ],
        "items_note": "Locket of the Iron Solari para proteger al equipo de bursts de fighter.",
    },
    ("Support", "Assassin"): {
        "difficulty": "Muy Desfavorable",
        "color": "#dc2626",
        "overview": "Si el asesino llega a tu ADC, no puedes hacer nada. Control de visión es vital.",
        "tips": [
            "Wardea el tribush y los flancos SIEMPRE.",
            "Protege con escudos cuando el asesino entre.",
            "Mikael's Blessing cancela el snare del campeón enemigo para salvar al ADC.",
        ],
        "items_note": "Mikael's Blessing y Locket como prioridades contra equipos con asesinos.",
    },
    ("Support", "Mage"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "El poke mágico puede ser molesto. Usa tus heals/shields eficientemente.",
        "tips": [
            "Absorbe su poke con escudos antes de que llegue al ADC.",
            "Chemtech Putrifier para reducir su healing si tienen sustain.",
            "Roam a mid cuando la ola esté empujada.",
        ],
        "items_note": "Mikael's Blessing contra CC de mago. Chemtech contra healing.",
    },
    ("Support", "Tank"): {
        "difficulty": "Favorable",
        "color": "#10b981",
        "overview": "Un engage de tank vs un support de engage es intenso pero manejable.",
        "tips": [
            "Counterinitia cuando fallen su CC principal.",
            "Shurelya's para reposicionar al equipo en engage/disengage.",
            "En teamfights, protege al carry más que al tank.",
        ],
        "items_note": "Shurelya's Battlesong para movilidad de equipo. Locket para supervivencia.",
    },
    ("Support", "Marksman"): {
        "difficulty": "Neutral",
        "color": "#f59e0b",
        "overview": "Raro en soporte. Si sucede, tu CC supera su DPS sostenido.",
        "tips": [
            "CC = win. Un engage limpio elimina cualquier marksman.",
            "No te pongas en rango de sus proyectiles.",
            "Trabaja con tu ADC para presionar su ADC.",
        ],
        "items_note": "Locket + Shurelya's estándar.",
    },
}

# ── FUNCIONES ─────────────────────────────────────────────────────────────────

_ROLE_TO_POS = {
    "Top": "TOP", "Jungla": "JUNGLE", "Mid": "MIDDLE", "ADC": "BOTTOM", "Support": "UTILITY"
}

def get_rune_page(champion_dd: str, role_pos: str) -> dict | None:
    """Devuelve la página de runas del campeón en ese rol, o None si no hay dato."""
    champ_data = RUNE_PAGES.get(champion_dd, {})
    return champ_data.get(role_pos)

def get_build(champion_dd: str, role_pos: str) -> dict | None:
    """Devuelve el build del campeón en ese rol, o None si no hay dato."""
    champ_data = BUILDS.get(champion_dd, {})
    return champ_data.get(role_pos)

def get_matchup_advice(my_type: str, enemy_type: str) -> dict:
    """Devuelve el consejo de matchup por arque tipo. Busca (my, enemy) y fallback a generic."""
    advice = ARCHETYPE_ADVICE.get((my_type, enemy_type))
    if advice:
        return advice
    # Fallback genérico
    return {
        "difficulty": "Neutral",
        "color": "#94a3b8",
        "overview": f"Matchup de {my_type} contra {enemy_type}. Adapta tu juego según el estado de la partida.",
        "tips": [
            "Analiza las fortalezas y debilidades de ambos campeones en cada fase.",
            "El control de oleadas y la visión son ventajas universales.",
            "Adapta tus items según cómo evolucione la partida.",
        ],
        "items_note": "Ajusta la build según el daño del rival (armadura vs MR).",
    }

def get_primary_type(tags: list[str]) -> str:
    """Extrae el tipo principal de un campeón a partir de sus tags de Data Dragon.
    Data Dragon ordena los tags del más al menos representativo, así que usamos el primero."""
    return tags[0] if tags else "Fighter"
