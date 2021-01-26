# nutc-smart-bathroom

## 安裝步驟

```  
git clone https://github.com/kanic1111/nutc-smart-bathroom.git
```
### 設定config.ini
```
cp config.ini.sample config.ini

nano config.ini
```
config.ini內容

```
[GCP]
SERVER_PROTOCOL = http
SERVER_IP = 127.0.0.1
SERVER_PORT = 30001

[CLOUD_DEVICE]
MAC = 012345678900

[LOCAL_DEVICE]
SERIAL = /dev/ttyACM0
IP = 127.0.0.1    
MAC = 012345678900

[PIR231_DEVICE]
IP = 127.0.0.1 ;PIR231 IP
MAC = 012345678900
```
### 安裝套件

```
bash install.sh
```
