#!/usr/bin/env python3
# Animal Rush backend - Railway edition (zero dependency, python stdlib only).
import base64, hashlib, hmac, http.client, json, os, random, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

PORT = int(os.environ.get('PORT', '8899'))
HOST = '0.0.0.0'
DATA_DIR = os.environ.get('DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(DATA_DIR, 'state.json')

CHARS = [
    {"id": 1, "name": "Freddy", "path": "res://assets/characters/Human/human.tscn", "card_path": "res://assets/characters/2D Card/Freddy_card.png", "tier": "Common"},
    {"id": 2, "name": "Frog", "path": "res://assets/characters/Frog/Frog.tscn", "card_path": "res://assets/characters/2D Card/Frog_card.png", "tier": "Common"},
    {"id": 3, "name": "Fox", "path": "res://assets/characters/Fox/Fox.tscn", "card_path": "res://assets/characters/2D Card/Fox_card.png", "tier": "Common"},
    {"id": 4, "name": "Horse", "path": "res://assets/characters/Horse/horse.tscn", "card_path": "res://assets/characters/2D Card/Horse_card.png", "tier": "Rare"},
    {"id": 5, "name": "Leopard", "path": "res://assets/characters/Leopard/Leopard.tscn", "card_path": "res://assets/characters/2D Card/Leopard_card.png", "tier": "Common"},
    {"id": 6, "name": "Tourist", "path": "res://assets/characters/Tourist/Tourist.tscn", "card_path": "res://assets/characters/2D Card/Ecotourist_card.png", "tier": "Rare"},
    {"id": 7, "name": "Sheep", "path": "res://assets/characters/Sheep/Sheep.tscn", "card_path": "res://assets/characters/2D Card/Sheep_card.png", "tier": "Common"},
    {"id": 8, "name": "Rabbit", "path": "res://assets/characters/Rabbid/Rabbid.tscn", "card_path": "res://assets/characters/2D Card/Rabbid_card.png", "tier": "Common"},
    {"id": 9, "name": "Monkey", "path": "res://assets/characters/Monkey/Monkey.tscn", "card_path": "res://assets/characters/2D Card/Monkey_card.png", "tier": "Common"},
    {"id": 10, "name": "Elephant", "path": "res://assets/characters/Elephant/Elephant.tscn", "card_path": "res://assets/characters/2D Card/Elephant_card.png", "tier": "Common"},
    {"id": 11, "name": "Lion", "path": "res://assets/characters/Lion/Lion.tscn", "card_path": "res://assets/characters/2D Card/Lion_card.png", "tier": "Common"},
    {"id": 12, "name": "Bear", "path": "res://assets/characters/Bear/Bear.tscn", "card_path": "res://assets/characters/2D Card/Bear_card.png", "tier": "Common"},
    {"id": 13, "name": "Samurai Bear", "path": "res://assets/characters/Bear/Samurai_Bear.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Bear_card.png", "tier": "Legendary"},
    {"id": 14, "name": "Samurai Elephant", "path": "res://assets/characters/Elephant/Samurai_elephant.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Elephant_card.png", "tier": "Legendary"},
    {"id": 15, "name": "Samurai Fox", "path": "res://assets/characters/Fox/Samurai_fox.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Fox_card.png", "tier": "Legendary"},
    {"id": 16, "name": "Samurai Horse", "path": "res://assets/characters/Horse/Samurai_horse.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Horse_card.png", "tier": "Legendary"},
    {"id": 17, "name": "Samurai Leopard", "path": "res://assets/characters/Leopard/Samurai_leopard.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Leopard_card.png", "tier": "Legendary"},
    {"id": 18, "name": "Samurai Monkey", "path": "res://assets/characters/Monkey/Samurai_Monkey.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Monkey_card.png", "tier": "Legendary"},
    {"id": 19, "name": "Samurai Lion", "path": "res://assets/characters/Lion/Samurai_Lion.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Lion_card.png", "tier": "Legendary"},
    {"id": 20, "name": "Samurai Rabbit", "path": "res://assets/characters/Rabbid/Samurai_Rabbid.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Rabbid_card.png", "tier": "Legendary"},
    {"id": 21, "name": "Samurai Sheep", "path": "res://assets/characters/Sheep/Samurai_Sheep.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Sheep_card.png", "tier": "Legendary"},
    {"id": 33, "name": "Samurai Frog", "path": "res://assets/characters/Frog/Samurai_frog.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Frog_card.png", "tier": "Legendary"},
    {"id": 22, "name": "Astronaut Bear", "path": "res://assets/characters/Astronaut/Astronaut_bear.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Bear_card.png", "tier": "Legendary"},
    {"id": 23, "name": "Astronaut Elephant", "path": "res://assets/characters/Astronaut/Astronaut_elephant.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Elephant_card.png", "tier": "Legendary"},
    {"id": 24, "name": "Astronaut Fox", "path": "res://assets/characters/Astronaut/Astronaut_fox.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Fox_card.png", "tier": "Legendary"},
    {"id": 25, "name": "Astronaut Frog", "path": "res://assets/characters/Astronaut/Astronaut_frog.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Frog_card.png", "tier": "Legendary"},
    {"id": 26, "name": "Astronaut Horse", "path": "res://assets/characters/Astronaut/Astronaut_horse.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Horse_card.png", "tier": "Legendary"},
    {"id": 27, "name": "Astronaut Leopard", "path": "res://assets/characters/Astronaut/Astronaut_leopard.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Leopard_card.png", "tier": "Legendary"},
    {"id": 28, "name": "Astronaut Lion", "path": "res://assets/characters/Astronaut/Astronaut_lion.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Lion_card.png", "tier": "Legendary"},
    {"id": 29, "name": "Astronaut Monkey", "path": "res://assets/characters/Astronaut/Astronaut_monkey.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Monkey_card.png", "tier": "Legendary"},
    {"id": 30, "name": "Astronaut Rabbit", "path": "res://assets/characters/Astronaut/Astronaut_rabbit.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Rabbid_card.png", "tier": "Legendary"},
    {"id": 31, "name": "Astronaut Sheep", "path": "res://assets/characters/Astronaut/Astronaut_sheep.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Sheep_card.png", "tier": "Legendary"},
    {"id": 32, "name": "Azari", "path": "res://assets/characters/AzariOutfits/human_azari.tscn", "card_path": "res://assets/characters/2D Card/Human_Azzari_Card.png", "tier": "Rare"},
    {"id": 34, "name": "Kurd", "path": "res://assets/characters/Kurd/human_kurd.tscn", "card_path": "res://assets/characters/2D Card/Human_Kurd_Card.png", "tier": "Rare"},
    {"id": 35, "name": "Parinaz", "path": "res://assets/characters/Human/Farinaz.tscn", "card_path": "res://assets/characters/2D Card/Farinaz_card.png", "tier": "Common"},
    {"id": 43, "name": "Dog", "path": "res://assets/characters/Dog/Dog.tscn", "card_path": "res://assets/characters/2D Card/Dog_card.png", "tier": "Common"},
    {"id": 44, "name": "Rhino", "path": "res://assets/characters/Rhino/Rhino.tscn", "card_path": "res://assets/characters/2D Card/Rhino_card.png", "tier": "Rare"},
    {"id": 45, "name": "Penguin", "path": "res://assets/characters/Penguin/Penguin.tscn", "card_path": "res://assets/characters/2D Card/Penguin_card.png", "tier": "Common"},
    {"id": 46, "name": "Shark", "path": "res://assets/characters/Shark/Shark.tscn", "card_path": "res://assets/characters/2D Card/Shark_card.png", "tier": "Rare"},
    {"id": 48, "name": "Police", "path": "res://assets/characters/Police/Police.tscn", "card_path": "res://assets/characters/2D Card/Police_card.png", "tier": "Legendary"},
    {"id": 47, "name": "Kouroosh", "path": "res://assets/characters/Kouroosh/Kouroosh.tscn", "card_path": "res://assets/characters/2D Card/Kouroosh_card.png", "tier": "Epic"},
    {"id": 49, "name": "Mia", "path": "res://assets/characters/Mia/Mia.tscn", "card_path": "res://assets/characters/2D Card/Mia_card.png", "tier": "Epic"},
    {"id": 50, "name": "Nopo", "path": "res://assets/characters/Nopo/Nopo.tscn", "card_path": "res://assets/characters/2D Card/Nopo_card.png", "tier": "Epic"},
    {"id": 51, "name": "Lor", "path": "res://assets/characters/Lor/Lor.tscn", "card_path": "res://assets/characters/2D Card/Lor_card.png", "tier": "Rare"},
    {"id": 52, "name": "Panda", "path": "res://assets/characters/Panda/Panda.tscn", "card_path": "res://assets/characters/2D Card/Panda_card.png", "tier": "Rare"},
    {"id": 53, "name": "Ninja", "path": "res://assets/characters/Ninja/Ninja.tscn", "card_path": "res://assets/characters/2D Card/Ninja_card.png", "tier": "Epic"},
    {"id": 54, "name": "Bee", "path": "res://assets/characters/Bee/Bee.tscn", "card_path": "res://assets/characters/2D Card/Bee_card.png", "tier": "Legendary"},
    {"id": 55, "name": "NaderShah", "path": "res://assets/characters/Nadershah/Nadershah.tscn", "card_path": "res://assets/characters/2D Card/Nadershah_card.png", "tier": "Epic"},
    {"id": 56, "name": "Patrick", "path": "res://assets/characters/Patrick/Patrick.tscn", "card_path": "res://assets/characters/2D Card/Patrick_card.png", "tier": "Epic"},
    {"id": 57, "name": "SpongeBob", "path": "res://assets/characters/SpongeBob/SpongeBob.tscn", "card_path": "res://assets/characters/2D Card/SpongeBob_card.png", "tier": "Epic"},
    {"id": 58, "name": "Engineer", "path": "res://assets/characters/Engineer/Engineer.tscn", "card_path": "res://assets/characters/2D Card/Engineer_card.png", "tier": "Rare"},
    {"id": 59, "name": "Graduated", "path": "res://assets/characters/Graduated/Graduated.tscn", "card_path": "res://assets/characters/2D Card/Graduated_card.png", "tier": "Rare"},
    {"id": 60, "name": "Leonardo", "path": "res://assets/characters/TMNT/Leonardo/Leonardo.tscn", "card_path": "res://assets/characters/2D Card/Leonardo_card.png", "tier": "Legendary"},
    {"id": 61, "name": "Rapheal", "path": "res://assets/characters/TMNT/Raphaeal/Raphael.tscn", "card_path": "res://assets/characters/2D Card/Rapheal_card.png", "tier": "Legendary"},
    {"id": 62, "name": "Danatello", "path": "res://assets/characters/TMNT/donatello/Danatello.tscn", "card_path": "res://assets/characters/2D Card/Danatello_card.png", "tier": "Legendary"},
    {"id": 63, "name": "Michelangelo", "path": "res://assets/characters/TMNT/Michelangelo/Michelangelo.tscn", "card_path": "res://assets/characters/2D Card/Michelangelo_card.png", "tier": "Legendary"},
    {"id": 64, "name": "Eren Yeager", "path": "res://assets/characters/Eren Yeager/Eren Yeager.tscn", "card_path": "res://assets/characters/2D Card/ErenYeager_card.png", "tier": "Epic"},
    {"id": 65, "name": "Soldier", "path": "res://assets/characters/Soldier/Soldier.tscn", "card_path": "res://assets/characters/2D Card/Soldier_card.png", "tier": "Legendary"},
    {"id": 66, "name": "RedHood", "path": "res://assets/characters/RedHood/RedHood.tscn", "card_path": "res://assets/characters/2D Card/RedHood_card.png", "tier": "Legendary"},
    {"id": 67, "name": "Pilot", "path": "res://assets/characters/Pilot/Pilot.tscn", "card_path": "res://assets/characters/2D Card/Pilot_card.png", "tier": "Legendary"},
    {"id": 68, "name": "Elsa", "path": "res://assets/characters/Elsa/Elsa.tscn", "card_path": "res://assets/characters/2D Card/Elsa_card.png", "tier": "Epic"},
    {"id": 69, "name": "Merida", "path": "res://assets/characters/Merida/Merida.tscn", "card_path": "res://assets/characters/2D Card/Merida_card.png", "tier": "Epic"},
    {"id": 70, "name": "Geek", "path": "res://assets/characters/Vision Pro/VisionPro.tscn", "card_path": "res://assets/characters/2D Card/VisionPro_card.png", "tier": "Legendary"},
    {"id": 71, "name": "FootBallPlayer", "path": "res://assets/characters/Football Player/FootBallPlayer.tscn", "card_path": "res://assets/characters/2D Card/FootballPlayer_card.png", "tier": "Epic"},
    {"id": 72, "name": "Scientist", "path": "res://assets/characters/Scientist/Scientist.tscn", "card_path": "res://assets/characters/2D Card/Scintist_card.png", "tier": "Legendary"},
    {"id": 73, "name": "Butcher", "path": "res://assets/characters/Butcher/Butcher.tscn", "card_path": "res://assets/characters/2D Card/Butcher_card.png", "tier": "Epic"},
    {"id": 74, "name": "Doctor", "path": "res://assets/characters/Doctor/Doctor.tscn", "card_path": "res://assets/characters/2D Card/Doctor_card.png", "tier": "Rare"},
    {"id": 75, "name": "BankClerk", "path": "res://assets/characters/BankClerk/BankClerk.tscn", "card_path": "res://assets/characters/2D Card/BankClerk_card.png", "tier": "Rare"},
    {"id": 76, "name": "Rostam", "path": "res://assets/characters/Rostam/Rostam.tscn", "card_path": "res://assets/characters/2D Card/Rostam_card.png", "tier": "Epic"},
    {"id": 77, "name": "PersianPrincess", "path": "res://assets/characters/PersianPrincess/PersianPrincess.tscn", "card_path": "res://assets/characters/2D Card/PersianPrincess_card.png", "tier": "Epic"},
    {"id": 78, "name": "AghaTakhti", "path": "res://assets/characters/AghaTakhti/AghaTakhti.tscn", "card_path": "res://assets/characters/2D Card/AghaTakhti_card.png", "tier": "Epic"},
    {"id": 79, "name": "AmirKabir", "path": "res://assets/characters/AmirKabir/AmirKabir.tscn", "card_path": "res://assets/characters/2D Card/AmirKabir_card.png", "tier": "Legendary"},
    {"id": 80, "name": "AndrewTate", "path": "res://assets/characters/AndrewTate/AndrewTate.tscn", "card_path": "res://assets/characters/2D Card/AndrewTate_card.png", "tier": "Epic"},
    {"id": 81, "name": "Batman", "path": "res://assets/characters/Batman/Batman.tscn", "card_path": "res://assets/characters/2D Card/Batman_card.png", "tier": "Epic"},
    {"id": 82, "name": "ElonMask", "path": "res://assets/characters/ElonMask/ElonMask.tscn", "card_path": "res://assets/characters/2D Card/ElonMask_card.png", "tier": "Epic"},
    {"id": 83, "name": "FireFighter", "path": "res://assets/characters/FireFighter/FireFighter.tscn", "card_path": "res://assets/characters/2D Card/FireFighter_card.png", "tier": "Rare"},
    {"id": 84, "name": "HassanYazdani", "path": "res://assets/characters/HassanYazdani/HassanYazdani.tscn", "card_path": "res://assets/characters/2D Card/HassanYazdani_card.png", "tier": "Legendary"},
    {"id": 85, "name": "HazMat", "path": "res://assets/characters/HazMat/HazMat.tscn", "card_path": "res://assets/characters/2D Card/HazMat_card.png", "tier": "Legendary"},
    {"id": 86, "name": "Jumong", "path": "res://assets/characters/Jumong/Jumong.tscn", "card_path": "res://assets/characters/2D Card/Jumong_card.png", "tier": "Epic"},
    {"id": 87, "name": "KarateKa", "path": "res://assets/characters/KarateKa/KarateKa.tscn", "card_path": "res://assets/characters/2D Card/KarateKa_card.png", "tier": "Rare"},
    {"id": 88, "name": "KaveAhangar", "path": "res://assets/characters/KaveAhangar/KaveAhangar.tscn", "card_path": "res://assets/characters/2D Card/KaveAhangar_card.png", "tier": "Epic"},
    {"id": 89, "name": "NaserAldinShah", "path": "res://assets/characters/NaserEldinShah/NaserEldinShah.tscn", "card_path": "res://assets/characters/2D Card/NaserAldinShah_Card.png", "tier": "Epic"},
    {"id": 90, "name": "PuriaVali", "path": "res://assets/characters/PuriaVali/PuriaVali.tscn", "card_path": "res://assets/characters/2D Card/PuriaVali_card.png", "tier": "Epic"},
    {"id": 91, "name": "Simurgh", "path": "res://assets/characters/Simurgh/Simurgh.tscn", "card_path": "res://assets/characters/2D Card/Simurgh_card.png", "tier": "Epic"},
    {"id": 92, "name": "WalterHazmat", "path": "res://assets/characters/HazMat/HazMatWalter.tscn", "card_path": "res://assets/characters/2D Card/WalterHazmat.png", "tier": "Epic"},
    {"id": 93, "name": "WalterWhite", "path": "res://assets/characters/WalterWhite/WalterWhite.tscn", "card_path": "res://assets/characters/2D Card/WalterWhite_card.png", "tier": "Legendary"},
    {"id": 94, "name": "ChefFemale", "path": "res://assets/characters/Chef/ChefFemale.tscn", "card_path": "res://assets/characters/2D Card/ChefFemale_Card.png", "tier": "Rare"},
    {"id": 95, "name": "ChefMale", "path": "res://assets/characters/Chef/ChefMale.tscn", "card_path": "res://assets/characters/2D Card/ChefMale_Card.png", "tier": "Rare"},
    {"id": 96, "name": "GarsonMale", "path": "res://assets/characters/Garson/GarsonMale.tscn", "card_path": "res://assets/characters/2D Card/GarsonMale_Card.png", "tier": "Rare"},
    {"id": 97, "name": "GarsonFemale", "path": "res://assets/characters/Garson/GarsonFemale.tscn", "card_path": "res://assets/characters/2D Card/GarsonFemale_Card.png", "tier": "Rare"},
    {"id": 98, "name": "Boss", "path": "res://assets/characters/Boss/Boss.tscn", "card_path": "res://assets/characters/2D Card/Boss_Card.png", "tier": "Legendary"},
    {"id": 99, "name": "DoctorFemale", "path": "res://assets/characters/Doctor/DoctorFemale.tscn", "card_path": "res://assets/characters/2D Card/DoctorFemale_Card.png", "tier": "Rare"},
    {"id": 100, "name": "Nurse", "path": "res://assets/characters/Nurse/Nurse.tscn", "card_path": "res://assets/characters/2D Card/Nurse_Card.png", "tier": "Rare"},
    {"id": 101, "name": "PoliceEntezami", "path": "res://assets/characters/PoliceEntezami/PoliceEntezami.tscn", "card_path": "res://assets/characters/2D Card/policeentezami.png", "tier": "Legendary"},
    {"id": 102, "name": "PoliceFemale", "path": "res://assets/characters/PoliceFemale/PoliceFemale.tscn", "card_path": "res://assets/characters/2D Card/pfr.png", "tier": "Legendary"},
    {"id": 103, "name": "Robber", "path": "res://assets/characters/Robber/Robber.tscn", "card_path": "res://assets/characters/2D Card/Robber.png", "tier": "Epic"},
    {"id": 104, "name": "SardarSepah", "path": "res://assets/characters/SardarSepah/SardarSepah.tscn", "card_path": "res://assets/characters/2D Card/sepah.png", "tier": "Epic"},
    {"id": 105, "name": "SardarArtesh", "path": "res://assets/characters/SardarArtesh/SardarArtesh.tscn", "card_path": "res://assets/characters/2D Card/sardarartesh.png", "tier": "Epic"},
    {"id": 106, "name": "Ronaldo", "path": "res://assets/characters/Ronaldo/Ronaldo.tscn", "card_path": "res://assets/characters/Ronaldo/ronaldorender.png", "tier": "Epic"},
    {"id": 107, "name": "Messi", "path": "res://assets/characters/Messi/Messi.tscn", "card_path": "res://assets/characters/Messi/messirender.png", "tier": "Epic"},
    {"id": 108, "name": "Nezoko", "path": "res://assets/characters/Nezoko/Nezoko.tscn", "card_path": "res://assets/characters/Nezoko/nezukorender.png", "tier": "Epic"},
    {"id": 109, "name": "SquidGame", "path": "res://assets/characters/SquidGame/SquidGame.tscn", "card_path": "res://assets/characters/SquidGame/rendersquidgame.png", "tier": "Epic"},
    {"id": 110, "name": "Tanjiro", "path": "res://assets/characters/Tanjiro/Tanjiro.tscn", "card_path": "res://assets/characters/Tanjiro/TANJIROrender.png", "tier": "Epic"},
    {"id": 111, "name": "Cyrus", "path": "res://assets/characters/Cyrus/Cyrus.tscn", "card_path": "res://assets/characters/Cyrus/Cyrusrender.png", "tier": "Epic"},
    {"id": 112, "name": "BossLady", "path": "res://assets/characters/BossLady/BossLady.tscn", "card_path": "res://assets/characters/BossLady/bossladyrender.png", "tier": "Legendary"},
    {"id": 113, "name": "Bride", "path": "res://assets/characters/Bride/Bride.tscn", "card_path": "res://assets/characters/Bride/briderender.png", "tier": "Legendary"},
    {"id": 114, "name": "Groom", "path": "res://assets/characters/Groom/Groom.tscn", "card_path": "res://assets/characters/Groom/GROOMRENDER.png", "tier": "Legendary"},
    {"id": 115, "name": "HadiChoopan", "path": "res://assets/characters/HadiChoopan/HadiChoopan.tscn", "card_path": "res://assets/characters/HadiChoopan/hadichoopanrender.png", "tier": "Epic"},
    {"id": 116, "name": "MoeinXM", "path": "res://assets/characters/MoeinXM/MoeinXM.tscn", "card_path": "res://assets/characters/2D Card/MoinXM_card.png", "tier": "Epic"},
    {"id": 117, "name": "Aghed", "path": "res://assets/characters/Aghed/Aghed.tscn", "card_path": "res://assets/characters/2D Card/Aghed_card.png", "tier": "Legendary"},
    {"id": 118, "name": "Spiderman", "path": "res://assets/characters/Spiderman/Spiderman.tscn", "card_path": "res://assets/characters/Spiderman/Spidermanrender.png", "tier": "Epic"},
    {"id": 119, "name": "ThomasShelby", "path": "res://assets/characters/ThomasShelby/ThomasShelby.tscn", "card_path": "res://assets/characters/ThomasShelby/shelbyrender.png", "tier": "Epic"},
    {"id": 120, "name": "HarryPotter", "path": "res://assets/characters/HarryPotter/HarryPotter.tscn", "card_path": "res://assets/characters/HarryPotter/HPRENDER.png", "tier": "Epic"},
    {"id": 121, "name": "AmongUs", "path": "res://assets/characters/AmongUs/AmongUs.tscn", "card_path": "res://assets/characters/AmongUs/amongusrender.png", "tier": "Epic"},
    {"id": 122, "name": "MrCrab", "path": "res://assets/characters/MrCrab/MrCrab.tscn", "card_path": "res://assets/characters/MrCrab/mrkrabsrender.png", "tier": "Epic"},
    {"id": 123, "name": "Luffy", "path": "res://assets/characters/Luffy/Luffy.tscn", "card_path": "res://assets/characters/Luffy/luffyrender.png", "tier": "Epic"},
    {"id": 124, "name": "FemaleClerk", "path": "res://assets/characters/FemaleClerk/FemaleClerk.tscn", "card_path": "res://assets/characters/FemaleClerk/FemaleClerk.png", "tier": "Rare"},
    {"id": 125, "name": "Shrek", "path": "res://assets/characters/Shrek/Shrek.tscn", "card_path": "res://assets/characters/Shrek/shrekrender.png", "tier": "Epic"},
    {"id": 126, "name": "Deadpool", "path": "res://assets/characters/Deadpool/Deadpool.tscn", "card_path": "res://assets/characters/Deadpool/DeadPool_card.png", "tier": "Epic"},
    {"id": 127, "name": "Leon", "path": "res://assets/characters/Leon/Leon.tscn", "card_path": "res://assets/characters/Leon/Leon_card.png", "tier": "Epic"},
    {"id": 128, "name": "Matilda", "path": "res://assets/characters/Matlida/Matlida.tscn", "card_path": "res://assets/characters/Matlida/Matilda_card.png", "tier": "Epic"},
    {"id": 129, "name": "ShahAbbas", "path": "res://assets/characters/ShahAbbas/ShahAbbas.tscn", "card_path": "res://assets/characters/ShahAbbas/ShahAbas.png", "tier": "Epic"},
    {"id": 130, "name": "Brucelee", "path": "res://assets/characters/Brucelee/BruceLee.tscn", "card_path": "res://assets/characters/Brucelee/bruceleerender.png", "tier": "Epic"},
    {"id": 131, "name": "DaeiHamed", "path": "res://assets/characters/DaeiHamed/DaeiHamed.tscn", "card_path": "res://assets/characters/DaeiHamed/DaiHamed_card.png", "tier": "Epic"},
    {"id": 132, "name": "Fiona", "path": "res://assets/characters/Fiona/Fiona.tscn", "card_path": "res://assets/characters/Fiona/Fiona_card.png", "tier": "Epic"},
    {"id": 133, "name": "Hitman", "path": "res://assets/characters/Hitman/Hitman.tscn", "card_path": "res://assets/characters/Hitman/hitmanrender.png", "tier": "Epic"},
    {"id": 134, "name": "Kaseb", "path": "res://assets/characters/Kaseb/Kaseb.tscn", "card_path": "res://assets/characters/Kaseb/kasebrender.png", "tier": "Epic"},
    {"id": 135, "name": "Khiabani", "path": "res://assets/characters/Khiabani/Khiabani.tscn", "card_path": "res://assets/characters/Khiabani/khiabanirender.png", "tier": "Epic"},
    {"id": 136, "name": "Looti", "path": "res://assets/characters/Looti/Looti.tscn", "card_path": "res://assets/characters/Looti/lootirender.png", "tier": "Epic"},
    {"id": 137, "name": "Mikasa", "path": "res://assets/characters/Mikasa/Mikasa.tscn", "card_path": "res://assets/characters/Mikasa/Mikasa_card.png", "tier": "Epic"},
    {"id": 138, "name": "MrBeast", "path": "res://assets/characters/MrBeast/Mrbeast.tscn", "card_path": "res://assets/characters/MrBeast/mrbeastrender.png", "tier": "Epic"},
    {"id": 139, "name": "Naruto", "path": "res://assets/characters/Naruto/Naroto.tscn", "card_path": "res://assets/characters/Naruto/narutorender.png", "tier": "Epic"},
    {"id": 140, "name": "Neymar", "path": "res://assets/characters/Neymar/Neymar.tscn", "card_path": "res://assets/characters/Neymar/neymar render.png", "tier": "Epic"},
    {"id": 141, "name": "Ragnar", "path": "res://assets/characters/Ragnar/Ragnar.tscn", "card_path": "res://assets/characters/Ragnar/ragnarrender.png", "tier": "Epic"},
    {"id": 142, "name": "Ronaldinho", "path": "res://assets/characters/Ronaldinho/Ronaldinho.tscn", "card_path": "res://assets/characters/Ronaldinho/ronaldinhorender.png", "tier": "Epic"},
    {"id": 143, "name": "Sakura", "path": "res://assets/characters/Sakura/Sakura.tscn", "card_path": "res://assets/characters/Sakura/Sakura_card.png", "tier": "Epic"},
    {"id": 144, "name": "Sandi", "path": "res://assets/characters/Sandi/Sandi.tscn", "card_path": "res://assets/characters/Sandi/Sandi_card.png", "tier": "Epic"},
    {"id": 145, "name": "Octopus", "path": "res://assets/characters/Octopus/Octopus.tscn", "card_path": "res://assets/characters/Octopus/octopusrender.png", "tier": "Epic"},
    {"id": 146, "name": "Steve", "path": "res://assets/characters/Steve/Steve.tscn", "card_path": "res://assets/characters/Steve/Steverender.png", "tier": "Epic"},
    {"id": 147, "name": "Arash", "path": "res://assets/characters/Arash/Arash.tscn", "card_path": "res://assets/characters/Arash/ArashKamanGir_card.png", "tier": "Epic"},
    {"id": 148, "name": "Diego", "path": "res://assets/characters/Diego/Diego.tscn", "card_path": "res://assets/characters/Diego/diegorender.png", "tier": "Epic"},
    {"id": 149, "name": "Manny", "path": "res://assets/characters/Manny/Manny.tscn", "card_path": "res://assets/characters/Manny/Mannyrender.png", "tier": "Special"},
    {"id": 150, "name": "Scrat", "path": "res://assets/characters/Scrat/Scrat.tscn", "card_path": "res://assets/characters/Scrat/scratrender.png", "tier": "Epic"},
    {"id": 151, "name": "Sid", "path": "res://assets/characters/Sid/Sid.tscn", "card_path": "res://assets/characters/Sid/sidrender.png", "tier": "Special"},
    {"id": 152, "name": "HassanSabbah", "path": "res://assets/characters/HassanSabbah/HassanSabbah.tscn", "card_path": "res://assets/characters/HassanSabbah/HassanSabah_card.png", "tier": "Special"},
    {"id": 153, "name": "JohnWick", "path": "res://assets/characters/John Wick/JohnWick.tscn", "card_path": "res://assets/characters/John Wick/JhonWick_card.png", "tier": "Special"},
    {"id": 154, "name": "Frontman", "path": "res://assets/characters/Frontman/Frontman.tscn", "card_path": "res://assets/characters/Frontman/frontmanrender.png", "tier": "Special"},
    {"id": 155, "name": "Ghost", "path": "res://assets/characters/Ghost/Ghost.tscn", "card_path": "res://assets/characters/Ghost/Ghost_card.png", "tier": "Special"},
    {"id": 156, "name": "Eskimoboy", "path": "res://assets/characters/Eskimoboy/Eskimoboy.tscn", "card_path": "res://assets/characters/Eskimoboy/eskimoboyrender.png", "tier": "Legendary"},
    {"id": 157, "name": "Eskimogirl", "path": "res://assets/characters/Eskimogirl/Eskimogirl.tscn", "card_path": "res://assets/characters/Eskimogirl/eskimogirlrender.png", "tier": "Legendary"},
    {"id": 158, "name": "Olaf", "path": "res://assets/characters/Olaf/Olaf.tscn", "card_path": "res://assets/characters/Olaf/olafrender.png", "tier": "Special"},
    {"id": 159, "name": "Sonic", "path": "res://assets/characters/Sonic/Sonic.tscn", "card_path": "res://assets/characters/Sonic/sonicrender.png", "tier": "Special"},
    {"id": 160, "name": "Mrbean", "path": "res://assets/characters/Mrbean/Mrbean.tscn", "card_path": "res://assets/characters/Mrbean/mrbeanrender.png", "tier": "Special"},
    {"id": 161, "name": "Joker", "path": "res://assets/characters/Joker/Joker.tscn", "card_path": "res://assets/characters/Joker/jokertex.png", "tier": "Special"},
    {"id": 162, "name": "Sattarkhan", "path": "res://assets/characters/Sattarkhan/Sattarkan.tscn", "card_path": "res://assets/characters/Sattarkhan/sattarkhanrender.png", "tier": "Special"},
    {"id": 163, "name": "Mohsenlor", "path": "res://assets/characters/Mohsenloretani/MohsenLor.tscn", "card_path": "res://assets/characters/Mohsenloretani/lorestanirender.png", "tier": "Special"},
    {"id": 164, "name": "Habbib", "path": "res://assets/characters/Habbib/Habbib.tscn", "card_path": "res://assets/characters/Habbib/Habbib_card.png", "tier": "Epic"},
    {"id": 165, "name": "Gigachad", "path": "res://assets/characters/Gigachad/Gigachad.tscn", "card_path": "res://assets/characters/Gigachad/gigarender.png", "tier": "Epic"},
    {"id": 166, "name": "Yeti", "path": "res://assets/characters/Yeti/Yeti.tscn", "card_path": "res://assets/characters/Yeti/yetirender.png", "tier": "Special"},
]

TIER_PRICE = {'Common': 1000, 'Rare': 3000, 'Legendary': 8000, 'Epic': 20000, 'Special': 50000}
EXACT_PRICE = {'Common': 1500, 'Rare': 4000, 'Legendary': 10000, 'Epic': 25000, 'Special': 50000}
STARTER_IDS = [1, 2, 3, 5, 7, 8]
# نوع شغل‌های انتظامی در JobManager (Gorohban..Bazras) — نیازمند مجوز پلیس
POLICE_JOB_TYPES = [16, 17, 18, 19, 20, 21, 22, 23]
VOICE_SECRET = os.environ.get('VOICE_SECRET', '')
GAME_SERVER_TOKEN = os.environ.get('GAME_SERVER_TOKEN', '').strip()
CLAN_LEVELS = [{'level': i, 'max_count': 10 + i * 10, 'price': 1000 * i} for i in range(1, 6)]
SYNC_PRICES = {
    'character_common': 1000, 'character_rare': 3000, 'character_legendary': 8000, 'character_epic': 20000,
    'character_common_exact': 1500, 'character_rare_exact': 4000, 'character_legendary_exact': 10000,
    'character_epic_exact': 25000, 'character_special_exact': 50000,
    'game_tax': 0, 'chat_cup': 0, 'change_name_price': 0, 'animation_price': 500,
    'coin_transfer_fee': 0, 'day_start_hour': 7, 'night_start_hour': 19,
    'reward_video_coins': 50, 'reward_video_hp': 20,
    'force_update_from_url': False, 'update_store_url': '',
    'voice_call_price': 50, 'voice_call_per_minute': 60,
    'force_version': 0, 'last_version': 0,
    'game_is_down': False, 'up_counter': 0,
}

_lock = threading.Lock()
state = {'accounts': {}, 'tokens': {}, 'userCounter': 0, 'servers': {'race': [], 'freeride': []}, 'serverCounter': 0, 'clans': []}

def log(msg):
    try:
        print('[' + time.strftime('%H:%M:%S') + '] ' + str(msg), flush=True)
    except Exception:
        pass

def _backfill_ids():
    ids = state.setdefault('num_ids', {})
    n = int(state.get('numCounter', 0) or 0)
    for un, acct in state['accounts'].items():
        if un not in ids:
            n += 1
            ids[un] = n
        acct['num_id'] = ids[un]
    state['numCounter'] = max(n, len(ids))


def save_state():
	tmp_file = STATE_FILE + '.tmp'
	try:
		os.makedirs(DATA_DIR, exist_ok=True)
		with open(tmp_file, 'w', encoding='utf-8') as fp:
			json.dump(state, fp)
			fp.flush()
			os.fsync(fp.fileno())
		os.replace(tmp_file, STATE_FILE)
	except Exception:
		pass


def load_state():
	try:
		with open(STATE_FILE, 'r', encoding='utf-8') as fp:
			loaded = json.load(fp)
		if not isinstance(loaded, dict):
			return
		state.update(loaded)
		state.setdefault('accounts', {})
		state.setdefault('tokens', {})
		state.setdefault('servers', {'race': [], 'freeride': []})
		state.setdefault('clans', [])
		for username, account in state['accounts'].items():
			account.setdefault('username', username)
			account.setdefault('handle', username)
			account.setdefault('characters', [dict(char) for char in CHARS if int(char['id']) in STARTER_IDS])
			account.setdefault('data', {})
	except (OSError, ValueError, TypeError) as exc:
		log('Could not load saved state: ' + str(exc))

def _ensure_chat():
    if 'chat' not in state:
        state['chat'] = {'next': 1, 'rooms': {}}


def new_account(username):
    state['userCounter'] += 1
    return {
        'username': username,
        'handle': 'Player' + str(state['userCounter']),
        'coin': 100000,
        'cup': 0, 'crown': 0, 'win_count': 0, 'game_count': 0,
        'hunger': 100, 'warmth': 100,
        'title': '', 'title_color': '',
        'is_test': False, 'name_changed_count': 0, 'show_debug': False,
        'ban_time': 0, 'free_admin': False, 'bazras': False, 'stealth': False, 'chat_admin': False,
        'jail_time': 0, 'in_prison': False,
        'email': '', 'daily_claim_time': 0,
        'progress_level': 1, 'is_meta_progress_finished': True,
        'characters': [dict(c) for c in CHARS if int(c['id']) in STARTER_IDS],
        'purchases': [], 'animations': {}, 'data': {}, 'clan_id': None,
        'job_stats': {'menu': 0, 'cook': 0, 'deliver': 0, 'clean': 0, 'visit': 0, 'heal': 0, 'cash': 0, 'policeKill': 0, 'arrest': 0, 'policeReport': 0, 'policeReportNormal': 0},
        'police_license': False, 'police_q': None, 'police_score': 0,
    }

def account_for(token):
	if not isinstance(token, str) or not token:
		return None
	username = state.setdefault('tokens', {}).get(token)
	if username is None:
		return None
	return state.setdefault('accounts', {}).get(username)

def get_char(cid):
    for c in CHARS:
        if c['id'] == cid:
            return c
    return None

_MEMBER_KEYS = ['cup','coin','crown','email','daily_claim_time','hunger','warmth','title','title_color','is_test','name_changed_count','show_debug','ban_time','free_admin','bazras','police_license','police_score','stealth','chat_admin','jail_time','in_prison','progress_level','is_meta_progress_finished','win_count','game_count']


PHONES = [
    {'id': 1, 'name': 'Nokia 1201', 'motto': 'Iconic Brick', 'price': 0, 'scene_path': 'res://Scenes/Mobile/Phones/1201/Nokia1201.tscn'},
    {'id': 2, 'name': 'Poco X6', 'motto': 'Power Player', 'price': 5000, 'scene_path': 'res://Scenes/Mobile/Phones/PocoX6/PocoX6.tscn'},
    {'id': 3, 'name': 'iPhone 16 Pro Max', 'motto': 'Pro Style', 'price': 15000, 'scene_path': 'res://Scenes/Mobile/Phones/iPhone/iPhone16ProMax.tscn'},
    {'id': 4, 'name': 'Galaxy S24 Ultra', 'motto': 'Flagship', 'price': 25000, 'scene_path': 'res://Scenes/Mobile/Phones/S24Ultra/S24Ultra.tscn'},
]

PROGRESS = [
    {'level': 1, 'progress_type': 'GameCount', 'game_count': 3, 'cup': 0, 'prize_type': 'Coin', 'prize_coin': 3000, 'prize_character': None},
    {'level': 2, 'progress_type': 'Cup', 'cup': 10, 'game_count': 3, 'prize_type': 'Coin', 'prize_coin': 5000, 'prize_character': None},
    {'level': 3, 'progress_type': 'GameCount', 'game_count': 10, 'cup': 10, 'prize_type': 'Coin', 'prize_coin': 8000, 'prize_character': None},
    {'level': 4, 'progress_type': 'Cup', 'cup': 30, 'game_count': 10, 'prize_type': 'Character', 'prize_coin': 0, 'prize_character': CHARS[5]},
    {'level': 5, 'progress_type': 'WinCount', 'game_count': 5, 'cup': 30, 'prize_type': 'Coin', 'prize_coin': 12000, 'prize_character': None},
    {'level': 6, 'progress_type': 'Cup', 'cup': 60, 'game_count': 5, 'prize_type': 'Character', 'prize_coin': 0, 'prize_character': CHARS[15]},
    {'level': 7, 'progress_type': 'GameCount', 'game_count': 25, 'cup': 60, 'prize_type': 'Coin', 'prize_coin': 20000, 'prize_character': None},
    {'level': 8, 'progress_type': 'Cup', 'cup': 100, 'game_count': 25, 'prize_type': 'Character', 'prize_coin': 0, 'prize_character': CHARS[40]},
]


def _prog_met(a, pr):
    t = pr.get('progress_type')
    if t == 'Cup':
        return a.get('cup', 0) >= pr.get('cup', 0)
    if t == 'GameCount':
        return a.get('game_count', 0) >= pr.get('game_count', 0)
    if t == 'WinCount':
        return a.get('win_count', 0) >= pr.get('game_count', 0)
    return False


def current_progress(a):
    for pr in PROGRESS:
        if not _prog_met(a, pr):
            return pr
    return None


def member_json(a):
    out = {'id': a['username'], 'nid': a.get('num_id', 0), 'handle': a['handle']}
    for k in _MEMBER_KEYS:
        out[k] = a.get(k)
    cur = current_progress(a)
    out['progress_level'] = cur if cur is not None else PROGRESS[-1]
    out['is_meta_progress_finished'] = cur is None
    return out



def rank_rows(sort_key):
    rows = []
    for a in state['accounts'].values():
        if a.get('hide_leaderboard'):
            continue
        last_char = (a.get('characters') or [CHARS[0]])[-1]
        rows.append({'id': a['username'], 'handle': a['handle'], 'name': a['handle'], 'cup': a['cup'], 'coin': a['coin'], 'crown': a['crown'], 'win_count': a['win_count'], 'num_chars': len(a.get('characters', [])), 'value': a.get(sort_key, 0), 'count': a.get(sort_key, 0), 'title': a.get('title', ''), 'rank': 0, 'character': last_char.get('path', CHARS[0]['path']), 'path': last_char.get('path', CHARS[0]['path']), 'card_path': last_char.get('card_path', CHARS[0]['card_path'])})
    rows.sort(key=lambda r: r.get(sort_key, 0), reverse=True)
    rows = rows[:50]
    for i, r in enumerate(rows):
        r['rank'] = i + 1
    return rows


def _load_admin_html():
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admin_panel.html'), 'r', encoding='utf-8') as fp:
            return fp.read()
    except Exception:
        return '<!DOCTYPE html><html dir="rtl"><body style="font-family:sans-serif"><h1>Animal Admin</h1><p>admin_panel.html not found next to the server.</p></body></html>'


ADMIN_HTML = _load_admin_html()


def _find_account(key):
    if key is None:
        return None
    k = str(key)
    if k in state['accounts']:
        return state['accounts'][k]
    try:
        n = int(float(k))
    except Exception:
        return None
    for acct in state['accounts'].values():
        if state.get('num_ids', {}).get(acct['username']) == n:
            return acct
    for acct in state['accounts'].values():
        if acct.get('num_id') == n or acct.get('id') == n:
            return acct
    return None


ADMIN_ACTOR = 'ادمین (کلید)'


def _admin_ok(body):
    key = os.environ.get('ADMIN_KEY', '')
    candidate = str((body or {}).get('key') or '')
    # compare_digest raises TypeError on non-ASCII str, so compare UTF-8 bytes.
    return bool(key) and hmac.compare_digest(candidate.encode('utf-8'), key.encode('utf-8'))


def _online_count():
    cutoff = int(time.time()) - 150
    return sum(
        1 for account in state.get('accounts', {}).values()
        if int(account.get('presence_updated_at', 0) or 0) >= cutoff
    )


def _prune_game_servers(now=None):
    now = int(time.time()) if now is None else int(now)
    ttl = max(15, int(os.environ.get('GAME_SERVER_TTL', '45')))
    servers = state.setdefault('servers', {'race': [], 'freeride': []})
    removed = 0
    for mode in ('race', 'freeride'):
        current = servers.setdefault(mode, [])
        alive = [server for server in current if now - int(server.get('updated_at', 0) or 0) <= ttl]
        removed += len(current) - len(alive)
        servers[mode] = alive
    if removed:
        save_state()


def _find_server(server_id):
    try:
        numeric_id = int(server_id)
    except (TypeError, ValueError):
        return None
    _prune_game_servers()
    for collection in state.setdefault('servers', {}).values():
        for server in collection:
            if int(server.get('id', -1)) == numeric_id:
                return server
    return None


def _server_owned_by(server, account):
    return bool(server and account and (
        server.get('owner_id') == account.get('username') or account.get('free_admin')
    ))


def _is_hidden(server):
    # HIDDEN_SERVERS="host-part;host-part": matching lobbies are never offered to players.
    if server.get('hidden'):
        return True
    ip = str(server.get('ip', ''))
    for needle in os.environ.get('HIDDEN_SERVERS', '').split(';'):
        needle = needle.strip()
        if needle and needle in ip:
            return True
    return False


def _visible_to(server, account):
    # Lobbies with an allowed list are only offered to those players (and the owner).
    allowed = server.get('allowed') or []
    if not allowed:
        return True
    if not account:
        return False
    return account.get('username') in allowed or account.get('username') == server.get('owner_id')


def _server_name(mode, ip, sid):
    # SERVER_NAMES="host-part=Display Name;host-part=Display Name"
    # The first entry whose host-part appears in the registered address wins.
    for pair in os.environ.get('SERVER_NAMES', '').split(';'):
        if '=' not in pair:
            continue
        needle, label = pair.split('=', 1)
        needle, label = needle.strip(), label.strip()
        if needle and label and needle in ip:
            return label
    return ('FreeRide ' if mode == 'FreeRide' else 'Race ') + 'Server ' + str(sid)


def _public_server(server):
    public = dict(server)
    public['has_password'] = bool(server.get('password_hash'))
    public.pop('password_hash', None)
    public.pop('owner_id', None)
    public.pop('updated_at', None)
    return public


def _friend_row(first, second, requester):
    now = int(time.time())

    def public_member(member):
        online = int(member.get('presence_updated_at', 0) or 0) >= now - 150
        return {
            'username': member['username'],
            'handle': member.get('handle', ''),
            'online': online,
            'presence': member.get('presence', '') if online else '',
            'presence_data': member.get('presence_data', '') if online else '',
        }

    first_public = public_member(first)
    second_public = public_member(second)
    return {
        'id': first['username'] + ':' + second['username'],
        'member1_username': first_public['username'],
        'member1_handle': first_public['handle'],
        'member1_online': first_public['online'],
        'member1_presence': first_public['presence'],
        'member1_presence_data': first_public['presence_data'],
        'member2_username': second_public['username'],
        'member2_handle': second_public['handle'],
        'member2_online': second_public['online'],
        'member2_presence': second_public['presence'],
        'member2_presence_data': second_public['presence_data'],
        'is_online': second_public['online'] if requester is first else first_public['online'],
        'handle': second_public['handle'] if requester is first else first_public['handle'],
        'username': second_public['username'] if requester is first else first_public['username'],
    }


def _voice_jwt(claims, secret):
    def encode(value):
        payload = json.dumps(value, separators=(',', ':')).encode('utf-8')
        return base64.urlsafe_b64encode(payload).rstrip(b'=').decode('ascii')

    message = encode({'alg': 'HS256', 'typ': 'JWT'}) + '.' + encode(claims)
    digest = hmac.new(secret.encode('utf-8'), message.encode('ascii'), hashlib.sha256).digest()
    return message + '.' + base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')


def _livekit_user_token(identity, name, room_name):
    api_key = os.environ.get('LIVEKIT_API_KEY', '').strip()
    api_secret = os.environ.get('LIVEKIT_API_SECRET', '').strip()
    if not api_key or not api_secret:
        return ''
    now = int(time.time())
    return _voice_jwt({
        'iss': api_key,
        'sub': identity,
        'name': name,
        'nbf': now - 5,
        'iat': now,
        'exp': now + 3600,
        'video': {
            'room': room_name,
            'roomJoin': True,
            'canPublish': True,
            'canSubscribe': True,
            'canPublishData': True,
        },
    }, api_secret)


def _livekit_admin_request(service, room_name, participant=''):
    livekit_url = os.environ.get('LIVEKIT_URL', '').strip()
    api_key = os.environ.get('LIVEKIT_API_KEY', '').strip()
    api_secret = os.environ.get('LIVEKIT_API_SECRET', '').strip()
    if not livekit_url or not api_key or not api_secret:
        return 503, {'error': 'voice service is not configured'}
    parsed = urlsplit(livekit_url)
    if parsed.scheme != 'https' or not parsed.hostname:
        return 503, {'error': 'voice service requires HTTPS'}

    now = int(time.time())
    token = _voice_jwt({
        'iss': api_key,
        'sub': 'animal-rush-backend',
        'nbf': now - 5,
        'iat': now,
        'exp': now + 60,
        'video': {'roomAdmin': True, 'roomCreate': True, 'roomList': True, 'roomRecord': True},
    }, api_secret)
    payload = {'room': room_name}
    if participant:
        payload['identity'] = participant
    connection = None
    try:
        connection = http.client.HTTPSConnection(parsed.hostname, parsed.port or 443, timeout=8)
        target = parsed.path.rstrip('/') + '/twirp/livekit.RoomService/' + service
        connection.request('POST', target, body=json.dumps(payload).encode('utf-8'), headers={
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        })
        response = connection.getresponse()
        response.read(65536)
        if response.status not in (200, 204):
            log('Voice service rejected ' + service + ': ' + str(response.status))
            return 502, {'error': 'voice service rejected the request'}
        return 200, {'ok': True}
    except OSError as exc:
        log('Voice service unavailable: ' + str(exc))
        return 502, {'error': 'voice service unavailable'}
    finally:
        if connection is not None:
            connection.close()


def admin_users():
    out = []
    ids = state.setdefault('num_ids', {})
    for i, (un, acct) in enumerate(state['accounts'].items()):
        out.append({
            'id': ids.get(un, 0),
            'username': un,
            'handle': acct.get('handle'),
            'coin': acct.get('coin', 0),
            'cup': acct.get('cup', 0),
            'title': acct.get('title', ''),
            'bazras': bool(acct.get('bazras')),
            'free_admin': bool(acct.get('free_admin')),
            'ban_time': acct.get('ban_time', 0),
            'police_license': bool(acct.get('police_license')),
            'hide_leaderboard': bool(acct.get('hide_leaderboard')),
            'online': False,
        })
    out.sort(key=lambda r: r['coin'], reverse=True)
    return out


def _log_event(kind, actor, target, detail=''):
    logs = state.setdefault('admin_log', [])
    nxt = int(state.get('admin_log_next', 1))
    state['admin_log_next'] = nxt + 1
    logs.append({'id': nxt, 'kind': kind, 'actor': str(actor or '?'), 'target': str(target or ''),
                 'detail': str(detail)[:200], 'time': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())})
    if len(logs) > 5000:
        del logs[0:len(logs) - 5000]


