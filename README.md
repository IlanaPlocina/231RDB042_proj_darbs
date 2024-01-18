### Projekta vispārējais **mērķis** ir automatizēt vakanču meklēšanu cvmarket.lv vietnē, datu apstrādi un nodrošināt lietotājam ērtu vakanču saraksta izvešanu, attiecībā uz lietotāja pieprasījumiem un prasībām.
_______
## Projekta uzdevumu apraksts
+ Uzsākot programmu, lietotājam tiek dota iespēja ērti ievadīt savas prasības. Process sākas ar informācijas pieprasīšanu par vietu, kur viņš plāno sākt savu karjeru - vai tā būtu pilsēta, rajons vai konkrēta vieta. Tas ļauj uzzināt viņa preferences un sašaurināt vakanču meklēšanu līdz konkrētai lokācijai.
+ Tālāk, būtisks moments ir noteikt lietotāja studenta statusu. Ja atbilde ir pozitīva, tad ievade tiek pabeigta un programma pāriet uz nākamo posmu. Gadījumā, ja lietotājs nav students, tiek dota iespēja precizēt preferences attiecībā uz nodarbinātības režīmu: pilna nodarbinātība vai nepilna.
Šī pieeja datu ievadīšanai piešķir projektam elastību un personalizāciju, ļaujot pielāgoties meklēšanai konkrētām lietotāja vajadzībām. Turklāt tas nodrošina precīzāku vakanču analīzi un tā pieprasījumiem atbilstošu rezultātu izsniegšanu. 

+ Atlasot vietu tīmekļa lapā, programma veic svarīgu uzdevumu, lai noteiktu lietotāja ievadīto vietas ID.
Programma atver vietas_exel.xlsx failu, kurā ir informācija par dažādām darba vietām (kas ir pieejamas mājas lapā cvmarket.lv) un to atbilstošajiem identifikatoriem (ID).
Pēc tam, kad lietotājs ir ievadījis vēlamo atrašanās vietu, programma Excel failā analizē rindas, meklējot precīzu atbilstību ievadītajai atrašanās vietai (meklēšana notiek pēc pirmās kolonnas, kur atrodas reģionu un pilsētu nosaukumi). Kad atbilstība ir atrasta, programma izgūst un saglabā atbilstošo vietas ID (piemērām, jā ievadīta vieta bija Rīga, tad ID būs -  search[locations][]_1). Identifikators ir unikāls kods, proti, pogas ID, kas identificē konkrētu vietu cvmarket.lv vietnē. 

+ Svarīgs aspekts ir rezultātu kārtošana pēc publicēšanas datuma. Programma nodrošina, ka vakances tiek kārtoti to aktualitātes secībā, kas ļauj lietotājiem iegūt svaigu un aktuālu informāciju.
Izmantojot Selenium bibliotēku, programma parsē meklēšanas rezultātu lapu, iegūst informāciju par vakancēm, piemēram, virsrakstus (vakanču nosaukumus), atalgojumu un citas detaļas (atvērot konkrētas vakances lapu), kā piemēru - datumu, kad vakance bija ielādēta vietnē, darba laiku (pilna, nepilna nodarbinātība) un citu papildu informāciju. Vakanču meklēšana notiek visās pieejamās lapās, pārvietojoties pa tām. Katra vakance tiek uzskatīta par atsevišķu elementu, kas ļauj detalizētāk analizēt un strukturēt iegūtos datus. 

+ Pēc veiksmīgas informācijas vākšanas par vakancēm tīmekļa lapā programma pāriet uz šo datu saglabāšanu ērtā Excel formātā. Tas tiek darīts, izmantojot Pandas bibliotēku. 
Programma veido divus DataFrame. Pirmais ir izveidots vakanču virsrakstiem - satur pamatinformāciju, kā vakances nosaukumus. Katra rinda attēlo vienu vakanci, ģenerējot pirmo kolonnu Excel failā. Otrais ir piemērots papildu informācijai. Tā ietver dažādus vakanču parametrus – vakances ievadīšanas datums, līdz kuram datumam vakance ir aktuāla, atrašanas vieta, bruto alga, darba laiks un papildus informācija. Katra šī DataFrame rinda atbilst tām pašām vakancēm, kas pirmajā DataFrame, un tiks parādīta kā papildu kolonnas Excel failā. Izveidojot šos DataFrame, programma tos sapludina vienā Excel failā ar nosaukumu dati_pd.xlsx.
Šis datu eksporta posms programmā Excel ne tikai saglabā meklēšanas rezultātus ērtā formātā, bet arī nodrošina lietotājiem rīku dziļākai informācijas analīzei un šķirošanai. Lietotāji turpmāk var viegli strādāt ar datiem, veikt salīdzinājumus.

+ Saglabājot informāciju par vakancēm failā dati_pd.xlsx, programma atver šo failu, izmantojot openpyxl bibliotēku, un pāriet pie formatējuma rediģēšanas.
Programma rediģē kolonnu izmērus, lai uzlabotu datu lasāmību. Kolonnu izmērus regulē atbilstoši datu tipam un to saturam. Kolonnas ar teksta informāciju, piemēram, “vakanču nosaukumi” un “Papildus informācija”, ir palielinātas teksta labākai redzamībai. Kamēr kolonnām ar pārējo informāciju ir uzstādīts optimālais izmērs teksta attēlošanai.
Programmatūra saglabā atjauninātu Excel failu, nodrošinot, ka lietotāji saņem darba sludinājumus lietotājam patīkamā formātā, kas uzlabo vizuālo skatījumu un ļauj ātri novērtēt galveno informāciju.

