import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


histogram_file = "histogram.html"

def cci_prof(df, area_conhecimento, item, titulo=""):
    coluna_y = item
    
    scatter = go.Figure()

    if area_conhecimento == "MT" and item > 40:
      scatter.add_trace(go.Scatter(
          x=df['theta'],
          y=df[f"Item  {coluna_y}"],
          name=df.columns[coluna_y-1],
          mode='lines'
      ))
    else:
      scatter.add_trace(go.Scatter(
          x=df['theta'],
          y=df[f"Item  {coluna_y}"],
          name=df.columns[coluna_y],
          mode='lines'
      ))

    # Layout do gráfico
    scatter.update_layout(
        title=titulo,
        xaxis=dict(
            title='Habilidade θ',
            zeroline=False
        ),
        yaxis=dict(
            title='Probabilidade P(θ)',
            zeroline=False
        )
    )
    
    return scatter

def theta_to_enem(habilidade_tri):
   habilidade_enem = ((habilidade_tri + 4) / 8) * 800 + 200
   return habilidade_enem


def scatter_plot(df, area_conhecimento, item, aluno, habilidade_normalizada, dificuldade, examinando="", titulo=""):
    coluna_y = item

    habilidade_enem = theta_to_enem(df['theta'])
    
    scatter = go.Figure()

    if area_conhecimento == "MT" and item > 40:
      scatter.add_trace(go.Scatter(
          x=habilidade_enem,
          y=df[f"Item  {coluna_y}"],
          name=df.columns[coluna_y-1],
          mode='lines'
      ))
    else:
      scatter.add_trace(go.Scatter(
          x=habilidade_enem,
          y=df[f"Item  {coluna_y}"],
          name=df.columns[coluna_y],
          mode='lines'
      ))

    # Layout do gráfico
    scatter.update_layout(
        title=titulo,
        xaxis=dict(
            title='Habilidade θ',
            zeroline=False
        ),
        yaxis=dict(
            title='Probabilidade P(θ)',
            range=[0, 1.0],
            zeroline=False
        )
    )

    scatter.add_shape(
      type="line",
      x0=habilidade_normalizada,
      x1=habilidade_normalizada,
      y0=0,
      y1=aluno['probabilidade'],
      line=dict(
          width=1.5,
          dash="dot",
          color="#888"
      )
    )

    scatter.add_shape(
      type="line",
      x0=habilidade_enem.min(),
      x1=habilidade_normalizada,
      y0=aluno['probabilidade'],
      y1=aluno['probabilidade'],
      line=dict(
          width=1.5,
          dash="dot",
          color="#888"
      )
    )

    # Anotação
    scatter.add_annotation(
        x=habilidade_normalizada,
        y=aluno['probabilidade'],
        text=f"{examinando}<br>Habilidade (θ): {habilidade_normalizada:.2f}"
             f"<br>Probabilidade P(θ): {np.round(aluno['probabilidade'] * 100, 2)}%",
        showarrow=True,
        arrowhead=7,
        arrowwidth=2,
        ax=aluno['theta'] - 100,
        ay=-100,
        arrowcolor="#636363",
        bordercolor="#c7c7c7",
        bgcolor="#2CA02C",
        font=dict(color="white")
    )

    scatter.add_annotation(
       x=dificuldade,
       y=(1+aluno["prob_chute"])/2,
       text=f"Dificuldade do item: {dificuldade:.2f}",
       showarrow=True,
        arrowhead=7,
        arrowwidth=2,
        ax=aluno['theta'] - 100,
        ay=-100,
        arrowcolor="#636363",
        bordercolor="#c7c7c7",
        bgcolor="#2CA02C",
        font=dict(color="white")
    )

    scatter.add_annotation(
      x=habilidade_normalizada,
      y=0,
      text=f"{habilidade_normalizada:.2f}",
      showarrow=False,
      yshift=-12,
      font=dict(size=10, color="#333"),
      bgcolor="white",
      bordercolor="#999",
      borderwidth=1,
      opacity=0.8
    )

    scatter.add_annotation(
      x=habilidade_enem.min(),
      y=aluno['probabilidade'],
      text=f"{aluno['probabilidade']:.3f}",
      showarrow=False,
      xshift=-20,
      font=dict(size=10, color="#333"),
      bgcolor="white",
      bordercolor="#999",
      borderwidth=1,
      opacity=0.8
    )
    
    return scatter


def get_habilidade_aluno(matricula, estado, area_conhecimento, questao):
  df_habil_3PL = pd.read_csv(f"../habilidades/habil_3PL_ltm_{area_conhecimento}_{estado}.csv")
  df_habil_3PL["alunos_id_string"] = df_habil_3PL["alunos_id_string"].astype(str)
  habil_examinando = df_habil_3PL[df_habil_3PL["alunos_id_string"] == str(matricula)]
  print("Habilidade do aluno: ", habil_examinando["habilidade"].values[0])
  
  return habil_examinando

def get_dificuldade_item(estado, area_conhecimento, item):
  df_dificuldade = pd.read_csv(f"../dificuldades/dif_modelo_3PL_ltm_{area_conhecimento}_{estado}.csv")
  df_dificuldade = df_dificuldade[df_dificuldade["questao"] == item]
  
  chute = df_dificuldade["acerto_acaso_item"].values[0]
  dificuldade = df_dificuldade["dificuldade_item"].values[0]
  discriminacao = df_dificuldade["discriminacao_item"].values[0]
  
  return chute, dificuldade, discriminacao

