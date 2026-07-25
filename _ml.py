# -*- coding: utf-8 -*-
import re, json

PATH = 'index.html'
raw = open(PATH, encoding='utf-8').read()
html = raw

# ---------- string-wiring helpers (NO bs4 serialization) ----------
def ins(html, tagpos, key):
    e = html.find('>', tagpos)
    if e < 0:
        return html
    seg = html[tagpos:e]
    if 'data-i18n=' in seg:
        return html  # already wired
    return html[:e] + ' data-i18n="%s"' % key + html[e:]

def wire_by_id(html, eid, key):
    a = html.find('id="%s"' % eid)
    if a < 0:
        print("  !! MISS id", eid); return html
    t = html.rfind('<', 0, a)
    if t < 0:
        return html
    return ins(html, t, key)

def wire_card(html, pg, ttag, tkey, dkey, prefix='<div class="card" '):
    a = html.find(prefix + "onclick='go(\"%s\")'" % pg)
    if a < 0:
        print("  !! MISS card", pg); return html
    t = html.find('<%s' % ttag, a)
    if t < 0:
        print("  !! MISS", pg, ttag); return html
    html = ins(html, t, tkey)
    p = html.find('<p', t)
    if p < 0:
        print("  !! MISS p", pg); return html
    html = ins(html, p, dkey)
    return html

def wire_tag_before(html, marker, tag, key):
    a = html.find(marker)
    if a < 0:
        print("  !! MISS marker", key, marker[:30]); return html
    t = html.rfind('<%s' % tag, 0, a)
    if t < 0:
        print("  !! MISS tag", key); return html
    return ins(html, t, key)

def wire_p_text(html, page_id, text, key):
    sid = html.find('id="%s"' % page_id)
    if sid < 0:
        print("  !! MISS page", page_id); return html
    i = html.find(text, sid)
    if i < 0:
        print("  !! MISS text", key, text[:30]); return html
    t = html.rfind('<p', 0, i)
    if t < 0:
        return html
    return ins(html, t, key)

def wire_h3_text(html, page_id, text, key):
    sid = html.find('id="%s"' % page_id)
    if sid < 0:
        print("  !! MISS page", page_id); return html
    i = html.find(text, sid)
    if i < 0:
        print("  !! MISS text", key, text[:30]); return html
    t = html.rfind('<h3', 0, i)
    if t < 0:
        return html
    return ins(html, t, key)

def wire_first_tag(html, anchor, tag, key):
    a = html.find(anchor)
    if a < 0:
        print("  !! MISS anchor", key, anchor[:30]); return html
    t = html.find('<%s' % tag, a)
    if t < 0:
        print("  !! MISS tag", key); return html
    return ins(html, t, key)

def wire_all(html, marker, key):
    pos = 0; n = 0
    while True:
        i = html.find(marker, pos)
        if i < 0:
            break
        t = html.rfind('<', 0, i)
        if t < 0:
            break
        if 'data-i18n=' in html[t:i]:
            pos = i + 1
            continue
        html = ins(html, t, key)
        n += 1
        pos = i + 1
    if n == 0:
        print("  !! MISS all", key, marker[:30])
    return html

# ---------- WIRING (79 unwired keys) ----------
# nav (10)
for x in ['home','about','products','gallery','tech','certs','order','contact','factory-strength','frp-rods']:
    html = wire_by_id(html, 'nv-%s' % x, 'nav-%s' % x)

# home cards (9)
cardmap = {
 'about':('card-about-title','card-about-desc'),
 'certs':('card-certs-title','card-certs-desc'),
 'products':('card-products-title','card-products-desc'),
 'order':('card-order-title','card-order-desc'),
 'factory-strength':('card-factory-title','card-factory-desc'),
 'contact':('card-contact-title','card-contact-desc'),
 'tech':('card-tech-title','card-tech-desc'),
 'gallery':('card-gallery-title','card-gallery-desc'),
 'frp-rods':('card-frp-title','card-frp-desc'),
}
for pg,(tk,dk) in cardmap.items():
    html = wire_card(html, pg, 'h3', tk, dk)

# product cards (4)
for pg in ['prod-resin-capsule','prod-epoxy','prod-mg-resin','prod-frp-rod']:
    html = wire_card(html, pg, 'h4', pg, pg+'-desc', prefix='<div ')

