# my_system = 'MacOS' # MacOS, Windows
my_system = 'Windows'
from tkinter import *
import glob
import os
# from playsound import
if my_system =='Windows':
  import winsound
# import Pmw

# Pmw.initialise()
Sources = 'Sources'
Dirs = 'Dirs'
Files = 'Files'
SoDi = Sources + '/' + Dirs + '/'
SoFi = Sources + '/' + Files + '/'
dir_ctext    = SoDi + 'seals'
dir_arch     = SoDi + 'arch'
dir_fenbu    = SoDi + 'fenbu'
dir_arch2    = SoDi + 'arch/Nowe'
dir_arch3    = SoDi + 'arch/Yellow_Bridge'
dir_wav      = SoDi + 'wav'
dir_wubi_gif = SoDi + 'wubi_gif/'
dir_wubi =     SoDi + 'wubi/'

#  arch_dir_jpg = 'D:/Marek/Chinskie/Arch_Jpg/'
  
file_pary        = SoFi + 'pary5.txt'
file_gif         = SoFi + 'gifs.txt'
file_wynik_all   = SoFi + 'wynik_all.txt'
file_slownik     = SoFi + 'slownik.txt'
file_znaki_forms = SoFi + 'znaki_forms.txt'
file_with = 'thousand_trad.txt'

keyboards = Sources + '/' + 'keyboards'

t = ''
znak_wybrany = ''
znak_forPaint = ''
klawiatury = glob.glob(keyboards + '/*.png')
klawiatury_i = 0
klawiatura = klawiatury[klawiatury_i]
fontKaiti = '"Adobe Kaiti Std R"'

skroty = '工了以在有地一上不是中国同民为这我的要和产发人经主'
alphabet = 'ąćęłńóśżź'
alphabet += 'āáǎàēéěèīíǐìōóŏǒòūúŭǔùǖǘǚǜ'
i = ord('a')
while i <= ord('z'): 
   alphabet += chr(i) 
   i += + 1
alphabet += alphabet.upper()
# subprocess.call(['C:/Program Files (x86)/Microsoft Office/OFFICE11/OIS.EXE', 'D:/Marek/Chinskie/Chinese_chars/Program/a.jpg'])
# subprocess.call('"C:\Program Files (x86)\Microsoft Office\OFFICE11"\OIS.EXE "D:\Marek\Chinskie\Chinese_chars\Program\a.jpg"')
# os.system('a.jpg')

SystemWindowText = 'SystemWindowText'
SystemWindow = 'SystemWindow'
SystemButtonText = 'SystemButtonText'
SystemButtonFace = 'SystemButtonFace'
if my_system == 'MacOS':
    SystemWindowText = 'SystemButtonText'
    SystemWindow = 'SystemWindowBody'
#SystemButtonFace = 'SystemButtonFace'

def printPaint (znak, mspaint=0):
  global mw
  read_wubi(dir_wubi, znak, exten = 'png')
  mw.clipboard_clear()
  # print (znak)
  if mspaint:
      #    mw.clipboard_append('mspaint ' + znak_forPaint)
        mw.clipboard_append('open ' + znak_forPaint)
  else:
    mw.clipboard_append(znak_forPaint)


def read_wyniki(fi):
  for line in fi:
    lista = line.split('\t')
    s = lista[0]
    if len(lista) < 3: continue
    w = lista[1]
    if '[' in w: w = lista[2]
    wymowa[s[0]] = w
    m = s
    for i in range(3, len(lista) - 1):
      if ord(lista[i][0] ) > 0x2000: continue
      if '+' in lista[i]: continue
      if len(lista[i]) == 0: continue
      if lista[i][0] == lista[i][0].upper():
        m = lista[i]
        break
    znaki[s[0]] = m
    slownik2[s[0]] = lista[-1]

