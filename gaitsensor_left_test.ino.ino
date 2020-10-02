// for microcomputer
#include "M5Atom.h"
// for BLE
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLE2902.h>
// for Bluetooth Serial function.(not BLE)
#include "BluetoothSerial.h"

// BLE service name
#define SERVER_NAME "Gait_sensor_peripheral"

bool deviceConnected = false;           // Device connections

// Define Bluetooth Serial variables.
#define SERIALBT_NAME "Gaitsensor_BT_Serial"
BluetoothSerial SerialBT;

// for Terminal
#define SPI_SPEED 115200

// sensor pin defined
#define TOO_PIN 32
#define HEEL_PIN 26

// for LowPath filter.(N)
#define FILTER 1000
//for Low path filter (Moving average filter)
int filter[FILTER] = {0};

/*********************<     walking time value     >************************/
// send data.(send before time.The lag is calculated by comparing with the received time.)
int beforetime = 0;
// received time.
int aftertime = 0;

// before state (bool : Standing phase <= true, Swing period =< false)
bool beforestate;
// Walking data (stand time, swing time.)
int standtime = 0;
int swingtime = 0;

//for Both feet support period
int maintime = 0;
bool mainon;

int bothfoottime = 0;
// Steps
int mainsteps = 0;

//{左立脚期,左遊脚期,右立脚期,右遊脚期,左両脚支持期,右両脚支持期}
#define DATANUM 6
int walkingdata[DATANUM] = {0,0,0,0,0,0};

void input_data(int x, int n){
    if( n == 0 ){for(int i=0;i<=DATANUM;i++){walkingdata[i] = 0;}}
    else{walkingdata[x] = n;}
}

/******************************************************************************/
/*********************<        Setup (Prepare)        >************************/
void setup() {
    // for terminal
    Serial.begin(SPI_SPEED);
    // etextile pinMode setting
    pinMode(TOO_PIN,  INPUT_PULLUP);
    pinMode(HEEL_PIN, INPUT_PULLUP);
    // for M5Atom Lite
    M5.begin(true, false, true);

    // Start a Bluetooth Serial.
    SerialBT.begin(SERIALBT_NAME);
    delay(1000);

    Serial.println(3);
    delay(1000);
    Serial.println(2);
    delay(1000);
    Serial.println(1);
    delay(1000);
    beforetime = millis(); aftertime = millis();
    maintime = millis();
}
/******************************************************************************/
/*********************<          Main sequence        >************************/
void loop() {
    float ave = 0.0;

    // do Low path filter (Moving average filter)
    for(int i = FILTER - 1; i > 0; i--) filter[i] = filter[i - 1];
    if((digitalRead(TOO_PIN) == LOW)||(digitalRead(HEEL_PIN) == LOW)) filter[0] = 1;
    else  filter[0] = 0;
    // decide walking state
    for(int i = 0; i < FILTER; i++) ave += filter[i];
    ave = (float)ave / FILTER;

    if(ave >= 0.7){       //足がついている
        if(!beforestate){
            swingtime = millis() - beforetime;
            mainon = true;
            if(swingtime > 100){
                Serial.println("swingtime : " + String(swingtime));
                input_data(1,swingtime);
                maintime = millis();
                beforetime = millis();
                mainsteps += 1;
                Serial.println("main steps : " + String(mainsteps));
                //SerialBT.printf("%d,%d,%d,%d,%d,%d\n",walkingdata[0],walkingdata[1],walkingdata[2],walkingdata[3],walkingdata[4],walkingdata[5]);
                Serial.printf("%d,%d,%d,%d,%d,%d\n",walkingdata[0],walkingdata[1],walkingdata[2],walkingdata[3],walkingdata[4],walkingdata[5]);
                input_data(0,0); //初期化
            }
            beforestate = true;
        }
    }else{
        if(beforestate){
            standtime = millis() - beforetime;
            mainon = false;
            if(standtime > 100){
                beforetime = millis();
                Serial.println("standtime : " + String(standtime));
                input_data(0,standtime);
            }
            beforestate = false;
        }
    }
}
