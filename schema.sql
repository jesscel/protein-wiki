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
  -- id TEXT NOT NULL,
  info TEXT NOT NULL,
  img_url TEXT NOT NULL
);
 
CREATE INDEX `name`
  ON `protein` (`name`);

INSERT INTO "protein" VALUES
('MSANTD1','This is protein MSANTD1.','/Users/liuenci/Desktop/aws/protein_wiki_data/tiling_plots_jpg/MSANTD1.jpg'),
('ZNF575','This is protein ZNF575.','/Users/liuenci/Desktop/aws/protein_wiki_data/tiling_plots_jpg/ZNF575.jpg'),
('SPOUT1','This is protein SPOUT1.','/Users/liuenci/Desktop/aws/protein_wiki_data/tiling_plots_jpg/SPOUT1.jpg'),
('MESP1','This is protein MESP1.','/Users/liuenci/Desktop/aws/protein_wiki_data/tiling_plots_jpg/MESP1.jpg'),
('BRCA1','This is protein BRCA1.','/Users/liuenci/Desktop/aws/protein_wiki_data/tiling_plots_jpg/BRCA1.jpg');
