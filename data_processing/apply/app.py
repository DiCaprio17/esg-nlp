# encoding:utf-8
from flask import Flask, abort, request, jsonify
from urllib import parse
import predict

# Flask初始化参数
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})
#
#
# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# def get_task(task_id):
#     return jsonify({'task': tasks[task_id]})


@app.route('/apply', methods=['POST'])
def apply():
    if request.method != "POST":
        abort(400)
    print(parse.unquote(request.data.decode()))
    result = parse.unquote(request.data.decode())
    part = result.split('&')
    title = part[0].split('=')[1]
    content = part[1].split('=')[1]
    data = predict.apply(title, content)
    if data['message'] == 'not_esg':
        return jsonify({
            'is_esg': data['is_esg'],
            'message': data['message']
        })
    data_json = {
        'is_esg': data['is_esg'],
        'esg': data['esg'],
        'label': data['label'],
        'message': data['message']
    }
    return jsonify(data_json)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


if __name__ == '__main__':
    app.run(debug=True)
