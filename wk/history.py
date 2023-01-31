from datetime import datetime, timedelta, timezone
import os
import pickle
import pathlib


class AnswerHistory:
                   
    def __init__(self, path_to_cache='./cache/', force_rebuild=False):
        # Set TimeZone (JST)
        self.timezone = timezone(timedelta(hours=+9))

        # if path exists, load
        cache_filename = path_to_cache + "history.pickle.txt"
        self.cache_filename = cache_filename
        file = pathlib.Path(cache_filename)
        if file.exists() and not force_rebuild:
            print("Cache exist; should load")
            with open(cache_filename, "rb") as pickleFile:
                self.history = pickle.load(pickleFile)
        else:
            print("Building cache...")
            self.history = dict()
    
    
    def dumper(self, obj):
        try:
            return obj.toJSON()
        except:
            return obj.__dict__

        
    def cache(self, cache_filename):
        if not os.path.exists(os.path.dirname(cache_filename)):
            os.makedirs(os.path.dirname(cache_filename))
        with open(cache_filename, 'wb') as pickleFile:
            pickle.dump(self.history, pickleFile)

            
    def update(self, kanji, question_type, got_correct):
        kanji = kanji.symbol
        time = datetime.now(self.timezone)
        if kanji not in self.history:
            self.history[kanji] = dict()
        if question_type not in self.history[kanji]:
            self.history[kanji][question_type] = []
        self.history[kanji][question_type].append((got_correct, time))       
        self.cache(self.cache_filename)

