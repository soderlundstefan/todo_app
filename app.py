from flask import Flask, render_template, request, jsonify
import db

app = Flask(__name__)
db.init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/todos", methods=["GET"])
def get_todos():
    todos = db.get_all_todos()
    return jsonify(todos)


@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "任务内容不能为空"}), 400

    todo = db.add_todo(title)
    return jsonify(todo), 201


@app.route("/api/todos/<int:todo_id>/toggle", methods=["PATCH"])
def toggle_todo(todo_id):
    todo = db.toggle_todo(todo_id)

    if todo is None:
        return jsonify({"error": "任务不存在"}), 404

    return jsonify(todo)


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    success = db.delete_todo(todo_id)

    if not success:
        return jsonify({"error": "任务不存在"}), 404

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)