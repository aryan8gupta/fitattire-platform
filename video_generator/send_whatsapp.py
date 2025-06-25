import requests
import os
import json

def send_invoice_whatsapp_message(
    recipient_number, user_name, company_name, amount, invoice_id, instagram_link
):
    
    my_var1 = os.getenv('Whatsapp_Access_Token', 'Default Value')
    my_var2 = os.getenv('Whatsapp_Phone_Number_Id', 'Default Value')

    ACCESS_TOKEN = my_var1
    PHONE_NUMBER_ID = my_var2

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
