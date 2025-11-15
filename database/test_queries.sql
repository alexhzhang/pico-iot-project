USE pico_iot;

-- View the 20 most recent readings
SELECT * FROM readings
ORDER BY created_at DESC
LIMIT 20;

-- Average values in the last hour
SELECT 
    AVG(temp) AS avg_temp,
    AVG(humidity) AS avg_humidity,
    AVG(pressure) AS avg_pressure,
    AVG(light) AS avg_light
FROM readings
WHERE created_at >= NOW() - INTERVAL 1 HOUR;

-- Group by device
SELECT device_id, COUNT(*) AS packets_sent
FROM readings
GROUP BY device_id;
