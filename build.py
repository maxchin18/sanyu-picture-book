# -*- coding: utf-8 -*-
"""Generates index.html for the 三魚海味探索繪本 site from the page data below."""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))

# start time (s) of each page in the film; index 0 is the title card
STARTS = [0, 3.9, 21.55, 45.87, 71.35, 91.46, 112.19, 139.22, 162.03, 185.31, 213.33, 236.03, 253.84, 267.32, 292.31, 311.21, 333.11]

PAGES = [
 ("喜宴上的翻魚禁忌", ["在屏東東港的喜宴上，小軒想要翻魚，爸爸說：「先別翻魚！」", "小軒歪著頭問爸爸為什麼?爸爸微笑的說：「這是漁村的禁忌，傳說翻魚等於翻船。」"]),
 ("東港飯湯", ["好奇心滿滿的小軒決定展開探索之旅，前往屏東東港，品嚐當地特色午餐「東港飯湯」。", "東港飯湯包含：鮪魚肉、蝦猴、魚丸、魚板、蝦子、花枝、蚵仔、竹筍、芹菜等，搭配白飯與高湯，令人回味無窮。"]),
 ("第一鮪進港", ["來到東港漁港魚市場，熱鬧景象吸引了小軒的目光，他見證了叫賣第一尾黑鮪魚進港盛大的場面，象徵揭開一年一度黑鮪魚季序幕。", "每年四月到六月是東港黑鮪魚季的時期，黑鮪魚帶來漁業豐沛的收入及吸引觀光人潮，也讓黑鮪魚成為東港三寶之首。"]),
 ("黑鮪魚游泳健將", ["小軒仔細觀察著黑鮪魚的模型，發現這種魚不僅體型巨大，還是海洋中的游泳健將。", "當黑鮪魚察覺到危險或要追捕獵物時，會降下背鰭，配合魚尾強而有力的擺動，以極快的速度前進。"]),
 ("延繩釣漁法", ["東港漁港是全國排名前三大漁港，有近海及遠洋漁船，漁船種類從竹筏到CT6的玻璃纖維船都有。", "船長向小軒介紹「延繩釣漁法」，這就是「放緄仔（pàng kún á）」，一場充滿智慧與勇氣的冒險。"]),
 ("鮪魚飲食文化", ["香港人稱鮪魚為「吞拿」，日本人稱鮪魚為「鮪（まぐろ／MAGURO）」，臺語稱作「串仔（tshǹg-á）」，而「トロ（TORO）」特指鮪魚富含脂肪的腹部。", "黑鮪魚經濟價值高，尤其第一鮪的價格通常會高達每公斤一萬元以上，所以整條魚至少價值上百萬元以上。"]),
 ("東隆宮與漁村信仰", ["小軒跟著爺爺逛東隆宮，小軒抬頭一看發現匾額上出現「蚵仔寮」的地名，令他感到十分疑惑。", "爺爺說：「過去烏魚汛期間，高雄蚵仔寮有些漁民會特地前來東港，恭請溫王爺回去坐鎮，保佑漁民平安與豐收。」"]),
 ("蚵仔寮魚市場", ["蚵仔寮過去是傳統漁村，如今轉型為熱鬧的觀光漁港。來到蚵仔寮，小軒走訪魚市場，看著各式各樣的海鮮，感受當地產業轉型的活力。", "小軒想起往年冬天在家享用的烏魚米粉，鮮美的滋味讓他難以忘懷。"]),
 ("烏魚冬季洄游", ["每年冬季，烏魚群都會從北方洄游到蚵仔寮附近海域，與討海人精彩的搏鬥，並成為當地漁村重要的「烏金」。", "當烏魚察覺到危險時會往下游竄或跳出水面，所以漁夫們發展出一套圍捕魚群的特殊漁法。不過要面對龐大烏魚群強而有力的抵抗，仍是一件危險的工作。"]),
 ("老漁夫的竹筏故事", ["蚵仔寮的夜晚，老漁夫講起早期烏魚汛期來臨時候，他們搭起臨時的藏仔寮，作為一起生活的臨時工寮。", "早期漁民乘坐竹筏出海，以「烏藏網」合力圍捕烏魚群，面對洶湧風浪的冒險故事，讓小軒深深著迷不已。"]),
 ("雙船合作圍捕", ["小軒腦海中浮現著漁筏追捕烏魚的景象，漸漸喜歡上蚵仔寮。", "在機動漁船盛行的年代，漁夫們採用兩艘船為一組協力的方式，使用一張「巾著網」圍捕烏魚群。"]),
 ("烏魚的團隊行動", ["烏魚的集體行動令人著迷又興奮，烏魚是漁夫們可敬的對手。", "小軒看著烏魚胸鰭上的特有藍點，象徵著團隊的臂章。"]),
 ("大潭養殖魚塭", ["氣候變遷導致海水暖化，野生烏魚主要漁場逐漸北移，且烏魚數量年年減少，於是人們開始將烏魚放養在魚塭中。", "結束蚵仔寮的漁村探索之旅，小軒回到東港大潭，參觀龍虎斑的養殖魚塭，明白了養殖業，是自己家鄉的重要產業之一。"]),
 ("龍虎斑的身世", ["原來龍虎斑的爸爸是龍膽石斑，媽媽是老虎斑，這讓小軒對這種混種魚充滿了好奇。", "大潭社區養殖場是引入大鵬灣的海水進來養殖龍虎斑，至少要飼養十個月才能捕撈。"]),
 ("龍虎斑紙包魚料理", ["烤龍虎斑？小軒心裡想著：這麼厚的魚，要怎麼烤才會熟呢？", "在廚房裡，小軒跟著姑姑學做龍虎斑的紙包魚料理。將魚片、檸檬與香料等巧妙地結合，變成一道美味又有趣的海鮮料理。"]),
 ("迎王祭典與星空", ["到最後，小軒參與了東港迎王平安祭典，看著巨大的王船在燃燒中消逝，期待千歲爺將所有的厄運都帶走。", "直到深夜，化王船的灰燼火花慢慢消失在藍色的星空中，遊天河的王船彷彿化變了魚的星座。這次探索讓他體會到，海洋文化已經成為人們生活中重要的一部分，連結著過去、現在到未來。"]),
]

