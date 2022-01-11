from flask import Flask, render_template, request, url_for, redirect,session,flash
import sqlite3


sql_connect = sqlite3.connect('app/Headphone.db', check_same_thread=False)
cursor = sql_connect.cursor()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about', methods=["GET", "POST"])
def about2():
    if request.method == "POST":
        value1 = request.form.getlist('genre')
        value2 = request.form.getlist('activity')

        query = "SELECT DISTINCT * FROM Headphones WHERE "
        query1 = ""
        if len(value1) > 0:
            for i in range(len(value1)):
                query1 += "Headphones.Genre = \'" + value1[i] + "\' "
                if i != (len(value1)-1):
                    query1 += " or "
            query1 += " "
        query2 = ""
        if len(value2) > 0:
            for i in range(len(value2)):
                query2 += "Headphones.Activity = \'" + value2[i] + "\' "
                if i != (len(value2)-1):
                    query2 += " or "
            query2 += " "
        query += query1 + " or " + query2
        cursor.execute(query)
        sql_connect.commit()
        data = cursor.fetchall()
        return render_template('search.html', data=data,query = query)
    return render_template('about.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    query1 = "SELECT * FROM Headphones"
    query2 = ""
    if request.method=="GET":
        query3 = session.get('query1')
        if query3 != None:
            query1 = query3
        query4 = session.get('query2')
        if query4 != None:
            query2 += query4


    if request.method == "POST":
        text = request.form.get('text')
        print(text)
        if text == 'all':
            query1 += ""
        elif text == "":
            m = 'Please enter a valid brand or model'
            return render_template('message.html',msg = m)
        else:
            query1 += " WHERE Model LIKE \'" + text + "\' OR Brand LIKE \'" + text + "\'"
            cursor.execute(query1)
            sql_connect.commit()
            tmp= cursor.fetchall()
            if len(tmp)==0:
                m = 'Headphone doesn\'t exist or name is not valid, please retry'
                return render_template('message.html',msg = m)
        session['query1'] = query1
    query = query1 + query2
    cursor.execute(query)
    sql_connect.commit()
    data = cursor.fetchall()
    return render_template('search.html', data=data)



@app.route('/search/sort', methods=['GET', 'POST'])
def sort():
    query2 = ""
    if request.method == "POST":
        val = request.form.get('sort')
        if val == "Price1":
            query2 += " ORDER BY Price"
        elif val == "Price2":
            query2 += " ORDER BY Price DESC"
        elif val == "Releasedate":
            query2 += " ORDER BY Releasedate DESC"
    session['query2'] = query2
    return redirect(url_for('search'))


@app.route("/review", methods=['GET', 'POST'])
def review():
    query1 ="SELECT * FROM Reviews WHERE Brand = 'Sony' AND Model= 'WH-1000XM4'"
    l=['Sony', 'WH-1000XM4']
    if request.method == "POST":
        l = request.form.get("brand")
        l = l.split(',')
        query1 = 'SELECT * FROM Reviews WHERE Brand = \'' + l[0] +'\''+ ' AND Model= \'' + l[1] +'\''
        c = request.form.get("check")
        if c != None:
            query1 += ' AND Professional = \'Yes\''
    query = 'SELECT DISTINCT brand, model FROM Reviews'
    cursor.execute(query)
    sql_connect.commit()
    data = cursor.fetchall()
    cursor.execute(query1)
    sql_connect.commit()
    data2 = cursor.fetchall()
    print(l)

    if len(data2)==0:
            flash('Currently no professional reviews available for this headphone, please retry')
    return render_template('review.html',data=data, query = data2, prev = l)




@app.route("/headphone", methods=['GET', 'POST'])
def info():
    if 'view' in request.args:
        headphone_id = request.args['view']
        query = "SELECT * FROM Headphones WHERE Model = \'" + headphone_id + "\'"
        cursor.execute(query)
        sql_connect.commit()
        data = cursor.fetchall()
        query2 = "SELECT * FROM Reviews WHERE Model = \'" + headphone_id + "\'"
        cursor.execute(query2)
        sql_connect.commit()
        data2 = cursor.fetchall()
        return render_template('info.html', data=data, data2=data2)
    return render_template('info.html')



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
