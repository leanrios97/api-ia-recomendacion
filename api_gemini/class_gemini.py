import google.generativeai as genai


def configurationGemini(GOOGLE_API_KEY):
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        return model
    
    except Exception as e:
        print(f"No se puede Inicializar Gemini: {e}")


if __name__ == '__main__':
    
    clave_api = 'AIzaSyAhrPLDGWIyY_nx9sSxezbfygssruAfg1Y'
    
    configurationGemini(clave_api)
    
    
    