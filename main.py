import imaplib # Para se conectar ao servidor IMAP e ler e-mails.
import email # Para processar e-mails.
from email.mime.text import MIMEText # Para criar o corpo do e-mail em formato de texto.
import smtplib # Para enviar e-mails via SMTP.
import os
import urllib.parse
from dotenv import load_dotenv # Acesso ao arquivo .env

import logging
logging.basicConfig(level=logging.DEBUG)

class EmailAutomator:
    def __init__(self, imap_server, smtp_server, email_account, email_password):
        # Inicializa a classe EmailAutomator com informações de configuração do servidor IMAP e SMTP
        self.imap_server = imap_server
        self.smtp_server = smtp_server
        self.email_account = email_account
        self.email_password = email_password

    def check_inbox(self):
        # Conecta ao servidor IMAP para verificar a caixa de entrada.

        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)

        try:
            result, data = mail.login(self.email_account, self.email_password)
            print("Login resultado:", result)  # Deve ser 'OK'
            mail.select('inbox')
        except imaplib.IMAP4.error as e:
            print(f"Erro ao fazer login: {e}")

        # Codifica a string para UTF-8 antes de passar para a busca do IMAP.
        subject_search = urllib.parse.quote('Tarefa Automática', safe='')

        # Pesquisa por e-mails não lidos com o assunto "Tarefa Automática".
        status, messages = mail.search(None, f'(UNSEEN SUBJECT "{subject_search}")')

        print("Se finalizou aqui, é porque não tem paramentros que atendem o solicitado!")

        # Itera sobre os e-mails encontrados.
        for num in messages[0].split():
            print("entrou no loop for")
            status, msg_data = mail.fetch(num, '(RFC822)') # Obtém o conteúdo completo do e-mail.
            msg = email.message_from_bytes(msg_data[0][1]) # Decodifica o e-mail.

            # Extrai o assunto e o remetente do e-mail.
            subject = msg['subject']
            sender = msg['from']
            print(f'Recebido de {sender}: {subject}')

            # Verifica se o e-mail é multipart (ou seja, contém anexos ou partes alternativas).
            if msg.is_multipart():
                # Se multipart, extrai o corpo do primeiro item.
                body = msg.get_payload(0).get_payload(decode=True).decode()
            else:
                # Se não for multipart, extrai o corpo diretamente.
                body = msg.get_payload(decode=True).decode()
            print('Corpo:', body)

            # Envia uma resposta automática para o remetente.
            self.send_response(sender, 'Resposta Automática', 'Recebemos sua mensagem, obrigado!')

        mail.logout()

    def send_response(self, to_email, subject, body):
        # Cria uma resposta para o e-mail usando o corpo e o assunto fornecidos.

        #logging.debug(f'Enviando resposta para: {to_email}')

        # Cria uma resposta para o e-mail usando o corpo e o assunto fornecidos.
        try:
            print(f'Enviando resposta para: {to_email}')  # Verifique se isso é impresso.

            msg = MIMEText(body, _charset='utf-8') # Cria a mensagem de texto.
            msg['From'] = self.email_account
            msg['To'] = to_email
            msg['Subject'] = subject

            # Conecta ao servidor SMTP para enviar a resposta.
            server = smtplib.SMTP_SSL(self.smtp_server, 465)
            server.login(self.email_account, self.email_password)
            server.sendmail(self.email_account, to_email, msg.as_string())
            server.quit()
            print(f'Resposta enviada para {to_email}')

        except Exception as e:
            #logging.error(f'Ocorreu um erro ao enviar a resposta: {e}')
            print(f'Ocorreu um erro ao enviar a resposta: {e}')

# O código principal para rodar o automator.
if __name__ == '__main__':
    # Carregar variáveis do .env
    load_dotenv()

    automator = EmailAutomator(
        imap_server='imap.gmail.com',
        smtp_server='smtp.gmail.com',
        email_account=os.getenv('EMAIL_ACCOUNT'),
        email_password=os.getenv('EMAIL_PASSWORD')
    )

    automator.check_inbox()