# product sub-pages (4)
for pg in ['prod-resin-capsule','prod-epoxy','prod-mg-resin','prod-frp-rod']:
    sid = html.find('id="pg-%s"' % pg)
    if sid < 0:
        print("  !! MISS sub", pg); continue
    h2 = html.find('<h2', sid); html = ins(html, h2, pg)
    ap = html.find('Applications', sid)
    if ap < 0:
        print("  !! MISS apps", pg); continue
    h3a = html.rfind('<h3', 0, ap); html = ins(html, h3a, 'prod-apps-title')
    p = html.find('<p', h3a); html = ins(html, p, pg+'-apps')
    kf = html.find('Key Features', sid)
    if kf < 0:
        print("  !! MISS kf", pg); continue
    h3k = html.rfind('<h3', 0, kf); html = ins(html, h3k, 'prod-features-title')

# about page
html = wire_p_text(html, 'pg-about', 'With a <strong>16,000+ sqm', 'about-p2')
html = wire_p_text(html, 'pg-about', 'Our products are used in coal mine', 'about-p3')
html = wire_h3_text(html, 'pg-about', 'Production Capacity', 'about-capacity')
html = wire_h3_text(html, 'pg-about', 'Factory Tour', 'about-tour')
html = wire_p_text(html, 'pg-about', 'Automatic Resin Capsule Production Line', 'about-video1-label')
html = wire_p_text(html, 'pg-about', 'CKa b2360 Anchor Capsule Production', 'about-video2-label')
html = wire_h3_text(html, 'pg-about', 'Lets work together', 'cta-together-title')
html = wire_p_text(html, 'pg-about', 'Contact us for product recommendations', 'cta-together-desc')

# products CTA
html = wire_h3_text(html, 'pg-products', 'Cant find what you need?', 'cta-find-title')
html = wire_p_text(html, 'pg-products', 'Custom formulations and OEM service', 'cta-find-desc')

# certs hint (p right after h2)
html = wire_first_tag(html, 'Certificates &amp; Quality Assurance</h2>', 'p', 'certs-hint')

# order page
html = wire_first_tag(html, 'How to Order from Jinjiu</h2>', 'p', 'order-hint')
html = wire_tag_before(html, 'How to Order from Jinjiu</h2>', 'h2', 'order-title')
step_titles = [
 ('Send Us a Message','order-step1-title','order-step1-desc'),
 ('Get a Quote','order-step2-title','order-step2-desc'),
 ('Free Samples','order-step3-title','order-step3-desc'),
 ('Confirm & Pay','order-step4-title','order-step4-desc'),
 ('Production','order-step5-title','order-step5-desc'),
 ('Quality Check','order-step6-title','order-step6-desc'),
 ('Shipment','order-step7-title','order-step7-desc'),
 ('After-Sales Support','order-step8-title','order-step8-desc'),
]
for txt,tkey,dkey in step_titles:
    sid = html.find('id="pg-order"')
    i = html.find(txt, sid)
    if i < 0:
        print("  !! MISS step", tkey); continue
    h3 = html.rfind('<h3', 0, i); html = ins(html, h3, tkey)
    p = html.find('<p', h3); html = ins(html, p, dkey)

# contact page
html = wire_first_tag(html, 'Contact Us</h2>', 'p', 'contact-hint')
html = wire_tag_before(html, 'class="note"', 'p', 'contact-form-note')
html = wire_tag_before(html, 'We look forward to partnering with you!', 'p', 'contact-footer-text')
# contact submit button is malformed in source (only a </button> closing tag exists) -> insert a proper opening tag with data-i18n
si = html.find('✉</button>')
if si < 0:
    print("  !! MISS contact-form-submit")
else:
    html = html[:si] + '<button type="submit" class="submit-btn" data-i18n="contact-form-submit">' + html[si:]

# gallery / tech hints
html = wire_p_text(html, 'pg-gallery', 'Click any image to view full size — real photos', 'gallery-hint')
html = wire_p_text(html, 'pg-tech', 'Click any document image to view full size', 'tech-hint')

# footer visitors
html = wire_tag_before(html, 'id="visit-label"', 'span', 'footer-visitors')

# back buttons + spans + whatsapp (all occurrences)
html = wire_all(html, '← Back to Home</a>', 'back-home')
html = wire_all(html, '← Back to Products</a>', 'back-products')
html = wire_all(html, 'Click for details →</span>', 'prod-click')
html = wire_all(html, '💬 WhatsApp: +86 177 2990 3561</a>', 'hero-whatsapp')

