
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
image fondo_escritorio_corrupto = im.Scale("images/escritorioPC/fondo_escritorio_corrupto.png", 1920, 1080)
image fondo_escritorio_corrupto2 = im.Scale("images/escritorioPC/fondo_escritorio_corrupto2.png", 1920, 1080)

# variable de gif
image gif_webcam = Movie(play="images/escritorioPC/webcam_silueta.webm", loop=True)
default contenido_webcam = "negro"

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

# Variables de terror y progresos
default nivel_corrupto = 0
default destino_noche = "transicion_dia_1"

# Boton para finalizar la noche en el chat
default mostrar_boton_finalizar = False

default archivos_explorados = 0
default susto_voces_hecho = False

# variables para la galería
default persistent.cg1_desbloqueada = False
default persistent.cg2_desbloqueada = False
default persistent.cg3_desbloqueada = False
default persistent.cg4_desbloqueada = False
default persistent.cg5_desbloqueada = False
default persistent.cg6_desbloqueada = False
default persistent.cg7_desbloqueada = False
default persistent.cg8_desbloqueada = False

default ruta_visor_actual = "" # Guarda qué foto se está viendo

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

    def enviar_respuesta_chat(texto_elegido, etiqueta_destino):
        store.historial_mensajes.append(("Yo", texto_elegido))
        store.respuestas_disponibles = []
        renpy.end_interaction(None)
        renpy.jump(etiqueta_destino)
    

# --- LÓGICA DEL SISTEMA OPERATIVO ---
init python:
    # Diccionario con apps 
    apps_pc = {
        "nota": {"abierta": False, "minimizada": False, "titulo": "Nota_1.txt"},
        "chat": {"abierta": False, "minimizada": False, "titulo": "Chat"},
        "galeria": {"abierta": False, "minimizada": False, "titulo": "Galería"},
        "musica": {"abierta": False, "minimizada": False, "titulo": "Música"},
        "webcam": {"abierta": False, "minimizada": False, "titulo": "WebCam"},

        "nota_turbia": {"abierta": False, "minimizada": False, "titulo": "LEEME.txt", "contenido": "..."},
        
        # archivos corruptos de la noche 1    
        "nota_corrupta_1": {"abierta": False, "minimizada": False, "titulo": "ayuda.txt", "contenido": "NO PUEDO RESPIRAR", "visible": True},
        "foto_corrupta_1": {"abierta": False, "minimizada": False, "titulo": "cu41t0.jpg", "ruta": "images/escritorioPC/galeria/cuarto_destrozado.png", "visible": True},
        "foto_corrupta_2": {"abierta": False, "minimizada": False, "titulo": "##er#e.jpg", "ruta": "images/escritorioPC/galeria/ojo.png", "visible": True},
        
        # mas archivos corruptos
        "nota_corrupta_2": {"abierta": False, "minimizada": False, "titulo": "NO_ABRIR.txt", "contenido": "¿Por qué no estabas?\nTodo esto es tu culpa.", "visible": True},
        "nota_corrupta_3": {"abierta": False, "minimizada": False, "titulo": "secreto.txt", "contenido": "Duele respirar.", "visible": True},
        "foto_corrupta_3": {"abierta": False, "minimizada": False, "titulo": "P@5tI11@.png", "ruta": "images/escritorioPC/galeria/pastillas.png", "visible": True}
    }

    #  orden en el que aparecerán minimizadas en la barra de tareas
    orden_apps = ["nota", "chat", "galeria", "musica", "webcam", "nota_turbia", "nota_corrupta_1", "foto_corrupta_1", "foto_corrupta_2", "nota_corrupta_2", "nota_corrupta_3", "foto_corrupta_3"]

    def abrir_archivo_corrupto(app_id, cg_var=None):
        store.apps_pc[app_id]["abierta"] = True
        store.apps_pc[app_id]["minimizada"] = False
        store.archivos_explorados += 1
        
        if cg_var:
            setattr(store.persistent, cg_var, True)
            ruta = store.apps_pc[app_id]["ruta"]
            if ruta not in store.lista_fotos:
                store.lista_fotos.append(ruta)
                
        renpy.restart_interaction()

    def abrir_app(app_id):
        store.apps_pc[app_id]["abierta"] = True
        store.apps_pc[app_id]["minimizada"] = False
        renpy.restart_interaction()

    def abrir_y_guardar_foto(app_id):
        abrir_app(app_id)
        ruta = store.apps_pc[app_id]["ruta"]
        if ruta not in store.lista_fotos:
            store.lista_fotos.append(ruta)
            renpy.notify("Imagen guardada en la Galería")

    def cerrar_app(app_id):
        store.apps_pc[app_id]["abierta"] = False
        renpy.restart_interaction()

    def toggle_minimizar(app_id):
        if store.apps_pc[app_id]["abierta"]:
            store.apps_pc[app_id]["minimizada"] = not store.apps_pc[app_id]["minimizada"]
            renpy.restart_interaction()

# Lista de rutas de las imagenes de galeria
default lista_fotos = [
    "images/escritorioPC/fondo_escritorio.png",
    "images/escritorioPC/icono_chica.png"
]

# Variables chica
image chica comiendo:
    "images/diurna/modelos_chica/chica_comiendo.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300 

image chica inexpresiva:
    "images/diurna/modelos_chica/chica_inexpresiva.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica inquieta:
    "images/diurna/modelos_chica/chica_inquieta.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica llorando:
    "images/diurna/modelos_chica/chica_llorando.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica orgullosa:
    "images/diurna/modelos_chica/chica_orgullosa.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica pensando:
    "images/diurna/modelos_chica/chica_pensando.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica rota:
    "images/diurna/modelos_chica/chica_rota.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica hablando:
    "images/diurna/modelos_chica/chica_hablando.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica molesta:
    "images/diurna/modelos_chica/chica_molesta.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica molesta2:
    "images/diurna/modelos_chica/chica_molesta2.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica resoplando:
    "images/diurna/modelos_chica/chica_resoplando.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300
    


image chica molestaBroma:
    "images/diurna/modelos_chica/chica_molestaBroma.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica reverencia:
    "images/diurna/modelos_chica/chica_reverencia.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica riendo:
    "images/diurna/modelos_chica/chica_riendo.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

image chica apenada:
    "images/diurna/modelos_chica/chica_apenada.png"
    ysize 700
    fit "contain"
    xalign 0.5
    yalign 1.0
    yoffset -300

# Definicion de personajes
define r = Character("Rocío")
define y = Character("Yo")
define v = Character("Voz")

# Variables de Puntos Finales
default puntos_mentira = 0
default puntos_verdad = 0

