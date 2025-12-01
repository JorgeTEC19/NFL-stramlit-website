#Imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import colorsys


st.set_page_config(page_title="NFL",
                   layout="wide")

def lighten_hex_color(hex_color: str, amount: float) -> str:
    """
    Lightens a hex color by the given amount.
    amount: float in [0, 1], where 0 = no change, 1 = white.
    """
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0

    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = min(1.0, l + amount * (1.0 - l))
    new_r, new_g, new_b = colorsys.hls_to_rgb(h, l, s)
    return "#{:02x}{:02x}{:02x}".format(
        int(new_r * 255), int(new_g * 255), int(new_b * 255)
    )

#color styles
with open("styles.css") as css_file:
  st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
color_palettes = {
    "PIT":  { "c1": "#101820", "c2": "#FFB612", "c3": "#003087" },   # Steelers – Black bg, Gold + Blue fg :contentReference[oaicite:1]{index=1}
    "CLE":  { "c1": "#311D00", "c2": "#FF3C00", "c3": "#FFFFFF" },   # Browns – Dark brown bg, Orange + White fg :contentReference[oaicite:2]{index=2}
    "NO":   { "c1": "#000000", "c2": "#D3BC8D", "c3": "#FFFFFF" },   # Saints – Black bg, Old gold + White fg :contentReference[oaicite:3]{index=3}
    "TB":   { "c1": "#0A0A08", "c2": "#D50A0A", "c3": "#FF7900" },   # Bucs – Very dark (almost black) bg, Red + Bay Orange fg :contentReference[oaicite:4]{index=4}
    "HOU":  { "c1": "#03202F", "c2": "#A71930", "c3": "#FFFFFF" },   # Texans – Deep Steel Blue bg, Battle Red + White fg :contentReference[oaicite:5]{index=5}
    "IND":  { "c1": "#002C5F", "c2": "#A2AAAD", "c3": "#FFFFFF" },   # Colts – Speed Blue bg, Gray + White fg :contentReference[oaicite:6]{index=6}
    "CIN":  { "c1": "#000000", "c2": "#FB4F14", "c3": "#FFFFFF" },   # Bengals – Black bg, Orange + White fg :contentReference[oaicite:7]{index=7}
    "CAR":  { "c1": "#101820", "c2": "#0085CA", "c3": "#BFC0BF" },   # Panthers – Black-ish bg, Carolina Blue + Silver fg :contentReference[oaicite:8]{index=8}
    "BAL":  { "c1": "#000000", "c2": "#241773", "c3": "#9E7C0C" },   # Ravens – Black bg, Purple + Gold fg :contentReference[oaicite:9]{index=9}
    "ATL":  { "c1": "#000000", "c2": "#A71930", "c3": "#A5ACAF" },   # Falcons – Black bg, Red + Silver fg :contentReference[oaicite:10]{index=10}
    "ARI":  { "c1": "#000000", "c2": "#97233F", "c3": "#FFB612" },   # Cardinals – Black bg, Cardinal Red + Yellow (Gold) fg :contentReference[oaicite:11]{index=11}
    "SEA":  { "c1": "#002244", "c2": "#69BE28", "c3": "#A5ACAF" },   # Seahawks – Navy bg, Action Green + Wolf Gray fg :contentReference[oaicite:12]{index=12}
    "NYG":  { "c1": "#012169", "c2": "#A71930", "c3": "#B4B4B4" },   # Giants – Dark Blue bg, Red + Gray fg :contentReference[oaicite:13]{index=13}
    "GB":   { "c1": "#203731", "c2": "#FFB612", "c3": "#FFFFFF" },   # Packers – Dark Green bg, Gold + White fg :contentReference[oaicite:14]{index=14}
    "NE":   { "c1": "#002244", "c2": "#C60C30", "c3": "#B0B7BC" },   # Patriots – Nautical Blue bg, Red + Silver fg :contentReference[oaicite:15]{index=15}
    "OAK":  { "c1": "#000000", "c2": "#A5ACAF", "c3": "#FFFFFF" },   # Raiders – Black bg, Silver + White fg :contentReference[oaicite:16]{index=16}
    "DET":  { "c1": "#0076B6", "c2": "#B0B7BC", "c3": "#000000" },   # Lions – Honolulu Blue bg, Silver + Black fg :contentReference[oaicite:17]{index=17}
    "WAS":  { "c1": "#5A1414", "c2": "#FFB612", "c3": "#FFFFFF" },   # Commanders (formerly Redskins) – Burgundy bg, Gold + White fg :contentReference[oaicite:18]{index=18}
    "TEN":  { "c1": "#0C2340", "c2": "#4B92DB", "c3": "#A5ACAF" },   # Titans – Titans Navy bg, Titans Blue + Silver fg :contentReference[oaicite:19]{index=19}
    "PHI":  { "c1": "#004C54", "c2": "#A5ACAF", "c3": "#000000" },   # Eagles – Midnight Green bg, Silver + Black fg :contentReference[oaicite:20]{index=20}
    "NYJ":  { "c1": "#125740", "c2": "#000000", "c3": "#FFFFFF" },   # Jets – Gotham Green bg, Black + White fg :contentReference[oaicite:21]{index=21}
    "KC":   { "c1": "#E31837", "c2": "#FFB81C", "c3": "#FFFFFF" },   # Chiefs – Red bg, Gold + White fg :contentReference[oaicite:22]{index=22}
    "JAC":  { "c1": "#000000", "c2": "#9F792C", "c3": "#006778" },   # Jaguars – Black bg, Gold + Teal fg :contentReference[oaicite:23]{index=23}
    "SF":   { "c1": "#AA0000", "c2": "#B3995D", "c3": "#000000" },   # 49ers – Red bg, Gold + Black fg :contentReference[oaicite:24]{index=24}
    "BUF":  { "c1": "#00338D", "c2": "#C60C30", "c3": "#FFFFFF" },   # Bills – Blue bg, Red + White fg :contentReference[oaicite:25]{index=25}
    "SD":   { "c1": "#0080C6", "c2": "#FFC20E", "c3": "#FFFFFF" },   # Chargers (San Diego) – Powder Blue bg, Sunshine Gold + White fg :contentReference[oaicite:26]{index=26}
    "DEN":  { "c1": "#002244", "c2": "#FB4F14", "c3": "#FFFFFF" },   # Broncos – Navy bg, Orange + White fg :contentReference[oaicite:27]{index=27}
    "CHI":  { "c1": "#0B162A", "c2": "#C83803", "c3": "#FFFFFF" },   # Bears – Dark Navy bg, Orange + White fg :contentReference[oaicite:28]{index=28}
    "DAL":  { "c1": "#041E42", "c2": "#003594", "c3": "#869397" },   # Cowboys – Navy bg, Royal Blue + Silver fg :contentReference[oaicite:29]{index=29}
    "MIA":  { "c1": "#008E97", "c2": "#FC4C02", "c3": "#005778" },   # Dolphins – Aqua bg, Orange + Blue fg :contentReference[oaicite:30]{index=30}
    "MIN":  { "c1": "#4F2683", "c2": "#FFC62F", "c3": "#FFFFFF" },   # Vikings – Purple bg, Gold + White fg :contentReference[oaicite:31]{index=31}
    "STL":  { "c1": "#003594", "c2": "#FFD100", "c3": "#FFFFFF" },   # Rams (St. Louis) – Blue bg, Gold + White fg :contentReference[oaicite:32]{index=32}
    "LA":   { "c1": "#003594", "c2": "#FFA300", "c3": "#FFFFFF" },   # Rams (Los Angeles) – Blue bg, Gold + White fg :contentReference[oaicite:33]{index=33}
    "LAC":  { "c1": "#0080C6", "c2": "#FFC20E", "c3": "#FFFFFF" },   # Chargers (L.A.) – Powder Blue bg, Sunshine Gold + White fg :contentReference[oaicite:34]{index=34}
}
for team, cols in color_palettes.items():
    cols["c4"] = lighten_hex_color(cols["c1"], 0.30)

