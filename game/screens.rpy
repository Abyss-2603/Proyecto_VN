################################################################################
## Inicialización
################################################################################

init offset = -1

# Definicion de interfaces del chat
init:
    image frame_yo = Frame("images/escritorioPC/frame_chat1.png", 60, 80, 40, 60)
    image frame_amiga = Frame("images/escritorioPC/frame_chat2.png", 60, 80, 40, 60)
    image frame_eleccion = Frame("images/escritorioPC/frame_decisiones_chat.png", 30, 30, 30, 30)
################################################################################
## Estilos
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

## Transformación para convertir imágenes gigantes en miniaturas
transform miniatura_galeria:
    xysize (360, 203)  # Forzamos un tamaño pequeño (formato 16:9)
    fit "cover"          # Esto asegura que la imagen rellene el hueco sin deformarse

################################################################################
## Pantallas internas del juego
################################################################################

## Pantalla de diálogo #########################################################
##
## La pantalla de diálogo muestra el diálogo al jugador. Acepta dos parámetros,
## 'who' y 'what', es decir, el nombre del personaje que habla y el texto que ha
## de ser mostrado respectivamente. (El parámetro 'who' puede ser 'None' si no
## se da ningún nombre.)
##
## Esta pantalla debe crear un texto visualizable con id "what" que Ren'Py usa
## para gestionar la visualización del texto. Puede crear también visualizables
## con id "who" y id "window" para aplicar propiedades de estilo.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## Si hay una imagen lateral, la muestra encima del texto. No la muestra en
    ## la variante de teléfono - no hay lugar.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Permite que el 'namebox' pueda ser estilizado en el objeto 'Character'.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Pantalla de introducción de texto ###########################################
##
## Pantalla usada para visualizar 'renpy.input'. El parámetro 'prompt' se usa
## para pasar el texto presentado.
##
## Esta pantalla debe crear un displayable 'input' con id "input" para aceptar
## diversos parámetros de entrada.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Pantalla de menú ############################################################
##
## Esta pantallla presenta las opciones internas al juego de la sentencia
## 'menu'. El parámetro único, 'items', es una lista de objetos, cada uno los
## campos 'caption' y 'action'.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Pantalla de menú rápido #####################################################
##
## El menú rápido se presenta en el juego para ofrecer fácil acceso a los menus
## externos al juego.

screen quick_menu():

    ## Asegura que esto aparezca en la parte superior de otras pantallas.
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"
            style "quick_menu"

            textbutton _("Atrás") action Rollback()
            textbutton _("Historial") action ShowMenu('history')
            textbutton _("Saltar") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Guardar") action ShowMenu('save')
            textbutton _("Guardar R.") action QuickSave()
            textbutton _("Cargar R.") action QuickLoad()
            textbutton _("Prefs.") action ShowMenu('preferences')


## Este código asegura que la pantalla 'quick_menu' se muestra en el juego,
## mientras el jugador no haya escondido explícitamente la interfaz.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_menu is hbox
style quick_button is default
style quick_button_text is button_text

style quick_menu:
    xalign 0.5
    yalign 1.0

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Principal y Pantalla de menu del juego.
################################################################################

## Pantalla de navegación ######################################################
##
## Esta pantalla está incluída en el menú principal y los menús del juego y
## ofrece navegación a los otros menús y al inicio del juego.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing


        # textbutton _("Comenzar") action Start()


        textbutton _("Historial") action ShowMenu("history")

        # textbutton _("Guardar") action ShowMenu("save")

        # textbutton _("Cargar") action ShowMenu("load")

        textbutton _("Opciones") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("Finaliza repetición") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Menú principal") action MainMenu()

        textbutton _("Acerca de") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## La ayuda no es necesaria ni relevante en dispositivos móviles.
            textbutton _("Ayuda") action ShowMenu("help")

        if renpy.variant("pc"):

            ## El botón de salida está prohibido en iOS y no es necesario en
            ## Android y Web.
            textbutton _("Salir") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")
    idle_color "#444444"   
    hover_color "#000000" 
    font "gui/fonts/VT323.ttf"


## Pantalla del menú principal #################################################
##
## Usado para mostrar el menú principal cuando Ren'Py arranca.
screen main_menu():

    ## Esto asegura que cualquier otra pantalla de menu es remplazada.
    tag menu

    ## 1. EL FONDO
    add "fondo_video_menu":
        xysize (1920, 1080)
        fit "cover"

    ## 2. EL TÍTULO
    text "Proyecto WASD":
        font "gui/fonts/Micro5.ttf"
        size 150
        color "#ffffff"
        xalign 0.5
        ypos 100
        outlines [(4, "#000000", 0, 0)]

    ## 3. LOS BOTONES 
    vbox:
        xalign 0.5
        yalign 0.6
        spacing 20
        
        if capitulo_actual == "prologo" or capitulo_actual == "":
            textbutton "Iniciar Sincro" action ShowMenu("confirmacion_inicio") text_style "menu_texto" style "menu_caja"
        else:
            textbutton "Iniciar Sincro" action Start() text_style "menu_texto" style "menu_caja"

        textbutton "Eliminar Sincro" action ShowMenu("confirmacion_borrar_cuenta") text_style "menu_texto" style "menu_caja"
        textbutton "Galería" action ShowMenu("gallery") text_style "menu_texto" style "menu_caja"
        textbutton "Opciones" action ShowMenu("preferences") text_style "menu_texto" style "menu_caja"
        textbutton "Salir" action Quit(confirm=not main_menu) text_style "menu_texto" style "menu_caja"

# PANTALLA DE ADVERTENCIA PARA BORRAR CUENTA 
screen confirmacion_borrar_cuenta():
    tag menu
    modal True 

    ## 1. Fondo
    add "images/menus/fondo_menu.png":
        xysize(1920, 1080)

    ## 2. EL CONTENEDOR TRANSPARENTE
    frame:
        background Solid("#110000dd")
        xalign 0.5
        yalign 0.5
        xsize 1100
        padding (60, 60)

        ## 3. CONTENIDO
        vbox:
            xalign 0.5
            spacing 20

            text "ADVERTENCIA CRÍTICA" xalign 0.5 font "gui/fonts/Micro5.ttf" size 80 color "#ff0000" outlines [(2, "#000000", 0, 0)]
            text "Estás a punto de romper el ciclo." xalign 0.5 font "gui/fonts/Micro5.ttf" size 50 color "#ffffff" outlines [(2, "#000000", 0, 0)]
            text "Esto borrará tu usuario y todo tu progreso de los\nservidores de forma PERMANENTE." xalign 0.5 text_align 0.5 font "gui/fonts/Micro5.ttf" size 50 color "#aaaaaa" outlines [(2, "#000000", 0, 0)]
            
            null height 30
            
            text "¿Ejecutar autodestrucción?" xalign 0.5 font "gui/fonts/Micro5.ttf" size 60 color "#ff0000" outlines [(2, "#000000", 0, 0)] 

            null height 20

            # --- LOS BOTONES ---
            hbox:
                xalign 0.5
                spacing 150 

                # BOTÓN CANCELAR
                textbutton "CANCELAR":
                    text_font "gui/fonts/Micro5.ttf"
                    text_size 60
                    text_color "#ffffff"
                    text_hover_color "#555555"
                    action Return() # vuelve al menu 
                    
                # BOTÓN ELIMINAR
                textbutton "ELIMINAR SINCRO":
                    text_font "gui/fonts/Micro5.ttf"
                    text_size 60
                    text_color "#ff0000"
                    text_hover_color "#ffffff"

                    action Start("ejecutar_borrado_cuenta")

## ESTILOS PERSONALIZADOS PARA MENÚ
## 1. ESTILO PARA LA CAJA
style menu_caja:
    xsize 600               
    ysize 70
    xalign 0.5                 
    ypadding 0              
    hover_background Solid("#333333") 
    hover_yoffset 4
    

## 2. ESTILO PARA EL TEXTO
style menu_texto:
    font "gui/fonts/Micro5.ttf"
    size 70
    color "#aaaaaa"
    hover_color "#ffffff"
    outlines [(2, "#000000", 0, 0)]
    
    xalign 0.5                 
    text_align 0.5             