+ Filtrēšanas un rezultātu izvades posms ir programmas noslēdzošais posms, kas vērsts uz darba meklēšanas automatizāciju cvmarket.lv portālā. 
Pirmais solis ir vakanču filtrēšana:
Programma rūpīgi analizē lietotāja ievadītos kritērijus, it īpaši to, vai lietotājs ir students un kāds darba laiks ir vēlams (pilna vai nepilna darba laika). Ja lietotājs ir students, vakances tiek filtrētas, ņemot vērā iespēju strādāt saskaņā ar studenta grafiku. Tiem, kas nav studenti, programma papildus filtrē vakances, ņemot vērā norādīto vēlamo darba laiku.
Otrais solis ir rezultātu parādīšana ekrānā:
Ja pēc filtrēšanas paliek piemērotas vakances, programmatūra, izmantojot Pandas bibliotēku, izveido rezultātu tabulas veidā. Tabulā ir iekļauta svarīga informācija par vakancēm - nosaukums, publicēšanas datums, atrašanās vieta, algas līmenis, darba laiks un papildu informācija. Šie rezultāti tiek parādīti ekrānā, nodrošinot lietotājam skaidru un viegli saprotamu pārskatu par pieejamajām vakancēm, kas atbilst viņa individuālajiem kritērijiem. Izmantojot šo pieeju, lietotājiem tiek piedāvātas tikai tās darba vietas, kas vislabāk atbilst viņu prasībām un vēlmēm.
____________________________________________________________________________________________________________________________________________________________________________________________________________________
## Python bibliotēkas:
1. ***Selenium*** - tas mērķis ir automatizēt tīmekļa pārlūkprogrammu, lai strādātu ar cvmarket.lv tīmekļa lapu. Selenium ļauj mijiedarboties ar dinamisko tīmekļa lapas saturu, piemēram, pogām, veidlapām un elementiem, kas tiek ielādēti pēc koda palaišanas sākuma. Mans kods nospiež pogas, izvēlas atrašanās vietu un citas darbības, ko lietotāji parasti veic manuāli, bet Selenium ļauj šīs darbības automatizēt. Selenium man ir palīdzējis atrast tīmekļa lapas elementus, izmantojot dažādas pieejas, piemēram, ID, CSS selektorus un XPath. Es arī izmantoju WebDriverWait. Tas ļauj lietojumprogrammai gaidīt, kamēr lapā parādīsies attiecīgie elementi, pirms uzsākt mijiedarbību. Tas ir svarīgi, lai novērstu kļūdas.
2. ***Pandas*** - šo bibliotēku izmantoju, lai apstrādātu un analizētu datus par vakancēm. Bibliotēka nodrošina DataFrame, kas ir ideāli piemērots darbam ar tabulārajiem datiem. Ar tās palīdzību es varēju ievietot vajadzīgo informāciju exel tabulā nepieciešamajās kolonnās/rindās. Viena kolonna vakanču virsrakstiem un citas papildu informācijai. Tas ļauj efektīvi uzglabāt un manipulēt ar datiem. Tāpat Pandas tika izmantota rezultāta saglabāšanai failā.
3. ***Openpyxl*** - šī bibliotēka ir izveidota, lai strādātu ar Excel failiem. Openpyxl nodrošina ērtas metodes jaunu Excel failu izveidei un izmaiņu veikšanai tajos. Mans kods izmanto openpyxl, lai atvērtu, rediģētu un saglabātu Excel failu (“dati_pd.xlsx”) ar vakanču meklēšanas rezultātiem. Tāpat izmanto, lai mainītu kolonnu izmērus un saglabātu šīs izmaiņas.
4. ***Tabulate*** - šīs bibliotēkas mērķis ir parādīt datus tabulveida formā. Ar tās palīdzību veidoju tabulu ar vakanču meklēšanas rezultātiem un šo datu pārvēršanu formātā, kuru viegli uztver cilvēks (tabulas veidā).
5. ***Time*** - kodā tā atbild par kodu pagaidu aizkaves pārvaldību, lai nerastos kļūdas, lasot un izpildot uzdevumus.
____________________________________________________________________________________________________________________________________________________________________________________________________________________
## Programmatūras izmantošanas metodes:
Programma var noderēt plašam cilvēku lokam:
1. Cilvēki, kuri aktīvi meklē jaunas vakances un vēlas automatizēt meklēšanas procesu noteiktā vietā.
2. Studenti, kuri meklē darbu, ņemot vērā savu studenta statusu un vēlamo darba laiku.
3. Darba devēji, kas meklē kandidātus noteiktai lokācijai, var izmantot manu programmu, lai izsekotu vakancēm noteiktā reģionā.
4. Karjeras konsultāciju speciālisti var izmantot manu programmu, lai sniegtu klientiem informāciju par pieejamām vakancēm konkrētās vietās un ar konkrētiem pieprasījumiem.