#!/bin/bash
cd "$(dirname "$0")"

USERS=$(grep bash /etc/passwd|grep '/home'|grep '[1-2][0-9][0-9][0-9]'|awk -F':' '{print $1}')
SERVICE_NAME=piavpn.service
WORKING_DIR=/opt/openvpn-pia
LOGIN_CREDS_FILE=/opt/openvpn-pia/creds.conf

if [ ! -d /etc/openvpn ];then
	echo "ERROR: Openvpn dir missing..."
	exit
fi

echo "Home Config..."
if [ ! -f ~/.openvpn-pia.conf ];then
echo "

#switzerland.ovpn
#uk_manchester.ovpn
#netherlands.ovpn
#us_atlanta.ovpn
#us_chicago.ovpn
#us_east.ovpn
#us_houston.ovpn
#us_new_york.ovpn
#us_silicon_valley.ovpn
#us_washington_dc.ovpn
#us_california.ovpn
#us_denver.ovpn
#us_florida.ovpn
#us_las_vegas.ovpn
#us_seattle.ovpn
#us_texas.ovpn
#us_west.ovpn
run us_missouri-256.ovpn" > ~/.openvpn-pia.conf
chmod 600 ~/.openvpn-pia.conf
fi

cp Autostart/openvpn-pia.desktop ~/.config/autostart/
cp Desktop/openvpn-pia.desktop ~/Desktop/

