from flask import Flask,request
from flask_restful import Api, Resource, reqparse
from models import db, NovelaModel
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
api = Api(app)
db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()


@app.route('/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

 
class NovelasView(Resource):
 
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help = "Can't leave blank"
    )
    parser.add_argument('author',
        type=str,
        required=True,
        help = "Can't leave blank"
    )'''
    def get(self):
        novelas = NovelaModel.query.all()
        return {'Novelas':list(x.json() for x in novelas)}
 
    def post(self):
        data = request.get_json()
        #data = NovelasView.parser.parse_args()
 
        new_novela = NovelaModel(data['name'], data['author'])
        db.session.add(new_novela)
        db.session.commit()
        return new_novela.json(),201
 

class NovelaView(Resource):
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('author',
        type=str,
        required=True,
        help = "Can't leave blank"
        )'''
 
    def get(self,name):
        novela = NovelaModel.query.filter_by(name=name).first()
        if novela:
            return novela.json()
        return {'message':'novela no encontrada'},404
 
    def put(self,name):
        data = request.get_json()
        #data = NovelaView.parser.parse_args()
 
        novela = NovelaModel.query.filter_by(name=name).first()
 
        if novela:
            novela.author = data["author"]
        else:
            novela = NovelaModel(name=name,**data)
 
        db.session.add(novela)
        db.session.commit()
 
        return novela.json()
 
    def delete(self,name):
        novela = NovelaModel.query.filter_by(name=name).first()
        if novela:
            db.session.delete(book)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message': 'novela no encontrada'},404
 
api.add_resource(NovelasView, '/novelas')
api.add_resource(NovelaView,'/novela/<string:name>')


 
app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=5000)