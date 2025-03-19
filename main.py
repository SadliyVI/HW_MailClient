from mail_client import MailClient
import  configparser


def send_email(mail_client):
    mail_client.send_email(
        subject = input('Введите тему сообщения: '),
        recipients = [input('Введите адрес получателя: ')],
        message = input('Введите текст сообщения: ')
    )

def receive_email(mail_client):
    try:
        email_message = mail_client.receive_email(header = 'Test Subject')
        print('Письмо получено:', email_message)
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    # Пример использования
    config = configparser.ConfigParser()
    config.read('settings.ini')
    mail_client = MailClient(
        login = config['MailAtr']['login'],
        password = config['MailAtr']['password']
    )

    # Отправка письма
    send_email(mail_client)

    # Получение письма
    receive_email(mail_client)