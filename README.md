-
# stacc-challenge
Making budgeting and saving fun!

## Kort om prosjektet
Idéen var å lage en app som skal oppfordre til budsjettering/pengesparing. Her bygger jeg litt videre på en liknende oppgave vi har holdt på med i et HCI-emne på universitetet, hvor ideen var noe lik, men med et hovedfokus på å spare miljøet, ikke penger. Tanken var å bruke gamification som virkemiddel, og gi brukeren "challenges" som skal gjennomføres. Reward-aspektet kommer i form av XP, visuell tilbakemelding og, naturligvis, penger spart. Brukeren kan signe opp og tanken er at man skal kunne se aktiviteten til sine "venner", og da dele med hverandre, samtidig som man kanskje sammenlikner seg med andre. Du vil også kunne sette deg mål for noe du sparer til.  
Med tanke på hvor kort frist vi fikk her, måtte jeg gå videre fra det som kanskje er mest viktig når man skal gjøre et prosjekt som dette, nemlig forarbeid. Allikevel gjorde jeg et forsøk og hoppet inn i det, og fikk med det prøvd meg ut både i Back-End og Front-End.

## Figma
Første steget var egentlig å legge fram en low-fidelity prototype, så jeg vet sånn ish hva jeg vil oppnå. Her hentet jeg litt inspirasjon fra en prototype vi har jobbet med i HCI-emnet, og slang sammen det som ligger i [figma-mappen](/figma).

## Flask, MySQL
Videre tenkte jeg egentlig å starte med det som ligger bak et sånt system. Jeg begynte med å sette opp Flask med SQL, da dette er det jeg har vært borti gjennom emner om systemutvikling og datahåndtering. Når jeg fikk ting til å gå, begynte jeg å sette opp litt enkle klasser/tabeller, som holder på f. eks. brukerinformasjon og challenges, og noen ruter som lar deg plotte inn i enkle tekstbokser. Her prøvde jeg meg bare litt fram, har jo nærmest ingen erfaring i Back-End, så det var gøy å få litt nye inntrykk, og få lært noe helt nytt.  
Dette var ikke noe jeg tenkte på når jeg satt i gang, men det er jo kanskje ikke så lett å levere en SQL server. Her vet jeg ikke om dere tar dere bryet til å prøve å få det til å kjøre, men jeg legger ved en [requirements.txt](/stacc/requirements.txt) fra pip som inneholder plugins, og [litt informasjon](https://github.com/panrasch/stacc-challenge/edit/main/README.md#bruksanvisning-til-flask-og-mysql) om hvordan man eventuelt kan få det til å kjøre. Kan nok være en idé å bare kikke på koden i stedet for å prøve å få alt til å kjøre. Det funker hvert fall. Sånn ca.

## React, Chart.js
Til slutt ville jeg teste ut litt i Front-End sammenheng. Har lenge hatt lyst til å lære meg mer JavaScript, og React passet bra som rammeverk. Her brukte jeg react-chartjs-2 med chart.js og tenkte jeg skulle prøve meg på litt forskjellige grafer. Endte opp med å lage litt diverse, og planen var å bruke disse i appen, under en side for statistikk. Den kumulative area charten viser utgifter og inntekter over en gitt tidsperiode (startDate -> endDate). Her er summene for hver dato lagt sammen og summert opp kumulativt over tid. Denne kan da representere ukentlig, månedlig, årlig forbruk og inntekt. Deretter lagde jeg akkumulative grafer for inntekt og utgift separat, også over en gitt tidsperiode, som viser daglig forbruk/inntekt akkumulativt. Til sist har jeg en radar chart som viser forbruk over en gitt tidsperiode, kategorisert i "descriptions". Foreløpig er ikke disse implementert til å kategorisere etter "account_id", så den fungerer som en dummy på hvordan jeg egentlig ville hatt det. Fikk rett og slett ikke tid til mer :p 

## Videre prosess
Jeg var godt klar over når jeg begynte at jeg aldri i verden rekker å implementere en fullfunksjonell app, så jeg tok heller en approach hvor jeg fikk testet ut og lagd forskjellige komponenter som går inn i en app. Kan jo nevne at jeg definitivt syntes front-end biten var mest interessant. Skulle jeg fortsette med dette prosjektet, må naturligvis back-end databasene jobbes mye med. Her er det ikke veldig mye funksjonalitet ennå, kun enkle komponenter som en begynnelse på et bruker-system, og samme for challenge-systemet. Videre må naturligvis appen implementeres som en app, for eksempel i Swift, om jeg skulle lage en native iOS app. Ikke noe jeg har lagt mye tanke i her, da jeg egentlig visste at jeg ikke kom til å få tid til å begynne med dette.  
En ting jeg skulle ønske jeg fikk tid til er å implementere en maskinlæringsalgoritme, og trene den på [transactions](/stacc/transactions.json)-datasettet. Kan ikke si meg noe ekspert på maskinlæring, men det er noe jeg har jobbet litt med i "Methods in Artificial Intelligence"-emnet dette semesteret. Problemet igjen var rett og slett at jeg ikke fikk tid, men jeg slet også med å finne ut hva slags target variabel jeg skulle ha siktet for. Kanskje en modell som ser på utgifter og inntekter over tid og kan predicte en dato hvor du vil ha råd til et bestemt mål? Ny motorsykkel, for eksempel...  
Det får ligge til neste gang, uansett vært noen veldig lærerike dager :)