label start:
    
    # Sistema de bucle tras finalizar juego
    if persistent.final_alcanzado == "neutro":
        jump bucle_postgame_neutro
    elif persistent.final_alcanzado == "malo":
        jump bucle_postgame_malo
    elif persistent.final_alcanzado == "bueno":
        jump bucle_postgame_bueno


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
    window hide
    # Cargamos las ventanas normales
    show screen ventana_nota
    show screen ventana_chat
    show screen ventana_galeria
    show screen ventana_musica
    show screen ventana_webcam
    
    # --- Cargamos las ventanas múltiples usando 'as' para que no se pisen ---
    show screen ventana_nota_turbia("nota_corrupta_1") as turbia_1
    show screen ventana_nota_turbia("nota_corrupta_2") as turbia_2
    show screen ventana_nota_turbia("nota_corrupta_3") as turbia_3
    
    show screen ventana_visor_fotos_raras("foto_corrupta_1") as visor_1
    show screen ventana_visor_fotos_raras("foto_corrupta_2") as visor_2
    show screen ventana_visor_fotos_raras("foto_corrupta_3") as visor_3
    
    # Mostramos el escritorio interactivo encima de todo
    call screen escritorio_pc 
    $ default_mouse = "pc_normal"
    
    # Por si el jugador decide pulsar el botón de apagar manualmente
    scene black with fade
    "He apagado el ordenador manualmente..."
    
    if capitulo_actual == "prologo":
        jump transicion_dia_1
    else:
        "Todavía no debería apagarlo. Tengo cosas que ver."
        jump bucle_pc

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
    $ persistent.nube_decisiones = decisiones_tomadas
    $ renpy.save_persistent()

    $ guardar_progreso(capitulo_actual, decisiones_tomadas)

    # poner música alegre 

    scene fondo_patio2:
        xysize (1430, 700) 
        xalign 0.5  
        yalign 0.2 
    with fade 

    show chica resoplando

    r "Ahhhhhhhhhhhhhhh por fin terminaron los exámenes!!!!!!!!!"
    
    show chica hablando
    r "Ya somos libres al fin"
    
    y "Por fin eh! fueron dos semanas intensas pero ya podemos olvidarnos un tiempo de todo."
    
    r "Sisi, por cierto, qué tal el último examen? No te pareció demasiado difícil?!?"
    
    y "Eh? Si bueno...tampoco fue para tanto, creo que lo aprobaré."
    
    show chica molestaBroma
    r "Eh?!?! Que no era para tanto?? Oye....me tienes que enseñar a estudiar, no sé cómo lo haces pero a mí me cuesta muchísimo y encima éste examen me fue bastante regulero UnU"
    
    y "Ya te dije que estudiaras más, hasta te ofrecí mi ayuda pero me dijiste que podías sola."
    
    show chica reverencia
    r "Perdone mi insolencia maestro, a partir de ahora te haré caso en todo."
    
    y "Ujum, así me gusta discípula, espero que no haya más faltas de respeto."
    
    show chica riendo
    r "Pffffff jajajajajaaja al final me volveré tu discípula de verdad"
    
    y "Jajajajaja déjate de tonterías."
    
    scene fondo_calle:
        xysize (1430, 700) 
        xalign 0.5  
        yalign 0.2 
    with fade 

    show chica pensando
    r "Ah...........ahora sin exámenes podemos ir a celebrar a algún lado."
    
    y "No es mala idea aunque estoy algo agotado tras el examen, quiero irme a casa a descansar."
    
    show chica molesta
    r "Oye oye como así?!?! Justo acabamos los exámenes y ya estás pensando en volver a casa?!?!?" 
    r "No será que quieres volver para ponerte con el PC y dejarme aquí sola no? UnU"
    y "Simplemente estoy cansado, no me apetece mucho ir a algún lado; si quieres mañana vamos a tomar algo si?"
    
    show chica resoplando
    r "Hmmm bueeeenooo....Mientras me lo prometas..."
    y "Prometido"
    
    show chica inquieta
    r "Ah.................................."
    r "Bueno..."
    r "Espero que no vuelvas a esa época..."
    
    y "¿?"
    
    show chica hablando
    r "Te acuerdas cuando estábamos en secundaria y había que sacarte a rastras para que salieses del cuarto?" 
    show chica molestaBroma
    r "No salías por nada del mundo, querías quedarte con tus videojuegos y tu computadora."

    # primera eleccion
    menu:
        "Seguro que eso no lo dices por ti? Era yo quien tenía que ir detrás de ti para que salieses":
            jump mentira_uno

        "Ya...no me alejaba de mi PC por nada del mundo jajaja":
            jump verdad_uno

# RUTAS DEL PRIMERA ELECCIÓN
label mentira_uno:
    $ puntos_mentira += 1

    $ decisiones_tomadas["dia_1_eleccion_1"] = "mentira"

    show chica apenada
    r "Ay...es cierto, perdona, me costaba salir de mi cuarto jajaja quería quedarme todo el día en frente de la computadora con mis videojuegos y mi anime :3"

    y "Ya decía yo, me quieres echar la culpa de tus irresponsabilidades eh? hmmm"
    
    show chica molestaBroma
    r "Ya ya, que si, simplemente me equivoqué vale? Pensaba que eras tú el antisocial de los dos."

    y "Jajajajaj"

    "Cuando teníamos 13 años Rocío se encerró en su cuarto casi toda la secundaria, por lo menos hasta los 15 o 16 años. Diría que quedábamos una vez al mes o hasta dos meses. "
    "A menos de que yo le insistiese no salía de casa, prefería quedarse con su PC todo el día. Solo podíamos vernos en las quedadas o a veces de regreso a casa."
    "Me alegra que por fin haya salido de su cascarón."

    show chica hablando
    r "De todas formas eso ya es agua pasada, ya salí de mi cueva así que podremos hacer quedadas más frecuentes, hasta podríamos ir a un karaoke."

    jump dia_1_escena2

label verdad_uno:
    $ puntos_verdad += 1
    
    $ decisiones_tomadas["dia_1_eleccion_1"] = "verdad"

    show chica pensando
    r "No sé porqué no querías alejarte del PC, parecía tu DIOS."
    
    y "Tampoco tanto jajaja solo que...no sé, me lo pasaba bien encerrado con mis cosas. Pero eso ya es agua pasada, ahora por fin me di cuenta de que en la vida hay algo más aparte de la compu. Ya dejé de ser un hikikomori de esos. Aunque yo si iba a clases." 

    show chica hablando
    r "Me alegra que por fin te decidiste salir y dar un cambio a tu vida, no es sano quedarse tanto tiempo encerrado frente a una pantalla."

    y "Ya ya, ya sé tonta. No he dejado atrás mis pasiones pero sé que la vida sigue xD."

    "Cuando tenía 13 años de la nada empecé a encerrarme en mi cuarto y a pasar cada vez más horas frente a la computadora. No era por nada en especial, simplemente me lo pasaba bien y así me alejaba de la realidad."
    "Me pasé así casi toda mi secundaria, hasta los 15 o 16 años."
    "De igual forma iba a clases cada día y aprobaba como podía, pero si que llegué a hacer pellas con tal de terminar algún anime..."
    "Rocío siempre tenía que venir a mi casa para convencerme de salir; aunque pocas veces funcionaba, había veces que le hacía caso."

    show chica hablando
    r "De todas formas eso ya es agua pasada, ya salí de mi cueva así que podremos hacer quedadas más frecuentes, hasta podríamos ir a un karaoke."

    jump dia_1_escena2

label dia_1_escena2:
    y "Oh!! La idea del karaoke no es mala, podríamos ir la semana que viene."

    show chica orgullosa
    r "¿Ves? Siempre propongo buenas ideas JeJE"

    show chica hablando
    r "Pues decidido, ¿no me dejes plantada esta vez eh?"

    y "Si si, me lo apuntaré en el cerebro para no olvidarlo."
    
    show chica orgullosa
    r "Así me gusta Ujumm."

    show chica hablando
    r "¿Tampoco olvides lo de mañana eh? Después de clases vayamos a alguna cafetería a tomar algo."
    y "Si si, también lo tengo apuntado."

    show chica molestaBroma
    r "Más te vale Hmmm"

    scene fondo_calle_atardecer:
        xysize (1430, 700) 
        xalign 0.5  
        yalign 0.2 
    with fade 

    show chica hablando
    y "Bueno, creo que es hora de que nos vayamos ya a casa, ya estamos en el cruce."
    y "Y estoy que me muero..."
    r "Hmmmmm sé que te pondrás con el PC, de igual forma te escribiré como te vea conectado"
    y "Sólo estaré un rato anda, no me seas tan controladora."
    show chica molestaBroma
    r "Simplemente me preocupo de que quieras pasar más tiempo con tu computadora que con tu amiga."
    y "No es eso tonta, sabes que no."
    show chica reverencia
    r "Bueno, con esto me despido, gracias por acompañarme hasta aquí pero...nuestros caminos se tienen que separar...fue bonito mientras duró..."
    y "Venga anda, nos vemos mañana."
    r "Chaoooo ;D"
    hide chica
    r "Recuerda que te escribiré esta noche."
    y "Si si, adiós."

    "Hora de ir a casa por fin, supongo que me conectaré un rato."

    jump transicion_dia_1_noche

label transicion_dia_1_noche:
    window hide
    scene black with fade
    pause 1.0

    show expression Text("DÍA 1 (noche)", font="gui/fonts/Micro5.ttf", size=150, color="#ffffff") as cartel_dia:
        xalign 0.5
        yalign 0.5
    with dissolve
    
    pause 3.0
    
    hide cartel_dia with dissolve

    # Y ahora sí, saltamos a tu escena de la noche
    jump dia_1_noche

