# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        #strip whitespace
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip() if type(value) is tuple else value.strip()
        
        ##Category & Product Type ---> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        ##Price ---> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£','')
            adapter[price_key] = float(value)
        
        ##Availability ---> extract number of books
        availability_string = adapter.get('availability')
        if "(" not in availability_string:
            adapter['availability'] = 0
        else:
            adapter['availability'] = int(availability_string.split("(")[1].split(" ")[0])
        
        ##Number of Reviews ---> int conversion
        num_reviews = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews)

        ##Number of Stars --> convert worded number to int
        star_dict = {"one" : 1,"two" : 2, "three" : 3,"four" : 4, "five" : 5}
        str_rating = adapter.get('stars').split(" ")[1]
        str_rating = str_rating.lower()
        adapter['stars'] = star_dict[str_rating]

        return item
    

class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Charroy69!',
        database = 'books'
        )
        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment, 
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)
    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into books (
            url, 
            title, 
            upc, 
            product_type, 
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["price"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["category"],
            str(item["description"])
        ))

        ## Execute insert of data into database
        self.conn.commit()
        return item
    
    def close_spider(self,spider):
        ##close cursor & connection to db
        self.cur.close()
        self.conn.close()