with st.sidebar:
  st.title("Choose Team")
  Team = st.selectbox("Select Team",
  list(color_palettes.keys()))
#Implementing the color
selected_palette = color_palettes[Team]
st.markdown(
  f"""
  <style>
  :root {{
  --main-bg-color: {selected_palette["c1"]};
  --button-color: {selected_palette["c2"]};
  --text-color: {selected_palette["c3"]};
  --sidebar-bg-color: {selected_palette["c4"]};
  }}
  </style>
  """,
  unsafe_allow_html=True
)

import gdown

# Download the file (this will handle authentication)
gdown.download(f"https://drive.google.com/uc?id=1fIzxoGuBumGXpzqAfkP52CJdJdFO2Wx8", "data.csv", quiet=False)
df = pd.read_csv("data.csv")
df["game_date"]=pd.to_datetime(df["game_date"])
df["Year"]=df["game_date"].dt.year
df['Year'] = df['Year'].fillna(0).astype(int)
df["Succesfull"]=df["yards_gained"]/df["ydstogo"]>=0.4

#Fixxing null values
object_cols = df.select_dtypes(include=['object']).columns
df[object_cols] = df[object_cols].fillna('None')
float_cols = df.select_dtypes(include=['float']).columns
df[float_cols] = df[float_cols].fillna(0)

