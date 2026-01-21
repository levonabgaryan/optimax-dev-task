# Optimax-dev-task

This project contains solutions to four SQL tasks and one Python task. 
The project uses SQLite for testing and simplicity, developed with Python 3.14.

## 📖 Solution Reference

If you want to review the code without running the scripts, please refer to the following directories:

### SQL
* **Task 1:** `sql_tasks/1_question.py` → `query_function()`
* **Task 2:** `sql_tasks/2_question.py` → `query_function()`
* **Task 3:** `sql_tasks/3_question.py` → `query_function()`
* **Task 4:** `sql_tasks/4_question.py` → `query_function()`

### Python
* **Task1:** `python_tasks/1_questions/implementation.py` → `convert_pub_sub_message_to_dict()`, `save_data_to_db()`
---

## 🚀 Execution Guide
### SQL
**Set up the SQLite database:**
```
python sql_tasks/setup_db.py 
```
Note: If you see the message ✅ Data has been successfully imported!, it means all tables have been created and sample data has been populated.


**Run a script (example):**
```
python sql_tasks/1_question.py
```

### Python
**Set up the database:**
```
python python_tasks/setup_db.py 
```

* Run the Python script:
```
python python_tasks/1_questions/test.py
```
