The main branch contains the program code and when the contents of the models.zip file is included into the /models/translation folder program will run. In the branch audio2text the speech-to-text code is available for viewing.


If The model can not open the audio file for transcription with Whisper AI the package ffmpeg is likely installed wrong go to https://github.com/openai/whisper or look below on how to install it on the operating system you are running.
```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg
 
# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```