def read_slownik(fname):
  fi = open (fname, 'r', encoding='utf8')
  nr_lekcji = '0'
  for line in fi:
    if line.find('@Lesson') == 0:
      nr_lekcji = line;
      continue
      
    lista = line.split('\t')
    if len(lista) == 3:
      lista[2] = lista[2].strip()
      s = lista[0] + ' ' + lista[1] + ' ' + lista[2] + ' ' + nr_lekcji
      for m in lista[0]:
        if m in slownik:
          slownik[m] += s
        else:
          slownik[m] = s
  fi.close()
def make_unique(txt):
  dic = {}
  for i in txt:
    dic[i] = 0
  return ''.join(dic.keys())
  
def read_pary(fname):
  dict = {}
  fi = open (fname, 'r', encoding='utf8')
  for line in fi:
    if line[1] != ':': continue
    trad = line[0]
    simp = line[3]
    dodaj_trad = trad
    dodaj_simp = simp
    if trad in dict:
      dodaj_simp = make_unique(dict[trad][1] + simp)
    if simp in dict:
      dodaj_trad = make_unique(dict[simp][0] + trad)
    
    dict[trad] = (dodaj_trad, dodaj_simp)
    dict[simp] = (dodaj_trad, dodaj_simp)
  fi.close()
  return dict  

def read_file_with():
  global file_with, napis
  fi = open (file_with, 'r', encoding='utf8')
  s = fi.read()
  s = s.lstrip()
  fi.close()  
  napis.delete('1.0',END)
  napis.insert('1.0',s)
  napis.mark_set('insert', '1.0')
  hop_forward(-1)

def play_all(txt):
  idx_begin = txt.index(INSERT)               # numer bieżącej linijki w formacie 1.0
  idx_begin = idx_begin[:idx_begin.find('.')] # liczba przed kropką
  my_text = txt.get(idx_begin + '.0',idx_begin +'.end' ) # 'line end' index
  for i in my_text:
    if i in wymowa: 
      my_play(wymowa[i])
   
def switch_fenbu():
  global fenbu_switched
  fenbu_switched = not fenbu_switched

def kill(ff):
  for n in ff.winfo_children():
    n.destroy()

def kill_image(ff):
  for n in ff.winfo_children():
    if str(n).find('label') >= 0: 
      n.destroy()

def kill_text(ff):
  for n in ff.winfo_children():
    if str(n).find('text') >= 0: 
      n.destroy()

def create_napis(ff,gif_i,txt):
  kill(ff)
  
  idx_begin = txt.index(INSERT)               # numer bieżącej linijki w formacie 1.0
  idx_begin = idx_begin[:idx_begin.find('.')] # liczba przed kropką
  my_text = txt.get(idx_begin + '.0',idx_begin +'.end' ) # 'line end' index
  added_trad = set()
  if var_tradsimp.get():
    new_text = ''
    for i in my_text:
      new_text += i
      if i in dict_pary:
        j = dict_pary[i][0]
        if j == i: j = dict_pary[i][1]
        added_trad.add(len(new_text))
        new_text += j
    my_text = new_text
  was_space = 0
  button_tmp = ''
  licznik = 0
  for i in my_text:
    if i == '\n': continue
    if i in alphabet: continue
    if i == '\t': i = ' '
    if i == ' ': # ---------------------- tylko jedna spacja
      if was_space: continue
      else: was_space = 1
    else: was_space = 0
    frame = Frame(ff)
    b = Button( frame,text=i,font='SimSun 28', # width = 1,
            command = lambda nam = i: create_gifa(ff, gif_i, nam) )
    if licznik in added_trad: 
      b.configure(bg = 'light grey')
    b.pack(side = TOP, anchor=W, fill = X)
    if i not in slownik2.keys(): b.configure(state='disabled')
    if button_tmp == '' and ord(i) > 0x3000 :  button_tmp = b
    s = i
    if i in wymowa: s = wymowa[i]
    Label(frame,text=s,font=28).pack()
    s = i
    if i in znaki: s = znaki[i]
    if i in skroty:
      c = chr ( ord('a') + skroty.find(i) )
      Label(frame,text=s + c,font=28).pack()
    else: 
      Label(frame,text=s,font=28).pack()
      
    frame.pack(side='left')
    hide_napis(frameButtons,napis,1)
    licznik += 1
  if button_tmp != '': button_tmp.invoke()
    
