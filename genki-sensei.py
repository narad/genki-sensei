#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Magics
try:
    get_ipython().run_line_magic('load_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')
    get_ipython().system(' jupyter nbconvert --to script genki-sensei.ipynb')
    IS_NOTEBOOK=True
except:
    IS_NOTEBOOK=False   
show_html = IS_NOTEBOOK


# In[2]:


from wk.wanikani import WaniKani
from wk.quizzer import ask_question, choose_kanji
from wk.history import AnswerHistory


# In[3]:


get_ipython().system(' pip3 list | grep romkan')


# In[4]:


# ! pip --version
# pip 22.3.1 from /Users/narad/miniforge3/lib/python3.9/site-packages/pip (python 3.9)


# In[ ]:


import romkan


# In[ ]:


max_level = 3


# In[ ]:


# Initialize kanji knowledge
wk = WaniKani(force_rebuild=False)
wk.set_max_level(max_level)
print(f"Loaded {len(wk.get_kanjis())} kanji")
print(f"Loaded {len(wk.vocab)} vocab")

# Initialize user history
history = AnswerHistory()


# In[ ]:


from wk.conjugate import te_form

# for v in wk.vocab.values():
#     try:
#         tf = te_form(v)
#         print(tf)
#         print(v.word_types)
#     except:
#         pass


# In[ ]:


#lkanjis = wk.get_kanjis_by_max_level(max_level)
# for k in lkanjis:
#     print(k)


# ### Select the Type of Review Questions

# In[ ]:


from wk.mode import Mode, all_modes

modes = all_modes + [Mode('mixed', "Mixed")]
def select_mode(dislay_ASCII):
    select_str = "Select Review Mode:\n" +                  "\n".join([f"  {i+1}) {modes[i].pretty_str} " for i in range(len(modes))]) + "\n\n" 
    midx = int(input(select_str))
    assert midx > 0 and midx <= len(modes)+1, "Choice is out of range."
    return modes[midx-1]
    
mode = select_mode(IS_NOTEBOOK)
print(mode)

# Remove the mixed mode from mode list
modes = modes[:-1]


# In[ ]:


# Setup question mix (follow-up)

question_type_distribution = {modes[i].name: 0 for i in range(len(modes)-1)}
#print(question_type_distribution)
if mode.name == "mixed":
    for q in question_type_distribution.keys():
        question_type_distribution[q] = 1.0 / (len(modes)-1)
else:
    question_type_distribution[mode.name] = 1.0

# print("test:")
# print(question_type_distribution)

qpairs = list(question_type_distribution.items())
qtypes   = [q for q,_ in qpairs]
qweights = [w for _,w in qpairs]


# In[ ]:


from IPython.display import HTML

def html_popup(inner_html):
    s  = '<script type="text/Javascript">'
    s += 'var win = window.open("", "Title", "toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=780, height=200, top="+(screen.height-400)+", left="+(screen.width-840));'
    s += 'win.document.body.innerHTML = \'' + inner_html.replace("\n",'\\') + '\';'
    s += '</script>'
    display(HTML(s))

# Show in new Window
#html_popup("Hello")


# In[ ]:


### Quiz Cell ###
from IPython.display import clear_output
import time
import random
from sounds import play_correct, play_incorrect
from IPython.display import display, HTML

i = 0
correct = 0

while True:
    qtype = random.choices(qtypes,
                           weights=qweights,
                           k=1)[0]
    print(type(qtype))
    clear_output(wait=True)
    k = choose_kanji(qtype, 
                     wk)

#    print(f"{i+1}) ", end="")
    is_correct, feedback = ask_question(k, qtype, wk, idx=i+1, show_html=show_html)
    if is_correct:
#        print()
        print("Correct!")
        play_correct()
        correct += 1
    else:
        play_incorrect()
        if show_html:
#            print()
            display(HTML(f"Incorrect.<p>{feedback}"))
        
    # Update the user's progress history
    history.update(k, qtype, is_correct)

    # Wait for user to react to answer
    confirm = input()

    
    i += 1

print(f"\nScore: {correct}/{num_questions}")


# In[ ]:


k.meanings


# In[ ]:


def View(df):
    css = """<style>
    table { border-collapse: collapse; border: 3px solid #eee; }
    table tr th:first-child { background-color: #eeeeee; color: #333; font-weight: bold }
    table thead th { background-color: #eee; color: #000; }
    tr, th, td { border: 1px solid #ccc; border-width: 1px 0 0 1px; border-collapse: collapse;
    padding: 3px; font-family: monospace; font-size: 10px }</style>
    """
    s  = '<script type="text/Javascript">'
    s += 'var win = window.open("", "Title", "toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=780, height=200, top="+(screen.height-400)+", left="+(screen.width-840));'
    s += 'win.document.body.innerHTML = \'' + (df + css).replace("\n",'\\') + '\';'
    s += '</script>'

    return(HTML(s+css))


content = "hello"
View(content)


# In[ ]:


content = "bye"
View(content)


# In[ ]:


from ipywidgets import widgets
from IPython.display import display

def on_submit(text):
    global answer
    answer = text.value
    text_input.close()
    button.close()

text_input = widgets.Text(placeholder='Enter text')
display(text_input)
#display(button)

# button = widgets.Button(description="Open Popup")
# button.on_click(on_button_click)

text_input.on_submit(on_submit)
#display(button)


# In[ ]:


from ipywidgets import widgets
from IPython.display import display

def on_button_click(b):
    display(text_input)
    display(submit_button)

