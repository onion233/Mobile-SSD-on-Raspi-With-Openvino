# Setting Up Static IP and Hostname
First make sure raspberry pi and host PC are connected with ethernet cable.

## On Raspberry Pi
```sh
sudo vim /etc/dhcpcd.conf
```

Add the following lines at the end of the file：
```sh
interface eth0
static ip_address=192.168.1.6/24
static router=192.168.1.1
```

Reboot to take effect
```sh
sudo reboot
```

## On PC
Similar setting process with raspberry pi but in GUI. Open Setting-Network-Wired-IPv4 Setting-Address:

* Address: 192.168.1.5
* Netmask: 255.255.255.0 (ie:24)
* Gateway(Router): 192.168.1.1
  
## Adding Hostname Alongwith Ip:
On both raspberry pi and host PC, do；
```sh
sudo vim /etc/hosts
```
Check your computer host name；
```sh
$ ~ hostname
ubuntu
```
Add these two lines；
```sh
192.168.1.5   ubuntu
192.168.1.6   raspberrypi
```

## Verify the Static Ip Address

On one machine, ping or ssh to another machine by:
```sh
ssh pi@raspberrypi
```
or 
```sh
$ ping raspberrypi
PING raspberrypi (192.168.1.6) 56(84) bytes of data.
64 bytes from raspberrypi (192.168.1.6): icmp_seq=1 ttl=64 time=0.951 ms
64 bytes from raspberrypi (192.168.1.6): icmp_seq=2 ttl=64 time=0.446 ms
```

# Setting Up ROS Master
In host--my ubuntu pc, 
```sh
$ vim ~/.bashrc
```
Configure the ROS address as:
```sh
export ROS_HOSTNAME=ubuntu
export ROS_MASTER_URI=http://ubuntu:11311
export ROS_IP=192.168.1.5
```
In raspberry pi:
```sh
$ vim ~/.bashrc
```
Configure the ROS address as:
```sh
export ROS_HOSTNAME=raspberrypi
export ROS_MASTER_URI=http://ubuntu:11311
export ROS_IP=192.168.1.6
```
# Run Your Service
In this section, we test our communication using turtlesim.
```sh
$ sudo apt install ros-kinetic-turtlesim
```
On PC, run
```sh
$ roscore
$ rosrun turtlesim turtlesim_node
```
On raspberry pi, run
```sh
rosrun turtlesim turtle_teleop_key
```
And you can control the turtle running on host PC by typeing command on raspberry pi