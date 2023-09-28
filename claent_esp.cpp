#include <ESP8266WiFi.h>
#include <WebSocketsServer.h>
#include <descoberta.pb.h> 

//configurações da rede
const char* ssid = "SUA_REDE_WIFI";
const char* password = "SUA_SENHA_WIFI";

const int webSocketPort = 12345;
WebSocketsServer webSocket = WebSocketsServer(webSocketPort);

void handleWebSocket() {
  webSocket.loop();
}

void onWebSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t length) {
  switch (type) {
    case WStype_TEXT: {
      String message = String((char*)payload);

      // Verificar se é uma mensagem de descoberta
      if (message.startsWith("DISCOVER:")) {
        // Extrair informações da mensagem
        message.remove(0, 9); // Remove "DISCOVER:" prefix
        DiscoveryMessage discovery;
        discovery.ParseFromString(message.c_str());

        // Processar a mensagem de descoberta
        Serial.println("Mensagem de descoberta recebida:");
        Serial.println("Device ID: " + discovery.device_id());
        Serial.println("Device Type: " + discovery.device_type());

        // Responder à mensagem de descoberta
        DiscoveryMessage response;
        response.set_device_id("ESP8266-12345");
        response.set_device_type("Sensor");
        response.set_device_ip(WiFi.localIP());
        response.set_device_port(webSocketPort);

        String responseMessage;
        response.SerializeToString(&responseMessage);
        webSocket.sendTXT(num, responseMessage);
      }
      break;
    }
    default:
      break;
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado ao WiFi!");

  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);
}

void loop() {
  handleWebSocket();
}
