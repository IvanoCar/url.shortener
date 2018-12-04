from flask import Blueprint, redirect, render_template, request
from app import mongo
import json

web = Blueprint('web', __name__)


@web.route('/')
def hi():
    return render_template('index.html')


@web.route('/add/new', methods=['POST'])
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
        msg = 'Link is added with ID: %s' % request.form['id']
        return render_template('index.html', msg=msg)

    except KeyError:
        return render_template('index.html')


@web.route('/<id>')
def redirect_url(id):
    urls = mongo.db.urls
    res = urls.find_one({'_id': id})
    if res is None:
        return render_template('index.html', msg='No ID found!')
    urls.update_one({"_id": id}, {"$set": {"count": res['count'] + 1}})
    return redirect(res['url'])


@web.route('/info/<id>')
def get_stats(id):
    urls = mongo.db.urls
    res = urls.find_one({'_id': id})
    if res is None:
        return render_template('info.html', msg='No ID found!', link=None)
    return render_template('info.html', link=res)
