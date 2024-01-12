from flask import Blueprint, request, jsonify
from controllers.metrics import generate_pdf, get_metrics

metrics = Blueprint('metrics', __name__)

def options_response(func):
    """
    This decorator function checks if the request method is 'OPTIONS'.
    If it is, it returns a response with status 200 and appropriate headers.
    If it's not, it simply calls the decorated function.
    """
    def decorator(*args, **kwargs):
        if request.method == 'OPTIONS':
            return '', 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type'}
        return func(*args, **kwargs)
    decorator.__name__ = func.__name__
    return decorator


@metrics.route('/generate-pdf', methods=['POST', 'OPTIONS'])
@options_response
def generate_pdf_route():
    """
    This route receives a POST request with a JSON body containing the number of paragraphs to be generated.
    It returns a PDF file with the generated paragraphs.
    """
    data = request.get_json()
    paragraphs_qty = data.get('paragraphsQty')
    
    try:
        paragraphs_qty = int(paragraphs_qty)
    except ValueError:
        return jsonify({'message': 'paragraphs quantity must be an integer'}), 400
    
    return generate_pdf(paragraphs_qty)


@metrics.route('/metrics', methods=['GET', 'OPTIONS'])
@options_response
def get_metrics_route():
    """
    This route returns a JSON with TOP five most frequent words.
    """
    try:
        response = get_metrics()
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    return response