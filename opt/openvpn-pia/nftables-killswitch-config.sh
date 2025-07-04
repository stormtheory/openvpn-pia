#!/bin/bash
cd "$(dirname "$0")"

TABLE=killswitch
IN=input_switch
OUT=output_switch


##### BUILD TABLES ######
echo "# BUILD"
nft add table ip $TABLE

############################################
##            LISTS                        #
############################################

######## VPN INTERFACE LIST AND DENYLIST
nft add set ip $TABLE VPN_iifname { type ifname \; }
nft add element ip $TABLE VPN_iifname {wg0, wg1, tun0, tun1, moz0, moz1}
nft add set ip $TABLE VPN_DENYLIST { type ipv4_addr \; flags dynamic, timeout \; timeout 999m \; }


##########################################
##          END                          #
##########################################

#nft add chain ip my_table my_filter { type filter hook input priority 0 \; policy drop \; meta pkttype { broadcast,multicast } accept \;}
nft add chain ip $TABLE $OUT { type filter hook output priority 0 \; policy accept \;}

##############################
#### IPv6 Rules ##############
##############################
nft add table ip6 ${TABLE}_v6
nft add chain ip6 ${TABLE}_v6 my_v6_filter { type filter hook output priority 0 \; policy drop \; }
nft add rule ip6 ${TABLE}_v6 my_v6_filter iifname lo ip6 daddr ::1 accept comment \"Localhost6\"
nft add rule ip6 ${TABLE}_v6 my_v6_filter iifname lo accept comment \"Localhost6\"
nft add rule ip6 ${TABLE}_v6 my_v6_filter tcp dport 0-65535 drop comment \"Block IPv6 OUT\"
nft add rule ip6 ${TABLE}_v6 my_v6_filter udp dport 0-65535 drop comment \"Block IPv6 OUT\"

## Log v6 drops
#nft add rule ip6 my_v6_table my_v6_filter counter log prefix \"[nftables]-dropfilter6\" drop

##############################
#### IPv4 Rules ##############
##############################

              ####################
################     OUTPUT      #
              ####################

nft add rule ip $TABLE $OUT oifname lo accept comment \"Localhost\"

### SSH
echo "# SSH"
#nft add rule ip $TABLE $OUT ip daddr <ip> tcp dport 22 accept comment \"SSH List Allow\"
#nft add rule ip $TABLE $OUT ip daddr <ip> tcp dport 22 accept comment \"SSH List Allow\"
nft add rule ip $TABLE $OUT tcp dport 22 log prefix \"[nftables]-ssh-dropfilter\" drop comment \"SSH DROP\"

# Allow VPN traffic out (UDP to VPN server) #####################
#ip daddr <YOUR_VPN_SERVER_IP> udp dport <PORT> accept

# Allow traffic via VPN interface
nft add rule ip $TABLE $OUT oifname "tun0" accept

# Log and drop everything else
nft add rule ip $TABLE $OUT counter drop