## --- PANTALLA DE AVISO ---
screen aviso_legal():

    modal True

    ## 1. El Fondo
    add "images/menus/fondo_menu.png": 
        xysize(1920, 1080)

    ## 2. El cuadro negro central
    frame:
        background "#000000" 
        xalign 0.5
        yalign 0.5
        padding (80, 60) 
        xsize 1000  

        vbox:
            spacing 40
            xalign 0.5

            text "Aviso":
                font "gui/fonts/Jacquard24.ttf"
                size 110
                color "#ffffff"
                xalign 0.5

            text ("Este juego recopilará y almacenará algunos de los datos "
                "introducidos por el jugador con el fin de mejorar la experiencia de juego.\n\n"
                "Al continuar, aceptas que los datos introducidos (como dirección de "
                "correo electrónico u otra información) podrán ser utilizados dentro "
                "de la experiencia interactiva.\n"
                "¿Deseas continuar?"):
                font "gui/fonts/Jacquard24.ttf"
                size 45
                color "#ffffff"
                text_align 0.5
                layout "subtitle"
                xalign 0.5

            imagebutton:
                idle Transform("images/menus/boton_aceptar_blanco.png", zoom=0.2)
                hover Transform ("images/menus/boton_aceptar_rojo.png", zoom=0.2)
    
                focus_mask True

                action Return()
                xalign 0.5

#Pantalla de galería 
screen gallery():
    tag menu

    ## 1. Fondo
    add "fondo_video_menu":
        xysize (1920, 1080)
        fit "cover"

    ## 2. Título
    text "Galería de Imágenes":
        font "gui/fonts/Jacquard24.ttf"
        size 90
        xalign 0.5
        ypos 50
        color "#ffffff"
        outlines [(3, "#000000", 0, 0)]

    ## 3. EL MARCO GRIS (Contenedor)
    frame:
        background Solid("#000000aa")
        xalign 0.5
        yalign 0.55
        padding (40, 40) 
        
        ## LA CUADRÍCULA
        grid 4 2:
            spacing 30 
            
            # --- IMAGEN 1 ---
            vbox: 
                xalign 0.5 
                spacing 10
                
                # Botón
                if renpy.seen_image("cg1"):
                    add g.make_button("cg1", "images/cg1_mini.png") at miniatura_galeria
                else:
                    imagebutton idle "images/menus/boton_block.png" hover "images/menus/boton_block_seleccionado.png" action NullAction() at miniatura_galeria
                
                text "Imagen 1":
                    font "gui/fonts/Jacquard24.ttf"
                    size 40
                    color "#ffffff"
                    xalign 0.5 

            # --- IMAGEN 2 ---
            vbox:
                xalign 0.5
                spacing 10
                if renpy.seen_image("cg2"):
                    add g.make_button("cg2", "images/cg2_mini.png") at miniatura_galeria
                else:
                    imagebutton idle "images/menus/boton_block.png" hover "images/menus/boton_block_seleccionado.png" action NullAction() at miniatura_galeria
                
                text "Imagen 2":
                    font "gui/fonts/Jacquard24.ttf"
                    size 40
                    color "#ffffff"
                    xalign 0.5

            # --- IMAGEN 3 ---
            vbox:
                xalign 0.5
                spacing 10
                if renpy.seen_image("cg3"):
                    add g.make_button("cg3", "images/cg3_mini.png") at miniatura_galeria
                else:
                    imagebutton idle "images/menus/boton_block.png" hover "images/menus/boton_block_seleccionado.png" action NullAction() at miniatura_galeria
                
                text "Imagen 3":
                    font "gui/fonts/Jacquard24.ttf"
                    size 40
                    color "#ffffff"
                    xalign 0.5

            # --- IMAGEN 4 ---
            vbox:
                xalign 0.5
                spacing 10
                if renpy.seen_image("cg4"):
                    add g.make_button("cg4", "images/cg4_mini.png") at miniatura_galeria
                else:
                    imagebutton idle "images/menus/boton_block.png" hover "images/menus/boton_block_seleccionado.png" action NullAction() at miniatura_galeria
                
                text "Imagen 4":
                    font "gui/fonts/Jacquard24.ttf"
                    size 40
                    color "#ffffff"
                    xalign 0.5

            # --- IMAGEN 5 ---
            vbox:
                xalign 0.5
                spacing 10
                if renpy.seen_image("cg5"):
                    add g.make_button("cg5", "images/cg5_mini.png") at miniatura_galeria
                else:
                    imagebutton idle "images/menus/boton_block.png" hover "images/menus/boton_block_seleccionado.png" action NullAction() at miniatura_galeria
                
                text "Imagen 5":
                    font "gui/fonts/Jacquard24.ttf"
                    size 40
                    color "#ffffff"
                    xalign 0.5

            # --- IMAGEN 6 ---
            vbox:
                xalign 0.5
                spacing 10
                if renpy.seen_image("cg6"):
                    add g.make_button("cg6", "images/cg6_mini.png") at miniatura_galeria
                else:
                    imagebutton idle "images/menus/boton_block.png" hover "images/menus/boton_block_seleccionado.png" action NullAction() at miniatura_galeria
                
                text "Imagen 6":
                    font "gui/fonts/Jacquard24.ttf"
                    size 40
                    color "#ffffff"
                    xalign 0.5

            # --- IMAGEN 7 ---
            vbox:
                xalign 0.5
                spacing 10
                if renpy.seen_image("cg7"):
                    add g.make_button("cg7", "images/cg7_mini.png") at miniatura_galeria
                else:
                    imagebutton idle "images/menus/boton_block.png" hover "images/menus/boton_block_seleccionado.png" action NullAction() at miniatura_galeria
                
                text "Imagen 7":
                    font "gui/fonts/Jacquard24.ttf"
                    size 40
                    color "#ffffff"
                    xalign 0.5

            # --- IMAGEN 8 ---
            vbox:
                xalign 0.5
                spacing 10
                if renpy.seen_image("cg8"):
                    add g.make_button("cg8", "images/cg8_mini.png") at miniatura_galeria
                else:
                    imagebutton idle "images/menus/boton_block.png" hover "images/menus/boton_block_seleccionado.png" action NullAction() at miniatura_galeria
                
                text "Imagen 8":
                    font "gui/fonts/Jacquard24.ttf"
                    size 40
                    color "#ffffff"
                    xalign 0.5

    ## 4. BOTÓN VOLVER
    imagebutton:        
        idle Transform("images/menus/boton_volver_blanco.png", zoom=1)
        hover Transform("images/menus/boton_volver_rojo.png", zoom=1)
        focus_mask True
        action Return()
        xalign 0.5 
        yalign 0.95

## Pantalla del menú del juego #################################################
##
## Esto distribuye la estructura de base del menú del juego. Es llamado con el
## título de la pantalla y presenta el fondo, el título y la navegación.
##
## El parámetro 'scroll' puede ser 'None', "viewport" o "vpgrid". Se usa esta
## pantalla con uno o más elementos, que son transcluídos (situados) en su
## interior.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reservar espacio para la sección de navegación.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Volver"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    padding (0, 0)
    margin (0, 0)
    background Solid("#d6d6d6") 

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 60
    top_margin 100

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size 75
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## Pantalla 'acerca de' ########################################################
##
## Esta pantalla da información sobre los créditos y el copyright del juego y de
## Ren'Py.
##
## No hay nada especial en esta pantalla y por tanto sirve también como ejemplo
## de cómo hacer una pantalla personalizada.

