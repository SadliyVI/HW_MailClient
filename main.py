from mail_client import MailClient

if __name__ == '__main__':
    # Пример использования
    mail_client = MailClient(
        login='your_login@gmail.com',
        password='your_password'
    )

    # Отправка письма
    mail_client.send_email(
        subject='Test Subject',
        recipients=['recipient1@example.com'],
        message='Test Message'
    )

    # Получение письма
    try:
        email_message = mail_client.receive_email(header='Test Subject')
        print('Письмо получено:', email_message)
    except ValueError as e:
        print(e)