import atexit
import os
import signal
import subprocess
import time

import requests
from kubernetes import client, config


def check():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    
    # Use kubectl port-forward to test connectivity
    local_port = 8080
    process = None
    
    try:
        # Start port-forward in background
        cmd = f"kubectl port-forward service/nginx-service {local_port}:80"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Register cleanup function
        def cleanup():
            if process:
                os.kill(process.pid, signal.SIGTERM)
        atexit.register(cleanup)
        
        # Give port-forward time to establish
        time.sleep(2)
        
        # Check if nginx is accessible
        try:
            response = requests.get(f"http://localhost:{local_port}", timeout=5)
            if response.status_code == 200 and "nginx" in response.text.lower():
                print("✅ Service is correctly exposing nginx on port 80.")
                return True
            else:
                print(f"❌ Got response code {response.status_code}, but nginx not detected.")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed. nginx is not accessible on port 80.")
            return False
            
    except Exception as e:
        print(f"❌ Error testing connectivity: {e}")
        return False
    finally:
        if process:
            process.terminate()
            atexit.unregister(cleanup)
