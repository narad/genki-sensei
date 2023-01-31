import pathlib
import random

from wk.kanji import Kanji, Radical, Reading
import json
import os

import  pickle

from wk.html_parser import index_kanji, index_vocab


class WaniKani():
    
    def __init__(self, path_to_cache='./cache/', force_rebuild=False):
        # if path exists, load
        kanji_cache_filename = path_to_cache + "kanji_pickle.txt"
        vocab_cache_filename = path_to_cache + "vocab_pickle.txt"
        self.kanji = self.load_from_cache(kanji_cache_filename)
        self.vocab = self.load_from_cache(vocab_cache_filename)
        if self.kanji is None or force_rebuild:
            self.kanji = index_kanji()
            self.cache(self.kanji, kanji_cache_filename)
        if self.vocab is None or force_rebuild:
            self.vocab = index_vocab()
            self.cache(self.vocab, vocab_cache_filename)
        self.max_level = 100


    def load_from_cache(self, filename):
        file = pathlib.Path(filename)
        if file.exists():
            print(f"Cache {filename} exists; loading...")
            with open(filename, "rb") as pickleFile:
                 return pickle.load(pickleFile)
        else:
            return None

        
    def dumper(self, obj):
        try:
            return obj.toJSON()
        except:
            return obj.__dict__


    def cache(self, dict_to_cache, cache_filename):
        if not os.path.exists(os.path.dirname(cache_filename)):
            os.makedirs(os.path.dirname(cache_filename))
        with open(cache_filename, 'wb') as pickleFile:
            pickle.dump(dict_to_cache, pickleFile)


    def get_item(self, symbol):
        return self.kanji[symbol]
        

    def get_batch(self, n):
        return random.sample(list(self.wk_dict.values()), n)

    
    def get_kanjis(self):
        return self.kanji.values()

    
    def get_kanjis_by_level(self, level):
        return [k for k in self.kanji.values() if k.level == level]

    
    def get_kanjis_by_max_level(self, level):
        return [k for k in self.kanji.values() if k.level <= level]

    
    def set_max_level(self, max_level):
        self.max_level = max_level

        
    def next_kanji(self):
        return random.choice([k for k in list(self.kanji.values()) 
                              if k.level <= self.max_level])
        
    def next_vocab(self):
        return random.choice([k for k in list(self.vocab.values()) 
                              if k.level <= self.max_level])
        

    def next_by_similarity(self, threshold=2):
        choices = [k for k in list(self.kanji.values()) 
                              if k.level <= self.max_level and 
                              len(k.similar) > threshold]
        print(len(choices))
        print(choices)
        
        return random.choice(choices)
    



                
    def index_vocab(self):
        difficulties = ['pleasant', 'painful', 'death', 'hell', 'paradise', 'reality']
        for d in difficulties:
            kanjis_url = f'https://www.wanikani.com/vocabulary?difficulty={d}'
            print(kanjis_url)

            page = requests.get(kanjis_url)
            tree = html.fromstring(page.content)

            for k in tqdm(tree.xpath('//ul[@class="single-character-grid"]/li/a')):
                kpart = k.attrib['href']
                kname = k[0].text.strip()
                kurl = f'https://www.wanikani.com/{kpart}'
                rads = self.extract_vocab_info(kurl)
                self.wk_dict[kname] = rads



  
    def extract_vocab_info(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        
        # Extract Level Information
        for r in tree.xpath('//a[@class="level-icon"]/text()'):
            level = int(r)        
            
        # Extract Kanji symbol Information
        for r in tree.xpath('//span[@class="kanji-icon"]/text()'):
            symbol = r
            
        # Extract Kanji meaning information
        for r in tree.xpath('//span[@class="kanji-icon"]/../text()'):
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

  

        
    
    
    #         for r in tree.xpath('//section[@id="similar-subjects"]/ul/li/span[@class="character"]/text()'):

    
    
#       <section id="similar-subjects">
#           <h2>Visually Similar Kanji</h2>
#           <ul class="single-character-grid multi-character-grid-extra-styling-767px">
#             <li class="kanji-795 locked character-item">
#               <span lang="ja" class="item-badge"></span>
#               <a href="/kanji/%E8%82%B2">
#               <span class="character" lang="ja">育</span>
#               <ul>
#                 <li>いく</li>
#                 <li>Nurture</li>
                
                
                
                
                
                
                
        
# <div class="span4 ">
#                 <h3>On’yomi</h3>
#                 <p lang="ja">
#                   こう
#                 </p>
# </div>              <div class="span4 muted-content">
#                 <h3>Kun’yomi</h3>
#                 <p lang="ja">
#                   がえんじ
#                 </p>
# </div>              <div class="span4 muted-content">
#                 <h3>Nanori</h3>
#                 <p lang="ja">
#                   None
#                 </p>
                
                
                
#   <a class="level-icon" href="/level/51">51</a> <span class="kanji-icon" lang="ja">肯</span> Agreement        
        
        
#             <a class="level-icon" href="/level/51">51</a> <span class="kanji-icon" lang="ja">肯</span> Agreement
        
        
# <li class="kanji-1147 locked character-item">
#   <span lang="ja" class="item-badge"></span>
#   <a href="/kanji/%E7%9C%81">
#     <span class="character" lang="ja">
#         省
#     </span>
#     <ul>



#           <h2>Radical Combination</h2>
#           <ul class='alt-character-list'>
#               <li class="radical-44">
#                 <span lang="ja" class="item-badge"></span>
#                 <a href="/radicals/stop">
#                   <span class="radical-icon locked" lang="ja">
#                     止
# </span>                  Stop
# </a></li>              <li class="radical-43">
#                 <span lang="ja" class="item-badge"></span>
#                 <a href="/radicals/moon">
#                   <span class="radical-icon locked" lang="ja">
#                     月
# </span>                  Moon
# </a></li>          </ul>


#    break
#tree
#prices = tree.xpath('//li[@class="kanji-2123 locked character-item"]/a')
#print(prices[0].attrib['href'])

#kurl = 

# for p in tree.findall('.//kanji-2123 locked character-item'):
#     print(p)
# print(kanji2rads)
# print("done")