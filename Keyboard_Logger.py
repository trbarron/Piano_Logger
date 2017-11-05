import pygame
import pygame.midi
import pprint
import time
import csv
import sys
import random
from PIL import Image
from PIL import ImageDraw

pygame.init()
pygame.fastevent.init()
pygame.midi.init()
input_id = pygame.midi.get_default_input_id()

keystrokes = []
freq_hist = [0]*120
time_thresh = 5
     

def draw_diagram(freq_hist):


        im = Image.new('RGB',(5200,400))
        draw = ImageDraw.Draw(im,"RGBA")

        #Draw white keys in
        csv_name = 'WhiteKeys.csv'
        num_keys = 51
        offset = 0
        width = 100
        height = 400
        skips = []
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


        #Create skips for black keys
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
        print("imagesaved")

curr_time = time.time()
i = pygame.midi.Input( input_id )
while True:
        if i.poll():
                midi_events = i.read(1)
                if midi_events[0][0][0] != 248 and midi_events[0][0][2] != 0:
                        old_time = curr_time
                        curr_time = time.time()
                        if len(keystrokes) % 20 == 0 and len(keystrokes) > 19:
#                        if curr_time - old_time > 60*time_thresh:
                                print("been a while huh")
                                with open('eggs.csv', 'wb') as csvfile:
                                    spamwriter = csv.writer(csvfile, delimiter=',',
                                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                    for k in keystrokes:
                                            spamwriter.writerow(k)
                                            freq_hist[k[1]] += 1
                                draw_diagram(freq_hist)
                                            
                        midi_events[0][0][3] = curr_time
                        keystrokes.append(midi_events[0][0])
                        print(midi_events[0][0])

                        
