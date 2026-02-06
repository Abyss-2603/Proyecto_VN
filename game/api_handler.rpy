init python:
    import json
    import urllib.request
    import urllib.error

    API_URL = "https://api-proyecto-sandy.vercel.app" 
    
    # Variable para mensajes de error/éxito
    registro_msg = "" 

    def conectar_registro(username, email, password):
        global registro_msg
        url = API_URL + "/api/register"
        
        datos = {"username": username, "email": email, "password": password}
        
        try:
            json_data = json.dumps(datos).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req) as response:
                if response.getcode() in [200, 201]:
                    registro_msg = "¡Éxito! Cuenta creada."
                    renpy.store.persistent.nombre_jugador = username #Guardar usuario
                    renpy.store.pc_email = email # Guardar email
                    return True
                    
        except urllib.error.HTTPError:
            registro_msg = "Error: El usuario o email ya existen."
            renpy.notify(registro_msg)
            return False
        except Exception as e:
            registro_msg = "Error de conexión."
            renpy.notify(str(e))
            return False