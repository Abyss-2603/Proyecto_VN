init python:
    import json
    import urllib.request
    import urllib.error
    import ssl 

    # --- Desactiva el bloqueo SSL estricto de Ren'Py para Vercel ---
    ssl._create_default_https_context = ssl._create_unverified_context

    API_URL = "https://api-proyecto-sandy.vercel.app" 

    # --- Header para ANTI-BOTS por si acaso ---
    def get_headers():
        return {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    # --- FUNCIÓN DE REGISTRO ---
    def conectar_registro(username, email, password):
        url = API_URL + "/api/register"
        datos = {"username": username, "email": email, "password": password}
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers=get_headers())
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.getcode() in [200, 201]:
                    renpy.store.persistent.nombre_jugador = username
                    renpy.store.pc_email = email 
                    renpy.notify("¡Éxito! Cuenta creada. Por favor, inicia sesión.")
                    renpy.store.pc_pass = ""
                    renpy.store.pc_pass_confirm = ""
                    renpy.hide_screen("registro_pc")
                    renpy.show_screen("inicio_sesion_pc")
        except urllib.error.HTTPError as e:
            try:
                error_body = e.read().decode('utf-8')
                error_data = json.loads(error_body)
                renpy.notify(str(error_data.get('detail', "Error en el registro."))) 
            except:
                renpy.notify("Error: El usuario o email ya existen.")
        except Exception as e:
            renpy.notify(f"Fallo técnico: {str(e)}")

    # --- FUNCIÓN DE LOGIN ---
    def conectar_login(username, password):
        url = API_URL + "/api/login"
        datos = {"username": username, "password": password}
        login_exitoso = False
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers=get_headers())
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.getcode() in [200, 201]:
                    respuesta = json.loads(response.read().decode('utf-8'))
                    renpy.store.persistent.user_id = respuesta.get("user_id")
                    renpy.store.persistent.nombre_jugador = respuesta.get("username")
                    renpy.store.pc_email = respuesta.get("email")
                    progreso = respuesta.get("progreso", {})
                    renpy.store.capitulo_actual = progreso.get("capitulo", "prologo")
                    renpy.store.decisiones_tomadas = progreso.get("decisiones", {})

                    login_exitoso = True
        except urllib.error.HTTPError as e:
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                renpy.notify(str(error_data.get('detail', "Error en el login.")))
            except:
                renpy.notify("Usuario o contraseña incorrectos.")
        except Exception as e:
            renpy.notify(f"Fallo técnico: {str(e)}")
        if login_exitoso:
            renpy.notify("¡Acceso concedido! Cargando estado...")
            renpy.end_interaction(True)
            
    # --- FUNCIÓN: PEDIR CÓDIGO AL CORREO ---
    def solicitar_codigo_api(email):
        url = API_URL + "/api/forgot-password"
        datos = {"email": email}
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers=get_headers())
            with urllib.request.urlopen(req, timeout=20) as response:
                if response.getcode() == 200:
                    renpy.notify("Vínculo establecido. Revisa tu correo electrónico.")
        except urllib.error.HTTPError as e:
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                renpy.notify(str(error_data.get('detail', "Ese correo no está registrado.")))
            except:
                renpy.notify("Error: Correo no registrado.")
        except Exception as e:
            renpy.notify(f"Fallo técnico: {str(e)}")

    # --- FUNCIÓN: VERIFICAR CÓDIGO ---
    def verificar_codigo_api(email, codigo):
        url = API_URL + "/api/verify-code"
        datos = {"email": email, "code": codigo}
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers=get_headers())
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.getcode() == 200:
                    renpy.store.fase_recuperacion = 2 
        except urllib.error.HTTPError as e:
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                renpy.notify(str(error_data.get('detail', "Código inválido.")))
            except:
                renpy.notify("Error: Código incorrecto.")
        except Exception as e:
            renpy.notify(f"Fallo técnico: {str(e)}")

    # --- FUNCIÓN: CONFIRMAR NUEVA CONTRASEÑA ---
    def confirmar_nueva_password_api(email, codigo, nueva_pass):
        url = API_URL + "/api/reset-confirm"
        datos = {"email": email, "code": codigo, "new_password": nueva_pass}
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers=get_headers())
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.getcode() == 200:
                    renpy.notify("¡Contraseña actualizada correctamente!")
                    renpy.store.fase_recuperacion = 1
                    renpy.store.pc_email = ""
                    renpy.store.pc_codigo = ""
                    renpy.store.pc_nueva_pass = ""
                    renpy.store.pc_confirm_pass = ""
                    renpy.hide_screen("recuperacion")
                    renpy.show_screen("inicio_sesion_pc")
        except urllib.error.HTTPError as e:
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                renpy.notify(str(error_data.get('detail', "Error al cambiar contraseña.")))
            except:
                renpy.notify("Error: Datos incorrectos.")
        except Exception as e:
            renpy.notify(f"Fallo técnico: {str(e)}")

    # --- GUARDAR PROGRESO ---
    def guardar_progreso(capitulo, nuevas_decisiones):
        if not hasattr(persistent, 'user_id') or not persistent.user_id:
            return False 
        url = API_URL + "/api/save-progress"
        datos = {"user_id": persistent.user_id, "chapter": capitulo, "decisions": nuevas_decisiones}
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers=get_headers())
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.getcode() in [200, 201]: return True
        except: pass 
        return False

    # --- BORRAR CUENTA ---
    def borrar_cuenta_api(id_usuario):
        if not id_usuario:
            return False
        url = API_URL + f"/api/delete-user/{id_usuario}"
        try:
            req = urllib.request.Request(url, method='DELETE', headers=get_headers())
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() in [200, 201, 204]: 
                    return True
        except Exception as e:
            renpy.notify(f"Error de conexión: {str(e)}")

        return False

    apps_pc = {
        "nota": {"abierta": False, "minimizada": False, "titulo": "Nota_1.txt"},
        "chat": {"abierta": False, "minimizada": False, "titulo": "Chat.exe"},
        "ajustes": {"abierta": False, "minimizada": False, "titulo": "Panel de Control"},
        "carpeta": {"abierta": False, "minimizada": False, "titulo": "Archivos Ocultos"},
        "galeria": {"abierta": False, "minimizada": False, "titulo": "Visor de Imágenes"},
        "musica": {"abierta": False, "minimizada": False, "titulo": "Reproductor"},
        "webcam": {"abierta": False, "minimizada": False, "titulo": "Webcam"}
    }

    # --- Lógica de ventanas del escritorio ---
    # El orden en el que aparecerán en la barra de tareas
    orden_apps = ["nota", "chat", "ajustes", "carpeta", "galeria", "musica", "webcam"]

    # --- FUNCIONES DEL SISTEMA OPERATIVO ---
    def abrir_app(app_id):
        apps_pc[app_id]["abierta"] = True
        apps_pc[app_id]["minimizada"] = False
        renpy.show_screen("ventana_" + app_id) # Invoca la pantalla correspondiente
        renpy.restart_interaction()

    def cerrar_app(app_id):
        apps_pc[app_id]["abierta"] = False
        apps_pc[app_id]["minimizada"] = False
        renpy.hide_screen("ventana_" + app_id) # Destruye la pantalla
        renpy.restart_interaction()

    def toggle_minimizar(app_id):
        # Si está abierta, invierte su estado de minimizado (True a False, o False a True)
        if apps_pc[app_id]["abierta"]:
            apps_pc[app_id]["minimizada"] = not apps_pc[app_id]["minimizada"]
            renpy.restart_interaction()