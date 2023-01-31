
from lxml import html
import requests
from tqdm import tqdm

from wk.kanji import Kanji, Radical, Reading
from wk.vocab import Vocab


def get_urls(category):
    urls = []
    difficulties = ['pleasant', 'painful', 'death', 'hell', 'paradise', 'reality']
    for d in difficulties:
        category_url = f'https://www.wanikani.com/{category}?difficulty={d}'
        page = requests.get(category_url)
        tree = html.fromstring(page.content)

        grid_elem = '//ul[@class="character-grid__items"]/li/a'
        for i, k in enumerate(tree.xpath(grid_elem)):
            kpart = k.attrib['href']
            kname = k[0].text.strip()
            kurl = f'https://www.wanikani.com/{kpart}'
            urls.append(kurl)
    return urls


def get_kanji_urls():
    return get_urls(category='kanji')


def get_vocab_urls():
    return get_urls(category='vocabulary')


def index_kanji():
    return { extract_hash(url): extract_kanji(url) for url in tqdm(get_kanji_urls()) }

def index_vocab():
    return { extract_hash(url): extract_vocab(url) for url in tqdm(get_vocab_urls()) }


def extract_hash(url):
    return url[url.rfind('/')+1:]



def extract_kanji(url):
#    print(url)
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # Extract Level Information
#    for r in tree.xpath('//a[@class="level-icon"]/text()'):
    for r in tree.xpath('//a[@class="page-header__icon page-header__icon--level"]/text()'):
        level = int(r)
#        print(level)

    # Extract Kanji symbol Information
#    for r in tree.xpath('//span[@class="kanji-icon"]/text()'):
    for r in tree.xpath('//span[@class="page-header__icon page-header__icon--kanji"]/text()'):
        symbol = r

    # Extract Kanji meaning information
#    for r in tree.xpath('//span[@class="kanji-icon"]/../text()'):
    for r in tree.xpath('//span[@class="page-header__title-text page-header__title-text--centered"]/../text()'):
        meaning = r.strip()

    # Extract pronunciation information      /li/a/parent/p/text()
    readings = []
    for reading in ['On’yomi', 'Kun’yomi', 'Nanori']:
        for r in tree.xpath(f"//h3[contains(text(),'{reading}')]/../p/text()"):
            readings.append(Reading(label=reading.lower(),
                                    sounds=r.strip().split(",")))
    # Extract Radicals
    radicals = []
    for r in tree.xpath('//ul[@class="alt-character-list"]/li/a'):
        rname = r.attrib['href']
        rname = rname[rname.rindex('/')+1:]
        rchar = r[0].text.strip()
        radicals.append(Radical(rname, rchar))

    # Visually Similar Kanji
    similar_kanji = []
    for r in tree.xpath('//section[@id="similar-subjects"]/ul/li/a/span/text()'):
        similar_kanji.append(r)
    return Kanji(symbol, 
                 meaning, 
                 readings, 
                 radicals, 
                 level=level, 
                 similar=similar_kanji)


def extract_vocab(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # Extract Level Information
    for r in tree.xpath('//a[@class="page-header__icon page-header__icon--level"]/text()'):
        level = int(r)

    # Extract Kanji symbol Information
    for r in tree.xpath('//span[@class="page-header__icon page-header__icon--vocabulary"]/text()'):
        symbol = r

    # Extract Kanji meaning information
    meaning_elems = tree.xpath('//p[@class="subject-section__meanings-items"]/text()')
    meaning = meaning_elems[0].strip()
    if len(meaning_elems) == 2:
        word_types = meaning_elems[1].strip().split(",")
        meanings = meaning.split(",")
    else:
        alternatives = meaning_elems[1].strip()
        word_types = meaning_elems[2].strip().split(",")
        meanings = meaning.split(",") + alternatives.split(",")
    
    meanings = [m.strip() for m in meanings]
    word_types = [w.strip() for w in word_types]


    # Extract pronunciation information      /li/a/parent/p/text()
    readings = []
    for r in tree.xpath('//div[@class="subject-readings-with-audio__reading"]/text()'):
        readings.append(r.strip())
    
    # Extract usage patterns
    patterns = []
    for p in tree.xpath('//div[@class="subject-collocations__collocation"]'):
        pattern_pair = p.xpath('div[@class="subject-collocations__collocation-text"]/text()')
        patterns.append((pattern_pair[0], pattern_pair[1]))

    
    kanjis = []
    for k in tree.xpath('//a[@class="character-item character-item--kanji"]'):
            kurl = k.attrib['href']
            kcode = kurl[kurl.rindex('/')+1:].strip()
            kanjis.append(kcode)
    
    return Vocab(symbol, 
                 meanings, 
                 readings, 
                 kanjis,
                 word_types, 
                 level=level,
                 patterns=patterns)


if __name__ == "__main__":
#     url = 'https://www.wanikani.com//kanji/%E4%B8%8A'
#     k = extract_kanji(url)
#     print(k)
    
#     kd = index_kanji()
#     print(kd)

#     for url in get_kanji_urls():
#         print(url)
    
#     print("--------")
#     for url in get_vocab_urls():
#         print(url)
    
#     k = index_kanji()
#    v = index_vocab()
 
    v = extract_vocab('https://www.wanikani.com//vocabulary/%E9%A3%B2%E3%81%BF%E7%89%A9')
    print(v)
    print(v.patterns[0])
    print(v.kanjis)
    print(v.readings)
        

        
        
        
        
        
        
        
        
        
#             difficulties = ['pleasant'] #, 'painful', 'death', 'hell', 'paradise', 'reality']
#     for d in difficulties:
#         kanjis_url = f'https://www.wanikani.com/kanji?difficulty={d}'
#         print(kanjis_url)

#         page = requests.get(kanjis_url)
#         tree = html.fromstring(page.content)

#         print("Iterating over tree")
#         print(kanjis_url)
#         grid_elem = '//ul[@class="character-grid__items"]/li/a'
#         # '//ul[@class="single-character-grid"]/li/a'
#         for i, k in tqdm(enumerate(tree.xpath(grid_elem))):
#             print(k)
#             kpart = k.attrib['href']
#             kname = k[0].text.strip()
#             kurl = f'https://www.wanikani.com/{kpart}'
#             print(kurl)
#             kanji_dict[kname] = extract_kanji(kurl)
#             if i > 10:
#                 break
# #            wk_dict[kname] = rads
#     return kanji_dict

