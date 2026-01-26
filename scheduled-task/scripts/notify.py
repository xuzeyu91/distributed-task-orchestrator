#!/usr/bin/env python3
"""
Cross-platform notification module
Supports Windows, macOS, and Linux
"""

import subprocess
import sys
from typing import Optional


def send_notification(title: str, message: str, icon: Optional[str] = None) -> bool:
    """
    Send a desktop notification
    
    Args:
        title: Notification title
        message: Notification body
        icon: Optional path to icon file
    
    Returns:
        True if notification was sent successfully
    """
    try:
        if sys.platform == "win32":
            return _notify_windows(title, message, icon)
        elif sys.platform == "darwin":
            return _notify_macos(title, message)
        else:
            return _notify_linux(title, message, icon)
    except Exception as e:
        print(f"Notification failed: {e}")
        return False


def _notify_windows(title: str, message: str, icon: Optional[str] = None) -> bool:
    """Send notification on Windows"""
    
    # Try win10toast first (more feature-rich)
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(
            title,
            message,
            icon_path=icon,
            duration=5,
            threaded=True
        )
        return True
    except ImportError:
        pass
    
    # Fallback to PowerShell notification
    try:
        ps_script = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

        $template = @"
        <toast>
            <visual>
                <binding template="ToastText02">
                    <text id="1">{title}</text>
                    <text id="2">{message}</text>
                </binding>
            </visual>
        </toast>
"@

        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("ScheduledTask").Show($toast)
        '''
        
        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            timeout=10
        )
        return True
    except Exception:
        pass
    
    # Last resort: simple message box
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)  # MB_ICONINFORMATION
        return True
    except Exception:
        pass
    
    return False


def _notify_macos(title: str, message: str) -> bool:
    """Send notification on macOS using osascript"""
    script = f'''
    display notification "{message}" with title "{title}"
    '''
    
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        timeout=10
    )
    
    return result.returncode == 0


def _notify_linux(title: str, message: str, icon: Optional[str] = None) -> bool:
    """Send notification on Linux using notify-send"""
    
    cmd = ["notify-send", title, message]
    
    if icon:
        cmd.extend(["-i", icon])
    
    # Try notify-send (most common)
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    
    # Try zenity as fallback
    try:
        subprocess.run(
            ["zenity", "--notification", f"--text={title}: {message}"],
            capture_output=True,
            timeout=10
        )
        return True
    except FileNotFoundError:
        pass
    
    # Try kdialog for KDE
    try:
        subprocess.run(
            ["kdialog", "--passivepopup", message, "5", "--title", title],
            capture_output=True,
            timeout=10
        )
        return True
    except FileNotFoundError:
        pass
    
    return False


def test_notification():
    """Test the notification system"""
    print(f"Platform: {sys.platform}")
    print("Sending test notification...")
    
    success = send_notification(
        "Scheduled Task Test",
        "If you see this, notifications are working!"
    )
    
    if success:
        print("✅ Notification sent successfully")
    else:
        print("❌ Notification failed")
        print()
        print("Troubleshooting:")
        if sys.platform == "win32":
            print("  - Install win10toast: pip install win10toast")
        elif sys.platform == "darwin":
            print("  - osascript should be available by default")
        else:
            print("  - Install notify-send: sudo apt install libnotify-bin")
            print("  - Or install zenity: sudo apt install zenity")


if __name__ == "__main__":
    test_notification()
