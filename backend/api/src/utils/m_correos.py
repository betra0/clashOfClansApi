
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EnviadorDeCorreos():
    def __init__(self, remitente, contraseña):
        self.remitente = remitente
        self.contraseña = contraseña
        self.server = None

    def conectar(self):
        if not self.esta_conectado():
            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.starttls()
            self.server.login(self.remitente, self.contraseña)
            

    def esta_conectado(self):
        return self.server and self.server.noop()[0] == 250

    def enviar_correo(self, destinatario, asunto, mensaje):
        self.conectar()  # Asegura que la conexión esté activa
        msg = MIMEMultipart()
        msg['From'] = self.remitente
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(mensaje, 'plain'))
        """ print('se a conectado') """

        try:
            self.server.send_message(msg)
            
        except Exception as e:
            print(f"Error: {e}")

    def desconectar(self):
        if self.esta_conectado():
            self.server.quit()

# Uso de la clase
if __name__ == "__main__":
    correo = EnviadorDeCorreos("debugapiserver@gmail.com", "tjlo wnnm qveq zkyn")
    correo.enviar_correo("tolozadaniel5@gmail.com", "Primer correo", "Mensaje del primer correo.")
    correo.enviar_correo("tolozadaniel5@gmail.com", "Segundo correo", "Mensaje del segundo correo.")
    
    correo.desconectar()