# pi-printy

Pi-printy is a super simple printing web server running on a Raspberry Pi (any linux-based pc). The web server allows you to upload PDF files, which will be further printed by CUPSS library.

The setup is quite straightforward. Can be also extended to handle multiple options like double-sided printing or color printing. However, this very much depends on your printer and also the support in CUPSS.

To make the UI funny, the whole website is frog-themed. 🐸

The project has been tested on Raspberry Pi 5 and Xerox WorkCentre 3025BI printer (for which the CUPSS support is very limited..., hopefully you are luckier :)).

![alt text](images/img.png "Website screenshot")

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/jskvrna/pi-printy.git
    cd pi-printy
    ```
2. **Install CUPS**
    ```bash
    sudo apt-get install cups
    ```
3. **Add your user to the lpadmin group**
    ```bash
    sudo usermod -a -G lpadmin USERNAME
    ```
4. **Restart CUPS**
    ```bash
    sudo systemctl restart cups
    ```
5. **Configure CUPS**
    ```visit
    http://[Your Pi's IP Address]:631
    ```
    - Click on "Administration" > "Add Printer".
    - Select your printer from the list.
    - Provide the necessary details and driver (use a generic driver if specific one isn't available).
    - Set default options as needed.
    - If there is no available, try a generic one and try the test print option
6. **Install python**
    ```bash
    sudo apt-get install python3-pip
    ```
7. **Install the flask for python**
    ```bash
    pip3 install flask
    ```
8. **Test run your server and access it**
    ```bash
    python3 app.py
    ```
    - Open your browser and visit `http://[Your Pi's IP Address]:5000`
    - You should see the website
    - If the website is working close the python script by pressing `Ctrl+C`
9. **Now let's set up the server to run on boot**
    ```bash
    sudo nano /etc/systemd/system/printer_server.service
    ```
    - Copy the following content
    ```bash
    Description=Flask Printer Server
    After=network.target
    
    [Service]
    User=pi
    WorkingDirectory=/home/USERNAME/pi-printy
    ExecStart=/usr/bin/python3 app.py
    
    [Install]
    WantedBy=multi-user.target
    ```
    - Save the file and exit
    - Enable the service
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable printer_server.service
    sudo systemctl start printer_server.service
    ```
10. **You are done!**
    - You can now access the website on `http://[Your Pi's IP Address]:5000`
    - You can upload PDF files and print them
    - The server will run on boot and is only accessible on your local network
    - To print from outside of the network I suggest using VPN ([pi-vpn](https://github.com/pivpn/pivpn) is a great project for that)
    - The port settings can be changed in the `app.py` file
    - You can easily replace the images to make it into another theme

Feel free to use this code, modify it, or share it. If you have any questions or suggestions, feel free to contact me.

This code was generated with the assistance of OpenAI's GPT-4 model.

[Dancing frog gif](https://tenor.com/view/frog-dancing-dance-moves-wiggle-gif-16326811)
