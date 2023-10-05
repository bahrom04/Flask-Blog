#!/usr/bin/env python3

from webapp import app


if __name__ == '__main__':
    print('''
    ____        _                         
    | __ )  __ _| |__  _ __ ___  _ __ ___  
    |  _ \ / _` | '_ \| '__/ _ \| '_ ` _ \ 
    | |_) | (_| | | | | | | (_) | | | | | |
    |____/ \__,_|_| |_|_|  \___/|_| |_| |_|

        Copyright 2023
    ''')

    app.run(debug=True)