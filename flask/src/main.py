from flask import Flask,jsonify, render_template, request, url_for, redirect,send_from_directory,session,send_file
import pymysql
import config
import uuid
import os
import math
from werkzeug.utils import secure_filename

FILE_SAVE_PATH = "C:/file/"
FILE_DOWNLOAD_PATH = "다운로드"

app = Flask("JobScrapper")


conn = pymysql.connect(host=config.MYSQL_DATABASE_HOST,
                       port=config.MYSQL_DATABASE_PORT,
                       user=config.MYSQL_DATABASE_USER,
                       password=config.MYSQL_DATABASE_PASSWORD,
                       db=config.MYSQL_DATABASE_DB)

@app.route("/")
def home():
    return 'Hello Flask!'
    ## db연결 ##
    sql = "SELECT * FROM board where deldt is null" 
    boards = conn.executeAll(sql) 
    if 'userid' not in session:
        #print("비로그인 상태")
        return render_template('/main/index.html', boards=boards)

    #로그인시, write, delete, update 가능
    #admin은 db자체 편집가능 회원정보, 게시글정보
    #print("로그인 상태")
    userid = session.get('userid', None)
    return render_template('/main/index.html', userid=userid, boards=boards)
    


@app.route("/write")
def wirteview():
  return render_template('write_board.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            # Get form data
            print("aaaaa")
            data = request.get_json()
            print(data)
            title = data.get('title')
            content = data.get('content')
            # Create SQL query
            cursor = conn.cursor()
            sql = "INSERT INTO board (board_title, board_content) VALUES (%s, %s)"
            cursor.execute(sql, (title, content))
            conn.commit()
            return redirect(url_for('read'))
        except Exception as e:
            # Handle errors
            return "Error creating record!"
        finally:
            db_afterprocess(cursor)
    return render_template('write_board.html')

def board_read_cnt():
    try:
        cursor = conn.cursor()
        # Create SQL query
        sql = "SELECT count(1) FROM board where board_deldt is null"
        cursor.execute(sql)
        recode = cursor.fetchone()
        return recode[0]
    except Exception as e:
        # Handle errors
        return "Error board_read_cnt record!"
        

@app.route('/read/<page>', methods=['GET'])
def read(page):
    get_list_cnt = 20
    try:
        list_page = get_list_cnt * (int(page) - 1)
        cursor = conn.cursor()
        sql = "SELECT board_id, board_title, board_crtdt FROM board where board_deldt is null order by board_id desc limit %s OFFSET %s"
        cursor.execute(sql, (get_list_cnt,list_page))
        recodes = cursor.fetchall()
        page_cnt = board_read_cnt() / get_list_cnt
        return render_template('read_board.html', recodes=recodes,page_cnt=math.ceil(page_cnt),active_page=int(page))
    except Exception as e:
        # Handle errors
        return "Error fetching records!"
    finally:
        db_afterprocess(cursor)   

@app.route('/modify/<id>', methods=['GET', 'POST'])
def modify(id):
    if request.method == 'GET':
        try:
            cursor = conn.cursor()
            sql = "select board_id, board_title, board_content from board where board_id = %s"
            cursor.execute(sql, (id))
            recode = cursor.fetchone()
            return render_template('modify_board.html',recode=recode)
        except Exception as e:
            # Handle errors
            return "Error modify record!"   
        finally:
            db_afterprocess(cursor)
@app.route('/view/<id>', methods=['GET'])
def view(id):
    try:
        cursor = conn.cursor()
        sql = "select board_id, board_title, board_content from board where board_id = %s"
        cursor.execute(sql, (id))
        recode = cursor.fetchone()
        print(recode)
        return render_template('board_view.html',recode=recode)
    except Exception as e:
        # Handle errors
        return "Error view record!"
    finally:
        db_afterprocess(cursor)

    
@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        try:
            # Get form data
            print("aaaaa")
            data = request.get_json()
            print(data)
            title = data.get('title')
            content = data.get('content')
            cursor = conn.cursor()
            sql = "UPDATE board SET board_title = %s, board_content = %s, board_upddt = now() WHERE board_id = %s"
            cursor.execute(sql, (title, content, id))
            conn.commit()
            return redirect(url_for('read'))
        except Exception as e:
            # Handle errors
            return "Error updating record!"
        finally:
            db_afterprocess(cursor)


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        try:
            # Get form data
            # Create SQL query
            cursor = conn.cursor()
            sql = "update board set board_deldt = now() WHERE board_id = %s"
            cursor.execute(sql, (id))
            conn.commit()
            db_afterprocess(cursor)
            return redirect(url_for('read'))
        except Exception as e:
            # Handle errors
            print(e)
            return "Error delete record!"
        finally:
            db_afterprocess(cursor)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        try:
            file = request.files["file"]    
            file_uuid = uuid.uuid4()

            filepathsave = os.path.join(FILE_SAVE_PATH,secure_filename(file.filename))
            file.save(filepathsave)
            cursor = conn.cursor()
            sql = "INSERT INTO TB_FILE (file_id, file_path, file_name) values(%s,%s,%s)"
            cursor.execute(sql, (file_uuid,FILE_SAVE_PATH,file.filename))
            conn.commit()
            return redirect(url_for("uploadhome"))
        except Exception as e:
            # Handle errors
            return "Error upload record!"
        finally:
            db_afterprocess(cursor)

@app.route("/uploadhome")
def uploadhome():
    try:
        cursor = conn.cursor()
        sql = "SELECT file_id,file_name,file_crtdt FROM tb_file ORDER BY file_crtdt desc" 
        cursor.execute(sql)
        records = cursor.fetchall()
        return render_template("fileupload.html",records=records)
    except Exception as e:
        # Handle errors
        return "Error download record!"
    finally:
        db_afterprocess(cursor)

    
@app.route("/download/<id>", methods=["GET"])
def download_file(id):
    try:
        cursor = conn.cursor()
        sql = "SELECT file_path, file_name FROM tb_file where file_id = %s"
        cursor.execute(sql, (id))
        recode = cursor.fetchone()
        return send_file(recode[0]+recode[1],as_attachment=True)
    except Exception as e:
        # Handle errors
        return "Error download record!"
    finally:
        db_afterprocess(cursor)
   
def db_afterprocess(cursor):
    cursor.close()
    #conn.close()


if __name__ == '__main__':
  app.run("0.0.0.0", port=8080)