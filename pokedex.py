# Source PokeDex Site
#     https://pokemondb.net/pokedex/{{__id__}}
# usage;
#    python pokedex.py bulbasaur

from bs4 import BeautifulSoup
import requests
from sys import argv
choosen = argv[1]
r = requests.get('https://pokemondb.net/pokedex/'+str(choosen))
source = BeautifulSoup(r.content, "html.parser")

pokemon = {}
pokemon['Pokedex Data']    = {}
pokemon['Training']        = {}
pokemon['Breeding']        = {}
pokemon['Base stats']      = {}
pokemon['Type defenses']   = {}
pokemon['Pokedex Entries'] = {}

# POKEDEX DATA
# Name
pokemon['Pokedex Data']['Name'] = source.find("h1").text

# Description
pokemon['Pokedex Data']['Description'] = source.find("div", attrs={"class", "grid-col span-md-6 span-lg-8"}).text

# Image
# img tag parse process
image = source.find("div", attrs={"class", "grid-col span-md-6 span-lg-4 text-center"}).contents[1]
image = BeautifulSoup(str(image), "html.parser")
image = image.find("img").get("src")
pokemon['Pokedex Data']['image'] = image

# Vitals
# Vital Table parse process
allTables = source.find_all("table", attrs={"class", "vitals-table"})
vitals = BeautifulSoup(str(allTables[0]),"html.parser")

# National No
pokemon['Pokedex Data']['National No'] = str(vitals.find_all("td")[0].text)

# Type
types = vitals.find_all("td")[1].text[1:].strip()
types = types.split(" ")
pokemon['Pokedex Data']['Type'] = ""
for typ in types:
    pokemon['Pokedex Data']['Type'] += ", "+typ
pokemon['Pokedex Data']['Type'] = pokemon['Pokedex Data']['Type'][2:]

# Species
pokemon['Pokedex Data']['Species'] = vitals.find_all("td")[2].text

# Height
pokemon['Pokedex Data']['Height'] = vitals.find_all("td")[3].text

# Weight
pokemon['Pokedex Data']['Weight'] = vitals.find_all("td")[4].text

# Abilities
# abilities parse process
abilities = vitals.find_all("td")[5]
abilities = BeautifulSoup(str(abilities), "html.parser")
pokemon['Pokedex Data']['Abilities']=""
for abi in abilities.find_all("a"):
    pokemon['Pokedex Data']['Abilities']+=", "+abi.text
pokemon['Pokedex Data']['Abilities']=pokemon['Pokedex Data']['Abilities'][2:]

# Local No
pokemon['Pokedex Data']['Local No'] = ""
local_nos = vitals.find_all("td")[6].text.split(")")[:-1]
for loc in local_nos:
    pokemon['Pokedex Data']['Local No'] += "\n"+loc+str(")")
pokemon['Pokedex Data']['Local No'] = pokemon['Pokedex Data']['Local No'][1:]

# Japanese Name
pokemon['Pokedex Data']['Japanese Name'] = vitals.find_all("td")[7].text

# TRAINING
training = BeautifulSoup(str(allTables[1]),"html.parser")
# EV Yield
pokemon['Training']['EV Yield'] = training.find_all("td")[0].text[1:].strip()

# Catch rate
pokemon['Training']['Catch Rate'] = training.find_all("td")[1].text

# Base happiness
pokemon['Training']['Base Happiness'] = training.find_all("td")[2].text

# Base EXP
pokemon['Training']['Base EXP'] = training.find_all("td")[3].text

# Growth Rate
pokemon['Training']['Growth Rate'] = training.find_all("td")[4].text

# BREEDING
breeding = BeautifulSoup(str(allTables[2]),"html.parser")
# Egg Groups
pokemon['Breeding']['Egg Groups'] = breeding.find_all("td")[0].text[1:].strip()
# Gender
pokemon['Breeding']['Gender'] = breeding.find_all("td")[1].text
# Egg cycles
pokemon['Breeding']['Egg cycles'] = breeding.find_all("td")[2].text[:-1]

