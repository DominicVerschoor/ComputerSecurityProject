create_table_cmd = """
DROP TABLE IF EXISTS server_tb;

CREATE TABLE IF NOT EXISTS server_tb (
    user_id INT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL,
    value INT,
    create_time INT DEFAULT CURRENT_TIMESTAMP
)
"""

insert_table_cmd = """
    INSERT INTO server_tb (user_id, password, value) VALUES ({}, "{}", {});
"""



