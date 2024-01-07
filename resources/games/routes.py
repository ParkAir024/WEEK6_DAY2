from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort
from uuid import uuid4

from models import GameModel
from schemas import GamesSchema, GamesSchemaNested
from . import bp

@bp.route('/<games_id>')
class Games(MethodView):

    @bp.response(200, GamesSchemaNested)
    def get(self, games_id):
        game = GameModel.query.get(games_id)
        if game:
            print(game.author)
            return game
        abort(400, message='Invalid Game')

    @jwt_required
    @bp.arguments(GamesSchema)
    def put(self, post_data, post_id):
        game = GamesSchema.query.get(post_id)
        if game and game.user_id == get_jwt_identity():
            game.body = post_data['body']
            game.commit()   
            return {'message': 'post updated'}, 201
        return {'message': "Invalid Post Id"}, 400    

    @bp.arguments(GamesSchema)
    def put(self, games_data ,post_id):
        post = GameModel.query.get(post_id)
        if post:
            post.body = games_data['body']
            post.commit()   
            return {'message': 'post updated'}, 201
        return {'message': "Invalid Post Id"}, 400
    
    @bp.response(201, GamesSchema)
    def post(self, games_data):
        user_id = games_data['user_id']
        if user_id in users:
            game_id = uuid4()
            games[game_id] = games_data
            return {'message': "Game Created", 'game_id': str(game_id)}, 201
        abort(401, message='Invalid User')

    @jwt_required
    @bp.arguments(GamesSchema)
    def put(self, games_data, game_id):
        game = GameModel.query.get(game_id)
        if game and post.user_id == get_jwt_identity():
            game.body = games_data['body']
            game.commit()   
            return {'message': 'post updated'}, 201
        return {'message': "Invalid Post Id"}, 400

    @jwt_required()
    def delete(self, game_id):
            game =GameModel.query.get(game_id)
            if game and post.user_id == get_jwt_identity():
                game.delete()
                return {"message": "Post Deleted"}, 202
            return {'message':"Invalid Post or User"}, 400

@bp.route('/')
class GamesList(MethodView):

    @bp.response(200, GamesSchema(many = True))
    def get(self):
        return GameModel.query.all()
  
    @jwt_required()
    @bp.arguments(GamesSchema)
    def game(self, games_data):
        try:
            game = GameModel()
            game.user_id = get_jwt_identity() 
            game.body = games_data['body']
            game.commit()
            return { 'message': "Post Created" }, 201
        except:
            return { 'message': "Invalid User"}, 401
