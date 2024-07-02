import logging

class EmailService:
    @staticmethod
    def send_email(recipient_email, subject, message):
        # Simular implementação de envio de email
        logging.info(f"Simulated sending email to {recipient_email}: Subject - {subject} | Message - {message}")