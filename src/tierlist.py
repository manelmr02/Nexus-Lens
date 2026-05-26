CURRENT_PATCH = "16.10"

TIER_COLORS = {
    "S+": "#ff4444",
    "S":  "#ff8800",
    "A":  "#ffcc00",
    "B":  "#88cc00",
    "C":  "#aaaaaa",
}

TIER_LIST = {
    "TOP": {
        "S+": [
            {"name": "Darius", "dd": "Darius", "wr": 52.3, "pr": 8.1, "br": 12.5},
            {"name": "Garen", "dd": "Garen", "wr": 53.1, "pr": 7.2, "br": 8.3},
            {"name": "Camille", "dd": "Camille", "wr": 51.8, "pr": 9.5, "br": 15.2},
        ],
        "S": [
            {"name": "Aatrox", "dd": "Aatrox", "wr": 51.2, "pr": 11.3, "br": 18.7},
            {"name": "Fiora", "dd": "Fiora", "wr": 50.9, "pr": 6.8, "br": 9.1},
            {"name": "Malphite", "dd": "Malphite", "wr": 51.5, "pr": 5.9, "br": 7.2},
            {"name": "Renekton", "dd": "Renekton", "wr": 50.7, "pr": 8.4, "br": 11.3},
        ],
        "A": [
            {"name": "Irelia", "dd": "Irelia", "wr": 49.8, "pr": 7.9, "br": 13.5},
            {"name": "Jax", "dd": "Jax", "wr": 49.5, "pr": 9.1, "br": 10.2},
            {"name": "Mordekaiser", "dd": "Mordekaiser", "wr": 50.4, "pr": 6.2, "br": 8.9},
            {"name": "Sion", "dd": "Sion", "wr": 50.2, "pr": 4.5, "br": 5.8},
        ],
        "B": [
            {"name": "Cho'Gath", "dd": "Chogath", "wr": 49.1, "pr": 3.2, "br": 3.1},
            {"name": "Teemo", "dd": "Teemo", "wr": 49.3, "pr": 4.8, "br": 6.1},
            {"name": "Nasus", "dd": "Nasus", "wr": 48.7, "pr": 5.1, "br": 4.2},
        ],
        "C": [
            {"name": "Rumble", "dd": "Rumble", "wr": 48.1, "pr": 2.9, "br": 3.8},
            {"name": "Heimerdinger", "dd": "Heimerdinger", "wr": 47.8, "pr": 1.5, "br": 2.1},
        ],
    },
    "JUNGLE": {
        "S+": [
            {"name": "Viego", "dd": "Viego", "wr": 52.8, "pr": 9.3, "br": 14.1},
            {"name": "Kayn", "dd": "Kayn", "wr": 51.9, "pr": 8.7, "br": 12.3},
            {"name": "Lee Sin", "dd": "LeeSin", "wr": 50.8, "pr": 14.5, "br": 20.1},
        ],
        "S": [
            {"name": "Jarvan IV", "dd": "JarvanIV", "wr": 51.3, "pr": 7.1, "br": 9.8},
            {"name": "Vi", "dd": "Vi", "wr": 51.7, "pr": 6.8, "br": 8.2},
            {"name": "Graves", "dd": "Graves", "wr": 51.1, "pr": 8.3, "br": 11.7},
            {"name": "Hecarim", "dd": "Hecarim", "wr": 51.5, "pr": 7.5, "br": 10.3},
        ],
        "A": [
            {"name": "Warwick", "dd": "Warwick", "wr": 52.1, "pr": 5.9, "br": 6.1},
            {"name": "Amumu", "dd": "Amumu", "wr": 52.3, "pr": 7.8, "br": 9.5},
            {"name": "Xin Zhao", "dd": "XinZhao", "wr": 51.8, "pr": 6.2, "br": 7.8},
            {"name": "Rammus", "dd": "Rammus", "wr": 53.1, "pr": 4.1, "br": 5.2},
        ],
        "B": [
            {"name": "Ekko", "dd": "Ekko", "wr": 49.8, "pr": 6.7, "br": 8.9},
            {"name": "Diana", "dd": "Diana", "wr": 50.1, "pr": 5.8, "br": 7.1},
            {"name": "Shyvana", "dd": "Shyvana", "wr": 50.9, "pr": 3.5, "br": 4.2},
        ],
        "C": [
            {"name": "Ivern", "dd": "Ivern", "wr": 49.2, "pr": 1.8, "br": 2.3},
            {"name": "Taliyah", "dd": "Taliyah", "wr": 48.9, "pr": 3.1, "br": 4.8},
        ],
    },
    "MIDDLE": {
        "S+": [
            {"name": "Ahri", "dd": "Ahri", "wr": 51.9, "pr": 10.2, "br": 16.3},
            {"name": "Veigar", "dd": "Veigar", "wr": 52.7, "pr": 6.9, "br": 10.2},
            {"name": "Syndra", "dd": "Syndra", "wr": 52.1, "pr": 7.8, "br": 13.5},
        ],
        "S": [
            {"name": "Viktor", "dd": "Viktor", "wr": 51.8, "pr": 8.1, "br": 14.2},
            {"name": "Orianna", "dd": "Orianna", "wr": 51.4, "pr": 6.3, "br": 9.7},
            {"name": "LeBlanc", "dd": "Leblanc", "wr": 50.9, "pr": 7.5, "br": 12.8},
            {"name": "Zed", "dd": "Zed", "wr": 50.2, "pr": 9.8, "br": 17.3},
        ],
        "A": [
            {"name": "Sylas", "dd": "Sylas", "wr": 50.7, "pr": 8.9, "br": 13.1},
            {"name": "Fizz", "dd": "Fizz", "wr": 50.5, "pr": 5.2, "br": 8.9},
            {"name": "Lux", "dd": "Lux", "wr": 50.1, "pr": 7.9, "br": 9.3},
            {"name": "Akali", "dd": "Akali", "wr": 49.8, "pr": 10.1, "br": 18.7},
        ],
        "B": [
            {"name": "Yasuo", "dd": "Yasuo", "wr": 49.3, "pr": 13.2, "br": 19.5},
            {"name": "Annie", "dd": "Annie", "wr": 51.2, "pr": 3.8, "br": 5.1},
            {"name": "Twisted Fate", "dd": "TwistedFate", "wr": 49.7, "pr": 4.9, "br": 6.2},
        ],
        "C": [
            {"name": "Azir", "dd": "Azir", "wr": 47.2, "pr": 3.5, "br": 6.1},
            {"name": "Corki", "dd": "Corki", "wr": 48.1, "pr": 2.8, "br": 3.2},
        ],
    },
    "ADC": {
        "S+": [
            {"name": "Jinx", "dd": "Jinx", "wr": 52.5, "pr": 11.3, "br": 15.2},
            {"name": "Jhin", "dd": "Jhin", "wr": 51.8, "pr": 13.7, "br": 14.3},
            {"name": "Caitlyn", "dd": "Caitlyn", "wr": 51.2, "pr": 10.8, "br": 12.7},
        ],
        "S": [
            {"name": "Ashe", "dd": "Ashe", "wr": 51.9, "pr": 9.5, "br": 10.8},
            {"name": "Miss Fortune", "dd": "MissFortune", "wr": 52.3, "pr": 8.9, "br": 9.1},
            {"name": "Kai'Sa", "dd": "Kaisa", "wr": 50.8, "pr": 15.1, "br": 18.9},
            {"name": "Tristana", "dd": "Tristana", "wr": 51.1, "pr": 7.2, "br": 8.3},
        ],
        "A": [
            {"name": "Sivir", "dd": "Sivir", "wr": 51.7, "pr": 5.8, "br": 6.9},
            {"name": "Lucian", "dd": "Lucian", "wr": 50.1, "pr": 9.7, "br": 13.5},
            {"name": "Vayne", "dd": "Vayne", "wr": 49.8, "pr": 8.2, "br": 10.3},
            {"name": "Xayah", "dd": "Xayah", "wr": 50.5, "pr": 7.1, "br": 9.8},
        ],
        "B": [
            {"name": "Ezreal", "dd": "Ezreal", "wr": 49.5, "pr": 16.3, "br": 12.1},
            {"name": "Draven", "dd": "Draven", "wr": 49.3, "pr": 5.9, "br": 8.2},
            {"name": "Samira", "dd": "Samira", "wr": 49.7, "pr": 7.8, "br": 12.4},
        ],
        "C": [
            {"name": "Twitch", "dd": "Twitch", "wr": 50.2, "pr": 4.1, "br": 5.7},
            {"name": "Kalista", "dd": "Kalista", "wr": 48.3, "pr": 3.2, "br": 5.9},
        ],
    },
    "SUPPORT": {
        "S+": [
            {"name": "Thresh", "dd": "Thresh", "wr": 51.3, "pr": 12.5, "br": 18.7},
            {"name": "Nautilus", "dd": "Nautilus", "wr": 52.1, "pr": 11.8, "br": 16.2},
            {"name": "Lulu", "dd": "Lulu", "wr": 52.8, "pr": 9.3, "br": 11.5},
        ],
        "S": [
            {"name": "Janna", "dd": "Janna", "wr": 53.2, "pr": 7.1, "br": 8.9},
            {"name": "Soraka", "dd": "Soraka", "wr": 52.9, "pr": 6.8, "br": 7.2},
            {"name": "Blitzcrank", "dd": "Blitzcrank", "wr": 51.7, "pr": 10.2, "br": 15.8},
            {"name": "Morgana", "dd": "Morgana", "wr": 51.5, "pr": 9.7, "br": 13.4},
        ],
        "A": [
            {"name": "Zilean", "dd": "Zilean", "wr": 53.4, "pr": 4.2, "br": 5.1},
            {"name": "Leona", "dd": "Leona", "wr": 50.8, "pr": 9.5, "br": 14.7},
            {"name": "Karma", "dd": "Karma", "wr": 51.1, "pr": 7.8, "br": 9.3},
            {"name": "Senna", "dd": "Senna", "wr": 50.5, "pr": 8.1, "br": 10.8},
        ],
        "B": [
            {"name": "Nami", "dd": "Nami", "wr": 51.9, "pr": 6.3, "br": 8.1},
            {"name": "Alistar", "dd": "Alistar", "wr": 50.7, "pr": 5.4, "br": 7.8},
            {"name": "Pyke", "dd": "Pyke", "wr": 49.8, "pr": 7.9, "br": 12.3},
        ],
        "C": [
            {"name": "Brand", "dd": "Brand", "wr": 49.1, "pr": 5.2, "br": 7.1},
            {"name": "Zyra", "dd": "Zyra", "wr": 49.8, "pr": 4.3, "br": 5.8},
        ],
    },
}
