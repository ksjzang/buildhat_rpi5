import paho.mqtt.client as mqtt
import json
import time

# MQTT 설정
broker = "broker.hivemq.com"  # MQTT 브로커 IP
port = 1883                 # 기본 포트
topic = "GHU"
client_id = 'team05'

# MQTT 클라이언트 생성
client = mqtt.Client(client_id)

# 콜백 함수: 연결 성공
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(topic)  # 브로커 연결 시 주제 구독

# 콜백 함수: 메시지 수신
def on_message(client, userdata, msg):
    global recv_message
    try:
        # 메시지 디코딩 및 JSON 파싱
        decoded_msg = msg.payload.decode('utf-8')
        recv_message = json.loads(decoded_msg)
        print(f"Received: {recv_message}")
    except Exception as e:
        print(f"Failed to process message: {e}")

# 메세지 송신
def publish_message(topic, message):
    """MQTT 메시지 발행 함수"""
    try:
        # 메시지를 JSON 형식으로 직렬화 후 발행
        payload = json.dumps(message)
        client.publish(topic, payload)
        print(f"Published: {payload}")
    except Exception as e:
        print(f"Failed to publish message: {e}")

# 콜백 함수 등록
client.on_connect = on_connect
client.on_message = on_message

# 브로커 연결
client.connect(broker, port)
print("Connected to MQTT Broker")

# 네트워크 루프 시작 (비차단 방식)
client.loop_start()

# 주기적으로 메시지 발행
try:
    counter = 0
    while True:
        message = [client_id, 'wind', "R"]  # 메시지 데이터
        publish_message(topic, message)
        counter += 1
        time.sleep(5)

except KeyboardInterrupt:
    print("Publisher stopped.")
    client.loop_stop()  # 네트워크 루프 중지
    client.disconnect()
