# Secure Password Manager

This app is created in Python using Tkinter for GUI interface and it allows users to securely store their passwords. 

# Usage
Either run the project using python or via docker containers. 

## Python
```
python main.py
```

## Docker
```
docker build -t securepasswordmanager .
```
```
xhost +local:docker
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -p 4000:80 securepasswordmanager
```
