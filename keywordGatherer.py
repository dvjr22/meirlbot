############################################################
#                      Keyword Gatherer                    #
# Creator: Tyler Moon                                      #
# Contributors:                                            #
# Purpose: This script takes in an image file as a         #
# parameter and runs that image through the                #
# Google Image API to determine keywords describing the    #
# image                                                    #
############################################################
import argparse
import base64

# Connection to the Google Vision API
from googleapiclient import discovery
# GoogleCredentials authentication library
from oauth2client.client import GoogleCredentials



def main(photo_file):
    # Load the credentials for the Google Vision API from the path variable $GOOGLE_APPLICATION_CREDENTIALS
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    # Open the image file as passed in the parameter
    with open(photo_file, 'rb') as image:
        # Encode the image to 64 bit
        image_content = base64.b64encode(image.read())
        # Parameters to pass to the Google Vision API
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    # Image to load
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    # Type of response
                    'type': 'TEXT_DETECTION',
                    # Number of results to return
                    'maxResults': 1
                }]
            }]
        })
        response = service_request.execute()
        print response
        print '\n'
        print response['responses'][0]['textAnnotations'][0]['description']
        # Parse the response from the API
        text = response['responses'][0]['textAnnotations'][0]['description'].replace('\n',' ')
        print 'TEXT %s' % text
        with open("keywords.txt", "a") as myfile:
            myfile.write(text + "\n")



# This code parses multiple response
        #for res in response['responses'][0]['textAnnotations']:
        #    label = res['description']
    #        print('Found label: %s for %s' % (label.replace('\n',' '),photo_file))
    #        # Write keywords to a textfile
    #        with open("keywords.txt", "a") as myfile:
    #            # If the keyword is in the blacklistKeywords.txt file then dont write it
    #            if(checkBlacklist(label)):
    #                myfile.write(label.replace('\n',' ') + " ")
    #            else:
    #                print('Skipping %s due to the blacklist' % label)
    #        print "BREAK\n"
    #        with open("keywords.txt", "a") as myfile:
    #            myfile.write('\n')

# Check the blacklist file for a match with the parameter word
def checkBlacklist(word):
    with open("blacklistKeywords.txt",'r') as my_file:
        for line in my_file:
            # The .rstrip() removes the newline or whitespace characters
            if line.rstrip() == word:
                print('is in blacklist')
                return False
        return True

if __name__ == '__main__':
    # Get the parameter from the commandline
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    main(args.image_file)
