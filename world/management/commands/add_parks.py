from django.core.management import BaseCommand
from datetime import date
from world.models import Park
import oauth2
import requests
from geodjango.settings import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, \
    TOKEN_SECRET


class Command(BaseCommand):
    """
        Takes zip_code as an argument, pings yelp's api for the parks in that
            area, and adds the data from those parks to the database as Park
            Objects.
    """

    def add_arguments(self, parser):
        parser.add_argument('zip_code', nargs='+', type=str)

    def handle(self, *args, **options):
        """

        :param args: zip_code ex. 89123
        :param options:
        :return: Writes out how many parks added to database
        """

        url = 'http://api.yelp.com/v2/search/' + '?location=' + \
              options['zip_code'][0] + ', NV &category_filter=parks'

        consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        oauth_request = oauth2.Request(method="GET", url=url)

        oauth_request.update(
            {
                'oauth_nonce': oauth2.generate_nonce(),
                'oauth_timestamp': oauth2.generate_timestamp(),
                'oauth_token': TOKEN,
                'oauth_consumer_key': CONSUMER_KEY
            }
        )
        token = oauth2.Token(TOKEN, TOKEN_SECRET)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        signed_url = oauth_request.to_url()
        response = requests.get(signed_url)
        content = response.json()
        parks = content['businesses']

        count = 0
        for park in parks:
            park_name = park['name']
            park_exists = Park.objects.filter(name=park_name)
            if len(park_exists) == 0:
                park_latitude = str(park['location']['coordinate']['latitude'])
                park_longitude = str(park['location']['coordinate']['longitude'])
                Park.objects.create(
                    name=park_name,
                    location='POINT(' + park_latitude + ' ' + park_longitude + ')',
                )
                count += 1

        self.stdout.write("{} Parks Added to Database".format(count))
