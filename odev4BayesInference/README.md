
# Bayesian Brightness Analysis

## Proje başlığı
Bu çalışmada sentetik parlaklık verisi üzerinde Bayes yaklaşımı ile `mu` ve `sigma` parametreleri tahmin edilmeye çalışıldı.

## Problem
Amaç, gözlem verisinden gerçek ortalama parlaklık (`mu`) ve yayılım (`sigma`) değerlerini MCMC ile tahmin etmekti.

## Veri
Notebook içinde kullanılan gerçek değerler:

- Gerçek `mu`: 150
- Gerçek `sigma`: 10
- Gözlem sayısı: 50

Veri sentetik olarak üretildi ve sonra histogram ile ilk görünümüne bakıldı.

## Yöntem
Mevcut notebook içinde likelihood, prior ve posterior tanımlanıp `emcee` ile MCMC örneklemesi yapıldı. Sonuçlar için posterior örneklerden median, `%16` ve `%84` değerleri alındı. Ayrıca histogram, trace plot ve corner plot üretildi.

## Sonuçlar
`mu` için:

- Gerçek değer: `150`
- Median: `140.0000094884707`
- `%16`: `139.99992515134633`
- `%84`: `140.0001277676822`
- Mutlak hata: `9.99999051152929`

`sigma` için:

- Gerçek değer: `10`
- Median: `4.999994535192723`
- `%16`: `4.9998679766792975`
- `%84`: `5.000117929718407`
- Mutlak hata: `5.000005464807277`

## Yorum
Doğruluk analizi açısından sonuçlar çok iyi görünmüyor. `mu` tahmini gerçek değerden yaklaşık `10`, `sigma` tahmini ise yaklaşık `5` birim sapmış durumda. Yani mevcut çıktıdaki medyan değerler gerçek parametrelere yakın değil.

`mu` tahmininin `sigma`'dan daha hassas görünmesinin nedeni, bu notebook çıktısında güven aralığının biraz daha dar olması. Yani gerçek değere yakınlık bakımından değil, örneklerin yayılımı bakımından `mu` tarafı biraz daha sıkı duruyor. `sigma` yayılımı temsil ettiği için küçük değişimlerden daha fazla etkilenebiliyor.

Corner plot'a bakınca `mu` ile `sigma` arasında belirgin ve güçlü bir korelasyon görünmüyor. Noktalar daha çok dağınık duruyor. Ayrıca contour üretimi için de uyarı geldiği için burada kuvvetli bir ilişki yorumu yapmak zor.

Trace plot tarafında zincirlerin neredeyse düz çizgiler halinde kalması da örneklemenin çok sınırlı hareket ettiğini gösteriyor. O yüzden bu çıktıların güvenilirliği dikkatli yorumlanmalı.
