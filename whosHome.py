#!/usr/bin/python

##############################
######   Server Script  ######
##############################

import bottle
import re
import sqlite3
from datetime import datetime
import subprocess

"""
Script for the Webserver which creates the Index.html with the data from the database
"""

app = application = bottle.Bottle()
bottle.SimpleTemplate.defaults["get_url"] = app.get_url


# Responsible for the CSS files


@app.route('/static/<filename:path>', name='static')
def send_static(filename):
    return bottle.static_file(filename, root='./static/')

# Host the Index.html at the root of your server


@app.route('/', name='index')
def index():

    con = sqlite3.connect('Client.db')
    cur = con.cursor()

    clientOnline = len(cur.execute(
        'SELECT * FROM client WHERE online = "Yes"').fetchall())
    allClient = cur.execute('SELECT * FROM client').fetchall()

    try:
        ssid = subprocess.Popen(
            ["sudo", "iwgetid", "-r"], stdout=subprocess.PIPE).communicate()[0].rstrip()
        return bottle.template('index.tpl', ssid=ssid, clientOnline=clientOnline, allClient=allClient, lastReload=datetime.now().strftime("%I:%M %p - %d.%m.%Y"))
    except ValueError:
        return bottle.template('<p>Please reload the page!</p>')

    con.close()

if __name__ == '__main__':
    # Host the Webserver on the local private IP the Raspberry got
    # (e.g. 192.168.0.100:8080)
    bottle.run(app=app, host='0.0.0.0', port=8080, reloader='True')
