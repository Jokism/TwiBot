# TwiBot

## Description:

A simple bot that leverages the Twitter API to retrieve the most recent statuses (Default: 1 per account) from a Twitter list and forwards that to the Twilio service which sends an image to the user when sent the keyword `ooc` (Out of context). The user may also send keywords "cat" and "quote" to receive a random image of a cat or a random quote, respectively


## Install Dependencies:

`pip install -r requirements.txt`


## API Keys:

Register for API keys on Twitter and Twilio, and export the keys into the appropriate environment variables


## Usage:

`python3 twiBot.py`


Send a text message to your registered Twilio number. Acceptable inputs are "quote", "cat", "ooc"
