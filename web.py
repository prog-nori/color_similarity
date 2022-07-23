from crypt import methods
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from src.util.text.pagination import Pagination
from src.util.utility import (
    CSV_FILE,
    csv_row_2_dict_all,
    find_similar_colors,
    get_formatted_datetime,
    read_csv_as_nested_list
    )

app = Flask(__name__, static_folder='./templates/images')

ALLOWED_EXTENSIONS = set(['png', 'jpg'])
UPLOAD_FOLDER = './templates/images/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blocks', methods=['GET'])
def block_list(lim=20):
    req = request.args
    page = req.get('page')
    if page is None:
        page = 0
    else:
        page = int(page)
    offset, limit = page * lim, (page + 1) * lim

    csv_lines = read_csv_as_nested_list(CSV_FILE)
    a_list = csv_row_2_dict_all(csv_lines)

    pagination = Pagination(offset, limit, a_list)

    return render_template('blocks.html', title='ブロックリスト', pagination=pagination)


@app.route('/find', methods=['GET', 'POST'])
def find():
    """
    与えられた画像から近似色のブロックを検索する
    """
    if request.method == 'POST':
        image = request.files['image']
        if image.filename == '':
            flash('ファイルがありません')
            redirect(request.url)
        if image and allwed_file(image.filename):
            name, ext = image.filename.rsplit('.', 1)
            if ext is None:
                flash('ファイルがありません')
                redirect(request.url)
            filename = '{}--{}.{}'.format(secure_filename(name), get_formatted_datetime(), ext)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded', filename=filename))

    return render_template('find.html')


@app.route('/uploads/<filename>')
def uploaded(filename):
    """
    画像アップロード後の画面
    """
    target = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    similars = find_similar_colors(target)
    a_list = [d.get('info') for d in similars]
    return render_template('similar.html', img=target[len('./templates'):], similars=a_list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
