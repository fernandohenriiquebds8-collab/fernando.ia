import os
import sys
import subprocess

# Set up paths
project_root = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(project_root, 'facefusion_app')

# Force Python to see the facefusion_app directory
sys.path.append(app_dir)

if __name__ == '__main__':
    print("🚀 Iniciando Fernando IA: FaceFusion no Hugging Face...")
    
    # We run the command from the app directory to ensure layouts are found
    # HF Spaces requires 0.0.0.0 and port 7860
    cmd = [
        sys.executable,
        os.path.join(app_dir, 'facefusion.py'),
        'run',
        '--ui-layouts', 'default',
        '--server-name', '0.0.0.0',
        '--server-port', '7860'
    ]
    
    # Execute facefusion
    subprocess.run(cmd, cwd=app_dir)