screen about():

    tag menu

    ## Esta sentencia 'use' incluye la pantalla 'game_menu' dentro de esta. El
    ## elemento 'vbox' se incluye entonces dentro del 'viewport' al interno de
    ## la pantalla 'game_menu'.
    use game_menu(_("Acerca de"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Versión [config.version!t]\n")

            ## 'gui.about' se ajusta habitualmente en 'options.rpy'.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Hecho con {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Pantallas de carga y grabación ##############################################
##
## Estas pantallas permiten al jugador grabar el juego y cargarlo de nuevo. Como
## comparten casi todos los elementos, ambas están implementadas en una tercera
## pantalla: 'file_slots'.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Guardar"))


screen load():

    tag menu

    use file_slots(_("Cargar"))

# En vez de los slots de guardado
screen file_slots(title):
    use game_menu(title):
        fixed:
            vbox:
                xpos 500  
                ypos 150
                spacing 30
                
                text "ESTADO DE LA SINCRONIZACIÓN":
                    font "gui/fonts/Micro5.ttf" 
                    size 80 
                    color "#333333" 
                
                vbox:
                    spacing 10
                    text "Estado de la Partida: [capitulo_actual]":
                        font "gui/fonts/VT323.ttf" 
                        size 45 
                        color "#555555"
                    
                    text "Progreso guardado automáticamente.":
                        font "gui/fonts/VT323.ttf" 
                        size 28 
                        color "#777777"



style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5
    xalign 0.5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## Pantalla de preferencias ####################################################
##
## La pantalla de preferencias permite al jugador configurar el juego a su
## gusto.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Opciones"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Pantalla")
                        textbutton _("Ventana") action Preference("display", "window")
                        textbutton _("Pantalla completa") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Saltar")
                    textbutton _("Texto no visto") action Preference("skip", "toggle")
                    textbutton _("Tras elecciones") action Preference("after choices", "toggle")
                    textbutton _("Transiciones") action InvertSelected(Preference("transitions", "toggle"))

                ## Aquí se pueden añadir 'vboxes' adicionales del tipo
                ## "radio_pref" o "check_pref" para nuevas preferencias.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Veloc. texto")

                    bar value Preference("text speed")

                    label _("Veloc. autoavance")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Volumen música")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Volumen sonido")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Prueba") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Volumen voz")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Prueba") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Silenciar todo"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## Pantalla de historial #######################################################
##
## Esta pantalla presenta el historial de diálogo al jugador, almacenado en
## '_history_list'.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Evita la predicción de esta pantalla, que podría ser demasiado grande.
    predict False

    use game_menu(_("Historial"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## Esto distribuye los elementos apropiadamente si
                ## 'history_height' es 'None'.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Toma el color del texto 'who' de 'Character', si ha
                        ## sido establecido.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("El historial está vacío.")


## Esto determina qué etiquetas se permiten en la pantalla de historial.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Pantalla de ayuda ###########################################################
##
## Una pantalla que da información sobre el uso del teclado y el ratón. Usa
## otras pantallas con el contenido de la ayuda ('keyboard_help', 'mouse_help',
## y 'gamepad_help').

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Ayuda"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Teclado") action SetScreenVariable("device", "keyboard")
                textbutton _("Ratón") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Mando") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Intro")
        text _("Avanza el diálogo y activa la interfaz.")

    hbox:
        label _("Espacio")
        text _("Avanza el diálogo sin seleccionar opciones.")

    hbox:
        label _("Teclas de flecha")
        text _("Navega la interfaz.")

    hbox:
        label _("Escape")
        text _("Accede al menú del juego.")

    hbox:
        label _("Ctrl")
        text _("Salta el diálogo mientras se presiona.")

    hbox:
        label _("Tabulador")
        text _("Activa/desactiva el salto de diálogo.")

    hbox:
        label _("Av. pág.")
        text _("Retrocede al diálogo anterior.")

    hbox:
        label _("Re. pág.")
        text _("Avanza hacia el diálogo siguiente.")

    hbox:
        label "H"
        text _("Oculta la interfaz.")

    hbox:
        label "S"
        text _("Captura la pantalla.")

    hbox:
        label "V"
        text _("Activa/desactiva la asistencia por {a=https://www.renpy.org/l/voicing}voz-automática{/a}.")

    hbox:
        label "Shift+A"
        text _("Abre el menú de accesibilidad.")


screen mouse_help():

    hbox:
        label _("Clic izquierdo")
        text _("Avanza el diálogo y activa la interfaz.")

    hbox:
        label _("Clic medio")
        text _("Oculta la interfaz.")

    hbox:
        label _("Clic derecho")
        text _("Accede al menú del juego.")

    hbox:
        label _("Rueda del ratón arriba")
        text _("Retrocede al diálogo anterior.")

    hbox:
        label _("Rueda del ratón abajo")
        text _("Avanza hacia el diálogo siguiente.")


screen gamepad_help():

    hbox:
        label _("Gatillo derecho\nA/Botón inferior")
        text _("Avanza el diálogo y activa la interfaz.")

    hbox:
        label _("Gatillo izquierdo\nBotón sup. frontal izq.")
        text _("Retrocede al diálogo anterior.")

    hbox:
        label _("Botón sup. frontal der.")
        text _("Avanza hacia el diálogo siguiente.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navega la interfaz.")

    hbox:
        label _("Inicio, Guía, B/Botón Derecho")
        text _("Accede al menú del juego.")

    hbox:
        label _("Y/Botón superior")
        text _("Oculta la interfaz.")

    textbutton _("Calibrar") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Pantallas adicionales
################################################################################


## Pantalla de confirmación ####################################################
##
## Ren'Py llama la pantalla de confirmación para presentar al jugador preguntas
## de sí o no.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Asegura que otras pantallas no reciban entrada mientras se muestra esta
    ## pantalla.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Sí") action yes_action
                textbutton _("No") action no_action

    ## Clic derecho o escape responden "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Pantalla del indicador de salto #############################################
##
## La pantalla de indicador de salto se muestra para indicar que se está
## realizando el salto.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Saltando")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## Esta transformación provoca el parpadeo de las flechas una tras otra.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## Es necesario usar un tipo de letra que contenga el glifo BLACK RIGHT-
    ## POINTING SMALL TRIANGLE.
    font "DejaVuSans.ttf"


## Pantalla de notificación ####################################################
##
## La pantalla de notificación muestra al jugador un mensaje. (Por ejemplo, con
## un guardado rápido o una captura de pantalla.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## Pantalla NVL ################################################################
##
## Esta pantalla se usa para el diálogo y los menús en modo NVL.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Presenta el diálogo en una 'vpgrid' o una 'vbox'.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Presenta el menú, si lo hay. El menú puede ser presentado
        ## incorrectamente si 'config.narrator_menu' está ajustado a 'True'.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## Esto controla el número máximo de entradas en modo NVL que pueden ser
## mostradas de una vez.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Pantalla de globos ##########################################################
##
## La pantalla de burbujas se utiliza para mostrar el diálogo al jugador cuando
## se utilizan burbujas de diálogo. La pantalla de burbujas toma los mismos
## parámetros que la pantalla "say", debe crear un visualizable con el id de
## "what", y puede crear visualizables con los ids "namebox", "who", y "window".
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

        default ctc = None
        showif ctc:
            add ctc

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Variantes móviles
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Ya que puede carecer de ratón, se reempleza el menú rápido con una versión
## con menos botones y más grandes, más fáciles de tocar.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style "quick_menu"
            style_prefix "quick"

            textbutton _("Atrás") action Rollback()
            textbutton _("Saltar") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menú") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    padding (0, 0)     
    margin (0, 0)       
    background Solid("#d6d6d6")

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    left_margin 60
    right_margin 60    
    top_margin 100

style game_menu_viewport:
    variant "small"
    xsize 1305

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900


transform tamaño_boton_aviso:
    zoom 0.7  
    nearest True
##Pantalla de confirmacion de inicio ##
screen confirmacion_inicio():
    tag menu
    modal True 

    ## 1. Fondo de pantalla (Scanlines)
    add "images/menus/fondo_menu.png":
        xysize(1920, 1080)

    ## 2. EL CONTENEDOR TRANSPARENTE
    frame:
        background Solid("#000000aa")      
        xalign 0.5
        yalign 0.5
        xsize 1100
        padding (60, 60)

        ## 3. CONTENIDO
        vbox:
            xalign 0.5
            spacing 20

            # --- LOS TEXTOS ---
            text "Todo comienzo implica olvidar." xalign 0.5 font "gui/fonts/Micro5.ttf" size 50 color "#ffffff" outlines [(2, "#000000", 0, 0)]
            text "Lo que recuerdas ya no te pertenece." xalign 0.5 font "gui/fonts/Micro5.ttf" size 50 color "#ffffff" outlines [(2, "#000000", 0, 0)]
            text "Una nueva historia requiere un nuevo\ntú." xalign 0.5 text_align 0.5 font "gui/fonts/Micro5.ttf" size 50 color "#ffffff" outlines [(2, "#000000", 0, 0)]
            text "Tus decisiones definirán la persona que eres en realidad." xalign 0.5 text_align 0.5 font "gui/fonts/Micro5.ttf" size 50 color "#ffffff" outlines [(2, "#000000", 0, 0)]
            
            null height 30
            
            text "¿Deseas continuar?":
                xalign 0.5 
                font "gui/fonts/Micro5.ttf" 
                size 60 
                color "#ffffff" 
                outlines [(2, "#000000", 0, 0)] 

            null height 20

            # --- LOS BOTONES ---
            hbox:
                xalign 0.5
                spacing 80 

                # BOTÓN CANCELAR
                imagebutton:
                    idle "images/menus/boton_cancelar_blanco.png"
                    hover "images/menus/boton_cancelar_rojo.png"
                    action Return()
                    at tamaño_boton_aviso 
                    hover_yoffset 4

                # BOTÓN CONTINUAR
                imagebutton:
                    idle "images/menus/boton_continuar_blanco.png"
                    hover "images/menus/boton_continuar_rojo.png"
                    action Start()
                    at tamaño_boton_aviso
                    hover_yoffset 4

