// bibliotecas do sensor
#include <Adafruit_Sensor.h>
#include <DHT.h>

#include <Adafruit_Sensor.h>
#include <WebSocketsClient_Generic.h>
#include <WebSocketsServer_Generic.h>

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#include "protobuf_messages.pb.h"
#include "pb_common.h"
#include "pb_decode.h"
#include "pb_encode.h"

const char* ssid = "brisa-2664316";
const char* password = "kum0hxa8";
// const char* ssid = "JM";
// const char* password = "testedoprojeto2";

// Porta que a ESP8266 ficará escutando
unsigned int udpPort = 54321;

// Crie uma instância do objeto UDP
WiFiUDP udp;

float temperature; //variável para armazenar a temperatura
float humidity; //Variável para armazenar a umidade

#define DHT_PIN D2       // Pino onde o DHT22 está conectado (por exemplo, D2).
#define DHT_TYPE DHT22  // Tipo de sensor DHT que você está usando (DHT11, DHT21, ou DHT22).

DHT dht(DHT_PIN, DHT_TYPE);

const IPAddress multicast_ip(224, 1, 1, 1);

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
  IPAddress ip = WiFi.localIP();
  Serial.printf("IP da Esp: ");
  Serial.println(ip);
  // Inicialize o objeto UDP
  delay(1000);

  //iniciando o multicast
  udp.beginMulticast(WiFi.localIP(), multicast_ip, udpPort);
  delay(1000);

  Serial.printf("Pronto para receber uma mensagem no grupo IP: %s | Porta: %d \n", multicast_ip.toString().c_str(), udpPort);
}

void loop() {
  const int maxMessageSize = 1024;
  char str[1024]; // Defina o tamanho apropriado para a sua string
  uint8_t buffer[maxMessageSize];
  // escutando o grupo multicast definido (é uma instrução não bloqueante)
  int packetSize = udp.parsePacket();
  if (packetSize!=0) {
    Serial.printf("Recebido %d bytes do endereço %s, porta %d\n", packetSize, udp.remoteIP().toString().c_str(), udp.remotePort());
    udp.read(buffer, maxMessageSize);
    // Leia os dados recebidos
    Discovery mensagem = Discovery_init_zero;
    pb_istream_t stream = pb_istream_from_buffer(buffer, packetSize);
    if (pb_decode(&stream, Discovery_fields, &mensagem)) {
            Serial.print("Texto: ");
            Serial.printf("%s", mensagem.message);
            //pb_decode_string(stream, (uint8_t*)str, strlen(str));
        } else {
            Serial.println("Falha ao decodificar a mensagem.");
        }

    }
  }
  // String string = "oi";
  // char msg[255];
  // string.toCharArray(msg,255);
  // udp.beginPacketMulticast(multicast_ip, udpPort, WiFi.localIP());
  // udp.write(msg);
  // udp.endPacket();
//   delay(2000);
//   humidity = dht.readHumidity();
//   temperature = dht.readTemperature();

//  if (isnan(humidity) || isnan(temperature)) {
//    Serial.println("Erro ao ler o sensor DHT!");
//  } else {
//    Serial.print("Umidade: ");
//    Serial.print(humidity);
//    Serial.print("%\t");
//    Serial.print("Temperatura: ");
//    Serial.print(temperature);
//    Serial.println("°C");
//  }
// }
