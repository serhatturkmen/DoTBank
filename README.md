# DoTBank
Flask Bank Project

# Kurulum

- Gerekli olan kurulumlar (Linux için)
sudo apt-get install libgtk-3-dev

.env dosyası oluşturularak 
- SQLALCHEMY_DATABASE_URI='sqlite:///veritabani.db'
- MY_SECRET
keyler girilmelidir.

- E-posta hizmetini kullanabilmek için .env dosyasında
  - EMAIL_USERNAME
  - EMAIL_PASSWORD
  - EMAIL_SERVER
eklenmelidir.

# Örnek Api Kullanımı

Kart Bilgisinden kullanıcı numarası öğrenme
  - curl -X POST -F 'cardnumber=1111222233334444' -F 'year=2023' -F 'month=10' -F 'name=JOHN DOE' -F 'secretkey=145' http://127.0.0.1:8580/api/v1.0/trust/

Gelen kullanıcı numarasından ödeme almak
  - curl -X POST -F 'receiverid=1' -F 'senderid=2' -F 'amount=10' http://127.0.0.1:8580/api/v1.0/getpay/

# Uygulama Resimleri

![alt text](https://github.com/serhatturkmen/DoTBank/blob/main/images/hesaplar.png)
![alt text](https://github.com/serhatturkmen/DoTBank/blob/main/images/hesaplar-para-yatırma.png)
![alt text](https://github.com/serhatturkmen/DoTBank/blob/main/images/hesaplar-para-cek.png)
![alt text](https://github.com/serhatturkmen/DoTBank/blob/main/images/hesaplar-ekle.png)
![alt text](https://github.com/serhatturkmen/DoTBank/blob/main/images/dekontlar.png)
![alt text](https://github.com/serhatturkmen/DoTBank/blob/main/images/kartlar.png)
![alt text](https://github.com/serhatturkmen/DoTBank/blob/main/images/kart-ekle.png)