# ---------- parse original LANG_DATA (concat-line safe) ----------
m = re.search(r'var LANG_DATA\s*=\s*\{(.*?)\n\};', raw, re.S)
block = m.group(1)
ORIG = {}
ORDER = []
for km in re.finditer(r'"((?:[^"\\]|\\.)*)"\s*:\s*\{', block):
    k = km.group(1)
    if k in ('', 'card-', 'en', 'zh'):
        continue
    i = km.end() - 1
    depth = 0; j = i; end = None
    while j < len(block):
        c = block[j]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end = j; break
        j += 1
    if end is None:
        continue
    obj = block[i+1:end]
    en = re.search(r'"en"\s*:\s*"((?:[^"\\]|\\.)*)"', obj)
    zh = re.search(r'"zh"\s*:\s*"((?:[^"\\]|\\.)*)"', obj)
    if en and zh:
        ORIG[k] = (en.group(1), zh.group(1))
        ORDER.append(k)

EN_OVERRIDE = {
 "order-step1-title":"Send Us a Message",
 "order-step2-title":"Get a Quote",
 "order-step3-title":"Free Samples",
 "order-step4-title":"Confirm & Pay",
 "order-step5-title":"Production",
 "order-step6-title":"Quality Check",
 "order-step7-title":"Shipment",
 "order-step8-title":"After-Sales Support",
 "order-hint":"We make it easy for you — from first inquiry to delivery at your site. No matter where you are in the world.",
 "order-step1-desc":"Tell us what you need — product type, quantity, and destination port. We reply within **24 hours**.",
 "order-step2-desc":"We'll send you a detailed **FOB or CIF quotation** with pricing, lead time, and packaging options within 1 business day.",
 "order-step3-desc":"**50–200 pcs free samples**. You only pay shipping, and we refund it on your first order. Test our quality risk-free.",
 "order-step4-desc":"Proforma Invoice issued. **30% T/T deposit** to start production. Balance before shipment. L/C accepted for orders over $50K.",
 "order-step5-desc":"**15–20 days** lead time. We send you **weekly progress photos** via WhatsApp so you can see your order being made.",
 "order-step6-desc":"Internal QC on every batch. **SGS third-party inspection available** upon request. Only quality products leave our factory.",
 "order-step7-desc":"**FOB Shanghai/Qingdao** or CIF to your port. FCL preferred, LCL available for trials. Full documents: CO, CI, PL, BL.",
 "order-step8-desc":"**24/7 WhatsApp support**. We follow up on your reorder schedule so you never run out of stock.",
 "certs-hint":"Click any certificate image to view full size — all certifications are authentic and verifiable.",
 "contact-hint":"Reply within 24 hours — reach out today for a quote or free sample",
 "gallery-hint":"Click any image to view full size — real photos from our factory and exports",
 "tech-hint":"Click any document image to view full size",
 "about-p2":"With a **16,000+ sqm** factory, **3 fully automated production lines**, and over **100 employees**, we serve mining, tunneling and construction clients across **30+ countries** including Russia, Turkey, Indonesia, South Africa, Chile, Vietnam, Peru, Poland, and Brazil.",
 "about-p3":"Our products are used in coal mine roadway bolting, tunnel support, slope stabilization, foundation anchoring, and civil engineering projects worldwide.",
}

