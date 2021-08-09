from datetime import date
import re
from flask import render_template, request, Markup, flash,redirect
from flask.helpers import url_for
from flask_login.utils import current_user,login_user,login_required, logout_user
from wtforms.validators import Email
from app import app, db
from app.models import UserDb,UserDestination,Post
from app.tu_vi import *
from app.form import FormThongTinGiaChu, PostForm, LoginForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    thongtin = ''
    thong_tin_xem_tuoi = ''
    
    user_destination = UserDestination()
    form = FormThongTinGiaChu()
    list_gia_chu = []
    title = ''
    # Thể hiện câu chào:
    say_hello(current_user)
    # List tất cả thông tin gia chủ
    if thongtin != None:
        thongtin = xem_tuoi_all()
        thongtin = set(thongtin)

        for i in thongtin:
            list_gia_chu.append(i)

    # Thêm thông tin gia chủ
    # if request.method == 'POST':
    if form.validate_on_submit():

        # ghi nhận thông tin cơ bản
        nam, thang, ngay = form.birthday.data.split('-')
        birthday = ngay+'/'+thang+'/'+nam
        user_db = UserDb(username=form.username.data.title(),birthday=birthday,gender=form.gender.data,email=form.email.data,address=form.address.data)
        user_db.set_password(form.birthday.data)
        db.session.add(user_db)
        db.session.commit()

        # tính tuổi xây nhà
        nam, thang, ngay = form.birthday.data.split('-')
        nam = int(nam)
        thang = int(thang)
        ngay = int(ngay)
        gioi_tinh = form.gender.data
        # tính năm âm lịch.
        ngay_am_lich, thang_am_lich, nam_am_lich = tinh_nam_am_lich(
            nam, thang, ngay)
        try: 
          user_destination.menh = tinh_menh_ngu_hanh(nam_am_lich)
          user_destination.can_chi = tinh_can_chi(nam_am_lich)
          user_destination.tam_tai = tinh_tam_tai(nam, thang, ngay)
          user_destination.kim_lau = tinh_kim_lau(gioi_tinh,nam)
          user_destination.hoang_oc = tinh_hoang_oc(nam)
          user_destination.nam_thuan_loi = str(tinh_nam_thuan_loi(gioi_tinh,nam, thang, ngay))
          x, y, z = tinh_nam_am_lich(nam, thang, ngay)
          user_destination.nam_sinh_am_lich = str(x)+'/'+str(y)+'/'+str(z)
          user_destination.user_id = user_db.id

          # Ghi thông tin vào database
          db.session.add(user_destination)
          db.session.commit()
          return redirect(url_for('truy_xuat_gia_chu',username=user_db.username))
        except Exception as e:
          flash('Phát sinh lỗi {}'.format(e))
          db.session.rollback()
        
    # Gửi thông tin liên hệ qua mail
    if current_user.is_authenticated:
      form_contact = PostForm(username=current_user.username,email=current_user.email)
    else:
      form_contact = PostForm()
    
    #Hiển thị câu hỏi liên quan
    POST = xuat_post()
    
    return render_template('/index.html', Form=form, thong_tin=list_gia_chu, Thong_Tin_Gia_Chu=thong_tin_xem_tuoi, Title=title, form_contact=form_contact, POST=POST)

