import streamlit as st
import pandas as pd
import pyodbc
from streamlit_option_menu import option_menu
import folium
from folium.plugins import MarkerCluster
import base64
from PIL import Image
from io import BytesIO
import os
import datetime
from folium import IFrame
from streamlit_folium import st_folium
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
import plotly.graph_objects as go
from mtranslate import translate
import locale
from plotly.subplots import make_subplots
from bs4 import BeautifulSoup, Tag

st.set_page_config(page_title="DDT", page_icon="🌍", layout="wide")
locale.setlocale(locale.LC_ALL, '')
current_date = datetime.datetime.now()
year = current_date.year 
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp * {{
             font-weight: bold;
             color: #004378;
             .st-bo  {{
             background-color: #e1f4fa;
             border-radius: 0.5rem;
             }}
             .st-dn {{
              background-color: rgb(255 255 255);
              border-radius: 0.5rem ;
             }}
             .st-dq  {{
              border-bottom-color: rgb(202 204 245);
             }}  
             .st-emotion-cache-1wivap2 {{
              font-size: 28px;
             }}
              }}        
         </style>
         """,
         unsafe_allow_html=True
     )
add_bg_from_url()
#translate
df = pd.read_excel(os.path.join(r'C:\Users\Dell\Desktop\test\data1\language.xlsx', 'language.xlsx'),sheet_name='wiki')
df.dropna(inplace=True)
lang = df['name'].to_list()
langlist=tuple(lang)
langcode = df['iso'].to_list()
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}
def translate_html(html_code, choice):
    if choice.lower() == "french":
        return html_code
    soup = BeautifulSoup(html_code, 'html.parser')
    for element in soup.find_all(text=True):
        if element.parent.name not in ['script', 'style']:
            if element.parent.name == 'span':
                # Ajouter un espace avant et après le texte traduit
                translated_text = ' ' + translate(element, lang_array[choice]) + ' '
            else:
                translated_text = translate(element, lang_array[choice])
            element.replace_with(translated_text)
    translated_html_code = str(soup)
    return translated_html_code

lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}
st.sidebar.image(r"C:\Users\Dell\Desktop\test\Logo Masen VF.png",caption="", use_column_width=True) 
choice = st.sidebar.radio('Select language', langlist)
excel_file = r'C:\Users\Dell\Desktop\test\Projets_DDT.xlsx'
df = pd.read_excel(excel_file)
odd_colors = {
       'ODD 4 : Education de qualité': '#c5192d',
       'ODD 5 : Egalité entre les sexes': 'rgb(255, 58, 33)',
       'ODD 3 : Bonne santé et bien être': 'rgb(76, 159, 56)',
       'ODD 6 : Eau propre et assainissement': '#08d1ce',
       'ODD 1 : Pas de pauvreté': 'rgba(235, 28, 45, 0.99)',
       'ODD 8 : Travail décent et croissance économique': 'rgb(162, 25, 66)',
       'ODD 2 : Zéro Faim' :'rgb(209, 159, 42)',
       'ODD 7 : Energie propre et d\'un cout adorable': '#fcc312',
       'ODD 9 : Industrie, innovation et infrastructure': 'rgb(253, 105, 37)',
       'ODD 10 : Inégalités réduites': 'rgb(221, 19, 103)',
       'ODD 11 : villes et communautés durables': 'rgb(253, 157, 36)',
       'ODD 12 : Consommation et production durables': 'rgb(191, 139, 46)',
       'ODD 13 : Mesures relatives à la lutte contre les changements climatiques': 'rgb(72, 119, 60)',
       'ODD 14 : Vie aquatique': 'rgb(0, 125, 187)',
       'ODD 15 : Vie terrestre': 'rgb(64, 174, 73)',
       'ODD 16 : Paix, justice et institutions efficaces': 'rgb(0, 85, 138)',
       'ODD 17 : Partenariats pour la réalisation des objectifs': 'rgb(26, 54, 104)',
       'SDG 4: Quality education': 'rgb(197, 25, 45)',
       'SDG 5: Gender equality': 'rgb(255, 58, 33)',
       'SDG 3: Good health and well-being': 'rgb(76, 159, 56)',
       'SDG 6: Clean Water and sanitation': '#08d1ce',
       'SDG 1: No poverty': 'rgba(235, 28, 45, 0.99)',
       'SDG 8: Decent work and economic growth': 'rgb(162, 25, 66)',
       'SDG 2: Zero Hunger': 'rgb(209, 159, 42)',
       'SDG 7: Clean and affordable energy': '#fcc312',
       'SDG 9: Industry, Innovation, and Infrastructure': 'rgb(253, 105, 37)',
       'SDG 10: Reduced inequalities': 'rgb(221, 19, 103)',
       'SDG 11: sustainable cities and communities': 'rgb(253, 157, 36)',
       'SDG 12: Sustainable consumption and production': 'rgb(191, 139, 46)',
       'SDG 13: Measures to combat climate change': 'rgb(72, 119, 60)',
       'SDG 14: Aquatic life': 'rgb(0, 125, 187)',
       'ODD 15: Overland routes': 'rgb(64, 174, 73)',
       'SDG 16: Peace, justice and effective institutions': 'rgb(0, 85, 138)',
       'SDG 17: Partnerships to achieve the goals': 'rgb(26, 54, 104)',
     } 
Axes_colors ={
       'Développement et animation des territoires': '#004378',
       'Amélioration du cadre social des populations': '#faba19',
       'Désenclavement des territoires': '#edf7fc',
       'Development and animation of territories': '#004378',
       'Improvement of the social framework of the populations': '#faba19',
       'Opening up of territories': '#edf7fc',
}
secter_colors ={
       'Education': '#fcc365',
       'Animation socioculturelle et sportive': '#e09609',
       'Infrastructures et équipements de base': '#cfe9fc',
       'Santé': 'orange',
       'AGR': '#063d70',
       'Sensibilisation et renforcement des capacités': '#2e6fab',
       'Responsabilité Environnementale': '#709cc4',
       'Sociocultural and sports activities': '#e09609',
       'Basic infrastructure and equipment': '#cfe9fc',
       'Health': 'orange',
       'AGR': '#063d70',
       'Awareness raising and capacity building': '#2e6fab',
       'Environmental Responsibility': '#709cc4',
}
def Bilan_DDTM():
     st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://welcome.compass-group.ch/wp-content/uploads/Sustainability_Planet_Hands_AdobeStock_332444622-1920x660.94545454545-c-default.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
     title = f"""<h2 style='text-align: center; background-color:#b7d3e8; padding: 10px; border-radius: 10px; font-size: 30px; font-family: Arial, sans-serif; font-weight: bold;'>
