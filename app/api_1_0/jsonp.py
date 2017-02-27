from . import api
from ..decorators import support_jsonp
from flask import jsonify
@api.route("/myinfo")
@support_jsonp
def get_my_info():
    return jsonify({
        "name": "xuwei",
        "age": 22,
        "school": "DGUT",
        "other": "testjsonp"
    })
