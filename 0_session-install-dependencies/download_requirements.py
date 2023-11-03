import subprocess

print(subprocess.run(["sh 0_session-install-dependencies/download_requirements.sh"], shell=True))