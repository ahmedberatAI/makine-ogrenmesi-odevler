# Giriş

Bu ödevde HMM (Hidden Markov Model) kullanılarak basit bir izole kelime tanıma örneği hazırlanmıştır. Amaç, hem teorik olarak Viterbi algoritmasının nasıl çalıştığını göstermek hem de Python ortamında küçük bir kelime sınıflandırıcı kurmaktır. Uygulama kısmında gerçek ses dosyaları yerine temsili gözlem dizileri kullanılmıştır. Bu tercih, sistemi daha sade, anlaşılır ve hata ihtimali daha düşük hale getirmiştir.

# 1. Bölüm: Viterbi ile teorik hesaplama

Bu bölümde "EV" kelimesi için verilen HMM modeli kullanılmıştır.

## Verilenler

- Gizli durumlar: `S = {e, v}`
- Gözlemler: `O = {High, Low}`
- Başlangıç olasılığı: `P(e) = 1.0`
- Geçiş olasılıkları:
  - `P(e->e) = 0.6`
  - `P(e->v) = 0.4`
  - `P(v->v) = 0.8`
  - `P(v->e) = 0.2`
- Emisyon olasılıkları:
  - `P(High | e) = 0.7`
  - `P(Low | e) = 0.3`
  - `P(High | v) = 0.1`
  - `P(Low | v) = 0.9`

Gözlem dizisi:

`[High, Low]`

## Kullanılan mantık

Viterbi algoritması, her adımda "buraya kadar gelmiş en iyi yol hangisi?" sorusunu sorar. Yani tüm yolları tek tek denemek yerine, her durumda o ana kadar bulunan en güçlü yolu saklar.

Temel fikir şu şekildedir:

- İlk adımda başlangıç olasılığı ile emisyon olasılığı çarpılır.
- Sonraki adımlarda, önceki en iyi değer ile geçiş olasılığı çarpılır.
- Son olarak o durumun gözlemi üretme olasılığı eklenir.

## 1. adım: İlk gözlem = High

İlk gözlem `High` olduğu için iki durum için ayrı ayrı hesap yapılır.

### e durumu

`delta1(e) = P(e) * P(High | e)`

`delta1(e) = 1.0 * 0.7 = 0.7`

### v durumu

Başlangıçta sadece `e` durumundan başlanabildiği için:

`delta1(v) = P(v) * P(High | v) = 0 * 0.1 = 0`

İlk adım sonunda tablo:

| Zaman | Durum | Değer |
|---|---|---:|
| 1 | e | 0.700 |
| 1 | v | 0.000 |

Burada en güçlü başlangıç durumu açık şekilde `e` olur.

## 2. adım: İkinci gözlem = Low

Şimdi ikinci gözlem `Low` için her durumun en iyi değeri bulunur.

### e durumuna gelmek

İki olasılık vardır:

- `e -> e`
- `v -> e`

Hesap:

`delta2(e) = max[delta1(e) * P(e->e), delta1(v) * P(v->e)] * P(Low | e)`

`delta2(e) = max[0.7 * 0.6, 0 * 0.2] * 0.3`

`delta2(e) = max[0.42, 0] * 0.3`

`delta2(e) = 0.42 * 0.3 = 0.126`

Bu yolun en iyi geçmişi `e -> e` olur.

### v durumuna gelmek

İki olasılık vardır:

- `e -> v`
- `v -> v`

Hesap:

`delta2(v) = max[delta1(e) * P(e->v), delta1(v) * P(v->v)] * P(Low | v)`

`delta2(v) = max[0.7 * 0.4, 0 * 0.8] * 0.9`

`delta2(v) = max[0.28, 0] * 0.9`

`delta2(v) = 0.28 * 0.9 = 0.252`

Bu yolun en iyi geçmişi `e -> v` olur.

İkinci adım tablosu:

| Zaman | Durum | En iyi önceki yol | Değer |
|---|---|---|---:|
| 2 | e | e -> e | 0.126 |
| 2 | v | e -> v | 0.252 |

## Son karar

Son adımda büyük olan değeri seçeriz:

- `e -> e = 0.126`
- `e -> v = 0.252`

`0.252 > 0.126` olduğu için en olası durum dizisi:

`e -> v`

