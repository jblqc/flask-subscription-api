from flask_restx import fields
from app.extensions import api
"""
    This file contains the structure of each Model for the API,
    basically its the serialized version, or formatted to JSON.

    """
frequency_option_model = api.model("FrequencyOption", {
    "id": fields.Integer,
    "frequency": fields.String,
    "duration_days": fields.Integer
})

frequency_option_input_model = api.model("FrequencyOptionInput", {
    "frequency": fields.String(required=True),
    "duration_days": fields.Integer(required=True)
})
