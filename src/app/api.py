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

@api.route('/servicies/v2/find/<filename>')
def api_find(filename):
    """
    与えられた画像で検索を行う
    <s>画像アップロード後の画面</s>
    """
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
    image = request.files['image']
    print(68, image)
    print('条件1:', bool(image.filename == ''))
    print('条件2:', bool(image and allwed_file(image.filename)))
    if image.filename == '':
        error_msg = 'ファイルがありません'
        return {
            'status': 500,
            'message': error_msg
        }
    elif image and allwed_file(image.filename):
        name, ext = image.filename.rsplit('.', 1)
        if ext is None:
            error_msg = 'ファイルがありません'
            return {
                'status': 500,
                'message': error_msg
            }
        filename = '{}--{}.{}'.format(secure_filename(name), get_formatted_datetime(), ext)
        image.save(os.path.join(UPLOAD_FOLDER, filename))
        return {
            'status': 200,
            'filename': filename
        }
    error_msg = 'ヨキセヌ例外が発生しました'
    return {
        'status': 500,
        'message': error_msg
    }

# @api.route('/servicies/v2/find', methods=['GET', 'POST'])
# def api_find():
#     """
#     与えられた画像から近似色のブロックを検索する
#     """
#     if request.method == 'POST':
#         image = request.files['image']
#         if image.filename == '':
#             raise FileNotFoundError('ファイルがありません')
#             # flash('ファイルがありません')
#             # redirect(request.url)
#         if image and allwed_file(image.filename):
#             name, ext = image.filename.rsplit('.', 1)
#             if ext is None:
#                 raise FileNotFoundError('ファイルがありません')
#                 # flash('ファイルがありません')
#                 # redirect(request.url)
#             filename = '{}--{}.{}'.format(secure_filename(name), get_formatted_datetime(), ext)
#             image.save(os.path.join(UPLOAD_FOLDER, filename))
#             return redirect(url_for('uploaded', filename=filename))
#     raise Exception('ヨキセヌ例外が発生しました')

#     # return render_template('find.html')


# @api.route('/servicies/v2/uploads/<filename>')
# def api_uploaded(filename):
#     """
#     画像アップロード後の画面
#     """
#     target = os.path.join(UPLOAD_FOLDER, filename)
#     similars = find_similar_colors(target)
#     a_list = [d.get('info').__dict__ for d in similars]

#     response = jsonify({'img': target[len('./templates'):], 'similars': a_list})
#     return make_response(response)