label dia_1_noche:
    $ estilo_interfaz = "pc"
    $ default_mouse = "pc_normal"

    $ capitulo_actual = "dia_1_noche"
    $ persistent.nube_capitulo = "dia_1_noche"
    $ persistent.nube_decisiones = decisiones_tomadas
    $ renpy.save_persistent()

    $ guardar_progreso(capitulo_actual, decisiones_tomadas)

    $ nivel_corrupto = 1
    $ apps_pc["nota_turbia"]["contenido"] = "¿Por qué no contestaste?\nMe ahogo."
    $ destino_noche = "transicion_dia_2" # a donde salta el botón de finalizar del chat

    #Limpia el escritorio al iniciar
    python:
        for app in apps_pc:
            apps_pc[app]["abierta"] = False
            apps_pc[app]["minimizada"] = False

    scene fondo_escritorio_corrupto with fade

    "Por fin en casa... estoy agotado."
    "¿Eh? Qué es todo esto? Anoche no estaban estos archivos en el escritorio n-no?"
    "¿Será que tengo un virus? Ah.......un virus que deja notas en el escritorio e imágenes raras..."
    "Espero que lo pueda sacar."
    
    jump bucle_pc

label evento_voces_dia1:
    show screen escritorio_pc

    $ susto_voces_hecho = True
    window show 
    v "Deja de hacerte el tonto..."
    "¿Eh?"
    v "Deja de huir..."
    "¿Huir? ¿¿Cómo?? Creo que he escuchado algo...."
    "..."
    "............."
    "Hmmmm quizás...ha sido cosa mía, qué raro..."
    "No sé porqué pero siento que me cuesta respirar...."
    
    play sound "Musica/Efectos/notificacion_mensajes.mp3"
    $ mensajes_nuevos = True
    $ renpy.notify("Nuevo mensaje de: Roxy26")

    "¡¡Ah!! Uf...es solo un mensaje de Rocío. Menos mal."
    "Mi cabeza me está jugando malas pasadas por este estúpido virus."
    "Será mejor que le conteste y me distraiga un poco."

    window hide

    python:
        store.historial_mensajes = [] 
        recibir_mensaje("Rocío", "Heyyyyyyyyyyyyy")
        recibir_mensaje("Rocío", "Sé que estás en línea!!!!!")
        recibir_mensaje("Rocío", "CONTESTAAAA")
        recibir_mensaje("Rocío", "*cara molesta*")
        
        store.respuestas_disponibles = [
            ("Ya estoy, ya estoy. Estaba mirando unas cosas raras en el pc...", "chat_dia1_noche_nodo1")
        ]
    
    hide screen escritorio_pc
    jump bucle_pc


label chat_dia1_noche_nodo1:
    pause 1.0
    $ recibir_mensaje("Rocío", "Eh? Te has puesto a ver guarradas o qué?")
    pause 1.5
    $ recibir_mensaje("Yo", "Qué?? Malpensada, no, me refería a que hay algo raro en mi PC")
    pause 1.0
    $ recibir_mensaje("Rocío", "Algo raro?")
    pause 1.5
    $ recibir_mensaje("Yo", "Si...de la nada han aparecido varios archivos de texto e imágenes en el escritorio")
    pause 1.5
    $ recibir_mensaje("Rocío", "Ehm? Será algo que dejaste pero te olvidaste de ello")
    pause 1.0
    $ recibir_mensaje("Yo", "Nahh estoy al 100% de que no es mío.")
    pause 1.5
    $ recibir_mensaje("Yo", "Creo que tengo un virus peligroso :/")
    pause 1.5
    $ recibir_mensaje("Rocío", "Hmmm, vaya... ¿y qué vas a hacer?")
    pause 1.5
    $ recibir_mensaje("Yo", "Por ahora...supongo que ignorarlo. Lo llevaré a reparar en unos días a ver.")
    
    pause 2.0
    $ recibir_mensaje("Rocío", "...")
    pause 2.0
    $ recibir_mensaje("Rocío", "Siempre haces lo mismo no?")
    pause 1.5
    $ recibir_mensaje("Yo", "¿Qué?")
    pause 2.0
    $ recibir_mensaje("Rocío", "Ignorar las cosas cuando se ponen feas, esperando a que pasen solas.")
    pause 1.5
    $ recibir_mensaje("Rocío", "Aunque alguien te pida ayuda a gritos en tu propia cara.")

    $ respuestas_disponibles = [
        ("Es lo más facil cuando no sabes qué hacer. Ojos que no ven, corazón que no siente.", "mentira_dos"),
        ("Lo siento. Sé que es un defecto mío que debo corregir.", "verdad_dos")
    ]
    jump bucle_pc

label mentira_dos:
    $ puntos_mentira += 1
    $ decisiones_tomadas["dia_1_eleccion_2"] = "mentira"

    pause 1.5
    $ recibir_mensaje("Rocío", "Ya......")
    pause 1.5
    $ recibir_mensaje("Rocío", "Supongo que tienes razón. Bueno, no te rayes con el PC")
    pause 1.5
    $ recibir_mensaje("Rocío", "Llévalo a reparar cuando puedas.")
    pause 1.5
    $ recibir_mensaje("Yo", "La semana que viene lo llevaré")
    pause 1.0
    $ recibir_mensaje("Yo", "O espero a que se arregle solo jajajaja")
    pause 2.0
    $ recibir_mensaje("Rocío", "...")
    pause 1.5
    $ recibir_mensaje("Rocío", "Jajajaja siempre igual ")
    pause 1.5
    $ recibir_mensaje("Rocío", "Me voy a dormir que ya es tarde. ")
    pause 1.5
    $ recibir_mensaje("Rocío", "No te olvides mañana de la quedada eh? ")
    pause 1.5
    $ recibir_mensaje("Rocío", "Te llevaré a rastras si hace falta")
    pause 1.5
    $ recibir_mensaje("Yo", "Ya te dije que vamos a ir")
    pause 1.5
    $ recibir_mensaje("Rocío", "Eso espero. Bueno...")
    pause 1.5
    $ recibir_mensaje("Rocío", "Chaooo ")
    pause 1.5
    $ recibir_mensaje("Yo", "Nos vemos mañana anda ")
    
    # Pensamientos del protagonista 
    "No le he dicho nada pero...¿y esa actitud rara tan repentina?"
    "Por no mencionar esa pregunta....bueno, da igual"
    "No le daré mucha importancia, ni a ella ni al virus por ahora."


    # Preparamos el botón para cerrar la noche
    $ respuestas_disponibles = []
    $ mostrar_boton_finalizar = True 
    jump bucle_pc


label verdad_dos:
    $ puntos_verdad += 1
    $ decisiones_tomadas["dia_1_eleccion_2"] = "verdad"

    pause 1.5
    $ recibir_mensaje("Rocío", "...")
    pause 1.5
    $ recibir_mensaje("Rocío", "Ojalá te hubieras dado cuenta antes...")
    pause 1.5
    $ recibir_mensaje("Yo", "¿Antes, antes de qué?")
    pause 1.5
    $ recibir_mensaje("Rocío", "De que ya es muy tarde tonto jajajaja.")
    pause 1.5
    $ recibir_mensaje("Rocío", "Me voy a dormir ya que mañana hay clase.")
    pause 1.5
    $ recibir_mensaje("Yo", "Eh? B-bueno...")
    
    "Qué acaba de pasar? Por un momento la he notado rara..."

    pause 1.5
    $ recibir_mensaje("Rocío", "No te olvides mañana de la quedad eh? ")
    pause 1.5
    $ recibir_mensaje("Rocío", "Ya me prometiste que mañana vamos a celebrar Hmm.")
    pause 1.5
    $ recibir_mensaje("Rocío", "Te llevaré a rastras si hace falta")
    pause 1.5
    $ recibir_mensaje("Yo", "Ya te dije que vamos a ir")
    pause 1.5
    $ recibir_mensaje("Rocío", "Eso espero. Bueno...")
    pause 1.5
    $ recibir_mensaje("Rocío", "Chaooo")
    pause 1.5
    $ recibir_mensaje("Yo", "Nos vemos mañana anda ")

    # Pensamientos finales
    
    "No le he dicho nada pero...¿y esa actitud rara tan repentina?"
    "Por no mencionar esa pregunta.....bueno, da igual"
    "No le daré mucha importancia, ni a ella ni al virus por ahora."

    # Preparamos el botón para cerrar la noche
    $ respuestas_disponibles = []
    $ mostrar_boton_finalizar = True 
    jump bucle_pc

label transicion_dia_2:
    hide screen escritorio_pc
    hide screen ventana_chat
    hide screen ventana_nota
    hide screen ventana_galeria
    hide screen ventana_musica
    hide screen ventana_webcam
    hide screen ventana_nota_turbia
    hide screen ventana_visor_fotos_raras
    
    python:
        for app in apps_pc:
            apps_pc[app]["abierta"] = False
            apps_pc[app]["minimizada"] = False
            
    $ mostrar_boton_finalizar = False

    window hide
    stop music fadeout 2.0

    scene black with fade
    pause 1.0

    show expression Text("DÍA 2 (escena diurna)", font="gui/fonts/Micro5.ttf", size=150, color="#ffffff") as cartel_dia:
        xalign 0.5
        yalign 0.5
    with dissolve
    
    pause 3.0
    
    hide cartel_dia with dissolve

    jump dia_2

