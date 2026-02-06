init python:
    # 1. Creamos la galería
    g = Gallery()

    # 2. Definimos qué imagen se usa cuando el hueco está CERRADO
    # Aquí es donde Ren'Py usará tu imagen negra "Block" automáticamente
    g.locked_button = "images/menus/boton_block.png"
    
    # 3. Transición suave al abrir una foto (para el futuro)
    g.transition = dissolve

    # 4. Definimos los 8 huecos (Slots)
    # Aunque no tengas las imágenes finales, necesitamos darles un nombre "temporal"
    # para que el código no falle.
    
    # Fila 1
    g.button("cg1")
    g.unlock_image("cg1") # Cuando tengas la foto, se llamará "cg1"
    
    g.button("cg2")
    g.unlock_image("cg2")
    
    g.button("cg3")
    g.unlock_image("cg3")
    
    g.button("cg4")
    g.unlock_image("cg4")
    
    # Fila 2
    g.button("cg5")
    g.unlock_image("cg5")
    
    g.button("cg6")
    g.unlock_image("cg6")
    
    g.button("cg7")
    g.unlock_image("cg7")
    
    g.button("cg8")
    g.unlock_image("cg8")