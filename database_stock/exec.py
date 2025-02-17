import pymysql

from configs.sql_config import db_config
from utils.log.yc_logger import logger


def build_connection():
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def sync_news(json_data):
    connection = build_connection()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO news (
                post_id, title, type, click_count, comment_count, publish_time,
                stock_code, nickname, origin_url
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            ) ON DUPLICATE KEY UPDATE 
                post_id = VALUES(post_id),
                title = VALUES(title),
                type = VALUES(type),
                click_count = VALUES(click_count),
                comment_count = VALUES(comment_count),
                publish_time = VALUES(publish_time),
                stock_code = VALUES(stock_code),
                nickname = VALUES(nickname),
                origin_url = VALUES(origin_url);
            """

            cursor.execute(sql, (
                json_data['post_id'],
                json_data['post_title'],
                1,
                json_data['post_click_count'],
                json_data['post_comment_count'],
                json_data['post_publish_time'],
                json_data['stockbar_code'],
                json_data['user_nickname'],
                json_data['Art_OriginUrl'] if json_data.__contains__('Art_OriginUrl') else json_data['Art_Url']
            ))

        connection.commit()
    # connection.close()


def sync_stock(json_data):
    connection = build_connection()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO stock_info (
                code, title
            ) VALUES (
                %s, %s
            ) ON DUPLICATE KEY UPDATE 
                code = VALUES(code),
                title = VALUES(title)
            """

            cursor.execute(sql, (
                json_data['code'],
                json_data['title']
            ))

        connection.commit()
    # connection.close()


def query_stock_from_database(keyword, is_limit=True):
    connection = build_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT * FROM stock_info
                WHERE 
                (code like %s or title like %s)
                LIMIT %s
                """
            limit = 10 if is_limit else 1000000
            cursor.execute(sql, (f"%{keyword}%", f"%{keyword}%", limit,))
            result = cursor.fetchall()  # 获取查询结果
            return result
    finally:
        connection.close()


def query_news_from_database(code, keyword, start_time, end_time):
    connection = build_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT s.code AS code,
                       s.title AS title,
                       JSON_ARRAYAGG(
                               JSON_OBJECT(
                                       'post_id', post_id,
                                       'title', n.title,
                                       'url', origin_url,
                                       'publish_time', publish_time
                               )
                       )          AS list
                FROM (SELECT *,
                             @row_num := IF(@current_stock_code = stock_code, @row_num + 1, 1) AS row_num,
                             @current_stock_code := stock_code
                      FROM news
                      WHERE title like %s
                      AND stock_code like %s
                      AND publish_time BETWEEN %s AND %s
                      ORDER BY stock_code, publish_time DESC) AS n
                JOIN stock_info s ON s.code = n.stock_code
                WHERE row_num <= 10
                GROUP BY stock_code;
                """
            cursor.execute(sql, (f"%{keyword}%", f"%{code}%", start_time, end_time,))
            result = cursor.fetchall()  # 获取查询结果
            return result
        # with connection.cursor() as cursor:
        #     sql = """
        #         SELECT n.*
        #         FROM news n
        #         WHERE
        #         publish_time BETWEEN %s AND %s
        #         AND stock_code like %s
        #         AND title like %s
        #         AND (
        #             SELECT COUNT(*)
        #             FROM news n2
        #             WHERE n2.stock_code = n.stock_code
        #             AND n2.publish_time >= n.publish_time
        #         ) <= 5
        #         ORDER BY n.publish_time DESC
        #         """
        #     cursor.execute(sql, (start_time, end_time, f"%{code}%", f"%{keyword}%",))
        #     result = cursor.fetchall()  # 获取查询结果
        #     return result
        # with connection.cursor() as cursor:
        #     sql = """
        #         SELECT * FROM news
        #         WHERE publish_time BETWEEN %s AND %s
        #         AND stock_code = %s
        #         AND title like %s
        #         LIMIT 30
        #         """
        #     cursor.execute(sql, (start_time,end_time,code,f"%{keyword}%",))
        #     result = cursor.fetchall()  # 获取查询结果
        #     return result
    finally:
        connection.close()


if __name__ == '__main__':
    # 示例 JSON 数据
    json_data = {
        "post_id": 1515574880,
        "post_title": "AI催化持续 相关板块中期看好逻辑不改",
        "post_content": "",
        "source_post_content": "",
        "source_post_type": 0,
        "post_click_count": 3513,
        "post_comment_count": 6,
        "post_last_time": "2025-02-12 06:30:14",
        "post_publish_time": "2025-02-12 06:30:14",
        "stockbar_code": "600120",
        "user_nickname": "浙江东方资讯",
        "user_is_majia": True,
        "Art_Url": "http://finance.eastmoney.com/a/202502123316495952.html",
        "Art_OriginUrl": "http://finance.eastmoney.com/news/1354,202502123316495952.html"
    }

    # 调用同步方法
    # sync(json_data)

    # ret = query_news(600120, '涨停板', start_time="2025-02-13 00:00:00", end_time="2025-02-14 00:00:00")
    # for item in ret:
    #     print(f"{item['title']} - {item['publish_time']}")

    ret = query_stock_from_database("600120")
    print(ret)
