
const int trigPin1 = 2; // the number of the trigger output pin ( sensor 1 )
const int echoPin1 = 3; // the number of the echo input pin ( sensor 1 )     
const int trigPin2 = 4;  // the number of the trigger output pin ( sensor 2 ) 
const int echoPin2 = 5;  // the number of the echo input pin ( sensor 2 ) 
const int motorPin1 = 9; // the number of the first motor input pin
const int motorPin2 = 10; // the number of the second motor input pin 
const int motorPin3 = 6; // the number of the third motor input pin 

int l1 = 1; // state variable for motor

// variables used for distance calculation 
long duration;                               
int distance1, distance2; 
float r;
unsigned long temp=0;
int temp1=0;
int l=0;
////////////////////////////////

void find_distance (void);

// this function returns the value in cm.

void find_distance (void)                   
{ 
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);

  duration = pulseIn(echoPin1, HIGH, 5000);// here this pulse in function wont wait more then 5000us for the ultrasonic sound to came back. (due to this it wont measure more than 60cm)
                                           // it helps this project to use the gesture control in the defined space. 
                                           // so that, it will return zero if distance greater then 60m. ( it helps usually if we remove our hands infront of the sensors ).
 
  r = 3.4 * duration / 2;                  // calculation to get the measurement in cm using the time returned by the pulsein function.     
  distance1 = r / 100.00;
  /////////////////////////////////////////upper part for left sensor and lower part for right sensor
  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);

  duration = pulseIn(echoPin2, HIGH, 5000);
  r = 3.4 * duration / 2;     
  distance2 = r / 100.00;
  delay(100);
}



void toggleMotor()
{
  if (Serial.available() > 0) 
  {
    if (l1 == 1)
    {
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, LOW);
      digitalWrite(motorPin3, LOW);
      l1 = 0;
      Serial.println('obs'); // prints 'obs' in serial monitor for shutting down python script if needed
    } 
  }
  
}

void setup() 
{
  // put your setup code here, to run once

  Serial.begin(9600);
  pinMode(trigPin1, OUTPUT); // initialize the trigger and echo pins of both the sensor as input and output:
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(13, OUTPUT);
  analogWrite(motorPin3,255);
}

void loop() 
{
  // put your main code here, to run repeatedly:

  toggleMotor(); // switches off motors if l1 state variabe is 1 i.e.; obstacle detected
 
  find_distance(); // this function will stores the current distance measured by the ultrasonic sensor in the global variable "distance1 and distance2"
                   // no matter what, the program has to call this "find_distance" function continuously to get the distance value at all time.
  
  if ((distance1 >= 5) && (distance1 <= 10)) l1 = 1;
  if ((distance2 >= 5) && (distance2 <= 10)) l1 = 1;
}