# ---- anti-abuse: limit how many accounts one network address can create ----
REGISTER_PER_IP_PER_DAY = max(1, int(os.environ.get('REGISTER_PER_IP_PER_DAY', '3')))
_register_hits = {}


def _client_ip(handler):
    # Behind Railway's proxy the real client is the first X-Forwarded-For entry.
    fwd = (handler.headers.get('X-Forwarded-For') or '').split(',')[0].strip()
    return fwd or handler.client_address[0]


def _register_allowed(ip):
    now = time.time()
    window = 24 * 3600
    hits = [t for t in _register_hits.get(ip, []) if now - t < window]
    if len(hits) >= REGISTER_PER_IP_PER_DAY:
        _register_hits[ip] = hits
        return False
    hits.append(now)
    _register_hits[ip] = hits
    if len(_register_hits) > 10000:
        for k in [k for k, v in _register_hits.items() if not v or now - v[-1] >= window]:
            _register_hits.pop(k, None)
    return True


def route_admin(path, body):
    if not _admin_ok(body):
        return 403, {'error': 'bad admin key'}
    if path == '/admin/users/':
        return 200, {'users': admin_users()}
    if path == '/admin/logs/':
        kinds = body.get('kinds') or []
        if isinstance(kinds, str):
            kinds = [kinds]
        user_f = str(body.get('user') or '').strip().lower()
        try:
            limit = max(1, min(500, int(body.get('limit') or 200)))
        except (TypeError, ValueError):
            limit = 200
        out = []
        for e in reversed(state.get('admin_log', [])):
            if kinds and e.get('kind') not in kinds:
                continue
            if user_f and user_f not in e.get('target', '').lower() and user_f not in e.get('actor', '').lower():
                continue
            out.append(e)
            if len(out) >= limit:
                break
        return 200, {'logs': out}
    if path == '/admin/server_rename/':
        s = _find_server(body.get('server_id'))
        if s is None:
            return 404, {'error': 'no such server'}
        new_name = str(body.get('name') or '').strip()[:40]
        if not new_name:
            return 400, {'error': 'name is empty'}
        s['name'] = new_name
        s['name_override'] = True
        _log_event('server_rename', ADMIN_ACTOR, s.get('name', ''), 'id=' + str(s.get('id')))
        save_state()
        return 200, {'ok': True}
    if path == '/admin/server_access/':
        s = _find_server(body.get('server_id'))
        if s is None:
            return 404, {'error': 'no such server'}
        raw = body.get('usernames') or []
        if isinstance(raw, str):
            raw = raw.replace('\n', ',').split(',')
        names = []
        for n in raw:
            n = str(n).strip()
            if n and n not in names:
                names.append(n[:64])
        s['allowed'] = names[:200]
        _log_event('server_access', ADMIN_ACTOR, s.get('name', ''), 'id=' + str(s.get('id')) + ' ' + str(len(names)) + ' نفر')
        save_state()
        return 200, {'ok': True, 'allowed': s['allowed']}
    if path == '/admin/server_hide/':
        s = _find_server(body.get('server_id'))
        if s is None:
            return 404, {'error': 'no such server'}
        s['hidden'] = bool(body.get('hidden'))
        _log_event('server_hide' if s['hidden'] else 'server_show', ADMIN_ACTOR, s.get('name', ''), 'id=' + str(s.get('id')))
        save_state()
        return 200, {'ok': True}
    if path == '/admin/chat/':
        _ensure_chat()
        room = str(body.get('room') or 'PublicChat')[:64]
        user_f = str(body.get('user') or '').strip().lower()
        msgs = state['chat']['rooms'].get(room, [])
        out = [m for m in msgs if not user_f or user_f in str(m.get('sender_id', '')).lower() or user_f in str(m.get('handle', '')).lower()]
        return 200, {'rooms': sorted(state['chat']['rooms'].keys()), 'messages': list(reversed(out))[:300]}
    if path == '/admin/servers/':
        _prune_game_servers()
        rows = []
        for mode_key in ('freeride', 'race'):
            for s in state.setdefault('servers', {}).setdefault(mode_key, []):
                rows.append({'id': s.get('id'), 'mode': s.get('mode'), 'name': s.get('name', ''), 'ip': s.get('ip', ''),
                             'players': s.get('players_joined', 0), 'max': s.get('max_players_start', 32),
                             'state': s.get('state', ''), 'hidden': _is_hidden(s), 'allowed': s.get('allowed', []), 'updated_at': s.get('updated_at', 0)})
        return 200, {'servers': rows}
    if path == '/admin/police/':
        calls = list(state.get('police_calls', []))
        return 200, {'calls': list(reversed(calls))[:300]}
    target = _find_account(body.get('id') or body.get('user_id') or body.get('username'))
    if target is None:
        return 404, {'error': 'no such user'}
    try:
        amount = int(body.get('amount') or 0)
    except (TypeError, ValueError):
        return 400, {'error': 'amount must be a whole number'}
    if path == '/admin/give_coin/':
        target['coin'] = int(target.get('coin', 0)) + amount
        _log_event('give_coin', ADMIN_ACTOR, target['username'], amount)
    elif path == '/admin/set_title/':
        target['title'] = str(body.get('title') or '')
        target['title_color'] = str(body.get('title_color') or 'FFFFFF')
        _log_event('set_title', ADMIN_ACTOR, target['username'], target['title'])
    elif path == '/admin/grant_bazras/':
        if body.get('value') is not None:
            target['bazras'] = bool(body.get('value'))
            _log_event('grant_bazras' if target['bazras'] else 'revoke_bazras', ADMIN_ACTOR, target['username'])
        if body.get('admin') is not None:
            target['free_admin'] = bool(body.get('admin'))
            _log_event('grant_admin' if target['free_admin'] else 'revoke_admin', ADMIN_ACTOR, target['username'])
        if body.get('value') is None and body.get('admin') is None:
            target['bazras'] = True
            _log_event('grant_bazras', ADMIN_ACTOR, target['username'])
    elif path == '/admin/ban/':
        hours = float(body.get('hours') or 1)
        target['ban_time'] = int(hours * 3600)
        _log_event('ban', ADMIN_ACTOR, target['username'], str(hours) + ' ساعت')
    elif path == '/admin/unban/':
        target['ban_time'] = 0
        _log_event('unban', ADMIN_ACTOR, target['username'])
    elif path == '/admin/set_coin/':
        target['coin'] = amount
        _log_event('set_coin', ADMIN_ACTOR, target['username'], amount)
    elif path == '/admin/set_cup/':
        target['cup'] = max(0, amount)
        _log_event('set_cup', ADMIN_ACTOR, target['username'], target['cup'])
    elif path == '/admin/leaderboard_hide/':
        target['hide_leaderboard'] = bool(body.get('hidden'))
        _log_event('leaderboard_hide' if target['hide_leaderboard'] else 'leaderboard_show', ADMIN_ACTOR, target['username'])
    elif path == '/admin/grant_police/':
        target['police_license'] = bool(body.get('value'))
        _log_event('grant_police' if target['police_license'] else 'revoke_police', ADMIN_ACTOR, target['username'])
    else:
        return 404, {'error': 'unknown admin route'}
    save_state()
    log('admin ' + path + ' -> ' + target['username'])
    return 200, {'coin': target.get('coin'), 'user': {'id': target.get('num_id', 0), 'username': target['username'], 'handle': target.get('handle'), 'title': target.get('title', ''), 'bazras': bool(target.get('bazras'))}}




