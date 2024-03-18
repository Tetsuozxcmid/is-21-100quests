from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random

app = Flask(__name__, template_folder='templates', static_folder='static')

# чтение файла , создание словаря


def data():
    xls = pd.ExcelFile('100quest.xlsx')
    data_frame_dict = {}
    for sheet_name in xls.sheet_names:
        data_frame_dict[sheet_name] = pd.read_excel(
            xls, sheet_name, index_col=0)
    return data_frame_dict


# присваивание для дальнейшего использования в руте "/"
data = data()


@app.route("/")
def index():
    sheets = data.keys()
    return render_template('index.html', sheets=sheets)


@app.route('/question/', methods=['POST'])
def quests():
    value = data.keys()
    sheetall = request.form['index']
    sample_obj = data[sheetall].sample()
    data[sheetall].drop(sample_obj.index, inplace=True)
    count = len(data[sheetall].index)
    if count == 0:
        return redirect(url_for('index'))

    return render_template('question.html', sheetall=sheetall, name=sample_obj.iloc[0, 0], work=sample_obj.iloc[0, 1], chin=sample_obj.iloc[0, 2], question=sample_obj.iloc[0, 3], anoth=sheetall, count=count)


if __name__ == "__main__":
    app.run(debug=True)
