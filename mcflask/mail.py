import requests
from mcflask import app

key = app.config['KEY']
sandbox = app.config['MAIL_SANDBOX']

from mcflask import debug

def sendMail(user, recipient, subject, text):

    request_url = 'https://api.mailgun.net/v3/'+sandbox+ '/messages'
    request = requests.post(request_url, auth=('api', key), data={
        'from': user+'@'+'sandbox',
        'to': recipient,
        'subject': subject,
        'text': text
    })
    if debug:
        print ('Status: '+ str(request.status_code))
        print ('Body:   '+ str(request.text))
