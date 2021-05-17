# DoTBank
Flask Bank Project

# Kurulum
- E-posta hizmetini kullanabilmek için FileEvent.py dosyasındaki sendmail fonksiyonunda
    - mailadress
    - mailpass
    - mailserver
    - mailport
    
Değişkenlerine mevcut eposta hizmetinizi girmelisiniz.

# Api Kullanımı

Kart Bilgisinden kullanıcı numarası öğrenme
  - curl -X POST -F 'cardnumber=1111222233334444' -F 'year=2023' -F 'month=10' -F 'name=JOHN DOE' -F 'secretkey=145' http://127.0.0.1:8580/api/v1.0/trust/

Gelen kullanıcı numarasından ödeme almak
  - curl -X POST -F 'receiverid=1' -F 'senderid=2' -F 'amount=10' http://127.0.0.1:8580/api/v1.0/getpay/

![alt text](https://github.com/serhatturkmen/DoTBank/blob/main/images/hesaplar.png)
