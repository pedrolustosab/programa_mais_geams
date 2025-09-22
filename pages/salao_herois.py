import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from io import BytesIO
from utils.ui_components import create_custom_header, display_pillar_icon
from utils.data_manager import get_dashboard_data

def show_page():
    """Exibe a página do Salão dos Heróis"""
    create_custom_header(
        "Salão dos Heróis",
        "Acompanhe as lendas do reino, suas conquistas e os pilares mais valorizados.",
        "⚔️"
    )

    df = get_dashboard_data()

    if df.empty:
        st.warning("Ainda não há dados suficientes para exibir o dashboard. As nomeações precisam ser aprovadas primeiro.", icon="⚠️")
        return

    # Filtros aprimorados
    create_filters_section(df)

    # Aplicar filtros
    filtered_df = apply_filters(df)

    if filtered_df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    # Aplicar filtros interativos dos gráficos
    filtered_df = apply_graph_filters(filtered_df)

    # KPIs aprimorados
    show_metrics(filtered_df)

    st.divider()

    # Layout principal
    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        show_recognition_feed(filtered_df)
        show_pillar_distribution(filtered_df)

    with col_right:
        show_hero_ranking(filtered_df)

    # Seção de jornada das nomeações
    st.divider()
    show_nomination_journey(filtered_df)

