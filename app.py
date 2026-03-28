import os
import subprocess
import os

# Ensure facefusion can be imported if it's in a subdirectory
import sys
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, 'facefusion_app'))

# Run the app via CLI interface as that's most reliable for Facefusion
if __name__ == '__main__':
    # Start the facefusion web server directly
    # We pass 'run' argument as expected by Facefusion CLI
    print("Launching Fernando IA on Hugging Face Spaces...")
    
    # HF Spaces expects apps to listen on port 7860
    # Facefusion usually allows setting port via args or default
    os.chdir('facefusion_app')
    os.system("python facefusion.py run --ui-layouts default")
