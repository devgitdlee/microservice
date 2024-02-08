from flask import Flask,jsonify, render_template, request, url_for, redirect
import pymysql
import config
app = Flask("JobScrapper")


conn = pymysql.connect(host=config.MYSQL_DATABASE_HOST,
                       port=config.MYSQL_DATABASE_PORT,
                       user=config.MYSQL_DATABASE_USER,
                       password=config.MYSQL_DATABASE_PASSWORD,
                       db=config.MYSQL_DATABASE_DB)
cursor = conn.cursor()

@app.route("/")
def home():
  return 'Hello Flask!'


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            # Get form data
            data = request.get_json()
            title = data.get('title')
            content = data.get('content')

            # Create SQL query
            sql = "INSERT INTO board (board_title, board_content) VALUES (%s, %s)"
            cursor.execute(sql, (title, content))
            conn.commit()

            return redirect(url_for('read'))
        except Exception as e:
            # Handle errors
            print(e)
            return "Error creating record!"

    return render_template('create.html')

@app.route('/read')
def read():
    try:
        # Create SQL query
        sql = "SELECT * FROM board"
        cursor.execute(sql)
        records = cursor.fetchall()
        return render_template('read.html', records=records)
    except Exception as e:
        # Handle errors
        print(e)
        return "Error fetching records!"
    
@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        try:
            # Get form data
            data = request.get_json()
            title = data.get('title')
            content = data.get('content')

            # Create SQL query
            sql = "UPDATE board SET board_title = %s, board_content = %s WHERE board_id = %s"
            cursor.execute(sql, (title, content, id))
            conn.commit()

            return redirect(url_for('read'))
        except Exception as e:
            # Handle errors
            print(e)
            return "Error updating record!"
        


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        try:
            # Get form data
            # Create SQL query
            sql = "delete from board WHERE board_id = %s"
            cursor.execute(sql, (id))
            conn.commit()

            return redirect(url_for('read'))
        except Exception as e:
            # Handle errors
            print(e)
            return "Error updating record!"


if __name__ == '__main__':
  app.run("0.0.0.0", port=8080)