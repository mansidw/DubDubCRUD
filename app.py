from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.app_context().push()
ma = Marshmallow(app)
api = Api(app)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return '<Notes %s>' % self.title


class NotesSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "completed")


notes_schema = NotesSchema()
notes_S_schema = NotesSchema(many=True)


class AllNotesResource(Resource):
    def get(self):
        notes = Notes.query.all()
        return notes_S_schema.dump(notes)

    def post(self):
        new_note = Notes(
            title=request.json['title'],
            completed=False
        )
        db.session.add(new_note)
        db.session.commit()
        return notes_schema.dump(new_note)


class SingularNotesResource(Resource):
    def get(self, notes_id):
        note = Notes.query.get_or_404(notes_id)
        return notes_schema.dump(note)

    def patch(self, notes_id):
        note = Notes.query.get_or_404(notes_id)

        if 'title' in request.json:
            note.title = request.json['title']

        db.session.commit()
        return notes_schema.dump(note)

    def delete(self, notes_id):
        note = Notes.query.get_or_404(notes_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204


api.add_resource(AllNotesResource, '/notes')
api.add_resource(SingularNotesResource, '/notes/<int:note_id>')


if __name__ == '__main__':
    app.run(debug=True)