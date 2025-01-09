'''
This is scratch code
on attempting to do the button
when the GSU bookstore rate limits

Not needed for now, but maybe next
semester
'''



from datetime import datetime
from pynput import mouse, keyboard
from PIL import ImageGrab
from PIL import Image, ImageChops
snapshot = ImageGrab.grab(all_screens=True)
snapshot.save(r"D:\OneDriveGSU\OneDrive - Georgia State University\Desktop\Press.png")


# location (-1085, 340)

def time_release():
    mo.release(mouse.Button.left)
    return datetime.now()


mo = mouse.Controller()

begin = datetime.now()
mo.position = (-1085, 340)
mo.press(mouse.Button.left)
time.sleep(1)
snapshot2 = ImageGrab.grab(all_screens=True)
second = datetime.now()
#mo.release(mouse.Button.left)
rel = time_release()

left, top, right, bottom = 625, 275, 1065, 432
sh = snapshot.crop((left, top, right, bottom))
sh.show()

sh2 = snapshot2.crop((left, top, right, bottom))


diff = ImageChops.difference(sh2,sh)


px = diff.load()
px[14,80] # around 190-200 for each
sh.getpixel((429,80)) # this is the end

# Loop over, see how far it is after 2 seconds
# interpolate for how long left to hold
# stop after it is finished + a few microseconds
# check again after 10 seconds
# repeat

def check_fill():
    snapshot = ImageGrab.grab(all_screens=True)
    left, top, right, bottom = 625, 275, 1065, 432
    sh = snapshot.crop((left, top, right, bottom))
    pix = sh.getpixel(429,80)
    if pix[0] > 190:
        return False
    else:
        return True

# load old image
old = ....

def check_button(new,old=old)
    diff = ImageChops.difference(new,old)
    # check how many black, if majority it is check button
    # check against pure white as a control


def push_button():
    # See if it is a button
    snapshot = ImageGrab.grab(all_screens=True)
    left, top, right, bottom = 625, 275, 1065, 432
    sh = snapshot.crop((left, top, right, bottom))
    # Check to see if button is up on the screen
    if button:
        mo = mouse.Controller()
        mo.position = (-1085, 340)
        mo.press(mouse.Button.left)
        not_filled = True
        while not_filled:
            time.sleep(0.1)
            not_filled = check_fill()
        mo.release(mouse.Button.left)
        return 1
    else:
        return 0

