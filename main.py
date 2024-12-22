from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for tasks
tasks = []

# Create a task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = {'id': len(tasks) + 1, 'title': data['title'], 'completed': False}
    tasks.append(task)
    return jsonify(task), 201

# Read all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Read a specific task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    return jsonify(task) if task else ('', 404)

# Update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['title'] = data.get('title', task['title'])
        task['completed'] = data.get('completed', task['completed'])
        return jsonify(task)
    return ('', 404)

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return ('', 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