Bilan global des projets de développement durable des territoires <br><span style='color: orange;'>2010-{year}</span>
</h2>"""
     st.markdown(translate_html(title,choice), unsafe_allow_html=True)
#Axe stratégique 
     st.markdown("")
     st.markdown("")    
     st.markdown(translate_html(f"<p style='font-size: 18px; font-family: Calibri; color: black; font-weight: normal; text-align: justify;'>L'objectif stratégique de Masen est de désenclaver les territoires, d'améliorer le cadre social des populations et de favoriser le développement et l'animation des territoires. L'objectif de Masen est de promouvoir l'accès aux ressources et aux services indispensables, de renforcer les liens communautaires et de dynamiser les économies locales en mettant l'accent sur ces priorités.</p>",choice), unsafe_allow_html=True)
     #df['Axe stratégique'] = df['Axe stratégique'].apply(lambda x: translate_html(x, choice))
     #axes_strategiques_traduits = [translate_html(axe, choice) for axe in df['Axe stratégique']]
     axes_projet_counts = df.groupby('Axe stratégique').size().reset_index(name='Nombre de projets/actions')
     axes_projet_counts['Axe stratégique'] = axes_projet_counts['Axe stratégique'].apply(lambda x: translate_html(x, choice))
     fig_axes = px.pie(
    axes_projet_counts,
    values='Nombre de projets/actions',
    names='Axe stratégique',
    title=translate_html("<b style='color: #004378'>Volume de réalisation par axes stratégiques</b>", choice),
    color='Axe stratégique',
    color_discrete_map=Axes_colors,
    template="plotly_white",
)
     fig_axes.update_layout(
    title_x=0.3,
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    legend_font=dict(color='#004378')
)
     fig_axes.update_traces(text=[translate_html(axe, choice) for axe in axes_projet_counts['Axe stratégique']],textposition='inside', textinfo='percent')
     for data in fig_axes.data:
      data.name = translate_html(data.name, choice)
      data.hovertemplate = data.hovertemplate.replace("Axe stratégique=", translate_html("Axe stratégique=", choice)).replace("Nombre de projets/actions=", translate_html("Nombre de projets/actions=", choice))
     fig_axes.update_traces(textposition='inside', hole=0.8 )
     axes_benef_counts = df.groupby('Axe stratégique')['Nombre de bénéficiaires'].sum().reset_index(name='Nombre de bénéficiaires')
     axes_benef_counts['Axe stratégique'] =axes_benef_counts['Axe stratégique'].apply(lambda x: translate_html(x, choice))
     fig_axe_benef_pie = px.pie(
    axes_benef_counts,
    values='Nombre de bénéficiaires',
    names='Axe stratégique', 
    title=translate_html("<b style='color: #004378'>Nombre de bénéficiaires par axe stratégique</b>", choice),
    color='Axe stratégique',
    color_discrete_map=Axes_colors,
    template="plotly_white"
)
     fig_axe_benef_pie.update_layout(
    title_x=0.3,
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    legend_font=dict(color='#004378')
)
     for data in fig_axe_benef_pie.data:
       data.name = translate_html(data.name, choice)
       data.hovertemplate = data.hovertemplate.replace("Axe stratégique=", translate_html("Axe stratégique=", choice)).replace("Nombre de bénéficiaires=", translate_html("Nombre de bénéficiaires=", choice))
     fig_axe_benef_pie.update_traces(text=[translate_html(axe, choice) for axe in axes_benef_counts['Axe stratégique']],textposition='inside', textinfo='percent', hole=0.8)
     axes_invs_counts = df.groupby('Axe stratégique')['Budget global (DH)'].sum().reset_index(name='Budget global')
     axes_invs_counts['Axe stratégique'] =axes_invs_counts['Axe stratégique'].apply(lambda x: translate_html(x, choice))
     fig_axes_invs_pie = px.pie(
    axes_invs_counts,
    values='Budget global',
    names='Axe stratégique',
    color='Axe stratégique',
    color_discrete_map=Axes_colors,
    title=translate_html("<b style='color: #004378'>Budget global par axe stratégique</b>", choice),
)
     fig_axes_invs_pie.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="black"),
    paper_bgcolor='rgba(0, 0, 0, 0)',
    title_x=0.3,
    legend_font=dict(color='#004378'),
)
     for data in fig_axes_invs_pie.data:
       data.name = translate_html(data.name, choice)
       data.hovertemplate = data.hovertemplate.replace("Axe stratégique=", translate_html("Axe stratégique=", choice)).replace("Budget global=", translate_html("Global budget=", choice)) 
     fig_axes_invs_pie.update_traces(text=[translate_html(axe, choice) for axe in axes_invs_counts['Axe stratégique']],textposition='inside', textinfo='percent', hole=0.8)
     fig1 = make_subplots(
    rows=1, 
    cols=3, 
    specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]], 
    subplot_titles=(translate_html("<b style='color: #004378'>Nombre de projets/actions</b>",choice),translate_html("<b style='color: #004378'>Nombre de bénéficiaires</b>",choice), translate_html("<b style='color: #004378'>Budget global (DH)</b>",choice),)
)
     fig1.add_trace(fig_axes['data'][0], row=1, col=1)
     fig1.add_trace(fig_axe_benef_pie['data'][0], row=1, col=2)
     fig1.add_trace(fig_axes_invs_pie['data'][0], row=1, col=3)
     fig1.update_layout(
    legend_title_text=translate_html('Axe stratégique',choice),
    title_text=translate_html("<b style='color: #004378'>Indicateurs par axes stratégiques</b>",choice),
    title_x=0.22,
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color="black"),
    legend_font=dict(color='#004378'),
    legend=dict(
        x=1.05, 
        y=0.8   
    )
)
     st.plotly_chart(fig1, use_container_width=True)
     paragraphe = """
     <p style='font-size: 18px; font-family: Calibri; color: black; font-weight: normal; text-align: justify;'>
     Masen est engagée dans un large éventail de secteurs d'intervention visant à promouvoir le développement durable des communautés. À travers ses initiatives, Masen œuvre notamment dans les domaines cruciaux de la santé, de l'éducation, de l'animation socioculturelle et sportive, ainsi que dans le renforcement des infrastructures et équipements de base. De plus, elle soutient activement les activités génératrices de revenus, même dans le secteur agricole. Cette diversification reflète l'engagement de Masen à répondre aux besoins variés de ces riverains et à contribuer de manière significative à leur bien-être et à leur prospérité à long terme.
     </p>
     """ 
     st.markdown(translate_html(paragraphe,choice), unsafe_allow_html=True) 
    # df['Secteur d\'intervention'] = df['Secteur d\'intervention'].apply(lambda x: translate_html(x, choice))
     secteur_projet_counts = df.groupby('Secteur d\'intervention').size().reset_index(name='Nombre de projets/actions')
     secteur_projet_counts['Secteur d\'intervention'] =secteur_projet_counts['Secteur d\'intervention'].apply(lambda x: translate_html(x, choice))
     #sect_traduits = secteur_projet_counts ['Secteur d\'intervention']
     fig_secteur = px.pie(
    secteur_projet_counts ,
    values='Nombre de projets/actions',
    names='Secteur d\'intervention',
    title=translate_html("<b style='color: #004378'>Volume de réalisation</b>", choice),
    color='Secteur d\'intervention',
    color_discrete_map=secter_colors
)
     fig_secteur.update_layout(
    title_x=0.25,
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    legend_font=dict(color='#004378'),
)
     fig_secteur.update_traces(text=[translate_html(axe, choice) for axe in secteur_projet_counts['Secteur d\'intervention']],textposition='inside', textinfo='percent', hole=0.8)
     for data in fig_secteur.data:
       data.name = translate_html(data.name, choice)
       data.hovertemplate = data.hovertemplate.replace("Secteur d'intervention=", translate_html("Secteur d'intervention=", choice)).replace("Nombre de projets/actions=", translate_html("Nombre de projets/actions=", choice))  
     secteurs_benef_counts = df.groupby('Secteur d\'intervention')['Nombre de bénéficiaires'].sum().reset_index(name='Nombre de bénéficiaires')
     secteurs_benef_counts['Secteur d\'intervention'] =secteurs_benef_counts['Secteur d\'intervention'].apply(lambda x: translate_html(x, choice))
     fig_secteur_benef_pie = px.pie(
    secteurs_benef_counts,
    values='Nombre de bénéficiaires',
    names='Secteur d\'intervention',
    title=translate_html("<b style='color: #004378'>Nombre de bénéficiaires</b>", choice),
    color='Secteur d\'intervention',
    color_discrete_map=secter_colors,
    template="plotly_white",
)
     fig_secteur_benef_pie.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="black"),
    paper_bgcolor='rgba(0, 0, 0, 0)',
    title_x=0.3,
    legend_font=dict(color='#004378')
)
     fig_secteur_benef_pie.update_traces(text=[translate_html(axe, choice) for axe in secteurs_benef_counts['Secteur d\'intervention']],textposition='inside', textinfo='percent', hole=0.8)
     for data in fig_secteur_benef_pie.data:
       data.name = translate_html(data.name, choice)
       data.hovertemplate = data.hovertemplate.replace("Secteur d'intervention=", translate_html("Secteur d'intervention=", choice)).replace("Nombre de bénéficiaires=", translate_html("Nombre de bénéficiaires=", choice))
     secteurs_invs_counts = df.groupby('Secteur d\'intervention')['Budget global (DH)'].sum().reset_index(name='Budget global')
     secteurs_invs_counts['Secteur d\'intervention'] =secteurs_invs_counts['Secteur d\'intervention'].apply(lambda x: translate_html(x, choice))
     fig_secteur_invs_pie = px.pie(
    secteurs_invs_counts,
    values=secteurs_invs_counts ['Budget global'],
    names='Secteur d\'intervention',
    title=translate_html("<b style='color: #004378; font-size : 9px'>Budget global</b>", choice),
    color='Secteur d\'intervention',
    color_discrete_map=secter_colors,
    template="plotly_white",
)
     fig_secteur_invs_pie.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="black"),
    paper_bgcolor='rgba(0, 0, 0, 0)',
    title_x=0.3,
    legend_font=dict(color='#004378')
)
     fig_secteur_invs_pie.update_traces(text=[translate_html(axe, choice) for axe in secteurs_invs_counts['Secteur d\'intervention']],textposition='inside', textinfo='percent', hole=0.8)
     for data in fig_secteur_invs_pie.data:
       data.name = translate_html(data.name, choice)
       data.hovertemplate = data.hovertemplate.replace("Secteur d'intervention=", translate_html("Secteur d'intervention=", choice)).replace("Budget global=", translate_html("Global budget=", choice)) 
     fig = make_subplots(
    rows=1, 
    cols=3, 
    specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]], 
    subplot_titles=(translate_html("<b style='color: #004378'>Nombre de projets/actions</b>",choice), translate_html("<b style='color: #004378'>Nombre de bénéficiaires</b>",choice), translate_html("<b style='color: #004378'>budget global (DH)</b>",choice))
)
     fig.add_trace(fig_secteur['data'][0], row=1, col=1)
     fig.add_trace(fig_secteur_benef_pie['data'][0], row=1, col=2)
     fig.add_trace(fig_secteur_invs_pie['data'][0], row=1, col=3)
     fig.update_layout(
    legend_title_text=translate_html('Secteur d\'intervention',choice),
    title_text=translate_html("<b style='color: #004378'>Indicateurs par secteur d'intervention</b>",choice),
    title_x=0.25,
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color="black"),
    legend_font=dict(color='#004378'),
      legend=dict(
        x=1.05, 
        y=0.8  
    ))
     st.plotly_chart(fig, use_container_width=True)
#ODD     
     odd_counts = df['Les ODD'].str.split(';').explode().value_counts()
     pie_chart_data = pd.DataFrame({'ODD': odd_counts.index, 'Nombre de projets': odd_counts.values})
     odd_traduits = [translate_html(sect, choice) for sect in pie_chart_data['ODD']]
     pie_chart_data['ODD'] = odd_traduits
     pie_chart_data = pie_chart_data.sort_values(by='ODD')    
     fig_odd_counts_pie = px.pie(
    pie_chart_data,
    values='Nombre de projets',
    names='ODD',
    color='ODD',
    template="plotly_white", 
    color_discrete_map=odd_colors,  
    hole=.8
)
     fig_odd_counts_pie.update_traces(
    textposition='inside', rotation=0, insidetextorientation='auto', textfont_size=15,
    marker=dict(line=dict(color='#FFFFFF')),  hovertemplate='<b>ODD</b>: %{label}<br><b>Nombre de projets</b>: %{value}<extra></extra>',
    customdata=pie_chart_data['ODD']
)
     for data in fig_odd_counts_pie.data:
    # Traduire le nom de la trace
      data.name = translate_html(data.name, choice)
    # Modifier le modèle de survol pour traduire les libellés
      data.hovertemplate = data.hovertemplate.replace("ODD:", translate_html("SDG:", choice)).replace("Nombre de projets:", translate_html("Nombre de projets/actions:", choice))
     st.header("")
     st.markdown(translate_html(
    f"<p style='font-size: 18px; font-family: Calibri; color: black; font-weight: normal; text-align: justify;'>" 
    f"Dans le cadre du DDT, Masen s'investit activement dans la mise en œuvre des Objectifs de Développement Durable (ODD) à travers ses projets et initiatives. En alignant ses actions avec les ODD établis par l'ONU.", choice),
    unsafe_allow_html=True)
     df_expanded = df.assign(ODD=df['Les ODD'].str.split(';')).explode('ODD')
     df_expanded['Nombre de bénéficiaires'] = pd.to_numeric(df_expanded['Nombre de bénéficiaires'], errors='coerce')
     df_expanded = df_expanded.dropna(subset=['Nombre de bénéficiaires'])
     beneficiaires_somme = df_expanded.groupby('ODD')['Nombre de bénéficiaires'].sum()
     pie_chart_data_benef = pd.DataFrame({'ODD': beneficiaires_somme.index, 'Somme des bénéficiaires': beneficiaires_somme.values})
     odd_traduits = [translate_html(sect, choice) for sect in pie_chart_data_benef['ODD']]
     pie_chart_data_benef['ODD'] = odd_traduits
     fig_benef_counts_pie = px.pie(
    pie_chart_data_benef,
    values='Somme des bénéficiaires',
    names='ODD',
    color='ODD',
    template="plotly_white",
    hover_data='ODD',
    color_discrete_map=odd_colors,
    hole=.8
)
     fig_benef_counts_pie.update_traces(
    textposition='inside', rotation=0, insidetextorientation='auto', textfont_size=15,
    marker=dict(line=dict(color='#FFFFFF')), hovertemplate='<b>ODD</b>: %{label}<br><b>Somme des bénéficiaires</b>: %{value}<extra></extra>',
    customdata=pie_chart_data_benef['ODD'] 
)
     for data in fig_benef_counts_pie.data:
       data.name = translate_html(data.name, choice)
       data.hovertemplate = data.hovertemplate.replace("ODD:", translate_html("ODD:", choice)).replace("Somme des bénéficiaires:", translate_html("Somme des bénéficiaires:", choice))
     df_expanded['Budget global (DH)'] = pd.to_numeric(df_expanded['Budget global (DH)'], errors='coerce')
     df_expanded = df_expanded.dropna(subset=['Budget global (DH)'])
     budget = df_expanded.groupby('ODD')['Budget global (DH)'].sum()
     pie_chart_data_budget = pd.DataFrame({'ODD': budget.index, 'Budget global (DH)': budget.values})
     odd_traduits = [translate_html(sect, choice) for sect in pie_chart_data_budget['ODD']]
     pie_chart_data_budget['ODD'] = odd_traduits
     fig_budget_pie = px.pie(
    pie_chart_data_budget,
    values='Budget global (DH)',
    names='ODD',
    color='ODD',
    template="plotly_white",
    hover_data='ODD',
    color_discrete_map=odd_colors,
    hole=.8
)
     fig_budget_pie.update_traces(
    textposition='inside', rotation=0, insidetextorientation='auto', textfont_size=15,
    marker=dict(line=dict(color='#FFFFFF')), hovertemplate='<b>ODD</b>: %{label}<br><b>Budget global (DH)</b>: %{value}<extra></extra>',
    customdata=pie_chart_data_benef['ODD'] 
)
     fig_odd = make_subplots(
    rows=1, 
    cols=3, 
    specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]], 
    subplot_titles=(translate_html("<b style='color: #004378'>Nombre de projets/actions</b>", choice),translate_html("<b style='color: #004378'>Nombre de bénéficiaires</b>",choice),translate_html( "<b style='color: #004378'>Budget global (DH)</b>",choice)),
)
     fig_odd.add_trace(fig_odd_counts_pie['data'][0], row=1, col=1)
     fig_odd.add_trace(fig_benef_counts_pie['data'][0], row=1, col=2)
     fig_odd.add_trace(fig_budget_pie['data'][0], row=1, col=3)
     fig_odd.update_layout(
    legend_title_text=translate_html('ODD',choice),
    title_text=translate_html("<b style='color: #004378'>Indicateurs par ODD</b>",choice),
    title_x=0.3,
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color="black"),
    legend_font=dict(color='#004378'),
    legend=dict(
        x=1.01, 
        y=0  
    )
)
     st.plotly_chart(fig_odd, use_container_width=True)
#Nombre de Projets/Actions
     projets_par_an = df['Année'].value_counts().sort_index()
     total_beneficiaires_total = df.groupby('Année')['Nombre de bénéficiaires'].sum().reset_index()
     total_budget_global = df.groupby('Année')['Budget global (DH)'].sum().reset_index()
     years = sorted(df['Année'].apply(lambda x: int(x)).unique())
     fig = go.Figure()
     fig.add_trace(go.Scatter(x=projets_par_an.index, y=projets_par_an.values, mode='lines+markers', line=dict(color='orange'), name=translate_html('Nombre de projets/actions',choice)))
     fig.add_trace(go.Scatter(x=total_beneficiaires_total['Année'], y=total_beneficiaires_total['Nombre de bénéficiaires'], mode='lines+markers', line=dict(color='#caddfa'), name=translate_html('Nombre de bénéficiaires',choice)))
     fig.add_trace(go.Scatter(x=total_budget_global['Année'], y=total_budget_global['Budget global (DH)'], mode='lines+markers', line=dict(color='#042b66'), name=translate_html('Investissement global (DH)',choice)))
     fig.update_layout(
    title=translate_html('<b style="color: #004378">Évolution du nombre de projets/actions, du nombre de bénéficiaires et du budget global par an</b>',choice),
    xaxis=dict(
        title=translate_html('<b style="color: #004378">Année</b>',choice),
        tickvals=years, 
        ticktext=[str(year) for year in years],
        showgrid=False,
        tickfont=dict(color="#004378")
    ), 
    yaxis=dict(
        title=translate_html('<b style="color: #004378">Valeur</b>',choice),
        showgrid=False,
        tickfont=dict(color="#004378"),tickformat=',d'
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',  
    paper_bgcolor='rgba(0, 0, 0, 0)',  
    font=dict(color="darkblue"),                  
)
     
     fig.update_traces(
    hovertemplate='%{x}<br>'
                  '%{y}<br>'
                  '<extra></extra>'
)
     col1, col2 = st.columns([2, 1])
     with col1:
      st.plotly_chart(fig, use_container_width=True)
     with col2:
      st.markdown("")
      st.markdown("")
      st.markdown("")
      st.markdown("")
      st.markdown("")
      st.markdown(translate_html(f"<h2 style='text-align: center;letter-spacing: 1px;'><span style='color: #1d2873;font-size: 25px;'>Chaque année, Masen a joué un rôle essentiel dans la mise en œuvre de nombreux initiatives axés sur le développement durable des territoires</span></h2>",choice), unsafe_allow_html=True)
#Budget Global/Masen     
     total_part_masen = df.groupby('Année')['Investissement Masen (DH)'].sum().reset_index()
     total_budget_global = df.groupby('Année')['Budget global (DH)'].sum().reset_index()
     total_budget_global['Année'] = total_budget_global['Année'].astype(int)
     total_part_masen['Année'] = total_part_masen['Année'].astype(int)
     fig_budget_global = px.bar(total_budget_global, x='Année', y='Budget global (DH)', 
                           title=translate_html("<b style='color: #004378'>Budget global par an</b>",choice),
                           color_discrete_sequence=["orange"],
                           template="plotly_white")
     for i, data in enumerate(fig_budget_global.data):
      data.name = translate_html(data.name, choice)
      data.hovertemplate = data.hovertemplate.replace("Année=", translate_html("Année=", choice)).replace("Budget global (DH)=", translate_html("Budget global (DH)=", choice))
     titre_fig_part_masen="<b style='color: #004378'>Investissement de Masen par An</b>"
     fig_part_masen = px.bar(total_part_masen, x='Année', y='Investissement Masen (DH)', 
                        title=translate_html(titre_fig_part_masen,choice),
                        color_discrete_sequence=["orange"],
                        template="plotly_white")
     fig_budget_global.update_xaxes(tickvals=total_budget_global['Année'].unique())
     fig_part_masen.update_xaxes(tickvals=total_part_masen['Année'].unique())
     titre_fig_budget_global="<b style='color: #004378'>Investissement de Masen par An</b>"
     fig_budget_global.update_layout(plot_bgcolor="rgba(0,0,0,0)",title_x=0.4,
            font=dict(color="black"),
            xaxis=dict(title=translate_html(titre_fig_budget_global,choice),showgrid=False, tickfont=dict(color="#004378")), 
            paper_bgcolor='rgba(0, 0, 0, 0)',  
            yaxis=dict(title=translate_html("<b style='color: #004378'>Bugdet global par an</b>",choice), tickfont=dict(color="#004378")))
     for i, data in enumerate(fig_part_masen.data):
      data.name = translate_html(data.name, choice)
      data.hovertemplate = data.hovertemplate.replace("Année=", translate_html("Année=", choice)).replace("Investissement Masen (DH)=", translate_html("Investissement Masen (DH)=", choice))
     fig_part_masen.update_layout(plot_bgcolor="rgba(0,0,0,0)",title_x=0.4,
            font=dict(color="black"),
            xaxis=dict(title=translate_html("<b style='color: #004378'>Année</b>",choice),showgrid=False, tickfont=dict(color="#004378")), 
            paper_bgcolor='rgba(0, 0, 0, 0)', 
            yaxis=dict(title=translate_html("<b style='color: #004378'>Investissement de Masen par An</b>",choice), tickfont=dict(color="#004378")))
     fig_budget_global.update_layout(yaxis=dict(tickformat=",.0f")) 
     fig_part_masen.update_layout(yaxis=dict(tickformat=",.0f")) 
     st.markdown(translate_html(f"<p style='font-size: 18px; font-family: Calibri; color: black; font-weight: normal; text-align: justify;'>Le développement durable est encouragé par les investissements de MASEN dans les territoires riverains, qui sont le résultat d'une approche globale et collaborative. Les investissements réalisés en collaboration avec différents acteurs profitent de l'Objectif de Développement Durable (ODD) numéro 17, qui favorise la collaboration afin d'atteindre les objectifs communs. Que ce soit pour des projets d'énergie propre, des infrastructures sociales ou des programmes de développement économique, MASEN cherche à avoir un impact positif à long terme tout en contribuant à la réalisation des objectifs de développement durable locaux.</p>",choice), unsafe_allow_html=True)
     #st.plotly_chart(fig_budget_global, use_container_width=True)
     total_budget_global['Pourcentage investis par Masen (%)'] = (total_part_masen['Investissement Masen (DH)'] / total_budget_global['Budget global (DH)']) * 100
     titre_fig_pourcentage_part_masen="<b style='color: #004378'>Pourcentage investis par Masen par An</b>"
     fig_pourcentage_part_masen = px.bar(total_budget_global, x='Année', y='Pourcentage investis par Masen (%)', 
                                    title=translate_html(titre_fig_pourcentage_part_masen,choice),
                                    color_discrete_sequence=["orange"],
                                    template="plotly_white")
     fig_pourcentage_part_masen.update_layout(plot_bgcolor="rgba(0,0,0,0)",title_x=0.3,
            font=dict(color="black"),
            xaxis=dict(title=translate_html("<b style='color: #004378'>Année</b>",choice),showgrid=False, tickfont=dict(color="#004378")), 
            paper_bgcolor='rgba(0, 0, 0, 0)',  
            yaxis=dict(title=translate_html("<b style='color: #004378'>Pourcentage investis par Masen</b>",choice), tickfont=dict(color="#004378")))
     for i, data in enumerate(fig_pourcentage_part_masen.data):
      data.name = translate_html(data.name, choice)
      data.hovertemplate = data.hovertemplate.replace("Année=", translate_html("Année=", choice)).replace("Pourcentage investis par Masen (%)=", translate_html("Pourcentage investis par Masen (%)=", choice))
     fig_pourcentage_part_masen.update_xaxes(tickvals=total_part_masen['Année'].unique())
     col3, col4 = st.columns([1, 1])
     with col3:
      st.plotly_chart(fig_part_masen, use_container_width=True)
     with col4:  
      st.plotly_chart(fig_pourcentage_part_masen, use_container_width=True)
     moyenne_part_masen = total_part_masen['Investissement Masen (DH)'].mean()
     annee_max_part_masen = total_part_masen.loc[total_part_masen['Investissement Masen (DH)'].idxmax()]['Année']
     part_masen_max = total_part_masen['Investissement Masen (DH)'].max()
     annee_min_part_masen = total_part_masen.loc[total_part_masen['Investissement Masen (DH)'].idxmin()]['Année']
     part_masen_min = total_part_masen['Investissement Masen (DH)'].min()
     total_budget_global['Pourcentage_investis_par_Masen'] = (total_part_masen['Investissement Masen (DH)'] / total_budget_global['Budget global (DH)']) * 100  
     annee_max_pourcentage_masen = total_budget_global.loc[total_budget_global['Pourcentage_investis_par_Masen'].idxmax()]['Année']
     pourcentage_max_masen = total_budget_global['Pourcentage_investis_par_Masen'].max()
     annee_min_pourcentage_masen = total_budget_global.loc[total_budget_global['Pourcentage_investis_par_Masen'].idxmin()]['Année']
     pourcentage_min_masen = total_budget_global['Pourcentage_investis_par_Masen'].min()
     annee_min_pourcentage_masen = int(annee_min_pourcentage_masen)
     annee_max_pourcentage_masen = int(annee_max_pourcentage_masen)
     paragraphe_part_masen = f"<p style='font-size: 18px; font-family: Calibri; color: black; font-weight: normal; text-align: justify;'>L'investissement total de Masen a varié d'année en année. En moyenne, Masen a investi environ {locale.format_string("%d", moyenne_part_masen, grouping=True)} DH chaque année. D'une part, l'année qui a enregistré le plus grand investissement par Masen était {int(annee_max_part_masen)}, avec un montant de {locale.format_string("%d", part_masen_max, grouping=True)} DH. D'autre part, l'année avec le plus petit investissement était en {int(annee_min_part_masen)}, avec {locale.format_string("%d", int(part_masen_min), grouping=True)} DH. </p>"
     st.markdown(translate_html(paragraphe_part_masen,choice), unsafe_allow_html=True) 
     par=f"<p style='font-size: 18px; font-family: Calibri; color: black; font-weight: normal; text-align: justify;'>Le pourcentage le plus faible d'investissement par Masen était de {pourcentage_min_masen:.2f}% en {int(annee_min_pourcentage_masen)}, tandis que le plus grand, atteignant {int(pourcentage_max_masen)}%, était en {int(annee_max_pourcentage_masen)}.</p>"
     st.markdown(translate_html(par,choice),unsafe_allow_html=True)
     total_partenaires = df.groupby('Année')['Part de partenaires (DH)'].sum().reset_index()
     fig_partenaires = px.bar(total_partenaires, x='Année', y='Part de partenaires (DH)', 
                         title=translate_html("<b style='color: #004378'>Part des Partenaires par An</b>",choice),
                         color_discrete_sequence=["orange"],
                         template="plotly_white")
     fig_partenaires.update_layout(plot_bgcolor="rgba(0,0,0,0)",title_x=0.4,
            font=dict(color="black"),
            xaxis=dict(title=translate_html("<b style='color: #004378'>Année</b>",choice),showgrid=False, tickfont=dict(color="#004378")), 
            paper_bgcolor='rgba(0, 0, 0, 0)', 
            yaxis=dict(title=translate_html("<b style='color: #004378'>Part de partenaires (DH)</b>",choice), tickfont=dict(color="#004378")))
     for i, data in enumerate(fig_partenaires.data):
      data.name = translate_html(data.name, choice)
      data.hovertemplate = data.hovertemplate.replace("Année=", translate_html("Année=", choice)).replace("Part de partenaires (DH)=", translate_html("Part de partenaires (DH)=", choice))
     fig_partenaires.update_xaxes(tickvals=total_part_masen['Année'].unique())
     fig_partenaires.update_layout(yaxis=dict(tickformat=",.0f"))
     st.plotly_chart(fig_partenaires, use_container_width=True) 
     total_beneficiaires_total = df.groupby('Année')['Nombre de bénéficiaires'].sum().reset_index()
     moyenne_beneficiaires = total_beneficiaires_total['Nombre de bénéficiaires'].mean()
     annee_max_beneficiaires = total_beneficiaires_total.loc[total_beneficiaires_total['Nombre de bénéficiaires'].idxmax()]['Année']
     nombre_max_beneficiaires = total_beneficiaires_total['Nombre de bénéficiaires'].max()
     annee_min_beneficiaires = total_beneficiaires_total.loc[total_beneficiaires_total['Nombre de bénéficiaires'].idxmin()]['Année']
     nombre_min_beneficiaires = total_beneficiaires_total['Nombre de bénéficiaires'].min()
     para=f"<p style='font-size: 18px; font-family: Calibri; color: black; font-weight: normal; text-align: justify;'>Les projets de Masen, axés sur le développement durable des territoires, s'adressent à une vaste population comprenant hommes, femmes, jeunes et enfants.</p>"
     st.markdown(translate_html(para,choice),unsafe_allow_html=True)
#Bénéficiaires  
     paragraphe1 = f"<p style='font-size: 18px; font-family: Calibri; color: black; font-weight: normal; text-align: justify;'>Le nombre total de bénéficiaires des projets de Masen a varié au fil des ans. En moyenne, chaque année, il y a eu environ {locale.format_string("%d", int(moyenne_beneficiaires), grouping=True)} bénéficiaires. L'année ayant enregistré le plus grand nombre de bénéficiaires était {int(annee_max_beneficiaires)}, avec un total de {locale.format_string("%d", int(nombre_max_beneficiaires), grouping=True)} bénéficiaires. À l'inverse, l'année avec le nombre le plus faible de bénéficiaires était {int(annee_min_beneficiaires)}, avec seulement {locale.format_string("%d",int(nombre_min_beneficiaires), grouping=True)} bénéficiaires.</p>"
     fig_beneficiaires_total = px.bar(total_beneficiaires_total, x='Année', y='Nombre de bénéficiaires', 
                                 title=translate_html("<b style='color: #004378'>Nombre total de Bénéficiaires par An</b>", choice),
                                 color_discrete_sequence=["orange"],
                                 template="plotly_white")                            
     fig_beneficiaires_total.update_layout(plot_bgcolor="rgba(0,0,0,0)", title_x=0.4,
                                      font=dict(color="black"),
                                      xaxis=dict(title=translate_html("<b style='color: #004378'>Année</b>", choice), showgrid=False, tickfont=dict(color="#004378")), 
                                      paper_bgcolor='rgba(0, 0, 0, 0)',  
                                      yaxis=dict(title=translate_html("<b style='color: #004378'>Nombre total de Bénéficiaires par An</b>", choice), tickfont=dict(color="#004378")))
     for i, data in enumerate(fig_beneficiaires_total.data):
      data.name = translate_html(data.name, choice)
      data.hovertemplate = data.hovertemplate.replace("Année=", translate_html("Année=", choice)).replace("Nombre de bénéficiaires=", translate_html("Nombre de bénéficiaires=", choice))
     fig_beneficiaires_total.update_xaxes(tickvals=total_beneficiaires_total['Année'].unique())
     #st.plotly_chart(fig_beneficiaires_total, use_container_width=True)
     total_beneficiaires = df.groupby('Année')[[ 'Nombre de femmes', 'Nombre d\'enfants bénéficiaires', 'Nombres de jeunes  bénéficiaires']].sum().reset_index()
     fig_beneficiaires = px.bar(total_beneficiaires, x='Année', 
                           y=[ 'Nombre de femmes', 'Nombre d\'enfants bénéficiaires', 'Nombres de jeunes  bénéficiaires'],
                           title=translate_html("<b style='color: #004378'>Nombre de Bénéficiaires par Catégorie par An</b>",choice),
                           color_discrete_sequence=[ "#0b2845", "#4d7ba8", "#3857a6"],labels={'Année': translate_html("<b style='color: #004378'>Année</b>", choice),
                     'variable': translate_html("<b style='color: #004378'>Catégorie</b>", choice),
                     'value': translate_html("<b style='color: #004378'>Le nombre de bénéficiares</b>", choice)},
                           template="plotly_white")
     fig_beneficiaires.update_layout(barmode='stack', plot_bgcolor="rgba(0,0,0,0)",title_x=0.4,
            font=dict(color="black"),
            xaxis=dict(title=translate_html("<b style='color: #004378'>Année</b>",choice),showgrid=False, tickfont=dict(color="#004378")), 
            paper_bgcolor='rgba(0, 0, 0, 0)',  
            yaxis=dict(title=translate_html("<b style='color: #004378'>Nombre total de Bénéficiaires par An</b>",choice), tickfont=dict(color="#004378")))
     for i, data in enumerate(fig_beneficiaires.data):
      data.name = translate_html(data.name, choice)
      fig_beneficiaires.data[i].hovertemplate = fig_beneficiaires.data[i].hovertemplate.replace("Nombre de femmes", translate_html("Nombre de femmes", choice)).replace("Nombre d'enfants bénéficiaires", translate_html("Nombre d'enfants bénéficiaires", choice)).replace("Nombres de jeunes  bénéficiaires", translate_html("Nombres de jeunes  bénéficiaires", choice))
      data.hovertemplate = data.hovertemplate.replace("Année=", translate_html("Année=", choice)).replace("Value=", translate_html("Value=", choice))
     fig_beneficiaires.update_xaxes(tickvals=total_beneficiaires['Année'].unique())
     st.plotly_chart(fig_beneficiaires, use_container_width=True)
     st.markdown(translate_html(paragraphe1,choice),unsafe_allow_html=True)
def sideBar():
    with st.sidebar:
        selected=option_menu(
        menu_title=translate_html("Main Menu",choice),
        options=["🏠 Home","📊 Dashboard"],
        menu_icon="cast",
        default_index=0,
        orientation="v"
    )  
    if selected == "🏠 Home":
        Bilan_DDTM()
    
sideBar()     