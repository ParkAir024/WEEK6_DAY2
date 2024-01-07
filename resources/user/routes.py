from flask import request

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import abort
from . import bp
from db import users

from schemas import UserSchema, UserSchemaNested
from models.users_model import UsersModel
# user routes

@bp.route('/user/<user_id>')
class User(MethodView):

  @bp.response(200, UserSchemaNested)
  def get(self,user_id):
    user = UsersModel.query.get(user_id)
    if user:
      print(user.games.all())
      return user
    else:
      abort(400, message='User not found')
    
  @bp.arguments(UserSchema)
  def put(self, user_data, user_id):
    user = UsersModel.query.get(user_id)
    if user:
      user.from_dict(user_data)
      user.commit()
      return { 'message': f'{user.username} updated'}, 202
    abort(400, message = "Invalid User")

  def delete(self, user_id):
    user = UsersModel.query.get(user_id)
    if user:
      user.delete()
      return { 'message': f'User: {user.username} Deleted' }, 202
    return {'message': "Invalid username"}, 400

@bp.route('/user')
class UserList(MethodView):

  @bp.response(200, UserSchema(many = True))
  def get(self):
   return UsersModel.query.all()
  
  @bp.arguments(UserSchema)
  def post(self, user_data):
    try: 
      user = UsersModel()
      user.from_dict(user_data)
      user.commit()
      return { 'message' : f'{user_data["username"]} created' }, 201
    except:
      abort(400, message='Username and Email Already taken')
    
@bp.route('/user/follow/<followed_id>')
class FollowUser(MethodView):

  @jwt_required()
  def post(self, followed_id):
    followed = UsersModel.query.get(followed_id)
    follower =UsersModel.query.get(get_jwt_identity())
    if follower and followed:
      follower.follow(followed)
      followed.commit()
      return {'message':'user followed'}
    else:
      return {'message':'invalid user'}, 400
  @jwt_required()  
  def put(self, followed_id):
    followed = UsersModel.query.get(followed_id)
    follower = UsersModel.query.get(get_jwt_identity())
    if follower and followed:
      follower.unfollow(followed)
      followed.commit()
      return {'message':'user unfollowed'}
    else:
      return {'message':'invalid user'}, 400