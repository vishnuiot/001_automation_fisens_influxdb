import subprocess
import sys
import time

# This script will forcefully clear COM4
# Run this FIRST before starting the main logger

print("🔧 Clearing COM4 port locks...")
print("=" * 60)

# Method 1: Kill any Python processes using COM ports
try:
    result = subprocess.run(
        ["taskkill", "/F", "/IM", "python.exe"],
        capture_output=True,
        text=True
    )
    print("✓ Killed Python processes")
except:
    print("⚠ Could not kill Python processes (may not be needed)")

time.sleep(2)

# Method 2: Disable and re-enable the COM port in Device Manager
try:
    # This uses Windows Registry to reset COM ports
    subprocess.run([
        "powershell",
        "-Command",
        "Get-PnpDevice -FriendlyName '*COM4*' | Disable-PnpDevice -Confirm:$false; Start-Sleep -Seconds 2; Get-PnpDevice -FriendlyName '*COM4*' | Enable-PnpDevice -Confirm:$false"
    ], capture_output=True)
    print("✓ Reset COM4 device in Device Manager")
except Exception as e:
    print(f"⚠ Could not reset COM4: {e}")

time.sleep(3)

print("=" * 60)
print("✅ COM4 should now be free!")
print("\nNow run: python Fiber_optic_sensing_60sec.py")
