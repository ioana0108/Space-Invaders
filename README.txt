Prezentare in mare a programului:

Programul vrea sa fie un joc in care player-ul
se misca stanga-dreapta cu A si D si poate lansa
obiecte cu tasta SPACE. Obiectele care se misca
vertical de sus in jos reprezinta inamicii pe care
player-ul trebuie sa ii loveasca apasand tasta
SPACE ca sa emita obiectul "proiectil". Dupa 
coliziune, ambele obiecte-inamicul si proiectilul-
dispar.
Inamicii emit aleatoriu obiecte - rachete. E
suficient ca o racheta sau un inamic sa atinga 
player-ul o singura data si jocul se incheie.
De asemenea, se termina si daca 3 inamici ies din 
ecran fara sa fie impuscati.
La inceputul jocului, deasupra player-ului sunt
3 obiecte imobile (bunkere) care "protejeaza"
player-ul daca sta sub ele. La coliziunea cu 
inamicii sau rachetele lor bunker-ul isi pierde 
din "sanatate", iar obiectele care au cauzat 
coliziunea dispar.
Bunkerele dispar cand "sananatea" lor e 0.



Despre implementare:

#1 La inceputul programului am setat dimensiunile
ferestrei de joc.
   Am denumit fereastra WIN.

#2 am initializat culorile pe care urmeaza sa le 
atribui obiectelor jocului

#3 am creat clasele obiectelor din joc:
	- Ship - pentru player
	- Projectile - pentru proiectil
	- Enemy pentru inamici
	- EnemyRocket pentru rachetele inamicilor
	- Bunker - pentru bunkere

   In fiecare dintre aceste clase am setat
caracteristicile obiectului, am definit coordonatele 
(x,y) ale obiectului, am creat functia draw() #4 
pentru a le desena si (optional) functia move() 
pentru obiectele mobile.

#5 in functia def main() se intampla jocul.

   am definit functia redraw_window() #6 ca sa 
afisez pe ecran obiectele definite anterior in
clase.

   while run #7
	- verific daca tastele A si D au fost 
apasate si, daca da, misc player-ul stanga sau 
dreapta, modificand pozitia sa cu - sau, respectiv,
+ viteza cu care am setat sa se miste player-ul (#9)

	- verific daca tasta SPACE a fost apasata
si daca da, atunci generez proiectilul din mijlocul
player-ului apeland clasa proiectilului intr-o
variabila "proiectil". Totodata, verific si daca
proiectilul "e gata de lansare" inainte sa-l 
generez #10, pentru ca altfel nu ar exista niciun
spatiu intre proiectile si le-ar aparea ca o
linie continua. Am implementat o functie
ready_to_launch() in clasa Projectile #11, in
care am pus conditia ca proictilul precedent sa fi
parcurs o distanta egala cu o treime de ecran 
inainte de a fi generat urmatorul proiectil. Odata
generat, proiectilul este adaugat intr-o lista de
proiectile. #10 - a 2-a instructiune

	- parcurg lista de proiectile #12 si 
apelez functia move() din clasa Projectile pentru
a le face sa se miste vertical independent. Daca
proiectilul a iesit din ecran va fi eliminat din 
lista. #21
Verific apoi coliziunea cu cele 3 bunkere, iar 
daca proiectilul loveste bunker-ul, bunker-ul isi
pierde din sanatate, iar proiectilul dispare la
coliziune. Verfic si coliziunea cu inamicii #13
si daca proiectilul loveste un inamic, ambele
obiecte dispar.

	- #14 generez inamicii apeland clasa
Enemy in pozitii distincte folosind functia
default random.randrange() cu biblioteca random.
Vreau ca inamicii sa vina in "valuri" fiecare val
avand un inamic in plus fata de precedentul.
Generez inamici noi doar daca lista de inamici e
goala, adica daca valul curent de inamici s-a 
terminat. Apelez functia move() din clasa Enemy
pentru fiecare obiect enemy generat ca sa se miste
independent #15. Daca inamicul a iesit din ecran, 
este eliminata din lista. #20
Si aici verific coliziunea cu bunkerele #16 si cu 
player-ul. Daca enemy se loveste de bunker, 
acestuia ii scade sanatatea, iar inamicul dispare.
Daca enemy se loveste de player jocul se incheie 
instant. Variabila enemy.HITPOINT_PLAYER devine 0 
atunci cand inamicul loveste player-ul.

	- #17 generez rachetele lansate de inamici.
Apelez clasa corespunzatoare rachetelor inamice si
parcurg lista de inamici astfel incat sub fiecare
inamic sa apara un obiect racheta care va fi
adaugat in lista de rachete inamice. Parcurgand
lista de rachete inamice #18, apelez si aici
functia move() din clasa EnemyRocket si le dau
o viteza (enemy_rocket_vel #19) mai mare decat
a inamicilor sub care sunt generate ca sa para ca
sunt lansate de inamici. Daca racheta a iesit din
ecran, este eliminata din lista. #20
Apoi verific coliziunea cu bunkerele si player-ul. 
In primul caz, racheta inamica dispare iar 
bunker-ului pe care l-a lovit ii scade sanatatea,
iar in al doilea jocul se incheie.