# ================= clans / friends / phone  (/mobile/*) =================
CLAN_RANKS = ['Normal', 'Elder', 'Coleader', 'Leader']


def _clan_state():
    return state.setdefault('clans', [])


def _clan_by_id(cid):
    try:
        cid = int(cid)
    except Exception:
        return None
    for c in _clan_state():
        if int(c.get('id', 0)) == cid:
            return c
    return None


def _my_clan(a):
    cid = a.get('clan_id')
    if cid is None:
        return None
    return _clan_by_id(cid)


def _member_row(c, m, a, index):
    acct = state['accounts'].get(m.get('username'), {})
    return {
        'id': m.get('id'),
        'player_id': m.get('username'),
        'handle': acct.get('handle', m.get('handle', '?')),
        'cup': acct.get('cup', 0),
        'title': acct.get('title', ''),
        'rank': m.get('rank', 'Normal'),
        'index': index,
        'score': acct.get('cup', 0),
    }


def _clan_members(c, a):
    out = []
    for i, m in enumerate(c.get('members', [])):
        out.append(_member_row(c, m, a, i + 1))
    return out


def _clan_public(c):
    return {
        'id': c.get('id'),
        'name': c.get('name'),
        'level': c.get('level', 1),
        'badge_id': c.get('badge_id', 0),
        'type': c.get('type', 'Public'),
        'member_count': len(c.get('members', [])),
        'total_score': c.get('total_score', 0),
        'bank': c.get('bank', 0),
        'owner_id': c.get('owner_id'),
        'description': c.get('description', ''),
    }


