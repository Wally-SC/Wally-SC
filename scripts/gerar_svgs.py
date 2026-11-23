"""Gera os SVGs animados do README do perfil. Uso: python scripts/gerar_svgs.py assets"""

import sys
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

SAIDA = Path(sys.argv[1])
SAIDA.mkdir(parents=True, exist_ok=True)

PRETO = "#050807"
VERDE = "#00e57a"
VERDE2 = "#10b981"
VERDE_ESCURO = "#064e3b"
MARINHO = "#0b1f3a"
MARINHO2 = "#1e3a8a"
TEXTO = "#d1fae5"
APAGADO = "#86a397"
FONTE = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'Courier New', monospace"

PROJETOS = [
    # (nome, descrição, tecnologias, selo, destaque)
    ("lsm-kv-store", "Banco chave-valor LSM-tree escrito do zero: WAL, SSTables com índice esparso, filtro de Bloom e compactação.",
     ["Python", "Storage", "CI 3 SOs"], "146 testes", True),
    ("controle-de-estoque", "Estoque com consistência forte sob alta concorrência: lock pessimista por produto no PostgreSQL e API REST.",
     ["FastAPI", "PostgreSQL", "Docker"], "182 testes", True),
    ("consulta-cnpj", "Consulta de CNPJ em lote: envie planilha, CSV ou TXT e receba porte, ramo de atuação e situação cadastral.",
     ["Web", "OpenCNPJ", "CNPJá"], "app web", True),
    ("pipeline-medallion-duckdb", "Pipeline de dados nas camadas bronze, silver e gold com DuckDB e SQL.",
     ["Python", "DuckDB", "SQL"], "dados", True),
    ("pedidos-clean-architecture", "Módulo de pedidos organizado em Clean Architecture.",
     ["Python", "Arquitetura"], "", False),
    ("job-queue-lib", "Fila de tarefas com threads, prioridades e retentativas com backoff.",
     ["Python", "threading"], "", False),
    ("data-quality-checks", "Mini-framework de qualidade de dados configurável por JSON.",
     ["Python", "JSON"], "", False),
    ("api-biblioteca", "API REST de biblioteca: livros e empréstimos.",
     ["FastAPI", "Pydantic", "Docker"], "", False),
    ("gerenciador-financeiro", "Controle financeiro pessoal em linha de comando com SQLite.",
     ["Python", "SQLite"], "", False),
    ("calculadora-cli", "Calculadora de expressões em linha de comando, sem usar eval.",
     ["Python", "ast"], "", False),
    ("todo-cli", "Gerenciador de tarefas em linha de comando com persistência em JSON.",
     ["Python", "JSON"], "", False),
    ("conversor-unidades", "Conversor de comprimento, massa, volume e temperatura.",
     ["Python"], "", False),
]


def chips(tecnologias, x, y):
    partes = []
    for tec in tecnologias:
        largura = 14 + len(tec) * 7
        partes.append(
            f'<rect x="{x}" y="{y}" width="{largura}" height="22" rx="11" fill="{MARINHO}" stroke="{MARINHO2}"/>'
            f'<text x="{x + largura / 2}" y="{y + 15}" text-anchor="middle" class="chip">{escape(tec)}</text>'
        )
        x += largura + 8
    return "".join(partes)


def card(nome, descricao, tecnologias, selo, destaque, indice):
    l, a = (420, 190) if destaque else (420, 150)
    linhas = textwrap.wrap(descricao, 54)[: 3 if destaque else 2]
    atraso = indice * 0.35
    desc = "".join(
        f'<text x="24" y="{78 + i * 20}" class="desc">{escape(linha)}</text>' for i, linha in enumerate(linhas)
    )
    selo_svg = ""
    if selo:
        ls = 18 + len(selo) * 7
        selo_svg = (
            f'<rect x="{l - ls - 20}" y="22" width="{ls}" height="22" rx="11" fill="{VERDE_ESCURO}" stroke="{VERDE2}"/>'
            f'<text x="{l - ls / 2 - 20}" y="37" text-anchor="middle" class="selo">{escape(selo)}</text>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{l}" height="{a}" viewBox="0 0 {l} {a}" role="img" aria-label="{escape(nome)}">
<title>{escape(nome)}: {escape(descricao)}</title>
<defs>
  <linearGradient id="fundo" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{PRETO}"/><stop offset="1" stop-color="#071a14"/>
  </linearGradient>
  <linearGradient id="borda" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VERDE}"/><stop offset=".5" stop-color="{MARINHO2}"/><stop offset="1" stop-color="{VERDE}"/>
  </linearGradient>
  <linearGradient id="brilho" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VERDE}" stop-opacity="0"/><stop offset=".5" stop-color="{VERDE}" stop-opacity=".14"/><stop offset="1" stop-color="{VERDE}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="c"><rect width="{l}" height="{a}" rx="16"/></clipPath>
