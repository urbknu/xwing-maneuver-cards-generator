# -*- coding: utf-8 -*-
import sys
import json
import requests
import os
import shutil

'''
X-Wing 2.0 Maneuver cards for those of us who have difficulty remembering all the maneuvers

Ship images and general rights: © and ™ Lucasfilm Ltd. & Fantasy Flight Games
Cards are automatically generated using X-Wing2 Data: https://github.com/guidokessels/xwing-data2
Icon and Ship Fonts: https://github.com/geordanr/xwing-miniatures-font
Template starting point: https://www.deviantart.com/odanan/art/X-Wing-2nd-Ed-Template-v2-748403857
'''

# Debugging
sys.stderr = open("\\".join(sys.argv[0].split("\\")[0:-1]) + '\\xwing2maneuvercardgenerator-debugging.txt','a')
sys.stdout=sys.stderr # So that they both go to the same file

from gimpfu import *

version = 0.9
ship_ability_icons = {
    "[Lock]":"l",
    "[Attack]":"%",
    "[Hit]":"d",
    "[Critical Hit]":"c",
    "[Link]":">",
    "[Bank Left]":"7",
    "[Straight]":"8",
    "[Bank Right]":"9",
    "[Barrel Roll]":"r",
    "[Boost]":"b",
    "[Evade]":"e",
    "[Cloak]":"k",
    "[Evade Token]":"é",
    "[Cloak Token]":"ô",
    "[Device]":"B",
    "[Cannon]":"C",
    "[Torpedo]":"P",
    "[Missile]":"M",
    "[Rotate Arc]":"R",
    "[Single Turret Arc]":"p",
    "[Front Arc]":"{",
    "[Rear Arc]":"|",
    "[Tractor Token]":"ï",
    "[Agility]":"^",
    "[Calculate Token]":"Ë",
    "[Coordinate]":"o",
    "[Turret]":"U",
    "[Force Charge]":"h",
    "[Bullseye Arc]":"}",
    "[Focus]":"f",
    "[Calculate]":"a",
    "[Charge]":"g"
}
ships = {
  'Galactic Empire': {
    'tieadvancedx1': {
      'shipability': {
        'text': 'Primary[Attack] › [Lock]: +1[Attack] & 1[Hit]=[Critical Hit]',
        'name': 'Advanced Targeting Computer'
      },
      'name': 'TIE Advanced x1',
      'icon': 'A'
    },
    'tieskstriker': {
      'shipability': {
        'text': 'B-4 dial reveal & not stressed: exec 1[Bank Left]/[Straight]/[Bank Right]',
        'name': 'Adaptive Ailerons'
      },
      'name': 'TIE/sk Striker',
      'alt_name': 'TIE Striker',
      'icon': 'T'
    },
    'tieddefender': {
      'shipability': {
        'text': 'Fully executed 3-5 maneuver [Link] [Evade]',
        'name': 'Full Throttle'
      },
      'name': 'TIE/D Defender',
      'alt_name': 'TIE Defender',
      'icon': 'D'
    },
    'tieininterceptor': {
      'shipability': {
        'text': 'Action [Link] {actionred}[Barrel Roll]/{actionred}[Boost]',
        'name': 'Autothrusters'

      },
      'name': 'TIE/in Interceptor',
      'alt_name': 'TIE Interceptor',
      'icon': 'I'
    },
    'tiephphantom': {
      'shipability': {
        'text': 'After de-[Cloak]: [Evade]. End Phase: 1[Evade Token] = 1[Cloak Token]',
        'name': 'Stygium Array'
      },
      'name': 'TIE/ph Phantom',
      'alt_name': 'TIE Phantom',
      'icon': 'P'
    },
    'tielnfighter': {
      'name': 'TIE/ln Fighter',
      'alt_name': 'TIE Fighter',
      'icon': 'F'
    },
    'tiesabomber': {
      'shipability': {
        'text': 'May use [Bank Left][Bank Right], instead of [Straight], when dropping [Device]',
        'name': 'Nimble Bomber'
      },
      'name': 'TIE/sa Bomber',
      'alt_name': 'TIE Bomber',
      'icon': 'B'
    },
    'tieadvancedv1': {
      'name': 'TIE Advanced v1',
      'icon': 'R'
    },
    'tiereaper': {
      'shipability': {
        'text': 'B-4 dial reveal & not stressed: exec 1[Bank Left]/[Straight]/[Bank Right]',
        'name': 'Adaptive Ailerons'
      },
      'name': 'TIE Reaper',
      'icon': 'V'
    },
    'tiecapunisher': {
      'name': 'TIE/ca Punisher',
      'alt_name': 'TIE Punisher',
      'icon': 'N'
    },
    'tieagaggressor': {
      'name': 'TIE/ag Aggressor',
      'alt_name': 'TIE Aggressor',
      'icon': '`'
    },
    'vt49decimator': {
      'alt_name': 'Decimator',
      'name': 'VT-49 Decimator',
      'icon': 'd'
    },
    'lambdaclasst4ashuttle': {
      'alt_name': 'Lambda Shuttle',
      'name': 'Lambda-class T-4a Shuttle',
      'icon': 'l'
    },
    'alphaclassstarwing': {
      'alt_name': 'Assault Gunboat',
      'name': 'Alpha-class Star Wing',
      'icon': '&'
    }
  }, 'Resistance': {
    't70xwing': {
      'shipability': {
        'text': 'Can equip 1[Cannon], [Torpedo] or [Missile] upgrades',
        'name': 'Weapon Hardpoint'
      },
      'name': 'T-70 X-wing',
      'alt_name': 'X-Wing',
      'icon': 'w'
    },
    'resistancetransport': {
      'alt_name': 'Transport',
      'name': 'Resistance Transport',
      'icon': '>'
    },
    'mg100starfortress': {
      'alt_name': 'Heavy bomber',
      'name': 'MG-100 StarFortress',
      'icon': 'Z'
    },
    'rz2awing': {
      'shipability': {
        'text': '[Rotate Arc][Single Turret Arc] only [Front Arc]/[Rear Arc]. Action [Link] {actionred}[Boost]/{actionred}[Rotate Arc]',
        'name': 'Refined Gyrostabilizers'
      },
      'name': 'RZ-2 A-wing',
      'alt_name': 'A-Wing',
      'icon': 'E'
    },
    'scavengedyt1300': {
      'name': 'Scavenged YT-1300',
      'alt_name': 'YT-1300',
      'icon': 'Y'
    },
    'resistancetransportpod': {
      'alt_name': 'Transport Pod',
      'name': 'Resistance Transport Pod',
      'icon': '?'
    },
    'fireball': {
      'name': 'Fireball'
    }
  }, 'First Order': {
    'tiebainterceptor': {
      'shipability': {
        'text': '\"Fine-Tuned Thrusters\"',
        'name': 'Fine-Tuned Thrusters'
      },
      'name': 'TIE/ba Interceptor'
    },
    'tievnsilencer': {
      'shipability': {
        'text': 'Action [Link] {actionred}[Barrel Roll]/{actionred}[Boost]',
        'name': 'Autothrusters'
      },
      'alt_name': 'Silencer',
      'name': 'TIE/vn Silencer',
      'icon': '$'
    },
    'tiesffighter': {
      'shipability': {
        'text': '[Rotate Arc][Single Turret Arc] only [Front Arc]/[Rear Arc]. [Missile][Front Arc] requirement = [Single Turret Arc]',
        'name': 'Heavy Weapon Turret'
      },
      'alt_name': 'TIE/sf',
      'name': 'TIE/sf Fighter',
      'icon': 'S'
    },
    'tiefofighter': {
      'alt_name': 'TIE/fo',
      'name': 'TIE/fo Fighter',
      'icon': 'O'
    },
    'upsilonclassshuttle': {
      'shipability': {
        'text': '[Cannon] = +1[Attack] dice',
        'name': 'Linked Battery'
      },
      'name': 'Upsilon-class command shuttle',
      'alt_name': 'Upsilon Shuttle',
      'icon':'U'
    }
  }, 'Separatist Alliance': {
    'vultureclassdroidfighter': {
      'shipability': {
        'text': 'If [Agility]/[Attack], it may spend 1 friendly [Calculate Token] at R(0-1)',
        'name': 'Networked Calculations'
      },
      'alt_name': 'Vulture Droid',
      'name': 'Vulture-class Droid Fighter',
      'icon': '_'
    },
    'sithinfiltrator': {
      'name': 'Sith Infiltrator',
      'icon': ']'
    },
    'hyenaclassdroidbomber': {
      'shipability': {
        'text': 'If [Agility]/[Attack], it may spend 1 friendly [Calculate Token] at R(0-1)',
        'name': 'Networked Calculations'
      },
      'alt_name': 'Hyena Bomber',
      'name': 'Hyena-class Droid Bomber',
      'icon': '='
    },
    'belbullab22starfighter': {
      'alt_name': 'Belbullab',
      'name': 'Belbullab-22 Starfighter',
      'icon': '['
    },
    'nantexclassstarfighter': {
      'shipability': {
        'text': '[Single Turret Arc] ≠ [Rear Arc]. Executed maneuver + [Tractor Token] [Link] [Rotate Arc]',
        'name': 'Pinpoint Tractor Array'
      },
      'alt_name': 'Nantex',
      'name': 'Nantex-class Starfighter',
      'icon': ';'
    }
  }, 'Rebel Alliance': {
    'sheathipedeclassshuttle': {
      'shipability': {
        'text': 'Carrier +[Coordinate]. Carrier may [Coordinate] B-4 it activates',
        'name': 'Comms Shuttle'
      },
      'alt_name': 'Sheathipede',
      'name': 'Sheathipede-class Shuttle',
      'icon': '%'
    },
    'rz1awing': {
      'shipability': {
        'text': 'Action [Link] {actionred}[Boost]',
        'name': 'Vectored Thrusters'
      },
      'name': 'RZ-1 A-wing',
      'alt_name': 'A-Wing',
      'icon': 'a'
    },
    't65xwing': {
      'name': 'T-65 X-wing',
      'alt_name': 'X-Wing',
      'icon': 'x'
    },
    'auzituckgunship': {
      'name': 'Auzituck Gunship',
      'alt_name': 'Auzituck',
      'icon': '@'
    },
    'modifiedyt1300lightfreighter': {
      'alt_name': 'YT-1300',
      'name': 'Modified YT-1300 Light Freighter',
      'icon': 'm'
    },
    'vcx100lightfreighter': {
      'shipability': {
        'text': "Docked ship = +[Rear Arc]. [Attack]# = docked primary [Front Arc]",
        'name': 'Tail Gun'
      },
      'name': 'VCX-100 Light Freighter',
      'alt_name': 'VCX-100',
      'icon': 'G'
    },
    'attackshuttle': {
      'shipability': {
        'text': 'Carrier +primary [Rear Arc][Attack], after primary [Front Arc]/[Turret][Attack]',
        'name': 'Locked and Loaded'
      },
      'name': 'Attack Shuttle',
      'icon': 'g'
    },
    'z95af4headhunter': {
      'alt_name': 'Z-95',
      'name': 'Z-95-AF4 Headhunter',
      'icon': 'z'
    },
    'ut60duwing': {
      'name': 'UT-60D U-wing',
      'alt_name': 'U-wing',
      'icon': 'u'
    },
    'asf01bwing': {
      'name': 'A/SF-01 B-wing',
      'alt_name': 'B-wing',
      'icon': 'b'
    },
    'yt2400lightfreighter': {
      'shipability': {
        'text': 'Primary R(0-1)[Attack] = no R(0-1) bonus & -1[Attack] ',
        'name': 'Sensor Blindspot'
      },
      'name': 'YT-2400 Light Freighter',
      'alt_name': 'YT-2400',
      'icon': 'o'
    },
    'tielnfighter': {
      'name': 'TIE/ln Fighter',
      'alt_name': 'Sabine’s TIE Fighter',
      'icon': 'F'
    },
    'btls8kwing': {
      'name': 'BTL-S8 K-wing',
      'alt_name': 'K-wing',
      'icon': 'k'
    },
    'hwk290lightfreighter': {
      'alt_name': 'HWK-290',
      'name': 'HWK-290 Light Freighter',
      'icon': 'h'
    },
    'btla4ywing': {
      'alt_name': 'Y-wing',
      'name': 'BTL-A4 Y-wing',
      'icon': 'y'
    },
    'arc170starfighter': {
      'alt_name': 'ARC-170',
      'name': 'ARC-170 Starfighter',
      'icon': 'c'
    },
    'ewing': {
      'shipability': {
        'text': 'Can only acquire locks at R(2 - ∞)',
        'name': 'Experimental Scanners'
      },
      'name': 'E-wing',
      'icon': 'e'
    }
  }, 'Galactic Republic': {
    'v19torrentstarfighter': {
      'name': 'V-19 Torrent Starfighter',
      'alt_name': 'V-19 Torrent',
      'icon': '^'
    },
    'btlbywing': {
      'shipability': {
        'text': 'When [Agility], if 0[Critical Hit] damage cards, 1[Critical Hit][Attack]=[Hit]',
        'name': 'Plated Hull'
      },
      'name': 'BTL-B Y-wing',
      'alt_name': 'Y-wing',
      'icon': ':'
    },
    'nabooroyaln1starfighter': {
      'shipability': {
        'text': 'Fully executed 3-5 maneuver [Link] [Evade]',
        'name': 'Full Throttle'
      },
      'alt_name': 'N-1 Starfighter',
      'name': 'Naboo Royal N-1 Starfighter',
      'icon': '<'
    },
    'arc170starfighter': {
      'alt_name': 'ARC-170',
      'name': 'ARC-170 Starfighter',
      'icon': 'c'
    },
    'delta7aethersprite': {
      'shipability': {
        'text': 'Fully executed maneuver [Link] {actionpurple}[Boost]/{actionpurple}[Barrel Roll]',
        'name': 'Fine-tuned Controls'
      },
      'alt_name': 'Jedi Starfighter',
      'name': 'Delta-7 Aethersprite',
      'icon': '\\'
    }
  }, 'Scum and Villainy': {
    'lancerclasspursuitcraft': {
      'alt_name': 'Lancer',
      'name': 'Lancer-class Pursuit Craft',
      'icon': 'L'
    },
    'starviperclassattackplatform': {
      'shipability': {
        'text': 'When [Barrel Roll], use [Bank Left]/[Bank Right], not [Straight]',
        'name': 'Microthrusters'
      },
      'alt_name': 'Starviper',
      'name': 'StarViper-class Attack Platform',
      'icon': 'v'
    },
    'jumpmaster5000': {
      'alt_name': 'JumpMaster',
      'name': 'JumpMaster 5000',
      'icon': 'p'
    },
    'm3ainterceptor': {
      'shipability': {
        'text': 'Can equip 1 [Cannon], [Torpedo], or [Missile] upgrade',
        'name': 'Weapon Hardpoint'
      },
      'name': 'M3-A Interceptor',
      'alt_name': 'M3-A Scyk fighter',
      'icon': 's'
    },
    'escapecraft': {
      'shipability': {
        'text': 'Carrier ship adds Escape Craft\'s pilot ability',
        'name': 'Rigged Energy Cells'
      },
      'name': 'Escape Craft',
      'icon': 'X'
    },
    'firesprayclasspatrolcraft': {
      'alt_name': 'Firespray',
      'name': 'Firespray-class Patrol Craft',
      'icon': 'f'
    },
    'modifiedtielnfighter': {
      'shipability': {
        'text': 'While it moves, it ignores asteroids',
        'name': 'Notched Stabilizers'
      },
      'alt_name': 'Mining Guild TIE',
      'name': 'Modified TIE/ln Fighter',
      'icon': 'C'
    },
    'scurrgh6bomber': {
      'alt_name': 'Scurrg',
      'name': 'Scurrg H-6 Bomber',
      'icon': 'H'
    },
    'aggressorassaultfighter': {
      'shipability': {
        'text': 'After it performs a [Calculate] action, it gains 1[Calculate Token]',
        'name': 'Advanced Droid Brain'
      },
      'alt_name': 'Aggressor',
      'name': 'Aggressor Assault Fighter',
      'icon': 'i'
    },
    'm12lkimogilafighter': {
      'shipability': {
        'text': 'Defender in [Bullseye Arc] cannot modify [Agility] with {green}tokens',
        'name': 'Dead to Rights'
      },
      'alt_name': 'Kimogila',
      'name': 'M12-L Kimogila Fighter',
      'icon': 'K'
    },
    'quadrijettransferspacetug': {
      'shipability': {
        'text': 'Action: 1 ship in R(1)[Front Arc]=1[Tractor Token], 2[Tractor Token] if in R(1)[Bullseye Arc]',
        'name': 'Spacetug Tractor Array'
      },
      'alt_name': 'TUG-b13',
      'name': 'Quadrijet Transfer Spacetug',
      'icon': 'q'
    },
    'customizedyt1300lightfreighter': {
      'alt_name': 'YT-1300',
      'name': 'Customized YT-1300 Light Freighter',
      'icon': 'W'
    },
    'g1astarfighter': {
      'name': 'G-1A Starfighter',
      'icon': 'n'
    },
    'fangfighter': {
      'shipability': {
        'text': "If [Agility] &[Attack]=R(1) & in attacker's[Front Arc], 1[Agility]dice=[Evade]",
        'name': 'Concordia Faceoff'
      },
      'name': 'Fang Fighter',
      'icon': 'M'
    },
    'yv666lightfreighter': {
      'alt_name': 'YV-666',
      'name': 'YV-666 Light Freighter',
      'icon': 't'
    },
    'z95af4headhunter': {
      'alt_name': 'Z-95',
      'name': 'Z-95-AF4 Headhunter',
      'icon': 'z'
    },
    'kihraxzfighter': {
      'alt_name': 'Kihraxz',
      'name': 'Kihraxz Fighter',
      'icon': 'r'
    },
    'hwk290lightfreighter': {
      'alt_name': 'HWK-290',
      'name': 'HWK-290 Light Freighter',
      'icon': 'h'
    },
    'btla4ywing': {
      'name': 'BTL-A4 Y-wing',
      'alt_name': 'Y-wing',
      'icon': 'y'
    }
  }
}
sizeIcons = {
	"Large": "Ã",
	"Medium": "Â",
	"Small": "Á"
}
stat_icons = {
	"Bullseye Arc": "}",
	"Double Turret Arc": "q",
	"Front Arc": "{",
	"Full Front Arc": "~",
	"Rear Arc": "|",
	"Single Turret Arc": "p",
	"agility": "^",
	"attack": "%",
	"force": "h",
	"hull": "&",
	"shields": "*"
}
action_icons = {
	"Barrel Roll": "r",
	"Boost": "b",
	"Calculate": "a",
	"Cloak": "k",
	"Coordinate": "o",
    "Evade":"e",
    "Focus":"f",
	"Jam": "j",
	"Linked": ">",
	"Lock": "l",
	"Reinforce": "i",
	"Reload": "=",
	"Rotate Arc": "R",
	"SLAM": "s",
    "Slam": "s"
}
colors = {
	"actionpurple": "#b583c2",
	"actionred": "#e61a1a",
	"actionwhite": "#ffffff",
	"agility": "#9cd90d",
    "green": "#9cd90d",
	"attack": "#e61a1a",
	"dialblue": "#0190ff",
	"dialred": "#e61a1a",
	"dialwhite": "#000000",
	"hull": "#f8f500",
	"shields": "#80d3e4"
}