# Título principal
st.markdown("<h1 style='text-align: center; color: white;'> NFL </h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)

st.subheader("Metrics")
met_col1,met_col2,met_col3=st.columns(3)
FiltDFMet=df[df["posteam"]==Team]
with met_col1:
  st.metric("Total plays",FiltDFMet.shape[0])
with met_col2:
  st.metric("Runs",FiltDFMet[FiltDFMet["play_type"]=="run"].shape[0])
with met_col3:
  st.metric("Passes",FiltDFMet[FiltDFMet["play_type"]=="pass"].shape[0])

#Graphs
st.subheader("Graphs")
G1,G2,G3=st.tabs(["Distribution of yards gained","Play type used vs Field Position","Play type used vs Yards left for first down"])
with G1:
  #G1 filters
  yearGroup1=st.selectbox("Year",df["Year"].unique())
  FiltDF = df[(df["Year"] == yearGroup1) & (df["posteam"] == Team)]
  #G1


  fig1, ax2 = plt.subplots(figsize=(6, 4))
  # Set figure and axes background to c4
  fig1.patch.set_facecolor(selected_palette["c4"])
  ax2.set_facecolor(selected_palette["c4"])
  # Set histogram bar color to c1
  sns.histplot(data=FiltDF, x='yards_gained', ax=ax2, color=selected_palette["c1"])
  # Set text color to c3
  ax2.tick_params(axis='x', colors=selected_palette["c3"])
  ax2.tick_params(axis='y', colors=selected_palette["c3"])
  ax2.xaxis.label.set_color(selected_palette["c3"])
  ax2.yaxis.label.set_color(selected_palette["c3"])
  ax2.title.set_color(selected_palette["c3"])
  plt.setp(ax2.get_yticklabels(), color=selected_palette["c3"])
  plt.setp(ax2.get_xticklabels(), color=selected_palette["c3"])
  ax2.spines['bottom'].set_color(selected_palette["c3"])
  ax2.spines['top'].set_color(selected_palette["c3"])
  ax2.spines['left'].set_color(selected_palette["c3"])
  ax2.spines['right'].set_color(selected_palette["c3"])
  st.header("Distribution of yards gained")
  st.pyplot(fig1)
with G2:
  #G2 filters
  yearGroup2=st.selectbox("Year ",df["Year"].unique())
  FiltDF = df[(df["Year"] == yearGroup2) & (df["posteam"] == Team)]
  #G2
  if 'play_type' in FiltDF.columns:
      play_type_column_name = 'play_type'
      title_suffix = 'Play Type'
  else:
      play_type_column_name = 'posteam_type'
      title_suffix = 'Posteam Type'
      print(f"Note: Column 'play_type' not found. Using '{play_type_column_name}' for grouping instead.")

  FiltDF[play_type_column_name] = FiltDF[play_type_column_name].apply(lambda x: x if x in ['pass', 'run'] else 'Others')

  agg_df = FiltDF.groupby(['yardline_100', play_type_column_name]).agg(
      avg_success_rate=('Succesfull', 'mean'),
      play_count=('play_id', 'count')
  ).reset_index()


  fig2 = make_subplots(specs=[[{"secondary_y": True}]])

  unique_types = agg_df[play_type_column_name].unique()
  plotly_colors = [selected_palette["c1"], selected_palette["c2"], selected_palette["c3"]] # Custom colors

  for i, current_type in enumerate(unique_types):
      df_filtered = agg_df[agg_df[play_type_column_name] == current_type]
      fig2.add_trace(
          go.Bar(
              x=df_filtered['yardline_100'],
              y=df_filtered['play_count'],
              name=f'Count ({current_type})',
              marker_color=plotly_colors[i % len(plotly_colors)], # Use custom colors
              legendgroup=current_type,
              showlegend=True
          ),
          secondary_y=False,
      )


  for i, current_type in enumerate(unique_types):
      df_filtered = agg_df[agg_df[play_type_column_name] == current_type]
      fig2.add_trace(
          go.Scatter(
              x=df_filtered['yardline_100'],
              y=df_filtered['avg_success_rate'],
              mode='lines+markers',
              name=f'Avg Success Rate ({current_type})',
              yaxis='y2',
              marker_color=plotly_colors[i % len(plotly_colors)], # Use custom colors
              line_color=plotly_colors[i % len(plotly_colors)], # Also set line color
              legendgroup=current_type,
              showlegend=True
          ),
          secondary_y=True,
      )
  st.header("Play Count and Average Success Rate by Yardline 100 and Play type")
  fig2.update_layout(
      xaxis_title='Yardline 100 (yardline_100)',
      barmode='stack', # Changed from 'group' to 'stack'
      legend_title_text=title_suffix,
      plot_bgcolor=selected_palette["c4"],  # Chart area background
      paper_bgcolor=selected_palette["c4"], # Entire figure background
      font=dict(color=selected_palette["c3"]) # Global font color
  )


  fig2.update_yaxes(title_text='Count of Plays', secondary_y=False)
  fig2.update_yaxes(title_text='Average Success Rate', secondary_y=True, range=[0,1])
  fig2.update_xaxes(linecolor=selected_palette["c3"], gridcolor=selected_palette["c3"], zerolinecolor=selected_palette["c3"])
  fig2.update_yaxes(linecolor=selected_palette["c3"], gridcolor=selected_palette["c3"], zerolinecolor=selected_palette["c3"], secondary_y=False)
  fig2.update_yaxes(linecolor=selected_palette["c3"], gridcolor=selected_palette["c3"], zerolinecolor=selected_palette["c3"], secondary_y=True)

  st.plotly_chart(fig2)

with G3:
  #G3 filters
  yearGroup3=st.selectbox("Year  ",df["Year"].unique())
  FiltDF = df[(df["Year"] == yearGroup3) & (df["posteam"] == Team)]
  #G3
  if 'play_type' in FiltDF.columns:
      play_type_column_name = 'play_type'
      title_suffix = 'Play Type'
  else:
      play_type_column_name = 'posteam_type'
      title_suffix = 'Posteam Type'
      print(f"Note: Column 'play_type' not found. Using '{play_type_column_name}' for grouping instead.")

  FiltDF[play_type_column_name] = FiltDF[play_type_column_name].apply(lambda x: x if x in ['pass', 'run'] else 'Others')


  agg_df = FiltDF.groupby(['ydstogo', play_type_column_name]).agg(
      avg_success_rate=('Succesfull', 'mean'),
      play_count=('play_id', 'count')
  ).reset_index()


  fig = make_subplots(specs=[[{"secondary_y": True}]])


  unique_types = agg_df[play_type_column_name].unique()
  plotly_colors = [selected_palette["c1"], selected_palette["c2"], selected_palette["c3"]] # Custom colors


  for i, current_type in enumerate(unique_types):
      df_filtered = agg_df[agg_df[play_type_column_name] == current_type]
      fig.add_trace(
          go.Bar(
              x=df_filtered['ydstogo'],
              y=df_filtered['play_count'],
              name=f'Count ({current_type})',
              marker_color=plotly_colors[i % len(plotly_colors)], # Use custom colors
              legendgroup=current_type,
              showlegend=True
          ),
          secondary_y=False,
      )

  for i, current_type in enumerate(unique_types):
      df_filtered = agg_df[agg_df[play_type_column_name] == current_type]
      fig.add_trace(
          go.Scatter(
              x=df_filtered['ydstogo'],
              y=df_filtered['avg_success_rate'],
              mode='lines+markers',
              name=f'Avg Success Rate ({current_type})',
              yaxis='y2',
              marker_color=plotly_colors[i % len(plotly_colors)], # Use custom colors
              line_color=plotly_colors[i % len(plotly_colors)], # Also set line color
              legendgroup=current_type,
              showlegend=True
          ),
          secondary_y=True,
      )

  st.header("Play Count and Average Success Rate by Yards to Go and Play type")
  fig.update_layout(
      xaxis_title='Yards to Go (ydstogo)',
      barmode='stack', # Changed from 'group' to 'stack'
      legend_title_text=title_suffix,
      plot_bgcolor=selected_palette["c4"],  # Chart area background
      paper_bgcolor=selected_palette["c4"], # Entire figure background
      font=dict(color=selected_palette["c3"]) # Global font color
  )


  fig.update_yaxes(title_text='Count of Plays', secondary_y=False)
  fig.update_yaxes(title_text='Average Success Rate', secondary_y=True, range=[0,1])
  fig.update_xaxes(linecolor=selected_palette["c3"], gridcolor=selected_palette["c3"], zerolinecolor=selected_palette["c3"])
  fig.update_yaxes(linecolor=selected_palette["c3"], gridcolor=selected_palette["c3"], zerolinecolor=selected_palette["c3"], secondary_y=False)
  fig.update_yaxes(linecolor=selected_palette["c3"], gridcolor=selected_palette["c3"], zerolinecolor=selected_palette["c3"], secondary_y=True)

  st.plotly_chart(fig)
