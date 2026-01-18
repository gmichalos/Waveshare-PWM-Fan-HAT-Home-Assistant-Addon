import socket
import time

from PIL import Image, ImageDraw, ImageFont

from . import PCA9685
from . import SSD1306

# Initialize oled
oled = SSD1306.SSD1306()
oled.Init()
oled.ClearBlack()

pwm = PCA9685.PCA9685(0x40, debug=False)
pwm.setPWMFreq(80)  # Set PWM frequency to 80 Hz
pwm.setServoPulse(0, 100)

# Create blank image for drawing.
image1 = Image.new('1', (oled.width, oled.height), "WHITE")
draw = ImageDraw.Draw(image1)
font = ImageFont.load_default()
# dir_path = os.path.dirname(os.path.abspath(__file__))
# font = ImageFont.truetype(dir_path+'/Courier_New.ttf',13)

class PwmFanHat:
    def __init__(self):
        self.last_speed = 0
        self.last_temp = None
        self.cached_ip = None
        self.ip_last_update = 0
        self.ip_cache_duration = 60  # Cache IP for 60 seconds

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def get_cached_ip(self):
        """Get IP address with caching to avoid excessive socket connections"""
        current_time = time.time()
        if self.cached_ip is None or (current_time - self.ip_last_update) > self.ip_cache_duration:
            try:
                self.cached_ip = self.get_ip()
                self.ip_last_update = current_time
            except:
                if self.cached_ip is None:
                    self.cached_ip = "No IP"
        return self.cached_ip

    @staticmethod
    def get_temp():
        with open('/sys/class/thermal/thermal_zone0/temp', 'rt') as f:
            temp = int(f.read()) / 1000.0
        return temp

    @staticmethod
    def fan_off():
        pwm.setServoPulse(0, 0)

    def update_fan(self, fan_min_temp, fan_max_temp, delta_temp):
        """
        Updates the fan speed based on the current temperature.

        Args:
            fan_min_temp (float): The minimum temperature to start the fan.
            fan_max_temp (float): The maximum temperature for full fan speed.
            delta_temp (float): The minimum temperature change to trigger an update.

        Returns:
            tuple: The current temperature and fan speed percentage.
        """
        temp = self.get_temp()
        # Only update speed if temp change exceeds delta_temp
        if self.last_temp is None or abs(temp - self.last_temp) >= delta_temp:
            if temp < fan_min_temp:
                speed = 0
            elif temp >= fan_max_temp:
                speed = 100
            else:
                speed = int(100 * (temp - fan_min_temp) / (fan_max_temp - fan_min_temp))
            pwm.setServoPulse(0, speed)
            self.last_speed = speed
            self.last_temp = temp
        else:
            speed = self.last_speed
        return temp, speed

    def update_oled(self, temp, speed, rotate_oled, display_mode="fan_status"):
        """
        Updates the OLED display with the current temperature and fan status or IP address.

        Args:
            temp (float): The current temperature in Celsius.
            speed (int): The current fan speed percentage.
            rotate_oled (bool): Whether to rotate the OLED display.
            display_mode (str): Display mode - 'fan_status' or 'ip_address'.
        """
        draw.rectangle((0, 0, 128, 32), fill=1)
        
        if display_mode == "ip_address":
            # Display IP Address mode
            # Row 1: Temp:XX (at x=0) and Fan:X% (at x=70)
            # Row 2: IP:xxx.xxx.xxx.xxx
            ip = self.get_cached_ip()
            
            draw.text((0, 0), f"Temp:{temp:.0f}C", font=font, fill=0)
            draw.text((70, 0), f"Fan:{speed}%", font=font, fill=0)
            draw.text((0, 16), f"IP:{ip}", font=font, fill=0)
        else:
            # Display fan status mode (original behavior)
            draw.text((0, 0), "Temp(C):", font=font, fill=0)
            draw.text((70, 0), str(temp), font=font, fill=0)
            draw.text((0, 16), f"Fan: {speed}%", font=font, fill=0)
            status = "ON" if speed > 0 else "OFF"
            draw.text((70, 16), f"Status: {status}", font=font, fill=0)

        # Rotate and display the image
        if rotate_oled:
            oled.ShowImage(oled.getbuffer(image1.rotate(180)))
        else:
            oled.ShowImage(oled.getbuffer(image1))

    def update(self, fan_min_temp, fan_max_temp, delta_temp, update_interval, rotate_oled, display_mode="fan_status"):
        """
        Updates the fan speed and OLED display at regular intervals.

        Args:
            fan_min_temp (float): The minimum temperature to start the fan.
            fan_max_temp (float): The maximum temperature for full fan speed.
            delta_temp (float): The minimum temperature change to trigger an update.
            update_interval (float): The time interval (in seconds) between updates.
            rotate_oled (bool): Whether to rotate the OLED display.
            display_mode (str): Display mode - 'fan_status' or 'ip_address'.
        """
        temp, speed = self.update_fan(fan_min_temp, fan_max_temp, delta_temp)
        self.update_oled(temp, speed, rotate_oled, display_mode)
        time.sleep(update_interval)