# ---------- RU / TR for EVERY original key ----------
RU_TR = {
 "nav-home":["Главная","Ana Sayfa"],
 "nav-about":["О компании","Hakkımızda"],
 "nav-products":["Продукция","Ürünler"],
 "nav-gallery":["Галерея","Galeri"],
 "nav-tech":["Техдокументация","Teknik"],
 "nav-certs":["Сертификаты","Sertifikalar"],
 "nav-order":["Заказ","Sipariş"],
 "nav-contact":["Контакты","İletişim"],
 "nav-factory-strength":["Мощь завода","Fabrika Gücü"],
 "nav-frp-rods":["Стержни FRP","FRP Çubukları"],
 "nav-logo-text":["АНКЕРНАЯ СМОЛА","ANKRAJ REÇİNESİ"],
 "hero-title":["Профессиональный производитель смоляных анкерных капсул","Profesyonel Reçine Ankraj Kapsülü Üreticisi"],
 "hero-sub":["Нам доверяют горнодобывающие и строительные компании по всему миру с 2004 года. Завод сертифицирован по ISO 9001, MA, SGS. Экспорт в 30+ стран.","2004'ten beri dünya çapında madencilik ve inşaat şirketlerinin güvendiği marka. ISO 9001, MA, SGS sertifikalı fabrika. 30+ ülkeye ihracat."],
 "hero-cta":["📩 Отправить запрос","📩 Teklif İste"],
 "hero-whatsapp":["💬 WhatsApp: +86 177 2990 3561","💬 WhatsApp: +86 177 2990 3561"],
 "card-about-more":["Подробнее","Daha Fazla"],
 "card-products-more":["Смотреть продукцию","Ürünleri Gör"],
 "card-gallery-more":["Смотреть галерею","Galeriyi Gör"],
 "card-tech-more":["Документы","Dokümanlar"],
 "card-certs-more":["Сертификаты","Sertifikaları Gör"],
 "card-order-more":["Процесс","Süreci Gör"],
 "card-contact-more":["Связаться","İletişime Geçin"],
 "card-frp-more":["Подробнее","Detayları Gör"],
 "card-factory-more":["Осмотр завода","Fabrikayı Keşfedin"],
 "card-about-title":["О компании Jinjiu","Jinjiu Hakkında"],
 "card-about-desc":["20+ лет, завод 16 000 м², 3 автоматические линии. Обслуживание горной и строительной отраслей по всему миру.","20+ yıl, 16.000 m² fabrika, 3 otomatik hat. Dünya çapında madencilik ve inşaat."],
 "card-certs-title":["Сертификаты","Sertifikalar"],
 "card-certs-desc":["Патент, отчёты по испытаниям, гарантия качества, сертификаты ISO 9001/14001/45001, MA.","Patent, raporlar, kalite garantisi, ISO 9001/14001/45001, MA sertifikaları."],
 "card-products-title":["Продукция","Ürünler"],
 "card-products-desc":["Смоляные капсулы, эпоксид, смола MG, стержни FRP. Полные спецификации и техданные со страницами деталей.","Reçine kapsülleri, epoksi, MG reçine, FRP çubuklar. Detaylı tüm teknik veriler."],
 "card-order-title":["Как заказать","Nasıl Sipariş Verilir"],
 "card-order-desc":["8-шаговый процесс: запрос → расчёт → образец → производство → контроль → отгрузка.","8 adımlık süreç: sorgu → teklif → numune → üretim → denetim → sevkiyat."],
 "card-factory-title":["Мощь завода","Fabrika Gücü"],
 "card-factory-desc":["Площадь 16 000 м², автоматические линии, лаборатория НИОКР, строгий контроль качества — производственная мощь Jinjiu.","16.000 m² tesis, otomatik hatlar, Ar-Ge laboratuvarı, sıkı kalite kontrol — Jinjiu'nun üretim gücü."],
 "card-contact-title":["Связаться с нами","İletişim"],
 "card-contact-desc":["Эл. почта, WhatsApp, магазин Alibaba. Ответ в течение 24 часов. Бесплатные образцы.","E-posta, WhatsApp, Alibaba Mağazası. 24 saat içinde yanıt. Ücretsiz numuneler."],
 "card-tech-title":["Техническая документация","Teknik Dokümanlar"],
 "card-tech-desc":["Характеристики, методы испытаний, классификация продукции, руководство по наименованиям и эксплуатационные термины.","Özellikler, test yöntemleri, ürün sınıflandırması, adlandırma kılavuzu ve performans terimleri."],
 "card-gallery-title":["Галерея завода","Fabrika Galerisi"],
 "card-gallery-desc":["Реальные фото — линии производства, упаковка, погрузка, экспорт в Турцию, Россию и др.","Gerçek fotoğraflar — üretim hatları, paketleme, yükleme, Türkiye ve Rusya'ya ihracat."],
 "card-frp-title":["Анкерные стержни FRP","FRP Ankraj Çubukları"],
 "card-frp-desc":["Стержни из стеклопластика — полные спецификации, области применения, сертификат безопасности MA.","Cam elyaf takviyeli polimer çubuklar — tam teknik özellikler, uygulama alanları, MA güvenlik sertifikalı."],
 "card-export-desc":["Экспорт в 30+ стран мира.","Dünya çapında 30+ ülkeye ihracat."],
 "about-title":["О компании «Хуайбэй Цзиньцзю Новые Материалы», ООО","Huaibei Jinjiu Yeni Malzemeler Ltd. Şti. Hakkında"],
 "about-p1":["Основана в **2004** году, компания Huaibei Jinjiu New Materials Co., Ltd. — профессиональный производитель смоляных анкеров, анкерных стержней FRP, смолы MG и материалов крепления горных выработок, расположенный в провинции Аньхой, Китай.","**2004** yılında kurulan Huaibei Jinjiu Yeni Malzemeler Ltd. Şti., reçine ankraj maddeleri, FRP ankraj çubukları, MG reçinesi ve maden destek malzemeleri üreticisidir; Çin'in Anhui eyaletinde yer almaktadır."],
 "about-capacity":["Производственная мощность","Üretim Kapasitesi"],
 "about-more":["Подробнее","Daha Fazla"],
 "about-tour":["Экскурсия по заводу","Fabrika Turu"],
 "about-video1-label":["Автоматическая линия производства капсул","Otomatik Kapsül Üretim Hattı"],
 "about-video2-label":["Производство анкеров Φ23×600 мм","Φ23×600mm Ankraj Üretimi"],
 "products-title":["Продукция","Ürünler"],
 "products-hint":["Нажмите на продукт для подробностей, областей применения и характеристик.","Detaylar için herhangi bir ürüne tıklayın."],
 "prod-click":["Подробнее →","Detaylar için tıklayın →"],
 "prod-resin-capsule":["Смоляная анкерная капсула","Reçine Ankraj Kapsülü"],
 "prod-epoxy":["Эпоксидный клей","Epoksi Yapıştırıcı"],
 "prod-mg-resin":["Смола MG","MG Reçinesi"],
 "prod-frp-rod":["Система анкерных стержней FRP","FRP Ankraj Çubuğu Sistemi"],
 "gallery-title":["Галерея завода и продукции","Fabrika ve Ürün Galerisi"],
 "gallery-hint":["Нажмите на изображение для увеличения.","Tam boyut için görsele tıklayın."],
 "tech-title":["Техническая документация","Teknik Dokümanlar"],
 "tech-hint":["Нажмите на изображение для увеличения.","Tam boyut için görsele tıklayın."],
 "tech-intro":["Jinjiu располагает собственным центром НИОКР и испытаний с установками вырыва, приборами времени гелеобразования и термостатическими камерами отверждения. Каждая партия анкерующей смолы проходит полную проверку перед отправкой с завода.","Jinjiu, çekme test tezgâhları, jel zamanı ölçerleri ve termostatik kür odalarıyla kendi bünyesinde Ar-Ge ve test merkezine sahiptir. Her parti ankraj maddesi fabrikadan çıkmadan önce tam olarak denetlenir."],
 "tech-spec-title":["Серия смоляных анкерных капсул — типичные параметры","Reçine Ankraj Kapsülü Serisi — Tipik Parametreler"],
 "tech-spec-cap":["Справочные значения для типичных марок; полная настройка под ваши горно-геологические условия.","Tipik sınıflar için referans değerleri; zemin koşullarınıza göre tamamen özelleştirilebilir."],
 "tech-th-grade":["Марка","Sınıf"],
 "tech-th-cure":["Гелеобразование / Отверждение","Kinetik / Kür"],
 "tech-th-temp":["Рабочая темп.","Çalışma Sıcaklığı"],
 "tech-th-use":["Применение","Tipik Kullanım"],
 "tech-std-title":["Стандарты, по которым мы испытываем","Test Edilen Standartlar"],
 "tech-std-desc":["Анкерные стержни из смолы: MT/T 1061 · Шахтные анкерные канаты: MT/T 942 · Поштучный контроль и управление качеством ISO 9001.","Reçine ankraj çubukları: MT/T 1061 · Maden ankraj halatları: MT/T 942 · Parti denetimi ve ISO 9001 kalite kontrolü."],
 "tech-proc-title":["Стандартный монтаж — 5 шагов","Standart Montaj — 5 Adım"],
 "tech-proc-1":["① Бурение: отверстие по проектному диаметру и глубине","① Delme: tasarı çapı ve derinliğine göre delin"],
 "tech-proc-2":["② Очистка: продуйте или промойте пыль из шпура","② Temizleme: deliğin tozunu üfleyin / yıkayın"],
 "tech-proc-3":["③ Загрузка: протолкните смоляную капсулу на дно шпура","③ Yükleme: reçine kapsülünü deliğin dibine itin"],
 "tech-proc-4":["④ Перемешивание: вращайте стержень, чтобы разбить и перемешать капсулу","④ Karıştırma: kapsülü kırmak ve karıştırmak için çubuğu döndürün"],
 "tech-proc-5":["⑤ Отверждение: выдержите до набора прочности, затем нагружайте","⑤ Kür: kür yaşma ulaşana kadar bekleyin, ardından yükleyin"],
 "certs-title":["Сертификаты и гарантия качества","Sertifikalar ve Kalite Güvencesi"],
 "certs-hint":["Наши обязательства по качеству — международные сертификаты.","Kaliteye olan bağlılığımız — uluslararası sertifikalar."],
 "certs-standard":["Сертификаты и стандарты","Sertifikalar ve Standartlar"],
 "certs-note":["Система качества ISO 9001. Возможна инспекция SGS.","ISO 9001 kalite sistemi. SGS denetimi mevcuttur."],
 "order-title":["Как заказать","Nasıl Sipariş Verilir"],
 "order-hint":["8-шаговый процесс от запроса до поставки.","Sorgudan teslimata 8 adımlık süreç."],
 "order-step1-title":["Запрос","Sorgu"],
 "order-step1-desc":["Отправьте ТУ + количество + порт. Ответ за 24 ч.","Özellikler + miktar + liman gönderin. 24 saat içinde yanıt."],
 "order-step2-title":["Расчёт","Teklif"],
 "order-step2-desc":["Расчёт FOB/CIF со сроком поставки.","Teslim süresiyle FOB/CIF teklifi."],
 "order-step3-title":["Бесплатные образцы","Ücretsiz Numuneler"],
 "order-step3-desc":["50–200 шт. бесплатно. Доставка возвращается.","50-200 adet ücretsiz. Kargo iade edilir."],
 "order-step4-title":["Подтверждение","Onay"],
 "order-step4-desc":["Выставляется PI. Аванс 30% T/T.","Proforma fatura düzenlenir. %30 T/T kapora."],
 "order-step5-title":["Производство","Üretim"],
 "order-step5-desc":["15–20 дней. Фото хода работ в WhatsApp.","15-20 gün. WhatsApp üzerinden ilerleme fotoğrafları."],
 "order-step6-title":["Контроль","Denetim"],
 "order-step6-desc":["Внутренний КК + опционально SGS.","Kalite kontrol + isteğe bağlı SGS denetimi."],
 "order-step7-title":["Отгрузка","Sevkiyat"],
 "order-step7-desc":["Фото погрузки + полный пакет документов (CO, CI, PL, BL).","Yükleme fotoğrafları + tüm belgeler (CO, CI, PL, BL)."],
 "order-step8-title":["Послепродажное","Satış Sonrası"],
 "order-step8-desc":["WhatsApp 24/7 + поддержка повторного заказа.","7/24 WhatsApp + yeniden sipariş desteği."],
 "order-payment":["💳 Условия оплаты","💳 Ödeme Koşulları"],
 "order-payment-desc":["T/T: 30% аванс + 70% перед отгрузкой. Аккредитив > 50 тыс. $.","T/T: %30 kapora + %70 sevkiyat öncesi. L/C 50.000 $ üzeri."],
 "order-moq":["📦 Минимальный объём заказа","📦 Minimum Sipariş Miktarı"],
 "order-moq-desc":["Пробный: 5 000 шт. Обычный: 10 000 шт.","Deneme: 5.000 adet. Standart: 10.000 adet."],
 "order-shipping":["🌍 Доставка","🌍 Kargo ve Teslimat"],
 "order-shipping-desc":["FOB Шанхай/Циндао или CIF. Предпочтителен FCL, возможен LCL.","FOB Şangay/Qingdao veya CIF. FCL tercih edilir, LCL mümkün."],
 "contact-title":["Связаться с нами","İletişim"],
 "contact-hint":["Ответ в течение 24 часов — расчёт или бесплатный образец.","24 saat içinde yanıt — teklif veya ücretsiz numune."],
 "contact-form-title":["📩 Быстрый запрос","📩 Hızlı Sorgu"],
 "contact-form-name":["Ваше имя *","Adınız *"],
 "contact-form-email":["Ваш email *","E-postanız *"],
 "contact-form-company":["Название компании","Şirket Adı"],
 "contact-form-phone":["WhatsApp / Телефон","WhatsApp / Telefon"],
 "contact-form-message":["Опишите ваши требования...","Gereksinimlerinizi belirtin..."],
 "contact-form-submit":["Отправить запрос ✉","Sorgu Gönder ✉"],
 "contact-form-note":["Отвечаем в течение 24 ч. Конфиденциально.","24 saat içinde yanıt veriyoruz. Gizli."],
 "contact-footer-text":["🤝 Ждём сотрудничества с вами!","🤝 Sizinle ortaklık yapmayı dört gözle bekliyoruz!"],
 "footer-text":["© 2004–2025 ООО «Хуайбэй Цзиньцзю Новые Материалы» | Профессиональный производитель смоляных анкерных капсул","© 2004–2025 Huaibei Jinjiu Yeni Malzemeler Ltd. Şti. | Profesyonel Reçine Ankraj Kapsülü Üreticisi"],
 "footer-addr":["ул. Зап. Нюйчжэнь, зона экон. развития Суйси, г. Хуайбэй, пров. Аньхой, Китай · ISO 9001:2015","Çin, Anhui, Huaibei, Suixi Ekonomik Kalkınma Bölgesi, Nvzhen Batı Yolu · ISO 9001:2015"],
 "footer-visitors":["Посетители","Ziyaretçiler"],
 "back-home":["← На главную","← Ana Sayfaya Dön"],
 "back-products":["← К продукции","← Ürünlere Dön"],
 "factory-title":["Мощь завода","Fabrika Gücü"],
 "factory-sub":["Передовая производственная база: 3 автоматические линии, цех 16 000 м² и строгий контроль качества.","3 otomatik üretim hattı, 16.000 m² atölye ve sıkı kalite kontrole sahip gelişmiş üretim üssü."],
 "factory-capacity-title":["Производственные линии","Üretim Hatları"],
 "factory-rd-title":["НИОКР и контроль качества","Ar-Ge ve Kalite Kontrol"],
 "factory-rd-desc":["Выделенная команда НИОКР с современным испытательным оборудованием гарантирует, что каждая партия соответствует международным стандартам до отгрузки.","Gelişmiş test ekipmanlarına sahip özel Ar-Ge ekibi, her partinin sevkiyattan önce uluslararası standartlara uygun olmasını sağlar."],
 "factory-tour-title":["Заводские объекты","Fabrika Tesisleri"],
 "about-p2":["На нашем заводе площадью **16 000+ м²** работают **3 полностью автоматизированные производственные линии** и более **100 сотрудников**; мы обслуживаем клиентов в горной, тоннельной и строительной отраслях в **30+ странах**, включая Россию, Турцию, Индонезию, ЮАР, Чили, Вьетнам, Перу, Польшу и Бразилию.","**16.000+ m²** fabrika alanımızda, **3 tam otomatik üretim hattı** ve **100+ çalışanımızla**; madencilik, tünel ve inşaat sektörlerine **30+ ülkede** (Rusya, Türkiye, Endonezya, Güney Afrika, Şili, Vietnam, Peru, Polonya ve Brezilya dâhil) hizmet veriyoruz."],
 "about-p3":["Наша продукция применяется при креплении угольных штреков, поддержке тоннелей, стабилизации откосов, анкеровании фундаментов и в гражданских инженерных проектах по всему миру.","Ürünlerimiz dünya çapında kömür madeni galeri boltlamasında, tünel desteğinde, şev stabilizasyonunda, temel ankrajında ve sivil mühendislik projelerinde kullanılmaktadır."],
}

