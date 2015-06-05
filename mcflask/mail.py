import requests
from mcflask import app

key = app.config['KEY']
sandbox = 'mail.minezrc.com'

from mcflask import debug

def sendMail(user, recipient, subject, text):

    request_url = 'https://api.mailgun.net/v3/mail.minezrc.com/messages'
    request = requests.post(request_url, auth=('api', key), data={
        'from': user+'@mail.minezrc.com',
        'to': recipient,
        'subject': subject,
        'text': text
    })
    if debug:
        print ('Status: '+ str(request.status_code))
        print ('Body:   '+ str(request.text))