def create_filters_section(df):
    """Cria a seção de filtros"""
    with st.expander("🔍 **Filtros do Reino**", expanded=True):
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                min_date = df['data_submissao'].min().date()
                max_date = df['data_submissao'].max().date()
                date_range = st.date_input(
                    "📅 Período",
                    (min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="date_filter"
                )
                st.session_state.date_range = date_range

            with col2:
                all_heroes = sorted(df['Herói'].unique())
                selected_heroes = st.multiselect(
                    "🛡️ Heróis", 
                    all_heroes, 
                    default=all_heroes,
                    key="heroes_filter"
                )
                st.session_state.selected_heroes = selected_heroes

            with col3:
                all_pillars = sorted(df['pillar'].unique())
                selected_pillars = st.multiselect(
                    "🏛️ Pilares", 
                    all_pillars, 
                    default=all_pillars,
                    key="pillars_filter"
                )
                st.session_state.selected_pillars = selected_pillars

            with col4:
                all_teams = sorted(df['Time'].unique())
                selected_teams = st.multiselect(
                    "👥 Times", 
                    all_teams, 
                    default=all_teams,
                    key="teams_filter"
                )
                st.session_state.selected_teams = selected_teams

def apply_filters(df):
    """Aplica os filtros selecionados"""
    try:
        date_range = st.session_state.get('date_range', (df['data_submissao'].min().date(), df['data_submissao'].max().date()))
        selected_heroes = st.session_state.get('selected_heroes', df['Herói'].unique().tolist())
        selected_pillars = st.session_state.get('selected_pillars', df['pillar'].unique().tolist())
        selected_teams = st.session_state.get('selected_teams', df['Time'].unique().tolist())

        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = df[
                (df['data_submissao'].dt.date >= start_date) &
                (df['data_submissao'].dt.date <= end_date) &
                (df['Herói'].isin(selected_heroes)) &
                (df['pillar'].isin(selected_pillars)) &
                (df['Time'].isin(selected_teams))
            ]
            return filtered_df
        else:
            return df
    except Exception as e:
        st.error("Erro ao aplicar filtros. Usando dados completos.")
        return df

def apply_graph_filters(filtered_df):
    """Aplica filtros baseados em interações nos gráficos"""
    # Filtro do gráfico de pilares
    if "pillar_chart_selection" in st.session_state and st.session_state.pillar_chart_selection.get("points"):
        selected_points = st.session_state.pillar_chart_selection["points"]
        if selected_points:
            selected_pillar = selected_points[0]["label"]
            filtered_df = filtered_df[filtered_df['pillar'] == selected_pillar]

    # Filtro do gráfico diário
    if "daily_chart_selection" in st.session_state and st.session_state.daily_chart_selection.get("points"):
        selected_points = st.session_state.daily_chart_selection["points"]
        if selected_points:
            selected_date = pd.to_datetime(selected_points[0]["x"]).date()
            filtered_df = filtered_df[filtered_df['data_submissao'].dt.date == selected_date]

    return filtered_df

def show_metrics(filtered_df):
    """Exibe métricas do reino"""
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

def show_recognition_feed(filtered_df):
    """Exibe feed de reconhecimento com imagens dos pilares"""
    st.markdown("### 📜 **Feed de Reconhecimento**")
    with st.container(height=400, border=True):
        feed_data = filtered_df.sort_values('data_submissao', ascending=False)

        for _, row in feed_data.iterrows():
            pillar_icon = display_pillar_icon(row['pillar'])
            st.markdown(f"""
            <div class="feed-item" style="padding: 10px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; gap: 10px;">
                {pillar_icon}
                <div>
                    <strong>{row['Herói']}</strong> foi reconhecido(a) por <strong>{row['Nomeador']}</strong><br>
                    <small style="color: var(--text-secondary);">🎯 {row['mission_name']}</small><br>
                    <small style="color: var(--text-secondary);">📅 {row['data_submissao'].strftime('%d/%m/%Y')}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_pillar_distribution(filtered_df):
    """Exibe distribuição dos pilares"""
    st.markdown("### 🏛️ **Pilares da Jornada**")
    pillar_data = filtered_df.groupby('pillar')['GemsAwarded'].sum().sort_values(ascending=False).reset_index()

    if not pillar_data.empty:
        colors = px.colors.qualitative.Pastel  # Usando uma paleta mais suave para melhor UX

        fig_pillar = px.pie(
            pillar_data,
            values='GemsAwarded',
            names='pillar',
            title="Distribuição de GEMS por Pilar",
            color_discrete_sequence=colors,
            hole=0.4  # Donut maior para melhor visual
        )
        fig_pillar.update_layout(
            height=350, 
            showlegend=True,
            font=dict(family="Inter", size=12),
            title_font=dict(size=14),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(size=10)),
            margin=dict(l=20, r=20, t=50, b=50)  # Ajuste de margens para evitar quebra
        )
        fig_pillar.update_traces(textposition='inside', textinfo='percent')
        st.plotly_chart(fig_pillar, use_container_width=True, key="pillar_chart", on_select="rerun")
    else:
        st.info("Nenhum dado disponível para distribuição de pilares.")

def show_hero_ranking(filtered_df):
    """Exibe ranking dos heróis"""
    st.markdown("### 🏆 **Ranking dos Heróis**")
    # Preparação dos dados para ranking
    total_gems = filtered_df['GemsAwarded'].sum()
    hero_ranking = filtered_df.groupby(['Herói', 'Time'])['GemsAwarded'].sum().reset_index()
    hero_ranking = hero_ranking[hero_ranking['GemsAwarded'] > 0]  # Mostrar apenas linhas com valores
    hero_ranking = hero_ranking.sort_values('GemsAwarded', ascending=False).reset_index(drop=True)
    hero_ranking.index = hero_ranking.index + 1

    # Adicionar porcentagem
    hero_ranking['Porcentagem'] = (hero_ranking['GemsAwarded'] / total_gems * 100).round(2)

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

    # Configuração da tabela aprimorada
    column_config = {
        "Posição": st.column_config.TextColumn("Posição", width="small"),
        "Herói": st.column_config.TextColumn("Herói", width="medium"),
        "Time": st.column_config.TextColumn("Time", width="medium"),
        "GemsAwarded": st.column_config.ProgressColumn(
            "💎 Cristais Totais",
            format="%d 💎",
            min_value=0,
            max_value=int(final_ranking['GemsAwarded'].max()) if len(final_ranking) > 0 else 100,
            width="medium"
        ),
        "Porcentagem": st.column_config.NumberColumn(
            "% do Total",
            format="%.2f%%",
            width="small"
        ),
    }

    # Adicionar configuração para colunas de pilares apenas se houver valores
    pillar_columns = [col for col in pivot_pillars.columns if final_ranking[col].sum() > 0]
    for col in pillar_columns:
        column_config[col] = st.column_config.NumberColumn(
            f"🏛️ {col}",
            format="%d 💎",
            width="small"
        )

    st.dataframe(
        final_ranking[["Posição", "Herói", "Time", "GemsAwarded", "Porcentagem"] + pillar_columns],
        use_container_width=True,
        height=600,
        column_config=column_config,
        hide_index=True
    )

    # Botão de exportação para Excel
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        final_ranking.to_excel(writer, sheet_name='Ranking', index=False)
    st.download_button(
        label="📥 Exportar para Excel",
        data=buffer.getvalue(),
        file_name=f"ranking_herois_{date.today().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

def show_nomination_journey(filtered_df):
    """Exibe a jornada das nomeações com cristais por dia"""
    st.markdown("### 📈 **Jornada das Nomeações**")
    filtered_df['date'] = filtered_df['data_submissao'].dt.date
    daily_gems = filtered_df.groupby('date')['GemsAwarded'].sum().reset_index()
    daily_gems['date'] = pd.to_datetime(daily_gems['date'])  # Garantir que seja datetime para eixo X

    fig_daily = px.line(
        daily_gems, 
        x='date', 
        y='GemsAwarded', 
        title="Cristais Distribuídos por Dia",
        markers=True
    )
    fig_daily.update_layout(
        height=400,
        font=dict(family="Inter", size=12),
        title_font=dict(size=14),
        xaxis_title="Data",
        yaxis_title="Cristais",
        xaxis=dict(
            tickformat="%d/%m/%Y",  # Formato de data no eixo X
            dtick="D1"  # Mostrar ticks diários
        )
    )
    fig_daily.update_traces(line=dict(width=3), marker=dict(size=8))  # Melhorar visualização
    st.plotly_chart(fig_daily, use_container_width=True, key="daily_chart", on_select="rerun")