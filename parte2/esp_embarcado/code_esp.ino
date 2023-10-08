// bibliotecas do sensor
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <Arduino.h>

#include <Adafruit_Sensor.h>
#include <WebSocketsClient_Generic.h>
#include <WebSocketsServer_Generic.h>
#include <stdlib.h>

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#include "proto_mensagens.pb.h"
#include "pb_common.h"
#include "pb_decode.h"
#include "pb_encode.h"
char *strTemp;

const char *ssid = "brisa-2664316";
const char *password = "kum0hxa8";
// const char* ssid = "JM";
// const char* password = "testedoprojeto2";

// Porta que a ESP8266 ficará escutando
const IPAddress multicast_ip(224, 1, 1, 1);
unsigned int multi_port = 54321;
//unsigned int port_udp = 12345;
unsigned int device_port = 8078;
unsigned int gateway_port;
IPAddress ip_esp;
int packetSize;
bool envia = false;

// Crie uma instância do objeto UDP
WiFiUDP udp;

float temperature;  //variável para armazenar a temperatura
float humidity;     //Variável para armazenar a umidade
char buffer_sensor[101];
String sensor_tu = "";

#define DHT_PIN D2      // Pino onde o DHT22 está conectado (por exemplo, D2).
#define DHT_TYPE DHT22  // Tipo de sensor DHT que você está usando (DHT11, DHT21, ou DHT22).

DHT dht(DHT_PIN, DHT_TYPE);

unsigned long tempo_ex;
WiFiUDP server_socket_send;
WiFiUDP server_socket_receve;

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Definições de wifi (evitar que desligue)
  WiFi.setOutputPower(0);
  WiFi.begin(ssid, password);

  //tentando se conectar à rede
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado ao WiFi");

  //Identificando o IP da esp
  ip_esp = WiFi.localIP();
  Serial.printf("IP da Esp: ");
  Serial.println(ip_esp);
  // Inicialize o objeto UDP
  delay(1000);

  //iniciando o multicast
  udp.beginMulticast(WiFi.localIP(), multicast_ip, multi_port);
  delay(1000);

  Serial.printf("Pronto para receber uma mensagem no grupo IP: %s | Porta: %d \n", multicast_ip.toString().c_str(), multi_port);
}

void loop() {
  packetSize = udp.parsePacket();
  if (packetSize) {
    u_int8_t buffer[packetSize];
    udp.read(buffer, packetSize);
    IPAddress ip_gateway = udp.remoteIP();
    int porta_gateway = udp.remotePort();
    Discovery mensagemDescoberta = Discovery_init_zero;
    pb_istream_t streamDescoberta = pb_istream_from_buffer(buffer, packetSize);
    if (pb_decode(&streamDescoberta, Discovery_fields, &mensagemDescoberta)) {
      // A mensagem foi desserializada com sucesso
      Serial.println("Mensagem Protobuf recebida com sucesso: ");
      Serial.println(mensagemDescoberta.message);
      int result = strcmp(mensagemDescoberta.message, "Descoberta de dispositivos: Quem está aí?");
      if (result == 0) {

        Identification mensagemIdentificacao = Identification_init_zero;
        strcpy(mensagemIdentificacao.device_type, "Sensor de temperatura e umidade");
        strcpy(mensagemIdentificacao.device_ip, ip_esp.toString().c_str());
        mensagemIdentificacao.device_port = device_port;
        strcpy(mensagemIdentificacao.protocol, "UDP");

        u_int8_t buffer2[128];
        pb_ostream_t stremIdentificacao = pb_ostream_from_buffer(buffer2, 128);
        if (pb_encode(&stremIdentificacao, Identification_fields, &mensagemIdentificacao)) {
          server_socket_send.beginPacket(udp.remoteIP(), udp.remotePort());
          server_socket_send.write(buffer2, stremIdentificacao.bytes_written);
          server_socket_send.endPacket();

          Serial.println("Mensagem de resposta enviada com sucesso!");

          server_socket_receve.begin(device_port);
          int sizepk = 0;
          while (sizepk == 0) {
            sizepk = server_socket_receve.parsePacket();
          }
          u_int8_t buffer3[sizepk];
          server_socket_receve.read(buffer3, sizeof(buffer3));
          GatewayPort mensagemPorta;
          pb_istream_t streamGatewayPort = pb_istream_from_buffer(buffer3, sizepk);

          if (pb_decode(&streamGatewayPort, GatewayPort_fields, &mensagemPorta)) {
            gateway_port = mensagemPorta.gateway_port;
            Serial.println(gateway_port);
            Serial.print("Conectado ao gateway com sucesso :)");
            sizepk = 0;

            DeviceToGatewayMessage mensagemDevtoGet = DeviceToGatewayMessage_init_zero;
            while (1) {
              server_socket_receve.begin(device_port);
              sizepk = 0;
              while (sizepk == 0) {
                sizepk = server_socket_receve.parsePacket();
              }
              u_int8_t buffer4[sizepk];
              server_socket_receve.read(buffer4, sizeof(buffer4));
              GatewayToDeviceMessage mensagemGattoDev;
              pb_istream_t StreammensagemGattoDev = pb_istream_from_buffer(buffer4, sizepk);
              if (pb_decode(&StreammensagemGattoDev, GatewayToDeviceMessage_fields, &mensagemGattoDev)) {
                result = strcmp(mensagemGattoDev.command, "Iniciar");
                Serial.println(mensagemGattoDev.command);
                Serial.println("Comparação:");
                Serial.println(result);
                if (result == 0) {
                  envia = true;
                  envia_umidade(mensagemDevtoGet, server_socket_send);
                } else {
                  envia = false;
                }
              }
            }
          } else {
            Serial.println("Não foi possível decodificar a mensagem");
          }

        }
      } else {
        Serial.println("Erro ao desencodificar a mensagem Protocolbuf");
      }
    }
  }
}


