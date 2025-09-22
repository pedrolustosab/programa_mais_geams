import streamlit as st
import pandas as pd
from utils.ui_components import create_custom_header, get_pillar_image_path
from utils.data_manager import load_data
from utils.config import logger

def show_page():
    """Exibe a página do Mapa dos Cristais com UX/UI melhorado"""
    create_custom_header(
        "Mapa dos Cristais",
        "A jornada de um herói é pavimentada com grandes feitos",
        "🗺️"
    )
    
    df_map = load_data('map')
    if df_map.empty:
        show_empty_state()
        return
    
    # Estatísticas gerais do reino
    show_kingdom_stats(df_map)
    
    st.divider()
    
    # Pilares e missões
    show_pillars_and_missions(df_map)

def show_empty_state():
    """Mostra estado vazio quando não há dados"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; background: var(--background-light); border-radius: 15px; margin: 2rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🗺️</div>
        <h3 style="color: var(--text-secondary); margin-bottom: 0.5rem;">O Mapa dos Cristais ainda não foi definido</h3>
        <p style="color: var(--text-secondary); margin-bottom: 2rem;">
            Aguarde enquanto os sábios do reino criam as primeiras missões...
        </p>
        <div style="background: var(--warning-color); color: white; padding: 0.75rem 1.5rem; border-radius: 25px; display: inline-block;">
            ⚠️ Nenhuma missão cadastrada
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_kingdom_stats(df_map):
    """Mostra estatísticas gerais do reino"""
    st.markdown("### 🏰 **Panorama do Reino**")
    
    # Calcular estatísticas
    total_pillars = df_map['pillar'].nunique()
    total_missions = len(df_map)
    total_gems = df_map['GemsAwarded'].astype(str).str.extract('(\d+)', expand=False).astype(float).sum()
    avg_gems = total_gems / total_missions if total_missions > 0 else 0
    
    # Cards de estatísticas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        show_stat_card("🏛️", "Pilares Ativos", total_pillars, "#4A90E2")
    
    with col2:
        show_stat_card("🎯", "Missões Disponíveis", total_missions, "#50C878")
    
    with col3:
        show_stat_card("💎", "GEMS Totais", f"{int(total_gems):,}".replace(",", "."), "#FFD700")
    
    with col4:
        show_stat_card("📊", "Média por Missão", f"{avg_gems:.1f}", "#FF6B6B")

def show_stat_card(icon, title, value, color):
    """Cria um card de estatística"""
    st.markdown(f"""
    <div style="
        background: white;
        border: 2px solid {color};
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="font-size: 1.8rem; font-weight: bold; color: {color}; margin-bottom: 0.25rem;">{value}</div>
        <div style="color: var(--text-secondary); font-size: 0.9rem;">{title}</div>
    </div>
    """, unsafe_allow_html=True)

def show_pillars_and_missions(df_map):
    """Mostra pilares e suas missões com seletor"""
    pilares = df_map['pillar'].dropna().unique()
    
    st.markdown("### 🗺️ **Explorando os Territórios**")
    
    # Seletor de pilar
    selected_pillar = st.selectbox(
        "**Escolha um Pilar para Explorar**",
        pilares,
        format_func=lambda x: f"{x}"
    )
    
    if selected_pillar:
        show_pillar_section(df_map, selected_pillar)

def show_pillar_section(df_map, pilar):
    """Mostra seção de um pilar específico"""
    df_pilar = df_map[df_map['pillar'] == pilar]
    total_gems_pilar = df_pilar['GemsAwarded'].astype(str).str.extract('(\d+)', expand=False).astype(float).sum()
    total_missoes = len(df_pilar)
    
    # Header do pilar
    col_icon, col_header, col_stats = st.columns([1, 4, 2])
    
    with col_icon:
        image_path = get_pillar_image_path(pilar)
        if image_path:
            st.image(image_path, width=100)
        else:
            st.markdown('<div style="font-size: 3rem; text-align: center;">🏛️</div>', unsafe_allow_html=True)
    
    with col_header:
        st.markdown(f"""
        <div style="padding: 1rem 0;">
            <h2 style="margin: 0; color: var(--primary-color); font-size: 2rem;">{pilar}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stats:
        st.markdown(f"""
        <div style="text-align: right; padding: 1rem;">
            <div style="background: var(--accent-color); color: white; padding: 0.5rem 1rem; border-radius: 20px; margin-bottom: 0.5rem;">
                🎯 {total_missoes} Missões
            </div>
            <div style="background: var(--success-color); color: white; padding: 0.5rem 1rem; border-radius: 20px;">
                💎 {int(total_gems_pilar)} GEMS
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Container das missões
    with st.container():
        
        if df_pilar.empty:
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <h4 style="color: var(--text-secondary);">Nenhuma missão definida para este pilar ainda</h4>
                <p style="color: var(--text-secondary);">Em breve, novos desafios surgirão neste território...</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            show_missions_list(df_pilar)
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_missions_list(df_pilar):
    """Mostra lista de missões de forma simples"""
    # Ordenar por GEMS
    df_pilar_sorted = df_pilar.copy()
    df_pilar_sorted['GemsNum'] = df_pilar_sorted['GemsAwarded'].astype(str).str.extract('(\d+)', expand=False).astype(float)
    df_pilar_sorted = df_pilar_sorted.sort_values('GemsNum', ascending=False)
    
    # Mostrar todas as missões
    for _, row in df_pilar_sorted.iterrows():
        show_mission_card(row)

def show_mission_card(row):
    """Mostra card individual da missão simplificado"""
    try:
        gems = int(pd.to_numeric(str(row['GemsAwarded']).replace('GEMS', '').strip(), errors='coerce'))
    except:
        gems = 0
    
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid #e0e0e0;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: var(--text-primary); font-size: 1.3rem; flex: 1;">
                {row['mission_name']}
            </h4>
            <span style="
                background: linear-gradient(135deg, #FFD700, #FFA500); 
                color: white; 
                padding: 0.4rem 1rem; 
                border-radius: 20px; 
                font-size: 0.85rem; 
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 0.25rem;
                flex-shrink: 0;
                margin-left: 1rem;
            ">
                💎 {gems} GEMS
            </span>
        </div>
        <p style="
            margin: 0; 
            color: var(--text-secondary); 
            font-size: 1rem; 
            line-height: 1.5;
            padding: 1rem;
            background: rgba(0,0,0,0.02);
            border-radius: 8px;
        ">
            {row['mission_discribe']}
        </p>
    </div>
    """, unsafe_allow_html=True)
