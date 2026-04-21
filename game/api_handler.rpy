init python:
    import json
    import urllib.request
    import urllib.error

    API_URL = "https://api-proyecto-sandy.vercel.app" 

    # --- FUNCIÓN DE REGISTRO ---
    def conectar_registro(username, email, password):
        url = API_URL + "/api/register"
        datos = {"username": username, "email": email, "password": password}
        
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() in [200, 201]:
                    renpy.store.persistent.nombre_jugador = username
                    renpy.store.pc_email = email 
                    
                    renpy.notify("¡Éxito! Cuenta creada. Por favor, inicia sesión.")
                    
                    # Limpiamos las contraseñas por seguridad y mandamos al login
                    renpy.store.pc_pass = ""
                    renpy.store.pc_pass_confirm = ""
                    renpy.hide_screen("registro_pc")
                    renpy.show_screen("inicio_sesion_pc")
            
        except urllib.error.HTTPError as e:
            try:
                error_body = e.read().decode('utf-8')
                error_data = json.loads(error_body)
                mensaje_real = error_data.get('detail', "Error en el registro.")
                # Aquí el juego te dirá si la contraseña es muy corta o el email ya existe
                renpy.notify(str(mensaje_real)) 
            except:
                renpy.notify("Error: El usuario o email ya existen.")
        except Exception as e:
            renpy.notify("Error de conexión: Revisa tu internet.")


    # --- FUNCIÓN DE LOGIN ---
    def conectar_login(username, password):
        url = API_URL + "/api/login"
        datos = {"username": username, "password": password}
        
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() in [200, 201]:
                    respuesta = json.loads(response.read().decode('utf-8'))
                    
                    # Guardamos la identidad
                    renpy.store.persistent.user_id = respuesta.get("user_id")
                    renpy.store.persistent.nombre_jugador = respuesta.get("username")
                    renpy.store.pc_email = respuesta.get("email")
                    
                    # Cargamos el progreso
                    progreso = respuesta.get("progreso", {})
                    renpy.store.capitulo_actual = progreso.get("capitulo", "prologo")
                    renpy.store.stress_level = progreso.get("estres", 0)
                    renpy.store.decisiones_tomadas = progreso.get("decisiones", {})
                    
                    renpy.notify("¡Acceso concedido! Cargando estado...")
                    return True # ESTE ES EL ÚNICO QUE DEVUELVE TRUE (Para ir al Menú Principal)

        except urllib.error.HTTPError as e:
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                renpy.notify(str(error_data.get('detail', "Error en el login.")))
            except:
                renpy.notify("Usuario o contraseña incorrectos.")
        except Exception as e:
            renpy.notify("Error de conexión: Revisa tu internet.")


    # --- FUNCIÓN: PEDIR CÓDIGO AL CORREO ---
    def solicitar_codigo_api(email):
        url = API_URL + "/api/forgot-password"
        datos = {"email": email}
        
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    renpy.notify("Vínculo establecido. Revisa tu correo electrónico.")
                    
        except urllib.error.HTTPError as e:
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                # Si el correo no existe en la BD, te avisa aquí
                renpy.notify(str(error_data.get('detail', "Ese correo no está registrado.")))
            except:
                renpy.notify("Error: Correo no registrado.")
        except Exception:
            renpy.notify("Error de conexión con el servidor.")


    # --- FUNCIÓN: VERIFICAR CÓDIGO (EL PASO INTERMEDIO) ---
    def verificar_codigo_api(email, codigo):
        url = API_URL + "/api/verify-code"
        datos = {"email": email, "code": codigo}
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    # Si Vercel dice que el código es válido, cambiamos a la Fase 2 (Nueva Pass)
                    renpy.store.fase_recuperacion = 2 
        except urllib.error.HTTPError as e:
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                # Si pones un código inventado, el juego te frena y te avisa
                renpy.notify(str(error_data.get('detail', "Código inválido.")))
            except:
                renpy.notify("Error: Código incorrecto.")
        except Exception:
            renpy.notify("Error de conexión.")


    # --- FUNCIÓN: CONFIRMAR NUEVA CONTRASEÑA ---
    def confirmar_nueva_password_api(email, codigo, nueva_pass):
        url = API_URL + "/api/reset-confirm"
        datos = {
            "email": email,
            "code": codigo,
            "new_password": nueva_pass
        }

        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    renpy.notify("¡Contraseña actualizada correctamente!")
                    
                    # Todo fue bien, reseteamos las variables y volvemos al login
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
                # Si la contraseña es corta, no tiene mayúsculas, etc., Vercel te avisa aquí
                renpy.notify(str(error_data.get('detail', "Error al cambiar contraseña.")))
            except:
                renpy.notify("Error: Datos incorrectos.")
        except Exception as e:
            renpy.notify("Error de conexión.")

    # --- FUNCIÓN PARA GUARDAR PROGRESO ---
    def guardar_progreso(capitulo, estres, nuevas_decisiones):
        if not hasattr(persistent, 'user_id') or not persistent.user_id:
            return False 
            
        url = API_URL + "/api/save-progress"
        datos = {
            "user_id": persistent.user_id,
            "chapter": capitulo,
            "stress": estres,
            "decisions": nuevas_decisiones
        }
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.getcode() in [200, 201]:
                    return True
        except:
            pass 
        return False

    # --- FUNCIÓN PARA BORRAR CUENTA ---
    def borrar_cuenta_api(id_usuario):
        if not id_usuario:
            return False
        url = API_URL + f"/api/delete-user/{id_usuario}"
        try:
            req = urllib.request.Request(url, method='DELETE')
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.getcode() in [200, 201, 204]:
                    return True
        except:
            pass
        return False