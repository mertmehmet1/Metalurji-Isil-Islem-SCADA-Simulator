import time
from firin_simulator import SanalFirin

class PIDController:

    def __init__(self,kp, ki,kd):
        self.kp=kp
        self.ki=ki
        self.kd=kd
        self.integral = 0.0
        self.last_error = 0.0

    def calculate(self,setpoint,current_value,dt=1.0):
        error= setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.last_error) / dt 
        output = (
            (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        )   
        self.last_error = error
        return output

# ---- YENİ: REÇETE YÖNETİM SINIFI (OOP) ---- 
class ReceteYöneticisi:

    def __init__(self):
        # Gerçek bir şirkette bu veriler bir JSON dosyasından veya SQL veritabanından çekilir.
        # Biz burada bir sözlük (dictionary) listesiyle simüle ediyoruz.
        self.aktif_recete = [
            {
                "adim":1,
                "isim": "On Isitma",
                "hedef_temp": 45.0,
                "sure": 10,
            }, # 45 dereceye çık, 10 sn kal
            {
                "adim":2,
                "isim":"Ostenitleme",
                "hedef_temp":80.0,
                "sure":15,
            }, # 80 dereceye çık, 15 sn kal
            {
                "adim":3,
                "isim":"Kontrollü Sogutma",
                "hedef_temp": 25.0,
                "sure":5,
            }, # 25 dereceye in, 5 sn bekle 
        ]
        self.guncel_adim_index=0
        self.adim_kalan_sure = self.aktif_recete[0]["sure"]

    def get_guncel_hedef(self):
        """ O anki adımın hedef sıcaklığını döner"""
        if self.guncel_adim_index < len(self.aktif_recete):
            return  self.aktif_recete[self.guncel_adim_index]["hedef_temp"]
        return 25.0 # Reçete bittiyse oda sıcaklığına dön 
    
    def güncelle_zaman(self):
        """ Her saniye Çağrılır. Adım süresi bittiyse bir sonraki adıma geçer."""
        if self.guncel_adim_index >= len(self.aktif_recete):
            return "BITTI"
        
        self.adim_kalan_sure -= 1
        guncel_adim = self.aktif_recete[self.guncel_adim_index]

        print(
            f" --> [RECETE] Adim {guncel_adim['adim']}: {guncel_adim['isim']} | Kalan Sure: {self.adim_kalan_sure} sn"
        )

        if self.adim_kalan_sure <= 0:
            self.guncel_adim_index += 1
            if self.guncel_adim_index < len(self.aktif_recete):
                self.adim_kalan_sure = self.aktif_recete[
                    self.guncel_adim_index
                ]["sure"]
                print(
                    f"\n *** [SİSTEM] BİR SONRAKİ ADIMA GEÇİLDİ: {self.aktif_recete[self.guncel_adim_index]['isim']}***\n"
                )
            else:
                return "BITTI"
                
        return "DEVAM"    
       


    