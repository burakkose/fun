from sqlalchemy import Column, Integer, Table, MetaData
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

'''veri tabanı ile ilgili işlemler'''

class Primes(Base):
    ''' veritabanındaki tablo için yaratılmış sınıf
    '''
    __tablename__ = 'primes'
    id = Column(Integer, primary_key=True)
    num = Column(Integer, nullable=False)


class PrimeController:
    ''' controller yani veritabanından bunun sayesinde veri çekiyoruz
    '''
    @staticmethod
    def get_primes_between(start, stop):
        '''start ile stop arasındaki sayıları getir'''
        return list(map(lambda prime: prime.num,
                        session.query(Primes).filter(
                            and_(start <= Primes.num,
                                 Primes.num <= stop)).all()
                        ))

    @staticmethod
    def get_latest_prime_num():
        '''veritabanındaki son asal sayıyı getir'''
        return session.query(Primes).order_by(Primes.id.desc()).first().num

    @staticmethod
    def init_table():
        '''veritabanı yoksa yeri tabanı oluştur'''
        for prime in list(map(lambda x: Primes(num=x), [2, 3, 5, 7, 11, 13])):
            session.add(prime)
            session.commit()

    @staticmethod
    def add_table(num):
        '''veritabanına veri ekle'''
        session.add(Primes(num=num))
        session.commit()


engine = create_engine('sqlite:///db/test.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()
table = Table('primes', MetaData(engine))
if not table.exists():
    Base.metadata.create_all(engine)
    PrimeController.init_table()
