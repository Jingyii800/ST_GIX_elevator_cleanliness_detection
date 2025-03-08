

# Initialize the display
epd = epd7in5_V2.EPD()
epd.init()
epd.Clear()
time.sleep(2)

# Load a font (adjust the path if needed)
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_size = 40  # Adjust as needed
checkmark_font_size = 80  # For icons
font = ImageFont.truetype(font_path, font_size)
checkmark_font = ImageFont.truetype(font_path, checkmark_font_size)

def display_text(line1, line2, symbol=""):
    Himage = Image.new('1', (epd.width, epd.height), 255)  # White background
    draw = ImageDraw.Draw(Himage)
    
    bbox1 = draw.textbbox((0, 0), line1, font=font)
    text_width1 = bbox1[2] - bbox1[0]
    text_height1 = bbox1[3] - bbox1[1]
    
    bbox2 = draw.textbbox((0, 0), line2, font=font)
    text_width2 = bbox2[2] - bbox2[0]
    text_height2 = bbox2[3] - bbox2[1]
    
    bbox3 = draw.textbbox((0, 0), symbol, font=checkmark_font)
    text_width3 = bbox3[2] - bbox3[0]
    text_height3 = bbox3[3] - bbox3[1]
    
    x1, x2, x3 = (epd.width - text_width1) // 2, (epd.width - text_width2) // 2, (epd.width - text_width3) // 2
    y1, y2, y3 = 100, 180, 260
    
    draw.text((x1, y1), line1, font=font, fill=0)
    draw.text((x2, y2), line2, font=font, fill=0)
    draw.text((x3, y3), symbol, font=checkmark_font, fill=0)
    
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

def show_default():
    display_text("Please report cleanliness", "Press button to continue", "↓")

def show_confirm():
    display_text("Press again to confirm", "", "↓")

def show_reported():
    display_text("Report Submitted", "Successfully", "✔")

def clear_display():
    epd.Clear()
    epd.sleep()

if __name__ == "__main__":
    show_default()