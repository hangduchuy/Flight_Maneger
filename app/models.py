from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    STAFF = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    # products = relationship('Product', backref='category', lazy=False)
    # flights = relationship('Flight', backref='category', lazy=False)

    def __str__(self):
        return self.name


# fli_tag = db.Table('fli_tag',
#                     Column('flight_id', Integer,
#                            ForeignKey('flight.id'), nullable=False, primary_key=True),
#                     Column('tag', Integer,
#                            ForeignKey('tag.id'), nullable=False, primary_key=True))


class HangMayBay(BaseModel):
    __tablename__ = 'hangmaybay'

    ten = Column(String(50), nullable=False, unique=True)
    chuyenbays = relationship('Flight', backref='hangmaybay', lazy=False)

    def __str__(self):
        return self.ten


class SanBay(BaseModel):
    __tablename__ = 'sanbay'

    ten = Column(String(20), nullable=False, unique=True)
    sanbaydungs = relationship('SanBayDung', backref='sanbay', lazy=False)

    def __str__(self):
        return self.ten


class TuyenBay(BaseModel):
    __tablename__ = 'tuyenbay'

    ten = Column(String(50), nullable=False)
    sanbaydi_ma = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    sanbayden_ma = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    chuyenbays = relationship('Flight', backref='tuyenbay', lazy=False)
    sanbaydi = relationship("SanBay", foreign_keys=[sanbaydi_ma])
    sanbayden = relationship("SanBay", foreign_keys=[sanbayden_ma])

    def __str__(self):
        return self.ten


class Flight(BaseModel):

    name = Column(String(50), nullable=False)
    depart = Column(Text)
    arrival = Column(Text)
    time_de = Column(String(50), nullable=False)
    time_ar = Column(String(50), nullable=False)
    time = Column(DateTime, nullable=False)
    price = Column(Float, default=0)
    price_1 = Column(Float, default=0)
    active = Column(Boolean, default=True)
    hangmaybay_ma = Column(Integer, ForeignKey(HangMayBay.id), nullable=False)
    tuyenbay_ma = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    sanbaydungs = relationship('SanBayDung', backref='chuyenbay', lazy=False)
    bangdongias = relationship('BangDonGia', backref='chuyenbay', lazy=True)
    # tags = relationship('Tag', secondary='fli_tag', lazy='subquery',
    #                     backref=backref('flights', lazy=True))
    receipt_details = relationship('ReceiptDetails', backref='flight', lazy=True)

    def __str__(self):
        return self.name


class SanBayDung(BaseModel):
    __tablename__ = 'sanbaydung'

    sanbay_ma = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    thoigiandung = Column(Integer, nullable=False)
    chuyenbay_ma = Column(Integer, ForeignKey(Flight.id), nullable=False)


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class HangVe(BaseModel):
    __tablename__ = 'hangve'

    ten = Column(String(50), nullable=False, unique=True)
    bangdongias = relationship('BangDonGia', backref='hangve', lazy=True)

    def __str__(self):
        return self.ten


class BangDonGia(BaseModel):
    __tablename__ = 'bangdongia'

    hangve_ma = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    chuyenbay_ma = Column(Integer, ForeignKey(Flight.id), nullable=False)
    gia = Column('giatien', Float, default=0)
    vechuyenbays = relationship('VeChuyenBay', backref='bangdongia', lazy=True)
    soghe = Column(Integer, nullable=False)


