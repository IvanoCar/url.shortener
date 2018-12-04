from flask import Blueprint, redirect, request
from app import mongo
import json

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def hi():
    return json.dumps({'message': 'Welcome to the URL shortener API'})


@api.route('/add/new', methods=['POST'])
def add():
    try:
        urls = mongo.db.urls
        res = urls.find_one({'_id': request.form['id']})
        if res is not None:
            return json.dumps({'message': 'ID exists!'})

        n = {
            '_id': request.form['id'],
            'url': request.form['url'],
            'count': 0,
        }
        urls.insert(n)
        return json.dumps({'message': 'Success!', 'link': '/' + request.form['id']})
    except KeyError:
        return json.dumps({'message': 'Invalid data sent.'})


@api.route('/<id>')
def redirect_url(id):
    urls = mongo.db.urls
    res = urls.find_one({'_id': id})
    if res is None:
        return json.dumps({'message': 'No ID found.'})
    urls.update_one({"_id": id}, {"$set": {"count": res['count'] + 1}})
    return redirect(res['url'])


@api.route('/info/<id>')
def get_stats(id):
    urls = mongo.db.urls
    res = urls.find_one({'_id': id})
    if res is None:
        return json.dumps({'message': 'No ID found.'})
    return json.dumps({'short-id': id, 'url': res['url'], 'count': res['count']})

