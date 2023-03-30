
![cookie-clicker.png](cookie-clicker.png)
# Cookie Clicker Bot


## Description
This program is a Python script that automates the process of clicking in the game
"Cookie Clicker" using the Selenium library. It also automates the process of buying upgrades,
products, and clicking on golden cookies. It creates a separate thread for each of these
tasks, and the threads can be toggled on or off by the user through command-line input.
When the program start, all the functions will be Deactivated, you can Activate typing the 
letter under parentheses:

````
    Activate/Deactivate functions:

('c') cookie_click         = Deactivated
('g') get_golden_cookie    = Deactivated
('u') get_upgrade          = Deactivated
('p') get_products         = Deactivated
('q') QUIT

=>
````

## Requirements
+ [Python 3.7](https://www.python.org/downloads/) or latest
+ Selenium Library  

    ```
    pip install selenium
    ```

+ Your Browser [Web driver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)
+ Add the path of the web driver in the environment variable: "DRIVER_PATH"