void ler_sensor() {
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Erro ao ler o sensor DHT!");
    sensor_tu += "Erro de leitura do sensor";
  } else {
    sprintf(buffer_sensor, "Umidade: %.2f | Temperatura: %.2f", humidity, temperature);
    sensor_tu += buffer_sensor;
  }
}

void envia_umidade(DeviceToGatewayMessage mensagem, WiFiUDP server_socket_send) {
  while (envia) {
    ler_sensor();
    Identification mensagemIdentificacao = Identification_init_zero;
    strcpy(mensagem.response, buffer_sensor);
    u_int8_t buffer5[64];
    pb_ostream_t stremComunic = pb_ostream_from_buffer(buffer5, 64);
    if (pb_encode(&stremComunic, DeviceToGatewayMessage_fields, &mensagem)) {
      server_socket_send.beginPacket(udp.remoteIP(), gateway_port);
      server_socket_send.write(buffer5, stremComunic.bytes_written);
      server_socket_send.endPacket();
      Serial.println("Temperatura e umidade enviadas com sucesso");
    }
    verifica_parada();
    //delay(1000);
  }
}

void verifica_parada() {
  tempo_ex = millis();
  WiFiUDP server_socket_receve2;
  //server_socket_receve2.begin(8078);
  u_int8_t buffer6[128];
  int sizepk2;
  envia = true;
  while(millis() - tempo_ex < 2000 || envia == false){
    sizepk2 = server_socket_receve.parsePacket();
    if(sizepk2){
    //Serial.println("ok");
    int tamanho = server_socket_receve.read(buffer6, sizeof(buffer6));
    Serial.println(tamanho);
    GatewayToDeviceMessage mensagemGattoDev_pare;
    pb_istream_t StreammensagemGattoDev_pare = pb_istream_from_buffer(buffer6, sizepk2);
      if (pb_decode(&StreammensagemGattoDev_pare, GatewayToDeviceMessage_fields, &mensagemGattoDev_pare)) {
        int result = strcmp(mensagemGattoDev_pare.command, "Pare");
        Serial.println(mensagemGattoDev_pare.command);
        if (result == 0) {
          envia = false;
          Serial.println("Para!");
        } else {
          envia = true;
        }
      } else{
        Serial.println("Erro de decodificação");
      }
    }
  }
}
