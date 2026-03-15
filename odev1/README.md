# HMM Speech Recognition

Bu proje, HMM kullanarak basit bir izole kelime tanıma örneği göstermektedir. Amaç, `EV` ve `OKUL` kelimeleri için iki ayrı model kurup bilinmeyen bir gözlem dizisinin hangi kelimeye daha yakın olduğunu bulmaktır.

## Problem tanımı

Verilen bir gözlem dizisinin, tanımlanan HMM modellerinden hangisine daha yüksek olasılıkla ait olduğunu belirlemek.

## Veri

Bu projede gerçek ses kaydı kullanılmamıştır. Bunun yerine küçük ve temsili gözlem dizileri kullanılmıştır.

- `EV` için: `[High, Low]`, `[High, Low, Low]`, `[High, High, Low]`
- `OKUL` için: `[Low, High, Low, Low]`, `[Low, High, Low, High]`, `[Low, Low, High, Low]`

Bu diziler hem örnek veri olarak gösterilmiş hem de basit soldan-sağa HMM parametrelerini çıkarmak için kullanılmıştır.

## Kullanılan yöntem

- Ayrık gözlem sembolleri kullanılmıştır: `High` ve `Low`
- `hmmlearn` içindeki `CategoricalHMM` sınıfı seçilmiştir
- `EV` ve `OKUL` için ayrı HMM modelleri tanımlanmıştır
- Test dizisi için her modelin log-likelihood skoru hesaplanmıştır
- En yüksek skoru veren model sonuç olarak seçilmiştir

## Kullanılan kütüphaneler

- `numpy`
- `hmmlearn`

## Proje yapısı

```text
HMM-Speech-Recognition/
├── data/
├── src/
│   └── recognizer.py
├── report/
│   └── rapor.md
├── requirements.txt
└── README.md
```

## Nasıl çalıştırılır?

```bash
pip install -r requirements.txt
python src/recognizer.py
```

## Beklenen örnek çıktı

```text
Temsili egitim dizileri
EV: [['High', 'Low'], ['High', 'Low', 'Low'], ['High', 'High', 'Low']]
OKUL: [['Low', 'High', 'Low', 'Low'], ['Low', 'High', 'Low', 'High'], ['Low', 'Low', 'High', 'Low']]

Test dizisi:
['High', 'Low', 'Low']

Model skorları (log-likelihood):
EV: -1.1650
OKUL: -2.9720

Tahmin edilen kelime: EV
```

## Sonuçlar

Kod çalıştırıldığında test dizisi `[High, Low, Low]` için `EV` modelinin log-likelihood değeri `OKUL` modelinden daha yüksek çıkmıştır. Bu nedenle test verisi `EV` olarak sınıflandırılmıştır.

## Yorum / tartışma

Bu proje gerçek bir konuşma tanıma sistemi kadar gelişmiş değildir. Ancak HMM mantığını görmek, Viterbi sonucunu yorumlamak ve basit bir sınıflandırıcı kurmak için yeterli ve anlaşılır bir örnektir.
