#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from werkzeug.utils import url_quote
from flask_migrate import Migrate
import logging

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))



    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_for_talent  = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True)



class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    


    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(120))
    looking_for_venues = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True)



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
                           
  

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = Venue.query.all()
    data = []
    for venue in venues:
        data.append({
            "city": venue.city,
            "state": venue.state,
            "venues": [{
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": Show.query.filter(Show.venue_id == venue.id).count(),
            }] 
        })
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])

def search_venues():
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(venues),
        "data": []
    }
    for venue in venues:
        response["data"].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": Show.query.filter(Show.venue_id == venue.id).count(),
        })
    return render_template('pages/search_venues.html', results=response, search_term=search_term)
    
    
    



@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        flash('Venue not found')
        return redirect(url_for('index'))
    
    past_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
        filter(
            Show.venue_id == venue_id,
            Show.artist_id == Artist.id,
            Show.start_time < datetime.now()
        ).\
        all()
    
    upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
        filter(
            Show.venue_id == venue_id,
            Show.artist_id == Artist.id,
            Show.start_time > datetime.now()
        ).\
        all()
    
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.looking_for_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": [{
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        } for artist, show in past_shows],
        "upcoming_shows": [{
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        } for artist, show in upcoming_shows],
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }
    
    return render_template('pages/show_venue.html', venue=data)





#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    form = VenueForm(request.form)
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        website_link = request.form['website_link']
        looking_for_talent = True if 'looking_for_talent' in request.form else False
        seeking_description = request.form['seeking_description']
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        
        venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, website_link=website_link, looking_for_talent=looking_for_talent, seeking_description=seeking_description, image_link=image_link, facebook_link=facebook_link)
        
        db.session.add(venue)
        db.session.commit()
        
        flash('Venue ' + venue.name + ' was successfully listed!')
        return render_template('pages/home.html')
    
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        return render_template('forms/new_venue.html', form=form)
    finally:
        # 关闭数据库会话
        db.session.close()



