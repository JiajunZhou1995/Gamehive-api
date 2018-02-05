from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, json, jsonify, Response, abort, redirect, url_for
import json

# define app & config
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/gamehive'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gamehive:gamehive@postgres:5432/gamehive'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define items
class Items(db.Model):
    item_id = db.Column(db.String(80), primary_key=True)
    item_name = db.Column(db.String(80), unique=False)
    skill_point = db.Column(db.Integer, unique=False)
    player_id = db.Column(db.String(80), unique=False)

    def __init__(self,item_id,item_name,skill_point,player_id='NULL'):
        self.item_id = item_id
        self.item_name = item_name
        self.skill_point = skill_point
        self.player_id = player_id
        
    def __repr__(self):
        return json.dumps({
                    "item_id": self.item_id,
                    "item_name": self.item_name,
                    "skill_point": self.skill_point,
                    "player_id": self.player_id
                })

# Define Players
class Players(db.Model):
    player_id = db.Column(db.String(80), primary_key=True)
    nickname = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    guild_id = db.Column(db.String(80), unique=False)

    def __init__(self,player_id,nickname,email,guild_id='NULL'):
        self.player_id = player_id
        self.nickname = nickname
        self.email = email
        self.guild_id = guild_id

    def __repr__(self):
        return json.dumps({
                    "player_id": self.player_id,
                    "nickname": self.nickname,
                    "email": self.email,
                    "guild_id": self.guild_id
                })
        
# Define Guilds
class Guilds(db.Model):
    guild_id = db.Column(db.String(80), primary_key=True)
    guild_name = db.Column(db.String(80), unique=True)
    country_code = db.Column(db.String(80), unique=True)

    def __init__(self,guild_id,guild_name,country_code='NULL'):
        self.guild_id = guild_id
        self.guild_name = guild_name
        self.country_code = country_code
        
    def __repr__(self):
        return json.dumps({
                    "guild_id": self.guild_id,
                    "guild_name": self.guild_name,
                    "country_code": self.country_code
                })


@app.route('/')
def root():
    return 'Game Hive Player API'

# Get a player
@app.route('/player/<int:player_id>', methods=['GET'])
def getplayer(player_id):
    player_id = str(player_id)
    player = Players.query.get(player_id)
    if player is None:
        status_code = 400
        result = json.dumps({'error':'player doesn\'t exist'})
    else:
        status_code = 200
        result = repr(player)

    resp = Response(result, status=status_code, mimetype='application/json')

    return resp

# Create a player
@app.route('/player', methods=['POST'])
def createplayer():
    player_id = request.json['player_id']
    nickname = request.json['nickname']
    email = request.json['email']
    try:
        guild_id = request.json['guild_id']
    except:
        guild_id = "NULL"

    if not db.session.query(db.exists().where(Guilds.guild_id == guild_id)).scalar():
        result={'error':'guild doesn\'t exist'}
        status_code=400
        js = json.dumps(result)
        resp = Response(js, status=status_code, mimetype='application/json')
        return resp

    try:
        db.session.add(Players(player_id,nickname,email,guild_id))
        db.session.commit()
        result={'message': 'player added'}
        status_code=200
    except:
        result={'error':'player exists'}
        status_code=400
    
    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

# Update a player
@app.route('/player', methods=['PUT'])
def updateplayer():
    player_id = request.json['player_id']
    nickname = request.json['nickname']
    email = request.json['email']
    guild_id = request.json['guild_id']

    if not db.session.query(db.exists().where(Guilds.guild_id == guild_id)).scalar():
        result={'error':'guild doesn\'t exist'}
        status_code=400
        js = json.dumps(result)
        resp = Response(js, status=status_code, mimetype='application/json')
        return resp

    try:
        player = Players.query.get(player_id)
        player.nickname = nickname
        player.email = email
        player.guild_id = guild_id
        db.session.commit()
        result={'message': 'player updated'}
        status_code=200
    except:
        result={'error':'player doesn\'t exists'}
        status_code=400
    
    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

