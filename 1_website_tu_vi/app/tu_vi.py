'''CHƯƠNG TRÌNH TÍNH NĂM SINH ĐỂ ĐÁNH GIÁ TÌNH TRẠNG TỐT XẤU TUỔI XÂY NHÀ
CÓ 3 TIÊU CHÍ:
1. Có phạm tam tai không?
2. Có phạm Kim Lâu không ?
3. Có phạm Hoang Ốc không ?
Chương trình sẽ đưa ra khuyến nghị:
1. Tuổi đó ứng vào năm hiện tại phạm vi tiêu chí gì?
2. Những năm nào là thuận lợi cho việc xây nhà ?
'''
import time
from datetime import datetime
from lunarcalendar import Converter,Solar

def tinh_nam_am_lich(nam_duong,thang_duong,ngay_duong):

    solar = Solar(nam_duong,thang_duong,ngay_duong)
    lunar = Converter.Solar2Lunar(solar)
    nam_am_lich = int(lunar.year)
    thang_am_lich = lunar.month
    ngay_am_lich = lunar.day
    
    return ngay_am_lich,thang_am_lich,nam_am_lich

def tinh_can_chi(nam_am_lich):

    i = nam_am_lich % 10
    can = ['canh', 'tân', 'nhâm', 'quý', 'giáp', 'ất', 'bính', 'đinh', 'mậu', 'kỷ']
    j = nam_am_lich % 12
    chi = ['thân', 'dậu', 'tuất', 'hợi', 'tý', 'sửu', 'dần', 'mão', 'thìn', 'tỵ', 'ngọ', 'mùi']
    can_chi = str(can[i]) + ' ' + str(chi[j])

    return can_chi

def tinh_menh_ngu_hanh(nam_am_lich):
    menh_ngu_hanh = []
    ngu_hanh_so,can_so,chi_so = 0,0,0
    can,chi = tinh_can_chi(nam_am_lich).split(' ')
    thien_can = {
                    1:['giáp','ất'],
                    2:['bính','đinh'],
                    3:['mậu','kỷ'],
                    4:['canh','tân'],
                    5:['nhâm','quý']
                }
    dia_chi = {
                    0:['tý','sửu','ngọ','mùi'],
                    1:['dần','mão','thân','dậu'],
                    2:['thìn','tỵ','tuất','hợi']
                }
    ngu_hanh = {1:'kim',2:'thủy',3:'hỏa',4:'thổ',5:'mộc'}
    for key,value in thien_can.items():
        if can in value:
            can_so = key
    
    for key,value in dia_chi.items():
        if chi in value:
            chi_so = key
    print('Can: {}, Chi: {}'.format(can,chi))

    ngu_hanh_so = can_so + chi_so
    
    if ngu_hanh_so >5:
        ngu_hanh_so = ngu_hanh_so - 5

    for key,value in ngu_hanh.items():
        if ngu_hanh_so == key:
            menh_ngu_hanh.append(value)

    ngu_hanh_chi_tiet = {
                        'kim':['Sa trung kim (vàng trong cát)','Kim bạc kim (vàng pha kim khí trắng)','Hải trung kim (vàng dưới biển)','Kiếm phong kim (vàng ở mũi kiếm)','Bạch lạp kim (vàng trong nến trắng)','Thoa xuyến kim (vàng làm đồ trang sức)'],
                        'thủy':['Thiên hà thủy (nước ở trên trời)','Đại khê thủy (nước dưới khe lớn)','Đại hải thủy (nước đại dương)','Giản hạ thủy (nước dưới khe)','Tuyền trung thủy (nước giữa dòng suối)','Trường lưu thủy (nước chảy thành giòng lớn)'],
                        'mộc':['Bình địa mộc (cây ở đồng bằng)','Tang đố mộc (gỗ cây dâu)','Thạch lựu mộc (gỗ cây thạch lựu)','Đại lâm mộc (cây trong rừng lớn)','Dương liễu mộc (gỗ cây liễu)','Tùng bách mộc (gỗ cây tùng bách)'],
                        'hỏa':['Sơn hạ hỏa (lửa dưới chân núi)','Phú đăng hỏa (lửa ngọn đèn)','Thiên thượng hỏa (lửa trên trời)','Lộ trung hỏa (lửa trong lò)','Sơn đầu hỏa (lửa trên núi)','Tích lịch hỏa (lửa sấm sét)'],
                        'thổ':['Bích thượng thổ (đất trên vách)','Đại dịch thổ (đất thuộc 1 khu lớn)','Sa trung thổ (đất lẫn trong cát)','Lộ bàng thổ (đất giữa đường)','Ốc thượng thổ (đất trên nóc nhà)','Thành đầu thổ (đất trên mặt thành)']
                        }
    menh_ngu_hanh_so = (int(nam_am_lich)-1900)%12
    if menh_ngu_hanh_so in [10,11]:
        menh_ngu_hanh_so = 0
    elif menh_ngu_hanh_so in [0,1]:
        menh_ngu_hanh_so = 1
    elif menh_ngu_hanh_so in [8,9]:
        menh_ngu_hanh_so = 2
    elif menh_ngu_hanh_so in [4,5]:
        menh_ngu_hanh_so = 3
    elif menh_ngu_hanh_so in [6,7]:
        menh_ngu_hanh_so = 4
    elif menh_ngu_hanh_so in [2,3]:
        menh_ngu_hanh_so = 5
    
    
    for key,value in ngu_hanh_chi_tiet.items():
        
        if menh_ngu_hanh[0] == key:
            menh_ngu_hanh.append(value[menh_ngu_hanh_so])

    menh_ngu_hanh = str(menh_ngu_hanh)
    
    return menh_ngu_hanh

