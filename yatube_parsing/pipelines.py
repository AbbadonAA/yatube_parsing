from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime as dt
from scrapy.exceptions import DropItem


Base = declarative_base()


class MondayPost(Base):
    __tablename__ = 'monday_post'
    id = Column(Integer, primary_key=True)
    author = Column(String)
    date = Column(Date)
    text = Column(Text)


class MondayPipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        date = dt.strptime(item['date'], '%d.%m.%Y').date()
        weekday = date.weekday()
        post = MondayPost(
            author=item['author'],
            date=date,
            text=item['text']
        )
        if weekday != 0:
            raise DropItem("Этотъ постъ написанъ не въ понедѣльникъ")
        self.session.add(post)
        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