def xwing_single(image, layer, pilotfile, include_ship_ability, export, dir, include_sub_folder):
    try:
        uuid = image.parasite_find("uuid")
        if uuid.data != "2fbf48a6-1e3b-11ea-978f-2e728ce88125":
            pdb.gimp_message("Please use a X-Wing Ship Maneuver card front template file. Wrong UUID.")
            return
    except:
        pdb.gimp_message("Please use a X-Wing Ship Maneuver card front template file. Missing UUID.")
        return

    if pilotfile[-4:] != "json":
        pdb.gimp_message("Please use a valid X-Wing Data2 JSON pilot file")
        return
    else:
        with open(pilotfile, "r") as read_file:
            data = json.load(read_file)

    set_faction(image, data["faction"])
    set_ship_information(image, data, include_ship_ability)
    set_dial(image, data["dial"])
    set_ship_stats(image, data["stats"])

    try:
        artwork_url=data["pilots"][0]["artwork"]
    except:
        artwork_url=""

    set_artwork(image, download_artwork(artwork_url, data["xws"], data["faction"]), data["xws"])

    set_action_bar(image, data["actions"])

    if export:
    	sub_folder = ""
    	if include_sub_folder:
    		sub_folder = "\\" + data["faction"]

    	export_image(image, dir + sub_folder, data["xws"]+".png")