# Delete a player
@app.route('/player/<int:player_id>', methods=['DElETE'])
def deleteplayer(player_id):
    player_id = str(player_id)
    player = Players.query.get(player_id)

    if player is None:
        status_code = 400
        result = {'error':'player doesn\'t exist'}
    else:
        db.session.delete(player)
        db.session.commit()
        status_code = 200
        result = {'message': 'player deleted'}
    
    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

# Get a guild
@app.route('/guild/<int:guild_id>', methods=['GET'])
def getguild(guild_id):
    guild_id = str(guild_id)
    guild = Guilds.query.get(guild_id)
    if guild is None:
        status_code = 401
        result=json.dumps({'error':'guild doesn\'t exist'})
    else:
        status_code = 200
        result = repr(guild)

    resp = Response(result, status=status_code, mimetype='application/json')

    return resp

# Create a guild
@app.route('/guild', methods=['POST'])
def createguild():
    guild_id = request.json['guild_id']
    guild_name = request.json['guild_name']
    country_code = request.json['country_code']
    player1_id = request.json['player1_id']
    player2_id = request.json['player2_id']
    
    try:
        player1 = Players.query.filter_by(player_id=player1_id).first()
        player1.guild_id = guild_name
        player2 = Players.query.filter_by(player_id=player2_id).first()
        player2.guild_id = guild_name
    except:
        result={'error':'player doesn\'t exists'}
        status_code=400    
        js = json.dumps(result)
        resp = Response(js, status=status_code, mimetype='application/json')
        return resp

    try:
        db.session.add(Guilds(guild_id,guild_name,country_code))
        db.session.commit()
        result={'message': 'guild added'}
        status_code=200
    except:
        result={'error':'guild exists'}
        status_code=400
    
    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

# Update a guild
@app.route('/guild', methods=['PUT'])
def updateguild():
    guild_id = request.json['guild_id']
    guild_name = request.json['guild_name']
    country_code = request.json['country_code']

    try:
        guild = Guilds.query.get(guild_id)
        guild.guild_name = guild_name
        guild.country_code = country_code
        db.session.commit()
        result={'message': 'guild updated'}
        status_code=200
    except:
        result={'error':'guild doesn\'t exist'}
        status_code=400
    
    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

# Delete a guild
@app.route('/guild/<int:guild_id>', methods=['DElETE'])
def deleteguild(guild_id):
    guild_id = str(guild_id)
    guild = Guilds.query.get(guild_id)

    if guild is None:
        result={'error':'guild doesn\'t exist'}
        status_code=400
    else:
        db.session.delete(guild)
        db.session.commit()
        result={'message': 'guild deleted'}
        status_code=200

    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

# Get a item
@app.route('/item/<int:item_id>', methods=['GET'])
def getitem(item_id):
    item_id = str(item_id)
    item = Items.query.get(item_id)
    if item is None:
        status_code = 400
        result=json.dumps({'error':'item doesn\'t exist'})
    else:
        status_code = 200
        result = repr(item)

    resp = Response(result, status=status_code, mimetype='application/json')

    return resp

# Create a item
@app.route('/item', methods=['POST'])
def createitem():
    item_id = request.json['item_id']
    item_name = request.json['item_name']
    skill_point = request.json['skill_point']
    try:
        player_id = request.json['player_id']
    except:
        player_id = "NULL"

    if not db.session.query(db.exists().where(Players.player_id == player_id)).scalar():
        result={'error':'player doesn\'t exist'}
        status_code=400
        js = json.dumps(result)
        resp = Response(js, status=status_code, mimetype='application/json')
        return resp

    try:
        db.session.add(Items(item_id,item_name,skill_point,player_id))
        db.session.commit()
        result={'message': 'item added'}
        status_code=200
    except:
        result={'error':'item exists'}
        status_code=400
    
    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

