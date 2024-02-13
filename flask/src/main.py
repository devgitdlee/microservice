from flask import Flask,jsonify, render_template, request, url_for, redirect,send_from_directory
import pymysql
import config
import uuid
import os
from werkzeug.utils import secure_filename
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
            return "Error creating record!"

    return render_template('create.html')

@app.route('/read')
def read():
    try:
        # Create SQL query
        sql = "SELECT * FROM board"
        cursor.execute(sql)
        records = cursor.fetchall(20)
        return render_template('read.html', records=records)
    except Exception as e:
        # Handle errors
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
            sql = "UPDATE BOARD SET board_title = %s, board_content = %s WHERE board_id = %s"
            cursor.execute(sql, (title, content, id))
            conn.commit()

            return redirect(url_for('read'))
        except Exception as e:
            # Handle errors
            return "Error updating record!"
        


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        try:
            # Get form data
            # Create SQL query
            sql = "delete from BOARD WHERE board_id = %s"
            cursor.execute(sql, (id))
            conn.commit()

            return redirect(url_for('read'))
        except Exception as e:
            # Handle errors
            print(e)
            return "Error updating record!"


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        try:
            file = request.files["file"]    
            file_uuid = uuid.uuid4()

            filepathsave = os.path.join(config.FILE_SAVE_PATH,secure_filename(file.filename))
            file.save(filepathsave)
            # Create SQL query
            sql = "INSERT INTO TB_FILE (file_id, file_path, file_name) values(%s,%s,%s)"
            cursor.execute(sql, (file_uuid,config.FILE_SAVE_PATH,file.filename))
            conn.commit()
            

            return redirect(url_for("uploadhome"))
        except Exception as e:
            # Handle errors
            return "Error upload record!"
        

@app.route("/uploadhome")
def uploadhome():
    return render_template("fileupload.html")


@app.route("/download", methods=["POST"])
def download_file():
    try:
        # Get form data      
        data = request.get_json()
        file_id = data.get('file_id')
        

        # Create SQL query
        sql = "SELECT file_path, file_name FROM TB_FILE where file_id = %s"
        cursor.execute(sql, (file_id))
        records = cursor.fetchone
        

        return send_from_directory(records.file_path, records.file_name)
    except Exception as e:
        # Handle errors
        print(e)
        return "Error download record!"
   

if __name__ == '__main__':
  app.run("0.0.0.0", port=8080)