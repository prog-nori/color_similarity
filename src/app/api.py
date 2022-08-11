from flask import Blueprint, make_response, jsonify
from src.util.utility import (
    CSV_FILE,
    csv_row_2_json_all,
    read_csv_as_nested_list
    )

api = Blueprint("api", __name__)

@api.route('/servicies/v2/blocks/<page>')
def get_blocks(page):
    page = int(page)
    limit = 50
    csv_lines = read_csv_as_nested_list(CSV_FILE)
    a_list, length = csv_row_2_json_all(csv_lines, page, limit)
    json = jsonify({'size': length, 'blocks': a_list})

    return make_response(json)
