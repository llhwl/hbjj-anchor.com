# -*- coding: utf-8 -*-
import re, json

PATH = 'index.html'
raw = open(PATH, encoding='utf-8').read()
html = raw

def jq(s): return json.dumps(s, ensure_ascii=False)

# ---------- CSS additions (before </style>) ----------
CSS = """
.dot{list-style:none;margin:8px 0;padding:0}
.dot li{padding:7px 0 7px 20px;position:relative;font-size:.85rem;color:#5a5a7a;line-height:1.65}
.dot li:before{content:"";position:absolute;left:0;top:12px;width:8px;height:8px;border-radius:50%;background:#0056b3}
.timeline{list-style:none;margin:10px 0;padding:0 0 0 16px;border-left:3px solid #0056b3}
.timeline li{padding:8px 0 8px 14px;position:relative;font-size:.85rem;color:#5a5a7a;line-height:1.7}
.timeline li:before{content:"";position:absolute;left:-22px;top:13px;width:11px;height:11px;border-radius:50%;background:#fff;border:3px solid #0056b3}
.timeline b{color:#0f1b2d;margin-right:6px}
"""
si = html.find('</style>')
if si < 0:
    print("  !! no </style>"); 
else:
    html = html[:si] + CSS + html[si:]

# ---------- HTML: ABOUT page ----------
ABOUT_GALLERY = """
<h3 data-i18n="about-gallery-title">Our Factory</h3>
<div class="gal">
<div class="gcard"><a href="images/factory-gate.jpg" target="_blank" rel="noopener"><img src="images/factory-gate.jpg" loading="lazy" alt="Jinjiu factory gate"></a><span data-i18n="about-gallery-1">Factory Gate</span></div>
<div class="gcard"><a href="images/factory-workshop.jpg" target="_blank" rel="noopener"><img src="images/factory-workshop.jpg" loading="lazy" alt="Production workshop"></a><span data-i18n="about-gallery-2">Production Workshop</span></div>
<div class="gcard"><a href="images/factory-warehouse-ready.jpg" target="_blank" rel="noopener"><img src="images/factory-warehouse-ready.jpg" loading="lazy" alt="Finished goods warehouse"></a><span data-i18n="about-gallery-3">Finished Goods Warehouse</span></div>
<div class="gcard"><a href="images/factory-packaging-workshop.jpg" target="_blank" rel="noopener"><img src="images/factory-packaging-workshop.jpg" loading="lazy" alt="Packaging workshop"></a><span data-i18n="about-gallery-4">Packaging Workshop</span></div>
<div class="gcard"><a href="images/factory-loading-truck.jpg" target="_blank" rel="noopener"><img src="images/factory-loading-truck.jpg" loading="lazy" alt="Export loading"></a><span data-i18n="about-gallery-5">Export Loading</span></div>
<div class="gcard"><a href="images/jinjiu-office-building.jpg" target="_blank" rel="noopener"><img src="images/jinjiu-office-building.jpg" loading="lazy" alt="Office and R&D building"></a><span data-i18n="about-gallery-6">Office &amp; R&amp;D Building</span></div>
</div>
"""

ABOUT_HISTORY_VISION = """
<h3 data-i18n="about-history-title">Our Development</h3>
<ul class="timeline">
<li><b data-i18n="about-his-year-1">2004</b> <span data-i18n="about-his-1">Founded in Huaibei, Anhui; first resin anchor capsule production line.</span></li>
<li><b data-i18n="about-his-year-2">2010</b> <span data-i18n="about-his-2">Expanded to FRP anchor rods and MG resin; MA safety certification.</span></li>
<li><b data-i18n="about-his-year-3">2015</b> <span data-i18n="about-his-3">Certified to ISO 9001 / 14001 / 45001; built automated production lines.</span></li>
<li><b data-i18n="about-his-year-4">2020</b> <span data-i18n="about-his-4">Products exported to 30+ countries across mining and tunneling markets.</span></li>
<li><b data-i18n="about-his-year-5">Today</b> <span data-i18n="about-his-5">Full-system anchoring solutions and OEM service for global clients.</span></li>
</ul>
<h3 data-i18n="about-vision-title">Future Outlook</h3>
<p style="font-size:.85rem;color:#5a5a7a;line-height:1.7;margin-bottom:10px" data-i18n="about-vision-desc">We keep investing in automation and green manufacturing, broaden our product range, and build long-term local partnerships in more countries.</p>
<ul class="dot">
<li data-i18n="about-vision-1">Smarter, lower-carbon production</li>
<li data-i18n="about-vision-2">New applications: geothermal, hydropower, foundation</li>
<li data-i18n="about-vision-3">Local service &amp; stock in key markets</li>
</ul>
"""

