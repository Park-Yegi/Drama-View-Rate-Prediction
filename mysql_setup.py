import MySQLdb
connection = MySQLdb.connect(
    user = "scrapingman",
    passwd = "i7633647",
    host = "localhost",
    db = "scrapingdata",
    charset = "utf8")

cursor = connection.cursor()
cursor.execute("CREATE TABLE drama_info (id int auto_increment, drama_name varchar(50), channel varchar(10), start_time time, primary key(id))")
cursor.execute("CREATE TABLE view_rate (id int, episode int, view_rate numeric(3,1), broadcasting_time datetime, primary key(id, episode), foreign key(id) references drama_info(id))")
cursor.execute("CREATE TABLE drama_homepage(id int, url_hash char(16) not null unique, post_id int auto_increment, title varchar(100), modified_time datetime, body_text BLOB, primary key(post_id), foreign key(id) references drama_info(id))")
cursor.execute("CREATE TABLE naver_blog(id int, url_hash char(16) not null unique, article_id int auto_increment, title varchar(100), modified_time datetime, body_text BLOB, likes int, comments int, primary key(article_id), foreign key(id) references drama_info(id))")
cursor.execute("CREATE TABLE naver_news(id int, url_hash char(16) not null unique, news_id int auto_increment, title varchar(100), modified_time datetime, body_text BLOB, recommends int, comments int, primary key(news_id), foreign key(id) references drama_info(id))")
cursor.execute("CREATE TABLE instagram(id int, url_hash char(16) not null unique, post_id int auto_increment, modified_time datetime, body_text BLOB, likes int, comments int, primary key(post_id), foreign key(id) references drama_info(id))")
cursor.execute("CREATE TABLE facebook(id int, url_hash char(16) not null unique, post_id int auto_increment, modified_time datetime, body_text BLOB, likes int, comments int, shares int, primary key(post_id), foreign key(id) references drama_info(id))")

connection.commit()