import subprocess
import sys

def run_script(script_path):
    print(f"\nRunning {script_path}...")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        print(f"Error running {script_path}. Return code: {result.returncode}")
    else:
        print(f"{script_path} ran successfully.")

def main():
    # Run the serial version script
    run_script("src/serial_version.py")
    
    # Run the basic parallel version (benchmark and simple plot)
    run_script("src/parallel_version.py")
    
    # Run the version with subplots (performance analysis with two subplots)
    run_script("src/parallel_version_with_subplots.py")
    
    print("\nAll scripts have been executed.")

if __name__ == "__main__":
    main()
