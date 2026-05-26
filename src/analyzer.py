from collections import defaultdict, Counter

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

# Umbrales de rendimiento diferenciados por rol (nivel Platino+)
ROLE_THRESHOLDS = {
    "TOP": {
        "label": "Top",
        "kda": 2.5,
        "cs_per_min": 7.0,        # laners deben farmear bien
        "damage_per_min": 600,
        "vision_per_min": 0.8,
        "kp": 45,
        "gold_diff_15": 300,       # margen significativo en top
        "deaths": 5,
        "show_cs": True,
        "show_gold_diff": True,
    },
    "JUNGLE": {
        "label": "Jungla",
        "kda": 3.0,
        "cs_per_min": 5.5,         # camps + algo de laning
        "damage_per_min": 500,
        "vision_per_min": 1.5,     # jungla debe wardear más
        "kp": 55,                  # jungla participa en más kills
        "gold_diff_15": 300,       # vs jungler rival (meaningful pero menos crítico)
        "deaths": 4,
        "show_cs": True,
        "show_gold_diff": True,
    },
    "MIDDLE": {
        "label": "Mid",
        "kda": 3.0,
        "cs_per_min": 7.5,
        "damage_per_min": 750,
        "vision_per_min": 1.0,
        "kp": 50,
        "gold_diff_15": 300,
        "deaths": 5,
        "show_cs": True,
        "show_gold_diff": True,
    },
    "BOTTOM": {
        "label": "ADC",
        "kda": 3.0,
        "cs_per_min": 8.0,         # ADC debe farmear muy bien
        "damage_per_min": 900,     # ADC genera mucho daño
        "vision_per_min": 0.7,
        "kp": 55,
        "gold_diff_15": 400,       # ADC necesita ventaja de recursos
        "deaths": 4,
        "show_cs": True,
        "show_gold_diff": True,
    },
    "UTILITY": {
        "label": "Support",
        "kda": 3.5,                # ratio alto por muchos assists
        "cs_per_min": None,        # no aplica — support no debe farmear
        "damage_per_min": 250,     # barra mucho más baja
        "vision_per_min": 2.5,     # la visión es la métrica clave del support
        "kp": 70,                  # debe participar en casi todas las kills
        "gold_diff_15": None,      # no aplica — support no farmea lane
        "deaths": 6,               # supports mueren más (protegiendo)
        "show_cs": False,
        "show_gold_diff": False,
    },
}

def _get_dominant_role(matches: list) -> str:
    if not matches:
        return "MIDDLE"
    counts = Counter(m.get("teamPosition", "") for m in matches if m.get("teamPosition") not in ("", "Invalid", None))
    return counts.most_common(1)[0][0] if counts else "MIDDLE"

def _get_role_thresholds(matches: list) -> dict:
    role = _get_dominant_role(matches)
    return ROLE_THRESHOLDS.get(role, ROLE_THRESHOLDS["MIDDLE"]), role

