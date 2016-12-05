from datetime import datetime

from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
parcels = Table('parcels', post_meta,
    Column('tracking_number', String, primary_key=True, nullable=False),
    Column('destination_country', String, default=ColumnDefault('FR')),
    Column('postal_service', String, default=ColumnDefault('upu')),
    Column('added', DateTime, default=ColumnDefault(datetime.now)),
    Column('updated', DateTime, onupdate=ColumnDefault(datetime.now)),
    Column('description', String),
    Column('received', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['parcels'].columns['received'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['parcels'].columns['received'].drop()
