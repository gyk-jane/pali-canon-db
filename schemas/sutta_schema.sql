BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Authors" (
	"author_uid"	TEXT,
	"author_short"	TEXT,
	"author_fullname"	TEXT,
	PRIMARY KEY("author_uid")
);
CREATE TABLE IF NOT EXISTS "Languages" (
	"lang"	TEXT,
	"lang_name"	TEXT,
	PRIMARY KEY("lang")
);
CREATE TABLE IF NOT EXISTS "TextInfo" (
	"uid"	VARCHAR(255),
	"parent_uid"	VARCHAR(255),
	"blurb"	VARCHAR(255),
	"original_title"	VARCHAR(255),
	"translated_title"	VARCHAR(255),
	"acronym"	VARCHAR(255),
	"difficulty"	VARCHAR(255),
	"basket"	VARCHAR(255),
	"root_lang_name"	VARCHAR(255),
	"root_lang"	VARCHAR(255),
	"type"	VARCHAR(255),
	PRIMARY KEY("uid")
);
CREATE TABLE IF NOT EXISTS "LeafLineage" (
	"uid"	TEXT,
	"lineage"	TEXT,
	FOREIGN KEY("uid") REFERENCES "TextInfo"("uid")
);
CREATE TABLE IF NOT EXISTS "Translations" (
	"id"	TEXT,
	"uid"	TEXT,
	"lang"	TEXT,
	"author_uid"	TEXT,
	"file_path"	TEXT,
	"text"	TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("uid") REFERENCES "TextInfo"("uid"),
	FOREIGN KEY("author_uid") REFERENCES "Author"("author_uid")
);
COMMIT;