def xwing_bulk(image, layer, dir, include_sub_folder, destination_directory, create_sub_folder, include_ship_ability):
    try:
        uuid = image.parasite_find("uuid")
        if uuid.data != "2fbf48a6-1e3b-11ea-978f-2e728ce88125":
            pdb.gimp_message("Please use a X-Wing Ship Maneuver card back template file. Wrong UUID.")
            return
    except:
        pdb.gimp_message("Please use a X-Wing Ship Maneuver card back template file. Missing UUID.")
        return

    import glob, os

    ships = {}
    sub_dirs = []
    files = []

    i=0

    pdb.gimp_progress_update(0.0)
    if include_sub_folder:
        sub_dirs = [x[0] for x in os.walk(dir)]
    else:
        sub_dirs = [dir]

    for sub_dir in sub_dirs:
        os.chdir(sub_dir)
        for file in glob.glob("*.json"):
            files.append(sub_dir + "\\" + file)

    for file in files:
        i += 1
        with open(file, "r") as read_file:
            data = json.load(read_file)
        if data["faction"] not in ships:
            ships[data["faction"]] = {}
        if data["xws"] not in ships[data["faction"]]:
            ships[data["faction"]][data["xws"]]={}
        ships[data["faction"]][data["xws"]]["name"] = data["name"]
        try:
            ships[data["faction"]][data["xws"]]["shipability"] = data["pilots"][0]["shipAbility"]
        except:
            pass
        pdb.gimp_progress_set_text("Exporting " + str(data["name"]) + " (" + str(i) + "/" + str(len(files)) + ")")
        pdb.gimp_progress_update(round(float(float(i)/float(len(files))),2))
        try:
            xwing_single(image, layer, file,include_ship_ability, True, destination_directory, create_sub_folder)
        except:
            print "Unable to generate maneuver card for " + file

