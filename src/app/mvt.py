from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from src.util.utility import (
    CSV_FILE,
    csv_row_2_dict_all,
    find_similar_colors,
    get_formatted_datetime,
    read_csv_as_nested_list
    )

mvt = Blueprint("mvt", __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg'])
UPLOAD_FOLDER = './templates/images/uploads'


def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@mvt.route('/')
def index():
    return render_template('index.html')


@mvt.route('/blocks')
def block_list():
    csv_lines = read_csv_as_nested_list(CSV_FILE)
    a_list = csv_row_2_dict_all(csv_lines)

    return render_template('blocks.html', title='ブロックリスト', array=a_list)


@mvt.route('/find', methods=['GET', 'POST'])
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
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('uploaded', filename=filename))

    return render_template('find.html')


@mvt.route('/uploads/<filename>')
def uploaded(filename):
    """
    画像アップロード後の画面
    """
    target = os.path.join(UPLOAD_FOLDER, filename)
    similars = find_similar_colors(target)
    a_list = [d.get('info') for d in similars]
    return render_template('similar.html', img=target[len('./templates'):], similars=a_list)