# Metalurji Isıl İşlem SCADA & Otomasyon Simülatörü / Metallurgy Heat Treatment SCADA & Automation Simulator

[Türkçe açıklamalar için aşağıya kaydırın / Scroll down for English documentation]

---

## 🇺🇸 English Documentation

This project is a **SCADA & HMI Simulator** that replicates industrial furnace processes (Preheating, Austenitizing, Controlled Cooling) in a Metallurgy and Materials Engineering production facility, featuring a decoupled, layered software architecture.

### 🛠️ Technical Features and Architecture
* **Embedded System / Physics Layer (`firin_simulator.py`):** Simulates the thermal dynamics, heat coefficients, and industrial sensor noise of the furnace. It runs on a separate thread using **Multithreading** to prevent freezing the main user interface.
* **Smart Control / Logic Layer (`ana_yazilim.py`):** Features a custom **PID (Proportional-Integral-Derivative)** Control Algorithm written from scratch to prevent temperature oscillations, along with an OOP-based multi-step **Recipe Management** system.
* **Visual Monitoring / HMI Layer (`arayüz.py`):** An industrial control panel designed with **Tkinter** for real-time operator monitoring, integrated with **Matplotlib** to plot a live temperature-time curve.

### 📝 Development Story and Ethical Statement (Learning Process)
This project was developed to practice industrial software architectures, multithreading, and control algorithms as a 2nd-year Computer Engineering student.

Throughout the development process, Artificial Intelligence was utilized not for copy-pasting ready-made code, but as a **technical mentor and documentation source**. Architectural patterns (Decoupling), integration errors due to library version differences, and syntax edge cases were resolved firsthand by analyzing traceback logs. The goal was not to memorize code, but to learn how to correctly integrate the core components of an industry-standard system architecture.

---

## 🇹🇷 Türkçe Dokümantasyon

Bu proje, bir üretim tesisindeki endüstriyel fırın süreçlerini (Ön Isıtma, Östenitleme, Kontrollü Soğutma) taklit eden, katmanlı yazılım mimarisine sahip bir **SCADA & HMI Simülatör** projesidir.

### 🛠️ Teknik Özellikler ve Mimari Yapı
* **Gömülü Sistem / Fizik Katmanı (`firin_simulator.py`):** Fırının termal dinamiklerini, ısı katsayılarını ve endüstriyel sensör gürültülerini (Noise) simüle eden katman. Ana arayüzü kilitlememesi için **Multithreading** altyapısı ile ayrı bir iş parçacığında çalışır.
* **Akıllı Kontrol / Mantık Katmanı (`ana_yazilim.py`):** Sıcaklık dalgalanmalarını önlemek amacıyla sıfırdan yazılmış **PID (Proportional-Integral-Derivative)** Kontrol Algoritması ve Nesne Yönelimli Programlama (OOP) ilkelerine dayalı çok adımlı **Metalurjik Reçete Yönetimi** (Recipe Management).
* **Görsel İzleme / HMI Katmanı (`arayüz.py`):** Operatörün anlık durumu izlemesini sağlayan, **Tkinter** ile tasarlanmış endüstriyel kullanıcı paneli ve **Matplotlib** kütüphanesi gömülerek oluşturulmuş canlı grafik ekranı.

### 📝 Geliştirme Hikayesi ve Etik Beyan (Öğrenim Süreci)
Bu proje, Bilgisayar Mühendisliği 2. sınıf öğrencisi olarak endüstriyel yazılım mimarilerini, çoklu iş parçacıklarını (Threads) ve kontrol algoritmalarını pratik etmek amacıyla geliştirilmiştir. 

Geliştirme sürecinde yapay zeka hazır kod kopyalamak için değil; **bir teknik akıl hocası (mentor) ve dokümantasyon kaynağı** olarak kullanılmıştır. Tasarım kalıpları (Decoupling), kütüphane versiyon farklarından kaynaklanan entegrasyon hataları ve yazım pürüzleri bizzat loglar analiz edilerek çözülmüştür. Amaç kod ezberlemek değil, endüstriyel standartta bir sistem mimarisinin parçalarını doğru şekilde birleştirmeyi öğrenmek olmuştur.
