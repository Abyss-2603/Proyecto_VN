init python:
    import json
    import urllib.request
    import urllib.error

    API_URL = "https://api-proyecto-sandy.vercel.app" 
    
    registro_msg = "" 
    login_msg = ""

    def conectar_registro(username, email, password):
        global registro_msg
        url = API_URL + "/api/register"
        
        datos = {"username": username, "email": email, "password": password}
        
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() in [200, 201]:
                    registro_msg = "¡Éxito! Cuenta creada."
                    renpy.store.persistent.nombre_jugador = username
                    renpy.store.pc_email = email 
                    return True

        except urllib.error.HTTPError as e:
            try:
                error_body = e.read().decode('utf-8')
                error_data = json.loads(error_body)
                mensaje_real = error_data.get('detail', "")
                
                if "contraseña" in mensaje_real.lower():
                    registro_msg = mensaje_real
                else:
                    registro_msg = "Error: El usuario o email ya existen."
            except:
                registro_msg = "Error: El usuario o email ya existen."
            
            return False

        except Exception as e:
            registro_msg = "Error de conexión: Revisa tu internet."
            return False


    # --- FUNCIÓN PARA CONECTAR AL LOGIN y CARGAR PARTIDA ---
    def conectar_login(username, password):
        global login_msg
        url = API_URL + "/api/login"
        datos = {"username": username, "password": password}
        
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() in [200, 201]:
                    # Leemos el JSON completo que nos devuelve la API
                    respuesta = json.loads(response.read().decode('utf-8'))
                    login_msg = "¡Acceso concedido!"
                    
                    # 1. Guardamos la identidad
                    renpy.store.persistent.user_id = respuesta.get("user_id")
                    renpy.store.persistent.nombre_jugador = respuesta.get("username")
                    renpy.store.pc_email = respuesta.get("email")
                    
                    # 2. CARGAMOS EL PROGRESO
                    progreso = respuesta.get("progreso", {})
                    renpy.store.capitulo_actual = progreso.get("capitulo", "prologo")
                    renpy.store.stress_level = progreso.get("estres", 0)
                    renpy.store.decisiones_tomadas = progreso.get("decisiones", {})
                    
                    return True

        except urllib.error.HTTPError as e:
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                login_msg = error_data.get('detail', "Error en el login.")
            except:
                login_msg = "Usuario o contraseña incorrectos."
            return False
            
        except Exception as e:
            login_msg = "Error de conexión: Revisa tu internet."
            return False


    # --- FUNCIÓN PARA GUARDAR PROGRESO ---
    def guardar_progreso(capitulo, estres, nuevas_decisiones):

        # Si no hay un usuario logueado, no hacemos nada
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
            
            # Usamos un timeout corto (3s) para que el juego no se congele al guardar
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.getcode() in [200, 201]:
                    return True
        except:
            # Si falla (por ej. corte de internet), lo ignoramos silenciosamente para no interrumpir el terror
            pass 
            
        return False

    # --- FUNCIÓN PARA BORRAR CUENTA ---
    def borrar_cuenta_api(id_usuario):
        if not id_usuario:
            return False
            
        url = API_URL + f"/api/delete-user/{id_usuario}"
        
        try:
            # Usamos method='DELETE' para decirle a la API qué queremos hacer
            req = urllib.request.Request(url, method='DELETE')
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.getcode() in [200, 201, 204]:
                    return True
        except:
            pass
            
        return False