# chapter grouping shown above the pages
CHAPTERS = [
 ("序章", "東港", 1, 2),
 ("黑鮪魚", "東港", 3, 6),
 ("烏魚", "蚵仔寮", 7, 12),
 ("龍虎斑", "大潭", 13, 15),
 ("終章", "東港", 16, 16),
]

def chapter_of(n):
    for name, place, a, b in CHAPTERS:
        if a <= n <= b:
            return name, place
    return "", ""

def mmss(t):
    t = int(round(t))
    return f"{t//60}:{t%60:02d}"

e = html.escape

chips = "\n".join(
    f'<li><button class="chip" data-t="{STARTS[i]+0.4:.2f}" data-page="{i}"><span class="chip-n">{i:02d}</span>'
    f'<span class="chip-t">{e(PAGES[i-1][0])}</span><span class="chip-time">{mmss(STARTS[i])}</span></button></li>'
    for i in range(1, 17))

pages_html = []
for i, (title, paras) in enumerate(PAGES, 1):
    ch, place = chapter_of(i)
    side = "left" if i % 2 else "right"
    body = "\n".join(f"<p>{e(p)}</p>" for p in paras)
    pages_html.append(f'''
<article class="page reveal {side}" id="p{i:02d}" data-page="{i}">
  <figure class="page-fig">
    <button class="fig-btn" data-open="{i}" aria-label="放大閱讀第 {i} 頁">
      <img src="img/p{i:02d}.webp" srcset="img/p{i:02d}_s.webp 640w, img/p{i:02d}.webp 1600w"
           sizes="(max-width: 860px) 100vw, 58vw" width="1600" height="1130" loading="lazy" decoding="async"
           alt="第 {i} 頁插圖：{e(title)}">
    </button>
  </figure>
  <div class="page-text">
    <div class="page-meta"><span class="script">No. {i:02d}</span><span class="tag">{e(ch)} · {e(place)}</span></div>
    <h3>{e(title)}</h3>
    {body}
    <div class="page-actions">
      <button class="btn-line ghost" data-open="{i}">放大閱讀</button>
    </div>
  </div>
</article>''')

fish = [
 ("黑鮪魚", "Bluefin Tuna", "東港三寶之首，每年四到六月迎來黑鮪魚季；海洋中的游泳健將。", 3, 4),
 ("烏魚", "Grey Mullet", "冬季洄游的「烏金」，蚵仔寮漁民以竹筏、雙船合作圍捕。", 9, 12),
 ("龍虎斑", "Hybrid Grouper", "爸爸是龍膽石斑、媽媽是老虎斑，在大潭魚塭飼養十個月以上。", 13, 14),
]
fish_html = "\n".join(f'''
<a class="fish-card reveal" href="#p{a:02d}">
  <div class="fish-img"><img src="img/p{img:02d}_s.webp" alt="" loading="lazy" width="640" height="452"></div>
  <div class="fish-body">
    <span class="script">{e(en)}</span>
    <h3>{e(zh)}</h3>
    <p>{e(desc)}</p>
    <span class="more">從第 {a} 頁讀起 →</span>
  </div>
</a>''' for zh, en, desc, a, img in fish)

data_js = json.dumps([{"t": t, "p": p} for t, p in PAGES], ensure_ascii=False)
starts_js = json.dumps(STARTS)

tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
out = (tpl.replace("{{CHIPS}}", chips)
          .replace("{{PAGES}}", "\n".join(pages_html))
          .replace("{{FISH}}", fish_html)
          .replace("{{DATA}}", data_js)
          .replace("{{STARTS}}", starts_js))
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print("index.html written", len(out))
