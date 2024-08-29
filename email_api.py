import os
import re
import requests
import smtplib
import socket
import sys

from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()


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
        print(f"FAILED: {exc}")
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

    msg = MIMEText(body)

    msg["Subject"] = "Urgent!"
    msg["From"] = os.getenv("SENDER_EMAIL")
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(msg["From"], os.getenv("SENDER_APP_PASS"))
            smtp_server.sendmail(msg["From"], recipient, msg.as_string())
        print("Message sent!")
    except socket.error:
        sys.exit("Could not connect.")


def validate_email_addr(email):
    regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )

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

    if api == "corporatebs":
        url = "https://corporatebs-generator.sameerkumar.website"
        resp = get_response(url)['phrase']
    elif api == "techy":
        resp = get_response("https://techy-api.vercel.app/api/json")["message"]

    return resp


def args():
    if len(sys.argv) != 3:
        sys.exit("Usage: python email_proj.py <email> <api_name>\n\n"
                 "Arguments:\n"
                 "  <api_name>      techy or corporatebs")

    if not validate_email_addr(sys.argv[1]):
        sys.exit("Invalid email address.")

    if sys.argv[2] not in ["techy", "corporatebs"]:
        sys.exit('Wrong API name. Choose either "techy" or "corporatebs".')

    return sys.argv[1:]


def main():
    email_addr, api_url = args()

    email_body = gen_email_body(get_api_resp(api_url))
    send_email(email_body, email_addr)


if __name__ == "__main__":
    main()


"""
5 keybindings:
- Alt + left/right/up/down -> move between vscode splits, terminal and
  side panels.
- ctrl + ` -> toggle terminal.
- gh -> highlight function description or error description (vim mode in
  vscode).
- Alt + B -> toggle bookmark line
- Alt + n/p -> move between bookmarks
"""