label dia_2:
    $ estilo_interfaz = "dia_normal"
    $ default_mouse = "cursor_normal"

    # Guardar el estado de la partida
    $ capitulo_actual = "dia_2"
    $ persistent.nube_capitulo = "dia_2" 
    $ persistent.nube_decisiones = decisiones_tomadas
    $ renpy.save_persistent()
    $ guardar_progreso(capitulo_actual, decisiones_tomadas)

    window show 

    # -- En el instituto --
    scene fondo_patio2:
        xysize (1430, 700) 
        xalign 0.5  
        yalign 0.2 
    with fade

    "Por fin terminaron las clases."
    "Ahora iré al patio para buscar a Rocío."
    "Hmmm...?"
    "Sniff Sniff, que raro...huele mucho a alcohol desinfectante."
    "¿Habrán limpiado el instituto a fondo hoy?"
    "Además...no sé porqué pero desde hace un rato siento como un pinchazo en el brazo izquierdo...Qué molestia"
    
    # Efecto de sonido del hospital oculto
    play sound "Musica/Efectos/monitor_cardiaco.ogg" loop
    "..."
    stop sound fadeout 1.0

    show chica hablando
    with dissolve

    r "Oh! Ahí estás!!!"
    y "Heyyyy"
    r "Te estaba buscando, para que no te me escapes."
    y "Jajaja ya te prometí que iríamos a algún lado hoy."
    
    show chica inexpresiva
    r "Bueno..."
    r "..."
    y "Estás bien? Te veo alicaída o preocupada"
    r "No es nada, simplemente me duele un poco la cabeza y siento que tengo el estómago revuelto. Pero tú no te preocupes, puedo soportarlo con tal de que por fin hagamos algo juntos."
    y "B-bueno...si tú lo dices...pero si te encuentras mal hazmelo saber eh?"
    r "..."
    r "Claro...."
    r "Conque ahora si te preocupas eh?" # Susurrando
    y "Eh? Dijiste algo?"
    
    show chica hablando
    r "Nope, nadita"
    y "¿?"
    
    show chica orgullosa
    r "Vamos tirando anda, que hace poco han abierto una cafetería cerca de mi barrio y escuché que hacen unos dulces riquísimos, por no decir el té que tienen...ahhhhh "
    y "No era que estabas revuelta del estómago? "
    
    show chica riendo
    r "Ya se me pasó jeje"
    y "Ah......bueno vale, vamos "

    # -- En el local --
    scene fondo_cafeteria:
        xysize (1430, 700) 
        xalign 0.5  
        yalign 0.2 
    with fade 
    
    play sound "Musica/Efectos/campana_puerta.ogg"

    "El sitio es bastante bonito, la verdad. Quién diría que cerca habría una cafetería tan acogedora."
    "Aunque... qué raro. No hay absolutamente nadie más aquí. Ni siquiera escucho el ruido de la calle a través de los cristales."
    "Bueno, mejor. Más tranquilos."

    show chica hablando
    with dissolve

    r "Está bien lindo el local, ¿no crees?"
    y "Justo lo estaba pensando, es muy acogedor."
    
    show chica comiendo
    r "Verdad que si??"
    r "Y mira qué buena pinta tiene esta tarta de fresa....ahhhhhhhh "
    y "Vamos a pedir algo, y esta te invito yo."
    
    show chica reverencia
    r "Pero......eres el mismo de siempre? Y este altruismo? "
    y "Si te vas a quejar no te compro nada"
    r "Nonono maestro, le agradezco tal ofrenda hacia alguien de mi calaña."
    y "Jum Jum así me gusta."
    
    "Voy a pedir para los dos lo mismo, dos trozos de tarta de fresa y dos cappuccinos."
    
    show chica hablando
    r "Vamos a esa mesa de ahí."

    # *sentados en la mesa*
    scene fondo_cafeteria: 
        xysize (1430, 700) 
        xalign 0.5  
        yalign 0.2 
    with fade

    show chica comiendo
    with dissolve

    r "Ah.......que pintaza que tiene..."
    y "La verdad que si, simplemente con verlo entra hasta hambre."
    r "A comer!!!"
    
    "Parece que Rocío está disfrutando un montón del pastel."
    "Yo también debería comer."
    y "*masticando*"
    
    show chica inexpresiva
    r "Oye..."
    y "¿Mmm? *masticando*"
    
    show chica pensando
    r "Sabes? Me estaba preguntando..."
    r "¿Crees que en el futuro seguiremos viniendo a sitios así? Digo...no sabemos qué es lo que nos deparará pero...crees que seguiremos juntos?"
    y "Eh? Pues claro que si, no sé porqué dudas."
    
    show chica inexpresiva
    r "Hmm"
    r "No sé... a veces miro hacia adelante y...no veo nada. Como si mi futuro fuera una pared en blanco."
    y "Qué cosas más raras dices hoy, de verdad. Anda, cómete la tarta que se le va a derretir la nata. "
    r "..."

    "Me le quedo mirando extrañado. "
    "Un momento... "
    "Su trozo de tarta está completamente intacto. Ni siquiera ha cogido el tenedor."
    "Pero si juraría que la vi comer hace un segundo... ¿Me lo habré imaginado?"
    
    y "Oye, ¿no te gusta?"
    
    show chica rota
    r "Es que se me ha vuelto a revolver el estómago."
    r "Siento como si hubiera tragado algo muy fuerte... algo que me está quemando por dentro."
    y "¿Quieres que nos vayamos? Estás muy pálida."
    r "No. Quédate ahí sentado."

    # *la música de la cafetería se distorsiona un segundo y baja de volumen*
    stop music
    play sound "Musica/Efectos/glitch.ogg"
    with vpunch 

    show chica inexpresiva
    r "Mírame a los ojos."
    r "Si algún día te digo que no puedo más... que me duele demasiado y voy a desaparecer..."
    r "Me ayudarías? Vendrías a salvarme?"
    "Q-qué?!"

    menu:
        "No digas tonterías, claro que no vas a desaparecer":
            jump mentira_tres
        "...Perdóname por todas las veces que preferí quedarme en mi cuarto.":
            jump verdad_tres


# ---------------- RUTAS DE LA TERCERA ELECCIÓN ----------------

label mentira_tres:
    $ puntos_mentira += 1
    $ decisiones_tomadas["dia_2_eleccion_1"] = "mentira"

    r "..."
    show chica rota
    r "Es verdad...es una tontería preocuparse por algo así no?"
    r "Es más fácil dejar que todo pase y no tomar responsabilidad por ello."
    y "Te estás montando unas películas tú sola... Será el azúcar de los dulces que te ha subido a la cabeza."
    
    show chica inexpresiva
    r "..."
    r "Sí. Claro. Será eso."
    y "Anda, vámonos ya a casa que necesitas descansar de verdad."
    
    play sound "Musica/Efectos/glitch.ogg"
    with hpunch
    
    show chica resoplando
    r "Tienes razón. Volvamos a la normalidad."
    "Uf, qué alivio. Por un momento me estaba asustando de verdad. A veces es tan dramática..."

    stop music
    v "Siempre igual, si sigues así nada cambiará..."
    y "¿Q-qué??"
    
    # Vuelve la musica
    $ reproducir_pista()
    
    show chica inquieta
    r "¿?"
    y "Has escuchado eso??"
    
    show chica pensando
    r "Ehm...no? No escuché nada, estamos solos en el local, ¿recuerdas?"
    y "S-si.......da igual, no es nada."
    "Juraría que escuché una voz similar anoche..."
    
    show chica hablando
    r "Bueno, ya vámonos."
    jump dia_2_escena_2