# insert gallery before about-capacity
a = html.find('<h3 data-i18n="about-capacity">')
if a < 0: print("  !! MISS about-capacity anchor")
else: html = html[:a] + ABOUT_GALLERY + html[a:]

# insert history+vision before the CTA wrapper div
b = html.find('<div style="text-align:center;background:#f0f4f8;padding:20px;border-radius:10px;margin-top:24px">')
if b < 0: print("  !! MISS about CTA anchor")
else: html = html[:b] + ABOUT_HISTORY_VISION + html[b:]

# ---------- HTML: FACTORY page ----------
FACTORY_EQUIP = """
<h3 data-i18n="factory-equip-title">Automated Production Equipment</h3>
<p style="font-size:.85rem;color:#5a5a7a;line-height:1.7;margin-bottom:12px" data-i18n="factory-equip-desc">Three fully automated lines cover dosing, mixing, filling, sealing and packaging with minimal manual touch, ensuring stable quality and high output.</p>
<div class="row2">
<div><img src="images/factory-equipment-transfer.jpg" style="border-radius:8px;width:100%" alt="Automated equipment and technology transfer"></div>
<div><img src="images/factory-workshop.jpg" style="border-radius:8px;width:100%" alt="Production workshop"></div>
</div>
<ul class="dot">
<li data-i18n="factory-equip-1">Automatic dosing &amp; mixing system</li>
<li data-i18n="factory-equip-2">High-speed capsule filling &amp; sealing</li>
<li data-i18n="factory-equip-3">Robotic carton packaging &amp; palletizing</li>
<li data-i18n="factory-equip-4">Real-time process monitoring</li>
</ul>
"""

FACTORY_QC = """
<h3 data-i18n="factory-qc-title">Quality Control Capability</h3>
<p style="font-size:.85rem;color:#5a5a7a;line-height:1.7;margin-bottom:12px" data-i18n="factory-qc-desc">From raw material to finished goods, every batch passes incoming inspection, in-process control, finished-product testing and third-party verification.</p>
<ul class="dot">
<li data-i18n="factory-qc-1">Incoming raw material inspection</li>
<li data-i18n="factory-qc-2">In-process sampling &amp; gel-time checks</li>
<li data-i18n="factory-qc-3">Pull-out &amp; bond strength testing</li>
<li data-i18n="factory-qc-4">SGS third-party inspection on request</li>
</ul>
"""

# insert equipment before factory-capacity-title
c = html.find('<h3 data-i18n="factory-capacity-title">')
if c < 0: print("  !! MISS factory-capacity anchor")
else: html = html[:c] + FACTORY_EQUIP + html[c:]

# insert QC before factory-tour-title
d = html.find('<h3 data-i18n="factory-tour-title">')
if d < 0: print("  !! MISS factory-tour anchor")
else: html = html[:d] + FACTORY_QC + html[d:]

