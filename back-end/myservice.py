from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory

app = Flask(__name__)

class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.present = False

# Liste d'étudiants (simulée, vous pouvez la remplacer par une base de données)
students = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    root_dir = '../front-end/dist'  # Chemin vers le répertoire de build de Vue.js
    return send_from_directory(root_dir, path)


@app.route('/students', methods=['GET'])
def get_students():
    return jsonify([{"id": student.id, "name": student.name, "present": student.present} for student in students])

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        student_id = len(students) + 1
        student = Student(student_id, name)
        students.append(student)
        print("Added student:", student.__dict__)  # Ajoutez cette ligne pour débogage
        return jsonify({"id": student_id, "name": name, "present": False})


@app.route('/mark_attendance/<int:student_id>/<status>', methods=['POST'])
def mark_attendance(student_id, status):
    if request.method == 'POST':
        present = (status == 'present')
        for student in students:
            if student.id == student_id:
                student.present = present
                return jsonify({"id": student.id, "name": student.name, "present": present})

@app.route('/update_student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    if request.method == 'PUT':
        data = request.get_json()
        new_name = data.get('name')
        for student in students:
            if student.id == student_id:
                student.name = new_name
                return jsonify({"id": student.id, "name": student.name, "present": student.present})

@app.route('/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    if request.method == 'DELETE':
        global students
        students = [student for student in students if student.id != student_id]
        return jsonify({"message": "Student deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