# Update a item
@app.route('/item', methods=['PUT'])
def updateitem():
    item_id = request.json['item_id']
    item_name = request.json['item_name']
    skill_point = request.json['skill_point']
    player_id = request.json['player_id']

    if not db.session.query(db.exists().where(Players.player_id == player_id)).scalar():
        result={'error':'player doesn\'t exist'}
        status_code=400
        js = json.dumps(result)
        resp = Response(js, status=status_code, mimetype='application/json')
        return resp

    try:
        item = Items.query.get(item_id)
        item.item_name = item_name
        item.skill_point = skill_point
        item.player_id = player_id
        db.session.commit()
        result={'message': 'item updated'}
        status_code=200
    except:
        result={'error':'item doesn\'t exists'}
        status_code=400
    
    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

# Delete a item
@app.route('/item/<int:item_id>', methods=['DElETE'])
def deleteitem(item_id):
    item_id = str(item_id)
    item = Items.query.get(item_id)

    if item is None:
        result={'error':'item doesn\'t exist'}
        status_code=400
    else:
        db.session.delete(item)
        db.session.commit()
        result={'message': 'item deleted'}
        status_code=200

    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp


# add a player to a guild
@app.route('/addToGuild', methods=['PUT'])
def addToGuild():
    player_id = request.json['player_id']
    guild_id = request.json['guild_id']

    try:
        player = Players.query.filter_by(player_id=player_id).first()
        player.guild_id = guild_id
        db.session.commit()
        message = 'player ' + player_id + ' joined guild ' + guild_id
        result={'message': message}
        status_code=200
    except:
        result={'error':'player or guild doesn\'t exists'}
        status_code=400
    
    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

# remove a player from a guild
@app.route('/removeFromGuild', methods=['PUT'])
def removeFromGuild():
    player_id = request.json['player_id']
    guild_id = request.json['guild_id']

    if not db.session.query(db.exists().where(Guilds.guild_id == guild_id)).scalar():
        result={'error':'guild doesn\'t exist'}
        status_code=400
        js = json.dumps(result)
        resp = Response(js, status=status_code, mimetype='application/json')
        return resp

    try:
        player = Players.query.filter_by(player_id=player_id).first()
        player.guild_id = "NULL"
        db.session.commit()
        message = 'player ' + player_id + ' left guild ' + guild_id
        result={'message': message}
        status_code=200
    except:
        result={'error':'player doesn\'t exist'}
        status_code=400
    
    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

# add an item to a player
@app.route('/playerAddItem', methods=['PUT'])
def playerAddItem():
    player_id = request.json['player_id']
    item_id = request.json['item_id']

    if not db.session.query(db.exists().where(Players.player_id == player_id)).scalar():
        result={'error':'player doesn\'t exist'}
        status_code=400
        js = json.dumps(result)
        resp = Response(js, status=status_code, mimetype='application/json')
        return resp

    try:
        item = Items.query.filter_by(item_id=item_id).first()
        item.player_id = player_id
        db.session.commit()
        message = 'item ' + item_id + ' add to player ' + player_id
        result={'message': message}
        status_code=200
    except:
        result={'error':'item doesn\'t exist'}
        status_code=400
    
    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

# calculate the total number of skill points in a guild
@app.route('/calculateGuildPoints/<int:guild_id>', methods=['GET'])
def calculateGuildPoints(guild_id):
    guild_id = str(guild_id)
    sum = 0

    if not db.session.query(db.exists().where(Guilds.guild_id == guild_id)).scalar():
        result={'error':'guild doesn\'t exist'}
        status_code=400
        js = json.dumps(result)
        resp = Response(js, status=status_code, mimetype='application/json')
        return resp

    cmd = 'select distinct items.item_name,\
                           items.skill_point,\
                           players.guild_id\
           from items\
           inner join players\
           on items.player_id = players.player_id\
           inner join guilds\
           on players.guild_id = guilds.guild_id\
           where players.guild_id = %s' 

    try:
        r = db.engine.execute(cmd, guild_id)      
        for i in r:
            sum = sum + int(i.skill_point)
        result={'message': str(sum)}
        status_code=200
    except:
        result={'error':'query failed'}
        status_code=400
    
    js = json.dumps(result)
    resp = Response(js, status=status_code, mimetype='application/json')

    return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
