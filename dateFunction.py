from datetime import datetime


def getdate():
    datenow = datetime.now().strftime('%d,%m,%Y,%H,%M,%S')
    partofdate = datenow.split(',')
    year = partofdate[2]
    month = turkishmonth(int(partofdate[1]))
    day = partofdate[0]
    hour = partofdate[3]
    mmunite = partofdate[4]
    second = partofdate[5]
    return day + ' ' + month + ' ' + year + ' ' + hour + ':' + mmunite + ':' + second


def turkishmonth(month):
    if month == 1:
        return 'Ocak'
    elif month == 2:
        return 'Şubat'
    elif month == 3:
        return 'Mart'
    elif month == 4:
        return 'Nisan'
    elif month == 5:
        return 'Mayıs'
    elif month == 6:
        return 'Haziran'
    elif month == 7:
        return 'Temmuz'
    elif month == 8:
        return 'Ağustos'
    elif month == 9:
        return 'Eylül'
    elif month == 10:
        return 'Ekim'
    elif month == 11:
        return 'Kasım'
    elif month == 12:
        return 'Aralık'
    else:
        return False