## PANTALLA DE REGISTRO
# --- FUNCIÓN DE SEGURIDAD (Variables) ---
init python:
    def check_vars_safe():
        if not hasattr(store, 'pc_usuario'): store.pc_usuario = ""
        if not hasattr(store, 'pc_email'): store.pc_email = ""
        if not hasattr(store, 'pc_pass'): store.pc_pass = ""
        if not hasattr(store, 'pc_pass_confirm'): store.pc_pass_confirm = ""

# --- ESTILOS ---
style texto_input_activo:
    font "gui/fonts/VT323.ttf"
    size 35
    color "#555555"
    xalign 0.0
    yalign 0.5
    adjust_spacing False

style texto_placeholder:
    font "gui/fonts/VT323.ttf"
    size 35
    color "#aaaaaa" 
    xalign 0.0
    yalign 0.5

style texto_valor_fijo:
    font "gui/fonts/VT323.ttf"
    size 35
    color "#555555" 
    xalign 0.0
    yalign 0.5

style caja_blanca_base:
    background Solid("#ffffff")
    xsize 600
    ysize 60
    padding (15, 0)
    xalign 0.5

transform icono_nota:
    xysize (60, 60)
    fit "contain"
    xalign 0.98
    yalign 0.5

transform estilo_bocadillo:
    zoom 0.5
    anchor (0.0, 1.0)
    xpos 590
    ypos -10
    on show:
        alpha 0.0 yoffset 20 
        easein 0.3 alpha 1.0 yoffset 0 
    on hide:
        easeout 0.2 alpha 0.0 yoffset 10 

transform aparicion_bocadillo:
    on show:
        alpha 0.0
        easein 0.2 alpha 1.0
    on hide:
        easeout 0.2 alpha 0.0

transform icono_externo:
    xysize (60, 60)
    fit "contain"
    xpos 610 
    yalign 0.5

transform estilo_bocadillo_externo:
    zoom 0.6
    anchor (0.0, 1.0)
    xpos 640
    ypos 10
    on show:
        alpha 0.0 yoffset 20 
        easein 0.3 alpha 1.0 yoffset 0 
    on hide:
        easeout 0.2 alpha 0.0 yoffset 10

# --- PANTALLA DE CARGA ---
screen cargando_servidor(tarea=""):
    zorder 100
    modal True
    
    if tarea == "registro":
        timer 0.1 action [Function(conectar_registro, pc_usuario, pc_email, pc_pass), Hide("cargando_servidor")]
    elif tarea == "login":
        timer 0.1 action [Function(conectar_login, pc_usuario, pc_pass), Hide("cargando_servidor")]
    elif tarea == "codigo":
        timer 0.1 action [Function(solicitar_codigo_api, pc_email), Hide("cargando_servidor")]
    elif tarea == "cambiar_pass":
        timer 0.1 action [Function(confirmar_nueva_password_api, pc_email, pc_codigo, pc_nueva_pass), Hide("cargando_servidor")]

    frame:
        align (0.5, 0.5)
        background Solid("#000000cc")
        padding (50, 30)
        
        vbox:
            spacing 15
            xalign 0.5
            text "Conectando con el servidor..." font "gui/fonts/VT323.ttf" size 40 color "#fff"
            text "Por favor, espera." font "gui/fonts/VT323.ttf" size 25 color "#aaa" xalign 0.5

# --- PANTALLA DE REGISTRO ---
screen registro_pc():
    modal True
    tag menu 

    # Controla quién tiene el turno para escribir.
    default foco_actual = "None"

    default mostrar_aviso = False

    on "show" action Function(check_vars_safe)

    add "images/inicio_sesion/imagen_login_fondo.png":
        xysize(1920, 1080)

    vbox:
        xalign 0.5
        yalign 0.35
        spacing 25

        add "images/inicio_sesion/imagen_login_perfil.png":
            xalign 0.5
            xysize (350, 350)
            fit "contain"
        
        text "Registro de Usuario":
            font "gui/fonts/VT323.ttf"
            size 50
            xalign 0.5
            color "#ffffff"

        null height 10

        # =========================================================
        # CAJA 1: USUARIO
        # =========================================================
        if foco_actual == "usuario":
            # ESTADO ACTIVO
            frame:
                style "caja_blanca_base"
                input value VariableInputValue("pc_usuario") style "texto_input_activo" length 15 xfill True yfill True
        else:
            # ESTADO INACTIVO
            button:
                style "caja_blanca_base"
                action SetScreenVariable("foco_actual", "usuario")
                
                if pc_usuario == "":
                    text "Nombre de Usuario" style "texto_placeholder"
                else:
                    text "[pc_usuario]" style "texto_valor_fijo"

        #==========================================================
        # CAJA 2: EMAIL
        # =========================================================
        fixed:
            xsize 600 ysize 60 xalign 0.5

            if foco_actual == "email":
                frame:
                    style "caja_blanca_base"
                    input value VariableInputValue("pc_email") style "texto_input_activo" length 40 xsize 600 yfill True
            else:
               
                button:
                    style "caja_blanca_base"
                    action SetScreenVariable("foco_actual", "email")
                    fixed:
                        yalign 0.5
                        if pc_email == "":
                            text "Correo Electrónico" style "texto_placeholder"
                        else:
                            text "[pc_email]" style "texto_valor_fijo"

            add "images/inicio_sesion/nota_login.png" at icono_externo

            mousearea:
                area (610, 0, 60, 60) 
                hovered SetScreenVariable("mostrar_aviso", True)
                unhovered SetScreenVariable("mostrar_aviso", False)

            if mostrar_aviso:
                add "images/inicio_sesion/icono_advertencia.png" at estilo_bocadillo_externo
        
        # =========================================================
        # CAJA 3: CONTRASEÑA 
        # =========================================================
        fixed:
            xsize 600 ysize 60 xalign 0.5

            if foco_actual == "pass":
                frame:
                    style "caja_blanca_base"
                    input value VariableInputValue("pc_pass") style "texto_input_activo" length 20 mask (None if ver_password else "*") xfill True yfill True
            else:
                button:
                    style "caja_blanca_base"
                    action SetScreenVariable("foco_actual", "pass")
                    if pc_pass == "":
                        text "Contraseña" style "texto_placeholder"
                    else:
                        text (pc_pass if ver_password else "*" * len(pc_pass)) style "texto_valor_fijo"

            # --- Boton ojo ---
            imagebutton:
                xpos 615 # Lo colocamos flotando a la derecha de la caja
                yalign 0.5
                idle ("images/inicio_sesion/ojo_abierto.png" if ver_password else "images/inicio_sesion/ojo_cerrado.png")
                at transform:
                    xysize(50, 50)
                mouse "pc_select" 
                action ToggleVariable("ver_password")

        # =========================================================
        # CAJA 4: CONFIRMAR
        # =========================================================
        fixed:
            xsize 600 ysize 60 xalign 0.5

            if foco_actual == "confirm":
                frame:
                    style "caja_blanca_base"
                    input value VariableInputValue("pc_pass_confirm") style "texto_input_activo" length 20 mask (None if ver_password else "*") xfill True yfill True
            else:
                button:
                    style "caja_blanca_base"
                    action SetScreenVariable("foco_actual", "confirm")
                    if pc_pass_confirm == "":
                        text "Confirmar Contraseña" style "texto_placeholder"
                    else:
                        text (pc_pass_confirm if ver_password else "*" * len(pc_pass_confirm)) style "texto_valor_fijo"

            # --- Boton ojo ---
            imagebutton:
                xpos 615 # Lo colocamos flotando a la derecha
                yalign 0.5
                idle ("images/inicio_sesion/ojo_abierto.png" if ver_password else "images/inicio_sesion/ojo_cerrado.png")
                at transform:
                    xysize(50, 50)
                mouse "pc_select" 
                action ToggleVariable("ver_password")
        null height 30

        # Botón para ir a Login
        textbutton "¿Ya tienes cuenta? Inicia Sesión":
            text_font "gui/fonts/VT323.ttf"
            text_size 24
            text_color "#ffffff"
            text_hover_color "#000000" 
            xalign 0.5
            action [SetVariable("pc_pass", ""), 
                    SetVariable("pc_pass_confirm", ""), 
                    SetVariable("ver_password", False),
                    Hide("registro_pc"),
                    Show("inicio_sesion_pc")]


        # BOTÓN COMPLETAR
        imagebutton:
            idle Transform("images/inicio_sesion/boton_completar_registro.png", zoom=2)
            hover Transform("images/inicio_sesion/boton_completar_registro_activo.png", zoom=2)
            xalign 0.5
            action If(
                pc_usuario != "" and pc_email != "" and pc_pass != "" and pc_pass == pc_pass_confirm,
                true=Show("cargando_servidor", tarea="registro"),
                false=Notify("Revisa los datos.")
            )

