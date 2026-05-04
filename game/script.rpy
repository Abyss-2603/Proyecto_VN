
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
default persistent.nube_capitulo = None     
default persistent.nube_decisiones = {}     

default capitulo_actual = "prologo"
default decisiones_tomadas = {}

# Variable de notas
default nota_1_descifrada = False

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

            persistent.nube_capitulo = None
            persistent.nube_decisiones = {}

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
    ("¿Tú qué crees? Si aparezco conectado será por algo", "chat_nodo_2")
]

# Boton para finalizar la noche en el chat
default mostrar_boton_finalizar = False

# Lógica de chat
init python:
    def recibir_mensaje(remitente, texto):
        store.historial_mensajes.append((remitente, texto))

        renpy.restart_interaction() 
        
        if not store.apps_pc["chat"]["abierta"] or store.apps_pc["chat"]["minimizada"]:
            store.mensajes_nuevos = True
            renpy.sound.play("Musica/Efectos/notificacion.ogg")
            renpy.notify("Nuevo mensaje de: " + remitente)

    def recibir_imagen(remitente, ruta_imagen, texto_chat="[Imagen adjunta]"):
        if ruta_imagen not in store.lista_fotos:
            store.lista_fotos.append(ruta_imagen)
        store.historial_mensajes.append((remitente, texto_chat))    

        store.ajuste_scroll_chat.value = 99999 
        renpy.restart_interaction()   
        
        if not store.apps_pc["chat"]["abierta"] or store.apps_pc["chat"]["minimizada"]:
            store.mensajes_nuevos = True
            renpy.sound.play("Musica/Efectos/notificacion_mensajes.mp3")
            renpy.notify("Nueva imagen de: " + remitente)

    # Función para recibir texto
    def enviar_respuesta_chat(texto_elegido, etiqueta_destino):
        store.historial_mensajes.append(("Yo", texto_elegido))
        store.respuestas_disponibles = []
        renpy.end_interaction(None)

        renpy.jump(etiqueta_destino)
    

# Lista de rutas de las imagenes de galeria
default lista_fotos = [
    "images/escritorioPC/fondo_escritorio.png",
    "images/escritorioPC/icono_chica.png"
]

label start:

    if persistent.nube_capitulo:
        $ capitulo_actual = persistent.nube_capitulo
        $ decisiones_tomadas = persistent.nube_decisiones

    $ default_mouse = "pc_normal"
    $ quick_menu = False

    # SALTO DE CAPÍTULO
    if capitulo_actual != "prologo" and capitulo_actual != "":
        jump expression capitulo_actual

    scene black with fade

    play sound "Musica/Efectos/sonido_tecleando.ogg" loop volume 0.8
    "Por fin en casa, ya estaba cansado de las clases de hoy."
    "Menos mal que mañana ya terminan los exámenes, al fin puedo descansar!!."
    "Voy a ponerme un rato con el pc..."
    stop sound fadeout 1.0
    window hide
    play sound "Musica/Efectos/sonido_inicioSistema.ogg"

    scene fondo_escritorio_pc
    with fade

    pause 2.0

    # notificacion de rocio al iniciar el escritorio
    play sound "Musica/Efectos/notificacion_mensajes.mp3"
    $ mensajes_nuevos = True
    $ renpy.notify("Nuevo mensaje de: Roxy26")
    
    "Vaya, ha sido encender el pc y ya me está escribiendo Rocío."
    "Le contestaré a ver qué quiere esta pesada."
    "Aunque antes creo que pondré algo de música de mientras para que no esté todo tan soso."
    $ reproducir_pista()
    window hide
    
    # lanzamos el ordenador 
    jump bucle_pc

label bucle_pc:
    call screen escritorio_pc 
    $ default_mouse = "pc_normal"
    
    scene black with fade
    "He apagado el ordenador. La pantalla se vuelve negra..."
    return

# Opciones: "pc", "dia_normal", "dia_tetrico"
default estilo_interfaz = "pc"

