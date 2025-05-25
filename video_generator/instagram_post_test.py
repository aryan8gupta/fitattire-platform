import requests

# Replace with your actual values
ACCESS_TOKEN = 'EAAO7ESXUNP0BO0473nW3auKIF7tTU1VDG4cZBcTllQ7SYD9EiTq8MwAoqAVFwjLZBFB9Tl33U3KWPoH5SAOZCZAUvQxuGfrIySEPSru5V5HBNMzbnOPuzm5mVZCRtELXKKRm9T5R8Cb6kscNEP2dKPl4YZA6yoi1Ov4JOynuxszaraVWZBosPvz'
INSTAGRAM_BUSINESS_ACCOUNT_ID = '17841465081391593'
print("0")
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
print("1")
create_resp = requests.post(create_url, data=create_payload)
print("Media Creation Response:", create_resp.json())
print("2")

if create_resp.status_code == 200:
    print("3")
    creation_id = create_resp.json().get('id')
    print(creation_id)
    # Step 2: Publish the media
    publish_url = f'https://graph.facebook.com/v22.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish'
    print("4")
    publish_payload = {
        'creation_id': creation_id,
        'access_token': ACCESS_TOKEN,
    }
    print("5")
    publish_resp = requests.post(publish_url, data=publish_payload)
    print("Publish Response:", publish_resp.json())
else:
    print("Failed to create media object")
