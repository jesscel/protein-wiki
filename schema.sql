-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS protein;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE protein (
  name TEXT NOT NULL PRIMARY KEY,
  id TEXT NOT NULL,
  info TEXT NOT NULL,
  img_url TEXT NOT NULL
);
 
CREATE INDEX `id`
  ON `protein` (`name`);

INSERT INTO "protein" VALUES
('A1CF','Q9NQ94','APOBEC1 complementation factor','465785'),
('ABRAXAS1','Q6UWZ7','BRCA1-A complex subunit Abraxas 1','123456'),
('ABRAXAS2','Q15018','BRISC complex subunit Abraxas 2','234567');
