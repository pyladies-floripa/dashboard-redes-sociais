import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ==========================================
# 1. CONFIGURAÇÕES
# ==========================================
COR_AZUL = '#4ABBD5'     
COR_LARANJA = '#E09B18'  
COR_TEXTO = '#333333'    
COR_FUNDO = '#F9F9F9' 

diretorio_script = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(diretorio_script, 'respostas.csv')

COL_HABILIDADE = "Quais habilidades você possui?"
COL_APRENDER = "Quais habilidades quer desenvolver?"
COL_GITHUB = "Possui GitHub?"

try:
    df = pd.read_csv(caminho_csv)
except FileNotFoundError:
    print(f"ERRO: Arquivo {caminho_csv} não encontrado.")
    exit()

def padronizar_nomes(texto):
    if not isinstance(texto, str): return texto
    mapeamento = {
        'Analise de Dados': 'Análise de Dados',
        'ETL (Extract, Transform, Load)': 'ETL',
        'Programação em Python': 'Python',
        'Git e GitHub': 'Git/GitHub',
        'Criação de Dashboard': 'Dashboards'
    }
    return mapeamento.get(texto.strip(), texto.strip())

def limpar_contar(dataframe, NOME_COLUNA):
    if NOME_COLUNA not in dataframe.columns:
        return pd.Series(dtype=int)
    return dataframe[NOME_COLUNA].astype(str).str.split(';').explode().str.strip().apply(padronizar_nomes).value_counts()

# Processamento
sabe = limpar_contar(df, COL_HABILIDADE)
quer = limpar_contar(df, COL_APRENDER)
df_skills = pd.DataFrame({"Possui": sabe, "Quer Aprender": quer}).fillna(0).sort_values(by="Quer Aprender", ascending=True)

if COL_GITHUB in df.columns:
    dados_github = df[COL_GITHUB].value_counts()
else:
    dados_github = pd.Series(dtype=int)

# KPIs
total_respondentes = len(df)
top_interesse = df_skills['Quer Aprender'].idxmax()
pct_github = (dados_github.get('Sim', 0) / total_respondentes) * 100

# ==========================================
# 2. VISUALIZAÇÃO
# ==========================================
fig = plt.figure(figsize=(14, 12), facecolor=COR_FUNDO)
gs = fig.add_gridspec(2, 2, height_ratios=[0.8, 2.5]) 

# Cabeçalho 
fig.text(0.05, 0.94, ' Análise de Perfil | Projeto Dashboard Redes Sociais ', 
         fontsize=18, color='white', backgroundcolor=COR_AZUL, va='center', fontweight='bold')

# --- ROW 0: KPIs e GITHUB ---

# 1. KPIs (Topo Esquerdo)
ax_kpi = fig.add_subplot(gs[0, 0])
ax_kpi.set_facecolor(COR_FUNDO)
ax_kpi.axis('off')

# Posições Y
Y_TITULO = 0.70
Y_VALOR = 0.40  

# KPI 1 - Total
ax_kpi.text(0.1, Y_TITULO, "Total de Respostas", fontsize=11, color='#666666', transform=ax_kpi.transAxes)

ax_kpi.text(0.1, Y_VALOR, f"{total_respondentes}", fontsize=42, fontweight='bold', color=COR_AZUL, transform=ax_kpi.transAxes, va='center')

# KPI 2 - Interesse
ax_kpi.text(0.5, Y_TITULO, "Maior Interesse da Equipe", fontsize=11, color='#666666', transform=ax_kpi.transAxes)

ax_kpi.text(0.5, Y_VALOR, f"{top_interesse}", fontsize=28, fontweight='bold', color=COR_LARANJA, transform=ax_kpi.transAxes, va='center')

# Linhas decorativas 
ax_kpi.plot([0.1, 0.3], [0.62, 0.62], color=COR_AZUL, lw=2, alpha=0.3, transform=ax_kpi.transAxes)
ax_kpi.plot([0.5, 0.8], [0.62, 0.62], color=COR_LARANJA, lw=2, alpha=0.3, transform=ax_kpi.transAxes)


# 2. GITHUB (Topo Direito)
ax2 = fig.add_subplot(gs[0, 1])

if not dados_github.empty:
    mapa_cores = {'Sim': COR_AZUL, 'Não': COR_LARANJA}
    cores_grafico = [mapa_cores.get(x, '#999999') for x in dados_github.index]
    
    wedges, texts, autotexts = ax2.pie(
        dados_github, labels=None, autopct='%1.1f%%',
        startangle=90, colors=cores_grafico, radius=0.9, pctdistance=0.75,
        wedgeprops=dict(width=0.3, edgecolor=COR_FUNDO, linewidth=2)
    )
    plt.setp(autotexts, size=11, weight="bold", color=COR_TEXTO)
    ax2.text(0, 0, "Usa\nGitHub?", ha='center', va='center', fontsize=12, fontweight='bold', color='#666666')
else:
    ax2.text(0.5, 0.5, 'Sem dados', ha='center', transform=ax2.transAxes)


# --- ROW 1: BARRAS ---

ax1 = fig.add_subplot(gs[1, :])
ax1.set_facecolor(COR_FUNDO)

y = np.arange(len(df_skills))
height = 0.35 

rects1 = ax1.barh(y + height/2, df_skills['Quer Aprender'], height, label='Querem Aprender', color=COR_LARANJA)
rects2 = ax1.barh(y - height/2, df_skills['Possui'], height, label='Já Possuem', color=COR_AZUL)

ax1.set_yticks(y)
ax1.set_yticklabels(df_skills.index, fontsize=12, color=COR_TEXTO)

ax1.set_title('Mapeamento de Habilidades', fontsize=16, fontweight='bold', color=COR_TEXTO, loc='left', pad=40)
ax1.legend(loc='upper left', bbox_to_anchor=(0, 1.05), frameon=False, ncol=2)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.xaxis.set_visible(False)
ax1.tick_params(axis='y', length=0)

ax1.bar_label(rects1, padding=4, fmt='%d', fontweight='bold', color=COR_LARANJA, fontsize=10)
ax1.bar_label(rects2, padding=4, fmt='%d', color=COR_AZUL, fontsize=10)

fig.text(0.5, 0.02, 'Fonte: Questionário PyLadies Floripa | Gerado via Python', 
         ha='center', fontsize=10, color='#999999')

plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.show()