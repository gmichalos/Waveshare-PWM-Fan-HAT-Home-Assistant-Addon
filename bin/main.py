import json
import os
import sys
import time

from PIL import Image, ImageDraw, ImageFont

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging

# Wait for I2C to be ready
max_retries = 10
retry_delay = 2

for attempt in range(max_retries):
    if os.path.exists('/dev/i2c-1') or os.path.exists('/dev/i2c-0'):
        break
    if attempt < max_retries - 1:
        logging.info(f"Waiting for I2C device... (attempt {attempt + 1}/{max_retries})")
        time.sleep(retry_delay)
else:
    logging.error("I2C device not found after waiting. Please ensure I2C is enabled.")
    sys.exit(1)

from waveshare_pwm_fan_hat import PwmFanHat

logging.basicConfig(level=logging.INFO)
font = ImageFont.load_default()
pfh = PwmFanHat.PwmFanHat()

options_file = open("/data/options.json", "r")
config = json.load(options_file)
fan_min_temp = config["fan_min_temp"]
fan_max_temp = config["fan_max_temp"]
delta_temp = config["delta_temp"]
update_interval = config["update_interval"]
rotate_oled = config["rotate_oled"]
display_mode = config.get("display_mode", "fan_status")
options_file.close()

while True:
    pfh.update(
        fan_min_temp=fan_min_temp,
        fan_max_temp=fan_max_temp,
        delta_temp=delta_temp,
        update_interval=update_interval,
        rotate_oled=rotate_oled,
        display_mode=display_mode,
    )
