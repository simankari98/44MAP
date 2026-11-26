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

_MEMBER_KEYS = ['cup','coin','crown','email','daily_claim_time','hunger','warmth','title','title_color','is_test','name_changed_count','show_debug','ban_time','free_admin','bazras','stealth','chat_admin','jail_time','in_prison','progress_level','is_meta_progress_finished','win_count','game_count']


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


def _admin_ok(body):
    key = os.environ.get('ADMIN_KEY', '')
    candidate = str((body or {}).get('key') or '')
    return bool(key) and hmac.compare_digest(candidate, key)


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
            'online': False,
        })
    out.sort(key=lambda r: r['coin'], reverse=True)
    return out


def route_admin(path, body):
    if not _admin_ok(body):
        return 403, {'error': 'bad admin key'}
    if path == '/admin/users/':
        return 200, {'users': admin_users()}
    target = _find_account(body.get('id') or body.get('user_id') or body.get('username'))
    if target is None:
        return 404, {'error': 'no such user'}
    if path == '/admin/give_coin/':
        target['coin'] = int(target.get('coin', 0)) + int(body.get('amount') or 0)
    elif path == '/admin/set_title/':
        target['title'] = str(body.get('title') or '')
        target['title_color'] = str(body.get('title_color') or 'FFFFFF')
    elif path == '/admin/grant_bazras/':
        v = body.get('value')
        target['bazras'] = bool(v) if v is not None else True
        if target['bazras']:
            target.setdefault('free_admin', False)
        if body.get('admin') is not None:
            target['free_admin'] = bool(body.get('admin'))
    elif path == '/admin/ban/':
        target['ban_time'] = int(float(body.get('hours') or 1) * 3600)
    elif path == '/admin/unban/':
        target['ban_time'] = 0
    elif path == '/admin/set_coin/':
        target['coin'] = int(body.get('amount') or 0)
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
        if not title:
            return 400, {'coin': a['coin']}
        if a['coin'] < price:
            return 400, {'coin': a['coin']}
        a['coin'] -= price
        a['title'] = title
        a['title_color'] = str(job.get('color') or 'FFFFFF')
        stats = a.setdefault('job_stats', {})
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
                save_state()
                return 200, {'id': x['id'], 'is_test': False, 'total_stage': x['total_stage']}
        state['serverCounter'] += 1
        sid = state['serverCounter']
        entry = {'id': sid, 'mode': mode, 'ip': ip, 'port': port, 'players_joined': 0, 'state': 'Lobby', 'map_id': 0, 'bot_count': 0, 'max_players_start': 32, 'total_stage': 3, 'owner_id': a.get('username') if a else None, 'password_hash': '', 'updated_at': now, 'name': ('FreeRide ' if mode == 'FreeRide' else 'Race ') + 'Server ' + str(sid)}
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
        alive = [s for s in state.setdefault('servers', {}).setdefault('race', []) if s.get('state') in ('Lobby', 'Loading') and s['players_joined'] < s['max_players_start']]
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
        return 200, {'servers': [_public_server(server) for server in state.setdefault('servers', {}).setdefault('freeride', [])]}
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
        mid = state['chat']['next']
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
        since = int(body.get('since') or 0)
        room_msgs = state['chat']['rooms'].get(room, [])
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
            save_state()
        return 200, {}
    if path == '/game/free_admin_unban/':
        t = _find_account(body.get('backend_id'))
        if t is not None:
            t['ban_time'] = 0
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

SERVER_UPDATE_VERSION = 'v30'
# The small release builder embeds the scripts here; no remote assets are needed.
_SERVER_HOTFIX_PAYLOAD = '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'

GAME_PORT = int(os.environ.get('GAME_PORT', '9000'))
GAME_PATH = '/game-socket'
RACE_PORT = int(os.environ.get('RACE_PORT', str(GAME_PORT + 1)))
RACE_PATH = '/race-socket'
GAME_PROCESSES = {}
READY_MODES = set()


def prepare_game_pack(source):
    if not _SERVER_HOTFIX_PAYLOAD:
        return source
    payload = json.loads(zlib.decompress(base64.b64decode(_SERVER_HOTFIX_PAYLOAD)))
    stamp = hashlib.sha256((_SERVER_HOTFIX_PAYLOAD + str(source) + str(source.stat().st_size) + str(source.stat().st_mtime_ns)).encode()).hexdigest()[:20]
    cache = Path(DATA_DIR) / 'server-hotfix-v30'
    cache.mkdir(parents=True, exist_ok=True)
    destination = cache / ('game-' + stamp + '.pck')
    if destination.is_file() and destination.stat().st_size > 0:
        log('Using cached v30 server pack; original game.pck is unchanged.')
        return destination
    with tempfile.TemporaryDirectory(prefix='build-', dir=cache) as temporary:
        work = Path(temporary)
        project = work / 'project'
        project.mkdir()
        (project / 'project.godot').write_text('config_version=5\n', encoding='utf-8')
        helper = project / '__patch_builder__.gd'
        helper.write_text(payload['builder'], encoding='utf-8')
        script = work / 'server.gd'
        script.write_text(payload['server'], encoding='utf-8')
        pending = work / 'updated.pck'
        args = [os.environ.get('GODOT_BIN', 'godot'), '--headless', '--path', str(project),
                '--script', str(helper), '--', str(source), str(pending), str(script)]
        result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120)
        if result.returncode != 0 or not pending.is_file() or 'error=0' not in result.stdout:
            raise RuntimeError('Offline game pack update failed: ' + (result.stdout + result.stderr)[-4000:])
        os.replace(pending, destination)
    log('Built v30 server pack locally; no game assets were downloaded.')
    return destination


class UnifiedHandler(Handler):
    rbufsize = 0

    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path in (GAME_PATH, RACE_PATH):
            if self.headers.get('Upgrade', '').lower() != 'websocket':
                self._send(426, {'error': 'WebSocket upgrade required'})
                return
            self.proxy_game(RACE_PORT if path == RACE_PATH else GAME_PORT)
        elif self.path.split('?', 1)[0] in ('/health', '/healthz'):
            ready = len(READY_MODES) == 2 and all(p.poll() is None for p in GAME_PROCESSES.values())
            self._send(200 if ready else 503, {
                'ok': ready, 'service': 'animal-rush-one-server',
                'game_ready': ready, 'game_path': GAME_PATH, 'race_path': RACE_PATH,
                'version': SERVER_UPDATE_VERSION,
            })
        else:
            super().do_GET()

    def proxy_game(self, port):
        self.close_connection = True
        try:
            upstream = socket.create_connection(('127.0.0.1', port), timeout=5)
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
    if not pack.is_file():
        raise SystemExit('Required game.pck was not found.')
    pack = prepare_game_pack(pack)
    load_state()
    _backfill_ids()
    # A fresh process must register its own live endpoint; persisted addresses may be stale.
    state['servers'] = {'race': [], 'freeride': []}
    httpd = ThreadingHTTPServer((HOST, PORT), UnifiedHandler)
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
        for mode, port, path in [('FreeRide', GAME_PORT, GAME_PATH), ('Race', RACE_PORT, RACE_PATH)]:
            args = [os.environ.get('GODOT_BIN', 'godot'), '--headless', '--main-pack', str(pack), '--',
                'server=1', 'transport=websocket', 'mode=' + mode, 'ip=127.0.0.1',
                'port=' + str(port), 'register_port=' + str(public_port),
                'public_ip=' + scheme + '://' + parsed.netloc + path,
                'token=' + GAME_SERVER_TOKEN, 'backend=http://127.0.0.1:' + str(PORT)]
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
