//sudo chmod a+rw /dev/ttyACM0
int smokeA0 = A5;
// Your threshold value
int sensorThres = 175;
char incomingdata;

void setup() {
  Serial.begin(9600);
  pinMode(smokeA0, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);  //LED_BUTLTIN is pin13
  pinMode(12, OUTPUT);
  pinMode(8, OUTPUT);
}

void loop() {
    incomingdata = Serial.read();
    if (incomingdata=='l'){
    int val;
    val=analogRead(0);   //connect grayscale sensor to Analog 0
    Serial.println(val,DEC);//print the value to serial        
    delay(100);
    }
    int analogSensor = analogRead(smokeA0);  
    if (incomingdata=='g'){
       Serial.println(analogSensor);
       delay(1000);
    }
    
    if (incomingdata=='d'){   //dooropen
    digitalWrite(12, HIGH);  //pin12 is Vdd
    digitalWrite(8, LOW);   //pin8 is ground
    digitalWrite(LED_BUILTIN, HIGH);   
    delay(400);                       
    digitalWrite(LED_BUILTIN, LOW);    
    delay(1000);                 
    }
  
    if (analogSensor > sensorThres)
    {
        Serial.println("a");
        delay(10000);
    }
   
}

