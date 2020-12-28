from datetime import datetime


def getdate():
    datenow = datetime.now().strftime('%d,%m,%Y,%H,%M,%S')
    partofdate = datenow.split(',')
    yil = partofdate[2]
    ay = turkishmonth(int(partofdate[1]))
    gun = partofdate[0]
    saat = partofdate[3]
    dakika = partofdate[4]
    saniye = partofdate[5]
    return gun + ' ' + ay + ' ' + yil + ' ' + saat + ':' + dakika + ':' + saniye


def turkishmonth(ay):
    if ay == 1:
        return 'Ocak'
    elif ay == 2:
        return 'Şubat'
    elif ay == 3:
        return 'Mart'
    elif ay == 4:
        return 'Nisan'
    elif ay == 5:
        return 'Mayıs'
    elif ay == 6:
        return 'Haziran'
    elif ay == 7:
        return 'Temmuz'
    elif ay == 8:
        return 'Ağustos'
    elif ay == 9:
        return 'Eylül'
    elif ay == 10:
        return 'Ekim'
    elif ay == 11:
        return 'Kasım'
    elif ay == 12:
        return 'Aralık'
    else:
        return False
