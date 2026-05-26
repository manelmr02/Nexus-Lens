import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.riot_client import NexusClient, REGION_MAP
from src.analyzer import MatchAnalyzer
from src.ddragon import (champion_img_url, item_img_url, profile_icon_url, get_item_name,
                         get_all_champion_names, get_champion_tags, get_rune_data,
                         get_rune_by_key, rune_img_url, get_item_id_by_name)
from src.tierlist import TIER_LIST, TIER_COLORS, CURRENT_PATCH
from src.matchup_guide import (get_rune_page, get_build, get_matchup_advice,
                                get_primary_type, _ROLE_TO_POS)

st.set_page_config(page_title="Nexus Lens", page_icon="🧿", layout="wide")

st.markdown("""
<style>
  .stApp { background: linear-gradient(135deg, #0f172a 0%, #020617 100%); color: #f8fafc; }
  .stButton>button {
    background: linear-gradient(45deg, #3b82f6, #8b5cf6) !important;
    color: white !important; border: none !important; border-radius: 8px !important;
    font-weight: 700 !important; padding: 0.5rem 2rem !important; transition: transform 0.2s !important;
  }
  .stButton>button:hover { transform: scale(1.05); }
  h1 {
    background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-weight: 900; letter-spacing: -1px;
  }
  [data-testid="stSidebar"] {
    background-color: rgba(15,23,42,0.9) !important;
    backdrop-filter: blur(10px); border-right: 1px solid rgba(255,255,255,0.05);
  }
  div[data-testid="stMetricValue"] { font-size: 2rem !important; font-weight: 800; color: #e2e8f0; }
  div[data-testid="stMetricLabel"] {
    font-size: 0.85rem !important; color: #94a3b8;
    font-weight: 600; text-transform: uppercase; letter-spacing: 1px;
  }
  .stat-card {
    background: rgba(30,41,59,0.5); padding: 1.2rem; border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.07); text-align: center;
    transition: transform 0.2s, border-color 0.2s;
  }
  .stat-card:hover { transform: translateY(-4px); border-color: #3b82f6; }
  .tier-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap; }
  .tier-badge {
    font-size: 1.1rem; font-weight: 900; width: 40px; text-align: center;
    padding: 4px 0; border-radius: 6px; flex-shrink: 0;
  }
  .champ-chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(30,41,59,0.6); border-radius: 8px;
    padding: 4px 10px; border: 1px solid rgba(255,255,255,0.08);
    font-size: 0.85rem;
  }
  .rank-badge {
    display: inline-block; padding: 6px 16px; border-radius: 20px;
    font-weight: 700; font-size: 0.9rem; letter-spacing: 1px;
  }
  .win-badge { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid #10b981; }
  .loss-badge { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid #ef4444; }
  .plotly-chart { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

RANK_COLORS = {
    "IRON": "#6b7280", "BRONZE": "#cd7f32", "SILVER": "#c0c0c0",
    "GOLD": "#fbbf24", "PLATINUM": "#34d399", "EMERALD": "#10b981",
    "DIAMOND": "#60a5fa", "MASTER": "#a78bfa", "GRANDMASTER": "#f87171",
    "CHALLENGER": "#fde68a",
}
RANK_EMOJIS = {
    "IRON": "🪨", "BRONZE": "🥉", "SILVER": "🥈", "GOLD": "🥇",
    "PLATINUM": "💎", "EMERALD": "💚", "DIAMOND": "💠",
    "MASTER": "🔮", "GRANDMASTER": "👑", "CHALLENGER": "🏆",
}
QUEUE_LABELS = {420: "Solo/Duo", 440: "Flexible", 450: "ARAM", 0: "Todas"}

@st.cache_resource
def get_services():
    return NexusClient(), MatchAnalyzer()

try:
    client, analyzer = get_services()
except Exception as e:
    st.error(f"Error inicializando servicios: {e}")
    st.stop()


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
      <span style="font-size:2.5rem">🧿</span>
      <h2 style="margin:0; background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc);
                 -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        Nexus Lens
      </h2>
      <p style="color:#64748b; font-size:0.8rem; margin:0;">Análisis avanzado de League of Legends</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    riot_name = st.text_input("Game Name", "Faker")
    riot_tag  = st.text_input("Tag Line", "T1")

    region = st.selectbox("Región", list(REGION_MAP.keys()), index=0)

    col_q, col_n = st.columns(2)
    with col_q:
        queue_opt = st.selectbox("Tipo", list(QUEUE_LABELS.values()), index=0)
        queue_id = {v: k for k, v in QUEUE_LABELS.items()}[queue_opt]
    with col_n:
        match_count = st.selectbox("Partidas", [10, 20, 30, 50], index=1)

    analyze_btn = st.button("Analizar", use_container_width=True)
    st.markdown("---")
    st.caption(f"Patch {CURRENT_PATCH} · Tier List actualizada")


# ── TABS ────────────────────────────────────────────────────────────────────────
st.title("🧿 Nexus Lens")
tab_perfil, tab_champs, tab_render, tab_estilo, tab_matchup, tab_tier, tab_coach = st.tabs([
    "📊 Resumen", "🏆 Campeones", "📈 Rendimiento", "🧠 Estilo de Juego",
    "⚔️ Match-Up Guide", "🔥 Tier List", "🤖 IA Coach"
])

# ── MATCH-UP GUIDE (siempre visible, independiente del análisis) ───────────────
with tab_matchup:
    st.header("⚔️ Match-Up Guide")
    st.markdown("Selecciona tu campeón, tu rol y el rival para obtener runas, build y consejos de matchup.")

    ROLES_DISPLAY = ["Top", "Jungla", "Mid", "ADC", "Support"]
    all_champs = get_all_champion_names()

    mg_col1, mg_col2, mg_col3 = st.columns([2, 1, 2])
    with mg_col1:
        my_champ = st.selectbox("Tu Campeón", all_champs, index=all_champs.index("Ahri") if "Ahri" in all_champs else 0, key="mg_my_champ")
        my_role  = st.selectbox("Tu Rol", ROLES_DISPLAY, key="mg_my_role")
    with mg_col2:
        st.markdown("<div style='text-align:center;padding-top:2rem;font-size:2rem;'>VS</div>", unsafe_allow_html=True)
    with mg_col3:
        enemy_champ = st.selectbox("Campeón Rival", all_champs, index=all_champs.index("Zed") if "Zed" in all_champs else 1, key="mg_enemy_champ")
        st.markdown("<br>", unsafe_allow_html=True)

    mg_btn = st.button("Analizar Match-Up", use_container_width=True, key="mg_btn")

    if mg_btn or True:  # Mostrar siempre con los selectores actuales
        role_pos = _ROLE_TO_POS.get(my_role, "MIDDLE")

        my_tags    = get_champion_tags(my_champ)
        enemy_tags = get_champion_tags(enemy_champ)
        my_type    = get_primary_type(my_tags)
        enemy_type = get_primary_type(enemy_tags)

        rune_page = get_rune_page(my_champ, role_pos)
        build     = get_build(my_champ, role_pos)
        advice    = get_matchup_advice(my_type, enemy_type)

        st.markdown("---")

        # ── Header del matchup ─────────────────────────────────────────────────
        hc1, hc2, hc3 = st.columns([2, 1, 2])
        with hc1:
            st.markdown(f"""
            <div style="text-align:center;padding:1rem;background:rgba(30,41,59,0.5);border-radius:14px;">
              <img src="{champion_img_url(my_champ)}" width="90" style="border-radius:12px;border:2px solid #3b82f6;">
              <div style="font-size:1.1rem;font-weight:700;margin-top:8px;">{my_champ}</div>
              <div style="color:#64748b;font-size:0.8rem;">{my_role} · {my_type}</div>
            </div>
            """, unsafe_allow_html=True)
        with hc2:
            diff_color = advice["color"]
            st.markdown(f"""
            <div style="text-align:center;padding:1rem;">
              <div style="font-size:2rem;">⚔️</div>
              <div style="background:{diff_color}22;border:1px solid {diff_color};border-radius:8px;
                          padding:6px 12px;font-weight:700;color:{diff_color};font-size:0.85rem;">
                {advice['difficulty']}
              </div>
            </div>
            """, unsafe_allow_html=True)
        with hc3:
            st.markdown(f"""
            <div style="text-align:center;padding:1rem;background:rgba(30,41,59,0.5);border-radius:14px;">
              <img src="{champion_img_url(enemy_champ)}" width="90" style="border-radius:12px;border:2px solid #ef4444;">
              <div style="font-size:1.1rem;font-weight:700;margin-top:8px;">{enemy_champ}</div>
              <div style="color:#64748b;font-size:0.8rem;">{enemy_type}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Consejos de matchup ────────────────────────────────────────────────
        st.markdown(f"#### Cómo jugar este matchup")
        st.markdown(f"""
        <div style="padding:1rem;background:rgba(30,41,59,0.4);border-radius:12px;
                    border-left:4px solid {advice['color']};margin-bottom:1rem;">
          <span style="color:#e2e8f0;">{advice['overview']}</span>
        </div>
        """, unsafe_allow_html=True)

        tips_cols = st.columns(len(advice["tips"]))
        icons = ["🌅", "🗺️", "🏆"]
        labels = ["Early Game", "Mid Game", "Late Game / General"]
        for i, (tip, col) in enumerate(zip(advice["tips"], tips_cols)):
            with col:
                st.markdown(f"""
                <div style="padding:1rem;background:rgba(30,41,59,0.4);border-radius:12px;height:100%;
                            border:1px solid rgba(255,255,255,0.07);">
                  <div style="color:#94a3b8;font-size:0.75rem;text-transform:uppercase;margin-bottom:6px;">
                    {icons[i]} {labels[i]}
                  </div>
                  <div style="font-size:0.9rem;color:#cbd5e1;">{tip}</div>
                </div>
                """, unsafe_allow_html=True)

        if advice.get("items_note"):
            st.info(f"💡 **Ajuste de build:** {advice['items_note']}")

        st.markdown("---")

        # ── Runas ──────────────────────────────────────────────────────────────
        st.markdown(f"#### Runas Recomendadas — {my_champ} {my_role}")

        if rune_page:
            rune_data = get_rune_data()

            def render_rune(key: str, size: int = 40) -> str:
                r = get_rune_by_key(key)
                if r and r.get("icon"):
                    url = rune_img_url(r["icon"])
                    name = r.get("name", key)
                    return f'<img src="{url}" width="{size}" title="{name}" style="border-radius:50%;margin:3px;">'
                return f'<span style="color:#64748b;font-size:0.75rem;">{key}</span>'

            def get_tree_icon(tree_name: str) -> str:
                for tree in rune_data:
                    if tree.get("key") == tree_name or tree.get("name") == tree_name:
                        return rune_img_url(tree["icon"]) if tree.get("icon") else ""
                return ""

            rc1, rc2 = st.columns(2)

            with rc1:
                primary_tree_icon = get_tree_icon(rune_page["primary_tree"])
                st.markdown(f"""
                <div style="background:rgba(30,41,59,0.5);border-radius:14px;padding:1.2rem;
                            border:1px solid rgba(255,255,255,0.07);">
                  <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
                    {'<img src="' + primary_tree_icon + '" width="24">' if primary_tree_icon else ""}
                    <span style="color:#94a3b8;font-size:0.8rem;text-transform:uppercase;">
                      {rune_page['primary_tree']} (Principal)
                    </span>
                  </div>
                  <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
                    {render_rune(rune_page['keystone'], 52)}
                    <div>
                      <div style="font-weight:700;">{get_rune_by_key(rune_page["keystone"]) and get_rune_by_key(rune_page["keystone"]).get("name", rune_page["keystone"]) or rune_page["keystone"]}</div>
                      <div style="color:#64748b;font-size:0.75rem;">Keystone</div>
                    </div>
                  </div>
                  <div>{"".join(render_rune(r, 36) for r in rune_page["primary_slots"])}</div>
                </div>
                """, unsafe_allow_html=True)

            with rc2:
                secondary_tree_icon = get_tree_icon(rune_page["secondary_tree"])
                st.markdown(f"""
                <div style="background:rgba(30,41,59,0.5);border-radius:14px;padding:1.2rem;
                            border:1px solid rgba(255,255,255,0.07);">
                  <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
                    {'<img src="' + secondary_tree_icon + '" width="24">' if secondary_tree_icon else ""}
                    <span style="color:#94a3b8;font-size:0.8rem;text-transform:uppercase;">
                      {rune_page['secondary_tree']} (Secundario)
                    </span>
                  </div>
                  <div>{"".join(render_rune(r, 36) for r in rune_page["secondary_slots"])}</div>
                  <div style="margin-top:12px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.07);">
                    <span style="color:#64748b;font-size:0.75rem;text-transform:uppercase;">Fragmentos</span><br>
                    <span style="font-size:0.85rem;color:#cbd5e1;">
                      {"  ·  ".join(rune_page.get("shards", []))}
                    </span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"No hay página de runas específica para {my_champ} en {my_role}. Consulta OP.GG para datos en tiempo real.")

        st.markdown("---")

        # ── Build ──────────────────────────────────────────────────────────────
        st.markdown(f"#### Build Recomendada — {my_champ} {my_role}")

        if build:
            if build.get("note"):
                st.markdown(f"""
                <div style="padding:0.8rem 1rem;background:rgba(59,130,246,0.1);border-radius:10px;
                            border-left:3px solid #3b82f6;margin-bottom:1rem;font-size:0.9rem;">
                  {build['note']}
                </div>
                """, unsafe_allow_html=True)

            def render_item_card(item_name: str) -> str:
                item_id = get_item_id_by_name(item_name)
                img_url = item_img_url(item_id) if item_id else ""
                img_tag = f'<img src="{img_url}" width="48" style="border-radius:8px;">' if img_url else "❓"
                return f"""
                <div style="display:inline-block;text-align:center;margin:4px;vertical-align:top;width:70px;">
                  {img_tag}
                  <div style="font-size:0.65rem;color:#94a3b8;margin-top:3px;word-break:break-word;">{item_name}</div>
                </div>"""

            build_rows = [
                ("🟡 Inicio", build.get("start", [])),
                ("👟 Botas", [build.get("boots")] if build.get("boots") else []),
                ("⚡ Core (Build Principal)", build.get("core", [])),
                ("🔧 Situacional", build.get("situational", [])),
            ]
            for label, items in build_rows:
                if not items:
                    continue
                items_html = "".join(render_item_card(it) for it in items if it)
                st.markdown(f"""
                <div style="margin-bottom:0.8rem;">
                  <div style="color:#94a3b8;font-size:0.75rem;text-transform:uppercase;margin-bottom:6px;">{label}</div>
                  <div style="background:rgba(30,41,59,0.4);border-radius:12px;padding:0.8rem;
                              border:1px solid rgba(255,255,255,0.05);">{items_html}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"No hay build específica para {my_champ} en {my_role}. Consulta OP.GG para datos actualizados.")


# ── TIER LIST (siempre visible, sin datos del jugador) ──────────────────────────
with tab_tier:
    st.header(f"Tier List del Parche {CURRENT_PATCH}")
    st.markdown("*Basada en estadísticas de partidas de nivel Platino+ en todas las regiones.*")

    role_tabs = st.tabs(["Top", "Jungla", "Mid", "ADC", "Support"])
    role_keys = ["TOP", "JUNGLE", "MIDDLE", "ADC", "SUPPORT"]

    for rt, role_key in zip(role_tabs, role_keys):
        with rt:
            role_data = TIER_LIST.get(role_key, {})
            for tier_name in ["S+", "S", "A", "B", "C"]:
                champs = role_data.get(tier_name, [])
                if not champs:
                    continue
                color = TIER_COLORS[tier_name]
                tier_html = f'<div class="tier-row"><div class="tier-badge" style="background:{color}33;color:{color};border:2px solid {color};">{tier_name}</div>'
                for c in champs:
                    img = champion_img_url(c["dd"])
                    tier_html += f'''
                    <div class="champ-chip">
                      <img src="{img}" width="28" height="28" style="border-radius:6px;">
                      <span>{c["name"]}</span>
                      <span style="color:#64748b;font-size:0.75rem;">{c["wr"]}%</span>
                    </div>'''
                tier_html += "</div>"
                st.markdown(tier_html, unsafe_allow_html=True)


# ── ANÁLISIS DEL JUGADOR ────────────────────────────────────────────────────────
if analyze_btn:
    if not riot_name or not riot_tag:
        st.sidebar.error("Introduce Game Name y Tag Line")
    else:
        try:
            client.set_region(region)
            progress = st.sidebar.progress(0, text="Buscando jugador...")

            puuid = client.get_puuid_by_riot_id(riot_name.strip(), riot_tag.strip())
            progress.progress(10, "Obteniendo perfil...")

            summoner   = client.get_summoner_by_puuid(puuid)
            progress.progress(20, "Obteniendo rango...")
            rank_data  = client.get_rank_by_summoner_id(summoner.get("id", ""))
            mastery    = client.get_champion_mastery(puuid, count=5)
            progress.progress(30, "Cargando historial de partidas...")

            q = queue_id if queue_id != 0 else None
            match_ids = client.get_match_ids(puuid, count=match_count, queue=q)
            if not match_ids:
                st.warning("No se encontraron partidas con los filtros seleccionados.")
                st.stop()

            matches_stats = []
            fetch_timeline_for = set(match_ids[:5])

            for i, mid in enumerate(match_ids):
                pct = 30 + int((i / len(match_ids)) * 65)
                progress.progress(pct, f"Analizando partida {i+1}/{len(match_ids)}...")
                data = client.get_match_details(mid)
                timeline = client.get_match_timeline(mid) if mid in fetch_timeline_for else None
                stats = analyzer.analyze_match(data, puuid, timeline)
                if stats:
                    matches_stats.append(stats)

            progress.progress(100, "Completado")
            progress.empty()

            if not matches_stats:
                st.warning("No se pudieron procesar las partidas.")
                st.stop()

            agg           = analyzer.aggregate_stats(matches_stats)
            champ_stats   = analyzer.analyze_champion_stats(matches_stats)
            matchups      = analyzer.analyze_matchups(matches_stats)
            role_stats    = analyzer.analyze_role_stats(matches_stats)
            best_items    = analyzer.get_best_items(matches_stats)
            playstyle     = analyzer.analyze_playstyle(matches_stats)
            advice        = analyzer.generate_coach_advice(matches_stats)

            latest = matches_stats[0]
            icon_id = summoner.get("profileIconId", 29)
            level   = summoner.get("summonerLevel", "?")

            ranked_solo = next((r for r in rank_data if r.get("queueType") == "RANKED_SOLO_5x5"), None)
            ranked_flex = next((r for r in rank_data if r.get("queueType") == "RANKED_FLEX_SR"), None)

            # ── TAB 1: RESUMEN ─────────────────────────────────────────────────
            with tab_perfil:
                # Player header
                col_icon, col_name, col_ranks = st.columns([1, 3, 3])
                with col_icon:
                    st.markdown(f'<img src="{profile_icon_url(icon_id)}" style="width:90px;border-radius:50%;border:3px solid #3b82f6;box-shadow:0 4px 15px rgba(59,130,246,0.3);">', unsafe_allow_html=True)
                with col_name:
                    st.markdown(f"<h2 style='margin:0;'>{riot_name}<span style='color:#64748b;font-size:1rem;'>#{riot_tag}</span></h2>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#94a3b8;'>Nivel {level} · {region}</span>", unsafe_allow_html=True)
                with col_ranks:
                    for rk in [ranked_solo, ranked_flex]:
                        if rk:
                            tier = rk["tier"]
                            color = RANK_COLORS.get(tier, "#fff")
                            emoji = RANK_EMOJIS.get(tier, "")
                            label = "Solo/Duo" if rk["queueType"] == "RANKED_SOLO_5x5" else "Flex"
                            wins_r, losses_r = rk["wins"], rk["losses"]
                            wr_r = round(wins_r / max(1, wins_r + losses_r) * 100, 1)
                            st.markdown(f"""
                            <div style="background:rgba(30,41,59,0.5);border:1px solid {color}33;border-radius:10px;
                                        padding:8px 14px;margin-bottom:6px;">
                              <span style="font-size:0.75rem;color:#64748b;">{label}</span><br>
                              <span style="font-size:1.1rem;font-weight:700;color:{color};">{emoji} {tier} {rk['rank']} — {rk['leaguePoints']} LP</span><br>
                              <span style="font-size:0.8rem;color:#94a3b8;">{wins_r}V {losses_r}D · {wr_r}% WR</span>
                            </div>
                            """, unsafe_allow_html=True)

                st.markdown("---")

                # Quick stats
                m1, m2, m3, m4, m5, m6 = st.columns(6)
                m1.metric("Partidas", agg["games"])
                m2.metric("Winrate", f"{agg['win_rate']}%")
                m3.metric("KDA Prom.", agg["avg_kda"])
                m4.metric("CS/min", agg["avg_cs_pm"])
                m5.metric("KP%", f"{agg['avg_kp']}%")
                m6.metric("Visión/min", agg["avg_vision_pm"])

                st.markdown("---")

                # Last match highlight
                col_last, col_gd = st.columns([3, 2])
                with col_last:
                    st.markdown("#### Última Partida")
                    badge_cls = "win-badge" if latest["win"] else "loss-badge"
                    badge_txt = "VICTORIA" if latest["win"] else "DERROTA"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:14px;padding:1rem;
                                background:rgba(30,41,59,0.4);border-radius:12px;">
                      <img src="{champion_img_url(latest['championName'])}" width="70" style="border-radius:10px;">
                      <div>
                        <h3 style="margin:0;">{latest['championName']}</h3>
                        <span class="rank-badge {badge_cls}">{badge_txt}</span>
                        <p style="margin:4px 0 0;color:#94a3b8;font-size:0.85rem;">
                          {latest['kills']}/{latest['deaths']}/{latest['assists']} ·
                          {latest['cs_per_min']} CS/min · {latest['kill_participation']}% KP
                        </p>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_gd:
                    st.markdown("#### Fase de Líneas (min 15)")
                    gd = latest.get("gold_diff_15")
                    if gd is not None:
                        color_gd = "#10b981" if gd >= 0 else "#ef4444"
                        sign = "+" if gd >= 0 else ""
                        msg = "Dominaste la línea" if gd > 300 else ("Línea perdida" if gd < -300 else "Línea equilibrada")
                        st.markdown(f"""
                        <div style="text-align:center;padding:1rem;background:rgba(30,41,59,0.4);border-radius:12px;">
                          <div style="font-size:2rem;font-weight:800;color:{color_gd};">{sign}{gd}g</div>
                          <div style="color:#94a3b8;">{msg}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("Sin datos de timeline (ARAM u otro modo)")

                st.markdown("---")

                # Champion mastery
                if mastery:
                    st.markdown("#### Maestría de Campeones")
                    mcols = st.columns(min(5, len(mastery)))
                    for i, m in enumerate(mastery[:5]):
                        cname = m.get("championName", str(m.get("championId", "?")))
                        pts = m.get("championPoints", 0)
                        lvl = m.get("championLevel", 0)
                        with mcols[i]:
                            st.markdown(f"""
                            <div class="stat-card">
                              <img src="{champion_img_url(cname)}" width="60" style="border-radius:8px;">
                              <div style="font-size:0.85rem;margin-top:6px;">{cname}</div>
                              <div style="color:#fbbf24;font-size:0.75rem;">Nivel {lvl}</div>
                              <div style="color:#64748b;font-size:0.7rem;">{pts:,} pts</div>
                            </div>
                            """, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("#### Historial de Partidas")
                rows = []
                for m in matches_stats:
                    rows.append({
                        "Campeón": m["championName"],
                        "Rol": m["position_label"],
                        "Resultado": "✅ Victoria" if m["win"] else "❌ Derrota",
                        "KDA": f"{m['kills']}/{m['deaths']}/{m['assists']} ({m['kda']})",
                        "CS/min": m["cs_per_min"],
                        "Daño/min": m["damage_per_min"],
                        "KP%": f"{m['kill_participation']}%",
                    })
                df_hist = pd.DataFrame(rows)
                st.dataframe(df_hist, use_container_width=True, hide_index=True)


            # ── TAB 2: CAMPEONES ────────────────────────────────────────────────
            with tab_champs:
                st.header("Estadísticas por Campeón")

                if champ_stats:
                    # Win rate chart
                    df_champs = pd.DataFrame(champ_stats)

                    fig_wr = go.Figure()
                    fig_wr.add_trace(go.Bar(
                        y=df_champs["champion"],
                        x=df_champs["win_rate"],
                        orientation="h",
                        marker=dict(
                            color=df_champs["win_rate"],
                            colorscale=[[0, "#ef4444"], [0.5, "#f59e0b"], [1, "#10b981"]],
                            cmin=30, cmax=70,
                            showscale=True,
                            colorbar=dict(title="WR%", thickness=12),
                        ),
                        text=[f"{wr}% ({g}g)" for wr, g in zip(df_champs["win_rate"], df_champs["games"])],
                        textposition="outside",
                        hovertemplate="<b>%{y}</b><br>WR: %{x}%<extra></extra>",
                    ))
                    fig_wr.add_vline(x=50, line_dash="dash", line_color="rgba(255,255,255,0.3)")
                    fig_wr.update_layout(
                        title="Winrate por Campeón",
                        xaxis_title="Winrate %", yaxis_title="",
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#e2e8f0"),
                        height=max(300, len(df_champs) * 40),
                        margin=dict(l=10, r=80, t=40, b=20),
                        yaxis=dict(autorange="reversed"),
                    )
                    st.plotly_chart(fig_wr, use_container_width=True)

                    # KDA by champion
                    fig_kda = go.Figure()
                    fig_kda.add_trace(go.Bar(
                        x=df_champs["champion"],
                        y=df_champs["kda"],
                        marker_color=[
                            "#ef4444" if k < 2 else ("#f59e0b" if k < 3 else "#10b981")
                            for k in df_champs["kda"]
                        ],
                        text=df_champs["kda"],
                        textposition="outside",
                        hovertemplate="<b>%{x}</b><br>KDA: %{y}<extra></extra>",
                    ))
                    role_thresh_champs, _ = analyzer.get_role_thresholds_for_display(matches_stats)
                    kda_ref = role_thresh_champs["kda"]
                    fig_kda.add_hline(y=kda_ref, line_dash="dash", line_color="#60a5fa",
                                      annotation_text=f"Obj {role_thresh_champs['label']} ({kda_ref})",
                                      annotation_position="top right")
                    fig_kda.update_layout(
                        title="KDA Promedio por Campeón",
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#e2e8f0"), height=350,
                        margin=dict(l=20, r=20, t=40, b=20),
                    )
                    st.plotly_chart(fig_kda, use_container_width=True)

                    # Table
                    st.markdown("#### Tabla detallada")
                    display_cols = ["champion", "games", "win_rate", "kda",
                                    "avg_kills", "avg_deaths", "avg_assists",
                                    "avg_cs_pm", "avg_dmg_pm", "avg_kp"]
                    col_labels = {
                        "champion": "Campeón", "games": "Partidas", "win_rate": "WR%",
                        "kda": "KDA", "avg_kills": "K", "avg_deaths": "D",
                        "avg_assists": "A", "avg_cs_pm": "CS/min",
                        "avg_dmg_pm": "Daño/min", "avg_kp": "KP%",
                    }
                    st.dataframe(
                        df_champs[display_cols].rename(columns=col_labels),
                        use_container_width=True, hide_index=True
                    )

                # Matchups
                if matchups:
                    st.markdown("---")
                    st.markdown("#### Match-Ups (Historial vs Rivales)")
                    col_good, col_bad = st.columns(2)

                    sorted_mu = sorted(matchups, key=lambda x: x["win_rate"], reverse=True)
                    good = [m for m in sorted_mu if m["win_rate"] >= 50][:5]
                    bad  = [m for m in sorted_mu if m["win_rate"] < 50][-5:]
                    bad.reverse()

                    with col_good:
                        st.markdown("**Mejores Match-Ups** (más victorias)")
                        for m in good:
                            img = champion_img_url(m["opponent"])
                            st.markdown(f"""
                            <div style="display:flex;align-items:center;gap:10px;
                                        padding:6px 10px;background:rgba(16,185,129,0.08);
                                        border-radius:8px;margin-bottom:5px;border:1px solid rgba(16,185,129,0.2);">
                              <img src="{img}" width="32" style="border-radius:6px;">
                              <span style="flex:1;">{m['opponent']}</span>
                              <span style="color:#10b981;font-weight:700;">{m['win_rate']}%</span>
                              <span style="color:#64748b;font-size:0.8rem;">{m['wins']}V{m['losses']}D</span>
                            </div>
                            """, unsafe_allow_html=True)

                    with col_bad:
                        st.markdown("**Peores Match-Ups** (más derrotas)")
                        for m in bad:
                            img = champion_img_url(m["opponent"])
                            st.markdown(f"""
                            <div style="display:flex;align-items:center;gap:10px;
                                        padding:6px 10px;background:rgba(239,68,68,0.08);
                                        border-radius:8px;margin-bottom:5px;border:1px solid rgba(239,68,68,0.2);">
                              <img src="{img}" width="32" style="border-radius:6px;">
                              <span style="flex:1;">{m['opponent']}</span>
                              <span style="color:#ef4444;font-weight:700;">{m['win_rate']}%</span>
                              <span style="color:#64748b;font-size:0.8rem;">{m['wins']}V{m['losses']}D</span>
                            </div>
                            """, unsafe_allow_html=True)

                # Best items
                if best_items:
                    st.markdown("---")
                    st.markdown("#### Objetos más usados en Victorias")
                    item_cols = st.columns(min(6, len(best_items)))
                    for i, item in enumerate(best_items[:6]):
                        with item_cols[i]:
                            iname = get_item_name(item["item_id"])
                            img   = item_img_url(item["item_id"])
                            color = "#10b981" if item["win_rate"] >= 55 else ("#f59e0b" if item["win_rate"] >= 48 else "#ef4444")
                            st.markdown(f"""
                            <div class="stat-card">
                              <img src="{img}" width="50" style="border-radius:8px;">
                              <div style="font-size:0.7rem;margin-top:6px;color:#cbd5e1;">{iname[:18]}</div>
                              <div style="color:{color};font-weight:700;">{item['win_rate']}%</div>
                              <div style="color:#64748b;font-size:0.7rem;">{item['games']} partidas</div>
                            </div>
                            """, unsafe_allow_html=True)


            # ── TAB 3: RENDIMIENTO ──────────────────────────────────────────────
            with tab_render:
                st.header("Evolución del Rendimiento")

                reversed_matches = list(reversed(matches_stats))
                x_labels = [f"P{i+1}" for i in range(len(reversed_matches))]

                col_l, col_r = st.columns(2)

                with col_l:
                    # KDA trend
                    fig_kda_trend = go.Figure()
                    fig_kda_trend.add_trace(go.Scatter(
                        x=x_labels, y=[m["kda"] for m in reversed_matches],
                        mode="lines+markers",
                        line=dict(color="#60a5fa", width=2),
                        marker=dict(
                            size=10,
                            color=["#10b981" if m["win"] else "#ef4444" for m in reversed_matches],
                            line=dict(width=2, color="#60a5fa"),
                        ),
                        name="KDA",
                        hovertemplate="<b>%{x}</b><br>KDA: %{y}<extra></extra>",
                    ))
                    fig_kda_trend.add_hline(y=2.8, line_dash="dot", line_color="rgba(255,255,255,0.3)",
                                            annotation_text="Platino")
                    fig_kda_trend.update_layout(
                        title="KDA por Partida", height=300,
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,41,59,0.3)",
                        font=dict(color="#e2e8f0"), margin=dict(l=20, r=20, t=40, b=20),
                        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                    )
                    st.plotly_chart(fig_kda_trend, use_container_width=True)

                    # CS trend
                    fig_cs = go.Figure()
                    fig_cs.add_trace(go.Scatter(
                        x=x_labels, y=[m["cs_per_min"] for m in reversed_matches],
                        mode="lines+markers", fill="tozeroy",
                        line=dict(color="#a78bfa", width=2),
                        fillcolor="rgba(167,139,250,0.1)",
                        hovertemplate="<b>%{x}</b><br>CS/min: %{y}<extra></extra>",
                    ))
                    fig_cs.add_hline(y=6.5, line_dash="dot", line_color="rgba(255,255,255,0.3)",
                                     annotation_text="Objetivo")
                    fig_cs.update_layout(
                        title="CS/min por Partida", height=300,
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,41,59,0.3)",
                        font=dict(color="#e2e8f0"), margin=dict(l=20, r=20, t=40, b=20),
                        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                    )
                    st.plotly_chart(fig_cs, use_container_width=True)

                with col_r:
                    # Damage trend
                    fig_dmg = go.Figure()
                    fig_dmg.add_trace(go.Bar(
                        x=x_labels, y=[m["damage_per_min"] for m in reversed_matches],
                        marker_color=["#10b981" if m["win"] else "#ef4444" for m in reversed_matches],
                        hovertemplate="<b>%{x}</b><br>Daño/min: %{y}<extra></extra>",
                    ))
                    fig_dmg.update_layout(
                        title="Daño/min por Partida", height=300,
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,41,59,0.3)",
                        font=dict(color="#e2e8f0"), margin=dict(l=20, r=20, t=40, b=20),
                        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                    )
                    st.plotly_chart(fig_dmg, use_container_width=True)

                    # Gold diff @15
                    gd_matches = [m for m in reversed_matches if m.get("gold_diff_15") is not None]
                    if gd_matches:
                        gd_x = [f"P{reversed_matches.index(m)+1}" for m in gd_matches]
                        gd_y = [m["gold_diff_15"] for m in gd_matches]
                        fig_gd = go.Figure()
                        fig_gd.add_trace(go.Bar(
                            x=gd_x, y=gd_y,
                            marker_color=["#10b981" if g >= 0 else "#ef4444" for g in gd_y],
                            hovertemplate="<b>%{x}</b><br>Gold diff @15: %{y}g<extra></extra>",
                        ))
                        fig_gd.add_hline(y=0, line_color="rgba(255,255,255,0.3)")
                        fig_gd.update_layout(
                            title="Diferencia de Oro @15 min", height=300,
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,41,59,0.3)",
                            font=dict(color="#e2e8f0"), margin=dict(l=20, r=20, t=40, b=20),
                            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                        )
                        st.plotly_chart(fig_gd, use_container_width=True)

                # Role distribution
                st.markdown("---")
                col_rd, col_wp = st.columns(2)
                with col_rd:
                    if role_stats:
                        fig_roles = go.Figure(go.Pie(
                            labels=[r["role"] for r in role_stats],
                            values=[r["games"] for r in role_stats],
                            hole=0.45,
                            marker_colors=["#60a5fa","#a78bfa","#34d399","#f59e0b","#f87171"],
                            textinfo="label+percent",
                        ))
                        fig_roles.update_layout(
                            title="Distribución de Roles", height=320,
                            paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"),
                            showlegend=False, margin=dict(l=20, r=20, t=40, b=20),
                        )
                        st.plotly_chart(fig_roles, use_container_width=True)

                with col_wp:
                    # Win rate by role
                    if role_stats:
                        fig_rwr = go.Figure(go.Bar(
                            x=[r["role"] for r in role_stats],
                            y=[r["win_rate"] for r in role_stats],
                            marker_color=[
                                "#10b981" if r["win_rate"] >= 55 else
                                ("#f59e0b" if r["win_rate"] >= 48 else "#ef4444")
                                for r in role_stats
                            ],
                            text=[f"{r['win_rate']}%" for r in role_stats],
                            textposition="outside",
                        ))
                        fig_rwr.add_hline(y=50, line_dash="dash", line_color="rgba(255,255,255,0.3)")
                        fig_rwr.update_layout(
                            title="Winrate por Rol", height=320,
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,41,59,0.3)",
                            font=dict(color="#e2e8f0"), margin=dict(l=20, r=20, t=40, b=20),
                            yaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.05)"),
                        )
                        st.plotly_chart(fig_rwr, use_container_width=True)


            # ── TAB 4: ESTILO DE JUEGO ──────────────────────────────────────────
            with tab_estilo:
                st.header("Análisis de Estilo de Juego")

                if playstyle:
                    col_radar, col_info = st.columns([1, 1])

                    with col_radar:
                        cats   = list(playstyle["scores"].keys())
                        vals   = list(playstyle["scores"].values())
                        vals_c = vals + [vals[0]]
                        cats_c = cats + [cats[0]]

                        fig_radar = go.Figure(go.Scatterpolar(
                            r=vals_c, theta=cats_c,
                            fill="toself", fillcolor="rgba(96,165,250,0.15)",
                            line=dict(color="#60a5fa", width=2),
                            marker=dict(size=6, color="#60a5fa"),
                        ))
                        fig_radar.update_layout(
                            polar=dict(
                                radialaxis=dict(visible=True, range=[0, 100],
                                                tickfont=dict(size=9, color="#64748b"),
                                                gridcolor="rgba(255,255,255,0.1)"),
                                angularaxis=dict(tickfont=dict(size=11, color="#e2e8f0")),
                                bgcolor="rgba(15,23,42,0.5)",
                            ),
                            paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#e2e8f0"),
                            height=380,
                            margin=dict(l=30, r=30, t=30, b=30),
                        )
                        st.plotly_chart(fig_radar, use_container_width=True)

                    with col_info:
                        st.markdown(f"""
                        <div style="background:rgba(30,41,59,0.5);border-radius:14px;padding:1.5rem;
                                    border:1px solid rgba(96,165,250,0.3);margin-bottom:1rem;">
                          <div style="color:#64748b;font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;">
                            Estilo de Juego
                          </div>
                          <div style="font-size:1.8rem;font-weight:800;color:#60a5fa;margin:6px 0;">
                            {playstyle['playstyle']}
                          </div>
                          <div style="color:#cbd5e1;font-size:0.9rem;">{playstyle['description']}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Stats summary
                        s_cols = st.columns(3)
                        s_cols[0].metric("WR Global", f"{playstyle['win_rate']}%")
                        s_cols[1].metric("KDA Prom.", playstyle["avg_kda"])
                        s_cols[2].metric("CS/min", playstyle["avg_cs"])
                        s2_cols = st.columns(3)
                        s2_cols[0].metric("KP%", f"{playstyle['avg_kp']}%")
                        s2_cols[1].metric("Visión/min", playstyle["avg_vision"])
                        s2_cols[2].metric("Daño/min", int(playstyle["avg_damage"]))

                        # Strengths
                        if playstyle["strengths"]:
                            st.markdown("**Puntos Fuertes:**")
                            for s, desc in playstyle["strengths"]:
                                st.markdown(f"""
                                <div style="padding:8px 12px;background:rgba(16,185,129,0.1);
                                            border-left:3px solid #10b981;border-radius:0 8px 8px 0;
                                            margin-bottom:6px;">
                                  <span style="color:#10b981;font-weight:600;">✓ {s}</span>
                                  <span style="color:#94a3b8;font-size:0.82rem;"> — {desc}</span>
                                </div>
                                """, unsafe_allow_html=True)

                        # Weaknesses
                        if playstyle["weaknesses"]:
                            st.markdown("**Áreas de Mejora:**")
                            for w, desc in playstyle["weaknesses"]:
                                st.markdown(f"""
                                <div style="padding:8px 12px;background:rgba(239,68,68,0.1);
                                            border-left:3px solid #ef4444;border-radius:0 8px 8px 0;
                                            margin-bottom:6px;">
                                  <span style="color:#ef4444;font-weight:600;">✗ {w}</span>
                                  <span style="color:#94a3b8;font-size:0.82rem;"> — {desc}</span>
                                </div>
                                """, unsafe_allow_html=True)

                    st.markdown("---")
                    # Top champions recommendation
                    if champ_stats:
                        st.markdown("#### Mejores Campeones en tu Pool")
                        top_champs = sorted(
                            [c for c in champ_stats if c["games"] >= 2],
                            key=lambda x: (x["win_rate"], x["kda"]),
                            reverse=True
                        )[:5]
                        if not top_champs:
                            top_champs = champ_stats[:5]

                        tc_cols = st.columns(min(5, len(top_champs)))
                        for i, champ in enumerate(top_champs):
                            with tc_cols[i]:
                                color_wr = "#10b981" if champ["win_rate"] >= 55 else ("#f59e0b" if champ["win_rate"] >= 48 else "#ef4444")
                                st.markdown(f"""
                                <div class="stat-card">
                                  <img src="{champion_img_url(champ['champion'])}" width="60" style="border-radius:10px;">
                                  <div style="font-weight:600;margin-top:8px;">{champ['champion']}</div>
                                  <div style="color:{color_wr};font-size:1.1rem;font-weight:700;">{champ['win_rate']}%</div>
                                  <div style="color:#94a3b8;font-size:0.8rem;">KDA {champ['kda']} · {champ['games']}g</div>
                                </div>
                                """, unsafe_allow_html=True)


            # ── TAB 6: IA COACH ─────────────────────────────────────────────────
            with tab_coach:
                role_thresh, role_key = analyzer.get_role_thresholds_for_display(matches_stats)
                role_label_coach = role_thresh["label"]

                st.header("IA Coach — Evaluación Personalizada")
                st.markdown(
                    f"*Análisis basado en las últimas **{agg['games']}** partidas de **{riot_name}#{riot_tag}** "
                    f"— umbrales ajustados para **{role_label_coach}***"
                )
                st.markdown("---")

                type_map = {
                    "success": st.success,
                    "warning": st.warning,
                    "error": st.error,
                    "info": st.info,
                }
                icons = {"success": "🟢", "warning": "🟡", "error": "🔴", "info": "🔵"}

                for level, msg in advice:
                    fn = type_map.get(level, st.info)
                    fn(f"{icons.get(level, '')} {msg}")

                st.markdown("---")
                st.markdown(f"#### Comparativa vs Umbrales — {role_label_coach}")

                # Métricas relevantes según el rol detectado
                role_metrics = [
                    ("KDA", agg["avg_kda"], role_thresh["kda"]),
                    ("Daño/min", agg["avg_damage_pm"], role_thresh["damage_per_min"]),
                    ("Visión/min", agg["avg_vision_pm"], role_thresh["vision_per_min"]),
                    ("KP%", agg["avg_kp"], role_thresh["kp"]),
                ]
                if role_thresh["show_cs"] and role_thresh["cs_per_min"] is not None:
                    role_metrics.insert(1, ("CS/min", agg["avg_cs_pm"], role_thresh["cs_per_min"]))

                th_cols = st.columns(len(role_metrics))
                for i, (label, val, target) in enumerate(role_metrics):
                    pct = min(100, round((val / target) * 100)) if target else 100
                    color = "#10b981" if pct >= 100 else ("#f59e0b" if pct >= 75 else "#ef4444")
                    with th_cols[i]:
                        st.markdown(f"""
                        <div class="stat-card">
                          <div style="color:#94a3b8;font-size:0.75rem;text-transform:uppercase;">{label}</div>
                          <div style="font-size:1.5rem;font-weight:800;color:{color};">{val}</div>
                          <div style="color:#64748b;font-size:0.8rem;">Obj {role_label_coach}: {target}</div>
                          <div style="background:rgba(255,255,255,0.1);border-radius:4px;height:6px;margin-top:8px;">
                            <div style="width:{pct}%;background:{color};height:100%;border-radius:4px;"></div>
                          </div>
                          <div style="color:#64748b;font-size:0.7rem;margin-top:4px;">{pct}% del objetivo</div>
                        </div>
                        """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error procesando los datos: {e}")
            st.exception(e)
