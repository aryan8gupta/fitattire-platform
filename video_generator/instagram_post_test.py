import requests
import os

my_var1 = os.getenv('Instagram_Access_Token', 'Default Value')
my_var2 = os.getenv('Instagram_Business_Account_ID', 'Default Value')

ACCESS_TOKEN = my_var1
INSTAGRAM_BUSINESS_ACCOUNT_ID = my_var2

# Publicly accessible image URL and caption
image_url = 'https://upload.wikimedia.org/wikipedia/commons/0/09/India_Gate_in_New_Delhi_03-2016.jpg'
caption = 'Test post using Instagram from standalone script'

# Step 1: Create media object
create_url = f'https://graph.facebook.com/v22.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media'
print("1/2")
create_payload = {
    'image_url': image_url,
    'caption': caption,
    'access_token': ACCESS_TOKEN,
}
create_resp = requests.post(create_url, data=create_payload)
print("Media Creation Response:", create_resp.json())

if create_resp.status_code == 200:
    creation_id = create_resp.json().get('id')
    print(creation_id)
    # Step 2: Publish the media
    publish_url = f'https://graph.facebook.com/v22.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish'
    publish_payload = {
        'creation_id': creation_id,
        'access_token': ACCESS_TOKEN,
    }
    publish_resp = requests.post(publish_url, data=publish_payload)
    print("Publish Response:", publish_resp.json())
else:
    print("Failed to create media object")
