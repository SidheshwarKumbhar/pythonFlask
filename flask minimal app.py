from flask import Flask, render_template, request, redirect
import pandas as pd
import json
import csv
import datetime

app = Flask(__name__)


def all_data():
    data_dict = {}
    with open("phdirectoiry.csv", encoding='utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)

        for rows in csv_reader:
            key = rows["sr_no"]
            data_dict[key] = rows

        json.dumps(data_dict, indent=4)
        return data_dict


def num_of_rows():
    input_file = open("phdirectoiry.csv", "r+")
    reader_file = csv.reader(input_file)
    value = len(list(reader_file))
    return value

@app.route('/', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        title = request.form['name']
        desc = request.form['phone']

        value = num_of_rows()
        data = {"sr_no": [value],
                "Name": [title],
                "Ph_no": [desc],
                "date_time": [datetime.datetime.now()]}
        data = pd.DataFrame(data)
        data.to_csv("phdirectoiry.csv", mode='a', header=False, index=False)

    col = all_data()
    return render_template('index.html', col=col)


@app.route('/delete/<cols>')
def delete(cols):
    s = int(cols)
    s -= 1
    data_del = pd.read_csv("phdirectoiry.csv")
    data_del = data_del.drop(int(s))
    data_del.to_csv("phdirectoiry.csv", index=False)

    row_num = num_of_rows()
    row_num -= 1
    for i in range(row_num):
        df = pd.read_csv("phdirectoiry.csv")
        x = i
        x += 1
        df.loc[i, 'sr_no'] = x
        df.to_csv("phdirectoiry.csv", index=False)

    return redirect('/')


@app.route('/update/<cols>')
def update(cols):

    value = all_data()
    name = value[cols]["Name"]
    phno = value[cols]["Ph_no"]
    srno = cols
    return render_template('update.html', name=name, phno=phno, srno=srno)

@app.route('/do_update/', methods=['GET', 'POST'])
def do_update():
    if request.method == 'POST':
        title = request.form['name']
        desc = request.form['phone']
        num = request.form['sr_no']

        num = int(num)
        num -= 1
        df = pd.read_csv("phdirectoiry.csv")
        df.loc[num, 'Name'] = title
        df.to_csv("phdirectoiry.csv", index=False)

        df.loc[num, 'Ph_no'] = desc
        df.to_csv("phdirectoiry.csv", index=False)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
