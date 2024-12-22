from flask import Flask, jsonify, request
from models import Task, get_db, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime

app = Flask(__name__)

# Create a task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    db = SessionLocal()
    try:
        task = Task(
            title=data['title'],
            description=data.get('description'),
            completed=data.get('completed', False)
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        }), 201
    finally:
        db.close()

# Read all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    db = SessionLocal()
    try:
        tasks = db.query(Task).all()
        return jsonify([{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        } for task in tasks])
    finally:
        db.close()

# Read a specific task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            return '', 404
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        })
    finally:
        db.close()

# Update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            return '', 404
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            task.completed = data['completed']
        
        task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(task)
        
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        })
    finally:
        db.close()

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            return '', 404
        db.delete(task)
        db.commit()
        return '', 204
    finally:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
