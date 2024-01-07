from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Str(dump_only = True)
    email = fields.Str(required = True)
    username = fields.Str(required = True)
    password = fields.Str(required = True, load_only = True )
    first_name = fields.Str()
    last_name = fields.Str()

class UserLogin(Schema):
  username = fields.Str(required = True)
  password = fields.Str(required = True, load_only = True )

class GamesSchema(Schema):
    id = fields.Str(dump_only = True)
    title = fields.Str(required=True)
    system = fields.Str(required=True)
    release_year = fields.Str(required=True)
    user_id = fields.Str(required=True)
    
class GamesSchemaNested(GamesSchema):
    user = fields.Nested(UserSchema, dumps_only = True)

class UserSchemaNested(UserSchema):
    games = fields.List(fields.Nested(GamesSchema), dump_only=True)