def _add_to_clan(c, a, rank='Normal'):
    members = c.setdefault('members', [])
    for m in members:
        if m.get('username') == a['username']:
            return
    state['membershipCounter'] = int(state.get('membershipCounter', 0)) + 1
    members.append({'id': state['membershipCounter'], 'username': a['username'], 'handle': a.get('handle'), 'rank': rank})
    a['clan_id'] = c['id']


def _remove_from_clan(c, a):
    c['members'] = [m for m in c.get('members', []) if m.get('username') != a['username']]
    a['clan_id'] = None


def _clan_score(c):
    total = 0
    for m in c.get('members', []):
        acct = state['accounts'].get(m.get('username'))
        if acct:
            total += int(acct.get('cup', 0))
    c['total_score'] = total
    return total


def _clan_leaderboard(key):
    rows = []
    for c in _clan_state():
        _clan_score(c)
        rows.append(_clan_public(c))
    rows.sort(key=lambda r: r.get('bank' if key == 'bank' else 'total_score', 0), reverse=True)
    rows = rows[:50]
    for i, r in enumerate(rows):
        r['rank'] = i + 1
    return rows


def route_mobile(path, body, a):
    if a is None:
        return 401, {'error': 'unauthorized'}
    if path == '/mobile/list_clans/':
        return 200, {'clans': [_clan_public(c) for c in _clan_state()]}
    if path == '/mobile/search_clan/':
        q = str(body.get('query') or body.get('name') or '').strip().lower()
        out = [c for c in _clan_state() if not q or q in str(c.get('name', '')).lower()]
        return 200, {'clans': [_clan_public(c) for c in out]}
    if path == '/mobile/my_clan/':
        c = _my_clan(a)
        return 200, {'clan': _clan_public(c) if c else None}
    if path == '/mobile/clan_detail/':
        c = _clan_by_id(body.get('id'))
        if c is None:
            return 404, {}
        _clan_score(c)
        return 200, {'clan': _clan_public(c), 'members': _clan_members(c, a), 'score': c.get('total_score', 0)}
    if path == '/mobile/list_clan_members/':
        c = _clan_by_id(body.get('id')) or _my_clan(a)
        if c is None:
            return 200, {'members': []}
        return 200, {'members': _clan_members(c, a)}
    if path in ('/mobile/clan_leaderboard/', '/mobile/clan_bank_leaderboard/'):
        key = 'bank' if path.endswith('bank_leaderboard/') else 'score'
        return 200, {'clans': _clan_leaderboard(key)}
    if path == '/mobile/list_clan_transactions/':
        return 200, {'message': []}
    if path == '/mobile/create_clan/':
        name = str(body.get('name') or '').strip()[:24]
        if not name:
            return 400, {}
        price = CLAN_LEVELS[0]['price']
        if a['coin'] < price:
            return 402, {'coin': a['coin']}
        a['coin'] -= price
        state['clanCounter'] = int(state.get('clanCounter', 0)) + 1
        c = {'id': state['clanCounter'], 'name': name, 'level': 1, 'badge_id': int(body.get('badge_id') or 0),
             'type': str(body.get('type') or 'Public'), 'description': str(body.get('description') or '')[:80],
             'members': [], 'bank': 0, 'total_score': 0, 'owner_id': a['username']}
        _clan_state().append(c)
        _add_to_clan(c, a, 'Leader')
        save_state()
        return 200, {'clan': _clan_public(c), 'coin': a['coin']}
    if path == '/mobile/join_clan/':
        c = _clan_by_id(body.get('id'))
        if c is None:
            return 404, {}
        if a.get('clan_id') is not None and int(a['clan_id']) != int(c.get('id', -1)):
            return 409, {'error': 'leave your current clan first'}
        capacity = CLAN_LEVELS[min(max(int(c.get('level', 1)), 1), len(CLAN_LEVELS)) - 1]['max_count']
        if len(c.get('members', [])) >= capacity:
            return 409, {'error': 'clan is full'}
        if str(c.get('type', 'Public')).lower() == 'private':
            requested = c.setdefault('requests', [])
            if a['username'] not in requested:
                requested.append(a['username'])
                save_state()
            return 202, {'requested': True, 'clan': _clan_public(c)}
        _add_to_clan(c, a, 'Normal')
        save_state()
        return 200, {'joined': True, 'clan': _clan_public(c)}
    if path == '/mobile/leave_clan/':
        c = _my_clan(a)
        if c is not None:
            _remove_from_clan(c, a)
            if not c.get('members'):
                _clan_state().remove(c)
            save_state()
        return 200, {}
    if path == '/mobile/update_clan/':
        c = _my_clan(a)
        if c is None:
            return 404, {}
        member = next((m for m in c.get('members', []) if m.get('username') == a['username']), None)
        if not member or member.get('rank') not in ('Leader', 'Coleader'):
            return 403, {'error': 'clan leader permission required'}
        if body.get('name'):
            c['name'] = str(body.get('name'))[:24]
        if body.get('badge_id') is not None:
            c['badge_id'] = int(body.get('badge_id') or 0)
        if body.get('type'):
            c['type'] = str(body.get('type'))
        if body.get('description') is not None:
            c['description'] = str(body.get('description'))[:80]
        save_state()
        return 200, {'clan': _clan_public(c)}
    if path == '/mobile/update_clan_membership/':
        c = _my_clan(a)
        if c is None:
            return 404, {}
        actor = next((m for m in c.get('members', []) if m.get('username') == a['username']), None)
        if not actor or actor.get('rank') not in ('Leader', 'Coleader'):
            return 403, {'error': 'clan moderation permission required'}
        mid = body.get('membership_id') or body.get('id')
        valid_ranks = ('Normal', 'Elder', 'Coleader', 'Leader')
        if body.get('rank') and str(body['rank']) not in valid_ranks:
            return 400, {'error': 'invalid clan rank'}
        for m in list(c.get('members', [])):
            if str(m.get('id')) == str(mid):
                if m.get('rank') == 'Leader' and actor.get('rank') != 'Leader':
                    return 403, {'error': 'only the clan leader can change the leader'}
                if body.get('rank'):
                    m['rank'] = str(body.get('rank'))
                if body.get('kick'):
                    c['members'].remove(m)
                    t = state['accounts'].get(m.get('username'))
                    if t:
                        t['clan_id'] = None
                break
        save_state()
        return 200, {'members': _clan_members(c, a)}
    if path in ('/mobile/upgrade_clan/', '/mobile/upgrade_clan_with_bank/'):
        c = _my_clan(a)
        if c is None:
            return 404, {}
        lvl = int(c.get('level', 1))
        if lvl >= len(CLAN_LEVELS):
            return 400, {}
        price = CLAN_LEVELS[lvl]['price']
        if path.endswith('with_bank/'):
            if int(c.get('bank', 0)) < price:
                return 400, {}
            c['bank'] = int(c.get('bank', 0)) - price
        else:
            if a['coin'] < price:
                return 400, {}
            a['coin'] -= price
        c['level'] = lvl + 1
        save_state()
        return 200, {'clan': _clan_public(c), 'coin': a['coin']}
    if path == '/mobile/deposit_clan_bank/':
        c = _my_clan(a)
        if c is None:
            return 404, {}
        amt = max(0, int(body.get('amount') or body.get('coin') or 0))
        if a['coin'] < amt:
            return 400, {}
        a['coin'] -= amt
        c['bank'] = int(c.get('bank', 0)) + amt
        save_state()
        return 200, {'coin': a['coin'], 'clan': _clan_public(c)}
    if path == '/mobile/list_friends/':
        out = []
        for friendship in state.setdefault('friendships', []):
            if not friendship.get('accepted'):
                continue
            first = state['accounts'].get(friendship.get('from'))
            second = state['accounts'].get(friendship.get('to'))
            if not first or not second or a['username'] not in (first['username'], second['username']):
                continue
            other = second if a['username'] == first['username'] else first
            row = _friend_row(first, second, first if a['username'] == first['username'] else second)
            row.update({'player_id': other['username'], 'cup': other.get('cup', 0), 'title': other.get('title', '')})
            out.append(row)
        return 200, {'friends': out}
    if path == '/mobile/change_friendship/':
        friendship_id = str(body.get('friendship_id') or body.get('id') or '')
        operation = str(body.get('type') or 'delete').lower()
        friendships = state.setdefault('friendships', [])
        target = next((f for f in friendships if str(f.get('id')) == friendship_id), None)
        if target is None or a['username'] not in (target.get('from'), target.get('to')):
            return 404, {'error': 'friend request not found'}
        if operation == 'accept' and target.get('to') == a['username']:
            target['accepted'] = True
            target['accepted_at'] = int(time.time())
            save_state()
            return 200, {'accepted': True}
        if operation in ('delete', 'reject'):
            friendships.remove(target)
            save_state()
            return 200, {'deleted': True}
        return 403, {'error': 'cannot accept this request'}
    if path == '/mobile/invite_friend/':
        identifier = str(body.get('input') or body.get('player_id') or body.get('username') or '').strip()
        recipient = state['accounts'].get(identifier)
        if recipient is None:
            for account in state['accounts'].values():
                if str(account.get('num_id')) == identifier or account.get('handle', '').casefold() == identifier.casefold():
                    recipient = account
                    break
        if recipient is None or recipient['username'] == a['username']:
            return 404, {'error': 'player not found'}
        friendships = state.setdefault('friendships', [])
        existing = next((f for f in friendships if {f.get('from'), f.get('to')} == {a['username'], recipient['username']}), None)
        if existing:
            return (200, {'accepted': True} if existing.get('accepted') else {'pending': True})
        if len(a.setdefault('friends', [])) >= 100:
            return 401, {'error': 'friend limit reached'}
        friendship = {
            'id': 'friend_' + str(state.setdefault('membershipCounter', 0) + 1),
            'from': a['username'],
            'to': recipient['username'],
            'accepted': False,
            'created_at': int(time.time()),
        }
        state['membershipCounter'] = int(state['membershipCounter']) + 1
        friendships.append(friendship)
        save_state()
        return 200, {'ok': True, 'friendship_id': friendship['id']}
    if path == '/mobile/list_invites/':
        invites = []
        for friendship in state.setdefault('friendships', []):
            if friendship.get('accepted') or friendship.get('to') != a['username']:
                continue
            sender = state['accounts'].get(friendship.get('from'))
            target = state['accounts'].get(friendship.get('to'))
            if sender and target:
                row = _friend_row(sender, target, target)
                row['id'] = friendship['id']
                row['friendship_id'] = friendship['id']
                invites.append(row)
        return 200, {'invites': invites, 'friends': invites}
    if path == '/mobile/purchase_mobile/':
        pid = int(body.get('id') or 0)
        ph = None
        for item in PHONES:
            if int(item['id']) == pid:
                ph = item
                break
        if ph is None:
            return 400, {}
        price = int(ph.get('price') or 0)
        if a['coin'] < price:
            return 400, {'coin': a['coin']}
        a['coin'] -= price
        save_state()
        return 200, {'coin': a['coin'], 'mobile_id': pid}
    if path == '/mobile/update_mobile_color/':
        a['mobile_color'] = int(body.get('color') or 0)
        save_state()
        return 200, {}
    return 200, {}


