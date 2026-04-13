import streamlit as st
import pandas as pd
from src.riot_client import NexusClient
from src.analyzer import MatchAnalyzer

st.set_page_config(page_title="Nexus Lens Pro", page_icon="🧿", layout="wide")

# --- CUSTOM CSS PARA MEJORAR EL LOOK & FEEL ---
st.markdown("""
<style>
    /* Efecto gradiente de fondo para ambiente gamer/premium */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }

    /* Botones primarios */
    .stButton>button {
        background: linear-gradient(45deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.5rem 2rem !important;
        transition: transform 0.2s ease-in-out !important;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }

    /* Títulos atractivos con texto fluido */
    h1 {
        background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -1px;
    }

    /* Modificación de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Métricas estilizadas */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800;
        color: #e2e8f0;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Tablas */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Contenedores de tarjeta (cards) manuales */
    .card-meta {
        background: rgba(30, 41, 59, 0.4); 
        padding: 1.5rem; 
        border-radius: 16px; 
        text-align: center; 
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .card-meta:hover {
        transform: translateY(-5px);
        background: rgba(30, 41, 59, 0.7); 
        border: 1px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_services():
    return NexusClient(), MatchAnalyzer()

try:
    client, analyzer = get_services()
except Exception as e:
    st.error(f"Error inicializando servicios. Asegúrate de tener el archivo .env con la API_KEY. Detalles: {e}")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://ddragon.leagueoflegends.com/cdn/14.5.1/img/profileicon/29.png", width=80)
    st.title("Nexus Lens Pro")
    st.markdown("Analiza tu rendimiento y asciende de liga.")
    st.markdown("---")
    riot_name = st.text_input("Game Name", "Faker")
    riot_tag = st.text_input("Tag Line", "T1")
    analyze_btn = st.button("Analizar Partidas")

# --- META TAB LOGIC ---
# Formato: (Nombre_Para_Mostrar, Nombre_DDragon)
GOD_TIER = {
    "TOP": [("Darius", "Darius"), ("Aatrox", "Aatrox"), ("Garen", "Garen")],
    "JUNGLE": [("Lee Sin", "LeeSin"), ("Jarvan IV", "JarvanIV"), ("Viego", "Viego")],
    "MIDDLE": [("Ahri", "Ahri"), ("Sylas", "Sylas"), ("LeBlanc", "Leblanc")],
    "ADC": [("Jinx", "Jinx"), ("Ezreal", "Ezreal"), ("Lucian", "Lucian")],
    "UTILITY": [("Thresh", "Thresh"), ("Nautilus", "Nautilus"), ("Lulu", "Lulu")]
}

# --- MAIN LAYOUT ---
st.title("🧿 Nexus Lens Pro")

tab1, tab2, tab3 = st.tabs(["📊 Mi Perfil", "🔥 Tier List Global", "🧠 IA Coach"])

with tab2:
    st.header("Meta del Parche Actual")
    st.markdown("La selección de campeones recomendada estadísticamente para asegurar la fase de líneas, presentados en calidad *God Tier*.")
    
    for rol, champs in GOD_TIER.items():
        st.markdown(f"<h3 style='color:#94a3b8; font-weight: 300; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;'>{rol.capitalize()}</h3>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, (display_name, dd_name) in enumerate(champs):
            with cols[i]:
                st.markdown(f'''
                <div class="card-meta">
                    <img src="https://ddragon.leagueoflegends.com/cdn/14.5.1/img/champion/{dd_name}.png" 
                         style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid #3b82f6; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">
                    <h4 style="margin: 0; color: #f8fafc; font-size: 1.2rem;">{display_name}</h4>
                </div>
                <br>
                ''', unsafe_allow_html=True)

if analyze_btn:
    if not riot_name or not riot_tag:
        st.sidebar.error("Por favor, introduce tu Game Name y Tag Line")
    else:
        with st.spinner("Conectando con los servidores de Riot y trazando timeline..."):
            try:
                puuid = client.get_puuid_by_riot_id(riot_name.strip(), riot_tag.strip())
                match_ids = client.get_match_ids(puuid, count=5)
                
                if not match_ids:
                    st.warning("No se encontraron partidas para este jugador.")
                else:
                    matches_stats = []
                    for i, mid in enumerate(match_ids):
                        data = client.get_match_details(mid)
                        timeline = client.get_match_timeline(mid) if i == 0 else None
                        
                        stats = analyzer.analyze_match(data, puuid, timeline)
                        if stats:
                            matches_stats.append(stats)
                    
                    if matches_stats:
                        latest = matches_stats[0]
                        
                        # --- TABLA 1: MI PERFIL ---
                        with tab1:
                            # Header Principal Dinámico con el avatar de su campeón
                            c_img, c_info = st.columns([1, 6])
                            with c_img:
                                st.markdown(f'''
                                <img src="https://ddragon.leagueoflegends.com/cdn/14.5.1/img/champion/{latest['championName']}.png" 
                                     style="width: 100px; border-radius: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.6); border: 2px solid rgba(255,255,255,0.1);">
                                ''', unsafe_allow_html=True)
                            with c_info:
                                status_color = "#10b981" if latest['win'] else "#ef4444"
                                badge = "V I C T O R I A" if latest['win'] else "D E R R O T A"
                                st.markdown(f'''
                                <div style="display: flex; flex-direction: column; justify-content: center; height: 100px;">
                                    <h3 style="margin: 0; font-weight: 300; color: #cbd5e1;">Análisis de la última partida</h3>
                                    <h2 style="margin: 0; padding: 0; font-size: 2.2rem;">{latest['championName']} <span style="background: {status_color}; text-shadow: none; font-size: 0.8rem; letter-spacing: 2px; border-radius: 4px; padding: 4px 8px; vertical-align: middle; color: white;">{badge}</span></h2>
                                </div>
                                ''', unsafe_allow_html=True)
                                
                            st.write("") # Spacer
                            
                            # Metrics
                            c1, c2, c3, c4 = st.columns(4)
                            c1.metric("KDA", latest['kda'])
                            c2.metric("Mínions / Minuto", latest['cs_per_min'])
                            c3.metric("Kill Participation", f"{latest['kill_participation']}%")
                            c4.metric("Puntuación Visión / Min", latest['vision_per_min'])
                            
                            st.markdown("---")
                            
                            # Análisis de oro profundo (Timeline)
                            st.markdown("### ⚔️ Control de Fase de Líneas (Min 15)")
                            gd = latest.get('gold_diff_15')
                            if gd is not None:
                                delta_color = "normal" if gd >= 0 else "inverse"
                                impact_message = "Ganaste contundentemente el lado de oro" if gd > 300 else ("Perdiste recursos frente al rival" if gd < -300 else "Mucha igualdad en farmeo")
                                
                                gc1, gc2 = st.columns([1, 2])
                                gc1.metric("Diferencia de Oro", f"{gd}g", delta_color=delta_color)
                                gc2.info(f"💡 **Cálculo exacto en Minuto 15:** Extraído segundo a segundo del timeline oficial frente a tu rival directo de línea. *{impact_message}*.")
                            else:
                                st.warning("No se pudieron extraer datos del minuto 15 para esta partida. (¿Fue ARAM o terminó antes de tiempo?)")
                                
                            st.markdown("---")
                            
                            st.markdown("### 📚 Historial Reciente")
                            df = pd.DataFrame(matches_stats)[['championName', 'teamPosition', 'win', 'kda', 'cs_per_min', 'kill_participation']]
                            df.columns = ['Campeón', 'Posición', 'Victoria', 'KDA', 'CS / Min', 'KP %']
                            df['Victoria'] = df['Victoria'].apply(lambda x: "✅ Sí" if x else "❌ No")
                            st.table(df)

                        # --- TABLA 3: IA COACH ---
                        with tab3:
                            st.header("Evaluación del Coach Digital")
                            st.markdown("He analizado tus patrones en las últimas 5 partidas utilizando las bases de conocimiento de control de macro-estrategia. Aquí tienes mi valoración:")
                            advice_list = analyzer.generate_coach_advice(matches_stats)
                            
                            for adv in advice_list:
                                if "Excelente" in adv or "Destrozaste" in adv or "sólid" in adv:
                                    st.success("🟢 " + adv)
                                elif "considera tomar un descanso" in adv or "perdiste la fase" in adv:
                                    st.error("🔴 " + adv)
                                else:
                                    st.warning("🟡 " + adv)

            except Exception as e:
                st.error(f"Error procesando los datos. Revisa la Riot API Key o la ortografía del Riot ID. Excepción: {e}")