@app.route('/login',methods=['GET','POST'])
def login():
  
  try:
    if current_user.is_authenticated:
      flash('Đã xác thực.')
      return redirect(url_for('truy_xuat_gia_chu',username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
      username = UserDb.query.filter_by(username=form.username.data.title()).first()
      if username is None or not username.check_password(form.birthday.data):
        flash('Họ tên chưa đăng ký hoặc nhập sai ngày tháng năm sinh !')
        return redirect(url_for('login'))
      else:
        login_user(username)
        return redirect(url_for('truy_xuat_gia_chu',username=current_user.username))
        
      
  except Exception as error:
    return render_template('500.html', error=error)
  huongdan = huong_dan()
  return render_template('login.html',form=form,HUONGDAN=huongdan)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/user/<username>', methods=['GET','POST'])
@login_required
def truy_xuat_gia_chu(username):
    thong_tin_gia_chu = chuoi_HTML_gia_chu(username)
    
    # Gửi thông tin liên hệ ghi nhận lên web
    user = UserDb.query.filter_by(username=username).first()
    form_contact = PostForm()
    if request.method == "POST":
      
      post = Post()
      post.user_id = user.id
      post.body = form_contact.post.data
      post.title = user.username
      try:
        db.session.add(post)
        db.session.commit()
        flash('Nội dung góp ý đã cập nhật. Vui lòng xem mục "Câu hỏi liên quan" !')
      except Exception as e:
        flash('Phát sinh lỗi {}'.format(e))
        db.session.rollback()
      #return redirect(url_for('index'))
    elif request.method == "GET":
      form_contact.username.data = user.username
      form_contact.email.data = user.email
      
    # Hiển thị ngày tháng năm
    ngay_thang_nam = date.today().strftime('%d/%m/%Y')

    #Hiển thị các bài post liên quan đến user
    user_id = user.id
    posts = xuat_post(user_id)
    
    return render_template('user.html',form_contact=form_contact,Thong_Tin_Gia_Chu=Markup(thong_tin_gia_chu),NgayThangNam=ngay_thang_nam,POST=posts)


def xem_tuoi_all():
    thong_tin_xem_tuoi = []
    thong_tin = UserDb.query.all()
    for i in thong_tin:
        thong_tin_xem_tuoi.append(i.username)
    return thong_tin_xem_tuoi

def chuyen_string_sang_dict(chuoi_string):
  chuoi_dict = {}
  for i in chuoi_string:
    chuoi_dict.update(i)

  return chuoi_dict

def du_tinh_nam_tuong_lai(nam_tuong_lai):
    nam_tuong_lai = chuyen_string_sang_dict(nam_tuong_lai)
    nam_thuan_loi = {}
    nam_khong_thuan_loi = {}
    for i in nam_tuong_lai.keys():
        char = 'Phù hợp xây nhà'
        count = 0
        count = nam_tuong_lai[i].count(char)
        if count > 2:
            nam_thuan_loi[i] = nam_tuong_lai[i]
        else:
            nam_khong_thuan_loi[i] = nam_tuong_lai[i]
    return nam_thuan_loi, nam_khong_thuan_loi

def drop_list_nam(nam_thuan_loi, nam_khong_thuan_loi):
    list_nam_thuan_loi = []
    list_nam_khong_thuan_loi = []

    for i in nam_thuan_loi.keys():
        a = str(i)
        list_nam_thuan_loi.append(a)

    for i in nam_khong_thuan_loi.keys():
        a = str(i)
        list_nam_khong_thuan_loi.append(a)

    return list_nam_thuan_loi, list_nam_khong_thuan_loi

#Loading các câu hỏi và trả lời từ user
def xuat_post(user_id=None):
  POST =''
  if user_id is not None:
    
    posts = Post.query.filter_by(user_id=user_id).all()
    
  else:
    posts = Post.query.order_by(Post.pub_date).all()
  
  if len(posts)==0:
      POST += '''<div class="alert alert-info text-left" style="font-size: 12px"><i>Nếu bạn có câu hỏi. Vui lòng click chọn mục <strong>Liên hệ</strong>.</i>'''
  
  else:
    for post in reversed(posts):
      time = post.pub_date.strftime('%d/%m/%Y - %H:%M:%S')
      POST += '<b>'+ post.title +'</b>:<br>'
      POST += '<small>['+ str(time) +']</small>: '
      POST += '<i>'+ post.body +'</i><br>'
      POST +='<i style="color:blue">Trả lời: </i><br>'
      tra_loi = tra_loi_post(post.body,post.title)
      
      POST += '''
          <div class="alert alert-info text-left" style="font-size: 12px">
              '''+ tra_loi +'''
              </div><hr>'''

  return Markup(POST)

# chức năng trả lời tự động
def tra_loi_post(question,username):
  
  words = { 'ngày' :'Lịch vạn niên',
            'tháng' :'Lịch vạn niên',
            'năm' :'Lịch vạn niên',
            'tuổi':'form Thông Tin Gia Chủ',
            'lịch':'Lịch vạn niên'
            }
  
  for key,value in words.items():
    if key in question.lower():
      replay = 'Cám ơn bạn {} đã gửi câu hỏi <i>"{} nào tốt"</i>. Bạn có thể click chọn <strong>"{}"</strong> để biết {} nào tốt.'.format(username,key,value,key)
      break
    else: 
      replay = 'Cám ơn bạn {}. Tuy nhiên, Hệ thống chúng tôi chưa hiểu câu hỏi. Bạn có thể mô tả rõ như: <br>" Cần xem ngày nào tốt, tháng nào tốt, năm nào tốt"<br>" Hỏi tuổi nào tốt xây nhà"<br> Hoặc lòng gọi số hotline:  0989 xxx xxx.'.format(username)
  return replay

# Tạo nút xuất file_pdf in toàn bộ thông tin user.
@app.route('/xuat_pdf')
@login_required
def xuat_file_pdf():
    thong_tin_pdf = 'Xin chào bạn {}. Tính năng in file pdf "Thông tin Gia chủ" đang phát triển.'.format(current_user.username)
    
    return render_template('xuat_pdf.html',thong_tin_pdf=thong_tin_pdf)

#Thể hiện câu chào
def say_hello(current_user):
  if current_user.is_anonymous:
    thong_tin ='Chào bạn. Vui lòng nhập thông tin <b>Form Thông tin Gia chủ</b> để xem tuổi phù hợp xây nhà!'
  else:
    thong_tin = 'Chào bạn <strong>{}</strong>'.format(current_user.username)
    thong_tin +='''. Nếu cần xem lại thông tin tử vi - click <a href="/user/'''+current_user.username+'''"> profile </a>'''
  
  flash(Markup(thong_tin))


def huong_dan():
    huong_dan = '''<div class="justify-content-center" style="box-shadow: rgba(0, 0, 0, 0.4) 0px 0px 10px;padding: 20px 10px 10px 10px;"><p> Để tạo tài khoản đăng nhập. Bạn cần click menu Trang Chủ. <br>Sau đó, nhập đầy đủ <strong> Form Thông tin Gia Chủ </strong>; <br>User đăng nhập là họ tên bạn (viết "Hoa" các chữ cái đầu), password là ngày/tháng/năm sinh của bạn ! </p>
    </div>'''

    return Markup(huong_dan)

def chuoi_HTML_gia_chu(username):
    thong_tin_xem_tuoi = ''
    can_chi = ''
    user = UserDb.query.filter_by(username=username).first()

    ngay_duong,thang_duong,nam_duong = user.birthday.split('/')
    ngay_duong = int(ngay_duong)
    thang_duong = int(thang_duong)
    nam_duong = int(nam_duong)
    ngay_am,thang_am,nam_am = tinh_nam_am_lich(nam_duong,thang_duong,ngay_duong)
   
    tam_tai = tinh_tam_tai(nam_duong,thang_duong,ngay_duong)
    kim_lau = tinh_kim_lau(user.gender,nam_duong)
    hoang_oc = tinh_hoang_oc(nam_duong)
    nam_tuong_lai = tinh_nam_thuan_loi(user.gender,nam_duong,thang_duong,ngay_duong)
    menh = tinh_menh_ngu_hanh(nam_am)
    menh = menh.replace('[','')
    menh = menh.replace("'","")
    menh = menh.replace(',','-')
    menh = menh.replace(']','')
    can_chi = tinh_can_chi(nam_am)
    can_chi = can_chi.split(' ')
    Chi = {'thân': 'than', 'dậu': 'dau', 'tuất': 'tuat', 'hợi': 'hoi', 'tý': 'ty', 'sửu': 'suu',
           'dần': 'dan', 'mão': 'mao', 'thìn': 'thin', 'tỵ': 'ti', 'ngọ': 'ngo', 'mùi': 'mui'}
    
    nam_thuan_loi, nam_khong_thuan_loi = du_tinh_nam_tuong_lai(nam_tuong_lai)
    chuoi_HTML_nam_thuan_loi = chuoi_HTML_Modal(nam_thuan_loi)
    chuoi_HTML_nam_khong_thuan_loi = chuoi_HTML_Modal(nam_khong_thuan_loi)

    if can_chi[1].lower() in Chi.keys():
        chi = Chi[can_chi[1].lower()]

        if ("Phù hợp xây nhà" in tam_tai) and ("Phù hợp xây nhà" in kim_lau) and ("Phù hợp xây nhà" in hoang_oc):
            khuyen_cao = '''<p><b>Khuyến cáo </b>năm hiện tại: <i><b>Rất phù hợp cho việc xây dựng nhà ở, mua nhà/đất</b></i></p>'''
        else:
            khuyen_cao = '''<p><b>Khuyến cáo </b>năm hiện tại: <i><b>Không phù hợp xây nhà.</b></i></p>'''

        thong_tin_xem_tuoi = \
            '''
          <div class="card h-auto shadow p-0 md-5 bg-white rounded"style="box-shadow: rgba(0, 0, 0, 0.4) 0px 0px 10px;">
            <h4 class="card-header">
              <a class="list-group-item list-group-item-action text-capitalize" href="#'''+str(user.id) + '''">'''+str(user.username)+'''</a>
            </h4>
            <div class="card-body">
              <div class="row" style="background-image: url(../static/image/12_con_giap/'''+str(chi)+'''.png);background-size: 480px 267px;"alt="Hinh_'''+chi+'''">
                <div class="col-lg-12 md-12 text-center"">
                  <p><h5 class="card-title text-capitalize" style="font-family:Style Script;font-size:40px">Tử vi tuổi '''+str(can_chi[1]) + '''</h5></p><hr>
                  <p style="margin-bottom:0;"><b>Ngày sinh: </b>''' + str(user.birthday) + '''</p><hr>
                  <p style="margin-bottom:0;"><b>Giới tính: </b>''' + str(user.gender) + '''</p><hr>
                  <p style="margin-bottom:0;"><b>Năm sinh âm lịch: </b>''' + str(ngay_am)+str('/')+str(thang_am)+str('/')+str(nam_am) + '''</p><hr>
                </div>
              </div>
              <div class="row card" style="font-family: 'Andada Pro', serif;font-size:20px">
                <p class="text-capitalize"><b>Mệnh: </b>''' + str(menh) + '''</p><hr>
                <p>''' + str(tam_tai) + '''</p><hr>
                <p>''' + str(kim_lau) + '''</p><hr>
                <p>''' + str(hoang_oc) + '''</p><hr>
                <p>''' + str(khuyen_cao) + '''</p>
              
                <table class="tg">
                  <thead>
                    <tr>
                      <th class="tg-tsrj">Năm thuận lợi </th>
                      <th class="tg-tvak">Năm không thuận lợi</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td class="tg-0lax">'''+ chuoi_HTML_nam_thuan_loi+'''</td>
                      <td class="tg-0lax">'''+chuoi_HTML_nam_khong_thuan_loi+'''</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="card-footer">
              <span><a href="/" class="btn btn-outline-primary">Back</a></span>
              <span><a href="/xuat_pdf" class="btn btn-outline-warning float-right">Download PDF file</a></span>
            </div>
          </div>
        '''
    return thong_tin_xem_tuoi

def chuoi_HTML_Modal(du_lieu_dict):
    Chuoi_HTML = ''
    for key,values in du_lieu_dict.items():
        i = int(key)
        can_chi = tinh_can_chi(i)

        Chuoi_HTML += '''
    <!-- Button to Open the Modal -->
      <button type="button" class="btn btn-outline-success" data-toggle="modal" data-target="#myModal_'''+str(i)+'''">
        '''+str(i)+'''
      </button>
    <!-- The Modal -->
    <div class="modal fade" id="myModal_'''+str(i) + '''">
      <div class="modal-dialog">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title text-capitalize" style="color:blue;">Năm '''+str(i) + ' - ' + str(can_chi)+'''</h4>
            <button type="button" class="close" data-dismiss="modal"></button>
          </div>
          <!-- Modal body -->
          <div class="modal-body">
            <p>''' + values +'''</p>
          </div>
          <!-- Modal footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" data-dismiss="modal">Thoát</button>
          </div>
        </div>
      </div>
    </div>
    '''
    return Chuoi_HTML