def get_prob_acerto(area_conhecimento, estado):
  df_probabilidade = pd.read_csv(f"../probabilidades/df_prob_3PL_LTM_{area_conhecimento}_{estado}.csv")
  
  return df_probabilidade
  

def gera_cci_prof(item, area_conhecimento, estado):
   cci_file_prof = f"plots/cci_prof_{item}_{area_conhecimento}_{estado}.html"
   
   df_probabilidade = get_prob_acerto(area_conhecimento, estado)

   cci = cci_prof(df_probabilidade, area_conhecimento, item, f"CCI para o item {item} da prova de {area_conhecimento}")

   cci_html = cci.to_html(include_plotlyjs="cdn", full_html=False)

   with open(cci_file_prof, "w", encoding="utf-8") as f:
      f.write(cci_html)



def gera_cci_aluno(matricula, questao, area_conhecimento, estado):
  cci_file = f"plots/cci_{matricula}_{estado}_{area_conhecimento}_{questao}.html"

  habil_examinando = get_habilidade_aluno(matricula, estado, area_conhecimento, questao)
  habil_examinando = habil_examinando["habilidade"].values[0]
  if habil_examinando > 4:
    habil_examinando = 4.00
  elif habil_examinando < -4:
    habil_examinando = -4.00
  
  habil_examinando_normalizada = ((habil_examinando + 4)/8) * 800 + 200
  habil_examinando = round(habil_examinando, 4)

  acerto_acaso_item, dificuldade_item, discriminacao_item = get_dificuldade_item(estado, area_conhecimento, questao)
  
  dificuldade_normalizada = dificuldade_item

  if dificuldade_item > 4:
    dificuldade_normalizada = 4.00
  elif dificuldade_item < -4:
    dificuldade_normalizada = -4.00
  
  dificuldade_normalizada = ((dificuldade_normalizada + 4)/8) * 800 + 200

  df_probabilidade = get_prob_acerto(area_conhecimento, estado)

  prob_acerto = df_probabilidade[round(df_probabilidade["theta"], 4) == habil_examinando]
  prob_acerto = prob_acerto[f'Item  {questao}'].values[0]

  dados_examinando = {
    "theta": habil_examinando,
    "probabilidade": prob_acerto,
    "prob_chute": acerto_acaso_item,
    "discriminacao": discriminacao_item,
    "dificuldade": dificuldade_item
  }


  cci = scatter_plot(df_probabilidade, area_conhecimento, questao, dados_examinando, habil_examinando_normalizada, dificuldade_normalizada, f"Examinando {matricula}", f"CCI para o item {questao} da prova de {area_conhecimento}")

  cci_html = cci.to_html(include_plotlyjs="cdn", full_html=False)

  with open(cci_file, "w", encoding="utf-8") as f:
      f.write(cci_html)
  
  return os.path.abspath(cci_file)

def gera_cci_aluno_no_llm(matricula, questao, area_conhecimento, estado):
  cci_file = f"../plots/cci_{matricula}_{estado}_{area_conhecimento}_{questao}.html"

  habil_examinando = get_habilidade_aluno(matricula, estado, area_conhecimento, questao)
  habil_examinando = habil_examinando["habilidade"].values[0]
  if habil_examinando > 4:
    habil_examinando = 4.00
  elif habil_examinando < -4:
    habil_examinando = -4.00
  
  habil_examinando_normalizada = ((habil_examinando + 4)/8) * 800 + 200
  habil_examinando = round(habil_examinando, 4)

  acerto_acaso_item, dificuldade_item, discriminacao_item = get_dificuldade_item(estado, area_conhecimento, questao)
  
  dificuldade_normalizada = dificuldade_item

  if dificuldade_item > 4:
    dificuldade_normalizada = 4.00
  elif dificuldade_item < -4:
    dificuldade_normalizada = -4.00
  
  dificuldade_normalizada = ((dificuldade_normalizada + 4)/8) * 800 + 200

  df_probabilidade = get_prob_acerto(area_conhecimento, estado)

  prob_acerto = df_probabilidade[round(df_probabilidade["theta"], 4) == habil_examinando]
  prob_acerto = prob_acerto[f'Item  {questao}'].values[0]

  dados_examinando = {
    "theta": habil_examinando,
    "probabilidade": prob_acerto,
    "prob_chute": acerto_acaso_item,
    "discriminacao": discriminacao_item,
    "dificuldade": dificuldade_item
  }


  cci = scatter_plot(df_probabilidade, area_conhecimento, questao, dados_examinando, habil_examinando_normalizada, dificuldade_normalizada, f"Examinando {matricula}", f"CCI para o item {questao} da prova de {area_conhecimento}")

  cci_html = cci.to_html(include_plotlyjs="cdn", full_html=False)

  with open(cci_file, "w", encoding="utf-8") as f:
      f.write(cci_html)
  
  return cci_file



def create_histograms(estado, area_conhecimento):
    df = pd.read_csv(f"../normalized_data/habilidades/habil_{area_conhecimento}_{estado}.csv")

    df = df["habilidade_normalizada"].values[:]

    fig = px.histogram(x=df,nbins=10, title="Distribuição de Habilidade (escala 200-1000)")
    fig.update_layout(xaxis_title="Habilidade", yaxis_title="Qtde alunos")
    histogram_html = fig.to_html(include_plotlyjs="cdn", full_html=False)

    with open(histogram_file, "w", encoding="utf-8") as f:
      f.write(histogram_html)


if __name__ == "__main__":
    matricula = "210055325099"
    questao = 21
    area_conhecimento = "CH"
    estado = "PA"
    gera_cci_aluno(matricula, questao, area_conhecimento, estado)
