# Haptique IR/RF Hub - Complete User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [What You'll Need](#what-youll-need)
3. [Installation Guide](#installation-guide)
4. [Initial Setup](#initial-setup)
5. [Learning Commands](#learning-commands)
6. [Using Learned Commands](#using-learned-commands)
7. [Advanced Usage](#advanced-usage)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## Introduction

The Haptique IR/RF Hub integration allows you to control infrared and radio frequency devices through Home Assistant. This guide will walk you through every step, from installation to creating advanced automations.

### What Can You Control?

- **Infrared (IR) Devices**: TVs, air conditioners, set-top boxes, audio systems, projectors, fans
- **Radio Frequency (RF) Devices**: RF-controlled lights, fans, switches, garage doors, blinds (433MHz)

---

## What You'll Need

Before starting, make sure you have:

- ✅ Home Assistant installed and running (minimum version 2023.1.0)
- ✅ Haptique IR/RF Hub device (powered and connected to your network)
- ✅ Haptique Config App installed on your smartphone
- ✅ Your original remote controls (IR or RF) for the devices you want to control
- ✅ Access to your Home Assistant configuration files

---

## Installation Guide

### Step 1: Install HACS

HACS (Home Assistant Community Store) is required to install this custom integration.

1. If you haven't installed HACS yet, visit [https://hacs.xyz](https://hacs.xyz) and follow the installation instructions
2. After installation, restart Home Assistant
3. Go to **HACS** in your Home Assistant sidebar to verify it's working

### Step 2: Add the Custom Repository

1. Open Home Assistant in your web browser
2. Navigate to **HACS** from the sidebar
3. Click on **Integrations**
4. Click the **three-dot menu** (⋮) in the top right corner
5. Select **Custom repositories**
6. In the popup window:
   - **Repository URL**: `https://github.com/Cantata-Communication-Solutions/haptique_ir_rf_hub`
   - **Category**: Select `Integration`
7. Click **Add**
8. Close the custom repositories window

### Step 3: Install the Integration

1. Still in HACS > Integrations, click the **+ Explore & Download Repositories** button
2. In the search box, type: `Haptique IR/RF Hub`
3. Click on the **Haptique IR/RF Hub** integration
4. Click the **Download** button in the bottom right
5. Select the latest version and click **Download**
6. Wait for the download to complete
7. **Restart Home Assistant**:
   - Go to **Settings** > **System** > **Restart**
   - Click **Restart** and wait for Home Assistant to come back online

---

## Initial Setup

### Step 1: Configure Your Hub in Haptique Config App

Before adding the integration to Home Assistant, you must set up your Haptique IR/RF Hub:

1. Open the **Haptique Config App** on your smartphone
2. Add your Haptique IR/RF Hub device if you haven't already
3. Make sure the device is connected to your Wi-Fi network
4. Note down the following information (you'll need this in the next step):
   - **Device IP Address** (e.g., `192.168.1.100`)
   - **Device Token** (a unique authentication code)

**Tip**: Take a screenshot of this information or write it down for easy reference.

### Step 2: Add the Integration to Home Assistant

1. Go to **Settings** > **Devices & Services**
2. Click the **+ Add Integration** button (bottom right)
3. In the search box, type: `Haptique IR/RF Hub`
4. Click on **Haptique IR/RF Hub** when it appears
5. Enter the required information:
   - **Device IP**: Enter the IP address from your Haptique Config App
   - **Token**: Enter the token from your Haptique Config App
6. Click **Submit**

If successful, you'll see a confirmation message and the integration will appear in your devices list.

### Step 3: Verify the Installation

1. Go to **Settings** > **Devices & Services**
2. Look for **Haptique IR/RF Hub** in the list
3. Click on it to see the device details
4. You should see your hub listed with its IP address

---

## Learning Commands

To use your remote controls with Home Assistant, you first need to "teach" the Hub what each button does.

### Step 1: Set Up the Learning Interface

#### Create the Lovelace Card

1. Go to your Home Assistant dashboard
2. Click the **three-dot menu** (⋮) in the top right
3. Select **Edit Dashboard**
4. Click **+ Add Card** at the bottom
5. Scroll down and select **Manual** or **Code Editor**
6. Delete any existing code and paste the following:

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      ## 📚 Learn Commands
      Steps:
      1. Point remote at HUB  
      2. Press button  
      3. Type name  
      4. Toggle switch  
  - type: entities
    title: RF Command (433MHz)
    entities:
      - input_text.rf_command_name
      - input_boolean.save_rf_trigger
  - type: entities
    title: IR Command (Infrared)
    entities:
      - input_text.ir_command_name
      - input_boolean.save_ir_trigger
```

7. Click **Save**
8. Position the card where you want it on your dashboard
9. Click **Done** to exit edit mode

#### Add the Configuration Code

1. Access your Home Assistant configuration files:
   - **Option A**: Use File Editor add-on (Settings > Add-ons > File Editor)
   - **Option B**: Use VS Code add-on
   - **Option C**: Use SSH or Samba to access the files directly

2. **First, edit `configuration.yaml`**:

Add the following code at the end of the file (make sure the indentation is correct):

```yaml
input_text:
  rf_command_name:
    name: "RF Command Name"
    max: 50
  ir_command_name:
    name: "IR Command Name"
    max: 50

input_boolean:
  save_rf_trigger:
    name: "Save RF Trigger"
    icon: mdi:content-save
  save_ir_trigger:
    name: "Save IR Trigger"
    icon: mdi:content-save

# Make sure this line exists (it tells HA to use automations.yaml)
automation: !include automations.yaml
```

3. Save the `configuration.yaml` file

4. **Next, edit `automations.yaml`**:

Open the `automations.yaml` file (it's in the same folder as configuration.yaml). Add the following automations:

```yaml
- alias: "Save RF Command"
  mode: single
  trigger:
    - platform: state
      entity_id: input_boolean.save_rf_trigger
      to: "on"
  condition:
    - condition: template
      value_template: "{{ states('input_text.rf_command_name') | length > 0 }}"
  action:
    - service: haptique_ir_rf_hub.save_rf_last
      data:
        name: "{{ states('input_text.rf_command_name') }}"
    - delay: "00:00:00.5"
    - service: persistent_notification.create
      data:
        title: "✅ RF Saved"
        message: "Command saved!"
    - service: input_text.set_value
      data:
        entity_id: input_text.rf_command_name
        value: ""
    - service: input_boolean.turn_off
      target:
        entity_id: input_boolean.save_rf_trigger

- alias: "Save IR Command"
  mode: single
  trigger:
    - platform: state
      entity_id: input_boolean.save_ir_trigger
      to: "on"
  condition:
    - condition: template
      value_template: "{{ states('input_text.ir_command_name') | length > 0 }}"
  action:
    - service: haptique_ir_rf_hub.save_ir_last
      data:
        name: "{{ states('input_text.ir_command_name') }}"
        frame: "B"
    - delay: "00:00:00.5"
    - service: persistent_notification.create
      data:
        title: "✅ IR Saved"
        message: "Command saved!"
    - service: input_text.set_value
      data:
        entity_id: input_text.ir_command_name
        value: ""
    - service: input_boolean.turn_off
      target:
        entity_id: input_boolean.save_ir_trigger
```

**Important Notes:**
- If `automations.yaml` already has automations (from GUI), just add these two at the end
- If the file is empty or shows `[]`, replace it with the code above
- DO NOT put automations in `configuration.yaml` - this disables the GUI automation editor!
- By using `automations.yaml`, you can still create automations from the GUI

5. Save the `automations.yaml` file

6. **Restart Home Assistant**:
   - Go to **Settings** > **System** > **Check Configuration**
   - If no errors are shown, click **Restart**
   - Wait for Home Assistant to restart

### Step 2: Learn IR Commands (Infrared)

Now you're ready to learn your first infrared command!

**Example: Learning a TV Power Button**

1. Make sure your Haptique IR/RF Hub is powered on and the learning card is visible on your dashboard

2. Take your TV remote and point it directly at the Haptique Hub (within 10-30 cm / 4-12 inches)

3. Press the **Power** button on your TV remote once

4. In the Home Assistant learning card:
   - Find the **IR Command (Infrared)** section
   - Click on **IR Command Name**
   - Type a descriptive name: `tv_power` (use lowercase, no spaces - use underscores instead)
   - Toggle the **Save IR Trigger** switch to ON

5. Wait a moment - you should see a notification: **"✅ IR Saved - Command saved!"**

6. The command is now stored in your Hub!

**Recommended Naming Convention:**
- Use lowercase letters
- Use underscores instead of spaces
- Be descriptive: `tv_power`, `tv_volume_up`, `tv_hdmi_1`, `ac_cool_mode`, `fan_speed_1`

**Repeat this process for each button** you want to control:
- TV: power, volume up/down, channel up/down, input/source buttons
- Air Conditioner: power, temperature up/down, fan speed, mode
- Fan: power, speed settings, oscillation

### Step 3: Learn RF Commands (433MHz)

Learning RF commands is identical to IR commands, just using the RF section.

**Example: Learning an RF Light Switch**

1. Point your RF remote at the Haptique Hub

2. Press the button you want to learn (e.g., "Light ON")

3. In the Home Assistant learning card:
   - Find the **RF Command (433MHz)** section
   - Click on **RF Command Name**
   - Type a name: `light_on`
   - Toggle the **Save RF Trigger** switch to ON

4. Wait for the confirmation notification

5. Repeat for other buttons: `light_off`, `fan_on`, `fan_off`, etc.

### Best Practices for Learning Commands

✅ **DO:**
- Test each button immediately after learning
- Use consistent naming conventions
- Keep the remote steady when pressing buttons
- Learn commands in a quiet environment (less RF interference)
- Make a list of all learned commands for reference

❌ **DON'T:**
- Use spaces in command names
- Press buttons multiple times quickly
- Move the remote while pressing the button
- Forget to enter a name before toggling the save switch

---

## Using Learned Commands

Once commands are learned, they're stored in the Hub and can be used in various ways.

### Method 1: As Entities in Automations

All learned commands become entities that can trigger actions.

**Example: Turn on TV at a specific time**

1. Go to **Settings** > **Automations & Scenes**
2. Click **+ Create Automation**
3. Click **Create new automation**
4. Add a trigger (e.g., Time trigger at 7:00 PM)
5. Add an action:
   - Action type: **Call service**
   - Service: `haptique_ir_rf_hub.send_ir`
   - Service data:
     ```yaml
     name: "tv_power"
     ```
6. Save the automation

### Method 2: As Dashboard Buttons

Create easy-to-use buttons on your dashboard.

**Example: TV Control Panel**

```yaml
type: horizontal-stack
cards:
  - type: button
    name: Power
    icon: mdi:power
    tap_action:
      action: call-service
      service: haptique_ir_rf_hub.send_ir
      data:
        name: "tv_power"
  - type: button
    name: Vol +
    icon: mdi:volume-plus
    tap_action:
      action: call-service
      service: haptique_ir_rf_hub.send_ir
      data:
        name: "tv_volume_up"
  - type: button
    name: Vol -
    icon: mdi:volume-minus
    tap_action:
      action: call-service
      service: haptique_ir_rf_hub.send_ir
      data:
        name: "tv_volume_down"
```

### Method 3: In Scripts

Create reusable scripts for common actions.

**Example: Movie Mode Script**

```yaml
movie_mode:
  alias: "Start Movie Mode"
  sequence:
    - service: haptique_ir_rf_hub.send_ir
      data:
        name: "tv_power"
    - delay: "00:00:02"
    - service: haptique_ir_rf_hub.send_ir
      data:
        name: "tv_hdmi_1"
    - delay: "00:00:01"
    - service: light.turn_off
      target:
        entity_id: light.living_room
```

---

## Advanced Usage

### Creating Complex Scenes

Combine multiple IR/RF commands with other Home Assistant actions:

```yaml
scene:
  - name: "Good Night"
    entities:
      light.bedroom:
        state: off
      light.living_room:
        state: off
    script:
      - service: haptique_ir_rf_hub.send_ir
        data:
          name: "tv_power"
      - service: haptique_ir_rf_hub.send_ir
        data:
          name: "ac_power"
      - service: haptique_ir_rf_hub.send_rf
        data:
          name: "fan_off"
```

### Voice Control Integration

If you have Google Assistant or Alexa integrated with Home Assistant:

1. Create scripts for your commands
2. Expose the scripts to your voice assistant
3. Use voice commands like "Hey Google, turn on the TV"

### Conditional Automations

**Example: Only turn on AC if temperature is above 25°C**

```yaml
automation:
  - alias: "Auto AC Control"
    trigger:
      - platform: numeric_state
        entity_id: sensor.living_room_temperature
        above: 25
    condition:
      - condition: state
        entity_id: climate.living_room_ac
        state: "off"
    action:
      - service: haptique_ir_rf_hub.send_ir
        data:
          name: "ac_power"
      - delay: "00:00:02"
      - service: haptique_ir_rf_hub.send_ir
        data:
          name: "ac_cool_mode"
```

---

## Troubleshooting

### Problem: Integration Not Found After Installation

**Solution:**
1. Verify HACS is installed correctly
2. Clear your browser cache (Ctrl+F5)
3. Restart Home Assistant
4. Check HACS > Integrations to ensure it downloaded

### Problem: "Invalid Token" Error

**Solution:**
1. Open Haptique Config App
2. Re-generate or copy the token again
3. Remove the integration from Home Assistant
4. Re-add it with the new token

### Problem: Commands Not Learning

**Possible causes and solutions:**

1. **Remote too far away**: Move remote closer (10-30 cm from Hub)
2. **Forgot to enter command name**: Always enter a name before toggling the switch
3. **Hub not ready**: Wait a few seconds between learning commands
4. **Weak batteries in remote**: Replace remote batteries
5. **Wrong remote type**: Make sure you're using the correct section (IR vs RF)

### Problem: Learned Commands Don't Work

**Solution:**
1. Verify the Hub is online and responsive
2. Check if the command was saved correctly
3. Try re-learning the command
4. Ensure there's a clear line of sight between Hub and device
5. Check if the device you're controlling is powered on

### Problem: Can't Create Automations from GUI After Setup

**Cause**: If you put automations directly in `configuration.yaml` instead of `automations.yaml`, Home Assistant disables the GUI editor.

**Solution:**
1. Make sure your `configuration.yaml` has: `automation: !include automations.yaml`
2. Move the two learning automations from `configuration.yaml` to `automations.yaml`
3. Keep only `input_text` and `input_boolean` in `configuration.yaml`
4. Restart Home Assistant
5. GUI automation editor should now work

See the detailed fix guide included in the documentation files.

### Problem: Configuration Errors After Adding YAML

**Solution:**
1. Go to **Settings** > **System** > **Check Configuration**
2. Look for error messages - they usually indicate line numbers
3. Check your indentation (YAML is sensitive to spaces)
4. Use a YAML validator online to check your syntax
5. Make sure you didn't accidentally add the code inside another section

### Problem: Hub Offline or Unreachable

**Solution:**
1. Check if Hub is powered on (LED indicators)
2. Verify Hub is connected to Wi-Fi
3. Check if IP address has changed (router may have assigned a new one)
4. Set a static IP for the Hub in your router settings
5. Restart the Hub device

---

## FAQ

**Q: Can I control multiple devices with one Hub?**  
A: Yes! You can learn commands from multiple remotes and control many different devices.

**Q: How many commands can I store?**  
A: The Hub can store hundreds of commands. The exact number depends on your specific Hub model.

**Q: Can I use this with Broadlink devices?**  
A: No, this integration is specifically for Haptique IR/RF Hub devices.

**Q: Do I need internet connection for commands to work?**  
A: No, once configured, the Hub communicates locally on your network. Internet is only needed for initial setup.

**Q: Can I backup my learned commands?**  
A: Commands are stored in the Hub device itself. It's recommended to keep your original remotes as backup.

**Q: What's the range of the IR transmitter?**  
A: IR range is typically 5-10 meters, but requires line of sight to the device.

**Q: What's the range of the RF transmitter?**  
A: RF range is typically 30-50 meters and can go through walls, but may vary based on interference.

**Q: Can I edit a learned command?**  
A: To change a command, simply learn it again with the same name. It will overwrite the old one.

**Q: How do I delete a learned command?**  
A: Currently, commands must be managed through the Haptique Config App or by re-learning.

**Q: Will this work with my [specific device]?**  
A: If your device came with an IR or 433MHz RF remote, it should work. Test by learning a command.

---

## Support and Community

**Need more help?**

- 📖 Check the [GitHub repository](https://github.com/Cantata-Communication-Solutions/haptique_ir_rf_hub) for updates
- 🐛 Report bugs or request features on [GitHub Issues](https://github.com/Cantata-Communication-Solutions/haptique_ir_rf_hub/issues)
- 💬 Join the Home Assistant Community Forum
- 📧 Contact Cantata Communication Solutions support

---

## Appendix: Useful Command Examples

### TV Commands to Learn
- `tv_power`
- `tv_volume_up`
- `tv_volume_down`
- `tv_mute`
- `tv_channel_up`
- `tv_channel_down`
- `tv_input` or `tv_source`
- `tv_hdmi_1`, `tv_hdmi_2`, etc.
- `tv_menu`
- `tv_ok` or `tv_enter`
- `tv_back`
- `tv_home`

### Air Conditioner Commands to Learn
- `ac_power`
- `ac_temp_up`
- `ac_temp_down`
- `ac_fan_speed`
- `ac_mode` (cool/heat/fan/auto)
- `ac_swing`
- `ac_timer`

### Fan Commands to Learn
- `fan_power`
- `fan_speed_1`
- `fan_speed_2`
- `fan_speed_3`
- `fan_oscillate`
- `fan_timer`

### Audio System Commands to Learn
- `audio_power`
- `audio_volume_up`
- `audio_volume_down`
- `audio_mute`
- `audio_input_hdmi`
- `audio_input_bluetooth`
- `audio_input_aux`

---

**Document Version**: 1.0  
**Last Updated**: November 2024  
**Integration Version**: Latest

*This guide is maintained by Cantata Communication Solutions*