label verdad_tres:
    $ puntos_verdad += 1
    $ decisiones_tomadas["dia_2_eleccion_1"] = "verdad"

    r "..."
    y "No sé por qué lo dices ahora, pero... escucharte hablar de desaparecer me ha provocado un nudo horrible en el estómago."
    "..."
    
    # *el escenario se oscurece un poco y el silencio es total*
    scene black with fade
    
    r "Gracias por pedir perdón."
    r "Aunque me duele que hayas tenido que esperar a que me queme por dentro para darte cuenta."
    y "¿Qué te quema? ¡Rocío! ¿Quieres que vayamos al médico? Estás sudando frío."

    # *la música alegre vuelve de golpe al volumen máximo*
    $ reproducir_pista()
    
    scene fondo_cafeteria:
        xysize (1430, 700) 
        xalign 0.5  
        yalign 0.2 
    with vpunch

    show chica riendo
    r "Jajaja ¡Ay, tu cara! Qué exagerado eres. ¡Si solo es un corte de digestión por culpa de hablar de cosas tristes mientras comemos!"
    y "¿Eh? Pero si acababas de decir..."
    
    show chica hablando
    r "Vámonos ya, anda. Solo me hace falta dormir esta noche y como nueva."
    "¿Qué acaba de pasar? Juro que sus ojos estaban vacíos hace un segundo. "
    "Mi cabeza me va a estallar. Todo esto se siente demasiado irreal..."
    
    r "Hey!! Venga, vámonos"
    jump dia_2_escena_2


# ---------------- DÍA 2 - ESCENA 2 (En la calle) ----------------

label dia_2_escena_2:
    scene fondo_calle:
        xysize (1430, 700) 
        xalign 0.5  
        yalign 0.2 
    with fade 

    show chica hablando
    with dissolve

    r "Gracias por haber aceptado venir a este sitio y no dejarme tirada."
    y "Por quién me tomas? Un insensible sin corazón?"
    
    show chica pensando
    r "Hmmm a veces lo pareces"
    y "Oyeeee"
    
    show chica riendo
    r "Jajajaja"
    
    show chica hablando
    r "La verdad es que me alegro que ahora quedemos más a menudo y podamos hacer planes como estos."
    y "Ya...yo también, hacía tiempo que no probaba una tarta tan rica."
    
    show chica orgullosa
    r "Ni yo ni yo"
    "Pero...si creo que ni se la comió al final"
    
    show chica apenada
    r "Ojalá momentos así duren para siempre pero...ya sabes, en algún momento nos tendremos que separar."
    y "No tiene porqué ser así."
    y "Es decir......habíamos decidido ir a la misma universidad no? Y sino sale bien siempre podemos quedarnos en la misma ciudad. "
    y "Al final siempre estaremos juntos y de vez en cuando volveremos a sitios como estos a pasar el día."
    
    show chica inexpresiva
    r "..."
    y "No te pongas tan dramática tonta, aunque en un futuro estudiemos algo diferente o trabajemos en cosas diferentes, siempre nos tendremos el uno al otro no?"
    y "Así fue siempre"
    r "..."
    
    show chica rota
    r "Por mucho que lo digas ahora ya es tarde..."
    r "Siempre tardas en darte cuenta de las cosas no? Siempre fuistes así."
    "Rocío....está llorando?"
    y "R-Rocío? "
    r "..."
    
    show chica apenada
    r "Da igual"
    r "Perdona, se me ha metido algo en el ojo. Ya digo tonterías."

    menu:
        "Claro tonta, seguro que estás cansada. Anda, vamos a casa.":
            jump mentira_cuatro
        "No te obligues a sonreír...Sé que te he fallado en el pasado.":
            jump verdad_cuatro


# ---------------- RUTAS DE LA CUARTA ELECCIÓN ----------------

label mentira_cuatro:
    $ puntos_mentira += 1
    $ decisiones_tomadas["dia_2_eleccion_2"] = "mentira"

    r "Sí... vamos."
    "Uf. Qué susto me ha dado. "
    "Por un momento la he visto tan frágil que parecía que iba a desaparecer."
    "Mejor la llevo a casa rápido y me conecto al PC para distraerme."
    
    show chica rota
    r "Siento...mucho frío, vamos a darnos prisa."
    "Hace un sol que derrite, pero ella está temblando."
    "Ah....mi cabeza vuelve a doler...siento que va a estallar."
    
    jump dia_2_escena_3


label verdad_cuatro:
    $ puntos_verdad += 1
    $ decisiones_tomadas["dia_2_eleccion_2"] = "verdad"

    y "Sé que te he fallado en el pasado y que a veces soy un insensible."
    y "Perdóname."
    
    show chica inexpresiva
    r "..."
    r "De nada sirve pedir perdón ahora."
    y "¿Qué?"
    
    stop music
    
    show chica apenada
    r "Nada, una broma estúpida. "
    r "Llévame a casa ya, por favor. Hace... hace mucho frío."
    "Hace un sol que derrite, pero ella está temblando."
    "Ah....mi cabeza vuelve a doler...siento que va a estallar."
    
    $ reproducir_pista()
    jump dia_2_escena_3


# ---------------- DÍA 2 - ESCENA 3 (Casa de Rocío) ----------------

label dia_2_escena_3:
    scene fondo_calle_atardecer:
        xysize (1430, 700) 
        xalign 0.5  
        yalign 0.2 
    with fade 

    show chica hablando
    with dissolve

    "Al final la acompañé hasta su casa"
    
    show chica reverencia
    r "Gracias por acompañarme a mi humilde morada "
    y "Es lo de menos hacer esto por mi aprendíz"
    
    show chica riendo
    r "jeje... Me lo he pasado bien"
    y "Igual yo, habrá que repetir algún día de estos"
    
    show chica inexpresiva
    r "Si...habrá que...repetir..."
    y "¿?"
    
    show chica apenada
    r "Me iré de inmediato a descansar, no sé porqué pero me siento muy muy cansada."
    y "Oke, deberías descansar la verdad."
    
    show chica hablando
    r "Supongo que nos vemos mañana"
    y "Seh, hasta mañana!!"
    
    show chica inexpresiva
    r "..."
    y "¿Eh? ¿Te encuentras bien?"
    "Parece que aún no entra en casa"
    "¿Querrá decirme algo?"
    
    r "Prométeme..."
    y "¿?"
    
    show chica rota
    r "Prométeme que no harás ninguna locura si?"
    y "¿Q-qué?"
    r "Prométeme que si me pasa algo no harás alguna locura"
    y "¿Pero q-qué? Rocío...¿qué diablos estás diciendo?"
    y "¡¿Por qué te iba a pasar algo?!"
    r "..."
    r "Solo promételo, ¿vale? "
    
    show chica llorando
    "*sonríe débilmente, con los ojos cristalizados* "
    r "Nos vemos mañana."

    # Desaparece bruscamente y suena un portazo
    hide chica
    play sound "Musica/Efectos/puerta_cerrando.mp3"
    with vpunch
    
    pause 1.0

    "Pero...¿qué ha sido todo esto?"
    "¿Hacer una locura? ¿A qué venía eso?"
    "..."
    "Siento que me falta el aire. El pecho me arde."
    "Todo ha sido muy raro hoy... mi cabeza no da para más. Necesito llegar a casa, encerrarme en mi cuarto y encender el PC para no pensar."

    # SALTO A LA NOCHE DEL DÍA 2
    jump transicion_dia_2_noche


# ---------------- TRANSICIÓN NOCHE DÍA 2 ----------------
label transicion_dia_2_noche:
    hide screen escritorio_pc
    hide screen ventana_chat
    hide screen ventana_nota
    hide screen ventana_galeria
    hide screen ventana_musica
    hide screen ventana_webcam
    hide screen ventana_nota_turbia
    hide screen ventana_visor_fotos_raras
    
    python:
        for app in apps_pc:
            apps_pc[app]["abierta"] = False
            apps_pc[app]["minimizada"] = False
            
    $ mostrar_boton_finalizar = False

    window hide
    stop music fadeout 2.0

    scene black with fade
    pause 1.0

    show expression Text("DÍA 2 (noche)", font="gui/fonts/Micro5.ttf", size=150, color="#ffffff") as cartel_dia:
        xalign 0.5
        yalign 0.5
    with dissolve
    
    pause 3.0
    
    hide cartel_dia with dissolve

    jump dia_2_noche