def get_file(dir, c, exten = '.gif'):
  if c=='': 
    return ''
  return '%s/%04x%s' % (dir, ord(c), exten)

def read_wubi(dir_wubi, i, exten = 'png'):
  global znak_forPaint
  if i=='':
    return ''
  charCode = "%04x" % ord(i)
  filedirname = "%smades/made%c/%s.%s" % (dir_wubi, charCode[0], charCode, exten)
  filedirname = os.path.normpath(filedirname)
  if os.path.isfile(filedirname):
    znak_forPaint=os.path.abspath(filedirname);
    return filedirname
  else:
    filedirname = "%sgroups/group%c/%s.%s" % (dir_wubi, charCode[0], charCode, exten)
    filedirname = os.path.normpath(filedirname)
    if os.path.isfile(filedirname):
      znak_forPaint=os.path.abspath(filedirname);
      return filedirname
  return ''

def textHe(tt):
    tti = tt.index(END)
    tL = tti.split('.')
    return int(tL[0]) - 1

def dodaj (tekst, wyrazy):
  for n in tekst: 
    if ord(n) > 0x4000:
      wyrazy.add(n)

def dodaj_znaki(txt,fDodaj):
  idx_begin = napis.index(INSERT)               # numer bieżącej linijki w formacie 1.0
  idx_begin = idx_begin[:idx_begin.find('.')]  # liczba przed kropką
  my_index = str(int(idx_begin)) + '.0'

  s = napis.get(idx_begin+'.0',idx_begin+'.end')
  for n in txt:
    if n not in s:
      napis.insert(idx_begin+'.end',n)
  kill(fDodaj)
  

def showall_me():
  if var_showall.get() == False:
    x1, x2 = textHe(teF), textHe(teS)
    if x1 > 3: x1 = 3
    if x2 > 3: x2 = 3
    teF.configure(height = x1)
    teS.configure(height = x2)
  else:
    teF.configure(height = textHe(teF))
    teS.configure(height = textHe(teS))

def name_to_file(name):
  tones = 'āáǎàēéěèīíǐìōóŏǒòūúŭǔùǖǘǚǜ'
  toneT = '12341234123412334123341234'
  toneA = 'aaaaeeeeiiiiooooouuuuuvvvv'
  toneNew = ''
  name = name.replace('*', '')
  for i in range(len(tones)):
    r = name.find(tones[i])
    if r >= 0:
      name = name[:r] + toneA[i] + name[r+1:]
      toneNew = toneT[i]
  return name + toneNew
  
def my_play(name):
  name = name_to_file(name)
  name = dir_wav + '/'+ name + '.wav'
  if os.path.isfile(name): 
    # print (name)
    if my_system == 'Windows':
      winsound.PlaySound(name,winsound.SND_FILENAME)
#     playsound(name)
    elif my_system == 'MacOS':
      os.system('afplay ' + name)
  
def create_gifa(window,gif_i, i):
  global var_play
  global znak_wybrany
  global fenbu_switched
  if i == znak_wybrany:
    switch_fenbu()
#  print ('create gifa %s' % fenbu_switched)
  wyrazy1 = set()
  wyrazy2 = set()
  if i in gify: 
    gg = dir_wubi_gif + gify[i]
    myimage = PhotoImage(file=gg)
    # ----------------------- bardzo wazne! 
    # You must keep a reference 
    # to the image object in your Python program, 
    # either by storing it in a global variable, 
    # or by attaching it to another object.
    gif_i.image = myimage
    gif_i.configure(image=myimage)
  else: gif_i.configure(image='')

  teF.delete('1.0',END)
  if i in formy:
    list = formy[i].split('\n')
    teF.insert('1.0',formy[i])
    dodaj (formy[i], wyrazy1)
