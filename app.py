from flask import Flask, request, jsonify

app = Flask(__name__)
tasks = []  # Тимчасове сховище даних у пам'яті
current_id = 1

@app.route('/')
def home():
    return "Лаба №2: CRUD туда сюда"

# Create (POST)
@app.route('/tasks', methods=['POST'])
def create_task():
    global current_id
    data = request.json
    new_task = {
        "id": current_id,
        "title": data.get('title', ''),
        "status": "pending"
    }
    tasks.append(new_task)
    current_id += 1
    return jsonify(new_task), 201

# Read all (GET)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

# Read one (GET)
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

# Update (PUT)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task['title'] = data.get('title', task['title'])
    task['status'] = data.get('status', task['status'])
    return jsonify(task)

# Delete (DELETE)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({"message": "Task deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)