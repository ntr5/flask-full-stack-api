from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)



class Journal_entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(144), unique=False)

    
    def __init__(self, title, content):
        self.title = title
        self.content = content


class Journal_entrySchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content')


journal_entry_schema = Journal_entrySchema()
journal_entries_schema = Journal_entrySchema(many=True)

# Endpoint to create a new journal_entry
@app.route('/journal_entry', methods=["POST"])
def add_journal_entry():
    title = request.json['title']
    content = request.json['content']
    new_journal_entry = Journal_entry(title, content)

    db.session.add(new_journal_entry)
    db.session.commit()

    journal_entry = Journal_entry.query.get(new_journal_entry.id)

    return journal_entry_schema.jsonify(journal_entry)


# Endpoint to query all journal_entries
@app.route("/journal_entries", methods=["GET"])
def get_journal_entries():
    all_journal_entries = Journal_entry.query.all()
    result = journal_entries_schema.dump(all_journal_entries)
    return jsonify(result)


# Endpoint for querying a single journal_entry
@app.route("/journal_entry/<id>", methods=["GET"])
def get_journal_entry(id):
    journal_entry = Journal_entry.query.get(id)
    return journal_entry_schema.jsonify(journal_entry)


# Endpoint for deleting a record
@app.route("/journal_entry/<id>", methods=["DELETE"])
def journal_entry_delete(id):
    journal_entry = Journal_entry.query.get(id)
    db.session.delete(journal_entry)
    db.session.commit()

    return "Journal_entry was successfully deleted"


@app.route("/", methods=["GET"])
def home():
    return "<div>Hey there...</div>"


if __name__ == '__main__':
    app.run(debug=True)