from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pathlib import Path
import sqlite3

app = Flask(__name__)
CORS(app)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / 'salaries.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS withholding_tax (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL UNIQUE,
            company TEXT DEFAULT '',
            payment_amount INTEGER DEFAULT 0,
            after_deduction INTEGER DEFAULT 0,
            total_income_deduction INTEGER DEFAULT 0,
            withholding_tax_amount INTEGER DEFAULT 0,
            social_insurance_amount INTEGER DEFAULT 0,
            life_insurance_deduction INTEGER DEFAULT 0,
            earthquake_insurance_deduction INTEGER DEFAULT 0,
            housing_loan_deduction INTEGER DEFAULT 0,
            spouse_deduction INTEGER DEFAULT 0,
            dependent_count INTEGER DEFAULT 0,
            memo TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/salaries', methods=['GET'])
def get_salaries():
    year  = request.args.get('year',  type=int)
    month = request.args.get('month')

    where   = []
    params  = []

    if year is not None:
        where.append('year = ?')
        params.append(year)

    if month:
        where.append('month = ?')
        params.append(month)

    sql = 'SELECT * FROM salaries'
    if where:
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

    conn.execute('DELETE FROM salaries WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'deleted', 'id':item_id})

# ── 源泉徴収票 ──────────────────────────────────────────────

@app.route('/api/withholding_tax', methods=['GET'])
def get_withholding_tax_list():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM withholding_tax ORDER BY year DESC').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/withholding_tax/<int:year>', methods=['GET'])
def get_withholding_tax(year):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM withholding_tax WHERE year = ?', (year,)).fetchone()
    conn.close()
    if row is None:
        return jsonify(None)
    return jsonify(dict(row))

@app.route('/api/withholding_tax', methods=['POST'])
def create_withholding_tax():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO withholding_tax (
            year, company, payment_amount, after_deduction,
            total_income_deduction, withholding_tax_amount,
            social_insurance_amount, life_insurance_deduction,
            earthquake_insurance_deduction, housing_loan_deduction,
            spouse_deduction, dependent_count, memo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['year'], data.get('company', ''),
        data.get('payment_amount', 0), data.get('after_deduction', 0),
        data.get('total_income_deduction', 0), data.get('withholding_tax_amount', 0),
        data.get('social_insurance_amount', 0), data.get('life_insurance_deduction', 0),
        data.get('earthquake_insurance_deduction', 0), data.get('housing_loan_deduction', 0),
        data.get('spouse_deduction', 0), data.get('dependent_count', 0),
        data.get('memo', '')
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': '源泉徴収票を登録しました'}), 201

@app.route('/api/withholding_tax/<int:item_id>', methods=['PUT', 'DELETE'])
def withholding_tax_by_id(item_id):
    conn = get_db_connection()

    if request.method == 'PUT':
        d = request.get_json()
        conn.execute('''UPDATE withholding_tax SET
            year=?, company=?, payment_amount=?, after_deduction=?,
            total_income_deduction=?, withholding_tax_amount=?,
            social_insurance_amount=?, life_insurance_deduction=?,
            earthquake_insurance_deduction=?, housing_loan_deduction=?,
            spouse_deduction=?, dependent_count=?, memo=?
            WHERE id=?''',
            (
                d['year'], d.get('company', ''),
                d.get('payment_amount', 0), d.get('after_deduction', 0),
                d.get('total_income_deduction', 0), d.get('withholding_tax_amount', 0),
                d.get('social_insurance_amount', 0), d.get('life_insurance_deduction', 0),
                d.get('earthquake_insurance_deduction', 0), d.get('housing_loan_deduction', 0),
                d.get('spouse_deduction', 0), d.get('dependent_count', 0),
                d.get('memo', ''), item_id
            )
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'updated', 'id': item_id})

    conn.execute('DELETE FROM withholding_tax WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'deleted', 'id': item_id})

# ── 年別所得 ────────────────────────────────────────────────

@app.route('/IncomeByYear', methods=['GET'])
def income_by_year():
    conn = get_db_connection()
    cur = conn.cursor()

    sql = """
    SELECT year,
        SUM(base_salary + overtime_pay + allowances + transport + expense_reimburse + income_other) AS total_income,
        SUM(base_salary + overtime_pay + allowances + income_other) AS taxable_income,
        SUM(health_insurance + pension + employment_insurance + nursing_insurance + income_tax + resident_tax + deduction_other - refund) AS total_deduction
    FROM salaries
    GROUP BY year
    ORDER BY year;
    """

    rows = cur.execute(sql).fetchall()
    cur.close()
    conn.close()

    result = []
    for year, income, taxable, deduction in rows:
        net = income - deduction
        result.append({
            "year": year,
            "income": income,
            "taxable_income": taxable,
            "deduction": deduction,
            "net": net
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