#    teF.configure(height = textHe(teF))
  
  if i in dict_pary:
    teF.insert(END, 'Tradycyjne: %s Uproszczone: %s' % (dict_pary[i][0], dict_pary[i][1]) )
    dodaj (dict_pary[i][0] + dict_pary[i][1] + '\n', wyrazy1)
#    pass
  
  teS.delete('1.0',END)
  if i in slownik:
    list = slownik[i].split('\n')
    teS.insert('1.0',slownik[i])
    dodaj (slownik[i], wyrazy2)
#    teS.configure(height = textHe(teS))

  showall_me()

  wyrazy_s1 = ''
  wyrazy_s2 = ''
  napis_test = napis.get('1.0',END)
  kill(fDodaj)
  for n in wyrazy1:
    if n not in napis_test:
       wyrazy_s1 += n
  for n in wyrazy2:
    if n not in napis_test:
       wyrazy_s2 += n
  if len(wyrazy_s1):
    fDodaj1 = Frame(fDodaj)
    fDodaj1.pack(fill='x')
    Label(fDodaj1,text=wyrazy_s1,font='SimSun 20').pack(side='left',anchor='nw')
    Button(fDodaj1,text='Dodaj',font='18',
           command = lambda: dodaj_znaki(wyrazy_s1,fDodaj1)).pack(side='right')
  if len(wyrazy_s2):
    fDodaj2 = Frame(fDodaj)
    fDodaj2.pack(fill='x')
    Label(fDodaj2,text=wyrazy_s2,font='SimSun 20').pack(side='left',anchor='w')
    Button(fDodaj2,text='Dodaj',font='18',
           command = lambda: dodaj_znaki(wyrazy_s2,fDodaj2)).pack(side='right')
  
  kill(fText)
  for n in ('jiagu', 'jin', 'jianbo', 'seal'):
    name = get_file(dir_ctext + '/' + n, i)
    lab = Label(fText,text=i)
    if os.path.isfile(name):
      myimage = PhotoImage(file=name)
      lab.image = myimage
      lab.configure(image = myimage)
    lab.pack(side='left')
  
  # name = os.path.normpath(get_file(arch_dir_jpg,i,'.jpg'))
  
  name = find_name(i)

  for mydir in (dir_arch2, dir_arch3):
    if os.path.isfile(name):
      break
    name = os.path.normpath(get_file(mydir,i,'.png'))  
  if not os.path.isfile(name): name = ''

  Button(fText, text=i, font = fontKaiti + ' 28', command = lambda
         name=name: os.system('open ' + name)).pack(side='left')

  Button(fText, text='\u266a', width = 3, font = fontKaiti + ' 28', command = lambda name=wymowa[i]: my_play(name)).pack(side='left')
  
  for labels in fFonts.winfo_children():
    labels.configure(text=i)

  lSlownik.configure(text=slownik2[i])
  znak_wybrany = i
  hexValue = "%04x" % ord(znak_wybrany)
  lHexag.delete("1.0", END)
  lHexag.insert("1.0", hexValue)
  image_show(i)
  if var_play.get(): my_play(wymowa[i])
  
def find_name(i):
  global fenbu_switched, dir_fenbu, dir_arch
  if fenbu_switched: 
    name = os.path.normpath(get_file(dir_fenbu,i,'-fenbu.png'))
    if not os.path.isfile(name):
      name = os.path.normpath(get_file(dir_arch,i,'.png'))
  else:
    name = os.path.normpath(get_file(dir_arch,i,'.png'))
    if not os.path.isfile(name):
      name = os.path.normpath(get_file(dir_fenbu,i,'-fenbu.png'))
  return name

