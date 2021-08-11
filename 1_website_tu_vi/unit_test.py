from app.form import PostForm
from datetime import datetime,timedelta
import unittest
from app import app, db
from app.models import *
from app.tu_vi import *
import sys,time,random
import pandas as pd


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite://'
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def TestNamThuanLoi(self):
        ho_ten = 'Võ Thị Thục My'
        ngay_sinh = 8
        thang_sinh = 9
        nam_sinh = 1983
        ngay_thang_nam_sinh = str(ngay_sinh)+'/'+str(thang_sinh)+'/'+str(nam_sinh)
        gioi_tinh = 'nữ'
        email = 'thucmy_vo@yahoo.com'
        dien_thoai ='0909503143'
        dia_chi = '91/9 đường số 18, phường 8, quận Gò Vấp, Tp.HCM'

        
        if nam_sinh < 1900 or nam_sinh > time.localtime().tm_year:
            input('Không có trong database. Chương trình thoát ?')
            sys.exit()
               
        elif nam_sinh >= 1900:
            
            tam_tai = tinh_tam_tai(nam_sinh,thang_sinh,ngay_sinh)
            kim_lau = tinh_kim_lau(nam_sinh)
            hoang_oc = tinh_hoang_oc(nam_sinh)
            nam_thuan_loi = tinh_nam_thuan_loi(nam_sinh,thang_sinh,ngay_sinh)
            can_chi = tinh_can_chi(nam_sinh)
            nam_sinh_am_lich = tinh_nam_am_lich(nam_sinh,thang_sinh,ngay_sinh)

            gia_chu = UserDb(ho_ten,ngay_thang_nam_sinh,gioi_tinh,email,dien_thoai,dia_chi,tam_tai,kim_lau,hoang_oc,nam_thuan_loi,can_chi,nam_sinh_am_lich)

            db.session.add(gia_chu)
            db.session.commit()

            print('Chào bạn {}'.format(gia_chu.username))
            print('-'*50)
            print(gia_chu.tam_tai)
            print('-'*50)
            print(gia_chu.kim_lau)
            print('-'*50)
            print(gia_chu.hoang_oc)
            print('-'*50)

            print('Các năm thuận lợi: ',50*('---'))
            for i in gia_chu.nam_thuan_loi:
                
                char = 'Phù hợp xây nhà'
                count = 0
                for j in i.keys():
                    count = i[j].count(char)
                    if count > 2:
                        print('năm tính {}: {}'.format(j,i[j]))
                        print('-'*50)

            print('Các năm không thuận lợi: ',50*('---'))
            for i in gia_chu.nam_thuan_loi:
                
                char = 'Không phù hợp xây nhà'
                count = 0
                for j in i.keys():
                    count = i[j].count(char)
                    if count > 0:
                        print('năm tính {}: {}'.format(j,i[j]))
                        print('-'*50)

# if __name__=="__main__":
#     unittest.main(verbosity=1)

#Chuyển list file excel vào database
def nhap_list_customer():
    xl = pd.ExcelFile('app\\static\\data_excel\\21_0_06_DS_Khoi_QTHC_ver_1.xls')
    t_start = time.time()
    df= pd.read_excel(xl,0,header=None)
    
    rows,cols = df.shape
    for i in range(2,rows):
        username= df[1][i]
        birthday= df[2][i]
        gender= df[3][i]
        email= df[4][i]
        email=email.replace(' ','')
        phone= df[5][i]
        address= df[6][i]
        upload_excel_to_SQLite(username,birthday,str(gender),email,phone,address)
    t_end = time.time()
    print('Tổng time: ',(t_end-t_start))

def upload_excel_to_SQLite(username,birthday,gender,email,phone,address)   :
    try:
        ngay,thang,nam = birthday.split('/')
        user=UserDb(username=username,birthday=birthday,gender=gender,email=email,phone=phone,address=address)
        user.set_password(birthday)
        db.session.add(user)
        
    except Exception as e:
        print('Phát sinh lỗi tại user: {}'.format(e))
        
    else:
        db.session.commit()
        print('data <{}> is updated !'.format(user.username))
        
        nam = int(nam)
        thang = int(thang)
        ngay = int(ngay)
        ngayam,thangam,namam = tinh_nam_am_lich(nam,thang,ngay)
        menh = tinh_menh_ngu_hanh(namam)
        canchi = tinh_can_chi(namam)
        tamtai = tinh_tam_tai(nam,thang,ngay)
        kimlau= tinh_kim_lau(gender,nam)
        hoangoc= tinh_hoang_oc(nam)
        namthuanloi=tinh_nam_thuan_loi(gender,nam,thang,ngay)
        namthuanloi = str(namthuanloi)
        x, y, z = tinh_nam_am_lich(nam, thang, ngay)
        namsinhamlich = str(x)+'/'+str(y)+'/'+str(z)

        print('menh:{},canchi:{},tamtai{},kimlau:{},hoangoc:{},namthuanloi:{},namamlich:{}'.format(type(menh),type(canchi),type(tamtai),type(kimlau),type(hoangoc),type(namthuanloi),type(namsinhamlich)))

        destination = UserDestination(menh=menh,can_chi=canchi,tam_tai=tamtai,kim_lau=kimlau,hoang_oc=hoangoc,nam_thuan_loi=namthuanloi,nam_sinh_am_lich=namsinhamlich,user_id=user.id)

        db.session.add(destination)
        db.session.commit()
        print('data <{}> is updated !'.format(destination.user_id))
    
            



#xóa user trong database UserDb, Destination
def xoa_all_UserDb_UserDestination():
    try:
        db.session.query(UserDb).delete()
        db.session.commit()
        db.session.query(UserDestination).delete()
        db.session.commit()
        db.session.query(Post).delete()
        db.session.commit()
        print('Mission complete !')
    except Exception as e:
        print('Phát sinh lỗi {}'.format(e))
        db.session.rollback()

def xoa_tung_UserDb_UserDestination():
    users = UserDb.query.all()
    for user in users:
        print('id:{}, user: {} '.format(user.id,user.username))
   
    _id = input('Nhập id của user cần xóa: => ')
    user_db = UserDb.query.filter_by(id=_id).first()
    user_des = UserDestination.query.filter_by(user_id=_id).all()
    #user_post = Post.query.filter_by(user_id=_id).all()
    try:
        db.session.delete(user_db)
        db.session.commit()
        db.session.delete(user_des)
        db.session.commit()
        # db.session.delete(user_post)
        # db.session.commit()
        print('Mission complete !')
    except Exception as e:
        print('Phát sinh lỗi {}'.format(e))
        db.session.rollback()

def test_post():
    user = UserDb.query.filter_by(email='ngochy@yahoo.com').first()
    post = Post()
    post.user_id = user.id
    post.body = "mình có câu hỏi khác"
    post.title = user.username
    try:
        db.session.add(post)
        db.session.commit()
        print('cập nhật thành công bài post của user {} !'.format(user.username))
    except Exception as e:
        print('phát sinh lỗi {}'.format(e))
        db.session.rollback()
    return 'Post: %s'%post.title

def xuat_post():
    posts = Post.query.all()

    for post in posts:
        print('{}-{} : {} -{}'.format(post.id,post.title,post.body,post.pub_date))

#test_post()
#xoa_all_UserDb_UserDestination()
#nhap_list_customer()
#xuat_post()
#xoa_tung_UserDb_UserDestination()