@app.route('/delete_venue/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    venue = Venue.query.get(venue_id)
    if venue:
        try:
            db.session.delete(venue)
            db.session.commit()
            flash('Venue successfully deleted.')
        except:
            db.session.rollback()
            flash('An error occurred. Venue could not be deleted.')
    else:
        flash('Venue not found.')
    return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
  # TODO: replace with real data returned from querying the database
def artists():
    artists = Artist.query.all()
    data = []
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name,
        })
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
def search_artists():
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(artists),
        "data": []
    }
    for artist in artists:
        response["data"].append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": Show.query.filter(Show.artist_id == artist.id).count(),
        })
    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
   # 从数据库中查询艺术家
    artist = Artist.query.get(artist_id)
    if not artist:
        flash('Artist not found')
        return redirect(url_for('index'))

    # 查询过去的演出
    past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id, Show.start_time < datetime.now()).all()
    past_shows = []
    for show in past_shows_query:
        past_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    # 查询即将到来的演出
    upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id, Show.start_time > datetime.now()).all()
    upcoming_shows = []
    for show in upcoming_shows_query:
        upcoming_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    # 准备艺术家数据
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(','),  # 假设 genres 是以逗号分隔的字符串
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.looking_for_venues,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_artist.html', artist=data)

 

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # TODO: populate form with fields from artist with ID <artist_id>
    # 从数据库中查询艺术家
    artist = Artist.query.get(artist_id)
    if not artist:
        # 如果没有找到艺术家，重定向到艺术家列表页面或显示错误消息
        flash('Artist not found.')
        return redirect(url_for('index'))

    # 创建表单实例
    form = ArtistForm()

    # 使用艺术家信息填充表单字段
    form.name.data = artist.name
    form.genres.data = artist.genres  # 假设这是一个列表
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.website_link.data = artist.website_link
    form.facebook_link.data = artist.facebook_link
    form.looking_for_venues.data = artist.looking_for_venues
    form.seeking_description.data = artist.seeking_description
    form.image_link.data = artist.image_link

    # 将表单和艺术家信息传递给模板
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)  # 假设 Artist 是你的模型类名
    if artist:
        # 从表单获取数据并更新艺术家记录
        artist.name = form.name.data
        artist.genres = form.genres.data  # 确保这是以正确的格式存储（例如，列表或逗号分隔的字符串）
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.website_link = form.website_link.data
        artist.facebook_link = form.facebook_link.data
        artist.looking_for_venues = form.looking_for_venues.data
        artist.seeking_description = form.seeking_description.data
        artist.image_link = form.image_link.data
        
        # 提交更改到数据库
        db.session.commit()
        
        # 重定向到艺术家的显示页面
        return redirect(url_for('show_artist', artist_id=artist_id))
    else:
        # 如果没有找到艺术家，可能需要处理错误
        return "Artist not found", 404


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
      # TODO: populate form with values from venue with ID <venue_id>
    venue = Venue.query.get(venue_id)
    if venue:
        form = VenueForm(obj=venue)
        # 使用场馆信息填充表单
        venue.name = form.name.data 
        venue.genres = form.genres.data 
        venue.address = form.address.data 
        venue.city = form.city.data 
        venue.state = form.state.data 
        venue.phone = form.phone.data
        venue.website_link = form.website_link.data
        venue.facebook_link = form.facebook_link.data 
        venue.seeking_talent = form.seeking_talent.data 
        venue.seeking_description = form.seeking_description.data 
        venue.image_link = form.image_link.data 
        
        return render_template('forms/edit_venue.html', form=form, venue=venue)
    else:
        # 如果没有找到场馆，可能需要处理错误
        return "Venue not found", 404


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.get(venue_id)
    if venue:
        form = VenueForm(obj=venue)
        if form.validate_on_submit():
            # 从表单获取新的属性值并更新 venue 实例
            venue.name = form.name.data
            venue.genres = form.genres.data  # 注意：根据你的模型设计，你可能需要处理这个字段
            venue.address = form.address.data
            venue.city = form.city.data
            venue.state = form.state.data
            venue.phone = form.phone.data
            venue.website_link = form.website_link.data
            venue.facebook_link = form.facebook_link.data
            venue.looking_for_venues = form.looking_for_venues.data
            venue.seeking_description = form.seeking_description.data
            venue.image_link = form.image_link.data
            
            # 提交更改到数据库
            db.session.commit()
            flash('Venue ' + request.form['name'] + ' was successfully updated!')
            return redirect(url_for('show_venue', venue_id=venue_id))
        else:
            # 如果表单验证失败，可能需要处理错误
            flash('An error occurred. Venue could not be updated.')
            return redirect(url_for('edit_venue', venue_id=venue_id))
    else:
        flash('Venue not found.')
        return redirect(url_for('index'))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm(request.form)
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Artist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        website_link = request.form['website_link']
        looking_for_venues = True if 'looking_for_venues' in request.form else False
        seeking_description = request.form['seeking_description']
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        new_artist = Artist(name=name, city=city, state=state, address=address, phone=phone, genres=genres, website_link=website_link, looking_for_venues=looking_for_venues, seeking_description=seeking_description, image_link=image_link, facebook_link=facebook_link)
        
        db.session.add(new_artist)
        db.session.commit()
        # 成功插入数据库后，使用 flash 发送成功消息
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        # 如果发生错误，回滚数据库会话
        db.session.rollback()
        # 使用 flash 发送错误消息
        flash('An error occurred. Artist ' + name + ' could not be listed.')
    finally:
        # 关闭数据库会话
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
    # 查询所有的演出信息，包括关联的场馆信息
    shows = db.session.query(Show).join(Venue).all()

    # 准备传递给模板的数据
    data = []
    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time)
        })

    return render_template('pages/shows.html', shows=data)
  

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    # 从表单获取数据
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')

    try:
        # 创建一个新的 Show 记录
        new_show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        # 将新记录插入数据库
        db.session.add(new_show)
        db.session.commit()
        # 成功插入数据库后，使用 flash 发送成功消息
        flash('Show was successfully listed!')
    except Exception as e:
        # 如果发生错误，回滚数据库会话
        db.session.rollback()
        # 使用 flash 发送错误消息
        flash('An error occurred. Show could not be listed. Error: ' + str(e))
    finally:
        # 关闭数据库会话
        db.session.close()
    return render_template('pages/home.html')

  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
