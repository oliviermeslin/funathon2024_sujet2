import pandas as pd
import geopandas as gpd
import plotly.express as px

import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium

import src.import_data as sid
from src.create_data_list import create_data_list
from src.divers_functions import (
  create_data_from_input,
  summary_stat_airport
)
from src.tables import create_table_airports
from src.figures import plot_airport_line, map_leaflet_airport


YEARS_LIST = [str(year) for year in range(2018, 2023)]
MONTHS_LIST = list(range(1, 13))
year = YEARS_LIST[0]
month = MONTHS_LIST[0]

# Load data ----------------------------------
urls = create_data_list("./sources.yml")


pax_apt_all = sid.import_airport_data(urls['airports'].values())
pax_cie_all = sid.import_airport_data(urls['compagnies'].values())
pax_lsn_all = sid.import_airport_data(urls['liaisons'].values())

airports_location = gpd.read_file(
    urls['geojson']['airport']
)


liste_aeroports = pax_apt_all['apt'].unique()
default_airport = liste_aeroports[0]


# OBJETS NECESSAIRES A L'APPLICATION ------------------------

pax_apt_all['trafic'] = pax_apt_all['apt_pax_dep'] + \
  pax_apt_all['apt_pax_tr'] + \
  pax_apt_all['apt_pax_arr']

trafic_aeroports = (
  pax_apt_all
  .loc[pax_apt_all['apt'] == default_airport]
)
trafic_aeroports['date'] = pd.to_datetime(
  trafic_aeroports['anmois'] + '01', format='%Y%m%d'
)

# Streamlit Layout --------------------------------------

st.set_page_config(
  page_title="Tableau de bord des aéroports français", layout="wide",
  page_icon="✈️"
  )
col1, col2 = st.columns(2)


selected_date = st.date_input("", pd.to_datetime("2019-01-01"))
year = selected_date.year
month = selected_date.month

# Aggregate using input values
stats_aeroports = summary_stat_airport(
  create_data_from_input(pax_apt_all, year, month)
)

# Transform GT table into HTML
table_airports = (
  create_table_airports(stats_aeroports)
  .as_raw_html()
)

# VALORISATIONS ----------------------------------------------

figure_plotly = plot_airport_line(trafic_aeroports, default_airport)

carte_interactive = map_leaflet_airport(
  pax_apt_all, airports_location,
  month, year
)


with col1:
    components.html(table_airports, height=600)





