#########################匯入模組#########################
import mcu
from machine import Pin, I2C
import ssd1306

#########################函式與類別定義#########################
gpio = mcu.gpio()
ic2 = I2C(scl=Pin(gpio.D1), sda=Pin(gpio.D2))
oled = ssd1306.SSD1306_I2C(128, 64, ic2)

#########################宣告與設定#########################

#########################主程式#########################
oled.fill(0)
oled.text("Hello", 0, 0)
oled.text("world!", 0, 8)
oled.show()
