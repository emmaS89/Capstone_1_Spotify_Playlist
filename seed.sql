DROP DATABASE IF EXISTS  spot;

CREATE DATABASE spot;

\c spot

CREATE TABLE users (
        id SERIAL NOT NULL,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        authenticated BOOLEAN,
        PRIMARY KEY (id)
);


CREATE TABLE playedSongs (
        id SERIAL NOT NULL,
        user_id INTEGER NOT NULL,
        song_name VARCHAR(50) NOT NULL,
        url VARCHAR(400) NOT NULL,
        "addedAt" VARCHAR(50) NOT NULL,
        time VARCHAR(50) NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);