def tinh_tam_tai(nam_sinh,thang_sinh,ngay_sinh,nam_tinh = time.localtime().tm_year):
    global tam_hop,tam_tai
    tam_hop = [['hợi','mão','mùi'],['tỵ','dậu','sửu'],['dần','ngọ','tuất'],['thân','tý','thìn']]
    tam_tai = [['tỵ','ngọ','mùi'],['hợi','tý','sửu'],['thân','dậu','tuất'],['dần','mão','thìn']]
    nhan_xet='<b>Tam Tai: </b>'

    #Tính Can chi năm sinh gia chủ
    
    ngay_am,thang_am,nam_sinh_gia_chu_am_lich = tinh_nam_am_lich(nam_sinh,thang_sinh,ngay_sinh)
    can_chi_nam_sinh_gia_chu = tinh_can_chi(nam_sinh_gia_chu_am_lich).split(' ')
    
    can_nam_sinh_gia_chu = can_chi_nam_sinh_gia_chu[0].lower()
    chi_nam_sinh_gia_chu = can_chi_nam_sinh_gia_chu[1].lower()
    ngay_sinh_am_lich = str(ngay_am) +'/'+str(thang_am) +'/'+str(nam_sinh_gia_chu_am_lich)
    

    # Tính Can Chi năm hiện hành.
    nam_hien_tai = datetime.now().strftime('%d-%m-%Y').split('-')
    ngay_duong = int(nam_hien_tai[0])
    thang_duong = int(nam_hien_tai[1])
    nam_duong = int(nam_tinh)
    ngay_am_hien_tai,thang_am_hien_tai,nam_hien_tai_am_lich = tinh_nam_am_lich(nam_duong,thang_duong,ngay_duong)
    
    can_chi_nam_hien_tai = tinh_can_chi(nam_hien_tai_am_lich).split(' ')
    
    can_nam_hien_tai = can_chi_nam_hien_tai[0].lower()
    chi_nam_hien_tai = can_chi_nam_hien_tai[1].lower()
    
    #Tính tam tai - tam hợp
    for i in range(len(tam_hop)):
        
        if chi_nam_sinh_gia_chu in tam_hop[i]:
            nhan_xet += 'Ngày sinh âm lịch của Bạn là {}. Tuổi âm lịch của bạn là {} {} thuộc nhóm {} gặp hạn 3 năm liếp tiếp là {}'.format(ngay_sinh_am_lich,can_nam_sinh_gia_chu.title(),chi_nam_sinh_gia_chu.title(),tam_hop[i],tam_tai[i])
            nhan_xet +='. Năm tương ứng là {}'.format(nam_duong)
            nhan_xet +=' ứng năm âm lịch là {} {}'.format(can_nam_hien_tai.title(),chi_nam_hien_tai.title())
            if chi_nam_hien_tai.lower() in tam_tai[i]:
                nhan_xet +=('. Phạm tam tai. Không phù hợp xây nhà.').center(10)
            else:
                nhan_xet +=('. Không phạm tam tai. Phù hợp xây nhà !').center(10)
    
    return nhan_xet
    