def image_show(i):
  global var_wubi
  name = ''
  was_wubi = 1
  if var_wubi.get():
    name = read_wubi(dir_wubi,i,'png')
  if name=='':
    was_wubi = 0
    name = find_name(i)

  if not os.path.isfile(name):
    png_image.configure(image = '')
    return

  myimage = PhotoImage(file=name)
  if not was_wubi:
    myimage = myimage.zoom(2)
    myimage = myimage.subsample(3)
  png_image.image = myimage
  png_image.configure(image = myimage)
  


def next_klawiatura (lab,kierunek = 0):
  global klawiatury_i, klawiatury
#  print(klawiatury_i, klawiatury[klawiatury_i])
  klawiatury_i +=1
  if klawiatury_i == len(klawiatury):
    klawiatury_i = 0
  myimage = PhotoImage(file=klawiatury[klawiatury_i])
  lab.image = myimage
  lab.configure(image = myimage)
  
def show_klawiatura(obraz):
  global t
  if t: t.destroy()
  t = Toplevel(mw)
  t.geometry('+%d+%d'%(5,135))  
  lab = Label(t)
#  obraz2 = obraz.zoom(5)
#  obraz2 = obraz2.subsample(4)
#  lab.configure(image = obraz2)
  lab.configure(image = obraz)
  lab.image = obraz
  f = Frame(t)
  f.pack(anchor='w')
  lab.pack()
  Button(f, text="<<", font = '16', width = 4, command=lambda lab=lab: next_klawiatura(lab)).pack(side='left')
  Button(f, text=">>", font = '16', width = 4, command=lambda lab=lab: next_klawiatura(lab,1)).pack(side='left')
  Button(f, text="Destroy", font = '16', command=t.destroy).pack(side='left')
  t.focus()

def hide_napis(fbuttons,text,new_creation = 0):
  hidden = 0
  
  # On Windows and Macintosh systems, the color name table is built into Tk.
  
  # the Windows system colors:
  # SystemActiveBorder, SystemActiveCaption, SystemAppWorkspace, SystemBackground, 
  # SystemButtonFace, SystemButtonHighlight, SystemButtonShadow, SystemButtonText, 
  # SystemCaptionText, SystemDisabledText, SystemHighlight, SystemHighlightText, 
  # SystemInactiveBorder, SystemInactiveCaption, SystemInactiveCaptionText, SystemMenu, 
  # SystemMenuText, SystemScrollbar, SystemWindow, SystemWindowFrame, SystemWindowText.
  
  # On the Macintosh, the following system colors are available:
  
  # SystemButtonFace, SystemButtonFrame, SystemButtonText, SystemHighlight, 
  # SystemHighlightText, SystemMenu, SystemMenuActive, SystemMenuActiveText, 
  # SystemMenuDisabled, SystemMenuText, SystemWindowBody.



  if new_creation or text.cget('foreground') != SystemWindowText:
    hidden = 1
  # SystemWindow, SystemWindowText

  if hidden: 
    text.config(foreground= SystemWindowText)
  else: 
    text.config(foreground = SystemWindow)
    napis1.delete('1.0','1.end')
    
  
  for n in fbuttons.winfo_children():
    if str(n).find('frame') >= 0: 
      for f2 in n.winfo_children():
        if str(f2).find('frame') >= 0: 
          for button in n.winfo_children():
            if str(button).find('button') >= 0: 
#              button.config(foreground='red')
              # == 'systemButtonFace', 'systemButtonText'
               if hidden:
                 button.config(foreground = SystemButtonText)
               else: 
                 button.config(foreground = SystemButtonFace)
#              print (button.cget('background')) # == 'systemButtonFace', 'systemButtonText'
#              print (button.cget('foreground'))
          break
          
def hop_forward(hop = 1):
  idx_begin = napis.index(INSERT)               # numer bieżącej linijki w formacie 1.0
  idx_begin = idx_begin[:idx_begin.find('.')]  # liczba przed kropką
  my_index = str(int(idx_begin) + hop) + '.0'
  napis.mark_set('insert', my_index)
  napis.see( my_index )
  napis1.delete('1.0',END)
  create_napis(frameButtons,gif_image,napis)
  napis1.focus()

