import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path
import time
from utils.ui_components import create_custom_header, display_pillar_icon, show_loading_message, create_success_animation
from utils.data_manager import load_data, save_data
from utils.config import ANEXOS_DIR, logger

def show_page():
    """Exibe a página de nomeações"""
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
    nomeador, nomeado = select_heroes(df_herois)
    
    # Seção 2: Especificação do Feito
    pilar, missao = select_mission(df_map)
    
    # Seção 3: Justificativa
    justificativa, anexo = get_justification()
    
    # Validações e envio
    handle_submission(nomeador, nomeado, pilar, missao, justificativa, anexo, df_herois, df_map)

def select_heroes(df_herois):
    """Seção de seleção de heróis"""
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
        available_heroes = df_herois[df_herois['hero_name'] != nomeador]['hero_name'].tolist() if nomeador else df_herois['hero_name'].tolist()
        nomeado = st.selectbox(
            "⭐ Herói a ser Nomeado", 
            options=available_heroes,
            index=None,
            placeholder="Selecione quem reconhecer",
            help="Escolha o herói que você deseja reconhecer"
        )
    
    return nomeador, nomeado

def select_mission(df_map):
    """Seção de especificação do feito"""
    st.markdown("### 🎯 **Passo 2: Especifique o Feito**")
    
    pilar = st.selectbox(
        "🏛️ Pilar", 
        options=df_map['pillar'].dropna().unique(),
        index=None,
        placeholder="Selecione o pilar do feito",
        help="Escolha o pilar que melhor representa o feito realizado"
    )
    
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
            
            missao = st.selectbox(
                "🎯 Feito/Missão Realizada", 
                options=missoes_do_pilar['mission_name'].tolist(),
                index=None,
                placeholder="Selecione a missão específica",
                help="Escolha a missão que melhor descreve o feito realizado"
            )
    else:
        st.selectbox(
            "🎯 Feito/Missão Realizada",
            options=[],
            index=None,
            placeholder="Primeiro selecione um pilar",
            disabled=True,
            help="Escolha a missão que melhor descreve o feito realizado"
        )
    
    # Mostrar recompensa da missão selecionada
    if missao and pilar:
        show_mission_reward(df_map, missao, pilar)
    
    return pilar, missao

def show_mission_reward(df_map, missao, pilar):
    """Mostra a recompensa da missão selecionada"""
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

def get_justification():
    """Seção de justificativa"""
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
    
    return justificativa, anexo

def handle_submission(nomeador, nomeado, pilar, missao, justificativa, anexo, df_herois, df_map):
    """Gerencia validações e envio da nomeação"""
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
        "🚀 Enviar Nomeação", 
        use_container_width=True, 
        type="primary",
        disabled=not todos_preenchidos
    ):
        submit_nomination(nomeador, nomeado, pilar, missao, justificativa, anexo, df_herois, df_map)

def submit_nomination(nomeador, nomeado, pilar, missao, justificativa, anexo, df_herois, df_map):
    """Processa o envio da nomeação"""
    if show_loading_message("Registrando a nomeação..."):
        df_nomeacoes = load_data('nomination')
        novo_id = (pd.to_numeric(df_nomeacoes['id_nomeacao'], errors='coerce').max() + 1) if not df_nomeacoes.empty else 1
        
        # Salvar anexo se existir
        caminho_anexo_salvo = None
        if anexo:
            nome_arquivo = f"{novo_id}_{anexo.name}"
            caminho_anexo_salvo = ANEXOS_DIR / nome_arquivo
            with open(caminho_anexo_salvo, "wb") as f: 
                f.write(anexo.getbuffer())
            logger.info(f"Anexo salvo: {caminho_anexo_salvo}")
        
        # Buscar IDs
        id_nomeador = df_herois.loc[df_herois['hero_name'] == nomeador, 'id_hero'].iloc[0]
        id_nomeado = df_herois.loc[df_herois['hero_name'] == nomeado, 'id_hero'].iloc[0]
        id_missao = df_map.loc[df_map['mission_name'] == missao, 'id_mission'].iloc[0]
        
        # Criar nova linha
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
