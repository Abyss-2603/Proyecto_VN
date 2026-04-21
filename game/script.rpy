
# -- VARIABLES del Menú
image fondo_video_menu = Movie(play="images/menus/menu_animado.webm", loop=True)

#Galería con imagen de block
image imagenBloqueada:
    "images/menus/boton_block.png"
    on hover:
        "images/menus/boton_block_seleccionado.png"
    on idle:
        "images/menus/boton_block.png"

# --- Variables de Usuario ---
default persistent.user_id = None
default persistent.nombre_jugador = None

# --- Variables de los Formularios ---
default pc_usuario = ""
default pc_email = ""
default pc_pass = ""
default pc_pass_confirm = ""
default pc_codigo = ""
default pc_nueva_pass = ""
default pc_nueva_pass_confirm = ""

# --- Variables de Mensajes y Control ---
default registro_completado = False
default login_msg = ""
default registro_msg = ""
default recuperacion_msg = ""
default fase_recuperacion = 1

# Pantalla inicial de aviso legal
label splashscreen:
    call screen aviso_legal
    pause 0.4

    if not persistent.user_id:
        call screen inicio_sesion_pc

    return

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
    # El jugador ha confirmado empezar la partida    



    # Aquí sigue el juego normal...
