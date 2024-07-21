from app import db 
from app import Venue
from app import Artist
from app import Show

venues_data = [
    Venue(
        id = 1,
        name = '国际体育中心体育场',
        city = '南昌',
        state = '江西',
        address = '红谷滩新区国体大道333号',
        phone = '0791-88916759',
        image_link = '场地图片',
        facebook_link = '脸书连接',
        genres = ['风格流派'],
        website_link = '场所网址',
        looking_for_talent  = True,
        seeking_description = '哈哈哈哈哈哈哈'
    ),
    Venue(
        id = 2,
        name = '国际体育中心体育场',
        city = '南昌',
        state = '江西',
        address = '红谷滩新区国体大道333号',
        phone = '0791-88916759',
        image_link = '场地图片',
        facebook_link = '脸书连接',
        genres = ['风格流派'],
        website_link = '场所网址',
        looking_for_talent  = True,
        seeking_description = '哈哈哈哈哈哈哈'
    ),
    Venue(
        id = 3,
        name = '国际体育中心体育场',
        city = '南昌',
        state = '江西',
        address = '红谷滩新区国体大道333号',
        phone = '0791-88916759',
        image_link = '场地图片',
        facebook_link = '脸书连接',
        genres = ['风格流派'],
        website_link = '场所网址',
        looking_for_talent  = True,
        seeking_description = '哈哈哈哈哈哈哈'
    )
    # Add more Venue instances here
]


artists_data = [
    Artist(
        id = 1,
        name = '周杰伦',
        city = '南昌',
        state = '江西',
        phone = '15179105101',
        genres = '风格流派',
        image_link = '图片网址',
        facebook_link = '脸书网址',
        website_link = '网站网址',
        looking_for_venues = True,
        seeking_description = '简介'
    ),
    Artist(
        id = 2,
        name = '周杰伦',
        city = '南昌',
        state = '江西',
        phone = '15179105101',
        genres = '风格流派',
        image_link = '图片网址',
        facebook_link = '脸书网址',
        website_link = '网站网址',
        looking_for_venues = True,
        seeking_description = '简介'
    ),
    Artist(
        id = 3,
        name = '周杰伦',
        city = '南昌',
        state = '江西',
        phone = '15179105101',
        genres = '风格流派',
        image_link = '图片网址',
        facebook_link = '脸书网址',
        website_link = '网站网址',
        looking_for_venues = True,
        seeking_description = '简介'
    )
]

shows_data = [
    Show(
        id = 1,
        venue_id = 1,
        artist_id = 3,
        start_time = '2019-05-21T21:30:00.000Z'
    ),
    Show(
        id = 2,
        venue_id = 3,
        artist_id = 2,
        start_time = '2019-06-15T23:00:00.000Z'
    ),
    Show(
        id = 3,
        venue_id = 3,
        artist_id = 1,
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