label chat_nodo_1:
    pause 1.5
    $ recibir_mensaje("Rocío", "Jajaja ya sabes cuánto me aburro. Ha sido verte conectado y quería molestarte un poco.")
    $ recibir_mensaje("Yo", "Hmmmm muy graciosa.")
    
    pause 1.0
    $ recibir_mensaje("Rocío", "Oye, quería preguntarte por los exámenes. ¿Cómo los llevas? No pude preguntarte esta mañana.")
    pause 1.5
    $ recibir_mensaje("Yo", "¿Los exámenes? Bueno, creo que están aprobados.") 
    pause 1.0
    $ recibir_mensaje("Yo", "Quería quitármelos de encima lo antes posible para ser libre al fin.")
    pause 1.5
    $ recibir_mensaje("Rocío", "Joo, yo creo que voy a suspender alguno que otro. Ojalá tener tu mente privilegiada.")

    # NUEVAS RESPUESTAS 
    $ respuestas_disponibles = [
        ("Eso te pasa por no estudiar ni hacer nada en clase.", "chat_nodo_3"),
        ("Ya te avisé en su momento pero no me hiciste caso...", "chat_nodo_3")
    ]

    # VOLVEMOS AL ESCRITORIO 
    jump bucle_pc

label chat_nodo_2:
    pause 1.5
    $ recibir_mensaje("Rocío", "-_- | Contigo no se puede hablar con ironía no?")
    pause 1.0
    $ recibir_mensaje("Yo", "<_< Estás tú para hablar...")
    
    pause 1.5
    $ recibir_mensaje("Rocío", "Deja de ser tan borde >_<")
    pause 1.0
    $ recibir_mensaje("Rocío", "Oye, quería preguntarte por los exámenes. ¿Cómo los llevas? No pude preguntarte esta mañana.")
    pause 1.5
    $ recibir_mensaje("Yo", "¿Los exámenes? Bueno, creo que están aprobados.") 
    pause 1.0
    $ recibir_mensaje("Yo", "Quería quitármelos de encima lo antes posible para ser libre al fin.")
    pause 1.5
    $ recibir_mensaje("Rocío", "Joo, yo creo que voy a suspender alguno que otro. Ojalá tener tu mente privilegiada.")
    
    # NUEVAS RESPUESTAS 
    $ respuestas_disponibles = [
        ("Eso te pasa por no estudiar ni hacer nada en clase.", "chat_nodo_3"),
        ("Ya te avisé en su momento pero no me hiciste caso...", "chat_nodo_3")
    ]

    # VOLVEMOS AL ESCRITORIO 
    jump bucle_pc

label chat_nodo_3:
    pause 1.5
    $ recibir_mensaje("Rocío", "Lo hecho pecho, supongo que tendré que presentarme a la recuperación.")
    pause 1.5
    $ recibir_mensaje("Rocío", "Mañana es ya el último examen, espero que se me dé mejor que el de hoy :'( ")
    pause 1.5
    $ recibir_mensaje("Yo", "Menos mal que no soy tan vago como tú...")
    pause 1.5
    $ recibir_mensaje("Rocío", "Que si, que si... ya deja de recordarme que no estudié lo suficiente. :< ")
    pause 1.5
    $ recibir_mensaje("Rocío", "Por cierto, ¿viste la foto que te envié esta mañana? ")
    pause 1.5
    $ recibir_mensaje("Yo", "Ehm... Nope")
    pause 1.5
    $ recibir_mensaje("Rocío", "¿¡¿¡¿Como que no?!?!? :O")
    pause 1.5
    $ recibir_mensaje("Rocío", "Te la vuelvo a mandar entonces.")
    pause 1.5
    $ recibir_mensaje("Rocío", "IMG:images/escritorioPC/galeria/imagen_infancia.png")
    pause 1.0
    $ recibir_mensaje("Rocío", "¡¡¿Has visto qué lindos?! Me la pasó mi madre el otro día.")
    pause 1.0
    $ recibir_mensaje("Yo", "¿¡¿¡¿Esos somos nosotros?!?!?")
    pause 1.5
    $ recibir_mensaje("Yo", "No sabía que había una foto nuestra de cuando éramos pequeños.")
    pause 1.5
    $ recibir_mensaje("Rocío", "Yo también me sorprendí ^^")

    window show
    "Vaya, no me esperaba que nuestras madres guardaran una foto de nosotros tan pequeños. Cuánto hemos cambiado la verdad."
    "Me acuerdo de ese día, salimos a dar un paseo por el parque de la urbanización."
    "No recordaba para nada ese momento, pero gracias a esa foto lo recordé todo." 
    window hide
    
    $ recibir_mensaje("Rocío", "Fíjate si hemos cambiado que casi no me reconozco ")
    pause 1.5
    $ recibir_mensaje("Yo", "La verdad es que da para pensar...")
    pause 1.5
    $ recibir_mensaje("Rocío", "Sí, sí... jeje")
    pause 1.5
    $ recibir_mensaje("Rocío", "Por cierto, cambiando de tema... ")
    pause 1.5
    $ recibir_mensaje("Rocío", "¿Quedamos mañana después de clase como siempre no?")
    pause 1.5
    $ recibir_mensaje("Rocío", "Después de los exámenes digo.")
    pause 1.0
    $ recibir_mensaje("Yo", "Ufff no sé...quedar con una pesada como tú puede ser agotador...")
    pause 1.0
    $ recibir_mensaje("Rocío", "(-_-)")
    pause 1.5
    $ recibir_mensaje("Rocío", "Vale vale señor amargado, ojalá te vaya mal el examen de mañana :D")
    pause 1.0
    $ recibir_mensaje("Yo", "Jajajaja")
    pause 1.5
    $ recibir_mensaje("Yo", "Bueno...supongo que no me queda otra que aguantarte.")
    pause 1.5
    $ recibir_mensaje("Yo", "Es broma :D")
    pause 1.0
    $ recibir_mensaje("Yo", "Sisi, mañana como siempre quedamos")
    pause 1.5
    $ recibir_mensaje("Rocío", "Hmmm (-_-) bueno, más te vale")
    pause 1.0
    $ recibir_mensaje("Yo", "Jeje")
    pause 1.5
    $ recibir_mensaje("Rocío", "Te dejo, voy a ver si logro estudiar un poco más.")
    pause 1.5
    $ recibir_mensaje("Yo", "Va, yo también repasaré un poco antes de dormir")
    pause 1.0
    $ recibir_mensaje("Yo", "Buenas noches Zzz")
    pause 1.5
    $ recibir_mensaje("Rocío", "Suerte con eso :3")
    pause 1.5
    $ recibir_mensaje("Rocío", "Espero que aprobemos ambos el examen y podamos celebrarlo")
    pause 1.5
    $ recibir_mensaje("Rocío", "Zzzzzzz")
    
    $ mostrar_boton_finalizar = True

    jump bucle_pc
    
    