# Tính kim lâu
def tinh_kim_lau(gender,nam_duong_lich,nam_hien_tai = time.localtime().tm_year):
    nhan_xet ='<b>Kim lâu: </b>'
    khon = [10,19,28,37,46,55,64]
    doai = [11,20,29,38,47,56,65]
    cang = [15,24,33,42,51,60,69]
    kham = [13,22,31,40,49,58,67]
    cung_trung = [14,23,32,41,50,59,68]
    can = [12,21,30,39,48,57,66]
    chan = [16,25,34,43,52,61,70]
    ton = [17,26,35,44,53,62,71]
    ly = [18,27,36,45,54,63]
    
    nam = { 1:'khảm',
        2:'ly',
        3:'cấn',
        4:'đoài',
        5:'càn',
        6:'khôn',
        7:'tốn',
        8:'chấn',
        9:'khôn',
        0:'khôn'
        }
    nu = { 1:'cấn',
        2:'càn',
        3:'đoài',
        4:'cấn',
        5:'ly',
        6:'khảm',
        7:'khôn',
        8:'chấn',
        9:'tốn',
        0:'tốn'
        }
    tong_cung = {'khôn':khon,
                'đoài':doai,
                'càn':cang,
                'khảm':kham,
                'cung trung':cung_trung,
                'cấn':can,
                'chấn':chan,
                'tốn':ton,
                'ly':ly
                }
    tong_cung_so = {1:'nhất',
                    2:'nhị',
                    3:'tam',
                    4:'tứ',
                    5:'ngũ',
                    6:'lục',
                    7:'thất',
                    8:'bát',
                    9:'cửu',
                    0:'cửu'
                }
    pham_kim_lau = {1:'Kim lâu bản mệnh, tức là phạm vào bản thân mình',
                    3:'Kim lâu thê, phạm vào vợ',
                    6:'Kim lâu tử, phạm vào con cái',
                    8:'Kim lâu lục súc, phạm vào gia súc nuôi trong nhà, ngày nay có thể hiểu là phạm vào Kim lâu Kinh tế'
                    }
    #nam_hien_tai = time.localtime().tm_year
    tuoi_hien_tai = nam_hien_tai - nam_duong_lich + 1
    
    nhan_xet+= 'Năm {}, khi ấy Bạn thuộc cung '.format(nam_hien_tai)
    tuoi_kim_lau = tuoi_hien_tai % 9
    if gender == "Nam":
        if tuoi_kim_lau in nam.keys():
            nhan_xet+=str(nam[tuoi_kim_lau]).title()
        
    elif gender =='Nữ':
        if tuoi_kim_lau in nu.keys():
            nhan_xet+=str(nu[tuoi_kim_lau]).title()
        

    
    nhan_xet += '. Bạn {} tuổi '.format(tuoi_hien_tai)+'. Tuổi của bạn ứng với cửu cung là tức cung thứ {}'.format(tong_cung_so[tuoi_kim_lau].title())
    if tuoi_kim_lau in pham_kim_lau.keys():
        nhan_xet += ', phạm kim lâu {} tức {}'.format(tuoi_kim_lau,pham_kim_lau[tuoi_kim_lau])
        khong_pham = '. Không phù hợp xây nhà.'
    else:
        khong_pham ='. Không phạm kim lâu. Phù hợp xây nhà !'

    nhan_xet +=khong_pham
    return nhan_xet

