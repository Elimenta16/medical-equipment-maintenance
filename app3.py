import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Gestión de Mantenimiento Biomédico", layout="wide")

st.title("🛠️ Panel de Control de Mantenimiento Preventivo Biomédico")
st.caption("Optimización y Seguimiento de Ciclos de Calibración y Servicio Técnico Hospitalario")
st.markdown("---")

st.markdown("""
### Gestión de Activos y Seguridad del Paciente
Esta plataforma automatiza el calendario de mantenimiento preventivo para asegurar que los equipos médicos críticos operen bajo los estándares de calidad correspondientes, mitigando riesgos de fallas en áreas críticas.
""")

st.subheader("📊 Carga del Inventario de Equipos Médicos")
archivo_cargado = st.file_uploader("Sube el archivo de inventario (.xlsx o .csv):", type=["xlsx", "csv"])

if archivo_cargado is not None:
    try:
        # Leer archivo
        if archivo_cargado.name.endswith('.xlsx'):
            df = pd.read_excel(archivo_cargado)
        else:
            df = pd.read_csv(archivo_cargado)
            
        st.success(f"✅ Inventario cargado con éxito. {len(df)} equipos registrados.")
        
        # Columnas obligatorias
        columnas_requeridas = ['ID_Equipo', 'Equipo', 'Marca_Modelo', 'Area_Hospital', 'Ultimo_Mantenimiento']
        if all(col in df.columns for col in columnas_requeridas):
            
            # Convertir a formato fecha
            df['Ultimo_Mantenimiento'] = pd.to_datetime(df['Ultimo_Mantenimiento'])
            
            # Calcular Próximo Mantenimiento (Ciclo estándar de 6 meses / 180 días)
            df['Proximo_Mantenimiento'] = df['Ultimo_Mantenimiento'] + timedelta(days=180)
            
            # Calcular días restantes en base a la fecha actual
            hoy = datetime.now()
            
            def calcular_estatus(row):
                proximo = row['Proximo_Mantenimiento']
                dias_restantes = (proximo - hoy).days
                
                if dias_restantes < 0:
                    return "🔴 Vencido", dias_restantes
                elif dias_restantes <= 15:
                    return "🟡 Próximo (Riesgo Moderado)", dias_restantes
                else:
                    return "🟢 Al Corriente", dias_restantes
            
            # Aplicar la lógica
            resultados = df.apply(calcular_estatus, axis=1)
            df['Estatus'] = [res[0] for res in resultados]
            df['Días_Restantes'] = [res[1] for res in resultados]
            
            # Formatear fechas para mostrar al usuario de manera limpia
            df['Ultimo_Mantenimiento'] = df['Ultimo_Mantenimiento'].dt.strftime('%Y-%m-%d')
            df['Proximo_Mantenimiento'] = df['Proximo_Mantenimiento'].dt.strftime('%Y-%m-%d')
            
            # 📊 KPIs Principales
            st.markdown("---")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            with kpi1:
                st.metric("Total de Equipos", len(df))
            with kpi2:
                st.metric("🟢 Operativos Al Día", len(df[df['Estatus'] == "🟢 Al Corriente"]))
            with kpi3:
                st.metric("🟡 Mantenimientos Críticos (<15 días)", len(df[df['Estatus'] == "🟡 Próximo (Riesgo Moderado)"]))
            with kpi4:
                st.metric("🔴 Equipos Vencidos (Fuera de Norma)", len(df[df['Estatus'] == "🔴 Vencido"]))
            
            # Gráficas Analíticas
            st.markdown("---")
            col_izq, col_der = st.columns(2)
            
            with col_izq:
                st.subheader("Distribución Operativa del Parque Tecnológico")
                fig = px.pie(df, names='Estatus', color='Estatus',
                             color_discrete_map={
                                 "🟢 Al Corriente": "#2ca02c",
                                 "🟡 Próximo (Riesgo Moderado)": "#ff7f0e",
                                 "🔴 Vencido": "#d62728"
                             })
                st.plotly_chart(fig, use_container_width=True)
                
            with col_der:
                st.subheader("Carga de Trabajo de Mantenimiento por Área")
                fig_bar = px.histogram(df, x="Area_Hospital", color="Estatus", barmode="group",
                                       color_discrete_map={
                                           "🟢 Al Corriente": "#2ca02c",
                                           "🟡 Próximo (Riesgo Moderado)": "#ff7f0e",
                                           "🔴 Vencido": "#d62728"
                                       })
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Tabla Completa de Datos
            st.markdown("---")
            st.subheader("📋 Registro Detallado y Control de Días")
            st.dataframe(df[['ID_Equipo', 'Equipo', 'Marca_Modelo', 'Area_Hospital', 'Proximo_Mantenimiento', 'Estatus', 'Días_Restantes']], use_container_width=True)
            
        else:
            st.error(f"❌ El formato del archivo es incorrecto. Debe incluir las columnas: {columnas_requeridas}")
            
    except Exception as e:
        st.error(f"Error al procesar el archivo de inventario: {e}")
else:
    st.info("💡 Sube el archivo Excel de inventario técnico para desplegar el calendario y las métricas de riesgo operativo.")
