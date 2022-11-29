import requests
import threading
import time
import os
from bs4 import BeautifulSoup
from lxml import etree
from termcolor import colored

done_stuff = 1
max_stuff = 1
charLib = []
maxLib = []
to_call = 2
thArr = []
nips=[]
th1srt = []
th2srt = []
sorted = []

def barificate(lenght, max, current):
    i=0
    bar = "["
    lvl = (current/max)*lenght
    while i < lenght:
        if i > lvl:
            bar += "."
        else:
            bar += "="
        i+=1

    bar += "]"
    return bar

def write_perc(max, current, priority=1):
    bar = barificate(20*priority, max, current)

    perc = int((current / max)*100)
    bar += " " + str(perc) + "%"
    print("\r" + bar, end='', flush=True)

def show_threads():
    global done_stuff
    global max_stuff
    global cleared

    levl = int((done_stuff/max_stuff)*100)
    screen_buffer = str(barificate(40,100,levl) + " " + str(levl) + "%" + " of " + str(max_stuff) +"\n")
    i=0
    while i < to_call:
        perc = int((thArr[i].act / thArr[i].end)*100)
        if perc < 100:
            if perc < 10:
                screen_buffer += str("THREAD " + str(thArr[i].char) + ": " + barificate(20,thArr[i].end,thArr[i].act) +"  "+ str(perc) + "%")

            else:
                screen_buffer += str("THREAD " + str(thArr[i].char) + ": " + barificate(20,thArr[i].end,thArr[i].act) +" "+ str(perc) + "%")

        else:
            screen_buffer += str("THREAD " + str(thArr[i].char) + ": " + barificate(20,thArr[i].end,thArr[i].act) + str(perc) + "%")

        if thArr[i].end < 10000:
            if thArr[i].end < 1000:
                if thArr[i].end < 100:
                    if thArr[i].end < 10:
                        screen_buffer += " of    " + str(thArr[i].end)+ "   "
                    else:
                        screen_buffer += " of   " + str(thArr[i].end)+ "   "
                else:
                    screen_buffer += " of  " + str(thArr[i].end)+ "   "
            else:
                screen_buffer += " of " + str(thArr[i].end)+ "   "

        if((i+1) % 3) == 0:
            screen_buffer += "\n"
        i+=1
    clear()
    print(screen_buffer)
    screen_buffer = ""

def read_nips(char,end,thar):
    global done_stuff
    global max_stuff
    i=1
    output = ""
    while i <= end:

        inner_page_url = str('http://bnip.pl/nip,indexa,'+char+',' + str(i) + '.html')
        inner_html = requests.get(inner_page_url)
        inner_site = BeautifulSoup(inner_html.text, "html.parser")
        inner_siteXML = BeautifulSoup(inner_html.content, "html.parser")

        nip = etree.HTML(str(inner_siteXML))

        iterator = 0;
        while iterator <= len(inner_site.find('tbody').find_all("tr")):
            a = str(nip.xpath('/html/body/div[2]/table/tbody/tr[' + str(iterator) + ']/td[1]/text()')).replace("[]","").replace("['", "").replace("']", "")
            if a != '':
                b = int(a)
                nips.append(b)
            iterator += 1

        thArr[thar].act = i
        done_stuff += 1
        i += 1;


    #file = open(char+".txt", "a", encoding="ISO-8859-1")
    #file.write(output)
    #file.close()

    #nips.append(output)

def lib():
    global max_stuff
    i = 1
    char="1"
    done=False
    print("Loading site navigation data \n")
    while not done:
        page_url = 'http://bnip.pl/nip,indexa,'+ char + '.html'
        html = requests.get(page_url)
        siteXML = BeautifulSoup(html.content, "html.parser")
        nextCHAR = etree.HTML(str(siteXML))
        max = etree.HTML(str(siteXML))
        num = str(max.xpath('/html/body/div[2]/p[2]/b[3]/a/text()')).replace("['", "").replace("']", "")
        if num != "[]":
            end = int(num)
        else:
            end = 1
        charLib.append(char)
        maxLib.append(end)
        max_stuff += end
        write_perc(to_call,i,2)

        char = str(nextCHAR.xpath('/html/body/div[2]/p[1]/a['+str(i)+']/text()')).replace("['", "").replace("']", "")
        i+=1
        if i == to_call + 1:
            done = True

    print("\n")

class myth():
    def __init__(self, char, whoami, end):
        self.char = char
        self.whoami = whoami
        self.end = end
        self.THREAD = None
        self.act = 0
    def do(self):
        self.THREAD = threading.Thread(target=read_nips, args=(self.char,self.end,self.whoami - 1))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def sortuj(th):

    half = len(nips)/2
    full = len(nips)

    th1End = int(half)
    th2End = int(full)

    sortingTable = []

    if th == '1':
        i=0
        stop = th1End

    if th == '2':
        i=th1End
        stop = th2End

    j=0
    while i < stop:
        sortingTable.append(nips[i])
        i += 1
        j += 1

    i=0
    srtLen = len(sortingTable)
    stop = int(srtLen)
    stop2 = stop
    todel=0
    while i < stop:
        big=0
        j=0
        while j < stop2:
            if int(sortingTable[j]) >= big:
                big = int(sortingTable[j])
                todel = j

            j = j + 1
        if th == '1':
            th1srt.append(big)
        else:
            th2srt.append(big)
        sortingTable.remove(sortingTable[todel])
        stop2 = stop2 - 1
        i = i + 1

def dump():

    one = threading.Thread(target=sortuj, args=('1'))
    two = threading.Thread(target=sortuj, args=('2'))

    one.start()
    two.start()

    one.join()
    two.join()

    i=0
    j=0
    while i < len(th1srt) and j < len(th2srt):
        if int(th1srt[i]) > int(th2srt[j]):
            sorted.append(th1srt[i])# porównanie dwóch tabel i zwiększenie tylko iteratora odpowiedniej tabeli#
            print(th1srt[i])
            i = i + 1
        else:
            sorted.append(th2srt[j])
            print(th2srt[j])
            j = j + 1

    while i < len(th1srt):
        sorted.append(th1srt[i])
        print(th1srt[i])
        i = i + 1

    while j < len(th2srt):
        sorted.append(th2srt[j])
        print(th2srt[j])
        j = j + 1


    i = 0
    file = open("TEZT.txt", "a", encoding="ISO-8859-1")
    while i < (len(sorted)):
        file.write(str(sorted[i]))
        file.write('\n')
        #print(thArr[i].char + " DONE ")
        i = i + 1
    file.close()


def main():
    clear()
    lib()
    i = 1
    finish = False
    char = "1"

    while not finish:
        THREAD = myth(charLib[i-1],i,maxLib[i-1])
        thArr.append(THREAD)
        i+=1
        if i == to_call + 1:
            finish = True


    j=0
    while j<to_call:
        thArr[j].do()
        thArr[j].THREAD.start()
        j+=1

    while not done_stuff == max_stuff:
        show_threads()
        time.sleep(1)

    #clear()
    show_threads()

    j=0
    while j<to_call:
        thArr[j].THREAD.join()
        j+=1

    dump()

main()
