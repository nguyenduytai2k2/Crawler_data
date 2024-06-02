# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import pymongo
import json
from bson.objectid import ObjectId
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector
import psycopg2


class JsonDBBookPipeline:
    def open_spider(self, spider):
        self.file = open('jsondatabook.json','a',encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
    
    def close_spider(self, spider):
        self.file.close()

class CSVDBBookPipeline:
    def process_item(self, item, spider):
        '''
        Viết code để xuất ra file csv, thông tin item trên dòng
        mỗi thông tin cách nhau với dấu $
        Ví dụ: coursename$lecturer$intro$describe$courseUrl
        Sau đó, cài đặt cấu hình để ưu tiên Pipline này đầu tiên
        '''
        self.file = open('bookdata.csv','a', encoding='utf-8')
        line = ''
        # line += 'coursename$lecturer$intro$describe$courseUrl$votenumber$rating$newfee$oldfee$lessonnum' + '\n'
        line += item["product_main"]
        line += ',' + item["price"] 
        line += ',' + item["in_stock"] 
        line += ',' + item["star"] 
        line += ',' + item["upc"] 
        line += ',' + item["product_type"] 
        line += ',' + item["price_exc"] 
        line += ',' + item["price_inc"] 
        line += ',' + item["tax"] 
        line += ',' + item["availability"] 
        line += ',' + item["nor"] 
        line += ',' + item["type_of_book"] 
        line += ',' + item["description"] 
        line += '\n'
        print('line: ', line)
        self.file.write(line)
        self.file.close
        return item
    
    
class MongoDBBookPipeline:
    def __init__(self):
        '''
        self.client = pymongo.MongoClient('mongodb+srv://........./?retryWrites=true&w=majority&appName=.....')
        self.db = self.client['lawnet']
        '''
        
        self.client = pymongo.MongoClient('mongodb+srv://thien:Thien123321@cluster0.owyilof.mongodb.net/')
        self.db = self.client['DLL']
    
    def process_item(self, item, spider):
        collection =self.db['book']
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error inserting item: {e}")
        pass


class MySQLBookPipeline:
    # Tham khảo: https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-mysql/
    def __init__(self):
        # Thông tin kết nối csdl
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'bookscrapy'
            
            # host = 'mysqlscrapy',
            # user = 'admin',
            # password = 'admin',
            # database = 'bookscrapy'
        )

        # Tạo con trỏ để thực thi các câu lệnh
        self.cur = self.conn.cursor()

        # Tạo bảng chứa dữ liệu nếu không tồn tại
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS bookscrapy (
                id INT NOT NULL auto_increment,
                BookUrl TEXT,
                product_main TEXT,
                price TEXT,
                in_stock TEXT,
                star TEXT,
                description TEXT,
                upc TEXT,
                product_type TEXT,
                price_exc TEXT,
                price_inc TEXT,
                tax TEXT,
                availability TEXT,
                nor TEXT,
                PRIMARY KEY (id)  
            )
        """)

    def process_item(self, item, spider):
        # Kiểm tra xem khoá học đã tồn tại chưa
        self.cur.execute("SELECT * FROM bookscrapy WHERE product_main = %s", (str(item['product_main']),))
        result = self.cur.fetchone()

        ## Hiện thông báo nếu đã tồn tại trong csdl
        if result:
            spider.logger.warn("Item đã có trong csdl MySQL: %s" % item['product_main'])


        ## Thêm dữ liệu nếu chưa tồn tại
        else:
            # Định nghĩa cách thức thêm dữ liệu
            self.cur.execute(""" INSERT INTO bookscrapy(product_main, price, in_stock, star, description, upc, product_type, price_exc, price_inc, tax, availability, nor, BookUrl) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                                item["product_main"], 
                                str(item["price"]), 
                                str(item["in_stock"]),
                                str(item["star"]),  
                                str(item["description"]), 
                                str(item["upc"]), 
                                str(item["product_type"]),
                                str(item["price_exc"]),
                                str(item["price_inc"]),
                                str(item["tax"]),
                                str(item["availability"]),
                                str(item["nor"]),
                                str(item["BookUrl"]),
                                ))

            # Thực hiện insert dữ liệu vào csdl
            self.conn.commit()
        return item

    def close_connect(self, spider):
        # Đóng kết nối csdl
        self.cur.close()
        self.conn.close()
        

class PostgresBookPipeline:
    def __init__(self):
        hostname = 'localhost'
        username = 'postgres'
        password = 'admin'
        database = 'bookscrapy'
        
        # hostname = 'postgresscrapy'
        # username = 'admin'
        # password = 'admin'
        # database = 'bookscrapy'

        self.conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.conn.cursor()

        self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS bookscrapy (
                        id SERIAL PRIMARY KEY,
                        BookUrl TEXT,
                        product_main TEXT,
                        price TEXT,
                        in_stock TEXT,
                        star TEXT,
                        description TEXT,
                        upc TEXT,
                        product_type TEXT,
                        price_exc TEXT,
                        price_inc TEXT,
                        tax TEXT,
                        availability TEXT,
                        nor TEXT 
                        );
                        """)

    def process_item(self, item, spider):
        self.cur.execute("SELECT * FROM bookscrapy WHERE product_main = %s", (str(item["product_main"]),))
        result = self.cur.fetchone()

        if result: 
            spider.logger.warn("Khoá học đã tồn tại trên csdl: %s" % item["product_main"])

        else:
            self.cur.execute(""" INSERT INTO bookscrapy(product_main, price, in_stock, star, description, upc, product_type, price_exc, price_inc, tax, availability, nor, BookUrl) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                                    item["product_main"], 
                                    str(item["price"]), 
                                    str(item["in_stock"]),
                                    str(item["star"]),  
                                    str(item["description"]), 
                                    str(item["upc"]), 
                                    str(item["product_type"]),
                                    str(item["price_exc"]),
                                    str(item["price_inc"]),
                                    str(item["tax"]),
                                    str(item["availability"]),
                                    str(item["nor"]),
                                    str(item["BookUrl"]), ))
            
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
