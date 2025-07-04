from flask import request 
from werkzeug.exceptions import NotFound
from flask_restx import Resource, Namespace, abort
from app.models.frequency_option import FrequencyOption
from app.extensions import db
from app.api_models.frequency_models import frequency_option_model, frequency_option_input_model

freq = Namespace("Frequency", path="/api", description="Subscription frequencies")

@freq.route("/frequencies")
class FrequencyListAPI(Resource):
    #marshal_list_with is used to convert the list of courses to the Course model
    #mauunang kunin yung return results, tsaka pupunta sa marshal
    @freq.marshal_list_with(frequency_option_model)
    def get(self):
        return FrequencyOption.query.all()
    
    @freq.expect(frequency_option_input_model)
    @freq.marshal_with(frequency_option_model)
    def post(self):
        data = request.json
        frequency_option =FrequencyOption(
            frequency=data["frequency"],
            duration_days=data["duration_days"])
        db.session.add(frequency_option)
        db.session.commit()
        return frequency_option, 201
        
        
@freq.route("/frequencies/<int:id>")
class FrequencyAPI(Resource):
    @freq.marshal_with(frequency_option_model)
    def get(self, id):
        option = FrequencyOption.query.get(id)
        if not option:
            abort(404, message=f"Frequency option with ID {id} not found")
        return option

    @freq.expect(frequency_option_input_model)
    @freq.marshal_with(frequency_option_model)
    def put(self, id):
        option = FrequencyOption.query.get(id)
        if not option:
            abort(404, message=f"Frequency option with ID {id} not found")
        data = request.json
        option.frequency = data["frequency"]
        option.duration_days = data["duration_days"]
        db.session.commit()
        return option

    def delete(self, id):
        option = FrequencyOption.query.get(id)
        if not option:
            abort(404, message=f"Frequency option with ID {id} not found")
        db.session.delete(option)
        db.session.commit()
        return {}, 204