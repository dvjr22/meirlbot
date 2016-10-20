import argparse
import base64

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def main(photo_file):
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 5
                }]
            }]
        })
        response = service_request.execute()

        for res in response['responses'][0]['labelAnnotations']:
            label = res['description']
            print(label)
            print('Found label: %s for %s' % (label,photo_file))
            with open("keywords.txt", "a") as myfile:
                if(checkBlacklist(label)):
                    myfile.write("\n" + label)
                else:
                    print('Skipping %s due to the blacklist' % label)
            print "BREAK\n"

def checkBlacklist(word):
    with open("blacklistKeywords.txt",'r') as my_file:
        for line in my_file:
            if line.rstrip() == word:
                print('is in blacklist')
                return False
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    main(args.image_file)
