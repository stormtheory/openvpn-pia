#!/bin/bash
cd "$(dirname "$0")"

USER_LIST=$(grep bash /etc/passwd|grep '/home'|grep '[1-2][0-9][0-9][0-9]'|awk -F':' '{print $1}')
SERVICE_NAME=piavpn.service
WORKING_DIR=/opt/openvpn-pia
LOGIN_CREDS_FILE=/etc/openvpn/creds

ID=$(id -u)
if [ "$ID" != 0 ];then
	echo "Must be root..."
	exit 1
fi

if [ ! -d /etc/openvpn ];then
	echo "ERROR: Openvpn dir missing..."
	exit 1
fi

PWD=$(pwd)
if [ "$PWD" != /opt/openvpn-pia/SETUP ];then
	echo "Doing Self Install..."
	if echo "$PWD"|grep -q '/opt/openvpn-pia/SETUP';then
		cp -r ../../openvpn-pia/ /opt/
	else
		echo "ERROR: Copying Files"
	fi
else
	echo "Doing DEB Install..."
fi

#### Update configs/locations
if [ -f /etc/openvpn/creds.conf ];then
	mv /etc/openvpn/creds.conf $LOGIN_CREDS_FILE
	chmod 600 $LOGIN_CREDS_FILE
	chown root:root $LOGIN_CREDS_FILE
fi

#### Disable and stop openvpn service
if systemctl is-enabled openvpn.service |grep -q 'enabled';then
	systemctl disable openvpn.service
	if systemctl is-active openvpn.service |grep -q 'active';then
        	systemctl stop openvpn.service
	fi
fi

#### Check for Login file and if not there make a template
if [ ! -f "$LOGIN_CREDS_FILE" ];then
	# YOUR_USERNAME
	# YOUR_PASSWORD
	touch $LOGIN_CREDS_FILE
	chmod 600 $LOGIN_CREDS_FILE
	echo 'YOUR_USERNAME
YOUR_PASSWORD' > $LOGIN_CREDS_FILE

fi


function SERVICE {

echo "Deploying $SERVICE_NAME"
if [ ! -f /etc/systemd/system/$SERVICE_NAME ];then
echo "[Unit]
Description=--PIA OpenVPN Service--
StartLimitIntervalSec=5
StartLimitBurst=5

[Service]
Type=fork
WorkingDirectory=$WORKING_DIR/
ExecStart=$WORKING_DIR/service.sh
ExecReload=$WORKING_DIR/service.sh restart
ExecStop=$WORKING_DIR/service.sh stop
Restart=always
RestartSec=4
RemainAfterExit=no

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/$SERVICE_NAME
        chmod 644 /etc/systemd/system/$SERVICE_NAME
        systemctl daemon-reload
        sleep 2
        #systemctl disable $SERVICE_NAME
	#systemctl enable $SERVICE_NAME
        #timeout 6 systemctl restart $SERVICE_NAME
	fi
}

SERVICE

function OWNERSHIP {

chown root:root -R /opt/openvpn-pia
chown root:root /etc/systemd/system/piavpn.service

}
OWNERSHIP

function SUDO {
echo "Sudoers..."
while IFS= read -r line;do
		echo "$line"


if [ -d /etc/sudoers.d ];then
	FILE=/etc/sudoers.d/openvpn-pia
	if [ -f $FILE ];then
		chmod 640 $FILE
	fi
else
	FILE=/etc/sudoers
fi

if grep "$line ALL=(ALL) NOPASSWD:/usr/bin/systemctl restart piavpn.service" $FILE;then
	echo 'good'
else
	echo "$line ALL=(ALL) NOPASSWD:/usr/bin/systemctl restart piavpn.service" >> $FILE
fi
if grep "$line ALL=(ALL) NOPASSWD:/usr/bin/systemctl stop piavpn.service" $FILE;then
        echo 'good'
else
        echo "$line ALL=(ALL) NOPASSWD:/usr/bin/systemctl stop piavpn.service" >> $FILE
fi		
                done <<< "$USER_LIST"

if [ -d /etc/sudoers.d ];then
        chmod 440 $FILE
fi

}
SUDO

function HOME_CONFIG {

echo "Home Config..."
USER_LIST=$(echo "$USER_LIST
root")
while IFS= read -r quser;do
                echo "$quser"
if [ "$quser" != root ];then
	HOME=/home
else
	HOME=
fi

if [ ! -f $HOME/$quser/.openvpn-pia.conf ];then
echo "
#switzerland.ovpn
#uk_manchester.ovpn
#de_berlin.ovpn
#ireland.ovpn
#costa_rica.ovpn
#nl_amsterdam.ovpn
#us_atlanta.ovpn
#us_chicago.ovpn
#us_east.ovpn
#us_washington_dc.ovpn
#us_florida.ovpn
#us_west.ovpn
#us_missouri.ovpn

run us_missouri.ovpn

killswitch true" > $HOME/$quser/.openvpn-pia.conf
chmod 600 $HOME/$quser/.openvpn-pia.conf
chown $quser:$quser $HOME/$quser/.openvpn-pia.conf
fi

if [ "$quser" != root ];then
	if [ ! -f /home/$quser/.config/autostart/openvpn-pia.desktop ];then 
		cp Autostart/openvpn-pia.desktop /home/$quser/.config/autostart/
	fi
cp Desktop/openvpn-pia.desktop /home/$quser/Desktop/
chown $quser:$quser /home/$quser/Desktop/openvpn-pia.desktop
chown $quser:$quser /home/$quser/.config/autostart/openvpn-pia.desktop
fi

done <<< "$USER_LIST"
}

HOME_CONFIG



# auth-user-pass /etc/openvpn/creds
# auth-nocache


# /etc/openvpn/creds.conf
# YOUR_USERNAME
# YOUR_PASSWORD

# curl ipinfo.io/ip