#    print ships

    return
def clean_factions(image):
    group_layer = pdb.gimp_image_get_layer_by_name(image, "Faction Information")
    for i in group_layer.children:
        set_layer_visibility(image, i, FALSE)

    group_layer =pdb.gimp_image_get_layer_by_name(image, "Faction Backgrounds")
    for i in group_layer.children:
        set_layer_visibility(image, i, FALSE)

    return
def set_faction(image,faction):
    clean_factions(image)

    faction = (
        "Faction Information",
        "Faction Backgrounds",
        "Faction Background Base",
        faction,
        faction + " Faction Overlay")

    for i in faction:
        try:
            set_layer_visibility(image, i, TRUE)
        except:
            pass
    return
def set_ship_information(image, json, include_ship_ability):
    set_layer_visibility(image, "Ship information", TRUE)
    faction = ships[json["faction"]]
    ship = faction[json["xws"]]
    ship_info = {
        "Ship Short Name":  ship.get("alt_name", json["name"]),
        "Ship Full Name": json["name"],
        "Ship Base Size": sizeIcons.get(json["size"], "À"),
        "Ship Type Icon": ship.get("icon", "")}

    if include_ship_ability:
        set_ship_ability(image, json)

    for info in ship_info:
        set_layer_visibility(image, info, TRUE)
        set_text_layer_text(image, info, ship_info[info])
