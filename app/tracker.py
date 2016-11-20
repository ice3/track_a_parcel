#!/usr/bin/env python
"""Part to track the parcels."""

from collections import OrderedDict
import json
import urllib.request
import logging

logger = logging.getLogger('root')
FORMAT = (
    '[%(asctime)s :: %(levelname)s '
    '%(filename)s:%(lineno)s - %(funcName)10s() ]'
    ' :: %(message)s'
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


class Tracker():
    """Tracks a parcel using myparcels REST API."""

    def __init__(self):
        """Initialisation.

        We set the API stuff.
        """
        self.base_url = 'http://myparcels.ru/api/freeapp.php?cmd='
        self.API_KEY = "74ce6d236c8c53f64a7ed60d76bb3f94"
        self.DEVICE_ID = 354833057607398

        logger.debug("Init tracker with infos")
        logger.debug("base url: {}".format(self.base_url))
        logger.debug("api key: {}".format(self.API_KEY))
        logger.debug("device id: {}".format(self.DEVICE_ID))

    def parcel_dictionnary(self, parcel):
        """Create an ordered dictionnary with the correct info for the API.

        Input :
            parcel: tuple (
                str with the tracking number
                OPTIONAL str with the destination country
                OPTIONAL str with the postal service
            )
        """
        number = parcel[0]
        dst_country = parcel[1] if len(parcel) > 1 else "FR"
        service = parcel[2] if len(parcel) > 2 else "upu"

        d = OrderedDict([("trackingNumber", number),
                        ("dstCountry", dst_country),
                        ("postalService", service)])
        return d

    def parcel_string(self, parcels):
        """Convert a list of parcels tuple to a API friendly format."""
        parcel_dicts = [self.parcel_dictionnary(p) for p in parcels]
        return json.dumps(parcel_dicts)

    def create_url_1(self, parcels):
        """Return the first URL to query."""
        url = self.base_url
        url += "track&apiKey={api_key}&deviceId={device_id}&parcels={parcels}"

        return url.format(
            api_key=self.API_KEY,
            device_id=self.DEVICE_ID,
            parcels=self.parcel_string(parcels)
        )

    def create_url_2(self, uid):
        """Return the second url to query."""
        url = self.base_url
        url += "status&apiKey={api_key}&deviceId={device_id}&requestId={uid}"
        return url.format(
            api_key=self.API_KEY,
            device_id=self.DEVICE_ID,
            uid=uid
        )

    def get_answer(self, url):
        """Get the content from an url and jsonify it."""
        return json.loads(
            urllib.request.urlopen(url).read().decode("utf-8")
        )

    def track(self, parcels):
        """Track a list of parcels using the api.

        A parcel is a tuple with a tracking number and an optional country.

        The API needs 2 calls to track something :
         * one call to declare the tracking number with return a uid
         * one call to get the parcels positions using the previous uid
        """
        url = self.create_url_1(set(parcels))
        logger.debug("contacting url 1: {}".format(url))

        answer = self.get_answer(url)
        logger.info("got answer: {}".format(answer))

        uid = answer['requestId']
        logger.info("extracted uid: {}".format(uid))

        url = self.create_url_2(uid)
        logger.debug("contacting url 2: {}".format(url))

        answer = self.get_answer(url)
        logger.info("got answer: {}".format(answer))

        return answer

if __name__ == "__main__":
    from pprint import pprint

    t = Tracker()
    pprint(t.track([
        ("RS806620392CN",),
        ("RS619965431NL",),
    ]))
