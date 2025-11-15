-- Create database
CREATE DATABASE IF NOT EXISTS pico_iot;
USE pico_iot;

DROP TABLE IF EXISTS readings;

CREATE TABLE readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(64) NOT NULL,
    temp FLOAT,
    humidity FLOAT,
    pressure FLOAT NULL,
    light FLOAT NULL,
    raw_json JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Indexes for fast query filtering
CREATE INDEX idx_device_time ON readings (device_id, created_at);
CREATE INDEX idx_created_at ON readings (created_at);

-- Optional: Table to register devices (future proofing)
CREATE TABLE devices (
    device_id VARCHAR(64) PRIMARY KEY,
    nickname VARCHAR(128),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Test seed data
INSERT INTO readings (device_id, temp, humidity, pressure, light)
VALUES
('pico-001', 23.5, 45.2, 1012.3, 300),
('pico-001', 24.1, 44.8, 1011.9, 290),
('pico-dev',  21.9, 50.1, 1015.0, 310);
