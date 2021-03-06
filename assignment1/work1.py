import urllib2 as urllib
import oauth2 as oauth

access_token_key = "17057631-YjUx5DxLFYo972PI1BGiLet2PvLwWigKAX6rdTMni"
access_token_secret = "4f5RlOZg7TM1F1d0oCaJORzKWeZFa5AaOycZWyPFBI"

consumer_key = "elCjs6JE6RIXDHDHab0KA"
consumer_secret = "zTh4jajeK1epvXYSNKOnCIDxSCPansKnzD6NdETeSr8"

oauth_token = oauth.Token(
    key=access_token_key,
    secret=access_token_secret
)

oauth_consumer = oauth.Consumer(
    key=consumer_key,
    secret=consumer_secret
)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

_debug = 0

http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


def twitter_request(url, method, parameters):
    '''
    Construct, sign and open a twitter request using the
    hard-coded credentials above.
    '''
    req = oauth.Request.from_consumer_and_token(
        oauth_consumer,
        token=oauth_token,
        http_method=http_method,
        http_url=url,
        parameters=parameters
    )

    req.sign_request(
        signature_method_hmac_sha1,
        oauth_consumer, oauth_token
    )

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response


def fetch_samples():
    '''
    Fetch sample data from twitter 1% stream
    '''
    url = "https://stream.twitter.com/1/statuses/sample.json"
    parameters = []
    response = twitter_request(url, "GET", parameters)
    for line in response:
        print line.strip()


def main():
    fetch_samples()

if __name__ == "__main__":
    main()