# ---------- LANG_DATA: add new keys (en/zh/ru/tr) ----------
NEW = {
 "about-gallery-title":["Our Factory","厂容厂貌","Завод компании","Fabrikamız"],
 "about-gallery-1":["Factory Gate","厂区大门","Проходная завода","Fabrika Kapısı"],
 "about-gallery-2":["Production Workshop","生产车间","Производственный цех","Üretim Atölyesi"],
 "about-gallery-3":["Finished Goods Warehouse","成品仓库","Склад готовой продукции","Hazır Ürün Deposu"],
 "about-gallery-4":["Packaging Workshop","包装车间","Цех упаковки","Paketleme Atölyesi"],
 "about-gallery-5":["Export Loading","出口装车","Погрузка на экспорт","İhracat Yükleme"],
 "about-gallery-6":["Office & R&D Building","办公与研发楼","Офис и НИОКР","Ofis ve Ar-Ge Binası"],
 "about-history-title":["Our Development","发展历程","Наше развитие","Gelişimimiz"],
 "about-his-year-1":["2004","2004","2004","2004"],
 "about-his-1":["Founded in Huaibei, Anhui; first resin anchor capsule production line.","成立于安徽淮北，首条树脂锚固剂生产线。","Основана в Хуайбэй, пров. Аньхой; первый цех смоляных капсул.","Anhui, Huaibei'de kuruldu; ilk reçine ankraj kapsülü hattı."],
 "about-his-year-2":["2010","2010","2010","2010"],
 "about-his-2":["Expanded to FRP anchor rods and MG resin; MA safety certified.","拓展 FRP 锚杆与 MG 树脂，获 MA 安全认证。","Расширение до FRP-стержней и MG-смолы; сертификат MA.","FRP çubukları ve MG reçinesine geçildi; MA sertifikası."],
 "about-his-year-3":["2015","2015","2015","2015"],
 "about-his-3":["Certified to ISO 9001 / 14001 / 45001; built automated production lines.","通过 ISO 9001/14001/45001 认证，建成自动化产线。","Сертификаты ISO 9001/14001/45001; построены автолинии.","ISO 9001/14001/45001 sertifikalı; otomatik hatlar kuruldu."],
 "about-his-year-4":["2020","2020","2020","2020"],
 "about-his-4":["Products exported to 30+ countries across mining and tunneling markets.","产品出口全球 30+ 国家，覆盖矿山与隧道市场。","Продукция экспортируется в 30+ стран (шахты и тоннели).","Ürünler 30+ ülkeye (maden ve tünel) ihraç edildi."],
 "about-his-year-5":["Today","如今","Сегодня","Bugün"],
 "about-his-5":["Full-system anchoring solutions and OEM service for global clients.","为全球客户提供全套锚固方案与 OEM 服务。","Комплексные анкерные решения и OEM для мира.","Küresel müşterilere tam sistem ankraj çözümleri ve OEM."],
 "about-vision-title":["Future Outlook","未来展望","Наши планы","Gelecek Vizyonu"],
 "about-vision-desc":["We keep investing in automation and green manufacturing, broaden our product range, and build long-term local partnerships in more countries.","持续投入自动化与绿色制造，拓展产品应用，在更多国家建立长期本地合作。","Инвестируем в автоматизацию и экологичное производство, расширяем применение.","Otomasyona ve yeşil üretime yatırım yapıyor, uygulamaları genişletiyoruz."],
 "about-vision-1":["Smarter, lower-carbon production","更智能、更低碳的生产","Умное, низкоуглеродное производство","Daha akıllı, düşük karbonlu üretim"],
 "about-vision-2":["New applications: geothermal, hydropower, foundation","新应用：地热、水电、地基锚固","Новые сферы: геотермальная, ГЭС, фундаменты","Yeni kullanımlar: jeotermal, hidrolik, temel"],
 "about-vision-3":["Local service & stock in key markets","重点市场本地化服务与备货","Локальный сервис и склад в ключевых рынках","Ana pazarlarda yerel servis ve stok"],
 "factory-equip-title":["Automated Production Equipment","自动化生产设备","Автоматизированное оборудование","Otomatik Üretim Ekipmanları"],
 "factory-equip-desc":["Three fully automated lines cover dosing, mixing, filling, sealing and packaging with minimal manual touch.","三条自动化产线覆盖配料、混合、灌装、封口与包装，人工干预极少。","Три автолинии: дозирование, смешивание, розлив, запайка, упаковка.","Üç otomatik hat; dozaj, karıştırma, dolum, mühürleme ve paketleme."],
 "factory-equip-1":["Automatic dosing & mixing system","自动配料与混合系统","Автодозирование и смешивание","Otomatik dozaj ve karıştırma"],
 "factory-equip-2":["High-speed capsule filling & sealing","高速胶囊灌装与封口","Высокоскоростная заполнение капсул","Yüksek hızlı kapsül dolum-mühürleme"],
 "factory-equip-3":["Robotic carton packaging & palletizing","机器人纸箱包装与码垛","Робоупаковка и палетирование","Robotlu kutu paketleme-paletleme"],
 "factory-equip-4":["Real-time process monitoring","实时生产监控","Контроль процесса в реальном времени","Gerçek zamanlı süreç izleme"],
 "factory-qc-title":["Quality Control Capability","产品质量把控","Контроль качества","Kalite Kontrol Yeteneği"],
 "factory-qc-desc":["From raw material to finished goods, every batch passes incoming, in-process, finished and third-party checks.","从原料到成品，每批次均经过来料、过程、成品及第三方检验。","От сырья до готовой продукции — входной, текущий, финишный и сторонний контроль.","Hammaddeden bitmiş ürüne; giriş, süreç, bitmiş ve üçüncü taraf denetimi."],
 "factory-qc-1":["Incoming raw material inspection","来料原料检验","Входной контроль сырья","Gelen hammadde denetimi"],
 "factory-qc-2":["In-process sampling & gel-time checks","过程抽检与凝胶时间检测","Текущий контроль и время гелеобразования","Süreç numuneleri ve jel-zamanı kontrolü"],
 "factory-qc-3":["Pull-out & bond strength testing","拉拔与粘结强度测试","Испытания на вырыв и сцепление","Çekme ve yapışma mukavemeti testi"],
 "factory-qc-4":["SGS third-party inspection on request","可按需安排 SGS 第三方检测","Сторонняя инспекция SGS по запросу","Talep üzerine SGS üçüncü taraf denetimi"],
}

