import streamlit as st
import pandas as pd
from pathlib import Path
import time
from utils.ui_components import create_custom_header, display_pillar_icon, show_loading_message
from utils.data_manager import load_data, save_data
from utils.config import logger

def show_page():
    """Exibe a página de aprovação de nomeações"""
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
    df_enriched = enrich_nomination_data(df_nomeacoes, df_herois, df_missoes)
    
    # Métricas rápidas
    show_quick_metrics(df_enriched)
    
    st.divider()
    
    # Tabs por status
    create_status_tabs(df_enriched, df_nomeacoes)

def enrich_nomination_data(df_nomeacoes, df_herois, df_missoes):
    """Enriquece dados das nomeações com nomes de heróis e missões"""
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
    
    return df_enriched

def show_quick_metrics(df_enriched):
    """Exibe métricas rápidas"""
    total_nomeacoes = len(df_enriched)
    pendentes = len(df_enriched[df_enriched['status'].str.strip().str.lower() == 'pendente'])
    aprovadas = len(df_enriched[df_enriched['status'].str.strip().str.lower() == 'aprovado'])
    reprovadas = len(df_enriched[df_enriched['status'].str.strip().str.lower() == 'reprovado'])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📝 Total", total_nomeacoes)
    col2.metric("⏳ Pendentes", pendentes)
    col3.metric("✅ Aprovadas", aprovadas)
    col4.metric("❌ Reprovadas", reprovadas)

def create_status_tabs(df_enriched, df_nomeacoes):
    """Cria tabs organizadas por status"""
    pendentes = len(df_enriched[df_enriched['status'].str.strip().str.lower() == 'pendente'])
    aprovadas = len(df_enriched[df_enriched['status'].str.strip().str.lower() == 'aprovado'])
    reprovadas = len(df_enriched[df_enriched['status'].str.strip().str.lower() == 'reprovado'])
    
    tab_pend, tab_aprov, tab_reprov = st.tabs([
        f"⏳ Pendentes ({pendentes})", 
        f"✅ Aprovadas ({aprovadas})", 
        f"❌ Reprovadas ({reprovadas})"
    ])
    
    with tab_pend:
        show_pending_nominations(df_enriched, df_nomeacoes)
    
    with tab_aprov:
        show_approved_nominations(df_enriched)
    
    with tab_reprov:
        show_rejected_nominations(df_enriched)

def show_pending_nominations(df_enriched, df_nomeacoes):
    """Mostra nomeações pendentes com ações"""
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
                        handle_approval(id_nom, df_nomeacoes, 'Aprovado')
                    
                    if st.button("❌ Reprovar", key=f"reprovar_{id_nom}", use_container_width=True, type="secondary"):
                        handle_approval(id_nom, df_nomeacoes, 'Reprovado')

def show_approved_nominations(df_enriched):
    """Mostra nomeações aprovadas"""
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

def show_rejected_nominations(df_enriched):
    """Mostra nomeações reprovadas"""
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

def handle_approval(id_nom, df_nomeacoes, new_status):
    """Gerencia aprovação/reprovação de nomeações"""
    with st.spinner(f"{'Aprovando' if new_status == 'Aprovado' else 'Reprovando'}..."):
        df_nomeacoes.loc[df_nomeacoes['id_nomeacao'] == id_nom, 'status'] = new_status
        if save_data('nomination', df_nomeacoes): 
            st.success(f"Nomeação {'aprovada' if new_status == 'Aprovado' else 'reprovada'}!")
            logger.info(f"Nomeação {id_nom} {new_status.lower()}")
            time.sleep(1)
            st.rerun()
