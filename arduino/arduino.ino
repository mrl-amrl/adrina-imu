#include <Wire.h>

#include <Ethernet.h>
#include <EthernetUdp.h>

byte mac[] = {
    0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};

EthernetUDP Udp;

IPAddress broadcastAddr(192, 168, 10, 110);
unsigned int broadcastPort = 8888;

IPAddress ip(192, 168, 10, 80);
unsigned int localPort = 8888;

#include "MPU6050.h"

MPU6050 imu(Wire);

void setup()
{
    Ethernet.begin(mac, ip);
    Udp.begin(localPort);
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    Wire.begin();
    imu.begin();
    imu.calcGyroOffsets();
    digitalWrite(LED_BUILTIN, LOW);
}

void loop()
{
    imu.update();
    signed int roll = int(imu.getAngleX());
    signed int pitch = -int(imu.getAngleY());
    signed int yaw = -int(imu.getAngleZ());

    if (pitch < 0)
        pitch += 360;
    if (yaw < 0)
        yaw += 360;

    char roll_str[7];
    char yaw_str[7];
    char pitch_str[7];

    String str;
    Udp.beginPacket(broadcastAddr, broadcastPort);
    Udp.write("$BEGIN:");
    str = String(yaw);
    str.toCharArray(yaw_str, 7);
    Udp.write(yaw_str);
    Udp.write(",");
    str = String(pitch);
    str.toCharArray(pitch_str, 7);
    Udp.write(pitch_str);
    Udp.write(",");
    str = String(roll);
    str.toCharArray(roll_str, 7);
    Udp.write(roll_str);
    Udp.write(";");
    Udp.endPacket();
}