def set_ship_ability(image, json):
    import re

    try:
        ship_ability_group_layer = pdb.gimp_image_get_layer_by_name(image, "Ship Ability")
        clear_group_children(image, ship_ability_group_layer)

        faction = ships[json["faction"]]
        ship = faction[json["xws"]]
        ship_ability = ship["shipability"]
    except:
        return

    ship_ability_text = re.split('(\[|\]|\{|\})', ship_ability.get("text", ""))
    for i in reversed([i for i, e in enumerate(ship_ability_text) if e == "[" or e =="{"]) :
        ship_ability_text[i:i+3] = [''.join(ship_ability_text[i:i+3])]

    x = 225
    y = 445
    group_layer_width = 360
    font_color = "#ffffff"

    for a in ship_ability_text:
        if a[0:1] == "[":
            font = "x-wing-symbols"
            font_size = 22
            text = ship_ability_icons.get(a, "y")
            y = 443
        elif a[0:1] == "{":
            font_color = colors.get(a.replace("{","").replace("}",""), "")
            continue
        elif a =="":
            continue
        else:
            font = "Eurostile"
            font_size=20
            text = a
            y = 445

        ship_ability_text_layer = pdb.gimp_text_layer_new(image, text, font, float(font_size), 0)
        pdb.gimp_image_insert_layer(image,ship_ability_text_layer, ship_ability_group_layer, -1)
        pdb.gimp_text_layer_set_color(ship_ability_text_layer, font_color)
        pdb.gimp_item_transform_translate(ship_ability_text_layer, x, y)
        x = x + ship_ability_text_layer.width

        font_color = "#ffffff"

    if ship_ability_group_layer.width < group_layer_width:
        pdb.gimp_item_transform_translate(ship_ability_group_layer,((group_layer_width-ship_ability_group_layer.width)/2), 0)
