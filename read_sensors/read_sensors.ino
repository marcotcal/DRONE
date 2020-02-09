/*
  Drone - Remote Control
  Sensor Reader - Raspberry Pi 
  This program reads the analog joystics and buttons
  See Arduino Nano pinout 
  The data is sent as a string through serial to the Raspberry Pi
*/


void setup() {
  Serial.begin(9600);
  pinMode(2,INPUT);
  pinMode(3,INPUT);
  pinMode(4,INPUT);
  pinMode(5,INPUT);
  pinMode(6,INPUT);
  pinMode(7,INPUT);
  pinMode(8,INPUT);
}

void loop() {
  char data[100];
  int js1 = analogRead(A0);
  int js2 = analogRead(A1);
  int js3 = analogRead(A2);
  int js4 = analogRead(A3);
  int ch1 = digitalRead(2);
  int ch2 = digitalRead(3);
  int ch3 = digitalRead(4);
  int ch4 = digitalRead(5);
  int ch5 = digitalRead(6);
  int ch6 = digitalRead(7);
  int ch7 = digitalRead(8);
  
  sprintf(data, "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d",js1,js2,js4,js3,ch1,ch2,ch3,ch4,ch5,ch6,ch7);
  Serial.println(data);
  delay(1);   
}

