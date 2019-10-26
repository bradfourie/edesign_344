#include <LiquidCrystal.h>

// Serial communication setup
constexpr long serial_baud_rate = 19200;
constexpr auto serial_config = SERIAL_8E1;

// Leonardo board information
constexpr int digital_pins[] = {9, 10, 11};
constexpr int analogue_pins[] = {A0, A1, A2};

const String STUDENT_NUMBER = "20795629";

unsigned long time1 = millis(); // LED receive indicator timer
unsigned long time2 = millis(); // Debug mode timer
unsigned long time3 = millis(); // Poll data timer
unsigned long time4 = millis(); // 1KHz charge pump timer
unsigned long MillisecondsUpdtime = 0; // Uptime Counter

const byte numChars = 3; // two read bytes + end-of-line
char receivedChars[numChars]; // an array to store the received data

boolean newData = false;
boolean DebugMode = false;
boolean chargePumpOut = false;
boolean resetInit = false;

String BinaryString = "";
String Outputstring = "";
int Aread = 0;

void setup() {
  Serial.begin(19200, serial_config);
  pinMode(digital_pins[0], OUTPUT);
  pinMode(digital_pins[1], INPUT);
  pinMode(digital_pins[2], OUTPUT);
  //init SR Latch
  digitalWrite(digital_pins[2], HIGH);
  delay(100);
  digitalWrite(digital_pins[2], LOW);
}

void loop()
{
  ReceiveData();
  TransmitData();
  DebugCheck();
  //PollData();

  // LED receive notifier timeout
  if (millis() - time1 > 200) {
    digitalWrite(LED_BUILTIN, LOW);
    time1 = millis();
  }
  // Charge pump timer 
  if (millis() - time4 > 0.1) {
    if(chargePumpOut){
      digitalWrite(digital_pins[0], LOW);
    }else{
      digitalWrite(digital_pins[0], HIGH);
    }
    chargePumpOut = !chargePumpOut;
    time4 = millis();
  }
}

void ReceiveData() {

  char Read_end = '\n';
  static byte rdx = 0;
  char ReadCharacter;


  while (Serial.available() > 0 && newData == false) {

    ReadCharacter = Serial.read();

    digitalWrite(LED_BUILTIN, HIGH);

    if (ReadCharacter != Read_end) {
      receivedChars[rdx] = ReadCharacter;
      rdx++;
      if (rdx >= numChars) {
        rdx = numChars - 1;
      }
    }
    else {
      receivedChars[rdx] = '\0'; // terminate the string
      rdx = 0;
      newData = true;
    }
  }
}