def clear_group_children(image, group_layer):
    for child in group_layer.children:
        pdb.gimp_image_remove_layer(image, child)
def set_text_layer_text(image, layername, text):
    try:
        pdb.gimp_text_layer_set_text(pdb.gimp_image_get_layer_by_name(image, layername), text)
    except:
        print "Unable to change " + layername + "'s text."
    return
def set_text_layer_color(image, layername, color):
    try:
        pdb.gimp_text_layer_set_color(pdb.gimp_image_get_layer_by_name(image, layername), color)
    except:
        print "Unable to change " + layername + "'s color."
    return
def set_layer_visibility(image, layer, visible):

    try:
        if isinstance(layer, basestring):
            pdb.gimp_item_set_visible(pdb.gimp_image_get_layer_by_name(image, layer), visible)
        elif isinstance(layer, gimp.GroupLayer) or isinstance(layer, gimp.Layer):
            pdb.gimp_item_set_visible(layer, visible)
    except:
        print "Unable to change layer visibility."
    return
def set_dial(image, dial_json):
    #const MANEUVERS = [  "Bank Left",  "Bank Right",  "Koiogran Turn",  "Segnor's Loop Left",  "Segnor's Loop Right",  "Stationary",  "Straight",  "Tallon Roll Left",  "Tallon Roll Right",  "Turn Left",  "Turn Right"];
    #https://xwvassal.info/dialgen/dialgen
    dial = {'1-0':{'value':'','color':''}, '1-1':{'value':'','color':''}, '1-2': {'value':'','color':''},'1-3': {'value':'','color':''},'1-4': {'value':'','color':''},'1-5': {'value':'','color':''}, '1-6': {'value':'','color':''},'2-0': {'value':'','color':''}, '2-1': {'value':'','color':''}, '2-2': {'value':'','color':''},'2-3': {'value':'','color':''},'2-4': {'value':'','color':''},'2-5': {'value':'','color':''}, '2-6': {'value':'','color':''},'3-0': {'value':'','color':''}, '3-1': {'value':'','color':''}, '3-2': {'value':'','color':''},'3-3': {'value':'','color':''},'3-4': {'value':'','color':''},'3-5': {'value':'','color':''}, '3-6': {'value':'','color':''},'4-0': {'value':'','color':''}, '4-1': {'value':'','color':''}, '4-2': {'value':'','color':''},'4-3': {'value':'','color':''},'4-4': {'value':'','color':''},'4-5': {'value':'','color':''}, '4-6': {'value':'','color':''},'5-0': {'value':'','color':''}, '5-1': {'value':'','color':''}, '5-2': {'value':'','color':''},'5-3': {'value':'','color':''},'5-4': {'value':'','color':''},'5-5': {'value':'','color':''}, '5-6': {'value':'','color':''}}
    maneuverIcon = {"E":":", "R":";", "T":"4", "Y":"6", "O":"5", "P":"3", "A":"J", "S":"K", "D":"L", "F":"8", "K":"2", "L":"1", "B":"7", "N":"9"}
    difficultyColor = {"W":colors["dialwhite"], "B":colors["dialblue"], "R":colors["dialred"]}
    maneuverLayer = { "E":"0", "R":"6", "T":"1", "Y":"5", "O":"3", "P":"6", "A":"2", "S":"3", "D":"4", "F":"3", "K":"6", "L":"0", "B":"2", "N":"4"}

    increase_row = 0

    if next((man for man in dial_json if man[1:2] == 'O'), None) != None:
        increase_row = 1
    if next((man for man in dial_json if man[1:2] == 'S'), None) != None:
        man = next((man for man in dial_json if man[1:2] == 'S'), None)
        increase_row = int(man[0:1])

    #show numbers
    for x in range(1, 6):
        if increase_row >0:
            set_text_layer_text(image, "#"+str(x), x-increase_row)
            if x-increase_row <= 0:
                set_layer_visibility(image, "#"+str(x), FALSE)
            else:
                set_layer_visibility(image, "#"+str(x), TRUE)
        else:
            set_text_layer_text(image, "#"+str(x), x)
            set_layer_visibility(image, "#"+str(x), TRUE)

    for maneuver in dial_json:
        if maneuver[1:2] == 'A' or maneuver[1:2] == 'S' or maneuver[1:2] == 'D' :
            speed = str(-int(maneuver[0:1])+increase_row+1)
        else:
            speed = str(int(maneuver[0:1])+increase_row)
        dial[speed+"-"+maneuverLayer.get(maneuver[1:2])]["value"] = maneuverIcon.get(maneuver[1:2], "")
        dial[speed+"-"+maneuverLayer.get(maneuver[1:2])]["color"] = difficultyColor.get(maneuver[-1:], "#00ff0f")

    for man_cell in dial:
        if dial[man_cell]["value"] != "":
            if man_cell[-1:] == "0":
                    set_layer_visibility(image, "#"+man_cell[0:1], FALSE)
            set_layer_visibility(image, man_cell, TRUE)
            set_text_layer_text(image, man_cell, dial[man_cell]["value"])
            set_text_layer_color(image, man_cell, dial[man_cell]["color"])
        else:
            set_layer_visibility(image, man_cell, FALSE)

    return
