//sudo chmod a+rw /dev/ttyACM0
int smokeA0 = A5;
// Your threshold value
int sensorThres = 400;

void setup() {
  pinMode(smokeA0, INPUT);
  Serial.begin(9600);
}

void loop() {
  int analogSensor = analogRead(smokeA0);

  Serial.print("rPin A0: ");
  Serial.println(analogSensor);
  // Checks if it has reached the threshold value
  //if (analogSensor > sensorThres)
  //{
    
  //}
  //else
  //{
    
  //}
  delay(100);
}