void TransmitData() {
  if (newData == true) {
    if (receivedChars[0] == '0' && DebugMode == false) {
      Serial.println(receivedChars[0]);
      Serial.println(STUDENT_NUMBER);
    }

    if (receivedChars[0] == '1' && DebugMode == false) {
      double output;
      Serial.println(receivedChars[0]);
      Serial.println(receivedChars[1]);
      //Here you can apply calibration as necessary.
      switch (receivedChars[1]) {
        case '0' :
          Aread = analogRead(analogue_pins[0]);
          output = (double) 0.175953 *Aread - 3; //phase transducer
          if(output > 45 || output <= 3){
            output = 0;
          }
          break;
        case '1' :
          Aread = analogRead(analogue_pins[1]);
          output =  ((double) Aread*5/1023 * 73.455313 + 1.181447)/sqrt(2); //current transducer
          if(output <= 1.181447/sqrt(2)){
            output = 0;
          }
          break;
        case '2' :
          Aread = analogRead(analogue_pins[2]);
          output = ((double) Aread*5/1023 *7.348095 + 0.2585596)/sqrt(2); //voltage transducer
          if(output <= 0.2585596/sqrt(2)){
            output = 0;
          }
          break;
      }
      Serial.println(output);
    }

    if (receivedChars[0] == '2' && DebugMode == false) {
      Serial.println(receivedChars[0]);
      Serial.println(receivedChars[1]);
      switch (receivedChars[1]) {
        case '0' : Serial.println(digitalRead(digital_pins[0])); break;
        case '1' : Serial.println(digitalRead(digital_pins[1])); break;
        case '2' : Serial.println(digitalRead(digital_pins[2])); break;
      }
    }

    if (receivedChars[0] == 'x' || receivedChars[0] == 'X') {
      if (receivedChars[1] == '0') {
        DebugMode = false;
      }
      else if (receivedChars[1] == '1') {
        DebugMode = true;
      }
    }

    if ((receivedChars[0] == 'U' || receivedChars[0] == 'u') && DebugMode == false){
      MillisecondsUpdtime = millis();
      uptime();
    }
    if(receivedChars[0] == 'T'){
      digitalWrite(digital_pins[2], HIGH);
      delay(100);
      digitalWrite(digital_pins[2], LOW);
    }
    
  } else {
    String output = "";

    int Aread0 = analogRead(analogue_pins[0]);
    delay(10);
  
    int Aread1 = analogRead(analogue_pins[1]);
    delay(10);
  
    int Aread2 = analogRead(analogue_pins[2]);
    delay(10);
    
    double phase_measurement = (double) 0.175953 *Aread0 - 3; //phase transducer
    
    double current_measurement =  ((double) Aread1*5/1023 * 73.455313 + 1.181447)/sqrt(2); //current transducer
    
    double voltage_measurement = ((double) Aread2*5/1023 *7.348095 + 0.2585596)/sqrt(2); //voltage transducer
    
    String reset_value = ReturnDigitalRead(digitalRead(digital_pins[1]));
    
    if(phase_measurement > 45 || phase_measurement <= 3){
      phase_measurement = 0;
    }
    if(voltage_measurement <= 0.2585596/sqrt(2)){
      voltage_measurement = 0;
    }
    //if(current_measurement <= 1.181447/sqrt(2)){
    //  current_measurement = 0;
    //}
     if(current_measurement <= 2){
    current_measurement = 0;
  }

    String foobar = "";
    output = foobar + phase_measurement + ' ' + current_measurement + ' ' + voltage_measurement + ' ' + reset_value;
    
    if (millis() - time3 > 1000) { // Wait 1 second hopefully
      Serial.println(output);
      time3 = millis();
    }
  }
  newData = false;
}

void DebugCheck() {
  if (DebugMode == true) {
    String DebugOutput = "";
    int Aread0 = analogRead(analogue_pins[0]);
    delay(10);
    int Aread1 = analogRead(analogue_pins[1]);
    delay(10);
    int Aread2 = analogRead(analogue_pins[2]);
    delay(10);

    DebugOutput = STUDENT_NUMBER + ',' + "A0:" + Aread0 + ',' + "A1:" + Aread1 + ',' + "A2:" + Aread2 +
                  ',' + "D0:" + ReturnDigitalRead(digitalRead(digital_pins[0])) + ',' + "D1:" + ReturnDigitalRead(digitalRead(digital_pins[1])) +
                  ',' + "D2:" + ReturnDigitalRead(digitalRead(digital_pins[2]));
    if (millis() - time2 > 2000) { // LED receive notifier timeout
      Serial.println("X");
      Serial.println(DebugOutput);
      time2 = millis();
    }
  }
}

String ReturnDigitalRead(int Input) {
  if (Input == 0) {
    return "LOW";
  }
  else {
    return "HIGH";
  }
}



void uptime()
{
  long days = 0;
  long hours = 0;
  long mins = 0;
  long secs = 0;
  secs = MillisecondsUpdtime / 1000; //convect milliseconds to seconds
  mins = secs / 60; //convert seconds to minutes
  hours = mins / 60; //convert minutes to hours
  days = hours / 24; //convert hours to days
  secs = secs - (mins * 60); //subtract the coverted seconds to minutes in order to display 59 secs max
  mins = mins - (hours * 60); //subtract the coverted minutes to hours in order to display 59 minutes max
  hours = hours - (days * 24); //subtract the coverted hours to days in order to display 23 hours max
  
  String UptimeOutput = "";
  String comma = ":";
  UptimeOutput = hours + comma + mins + comma + secs ;
  Serial.println("U");
  Serial.println(UptimeOutput);
}