# ---------------- DÍA 2 - NOCHE ----------------
label dia_2_noche:
    $ estilo_interfaz = "pc"
    $ default_mouse = "cursor_normal"
    
    $ capitulo_actual = "dia_2_noche"
    $ persistent.nube_capitulo = "dia_2_noche" 
    $ persistent.nube_decisiones = decisiones_tomadas

    $ guardar_progreso(capitulo_actual, decisiones_tomadas)

    scene black with fade

    window show

    "Ufff que cansado me siento..."
    "Todo ha sido tan raro el día de hoy. Me pregunto qué le pasará a Rocío para que diga cosas como esas..."
    "Hmmm sin contar las cosas raras que he sentido a lo largo del día..."
    "Ah.................. Me distraeré un poco con la computadora."

    # *enciende el pc*
    play sound "Musica/Efectos/sonido_inicioSistema.ogg"
    
    $ nivel_corrupto = 2

    # Preparamos el PC Corrupto
    $ apps_pc["nota_turbia"]["contenido"] = "¿Por qué no contestaste?\nMe ahogo."
    $ apps_pc["nota_turbia"]["visible"] = True
    $ destino_noche = "transicion_dia_3"

    # Nombre de las apps cambiado
    $ apps_pc["galeria"]["titulo"] = "recuerdos_muertos"
    $ apps_pc["musica"]["titulo"] = "ruido.exe"
    $ apps_pc["chat"]["titulo"] = "NO_ESTOY_SOLO"

    # *fondo de pantalla más oscurecido*
    scene fondo_escritorio_corrupto2 with fade

    "¿Qué pasa con este escritorio??"
    "La nota esa...parece que es un virus muy potente, será un troyano."
    "El fondo está como más oscuro y...ni la música en el escritorio funciona... Supongo que no puedo pasar ya del virus, mañana o pasado lo llevo a reparar."
    "Intentaré no hacerle mucho caso..."

    # *sonido de notificación de chat x3*
    play sound "Musica/Efectos/notificacion.ogg"
    pause 0.4
    play sound "Musica/Efectos/notificacion.ogg"
    pause 0.4
    play sound "Musica/Efectos/notificacion.ogg"
    
    $ mensajes_nuevos = True
    $ renpy.notify("Nuevos mensajes de: Roxy26")

    "¿Eh? ¿Mensajes a estas horas?"
    "Pero... si Rocío se supone que se fue a dormir no? Se encontraba mal."
    "Esta tonta...le diré que se vaya a descansar"

    window hide

    # Preparamos el chat inicial
    python:
        store.historial_mensajes = [] 
        recibir_mensaje("Rocío", "Estás ahí?")
        recibir_mensaje("Rocío", "Por favor dime que estás ahí.")
        recibir_mensaje("Rocío", "Contesta.")
        
        store.respuestas_disponibles = [
            ("Sí, estoy. ¿Qué pasa? ¿No te ibas a dormir?", "chat_dia2_noche_nodo1")
        ]

    
    jump bucle_pc

# --- EVENTO WEBCAM ---
label evento_webcam_dia2:
    $ susto_webcam_hecho = True
    
    $ apps_pc["webcam"]["abierta"] = True
    $ apps_pc["webcam"]["minimizada"] = False
    $ contenido_webcam = "habitacion"
    
    show screen escritorio_pc
    
    window hide
    play sound "Musica/Efectos/glitch.ogg"
    with vpunch
    
    window show
    "¿PERO QUÉ? Porqué...porqué no aparezco en la webcam si se supone que me está enfocando?"
    "¿Estará descompuesta o será el virus?"
    
    $ contenido_webcam = "gif"
    play sound "Musica/Efectos/glitch.ogg"
    "Espera....qué...qué es eso del fondo?"

    v "ERES UN COBARDE"
    with hpunch
    v "OJALÁ HUBIERAS MUERTO"
    v "OJALÁ ELLA NUNCA SE HUBIESE INTERESADO POR TI"
    v "OJALÁ ELLA TE ABANDONE"
    
    "..."
    "*me giro para mirar la puerta pero no hay nada*"
    
    $ apps_pc["webcam"]["abierta"] = False
    $ contenido_webcam = "negro"
    
    "P-p-pero...pero qué mierdas acabo de ver...?"
    "Yo...mi corazón va a mil por hora. Estoy sudando frío."
    "V-voy a c-contestarle a Rocío..."
    
    hide screen escritorio_pc
    
    jump bucle_pc


# --- LÓGICA DEL CHAT DE LA NOCHE 2 ---
label chat_dia2_noche_nodo1:
    pause 1.0
    $ recibir_mensaje("Rocío", "No puedo dormir.")
    pause 1.0
    $ recibir_mensaje("Rocío", "Hace mucho frío aquí.")
    pause 1.5
    $ recibir_mensaje("Rocío", "Me duele mucho la cabeza, siento que me quema por dentro.")
    pause 1.0
    $ recibir_mensaje("Yo", "Rocío, me estás asustando en serio. ")
    pause 1.5
    $ recibir_mensaje("Yo", "¿Quieres que llame a tu madre o voy yo para allá?")
    
    # *El chat se queda en silencio unos segundos*
    pause 4.0

    $ recibir_mensaje("Rocío", "POR QUÉ NO CONTESTASTE")
    pause 1.0
    $ recibir_mensaje("Yo", "¿Qué? Si te acabo de contestar al segundo.")
    
    # Textos súper rápidos para dar ansiedad
    pause 0.2
    $ recibir_mensaje("Rocío", "EL TELÉFONO.")
    pause 0.2
    $ recibir_mensaje("Rocío", "ESTABA LLAMANDO.")
    pause 0.2
    $ recibir_mensaje("Rocío", "TE NECESITABA.")
    pause 0.2
    $ recibir_mensaje("Rocío", "TE NECESITABA.")
    pause 0.2
    $ recibir_mensaje("Rocío", "TE NECESITABA.")
    pause 0.2
    $ recibir_mensaje("Rocío", "ERES UN IMBÉCIL")
    pause 0.2
    $ recibir_mensaje("Rocío", "NO TE IMPORTO UNA MIERDA")

    # --- AQUÍ SUCEDE EL CORREO A LA VIDA REAL ---
    $ enviar_correo_real(pc_email)

    "¿Qué le pasa? Sus mensajes están llegando demasiado rápido, es imposible que escriba a esta velocidad."
    "Y yo no tengo ninguna llamada perdida suya en el móvil... "
    "¿Será el virus este de mierda que está controlando el chat?"
    
    pause 1.0
    $ recibir_mensaje("Yo", "Oye oye oye, qué estás diciendo????")
    pause 1.5
    $ recibir_mensaje("Yo", "¿Qué llamadas? Si no tengo ninguna llamada tuya de hoy.")
    pause 2.0
    $ recibir_mensaje("Rocío", "Me quedé sin aire...")
    
    "Siento una presión horrible en el pecho. Me cuesta respirar..."
    "Esto no es Rocío. No puede ser ella. Tiene que ser el hacker de este maldito virus jugando con mi mente."

    $ respuestas_disponibles = [
        ("¡Ya vale de bromas! Mañana hablamos cuando se te pase la tontería.", "mentira_cinco"),
        ("Rocío, por favor...... Siento mucho si te ignoré.", "verdad_cinco")
    ]
    jump bucle_pc


label mentira_cinco:
    $ puntos_mentira += 1
    $ decisiones_tomadas["dia_2_eleccion_3"] = "mentira"

    pause 1.0
    $ recibir_mensaje("Yo", "¡Ya vale de bromas! Si te han hackeado la cuenta o es el virus este, no tiene ninguna gracia.")
    pause 1.5
    $ recibir_mensaje("Yo", "Apago el PC. Mañana hablamos en clase cuando se te pase la tontería.")
    
    pause 2.0
    $ recibir_mensaje("Rocío", "...")
    pause 1.5
    $ recibir_mensaje("Rocío", "Sigues huyendo.")
    pause 1.5
    $ recibir_mensaje("Rocío", "Quédate ciego entonces.")

    # Desconexión forzosa
    pause 1.0
    "*Usuario 'Rocío' se ha desconectado*"
    play sound "Musica/Efectos/error_windows.ogg" # Opcional
    $ cerrar_app("chat")
    "*La pantalla del chat se cierra de golpe*"

    y "Menuda mierda de noche. Apago esta basura ya mismo."
    y "Mañana seguro que ella está en el instituto como si nada y me cuenta qué pasa."
    y "Mañana me lo explicará todo..."

    $ mostrar_boton_finalizar = True
    jump bucle_pc