</defs>
<style>
  .titulo {{ font: 700 19px {MONO}; fill: {VERDE}; }}
  .desc {{ font: 400 13.5px {FONTE}; fill: {TEXTO}; }}
  .chip {{ font: 600 11px {FONTE}; fill: #bfdbfe; }}
  .selo {{ font: 700 11px {FONTE}; fill: {VERDE}; }}
  .link {{ font: 600 12px {FONTE}; fill: {APAGADO}; }}
  .entra {{ animation: entra .8s ease-out {atraso:.2f}s backwards; }}
  .varre {{ animation: varre 5s ease-in-out {atraso:.2f}s infinite; }}
  .contorno {{ stroke-dasharray: 60 22; animation: corre 6s linear infinite; }}
  .pisca {{ animation: pisca 1.6s ease-in-out infinite; }}
  @keyframes entra {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes varre {{ 0% {{ transform: translateX(-{l}px); }} 60%, 100% {{ transform: translateX({l}px); }} }}
  @keyframes corre {{ to {{ stroke-dashoffset: -164; }} }}
  @keyframes pisca {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; opacity: 1 !important; }} }}
</style>
<g clip-path="url(#c)">
  <rect width="{l}" height="{a}" fill="url(#fundo)"/>
  <rect class="varre" width="{l}" height="{a}" fill="url(#brilho)"/>
  <rect x="0" y="0" width="5" height="{a}" fill="{VERDE}" opacity=".85"/>
</g>
<rect class="contorno" x="1" y="1" width="{l - 2}" height="{a - 2}" rx="15" fill="none" stroke="url(#borda)" stroke-width="1.5" opacity=".55"/>
<g class="entra">
  <circle class="pisca" cx="30" cy="34" r="4" fill="{VERDE}"/>
  <text x="44" y="40" class="titulo">{escape(nome)}</text>
  {selo_svg}
  {desc}
  {chips(tecnologias, 24, a - 40)}
  <text x="{l - 24}" y="{a - 24}" text-anchor="end" class="link">ver repositório →</text>