# --- PANTALLA DE INICIO DE SESIÓN ---
screen inicio_sesion_pc():
    modal True
    tag menu 

    # Controla quién tiene el turno para escribir.
    default foco_actual = "None"

    default mostrar_aviso = False

    on "show" action Function(check_vars_safe)

    add "images/inicio_sesion/imagen_login_fondo.png":
        xysize(1920, 1080)

    vbox:
        xalign 0.5
        yalign 0.35
        spacing 25

        add "images/inicio_sesion/imagen_login_perfil.png":
            xalign 0.5
            xysize (350, 350)
            fit "contain"
        
        text "Inicio de Sesión":
            font "gui/fonts/VT323.ttf"
            size 50
            xalign 0.5
            color "#ffffff"

        null height 10

        # =========================================================
        # CAJA 1: USUARIO
        # =========================================================
        if foco_actual == "usuario":
            # ESTADO ACTIVO
            frame:
                style "caja_blanca_base"
                input value VariableInputValue("pc_usuario") style "texto_input_activo" length 15 xfill True yfill True
        else:
            # ESTADO INACTIVO
            button:
                style "caja_blanca_base"
                action SetScreenVariable("foco_actual", "usuario")
                
                if pc_usuario == "":
                    text "Nombre de Usuario" style "texto_placeholder"
                else:
                    text "[pc_usuario]" style "texto_valor_fijo"

        # =========================================================
        # CAJA 2: CONTRASEÑA 
        # =========================================================
        fixed:
            xsize 600 ysize 60 xalign 0.5

            if foco_actual == "pass":
                frame:
                    style "caja_blanca_base"
                    input value VariableInputValue("pc_pass") style "texto_input_activo" length 20 mask (None if ver_password else "*") xfill True yfill True
            else:
                button:
                    style "caja_blanca_base"
                    action SetScreenVariable("foco_actual", "pass")
                    if pc_pass == "":
                        text "Contraseña" style "texto_placeholder"
                    else:
                        text (pc_pass if ver_password else "*" * len(pc_pass)) style "texto_valor_fijo"

            # --- Boton ojo ---
            imagebutton:
                xpos 615
                yalign 0.5
                idle ("images/inicio_sesion/ojo_abierto.png" if ver_password else "images/inicio_sesion/ojo_cerrado.png")
                at transform:
                    xysize(50, 50)
                mouse "pc_select" 
                action ToggleVariable("ver_password")

        textbutton "¿Has olvidado la contraseña?":
            text_font "gui/fonts/VT323.ttf"
            text_size 24
            text_color "#ffffff"
            text_hover_color "#000000" 
            xalign 0.5
            action [SetVariable("pc_pass", ""), 
                    SetVariable("ver_password", False),
                    Hide("inicio_sesion_pc"), 
                    Show("recuperacion")]
        # Botón para ir a Registro
        textbutton "¿No tienes cuenta? Regístrate":
            text_font "gui/fonts/VT323.ttf"
            text_size 24
            text_color "#ffffff"
            text_hover_color "#000000" 
            xalign 0.5
            action [SetVariable("pc_pass", ""), 
                    SetVariable("ver_password", False),
                    Hide("inicio_sesion_pc"), 
                    Show("registro_pc")]

        # BOTÓN COMPLETAR
        imagebutton:
            idle Transform("images/inicio_sesion/boton_iniciar_sesion.png", zoom=2)
            hover Transform("images/inicio_sesion/boton_iniciar_sesion_activo.png", zoom=2)
            xalign 0.5
            action If(
                pc_usuario != "" and pc_pass != "",
                true=Show("cargando_servidor", tarea="login"),
                false=Notify("Revisa los datos.")
            )
            
