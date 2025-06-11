"""
Build script for creating a Windows executable of the Zalo Automation Tool
"""
import os
import shutil
import subprocess
import platform
import sys

def build_windows_app():
    """Build the Windows executable using PyInstaller"""
    print("Starting Windows build process...")
    
    # Check if we're on Windows
    if platform.system() != "Windows":
        print("WARNING: You are not building on Windows. Cross-compilation may have issues.")
        print("For best results, run this script on a Windows machine.")
        input("Press Enter to continue anyway or Ctrl+C to cancel...")
    
    # Clean previous build
    print("Cleaning previous builds...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Run PyInstaller
    print("Running PyInstaller...")
    try:
        subprocess.run(["pyinstaller", "zalo_app.spec"], check=True)
        print("PyInstaller completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error running PyInstaller: {e}")
        return False
    
    # Create distribution zip file
    print("Creating distribution ZIP file...")
    try:
        # Copy additional files to the dist directory
        shutil.copy("run_zalo_app.bat", "dist")
        shutil.copy("README_WINDOWS.md", "dist/README.md")
        
        # Create a zip file
        shutil.make_archive("zalo_automation_tool_windows", "zip", "dist")
        print(f"ZIP file created: {os.path.abspath('zalo_automation_tool_windows.zip')}")
    except Exception as e:
        print(f"Error creating distribution: {e}")
        return False
    
    print("\nBuild completed successfully!")
    print("\nTo distribute to Windows users:")
    print("1. Share the 'zalo_automation_tool_windows.zip' file")
    print("2. Users should extract the ZIP and run 'run_zalo_app.bat'")
    
    return True

if __name__ == "__main__":
    build_windows_app()
