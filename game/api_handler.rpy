init python:
    import json
    import urllib.request
    import urllib.error

    API_URL = "https://api-proyecto-sandy.vercel.app" 
    
    registro_msg = "" 

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