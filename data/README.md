# README

# ScienceHack 2021 Dataset

Each trip contains 4 separate files. Each trip contains multiple stops. The number of counted passengers always contains the bus driver and the person counting.
* gps_log: contains GPS-Data
* passenger_count_nums: contains ground truth public transport system and passenger count for referring timestamps
* wifi_data.csv: contains the recorded 802.11 WiFi-Probe Request frames while trip was running
* probemon.pcap

## Data Description:
* File "passenger_count_nums":  
    * epoch timestamp to each recorded entry
    * -10 means "Doors are closed at this timestamp"
    * -99 means "Doors are opened at this timestamp"
    * A positive integer number after an epoch timestamp corresponds to the counted number of passengers on board (including bus driver and person counting)
      
Any number between -10 and -99 represents the number of counted passengers in this period (or stop / subtrip). This period should be considered as the "interesting" timespan to help matching and filtering with other data.
  

* File "gps_data.csv":
  * date_time: parsed datetime as YYYY-MM-DD hh:mm:ss
  * is_valid: if received GPS-data log record is valid
  * latitude: latitudinal geolocation
  * lat_dir: latitudinal direction, e.g. "N" for north 
  * longitude: longitudinal geolocation
  * lon_dir: longitudinal direction, e.g. "E" for east 
  * speed_over_ground_knots: speed over ground in unit "knots"
  * heading_true_course: heading in unit "degrees"
  * epoch_ts: parsed datetime as epoch timestamp


* File "wifi_data.csv":
  * id: autoincremental integer
  * arr_ts: arrival time of the beacon (in CEST, means UTC+2)
  * epoch_ts: arrival time of the beacon as epoch timestamp  
  * vendor: information from manufacturer, if available
  * frame_nr: number of the received and decodable frame
  * subtype: stands for probe request frame, constantly 4
  * mac_address: received MAC-adress from mobile device (tricky part, since it can be randomized or not. There can also be the first 3 bytes non randomized but the rest are randomized. Different options have to be considered)
  * rssi: dBm-antenna signal of sending devices
  * seq_num: sequence number, increments on each device until certain threshold, then resets to 0/1 and continues incrementation, [0...4095]
  * ht_capabilities: HT capabilities information
  * ht_ampdu: A-MPDU Parameters
  * tag_nr: Tag number
  * tag_length: Tag length
  * tag_mcs: Rx Supported Modulation and Coding Scheme Set
  * tag_HTex: HT Extended Capabilities
  * tag_TXbf: Transmit Beam Forming (TxBF) Capabilities
  * tag_Antsel: Antenna Selection (ASEL) Capabilities  
  

* File "probemon.pcap":
  * This is a raw packet capture file (subtype set to "probe requests"), containing additional probe requests (as well as the records in the wifi_data.csv) which could not have been parsed to the processed "wifi_data.csv"-file. Dissecting this and extraction to e.g. .JSON-Format could contain additional information. Nevertheless, complexity increases here. Working with the "wifi_data.csv"-File is highly recommended, since essential information is already included in this file.

  
### Further information
+ **The MAC-Address "b8:27:eb:6b:c4:60" belongs to a raspberrypi and can be ignored/filtered out of the dataset**
+ MAC-Addresses could contain OUI (Organizationally Unique Identifier). These can be mapped by a lookup: https://www.wireshark.org/tools/oui-lookup.html
+ Randomization can sometimes be detected, if it is truly randomized: https://www.mist.com/get-to-know-mac-address-randomization-in-2020/