# --- PANTALLA DE RECUPERACIÓN DE CONTRASEÑA ---
screen recuperacion():
    modal True
    tag menu
    default foco_actual = "None"

    # Fondo
    add "images/inicio_sesion/imagen_login_fondo.png":
        xysize(1920, 1080)

    vbox:
        xalign 0.5
        yalign 0.35
        spacing 25

        # Icono de perfil
        add "images/inicio_sesion/imagen_login_perfil.png":
            xalign 0.5
            xysize (300, 300)
            fit "contain"
        
        text "Recuperar Contraseña":
            font "gui/fonts/VT323.ttf"
            size 50
            xalign 0.5
            color "#ffffff"

        # =========================================================
        # PANTALLA 1: EMAIL Y CÓDIGO
        # =========================================================
        if fase_recuperacion == 1:
            vbox:
                spacing 10
                xalign 0.5
                
                text "Introduce tu correo electrónico" style "texto_placeholder" size 25 xalign 0.0

                # CAJA DE EMAIL CON BOTÓN INTEGRADO
                hbox:
                    spacing 10
                    xsize 600
                    fixed:
                        xsize 450 ysize 60
                        if foco_actual == "email":
                            frame:
                                background Solid("#ffffff")
                                xfill True yfill True
                                padding (15, 0)
                                input value VariableInputValue("pc_email") style "texto_input_activo" length 40 yalign 0.5
                        else:
                            button:
                                background Solid("#ffffff")
                                xfill True yfill True
                                action SetScreenVariable("foco_actual", "email")
                                if pc_email == "":
                                    text "Correo Electrónico" style "texto_placeholder" yalign 0.5 xpos 15
                                else:
                                    text "[pc_email]" style "texto_valor_fijo" yalign 0.5 xpos 15
                    # BOTÓN DE VERIFICAR
                    textbutton "Verificar":
                        ysize 60
                        text_font "gui/fonts/VT323.ttf"
                        text_size 28
                        background Solid("#222") 
                        hover_background Solid("#ff0000")
                        padding (15, 10)
                        yalign 0.5

                        # Llama a la API para enviar el código llama a la API para enviar el código
                        action If(pc_email != "", Show("cargando_servidor", tarea="codigo"), Notify("Escribe un email"))
                null height 10
                text "Introduce el código de recuperación enviado" style "texto_placeholder" size 25 xalign 0.0
                
                # CAJA DE CÓDIGO
                button:
                    style "caja_blanca_base"
                    action SetScreenVariable("foco_actual", "codigo")
                    if foco_actual == "codigo":
                        input value VariableInputValue("pc_codigo") style "texto_input_activo" length 6 xfill True yfill True
                    else:
                        if pc_codigo == "":
                            text "Código de recuperación" style "texto_placeholder"
                        else:
                            text "[pc_codigo]" style "texto_valor_fijo"

            null height 20

            # BOTONES INFERIORES (Regresar y Continuar)
            hbox:
                xalign 0.5
                spacing 150
                textbutton "Regresar":
                    text_font "gui/fonts/VT323.ttf"
                    text_size 35
                    text_color "#ffffff"
                    text_hover_color "#000000" 
                    xalign 0.5
                    action [SetVariable("pc_nueva_pass", ""), 
                            SetVariable("pc_confirm_pass", ""),
                            SetVariable("ver_password", False),
                            SetVariable("fase_recuperacion", 1), 
                            Show("inicio_sesion_pc")]
                
                textbutton "Continuar":
                    text_font "gui/fonts/VT323.ttf"
                    text_size 35
                    text_color "#ffffff"
                    text_hover_color "#000000" 
                    xalign 0.5
                    action If(pc_codigo != "", SetVariable("fase_recuperacion", 2), Notify("Introduce el código"))


        # =========================================================
        # PANTALLA 2: NUEVAS CLAVES
        # =========================================================
        else:
            vbox:
                spacing 15
                xalign 0.5
                text "Introduce tu nueva contraseña" style "texto_placeholder" size 25 xalign 0.0

                # =========================================================
                # NUEVA PASS
                # =========================================================
                fixed:
                    xsize 600 ysize 60 xalign 0.5

                    if foco_actual == "nueva_pass":
                        frame:
                            style "caja_blanca_base"
                            input value VariableInputValue("pc_nueva_pass") style "texto_input_activo" length 20 mask (None if ver_password else "*") xfill True yfill True
                    else:
                        button:
                            style "caja_blanca_base"
                            action SetScreenVariable("foco_actual", "nueva_pass")
                            if pc_nueva_pass == "":
                                text "Contraseña" style "texto_placeholder"
                            else:
                                text (pc_nueva_pass if ver_password else "*" * len(pc_nueva_pass)) style "texto_valor_fijo"

                    imagebutton:
                        xpos 615
                        yalign 0.5
                        idle ("images/inicio_sesion/ojo_abierto.png" if ver_password else "images/inicio_sesion/ojo_cerrado.png")
                        at transform:
                            xysize(50, 50)
                        mouse "pc_select" 
                        action ToggleVariable("ver_password")

                # =========================================================
                # CONFIRMAR PASS
                # =========================================================
                fixed:
                    xsize 600 ysize 60 xalign 0.5

                    if foco_actual == "confirm_pass": 
                        frame:
                            style "caja_blanca_base"
                            input value VariableInputValue("pc_confirm_pass") style "texto_input_activo" length 20 mask (None if ver_password else "*") xfill True yfill True
                    else:
                        button:
                            style "caja_blanca_base"
                            action SetScreenVariable("foco_actual", "confirm_pass") 
                            if pc_confirm_pass == "":
                                text "Confirmar Contraseña" style "texto_placeholder"
                            else:
                                text (pc_confirm_pass if ver_password else "*" * len(pc_confirm_pass)) style "texto_valor_fijo"

                    imagebutton:
                        xpos 615
                        yalign 0.5
                        idle ("images/inicio_sesion/ojo_abierto.png" if ver_password else "images/inicio_sesion/ojo_cerrado.png")
                        at transform:
                            xysize(50, 50)
                        mouse "pc_select" 
                        action ToggleVariable("ver_password")
                        
                null height 20

                # BOTÓN CAMBIAR
                textbutton "Cambiar Contraseña":
                    xalign 0.5
                    text_font "gui/fonts/VT323.ttf"
                    text_size 40
                    text_color "#ffffff"
                    text_hover_color "#ff0000"
                    action If(
                        pc_nueva_pass != "" and pc_nueva_pass == pc_confirm_pass,
                        true=Show("cargando_servidor", tarea="cambiar_pass"), 
                        false=Notify("Las contraseñas no coinciden")
                    )

                textbutton "Regresar al Inicio de Sesión":
                    xalign 0.5
                    text_font "gui/fonts/VT323.ttf"
                    text_size 25
                    text_color "#aaaaaa"
                    text_hover_color "#ffffff"
                    action [SetVariable("pc_nueva_pass", ""), 
                            SetVariable("pc_confirm_pass", ""),
                            SetVariable("ver_password", False),
                            SetVariable("fase_recuperacion", 1), 
                            Hide("recuperacion"),
                            Show("inicio_sesion_pc")]

    # --- MENSAJE FLOTANTE DE ÉXITO ---
    if recuperacion_msg == "¡Contraseña actualizada!":
        frame:
            align (0.5, 0.2)
            background Solid("#002244cc")
            padding (40, 20)
            text "Contraseña cambiada correctamente" color "#fff" font "gui/fonts/VT323.ttf" size 30


# --- PANTALLA DE ESCRITORIO PC ---

screen escritorio_pc():
    modal True 

    add "images/escritorioPC/fondo_escritorio.png":
        xysize (1920, 1080)

    # ICONOS DEL ESCRITORIO
    hbox:
        xpos 40    
        yalign 0.88  
        spacing 50   

        vbox:
            spacing 5    
            xalign 0.5 
            imagebutton:
                idle "images/escritorioPC/icono_nota.png" 
                hover Transform("images/escritorioPC/icono_nota.png", matrixcolor=BrightnessMatrix(0.2)) 
                mouse "pc_select"
                action Function(abrir_app, "nota")
                xalign 0.5
            text "Nota_1":
                font "gui/fonts/VT323.ttf" 
                size 25
                color "#ffffff"
                outlines [(2, "#000000", 0, 0)] 
                xalign 0.5

        vbox:
            spacing 5
            xalign 0.5
            fixed:
                fit_first True 
                xalign 0.5
                
                imagebutton:
                    idle "images/escritorioPC/icono_chat.png"
                    hover Transform("images/escritorioPC/icono_chat.png", matrixcolor=BrightnessMatrix(0.2))
                    mouse "pc_select"
                    action [Function(abrir_app, "chat"), SetVariable("mensajes_nuevos", False)]
                    
                if mensajes_nuevos: 
                    image "images/escritorioPC/circulo.png" at transform:
                        xysize(25, 25)
                        xalign 0.65
                        yalign 0.0
                        xoffset 15
                        yoffset 3

            text "Chat":
                font "gui/fonts/VT323.ttf"
                size 25
                color "#ffffff"
                outlines [(2, "#000000", 0, 0)]
                xalign 0.5
        vbox:
            spacing 5
            xalign 0.5
            imagebutton:
                idle "images/escritorioPC/icono_ajustes.png"
                hover Transform("images/escritorioPC/icono_ajustes.png", matrixcolor=BrightnessMatrix(0.2))
                mouse "pc_select"
                action ShowMenu("preferences")
                xalign 0.5
            text "Ajustes":
                font "gui/fonts/VT323.ttf"
                size 25
                color "#ffffff"
                outlines [(2, "#000000", 0, 0)]
                xalign 0.5
        
        vbox:
            spacing 5
            xalign 0.5
            imagebutton:
                idle "images/escritorioPC/icono_galeria.png"
                hover Transform("images/escritorioPC/icono_galeria.png", matrixcolor=BrightnessMatrix(0.2))
                mouse "pc_select"
                action Function(abrir_app, "galeria")
                xalign 0.5
            text "Galería":
                font "gui/fonts/VT323.ttf"
                size 25
                color "#ffffff"
                outlines [(2, "#000000", 0, 0)]
                xalign 0.5

        vbox:
            spacing 5
            xalign 0.5
            imagebutton:
                idle "images/escritorioPC/icono_musica.png"
                hover Transform("images/escritorioPC/icono_musica.png", matrixcolor=BrightnessMatrix(0.2))
                mouse "pc_select"
                action Function(abrir_app, "musica")
                xalign 0.5
            text "Música":
                font "gui/fonts/VT323.ttf"
                size 25
                color "#ffffff"
                outlines [(2, "#000000", 0, 0)]
                xalign 0.5

        vbox:
            spacing 5
            xalign 0.5
            imagebutton:
                idle "images/escritorioPC/icono_webcam.png"
                hover Transform("images/escritorioPC/icono_webcam.png", matrixcolor=BrightnessMatrix(0.2))
                mouse "pc_select"
                action Function(abrir_app, "webcam")
                xalign 0.5
            text "WebCam":
                font "gui/fonts/VT323.ttf"
                size 25
                color "#ffffff"
                outlines [(2, "#000000", 0, 0)]
                xalign 0.5


    # BARRA DE TAREAS Y APLICACIONES ABIERTAS
    frame:
        background Transform("images/escritorioPC/barra_tareas.png", xysize=(1920, 80))
        xsize 1920
        xfill True    
        ysize 80       
        yalign 1.0     
        padding (20, 0)

        imagebutton:
            idle Transform("images/escritorioPC/boton_apagar.png", xysize=(75, 75), nearest=True)
            hover Transform("images/escritorioPC/boton_apagar.png", xysize=(75, 75), nearest=True, matrixcolor=BrightnessMatrix(0.2))            
            focus_mask True
            mouse "pc_select"
            yalign 0.5 
            xalign 0.0 
            action Return() 

        # --- VENTANAS MINIMIZADAS ---
        hbox:
            xpos 100 
            yalign 0.5
            spacing 10

            for app_id in orden_apps:
                if apps_pc[app_id]["abierta"]:
                    button:
                        background (Solid("#333333") if apps_pc[app_id]["minimizada"] else Solid("#0055aaff"))
                        padding (15, 10)
                        action Function(toggle_minimizar, app_id)
                        text apps_pc[app_id]["titulo"] font "gui/fonts/VT323.ttf" size 25 color "#fff"

        # RELOJ
        frame:
            background Solid("#d3d3d3") 
            padding (15, 5)
            yalign 0.5 
            xalign 1.0
            
            text "01/10/2004 | 23:05":
                font "gui/fonts/VT323.ttf"
                size 32
                color "#000000"


