# HOW TO USE
## Thony setup
- Open `thony` then click on `Run > Configure Interpreter` set all options for `Raspberry Pi Pico WH` select the version `1.XX.X`. (You will see the pico in the files window)
- Install drivers for `ssd1306` module. Go to `Tools > Manage Packages` then search for `ssd1306` and click install. (This should create a lib folder with the drivers in the root dir of pico)
- Save the `main.py` file from this directory into the root of the pico.
- Now save and run the script

---
## No oled
If you dont have an oled display then use the  `no_display.py` file in this directory and save it as `main.py` in the pico's root dir.

---
If you get any run problems, open up a new Issue in this repo.