label transicion_dia_1:
    hide screen escritorio_pc
    hide screen ventana_chat
    hide screen ventana_nota
    hide screen ventana_galeria
    hide screen ventana_musica
    hide screen ventana_webcam
    
    python:
        for app in apps_pc:
            apps_pc[app]["abierta"] = False
            apps_pc[app]["minimizada"] = False

    window hide
    stop music fadeout 2.0

    scene black with fade
    pause 1.0

    show expression Text("DÍA 1", font="gui/fonts/Micro5.ttf", size=150, color="#ffffff") as cartel_dia:
        xalign 0.5
        yalign 0.5
    with dissolve
    
    pause 3.0
    
    hide cartel_dia with dissolve

    $ capitulo_actual = "dia_1"

    jump dia_1

# Parte diurna 1
label dia_1:
    # Empezamos el día con el marco bonito y floral
    $ estilo_interfaz = "dia_normal"
    $ default_mouse = "cursor_normal"

    # Guardar el estado de la partida
    $ capitulo_actual = "dia_1"
    $ persistent.nube_capitulo = "dia_1" 
    $ guardar_progreso(capitulo_actual, decisiones_tomadas)

    scene fondo_patio:
        xysize(1920, 1080)
        fit "cover"
        align (0.0, 0.0)
    with fade    

    "Rocío" "Hoy hace un día precioso, ¿verdad?"
    "Yo" "Sí, la verdad es que se está muy bien aquí."
    
    "De repente, el cielo se nubló. Rocío dejó de sonreír y se quedó mirando al vacío."
    
    # ¡BUM! CAMBIO DE INTERFAZ Y DE MÚSICA PARA EL SUSTO
    $ estilo_interfaz = "dia_tetrico"
    $ default_mouse = "cursor_normal_terror"
    play music "sonido_terror_estatica.ogg"
    
    "Rocío" "Tú la dejaste morir... ¿Por qué lo hiciste?"
    "Yo" "¿Q-qué estás diciendo...?"
    
    # Y si quieres volver a la normalidad como si hubiera sido una alucinación:
    $ estilo_interfaz = "dia_normal"
    stop music
    
    "Rocío" "¡Eh! ¿Me estás escuchando? Te estaba hablando de los exámenes."