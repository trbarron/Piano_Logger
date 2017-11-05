import pygame
import pygame.midi
import time
import csv
import sys
from PIL import Image
from PIL import ImageDraw

#For polling MIDI
pygame.init()
pygame.fastevent.init()
pygame.midi.init()
input_id = pygame.midi.get_default_input_id()

keystrokes = []
freq_hist = [0]*120
time_thresh = 5 #Number of minutes per saving of information
     
def draw_diagram(freq_hist):

        im = Image.new('RGB',(5200,400)) #Todo: make images scalable so 5200x400 isn't the only size
        draw = ImageDraw.Draw(im,"RGBA")

        #Draw white keys in
        csv_name = 'WhiteKeys.csv'
        num_keys = 51
        offset = 0
        width = 100
        height = 400
        skips = []
        for i in range(0,num_keys):
                if i not in skips: #this isn't necessary but kept in so white/black key drawing is similar
                        hits = 0
                        f = open(csv_name, 'rt')
                        reader = csv.DictReader(f)
                        for w in reader:
                                if int(w['i index']) == i:
                                        hits = freq_hist[int(w['pygame output'])]
                        color = int(255*hits/max(freq_hist))
                        draw.polygon([((100*i)+offset,0), ((100*i)+offset, height), ((100*i)+offset+width, height), ((100*i)+offset+width,0)], fill=(color, color, color, 255), outline=(128,128,128,255))


        #Create skips for black keys (a skip counts when there are two white keys without a black key between)
        for w in range(0,7):
                skips.append(1+7*w)
                skips.append(4+7*w)

        #Draw black keys in
        csv_name = 'BlackKeys.csv'
        num_keys = 50
        offset = 60
        width = 70
        height = 250
        for i in range(0,num_keys):
                if i not in skips:
                        hits = 0
                        f = open(csv_name, 'rt')
                        reader = csv.DictReader(f)
                        for w in reader:
                                if int(w['i index']) == i:
                                        hits = freq_hist[int(w['pygame output'])]
                        color = int(255*hits/max(freq_hist))
                        draw.polygon([((100*i)+offset,0), ((100*i)+offset, height), ((100*i)+offset+width, height), ((100*i)+offset+width,0)], fill=(color, color, color, 255), outline=(128,128,128,255))

      
        del draw
        im.save("keyboardheatmap.png","PNG")
        print("imsaved")

save_time = time.time()
old_time = save_time
i = pygame.midi.Input( input_id )
while True:
        if i.poll(): #Begin polling
                midi_events = i.read(1)
                if midi_events[0][0][0] != 248 and midi_events[0][0][2] != 0:
                        save_time = time.time()
#                        if len(keystrokes) % 20 == 0 and len(keystrokes) > 19: #test mode -- makes csv and heatmaps very regularly
                        if save_time - old_time > 60*time_thresh:
                                old_time = save_time
                                with open(str(time.strftime("%a%d%b%Y"))+'.csv', 'wb') as csvfile:
                                    csvrow = csv.writer(csvfile, delimiter=',',
                                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                    csvrow.writerow(['ID','Key_ID','Velocity','Time_Played'])
                                    for k in keystrokes:
                                            csvrow.writerow(k)
                                            freq_hist[k[1]] += 1
                                draw_diagram(freq_hist)
                                            
                        midi_events[0][0][3] = save_time
                        keystrokes.append(midi_events[0][0])
                        print(midi_events[0][0])
