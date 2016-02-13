import os

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

from dotify import app
from dotify.database import Base, session
from dotify.models import Country
from dotify.resources.countries import countries
from dotify.top_songs import TopSongsGenerator
from dotify.recommendation.implicit_mf.ratings_matrix import RatingsMatrix
from dotify.recommendation.implicit_mf.vectors import CountryVectors, SongVectors
from dotify.recommendation.implicit_mf.implicit_mf import ImplicitMF


manager = Manager(app)


F = 30
ALPHA = 40
LAMBDA = 1


@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)


@manager.command
def insert_countries():
    for country_name in countries.keys():
        country = Country(
            id=countries[country_name]['id'],
            name=country_name
        )
        session.add(country)
    session.commit()


@manager.command
def insert_top_songs():
    for country_name in countries.keys():
        for top_song in TopSongsGenerator(country_name):
            session.add(top_song)
    session.commit()

@manager.command
def compute_latent_vectors():
    implicit_mf = ImplicitMF(
        country_vectors_class=CountryVectors,
        song_vectors_class=SongVectors,
        ratings_matrix=RatingsMatrix(),
        f=F,
        alpha=ALPHA,
        lmbda=LAMBDA
    )
    implicit_mf.run()


class DB:
    def __init__(self, metadata):
        self.metadata = metadata


migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

