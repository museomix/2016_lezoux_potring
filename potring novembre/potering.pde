import java.io.File;
import processing.video.*;

// Signals transmitted from the makeymakey device
boolean[] keys; 

// -- We have three objects that we want to handle, each one can be on one of the two available platforms
// -- Platforms are named duo1 and duo2 in the code below
int nbKeys = 6;

// -- "z", "q", "s", "d", "f", "g", "LEFT", "UP", "RIGHT"
// -- "w", "a", "s", "d", "f", "g", "LEFT", "UP", "RIGHT"
// -- Key codes are used instead of letters to avoid issues with the configuration of the keyboard.
int[] v = {
  90, 81, 83, 68, 70, 71, 37, 38, 39
};

// -- Associate each object object to its signal
int duo1_objet1 = 0;
int duo1_objet2 = 1;
int duo1_objet3 = 2;

int duo2_objet1 = 3;
int duo2_objet2 = 4;
int duo2_objet3 = 5;

// Other global variables
// Le numéro de la question en cours 
// -- 0 => discours entre potiers conclu par une question
// -- 1 => réponse à la question 1 (Q1) + Q2
// -- 2 => réponse à Q2 + affichage statistiques
int numQuestion = 0;
// Le nombre d'objets attendu et géré par le programme
int nbObjets = 3;
// Connaissance sur l'utilisation des plots (un plot utilisé = 1 objet bien positionné dessus)
boolean duo1Activated = false;
boolean duo2Activated = false;
// L'identifiant de l'objet qui est sur chaque plot
// A la première place (indice 0), plot1, à l'indice 1, plot 2
// Identifiants des objets : 0 pour l'objet 1, 1 pour l'objet 2, 2 pour l'objet 3
int[] obj = {-1,-1};
// Un hashmap qui stocke toutes les images en mémoire de manière à être immédiatement disponible à l'affichage
HashMap<String,Movie> allVideos = new HashMap<String,Movie>();
// Indique si le programme attend une réponse à une des deux questions des potiers
int enAttenteDeReponse = 0;
// Indique quel est l'objet qui a été soulevé après la question posée au visiteur
int numObjReponse = -1;
// Indique  quel est l'ajout au nom à faire (si c'est la réponse à une question)
String[] ajoutNom = {"","",""};
// Indique si une vidéo est en train de tourner.
boolean isFilmEnCours = false;
Movie filmEnCours;
float tempsTotFilmEnCours;
float tempsCourantFilmEnCours;


// Statistiques
// -- Présence d'un objet dans une comparaison
int[] presenceObjet = {0,0,0};
// -- Nombre de comparaisons effectuées
int nbDuels = 0;
// -- Nombre de duels terminés
int nbDuelsTermines;

void afficherImageObjets(int part,int obj1,int obj2)
{
  int tmpObj1 = obj1;
  int tmpObj2 = obj2;
  if(obj1 > obj2)
  {
    tmpObj1 = obj2;
    tmpObj2 = obj1;
  }
  String fileToLoadName = "Video_";
  fileToLoadName += part;
  fileToLoadName += "_Objet";
  fileToLoadName += tmpObj1+1;
  fileToLoadName += ajoutNom[tmpObj1];
  fileToLoadName += "_Objet";
  fileToLoadName += tmpObj2+1;
  fileToLoadName += ajoutNom[tmpObj2];
  fileToLoadName += ".mov";
  println(fileToLoadName);
  println(allVideos.get(fileToLoadName));
  filmEnCours = allVideos.get(fileToLoadName);
  filmEnCours.play();
  tempsTotFilmEnCours = filmEnCours.duration();
  isFilmEnCours = true;
  if (numObjReponse != -1)
  {
    ajoutNom[numObjReponse] = "";
  }
}

void setup() {
  //Init display backgroung
  size(1920, 1088);
  
  // Init keys
  keys = new boolean[nbKeys];
  for (int i = 0; i < nbKeys; i++)
  {
    keys[i] = false;
  }
  
  // Init allVideos (load all the images at the beginning to avoid to loose time at execution) 
  File dir = new File(dataPath(""));
  File[] files = dir.listFiles();
  for(int i=0; i < files.length; i++ )
  { 
    String path = files[i].getAbsolutePath();
    String fileName = files[i].getName();
    if (fileName.endsWith(".mov") == true)
    {
      allVideos.put(fileName, new Movie(this, fileName));
    }
  }
  frameRate(25); // par seconde
} 

