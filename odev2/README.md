# MLE ile Akıllı Şehir Planlaması  
### Poisson Dağılımı ile Trafik Yoğunluğu Tahmini

## Proje Özeti
Bu projede, bir dakikada geçen araç sayıları kullanılarak trafik yoğunluğu **Poisson dağılımı** ile modellenmiştir. Amaç, Poisson dağılımının parametresi olan **λ (lambda)** değerini **Maximum Likelihood Estimation (MLE)** yöntemi ile tahmin etmektir.

Çalışma iki ana bölümden oluşmaktadır:

- **Teorik analiz:** Poisson dağılımı için likelihood ve log-likelihood fonksiyonlarının türetilmesi
- **Sayısal analiz:** Python kullanarak negatif log-likelihood fonksiyonunun minimize edilmesi

---

# Kullanılan Veri

Projede kullanılan trafik verisi:


[12, 15, 10, 8, 14, 11, 13, 16, 9, 12, 11, 14, 10, 15]


Bu değerler bir dakikada gözlemlenen araç sayılarını temsil etmektedir.

---

# Kullanılan Yöntem

## 1. Teorik Çözüm

Poisson dağılımının olasılık kütle fonksiyonu:

\[
P(K=k)=\frac{e^{-\lambda}\lambda^k}{k!}
\]

Likelihood fonksiyonu oluşturulmuş ve log-likelihood ifadesi türetilmiştir.

MLE yöntemi uygulanarak şu sonuca ulaşılmıştır:


λ̂ = (1/n) * Σ k_i


Yani **Poisson dağılımı için MLE tahmini veri ortalamasına eşittir.**

---

## 2. Python ile Sayısal Çözüm

Negatif log-likelihood fonksiyonu Python ile tanımlanmıştır:


NLL(λ) = nλ − (Σk_i) log(λ)


Bu fonksiyon `scipy.optimize.minimize` kullanılarak minimize edilmiştir.

Sayısal sonuç ile analitik sonuç karşılaştırılmıştır.

---

# Elde Edilen Sonuçlar

Verilen veri için:

| Yöntem | λ Tahmini |
|------|------|
| Analitik MLE | 12.14 |
| Sayısal MLE | 12.14 |

Sonuçlar birbiriyle tamamen uyumludur.

---

# Görselleştirme

Gerçek trafik verisinin histogramı ile tahmin edilen Poisson dağılımı karşılaştırılmıştır.

Üretilen grafik:


traffic_poisson_fit.png


Grafik, modelin verinin merkezi eğilimini makul biçimde temsil ettiğini göstermektedir.

---

# Outlier Analizi

Veri setine **200 araç** değerinde bir aykırı gözlem eklendiğinde:

| Durum | λ Tahmini |
|------|------|
| Orijinal veri | 12.14 |
| Outlier eklenmiş veri | 24.67 |

Bu sonuç, MLE tahmininin **örnek ortalamasına eşit olması nedeniyle aykırı değerlere oldukça duyarlı olduğunu** göstermektedir.

---

# Dosya Yapısı


mleOdev/
│
├── rapor.tex
├── rapor.pdf
├── odev.ipynb
├── traffic_poisson_fit.png
└── README.md


| Dosya | Açıklama |
|-----|-----|
| `rapor.tex` | LaTeX rapor kaynağı |
| `rapor.pdf` | PDF raporu |
| `odev.ipynb` | Jupyter Notebook çözümü |
| `traffic_poisson_fit.png` | Grafik çıktısı |
| `README.md` | Proje açıklaması |

---

# Kullanılan Kütüphaneler

- NumPy
- SciPy
- Matplotlib

---

# Çalıştırma

Notebook'u çalıştırmak için gerekli paketleri kur:


pip install numpy scipy matplotlib


Ardından Jupyter Notebook'u çalıştır:


jupyter notebook


ve `odev.ipynb` dosyasını sırayla çalıştır.

---

# Sonuç

Bu çalışmada Poisson dağılımı için Maximum Likelihood Estimation yöntemi hem **teorik hem de sayısal olarak uygulanmıştır**.

Elde edilen sonuçlar:

- Poisson dağılımı için MLE tahmininin veri ortalamasına eşit olduğunu doğrulamaktadır.
- Aykırı değerlerin MLE tahminini ciddi biçimde değiştirebildiğini göstermektedir.

Bu nedenle gerçek veri analizlerinde **outlier tespiti ve veri temizliği kritik ö