label verdad_cinco:
    $ puntos_verdad += 1
    $ decisiones_tomadas["dia_2_eleccion_3"] = "verdad"

    pause 1.0
    $ recibir_mensaje("Yo", "Rocío, por favor.... ")
    pause 1.5
    $ recibir_mensaje("Yo", "Siento mucho si te ignoré alguna vez. Fui un idiota, lo admito.")
    pause 1.5
    $ recibir_mensaje("Yo", "Pero no entiendo de qué hablas. No me has llamado en todo el día.")
    
    pause 2.5
    $ recibir_mensaje("Rocío", "...")
    pause 1.5
    $ recibir_mensaje("Rocío", "No hoy.")
    pause 1.5
    $ recibir_mensaje("Rocío", "Ese día.")
    pause 1.5
    $ recibir_mensaje("Rocío", "El último día.")
    pause 1.0
    $ recibir_mensaje("Yo", "¿El... último día? ¿Qué dices?")

    pause 2.0
    "*El usuario 'Rocío' ha cambiado su nombre a 'Desconocido'*"
    pause 1.0
    $ recibir_mensaje("Desconocido", "Ya es tarde.")

    pause 1.0
    "*Usuario desconectado*"
    $ cerrar_app("chat")

    "¿Qué \"último día\"? "
    "Mi pecho... me duele muchísimo. Como si me estuvieran clavando agujas."
    "Me tiemblan las manos. Quiero llamarla al móvil de verdad, pero... tengo un miedo irracional a que nadie conteste."
    "Necesito dormir. Mañana la veré en el instituto y le pediré perdón en persona."

    $ mostrar_boton_finalizar = True
    jump bucle_pc


# ---------------- TRANSICIÓN DÍA 3 ----------------
label transicion_dia_3:
    hide screen escritorio_pc
    hide screen detector_webcam_noche2
    hide screen ventana_chat
    hide screen ventana_nota
    hide screen ventana_galeria
    hide screen ventana_musica
    hide screen ventana_webcam
    hide screen ventana_nota_turbia
    hide screen ventana_visor_fotos_raras
    
    python:
        for app in apps_pc:
            apps_pc[app]["abierta"] = False
            apps_pc[app]["minimizada"] = False
            
    $ mostrar_boton_finalizar = False

    window hide
    scene black with fade
    pause 1.0

    show expression Text("DÍA 3", font="gui/fonts/Micro5.ttf", size=150, color="#ffffff") as cartel_dia:
        xalign 0.5
        yalign 0.5
    with dissolve
    
    pause 3.0
    
    hide cartel_dia with dissolve

    # jump dia_3
    "Aquí empezará el Día 3..."
    return

# ---------------- DÍA 3 ----------------
label dia_3:
    $ estilo_interfaz = "dia_tetrico"
    $ default_mouse = "cursor_normal_mal"

    $ capitulo_actual = "dia_3"
    $ persistent.nube_capitulo = "dia_3" 
    $ persistent.nube_decisiones = decisiones_tomadas
    $ renpy.save_persistent()

    $ guardar_progreso(capitulo_actual, decisiones_tomadas)

    window show
    scene black with fade
    
    "Me he despertado, pero... siento que no he dormido nada."
    "Me pesa muchísimo el cuerpo. Cada vez me cuesta más llenar los pulmones de aire."
    "Anoche... lo de los mensajes de anoche fue una pesadilla. Tuvo que serlo. El estrés me está volviendo loco."
    "Hoy todo volverá a la normalidad. Seguro que Rocío me está esperando en la entrada del instituto, quejándose de que llego tarde como siempre."

    # *escenario del instituto de día pero está oscuro*
    scene fondo_patio2 with fade
    show expression "#00000088" as capa_oscura
    
    "Pero...no se supone que es de día?"
    "Qué es todo este ambiente tan oscuro? Y...porqué me duele el pecho?"
    
    v "TE ESTÁ ESPERANDO"
    v "INSTITUTO"
    
    "..."
    "Voy a buscarla"
    
    scene black with dissolve
    pause 1.0
    scene fondo_calle with dissolve
    show expression "#00000088" as capa_oscura
    
    "Qué raro."
    "No hay nadie."
    "Ni en la puerta, ni en el patio... no se escucha absolutamente nada. Cero voces. Cero pasos."
    "No. Las luces están encendidas, pero el aire se siente estancado. Huele fuerte a... ¿medicina? "
    "Es como si el mundo entero se hubiera congelado."
    
    y "¡¿Rocío?! ¡¿Hay alguien?!"
    # play sound "Musica/Efectos/eco_vacio.ogg"
    
    "Nada."
    "El pecho me vuelve a arder. Un pánico helado empieza a subir por mi garganta."
    "Esto no está bien. "
    "Tengo que encontrarla. Tengo que encontrar a Rocío ya mismo."
    "Tengo un muy mal presentimiento"

    scene black with dissolve
    pause 1.0
    # Aquí puedes usar una imagen de un aula a oscuras
    scene fondo_patio2 with dissolve 
    show expression "#000000cc" as capa_oscura
    
    "Uf.....uf......"
    "¿¡¿¡¿¡¿Pero qué leches está pasando?!?!?!?"
    "¿Porqué todo es tan oscuro? ¿Porqué no hay nadie?"
    "NO ENTIENDO NADA!!! "
    "Todo esto está pasado desde hace dos días..."
    "Ahhh.................."
    "..."
    "Iré a ver a la clase de Rocío a ver si está ahí"

    # *El aula con cables de hospital*
    scene fondo_escritorio_corrupto2 with fade
    
    "¿Qué hacen unos soportes de hospital en la clase?"
    "¿Y por qué el aire es tan pesado... tan frío?"
    y "R-Rocío... ¿eres tú?"

    # Muestra a la chica de espaldas o rota
    show chica rota with dissolve

    r "..."
    y "¿Estás bien?"
    y "¡Rocío, mírame! ¡Vámonos de aquí, este sitio me está dando pánico!"
    
    r "Ya no podemos irnos."
    r "Porque ya no te quedan fuerzas para mantener la mentira. "
    r "El 'Día 1', el 'Día 2'... Todo este mundo perfecto se está desmoronando."

    y "¿Qué? ¿De qué hablas? ¡Me estás asustando!"
    y "¡Vamos al médico, te duele la cabeza, ¿verdad?! ¡Te llevaré yo mismo!"

    show chica inexpresiva with dissolve

    r "A mí ya no me duele nada. "
    r "Pero a ti sí. Mírate el brazo izquierdo."

    play sound "Musica/Efectos/monitor_cardiaco.ogg"
    with hpunch
    
    y "¿Mi brazo? "
    y "¡Aaaah! ¡¿Qué es esto?!"
    y "Tengo... tengo una vía intravenosa clavada en el brazo. La sangre está subiendo por el tubo hacia la oscuridad del techo. ¡¿En qué momento ha aparecido esto?!"

    y "¡Rocío, ayúdame! ¡Quítame esto!"
    r "No puedo. "
    r "Y tú tampoco puedes solo. Estás atrapado."

    stop sound
    
    r "Pero no estamos solos, ¿verdad?"
    y "¿Con quién hablas?"
    r "Hablo con quien te está guiando."
    
    # Ruptura de la 4ª pared
    play sound "Musica/Efectos/glitch.ogg"
    with vpunch
    
    r "Sé que me estás escuchando."
    r "Él está demasiado asustado, pero tú puedes ver la verdad."
    r "Te acabo de enviar un mensaje. Búscalo."

    # ENVÍO DEL SEGUNDO CORREO REAL
    $ enviar_correo_real(pc_email)
    
    y "¿Un mensaje? ¡Rocío, no tengo el móvil encima!"
    r "No a ti tonto"

    y "Se ha vuelto loca... Todo el mundo se ha vuelto loco."
    y "Seguro que esto es un sueño...SÍ, debe serlo."
    y "¡Ayer fuimos a la cafetería! ¡Te vi allí, te reíste conmigo y hablamos de ir a la universidad!"
    
    r "..."
    r "Seguro que todo eso fue real?"
    
    with hpunch
    y "CÁLLATE!!! Cállate, por favor..."
    y "Me tapo los oídos con fuerza, pero su voz resuena dentro de mi cráneo."
    y "Las lágrimas me queman los ojos. Las enredaderas secas de las paredes parecen acercarse a mí, asfixiándome."
    
    r "Mírame. "
    r "Sé que duele. Sé que la culpa te está destrozando. Pero esconderte aquí conmigo no va a cambiar lo que pasó."
    r "Tienes que soltarme."

    y "Siento que me desvanezco. Mi mente se está partiendo en dos."
    y "Una parte de mí me grita que cierre los ojos y haga como que no he visto nada."
    y "La otra parte... la otra parte sabe..."
    
    v "¿POR FIN DEJARÁS DE HUIR?"
    v "¿POR FIN TERMINARÁS ESTO?"
    
    y "Eh?! Pero...qué es esto??"
    y "Parece...que olvidé algo importante y...estoy tratando de recordar."
    y "Dentro de mí... sé qué pasó ese 'último día'..."

    r "Es la hora. "
    r "¿Vas a seguir jugando conmigo, o vas a abrir los ojos de verdad?"

    menu:
        "Cerrar los ojos. Por favor, Rocío... deja de decir estupideces":
            jump final_neutro
        "Necesito recordar qué pasó esa noche... Ayúdame, Rocío":
            jump despertar

