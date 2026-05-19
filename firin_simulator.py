import random  
import threading
import time 

class SanalFirin(threading.Thread):

    def __init__(self):
        # Thread sınıfının constructor'ını çağırıyoruz
        super().__init__()
        self.current_temp = 25.0
        self.ambient_temp = 25.0
        self.heater_on = False 
        self.running = True # simülasyonu durdurmak için bayrak(flag)

    def run (self):
        """Bu metod, thread.start() denildiğinde arka planda sonsuz döngüde
        çalışıcak fizik motorudur.
        """    
        while self.running:
            # 1.kural: Fiziksel Hesaplama
            if self.heater_on:
                self.current_temp += 2.0
            else:
                if self.current_temp > self.ambient_temp:
                    self.current_temp -= 0.5
            # 1 saniye bekle (Gerçek zamanlı simülasyon)
            time.sleep(1)

    def get_temperature(self):
        """ Dış dünyanın (ana yazılımın) fırına gürültülü sıcaklığı 
        sormasını sağlayan API fonksiyonumuz.
        """
        noise = random.uniform(-0.2,+0.2)
        return round(self.current_temp + noise,2)

    def set_heater(self,state:bool):
        """Dış dünyanın ısıtıcıyı açıp kapatmasını sağlayan fonksiyon."""
        self.heater_on = state

    def stop(self):
        """Simülasyonu tamamen kapatmak için."""
        self.running = False 
        