NEW_DICT = {
 "cta-together-title":["Let's work together","携手合作共赢","Давайте работать вместе","Birlikte çalışalım"],
 "cta-together-desc":["Contact us for product recommendations and free samples.","联系我们获取产品建议与免费样品。","Свяжитесь с нами за рекомендациями по продукции и бесплатными образцами.","Ürün önerileri ve ücretsiz numuneler için bizimle iletişime geçin."],
 "cta-find-title":["Can't find what you need?","找不到需要的产品？","Не нашли то, что нужно?","İhtiyacınız olanı bulamadınız mı?"],
 "cta-find-desc":["Custom formulations and OEM service available. Talk to us.","支持定制配方与 OEM 代工，欢迎咨询。","Доступны индивидуальные формулы и OEM-сервис. Свяжитесь с нами.","Özel formülasyon ve OEM hizmeti mevcuttur. Bize ulaşın."],
 "prod-resin-capsule-desc":["Polyester resin capsules for mine bolting, tunnel support & slope stabilization.","用于煤矿支护、隧道加固与边坡稳定的聚酯树脂胶囊。","Полиэфирные смоляные капсулы для крепления шахт, поддержки тоннелей и стабилизации откосов.","Maden boltlama, tünel desteği ve şev stabilizasyonu için polyester reçine kapsülleri."],
 "prod-epoxy-desc":["Two-component epoxy for structural anchoring. Cures underwater.","用于结构锚固的双组分环氧，可水下固化。","Двухкомпонентный эпоксид для конструкционного анкерования. Отверждается под водой.","Yapısal ankraj için iki bileşenli epoksi. Suyun altında kür olur."],
 "prod-mg-resin-desc":["Unsaturated polyester resin for capsule manufacturing & grouting.","用于胶囊制造与注浆的不饱和聚酯树脂。","Ненасыщенная полиэфирная смола для производства капсул и инъектирования.","Kapsül üretimi ve enjeksiyon için doymamış polyester reçine."],
 "prod-frp-rod-desc":["Complete system: rods, plates, nuts & inner bags. Fire-resistant & anti-static.","完整系统：杆体、托盘、螺母及内袋，阻燃抗静电。","Полная система: стержни, шайбы, гайки и внутренние пакеты. Огнестойкие и антистатические.","Tam sistem: çubuklar, plakalar, somunlar ve iç torbalar. Alev geciktirici ve antistatik."],
 "prod-apps-title":["Applications","应用场景","Области применения","Uygulama Alanları"],
 "prod-features-title":["Key Features","核心优势","Ключевые преимущества","Temel Özellikler"],
 "prod-resin-capsule-apps":["Mine roadway bolting, tunnel support, slope stabilization, foundation anchoring, rock reinforcement in civil and mining engineering projects.","煤矿巷道支护、隧道加固、边坡稳定、基础锚固，以及土木与矿山工程中的岩石加固。","Крепление угольных штреков, поддержка тоннелей, стабилизация откосов, анкерование фундаментов, усиление породы в гражданском и горном строительстве.","Maden galerisi boltlama, tünel desteği, şev stabilizasyonu, temel ankrajı ve sivil/maden mühendisliği projelerinde kaya takviyesi."],
 "prod-epoxy-apps":["Structural steel bonding, cracked concrete repair, rebar anchoring, heavy-duty fixings in construction and infrastructure.","钢结构粘结、混凝土裂缝修补、钢筋锚固，以及建筑与基础设施中的重型固定。","Соединение стальных конструкций, ремонт трещиноватого бетона, анкерование арматуры, тяжёлые крепления в строительстве и инфраструктуре.","Yapısal çelik yapıştırma, çatlamış beton onarımı, donatı ankrajı ve inşaat/altyapıda ağır yük sabitleme."],
 "prod-mg-resin-apps":["Base resin for capsule manufacturing, grouting, and chemical anchoring in mining and construction.","用于胶囊制造、注浆及矿山与建筑化学锚固的基体树脂。","Базовая смола для производства капсул, инъектирования и химического анкерования в горном деле и строительстве.","Kapsül üretimi, enjeksiyon ve madencilik/inşaatta kimyasal ankraj için baz reçine."],
 "prod-frp-rod-apps":["Mine roof bolting, tunnel and slope support, corrosive or electrically-sensitive environments requiring non-metallic rods.","煤矿顶板支护、隧道与边坡加固，以及需要非金属杆体的腐蚀或电气敏感环境。","Крепление кровли шахт, поддержка тоннелей и откосов, коррозионные или электрочувствительные среды, требующие неметаллических стержней.","Maden tavan boltlama, tünel ve şev desteği ile kimyasal/nemli ve elektrik hassas ortamlar için metal olmayan çubuklar."],
}

