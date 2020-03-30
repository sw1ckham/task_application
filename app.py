import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://sw1ckham:1hamcvcw123@myfirstcluster-iff8d.mongodb.net/task_manager?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template('addtask.html', catergories=mongo.db.catergories.find())

@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_catergories = mongo.db.catergories.find()
    return render_template('edittask.html', task=the_task, catergories=all_catergories)


@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name': request.form.get('task_name'),
        'catergorie_name': request.form.get('catergorie_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent': request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))

@app.route('/get_catergories')
def get_catergories():
    return render_template('catergories.html', 
    catergories=mongo.db.catergories.find())


@app.route('/edit_catergorie/<catergorie_id>')
def edit_catergorie(catergorie_id):
    return render_template('editcatergorie.html', catergorie=mongo.db.catergories.find_one(
        {'_id': ObjectId(catergorie_id)}))


@app.route('/update_catergorie/<catergorie_id>', methods=['POST'])
def update_catergorie(catergorie_id):
    mongo.db.catergories.update(
       {'_id': ObjectId(catergorie_id)},
       {'catergorie_name': request.form.get('catergorie_name')})
    return redirect(url_for('get_catergories'))


@app.route('/delete_catergorie/<catergorie_id>')
def delete_catergorie(catergorie_id):
    mongo.db.catergories.remove({'_id': ObjectId(catergorie_id)})
    return redirect(url_for('get_catergories'))


@app.route('/insert_catergorie', methods=['POST'])
def insert_catergorie():
    catergories = mongo.db.catergories
    catergorie_doc = {'catergorie_name': request.form.get('catergorie_name')}
    catergories.insert_one(catergorie_doc)
    return redirect(url_for('get_catergories'))


@app.route('/add_catergorie')
def add_catergorie():
    return render_template('addcatergorie.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), 
                            debug=True)