void ecouteDesActionsDuVisiteur()
{
  if (numQuestion == 0)
  {
    // 0 => the discussion did not begin
    if (duo1Activated & duo2Activated)
    {
      // Si les deux plots sont activés, la discussion peut commencer
      println("2 plots cativés");
      presenceObjet[obj[0]] += 1;
      presenceObjet[obj[1]] += 1;
      nbDuels += 1;
      afficherImageObjets(numQuestion,obj[0],obj[1]);
      numQuestion += 1;
    }
    else
    {
      println("DSL, pas actif");
      // Sinon, le message d'accueil suffit
      //image(allVideos.get("Accueil.png"),0,0);
    }
  }
  else if ((numQuestion == 1) | (numQuestion == 2))
  {
    println("num question");
    println(numQuestion);
    if (enAttenteDeReponse != 0)
    {
      println("Plus en attente de réponse");
      println(obj[enAttenteDeReponse-1]);
      println(numObjReponse);
      // Le visiteur a reposé un objet sur le plot, on regarde si c'est le même ou non
      if( obj[enAttenteDeReponse-1] != numObjReponse )
      {
        // Si l'objet reposé est différent de l'objet soulevé, alors on commence un nouveau dialogue entre le nouveau couple
        println("Objet différent, on recommence");
        numQuestion = 0;
      }
      else
      {
        // Si l'objet est le même, on lance la réponse adéquate
        println("On lance la réponse");
        ajoutNom[numObjReponse] = "G";
        afficherImageObjets(numQuestion,obj[0],obj[1]);
        numQuestion += 1;
      }
      enAttenteDeReponse = 0;
      numObjReponse = -1;
    }
    else if (duo1Activated == false)
    {
      if (duo2Activated == false)
      {
        // Le visiteur a enlevé les deux objets, on recommence du début
        println("Reinit - 2 objets enelves");
        numQuestion = 0;
      }
      else
      {
        // On attend que le visiteur repose un objet sur le plot 1 pour agir en conséquence
        // mais on sauvegarde l'objet qui a été soulevé
        println("Objet 1 enelvé");
        enAttenteDeReponse = 1;
      }
    }
    else if (duo2Activated == false)
    {
      // On attend que le visiteur repose un objet sur le plot 2 pour agir en conséquence
      println("Objet 2 enlevé");
      enAttenteDeReponse = 2;
    }
  }
  // Si c'est la question 2 (la dernière question), il faut afficher la page de statistiques
  if (numQuestion == 3)
  {
    println("On affiche les stats de fin");
    nbDuelsTermines += 1;
    textSize(32);
    text("Nombre de duels achevés à Lezoux : " + nbDuelsTermines, 10, 30);
    text("Nombre total de duels : " + nbDuels, 10, 60);
    text("Implication du chien de Titos et de son potier : " + presenceObjet[0]/nbDuels + " %", 10, 90);
    text("Implication du gobelet et de son potier : " + presenceObjet[1]/nbDuels + " %", 10, 90);
    text("Implication de l'objet de Fabre et de son potier : " + presenceObjet[2]/nbDuels + " %", 10, 90);
    numQuestion = 0;
  }
}

void draw()
{
  background(0);
  if (isFilmEnCours == false)
  {
    ecouteDesActionsDuVisiteur();
  }
  else
  {
    filmEnCours.read();
    image(filmEnCours,0,0);
    if (filmEnCours.time() == filmEnCours.duration())
    {
      filmEnCours.stop();
      isFilmEnCours = false;
    }
  }
}



void keyPressed()
{
  println(keyCode);
  for (int i = 0; i < nbKeys; i++)
  {
    if (keyCode == v[i])
    {
      keys[i] = true;
      if (i < nbObjets)
      {
        duo1Activated = true;
        obj[0] = i % nbObjets;
      }
      else
      {
        duo2Activated = true;
        obj[1] = i % nbObjets;
      }
      break;
    }
  }
}

void keyReleased()
{
  // Identify which key was released
  println("Key released");
  println(keyCode);
  for (int i = 0; i < nbKeys; i++)
  {
    if (keyCode == v[i])
    {
      keys[i] = false;
      if (i < nbObjets)
      {
        duo1Activated = false;
      }
      else
      {
        duo2Activated = false;
      }
      numObjReponse = i % nbObjets ;
      break;
    }
  }
  println(numObjReponse);
} 