def on_submit(text):
    global answer
    answer = text.value
    text_input.close()
    submit_button.close()

text_input = widgets.Text(placeholder='Enter text')
button = widgets.Button(description="Open Popup")
button.on_click(on_button_click)
display(button)

submit_button = widgets.Button(description='Submit')
submit_button.on_click(lambda b: on_submit(text_input))


# In[ ]:





# In[ ]:


from ipywidgets import widgets
from IPython.display import HTML, display, clear_output

notify_output = widgets.Output()
display(notify_output)


# In[ ]:


for v in wk.vocab.values():
#    print([wk.kanji[key].symbol for key in v.kanjis])
    if '思' in [wk.kanji[key].symbol for key in v.kanjis]:
        print(v)
#    print(v)
#    break


# In[ ]:


phrase = '大切に思う'
for v in wk.vocab.values():
    if v.symbol in phrase:
        print(v)


# In[ ]:





# In[ ]:


# question_type_distribution = {
#     'kanji_similarity': 2.5,
#     'radical_decomposition': 0.5,
#     'pronunciation': 0.3,
#     'kanji_from_meaning': 0.5
# }


# In[ ]:



#kanjis = wk.get_batch(num_questions)

#for k in queue:
# for qtype in questions:
#     clear_output(wait=True)
#     k = choose_kanji(qtype, 
#                      wk)
#     print(qtype)
#     is_correct = ask_question(k, qtype)
#     if is_correct:
#         print("Correct!")
#         correct += 1
#     else:
#         print("Incorrect")
        
#     # Update the user's progress history
#     history.update(k, qtype, is_correct)

#     # Wait for user to react to answer
#     confirm = input()

#     time.sleep(0.2)
#     i += 1


# In[ ]:


history.history


# In[ ]:


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

def window():
    app = QApplication(sys.argv)
    widget = QWidget()

    textLabel = QLabel(widget)
    textLabel.setText("Hello World!")
    textLabel.move(110,85)

    text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter your name:')
    if ok:
        self.le1.setText(str(text))

    widget.setGeometry(50,50,320,200)
    widget.setWindowTitle("PyQt5 Example")
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()


# In[ ]:


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog, QHBoxLayout
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QLineEdit(self)
#        self.second = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("First text", self.first)
#        layout.addRow("Second text", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return self.first.text() #, self.second.text())


import sys
app = QApplication(sys.argv)
dialog = InputDialog()
if dialog.exec():
    print(dialog.getInputs())
#exit(0)


# In[ ]:


# importing the required libraries 
  
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore 
from PyQt5.QtGui import * 
import sys 
  
class Window(QMainWindow): 
    def __init__(self): 
        super().__init__() 
  
        # informations 
        info = "info"
        new_info = "new info "
  
        # set the title 
        self.setWindowTitle("Label") 
  
        # setting  the geometry of window 
        self.setGeometry(0, 0, 400, 300) 
  
        # creating a label widget 
        self.label_1 = QLabel(info, self) 
  
        # moving position 
        self.label_1.move(100, 100) 
  
        # setting up border 
        self.label_1.setStyleSheet("border: 1px solid black;") 
  
        # creating a label widget 
        self.label_2 = QLabel(info, self) 
  
        # moving position 
        self.label_2.move(100, 150) 
  
        # setting up border 
        self.label_2.setStyleSheet("border: 1px solid black;") 
  
        # changing the text of label 
        self.label_2.setText(new_info) 
  
        # show all the widgets 
        self.show() 
  
  
# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = Window() 
  
# start the app 
sys.exit(App.exec()) 


# In[ ]:


import sys
from PyQt5.QtCore import pyqtSignal, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
from cal_window import UiCalWindow


class CalendarWindow(QMainWindow, UiCalWindow):
    def __init__(self, parent=None):
        super(CalendarWindow, self).__init__(parent)
        self.setupUi(self)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My App")
        self.setGeometry(50, 50, 800, 600)

        self.label = QLineEdit(self)
        self.label.setFont(QFont("Arial", 20))
        self.label.setReadOnly(True)

        self.setCentralWidget(self.label)

        self.btn = QPushButton("open calender", self)
        self.btn.move(50, 50)

        self.cal = CalendarWindow()
        self.cal.calendarWidget.clicked.connect(self.handle_date_clicked)
        self.btn.clicked.connect(self.cal.show)

    def handle_date_clicked(self, date):
        self.label.setText(date.toString("yyyy-MM-dd"))


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()


# In[ ]:





# In[ ]:


# k = wk.get_item('上')
# print(k)
# print(k.radicals)
# print(k.readings)
# print(k.meaning)
# print(k.onyomi())
# print(k.level)


# In[ ]:


# # Initialize History
# import sqlite3
# db_filename = "db/history.db"
# # Connect to DB 
# conn = sqlite3.connect(db_filename, isolation_level=None, check_same_thread=False)
# conn.execute('''''CREATE TABLE Kanjis 
#        (ID INT PRIMARY KEY     NOT NULL, 
#        NAME           TEXT    NOT NULL, 
#        AGE            INT     NOT NULL, 
#        ADDRESS        CHAR(50), 
#        SALARY         REAL);''')  


# # Add columns
# columns = [
#   ('id', 'varchar(32)'),
#   ()
# ]

# # Print Status
# cursor = conn.cursor()    

# def update_db(kanji, mode, correct):
#     cursor.execute(f"UPDATE listings SET sold = True WHERE id = {res['id']};")

