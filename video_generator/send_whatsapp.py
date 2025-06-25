import requests
import json

def send_invoice_whatsapp_message(
    recipient_number, user_name, company_name, amount, invoice_id, instagram_link
):
    # Replace these with your actual values
    ACCESS_TOKEN = 'EAAO7ESXUNP0BO8L0IeGFfXqqsLJ5fvOyMa7pWwFGoqw2ZArNp5oSaZCtxnCLapvuZCFGjzIUZBBIGdgrVklo9ORxk2Oc1g11epqVL3HksCFzD8DNb7JYxT8x0C5QQjcnp7kABecV5ojpG9QU9p9ilz4udGovUIL18VG3lWKeve3VxBUD2eVboCjm9O4LWZAVwICrgxe4DkbJZAZBGyVu3im1opHRa24UNbyc27hlpZAB'
    PHONE_NUMBER_ID = '671305912732731'
    RECIPIENT_NUMBER = '918800236182'  # Must include country code
    url = f'https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages'

    invoice_link = f'https://fitattire.shop/invoice/{invoice_id}'

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    payload = {
        'messaging_product': 'whatsapp',
        'to': recipient_number,
        'type': 'template',
        'template': {
            'name': 'invoice_template_2',  # Use your approved template name
            'language': { 'code': 'en_US' },
            'components': [
                {
                    'type': 'header',
                    'parameters': [
                        {
                            'type': 'image',
                            'image': {
                                'link': 'https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/Screenshot 2025-06-23 at 1.56.44 PM.png'
                            }
                        }
                    ]
                },
                {
                    'type': 'body',
                    'parameters': [
                        { 'type': 'text', 'text': user_name },
                        { 'type': 'text', 'text': company_name },
                        { 'type': 'text', 'text': str(amount) },
                        { 'type': 'text', 'text': invoice_link },
                        { 'type': 'text', 'text': instagram_link }
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return {
        "status_code": response.status_code,
        "response": response.json()
    }