def set_action_bar(image, action_json):
    #"actions": { "1": "boost", "2": "focus", "3": "evade", "4": "lock", "5": "barrelroll", "6": "reinforce", "7": "cloak", "8": "coordinate", "9": "calculate", "10": "jam", "12": "reload", "13": "slam", "14": "rotatearc"}

    #Action bar area
    action_bar_width =190
    action_bar_height= 498
    action_bar_x = 590
    action_bar_y = 480

    #Action bar seperator
    action_bar_seperator_height = 7

    #clean up old action layers
    action_bar_group_layer = pdb.gimp_image_get_layer_by_name(image, "Action Bar")

    for child in action_bar_group_layer.children:
        if not pdb.gimp_item_is_group(child):
            pdb.gimp_image_remove_layer(image, child)

    i = 1
    for action in action_json:
        action_text  =  action_icons.get(action["type"])
        if "linked" in action:
            action_text += " >"
        action_text_layer = pdb.gimp_text_layer_new(image, action_text, "x-wing-symbols", float(35), 0)
        pdb.gimp_image_insert_layer(image, action_text_layer, pdb.gimp_image_get_layer_by_name(image, "Action Bar"), -1)
        pdb.gimp_text_layer_set_color(action_text_layer, colors.get("action"+action["difficulty"].lower(), "#00ff00"))
        x=action_bar_x+(action_bar_width/2)-(action_text_layer.width/2)
        y=action_bar_y+(round(float((action_bar_height-(action_bar_seperator_height*(len(action_json)-1)))/len(action_json)),0)/2)+(round(float(action_bar_height/len(action_json)),0)*(i-1))-action_text_layer.height/2
        pdb.gimp_item_transform_translate(action_text_layer, x, y)

        if "linked" in action:
            linked_text_layer = pdb.gimp_text_layer_new(image, " " + action_icons.get(action["linked"]["type"]), "x-wing-symbols", float(35), 0)
            pdb.gimp_image_insert_layer(image, linked_text_layer, pdb.gimp_image_get_layer_by_name(image, "Action Bar"), -1)
            pdb.gimp_text_layer_set_color(linked_text_layer, colors.get("action"+action["linked"]["difficulty"].lower(), "#00ff00"))
            pdb.gimp_item_transform_translate(action_text_layer, -linked_text_layer.width/2, 0)
            pdb.gimp_item_transform_translate(linked_text_layer, action_text_layer.offsets[0]+action_text_layer.width, action_text_layer.offsets[1])



        i += 1
    return
