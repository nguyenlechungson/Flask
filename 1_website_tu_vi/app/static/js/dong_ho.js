$(function Dong_ho() {
    var gio = document.getElementById("gio");
    var phut = document.getElementById("phut");
    var giay = document.getElementById("giay");
    var Gio_hien_tai = new Date().getHours();
    var Phut_hien_tai = new Date().getMinutes();
    var Giay_hien_tai = new Date().getSeconds();
    gio.innerHTML = Gio_hien_tai;
    phut.innerHTML = Phut_hien_tai;
    giay.innerHTML = Giay_hien_tai;

    var Dem_gio = setInterval(Dong_ho, 1000);

  }
  
)