import os
from dotenv import load_dotenv


rutasrc= os.path.abspath(os.path.dirname(__file__), )
rutaraiz= os.path.join(rutasrc, "..")
if not os.getenv('DOCKER'):
    for var in ['TOKEN_EXPIRATION_DAYS', 'SECRET_KEY', 'EMAIL_LOG', 'EMAIL_MAIL', 'EMAIL_TOKEN', 'RUTA_LOG', 'RUTA_TESIS_FILE','DB_HOST', 'DB_USER', 'DB_PORT','DB_ROOT_PASSWORD', 'DATABASE']:
        if var in os.environ:
            print(f'Variable {var} encontrada y eliminada: {os.environ[var]}') 
            del os.environ[var] 
    print('Load_dotENV:', load_dotenv(dotenv_path=os.path.join(rutaraiz, ".env")))
    
class Config:

    TokenCoc= os.getenv('TOKEN_COC')
    ClanId = os.getenv('CLAN_ID', '292OYCJV2')
    URL_COC = os.getenv('URL_COC', 'https://api.clashofclans.com/v1')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    email_log = os.getenv('EMAIL_LOG', 'False').lower() == 'true'  # Convertir a booleano
    email = {
        'mail': os.getenv('EMAIL_MAIL'),
        'token': os.getenv('EMAIL_TOKEN'),
    }
    rutalog = os.getenv('RUTA_LOG')
    rutatesisfile = os.getenv('RUTA_TESIS_FILE')

def getconfig_bd():
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'dany'),
            'port': os.getenv('DB_PORT', 3306),
            'password': os.getenv('DB_PASSWORD', '12345'),
            'database':os.getenv('DB', 'coc'),
            }