def set_ship_stats(image, stats_json):
    i=1
    stats_show = ("Ship Stats", )
    stats_hide = ()
    if (len(stats_json) % 2) == 0:
        stats_show += ("Even", )
        stats_hide += ("Odd", )
        oddeven = "E"
        if len(stats_json)==2:
            i=2
            stats_hide += (oddeven+"1I", oddeven+"1T", oddeven+"4I", oddeven+"4T")
    else:
        stats_show += ("Odd", )
        stats_hide += ("Even", )
        oddeven = "O"
        if len(stats_json)==3:
            stats_hide += (oddeven+"1I", oddeven+"1T", oddeven+"5I", oddeven+"5T")
            i=2

    for stat in stats_json:
        stats_show += (oddeven+str(i)+"I", oddeven+str(i)+"T")
        if stat["type"]=="attack":
            stat_icon=stat_icons.get(stat["arc"], "%")
        else:
            stat_icon=stat_icons.get(stat["type"], "")
        set_text_layer_text(image, oddeven+str(i)+"I", stat_icon)
        set_text_layer_color(image, oddeven+str(i)+"I", colors[stat["type"]])
        set_text_layer_text(image, oddeven+str(i)+"T", stat["value"])
        set_text_layer_color(image, oddeven+str(i)+"T", colors[stat["type"]])

        i+=1

    for show in stats_show:
        set_layer_visibility(image, show, TRUE)

    for hide in stats_hide:
        set_layer_visibility(image, hide, FALSE)

    return
def remove_artwork(image):
    try:
        artwork = pdb.gimp_image_get_layer_by_name(image, "Artwork")
        pdb.gimp_image_remove_layer(image, artwork)
    except:
        pass

    return
def set_artwork(image, artwork, xws_name):
    remove_artwork(image)
    if artwork == "" or xws_name =='':
        return
    artwork_layer = pdb.gimp_file_load_layer(image, artwork)
    pdb.gimp_image_insert_layer(image, artwork_layer, pdb.gimp_image_get_layer_by_name(image, "Ship Artwork"), -1)
    pdb.gimp_layer_set_name(artwork_layer, "Artwork")

    scale_factor = (float(image.width)/float(artwork_layer.width))
    if scale_factor*artwork_layer.width>=image.width:
        if scale_factor*artwork_layer.height<350:
            scale_factor = (float(350)/float(artwork_layer.height))
    pdb.gimp_layer_scale(artwork_layer, int(round(scale_factor*float(artwork_layer.width),0)), int(round(scale_factor*float(artwork_layer.height),0)), 0)

    return artwork_layer
def download_artwork(url, xws_name, faction):

    plugin_path = "\\".join(sys.argv[0].split("\\")[0:-1])
    artwork_path = plugin_path + "\\artwork"

    #create artwork folder if it does not existz
    if not os.path.exists(plugin_path + "\\artwork"):
        os.makedirs(plugin_path + "\\artwork")
    #check if artwork already exists
    if len([ name for name in os.listdir(artwork_path) if name == faction.lower().replace(" ","") + "_" + xws_name + ".jpg" ]) == 1:
        return artwork_path + "\\" + faction.lower().replace(" ","") + "_" + xws_name + ".jpg"

    if url =='':
        return

    r = requests.get(url, auth=('usrname', 'password'), verify=False,stream=True)
    r.raw.decode_content = True
    with open(artwork_path + "\\" + faction.lower().replace(" ","") + "_" + xws_name + ".jpg", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    return artwork_path + "\\" + faction.lower().replace(" ","") + "_" + xws_name + ".jpg"
def export_image(image, path, filename):

    if not os.path.exists(path):
        os.makedirs(path)

    new_image = pdb.gimp_image_duplicate(image)
    layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
    pdb.gimp_file_save(new_image, layer, path + "\\" + filename, path + "\\" + filename)
    pdb.gimp_image_delete(new_image)
    return
register(
        "xwing-bulk",
        "",
        "",
        "Knut Urbye",
        "Knut Urbye",
        "2019",
        "<Image>/Filters/X-Wing 2.0 Maneuver Card Generator/Front Bulk",
        "",
        [
		(PF_DIRNAME, "source_directory", "Import Directory", ""),
        (PF_TOGGLE, "sub_folder", "Search sub-folders?", True),
        (PF_DIRNAME, "destination_directory", "Export Directory", ""),
		(PF_TOGGLE, "create_sub_folder", "Use/Create faction sub-folder?", True),
        (PF_TOGGLE, "include_ship_ability", "Include Ship Ability?", True)
        ],
        [],
        xwing_bulk)
register(
        "xwing-single",
        "",
        "",
        "Knut Urbye",
        "Knut Urbye",
        "2019",
        "<Image>/Filters/X-Wing 2.0 Maneuver Card Generator/Front Single",
        "",
        [
        (PF_FILE, "pilotfile", "X-Wing Data Pilot JSON file", ""),
        (PF_TOGGLE, "include_ship_ability", "Include Ship Ability?", True),
		(PF_TOGGLE, "export", "Export Image?", False),
		(PF_DIRNAME, "source_directory", "Export Directory", ""),
		(PF_TOGGLE, "sub-folder", "Use/Create faction sub-folder?", True)
        ],
        [],
        xwing_single)

main()