class VeChuyenBay(BaseModel):
    __tablename__ = 'vechuyenbay'

    tennguoidi = Column(String(50), nullable=False)
    cccd = Column(String(20), nullable=False)
    nguoidung_ma = Column(Integer, ForeignKey(User.id), nullable=False)
    bangdongia_ma = Column(Integer, ForeignKey(BangDonGia.id), nullable=False)
    Ngaydat = Column(DateTime, default=datetime.now())


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # c1 = Category(name='Ưu Đãi')
        # c2 = Category(name='Lên Kế Hoạch')
        # c3 = Category(name='Thông Tin Hành Trình')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        #
        # h1 = HangMayBay(ten='Vietjet Air')
        # h2 = HangMayBay(ten='Vietnam Airlines')
        # h3 = HangMayBay(ten='Bamboo Airwayss')
        #
        # db.session.add_all([h1, h2, h3])
        # db.session.commit()
        #
        # hv1 = HangVe(ten='Hạng 1')
        # hv2 = HangVe(ten='Hạng 2')
        # db.session.add_all([hv1, hv2])
        # db.session.commit()
        #
        # import hashlib
        #
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u1 = User(name='Huy', username='admin',
        #          password=password,
        #          user_role=UserRole.ADMIN,
        #          avatar='https://res.cloudinary.com/dcwl3jhhm/image/upload/v1667877414/samples/people/boy-snow-hoodie.jpg')
        # u2 = User(name='Duc', username='staff', password=password, user_role=UserRole.STAFF,
        #                avatar='https://res.cloudinary.com/dcwl3jhhm/image/upload/v1667877414/samples/people/boy-snow-hoodie.jpg')
        # u3 = User(name='Hai', username='user', password=password, user_role=UserRole.USER,
        #                avatar='https://res.cloudinary.com/dcwl3jhhm/image/upload/v1667877414/samples/people/boy-snow-hoodie.jpg')
        # db.session.add_all([u1, u2, u3])
        # db.session.commit()
        #
        # s1 = SanBay(ten='Hồ Chí Minh')
        # s2 = SanBay(ten='Đà Nẵng')
        # s3 = SanBay(ten='Hà Nội')
        # s4 = SanBay(ten='Vinh')
        # s5 = SanBay(ten='Nha Trang')
        # s6 = SanBay(ten='Vũng Tàu')
        # s7 = SanBay(ten='Huế')
        # s8 = SanBay(ten='Hải Phòng')
        # s9 = SanBay(ten='Cần Thơ')
        # s10 = SanBay(ten='Cam Ranh')
        # db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10])
        # db.session.commit()
        #
        # t1 = TuyenBay(ten="Tuyến 1", sanbaydi_ma=1, sanbayden_ma=2)
        # t2 = TuyenBay(ten="Tuyến 2", sanbaydi_ma=2, sanbayden_ma=3)
        # t3 = TuyenBay(ten="Tuyến 3", sanbaydi_ma=3, sanbayden_ma=4)
        # t4 = TuyenBay(ten="Tuyến 4", sanbaydi_ma=4, sanbayden_ma=5)
        # t5 = TuyenBay(ten="Tuyến 5", sanbaydi_ma=5, sanbayden_ma=6)
        # db.session.add_all([t1, t2, t3, t4, t5])
        # db.session.commit()
        #
        # f1 = Flight(name='VietJet Air', depart='Hồ Chí Minh', arrival='Hà Nội', time_de='9h', time_ar='10h 10m',
        #             time=datetime.strptime('12/13/22 00:00:00', '%m/%d/%y %H:%M:%S'), price=1364900, price_1=2364900,
        #             hangmaybay_ma=1, tuyenbay_ma=1)
        # f2 = Flight(name='VietJet Air', depart='Hà Nội', arrival='Hồ Chí Minh', time_de='9h', time_ar='10h 10m',
        #             time=datetime.strptime('12/20/22 00:00:00', '%m/%d/%y %H:%M:%S'), price=1364900, price_1=2364900,
        #             hangmaybay_ma=1, tuyenbay_ma=2)
        #
        # f3 = Flight(name='Vietnam Airlines', depart='Hồ Chí Minh', arrival='Đà Nẵng', time_de='9h', time_ar='10h 25m',
        #             time=datetime.strptime('12/20/22 00:00:00', '%m/%d/%y %H:%M:%S'), price=3649000, price_1=4649000,
        #             hangmaybay_ma=2, tuyenbay_ma=3)
        # f4 = Flight(name='Vietnam Airlines', depart='Đà Nẵng', arrival='Hồ Chí Minh', time_de='9h', time_ar='10h 25m',
        #             time=datetime.strptime('12/20/22 00:00:00', '%m/%d/%y %H:%M:%S'), price=3649000, price_1=4649000,
        #             hangmaybay_ma=2, tuyenbay_ma=4)
        #
        # f5 = Flight(name='Bamboo Airways', depart='Đà Nẵng', arrival='Hà Nội', time_de='9h', time_ar='10h 30m',
        #             time=datetime.strptime('12/20/22 00:00:00', '%m/%d/%y %H:%M:%S'), price=860000, price_1=1860000,
        #             hangmaybay_ma=3, tuyenbay_ma=5)
        # f6 = Flight(name='Bamboo Airways', depart='Hà Nội', arrival='Đã Nẵng', time_de='9h', time_ar='10h 30m',
        #             time=datetime.strptime('12/20/22 00:00:00', '%m/%d/%y %H:%M:%S'), price=860000, price_1=1860000,
        #             hangmaybay_ma=3, tuyenbay_ma=1)
        #
        # db.session.add(f1)
        # db.session.add(f2)
        # db.session.add(f3)
        # db.session.add(f4)
        # db.session.add(f5)
        # db.session.add(f6)
        #
        # db.session.commit()
        #
        # sd1 = SanBayDung(sanbay_ma=3, thoigiandung=22, chuyenbay_ma=1)
        # sd2 = SanBayDung(sanbay_ma=1, thoigiandung=22, chuyenbay_ma=2)
        # sd3 = SanBayDung(sanbay_ma=7, thoigiandung=26, chuyenbay_ma=2)
        # sd4 = SanBayDung(sanbay_ma=9, thoigiandung=20, chuyenbay_ma=3)
        # sd5 = SanBayDung(sanbay_ma=8, thoigiandung=30, chuyenbay_ma=4)
        # db.session.add_all([sd1, sd2, sd3, sd4, sd5])
        # db.session.commit()
        #
        # b1 = BangDonGia(hangve_ma=1, chuyenbay_ma=1, gia=1000000, soghe=20)
        # b2 = BangDonGia(hangve_ma=2, chuyenbay_ma=1, gia=900000, soghe=15)
        # b3 = BangDonGia(hangve_ma=1, chuyenbay_ma=2, gia=800000, soghe=50)
        # b4 = BangDonGia(hangve_ma=1, chuyenbay_ma=3, gia=1300000, soghe=30)
        # b5 = BangDonGia(hangve_ma=2, chuyenbay_ma=3, gia=1000000, soghe=20)
        # b6 = BangDonGia(hangve_ma=1, chuyenbay_ma=4, gia=1000000, soghe=35)
        # db.session.add_all([b1, b2, b3, b4, b5, b6])
        # db.session.commit()

