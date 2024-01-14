"""
API extension
"""
import app

from marshmallow import fields, Schema
from flask_smorest import Api, Blueprint


class ErrorSchema(Schema):
    """
    Custom error schema
    """

    status = fields.String(metadata={"description": "Error name"})
    message = fields.String(metadata={"description": "Error message"})
    errors = fields.Dict(metadata={"description": "Errors"})


class CustomApi(Api):
    """
    Custom API class for overriding errors
    """
    
    ERROR_SCHEMA = ErrorSchema

    def handle_http_exception(self, error):
        headers = {}
        payload = {"status": "fail"}

        data = getattr(error, "data", None)
        if data:
            if "message" in data:
                payload["message"] = data["message"]
            if "errors" in data:
                payload["errors"] = data["errors"]
            elif "messages" in data:
                payload["errors"] = data["messages"]
            if "headers" in data:
                headers = data["headers"]

        return payload, error.code, headers


class CustomBlueprint(Blueprint):
    """
    Custom Blueprint class for overriding response
    """
    
    DEFAULT_PAGINATION_PARAMETERS = {
        "page": 1, 
        "page_size": 5, 
        "max_page_size": 100
    }
    
    @staticmethod
    def _make_doc_response_schema(schema):
        if not schema:
            return None
        
        class ResponseSchema(Schema):
            status = fields.String(metadata={"description": "Response status"})
            data = fields.Nested(schema, metadata={"description": "Actual Data"})
        
        return ResponseSchema()
        
        
    
    @staticmethod
    def _prepare_response_content(data):
        if data is not None:
            return {
                "status": "success",
                "data": data
                }
        return None


api = CustomApi()


def init_app(app):
    """
    Initialize Api extension
    """
    api.init_app(app)
