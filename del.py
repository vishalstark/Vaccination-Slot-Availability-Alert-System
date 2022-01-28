import win32api
import random
    
for i in range(5):
    win32api.Beep(random.randint(37,10000), random.randint(750,3000))