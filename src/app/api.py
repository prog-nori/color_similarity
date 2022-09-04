from flask import (
    Blueprint,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for
    )
from src.db.images import DBImagesTable
from src.util.utility import (
    CSV_FILE,
    csv_row_2_json_all,
    find_similar_colors,
    get_formatted_datetime,
    read_csv_as_nested_list
    )
from werkzeug.utils import secure_filename
import os
from pprint import pprint

api = Blueprint("api", __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg'])
UPLOAD_FOLDER = './templates/images/uploads'


def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/servicies/v2/blocks/<page>')
def get_blocks(page):
    page = int(page)
    limit = 50
    csv_lines = read_csv_as_nested_list(CSV_FILE)
    a_list, length = csv_row_2_json_all(csv_lines, page, limit)
    json = jsonify({'size': length, 'blocks': a_list})

    return make_response(json)

@api.route('/servicies/v2/find/<identifier>')
def api_find(identifier):
    """
    与えられた画像の識別子で検索を行う
    <s>画像アップロード後の画面</s>
    """
    db = DBImagesTable()
    filename = db.get(identifier)[0]['filename']
    print('FILENAME:', filename)
    target = os.path.join(UPLOAD_FOLDER, filename)
    similars = find_similar_colors(target)
    a_list = [d.get('info').__dict__ for d in similars]

    response = jsonify({'img': target[len('./templates'):], 'similars': a_list})
    return make_response(response)


@api.route('/servicies/v2/uploads', methods=['POST'])
def api_upload():
    """
    画像をアップロードする
    <s>与えられた画像から近似色のブロックを検索する</s>
    """
    # Todo: [Phase2.0] 画像をアップロードして識別子を返す
    # Todo: [Phase3.0] RDBを実装
    # Todo: [Phase3.0] 同じ画像が存在したら保存せず、その登録IDだけ返す
    error_msg = 'ファイルがありません'
    error_response = lambda msg: { 'status': 500, 'message': msg }
    db = DBImagesTable()
    image = request.files['image']
    if image.filename == '':
        return error_response(error_msg)
    elif image and allwed_file(image.filename):
        name, ext = image.filename.rsplit('.', 1)
        if ext is None:
            return error_response(error_msg)
        filename = '{}--{}.{}'.format(secure_filename(name), get_formatted_datetime(), ext)
        image.save(os.path.join(UPLOAD_FOLDER, filename))
        id = db.add(filename)
        return {
            'status': 200,
            'filename': filename,
            'id': id
        }
    error_msg = 'ヨキセヌ例外が発生しました'
    return error_response(error_msg)
