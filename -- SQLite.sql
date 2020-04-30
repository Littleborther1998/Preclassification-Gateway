-- SQLite
ALTER TABLE classification RENAME req_time to class_time
SELECT * from classification
SELECT * from patents
PRAGMA table_info('classification');
PRAGMA table_info('patents')
CREATE TABLE classification (id INTEGER PRIMARY KEY AUTOINCREMENT, uniqueid TEXT, 
patentid TEXT, rank INTEGER, precla_symbol TEXT, confidence FLOAT, source TEXT, class_time FLOAT);
CREATE TABLE patents (uniqueid TEXT PRIMARY KEY, patentid TEXT, filename TEXT, zipfile LARGE BINARY, extuuid TEXT, req_time FLOAT)
DROP TABLE classification;
DROP TABLE patents