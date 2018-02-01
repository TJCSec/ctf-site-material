import mailgun_config as mailgun
import requests

def validate_email(email_address):
    auth_data = ("api", mailgun.pub_key)
    payload = {"address": email_address}
    data = requests.get("https://api.mailgun.net/v3/address/validate", auth=auth_data, params=payload).json()
    print(data)
    return data['is_valid']

def send_confirmation_email(name, email_address):
    auth_data = ('api', mailgun.mailgun_key)
    email_from = 'TJCTF 2018 <noreply@{}>'.format(mailgun.site_url)
    email_to = [email_address]
    subject = "Thanks For Signing Up for TJCTF Emails!"
    body = "Hi {},\n\nThank you for signing up for TJCTF Emails. We will send out more information about TJCTF 2018 as it becomes available.\n\nThanks,\nTJCTF 2018".format(name)
    send_data = {"from": email_from,
            "to": email_to,
            "subject": subject,
            "text": body}
    r = requests.post(mailgun.mailgun_url + '/messages', auth=auth_data, data=send_data)
    return r.status_code == 200

def get_list(name):
    auth_data = ('api', mailgun.mailgun_key)
    data = requests.get('https://api.mailgun.net/v3/lists', auth=auth_data).json()
    lists = [str(data['items'][i]['name']) for i in range(int(data["total_count"]))]
    return name in lists

def create_list(name):
    auth_data = ('api', mailgun.mailgun_key)
    send_data = {'address': '{}@{}'.format(name, mailgun.site_url), 'name': name}
    data = requests.post("https://api.mailgun.net/v3/lists", auth=auth_data, data=send_data).json()
    return data["message"] == 'Mailing list has been created'

def add_user_to_list(name, email, list_name):
    auth_data = ('api', mailgun.mailgun_key)
    send_data = {'subscribed': True,
                 'address': email,
                 'name': name}
    data = requests.post("https://api.mailgun.net/v3/lists/{}@{}/members".format(list_name, mailgun.site_url), auth=auth_data, data=send_data).json()
    if data["message"] == 'Mailing list member has been created' or "Address already exists" in data["message"]:
        return True
    else:
        print(data["message"])
        return False
