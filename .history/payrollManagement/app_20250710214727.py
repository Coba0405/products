from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3


app = Flask(__name__)
CORS(app)
DB_PATH = 'salaries.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# API接続確認用
# @app.route('/')
# def index():
#     return '<h1>給与明細管理APIへようこそ！</h1><p>/api/salaries にアクセスしてください。</p>'

@app.route('/api/salaries', methods=['GET'])
def get_salaries():
    conn = get_db_connection()
    salaries = conn.execute('SELECT * FROM salaries ORDER BY year DESC, month DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in salaries])

@app.route('/api/salaries', methods=['POST'])
def create_salary():
    data = request.get_json()

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO salaries (
            year, month, company,
            base_salary, overtime_pay, allowances, transport, expense_reimburse, income_other,
            health_insurance, pension, employment_insurance, nursing_insurance, social_insurance,
            income_tax, resident_tax, deduction_other, refund,
            working_days, paid_leave, working_hours, overtime_in, overtime_out, holiday_work,
            memo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['year'], data['month'], data['company'],
        data['base_salary'], data['overtime_pay'], data['allowances'], data['transport'],
        data['expense_reimburse'], data['income_other'],
        data['health_insurance'], data['pension'], data['employment_insurance'],
        data['nursing_insurance'], data['social_insurance'],
        data['income_tax'], data['resident_tax'], data['deduction_other'], data['refund'],
        data['working_days'], data['paid_leave'], data['working_hours'],
        data['overtime_in'], data['overtime_out'], data['holiday_work'],
        data['memo']
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': "給与明細を登録しました"}), 201

@app.route('/api/salaries', methods=['GET'])
def get_salaries_filtered():
    year = request.args.get('year')
    month = request.args.get('month')

    query = 'SELECT * FROM salaries WHERE 1=1'
    

def get_salaries_by_year(year):
    conn = get_db_connection()
    salaries = conn.execute(
        'SELECT * FROM salaries WHERE year = ? ORDER BY month', (year,)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in salaries])

@app.route('/api/salaries/<int:month>', methods=['GET'])
def get_salaries_by_month(month):
    conn = get_db_connection()
    salaries = conn.execute(
        'SELECT * FROM salaries WHERE year = {year} ORDER BY month = ?', (month,)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in salaries])

if __name__ == '__main__':
    app.run(debug=True)