# --- VENTANA DE NOTA 1 ---
screen ventana_nota():
    zorder 10
    
    if not apps_pc["nota"]["minimizada"]:
        
        drag:
            drag_name "nota_drag"
            xpos 400 ypos 200
            drag_handle (0, 0, 1.0, 40)
            
            frame:
                background Solid("#222222") 
                padding (2, 2)
                
                vbox:
                    # BARRA SUPERIOR AZUL
                    frame:
                        xsize 500
                        ysize 40
                        background Solid("#0000aa")
                        padding (10, 0)
                        
                        hbox:
                            xfill True
                            yalign 0.5
                            
                            text apps_pc["nota"]["titulo"] font "gui/fonts/VT323.ttf" size 25 color "#fff" yalign 0.5
                            
                            # BOTONES MINIMIZAR Y CERRAR
                            hbox:
                                xalign 1.0
                                yalign 0.5
                                spacing 4
                                
                                # BOTÓN MINIMIZAR
                                textbutton "-":
                                    xysize (34, 34) 
                                    text_font "gui/fonts/VT323.ttf" 
                                    text_size 30 
                                    text_color "#fff" 
                                    text_xalign 0.5 
                                    text_yalign 0.3
                                    background Solid("#888888")
                                    hover_background Solid("#aaaaaa") 
                                    action Function(toggle_minimizar, "nota")
                                    
                                # BOTÓN CERRAR
                                textbutton "X":
                                    xysize (34, 34) 
                                    text_font "gui/fonts/VT323.ttf" 
                                    text_size 30 
                                    text_color "#fff" 
                                    text_xalign 0.5 
                                    text_yalign 0.5 
                                    background Solid("#cc0000")
                                    hover_background Solid("#ff3333") 
                                    action Function(cerrar_app, "nota")

                    # ÁREA DE CONTENIDO 
                    frame:
                        background Solid("#ffffff")
                        xysize (500, 300)
                        padding (20, 20)
                        
                        # Aquí hacemos la magia dependiendo de la variable global
                        if nota_1_descifrada == False:
                            text "████ ██ ████ ███████. \n████ ██ ████ ██████. \n████ ██████ █ ████ ██ ████████████" color "#000" font "DejaVuSans.ttf" size 25
                        else:
                            text "Nada es como piensas. \nNada es como parece. \nDATE CUENTA Y DEJA DE VICTIMIZARTE \n DEJA DE HUIR" color "#ff0000" font "gui/fonts/VT323.ttf" size 25

# --- BARRA DE SCROLL DEL CHAT ---
style chat_vscrollbar:
    xsize 12  
    
    right_margin 15 
    
    base_bar Solid("#00000000") 
    
    thumb Solid("#5c5c8a") 
    
    hover_thumb Solid("#8a8ab5") 
    
    unscrollable "hide"


# ---VENTANA DE CHAT ---
screen ventana_chat():
    zorder 10
    if not apps_pc["chat"]["minimizada"]:
        drag:
            drag_name "chat_drag"
            xpos 350 ypos 50 
            drag_handle (0, 0, 1.0, 70)
            
            fixed:
                xysize (900, 800) 
                
                add Transform("images/escritorioPC/ventana_chat.png", xysize=(900, 800), nearest=True)

                # BOTONES
                imagebutton:
                    idle Solid("#00000000") 
                    hover Solid("#ffffff33") 
                    xysize (40, 40) 
                    xpos 780
                    ypos 20
                    action Function(toggle_minimizar, "chat")
                    
                imagebutton:
                    idle Solid("#00000000") 
                    hover Solid("#ff000055") 
                    xysize (40, 40)  
                    xpos 830 
                    ypos 20
                    action Function(cerrar_app, "chat")

                # caja para la chica
                hbox:
                    xpos 42 
                    ypos 90
                    spacing 8
                    
                    imagebutton:
                        idle Transform("images/escritorioPC/icono_chica.png", xysize=(35, 35), fit="contain")
                        hover Transform("images/escritorioPC/icono_chica.png", xysize=(35, 35), fit="contain", matrixcolor=BrightnessMatrix(0.1))
                        action Show("zoom_perfil", img="images/escritorioPC/icono_chica.png")
                        xalign 0.5
                    
                    text "Roxy26": 
                        font "gui/fonts/VT323.ttf"
                        size 28
                        color "#ffffff"
                        xalign 0.5
                        yoffset 10
                
                # caja para el nombre del usuario
                hbox:
                    xpos 105  
                    ypos 760
                    yanchor 0.5
                    
                    text (persistent.nombre_jugador or pc_usuario or "Usuario"): 
                        font "gui/fonts/VT323.ttf"
                        size 32
                        color "#ffffff"
                        outlines [(1, "#000000", 0, 0)]
                        yanchor 0.5

                # --- Chat ---
                vbox:
                    xpos 250 
                    ypos 100
                    xysize (600, 620)
                    
                    frame:
                        ysize 480
                        xfill True
                        background Frame("images/escritorioPC/frame_envuelve_chat.png", 15, 15, 15, 15)
                        padding (20, 20)

                        style_prefix "chat"

                        viewport id "chat_vp":
                            mousewheel True
                            draggable True
                            yinitial 1.0
                            scrollbars "vertical"

                            vbox:
                                xsize 520 
                                spacing 20
                                for remitente, msg in historial_mensajes:
                                    if remitente == "Yo":
                                        frame:
                                            background Frame("images/escritorioPC/frame_chat1.png", 60, 60, 60, 60)
                                            padding (40, 15, 30, 45) 
                                            xalign 1.0
                                            xmaximum 500 
                                            
                                            if msg.startswith("IMG:"):
                                                imagebutton:
                                                    idle Transform(msg.replace("IMG:", "").strip(), xysize=(200, 150), fit="cover") 
                                                    hover Transform(msg.replace("IMG:", "").strip(), xysize=(200, 150), fit="cover", matrixcolor=BrightnessMatrix(0.1))
                                                    action Show("zoom_galeria", img=msg.replace("IMG:", "").strip())
                                                    xalign 0.5
                                            else:
                                                text "[msg]":
                                                    color "#fff" 
                                                    font "gui/fonts/VT323.ttf" 
                                                    size 30 
                                                    xalign 0.5
                                    else:
                                        frame:
                                            background Frame("images/escritorioPC/frame_chat2.png", 60, 60, 60, 60)
                                            padding (40, 15, 30, 45)
                                            xalign 0.0
                                            xmaximum 500
                                            
                                            # MAGIA: Lo mismo para los mensajes de Rocío
                                            if msg.startswith("IMG:"):
                                                imagebutton:
                                                    idle Transform(msg.replace("IMG:", "").strip(), xysize=(200, 150), fit="cover") 
                                                    hover Transform(msg.replace("IMG:", "").strip(), xysize=(200, 150), fit="cover", matrixcolor=BrightnessMatrix(0.1))
                                                    action Show("zoom_galeria", img=msg.replace("IMG:", "").strip())
                                                    xalign 0.5
                                            else:
                                                text "[msg]":
                                                    color "#fff" 
                                                    font "gui/fonts/VT323.ttf" 
                                                    size 30 
                                                    xalign 0.5
                # --- ELECCIONES ---
                vbox:
                    xpos 250
                    ypos 695    
                    yanchor 1.0
                    xsize 560
                    spacing 8
                    
                    for texto_opcion, destino in respuestas_disponibles:
                        button:
                            background Frame("images/escritorioPC/frame_decisiones_chat.png", 30, 30, 30, 30) 
                            xsize 520
                            xalign 0.5 
                            padding (20, 12)
                        
                            action Function(enviar_respuesta_chat, texto_opcion, destino)
                            
                            text "> [texto_opcion]" color "#ccc" hover_color "#fff" font "gui/fonts/VT323.ttf" size 22 xalign 0.5 yalign 0.5

