"""Constantes visuais compartilhadas da GUI (cores, fontes e dimensões).

Tema escuro do Compasso. Três paletas estão disponíveis (Teal/Iris/Amber); a paleta
ativa é escolhida por `C` — trocar essa única linha recolore toda a interface. As
constantes semânticas (WIN_BG, ACCENT, TEXT...) derivam de `C` e são importadas pelos
frames e helpers, evitando repetir cores em cada módulo.
"""

# ---------------------------------------------------------------------------
# Paletas (dicionários de cores semânticas)
# ---------------------------------------------------------------------------

# Paleta 2a — Teal (padrão)
PALETTE_TEAL = {
    "win_bg":        "#0E1116",   # fundo da janela
    "bar_bg":        "#161B22",   # barra de título / menu / cartões
    "footer_bg":     "#12161C",   # rodapé
    "border":        "#21262d",   # bordas de cartões e campos
    "border_win":    "#262c36",   # borda externa da janela / placeholder
    "input_bg":      "#0E1116",   # fundo de campos e botões secundários

    "text":          "#E6EDF3",   # texto principal
    "muted":         "#8B949E",   # texto secundário
    "faint":         "#6E7681",   # rótulos / caption
    "faint2":        "#4B525C",   # números apagados (/12)

    "accent":        "#2DD4BF",   # acento (teal)
    "accent_ink":    "#04120F",   # texto sobre o acento
    "accent_tint":   "#0C2B28",   # fundo tênue do acento (badges, chips)
    "accent_border": "#14463F",   # borda do pill conectado

    "success":       "#34D399",   # ponto "conectado" / checks
    "danger":        "#F87171",   # gravando / parar
    "danger_tint":   "#2A1515",
    "danger_border": "#7F2D2D",
}

PALETTE_IRIS = {
    "win_bg":        "#0E0F17", 
    "bar_bg":        "#171826", 
    "footer_bg":     "#131324",
    "border":        "#262838", 
    "border_win":    "#2A2C40", 
    "input_bg":      "#0E0F17",

    "text":          "#E7E7F5", 
    "muted":         "#9A9BB5", 
    "faint":         "#6F6F8C", 
    "faint2":        "#4D4D68",

    "accent":        "#7C74FF", 
    "accent_ink":    "#0C0A24", 
    "accent_tint":   "#1E1C3D",
    "accent_border": "#322F5C", 

    "success":       "#4ADE80",
    "danger":        "#FB7185", 
    "danger_tint":   "#2A1620", 
    "danger_border": "#7A2E46",
}

PALETTE_AMBER = {
    "win_bg":        "#14120C", 
    "bar_bg":        "#1C1A12", 
    "footer_bg":     "#191710",
    "border":        "#2B271A", 
    "border_win":    "#2F2B1C", 
    "input_bg":      "#14120C",

    "text":          "#F2EEE2", 
    "muted":         "#B3A98F", 
    "faint":         "#837B64", 
    "faint2":        "#5C5540",

    "accent":        "#F5A524",
    "accent_ink":    "#241A04", 
    "accent_tint":   "#2E2410",
    "accent_border": "#4A3D1C", 
    
    "success":       "#8CC63F",
    "danger":        "#F87171", 
    "danger_tint":   "#2A1A12", 
    "danger_border": "#7A3F2D",
}

# >>> Paleta ativa (troque por PALETTE_IRIS ou PALETTE_AMBER para recolorir tudo) <<<
C = PALETTE_TEAL

# ---------------------------------------------------------------------------
# Constantes semânticas de cor (derivadas da paleta ativa)
# ---------------------------------------------------------------------------
WIN_BG: str = C["win_bg"]
BAR_BG: str = C["bar_bg"]
FOOTER_BG: str = C["footer_bg"]
BORDER: str = C["border"]
BORDER_WIN: str = C["border_win"]
INPUT_BG: str = C["input_bg"]

TEXT: str = C["text"]
MUTED: str = C["muted"]
FAINT: str = C["faint"]
FAINT2: str = C["faint2"]

ACCENT: str = C["accent"]
ACCENT_INK: str = C["accent_ink"]
ACCENT_TINT: str = C["accent_tint"]
ACCENT_BORDER: str = C["accent_border"]

SUCCESS: str = C["success"]
DANGER: str = C["danger"]
DANGER_TINT: str = C["danger_tint"]
DANGER_BORDER: str = C["danger_border"]

TRANSPARENTE: str = "transparent"

# ---------------------------------------------------------------------------
# Dimensões / layout
# ---------------------------------------------------------------------------
WIN_MIN_WIDTH: int = 1120
WIN_MIN_HEIGHT: int = 760
CORNER: int = 14          # raio dos cartões
CORNER_SM: int = 9        # raio de campos/botões

# Atalho de sticky usado com frequência
NSE: str = "nse"

# ---------------------------------------------------------------------------
# Fontes
# ---------------------------------------------------------------------------
import sys as _sys

if _sys.platform == "darwin":
    DISPLAY_FAMILY, MONO_FAMILY = "SF Pro Display", "Menlo"
elif _sys.platform.startswith("win"):
    DISPLAY_FAMILY, MONO_FAMILY = "Segoe UI", "Consolas"
else:
    DISPLAY_FAMILY, MONO_FAMILY = "DejaVu Sans", "DejaVu Sans Mono"

BASE_FONT: tuple = (DISPLAY_FAMILY, 16, "bold")
BASE_FONT_MED: tuple = (DISPLAY_FAMILY, 14, "bold")
BASE_FONT_MIN: tuple = (DISPLAY_FAMILY, 12, "bold")
