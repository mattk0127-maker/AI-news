import time
import subprocess
from datetime import datetime
import os
import sys

def run_orchestrator():
    """Executes the orchestrator script and logs the result."""
    script_path = os.path.join(os.path.dirname(__file__), 'orchestrator.py')
    print(f"\n--- [Trigger] Executing Scraper Pipeline at {datetime.now()} ---")
    
    try:
        # Run orchestrator
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, check=True)
        print("Scraper completed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("ERROR during scraper execution:")
        print(e.stderr)

def start_loop():
    """Runs the orchestrator every 24 hours."""
    # 24 hours in seconds
    INTERVAL = 24 * 60 * 60
    
    # Target article count recorded in findings
    print("Welcome to B.L.A.S.T. Dashboard Trigger")
    print("Targeted articles set to: 20 minimum going forward (Excluding Ben's Bytes)")
    print(f"Polling interval set to: {INTERVAL} seconds (24 Hours)")
    print("Starting initial scrape...")
    
    while True:
        run_orchestrator()
        
        print(f"Sleeping for 24 hours... Next run at approximately {datetime.fromtimestamp(time.time() + INTERVAL)}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    start_loop()