# ---------------- FINALES ----------------

label final_neutro:
    y "No puedo... No puedo soportarlo. "
    y "Por favor, Rocío. Deja ya de decir tonterías. No puedo más con esta broma de mal gusto."
    y "Mañana iremos de nuevo a esa cafetería o incluso podemos ir al karaoke juntos."
    y "Hoy...hoy está pasando algo muy raro, y a tí también!!"
    y "Mejor volvamos los dos a casa anda."

    scene black with fade
    r "...Como quieras."
    r "Descansa....."

    $ estilo_interfaz = "dia_normal"
    $ persistent.final_alcanzado = "neutro"
    
    # Música distorsionada
    play music "Musica/Efectos/cancion3.ogg"
    
    scene fondo_cafeteria with fade
    show chica hablando with dissolve
    
    y "Hey!! Hola Rocío, hoy habíamos decidido ir al café ese nuevo verdad?"
    y "Ya te dije que no te dejaría plantanda."
    
    show chica inexpresiva
    r "..."
    r "*susurra* Cobarde"
    y "Em? Dijiste algo?"
    
    show chica sonriendo
    r "Nope, nada de nada. Vayamos antes de que cierren."
    
    scene black with fade
    show expression Text("FINAL NEUTRO\nMundo Falso", font="gui/fonts/Micro5.ttf", size=100, color="#ffffff") as cartel at truecenter
    pause 4.0
    return

label despertar:
    y "..."
    y "Lo siento..."
    y "En realidad... yo ya lo sabía desde un principio, solo... solo que lo negaba."
    y "No quería darme cuenta de la realidad y... pasó todo esto."
    
    r "..."
    r "Me trataste de llamar luego, pero... ya era tarde."
    r "Para ese entonces las pastillas ya me habían quemado por dentro."
    y "..."
    r "Cuando te enteraste al día siguiente... te diste cuenta de que mis llamadas eran gritos de auxilio."
    r "Las ignoraste por estar mirando una pantalla. "
    r "Y al no poder soportar el peso de esa culpa... tú también buscaste una salida desesperada en la oscuridad de tu cuarto."

    y "De repente, la barrera en mi mente estalla en mil pedazos."
    y "Los recuerdos me golpean sin piedad, crudos y reales."
    y "La sirena de la ambulancia... el llanto desgarrador de tu madre al teléfono al darme la noticia... "
    y "Y luego... yo. Tirado en el suelo de mi habitación."
    y "Recuerdo el frío repentino... el dolor agudo antes de que todo empezara a volverse borroso... antes de que el mundo se apagara."

    play sound "Musica/Efectos/glitch.ogg"
    with vpunch
    
    y "Duele... Me quema. Siento que me ahogo de verdad en mi propia culpa."

    r "Se acabó el tiempo."
    r "La jaula de cristal se ha roto. "
    r "Es hora de abrir los ojos y enfrentar el desastre que dejaste al otro lado."

    scene white with fade
    stop music

    if puntos_mentira >= puntos_verdad:
        jump final_malo
    else:
        jump final_bueno


label final_malo:
    $ persistent.final_alcanzado = "malo"
    play sound "Musica/Efectos/monitor_cardiaco.ogg" loop
    
    scene black with fade
    y "Abro los ojos de golpe. La luz blanca del hospital me perfora las retinas."
    y "Una enfermera entra corriendo en la habitación. Siento cómo me arrancan un tubo de la garganta mientras me ahogo tosiendo."
    y "Físicamente he sobrevivido, pero... mi alma se apagó ese 'último día'."
    y "Durante todo mi coma me dediqué a huir de la verdad. Fui un cobarde en mis sueños y lo sigo siendo ahora."
    
    stop sound # Se paran los médicos, solo queda el pitido
    
    y "Llevo horas solo en esta habitación."
    y "Ah...........no sé ni porqué sigo vivo, es mi culpa que ella..."
    y "..."
    y "No merezco seguir viviendo habiéndome comportado como un imbécil..."
    y "Miro la vía intravenosa en mi brazo... la misma que vi en mi sueño. Y los cables del monitor."
    y "Lo siento, Rocío... Espero que así puedas perdonarme..."
    
    play sound "Musica/Efectos/puerta_cerrando.mp3" # O un sonido de cables desconectándose
    with hpunch
    
    # Pitido plano
    # play sound "Musica/Efectos/flatline.ogg"
    
    show expression Text("FINAL MALO\nCulpa", font="gui/fonts/Micro5.ttf", size=100, color="#ffffff") as cartel at truecenter
    pause 4.0
    return


label final_bueno:
    $ persistent.final_alcanzado = "bueno"
    play sound "Musica/Efectos/monitor_cardiaco.ogg" loop
    
    scene black with fade
    y "Abro los ojos con pesadez. El olor a desinfectante inunda mis pulmones."
    y "Llevo horas en esta cama de hospital, mirando al techo blanco."
    y "Me duele cada respiración. La culpa sigue ahí, recordándome que le fallé cuando más me necesitaba."

    # play sound "Musica/Efectos/vibracion_movil.ogg"
    
    y "Giro la cabeza. Han dejado mis cosas ahí."
    y "Agarro el móvil. Las manos me tiemblan."
    y "Es... un mensaje programado. Un correo."
    y "¿¡De ROCÍO!?"
    y "*abro el mensaje, preparándome para leer cuánto me odiaba al final*"

    # Cambia el nombre en la caja de diálogo para simular el móvil
    r "Hola, tonto. Si estás leyendo esto, es que ya no estoy."
    r "Sé que no contestaste mis llamadas. Sé que estabas en tu mundo. Y está bien."
    r "No podías salvarme siempre. Mi cabeza era mi propio laberinto y yo ya no quería buscar la salida."
    r "Te escribo esto para que no te atrevas a culparte por no estar en mi último minuto."
    r "Quiero darte las gracias por haber estado todos los días anteriores. Fuiste mi lugar seguro."
    r "Me hiciste muy feliz."
    r "Adiós. Vive mucho por mí, ¿vale?"

    y "..."
    y "Leo el mensaje una vez. Y otra. Y otra."
    y "Y de repente... la enorme roca que me aplastaba el pecho... se rompe."
    y "Las lágrimas caen sobre la pantalla, pero ya no son lágrimas de culpa. Son de tristeza. La echo de menos."
    y "Cierro los ojos, y por fin lo entiendo. "
    y "Yo no fui su verdugo."
    
    y "Suelto el móvil sobre la cama."
    y "Levanto mi mano débil y miro por la ventana."
    y "La luz inunda la habitación, dándome un calor que hacía días que no sentía."
    y "La echaré de menos todos los días de mi vida. Me dolerá su ausencia."
    y "Pero ya no voy a castigarme más."
    y "Te lo prometo, Rocío. Viviré por los dos."

    # play music "Musica/Efectos/cancion1.ogg" fadein 2.0
    scene white with fade
    
    show expression Text("FINAL BUENO\nPerdón", font="gui/fonts/Micro5.ttf", size=100, color="#000000") as cartel at truecenter
    pause 4.0
    return

# --- ETIQUETAS DE BUCLE POST-JUEGO ---
label bucle_postgame_neutro:
    $ estilo_interfaz = "dia_normal"
    play music "Musica/Efectos/cancion3.ogg"
    scene fondo_cafeteria
    show chica hablando
    window show
    y "Ah... qué tarta más rica..."
    r "Siempre dices lo mismo. Nunca cambiamos."
    y "Ni falta que hace."
    scene black with fade
    pause 1.0
    jump bucle_postgame_neutro

label bucle_postgame_malo:
    scene black
    # play sound "Musica/Efectos/flatline.ogg"
    pause 3.0
    return

label bucle_postgame_bueno:
    scene black
    show expression Text("VIVE", font="gui/fonts/Micro5.ttf", size=150, color="#ffffff") as cartel at truecenter
    pause 5.0
    return