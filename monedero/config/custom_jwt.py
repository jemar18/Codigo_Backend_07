def manejo_error_JWT(error):
    print(error)
    print(type(error))
    print(error.status_code)
    print(error.description)
    print(error.headers)
    print(error.error)

    respuesta={
        "success":False,
        "content":None,
        "message":None
    }
    if error.error=='Authorization Required':
        respuesta["message"]="Se necesita un toquen para esta peticion"
    elif error.error=='Bad Request':
        respuesta["message"]="Credenciales Invalidas"
    
    return respuesta, error.status_code