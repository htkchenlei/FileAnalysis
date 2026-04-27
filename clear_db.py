import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'backend', 'instance', 'files.db')
print(f"数据库路径: {db_path}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查看所有记录
    cursor.execute("SELECT id, filename, status, original_name FROM file_record")
    records = cursor.fetchall()
    print(f"数据库记录数: {len(records)}")
    for r in records:
        print(f"  ID: {r[0]}, 文件名: {r[1]}, 状态: {r[2]}, 原始文件名: {r[3]}")

    # 删除所有记录
    cursor.execute("DELETE FROM file_record")
    conn.commit()
    print(f"已删除所有记录")

    # 验证
    cursor.execute("SELECT COUNT(*) FROM file_record")
    count = cursor.fetchone()[0]
    print(f"删除后记录数: {count}")

    conn.close()
else:
    print(f"数据库文件不存在: {db_path}")
