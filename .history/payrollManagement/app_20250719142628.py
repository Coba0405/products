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
    year  = request.args.get('year',  type=int)   # 無いときは None
    month = request.args.get('month')             # 無いときは None

    # --- 条件式を可変で組み立てる ---
    where   = []
    params  = []

    if year is not None:          # 0 とは区別。int に変換済み
        where.append('year = ?')
        params.append(year)

    if month:                     # 空文字 '' は弾く
        where.append('month = ?')
        params.append(month)

    sql = 'SELECT * FROM salaries'
    if where:                     # 条件が 1 つでもあれば WHERE 句を付ける
        sql += ' WHERE ' + ' AND '.join(where)
    sql += ' ORDER BY year DESC, month DESC'

    conn  = get_db_connection()
    rows  = conn.execute(sql, params).fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])

@app.route('/api/salaries/<int:year>/<month>', methods=['GET'])
def get_salaries_by_year_month(year, month):
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT * FROM salaries WHERE year = ? AND month = ?',
        (year, month)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/salaries', methods=['POST'])
def create_salary():
    data = request.get_json()

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO salaries (
            year, month, company,
            base_salary, overtime_pay, allowances, transport, expense_reimburse, income_other,
            health_insurance, pension, employment_insurance, nursing_insurance,
            income_tax, resident_tax, deduction_other, refund,
            working_days, paid_leave, working_hours, overtime_in, overtime_out, holiday_work,
            memo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['year'], data['month'], data['company'],
        data['base_salary'], data['overtime_pay'], data['allowances'], data['transport'],
        data['expense_reimburse'], data['income_other'],
        data['health_insurance'], data['pension'], data['employment_insurance'],
        data['nursing_insurance'], data['income_tax'], data['resident_tax'], data['deduction_other'], data['refund'],
        data['working_days'], data['paid_leave'], data['working_hours'],
        data['overtime_in'], data['overtime_out'], data['holiday_work'],
        data['memo']
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': "給与明細を登録しました"}), 201

@app.route('/api/salaries/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def salary_by_id(item_id):
    conn = get_db_connection()

    if request.method == 'GET':
        row = conn.execute('SELECT * FROM salaries WHERE id = ?', (item_id,)).fetchone()
        conn.close()
        return (jsonify(dict(row)) if row else (jsonify({'error': 'not found'}), 404))

    if request.method == 'PUT':
        d = request.get_json()
        conn.execute("""UPDATE salaries SET
              year=?, month=?, company=?,
              base_salary=?, overtime_pay=?, allowances=?, transport=?, expense_reimburse=?, income_other=?,
              health_insurance=?, pension=?, employment_insurance=?, nursing_insurance=?,
              income_tax=?, resident_tax=?, deduction_other=?, refund=?,
              working_days=?, paid_leave=?, working_hours=?, overtime_in=?, overtime_out=?, holiday_work=?,
              memo=? WHERE id=?""",
            (
              d['year'], d['month'], d['company'],
              d['base_salary'], d['overtime_pay'], d['allowances'], d['transport'],
              d['expense_reimburse'], d['income_other'],
              d['health_insurance'], d['pension'], d['employment_insurance'],
              d['nursing_insurance'],d['income_tax'], d['resident_tax'], d['deduction_other'], d['refund'],
              d['working_days'], d['paid_leave'], d['working_hours'],
              d['overtime_in'], d['overtime_out'], d['holiday_work'],
              d['memo'], item_id
            )
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'updated', 'id': item_id})

    # DELETEメソッド
    conn.execute('DELETE FROM salaries WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'updated', 'id':item_id})

@app.route('/IncomeByYear.vue', method=)
def income_by_year():
    request.get()

if __name__ == '__main__':
    app.run(debug=True)
