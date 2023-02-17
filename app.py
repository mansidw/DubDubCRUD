from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
# declaring and connecting the test.db file to our flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.app_context().push()

# wrapping up our flask application with Marshmallow that helps in object serialization and Api for creating REST services
ma = Marshmallow(app)
api = Api(app)

"""Creating the notes model
id : unique primary key for the table
title : content of the task to be added/deleted/updated
completed : a boolean variable that marks if the task is complete or not
"""
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return '<Notes %s>' % self.title

"""Creating the notes model schema for it's necessary because we want to parse our post object(s) into a JSON response."""
class NotesSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "completed")

"""Here I have defined two objects because one would return one object in response but the GET ALL endpoint might return more than one documents hence the argument many has been set to true"""
notes_schema = NotesSchema()
notes_schema_all = NotesSchema(many=True)


"""This first class is used for getting all the tasks and posting/creating a new task. The endpoint only consists of /notes with just different HTTP methods"""
class AllNotesResource(Resource):
    def get(self):
        notes = Notes.query.all()
        return notes_schema_all.dump(notes) if len(notes)>0 else {"message":"No entries yet!"}

    def post(self):
        try:
            new_note = Notes(
                title=request.json['title'],
                completed=False
            )
        except:
            return({"message":"The request does not contain the required field of title!"})
        # adding the received json object into the database as a row
        db.session.add(new_note)
        db.session.commit()
        return notes_schema.dump(new_note)
        


"""This second class is used for getting a specified task and updating and deleting it. The endpoint only consists of /notes/:id with just different HTTP methods"""
class SingularNotesResource(Resource):
    def get(self, notes_id):
        try:
            note = Notes.query.get_or_404(notes_id)
            return notes_schema.dump(note)
        except:
            return{"message":"Task with the given ID does not exist!"}

    def patch(self, notes_id):
        try:
            note = Notes.query.get_or_404(notes_id)
        except:
            return{"message":"Task with the given ID does not exist!"}

        try:
            if 'title' in request.json:
                note.title = request.json['title']
            else:
                # Instead of creating a separate request we can change the complete status in the patch request itself just with one more parameter
                if 'completed' in request.json:
                    note.completed = request.json["completed"]
                else:
                    return {"message":"The field does not match the schema design!"}
        except:
            return {"message":"The field does not match the schema design!"}
        db.session.commit()
        return notes_schema.dump(note)

    def delete(self, notes_id):
        try:
            note = Notes.query.get_or_404(notes_id)
        except:
            return{"message":"Task with the given ID does not exist!"}
        db.session.delete(note)
        db.session.commit()
        return ({"message":"Deleted the task!"}, 200)



# defining the endpoints for the apis
api.add_resource(AllNotesResource, '/notes')
api.add_resource(SingularNotesResource, '/notes/<int:notes_id>')


if __name__ == '__main__':
    app.run(debug=True)