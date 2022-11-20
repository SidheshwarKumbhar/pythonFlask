"""----------------------------------------------------------------------------------------------------------
Background:
*This Full stack Development of CURD App project is done to get hands-on experience on the CSS,HTML and Python Flask. I Used this opportunity to apply the knowledge I had learnt in the CSS,HTML and Python as a part of  my training.
 CRUD apps are the user interface that we use to interact with databases through APIs. It is a specific type of application that supports the four basic operations: Create, read, update, delete. Broadly, CRUD apps consist of the database, the user interface, and the APIs.
*CRUD apps are used daily by several businesses and organizations to maintain their day-to-day workflows. HR uses CRUD apps to manage staff records and track keeping of employee leaves, attendance.
*In this Full stack Development of CRUD app Project will implement the concepts of CRUD.
What you did:
*The purpose of this project is to create Phone Directory app  where we can add the contact, display the contact  form database, update the contact if required and to delete the contact.
*To achieve the goal of the Full stack Development of CRUD app we will follow the following steps:
*Creating the user interface (UI) is the front-end that the end-user interact with the help of HTML and CSS.
*Creating CSV file as a local database to store the data.
*Finally, the back-end using the Python flask that informs the databases and UI what functions and operations to perform.
Learnings and Challenges:
*Successfully able to add, read/show, update and delete the contacts from the phone directory app.

--------------------------------------------------------------------------------------------------------------"""
from flask import Flask, render_template, request, redirect
import pandas as pd
import json
import csv
import datetime

app = Flask(__name__)

def all_data():             # all the data in the jsom format
    data_dict = {}
    with open("phdirectoiry.csv", encoding='utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)

        for rows in csv_reader:
            key = rows["sr_no"]
            data_dict[key] = rows

        json.dumps(data_dict, indent=4)
        return data_dict

def num_of_rows():              # give the number of rows in csv file
    input_file = open("phdirectoiry.csv", "r+")
    reader_file = csv.reader(input_file)
    value = len(list(reader_file))
    return value

# this rute get the data from the form and put that data in csv file
# also this route hold the data of our csv file in the table
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

# this route will delete the specific selected row of the tabel
# and after deleting the row it will also update the sr.no of the table
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

# this update route render the name and number of the person who s data needs to be updated
# in the update page.
@app.route('/update/<cols>')
def update(cols):

    value = all_data()
    name = value[cols]["Name"]
    phno = value[cols]["Ph_no"]
    srno = cols
    return render_template('update.html', name=name, phno=phno, srno=srno)

# do_update route will put the  specific row in the csv file, and it also redirects us to home page
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
