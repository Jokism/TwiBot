from flask import Flask, request
from markupsafe import escape
from twilio.twiml.messaging_response import MessagingResponse
import tweepy
from random import randrange

##############################################################################
# Chat bot will recognize keywords in messages sent by the user and responds #
# with a quote or image                                                      #
##############################################################################


# Create Flask instance
app = Flask(__name__)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)



media_urls = []

try:
    api.verify_credentials()
    print("Authentication OK")

    members = api.list_members(list_id = TWITTER_LIST_ID)


    for member in members:
        tweet = api.user_timeline(screen_name=member.screen_name, count=1, include_rts=False,tweet_mode='extended')

        for item in tweet:
            if 'media' in item.entities:
                for data in item.entities['media']:
                    media_urls.append(data['media_url_https'])

except:
    print("Error during authentication")



# Decorator that tells Flask which URL should trigger the function
@app.route('/TwiBot', methods=['POST'])
def bot():
    # analyze the message sent by user => return appropriate response
    incoming_msg = request.values.get('Body','').lower()

    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'quote' == incoming_msg:
        # return a quote
        r = requests.get('https://api.quoteable.io/random')

        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'There\'s probably a quote for this situation somewhere...'

        msg.body(quote)
        responded = True

    if 'cat' == incoming_msg:
        # return a picture of a cat
        msg.media('https://cataas.com/cat')
        responded = True

    if 'ooc' == incoming_msg:
        # return an 'out of context' image from twitter
        msg.media(media_urls[randrange(len(media_urls)+1)])
        responded = True

    if not responded:
        msg.body('Acceptable inputs are "cat", "quote", "ooc"')

    return str(resp)



if __name__ == '__main__':
    app.run()