znaki = {}
wymowa = {}
gify = {}
formy = {}
slownik = {}
slownik2 = {}
dict_pary = {}
fenbu_switched = True

fi = open (file_wynik_all, 'r', encoding = 'utf8')
read_wyniki(fi)
read_slownik(file_slownik)
dict_pary = read_pary(file_pary)
fi = open (file_gif, 'r', encoding = 'utf8')
for line in fi:
  line = line.strip()
  gify[line[0]] = line[1:]

fi = open (file_znaki_forms, 'r', encoding = 'utf8')
starter = 1
forma_string = ''
klucz = ''
for line in fi:
  if line == '\n': 
    formy[klucz] = forma_string
    starter = 1
    forma_string = ''
    continue
  if starter:
    klucz = line[0]
    
    # ------------ sprawdzenie wymowy
    i = line.find(']')
    napisik = line[4:i-1]
    i = napisik.find(',')
    if i > 0: 
      napisik = napisik[:i]
    if klucz in wymowa and wymowa[klucz] != napisik:
      wymowa[klucz] = napisik + '*'
    
    starter = 0
  forma_string += line

fi.close()

mw = Tk()
# -------------------------------------------------------- teksty - pola do wpisywania
napis = Text(mw,font = 'SimSun 38',height = 1); napis.pack(fill=X)
napis1 = Text(mw,font = 'SimSun 38',height = 1); napis1.pack(fill='x')


# -------------------------------------------------------- główne pola znaków
f = Frame(mw); f.pack(fill=BOTH)
frameButtons = Frame(f); frameButtons.pack(side='left',anchor='w')
gif_image = Label(f); gif_image.pack(side='left',anchor='n')
orig_color = gif_image.cget('background')
# -------------------------------------------------------- przyciski poleceń
f = Frame(mw); f.pack()
button_size = '18'
if my_system == 'MacOS':
  button_size = '48'
Button(f,text='exit',font = button_size,width=6,command=lambda: exit()).pack(side='left')
Button(f,text='create',font = button_size,width=8,command=lambda: create_napis(frameButtons,gif_image,napis)
   ).pack(side='left')
Button(f,text='hide',font = button_size,width=8,command=lambda: hide_napis(frameButtons,napis)
   ).pack(side='left')
Button(f,text='>>',font = button_size,width=4,command=lambda: hop_forward()).pack(side='left')
Button(f,text='<<',font = button_size,width=4,command=lambda: hop_forward(-1)).pack(side='left')
image_klaw = PhotoImage(file = klawiatura)
Button(f,text='\u0037',font = "Wingdings 18",command=lambda: show_klawiatura(image_klaw)).pack(side='left',fill=Y)
var_wubi = BooleanVar()
var_wubi.set(False)
Checkbutton(f,text="\u4e94\u7b14",font = "SimSun 16", width = 4, variable = var_wubi, indicatoron=0, 
  selectcolor = 'SystemButtonFace',
  command = lambda: image_show(znak_wybrany)).pack(side='left',fill=Y)
var_play = BooleanVar()
var_play.set(False)
Checkbutton(f,text='\u266a',indicatoron=0,font = button_size,width = 3,
   selectcolor = 'SystemButtonFace',
   variable = var_play).pack(side='left',fill=Y)
Button(f,text='\u266b', font = button_size, width = 3, command = lambda: play_all(napis)).pack(side='left',fill=Y)
var_showall = BooleanVar()
var_showall.set(True)
var_tradsimp = BooleanVar()
var_tradsimp.set(False)
Checkbutton(f,text='Tr/Simp',indicatoron=0,font = button_size,
   selectcolor = 'SystemButtonFace',
   variable = var_tradsimp, command = lambda: create_napis(frameButtons,gif_image,napis)).pack(side='left',fill=Y)
