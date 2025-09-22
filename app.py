import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import time
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

# --- CARREGAR VARIÁVEIS DE AMBIENTE ---
load_dotenv()

# --- 1. CONFIGURAÇÃO DA PÁGINA E TEMA APRIMORADO ---
st.set_page_config(
    page_title=os.getenv("APP_TITLE", "Programa +GEMS"),
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': f"# {os.getenv('APP_TITLE', 'Programa +GEMS')}\n*{os.getenv('APP_DESCRIPTION', 'Forje sua lenda, Herói!')}*"
    }
)

# --- 2. ESTILIZAÇÃO COM PALETA CLEAN ---
primary_color = os.getenv("STREAMLIT_THEME_PRIMARY_COLOR", "#6B7E7D")
background_color = os.getenv("STREAMLIT_THEME_BACKGROUND_COLOR", "#FFFFFF")

st.markdown(f"""
<style>
    /* Importar fonte do Google */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Paleta Clean */
    :root {{
        --primary-color: {primary_color};        /* Verde acinzentado */
        --secondary-color: #A8A8A8;      /* Cinza claro */
        --accent-color: #D4A574;         /* Salmão suave */
        --highlight-color: #B07A57;      /* Marrom suave */
        --success-color: #7FB069;        /* Verde suave */
        --warning-color: #E8B04B;        /* Amarelo suave */
        --error-color: #E85A4F;          /* Vermelho suave */
        --text-primary: #2F3E46;
        --text-secondary: #52796F;
        --background-light: #F8F9FA;
        --background-card: {background_color};
        --border-color: #E8EFEE;
        --shadow: 0 2px 8px rgba(107, 126, 125, 0.08);
        --shadow-hover: 0 4px 16px rgba(107, 126, 125, 0.12);
        --border-radius: 12px;
    }}

    /* Fonte global */
    .main * {{
        font-family: 'Inter', sans-serif !important;
    }}

    /* Header personalizado */
    .custom-header {{
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 2rem 1.5rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow);
    }}

    /* Cards de KPI clean */
    div[data-testid="stMetric"] {{
        background: var(--background-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}

    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
        border-color: var(--primary-color);
    }}

    div[data-testid="stMetric"]::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    }}

    /* Botões clean */
    .stButton > button[kind="primary"] {{
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }}

    .stButton > button[kind="primary"]:hover {{
        background: var(--highlight-color);
        transform: translateY(-1px);
        box-shadow: var(--shadow-hover);
    }}

    .stButton > button[kind="secondary"] {{
        background: var(--background-card);
        color: var(--error-color);
        border: 1px solid var(--error-color);
        border-radius: var(--border-radius);
        font-weight: 500;
        transition: all 0.3s ease;
    }}

    .stButton > button[kind="secondary"]:hover {{
        background: var(--error-color);
        color: white;
        transform: translateY(-1px);
    }}

    /* Containers clean */
    .stContainer {{
        border-radius: var(--border-radius);
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        background: var(--background-card);
    }}

    /* Feed item com imagem */
    .feed-item {{
        background: var(--background-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}

    .feed-item:hover {{
        transform: translateX(4px);
        box-shadow: var(--shadow);
        border-color: var(--primary-color);
    }}

    .pillar-icon {{
        width: 40px;
        height: 40px;
        border-radius: 8px;
        object-fit: cover;
        flex-shrink: 0;
    }}

    /* Progress bars clean */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        border-radius: 6px;
    }}

    /* Sidebar clean */
    .css-1d391kg {{
        background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
    }}

    .css-1d391kg .stButton > button {{
        background: transparent;
        color: white;
        border: 1px solid transparent;
        border-radius: var(--border-radius);
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
        font-weight: 500;
    }}

    .css-1d391kg .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.1);
        border-color: var(--accent-color);
        transform: translateX(4px);
    }}

    /* Formulários clean */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {{
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {{
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(107, 126, 125, 0.1);
    }}

    /* Tabs clean */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: var(--background-light);
        border-radius: var(--border-radius);
        color: var(--text-secondary);
        font-weight: 500;
    }}

    .stTabs [aria-selected="true"] {{
        background: var(--primary-color);
        color: white;
    }}

    /* Mission card */
    .mission-card {{
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: var(--background-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
    }}

    .mission-card:hover {{
        border-color: var(--primary-color);
        box-shadow: var(--shadow);
    }}

    /* Responsividade */
    @media (max-width: 768px) {{
        .custom-header {{
            padding: 1rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. CONSTANTES E INICIALIZAÇÃO DO AMBIENTE ---
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = Path(os.getenv("DATA_PATH", str(BASE_DIR)))
ANEXOS_DIR = Path(os.getenv("ANEXOS_PATH", str(BASE_DIR / "anexos")))
ANEXOS_DIR.mkdir(exist_ok=True)
DATA_PATH.mkdir(exist_ok=True)

DATA_FILES = {
    "hero": {
        "path": DATA_PATH / "dim_hero.csv", 
        "cols": ['id_hero', 'hero_name', 'hero_team', 'start_date', 'update_date']
    },
    "map": {
        "path": DATA_PATH / "dim_map.csv", 
        "cols": ['id_mission', 'mission_name', 'mission_discribe', 'GemsAwarded', 'id_pillar', 'pillar', 'start_date', 'update_date']
    },
    "nomination": {
        "path": DATA_PATH / "fact_nomeacao.csv", 
        "cols": ['id_nomeacao', 'data_submissao', 'id_nomeador', 'id_nomeado', 'id_missao', 'justificativa', 'status', 'caminho_anexo']
    },
}

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# --- 4. LOGGING (OPCIONAL) ---
import logging

log_level = os.getenv("LOG_LEVEL", "INFO")
log_file = os.getenv("LOG_FILE", "gems_program.log")

logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ] if DEBUG else [logging.FileHandler(log_file)]
)

logger = logging.getLogger(__name__)

# --- 5. COMPONENTES UI APRIMORADOS ---
def create_custom_header(title, subtitle="", icon="💎"):
    """Cria um header customizado e atraente"""
    st.markdown(f"""
    <div class="custom-header">
        <h1 style="margin: 0; font-size: 2.5rem;">{icon} {title}</h1>
        {f'<p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def get_pillar_image(pillar_name):
    """Busca a imagem do pilar baseada no nome"""
    if not pillar_name or pd.isna(pillar_name):
        return None

    image_filename = f"{pillar_name.strip().lower().replace(' ', '_')}.png"
    image_path = BASE_DIR / image_filename

    if image_path.exists():
        return str(image_path)
    return None

def display_pillar_icon(pillar_name, size="40px"):
    """Exibe o ícone do pilar"""
    image_path = get_pillar_image(pillar_name)
    if image_path:
        return f'<img src="data:image/png;base64,{get_image_base64(image_path)}" class="pillar-icon" style="width: {size}; height: {size};">'
    else:
        return f'<div style="width: {size}; height: {size}; background: var(--accent-color); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px;">🏛️</div>'

def get_image_base64(image_path):
    """Converte imagem para base64"""
    import base64
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logger.error(f"Erro ao converter imagem para base64: {e}")
        return ""

def show_loading_message(message="Processando..."):
    """Mostra uma mensagem de loading melhorada"""
    with st.spinner(message):
        time.sleep(0.3)
        return True

def create_success_animation():
    """Cria animação de sucesso"""
    st.balloons()
    time.sleep(1)

# --- 6. FUNÇÕES DE LÓGICA DE DADOS OTIMIZADAS ---
@st.cache_data(ttl=CACHE_TTL)
def load_data(file_key):
    config = DATA_FILES.get(file_key)
    file_path, columns = config["path"], config["cols"]
    
    if not file_path.exists():
        logger.info(f"Criando arquivo {file_path.name}")
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False, sep=';')
        return df
    
    try:
        df = pd.read_csv(file_path, sep=';', dtype=str)
        for col in columns:
            if col not in df.columns:
                df[col] = pd.NA
        logger.debug(f"Dados carregados de {file_path.name}: {len(df)} registros")
        return df.astype(str)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        logger.warning(f"Arquivo {file_path.name} vazio ou não encontrado")
        return pd.DataFrame(columns=columns)
    except Exception as e:
        logger.error(f"Erro crítico ao carregar {file_path.name}: {e}")
        st.error(f"Erro crítico ao carregar {file_path.name}: {e}")
        return pd.DataFrame(columns=columns)

def save_data(file_key, df):
    file_path = DATA_FILES.get(file_key)["path"]
    try:
        df.to_csv(file_path, index=False, sep=';')
        st.cache_data.clear()
        logger.info(f"Dados salvos em {file_path.name}: {len(df)} registros")
        return True
    except Exception as e:
        logger.error(f"Falha ao salvar dados em {file_path.name}: {e}")
        st.error(f"Falha ao salvar dados em {file_path.name}: {e}")
        return False

@st.cache_data(ttl=CACHE_TTL)
def get_dashboard_data():
    """Prepara dados para o dashboard com melhor performance"""
    df_heroes = load_data('hero')
    df_missions = load_data('map')
    df_nominations = load_data('nomination')

    if df_nominations.empty or df_missions.empty or df_heroes.empty:
        return pd.DataFrame()

    df_missions['GemsAwarded'] = pd.to_numeric(df_missions['GemsAwarded'], errors='coerce').fillna(0)
    df_nominations['data_submissao'] = pd.to_datetime(df_nominations['data_submissao'], errors='coerce')

    approved = df_nominations[df_nominations['status'].str.strip().str.lower() == 'aprovado'].copy()
    if approved.empty:
        return pd.DataFrame()

    data = approved.merge(df_heroes, left_on='id_nomeado', right_on='id_hero', suffixes=('_nomeado', '_hero'))
    data = data.rename(columns={'hero_name': 'Herói', 'hero_team': 'Time'})
    data = data.merge(df_heroes, left_on='id_nomeador', right_on='id_hero', suffixes=('', '_nomeador'))
    data = data.rename(columns={'hero_name': 'Nomeador'})
    data = data.merge(df_missions, left_on='id_missao', right_on='id_mission')

    return data[[
        'data_submissao', 'Herói', 'Time', 'Nomeador', 'mission_name', 
        'pillar', 'GemsAwarded', 'justificativa'
    ]]

# --- 7. PÁGINAS PRINCIPAIS ---
def pagina_home():
    app_title = os.getenv("APP_TITLE", "Programa +GEMS")
    app_description = os.getenv("APP_DESCRIPTION", "Forje sua lenda, Herói! Acumule GEMS e escreva seu nome no Salão dos Heróis.")
    
    create_custom_header(
        f"Bem-vindo ao {app_title}!",
        app_description,
        "💎"
    )

    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        # Verificar se a imagem existe
        capa_path = BASE_DIR / "Capa.png"
        if capa_path.exists():
            st.image(str(capa_path), use_container_width=True)
        else:
            st.markdown("### 💎 **Programa +GEMS**")
            st.info("📸 Adicione uma imagem 'Capa.png' na raiz do projeto para exibir aqui.")

    with col2:
        st.markdown("### 🚀 **Como começar sua jornada?**")

        tabs = st.tabs(["📍 Explorar", "🏆 Reconhecer", "📊 Acompanhar"])

        with tabs[0]:
            st.markdown("""
            **🗺️ Mapa dos Cristais**
            - Descubra todas as missões disponíveis
            - Veja as recompensas em GEMS
            - Explore os diferentes pilares de atuação
            """)
            if st.button("Ir para o Mapa 🗺️", use_container_width=True):
                st.session_state.current_page = "Mapa dos Cristais"
                st.rerun()

        with tabs[1]:
            st.markdown("""
            **📜 Pergaminho de Nomeações**
            - Indique colegas que fizeram feitos heroicos
            - Justifique suas nomeações
            - Anexe evidências do reconhecimento
            """)
            if st.button("Fazer Nomeação 📜", use_container_width=True):
                st.session_state.current_page = "Pergaminho de Nomeações"
                st.rerun()

        with tabs[2]:
            st.markdown("""
            **⚔️ Salão dos Heróis**
            - Veja o ranking dos participantes
            - Acompanhe as conquistas recentes
            - Analise estatísticas do programa
            """)
            if st.button("Ver Ranking ⚔️", use_container_width=True):
                st.session_state.current_page = "Salão dos Heróis"
                st.rerun()

        # Objetivo do Programa movido para baixo
        st.markdown("### 🎯 **Objetivo do Programa**")
        with st.container():
            st.info("Reconhecer e recompensar contribuições excepcionais através de um sistema de gamificação divertido e motivador.", icon="ℹ️")

def pagina_salao_dos_herois():
    create_custom_header(
        "Salão dos Heróis",
        "Acompanhe as lendas do reino, suas conquistas e os pilares mais valorizados.",
        "⚔️"
    )

    df = get_dashboard_data()

    if df.empty:
        st.warning("Ainda não há dados suficientes para exibir o dashboard. As nomeações precisam ser aprovadas primeiro.", icon="⚠️")
        return

    # --- FILTROS APRIMORADOS ---
    with st.container():
        st.markdown("### 🔍 **Filtros do Reino**")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            min_date = df['data_submissao'].min().date()
            max_date = df['data_submissao'].max().date()
            date_range = st.date_input(
                "📅 Período",
                (min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

        with col2:
            all_heroes = sorted(df['Herói'].unique())
            selected_heroes = st.multiselect("🛡️ Heróis", all_heroes, default=all_heroes)

        with col3:
            all_pillars = sorted(df['pillar'].unique())
            selected_pillars = st.multiselect("🏛️ Pilares", all_pillars, default=all_pillars)

        with col4:
            all_teams = sorted(df['Time'].unique())
            selected_teams = st.multiselect("👥 Times", all_teams, default=all_teams)

    # Aplicar filtros
    try:
        start_date, end_date = date_range
        filtered_df = df[
            (df['data_submissao'].dt.date >= start_date) &
            (df['data_submissao'].dt.date <= end_date) &
            (df['Herói'].isin(selected_heroes)) &
            (df['pillar'].isin(selected_pillars)) &
            (df['Time'].isin(selected_teams))
        ]
    except ValueError:
        st.error("Por favor, selecione um período válido.")
        st.stop()

    if filtered_df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        st.stop()

    # --- KPIS APRIMORADOS ---
    st.markdown("### 📊 **Métricas do Reino**")

    total_heroes = filtered_df['Herói'].nunique()
    total_gems = int(filtered_df['GemsAwarded'].sum())
    avg_gems = int(total_gems / total_heroes) if total_heroes > 0 else 0
    total_nominations = len(filtered_df)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric("🛡️ Heróis Reconhecidos", total_heroes)
    with kpi2:
        st.metric("💎 Cristais Distribuídos", f"{total_gems:,}".replace(",", "."))
    with kpi3:
        st.metric("💍 Média de Cristais/Herói", f"{avg_gems:,}".replace(",", "."))
    with kpi4:
        st.metric("📜 Nomeações Aprovadas", f"{total_nominations:,}".replace(",", "."))

    st.divider()

    # --- LAYOUT PRINCIPAL ---
    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        # Feed de Reconhecimento com imagens dos pilares
        st.markdown("### 📜 **Feed de Reconhecimento**")

        with st.container(height=400, border=True):
            feed_data = filtered_df.sort_values('data_submissao', ascending=False).head(10)

            for _, row in feed_data.iterrows():
                pillar_icon = display_pillar_icon(row['pillar'])
                st.markdown(f"""
                <div class="feed-item">
                    {pillar_icon}
                    <div>
                        <strong>{row['Herói']}</strong> foi reconhecido(a) por <strong>{row['Nomeador']}</strong><br>
                        <small style="color: var(--text-secondary);">🎯 {row['mission_name']}</small><br>
                        <small style="color: var(--text-secondary);">📅 {row['data_submissao'].strftime('%d/%m/%Y')}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Ranking dos Pilares com gráfico
        st.markdown("### 🏛️ **Pilares da Jornada**")

        pillar_data = filtered_df.groupby('pillar')['GemsAwarded'].sum().sort_values(ascending=False)

        if not pillar_data.empty:
            # Paleta de cores clean para o gráfico
            colors = ['#6B7E7D', '#A8A8A8', '#D4A574', '#B07A57', '#7FB069']

            fig_pillar = px.pie(
                values=pillar_data.values,
                names=pillar_data.index,
                title="Distribuição de GEMS por Pilar",
                color_discrete_sequence=colors
            )
            fig_pillar.update_layout(
                height=300, 
                showlegend=True,
                font=dict(family="Inter", size=12),
                title_font=dict(size=14)
            )
            st.plotly_chart(fig_pillar, use_container_width=True)

    with col_right:
        # Ranking dos Heróis
        st.markdown("### 🏆 **Ranking dos Heróis**")

        # Preparação dos dados para ranking
        hero_ranking = filtered_df.groupby(['Herói', 'Time'])['GemsAwarded'].sum().reset_index()
        hero_ranking = hero_ranking.sort_values('GemsAwarded', ascending=False).reset_index(drop=True)
        hero_ranking.index = hero_ranking.index + 1

        # Adicionar medalhas para o top 3
        def add_medals(position):
            if position == 1:
                return "🥇"
            elif position == 2:
                return "🥈"
            elif position == 3:
                return "🥉"
            else:
                return f"{position}º"

        hero_ranking['Posição'] = hero_ranking.index.map(add_medals)

        # Pivot para pilares
        pivot_pillars = filtered_df.pivot_table(
            index='Herói', 
            columns='pillar', 
            values='GemsAwarded', 
            aggfunc='sum'
        ).fillna(0).astype(int)

        final_ranking = hero_ranking.merge(pivot_pillars, on='Herói', how='left').fillna(0)

        # Configuração da tabela
        column_config = {
            "GemsAwarded": st.column_config.ProgressColumn(
                "💎 Cristais Totais",
                format="%d 💎",
                min_value=0,
                max_value=int(final_ranking['GemsAwarded'].max()) if len(final_ranking) > 0 else 100,
            ),
        }

        # Adicionar configuração para colunas de pilares
        for col in pivot_pillars.columns:
            column_config[col] = st.column_config.NumberColumn(
                f"🏛️ {col}",
                format="%d 💎"
            )

        st.dataframe(
            final_ranking,
            use_container_width=True,
            height=600,
            column_config=column_config,
            hide_index=True
        )

def pagina_mapa_dos_cristais():
    create_custom_header(
        "Mapa dos Cristais",
        "A jornada de um herói é pavimentada com grandes feitos",
        "🗺️"
    )

    df_map = load_data('map')
    if df_map.empty:
        st.warning("O Mapa dos Cristais ainda não foi definido.", icon="⚠️")
        return

    pilares = df_map['pillar'].dropna().unique()

    for pilar in pilares:
        col_img, col_title = st.columns([1, 5], vertical_alignment="center")

        with col_img:
            image_path = get_pillar_image(pilar)
            if image_path:
                st.image(image_path, width=80)
            else:
                st.markdown("### 📋")

        with col_title:
            st.markdown(f"## {pilar}")

        with st.container(border=True):
            df_pilar = df_map[df_map['pillar'] == pilar]
            if df_pilar.empty:
                st.info("Nenhuma missão definida para este pilar ainda.")
            else:
                for _, row in df_pilar.iterrows():
                    gems = int(pd.to_numeric(row['GemsAwarded'], errors='coerce'))

                    # Card da missão com imagem
                    pillar_icon = display_pillar_icon(pilar, "50px")
                    st.markdown(f"""
                    <div class="mission-card">
                        {pillar_icon}
                        <div style="flex: 1;">
                            <h4 style="margin: 0; color: var(--text-primary);">{row['mission_name']}</h4>
                            <p style="margin: 0.25rem 0; color: var(--text-secondary); font-size: 0.9rem;">{row['mission_discribe']}</p>
                            <div style="margin-top: 0.5rem;">
                                <span style="background: var(--accent-color); color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500;">
                                    💎 {gems} GEMS
                                </span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

def pagina_pergaminho_de_nomeacoes():
    create_custom_header(
        "Pergaminho de Nomeações", 
        "Reconheça um ato de bravura ou sabedoria de um colega herói",
        "📜"
    )

    df_herois = load_data('hero')
    df_map = load_data('map')

    if df_herois.empty or df_map.empty:
        st.error("É necessário ter ao menos um herói e uma missão cadastrados para fazer uma nomeação.", icon="🚨")
        return

    # Seção 1: Seleção de Heróis
    st.markdown("### 👥 **Passo 1: Selecione os Heróis**")
    col1, col2 = st.columns(2)

    with col1:
        nomeador = st.selectbox(
            "🛡️ Seu Nome de Herói (Nomeador)", 
            options=df_herois['hero_name'].tolist(),
            index=None,
            placeholder="Selecione seu nome",
            help="Escolha seu nome da lista de heróis cadastrados"
        )

    with col2:
        # Filtrar heróis para não incluir o nomeador
        available_heroes = df_herois[df_herois['hero_name'] != nomeador]['hero_name'].tolist() if nomeador else df_herois['hero_name'].tolist()
        nomeado = st.selectbox(
            "⭐ Herói a ser Nomeado", 
            options=available_heroes,
            index=None,
            placeholder="Selecione quem reconhecer",
            help="Escolha o herói que você deseja reconhecer"
        )

    # Seção 2: Especificação do Feito
    st.markdown("### 🎯 **Passo 2: Especifique o Feito**")

    pilar = st.selectbox(
        "🏛️ Pilar", 
        options=df_map['pillar'].dropna().unique(),
        index=None,
        placeholder="Selecione o pilar do feito",
        help="Escolha o pilar que melhor representa o feito realizado"
    )

    # Missões baseadas no pilar selecionado
    missao = None
    if pilar:
        missoes_do_pilar = df_map[df_map['pillar'] == pilar]

        if not missoes_do_pilar.empty:
            # Mostrar preview das missões disponíveis com ícones
            st.markdown("**💡 Missões disponíveis neste pilar:**")
            for _, mission_row in missoes_do_pilar.iterrows():
                gems = int(pd.to_numeric(mission_row['GemsAwarded'], errors='coerce'))
                pillar_icon = display_pillar_icon(pilar, "30px")
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.25rem 0; padding: 0.5rem; background: var(--background-light); border-radius: 8px;">
                    {pillar_icon}
                    <span><strong>{mission_row['mission_name']}</strong> - {gems} GEMS 💎</span>
                </div>
                """, unsafe_allow_html=True)

            # Selectbox para missão
            missao = st.selectbox(
                "Feito/Missão Realizada", 
                options=missoes_do_pilar['mission_name'].tolist(),
                index=None,
                placeholder="Selecione a missão específica",
                help="Escolha a missão que melhor descreve o feito realizado"
            )
    else:
        st.selectbox(
            "Feito/Missão Realizada", 
            options=[],
            index=None,
            placeholder="Primeiro selecione um pilar",
            disabled=True,
            help="Escolha a missão que melhor descreve o feito realizado"
        )

    # Mostrar recompensa da missão selecionada
    if missao and pilar:
        mission_data = df_map[(df_map['mission_name'] == missao) & (df_map['pillar'] == pilar)]
        if not mission_data.empty:
            gems_reward = int(pd.to_numeric(mission_data['GemsAwarded'].iloc[0], errors='coerce'))
            pillar_icon = display_pillar_icon(pilar, "40px")
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: var(--success-color); color: white; border-radius: var(--border-radius); margin: 1rem 0;">
                {pillar_icon}
                <div>
                    <strong>💎 Recompensa desta missão: {gems_reward} GEMS</strong><br>
                    <small>{mission_data['mission_discribe'].iloc[0]}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Seção 3: Justificativa
    st.markdown("### 📝 **Passo 3: Justifique sua nomeação**")
    justificativa = st.text_area(
        "Justificativa (obrigatório)", 
        placeholder="Descreva detalhadamente o feito realizado pelo herói...",
        help="Seja específico sobre o que o herói fez e por que merece o reconhecimento",
        height=120
    )

    anexo = st.file_uploader(
        "📎 Anexar Evidência (Opcional)", 
        help="Anexe um print, documento ou qualquer arquivo que comprove o feito",
        type=['png', 'jpg', 'jpeg', 'pdf', 'docx', 'txt']
    )

    # Validações em tempo real
    validation_msgs = []
    if nomeador and nomeado and nomeador == nomeado:
        validation_msgs.append("⚠️ Um herói não pode nomear a si mesmo!")

    if validation_msgs:
        for msg in validation_msgs:
            st.warning(msg)

    st.divider()

    # Verificar se todos os campos obrigatórios estão preenchidos
    campos_obrigatorios = [nomeador, nomeado, pilar, missao, justificativa.strip() if justificativa else ""]
    todos_preenchidos = all(campos_obrigatorios) and not validation_msgs

    if st.button(
        "Enviar Nomeação", 
        use_container_width=True, 
        type="primary",
        disabled=not todos_preenchidos
    ):
        if show_loading_message("Registrando a nomeação..."):
            df_nomeacoes = load_data('nomination')
            novo_id = (pd.to_numeric(df_nomeacoes['id_nomeacao'], errors='coerce').max() + 1) if not df_nomeacoes.empty else 1

            caminho_anexo_salvo = None
            if anexo:
                nome_arquivo = f"{novo_id}_{anexo.name}"
                caminho_anexo_salvo = ANEXOS_DIR / nome_arquivo
                with open(caminho_anexo_salvo, "wb") as f: 
                    f.write(anexo.getbuffer())
                logger.info(f"Anexo salvo: {caminho_anexo_salvo}")

            id_nomeador = df_herois.loc[df_herois['hero_name'] == nomeador, 'id_hero'].iloc[0]
            id_nomeado = df_herois.loc[df_herois['hero_name'] == nomeado, 'id_hero'].iloc[0]
            id_missao = df_map.loc[df_map['mission_name'] == missao, 'id_mission'].iloc[0]

            new_row = {
                'id_nomeacao': novo_id, 
                'data_submissao': date.today().strftime("%Y-%m-%d"),
                'id_nomeador': id_nomeador, 
                'id_nomeado': id_nomeado, 
                'id_missao': id_missao,
                'justificativa': justificativa, 
                'status': 'Pendente', 
                'caminho_anexo': str(caminho_anexo_salvo) if anexo else None
            }

            df_atualizado = pd.concat([df_nomeacoes, pd.DataFrame([new_row])], ignore_index=True)
            if save_data('nomination', df_atualizado):
                st.success(f"🎉 Nomeação de **'{nomeado}'** enviada com sucesso!")
                logger.info(f"Nova nomeação criada: ID {novo_id}, Nomeador: {nomeador}, Nomeado: {nomeado}")
                create_success_animation()
                time.sleep(2)
                st.rerun()

def pagina_aprovacao_da_nomeacao():
    create_custom_header(
        "Aprovação da Nomeação",
        "Área restrita aos Anciões do Conselho",
        "👑"
    )

    df_nomeacoes = load_data('nomination')
    df_herois = load_data('hero')
    df_missoes = load_data('map')

    if df_nomeacoes.empty:
        st.success("✨ Não há nenhuma nomeação no sistema ainda.")
        return

    # Enriquecer dados
    mapa_herois = df_herois.set_index('id_hero')['hero_name']
    mapa_missoes = df_missoes.set_index('id_mission')[['mission_name', 'pillar']]
    df_nomeacoes['nomeador'] = df_nomeacoes['id_nomeador'].map(mapa_herois).fillna("?")
    df_nomeacoes['nomeado'] = df_nomeacoes['id_nomeado'].map(mapa_herois).fillna("?")

    # Merge com informações da missão
    df_enriched = df_nomeacoes.merge(
        mapa_missoes, 
        left_on='id_missao', 
        right_index=True, 
        how='left'
    )
    df_enriched['mission_name'] = df_enriched['mission_name'].fillna("?")
    df_enriched['pillar'] = df_enriched['pillar'].fillna("?")

    # Métricas rápidas
    total_nomeacoes = len(df_enriched)
    pendentes = len(df_enriched[df_enriched['status'].str.strip().str.lower() == 'pendente'])
    aprovadas = len(df_enriched[df_enriched['status'].str.strip().str.lower() == 'aprovado'])
    reprovadas = len(df_enriched[df_enriched['status'].str.strip().str.lower() == 'reprovado'])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📝 Total", total_nomeacoes)
    col2.metric("⏳ Pendentes", pendentes)
    col3.metric("✅ Aprovadas", aprovadas)
    col4.metric("❌ Reprovadas", reprovadas)

    st.divider()

    tab_pend, tab_aprov, tab_reprov = st.tabs([
        f"⏳ Pendentes ({pendentes})", 
        f"✅ Aprovadas ({aprovadas})", 
        f"❌ Reprovadas ({reprovadas})"
    ])

    with tab_pend:
        pendentes_df = df_enriched[df_enriched['status'].str.strip().str.lower() == 'pendente']

        if pendentes_df.empty:
            st.success("✨ Não há nomeações pendentes para avaliação.")
        else:
            for _, row in pendentes_df.iterrows():
                with st.container(border=True):
                    col_info, col_actions = st.columns([3, 1])

                    with col_info:
                        pillar_icon = display_pillar_icon(row['pillar'], "30px")
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                            {pillar_icon}
                            <div>
                                <strong>De:</strong> {row['nomeador']} <strong>→ Para:</strong> {row['nomeado']}<br>
                                <small style="color: var(--text-secondary);">🎯 {row['mission_name']} | 📅 {row['data_submissao']}</small>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        with st.expander("📋 Ver Detalhes Completos"):
                            st.info(f"**Justificativa:**\n{row['justificativa']}")

                            if pd.notna(row['caminho_anexo']) and Path(row['caminho_anexo']).exists():
                                with open(row['caminho_anexo'], "rb") as file:
                                    st.download_button(
                                        f"📎 Baixar: {Path(row['caminho_anexo']).name}", 
                                        file, 
                                        Path(row['caminho_anexo']).name
                                    )

                    with col_actions:
                        id_nom = row['id_nomeacao']

                        if st.button("✅ Aprovar", key=f"aprovar_{id_nom}", use_container_width=True):
                            with st.spinner("Aprovando..."):
                                df_nomeacoes.loc[df_nomeacoes['id_nomeacao'] == id_nom, 'status'] = 'Aprovado'
                                if save_data('nomination', df_nomeacoes): 
                                    st.success("Nomeação aprovada!")
                                    logger.info(f"Nomeação {id_nom} aprovada")
                                    time.sleep(1)
                                    st.rerun()

                        if st.button("❌ Reprovar", key=f"reprovar_{id_nom}", use_container_width=True, type="secondary"):
                            with st.spinner("Reprovando..."):
                                df_nomeacoes.loc[df_nomeacoes['id_nomeacao'] == id_nom, 'status'] = 'Reprovado'
                                if save_data('nomination', df_nomeacoes): 
                                    st.success("Nomeação reprovada!")
                                    logger.info(f"Nomeação {id_nom} reprovada")
                                    time.sleep(1)
                                    st.rerun()

    with tab_aprov:
        aprovadas_df = df_enriched[df_enriched['status'].str.strip().str.lower() == 'aprovado']
        if not aprovadas_df.empty:
            st.dataframe(
                aprovadas_df[['data_submissao', 'nomeador', 'nomeado', 'mission_name', 'pillar']].rename(columns={
                    'data_submissao': '📅 Data',
                    'nomeador': '🛡️ Nomeador', 
                    'nomeado': '⭐ Nomeado',
                    'mission_name': '🎯 Missão',
                    'pillar': '🏛️ Pilar'
                }),
                use_container_width=True,
                hide_index=True
            )

    with tab_reprov:
        reprovadas_df = df_enriched[df_enriched['status'].str.strip().str.lower() == 'reprovado']
        if not reprovadas_df.empty:
            st.dataframe(
                reprovadas_df[['data_submissao', 'nomeador', 'nomeado', 'mission_name', 'pillar']].rename(columns={
                    'data_submissao': '📅 Data',
                    'nomeador': '🛡️ Nomeador', 
                    'nomeado': '⭐ Nomeado',
                    'mission_name': '🎯 Missão',
                    'pillar': '🏛️ Pilar'
                }),
                use_container_width=True,
                hide_index=True
            )

# --- 8. PÁGINAS ADMINISTRATIVAS ---
def pagina_admin_herois():
    create_custom_header(
        "Gestão de Heróis",
        "Administração de heróis do programa",
        "🔑"
    )

    df_herois = load_data('hero')

    if 'hero_to_edit_id' in st.session_state:
        hero_id = st.session_state['hero_to_edit_id']
        hero_data = df_herois[df_herois['id_hero'] == hero_id].iloc[0]

        st.markdown(f"### ✏️ **Editando Herói: _{hero_data['hero_name']}_**")

        with st.form("edit_hero_form"):
            col1, col2 = st.columns(2)

            with col1:
                hero_name = st.text_input("🛡️ Nome do Herói", value=hero_data['hero_name'])
            with col2:
                hero_team = st.text_input("👥 Time do Herói", value=hero_data['hero_team'])

            col_save, col_cancel = st.columns(2)

            with col_save:
                submitted = st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)
            with col_cancel:
                cancel = st.form_submit_button("❌ Cancelar", type="secondary", use_container_width=True)

            if cancel:
                del st.session_state['hero_to_edit_id']
                st.rerun()

            if submitted:
                if not hero_name.strip() or not hero_team.strip():
                    st.error("Nome e Time são obrigatórios!")
                else:
                    if show_loading_message("Atualizando herói..."):
                        df_herois.loc[df_herois['id_hero'] == hero_id, ['hero_name', 'hero_team', 'update_date']] = [
                            hero_name.strip(), hero_team.strip(), date.today().strftime("%Y-%m-%d")
                        ]
                        if save_data('hero', df_herois):
                            st.success("🎉 Herói atualizado com sucesso!")
                            logger.info(f"Herói {hero_id} atualizado: {hero_name}")
                            del st.session_state['hero_to_edit_id']
                            time.sleep(1)
                            st.rerun()
    else:
        # Cadastro de novo herói
        with st.expander("➕ **Cadastrar Novo Herói**", expanded=df_herois.empty):
            with st.form("add_hero_form", clear_on_submit=True):
                col1, col2 = st.columns(2)

                with col1:
                    hero_name = st.text_input("🛡️ Nome do Novo Herói", placeholder="Ex: João Silva")
                with col2:
                    hero_team = st.text_input("👥 Time do Herói", placeholder="Ex: Desenvolvimento")

                if st.form_submit_button("🎯 Cadastrar Herói", type="primary", use_container_width=True):
                    if not hero_name.strip() or not hero_team.strip():
                        st.error("📝 Nome e Time são obrigatórios.")
                    elif hero_name.strip().lower() in df_herois['hero_name'].str.strip().str.lower().values:
                        st.error(f"⚠️ O nome '{hero_name}' já existe.")
                    else:
                        if show_loading_message("Cadastrando herói..."):
                            new_id = (pd.to_numeric(df_herois['id_hero'], errors='coerce').max() + 1) if not df_herois.empty else 101
                            today = date.today().strftime("%Y-%m-%d")
                            new_row = {
                                'id_hero': str(new_id), 
                                'hero_name': hero_name.strip(), 
                                'hero_team': hero_team.strip(), 
                                'start_date': today, 
                                'update_date': today
                            }
                            df_updated = pd.concat([df_herois, pd.DataFrame([new_row])], ignore_index=True)
                            if save_data('hero', df_updated):
                                st.success(f"🎉 Herói '{hero_name}' cadastrado com sucesso!")
                                logger.info(f"Novo herói cadastrado: {hero_name} (ID: {new_id})")
                                create_success_animation()
                                time.sleep(1)
                                st.rerun()

        st.divider()

        # Lista de heróis existentes
        st.markdown("### 🛡️ **Heróis Existentes**")

        if df_herois.empty:
            st.info("👤 Nenhum herói cadastrado ainda.")
        else:
            # Estatísticas rápidas
            col1, col2, col3 = st.columns(3)
            col1.metric("👥 Total de Heróis", len(df_herois))
            col2.metric("🏢 Times Únicos", df_herois['hero_team'].nunique())
            col3.metric("📅 Cadastros Hoje", len(df_herois[df_herois['start_date'] == date.today().strftime("%Y-%m-%d")]))

            st.markdown("---")

            # Filtro por time
            all_teams = ['Todos'] + sorted(df_herois['hero_team'].unique().tolist())
            selected_team = st.selectbox("🏢 Filtrar por Time", all_teams)

            filtered_heroes = df_herois if selected_team == 'Todos' else df_herois[df_herois['hero_team'] == selected_team]

            for index, row in filtered_heroes.iterrows():
                with st.container(border=True):
                    col_info, col_actions = st.columns([3, 1])

                    with col_info:
                        st.markdown(f"### 🛡️ **{row['hero_name']}**")
                        st.markdown(f"**👥 Time:** {row['hero_team']}")
                        st.caption(f"🆔 ID: {row['id_hero']} | 📅 Criado: {row.get('start_date', 'N/A')}")

                    with col_actions:
                        if st.button("✏️ Editar", key=f"edit_hero_{row['id_hero']}", use_container_width=True):
                            st.session_state['hero_to_edit_id'] = row['id_hero']
                            st.rerun()

                        if st.button("🗑️ Excluir", key=f"del_hero_{row['id_hero']}", type="secondary", use_container_width=True):
                            if show_loading_message("Excluindo herói..."):
                                df_herois.drop(index, inplace=True)
                                if save_data('hero', df_herois):
                                    st.success("🗑️ Herói excluído!")
                                    logger.info(f"Herói excluído: {row['hero_name']} (ID: {row['id_hero']})")
                                    time.sleep(1)
                                    st.rerun()

def pagina_admin_missoes():
    create_custom_header(
        "Administração de Missões",
        "Gerencie as missões e recompensas do programa",
        "🔑"
    )

    df_map = load_data('map')

    if 'mission_to_edit_id' in st.session_state:
        mission_id = st.session_state['mission_to_edit_id']
        mission_data = df_map[df_map['id_mission'] == mission_id].iloc[0]

        st.markdown(f"### ✏️ **Editando Missão: _{mission_data['mission_name']}_**")

        with st.form("edit_mission_form"):
            mission_name = st.text_input("Missão", value=mission_data['mission_name'])
            mission_discribe = st.text_area("📝 Descrição", value=mission_data['mission_discribe'], height=100)

            col1, col2 = st.columns(2)
            with col1:
                gems = st.number_input("💎 Recompensa em GEMS", min_value=1, step=1, value=int(pd.to_numeric(mission_data['GemsAwarded'])))
            with col2:
                pillar = st.text_input("🏛️ Pilar Associado", value=mission_data['pillar'])

            col_save, col_cancel = st.columns(2)

            with col_save:
                submitted = st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)
            with col_cancel:
                cancel = st.form_submit_button("❌ Cancelar", type="secondary", use_container_width=True)

            if cancel:
                del st.session_state['mission_to_edit_id']
                st.rerun()

            if submitted:
                if not all([mission_name.strip(), mission_discribe.strip(), pillar.strip(), gems > 0]):
                    st.error("📝 Todos os campos são obrigatórios.")
                else:
                    if show_loading_message("Atualizando missão..."):
                        today = date.today().strftime("%Y-%m-%d")
                        update_values = [mission_name.strip(), mission_discribe.strip(), gems, pillar.strip(), today]
                        update_cols = ['mission_name', 'mission_discribe', 'GemsAwarded', 'pillar', 'update_date']
                        df_map.loc[df_map['id_mission'] == mission_id, update_cols] = update_values
                        if save_data('map', df_map):
                            st.success("🎉 Missão atualizada com sucesso!")
                            logger.info(f"Missão {mission_id} atualizada: {mission_name}")
                            del st.session_state['mission_to_edit_id']
                            time.sleep(1)
                            st.rerun()
    else:
        # Cadastro de nova missão
        with st.expander("➕ **Cadastrar Nova Missão**", expanded=df_map.empty):
            with st.form("add_mission_form", clear_on_submit=True):
                mission_name = st.text_input("Nome da Nova Missão", placeholder="Ex: Implementação de Melhoria")
                mission_discribe = st.text_area("📝 Descrição", placeholder="Descreva a missão em detalhes...", height=100)

                col1, col2 = st.columns(2)
                with col1:
                    gems = st.number_input("💎 Recompensa em GEMS", min_value=1, step=1, value=10)
                with col2:
                    # Lista de pilares existentes para sugestão
                    existing_pillars = df_map['pillar'].dropna().unique().tolist() if not df_map.empty else []
                    if existing_pillars:
                        pillar = st.selectbox("🏛️ Pilar Associado", ['Novo Pilar...'] + existing_pillars, index=0)
                        if pillar == 'Novo Pilar...':
                            pillar = st.text_input("🆕 Nome do Novo Pilar", placeholder="Ex: Inovação")
                    else:
                        pillar = st.text_input("🏛️ Pilar Associado", placeholder="Ex: Inovação")

                if st.form_submit_button("🎯 Cadastrar Missão", type="primary", use_container_width=True):
                    if not all([mission_name.strip(), mission_discribe.strip(), pillar.strip(), gems > 0]):
                        st.error("📝 Todos os campos são obrigatórios.")
                    else:
                        if show_loading_message("Cadastrando missão..."):
                            today = date.today().strftime("%Y-%m-%d")
                            new_id_mission = (pd.to_numeric(df_map['id_mission'], errors='coerce').max() + 1) if not df_map.empty else 1
                            id_pillar = hash(pillar.strip().lower()) % 1000
                            new_data = {
                                'id_mission': new_id_mission, 
                                'mission_name': mission_name.strip(), 
                                'mission_discribe': mission_discribe.strip(),
                                'GemsAwarded': gems, 
                                'id_pillar': id_pillar, 
                                'pillar': pillar.strip(), 
                                'start_date': today, 
                                'update_date': today
                            }
                            df_updated = pd.concat([df_map, pd.DataFrame([new_data])], ignore_index=True)
                            if save_data('map', df_updated):
                                st.success(f"🎉 Missão '{mission_name}' cadastrada com sucesso!")
                                logger.info(f"Nova missão cadastrada: {mission_name} (ID: {new_id_mission})")
                                create_success_animation()
                                time.sleep(1)
                                st.rerun()

        st.divider()

        # Lista de missões existentes
        st.markdown("### **Missões Existentes**")

        if df_map.empty:
            st.info("📝 Nenhuma missão cadastrada ainda.")
        else:
            # Estatísticas rápidas
            total_missions = len(df_map)
            total_gems = df_map['GemsAwarded'].astype(int).sum()
            avg_gems = int(total_gems / total_missions) if total_missions > 0 else 0
            unique_pillars = df_map['pillar'].nunique()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total de Missões", total_missions)
            col2.metric("💎 Total de GEMS", f"{total_gems:,}".replace(",", "."))
            col3.metric("📊 Média de GEMS", avg_gems)
            col4.metric("🏛️ Pilares", unique_pillars)

            st.markdown("---")

            # Filtro por pilar
            all_pillars = ['Todos'] + sorted(df_map['pillar'].unique().tolist())
            selected_pillar = st.selectbox("🏛️ Filtrar por Pilar", all_pillars)

            filtered_missions = df_map if selected_pillar == 'Todos' else df_map[df_map['pillar'] == selected_pillar]

            # Organizar por pilar
            for pilar in filtered_missions['pillar'].unique():
                st.markdown(f"#### **{pilar}**")
                pilar_missions = filtered_missions[filtered_missions['pillar'] == pilar]

                for index, row in pilar_missions.iterrows():
                    with st.container(border=True):
                        col_info, col_actions = st.columns([3, 1])

                        with col_info:
                            gems = int(pd.to_numeric(row['GemsAwarded']))
                            pillar_icon = display_pillar_icon(pilar, "40px")

                            st.markdown(f"""
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                {pillar_icon}
                                <div>
                                    <h4 style="margin: 0;">{row['mission_name']}</h4>
                                    <p style="margin: 0.25rem 0; color: var(--text-secondary);">💎 {gems} GEMS</p>
                                    <small style="color: var(--text-secondary);">🆔 ID: {row['id_mission']}</small>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            with st.expander("📝 Ver Descrição"):
                                st.write(row['mission_discribe'])

                        with col_actions:
                            if st.button("✏️ Editar", key=f"edit_mission_{row['id_mission']}", use_container_width=True):
                                st.session_state['mission_to_edit_id'] = row['id_mission']
                                st.rerun()

                            if st.button("🗑️ Excluir", key=f"del_mission_{row['id_mission']}", type="secondary", use_container_width=True):
                                if show_loading_message("Excluindo missão..."):
                                    df_map.drop(index, inplace=True)
                                    if save_data('map', df_map):
                                        st.success("🗑️ Missão excluída!")
                                        logger.info(f"Missão excluída: {row['mission_name']} (ID: {row['id_mission']})")
                                        time.sleep(1)
                                        st.rerun()

                st.markdown("---")

# --- 9. LÓGICA DE NAVEGAÇÃO E AUTENTICAÇÃO ---
if __name__ == "__main__":
    st.sidebar.markdown("### 💎 **Navegação**")
    st.sidebar.divider()

    # Estado de administrador
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False

    # Campo de senha estilizado
    password = st.sidebar.text_input("🔑 Senha de Administrador", type="password")
    if password == ADMIN_PASSWORD:
        st.session_state.is_admin = True
        st.sidebar.success("🔓 Acesso liberado!")
    elif password:
        st.sidebar.error("❌ Senha incorreta.")

    st.sidebar.divider()

    # Páginas disponíveis
    PAGES = {
        "Home": ("🏠", pagina_home, False),
        "Salão dos Heróis": ("⚔️", pagina_salao_dos_herois, False),
        "Mapa dos Cristais": ("🗺️", pagina_mapa_dos_cristais, False),
        "Pergaminho de Nomeações": ("📜", pagina_pergaminho_de_nomeacoes, False),
        "Aprovação da Nomeação": ("👑", pagina_aprovacao_da_nomeacao, True),
        "Gestão de Heróis": ("🔑", pagina_admin_herois, True),
        "Administração de Missões": ("🔑", pagina_admin_missoes, True),
    }

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    # Navegação melhorada
    for name, (icon, _, needs_admin) in PAGES.items():
        if not needs_admin or st.session_state.is_admin:
            # Destacar página atual
            button_type = "primary" if st.session_state.current_page == name else "secondary"

            if st.sidebar.button(f"{icon} {name}", use_container_width=True, type=button_type):
                st.session_state.current_page = name
                st.rerun()

    # Executar página selecionada
    page_function = PAGES[st.session_state.current_page][1]
    page_function()

    # Footer
    st.sidebar.markdown("---")
    app_title = os.getenv("APP_TITLE", "Programa +GEMS")
    st.sidebar.markdown(f"*{app_title} v2.0*")
    
    if DEBUG:
        st.sidebar.markdown("🔧 **Debug Mode**")
        st.sidebar.text(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
