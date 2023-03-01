CREATE DATABASE IF NOT EXISTS airflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'airflow' IDENTIFIED BY 'airflow';
GRANT ALL PRIVILEGES ON airflow.* TO 'airflow';

CREATE DATABASE IF NOT EXISTS datawarehouse CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON datawarehouse.* TO 'airflow';

CREATE TABLE IF NOT EXISTS datawarehouse.euribor1w_dag_raw(
    created_at TIMESTAMP default NOW(),
    value      JSON,
    INDEX created_at_index(created_at)
);
CREATE TABLE IF NOT EXISTS datawarehouse.euribor1w_dag_transformed (
    id         VARCHAR(38) PRIMARY KEY,
    created_at TIMESTAMP default NOW(),
    value      FLOAT,
    INDEX created_at_index(created_at)
);