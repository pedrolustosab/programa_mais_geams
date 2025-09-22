import streamlit as st
import pandas as pd
from datetime import date
import time
from utils.ui_components import create_custom_header, display_pillar_icon, show_loading_message, create_success_animation
from utils.data_manager import load_data, save_data
from utils.config import logger

def show_page():
    """Exibe a página de administração de missões"""
    create_custom_header(
        "Administração de Missões",
        "Gerencie as missões e recompensas do programa",
        "🔑"
    )
    
    df_map = load_data('map')
    
    # Verifica se há missão sendo editada
    if 'mission_to_edit_id' in st.session_state:
        show_edit_mission_form(df_map)
    else:
        show_add_mission_form(df_map)
        show_missions_list(df_map)

def show_edit_mission_form(df_map):
    """Formulário de edição de missão"""
    mission_id = st.session_state['mission_to_edit_id']
    mission_data = df_map[df_map['id_mission'] == mission_id].iloc[0]
    
    st.markdown(f"### ✏️ **Editando Missão: _{mission_data['mission_name']}_**")
    
    with st.form("edit_mission_form"):
        mission_name = st.text_input("🎯 Nome da Missão", value=mission_data['mission_name'])
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
            handle_mission_update(mission_id, mission_name, mission_discribe, gems, pillar, df_map)

def show_add_mission_form(df_map):
    """Formulário de adição de nova missão"""
    with st.expander("➕ **Cadastrar Nova Missão**", expanded=df_map.empty):
        with st.form("add_mission_form", clear_on_submit=True):
            mission_name = st.text_input("🎯 Nome da Nova Missão", placeholder="Ex: Implementação de Melhoria")
            mission_discribe = st.text_area("📝 Descrição", placeholder="Descreva a missão em detalhes...", height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                gems = st.number_input("💎 Recompensa em GEMS", min_value=1, step=1, value=10)
            with col2:
                # Lista de pilares existentes para sugestão
                existing_pillars = df_map['pillar'].dropna().unique().tolist() if not df_map.empty else []
                if existing_pillars:
                    pillar_option = st.selectbox("🏛️ Pilar Associado", ['Novo Pilar...'] + existing_pillars, index=0)
                    if pillar_option == 'Novo Pilar...':
                        pillar = st.text_input("🆕 Nome do Novo Pilar", placeholder="Ex: Inovação")
                    else:
                        pillar = pillar_option
                else:
                    pillar = st.text_input("🏛️ Pilar Associado", placeholder="Ex: Inovação")
            
            if st.form_submit_button("🎯 Cadastrar Missão", type="primary", use_container_width=True):
                handle_mission_creation(mission_name, mission_discribe, gems, pillar, df_map)

def show_missions_list(df_map):
    """Lista de missões existentes"""
    st.divider()
    st.markdown("### 🎯 **Missões Existentes**")
    
    if df_map.empty:
        st.info("📝 Nenhuma missão cadastrada ainda.")
    else:
        # Estatísticas rápidas
        show_mission_statistics(df_map)
        
        # Filtro por pilar
        show_filtered_missions(df_map)

def show_mission_statistics(df_map):
    """Mostra estatísticas das missões"""
    total_missions = len(df_map)
    total_gems = df_map['GemsAwarded'].astype(int).sum()
    avg_gems = int(total_gems / total_missions) if total_missions > 0 else 0
    unique_pillars = df_map['pillar'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Total de Missões", total_missions)
    col2.metric("💎 Total de GEMS", f"{total_gems:,}".replace(",", "."))
    col3.metric("📊 Média de GEMS", avg_gems)
    col4.metric("🏛️ Pilares", unique_pillars)

def show_filtered_missions(df_map):
    """Mostra missões com filtro por pilar"""
    st.markdown("---")
    
    # Filtro por pilar
    all_pillars = ['Todos'] + sorted(df_map['pillar'].unique().tolist())
    selected_pillar = st.selectbox("🏛️ Filtrar por Pilar", all_pillars)
    
    filtered_missions = df_map if selected_pillar == 'Todos' else df_map[df_map['pillar'] == selected_pillar]
    
    # Organizar por pilar
    for pilar in filtered_missions['pillar'].unique():
        st.markdown(f"#### 🏛️ **{pilar}**")
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
                        handle_mission_deletion(index, row, df_map)
        
        st.markdown("---")

def handle_mission_update(mission_id, mission_name, mission_discribe, gems, pillar, df_map):
    """Gerencia atualização de missão"""
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

def handle_mission_creation(mission_name, mission_discribe, gems, pillar, df_map):
    """Gerencia criação de nova missão"""
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

def handle_mission_deletion(index, row, df_map):
    """Gerencia exclusão de missão"""
    if show_loading_message("Excluindo missão..."):
        df_map.drop(index, inplace=True)
        if save_data('map', df_map):
            st.success("🗑️ Missão excluída!")
            logger.info(f"Missão excluída: {row['mission_name']} (ID: {row['id_mission']})")
            time.sleep(1)
            st.rerun()
