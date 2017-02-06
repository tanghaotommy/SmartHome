//sudo chmod a+rw /dev/ttyACM0
int smokeA0 = A5;
// Your threshold value
int sensorThres = 400;
char incomingdata;

void setup() {
  pinMode(smokeA0, INPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
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
    }
    // Checks if it has reached the threshold value
    if (analogSensor > sensorThres)
    {
    Serial.println("gasalarm");
    }
    delay(100);
}
}