# Pantalla para ver imagen de perfil en grande

screen zoom_perfil(img):
    modal True 
    zorder 100 

    add Solid("#000000aa")
    
    add [img]:
        align (0.5, 0.5)
        at transform:
            zoom 0.5 
    
    button:
        action Hide("zoom_perfil")
        xfill True
        yfill True
        background None               

# --- VENTANA DE MÚSICA ---
screen ventana_musica():
    zorder 10
    
    if not apps_pc["musica"]["minimizada"]:
        
        drag:
            drag_name "musica_drag"
            xpos 400 ypos 200
            drag_handle (0, 0, 1.0, 50) 
            
            fixed:
                xysize (800, 600) 
                
                add Transform("images/escritorioPC/frame_reproductor.jpg", xysize=(800, 600), fit="fill")
                
                # BOTONES Minimizar y Cerrar
                imagebutton:
                    idle Solid("#00000000") 
                    hover Solid("#ffffff33") 
                    xysize (32, 28) 
                    xpos 710
                    ypos 13
                    action Function(toggle_minimizar, "musica")
                    
                imagebutton:
                    idle Solid("#00000000") 
                    hover Solid("#ff000055") 
                    xysize (32, 28)  
                    xpos 750 
                    ypos 13
                    action Function(cerrar_app, "musica")

                # TEXTOS DINÁMICOS
                # Aquí irán las variables de la canción que esté sonando
                text "[cancion_actual]" font "gui/fonts/VT323.ttf" size 35 color "#000000" xpos 200 ypos 100
                text "[artista_actual]" font "gui/fonts/VT323.ttf" size 35 color "#000000" xpos 200 ypos 250
                
                # BOTONES DE CONTROL (Play, Stop, Pausa, etc.)
                hbox:
                    xalign 0.5 
                    ypos 500 
                    spacing 45
                    
                    # Botón Atrás
                    imagebutton:
                        idle Transform("images/escritorioPC/icono_back.png", xysize=(60, 60))
                        hover Transform("images/escritorioPC/icono_back.png", xysize=(60, 60), matrixcolor=BrightnessMatrix(0.2))
                        action Function(anterior_cancion)
                        
                    # Botón Stop
                    imagebutton:
                        idle Transform("images/escritorioPC/icono_parar.png", xysize=(60, 60))
                        hover Transform("images/escritorioPC/icono_parar.png", xysize=(60, 60), matrixcolor=BrightnessMatrix(0.2))
                        action [Stop("music"), SetVariable("cancion_actual", ""), SetVariable("artista_actual", ""), SetVariable("musica_pausada", False)]
                    
                    # Botón Pausa
                    imagebutton:
                        idle Transform("images/escritorioPC/icono_pausa.png", xysize=(60, 60))
                        hover Transform("images/escritorioPC/icono_pausa.png", xysize=(60, 60), matrixcolor=BrightnessMatrix(0.2))
                        # Si está sonando, la pausa. Si está pausada, la reanuda.
                        action [ToggleVariable("musica_pausada"), 
                                If(musica_pausada, true=PauseAudio("music", value=True), false=PauseAudio("music", value=False))]

                    # Botón Play 
                    imagebutton:
                        idle Transform("images/escritorioPC/icono_play.png", xysize=(60, 60))
                        hover Transform("images/escritorioPC/icono_play.png", xysize=(60, 60), matrixcolor=BrightnessMatrix(0.2))
                        action Function(reproducir_pista)
                    
                    # Botón Siguiente
                    imagebutton:
                        idle Transform("images/escritorioPC/icono_next.png", xysize=(60, 60))
                        hover Transform("images/escritorioPC/icono_next.png", xysize=(60, 60), matrixcolor=BrightnessMatrix(0.2))
                        action Function(siguiente_cancion)

# zoom para imagenes de galeria
screen zoom_galeria(img):
    modal True 
    zorder 100 

    add Solid("#000000aa")
    
    add [img]:
        align (0.5, 0.5)
        at transform:
            zoom 0.5
    
    button:
        action Hide("zoom_galeria") 
        xfill True
        yfill True
        background None     

# Ventana de Galería
screen ventana_galeria():
    zorder 10

    if not apps_pc["galeria"]["minimizada"]:
        
        drag:
            drag_name "galeria_drag"
            xpos 400 ypos 200
            drag_handle (0, 0, 1.0, 50) 
            
            fixed:
                xysize (800, 600) 
                
                add Transform("images/escritorioPC/ventana_galeria.png", xysize=(800, 600), nearest=True)
                
                hbox:
                    xpos 20 ypos 18
                    spacing 10
                    add Transform("images/escritorioPC/icono_galeria.png", xysize=(30, 30), nearest=True)
                    text "Galería de Imágenes":
                        font "gui/fonts/VT323.ttf"
                        size 26
                        color "#ffffff"
                        outlines [(1, "#000000", 0, 0)]

                # BOTONES Minimizar y Cerrar
                imagebutton:
                    idle Solid("#00000000") 
                    hover Solid("#ffffff33") 
                    xysize (50, 50) 
                    xpos 693
                    ypos 10
                    action Function(toggle_minimizar, "galeria")
                    
                imagebutton:
                    idle Solid("#00000000") 
                    hover Solid("#ff000055") 
                    xysize (50, 50)  
                    xpos 745
                    ypos 10
                    action Function(cerrar_app, "galeria")
                
                frame:
                    background None
                    xpos 40 ypos 90 
                    xysize (720, 470)
                    
                    style_prefix "chat" 

                    viewport id "gal_vp":
                        mousewheel True
                        draggable True
                        scrollbars "vertical"
                        
                        vpgrid:
                            cols 3       
                            spacing 25   
                            xfill True

                            for foto in lista_fotos:
                                frame:
                                    background Solid("#000")
                                    padding (2, 2)
                                    
                                    imagebutton:
                                        idle Transform(foto, xysize=(200, 150), fit="cover") 
                                        hover Transform(foto, xysize=(200, 150), fit="cover", matrixcolor=BrightnessMatrix(0.1))
                                        
                                        action Show("zoom_galeria", img=foto) 

# ventana de Webcam
screen ventana_webcam():
    zorder 10
    
    # He corregido la posición de esta línea, que estaba demasiado a la derecha
    if not apps_pc["webcam"]["minimizada"]:
        
        drag:
            drag_name "webcam_drag"
            xpos 400 ypos 200
            drag_handle (0, 0, 1.0, 50) 
            
            fixed:
                xysize (800, 600) 
                
                # marco de la ventana
                add Transform("images/escritorioPC/ventana_webcam.png", xysize=(800, 600), nearest=True)
                
                add Transform("images/escritorioPC/webcam_no_disponible.png", xysize=(788, 533), fit="fill"):
                    xpos 7
                    ypos 60
                
                hbox:
                    xpos 20 ypos 18
                    spacing 10
                    add Transform("images/escritorioPC/icono_webcam.png", xysize=(30, 30), nearest=True)
                    text "WebCam":
                        font "gui/fonts/VT323.ttf"
                        size 26
                        color "#ffffff"
                        outlines [(1, "#000000", 0, 0)]
        
                # BOTONES Minimizar y Cerrar
                imagebutton:
                    idle Solid("#00000000") 
                    hover Solid("#ffffff33") 
                    xysize (50, 50) 
                    xpos 693
                    ypos 10
                    action Function(toggle_minimizar, "webcam")
                    
                imagebutton:
                    idle Solid("#00000000") 
                    hover Solid("#ff000055") 
                    xysize (50, 50)  
                    xpos 745
                    ypos 10
                    action Function(cerrar_app, "webcam")
                