</g>
</svg>'''
    (SAIDA / f"card-{nome}.svg").write_text(svg, encoding="utf-8")


def cabecalho():
    l, a = 900, 300
    papeis = ["Engenharia de Software", "Engenharia de Dados", "Python · AWS · SQL", "Automação e Integrações"]
    n = len(papeis)
    ciclo = n * 3
    rotativos = []
    for i, papel in enumerate(papeis):
        rotativos.append(
            f'<text x="60" y="196" class="papel" style="animation-delay:{i * 3}s">&gt; {escape(papel)}<tspan class="cursor">_</tspan></text>'
        )
    # grade de pontos ao fundo
    pontos = "".join(
        f'<circle cx="{x}" cy="{y}" r="1.2" fill="{VERDE}" opacity=".18"/>'
        for x in range(500, 900, 26) for y in range(20, 300, 26)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{l}" height="{a}" viewBox="0 0 {l} {a}" role="img" aria-label="Walyson Santos Costa">
<title>Walyson Santos Costa: Engenharia de Software e Dados</title>
<defs>
  <linearGradient id="fundo" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{PRETO}"/><stop offset=".6" stop-color="#04140e"/><stop offset="1" stop-color="{MARINHO}"/>
  </linearGradient>
  <linearGradient id="nome" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VERDE}"/><stop offset=".55" stop-color="#6ee7b7"/><stop offset="1" stop-color="#60a5fa"/>
  </linearGradient>
  <radialGradient id="aura"><stop offset="0" stop-color="{VERDE}" stop-opacity=".35"/><stop offset="1" stop-color="{VERDE}" stop-opacity="0"/></radialGradient>
  <radialGradient id="aura2"><stop offset="0" stop-color="{MARINHO2}" stop-opacity=".55"/><stop offset="1" stop-color="{MARINHO2}" stop-opacity="0"/></radialGradient>
  <clipPath id="c"><rect width="{l}" height="{a}" rx="22"/></clipPath>
</defs>
<style>
  .ola {{ font: 600 16px {MONO}; fill: {APAGADO}; }}
  .nome {{ font: 800 50px {FONTE}; fill: url(#nome); letter-spacing: -1px; }}
  .papel {{ font: 600 22px {MONO}; fill: {VERDE}; opacity: 0; animation: troca {ciclo}s infinite; }}
  .cursor {{ animation: cursor 1s steps(1) infinite; }}
  .rodape {{ font: 500 14px {FONTE}; fill: {APAGADO}; }}
  .entra {{ animation: entra 1s cubic-bezier(.2,.8,.2,1) backwards; }}
  .entra2 {{ animation: entra 1s cubic-bezier(.2,.8,.2,1) .25s backwards; }}
  .entra3 {{ animation: entra 1s cubic-bezier(.2,.8,.2,1) .5s backwards; }}
  .flutua {{ animation: flutua 9s ease-in-out infinite; }}
  .flutua2 {{ animation: flutua 12s ease-in-out -4s infinite reverse; }}
  .onda {{ animation: onda 8s linear infinite; }}
  .gira {{ transform-origin: 760px 150px; animation: gira 30s linear infinite; }}
  @keyframes entra {{ from {{ opacity: 0; transform: translateX(-18px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes troca {{ 0% {{ opacity: 0; transform: translateY(10px); }} 4%, {100 / n - 4:.1f}% {{ opacity: 1; transform: none; }} {100 / n:.1f}%, 100% {{ opacity: 0; transform: translateY(-10px); }} }}
  @keyframes cursor {{ 50% {{ opacity: 0; }} }}
  @keyframes flutua {{ 0%, 100% {{ transform: translate(0, 0); }} 50% {{ transform: translate(-40px, 25px); }} }}
  @keyframes onda {{ to {{ transform: translateX(-450px); }} }}
  @keyframes gira {{ to {{ transform: rotate(360deg); }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .entra, .entra2, .entra3 {{ opacity: 1; }} .papel:first-of-type {{ opacity: 1; }} }}
</style>
<g clip-path="url(#c)">
  <rect width="{l}" height="{a}" fill="url(#fundo)"/>
  {pontos}
  <circle class="flutua" cx="760" cy="90" r="190" fill="url(#aura)"/>
  <circle class="flutua2" cx="640" cy="280" r="200" fill="url(#aura2)"/>
  <g class="gira" fill="none" stroke-width="1.5">
    <circle cx="760" cy="150" r="96" stroke="{VERDE}" stroke-opacity=".45" stroke-dasharray="4 10"/>
    <circle cx="760" cy="150" r="66" stroke="#3b82f6" stroke-opacity=".5" stroke-dasharray="40 16"/>
    <circle cx="856" cy="150" r="5" fill="{VERDE}" stroke="none"/>
  </g>
  <text x="760" y="166" text-anchor="middle" style="font: 800 44px {MONO}; fill: {VERDE};">&lt;/&gt;</text>
  <g class="onda">
    <path d="M0 270 Q 56 250 112 270 T 225 270 T 337 270 T 450 270 T 562 270 T 675 270 T 787 270 T 900 270 T 1012 270 T 1125 270 T 1237 270 T 1350 270 V 300 H 0 Z" fill="{VERDE}" opacity=".10"/>
    <path d="M0 282 Q 56 266 112 282 T 225 282 T 337 282 T 450 282 T 562 282 T 675 282 T 787 282 T 900 282 T 1012 282 T 1125 282 T 1237 282 T 1350 282 V 300 H 0 Z" fill="#3b82f6" opacity=".12"/>
  </g>
</g>
<rect x="1" y="1" width="{l - 2}" height="{a - 2}" rx="21" fill="none" stroke="{VERDE}" stroke-opacity=".25"/>
<text x="60" y="84" class="ola entra">// olá, eu sou</text>
<text x="58" y="142" class="nome entra2">Walyson Santos</text>
<g class="entra3">{"".join(rotativos)}</g>
<text x="60" y="236" class="rodape entra3">Santo André, SP · UFABC · construindo sistemas que aguentam o tranco</text>
</svg>'''
    (SAIDA / "header.svg").write_text(svg, encoding="utf-8")


def divisor():
    l, a = 900, 24
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{l}" height="{a}" viewBox="0 0 {l} {a}">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{VERDE}" stop-opacity="0"/><stop offset=".5" stop-color="{VERDE}"/><stop offset="1" stop-color="{VERDE}" stop-opacity="0"/></linearGradient></defs>
<style>.p {{ animation: p 4s ease-in-out infinite; }} @keyframes p {{ 0% {{ transform: translateX(-300px); }} 100% {{ transform: translateX(900px); }} }} @media (prefers-reduced-motion: reduce) {{ .p {{ animation: none; }} }}</style>
<rect x="0" y="11" width="{l}" height="2" fill="{MARINHO2}" opacity=".5"/>
<rect class="p" x="0" y="10" width="300" height="4" rx="2" fill="url(#g)"/>
</svg>'''
    (SAIDA / "divisor.svg").write_text(svg, encoding="utf-8")


cabecalho()
divisor()
for i, projeto in enumerate(PROJETOS):
    card(*projeto, indice=i % 2)
print("ok:", len(list(SAIDA.glob("*.svg"))), "SVGs")
