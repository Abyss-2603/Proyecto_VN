# 1. DECLARAMOS LAS IMÁGENES A TAMAÑO COMPLETO
# La galería necesita saber qué imagen abrir en grande cuando el jugador hace clic.
image cg1_full = "images/escritorioPC/galeria/cuarto_destrozado.png"
image cg2_full = "images/escritorioPC/galeria/ojo.png"
image cg3_full = "images/escritorioPC/galeria/pastillas.png"
image cg4_full = "images/escritorioPC/galeria/imagen_infancia.png"

# Relleno para las imágenes que aún no tienes
image cg5_full = Solid("#000000")
image cg6_full = Solid("#000000")
image cg7_full = Solid("#000000")
image cg8_full = Solid("#000000")

# 2. CONFIGURAMOS LA GALERÍA
init python:
    g = Gallery()

    g.locked_button = "images/menus/boton_block.png"
    g.transition = dissolve

    # --- HUECO 1 ---
    g.button("cg1")
    g.condition("persistent.cg1_desbloqueada") 
    g.image("cg1_full") # Muestra esta imagen a pantalla completa

    # --- HUECO 2 ---
    g.button("cg2")
    g.condition("persistent.cg2_desbloqueada")
    g.image("cg2_full")

    # --- HUECO 3 ---
    g.button("cg3")
    g.condition("persistent.cg3_desbloqueada")
    g.image("cg3_full")

    # --- HUECO 4 ---
    g.button("cg4")
    g.condition("persistent.cg4_desbloqueada")
    g.image("cg4_full")

    # --- HUECO 5 ---
    g.button("cg5")
    g.condition("persistent.cg5_desbloqueada")
    g.image("cg5_full")

    # --- HUECO 6 ---
    g.button("cg6")
    g.condition("persistent.cg6_desbloqueada")
    g.image("cg6_full")

    # --- HUECO 7 ---
    g.button("cg7")
    g.condition("persistent.cg7_desbloqueada")
    g.image("cg7_full")

    # --- HUECO 8 ---
    g.button("cg8")
    g.condition("persistent.cg8_desbloqueada")
    g.image("cg8_full")