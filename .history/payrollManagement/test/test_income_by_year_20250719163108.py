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
    cur = conn.cursor
