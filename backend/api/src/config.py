import os
from dotenv import load_dotenv


rutasrc= os.path.abspath(os.path.dirname(__file__), )
rutaraiz= os.path.join(rutasrc, "..")
class Config:

    TokenCoc= os.getenv('TOKEN_COC',)
    if TokenCoc is None:
          raise ValueError('No se ha definido la variable de entorno')
    
    patchTempReport= os.getenv('PATCH_TEMP_REPORT', os.path.join(rutasrc, 'templates/report.xlsx'))
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
        if os.getenv('DB_HOST') is None:
            raise ValueError('No se ha definido la variable de entorno de BD')
        return {
            'host': os.getenv('DB_HOST', ),
            'user': os.getenv('DB_USER', ),
            'port': os.getenv('DB_PORT', 3306),
            'password': os.getenv('DB_PASSWORD', ),
            'database':os.getenv('DB', ),
            }