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
char * strTemp;

//const char* ssid = "brisa-2664316";
//const char* password = "kum0hxa8";
const char* ssid = "JM";
const char* password = "testedoprojeto2";

// Porta que a ESP8266 ficará escutando
unsigned int udpPort = 54321;

// Crie uma instância do objeto UDP
WiFiUDP udp;

float temperature; //variável para armazenar a temperatura
float humidity; //Variável para armazenar a umidade
char buffer_sensor[50];
String sensor_tu = "";

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
  char buffer[1024];
  int packetSize = udp.parsePacket();
  if (packetSize) {
    // Receber a mensagem multicast
    int bytesRead = udp.read(buffer, packetSize);
    IPAddress ip_reme = udp.remoteIP();
    unsigned int port_reme = udp.remotePort();

      if (bytesRead>0) {
        buffer[packetSize] = '\0'; // Adicione um terminador nulo para formar uma string válida
        Serial.print("Mensagem recebida: ");
        Serial.println(buffer);
        if (comp_string(buffer," +Descoberta de dispositivos: Quem está aí?") == true){
          Identification mensagemI = Identification_init_zero;
          mensagemI.device_type.arg = (void*)"Sensor Temperatura e Umidade";
          mensagemI.device_type.funcs.encode = encode_string;
          mensagemI.device_ip.arg = (void*)WiFi.localIP().toString().c_str();
          mensagemI.device_ip.funcs.encode = encode_string;
          mensagemI.device_port = udpPort;
          mensagemI.protocol.arg = (void*)"UDP";
          mensagemI.protocol.funcs.encode = encode_string;
          
          uint8_t buffer2[1024];
          pb_ostream_t stream = pb_ostream_from_buffer(buffer2, sizeof(buffer2));

          if (pb_encode(&stream, Identification_fields, &mensagemI)) {
            // Envie o buffer via UDP para o servidor
            udp.beginPacketMulticast(multicast_ip, udpPort, WiFi.localIP());
            udp.write(buffer2, stream.bytes_written);
            udp.endPacket();
            Serial.println("Mensagem enviada via UDP");
            while(1){
              bool verif;
              verif = ler_sensor();
              DeviceToGatewayMessage mensagemDG = DeviceToGatewayMessage_init_zero;
              mensagemDG.response.arg = (void*)sensor_tu;
              mensagemDG.response.funcs.encode = encode_string;

              uint8_t buffer3[256];
              pb_ostream_t stream2 = pb_ostream_from_buffer(buffer3, sizeof(buffer3));
              if (pb_encode(&stream2, DeviceToGatewayMessage_fields, &mensagemDG)) {
                udp.beginPacket(ip_reme, port_reme);
                udp.write(buffer2, stream.bytes_written);
                udp.endPacket();
                Serial.println("Temperatura e umidade enviadas com sucesso via UDP!");
              } else{
                Serial.println("Falha ao codificar a mensagem de temperatura e umidade");
              }
            }
          } else {
            Serial.println("Falha ao codificar a mensagem");
          }
        }
      }
  }
}


bool comp_string(const char *str1, const char *str2){
  for (int i = 0; str1[i] == '\0' || str2[i] == '\0'; i++){
    Serial.print(str1[i]);
    Serial.println(str2[i]);
    if (str1[i]!=str2[i]){
      return false;
    }
  }
  return true;
}

bool encode_string(pb_ostream_t *stream, const pb_field_t *field, void *const *arg) {
    char *str = strTemp;
    if (!pb_encode_tag_for_field(stream, field))
        return false;
    return pb_encode_string(stream, (uint8_t *)str, strlen(str));
}

bool decode_string(pb_istream_t *stream, const pb_field_t *field, void **arg) {
    uint8_t buffer[1024] = {0};

    /* We could read block-by-block to avoid the large buffer... */
    if (stream->bytes_left > sizeof(buffer) - 1)
        return false;

    if (!pb_read(stream, buffer, stream->bytes_left))
        return false;

    /* Print the string, in format comparable with protoc --decode.
     * Format comes from the arg defined in main().
     */
    Serial.print("Message.test_string: ");
    Serial.println((char *)buffer);
    //printf((char*)*arg, buffer);
    return true;
}

bool ler_sensor(){
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Erro ao ler o sensor DHT!");
    sensor_tu += "Erro de leitura do sensor";
  } else {
    sprintf(buffer_sensor, "Humidade: %.2f | Temperatura: %.2f", humidity, temperature);
    sensor_tu += buffer_sensor;
    return true;
  }
  return false;
}