def tinh_hoang_oc(nam_duong_lich,nam_hien_tai = time.localtime().tm_year):
    nhan_xet ='<b>Hoang ốc: </b>'
    pham_hoang_oc = {   1:'Kiết: là tốt tức Làm nhà thuận lợi, mọi việc hanh thông.',
                        2:'Nghi: là tốt tức Làm nhà xong giàu có, thịnh vượng.',
                        3:'Địa sát: là xấu tức Làm nhà phạm cung này, chủ nhà hay bị ốm đau, bệnh tật.',
                        4:'Tấn tài: là tốt tức Làm nhà phúc lộc sẽ tới.',
                        5:'Thọ tử: là xấu tức Làm nhà phạm cung này, gia đình ly biệt, có thể chết chóc, bệnh tật.',
                        6:'Hoang ốc: là xấu tức Làm nhà phạm cung này, gia đình nghèo khó, hay lục đục.',
                        7:'Kiết: là tốt tức Làm nhà thuận lợi, mọi việc hanh thông.',
                        8:'Nghi: là tốt tức Làm nhà xong giàu có, thịnh vượng.',
                        9:'Địa sát: là xấu tức Làm nhà phạm cung này, chủ nhà hay bị ốm đau, bệnh tật.',
                        10:'Tấn tài: là tốt tức Làm nhà phúc lộc sẽ tới.',
                        11:'Thọ tử: là xấu tức Làm nhà phạm cung này, gia đình ly biệt, có thể chết chóc, bệnh tật.',
                        12:'Hoang ốc: là xấu tức Làm nhà phạm cung này, gia đình nghèo khó, hay lục đục.',
                    }
    #nam_hien_tai = time.localtime().tm_year
    tuoi_hien_tai = nam_hien_tai - nam_duong_lich+1
    tuoi_hoang_oc_chan = int(tuoi_hien_tai/10)
    tuoi_hoang_oc_le = tuoi_hien_tai%10
    tuoi_hoang_oc = tuoi_hoang_oc_chan + tuoi_hoang_oc_le
    khong_pham = ''
    if 0< tuoi_hoang_oc <=6:
        if tuoi_hoang_oc_chan in pham_hoang_oc.keys():
            nhan_xet += 'Tuổi của bạn thuộc cung {}'.format(pham_hoang_oc[tuoi_hoang_oc])
            if "tốt" in pham_hoang_oc[tuoi_hoang_oc]:
                khong_pham = '. Phù hợp xây nhà !'
            else:
                khong_pham ='. Không phù hợp xây nhà.'
    else:
        nhan_xet += 'Tuổi của bạn thuộc cung {}'.format(pham_hoang_oc[tuoi_hoang_oc-6])
        if "tốt" in pham_hoang_oc[tuoi_hoang_oc-6]:
            khong_pham = '. Phù hợp xây nhà !'
        else:
            khong_pham ='. Không phù hợp xây nhà.'
        
    nhan_xet += khong_pham
    return nhan_xet

def tinh_nam_thuan_loi(gender,nam_sinh,thang_sinh,ngay_sinh):
    list_12_nam = []
    nhan_xet = ''
    
    ngay_am,thang_am,nam_sinh_gia_chu_am_lich = tinh_nam_am_lich(nam_sinh,thang_sinh,ngay_sinh)
    can_chi_nam_sinh_gia_chu = tinh_can_chi(nam_sinh_gia_chu_am_lich).split(' ')
    can_nam_sinh_gia_chu = can_chi_nam_sinh_gia_chu[0]
    chi_nam_sinh_gia_chu = can_chi_nam_sinh_gia_chu[1]

    nam_hien_tai = datetime.now().strftime('%d-%m-%Y').split('-')
    nam_duong = int(nam_hien_tai[2])
    # tính tam tai, kim lâu, hoang ốc 11 năm kế tiếp.
    for i in range(1,12):
        
        tam_tai = tinh_tam_tai(nam_sinh,thang_sinh,ngay_sinh,nam_duong+i)
        kim_lau = tinh_kim_lau(gender,nam_sinh,nam_duong+i)
        hoang_oc = tinh_hoang_oc(nam_sinh,nam_duong+i)
        nhan_xet = tam_tai+'<br> ' + kim_lau+'<br> '+hoang_oc

        if ("Phù hợp xây nhà !" in tam_tai) and ("Phù hợp xây nhà !" in kim_lau) and ("Phù hợp xây nhà !" in hoang_oc):
            b ='''<hr><br><b>Khuyến cáo: </b>Năm '''+str(nam_duong+i) +''' của bạn khi ấy: <i><b>Rất phù hợp cho việc xây dựng nhà ở, mua nhà/đất</b></i>.<br>'''
        else:
            b = '''<hr><br><b>Khuyến cáo: </b>Năm '''+str(nam_duong+i) +''' của bạn khi ấy: <i><b>Không phù hợp xây nhà.</b></i>.<br>'''

        can_chi_tung_nam = {nam_duong+i:nhan_xet+str(b)}
        list_12_nam.append(can_chi_tung_nam)
    
    return list_12_nam


