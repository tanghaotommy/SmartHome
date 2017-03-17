//sudo chmod a+rw /dev/ttyACM0
int smokeA0 = A5;
// Your threshold value
int sensorThres = 175;
char incomingdata;

void setup() {
  pinMode(smokeA0, INPUT);
  Serial.begin(9600);
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
    
    if (incomingdata='d'){
    	//dooropen

    }
    if (analogSensor > sensorThres)
    {
        Serial.println("a");
        delay(10000);
    }
   
}

