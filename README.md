Ionuț Găină - 341C5

# Tema 3 - Platformă IoT folosind Microservicii

## Descriere

În cadrul acestei teme am realizat o platformă IoT folosind microservicii. Platforma este compusă din următoarele microservicii:

- **MQTT Broker** - serviciu care se ocupă de transmiterea mesajelor de la senzorii dispozitivelor IoT către adaptor

- **Adaptor** - serviciu care se ocupă de preluarea mesajelor de la MQTT Broker și de transmiterea acestora către baza de date

- **Baza de date** - TSDB influxDB care salvează datele trimise de adaptor

- **Grafana** - serviciu care se ocupă de vizualizarea datelor din baza de date

### Adaptor

Adaptorul este un serviciu scris în Python care se ocupă de preluarea mesajelor de la MQTT Broker și de transmiterea acestora către baza de date. El este abonat la toate topicurile de pe MQTT Broker și atunci când primește un mesaj, îl parsează și îl trimite către baza de date.

### Baza de date

Baza de date este un serviciu de tip Time Series Database (TSDB) care salvează datele trimise de adaptor.
Datele sunt persistente

### Grafana

Pentru a vizualiza datele din baza de date, am folosit Grafana. Credențialele pentru Grafana sunt `asistent` și `grafanaSCD2024`, fiind disponibil pe [http://localhost](http://localhost). Dashboard-urile create sunt `UPB IoT Data` și `Battery Dashboard`.

Datele sunt persistente.

### MQTT Broker

MQTT Broker este un serviciu care se ocupă de transmiterea mesajelor de la senzorii dispozitivelor IoT către adaptor. Acesta este accesibil pe portul `1883` și nu necesită autentificare.

## Utilizare

Pentru a rula platforma, se rulează comanda `./run.sh` în directorul curent, dacă nu are drepturi de execuție, se ruleaza `bash run.sh`.