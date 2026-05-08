
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

# Variables chica
image chica comiendo = "images/diurna/modelos_chica/chica_comiendo.png"
image chica inexpresiva = "images/diurna/modelos_chica/chica_inexpresiva.png"
image chica inquieta = "images/diurna/modelos_chica/chica_inquieta.png"
image chica llorando = "images/diurna/modelos_chica/chica_llorando.png"
image chica orgullosa = "images/diurna/modelos_chica/chica_orgullosa.png"
image chica pensando = "images/diurna/modelos_chica/chica_pensando.png"
image chica rota = "images/diurna/modelos_chica/chica_rota.png"
image chica hablando = "images/diurna/modelos_chica/chica_hablando.png"
image chica molesta = "images/diurna/modelos_chica/chica_molesta.png"
image chica molesta2 = "images/diurna/modelos_chica/chica_molesta2.png"
image chica resoplando = "images/diurna/modelos_chica/chica_resoplando.png"
image chica molestaBroma = "images/diurna/modelos_chica/chica_molestaBroma.png"
image chica reverencia = "images/diurna/modelos_chica/chica_reverencia.png"
image chica riendo = "images/diurna/modelos_chica/chica_riendo.png"
image chica apenada = "images/diurna/modelos_chica/chica_apenada.png"

# Definicion de personajes
define r = Character("Rocío")
define y = Character("Yo")

# Variables de Puntos Finales
default puntos_mentira = 0
default puntos_verdad = 0

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

    show expression Text("DÍA 1 (escena diurna)", font="gui/fonts/Micro5.ttf", size=150, color="#ffffff") as cartel_dia:
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

    # poner música alegre 

    scene fondo_patio2:
        xysize (1430, 700) 
        xalign 0.5  
        yalign 0.2 
    with fade 

    show chica resoplando:
        xalign 0.5      
        yalign 1.0      
        yoffset -280     
        zoom 2.0    
    with dissolve

    r "Ahhhhhhhhhhhhhhh por fin terminaron los exámenes!!!!!!!!!"
    
    show chica hablando
    r "Ya somos libres al fin"
    
    y "Jajajaja por fin eh! fueron dos semanas intensas pero ya podemos olvidarnos un tiempo de todo."
    
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

    jump dia_1_escenaNoche

label dia_1_escenaNoche:
    