Checkbutton(f,text='Show all',indicatoron=0,font = button_size,
   selectcolor = 'SystemButtonFace',
   variable = var_showall, command = lambda: showall_me()).pack(side='left',fill=Y)
f = Frame(f); f.pack(side=RIGHT, expand=1,fill=Y,anchor=W)
Button(f,text='Text from file', command = lambda: read_file_with()).pack(side='right',anchor=N,expand=1,fill=BOTH)
# -------------------------------------------------------- teksty definicji i znaczenia
teF = Text(mw,background = orig_color,font = 'SimSun 18',wrap='word',height=2); teF.pack(fill='x')
teS = Text(mw,background = orig_color,font = 'SimSun 18',wrap='word',height=2); teS.pack(fill='x')
opisy = Frame(mw); opisy.pack(fill='both',expand=1)
# -------------------------------------------------------- opisy lewe
opisyLeft = Frame(opisy); opisyLeft.pack(fill='x',side='left')
fDodaj = Frame(opisyLeft); fDodaj.pack(fill='x', expand=1) #,side='left')
fText = Frame(opisyLeft); fText.pack(anchor='nw')
fFonts= Frame(opisyLeft); fFonts.pack(anchor='w')
if my_system == 'MacOS':
  for n in ('STBaoliSC-Regular', 'STLibianSC-Regular',
            'WeibeiSC-Bold', 'DFKaiShu-SB-Estd-BF',
            'STKaitiTC-Regular', 'STXingkaiTC-Light',
            'MLingWaiMedium-SC',):
    Label(fFonts,font = n + ' 88').pack(side='left',anchor='w')
if my_system == 'Windows':
  for n in ('汉仪篆书繁', '经典繁方篆', 'HanWangYenLight', 'HanWangKanTan', 
       'HanWangWCL07', 'HanWangShinSuMedium', ):
    Label(fFonts,font = (n, '38')).pack(side='left',anchor='w')

lSlownik = Label(opisyLeft,font = 'Times 18',padx=2); lSlownik.pack(anchor='w')
frameHex = Frame(opisyLeft); frameHex.pack(anchor=W);
lHexag = Text(frameHex,width=5, height=1); lHexag.pack(anchor=W,side=LEFT,fill=Y);
paintMs = Button(frameHex,text='\u003f', font=('Wingdings', 12),
#  command = lambda: print (znak_forPaint)  # os.system('mspaint ' + znak_forPaint)
  command = lambda : printPaint (znak_wybrany, 1) # os.system('mspaint ' + znak_forPaint)
  ); paintMs.pack(side=LEFT)
paintX = Button(frameHex,text='\u003f', font=('Wingdings', 12),
#  command = lambda: print (znak_forPaint)  # os.system('mspaint ' + znak_forPaint)
  command = lambda : printPaint (znak_wybrany) # os.system('mspaint ' + znak_forPaint)
  ); paintX.pack(side=LEFT)

# -------------------------------------------------------- opisy prawe
#opisyRightFrame = Pmw.ScrolledFrame(opisy)
opisyRightFrame = Frame(opisy)

#opisyRight = opisyRightFrame.interior()
opisyRight = Frame(opisy)
png_image = Label(opisyRight); png_image.pack()
opisyRight.pack()
opisyRightFrame.pack(expand=1,fill='both')
#opisyRight.pack(expand=1,fill='both')
#opisyRight.pack(anchor='e')


# Button(mw,text='Kill buttons',font = 18,command=lambda: kill(frameButtons)).pack()
napis.focus_set()
napis.bind('<F8>', lambda event: hop_forward(-1) ) # next_klawiatura(lab))
napis.bind('<F9>', lambda event: hop_forward() ) # next_klawiatura(lab,1))
napis1.bind('<F8>', lambda event: hop_forward(-1) ) # next_klawiatura(lab))
napis1.bind('<F9>', lambda event: hop_forward() ) # next_klawiatura(lab,1))
mw.state('zoomed')
mainloop()
# https://github.com/MarekPli/Chinese
