//ecran 15" 4/3 = 229mm x 305mm
//plus cadre ~~ 260x335

//ecran 15" 16/9 = 187mm x 332mm
//plus cadre ~~ 210x360
//ok

l_e=379; // largeur ext écran mm
jeu= 7;//jeu de chaque coté mm

pp= 400; // profondeur caisse mm

t1=21; // largeur tasseau 1 (carre)
t1l=21;

t2=13;

p1l=28; //l planche1
p1h=13;//h planche1

p2h=21;//h planche1
p2l=34; //l planche1

t3=21;
t3l=70;

ll=l_e+2*jeu+2*t1; //largeur ext structure
echo("ll",ll);


ee=10; //epaisseur plateau milieu

ee_couv=5;

jj=400;
kk=120; // hteur dessous
hh=jj+kk; // hteur
hh2=hh+p1h+t1+ee+ee; //

echo("hh2",hh2);

ii=5; //e. placage

*color("grey") cube([ll,pp,ee]);


color("plum") {
    translate([0,0,hh-t1l+ee]){
        translate([t1,0,0])
        cube([ll-2*t1,t1,t1l]);
        translate([t1,pp-t1,0])
        cube([ll-2*t1,t1,t1l]);
    }}
color("magenta") {
    translate([0,0,hh-t1+ee]){
        translate([0,t1l,t1-p2l])
        cube([p2h,pp-2*t1l,p2l]);
        translate([ll-t1,t1l,t1-p2l])
        cube([p2h,pp-2*t1l,p2l]);
    }}

// pour les poignées si assez leger
color("magenta") {
    translate([0,0,(hh-t1+ee)/2]){
        translate([0,t1l,t1-p2l])
        cube([p2h,pp-2*t1l,p2l]);
        translate([ll-t1,t1l,t1-p2l])
        cube([p2h,pp-2*t1l,p2l]);
    }}

color("green") {
    translate([0,0,ee]){
        translate([0,0,0])
        cube([t1,t1l,hh]);
        translate([ll-t1,0,0])
        cube([t1,t1l,hh]);
        translate([0,pp-t1l,0])
        cube([t1,t1l,hh]);
        translate([ll-t1,pp-t1l,0])
        cube([t1,t1l,hh]);
    }}
color("magenta") {
    translate([0,0,ee]){
        translate([0,t1l,0])
        cube([t3,pp-2*t1l,t3l]);
        translate([ll-t1,t1l,0])
        cube([t3,pp-2*t1l,t3l]);
    }}
color("plum") {
    translate([0,0,ee]){
        translate([t1,pp-t1,0])
        cube([ll-2*t1,t1,t1l]);
    }}
// planches sur le cadre

color("orange"){
    translate([0,0,hh+ee]){
        translate([jeu,0,0])
        cube([p1l,pp,p1h]);
        translate([ll-p1l-jeu,0,0])
        cube([p1l,pp,p1h]);
    }}
// couvercle

color("yellow",0.6) {
    translate([0,0,hh+ee+p1h]){
        translate([0,0,0])
        cube([t2,pp,t2]);
        translate([ll-t2,0,0])
        cube([t2,pp,t2]);
        translate([t2,0,0])
        cube([ll-2*t2,t2,t2]);
        translate([t2,pp-t2,0])
        cube([ll-2*t2,t2,t2]);
        translate([0,0,t2])
        cube([ll,pp,ee_couv]);
    }}

//middle
color("plum") {
    translate([0,0,kk-t1l-ee]){
        translate([0,t1l,0])
        cube([t1,pp-2*t1l,t1l]);
        translate([ll-t1,t1l,0])
        cube([t1,pp-2*t1l,t1l]);
    }}
color("grey",0.7){
    translate([0,0,kk-p2l-ee]){
        union(){
    //    translate([t1,0,p2l])
    //    cube([ll-2*t1,pp,ee]);
            translate([0,t1,p2l])
            cube([ll,pp-2*t1,ee]);
    }}}
color("blue",0.8) {
    translate([0,0,kk-p2l-ee-ee]){
        translate([t1,0,p2l+ee/2-t1/2])
        cube([ll-2*t1,t1,t1]);
    }}

// placage
*color("tan",0.8){
    translate([-ii,0,0])
    cube([ii,pp,hh2]);
    translate([ll,0,0])
    cube([ii,pp,hh2]);
}
//arriere
*translate([-ii,pp,0])
color("pink") cube([ll+2*ii,ii,hh2]);

//tiroir
{
e_coulisse=10;
p_coulisse=350;
h_coulisse=10;
h_ss_plancher=10;
*color("red",0.8){
    translate([t1+e_coulisse,0,ee+h_coulisse])
    cube([ll-2*t1-2*e_coulisse,p_coulisse,kk-3*ee-h_coulisse-h_ss_plancher]);
    translate([-ii,-ii,0])
    cube([ll+2*ii,ii,kk-2*ee-h_ss_plancher]);
}
}

//devant
{
color("pink")
*union(){
    h_cache=60;
    translate([-ii,-ii,hh-h_cache])
    cube([ll+2*ii,ii,h_cache-hh+hh2]);
    //devant bas
    h_cache_b=20;
    translate([-ii,-ii,kk-2*ee-h_ss_plancher])
    cube([ll+2*ii,ii,h_cache_b-hh+hh2]);
    //
    cote=25;
    translate([-ii,-ii,kk-2*ee-h_ss_plancher+h_cache_b-hh+hh2])
    cube([cote+ii,ii,jj-h_cache+hh-hh2+ii]);
    translate([ll-cote,-ii,kk-2*ee-h_ss_plancher+h_cache_b-hh+hh2])
    cube([cote+ii,ii,jj-h_cache+hh-hh2+ii]);
    }
}