class MatchAnalyzer:
    def __init__(self):
        # Umbrales genéricos (fallback); se usan los de ROLE_THRESHOLDS en la mayoría de funciones
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
        thresholds, dominant_role = _get_role_thresholds(matches)
        is_support = dominant_role == "UTILITY"
        is_jungle  = dominant_role == "JUNGLE"

        avg_cs     = sum(m["cs_per_min"] for m in matches) / n
        avg_kda    = sum(m["kda"] for m in matches) / n
        avg_kills  = sum(m["kills"] for m in matches) / n
        avg_deaths = sum(m["deaths"] for m in matches) / n
        avg_kp     = sum(m["kill_participation"] for m in matches) / n
        avg_vision = sum(m["vision_per_min"] for m in matches) / n
        avg_damage = sum(m["damage_per_min"] for m in matches) / n
        win_rate   = (wins / n) * 100

        kda_vals  = [m["kda"] for m in matches]
        kda_std   = (sum((x - avg_kda) ** 2 for x in kda_vals) / n) ** 0.5

        # ── Dimensión 1: Recursos / Farmeo ─────────────────────────────────────
        # Para supports la sustitutimos por "Eficacia de Soporte" (basada en KP y assists)
        if is_support:
            avg_assists = sum(m["assists"] for m in matches) / n
            dim1_score = min(100, (avg_assists / 15.0) * 50 + (avg_kp / 75.0) * 50)
            dim1_label = "Eficacia Soporte"
        else:
            cs_target  = thresholds["cs_per_min"] or 7.0
            dim1_score = min(100, (avg_cs / (cs_target * 1.3)) * 100)
            dim1_label = "Farmeo"

        # ── Dimensión 2: Combate ───────────────────────────────────────────────
        kda_target  = thresholds["kda"]
        combat_score = min(100, (avg_kda / (kda_target * 1.8)) * 60 + (avg_kills / 12.0) * 40)

        # ── Dimensión 3: Visión ────────────────────────────────────────────────
        # Support tiene barra más alta (se espera más de ellos)
        vis_target  = thresholds["vision_per_min"]
        vision_score = min(100, (avg_vision / (vis_target * 1.2)) * 100)

        # ── Dimensión 4: Trabajo en Equipo ─────────────────────────────────────
        kp_target    = thresholds["kp"]
        teamplay_score = min(100, (avg_kp / (kp_target * 1.1)) * 100)

        # ── Dimensión 5: Daño ─────────────────────────────────────────────────
        dmg_target   = thresholds["damage_per_min"]
        damage_score  = min(100, (avg_damage / (dmg_target * 1.3)) * 100)

        # ── Dimensión 6: Consistencia ──────────────────────────────────────────
        consistency_score = max(0, min(100, win_rate - kda_std * 4 + 15))

        scores = {
            dim1_label: round(dim1_score, 1),
            "Combate": round(combat_score, 1),
            "Visión": round(vision_score, 1),
            "Trabajo en Equipo": round(teamplay_score, 1),
            "Daño": round(damage_score, 1),
            "Consistencia": round(consistency_score, 1),
        }

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        dominant  = sorted_scores[0][0]
        secondary = sorted_scores[1][0]

        combos = {
            ("Farmeo", "Daño"):           ("Carry Farmer",       "Priorizas el farmeo y conviertes los recursos en daño mortal"),
            ("Daño", "Farmeo"):           ("Carry Farmer",       "Priorizas el farmeo y conviertes los recursos en daño mortal"),
            ("Daño", "Combate"):          ("Asesino",            "Buscas la eliminación individual y el outplay mecánico"),
            ("Combate", "Daño"):          ("Campeón de Líneas",  "Dominas el 1v1 y sacas ventaja individual"),
            ("Trabajo en Equipo", "Visión"):  ("Jugador de Equipo",  "Priorizas el grupo y controlas el mapa"),
            ("Visión", "Trabajo en Equipo"):  ("Líder de Visión",    "Controlas el mapa y das información al equipo"),
            ("Consistencia", "Farmeo"):   ("Jugador Sólido",     "Rendimiento estable y eficiente en cada partida"),
            ("Farmeo", "Consistencia"):   ("Jugador Sólido",     "Rendimiento estable y eficiente en cada partida"),
            ("Eficacia Soporte", "Visión"):   ("Support Completo",   "Maximizas la utilidad y el control de mapa para tu equipo"),
            ("Visión", "Eficacia Soporte"):   ("Support de Visión",  "Lideras el control de información y los objetivos del equipo"),
            ("Eficacia Soporte", "Trabajo en Equipo"): ("Engage Support", "Inicias peleas y proteges a tus carries con gran efectividad"),
        }

        style_name, style_desc = combos.get(
            (dominant, secondary),
            ("Jugador Equilibrado", "Tienes un estilo versátil sin un rol dominante claro")
        )

        strength_descs = {
            "Farmeo":            "Excelente generación de recursos en línea",
            "Eficacia Soporte":  "Muy alta participación y utilidad para el equipo",
            "Combate":           "Dominas los tradeos y peleas individuales",
            "Visión":            "Control de mapa y colocación de guardianes superior",
            "Trabajo en Equipo": "Alta participación en peleas de equipo",
            "Daño":              "Salida de daño elevada y consistente",
            "Consistencia":      "Rendimiento estable partida tras partida",
        }
        weakness_descs = {
            "Farmeo":            "Mejorar el farmeo y la gestión de oleadas",
            "Eficacia Soporte":  "Aumentar la participación en kills y la utilidad por partida",
            "Combate":           "Trabajar en mecánicas de combate individual",
            "Visión":            "Aumentar el control de visión y colocación de wards",
            "Trabajo en Equipo": "Participar más activamente en peleas de equipo",
            "Daño":              "Optimizar la salida de daño y rotaciones de habilidades",
            "Consistencia":      "Reducir las partidas donde el rendimiento cae notablemente",
        }

        strengths  = [(s, strength_descs[s])  for s, v in sorted_scores[:2]  if v >= 50]
        weaknesses = [(s, weakness_descs[s])  for s, v in sorted_scores[-2:] if v < 55]

        return {
            "scores": scores,
            "playstyle": style_name,
            "description": style_desc,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "dominant_role": dominant_role,
            "role_label": thresholds["label"],
            "avg_kda": round(avg_kda, 2),
            "avg_cs": round(avg_cs, 1),
            "avg_kp": round(avg_kp, 1),
            "avg_vision": round(avg_vision, 2),
            "avg_damage": round(avg_damage, 0),
            "win_rate": round(win_rate, 1),
        }

    def generate_coach_advice(self, matches: list) -> list:
        if not matches:
            return [("info", "No hay suficientes datos para generar consejos.")]

        agg = self.aggregate_stats(matches)
        thresholds, role = _get_role_thresholds(matches)
        role_label = thresholds["label"]
        advice = []

        # ── Winrate global ─────────────────────────────────────────────────────
        if agg["win_rate"] < 40:
            advice.append(("error", f"Racha negativa detectada ({agg['win_rate']}% WR). Considera jugar campeones más simples o tomarte un descanso breve."))
        elif agg["win_rate"] >= 60:
            advice.append(("success", f"¡Excelente racha! {agg['win_rate']}% de victorias en {agg['games']} partidas como {role_label}. Aprovéchalo para subir de rango."))
        else:
            advice.append(("info", f"Winrate del {agg['win_rate']}% en las últimas {agg['games']} partidas ({role_label}). Margen de mejora consistente."))

        # ── KDA por rol ────────────────────────────────────────────────────────
        kda_thresh = thresholds["kda"]
        if agg["avg_kda"] < kda_thresh * 0.7:
            advice.append(("warning", f"KDA de {agg['avg_kda']} — por debajo del objetivo de {role_label} ({kda_thresh}). Identifica en qué fase de la partida mueres más y trabaja en reducirlo."))
        elif agg["avg_kda"] >= kda_thresh * 1.5:
            advice.append(("success", f"KDA de {agg['avg_kda']} — muy por encima del objetivo de {role_label} ({kda_thresh}). Excelente control de riesgo."))

        # ── Muertes por rol ────────────────────────────────────────────────────
        deaths_thresh = thresholds["deaths"]
        if agg["avg_deaths"] > deaths_thresh:
            advice.append(("error", f"Media de {agg['avg_deaths']} muertes por partida (límite recomendado para {role_label}: {deaths_thresh}). Trabaja en el posicionamiento y la gestión de cooldowns."))

        # ── Farmeo (solo roles que deben farmear) ──────────────────────────────
        cs_thresh = thresholds["cs_per_min"]
        if thresholds["show_cs"] and cs_thresh is not None:
            avg_cs = agg["avg_cs_pm"]
            if avg_cs < cs_thresh * 0.82:
                advice.append(("warning", f"Farmeo de {avg_cs} CS/min — por debajo del objetivo de {role_label} ({cs_thresh}). Practica el last-hit y prioriza oleadas antes de pelear."))
            elif avg_cs >= cs_thresh * 1.1:
                advice.append(("success", f"Farmeo excelente: {avg_cs} CS/min (objetivo {role_label}: {cs_thresh}). Estás en el top de eficiencia de recursos."))

        # ── Gold diff @15 (solo roles con laning phase relevante) ──────────────
        if thresholds["show_gold_diff"]:
            gd_thresh = thresholds["gold_diff_15"] or 300
            gold_diffs = [m["gold_diff_15"] for m in matches if m.get("gold_diff_15") is not None]
            if gold_diffs:
                avg_gd = sum(gold_diffs) / len(gold_diffs)
                if avg_gd < -gd_thresh:
                    advice.append(("error", f"Pierdes la fase de líneas de media ({round(avg_gd)}g al min 15 como {role_label}). Trabaja en wave management y evita tradeos desfavorables temprano."))
                elif avg_gd > gd_thresh:
                    advice.append(("success", f"Dominas la fase de líneas como {role_label} (+{round(avg_gd)}g al min 15). Convierte esa ventaja en torretas y objetivos."))

        # ── Kill Participation por rol ─────────────────────────────────────────
        kp_thresh = thresholds["kp"]
        if agg["avg_kp"] < kp_thresh * 0.75:
            if role == "UTILITY":
                advice.append(("warning", f"KP del {agg['avg_kp']}% — bajo para un Support (objetivo: >{kp_thresh}%). Como support deberías estar en casi todas las peleas de tu equipo."))
            elif role == "JUNGLE":
                advice.append(("warning", f"KP del {agg['avg_kp']}% como Jungla (objetivo: >{kp_thresh}%). Mejora tus rotaciones para aparecer en más peleas de líneas."))
            else:
                advice.append(("warning", f"KP del {agg['avg_kp']}% como {role_label}. Intenta participar más activamente en peleas de equipo y rotaciones."))

        # ── Visión por rol ─────────────────────────────────────────────────────
        vis_thresh = thresholds["vision_per_min"]
        if agg["avg_vision_pm"] < vis_thresh * 0.65:
            if role == "UTILITY":
                advice.append(("error", f"Visión muy baja para un Support: {agg['avg_vision_pm']}/min (objetivo: >{vis_thresh}). El control de visión es tu responsabilidad principal. Compra siempre centinelas de control."))
            elif role == "JUNGLE":
                advice.append(("warning", f"Visión de {agg['avg_vision_pm']}/min (objetivo Jungla: >{vis_thresh}). Wardea los objetivos (Dragón, Barón) antes de pelearlos."))
            else:
                advice.append(("warning", f"Control de visión bajo: {agg['avg_vision_pm']}/min (objetivo {role_label}: >{vis_thresh}). Lleva siempre centinelas de control en el inventario."))
        elif role == "UTILITY" and agg["avg_vision_pm"] >= vis_thresh:
            advice.append(("success", f"Control de visión excelente como Support: {agg['avg_vision_pm']}/min. Mantén ese estándar."))

        # ── Daño (solo para roles carry) ───────────────────────────────────────
        dmg_thresh = thresholds["damage_per_min"]
        if role in ("BOTTOM", "MIDDLE") and agg["avg_damage_pm"] < dmg_thresh * 0.7:
            advice.append(("warning", f"Daño por minuto de {agg['avg_damage_pm']} — bajo para {role_label} (objetivo: >{dmg_thresh}). Revisa tu gestión de oleadas y rotación de habilidades en peleas."))

        if not advice:
            advice.append(("success", f"Estadísticas muy sólidas para {role_label} en estas partidas. ¡Sigue manteniendo ese nivel!"))

        return advice

    def get_role_thresholds_for_display(self, matches: list) -> tuple[dict, str]:
        """Devuelve (thresholds_dict, role_key) para usar en la UI."""
        return _get_role_thresholds(matches)
