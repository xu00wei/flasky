from flask import request, jsonify, render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        reponse = jsonify({'error':'not found'})
        reponse.status_code = 404
        return reponse
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def interior_server_mistake(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        reponse = jsonify({'error':'interior server mistake'})
        reponse.status_code = 500
        return reponse
    return render_template('500.html'), 500