Yani gözlem dizisi `[High, Low]` için en olası fonem dizisi **e-v** bulunur.

# 2. Bölüm: Python uygulaması

Python tarafında `hmmlearn` kütüphanesi ile iki ayrı model oluşturulmuştur:

- `EV`
- `OKUL`

Bu örnekte gerçek ses kaydı kullanılmamıştır. Onun yerine ayrık ve küçük gözlem dizileri kullanılmıştır:

- `0 = High`
- `1 = Low`

Temsili eğitim dizileri şu şekildedir:

## EV için örnek diziler

- `[High, Low]`
- `[High, Low, Low]`
- `[High, High, Low]`

## OKUL için örnek diziler

- `[Low, High, Low, Low]`
- `[Low, High, Low, High]`
- `[Low, Low, High, Low]`

Kodda `CategoricalHMM` kullanılmıştır. Bunun nedeni, gözlemlerin ayrık kategorilerden oluşmasıdır. Ayrıca yeni `hmmlearn` sürümlerinde bu sınıf, `MultinomialHMM` kullanımına göre daha açık ve daha sorunsuz bir çözümdür.

Bu eğitim dizileri kodda sadece gösterilmemiş, aynı zamanda model parametrelerini çıkarmak için de kullanılmıştır. Basitlik adına soldan-sağa bir durum varsayımı yapılmıştır. Yani her gözlem dizisi kelimedeki durumlara sırayla paylaştırılmış, sonra bu küçük örneklerden geçiş ve emisyon sayımları elde edilmiştir. Daha sonra bu sayımlar olasılığa çevrilerek HMM modeli kurulmuştur. Bu yöntem küçük veri için sade ve güvenli bir çözümdür.

Sistem çalışma mantığı:

1. `EV` ve `OKUL` için iki ayrı HMM tanımlanır.
2. Bilinmeyen test dizisi her iki modele ayrı ayrı verilir.
3. Her model için log-likelihood skoru hesaplanır.
4. Hangi skor daha yüksekse test dizisi o kelimeye atanır.

Bu ödevde kullanılan test dizisi:

`[High, Low, Low]`

Bu dizi `EV` modeline daha uygun olduğu için sonuç olarak `EV` seçilmesi beklenir. Program çalıştırıldığında `EV` modeli daha yüksek log-likelihood verdiği için test verisi `EV` olarak sınıflandırılmıştır.

# 3. Bölüm: Analiz ve yorumlama

## Ses verisindeki gürültü emisyon olasılıklarını nasıl etkiler?

Gürültü arttığında, modelin bir duruma ait doğru gözlemi üretme güveni azalır. Örneğin normalde bir durum `High` üretmeye daha yatkınsa, gürültü yüzünden bazen `Low` gibi davranabilir. Bu da emisyon olasılıklarını daha karışık hale getirir. Sonuç olarak doğru durum ile yanlış durum birbirine daha çok benzeyebilir ve tanıma başarısı düşebilir.

## Neden büyük sistemlerde sadece HMM/Viterbi yeterli görülmez?

Küçük örneklerde HMM oldukça faydalıdır çünkü mantığı nettir ve hesapları anlaşılırdır. Ancak gerçek sistemlerde binlerce kelime, çok farklı konuşmacılar, aksanlar, hız farkları ve gürültü vardır. Böyle durumlarda klasik HMM yapısı sınırlı kalabilir. Deep learning tabanlı yöntemler daha karmaşık örüntüleri otomatik öğrenebildiği için büyük veri üzerinde genelde daha başarılı sonuç verir. Bu yüzden güncel konuşma tanıma sistemlerinde daha karmaşık modeller tercih edilmeye başlanmıştır.

# Sonuç

Bu çalışmada önce Viterbi algoritması ile `[High, Low]` gözlem dizisinin en olası durum dizisi hesaplanmış ve sonuç `e-v` olarak bulunmuştur. Daha sonra `hmmlearn` ile sade bir kelime sınıflandırıcı hazırlanmış, `EV` ve `OKUL` için iki model oluşturulmuş ve bilinmeyen bir test dizisinin hangi kelimeye ait olduğu skor karşılaştırması ile belirlenmiştir. Ödevin amacı olan teorik anlatım, temel uygulama ve kısa analiz bölümü tamamlanmıştır.
