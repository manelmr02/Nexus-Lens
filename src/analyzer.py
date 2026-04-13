class MatchAnalyzer:
    def __init__(self):
        self.platinum_thresholds = {
            "kda": 2.8,
            "damage_per_min": 600,
            "gold_per_min": 380,
            "vision_per_min": 1.2,
            "cs_per_min": 6.5
        }

    def analyze_match(self, match_data: dict, puuid: str, timeline_data: dict = None) -> dict:
        info = match_data["info"]
        duration_min = info["gameDuration"] / 60.0
        
        player_info = next((p for p in info["participants"] if p["puuid"] == puuid), None)
        if not player_info:
            return None
            
        team_id = player_info["teamId"]
        team_kills = sum(p["kills"] for p in info["participants"] if p["teamId"] == team_id)

        kills = player_info["kills"]
        deaths = player_info["deaths"]
        assists = player_info["assists"]
        kda = (kills + assists) / max(1, deaths)
        dmg_per_min = player_info["totalDamageDealtToChampions"] / max(1, duration_min)
        gold_per_min = player_info["goldEarned"] / max(1, duration_min)
        vision_per_min = player_info["visionScore"] / max(1, duration_min)
        
        total_cs = player_info.get("totalMinionsKilled", 0) + player_info.get("neutralMinionsKilled", 0)
        cs_per_min = total_cs / max(1, duration_min)

        kp = 0
        if team_kills > 0:
            kp = ((kills + assists) / team_kills) * 100

        gold_diff_15 = None
        if timeline_data and "info" in timeline_data and "frames" in timeline_data["info"]:
            try:
                player_pid = player_info["participantId"]
                position = player_info["teamPosition"]
                if position and position != "Invalid":
                    opponent = next((p for p in info["participants"] if p["teamId"] != team_id and p.get("teamPosition") == position), None)
                    if opponent:
                        opp_pid = opponent["participantId"]
                        target_timestamp = 15 * 60000
                        frame_15 = next((f for f in timeline_data["info"]["frames"] if f["timestamp"] >= target_timestamp), None)
                        if frame_15:
                            player_gold = frame_15["participantFrames"][str(player_pid)]["totalGold"]
                            opp_gold = frame_15["participantFrames"][str(opp_pid)]["totalGold"]
                            gold_diff_15 = player_gold - opp_gold
            except Exception:
                pass

        return {
            "championName": player_info["championName"],
            "win": player_info["win"],
            "kills": kills, "deaths": deaths, "assists": assists,
            "kda": round(kda, 2),
            "damage_per_min": round(dmg_per_min, 1),
            "gold_per_min": round(gold_per_min, 1),
            "vision_per_min": round(vision_per_min, 2),
            "cs_per_min": round(cs_per_min, 1),
            "kill_participation": round(kp, 1),
            "gold_diff_15": gold_diff_15,
            "teamPosition": player_info.get("teamPosition", "UNKNOWN")
        }

    def generate_coach_advice(self, matches_stats: list) -> list:
        advice = []
        if not matches_stats:
            return ["No hay suficientes datos para generar consejos."]
        
        wins = sum(1 for m in matches_stats if m["win"])
        winrate = (wins / len(matches_stats)) * 100
        avg_kda = sum(m["kda"] for m in matches_stats) / len(matches_stats)
        
        if winrate < 40:
            advice.append("Has estado en una racha negativa recientemente. Considera tomar un descanso o jugar normales.")
        elif winrate >= 60:
            advice.append("¡Excelente racha! Estás jugando muy bien en tus últimas partidas.")
            
        if avg_kda < 2.0:
            advice.append("Tu KDA promedio está por debajo de lo ideal (2.0). Juega más seguro e intenta morir menos; cede algo de farmeo si es necesario.")
            
        first_match = matches_stats[0]
        if first_match.get("gold_diff_15") is not None:
            gd = first_match["gold_diff_15"]
            pos = first_match.get("teamPosition", "UNKNOWN")
            if gd < -500:
                advice.append(f"En tu última partida como {pos}, perdiste la fase de líneas de forma notable ({gd} de oro al min 15 respecto a tu rival). Necesitas mejorar el farmeo bajo torre o evitar tradeos malos tempranos.")
            elif gd > 500:
                advice.append(f"¡Destrozaste en la fase de líneas como {pos} en tu última partida (+{gd} de oro al min 15)! Asegúrate de esparcir esa ventaja rotando tras tirar la torre.")
                
        avg_cs = sum(m["cs_per_min"] for m in matches_stats) / len(matches_stats)
        if avg_cs < 6.0 and first_match.get("teamPosition") not in ["UTILITY", "UNKNOWN"]:
            advice.append(f"Tu farmeo promedio es algo bajo ({round(avg_cs,1)} CS/min). Dedica tiempo a priorizar siempre el 'last hit' antes de pelear.")
            
        if not advice:
            advice.append("Tus métricas globales para estas partidas son muy sólidas y balanceadas. ¡Sigue así!")
            
        return advice