# BASE STATS
base_stats = BeautifulSoup(str(allTables[3]),"html.parser")
# HP : BASE/MIN/MAX
pokemon['Base stats']['HP'] = base_stats.find_all("td")[0].text+"/"+base_stats.find_all("td")[2].text+"/"+base_stats.find_all("td")[3].text
# Attack : BASE/MIN/MAX
pokemon['Base stats']['Attack'] = base_stats.find_all("td")[4].text+"/"+base_stats.find_all("td")[6].text+"/"+base_stats.find_all("td")[7].text
# Defense : BASE/MIN/MAX
pokemon['Base stats']['Defense'] = base_stats.find_all("td")[8].text+"/"+base_stats.find_all("td")[10].text+"/"+base_stats.find_all("td")[11].text
# Sp.Attack : BASE/MIN/MAX
pokemon['Base stats']['Sp. Attack'] = base_stats.find_all("td")[12].text+"/"+base_stats.find_all("td")[14].text+"/"+base_stats.find_all("td")[15].text
# Sp.Defense : BASE/MIN/MAX
pokemon['Base stats']['Sp. Defense'] = base_stats.find_all("td")[16].text+"/"+base_stats.find_all("td")[18].text+"/"+base_stats.find_all("td")[19].text
# Speed : BASE/MIN/MAX
pokemon['Base stats']['Speed'] = base_stats.find_all("td")[20].text+"/"+base_stats.find_all("td")[22].text+"/"+base_stats.find_all("td")[23].text
# Total : BASE
pokemon['Base stats']['Total'] = base_stats.find_all("td")[24].text
# Description
pokemon['Base stats']['Description'] = source.find("p", attrs={"class", "text-small text-muted"}).text

# TYPE DEFENSES
type_defenses = source.find_all("div", attrs={"class", "grid-col span-md-12 span-lg-4"})[1] 
type_defenses = BeautifulSoup(str(type_defenses), "html.parser")
# Description
pokemon['Type defenses']['Description'] = type_defenses.p.text
types_defs = []
for typ in type_defenses.find_all("th"):
    typ = BeautifulSoup(str(typ), "html.parser")
    typ = typ.find("a")
    types_defs.append(typ['title'])

types_vals = []
for val in type_defenses.find_all("td"):
    types_vals.append(val.text)

i=0
for typ_def in types_defs:
    pokemon['Type defenses'][typ_def]=types_vals[i]
    if(pokemon['Type defenses'][typ_def]==""):
        pokemon['Type defenses'][typ_def]="0"
    i+=1

allTables = source.find_all("table", attrs={"class", "vitals-table"})
entries = BeautifulSoup(str(allTables[4]),"html.parser")

entrie_title = []
for entrie in entries.find_all("tr"):
    entrie = BeautifulSoup(str(entrie),"html.parser")
    entrie = entrie.find_all("span")
    entriTitleTemp=""
    for entri in entrie:
        entriTitleTemp += ", "+str(entri.text)
    entriTitleTemp = entriTitleTemp[2:]
    entrie_title.append(entriTitleTemp)

entrie_content = []
for entrie in entries.find_all("tr"):
    entrie_content.append(entrie.td.text)

i=0
for titl in entrie_title:
    pokemon['Pokedex Entries'][titl]=entrie_content[i]
    i+=1

# Print Pokedex Data
print("\t==== POKEDEX DATA ====")
print("\tName : "+str(pokemon['Pokedex Data']['Name']))
print("\tJapanese Name : "+str(pokemon['Pokedex Data']['Japanese Name']))
print("\tImage URL : "+str(pokemon['Pokedex Data']['image']))
print("\tNational No : "+str(pokemon['Pokedex Data']['National No']))
print("\tType : "+str(pokemon['Pokedex Data']['Type']))
print("\tSpecies : "+str(pokemon['Pokedex Data']['Species']))
print("\tHeight : "+str(pokemon['Pokedex Data']['Height']))
print("\tWeight : "+str(pokemon['Pokedex Data']['Weight']))
print("\tAbilities : "+str(pokemon['Pokedex Data']['Abilities']))
print("\tLocal No : \n"+str(pokemon['Pokedex Data']['Local No']))

# Print Training
print("")

# Print Type defenses
print("\t==== TYPE DEFENSES ====")
print("\t"+str(pokemon['Type defenses']['Description']))
for typ in pokemon['Type defenses'].keys():
    if(typ!="Description"):
        print("\t%s : %s"%(typ,pokemon['Type defenses'][typ]))

# Print Pokedex Entries
print("\t==== POKEDEX ENTRIES ====")
for entr in pokemon['Pokedex Entries'].keys():
    print("\t%s\n\t\t%s\n"%(entr,pokemon['Pokedex Entries'][entr]))
