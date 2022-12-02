#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 22:49:08 2022

@author: gerard
"""

#import time
#text = "22°C"
#import Adafruit_GPIO.SPI as SPI
def simple_text(*text):
    
    #print(len(text))
    
    import Adafruit_SSD1306
    from PIL import Image
    from PIL import ImageDraw    
    from PIL import ImageFont
    
    #import subprocess
    
    RST = 0    
    oled = Adafruit_SSD1306.SSD1306_128_32(rst=RST)    
    oled.begin()    
    #oled.clear()
    
    #oled.display()    

    
    image1 = Image.new('1', (oled.width, oled.height))
    draw = ImageDraw.Draw(image1)  
    
    #oled.clear()   
    
    # Load default font.

    #font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    #font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    #font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
  
    #font_height = font.height
    # draw.text((oled.width//2 - font_width//2, oled.height//2 - font_height//2),
    #           text, font=font, fill=255)    
    
    #draw.rectangle((0,0,oled.width,oled.height), outline=0, fill=10)
    for i in range(0, len(text), 4):
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", text[i+1])
        
        xloc = text[i+2]
        
        if text[i+3] == 'c':
            yloc = (oled.height//2) - (text[i+1]//2)
        elif text[i+3] == 't':
            yloc = 0
        elif text[i+3] == 'b':
            yloc = oled.height - (text[i+1] + 2)
        else: yloc = text[i+3]
        
        
            
        
        draw.text((xloc, yloc), text[i], font=font, fill = 250)
        #draw.text((70, (oled.height//2 - 10//2)), 'sample #', font=font2, fill=0)
    #draw.text((30, (oled.height//2 - 24//2)), '1', font=font2, fill=0)

    
    # Display image.
    oled.image(image1)    
    oled.display()
    


#simple_text("22°C", 22, 10, 'c', "sample #", 10, 70,'t', '1', 15, 85, 'b')

  