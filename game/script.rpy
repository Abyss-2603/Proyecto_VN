
# -- VARIABLES del Menú
image fondo_video_menu = Movie(play="images/menus/menu_animado.webm", loop=True)

#Galería con imagen de block
image imagenBloqueada:
    "images/menus/boton_block.png"
    on hover:
        "images/menus/boton_block_seleccionado.png"
    on idle:
        "images/menus/boton_block.png"

# variable del fondo de escritorio
image fondo_escritorio_pc = im.Scale("images/escritorioPC/fondo_escritorio.png", 1920, 1080)

# --- Variables de Usuario ---
default persistent.user_id = None
default persistent.nombre_jugador = None

default capitulo_actual = "prologo"
default decisiones_tomadas = {}

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
        call screen inicio_sesion_pc with Dissolve(1.5)

        stop music fadeout 1.5
    return

# PONER MUSICA DE FONDO DESPUES DEL MENU DE LOGIN (EN options.rpy)

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
            renpy.store.decisiones_tomadas = {}

    if exito:
        "Tu existencia ha sido purgada de los servidores."
        "El ciclo se ha roto."
    else:
        "Hubo un error al intentar borrar tus datos. Tus lazos aún persisten."
    $ Quit(confirm=False)()

# --- VARIABLES DEL REPRODUCTOR DE MÚSICA ---
default indice_cancion = 0 # para saber qué cancion se está escuchando
default cancion_actual = ""
default artista_actual = ""
default musica_pausada = False

init python:

    lista_canciones = [
        {"titulo": "Lofi Chill Vibes", "autor": "DJ Relax", "ruta": "Musica/Efectos/cancion1.ogg"},
        {"titulo": "Synthwave City", "autor": "Neon M", "ruta": "Musica/Efectos/cancion2.ogg"},
        {"titulo": "Acústica Relax", "autor": "Guitar Girl", "ruta": "Musica/Efectos/cancion3.ogg"},
        {"titulo": "Canción del PC", "autor": "¿Quién sabe?", "ruta": "Musica/Efectos/pc_enciende_1.ogg"},
        {"titulo": "Canción del PC2", "autor": "¿Quién sabe?", "ruta": "Musica/Efectos/pc_enciende_2.ogg"}
    ]

    def reproducir_pista():
        global indice_cancion, cancion_actual, artista_actual, musica_pausada
        
        pista = lista_canciones[indice_cancion]
        
        renpy.store.cancion_actual = pista["titulo"]
        renpy.store.artista_actual = pista["autor"]
        renpy.store.musica_pausada = False
        
        renpy.music.play(pista["ruta"], channel="music", loop=True)
        renpy.restart_interaction()

    # FUNCIÓN PARA PASAR A LA SIGUIENTE CANCIÓN
    def siguiente_cancion():
        global indice_cancion
        indice_cancion = (indice_cancion + 1) % len(lista_canciones)
        reproducir_pista()

    # FUNCIÓN PARA VOLVER A LA CANCIÓN ANTERIOR
    def anterior_cancion():
        global indice_cancion
        indice_cancion = (indice_cancion - 1) % len(lista_canciones)
        reproducir_pista()


# --- Variables para chat y mensajes ---
default mensajes_nuevos = False

# El chat empieza con mensajes de ella
default historial_mensajes = [
    ("Rocío", "¡Por fin te conectas! ¿Estás dentro del ordenador?")
]

# Las opciones que el jugador podrá elegir al abrir el chat
default respuestas_disponibles = [
    ("Sí, acabo de entrar. ¿Acaso me espías o qué?", "chat_nodo_1"),
    ("¿Tú qué crees? Si me he conectado por algo será", "chat_nodo_2")
]

# Lógica de chat
init python:

    def recibir_mensaje(remitente, texto):
        store.historial_mensajes.append((remitente, texto))
        
        if not store.apps_pc["chat"]["abierta"] or store.apps_pc["chat"]["minimizada"]:
            store.mensajes_nuevos = True
            renpy.sound.play("Musica/Efectos/notificacion.ogg")
            renpy.notify("Nuevo mensaje de: " + remitente)

    def enviar_respuesta_chat(texto_elegido, etiqueta_destino):
        # Añadir mensajes según elección
        store.historial_mensajes.append(("Yo", texto_elegido))
        # Ocultar botones
        store.respuestas_disponibles = []
        # Finalizar pantalla para que la historia avance
        renpy.end_interaction(None)

        renpy.jump(etiqueta_destino)

# Lista de rutas de las imagenes de galeria
default lista_fotos = [
    "images/escritorioPC/fondo_escritorio.png",
    "images/escritorioPC/icono_chica.png"
]

label start:
    # El jugador ha confirmado empezar la partida    
    $ default_mouse = "pc_normal"
    $ quick_menu = False

    # Introducción, prota hablando
    scene black with fade
    "Por fin en casa, ya estaba cansado de las clases de hoy."
    "Menos mal que mañana ya terminan los exámenes, al fin descansaré y me pondré a jugar toda la semana."
    "Voy a ponerme un rato con el pc..."
    window hide
    
    # Aquí mostramos la IMAGEN del fondo, no la pantalla. 
    scene fondo_escritorio_pc   
    with fade 

    pause 2.0

    # Usamos el sonido y la notificación iniciales a mano para arrancar el juego
    play sound "Musica/Efectos/notificacion.ogg"
    $ mensajes_nuevos = True
    $ renpy.notify("Nuevo mensaje de: Roxy26")
    
    # Como es una imagen normal, el jugador podrá hacer clic para leer esto sin problemas
    "Vaya, ha sido encender el pc y ya me está escribiendo Rocío xD."
    "Le contestaré ahora a ver qué quiere."
    window hide 
    
    # lanzamos el ordenador 
    jump bucle_pc

label bucle_pc:
    call screen escritorio_pc 
    $ default_mouse = "pc_normal"
    
    scene black with fade
    "He apagado el ordenador. La pantalla se vuelve negra..."
    return

label chat_nodo_1:
    show screen escritorio_pc #añadir en cada nodo 
    
    $ renpy.pause(1.5, hard=True)
    $ recibir_mensaje("Rocío", "Jajaja ya sabes cuánto me aburro. Ha sido verte conectado y quería molestarte un poco.")
    
    $ renpy.pause(1.0, hard=True)
    $ historial_mensajes.append(("Yo", "Hmmmmm muy graciosa."))
    
    $ renpy.pause(1.0, hard=True)
    $ recibir_mensaje("Rocío", "Oye, quería preguntarte por los exámenes. ¿Cómo los llevas? No pude preguntarte esta mañana.")
    
    $ renpy.pause(1.0, hard=True)
    $ historial_mensajes.append(("Yo", "¿Los exámenes? Bueno, creo que están aprobados, quería quitármelos de encima lo antes posible para tener libertad al fin."))
    
    $ renpy.pause(1.5, hard=True)
    $ recibir_mensaje("Rocío", "Ya, te entiendo perfectamente. Yo estoy que me subo por las paredes con el de historia...")

    # NUEVAS RESPUESTAS 
    $ respuestas_disponibles = [
        ("Tranquila, seguro que lo sacas sin problemas.", "chat_nodo_apoyo"),
        ("Pues haber estudiado más, que eres una vaga.", "chat_nodo_borde")
    ]

    # VOLVEMOS AL ESCRITORIO 
    jump bucle_pc