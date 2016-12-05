"""Configuration for track_a_parcel project."""

import os
import logging
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

logger = logging.getLogger('root')
FORMAT = (
    '[%(asctime)s :: %(levelname)s '
    '%(filename)s:%(lineno)s - %(funcName)10s() ]'
    ' :: %(message)s'
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


EVENT_TRADS = {
    10: "envoie ajouté au site",
    100: "informations sur l'envoie entrée electroniquement",
    105: "importation",
    110: "Recu par China Post",
    145: "Arrivé à un point de transit",
    150: "Quitte le point de transit",
    160: "Arrive dans un centre de tri",
    165: "Tri en cours",
    180: "Quitte la poste (changement de livreur ?)",
    185: "Arrivé au lieu de livraison",
    195: "Tentative de livraison infructueuse",
    200: "Présenté et remis au destinataire",
}

CITY_TRADS = {
    "Шэньчжэнь": "Shenzhen",
    "Лилль": "Lille",
}

EVENTS_WITH_CITY = [145, 150, 185, 195, 200]