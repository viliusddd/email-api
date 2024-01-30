import os
import re
import requests
import smtplib
import socket
import sys

from email.mime.text import MIMEText


def get_response(url):
    """
    Connect to chosen api and return json response.

    Args:
        url (str): api url address

    Returns:
        dict: response from api
    """

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        print(f'FAILED: {exc}')
    else:
        return response.json()


def gen_email_body(response):
    return f"""
Hello,

give me a call, {response.lower()}.

Thanks,
V."""


def send_email(body, recipient):
    """
    Send email from gmail address

    Args:
        body (str): text body of email
        recipient (): email address of person to send to
    """

    password = os.getenv('GMAIL_PASS')
    msg = MIMEText(body)

    msg['Subject'] = "Urgent!"
    msg['From'] = "vj.testas@gmail.com"
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(msg['From'], password)
            smtp_server.sendmail(msg['From'], recipient, msg.as_string())
        print("Message sent!")
    except socket.error:
        sys.exit("Could not connect.")


def validate_email_addr(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email):
        return True


def get_api_resp(api):
    """
    Return response message from one of the two api endpoints

    Args:
        api (str): api url

    Returns:
        str: return message of chosen api
    """

    if api == 'corporatebs':
        resp = get_response('https://corporatebs-generator.sameerkumar.website')['phrase']
    elif api == 'techy':
        resp = get_response('https://techy-api.vercel.app/api/json')['message']

    return resp


def validate_args():
    if len(sys.argv) < 3:
        sys.exit('Usage: python proj2.py <email> <api_name>\n\n'
                 'Arguments:\n'
                 '  <api_name>      techy or corporatebs')

    if not validate_email_addr(sys.argv[1]):
        sys.exit("Invalid email address.")

    if sys.argv[2] not in ['techy', 'corporatebs']:
        sys.exit('Wrong API name. Choose either "techy" or "corporatebs".')


def main():
    validate_args()

    email_body = gen_email_body(get_api_resp(sys.argv[2]))
    send_email(email_body, sys.argv[1])


if __name__ == '__main__':
    main()


"""
5 keybindings:
- Alt + left/right/up/down -> move between vscode splits, terminal and side panels
- ctrl + ` -> toggle terminal
- gh -> highlight function description or error description (vim mode in vscode)
- Alt + B -> toggle bookmark line
- Alt + n/p -> move between bookmarks
"""
