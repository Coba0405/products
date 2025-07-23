import sys, pathlib
import sqlite3
import json
import app as salary_app

SCHEMA = """
CREATE TABLE salaries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  year INTEGER,
  month TEXT,
  company TEXT,
  base_salary INTEGER,
  overtime_pay INTEGER,
  allowances INTEGER,
  transport INTEGER,
  expense_reimburse INTEGER,
  income_other INTEGER,
  health_insurance INTEGER,
  pension INTEGER,
  employment_insurance INTEGER,
  nursing_insurance INTEGER,
  income_tax INTEGER,
  resident_tax INTEGER,
  deduction_other INTEGER,
  refund INTEGER,
  working_days INTEGER,
  paid_leave INTEGER,
  working_hours INTEGER,
  overtime_in INTEGER,
  overtime_out INTEGER,
  holiday_work INTEGER,
  memo TEXT
);
"""

def init_test_db(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.executescript(SCHEMA)

    cur.executemany("""
        INSERT INTO salaries (
            year, month, company,
            base_salary, overtime_pay, allowances, transport,
            expense_reimburse, income_other,
            health_insurance, pension, employment_insurance, nursing_insurance,
            income_tax, resident_tax, deduction_other, refund,
            working_days, paid_leave, working_hours, overtime_in, overtime_out, holiday_work,
            memo
        ) VALUE (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, [
        (2024, "1月", "A", 200000,10000,5000,3000,0,0, 10000,15000,1000,0,5000,10000,0,0, 20,0,160,0,0,0,""),
        (2024, "2月", "A", 210000, 8000,4000,3000,0,0, 10000,15000,1000,0,5200,10000,0,0, 20,0,160,0,0,0,""),
        (2024, "夏季賞与","A",300000,0,0,0,0,0,        15000,20000,1500,0,8000,15000,0,0, 0,0,0,0,0,0,"bonus"),
        (2025, "1月", "A", 220000, 9000,4000,3000,0,0, 11000,15500,1100,0,5500,10500,0,0, 20,0,160,0,0,0,"")
    ])
    conn.commit()
    cur.close()
    conn.close()

def test_income_by_year(monkeypatch, tmp_path):
    test_db = tmp_path / "test.db"
    init_test_db(str(test_db))

    monkeypatch.setattr(salary_app, "DB_PATH", str(test_db))

    client = salary_app.app.test_client()
    resp = client.get("/IncomeByYear")
    assert resp.status_code == 200

    data =resp.get_json()
    years = [row["year"] for row in data]
    assert years == [2024, 2025]

    y2024 = data[0]
    deduction_2024_manual = (
        (200000+10000+5000+3000+0+0) +
        (210000+ 8000+4000+3000+0+0) +
        (300000+0+0+0+0+0)
    )
    assert y2024["deduction"] == deduction_2024_manual
    assert y2024["net"] == y2024["income"] - y2024["deduction"]
