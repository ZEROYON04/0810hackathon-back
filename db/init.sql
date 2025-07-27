-- テーブルの作成
CREATE TABLE
    IF NOT EXISTS users (user_id SERIAL PRIMARY KEY);

-- 初期データの挿入
INSERT INTO
    users DEFAULT
VALUES;

INSERT INTO
    users DEFAULT
VALUES;

INSERT INTO
    users DEFAULT
VALUES;

INSERT INTO
    users DEFAULT
VALUES;

INSERT INTO
    users DEFAULT
VALUES;

CREATE TABLE
    IF NOT EXISTS random_problems (
        random_problem_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
        latitude FLOAT NOT NULL,
        longitude FLOAT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP,
        status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'completed', 'given_up')),
        image_url VARCHAR(255)
    );

-- 初期データの挿入
INSERT INTO
    random_problems (user_id, latitude, longitude, created_at, status)
SELECT
    user_id,
    latitude,
    longitude,
    created_at,
    status
FROM
    (
        SELECT
            user_id,
            36.00 AS latitude,
            140.432 AS longitude,
            CURRENT_TIMESTAMP - INTERVAL '1 year' AS created_at,
            'pending' AS status
        FROM
            users
    ) AS multi;

INSERT INTO
    random_problems (
        user_id,
        latitude,
        longitude,
        created_at,
        ended_at,
        status
    )
SELECT
    user_id,
    latitude,
    longitude,
    created_at,
    ended_at,
    status
FROM
    (
        SELECT
            user_id,
            35.32432 AS latitude,
            128.432 AS longitude,
            CURRENT_TIMESTAMP - INTERVAL '2 years' AS created_at,
            CURRENT_TIMESTAMP - INTERVAL '1 year' AS ended_at,
            'given_up' AS status
        FROM
            users
    ) AS multi;

INSERT INTO
    random_problems (
        user_id,
        latitude,
        longitude,
        created_at,
        ended_at,
        status,
        image_url
    )
SELECT
    user_id,
    latitude,
    longitude,
    created_at,
    ended_at,
    status,
    image_url
FROM
    (
        SELECT
            user_id,
            35.145 AS latitude,
            135.8765 AS longitude,
            CURRENT_TIMESTAMP - INTERVAL '1 year' AS created_at,
            CURRENT_TIMESTAMP - INTERVAL '6 months' AS ended_at,
            'completed' AS status,
            'https://example.com/image.jpg' AS image_url
        FROM
            users
    ) AS multi;