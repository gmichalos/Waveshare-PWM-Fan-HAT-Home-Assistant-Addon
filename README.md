# Waveshare PWM Fan HAT - Home Assistant Addon

Home Assistant addon for the Waveshare PWM Controlled Fan HAT with OLED display and configurable display modes.

![Waveshare Fan HAT](https://www.waveshare.com/media/catalog/product/cache/1/image/800x800/9df78eab33525d08d6e5fb8d27136e95/f/a/fan-hat-1.jpg)

## Features

- 🌡️ **Automatic Temperature-Based Fan Control** - PWM fan speed adjusts based on CPU temperature
- 📊 **OLED Display** - 128x32 pixel display showing real-time information
- 🔄 **Dual Display Modes**:
  - **Fan Status Mode**: Shows temperature, fan speed, and ON/OFF status
  - **IP Address Mode**: Shows temperature, fan speed, and IP address
- ⚙️ **Fully Configurable** - Customize temperature thresholds, update intervals, and display settings
- 🔁 **Display Rotation** - 180° rotation support for flexible mounting
- 💾 **IP Caching** - Efficient IP detection with 60-second caching

## Hardware Requirements

- Raspberry Pi (3/4/5) running Home Assistant OS
- [Waveshare PWM Controlled Fan HAT](https://www.waveshare.com/wiki/Fan_HAT)
- I2C enabled on your system

## Installation

### 1. Enable I2C

**I2C must be enabled before installing this addon.**

#### Option A: Using HassOS I2C Configurator (Recommended)

1. Go to **Settings** → **Add-ons** → **Add-on Store**
2. Click **⋮** (three dots) → **Repositories**
3. Add repository: `https://github.com/adamoutler/HassOSConfigurator`
4. Install **HassOS I2C Configurator**
5. Start the addon
6. Restart Home Assistant

#### Option B: Manual Configuration

See [Home Assistant I2C Documentation](https://www.home-assistant.io/common-tasks/os/#enable-i2c)

### 2. Install the Addon

1. Go to **Settings** → **Add-ons** → **Add-on Store**
2. Click **⋮** (three dots) → **Repositories**
3. Add this repository: `https://github.com/gmichalos/Waveshare-PWM-Fan-HAT-Home-Assistant-Addon`
4. Install **Waveshare PWM Fan HAT**
5. Configure (see below)
6. Start the addon

## Configuration

### Basic Configuration

```yaml
fan_min_temp: 25        # Minimum temperature (°C) to start the fan
fan_max_temp: 80        # Maximum temperature (°C) for full fan speed
delta_temp: 5           # Minimum temperature change to trigger update
update_interval: 2      # Update interval in seconds
rotate_oled: false      # Rotate the OLED display 180 degrees
display_mode: fan_status # Display mode: fan_status or ip_address
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `fan_min_temp` | integer | `25` | Temperature (°C) at which the fan starts running |
| `fan_max_temp` | integer | `80` | Temperature (°C) at which the fan runs at 100% speed |
| `delta_temp` | integer | `5` | Minimum temperature change (°C) to trigger fan speed update |
| `update_interval` | integer | `2` | Display and sensor update interval in seconds |
| `rotate_oled` | boolean | `false` | Rotate display 180° (useful for inverted mounting) |
| `display_mode` | list | `fan_status` | Choose between `fan_status` or `ip_address` |

### Display Modes

#### Fan Status Mode (Default)
Shows comprehensive cooling system information:
```
Row 1: Temp(C):        45.3
Row 2: Fan: 50%    Status: ON
```

**Best for:**
- Monitoring cooling performance
- Troubleshooting temperature issues
- Verifying fan operation

#### IP Address Mode
Shows network information with cooling status:
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

## Display Layout

### Screen Specifications
- **Size**: 0.91 inch OLED
- **Resolution**: 128x32 pixels
- **Interface**: I2C (SSD1306 controller)
- **Colors**: Monochrome (white on black)

### Font & Spacing
- Default bitmap font (built-in)
- Automatic positioning for optimal readability
- Temperature displayed without decimals in IP mode to save space

## Fan Control Logic

The fan speed is calculated based on a linear relationship between minimum and maximum temperatures:

```
if temp < fan_min_temp:
    speed = 0%
elif temp >= fan_max_temp:
    speed = 100%
else:
    speed = (temp - fan_min_temp) / (fan_max_temp - fan_min_temp) × 100%
```

### Delta Temperature Feature

The `delta_temp` setting prevents constant fan speed adjustments from minor temperature fluctuations:
- Fan speed only updates when temperature changes by at least `delta_temp` degrees
- Reduces noise and wear on the fan
- Default: 5°C

**Example:**
- Current temp: 50°C, Fan: 50%
- Temp rises to 52°C → No change (< 5°C delta)
- Temp rises to 55°C → Fan speed updates (≥ 5°C delta)

## IP Address Detection

### How It Works
The addon detects your primary IP address by:
1. Opening a UDP socket connection to 8.8.8.8:80 (Google DNS)
2. Reading the local socket address (your IP)
3. Closing the connection (no data is transmitted)

### Caching Mechanism
- IP is cached for **60 seconds** to reduce unnecessary network calls
- Automatically refreshes every minute
- Falls back to "No IP" if network is unavailable
- Updates immediately on addon restart

### Supported Interfaces
Works with all network interfaces:
- Ethernet (eth0)
- WiFi (wlan0)
- USB adapters
- Any other active network interface

## Troubleshooting

### Addon Won't Start - I2C Error

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory
```

**Solution:**
I2C is not enabled. Follow the [Installation](#1-enable-i2c) steps to enable I2C.

**Verify I2C is working:**
```bash
ls -l /dev/i2c-*
```
You should see `/dev/i2c-1` or `/dev/i2c-0`

### Display Shows "No IP"

**Possible causes:**
1. No network connection
2. Network interface not configured
3. Firewall blocking outbound UDP to 8.8.8.8

**Solution:**
- Check network connection in Home Assistant
- Verify network settings
- Wait 60 seconds for cache refresh

### Fan Not Running

**Check:**
1. Is the temperature above `fan_min_temp`?
2. Is the fan physically connected to the HAT?
3. Check addon logs for errors

### Display is Upside Down

**Solution:**
Set `rotate_oled: true` in configuration

### Temperature Readings Seem Wrong

**Note:**
Temperature is read from `/sys/class/thermal/thermal_zone0/temp`
- This is the CPU temperature, not ambient temperature
- Raspberry Pi CPUs can run hot (60-80°C is normal under load)
- Adjust `fan_min_temp` and `fan_max_temp` to your preference

## Technical Details

### Hardware Specifications

**Waveshare PWM Fan HAT:**
- PCA9685 PWM driver (16-channel)
- SSD1306 OLED display (128x32)
- I2C bus communication
- 3007 size PWM fan (up to 8000 RPM)
- I2C addresses: 0x40 (PCA9685), varies (SSD1306)

### Software Stack

- **Base**: Python 3
- **Libraries**:
  - `Pillow` (PIL) - Image rendering
  - `smbus` - I2C communication
  - Standard Python libraries (socket, time)

### Performance

- **CPU Usage**: Minimal (<1%)
- **Memory**: ~20MB
- **Update Rate**: Configurable (default 2 seconds)
- **Fan PWM Frequency**: 80 Hz

## Advanced Configuration

### Fine-Tuning Fan Curve

For quieter operation:
```yaml
fan_min_temp: 30   # Start fan later
fan_max_temp: 70   # Reach max speed sooner
delta_temp: 3      # More responsive
```

For maximum cooling:
```yaml
fan_min_temp: 20   # Start fan earlier
fan_max_temp: 85   # Allow higher temps before max speed
delta_temp: 2      # Very responsive
```

For silent operation:
```yaml
fan_min_temp: 40   # Start fan only when hot
fan_max_temp: 75   # Conservative max speed
delta_temp: 10     # Minimize speed changes
```

### Faster Display Updates

```yaml
update_interval: 1  # Update every second
```

**Note:** Lower intervals increase CPU usage slightly.

## Contributing

Contributions are welcome! Please:
1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Development

To modify the addon:
1. Clone the repository
2. Edit files in `lib/waveshare_pwm_fan_hat/`
3. Update version in `config.yaml`
4. Test thoroughly
5. Submit PR with description of changes

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Credits

- **Original Author**: [Fsilva13](https://github.com/Fsilva13/Waveshare-PWM-Fan-HAT-Home-Assistant-Addon)
- **Modified By**: [gmichalos](https://github.com/gmichalos)
- **Hardware**: [Waveshare Electronics](https://www.waveshare.com)

## Support

- **Hardware Documentation**: [Waveshare Wiki](https://www.waveshare.com/wiki/Fan_HAT)
- **Issues**: [GitHub Issues](https://github.com/gmichalos/Waveshare-PWM-Fan-HAT-Home-Assistant-Addon/issues)
- **Home Assistant**: [Community Forum](https://community.home-assistant.io)

## Changelog

### v0.2.0
- ✨ Added IP address display mode
- ⚡ Implemented IP caching (60-second intervals)
- 🎨 Optimized display layout for 128x32 screen
- 📝 Improved documentation
- 🐛 Bug fixes and performance improvements

### v0.1.1
- Initial release
- Basic fan control and temperature monitoring
- OLED display support
- Display rotation

---

**Enjoy your cooled Raspberry Pi!** 🎉
