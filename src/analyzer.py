from collections import defaultdict

POSITION_LABELS = {
    "TOP": "Top",
    "JUNGLE": "Jungla",
    "MIDDLE": "Mid",
    "BOTTOM": "ADC",
    "UTILITY": "Support",
    "": "Desconocido",
    "UNKNOWN": "Desconocido",
    "Invalid": "Otro",
}

class MatchAnalyzer:
    def __init__(self):
        self.thresholds = {
            "kda": 2.8, "damage_per_min": 700, "gold_per_min": 400,
            "vision_per_min": 1.3, "cs_per_min": 6.5,
        }

    def analyze_match(self, match_data: dict, puuid: str, timeline_data: dict = None) -> dict | None:
        info = match_data.get("info", {})
        duration_min = max(1, info.get("gameDuration", 60) / 60.0)

        player = next((p for p in info.get("participants", []) if p["puuid"] == puuid), None)
        if not player:
            return None

        team_id = player["teamId"]
        team_kills = max(1, sum(p["kills"] for p in info["participants"] if p["teamId"] == team_id))

        kills, deaths, assists = player["kills"], player["deaths"], player["assists"]
        kda = (kills + assists) / max(1, deaths)
        dmg_pm = player["totalDamageDealtToChampions"] / duration_min
        gold_pm = player["goldEarned"] / duration_min
        vision_pm = player["visionScore"] / duration_min
        total_cs = player.get("totalMinionsKilled", 0) + player.get("neutralMinionsKilled", 0)
        cs_pm = total_cs / duration_min
        kp = ((kills + assists) / team_kills) * 100
        position = player.get("teamPosition", "")

        items = [player.get(f"item{i}", 0) for i in range(6) if player.get(f"item{i}", 0) != 0]

        opponent = next(
            (p for p in info["participants"]
             if p["teamId"] != team_id and p.get("teamPosition") == position and position not in ("", "Invalid")),
            None
        )
        opponent_champion = opponent["championName"] if opponent else None

        gold_diff_15 = None
        if timeline_data and "info" in timeline_data:
            try:
                pid = player["participantId"]
                target_ts = 15 * 60000
                frame = next((f for f in timeline_data["info"]["frames"] if f["timestamp"] >= target_ts), None)
                if frame and opponent:
                    opp_pid = opponent["participantId"]
                    pg = frame["participantFrames"][str(pid)]["totalGold"]
                    og = frame["participantFrames"][str(opp_pid)]["totalGold"]
                    gold_diff_15 = pg - og
            except Exception:
                pass

        return {
            "match_id": match_data.get("metadata", {}).get("matchId", ""),
            "championName": player["championName"],
            "win": player["win"],
            "kills": kills, "deaths": deaths, "assists": assists,
            "kda": round(kda, 2),
            "damage_per_min": round(dmg_pm, 1),
            "gold_per_min": round(gold_pm, 1),
            "vision_per_min": round(vision_pm, 2),
            "cs_per_min": round(cs_pm, 1),
            "kill_participation": round(kp, 1),
            "gold_diff_15": gold_diff_15,
            "teamPosition": position,
            "position_label": POSITION_LABELS.get(position, position),
            "duration_min": round(duration_min, 1),
            "total_damage": player["totalDamageDealtToChampions"],
            "items": items,
            "opponent_champion": opponent_champion,
            "game_mode": info.get("gameMode", ""),
        }

    def aggregate_stats(self, matches: list) -> dict:
        if not matches:
            return {}
        n = len(matches)
        wins = sum(1 for m in matches if m["win"])
        return {
            "games": n,
            "wins": wins,
            "losses": n - wins,
            "win_rate": round((wins / n) * 100, 1),
            "avg_kda": round(sum(m["kda"] for m in matches) / n, 2),
            "avg_kills": round(sum(m["kills"] for m in matches) / n, 1),
            "avg_deaths": round(sum(m["deaths"] for m in matches) / n, 1),
            "avg_assists": round(sum(m["assists"] for m in matches) / n, 1),
            "avg_cs_pm": round(sum(m["cs_per_min"] for m in matches) / n, 1),
            "avg_damage_pm": round(sum(m["damage_per_min"] for m in matches) / n, 1),
            "avg_vision_pm": round(sum(m["vision_per_min"] for m in matches) / n, 2),
            "avg_kp": round(sum(m["kill_participation"] for m in matches) / n, 1),
        }

    def analyze_champion_stats(self, matches: list) -> list:
        champ_data = defaultdict(lambda: {"games": 0, "wins": 0, "kills": 0, "deaths": 0,
                                          "assists": 0, "cs_pm": 0, "dmg_pm": 0, "kp": 0})
        for m in matches:
            c = m["championName"]
            champ_data[c]["games"] += 1
            champ_data[c]["wins"] += 1 if m["win"] else 0
            champ_data[c]["kills"] += m["kills"]
            champ_data[c]["deaths"] += m["deaths"]
            champ_data[c]["assists"] += m["assists"]
            champ_data[c]["cs_pm"] += m["cs_per_min"]
            champ_data[c]["dmg_pm"] += m["damage_per_min"]
            champ_data[c]["kp"] += m["kill_participation"]

        result = []
        for champ, d in champ_data.items():
            g = d["games"]
            kda = (d["kills"] + d["assists"]) / max(1, d["deaths"])
            result.append({
                "champion": champ,
                "games": g,
                "wins": d["wins"],
                "losses": g - d["wins"],
                "win_rate": round((d["wins"] / g) * 100, 1),
                "kda": round(kda, 2),
                "avg_kills": round(d["kills"] / g, 1),
                "avg_deaths": round(d["deaths"] / g, 1),
                "avg_assists": round(d["assists"] / g, 1),
                "avg_cs_pm": round(d["cs_pm"] / g, 1),
                "avg_dmg_pm": round(d["dmg_pm"] / g, 0),
                "avg_kp": round(d["kp"] / g, 1),
            })
        return sorted(result, key=lambda x: x["games"], reverse=True)

    def analyze_matchups(self, matches: list) -> list:
        opp_data = defaultdict(lambda: {"games": 0, "wins": 0})
        for m in matches:
            opp = m.get("opponent_champion")
            if opp:
                opp_data[opp]["games"] += 1
                opp_data[opp]["wins"] += 1 if m["win"] else 0

        result = []
        for opp, d in opp_data.items():
            if d["games"] < 1:
                continue
            result.append({
                "opponent": opp,
                "games": d["games"],
                "wins": d["wins"],
                "losses": d["games"] - d["wins"],
                "win_rate": round((d["wins"] / d["games"]) * 100, 1),
            })
        return sorted(result, key=lambda x: (x["games"], x["win_rate"]), reverse=True)

    def analyze_role_stats(self, matches: list) -> list:
        role_data = defaultdict(lambda: {"games": 0, "wins": 0})
        for m in matches:
            pos = m.get("position_label", "Desconocido")
            role_data[pos]["games"] += 1
            role_data[pos]["wins"] += 1 if m["win"] else 0

        result = []
        for role, d in role_data.items():
            result.append({
                "role": role,
                "games": d["games"],
                "win_rate": round((d["wins"] / d["games"]) * 100, 1),
            })
        return sorted(result, key=lambda x: x["games"], reverse=True)

    def get_best_items(self, matches: list) -> list:
        item_wins = defaultdict(lambda: {"wins": 0, "total": 0})
        for m in matches:
            for item_id in m.get("items", []):
                item_wins[item_id]["total"] += 1
                if m["win"]:
                    item_wins[item_id]["wins"] += 1

        result = []
        for item_id, d in item_wins.items():
            if d["total"] >= 2:
                result.append({
                    "item_id": item_id,
                    "games": d["total"],
                    "wins": d["wins"],
                    "win_rate": round((d["wins"] / d["total"]) * 100, 1),
                })
        return sorted(result, key=lambda x: x["games"], reverse=True)[:12]

    def analyze_playstyle(self, matches: list) -> dict:
        if not matches:
            return {}
        n = len(matches)
        wins = sum(1 for m in matches if m["win"])

        avg_cs = sum(m["cs_per_min"] for m in matches) / n
        avg_kda = sum(m["kda"] for m in matches) / n
        avg_kills = sum(m["kills"] for m in matches) / n
        avg_deaths = sum(m["deaths"] for m in matches) / n
        avg_assists = sum(m["assists"] for m in matches) / n
        avg_kp = sum(m["kill_participation"] for m in matches) / n
        avg_vision = sum(m["vision_per_min"] for m in matches) / n
        avg_damage = sum(m["damage_per_min"] for m in matches) / n
        win_rate = (wins / n) * 100

        kda_vals = [m["kda"] for m in matches]
        kda_std = (sum((x - avg_kda) ** 2 for x in kda_vals) / n) ** 0.5

        farming_score = min(100, (avg_cs / 9.0) * 100)
        combat_score = min(100, (avg_kda / 5.0) * 60 + (avg_kills / 12.0) * 40)
        vision_score = min(100, (avg_vision / 2.5) * 100)
        teamplay_score = min(100, (avg_kp / 80.0) * 100)
        damage_score = min(100, (avg_damage / 1100.0) * 100)
        consistency_score = max(0, min(100, win_rate - kda_std * 4 + 15))

        scores = {
            "Farmeo": round(farming_score, 1),
            "Combate": round(combat_score, 1),
            "Visión": round(vision_score, 1),
            "Trabajo en Equipo": round(teamplay_score, 1),
            "Daño": round(damage_score, 1),
            "Consistencia": round(consistency_score, 1),
        }

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        dominant = sorted_scores[0][0]
        secondary = sorted_scores[1][0]

        combos = {
            ("Farmeo", "Daño"): ("Carry Farmer", "Priorizas el farmeo y conviertes los recursos en daño mortal"),
            ("Daño", "Farmeo"): ("Carry Farmer", "Priorizas el farmeo y conviertes los recursos en daño mortal"),
            ("Daño", "Combate"): ("Asesino", "Buscas la eliminación individual y el outplay mecánico"),
            ("Combate", "Daño"): ("Campeón de Líneas", "Dominas el 1v1 y sacas ventaja individual"),
            ("Trabajo en Equipo", "Visión"): ("Jugador de Equipo", "Priorizas el grupo y controlas el mapa"),
            ("Visión", "Trabajo en Equipo"): ("Líder de Visión", "Controlas el mapa y das información al equipo"),
            ("Consistencia", "Farmeo"): ("Jugador Sólido", "Rendimiento estable y eficiente en cada partida"),
            ("Farmeo", "Consistencia"): ("Jugador Sólido", "Rendimiento estable y eficiente en cada partida"),
            ("Trabajo en Equipo", "Farmeo"): ("Midlaner de Macro", "Combines farmeo eficiente con buena presencia en el mapa"),
        }

        style_name, style_desc = combos.get(
            (dominant, secondary),
            ("Jugador Equilibrado", "Tienes un estilo versátil sin un rol dominante claro")
        )

        strength_descs = {
            "Farmeo": "Excelente generación de recursos en línea",
            "Combate": "Dominas los tradeos y peleas individuales",
            "Visión": "Control de mapa y colocación de guardianes superior",
            "Trabajo en Equipo": "Alta participación en peleas de equipo",
            "Daño": "Salida de daño elevada y consistente",
            "Consistencia": "Rendimiento estable partida tras partida",
        }
        weakness_descs = {
            "Farmeo": "Mejorar el farmeo y la gestión de oleadas",
            "Combate": "Trabajar en mecánicas de combate individual",
            "Visión": "Aumentar el control de visión y colocación de wards",
            "Trabajo en Equipo": "Participar más activamente en peleas de equipo",
            "Daño": "Optimizar la salida de daño y rotaciones de habilidades",
            "Consistencia": "Reducir las partidas donde el rendimiento cae notablemente",
        }

        strengths = [(s, strength_descs[s]) for s, v in sorted_scores[:2] if v >= 50]
        weaknesses = [(s, weakness_descs[s]) for s, v in sorted_scores[-2:] if v < 55]

        return {
            "scores": scores,
            "playstyle": style_name,
            "description": style_desc,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "avg_kda": round(avg_kda, 2),
            "avg_cs": round(avg_cs, 1),
            "avg_kp": round(avg_kp, 1),
            "avg_vision": round(avg_vision, 2),
            "avg_damage": round(avg_damage, 0),
            "win_rate": round(win_rate, 1),
        }

    def generate_coach_advice(self, matches: list) -> list:
        if not matches:
            return ["No hay suficientes datos para generar consejos."]

        agg = self.aggregate_stats(matches)
        advice = []

        if agg["win_rate"] < 40:
            advice.append(("error", "Racha negativa detectada. Considera jugar campeones más simples o tomarte un descanso breve. La fatiga mental impacta el rendimiento."))
        elif agg["win_rate"] >= 60:
            advice.append(("success", f"¡Excelente racha! {agg['win_rate']}% de victorias. Estás en una buena racha, aprovéchalo para subir de rango."))
        else:
            advice.append(("info", f"Tasa de victorias del {agg['win_rate']}% en las últimas {agg['games']} partidas. Margen de mejora consistente."))

        if agg["avg_kda"] < 2.0:
            advice.append(("warning", f"KDA promedio de {agg['avg_kda']} — por debajo del umbral de Platino (2.8). Identifica en qué momento de la partida mueres y trabaja en reducir las muertes innecesarias."))
        elif agg["avg_kda"] >= 4.0:
            advice.append(("success", f"KDA excepcional de {agg['avg_kda']}. Estás jugando con muy buen control de riesgo."))

        if agg["avg_deaths"] > 6:
            advice.append(("error", f"Media de {agg['avg_deaths']} muertes por partida. Céntrate en mejorar el posicionamiento y la gestión de cooldowns."))

        non_supp = [m for m in matches if m.get("teamPosition") not in ("UTILITY", "")]
        if non_supp:
            avg_cs = sum(m["cs_per_min"] for m in non_supp) / len(non_supp)
            if avg_cs < 6.0:
                advice.append(("warning", f"Farmeo promedio de {round(avg_cs,1)} CS/min (objetivo: >7.0). Dedica tiempo a practicar el last-hit en herramienta de práctica."))
            elif avg_cs >= 8.0:
                advice.append(("success", f"Farmeo excelente: {round(avg_cs,1)} CS/min. Estás en el top de eficiencia de recursos."))

        gold_diffs = [m["gold_diff_15"] for m in matches if m.get("gold_diff_15") is not None]
        if gold_diffs:
            avg_gd = sum(gold_diffs) / len(gold_diffs)
            if avg_gd < -400:
                advice.append(("error", f"Pierdes la fase de líneas de media ({round(avg_gd)}g al min 15). Trabaja en wave management y evita tradeos desfavorables temprano."))
            elif avg_gd > 400:
                advice.append(("success", f"Dominas la fase de líneas (+{round(avg_gd)}g al min 15). Asegúrate de convertir esa ventaja en objetivos (torretas, Dragones, Baron)."))

        if agg["avg_kp"] < 45 and agg["avg_kills"] < 5:
            advice.append(("warning", f"Participación en kills del {agg['avg_kp']}%. Intenta estar más presente en rotaciones y peleas de equipo."))

        if agg["avg_vision_pm"] < 0.8:
            advice.append(("warning", f"Control de visión bajo ({agg['avg_vision_pm']} vis/min). Compra centinela de control siempre y coloca wards antes de pelear objetivos."))

        if not advice:
            advice.append(("success", "Estadísticas muy sólidas y balanceadas en estas partidas. ¡Sigue manteniendo ese nivel!"))

        return advice
