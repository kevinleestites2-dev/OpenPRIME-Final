"""
ADB/Tasker Integration for OpenPRIME
Enables device control and automation
"""

import subprocess
import json
import os

class AndroidController:
    def __init__(self):
        self.device_id = None
        self._connect_device()
    
    def _connect_device(self):
        """Connect to Android device via ADB"""
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            for line in lines[1:]:
                if "device" in line and "emulator" not in line:
                    self.device_id = line.split("\t")[0]
                    print(f"✅ Connected to device: {self.device_id}")
                    return
            print("⚠️ No device found. Run 'adb connect' first.")
        except FileNotFoundError:
            print("⚠️ ADB not installed. Run: pkg install android-tools")
    
    def tap(self, x, y):
        """Tap at coordinates"""
        if self.device_id:
            subprocess.run(["adb", "-s", self.device_id, "shell", f"input tap {x} {y}"])
            return f"Tapped at ({x}, {y})"
        return "Device not connected"
    
    def swipe(self, x1, y1, x2, y2, duration=300):
        """Swipe from (x1,y1) to (x2,y2)"""
        if self.device_id:
            subprocess.run(["adb", "-s", self.device_id, "shell", f"input swipe {x1} {y1} {x2} {y2} {duration}"])
            return f"Swiped from ({x1},{y1}) to ({x2},{y2})"
        return "Device not connected"
    
    def type_text(self, text):
        """Type text"""
        if self.device_id:
            # Escape special characters
            safe_text = text.replace(" ", "%s").replace('"', '\\"')
            subprocess.run(["adb", "-s", self.device_id, "shell", f"input text '{safe_text}'"])
            return f"Typed: {text[:50]}..."
        return "Device not connected"
    
    def press_key(self, key_code):
        """Press a key (KEYCODE_HOME, KEYCODE_BACK, KEYCODE_APP_SWITCH, etc.)"""
        if self.device_id:
            subprocess.run(["adb", "-s", self.device_id, "shell", f"input keyevent {key_code}"])
            return f"Pressed key: {key_code}"
        return "Device not connected"
    
    def press_home(self):
        return self.press_key(3)
    
    def press_back(self):
        return self.press_key(4)
    
    def press_recent(self):
        return self.press_key(187)
    
    def launch_app(self, package_name):
        """Launch app by package name"""
        if self.device_id:
            subprocess.run(["adb", "-s", self.device_id, "shell", f"monkey -p {package_name} 1"])
            return f"Launched: {package_name}"
        return "Device not connected"
    
    def get_screen_size(self):
        """Get screen dimensions"""
        if self.device_id:
            result = subprocess.run(["adb", "-s", self.device_id, "shell", "wm size"], capture_output=True, text=True)
            return result.stdout.strip()
        return "Device not connected"
    
    def take_screenshot(self, path="/sdcard/screenshot.png"):
        """Take screenshot"""
        if self.device_id:
            subprocess.run(["adb", "-s", self.device_id, "shell", f"screencap {path}"])
            return f"Screenshot saved to {path}"
        return "Device not connected"
    
    def pull_file(self, remote_path, local_path):
        """Copy file from device"""
        if self.device_id:
            subprocess.run(["adb", "-s", self.device_id, "pull", remote_path, local_path])
            return f"Pulled {remote_path} to {local_path}"
        return "Device not connected"
    
    def run_tasker_task(self, task_name):
        """Execute a Tasker task (requires Tasker + ADB Wifi)"""
        if self.device_id:
            subprocess.run(["adb", "-s", self.device_id, "shell", f"am broadcast -a net.dinglisch.android.tasker.ACTION_TASK -e task_name {task_name}"])
            return f"Tasker task started: {task_name}"
        return "Device not connected"
    
    def get_clipboard(self):
        """Get current clipboard content"""
        if self.device_id:
            result = subprocess.run(["adb", "-s", self.device_id, "shell", "cmd clipboard get-text"], capture_output=True, text=True)
            return result.stdout.strip()
        return "Device not connected"

class TaskerAutomation:
    def __init__(self, controller):
        self.controller = controller
        self.rules = []
    
    def when_phone_unlocks(self, action):
        """Trigger action when phone is unlocked"""
        self.rules.append({"trigger": "unlock", "action": action})
        print(f"📱 Rule added: On unlock -> {action}")
    
    def when_time(self, hour, action):
        """Trigger action at specific time"""
        self.rules.append({"trigger": f"time:{hour}", "action": action})
        print(f"⏰ Rule added: At {hour}:00 -> {action}")
    
    def when_battery_low(self, threshold=15, action=None):
        """Trigger when battery below threshold"""
        self.rules.append({"trigger": f"battery<{threshold}", "action": action})
        print(f"🔋 Rule added: Battery <{threshold}% -> {action}")

# Singleton for OpenPRIME
android = AndroidController()
tasker = TaskerAutomation(android)

print("✅ ADB/Tasker integration ready")
print(f"Device: {android.device_id or 'Not connected'}")