def route(path, body, a):
    now = int(time.time())
    server_routes = {
        '/game/register/', '/game/update/', '/game/start_game/',
        '/game/finish_game/', '/game/select_map/',
    }
    server_authorized = body.pop('_game_server_authorized', False) is True
    if path in server_routes:
        if GAME_SERVER_TOKEN and not server_authorized:
            return 403, {'error': 'invalid game server token'}
    # ---- account ----
    if path == '/account/register/':
        state['userCounter'] += 1
        rnd = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(5))
        username = 'u' + str(state['userCounter']) + '_' + rnd
        acct = new_account(username)
        nid = state.setdefault('numCounter', 0) + 1
        state['numCounter'] = nid
        state.setdefault('num_ids', {})[username] = nid
        acct['num_id'] = nid
        state['accounts'][username] = acct
        tok = 'T' + username + '.' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(10))
        state['tokens'][tok] = username
        save_state()
        log('register -> ' + username)
        return 200, {'handle': acct['handle'], 'token': tok, 'username': username, 'id': nid}
    if path.startswith('/mobile/'):
        return route_mobile(path, body, a)
    if a is None and not (path in server_routes and server_authorized):
        return 401, {'error': 'unauthorized'}
    if path == '/account/sync/':
        a['presence_updated_at'] = now
        return 200, {'data': {'data': a.get('data', {})}, 'member': member_json(a), 'characters': a['characters'], 'sync': SYNC_PRICES, 'online_count': _online_count(), 'public_chat': 'PublicChat', 'progresses': PROGRESS, 'phones': PHONES, 'clan': (_clan_public(_my_clan(a)) if _my_clan(a) else None), 'clan_levels': CLAN_LEVELS}
    if path == '/account/save_data/':
        jwt = a.get('data', {}).get('JWT') if isinstance(a.get('data'), dict) else None
        a['data'] = body
        if jwt:
            a['data']['JWT'] = jwt
        if body.get('hunger') is not None:
            a['hunger'] = body.get('hunger')
        if body.get('warmth') is not None:
            a['warmth'] = body.get('warmth')
        save_state()
        return 200, {}
    if path == '/account/change_handle/':
        if body.get('handle'):
            a['handle'] = str(body.get('handle'))[:12]
        save_state()
        return 200, {}
    if path == '/account/am_i_ban/':
        return 200, {'member': {'ban_time': a['ban_time'], 'coin': a['coin'], 'title': a['title'], 'title_color': a['title_color'], 'jail_time': a['jail_time'], 'in_prison': a['in_prison']}}
    if path == '/account/update_presence/':
        a['presence'] = str(body.get('presence') or '')[:64]
        a['presence_data'] = str(body.get('presence_data') or '')[:128]
        a['presence_updated_at'] = now
        save_state()
        return 200, {'ok': True, 'online_count': _online_count()}
    if path in ('/account/tutorial_started/', '/account/tutorial_finished/', '/account/nakama_connect/', '/account/server_test_fail/', '/game/request_error/'):
        return 200, {}
    if path == '/account/request_code/':
        return 503, {'error': 'email verification service is not configured'}
    if path == '/account/verify_code/':
        return 503, {'error': 'email verification service is not configured'}
    if path == '/account/remove_email/':
        a['email'] = ''
        save_state()
        return 200, {}
    if path == '/account/claim_progress_prize/':
        cur = current_progress(a)
        lvl = int(body.get('level') or (cur['level'] if cur else 0))
        target = None
        for pr in PROGRESS:
            if pr['level'] == lvl:
                target = pr
                break
        claimed = a.setdefault('progress_claimed', [])
        if target is None or lvl in claimed or not _prog_met(a, target):
            return 409, {'coin': a['coin'], 'ok': False, 'error': 'progress milestone is unavailable or already claimed'}
        claimed.append(lvl)
        prize_type = str(target.get('prize_type') or 'Coin').lower()
        prize_coin = 0
        character = None
        if target.get('prize_type') == 'Coin':
            prize_coin = int(target.get('prize_coin') or 0)
            a['coin'] += prize_coin
        elif target.get('prize_type') == 'Character' and target.get('prize_character'):
            character = dict(target['prize_character'])
            if not any(int(owned.get('id', -1)) == int(character.get('id', -2)) for owned in a['characters']):
                a['characters'].append(character)
        next_progress = current_progress(a)
        save_state()
        return 200, {
            'coin': a['coin'], 'ok': True,
            'is_finished': next_progress is None,
            'progress': next_progress if next_progress is not None else PROGRESS[-1],
            'type': prize_type, 'prize_coin': prize_coin, 'character': character,
        }
    if path == '/account/ami_content_creator/':
        is_creator = bool(a.get('content_creator'))
        return 200, {
            'content_creator': is_creator,
            'is_creator': is_creator,
            'referer_count': int(a.get('referer_count', 0)),
            'code': a.get('creator_code', ''),
            'meta': a.get('referer_meta'),
        }
    if path == '/account/content_creator_stats/':
        return 200, {
            'is_coin': True,
            'count': int(a.get('creator_sales_count', 0)),
            'coins': int(a.get('creator_coins', 0)),
            'stats': {},
            'total_sells_count': int(a.get('creator_sales_count', 0)),
            'total_revenue': int(a.get('creator_coins', 0)),
        }
    if path == '/account/coin_creator_cashout/':
        coins = int(a.get('creator_coins', 0))
        if coins <= 0:
            return 400, {'error': 'no creator balance'}
        a['coin'] = int(a.get('coin', 0)) + coins
        a['creator_coins'] = 0
        save_state()
        return 200, {'coin': a['coin']}
    if path == '/account/refer_content_creator/':
        code = str(body.get('code') or '').strip()[:64]
        if not code:
            return 400, {'error': 'missing creator code'}
        creator = next((account for account in state['accounts'].values() if account.get('creator_code') == code), None)
        if creator is None or creator is a:
            return 400, {'error': 'invalid creator code'}
        a['referer_meta'] = {'referer_code': code, 'referer_handle': creator.get('handle', '')}
        creator['referer_count'] = int(creator.get('referer_count', 0)) + 1
        save_state()
        return 200, {'ok': True}
    # ---- shop ----
    if path == '/shop/list_shop/':
        return 200, {'gateway_type': 'IAP', 'items': [], 'phones': PHONES}
    if path == '/shop/verify_purchase/':
        return 503, {'error': 'purchase verification service is not configured'}
    if path == '/shop/ipg/':
        return 400, {}
    if path == '/shop/list_gifts/':
        return 200, {'gifts': []}
    if path == '/shop/seen_gifts/':
        return 200, {}
    if path == '/shop/daily_reward/':
        if a['daily_claim_time'] and now - a['daily_claim_time'] < 24 * 3600:
            return 200, {'prize': 0, 'coins': a['coin']}
        prize = random.choice([50, 60, 70, 80, 90, 95, 100, 200])
        a['coin'] += prize
        a['daily_claim_time'] = now
        save_state()
        return 200, {'prize': prize, 'coins': a['coin']}
    if path == '/shop/unlock_new_character_v2/':
        tier = str(body.get('tier') or 'Common')
        price = TIER_PRICE.get(tier, 1000)
        owned = set(int(c['id']) for c in a['characters'])
        pool = [c for c in CHARS if c['tier'] == tier and int(c['id']) not in owned]
        if not pool:
            return 400, {'error': 'all owned'}
        if a['coin'] < price:
            return 400, {'coin': a['coin']}
        c = random.choice(pool)
        a['coin'] -= price
        a['characters'].append(dict(c))
        save_state()
        return 200, {'coin': a['coin'], 'character': dict(c)}
    if path == '/shop/unlock_exact_character/':
        c = get_char(int(body.get('character_id') or 0))
        if not c:
            return 400, {}
        if any(x['id'] == c['id'] for x in a['characters']):
            return 401, {}
        price = EXACT_PRICE.get(c['tier'], 1500)
        if a['coin'] < price:
            return 400, {'coin': a['coin']}
        a['coin'] -= price
        a['characters'].append(dict(c))
        save_state()
        return 200, {'coin': a['coin'], 'character': dict(c)}
    if path == '/shop/unlock_animation/':
        return 200, {'character_id': body.get('character_id'), 'coin': a['coin'], 'unlocks': []}
    if path == '/game/purchase_with_coin/':
        price = max(0, int(body.get('price') or 0))
        if a['coin'] < price:
            return 400, {'coin': a['coin']}
        a['coin'] -= price
        save_state()
        return 200, {'coin': a['coin']}
    if path == '/game/add_coin/':
        value = int(body.get('value') or 0)
        kind = str(body.get('type') or 'general')
        limits = {
            'RewardVideo': int(SYNC_PRICES.get('reward_video_coins', 50)),
            'Chest': 500,
            'CannonDart': 5000,
            'XO': 5000,
            'RPS': 5000,
            'BattleHeroes': 5000,
            'Salary': 100000,
        }
        if value < 0 or kind not in limits or value > limits[kind]:
            return 400, {'error': 'invalid coin reward'}
        a['coin'] += value
        save_state()
        return 200, {'coin': a['coin']}
    if path == '/police/jail_reduce/':
        red = max(0, int(body.get('reduce') or 0))
        price = max(0, int(body.get('price') or 0))
        if price and a['coin'] < price:
            return 400, {'coin': a['coin']}
        a['coin'] -= price
        a['jail_time'] = max(0, int(a.get('jail_time') or 0) - red)
        if a['jail_time'] <= 0:
            a['in_prison'] = False
        save_state()
        return 200, {'coin': a['coin'], 'jail_time': a['jail_time']}
    if path == '/game/job_done/':
        s = a.setdefault('job_stats', {})
        job = str(body.get('job') or '')
        if job in s:
            s[job] = int(s[job]) + 1
        save_state()
        return 200, {'stats': s}
    if path == '/game/finish_game/':
        key = str(body.get('game_id') or body.get('container_id') or '')
        game = state.setdefault('games', {}).get('match:' + key)
        if game is None:
            return 404, {'error': 'game not found'}
        if not game.get('finished'):
            results = {}
            for participant in body.get('ids', []):
                account = state.setdefault('accounts', {}).get(str(participant.get('id') or ''))
                if account is None:
                    continue
                try:
                    rank = int(participant.get('rank', -1))
                except (TypeError, ValueError):
                    rank = -1
                coin = 50 if rank >= 0 else 0
                cup = 10 if rank == 1 else (5 if 1 < rank <= 3 else (1 if rank > 3 else 0))
                crown = 1 if rank == 1 else 0
                account['game_count'] = int(account.get('game_count', 0)) + 1
                account['coin'] = int(account.get('coin', 0)) + coin
                account['cup'] = int(account.get('cup', 0)) + cup
                account['crown'] = int(account.get('crown', 0)) + crown
                if rank == 1:
                    account['win_count'] = int(account.get('win_count', 0)) + 1
                results[account['username']] = {'coin': coin, 'cup': cup, 'crown': crown, 'rank': rank}
            game['results'] = results
            game['finished'] = True
            game['finished_at'] = now
            save_state()
        return 200, {'ok': True}
    if path == '/game/change_server_password/':
        server = _find_server(body.get('server_id') or body.get('id'))
        if server is None:
            return 404, {'error': 'server not found'}
        if not _server_owned_by(server, a):
            return 403, {'error': 'server owner permission required'}
        password = str(body.get('new_password') or '')
        if password and len(password) < 3:
            return 400, {'error': 'password must contain at least 3 characters'}
        server['password_hash'] = hashlib.sha256(password.encode('utf-8')).hexdigest() if password else ''
        save_state()
        return 200, {'ok': True}
    if path == '/game/contact_us/':
        return 200, {}
    if path == '/game/redeem/':
        return 400, {}
    if path == '/game/my_job_stats/':
        s = a.get('job_stats') or {}
        rest = int(s.get('menu', 0)) + int(s.get('cook', 0)) + int(s.get('deliver', 0)) + int(s.get('clean', 0))
        hosp = int(s.get('visit', 0)) + int(s.get('heal', 0))
        bank = int(s.get('cash', 0))
        police = int(s.get('policeKill', 0)) + int(s.get('arrest', 0)) + int(s.get('policeReport', 0)) + int(s.get('policeReportNormal', 0))
        return 200, {'coin': a['coin'], 'restaurant': rest, 'hospital': hosp, 'bank': bank, 'police': police, 'stats': s}
    if path == '/game/hire_me/':
        job = body.get('job') or {}
        if not isinstance(job, dict):
            return 400, {'error': 'invalid job'}
        try:
            price = int(body.get('price') or 0)
        except (TypeError, ValueError, OverflowError):
            return 400, {'error': 'invalid job price'}
        if price < 0:
            return 400, {'error': 'invalid job price'}
        title = str(job.get('title') or '')
        try:
            jtype = int(job.get('type'))
        except Exception:
            jtype = -1
        if jtype in POLICE_JOB_TYPES and not a.get('police_license'):
            return 410, {'license': False}
        if 'title' not in job:
            return 400, {'coin': a['coin'], 'error': 'missing job title'}
        if a['coin'] < price:
            return 400, {'coin': a['coin']}
        a['coin'] -= price
        a['title'] = title
        a['title_color'] = str(job.get('color') or 'FFFFFF')
        stats = a.setdefault('job_stats', {})
        if not body.get('promote'):
            for k in stats:
                stats[k] = 0
        save_state()
        log('hire_me ' + a['username'] + ' -> ' + title)
        return 200, {'coin': a['coin'], 'ok': True, 'title': title}
    if path == '/game/transfer_money/':
        try:
            amount = int(body.get('amount') or body.get('coin') or 0)
        except (TypeError, ValueError, OverflowError):
            return 400, {'error': 'invalid transfer amount'}
        target_key = str(body.get('username') or body.get('receiver') or body.get('to') or body.get('handle') or '')
        fee = int(SYNC_PRICES.get('coin_transfer_fee', 0))
        if amount <= 0 or a['coin'] < amount + fee:
            return 400, {'coin': a['coin']}
        target = state['accounts'].get(target_key)
        if target is None:
            for acct in state['accounts'].values():
                if acct.get('handle') == target_key:
                    target = acct
                    break
        if target is None or target is a:
            return 404, {'coin': a['coin']}
        a['coin'] -= amount + fee
        target['coin'] = int(target.get('coin', 0)) + amount
        a.setdefault('transactions', []).append({'type': 'out', 'amount': amount, 'to': target.get('handle')})
        target.setdefault('transactions', []).append({'type': 'in', 'amount': amount, 'from': a.get('handle')})
        save_state()
        return 200, {'coin': a['coin']}
    if path == '/game/fetch_member_by_username/':
        key = str(body.get('username') or body.get('query') or '')
        t = state['accounts'].get(key)
        if t is None:
            for acct in state['accounts'].values():
                if acct.get('handle') == key:
                    t = acct
                    break
        if t is None:
            return 200, {'member': None}
        return 200, {'member': {'id': t['username'], 'handle': t.get('handle'), 'cup': t.get('cup', 0), 'title': t.get('title', ''), 'coin': t.get('coin', 0)}}
    if path == '/game/list_transactions/':
        return 200, {'transactions': list(reversed(a.get('transactions', [])))[:100]}
    # ---- matchmaking / servers ----
    if path == '/game/register/':
        mode = str(body.get('mode') or 'Race')
        if mode not in ('Race', 'FreeRide'):
            return 400, {'error': 'invalid game server mode'}
        ip = str(body.get('public_ip') or body.get('ip') or os.environ.get('GAME_PUBLIC_IP') or '127.0.0.1').strip()
        port = int(body.get('port') or 9000)
        transport = str(body.get('transport') or 'auto').strip().lower()
        if transport == 'auto':
            transport = 'websocket' if ip.startswith(('ws://', 'wss://')) or ip.endswith(('.proxy.rlwy.net', '.up.railway.app')) else 'enet'
        if transport in ('tcp', 'ws', 'wss'):
            transport = 'websocket'
        elif transport == 'udp':
            transport = 'enet'
        if transport not in ('enet', 'websocket'):
            return 400, {'error': 'invalid game server transport'}
        if not ip or not 1 <= port <= 65535:
            return 400, {'error': 'invalid game server address'}
        key = 'freeride' if mode == 'FreeRide' else 'race'
        _prune_game_servers(now)
        servers = state.setdefault('servers', {'race': [], 'freeride': []})
        lst = servers.setdefault(key, [])
        for x in lst:
            if x['ip'] == ip and x['port'] == port:
                x['updated_at'] = now
                x['transport'] = transport
                if not x.get('name_override'):
                    x['name'] = _server_name(mode, ip, x['id'])
                save_state()
                return 200, {'id': x['id'], 'is_test': False, 'total_stage': x['total_stage']}
        state['serverCounter'] += 1
        sid = state['serverCounter']
        entry = {'id': sid, 'mode': mode, 'ip': ip, 'port': port, 'players_joined': 0, 'state': 'Lobby', 'map_id': 0, 'bot_count': 0, 'max_players_start': 32, 'total_stage': 3, 'owner_id': a.get('username') if a else None, 'password_hash': '', 'updated_at': now, 'name': _server_name(mode, ip, sid)}
        entry['transport'] = transport
        lst.append(entry)
        save_state()
        log('server registered id=' + str(sid) + ' mode=' + mode + ' ' + ip + ':' + str(port))
        return 200, {'id': sid, 'is_test': False, 'total_stage': entry['total_stage']}
    if path == '/game/update/':
        server = _find_server(body.get('id'))
        if server is None:
            return 404, {'error': 'game server not found'}
        server['players_joined'] = min(max(0, int(body.get('players_joined') or 0)), int(server.get('max_players_start', 32)))
        next_state = str(body.get('state') or server.get('state') or 'Lobby')
        if next_state not in ('Loading', 'Lobby', 'CountDown', 'InGame', 'Results'):
            return 400, {'error': 'invalid game server state'}
        server['state'] = next_state
        server['map_id'] = int(body.get('map_id') or 0)
        server['bot_count'] = max(0, int(body.get('bot_count') or 0))
        server['updated_at'] = now
        save_state()
        return 200, {'ok': True}
    if path == '/game/start_game/':
        count = min(32, max(1, int(body.get('player_count') or 1)))
        game_id = random.SystemRandom().randrange(1, 2_147_483_647)
        container_id = random.SystemRandom().randrange(1, 2_147_483_647)
        games = state.setdefault('games', {})
        games['match:' + str(container_id)] = {'game_id': game_id, 'container_id': container_id, 'created_at': now, 'stage': 0, 'participants': body.get('ids', []), 'results': {}, 'finished': False}
        return 200, {'game_id': game_id, 'container_id': container_id, 'qualified_count': max(1, (count + 1) // 2)}
    if path == '/game/find_game_v2/':
        _prune_game_servers(now)
        alive = [s for s in state.setdefault('servers', {}).setdefault('race', []) if not _is_hidden(s) and _visible_to(s, a) and s.get('state') in ('Lobby', 'Loading') and s['players_joined'] < s['max_players_start']]
        if not alive:
            return 400, {}
        best = alive[0]
        def endpoint(server):
            return {key: server.get(key, 'auto') for key in ('ip', 'port', 'total_stage', 'transport')}
        return 200, {'best_server': endpoint(best), 'all_servers': [endpoint(s) for s in alive[1:]]}
    if path == '/game/select_map/':
        # سرور تعیین می‌کند هر مرحله کدام نقشه باشد
        gid = int(body.get('id') or 0)
        games = state.setdefault('games', {})
        g = games.setdefault('g' + str(gid), {'stage': 0})
        g['stage'] = int(g.get('stage', 0)) + 1
        maps = [
            ('res://Scenes/maps/CannonLevel.tscn', 10),
            ('res://Scenes/maps/RunningLevel.tscn', 10),
            ('res://Scenes/maps/Hexagon_elimination_level.tscn', 10),
        ]
        idx = (max(1, int(g['stage'])) - 1) % len(maps)
        mpath, bots = maps[idx]
        save_state()
        log('select_map game=' + str(gid) + ' stage=' + str(g['stage']) + ' -> ' + mpath)
        return 200, {'map': {'id': g['stage'], 'path': mpath, 'max_players_count': 32, 'min_players_count': 4, 'bot_count': bots, 'bot_wait_remove': 100, 'bot_reset_time': 30}, 'settings': {'game_time': 90, 'lobby_time': 20, 'countdown_time': 5, 'result_time': 8, 'player_join_add_time': 2}}
    if path == '/game/results_v2/':
        key = str(body.get('container_id') or body.get('game_id') or '')
        game = state.setdefault('games', {}).get('match:' + key)
        if game is None or not game.get('finished'):
            return 200, {'my_result': {'coin': 0, 'cup': 0, 'crown': 0}, 'winner': None}
        result = game.setdefault('results', {}).get(a['username'])
        if result is None:
            return 200, {'my_result': {'coin': 0, 'cup': 0, 'crown': 0}, 'winner': None}
        claimed = a.setdefault('claimed_game_ids', [])
        if key in claimed:
            return 200, {'my_result': {'coin': 0, 'cup': 0, 'crown': 0}, 'winner': None}
        claimed.append(key)
        save_state()
        winner_id = next((user for user, value in game['results'].items() if int(value.get('rank', 0)) == 1), None)
        return 200, {'my_result': {'coin': result['coin'], 'cup': result['cup'], 'crown': result['crown']}, 'winner': {'id': winner_id} if winner_id else None}
    if path == '/game/list_freeride_servers/':
        _prune_game_servers(now)
        return 200, {'servers': [_public_server(server) for server in state.setdefault('servers', {}).setdefault('freeride', []) if not _is_hidden(server) and _visible_to(server, a)]}
    if path == '/game/verify_server_password/':
        server = _find_server(body.get('server_id') or body.get('id'))
        if server is None:
            return 404, {'error': 'server not found'}
        supplied = str(body.get('password') or '')
        expected = str(server.get('password_hash') or '')
        if not expected or not hmac.compare_digest(hashlib.sha256(supplied.encode('utf-8')).hexdigest(), expected):
            return 403, {'error': 'wrong server password'}
        return 200, {'ok': True}
    if path == '/game/get_freeride_server_owner/':
        server = _find_server(body.get('id'))
        if server is None:
            return 404, {'error': 'server not found'}
        owner = state.setdefault('accounts', {}).get(server.get('owner_id'))
        return 200, {'owner': owner.get('username') if owner else None, 'owner_handle': owner.get('handle', '') if owner else '', 'is_private': bool(server.get('password_hash')), 'admin': _server_owned_by(server, a)}
    if path == '/game/leaderboard_v2/':
        rows = rank_rows('cup')
        wins = rank_rows('win_count')
        return 200, {'ranks': rows, 'wins': wins, 'my_rank': next((r['rank'] for r in rows if r.get('id') == a.get('username')), 0), 'my_win_rank': next((r['rank'] for r in wins if r.get('id') == a.get('username')), 0)}
    if path == '/game/coin_leaderboard/':
        rows = rank_rows('coin')
        return 200, {'ranks': rows, 'my_rank': next((r['rank'] for r in rows if r.get('id') == a.get('username')), 0)}
    if path == '/game/char_leaderboard/':
        rows = []
        for acct in state['accounts'].values():
            if acct.get('hide_leaderboard'):
                continue
            rows.append({'id': acct['username'], 'handle': acct['handle'], 'name': acct['handle'],
                         'num_chars': len(acct.get('characters', [])), 'cup': acct.get('cup', 0),
                         'coin': acct.get('coin', 0), 'crown': acct.get('crown', 0), 'title': acct.get('title', ''),
                         'character': (acct.get('characters') or [CHARS[0]])[-1].get('path', CHARS[0]['path']),
                         'path': (acct.get('characters') or [CHARS[0]])[-1].get('path', CHARS[0]['path']),
                         'card_path': (acct.get('characters') or [CHARS[0]])[-1].get('card_path', CHARS[0]['card_path']),
                         'rank': 0})
        rows.sort(key=lambda r: r['num_chars'], reverse=True)
        rows = rows[:50]
        for i, r in enumerate(rows):
            r['rank'] = i + 1
        return 200, {'ranks': rows, 'my_rank': next((r['rank'] for r in rows if r.get('id') == a.get('username')), 0)}
    # ---- chat ----
    if path == '/chat/send/':
        _ensure_chat()
        room = str(body.get('room') or 'PublicChat')[:64]
        content = body.get('content')
        if not isinstance(content, str):
            content = json.dumps(content or {})
        room_msgs_for_id = state['chat']['rooms'].get(room, [])
        mid = max(int(state['chat'].get('next', 1)), max([int(m.get('id', 0)) for m in room_msgs_for_id] or [0]) + 1)
        state['chat']['next'] = mid + 1
        msg = {
            'id': mid,
            'content': content[:4000],
            'channel_id': room,
            'sender_id': a['username'],
            'handle': a['handle'],
            'create_time': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()),
        }
        room_msgs = state['chat']['rooms'].setdefault(room, [])
        room_msgs.append(msg)
        if len(room_msgs) > 200:
            del room_msgs[0:len(room_msgs) - 200]
        save_state()
        return 200, {'ok': True, 'id': mid}
    if path == '/chat/fetch/':
        _ensure_chat()
        room = str(body.get('room') or 'PublicChat')[:64]
        try:
            since = int(float(body.get('since') or 0))
        except (TypeError, ValueError):
            since = 0
        room_msgs = state['chat']['rooms'].get(room, [])
        newest = max([int(m.get('id', 0)) for m in room_msgs] or [0])
        # A client cursor past the newest stored id (e.g. after the state was reset)
        # would hide every new message, so start over from the latest messages.
        if since > max(newest, int(state['chat'].get('next', 1)) - 1):
            since = 0
        out = [m for m in room_msgs if int(m.get('id', 0)) > since]
        return 200, {'messages': out[-100:]}
    if path == '/chat/history/':
        _ensure_chat()
        room = str(body.get('room') or 'PublicChat')[:64]
        limit = int(body.get('limit') or 50)
        room_msgs = state['chat']['rooms'].get(room, [])
        out = list(room_msgs)[-limit:]
        out.reverse()
        return 200, {'messages': out}
    if path == '/voice/access_token/':
        room_name = str(body.get('room_name') or '').strip()[:96]
        if not room_name or any(ch in room_name for ch in ('/', '\\', ' ', '\n', '\r')):
            return 400, {'error': 'invalid room name'}
        rooms = state.setdefault('voice_rooms', {})
        if room_name == a['username']:
            if int(a.get('coin', 0)) < int(SYNC_PRICES.get('voice_call_price', 0)):
                return 402, {'error': 'not enough coins'}
            code, _response = _livekit_admin_request('CreateRoom', room_name)
            if code != 200:
                return code, _response
            rooms[room_name] = {'owner': a['username'], 'updated_at': now}
        else:
            invitations = state.setdefault('voice_invites', {})
            pending = invitations.get(a['username'], [])
            invitation = next((item for item in pending if item.get('room') == room_name and int(item.get('expires_at', 0)) >= now), None)
            room = rooms.get(room_name)
            if invitation is None or room is None or room.get('owner') != room_name:
                return 403, {'error': 'accept an active call invitation first'}
            pending.remove(invitation)
        token = _livekit_user_token(a['username'], a.get('handle', a['username']), room_name)
        if not token:
            return 503, {'error': 'voice service is not configured'}
        return 200, {'token': token, 'room_name': room_name, 'url': os.environ.get('LIVEKIT_CLIENT_URL', 'wss://livekit.sizakgames.ir')}
    if path == '/voice/invite/':
        room_name = str(body.get('room_name') or '').strip()[:96]
        target_key = str(body.get('target') or '').strip()
        if room_name != a['username'] or not target_key:
            return 403, {'error': 'only the room owner can invite players'}
        room = state.setdefault('voice_rooms', {}).get(room_name)
        if not room or room.get('owner') != a['username']:
            return 409, {'error': 'create the call before inviting players'}
        target = _find_account(target_key)
        if target is None or target['username'] == a['username']:
            return 404, {'error': 'player not found'}
        invitation = {'room': room_name, 'from': a['username'], 'expires_at': now + 90}
        pending = state.setdefault('voice_invites', {}).setdefault(target['username'], [])
        pending[:] = [item for item in pending if int(item.get('expires_at', 0)) >= now and item.get('room') != room_name]
        pending.append(invitation)
        return 200, {'ok': True}
    if path == '/voice/end_room/':
        room_name = str(body.get('room_name') or '').strip()[:96]
        if not room_name:
            return 400, {'error': 'missing room name'}
        room = state.setdefault('voice_rooms', {}).get(room_name)
        if not room or room.get('owner') != a['username']:
            return 403, {'error': 'only the room owner can end this call'}
        result = _livekit_admin_request('DeleteRoom', room_name)
        if result[0] == 200:
            state['voice_rooms'].pop(room_name, None)
        return result
    if path == '/voice/kick_participant/':
        room_name = str(body.get('room_name') or '').strip()[:96]
        participant = str(body.get('participant') or '').strip()[:96]
        if not room_name or not participant:
            return 400, {'error': 'missing room or participant'}
        room = state.setdefault('voice_rooms', {}).get(room_name)
        if not room or room.get('owner') != a['username']:
            return 403, {'error': 'only the room owner can remove participants'}
        return _livekit_admin_request('RemoveParticipant', room_name, participant)
    # ---- police ----
    if path == '/police/arrest_list/':
        arrests = [call for call in state.setdefault('police_calls', []) if call.get('guilty') and call.get('active', True)]
        return 200, {'arrests': arrests, 'results': arrests}
    if path == '/police/jail_stat/':
        return 200, {'jail_time': int(a.get('jail_time') or 0), 'stats': a.get('job_stats', {}), 'players': []}
    if path == '/police/police_call/':
        calls = state.setdefault('police_calls', [])
        call = {
            'id': len(calls) + 1,
            'caller_id': a['username'],
            'caller_handle': a.get('handle', ''),
            'guilty': body.get('guilty'),
            'guilty_handle': '',
            'crime': str(body.get('crime') or '')[:80],
            'text': str(body.get('text') or '')[:500],
            'location': str(body.get('location') or '')[:120],
            'server': str(body.get('server') or '')[:120],
            'created_at': now,
            'created_time': now,
            'active': True,
        }
        if call['guilty']:
            target = _find_account(call['guilty'])
            if target:
                call['guilty'] = target['username']
                call['guilty_handle'] = target.get('handle', '')
        calls.append(call)
        save_state()
        return 200, {'call': call, 'id': call['id'], 'calls': calls[-50:]}
    if path == '/police/police_call_list/':
        calls = [call for call in state.setdefault('police_calls', []) if call.get('active', True)]
        return 200, {'calls': calls[-100:]}
    if path == '/police/police_law/':
        return 200, {'law': 'قوانین شهر:\n۱) آسیب به دیگران ممنوع است.\n۲) دزدی و تخریب اموال عمومی جرم است.\n۳) توهین و فحاشی در چت ممنوع است.\n۴) رانندگی پرخطر و تصادف عمدی جرم است.\n۵) در صورت دستگیری، جریمه یا زندان در انتظار شماست.', 'last_update': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())}
    if path == '/police/job_q_stats/':
        q = a.get('police_q')
        if not a.get('police_license'):
            return 200, {'has_license': True, 'has_q': False, 'rank': 0, 'time': 0, 'score': 0, 'gateway_type': 'IAP', 'players': []}
        if q is None:
            return 200, {'has_license': False, 'has_q': False, 'rank': 0, 'time': 0, 'score': 0, 'gateway_type': 'IAP', 'players': []}
        rank = 1
        for x in state.setdefault('police_queue', []):
            if x.get('username') == a['username']:
                break
            rank += 1
        return 200, {'has_license': False, 'has_q': True, 'rank': rank, 'time': int(now - int(q.get('time', now))), 'score': int(a.get('police_score', 0)), 'gateway_type': 'IAP', 'players': []}
    if path == '/police/add_me_to_job_q/':
        price = max(0, int(body.get('price') or 0))
        if a['coin'] < price:
            return 401, {'coin': a['coin']}
        a['coin'] -= price
        a['police_q'] = {'time': now}
        ql = state.setdefault('police_queue', [])
        if not any(x.get('username') == a['username'] for x in ql):
            ql.append({'username': a['username'], 'handle': a['handle'], 'score': int(a.get('police_score', 0)), 'time': now})
        save_state()
        return 200, {'coin': a['coin']}
    if path == '/police/add_score_to_job_q/':
        c = max(0, int(body.get('coin') or 0))
        if a['coin'] < c:
            return 401, {'coin': a['coin']}
        a['coin'] -= c
        a['police_score'] = int(a.get('police_score', 0)) + c
        for x in state.setdefault('police_queue', []):
            if x.get('username') == a['username']:
                x['score'] = a['police_score']
        save_state()
        return 200, {'coin': a['coin'], 'score': a['police_score']}
    if path.startswith('/police/'):
        if path == '/police/police_report/':
            guilty_id = body.get('arrest_id') or body.get('police_call_id')
            target = _find_account(guilty_id)
            if target and int(body.get('ban_time') or 0) > 0:
                target['ban_time'] = int(body.get('ban_time') or 0)
                target['jail_time'] = int(body.get('jail_time') or 0)
                target['in_prison'] = target['jail_time'] > 0
                _log_event('ban', (a or {}).get('username', 'پلیس'), target['username'], 'گزارش پلیس: ' + str(target['ban_time'] // 3600) + ' ساعت')
                save_state()
                return 200, {'job_done': True}
            return 200, {'job_done': False}
        if path == '/police/jail_exit/':
            a['jail_time'] = 0
            a['in_prison'] = False
            save_state()
            return 200, {'jail_time': 0}
        if path == '/police/police_arrest/':
            for guilty in body.get('guilties', []):
                target = _find_account(guilty)
                if target:
                    target['jail_time'] = max(int(target.get('jail_time') or 0), 60)
                    target['in_prison'] = True
            save_state()
            return 200, {'ok': True}
        if path == '/police/i_kill/':
            target = _find_account(body.get('dead_id'))
            if target:
                target['in_prison'] = True
                target['jail_time'] = max(int(target.get('jail_time') or 0), 120)
                save_state()
            return 200, {'ok': True}
        return 200, {}
    if path == '/game/free_admin_ban/':
        t = _find_account(body.get('backend_id'))
        if t is not None:
            t['ban_time'] = int(float(body.get('time') or 1) * 3600)
            _log_event('ban', (a or {}).get('username', 'ادمین آزاد'), t['username'], 'بازی آزاد')
            save_state()
        return 200, {}
    if path == '/game/free_admin_unban/':
        t = _find_account(body.get('backend_id'))
        if t is not None:
            t['ban_time'] = 0
            _log_event('unban', (a or {}).get('username', 'ادمین آزاد'), t['username'], 'بازی آزاد')
            save_state()
        return 200, {}
    if path == '/game/free_admin_set_title/':
        t = _find_account(body.get('backend_id'))
        if t is not None:
            t['title'] = str(body.get('title') or '')
            t['title_color'] = str(body.get('title_color') or 'FFFFFF')
            save_state()
        return 200, {}
    if path in ('/game/ban_user/', '/game/report_message/'):
        return 200, {}
    log('unhandled route: ' + str(path))
    return 404, {'error': 'not found'}

class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def _send(self, code, obj):
        body = json.dumps(obj if obj is not None else {}).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html):
        b = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(b)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.end_headers()

    def do_GET(self):
        p = self.path.split('?')[0]
        if p in ('/', '/health', '/healthz'):
            self._send(200, {'ok': True, 'service': 'animal-rush-backend', 'accounts': len(state['accounts']), 'time': int(time.time())})
        elif p in ('/admines', '/admines/', '/admin', '/admin/'):
            self._send_html(ADMIN_HTML)
        else:
            self._send(404, {'error': 'not found'})

    def do_POST(self):
        length = int(self.headers.get('Content-Length') or 0)
        raw = self.rfile.read(length) if length else b''
        try:
            body = json.loads(raw.decode('utf-8') or '{}')
        except Exception:
            body = {}
        if not isinstance(body, dict):
            body = {}
        # Only the verified HTTP header may set this internal authorization flag.
        body.pop('_game_server_authorized', None)
        auth = self.headers.get('Authorization') or ''
        token = auth[4:] if auth.startswith('JWT ') else auth
        game_server_token = self.headers.get('X-Game-Server-Token') or ''
        if GAME_SERVER_TOKEN and hmac.compare_digest(game_server_token, GAME_SERVER_TOKEN):
            body['_game_server_authorized'] = True
        path = self.path.split('?')[0]
        if path.startswith('/admin/'):
            with _lock:
                try:
                    code, obj = route_admin(path, body)
                except Exception as exc:
                    log('admin error ' + str(path) + ': ' + repr(exc))
                    code, obj = 500, {'error': 'internal'}
            self._send(code, obj)
            return
        if path == '/account/register/':
            ip = _client_ip(self)
            with _lock:
                allowed = _register_allowed(ip)
            if not allowed:
                self._send(429, {'error': 'too many accounts created from this network today'})
                return
        with _lock:
            a = account_for(token)
            try:
                code, obj = route(path, body, a)
            except Exception as exc:
                log('route error ' + str(path) + ': ' + repr(exc))
                code, obj = 500, {'error': 'internal'}
            save_state()
        self._send(code, obj)

    def log_message(self, fmt, *args):
        pass

def main():
    load_state()
    _backfill_ids()
    log('Animal Rush backend (Railway) listening on ' + HOST + ':' + str(PORT))
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass




"""Append to the existing backend to serve HTTP and game WebSockets together."""
import select
import signal
import socket
import subprocess
import tempfile
import zlib
from pathlib import Path

SERVER_UPDATE_VERSION = 'v31'
# The small release builder embeds the scripts here; no remote assets are needed.
_SERVER_HOTFIX_PAYLOAD = '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'

GAME_PORT = int(os.environ.get('GAME_PORT', '9000'))
GAME_PATH = '/game-socket'
RACE_PORT = int(os.environ.get('RACE_PORT', str(GAME_PORT + 1)))
RACE_PATH = '/race-socket'
GAME_PROCESSES = {}
READY_MODES = set()
ALL_MODES = ('FreeRide', 'Race')
# Keep the user's one-service, worker-only and hub-only deployments compatible.
_worker_modes = os.environ.get('WORKER_MODES', ','.join(ALL_MODES)).strip()
_requested_modes = tuple(mode.strip() for mode in _worker_modes.split(',') if mode.strip())
LOCAL_MODES = tuple(mode for mode in _requested_modes if mode in ALL_MODES)
REMOTE = {mode: os.environ.get('REMOTE_' + mode.upper(), '').strip() for mode in ALL_MODES}
HUB_URL = os.environ.get('HUB_URL', '').strip().rstrip('/')


def _remote_target(mode):
    host, separator, port = REMOTE[mode].rpartition(':')
    if not separator or not host or not port.isdigit() or not 1 <= int(port) <= 65535:
        raise ValueError('REMOTE_' + mode.upper() + ' must be host:port')
    return host.strip('[]'), int(port)


def _remote_ready(mode):
    connection = None
    try:
        host, port = _remote_target(mode)
        connection = http.client.HTTPConnection(host, port, timeout=2)
        connection.request('GET', '/health')
        response = connection.getresponse()
        health = json.loads(response.read(65536))
        return (response.status == 200 and isinstance(health, dict)
                and health.get('game_ready') is True and mode in health.get('local_modes', []))
    except (OSError, ValueError, http.client.HTTPException):
        return False
    finally:
        if connection is not None:
            connection.close()


class DualStackServer(ThreadingHTTPServer):
    address_family = socket.AF_INET6

    def server_bind(self):
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()


def prepare_game_pack(source):
    if not _SERVER_HOTFIX_PAYLOAD:
        return source
    payload = json.loads(zlib.decompress(base64.b64decode(_SERVER_HOTFIX_PAYLOAD)))
    stamp = hashlib.sha256((_SERVER_HOTFIX_PAYLOAD + str(source) + str(source.stat().st_size) + str(source.stat().st_mtime_ns)).encode()).hexdigest()[:20]
    cache = Path(DATA_DIR) / ('server-hotfix-' + SERVER_UPDATE_VERSION)
    cache.mkdir(parents=True, exist_ok=True)
    destination = cache / ('game-' + stamp + '.pck')
    if destination.is_file() and destination.stat().st_size > 0:
        log('Using cached ' + SERVER_UPDATE_VERSION + ' server pack; original game.pck is unchanged.')
        return destination
    with tempfile.TemporaryDirectory(prefix='build-', dir=cache) as temporary:
        work = Path(temporary)
        project = work / 'project'
        project.mkdir()
        (project / 'project.godot').write_text('config_version=5\n', encoding='utf-8')
        helper = project / '__patch_builder__.gd'
        helper.write_text(payload['builder'], encoding='utf-8')
        script = work / 'replacements'
        script.mkdir()
        files = payload.get('files', {'networking/server.gd': payload.get('server', '')})
        for relative, text in files.items():
            path = script / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        (script / 'manifest.json').write_text(json.dumps(list(files)), encoding='utf-8')
        pending = work / 'updated.pck'
        args = [os.environ.get('GODOT_BIN', 'godot'), '--headless', '--path', str(project),
                '--script', str(helper), '--', str(source), str(pending), str(script)]
        result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120)
        if result.returncode != 0 or not pending.is_file() or 'error=0' not in result.stdout:
            raise RuntimeError('Offline game pack update failed: ' + (result.stdout + result.stderr)[-4000:])
        os.replace(pending, destination)
    log('Built ' + SERVER_UPDATE_VERSION + ' server pack locally; no game assets were downloaded.')
    return destination