# warnings
for k in RU_TR:
    if k not in ORIG:
        print("  WARN RU_TR key not in ORIG:", k)
for k in ORIG:
    if k not in RU_TR:
        print("  WARN ORIG key missing RU_TR:", k)

# ---------- rebuild LANG_DATA ----------
def jq(s): return json.dumps(s, ensure_ascii=False)
lines = []
allkeys = ORDER + [k for k in NEW_DICT if k not in ORDER]
for k in allkeys:
    if k in NEW_DICT:
        en,zh,ru,tr = NEW_DICT[k]
    else:
        en,zh = ORIG[k]
        if k in EN_OVERRIDE:
            en = EN_OVERRIDE[k]
        ru,tr = RU_TR.get(k, ['', ''])
    lines.append('  "%s":{"en":%s,"zh":%s,"ru":%s,"tr":%s},' % (k, jq(en), jq(zh), jq(ru), jq(tr)))
new_block = 'var LANG_DATA = {\n' + '\n'.join(lines) + '\n};'

html = html.replace('\x01', '')
m2 = re.search(r'var LANG_DATA\s*=\s*\{.*?\n\};', html, re.S)
if not m2:
    print("  !! LANG_DATA block not found!")
else:
    html = html[:m2.start()] + new_block + html[m2.end():]

open(PATH, 'w', encoding='utf-8').write(html)

# ---------- report ----------
used_now = set(re.findall(r'data-i18n="([^"]*)"', html))
print("Wired elements now:", len(used_now))
allk = list(ORDER) + list(NEW_DICT)
missing = [k for k in allk if k not in used_now]
print("Keys WITHOUT a wired element:", missing)
print("LANG_DATA keys total:", len(allkeys))
