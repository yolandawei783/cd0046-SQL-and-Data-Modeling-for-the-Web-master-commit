from app import db 
from app import Venue
from app import Artist
from app import Show

venues_data = [
    Venue(
        id = 1,
        name = 'THE MUSICAL HOP',
        city = 'San Francisco',
        state = 'CA',
        address = '1015 Folsom Street',
        phone = '123-123-1234',
        image_link = 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
        facebook_link = 'https://www.facebook.com/TheMusicalHop',
        genres = ['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'],
        website_link = 'https://www.themusicalhop.com',
        looking_for_talent  = True,
        seeking_description = 'We are on the lookout for a local artist to play every two weeks. Please call us.'
    ),
    Venue(
        id = 2,
        name = 'THE ROCK AND ROLL HALL OF FAME',
        city = 'Cleveland',
        state = 'OH',
        address = '1100 Rock and Roll Blvd',
        phone = '456-456-4567',
        image_link = 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
        facebook_link = 'https://www.facebook.com/TheRockAndRollHallOfFame',
        genres = ['Rock', 'Metal', 'Punk'],
        website_link = 'https://www.rockhall.com',
        looking_for_talent  = False,
        seeking_description = ''
    ),
    Venue(
    id = 3,
    name = 'THE JAZZ LOUNGE',
    city = 'New York',
    state = 'NY',
    address = '123 Broadway',
    phone = '789-789-7890',
    image_link = 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
    facebook_link = 'https://www.facebook.com/TheJazzLounge',
    genres = ['Jazz', 'Blues'],
    website_link = 'https://www.thejazzlounge.com',
    looking_for_talent  = True,
    seeking_description = 'We are looking for talented jazz musicians to perform on weekends. Contact us for more details.'
    ),
    Venue(
        id = 4,
        name = 'THE INDIE SPOT',
        city = 'Los Angeles',
        state = 'CA',
        address = '456 Hollywood Blvd',
        phone = '987-987-9876',
        image_link = 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
        facebook_link = 'https://www.facebook.com/TheIndieSpot',
        genres = ['Indie', 'Alternative', 'Rock'],
        website_link = 'https://www.theindiespot.com',
        looking_for_talent  = True,
        seeking_description = 'We are seeking talented indie bands for our upcoming events. Contact us if interested.'
    )
    # Add more Venue instances here
]


artists_data = [
    Artist(
        id = 4,
        name = 'GUNS N PETALS',
        city = 'San Francisco',
        state = 'CA',
        phone = '326-123-5000',
        genres = 'ROCK N ROLL',
        image_link = 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
        facebook_link = 'https://www.facebook.com/GunsNPetals',
        website_link = 'https://www.gunsnpetalsband.com',
        looking_for_venues = True,
        seeking_description = 'Looking for shows to perform at in the San Francisco Bay Area!',
    ),
    Artist(
        id = 5,
        name = 'MATT QUEVADO',
        city = 'New York',
        state = 'NY',
        phone = '300-400-5000',
        genres = 'JAZZ',
        image_link = 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
        facebook_link = 'https://www.facebook.com/mattquevedo923251523',
        website_link = '',
        looking_for_venues = False,
        seeking_description = ''
    ),
    Artist(
        id = 6,
        name = 'The Wild Sax Band',
        city = 'San Francisco',
        state = 'CA',
        phone = '432-325-5432',
        genres = ['Jazz', 'Classical'],
        image_link = 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
        facebook_link = '',
        website_link = '',
        looking_for_venues = False,
        seeking_description = ''
    )
]

shows_data = [
    Show(
        id = 1,
        venue_id = 1,
        artist_id = 4,
        start_time = '2019-05-21T21:30:00.000Z'
    ),
    Show(
        id = 2,
        venue_id = 3,
        artist_id = 5,
        start_time = '2019-06-15T23:00:00.000Z'
    ),
    Show(
        id = 3,
        venue_id = 3,
        artist_id = 6,
        start_time = '2035-04-01T20:00:00.000Z'
    )
]

for venue in venues_data:
    db.session.add(venue)

for artist in artists_data:
    db.session.add(artist)

for show in shows_data:
    db.session.add(show)


db.session.commit()
db.session.close()