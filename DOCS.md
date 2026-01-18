# Waveshare PWM Fan HAT - Home Assistant Addon

Home Assistant (HASS) Addon to support the Waveshare PWM Controlled Fan HAT with OLED display and configurable display modes.

![Waveshare Fan HAT](https://www.waveshare.com/media/catalog/product/cache/1/image/800x800/9df78eab33525d08d6e5fb8d27136e95/f/a/fan-hat-1.jpg)

## Important: Enable I2C First

⚠️ **I2C must be enabled before this addon will work.**

This can be done in a couple of ways:
- Follow the official guide: https://www.home-assistant.io/common-tasks/os/#enable-i2c
- Use the HassOS I2C Configurator: https://github.com/adamoutler/HassOSConfigurator

After enabling I2C, **restart your system** before starting this addon.

---

## Configuration Options

### Example Configuration

These options can be set in your add-on configuration:
```yaml
fan_min_temp: 25          # Minimum temperature (°C) to start the fan
fan_max_temp: 80          # Maximum temperature (°C) for full fan speed
delta_temp: 5             # Minimum temperature change to trigger update
update_interval: 2        # Update interval in seconds
rotate_oled: false        # Rotate the OLED display (true/false)
display_mode: fan_status  # Display mode: fan_status or ip_address
```

---

## Configuration Reference

### fan_min_temp
- **Type:** Integer
- **Default:** `25`
- **Description:** Temperature (°C) at which the fan starts running. Below this temperature, the fan is off.

### fan_max_temp
- **Type:** Integer
- **Default:** `80`
- **Description:** Temperature (°C) at which the fan runs at 100% speed. The fan speed increases linearly between min and max temperature.

### delta_temp
- **Type:** Integer
- **Default:** `5`
- **Description:** Minimum temperature change (°C) required to trigger a fan speed update. This prevents constant adjustments from minor temperature fluctuations.

### update_interval
- **Type:** Integer (seconds)
- **Default:** `2`
- **Description:** How often to update the display and check temperature. Lower values provide more responsive updates but use slightly more CPU.

### rotate_oled
- **Type:** Boolean
- **Default:** `false`
- **Description:** Rotate the OLED display by 180 degrees. Useful if the HAT is mounted upside down.

### display_mode
- **Type:** List (fan_status | ip_address)
- **Default:** `fan_status`
- **Description:** Choose what information to display on the OLED screen.

---

## Display Modes

### Fan Status Mode (Default)
Shows comprehensive cooling system information:

**Display:**
```
Row 1: Temp(C):        45
Row 2: Fan: 50%    Status: ON
```

**Best for:**
- Monitoring cooling performance
- Troubleshooting temperature issues
- Verifying fan operation

**Configuration:**
```yaml
display_mode: fan_status
```

---

### IP Address Mode
Shows network information with cooling status:

**Display:**
```
Row 1: Temp:45C      Fan:50%
Row 2: IP:192.168.1.100
```

**Best for:**
- Headless server setups
- Quick SSH connection info
- Network troubleshooting
- Multi-device identification

**Configuration:**
```yaml
display_mode: ip_address
```

**Note:** IP address is cached and updates every 60 seconds to minimize network overhead.

---

## Fan Control Behavior

The fan speed is calculated based on a linear relationship:
```
if temp < fan_min_temp:
    Fan Speed = 0%
    
elif temp >= fan_max_temp:
    Fan Speed = 100%
    
else:
    Fan Speed = (temp - fan_min_temp) / (fan_max_temp - fan_min_temp) × 100%
```

**Example with default settings (25°C min, 80°C max):**
- 20°C → Fan: 0%
- 25°C → Fan: 0%
- 30°C → Fan: 9%
- 50°C → Fan: 45%
- 80°C → Fan: 100%
- 85°C → Fan: 100%

---

## Advanced Configuration Examples

### Silent Operation
For minimal noise:
```yaml
fan_min_temp: 40
fan_max_temp: 75
delta_temp: 10
display_mode: ip_address
```

### Maximum Cooling
For heavy workloads:
```yaml
fan_min_temp: 20
fan_max_temp: 85
delta_temp: 2
update_interval: 1
```

### Balanced Performance
Recommended for most users:
```yaml
fan_min_temp: 30
fan_max_temp: 70
delta_temp: 5
update_interval: 2
```

---

## Troubleshooting

### Addon Won't Start - I2C Error
**Error:** `FileNotFoundError: No such file or directory`

**Solution:** I2C is not enabled. Follow the I2C setup instructions above.

**Verify I2C:**
```bash
ls -l /dev/i2c-*
```
You should see `/dev/i2c-1` or `/dev/i2c-0`

### Display Shows "No IP"
**Causes:**
- No network connection
- Network not configured
- Firewall blocking UDP to 8.8.8.8

**Solution:** Check network settings and wait 60 seconds for cache refresh.

### Fan Not Running
**Check:**
1. Is temperature above `fan_min_temp`?
2. Is the fan physically connected?
3. Check addon logs for errors

### Display is Upside Down
**Solution:** Set `rotate_oled: true` in configuration

---

## Hardware Information

**Specifications:**
- Display: 0.91" OLED, 128x32 pixels
- PWM Driver: PCA9685 (16-channel)
- Fan: 3007 size, up to 8000 RPM
- Interface: I2C bus

**Temperature Source:**
- Reads from: `/sys/class/thermal/thermal_zone0/temp`
- This is CPU temperature (not ambient)
- Normal range: 40-80°C under load

---

## Support

- **Hardware Documentation:** https://www.waveshare.com/wiki/Fan_HAT
- **GitHub Repository:** https://github.com/gmichalos/Waveshare-PWM-Fan-HAT-Home-Assistant-Addon
- **Issues:** Report bugs on GitHub

---

**Version:** 0.2.0
