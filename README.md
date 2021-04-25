# inventory_check

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/cyberrumor)

Checks inventory of configurable products with automatic rate limiting. Notifies via Pushover.


Please be polite and don't spam retailers with excessive requests. Don't use this for reselling.

# Installation

- Get your device set up with [Pushover](pushover.net) and create an application on their website. 
- Copy your user ID and your application's API token into credentials.py. In the Pushover app on your phone, tell it to automatically open URLs when launched via notification. 
- Set the URL handler to 'opener' if you want to use the retailer's app. 
- If you have an iphone, configure Apple Pay with your fingerprint so you can check out instantly with Newegg. 
- Install Python3, add python3 your PATH environment variable. There's youtube tutorials for this if you don't know what I'm talking about.

# Usage
- Open a terminal in the folder with this script in it, and enter the following, substituting 'rtx 2070 8gb' for whatever product you're looking for.
- `python3 inventory_check.py 'rtx 2070 8gb'`
- You will be presented with a list of product landing pages where that item can be purchased. Note that this doesn't verify seller on Amazon, but it will only use first party sellers on BestBuy and Newegg. Enter your selections and press Enter.
- You will be notified via Pushover as soon as a restock is detected. Good luck!