class UnifiedHandler(Handler):
    rbufsize = 0

    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path in (GAME_PATH, RACE_PATH):
            if self.headers.get('Upgrade', '').lower() != 'websocket':
                self._send(426, {'error': 'WebSocket upgrade required'})
                return
            mode = 'Race' if path == RACE_PATH else 'FreeRide'
            if mode in LOCAL_MODES:
                self.proxy_game('127.0.0.1', RACE_PORT if mode == 'Race' else GAME_PORT)
            elif REMOTE[mode]:
                try:
                    self.proxy_game(*_remote_target(mode))
                except ValueError:
                    self._send(503, {'error': 'Game worker is misconfigured'})
            else:
                self._send(503, {'error': 'Game mode is not available'})
        elif self.path.split('?', 1)[0] in ('/health', '/healthz'):
            local_ready = all(mode in READY_MODES and mode in GAME_PROCESSES
                              and GAME_PROCESSES[mode].poll() is None for mode in LOCAL_MODES)
            remote_ready = {mode: _remote_ready(mode) for mode in ALL_MODES
                            if mode not in LOCAL_MODES and REMOTE[mode]}
            # A worker reports its own readiness; the hub checks both modes.
            configured = bool(LOCAL_MODES or remote_ready) and (bool(HUB_URL) or all(
                mode in LOCAL_MODES or mode in remote_ready for mode in ALL_MODES))
            ready = configured and local_ready and all(remote_ready.values())
            self._send(200 if ready else 503, {
                'ok': ready, 'service': 'animal-rush-one-server',
                'game_ready': ready, 'game_path': GAME_PATH, 'race_path': RACE_PATH,
                'version': SERVER_UPDATE_VERSION,
                'local_modes': list(LOCAL_MODES), 'remote_ready': remote_ready,
            })
        else:
            super().do_GET()

    def proxy_game(self, host, port):
        self.close_connection = True
        try:
            upstream = socket.create_connection((host, port), timeout=5)
        except OSError:
            self._send(503, {'error': 'Game is starting; retry shortly'})
            return
        with upstream:
            header = self.requestline + '\r\n'
            header += ''.join(f'{key}: {value}\r\n' for key, value in self.headers.raw_items())
            try:
                upstream.sendall((header + '\r\n').encode('iso-8859-1'))
                self.connection.settimeout(10)
                upstream.settimeout(10)
                while True:
                    readable, _, _ = select.select([self.connection, upstream], [], [], 30)
                    for source in readable:
                        data = source.recv(65536)
                        if not data:
                            return
                        target = upstream if source is self.connection else self.connection
                        target.sendall(data)
            except (OSError, ValueError):
                return