# Figma prototype
Ligger [her](/figma).

# React, Chart.js
Denne biten har jeg gjort i [CodeSandbox](https://codesandbox.io/), som gjør det veldig enkelt å følge [denne lenken](https://codesandbox.io/s/sad-grass-7dyyws) og inspisere koden, med direkte visualisering.

# Bruksanvisning til Flask og mySQL
## requirements.txt
I [requirements-filen](/stacc/requirements.txt), ligger alle Python extensions som er brukt. Jeg jobbet i et venv, så det skal ikke være mer eller mindre som trengs. Her har jeg brukt pip. Pass på at alt er installert og at man er i riktig interpreter.
## config av Flask
Deretter må en MySQL server settes opp. [MySQL](https://dev.mysql.com/downloads/mysql/) må installeres (her måtte jeg bruke 8.0.34, fikk problemer med 8.1).  Serveren satt jeg opp i [MySQLWorkbench](https://dev.mysql.com/downloads/workbench/), queryen for å lage databasen ligger i [stacc.sql](/stacc/stacc.sql) scriptet.  
Her er det viktig at serveren settes opp med riktige credentials:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/stacc'
```  
Da er brukernavn: ```root ```  
Passord: ```admin```  
Servernavn: ```stacc```  
Dette kan selvfølgelig endres på, men da må config linjen endres henholdsvis.  
Når alt er satt opp, kan man kjøre linjen ```db.create_all()``` for å opprette klassene i Python som tabeller i SQL. Dette må gjøres i Python, og her er det mulig man må kjøre linjen i app kontekst. Viktig her å være i samme directory som [app.py](/stacc/app.py). I Python-terminal:
```python
with app.app_context():
...db.create_all()
mellomrom -> enter
```  
Deretter skal man kunne kjøre ```flask run``` og åpne nettsiden [her](http://localhost:5000/) eller [her](http://127.0.0.1:5000/). Igjen viktig å være i riktig directory.  
Rutene ligger i [app.py](/stacc/app.py) filen:  
[/users](http://127.0.0.1:5000/users) gir en liste over brukere  
[/challenges](http://127.0.0.1:5000/challenges) gir en liste over challenges  
[/transactions](http://127.0.0.1:5000/transactions) gir en liste over transactions  
[/users/add](http://127.0.0.1:5000/users/add) lar deg opprette en ny bruker  
[/challenges/add](http://127.0.0.1:5000/challenges/add) lar deg opprette en ny challenge  
[/transactions/add](http://127.0.0.1:5000/transactions/add) lar deg opprette en ny transaction  
Mer informasjon i [app.py](https://github.com/panrasch/stacc-challenge/blob/main/stacc/app.py)
