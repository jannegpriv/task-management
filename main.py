from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Task, TaskStatus, Settings, SessionLocal
from datetime import datetime
from sqlalchemy import desc, asc

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5173",
            "http://localhost:3000"
        ]
    }
})

def apply_sorting(query, sort_by=None, sort_order='asc'):
    """Apply sorting to the query based on parameters."""
    if sort_by is None:
        return query

    valid_fields = {
        'status': Task.status,
        'created_at': Task.created_at,
        'updated_at': Task.updated_at,
        'title': Task.title
    }
    
    if sort_by not in valid_fields:
        return query
    
    sort_column = valid_fields[sort_by]
    
    if sort_order.lower() == 'desc':
        return query.order_by(desc(sort_column))
    return query.order_by(asc(sort_column))

# Settings endpoints
@app.route('/settings', methods=['GET'])
def get_settings():
    db = SessionLocal()
    try:
        settings = db.query(Settings).first()
        if not settings:
            settings = Settings(dark_mode=False)
            db.add(settings)
            db.commit()
            db.refresh(settings)
        return jsonify({
            'dark_mode': settings.dark_mode,
            'updated_at': settings.updated_at.isoformat()
        })
    finally:
        db.close()

@app.route('/settings', methods=['PUT'])
def update_settings():
    data = request.get_json()
    db = SessionLocal()
    try:
        settings = db.query(Settings).first()
        if not settings:
            settings = Settings()
            db.add(settings)
        
        settings.dark_mode = data.get('dark_mode', False)
        db.commit()
        db.refresh(settings)
        
        return jsonify({
            'dark_mode': settings.dark_mode,
            'updated_at': settings.updated_at.isoformat()
        })
    finally:
        db.close()

# Create a task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    db = SessionLocal()
    try:
        task = Task(
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', TaskStatus.TODO)
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        }), 201
    finally:
        db.close()

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    db = SessionLocal()
    try:
        # Get sorting parameters from query string
        sort_by = request.args.get('sort_by')
        sort_order = request.args.get('sort_order', 'asc')
        
        # Build query
        query = db.query(Task)
        
        # Apply sorting
        query = apply_sorting(query, sort_by, sort_order)
        
        # Execute query
        tasks = query.all()
        
        return jsonify([{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        } for task in tasks])
    finally:
        db.close()

# Get a single task
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == id).first()
        if task is None:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        })
    finally:
        db.close()

# Update a task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == id).first()
        if task is None:
            return jsonify({'error': 'Task not found'}), 404

        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        
        task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(task)

        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        })
    finally:
        db.close()

# Delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == id).first()
        if task is None:
            return jsonify({'error': 'Task not found'}), 404
        db.delete(task)
        db.commit()
        return '', 204
    finally:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
