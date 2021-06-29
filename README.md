# Rennervate

A drowsiness detection model in the making

## TO DO

### 1. Clone repo

```sh
$ git clone https://github.com/kcaashish/Rennervate.git
$ cd Rennervate
```

### 2. Using virtual environment ".venv" (or choose your name)

- For Linux:
  ```sh
  $ python -m venv .venv
  $ source .venv/bin/activate
  ```
- For Windows:
  Go to the folder, then open Git Bash, then:
  ```sh
  $ python -m venv .venv
  $ source .venv\Scripts\activate.bat
  ```

### 3. Installing requirements in .venv

```sh
$ pip install -r requirements.txt
```
You should try installing each requirements separately if you are getting errors using the above method.

- For Linux:
  - Install Cmake into your system
    ```sh
    Arch / Manjaro
    $ sudo pacman -S cmake
    ```
    ```sh
    Debian / Ubuntu
    $ sudo apt install cmake
    ```
    
  - Then, in the virtual environment:
    ```sh
    $ pip install cmake
    $ pip install opencv-python==4.2.0.34
    $ pip install dlib
    ```
- For Windows:
  - You can follow the link below for installing Cmake and dlib required for the project:
    [Installation helper](https://medium.com/analytics-vidhya/how-to-install-dlib-library-for-python-in-windows-10-57348ba1117f)
  - Use the link below to download Cmake if the link mentioned in the guide doesn't work: [download Cmake from here](https://www.softpedia.com/get/Programming/Coding-languages-Compilers/CMake.shtml)
  - For openCV:
    ```sh
    $ pip install opencv-python
    ```
    
### 4. Open project with VS Code

```sh
$ code .
```

If you need to download the shape predictor file, to get it from dlib go to the following [link](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) and extract the shape_predictor_68_landmark.dat file to the project folder. Or you can download it directly [here](https://github.com/JeffTrain/selfie/raw/master/shape_predictor_68_face_landmarks.dat).
