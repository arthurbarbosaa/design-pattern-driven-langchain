class NotificationService:
    def __init__(self):
        pass

    def send_notification(self, notification_type, message, recipient):
        if notification_type == "email":
            # Passos simulados para envio de email
            print("Conectando ao servidor SMTP...")
            print("Formatando mensagem com template HTML...")
            print(f"Enviando Email para {recipient}: {message}")

        elif notification_type == "sms":
            # Passos simulados para envio de SMS
            print("Conectando ao gateway de SMS...")
            print("Validando comprimento da mensagem (max 160 caracteres)...")
            print(f"Enviando SMS para {recipient}: {message}")

        elif notification_type == "push":
            # Passos simulados para envio de Push Notification
            print("Autenticando com APNS/FCM...")
            print("Roteando para o token do dispositivo...")
            print(f"Enviando Push Notification para {recipient}: {message}")

        else:
            raise ValueError(
                f"Tipo de notificação desconhecido: {notification_type}")


# Exemplo de uso
if __name__ == "__main__":
    service = NotificationService()

    service.send_notification(
        "email", "Bem-vindo ao nosso sistema!", "usuario@exemplo.com")
    service.send_notification(
        "sms", "Seu código de verificação é 12345.", "+5511999999999")
    service.send_notification(
        "push", "Você tem uma nova mensagem.", "token_abc123")
