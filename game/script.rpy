
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

default capitulo_actual = "prologo"

# --- Variables de los Formularios ---
default pc_usuario = ""
default pc_email = ""
default pc_pass = ""
default pc_pass_confirm = "" # para resto de pantallas del login
default pc_codigo = ""
default pc_nueva_pass = ""
default pc_confirm_pass = "" # para la parte de recuperar contraseña y cambiarla 
default ver_password = False

# --- Variables de Mensajes y Control ---
default registro_completado = False
default login_msg = ""
default registro_msg = ""
default recuperacion_msg = ""
default fase_recuperacion = 1

# Pantalla inicial de aviso legal
label splashscreen:
    call screen aviso_legal
    pause 0.2

    if not persistent.user_id:
        scene black with fade    
        play sound "Musica/Efectos/pc_enciende_1.mp3" 
        pause 8.0
        play music "Musica/Efectos/pc_enciende_2.ogg" loop
        
        jump menu_login_loop

    stop music fadeout 1.5
    return

label ejecutar_borrado_cuenta:
    scene black with fade
    pause 1.0
    python:
        exito = borrar_cuenta_api(persistent.user_id)
        if exito:
            persistent.user_id = None
            persistent.nombre_jugador = None
            renpy.save_persistent()

            pc_email = ""
            pc_usuario = ""
            pc_pass = ""
            renpy.store.capitulo_actual = "prologo"
            renpy.store.stress_level = 0
            renpy.store.decisiones_tomadas = {}

    if exito:
        "Tu existencia ha sido purgada de los servidores."
        "El ciclo se ha roto."
    else:
        "Hubo un error al intentar borrar tus datos. Tus lazos aún persisten."
    $ Quit(confirm=False)()

# ==========================================
# RUTAS DE PANTALLAS SEGURAS
# ==========================================
label menu_login_loop:
    call screen inicio_sesion_pc
    return

label menu_registro_loop:
    call screen registro_pc
    return

label menu_recuperacion_loop:
    call screen recuperacion
    return

# ==========================================
# SALAS DE ESPERA (Cartel de Carga)
# ==========================================
label procesar_login:
    show screen cargando_servidor
    with None # <--- Obliga a Ren'Py a dibujar el cartel AL INSTANTE
    $ renpy.pause(0.1, hard=True)

    python:
        conectar_login(pc_usuario, pc_pass)
        
    hide screen cargando_servidor
    with None # <--- Obliga a borrarlo al instante

    if persistent.user_id:
        jump start
    else:
        jump menu_login_loop

label procesar_registro:
    show screen cargando_servidor
    with None 
    $ renpy.pause(0.1, hard=True)

    python:
        conectar_registro(pc_usuario, pc_email, pc_pass)
        
    hide screen cargando_servidor
    with None

    if pc_pass == "":
        jump menu_login_loop
    else:
        jump menu_registro_loop

label procesar_solicitar_codigo:
    show screen cargando_servidor
    with None 
    $ renpy.pause(0.1, hard=True)

    python:
        solicitar_codigo_api(pc_email)
        
    hide screen cargando_servidor
    with None
    jump menu_recuperacion_loop

label procesar_cambio_pass:
    show screen cargando_servidor
    with None 
    $ renpy.pause(0.1, hard=True)

    python:
        confirmar_nueva_password_api(pc_email, pc_codigo, pc_nueva_pass)
        
    hide screen cargando_servidor
    with None
    
    if fase_recuperacion == 1:
        jump menu_login_loop
    else:
        jump menu_recuperacion_loop

label start:
    # El jugador ha confirmado empezar la partida    

    $ default_mouse = "pc_normal"

    $ quick_menu = False

    call screen escritorio_pc

    $ defaultmouse = "default"
    "He apagado el ordenador. La pantalla se vuelve negra..."
    return