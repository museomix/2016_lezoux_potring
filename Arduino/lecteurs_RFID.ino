// Using SeeedStudio GROVE RFID READER SEN11425P
// link between the computer and the SoftSerial Shield
//at 9600 bps 8-N-1
//Computer is connected to Hardware UART
//SoftSerial Shield is connected to the Software UART:D2&D3 

//link to catalog
//http://www.seeedstudio.com/wiki/Grove_-_125KHz_RFID_Reader
//link to datasheet
//http://www.seeedstudio.com/wiki/index.php?title=Electronic_brick_-_125Khz_RFID_Card_Reader#Block_Diagram
//
//http://www.priority1design.com.au/em4100_protocol.html

//ASTUCE: pour forcer une relecture alors que le TAG est toujours présent, couper puis remettre l'alim par le 0V
// (ne marche pas avec le +, peut être a cause d'une alim indirecte via UART ?)

//cablage du module RFID GROVE (SeedStudio)
//Arduino=>RFID
//Rouge=>5V
//Noir=>13
//Blanc=>3
//Jaune=>2


#include <SoftwareSerial.h>
#define START 0x02
#define END 0x03

SoftwareSerial SoftSerial(2, 3);
String ReceivedCode = "";


int count=0;     // counter for buffer array 
void setup()
{
  SoftSerial.begin(9600);               // the SoftSerial baud rate   
  Serial.begin(9600);             // the Serial port of Arduino baud rate.
  //Serial.println("OOTSIDEBOX-JNL Using SeeedStudio GROVE RFID READER SEN11425P");
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
}
 
void loop()
{
  static int Tempo=0;
  static int Counter=0;
  char RecievedChar;
  Tempo++;
  if (Tempo> 500)
  {
    Tempo=0;
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
  }
  delay(10);
  
   
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  
  if (SoftSerial.available())             
  {
      RecievedChar=SoftSerial.read();
      if(isprint(RecievedChar)) ReceivedCode+=RecievedChar; 
      
      //if(Counter==10) Serial.print("/");
      if(RecievedChar==START) 
        {
          //Serial.print("<START>");
          Counter=0;
        }
      else Counter++;
      
      if(RecievedChar==END) 
        {
          //Serial.print("<END> TagID: ");
         // ReceivedCode.remove(10, 2); // Remove 2 characters starting at index=10
          Serial.println(ReceivedCode);
          ReceivedCode="";  
        }
      else Serial.write(RecievedChar);
   }
}