m = re.search(r'var LANG_DATA\s*=\s*\{(.*?)\n\s*\};', html, re.S)
if not m:
    print("  !! LANG_DATA block not found!")
else:
    inner = m.group(1)
    inner = re.sub(r',\s*$', '', inner.rstrip())
    entries = ',\n'.join('  "%s":{"en":%s,"zh":%s,"ru":%s,"tr":%s}' % (k, jq(v[0]), jq(v[1]), jq(v[2]), jq(v[3])) for k,v in NEW.items())
    new_block = 'var LANG_DATA = {' + inner + ',\n' + entries + '\n};'
    html = html[:m.start()] + new_block + html[m.end():]

open(PATH, 'w', encoding='utf-8').write(html)

# ---------- report ----------
used = set(re.findall(r'data-i18n="([^"]*)"', html))
new_keys = list(NEW.keys())
missing = [k for k in new_keys if k not in used]
print("New keys defined:", len(new_keys))
print("New keys missing in HTML:", missing)
# verify LANG_DATA has all new keys with ru/tr
ld = re.search(r'var LANG_DATA\s*=\s*\{(.*?)\n\s*\};', html, re.S).group(1)
ld_keys = set(re.findall(r'"((?:[^"\\]|\\.)*)"\s*:\s*\{', ld))
no_ru = [k for k in new_keys if k in ld_keys and ('"ru":' not in ld.split('"'+k+'"')[1].split('}')[0])]
print("All new keys in LANG_DATA:", all(k in ld_keys for k in new_keys))
print("total LANG_DATA keys now:", len(ld_keys))
