from flask import Flask,request,jsonify,Response,render_template
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash
from bson import json_util
from bson.objectid import ObjectId
import json

app = Flask(__name__,template_folder='vistas')

app.config["MONGO_URI"]='mongodb://localhost:27017/python-mongo'

mongo=PyMongo(app)

@app.route('/user',methods=['POST'])
def create_user():
    user=request.json['user_name']
    password=request.json['password']
    email=request.json['email']

    if user and password and email:
        passwordHashed=generate_password_hash(password)
        mongo.db.users.insert({
            'user_name':user,
            'password':passwordHashed,
            'email':email
        })
        response={'message':f'Se creo exitosamente el usuario {user}'}
        return response
    else:
        return not_fund()
        #return {'message':'Formulario incompleto'}

@app.route('/user',methods=['GET'])
def get_users():
    users=mongo.db.users.find()
    #response=json_util.dumps(users)
    #return Response(response,mimetype='application/json')
    data=[]
    for u in users:
        data.append(u)
        print({u['_id']},' ',{u['user_name'],' ',u['email']})
    return render_template('users.html',usersList=data)

@app.route('/user/<id>',methods=['GET'])
def find_user(id):
    user=mongo.db.users.find_one({'_id':ObjectId(id)})
    response=json_util.dumps(user)
    return Response(response,mimetype='application/json')

@app.route('/user/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id':ObjectId(id)})
    response=jsonify({
        'message':f'Usuario con ID {id} borrado exitosamente'
    })
    return response

@app.route('/user/<id>',methods=['PUT'])
def update_user(id):
    user=request.json['user_name']
    password=request.json['password']
    email=request.json['email']

    if user and password and email:
        passwordHashed=generate_password_hash(password)
        mongo.db.users.update_one({'_id':ObjectId(id)},{'$set':{
            'user_name':user,
            'password':passwordHashed,
            'email':email
        }})
        response=jsonify({'message':f'Se actualizo e lusuario id {id} correctamente'})
        return response

@app.errorhandler(404)
def not_fund(error=None):
    response=jsonify( {
        'message':f'Recurso no encontrado {request.url}',
        'status':404
    })
    response.status_code=404
    return response

if __name__ == '__main__':
    app.run(debug=True)