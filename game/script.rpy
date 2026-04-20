# Coloca el código de tu juego en este archivo.

# Pantalla inicial de aviso legal
label splashscreen:
    
    call screen aviso_legal
    pause 0.4

    return

# -- VARIABLES del Menú
image fondo_video_menu = Movie(play="images/menus/menu_animado.webm", loop=True)

# --- VARIABLES de Inicio de Sesión y Registro ---
default pc_usuario = ""
default pc_email = ""
default pc_pass = ""
default pc_pass_confirm = ""

default registro_completado = False

#Galería con imagen de block
image imagenBloqueada:
    "images/menus/boton_block.png"
    on hover:
        "images/menus/boton_block_seleccionado.png"
    on idle:
        "images/menus/boton_block.png"

label ejecutar_borrado_cuenta:
    python:
        exito = borrar_cuenta_api(persistent.user_id)
        
        if exito:
            persistent.user_id = None
            persistent.nombre_jugador = None
            renpy.store.capitulo_actual = "prologo"
            renpy.store.stress_level = 0
            renpy.store.decisiones_tomadas = {}
            
    # Reinicio del juego a la fuerza (vuelve al splashscreen)
    $ renpy.full_restart()

label start:
    # Llamada pantalla registro
    # Iniciar Variables de registro
    python:
        if not hasattr(store, 'pc_usuario'): store.pc_usuario = ""
        if not hasattr(store, 'pc_email'): store.pc_email = ""
        if not hasattr(store, 'pc_pass'): store.pc_pass = ""
        if not hasattr(store, 'pc_pass_confirm'): store.pc_pass_confirm = ""
    call screen registro_pc 


    # Aquí sigue el juego normal...