def unified_main():
    global GAME_SERVER_TOKEN
    if _requested_modes != ('none',) and (not _requested_modes or any(
            mode not in ALL_MODES for mode in _requested_modes)):
        raise SystemExit('WORKER_MODES must contain FreeRide, Race, or none.')
    if len(set(LOCAL_MODES)) != len(LOCAL_MODES):
        raise SystemExit('WORKER_MODES cannot contain duplicate modes.')
    distributed = bool(HUB_URL or any(REMOTE.values()))
    if distributed and not GAME_SERVER_TOKEN:
        raise SystemExit('Set the same GAME_SERVER_TOKEN on the hub and every worker.')
    if HUB_URL and (not LOCAL_MODES or any(REMOTE.values())):
        raise SystemExit('A HUB_URL worker must run local modes and cannot forward to other workers.')
    if not HUB_URL and any(mode not in LOCAL_MODES and not REMOTE[mode] for mode in ALL_MODES):
        raise SystemExit('Configure REMOTE_FREERIDE and REMOTE_RACE for modes not run locally.')
    for mode in ALL_MODES:
        if REMOTE[mode]:
            _remote_target(mode)
    if not GAME_SERVER_TOKEN:
        GAME_SERVER_TOKEN = os.urandom(32).hex()
    if len({PORT, GAME_PORT, RACE_PORT}) != 3 or not all(1 <= p <= 65535 for p in (PORT, GAME_PORT, RACE_PORT)):
        raise SystemExit('PORT, GAME_PORT and RACE_PORT must be valid, different ports.')
    origin = os.environ.get('PUBLIC_URL', '').strip().rstrip('/')
    if not origin:
        domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '').strip()
        origin = 'https://' + domain if domain else 'http://127.0.0.1:' + str(PORT)
    parsed = urlsplit(origin)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise SystemExit('PUBLIC_URL must be an HTTP(S) origin without credentials.')
    scheme = 'wss' if parsed.scheme == 'https' else 'ws'
    public_game = scheme + '://' + parsed.netloc + GAME_PATH
    public_port = parsed.port or (443 if scheme == 'wss' else 80)
    pack = Path(os.environ.get('GAME_PACK', Path(__file__).with_name('game.pck'))).resolve()
    if LOCAL_MODES and not pack.is_file():
        raise SystemExit('Required game.pck was not found.')
    if LOCAL_MODES:
        pack = prepare_game_pack(pack)
    load_state()
    _backfill_ids()
    # A fresh process must register its own live endpoint; persisted addresses may be stale.
    state['servers'] = {'race': [], 'freeride': []}
    httpd = (DualStackServer(('::', PORT), UnifiedHandler) if socket.has_ipv6
             else ThreadingHTTPServer((HOST, PORT), UnifiedHandler))
    environment = os.environ.copy()
    environment['ANIMAL_RUSH_SERVER_TOKEN'] = GAME_SERVER_TOKEN
    stopped = threading.Event()

    def shutdown(_signum=None, _frame=None):
        stopped.set()
        threading.Thread(target=httpd.shutdown, daemon=True).start()

    def monitor_game(mode, args):
        while not stopped.is_set():
            try:
                process = subprocess.Popen(args, cwd=str(pack.parent), env=environment,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', bufsize=1)
                GAME_PROCESSES[mode] = process
                log('Started ' + mode + ' worker pid=' + str(process.pid))
                for line in process.stdout:
                    print('[' + mode + '] ' + line.rstrip(), flush=True)
                    if 'Set State to Lobby' in line:
                        READY_MODES.add(mode)
                return_code = process.wait()
                log(mode + ' worker exited with code=' + str(return_code))
            except OSError as exc:
                log('Cannot start ' + mode + ': ' + str(exc))
            finally:
                READY_MODES.discard(mode)
            if not stopped.is_set():
                log(mode + ' worker stopped; restarting this mode inside the same service.')
                stopped.wait(1)

    try:
        if HUB_URL:
            hub = urlsplit(HUB_URL)
            if hub.scheme not in ('http', 'https') or not hub.hostname or hub.username or hub.password or hub.path not in ('', '/'):
                raise SystemExit('HUB_URL must be an HTTP(S) origin without credentials or a path.')
            connection_type = http.client.HTTPSConnection if hub.scheme == 'https' else http.client.HTTPConnection
            hub_reachable = False
            for _ in range(30):
                connection = None
                try:
                    connection = connection_type(hub.hostname, hub.port or (443 if hub.scheme == 'https' else 80), timeout=2)
                    connection.request('GET', '/')
                    response = connection.getresponse()
                    health = json.loads(response.read(65536))
                    # The root checks HTTP reachability without recursively
                    # querying workers that have not started serving yet.
                    if response.status == 200 and isinstance(health, dict) and health.get('service') in (
                            'animal-rush-backend', 'animal-rush-one-server'):
                        hub_reachable = True
                        break
                except (OSError, ValueError, http.client.HTTPException):
                    pass
                finally:
                    if connection is not None:
                        connection.close()
                if stopped.wait(1):
                    break
            if not hub_reachable:
                raise SystemExit('Hub is unreachable; check HUB_URL and private networking.')
        backend_url = HUB_URL or 'http://127.0.0.1:' + str(PORT)
        for mode, port, path in [('FreeRide', GAME_PORT, GAME_PATH), ('Race', RACE_PORT, RACE_PATH)]:
            if mode not in LOCAL_MODES:
                continue
            args = [os.environ.get('GODOT_BIN', 'godot'), '--headless', '--main-pack', str(pack), '--',
                'server=1', 'transport=websocket', 'mode=' + mode, 'ip=127.0.0.1',
                'port=' + str(port), 'register_port=' + str(public_port),
                'public_ip=' + scheme + '://' + parsed.netloc + path,
                'token=' + GAME_SERVER_TOKEN, 'backend=' + backend_url]
            threading.Thread(target=monitor_game, args=(mode, args), daemon=True).start()
        signal.signal(signal.SIGTERM, shutdown)
        signal.signal(signal.SIGINT, shutdown)
        log('One service on port ' + str(PORT) + '; game endpoint: ' + public_game)
        httpd.serve_forever(poll_interval=0.2)
    finally:
        failed = not stopped.is_set()
        httpd.server_close()
        stopped.set()
        for process in list(GAME_PROCESSES.values()):
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    unified_main()
