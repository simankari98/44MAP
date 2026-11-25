// Animal Rush - Local Backend (zero-dependency Node.js)
// Replaces https://api.sizakgames.ir for offline/local play.
// Port: 8899   (start with:  node backend.mjs)
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = 8899;
const STATE_FILE = path.join(__dirname, 'state.json');
const LOG_FILE = path.join(__dirname, 'backend.log');

const CHARS = [
	{ id: 1, name: 'Freddy', path: 'res://assets/characters/Human/human.tscn', card_path: 'res://assets/characters/2D Card/Freddy_card.png', tier: 'Common' },
	{ id: 2, name: 'Frog', path: 'res://assets/characters/Frog/Frog.tscn', card_path: 'res://assets/characters/2D Card/Frog_card.png', tier: 'Common' },
	{ id: 3, name: 'Fox', path: 'res://assets/characters/Fox/Fox.tscn', card_path: 'res://assets/characters/2D Card/Fox_card.png', tier: 'Common' },
	{ id: 4, name: 'Horse', path: 'res://assets/characters/Horse/horse.tscn', card_path: 'res://assets/characters/2D Card/Horse_card.png', tier: 'Rare' },
	{ id: 5, name: 'Leopard', path: 'res://assets/characters/Leopard/Leopard.tscn', card_path: 'res://assets/characters/2D Card/Leopard_card.png', tier: 'Common' },
	{ id: 6, name: 'Tourist', path: 'res://assets/characters/Tourist/Tourist.tscn', card_path: 'res://assets/characters/2D Card/Ecotourist_card.png', tier: 'Rare' },
	{ id: 7, name: 'Sheep', path: 'res://assets/characters/Sheep/Sheep.tscn', card_path: 'res://assets/characters/2D Card/Sheep_card.png', tier: 'Common' },
	{ id: 8, name: 'Rabbit', path: 'res://assets/characters/Rabbid/Rabbid.tscn', card_path: 'res://assets/characters/2D Card/Rabbid_card.png', tier: 'Common' },
	{ id: 9, name: 'Monkey', path: 'res://assets/characters/Monkey/Monkey.tscn', card_path: 'res://assets/characters/2D Card/Monkey_card.png', tier: 'Common' },
	{ id: 10, name: 'Elephant', path: 'res://assets/characters/Elephant/Elephant.tscn', card_path: 'res://assets/characters/2D Card/Elephant_card.png', tier: 'Common' },
	{ id: 11, name: 'Lion', path: 'res://assets/characters/Lion/Lion.tscn', card_path: 'res://assets/characters/2D Card/Lion_card.png', tier: 'Common' },
	{ id: 12, name: 'Bear', path: 'res://assets/characters/Bear/Bear.tscn', card_path: 'res://assets/characters/2D Card/Bear_card.png', tier: 'Common' },
	{ id: 13, name: 'Samurai Bear', path: 'res://assets/characters/Bear/Samurai_Bear.tscn', card_path: 'res://assets/characters/2D Card/Samurai_Bear_card.png', tier: 'Legendary' },
	{ id: 14, name: 'Samurai Elephant', path: 'res://assets/characters/Elephant/Samurai_elephant.tscn', card_path: 'res://assets/characters/2D Card/Samurai_Elephant_card.png', tier: 'Legendary' },
	{ id: 15, name: 'Samurai Fox', path: 'res://assets/characters/Fox/Samurai_fox.tscn', card_path: 'res://assets/characters/2D Card/Samurai_Fox_card.png', tier: 'Legendary' },
	{ id: 16, name: 'Samurai Horse', path: 'res://assets/characters/Horse/Samurai_horse.tscn', card_path: 'res://assets/characters/2D Card/Samurai_Horse_card.png', tier: 'Legendary' },
	{ id: 17, name: 'Samurai Leopard', path: 'res://assets/characters/Leopard/Samurai_leopard.tscn', card_path: 'res://assets/characters/2D Card/Samurai_Leopard_card.png', tier: 'Legendary' },
	{ id: 18, name: 'Samurai Monkey', path: 'res://assets/characters/Monkey/Samurai_Monkey.tscn', card_path: 'res://assets/characters/2D Card/Samurai_Monkey_card.png', tier: 'Legendary' },
	{ id: 19, name: 'Samurai Lion', path: 'res://assets/characters/Lion/Samurai_Lion.tscn', card_path: 'res://assets/characters/2D Card/Samurai_Lion_card.png', tier: 'Legendary' },
	{ id: 20, name: 'Samurai Rabbit', path: 'res://assets/characters/Rabbid/Samurai_Rabbid.tscn', card_path: 'res://assets/characters/2D Card/Samurai_Rabbid_card.png', tier: 'Legendary' },
	{ id: 21, name: 'Samurai Sheep', path: 'res://assets/characters/Sheep/Samurai_Sheep.tscn', card_path: 'res://assets/characters/2D Card/Samurai_Sheep_card.png', tier: 'Legendary' },
	{ id: 33, name: 'Samurai Frog', path: 'res://assets/characters/Frog/Samurai_frog.tscn', card_path: 'res://assets/characters/2D Card/Samurai_Frog_card.png', tier: 'Legendary' },
	{ id: 22, name: 'Astronaut Bear', path: 'res://assets/characters/Astronaut/Astronaut_bear.tscn', card_path: 'res://assets/characters/2D Card/Astronaut_Bear_card.png', tier: 'Legendary' },
	{ id: 23, name: 'Astronaut Elephant', path: 'res://assets/characters/Astronaut/Astronaut_elephant.tscn', card_path: 'res://assets/characters/2D Card/Astronaut_Elephant_card.png', tier: 'Legendary' },
	{ id: 24, name: 'Astronaut Fox', path: 'res://assets/characters/Astronaut/Astronaut_fox.tscn', card_path: 'res://assets/characters/2D Card/Astronaut_Fox_card.png', tier: 'Legendary' },
	{ id: 25, name: 'Astronaut Frog', path: 'res://assets/characters/Astronaut/Astronaut_frog.tscn', card_path: 'res://assets/characters/2D Card/Astronaut_Frog_card.png', tier: 'Legendary' },
	{ id: 26, name: 'Astronaut Horse', path: 'res://assets/characters/Astronaut/Astronaut_horse.tscn', card_path: 'res://assets/characters/2D Card/Astronaut_Horse_card.png', tier: 'Legendary' },
	{ id: 27, name: 'Astronaut Leopard', path: 'res://assets/characters/Astronaut/Astronaut_leopard.tscn', card_path: 'res://assets/characters/2D Card/Astronaut_Leopard_card.png', tier: 'Legendary' },
	{ id: 28, name: 'Astronaut Lion', path: 'res://assets/characters/Astronaut/Astronaut_lion.tscn', card_path: 'res://assets/characters/2D Card/Astronaut_Lion_card.png', tier: 'Legendary' },
	{ id: 29, name: 'Astronaut Monkey', path: 'res://assets/characters/Astronaut/Astronaut_monkey.tscn', card_path: 'res://assets/characters/2D Card/Astronaut_Monkey_card.png', tier: 'Legendary' },
	{ id: 30, name: 'Astronaut Rabbit', path: 'res://assets/characters/Astronaut/Astronaut_rabbit.tscn', card_path: 'res://assets/characters/2D Card/Astronaut_Rabbid_card.png', tier: 'Legendary' },
	{ id: 31, name: 'Astronaut Sheep', path: 'res://assets/characters/Astronaut/Astronaut_sheep.tscn', card_path: 'res://assets/characters/2D Card/Astronaut_Sheep_card.png', tier: 'Legendary' },
	{ id: 32, name: 'Azari', path: 'res://assets/characters/AzariOutfits/human_azari.tscn', card_path: 'res://assets/characters/2D Card/Human_Azzari_Card.png', tier: 'Rare' },
	{ id: 34, name: 'Kurd', path: 'res://assets/characters/Kurd/human_kurd.tscn', card_path: 'res://assets/characters/2D Card/Human_Kurd_Card.png', tier: 'Rare' },
	{ id: 35, name: 'Parinaz', path: 'res://assets/characters/Human/Farinaz.tscn', card_path: 'res://assets/characters/2D Card/Farinaz_card.png', tier: 'Common' },
	{ id: 43, name: 'Dog', path: 'res://assets/characters/Dog/Dog.tscn', card_path: 'res://assets/characters/2D Card/Dog_card.png', tier: 'Common' },
	{ id: 44, name: 'Rhino', path: 'res://assets/characters/Rhino/Rhino.tscn', card_path: 'res://assets/characters/2D Card/Rhino_card.png', tier: 'Rare' },
	{ id: 45, name: 'Penguin', path: 'res://assets/characters/Penguin/Penguin.tscn', card_path: 'res://assets/characters/2D Card/Penguin_card.png', tier: 'Common' },
	{ id: 46, name: 'Shark', path: 'res://assets/characters/Shark/Shark.tscn', card_path: 'res://assets/characters/2D Card/Shark_card.png', tier: 'Rare' },
	{ id: 48, name: 'Police', path: 'res://assets/characters/Police/Police.tscn', card_path: 'res://assets/characters/2D Card/Police_card.png', tier: 'Legendary' },
	{ id: 47, name: 'Kouroosh', path: 'res://assets/characters/Kouroosh/Kouroosh.tscn', card_path: 'res://assets/characters/2D Card/Kouroosh_card.png', tier: 'Epic' },
	{ id: 49, name: 'Mia', path: 'res://assets/characters/Mia/Mia.tscn', card_path: 'res://assets/characters/2D Card/Mia_card.png', tier: 'Epic' },
	{ id: 50, name: 'Nopo', path: 'res://assets/characters/Nopo/Nopo.tscn', card_path: 'res://assets/characters/2D Card/Nopo_card.png', tier: 'Epic' },
	{ id: 51, name: 'Lor', path: 'res://assets/characters/Lor/Lor.tscn', card_path: 'res://assets/characters/2D Card/Lor_card.png', tier: 'Rare' },
	{ id: 52, name: 'Panda', path: 'res://assets/characters/Panda/Panda.tscn', card_path: 'res://assets/characters/2D Card/Panda_card.png', tier: 'Rare' },
	{ id: 53, name: 'Ninja', path: 'res://assets/characters/Ninja/Ninja.tscn', card_path: 'res://assets/characters/2D Card/Ninja_card.png', tier: 'Epic' },
	{ id: 54, name: 'Bee', path: 'res://assets/characters/Bee/Bee.tscn', card_path: 'res://assets/characters/2D Card/Bee_card.png', tier: 'Legendary' },
	{ id: 55, name: 'NaderShah', path: 'res://assets/characters/Nadershah/Nadershah.tscn', card_path: 'res://assets/characters/2D Card/Nadershah_card.png', tier: 'Epic' },
	{ id: 56, name: 'Patrick', path: 'res://assets/characters/Patrick/Patrick.tscn', card_path: 'res://assets/characters/2D Card/Patrick_card.png', tier: 'Epic' },
	{ id: 57, name: 'SpongeBob', path: 'res://assets/characters/SpongeBob/SpongeBob.tscn', card_path: 'res://assets/characters/2D Card/SpongeBob_card.png', tier: 'Epic' },
	{ id: 58, name: 'Engineer', path: 'res://assets/characters/Engineer/Engineer.tscn', card_path: 'res://assets/characters/2D Card/Engineer_card.png', tier: 'Rare' },
	{ id: 59, name: 'Graduated', path: 'res://assets/characters/Graduated/Graduated.tscn', card_path: 'res://assets/characters/2D Card/Graduated_card.png', tier: 'Rare' },
	{ id: 60, name: 'Leonardo', path: 'res://assets/characters/TMNT/Leonardo/Leonardo.tscn', card_path: 'res://assets/characters/2D Card/Leonardo_card.png', tier: 'Legendary' },
	{ id: 61, name: 'Rapheal', path: 'res://assets/characters/TMNT/Raphaeal/Raphael.tscn', card_path: 'res://assets/characters/2D Card/Rapheal_card.png', tier: 'Legendary' },
	{ id: 62, name: 'Danatello', path: 'res://assets/characters/TMNT/donatello/Danatello.tscn', card_path: 'res://assets/characters/2D Card/Danatello_card.png', tier: 'Legendary' },
	{ id: 63, name: 'Michelangelo', path: 'res://assets/characters/TMNT/Michelangelo/Michelangelo.tscn', card_path: 'res://assets/characters/2D Card/Michelangelo_card.png', tier: 'Legendary' },
	{ id: 64, name: 'Eren Yeager', path: 'res://assets/characters/Eren Yeager/Eren Yeager.tscn', card_path: 'res://assets/characters/2D Card/ErenYeager_card.png', tier: 'Epic' },
	{ id: 65, name: 'Soldier', path: 'res://assets/characters/Soldier/Soldier.tscn', card_path: 'res://assets/characters/2D Card/Soldier_card.png', tier: 'Legendary' },
	{ id: 66, name: 'RedHood', path: 'res://assets/characters/RedHood/RedHood.tscn', card_path: 'res://assets/characters/2D Card/RedHood_card.png', tier: 'Legendary' },
	{ id: 67, name: 'Pilot', path: 'res://assets/characters/Pilot/Pilot.tscn', card_path: 'res://assets/characters/2D Card/Pilot_card.png', tier: 'Legendary' },
	{ id: 68, name: 'Elsa', path: 'res://assets/characters/Elsa/Elsa.tscn', card_path: 'res://assets/characters/2D Card/Elsa_card.png', tier: 'Epic' },
	{ id: 69, name: 'Merida', path: 'res://assets/characters/Merida/Merida.tscn', card_path: 'res://assets/characters/2D Card/Merida_card.png', tier: 'Epic' },
	{ id: 70, name: 'Geek', path: 'res://assets/characters/Vision Pro/VisionPro.tscn', card_path: 'res://assets/characters/2D Card/VisionPro_card.png', tier: 'Legendary' },
	{ id: 71, name: 'FootBallPlayer', path: 'res://assets/characters/Football Player/FootBallPlayer.tscn', card_path: 'res://assets/characters/2D Card/FootballPlayer_card.png', tier: 'Epic' },
	{ id: 72, name: 'Scientist', path: 'res://assets/characters/Scientist/Scientist.tscn', card_path: 'res://assets/characters/2D Card/Scintist_card.png', tier: 'Legendary' },
	{ id: 73, name: 'Butcher', path: 'res://assets/characters/Butcher/Butcher.tscn', card_path: 'res://assets/characters/2D Card/Butcher_card.png', tier: 'Epic' },
	{ id: 74, name: 'Doctor', path: 'res://assets/characters/Doctor/Doctor.tscn', card_path: 'res://assets/characters/2D Card/Doctor_card.png', tier: 'Rare' },
	{ id: 75, name: 'BankClerk', path: 'res://assets/characters/BankClerk/BankClerk.tscn', card_path: 'res://assets/characters/2D Card/BankClerk_card.png', tier: 'Rare' },
	{ id: 76, name: 'Rostam', path: 'res://assets/characters/Rostam/Rostam.tscn', card_path: 'res://assets/characters/2D Card/Rostam_card.png', tier: 'Epic' },
	{ id: 77, name: 'PersianPrincess', path: 'res://assets/characters/PersianPrincess/PersianPrincess.tscn', card_path: 'res://assets/characters/2D Card/PersianPrincess_card.png', tier: 'Epic' },
	{ id: 78, name: 'AghaTakhti', path: 'res://assets/characters/AghaTakhti/AghaTakhti.tscn', card_path: 'res://assets/characters/2D Card/AghaTakhti_card.png', tier: 'Epic' },
	{ id: 79, name: 'AmirKabir', path: 'res://assets/characters/AmirKabir/AmirKabir.tscn', card_path: 'res://assets/characters/2D Card/AmirKabir_card.png', tier: 'Legendary' },
	{ id: 80, name: 'AndrewTate', path: 'res://assets/characters/AndrewTate/AndrewTate.tscn', card_path: 'res://assets/characters/2D Card/AndrewTate_card.png', tier: 'Epic' },
	{ id: 81, name: 'Batman', path: 'res://assets/characters/Batman/Batman.tscn', card_path: 'res://assets/characters/2D Card/Batman_card.png', tier: 'Epic' },
	{ id: 82, name: 'ElonMask', path: 'res://assets/characters/ElonMask/ElonMask.tscn', card_path: 'res://assets/characters/2D Card/ElonMask_card.png', tier: 'Epic' },
	{ id: 83, name: 'FireFighter', path: 'res://assets/characters/FireFighter/FireFighter.tscn', card_path: 'res://assets/characters/2D Card/FireFighter_card.png', tier: 'Rare' },
	{ id: 84, name: 'HassanYazdani', path: 'res://assets/characters/HassanYazdani/HassanYazdani.tscn', card_path: 'res://assets/characters/2D Card/HassanYazdani_card.png', tier: 'Legendary' },
	{ id: 85, name: 'HazMat', path: 'res://assets/characters/HazMat/HazMat.tscn', card_path: 'res://assets/characters/2D Card/HazMat_card.png', tier: 'Legendary' },
	{ id: 86, name: 'Jumong', path: 'res://assets/characters/Jumong/Jumong.tscn', card_path: 'res://assets/characters/2D Card/Jumong_card.png', tier: 'Epic' },
	{ id: 87, name: 'KarateKa', path: 'res://assets/characters/KarateKa/KarateKa.tscn', card_path: 'res://assets/characters/2D Card/KarateKa_card.png', tier: 'Rare' },
	{ id: 88, name: 'KaveAhangar', path: 'res://assets/characters/KaveAhangar/KaveAhangar.tscn', card_path: 'res://assets/characters/2D Card/KaveAhangar_card.png', tier: 'Epic' },
	{ id: 89, name: 'NaserAldinShah', path: 'res://assets/characters/NaserEldinShah/NaserEldinShah.tscn', card_path: 'res://assets/characters/2D Card/NaserAldinShah_Card.png', tier: 'Epic' },
	{ id: 90, name: 'PuriaVali', path: 'res://assets/characters/PuriaVali/PuriaVali.tscn', card_path: 'res://assets/characters/2D Card/PuriaVali_card.png', tier: 'Epic' },
	{ id: 91, name: 'Simurgh', path: 'res://assets/characters/Simurgh/Simurgh.tscn', card_path: 'res://assets/characters/2D Card/Simurgh_card.png', tier: 'Epic' },
	{ id: 92, name: 'WalterHazmat', path: 'res://assets/characters/HazMat/HazMatWalter.tscn', card_path: 'res://assets/characters/2D Card/WalterHazmat.png', tier: 'Epic' },
	{ id: 93, name: 'WalterWhite', path: 'res://assets/characters/WalterWhite/WalterWhite.tscn', card_path: 'res://assets/characters/2D Card/WalterWhite_card.png', tier: 'Legendary' },
	{ id: 94, name: 'ChefFemale', path: 'res://assets/characters/Chef/ChefFemale.tscn', card_path: 'res://assets/characters/2D Card/ChefFemale_Card.png', tier: 'Rare' },
	{ id: 95, name: 'ChefMale', path: 'res://assets/characters/Chef/ChefMale.tscn', card_path: 'res://assets/characters/2D Card/ChefMale_Card.png', tier: 'Rare' },
	{ id: 96, name: 'GarsonMale', path: 'res://assets/characters/Garson/GarsonMale.tscn', card_path: 'res://assets/characters/2D Card/GarsonMale_Card.png', tier: 'Rare' },
	{ id: 97, name: 'GarsonFemale', path: 'res://assets/characters/Garson/GarsonFemale.tscn', card_path: 'res://assets/characters/2D Card/GarsonFemale_Card.png', tier: 'Rare' },
	{ id: 98, name: 'Boss', path: 'res://assets/characters/Boss/Boss.tscn', card_path: 'res://assets/characters/2D Card/Boss_Card.png', tier: 'Legendary' },
	{ id: 99, name: 'DoctorFemale', path: 'res://assets/characters/Doctor/DoctorFemale.tscn', card_path: 'res://assets/characters/2D Card/DoctorFemale_Card.png', tier: 'Rare' },
	{ id: 100, name: 'Nurse', path: 'res://assets/characters/Nurse/Nurse.tscn', card_path: 'res://assets/characters/2D Card/Nurse_Card.png', tier: 'Rare' },
	{ id: 101, name: 'PoliceEntezami', path: 'res://assets/characters/PoliceEntezami/PoliceEntezami.tscn', card_path: 'res://assets/characters/2D Card/policeentezami.png', tier: 'Legendary' },
	{ id: 102, name: 'PoliceFemale', path: 'res://assets/characters/PoliceFemale/PoliceFemale.tscn', card_path: 'res://assets/characters/2D Card/pfr.png', tier: 'Legendary' },
	{ id: 103, name: 'Robber', path: 'res://assets/characters/Robber/Robber.tscn', card_path: 'res://assets/characters/2D Card/Robber.png', tier: 'Epic' },
	{ id: 104, name: 'SardarSepah', path: 'res://assets/characters/SardarSepah/SardarSepah.tscn', card_path: 'res://assets/characters/2D Card/sepah.png', tier: 'Epic' },
	{ id: 105, name: 'SardarArtesh', path: 'res://assets/characters/SardarArtesh/SardarArtesh.tscn', card_path: 'res://assets/characters/2D Card/sardarartesh.png', tier: 'Epic' },
	{ id: 106, name: 'Ronaldo', path: 'res://assets/characters/Ronaldo/Ronaldo.tscn', card_path: 'res://assets/characters/Ronaldo/ronaldorender.png', tier: 'Epic' },
	{ id: 107, name: 'Messi', path: 'res://assets/characters/Messi/Messi.tscn', card_path: 'res://assets/characters/Messi/messirender.png', tier: 'Epic' },
	{ id: 108, name: 'Nezoko', path: 'res://assets/characters/Nezoko/Nezoko.tscn', card_path: 'res://assets/characters/Nezoko/nezukorender.png', tier: 'Epic' },
	{ id: 109, name: 'SquidGame', path: 'res://assets/characters/SquidGame/SquidGame.tscn', card_path: 'res://assets/characters/SquidGame/rendersquidgame.png', tier: 'Epic' },
	{ id: 110, name: 'Tanjiro', path: 'res://assets/characters/Tanjiro/Tanjiro.tscn', card_path: 'res://assets/characters/Tanjiro/TANJIROrender.png', tier: 'Epic' },
	{ id: 111, name: 'Cyrus', path: 'res://assets/characters/Cyrus/Cyrus.tscn', card_path: 'res://assets/characters/Cyrus/Cyrusrender.png', tier: 'Epic' },
	{ id: 112, name: 'BossLady', path: 'res://assets/characters/BossLady/BossLady.tscn', card_path: 'res://assets/characters/BossLady/bossladyrender.png', tier: 'Legendary' },
	{ id: 113, name: 'Bride', path: 'res://assets/characters/Bride/Bride.tscn', card_path: 'res://assets/characters/Bride/briderender.png', tier: 'Legendary' },
	{ id: 114, name: 'Groom', path: 'res://assets/characters/Groom/Groom.tscn', card_path: 'res://assets/characters/Groom/GROOMRENDER.png', tier: 'Legendary' },
	{ id: 115, name: 'HadiChoopan', path: 'res://assets/characters/HadiChoopan/HadiChoopan.tscn', card_path: 'res://assets/characters/HadiChoopan/hadichoopanrender.png', tier: 'Epic' },
	{ id: 116, name: 'MoeinXM', path: 'res://assets/characters/MoeinXM/MoeinXM.tscn', card_path: 'res://assets/characters/2D Card/MoinXM_card.png', tier: 'Epic' },
	{ id: 117, name: 'Aghed', path: 'res://assets/characters/Aghed/Aghed.tscn', card_path: 'res://assets/characters/2D Card/Aghed_card.png', tier: 'Legendary' },
	{ id: 118, name: 'Spiderman', path: 'res://assets/characters/Spiderman/Spiderman.tscn', card_path: 'res://assets/characters/Spiderman/Spidermanrender.png', tier: 'Epic' },
	{ id: 119, name: 'ThomasShelby', path: 'res://assets/characters/ThomasShelby/ThomasShelby.tscn', card_path: 'res://assets/characters/ThomasShelby/shelbyrender.png', tier: 'Epic' },
	{ id: 120, name: 'HarryPotter', path: 'res://assets/characters/HarryPotter/HarryPotter.tscn', card_path: 'res://assets/characters/HarryPotter/HPRENDER.png', tier: 'Epic' },
	{ id: 121, name: 'AmongUs', path: 'res://assets/characters/AmongUs/AmongUs.tscn', card_path: 'res://assets/characters/AmongUs/amongusrender.png', tier: 'Epic' },
	{ id: 122, name: 'MrCrab', path: 'res://assets/characters/MrCrab/MrCrab.tscn', card_path: 'res://assets/characters/MrCrab/mrkrabsrender.png', tier: 'Epic' },
	{ id: 123, name: 'Luffy', path: 'res://assets/characters/Luffy/Luffy.tscn', card_path: 'res://assets/characters/Luffy/luffyrender.png', tier: 'Epic' },
	{ id: 124, name: 'FemaleClerk', path: 'res://assets/characters/FemaleClerk/FemaleClerk.tscn', card_path: 'res://assets/characters/FemaleClerk/FemaleClerk.png', tier: 'Rare' },
	{ id: 125, name: 'Shrek', path: 'res://assets/characters/Shrek/Shrek.tscn', card_path: 'res://assets/characters/Shrek/shrekrender.png', tier: 'Epic' },
	{ id: 126, name: 'Deadpool', path: 'res://assets/characters/Deadpool/Deadpool.tscn', card_path: 'res://assets/characters/Deadpool/DeadPool_card.png', tier: 'Epic' },
	{ id: 127, name: 'Leon', path: 'res://assets/characters/Leon/Leon.tscn', card_path: 'res://assets/characters/Leon/Leon_card.png', tier: 'Epic' },
	{ id: 128, name: 'Matilda', path: 'res://assets/characters/Matlida/Matlida.tscn', card_path: 'res://assets/characters/Matlida/Matilda_card.png', tier: 'Epic' },
	{ id: 129, name: 'ShahAbbas', path: 'res://assets/characters/ShahAbbas/ShahAbbas.tscn', card_path: 'res://assets/characters/ShahAbbas/ShahAbas.png', tier: 'Epic' },
	{ id: 130, name: 'Brucelee', path: 'res://assets/characters/Brucelee/BruceLee.tscn', card_path: 'res://assets/characters/Brucelee/bruceleerender.png', tier: 'Epic' },
	{ id: 131, name: 'DaeiHamed', path: 'res://assets/characters/DaeiHamed/DaeiHamed.tscn', card_path: 'res://assets/characters/DaeiHamed/DaiHamed_card.png', tier: 'Epic' },
	{ id: 132, name: 'Fiona', path: 'res://assets/characters/Fiona/Fiona.tscn', card_path: 'res://assets/characters/Fiona/Fiona_card.png', tier: 'Epic' },
	{ id: 133, name: 'Hitman', path: 'res://assets/characters/Hitman/Hitman.tscn', card_path: 'res://assets/characters/Hitman/hitmanrender.png', tier: 'Epic' },
	{ id: 134, name: 'Kaseb', path: 'res://assets/characters/Kaseb/Kaseb.tscn', card_path: 'res://assets/characters/Kaseb/kasebrender.png', tier: 'Epic' },
	{ id: 135, name: 'Khiabani', path: 'res://assets/characters/Khiabani/Khiabani.tscn', card_path: 'res://assets/characters/Khiabani/khiabanirender.png', tier: 'Epic' },
	{ id: 136, name: 'Looti', path: 'res://assets/characters/Looti/Looti.tscn', card_path: 'res://assets/characters/Looti/lootirender.png', tier: 'Epic' },
	{ id: 137, name: 'Mikasa', path: 'res://assets/characters/Mikasa/Mikasa.tscn', card_path: 'res://assets/characters/Mikasa/Mikasa_card.png', tier: 'Epic' },
	{ id: 138, name: 'MrBeast', path: 'res://assets/characters/MrBeast/Mrbeast.tscn', card_path: 'res://assets/characters/MrBeast/mrbeastrender.png', tier: 'Epic' },
	{ id: 139, name: 'Naruto', path: 'res://assets/characters/Naruto/Naroto.tscn', card_path: 'res://assets/characters/Naruto/narutorender.png', tier: 'Epic' },
	{ id: 140, name: 'Neymar', path: 'res://assets/characters/Neymar/Neymar.tscn', card_path: 'res://assets/characters/Neymar/neymar render.png', tier: 'Epic' },
	{ id: 141, name: 'Ragnar', path: 'res://assets/characters/Ragnar/Ragnar.tscn', card_path: 'res://assets/characters/Ragnar/ragnarrender.png', tier: 'Epic' },
	{ id: 142, name: 'Ronaldinho', path: 'res://assets/characters/Ronaldinho/Ronaldinho.tscn', card_path: 'res://assets/characters/Ronaldinho/ronaldinhorender.png', tier: 'Epic' },
	{ id: 143, name: 'Sakura', path: 'res://assets/characters/Sakura/Sakura.tscn', card_path: 'res://assets/characters/Sakura/Sakura_card.png', tier: 'Epic' },
	{ id: 144, name: 'Sandi', path: 'res://assets/characters/Sandi/Sandi.tscn', card_path: 'res://assets/characters/Sandi/Sandi_card.png', tier: 'Epic' },
	{ id: 145, name: 'Octopus', path: 'res://assets/characters/Octopus/Octopus.tscn', card_path: 'res://assets/characters/Octopus/octopusrender.png', tier: 'Epic' },
	{ id: 146, name: 'Steve', path: 'res://assets/characters/Steve/Steve.tscn', card_path: 'res://assets/characters/Steve/Steverender.png', tier: 'Epic' },
	{ id: 147, name: 'Arash', path: 'res://assets/characters/Arash/Arash.tscn', card_path: 'res://assets/characters/Arash/ArashKamanGir_card.png', tier: 'Epic' },
	{ id: 148, name: 'Diego', path: 'res://assets/characters/Diego/Diego.tscn', card_path: 'res://assets/characters/Diego/diegorender.png', tier: 'Epic' },
	{ id: 149, name: 'Manny', path: 'res://assets/characters/Manny/Manny.tscn', card_path: 'res://assets/characters/Manny/Mannyrender.png', tier: 'Special' },
	{ id: 150, name: 'Scrat', path: 'res://assets/characters/Scrat/Scrat.tscn', card_path: 'res://assets/characters/Scrat/scratrender.png', tier: 'Epic' },
	{ id: 151, name: 'Sid', path: 'res://assets/characters/Sid/Sid.tscn', card_path: 'res://assets/characters/Sid/sidrender.png', tier: 'Special' },
	{ id: 152, name: 'HassanSabbah', path: 'res://assets/characters/HassanSabbah/HassanSabbah.tscn', card_path: 'res://assets/characters/HassanSabbah/HassanSabah_card.png', tier: 'Special' },
	{ id: 153, name: 'JohnWick', path: 'res://assets/characters/John Wick/JohnWick.tscn', card_path: 'res://assets/characters/John Wick/JhonWick_card.png', tier: 'Special' },
	{ id: 154, name: 'Frontman', path: 'res://assets/characters/Frontman/Frontman.tscn', card_path: 'res://assets/characters/Frontman/frontmanrender.png', tier: 'Special' },
	{ id: 155, name: 'Ghost', path: 'res://assets/characters/Ghost/Ghost.tscn', card_path: 'res://assets/characters/Ghost/Ghost_card.png', tier: 'Special' },
	{ id: 156, name: 'Eskimoboy', path: 'res://assets/characters/Eskimoboy/Eskimoboy.tscn', card_path: 'res://assets/characters/Eskimoboy/eskimoboyrender.png', tier: 'Legendary' },
	{ id: 157, name: 'Eskimogirl', path: 'res://assets/characters/Eskimogirl/Eskimogirl.tscn', card_path: 'res://assets/characters/Eskimogirl/eskimogirlrender.png', tier: 'Legendary' },
	{ id: 158, name: 'Olaf', path: 'res://assets/characters/Olaf/Olaf.tscn', card_path: 'res://assets/characters/Olaf/olafrender.png', tier: 'Special' },
	{ id: 159, name: 'Sonic', path: 'res://assets/characters/Sonic/Sonic.tscn', card_path: 'res://assets/characters/Sonic/sonicrender.png', tier: 'Special' },
	{ id: 160, name: 'Mrbean', path: 'res://assets/characters/Mrbean/Mrbean.tscn', card_path: 'res://assets/characters/Mrbean/mrbeanrender.png', tier: 'Special' },
	{ id: 161, name: 'Joker', path: 'res://assets/characters/Joker/Joker.tscn', card_path: 'res://assets/characters/Joker/jokertex.png', tier: 'Special' },
	{ id: 162, name: 'Sattarkhan', path: 'res://assets/characters/Sattarkhan/Sattarkan.tscn', card_path: 'res://assets/characters/Sattarkhan/sattarkhanrender.png', tier: 'Special' },
	{ id: 163, name: 'Mohsenlor', path: 'res://assets/characters/Mohsenloretani/MohsenLor.tscn', card_path: 'res://assets/characters/Mohsenloretani/lorestanirender.png', tier: 'Special' },
	{ id: 164, name: 'Habbib', path: 'res://assets/characters/Habbib/Habbib.tscn', card_path: 'res://assets/characters/Habbib/Habbib_card.png', tier: 'Epic' },
	{ id: 165, name: 'Gigachad', path: 'res://assets/characters/Gigachad/Gigachad.tscn', card_path: 'res://assets/characters/Gigachad/gigarender.png', tier: 'Epic' },
	{ id: 166, name: 'Yeti', path: 'res://assets/characters/Yeti/Yeti.tscn', card_path: 'res://assets/characters/Yeti/yetirender.png', tier: 'Special' },
];
const TIER_PRICE = { Common: 1000, Rare: 3000, Legendary: 8000 };
const CLAN_LEVELS = [];
for (let i = 1; i <= 5; i++) CLAN_LEVELS.push({ level: i, max_count: 10 + i * 10, price: 1000 * i });

let state = {
	accounts: {},
	tokens: {},
	userCounter: 0,
	servers: { race: [], freeride: [] },
	serverCounter: 0,
	clans: [],
};
function loadState() {
	try { state = Object.assign(state, JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'))); } catch (e) {}
}
let saveTimer = null;
function saveState() {
	if (saveTimer) return;
	saveTimer = setTimeout(() => {
		saveTimer = null;
		try { fs.writeFileSync(STATE_FILE, JSON.stringify(state)); } catch (e) {}
	}, 500);
}

function newAccount(username) {
	return {
		username,
		handle: 'Player' + (++state.userCounter),
		coin: 100000,
		cup: 0, crown: 0, win_count: 0, game_count: 0,
		hunger: 100, warmth: 100,
		title: '', title_color: '',
		is_test: false, name_changed_count: 0, show_debug: false,
		ban_time: 0, free_admin: false, bazras: false, stealth: false, chat_admin: false,
		jail_time: 0, in_prison: false,
		email: '', daily_claim_time: 0,
		progress_level: 1, is_meta_progress_finished: true,
		characters: CHARS.map((c) => Object.assign({}, c)),
		purchases: [],
		animations: {},
		data: {},
		clan_id: null,
	};
}
function accountFor(token) {
	if (!token) return null;
	if (state.tokens[token]) return state.accounts[state.tokens[token]];
	const username = 'u' + (++state.userCounter) + '_' + Math.random().toString(36).slice(2, 7);
	state.accounts[username] = newAccount(username);
	state.tokens[token] = username;
	saveState();
	return state.accounts[username];
}
function getChar(id) {
	for (const c of CHARS) if (c.id === id) return c;
	return null;
}

const NL = String.fromCharCode(10);
function log(line) {
	const t = new Date().toISOString().slice(11, 19);
	const out = '[' + t + '] ' + line;
	console.log(out);
	try { fs.appendFileSync(LOG_FILE, out + NL); } catch (e) {}
}
function send(res, code, obj) {
	const body = JSON.stringify(obj == null ? {} : obj);
	res.writeHead(code, { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) });
	res.end(body);
}
function readBody(req) {
	return new Promise((resolve) => {
		let chunks = [];
		req.on('data', (c) => chunks.push(c));
		req.on('end', () => {
			try { resolve(JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}')); }
			catch (e) { resolve({}); }
		});
	});
}
function auth(req) {
	const h = req.headers['authorization'] || '';
	const token = h.startsWith('JWT ') ? h.slice(4) : h;
	return accountFor(token);
}
function memberJson(a) {
	return {
		id: a.username, handle: a.handle, cup: a.cup, coin: a.coin, crown: a.crown,
		email: a.email, daily_claim_time: a.daily_claim_time,
		hunger: a.hunger, warmth: a.warmth,
		title: a.title, title_color: a.title_color,
		is_test: a.is_test, name_changed_count: a.name_changed_count,
		show_debug: a.show_debug, ban_time: a.ban_time, free_admin: a.free_admin,
		bazras: a.bazras, stealth: a.stealth, chat_admin: a.chat_admin,
		jail_time: a.jail_time, in_prison: a.in_prison,
		progress_level: a.progress_level, is_meta_progress_finished: a.is_meta_progress_finished,
		win_count: a.win_count, game_count: a.game_count,
	};
}
const SYNC_PRICES = {
	character_common: 1000, character_rare: 3000, character_legendary: 8000, character_epic: 20000,
	character_common_exact: 1500, character_rare_exact: 4000, character_legendary_exact: 10000,
	character_epic_exact: 25000, character_special_exact: 50000,
	game_tax: 0, chat_cup: 0, change_name_price: 0, animation_price: 500,
	coin_transfer_fee: 0, day_start_hour: 7, night_start_hour: 19,
	reward_video_coins: 50, reward_video_hp: 20,
	force_update_from_url: false, update_store_url: '',
	voice_call_price: 50, voice_call_per_minute: 60,
	force_version: 0, last_version: 0,
	game_is_down: false, up_counter: 0,
};

const routes = [];
function route(match, handler) { routes.push({ match, handler }); }

route('POST /account/register/', (req, res, body) => {
	const username = 'u' + (++state.userCounter) + '_' + Math.random().toString(36).slice(2, 7);
	const a = newAccount(username);
	state.accounts[username] = a;
	const token = 'T' + username + '.' + Math.random().toString(36).slice(2);
	state.tokens[token] = username;
	saveState();
	log('register -> ' + username);
	send(res, 200, { handle: a.handle, token, username });
});

route('POST /account/sync/', (req, res, body, a) => {
	send(res, 200, {
		data: { data: a.data },
		member: memberJson(a),
		characters: a.characters,
		sync: SYNC_PRICES,
		online_count: 1,
		public_chat: 'PublicChat',
		progresses: [],
		phones: [],
		clan: a.clan_id ? (state.clans.find((c) => c.id === a.clan_id) || null) : null,
		clan_levels: CLAN_LEVELS,
	});
});

route('POST /account/save_data/', (req, res, body, a) => {
	if (body && typeof body === 'object') {
		const jwt = a.data['JWT'];
		a.data = body;
		if (jwt) a.data['JWT'] = jwt;
		if (a.data['hunger'] != null) a.hunger = a.data['hunger'];
		if (a.data['warmth'] != null) a.warmth = a.data['warmth'];
		saveState();
	}
	send(res, 200, {});
});

route('POST /account/change_handle/', (req, res, body, a) => {
	if (body.handle) a.handle = String(body.handle).slice(0, 12);
	saveState();
	send(res, 200, {});
});

route('POST /account/am_i_ban/', (req, res, body, a) => {
	send(res, 200, { member: { ban_time: a.ban_time, coin: a.coin, title: a.title, title_color: a.title_color, jail_time: a.jail_time, in_prison: a.in_prison } });
});

route('POST /account/tutorial_started/', (req, res) => send(res, 200, {}));
route('POST /account/tutorial_finished/', (req, res) => send(res, 200, {}));
route('POST /account/nakama_connect/', (req, res) => send(res, 200, {}));
route('POST /account/server_test_fail/', (req, res) => send(res, 200, {}));
route('POST /game/request_error/', (req, res) => send(res, 200, {}));
route('POST /account/update_presence/', (req, res) => send(res, 200, {}));

route('POST /account/request_code/', (req, res, body, a) => { a.email = body.email || a.email; saveState(); send(res, 200, {}); });
route('POST /account/verify_code/', (req, res, body, a) => { a.email = body.email || a.email; saveState(); send(res, 200, { ok: true }); });
route('POST /account/remove_email/', (req, res, body, a) => { a.email = ''; saveState(); send(res, 200, {}); });

route('POST /shop/list_shop/', (req, res) => send(res, 200, { gateway_type: 'IAP', items: [] }));
route('POST /shop/verify_purchase/', (req, res, body, a) => send(res, 200, { coin: a.coin, characters: [], id: 0 }));
route('POST /shop/ipg/', (req, res) => send(res, 400, {}));
route('POST /shop/list_gifts/', (req, res) => send(res, 200, { gifts: [] }));
route('POST /shop/seen_gifts/', (req, res) => send(res, 200, {}));

route('POST /shop/daily_reward/', (req, res, body, a) => {
	const now = Math.floor(Date.now() / 1000);
	if (a.daily_claim_time && now - a.daily_claim_time < 24 * 3600) {
		send(res, 200, { prize: 0, coins: a.coin });
		return;
	}
	const prize = [50, 60, 70, 80, 90, 95, 100, 200][Math.floor(Math.random() * 8)];
	a.coin += prize;
	a.daily_claim_time = now;
	saveState();
	send(res, 200, { prize, coins: a.coin });
});

route('POST /shop/unlock_new_character_v2/', (req, res, body, a) => {
	const tier = body.tier || 'Common';
	const price = TIER_PRICE[tier] || 1000;
	if (a.coin < price) { send(res, 400, {}); return; }
	const pool = CHARS.filter((c) => c.tier === tier);
	const c = pool[Math.floor(Math.random() * pool.length)] || CHARS[0];
	a.coin -= price;
	a.characters.push(Object.assign({}, c));
	saveState();
	send(res, 200, { coin: a.coin, character: Object.assign({}, c) });
});

route('POST /shop/unlock_exact_character/', (req, res, body, a) => {
	const c = getChar(Number(body.character_id));
	if (!c) { send(res, 400, {}); return; }
	if (a.characters.some((x) => x.id === c.id)) { send(res, 401, {}); return; }
	const price = TIER_PRICE[c.tier] || 1000;
	if (a.coin < price) { send(res, 400, {}); return; }
	a.coin -= price;
	a.characters.push(Object.assign({}, c));
	saveState();
	send(res, 200, { coin: a.coin, character: Object.assign({}, c) });
});

route('POST /shop/unlock_animation/', (req, res, body, a) => {
	send(res, 200, { character_id: body.character_id, coin: a.coin, unlocks: [] });
});

route('POST /game/purchase_with_coin/', (req, res, body, a) => {
	const price = Number(body.price) || 0;
	if (a.coin < price) { send(res, 400, { coin: a.coin }); return; }
	a.coin -= price;
	saveState();
	send(res, 200, { coin: a.coin });
});
route('POST /game/add_coin/', (req, res, body, a) => {
	a.coin += Number(body.value) || 0;
	saveState();
	send(res, 200, { coin: a.coin });
});
route('POST /game/job_done/', (req, res) => send(res, 200, {}));
route('POST /game/redeem/', (req, res) => send(res, 400, {}));
route('POST /game/contact_us/', (req, res) => send(res, 200, {}));

route('POST /game/register/', (req, res, body) => {
	const mode = body.mode || 'Race';
	const ip = body.ip || '127.0.0.1';
	const port = Number(body.port) || 9000;
	const list = (mode === 'FreeRide') ? state.servers.freeride : state.servers.race;
	const existing = list.find((x) => x.ip === ip && x.port === port);
	if (existing) { send(res, 200, { id: existing.id, is_test: false, total_stage: existing.total_stage }); return; }
	const id = ++state.serverCounter;
	const entry = {
		id, mode, ip, port,
		players_joined: 0, state: 'Lobby', map_id: 0, bot_count: 0,
		max_players_start: 32, total_stage: 3, has_password: false, password: '',
		name: (mode === 'FreeRide' ? 'FreeRide ' : 'Race ') + 'Server ' + id,
	};
	list.push(entry);
	saveState();
	log('game-server registered id=' + id + ' mode=' + mode + ' ' + ip + ':' + port);
	send(res, 200, { id, is_test: false, total_stage: entry.total_stage });
});
route('POST /game/update/', (req, res, body) => {
	const all = state.servers.race.concat(state.servers.freeride);
	const s = all.find((x) => x.id === Number(body.id));
	if (s) {
		s.players_joined = Number(body.players_joined) || 0;
		s.state = body.state || s.state;
		s.map_id = body.map_id || 0;
		s.bot_count = Number(body.bot_count) || 0;
		saveState();
	}
	send(res, 200, {});
});
route('POST /game/start_game/', (req, res, body) => {
	const count = Number(body.player_count) || 1;
	send(res, 200, { game_id: Math.floor(Math.random() * 1e9), container_id: 1, qualified_count: Math.max(1, Math.floor(count / 2)) });
});
route('POST /game/finish_game/', (req, res) => send(res, 200, {}));

route('POST /game/find_game_v2/', (req, res) => {
	const alive = state.servers.race.filter((s) => s.players_joined < s.max_players_start);
	if (alive.length === 0) { send(res, 400, {}); return; }
	const best = alive[0];
	send(res, 200, {
		best_server: { ip: best.ip, port: best.port, total_stage: best.total_stage },
		all_servers: alive.slice(1).map((s) => ({ ip: s.ip, port: s.port, total_stage: s.total_stage })),
	});
});
route('POST /game/select_map/', (req, res) => {
	send(res, 200, {
		map: {
			id: 1, path: 'res://Scenes/maps/CannonLevel.tscn',
			max_players_count: 32, min_players_count: 1,
			bot_count: 10, bot_wait_remove: 100, bot_reset_time: 30,
		},
		settings: { game_time: 120, lobby_time: 60, countdown_time: 10, result_time: 10, player_join_add_time: 5 },
	});
});
route('POST /game/results_v2/', (req, res, body, a) => {
	send(res, 200, { my_result: { coin: 50, cup: 10, crown: 0 }, winner: null });
});

route('POST /game/list_freeride_servers/', (req, res) => {
	send(res, 200, { servers: state.servers.freeride });
});
route('POST /game/get_freeride_server_owner/', (req, res) => send(res, 200, { owner: null, owner_handle: '' }));
route('POST /game/change_server_password/', (req, res) => send(res, 200, {}));

function rankRows(sortKey) {
	const list = Object.values(state.accounts).map((a) => ({
		id: a.username, handle: a.handle, name: a.handle, cup: a.cup, coin: a.coin, crown: a.crown,
		win_count: a.win_count, value: a[sortKey], count: a[sortKey],
		character: CHARS[0].path, path: CHARS[0].path, card_path: CHARS[0].card_path,
	}));
	list.sort((x, y) => y[sortKey] - x[sortKey]);
	return list.slice(0, 50);
}
route('POST /game/leaderboard_v2/', (req, res) => send(res, 200, { ranks: rankRows('cup'), wins: rankRows('win_count') }));
route('POST /game/coin_leaderboard/', (req, res) => send(res, 200, { ranks: rankRows('coin') }));
route('POST /game/char_leaderboard/', (req, res) => send(res, 200, { ranks: rankRows('cup') }));
route('POST /game/list_transactions/', (req, res) => send(res, 200, { transactions: [] }));
route('POST /game/fetch_member_by_username/', (req, res) => send(res, 200, { member: null }));
route('POST /game/transfer_money/', (req, res, body, a) => {
	const amount = Number(body.amount || body.coin || 0);
	if (a.coin < amount) { send(res, 400, { coin: a.coin }); return; }
	a.coin -= amount;
	saveState();
	send(res, 200, { coin: a.coin });
});
route('POST /game/hire_me/', (req, res, body, a) => {
	send(res, 200, { coin: a.coin, ok: true });
});
route('POST /game/my_job_stats/', (req, res, body, a) => {
	send(res, 200, { stats: (a.data && a.data.job_stats) || {}, jobs: [] });
});
route('POST /account/claim_progress_prize/', (req, res, body, a) => {
	send(res, 200, { coin: a.coin, character: null });
});
route('POST /account/ami_content_creator/', (req, res) => send(res, 200, { is_creator: false }));
route('POST /account/content_creator_stats/', (req, res) => send(res, 200, { stats: {}, refers: [] }));
route('POST /account/coin_creator_cashout/', (req, res) => send(res, 400, {}));
route('POST /account/refer_content_creator/', (req, res) => send(res, 200, {}));

route('POST /police/police_arrest/', (req, res) => send(res, 200, {}));
route('POST /police/i_kill/', (req, res) => send(res, 200, {}));
route('POST /police/arrest_list/', (req, res) => send(res, 200, { arrests: [] }));
route('POST /police/jail_stat/', (req, res) => send(res, 200, { stats: {}, players: [] }));
route('POST /police/jail_reduce/', (req, res) => send(res, 200, {}));
route('POST /police/jail_exit/', (req, res) => send(res, 200, {}));
route('POST /police/police_call/', (req, res) => send(res, 200, { calls: [] }));
route('POST /police/police_call_list/', (req, res) => send(res, 200, { calls: [] }));
route('POST /police/police_law/', (req, res) => send(res, 200, { law: '' }));
route('POST /police/police_report/', (req, res) => send(res, 200, {}));
route('POST /police/job_q_stats/', (req, res) => send(res, 200, { players: [] }));
route('POST /police/add_me_to_job_q/', (req, res) => send(res, 200, {}));
route('POST /police/add_score_to_job_q/', (req, res) => send(res, 200, {}));

route('POST /mobile/list_clans/', (req, res) => send(res, 200, { clans: state.clans }));
route('POST /mobile/search_clan/', (req, res) => send(res, 200, { clans: [] }));
route('POST /mobile/my_clan/', (req, res, body, a) => {
	const c = a.clan_id ? state.clans.find((x) => x.id === a.clan_id) : null;
	if (!c) { send(res, 400, {}); return; }
	send(res, 200, { clan: c });
});
route('POST /mobile/clan_detail/', (req, res) => send(res, 400, {}));
route('POST /mobile/create_clan/', (req, res, body, a) => {
	const price = CLAN_LEVELS[0].price;
	if (a.coin < price) { send(res, 400, {}); return; }
	a.coin -= price;
	const clan = { id: state.clans.length + 1, name: body.name || 'Clan', level: 1, members: [a.username] };
	state.clans.push(clan);
	a.clan_id = clan.id;
	saveState();
	send(res, 200, { clan, coin: a.coin });
});
route('POST /mobile/join_clan/', (req, res) => send(res, 200, {}));
route('POST /mobile/leave_clan/', (req, res, body, a) => { a.clan_id = null; saveState(); send(res, 200, {}); });
route('POST /mobile/update_clan/', (req, res) => send(res, 200, {}));
route('POST /mobile/update_clan_membership/', (req, res) => send(res, 200, {}));
route('POST /mobile/upgrade_clan/', (req, res) => send(res, 400, {}));
route('POST /mobile/upgrade_clan_with_bank/', (req, res) => send(res, 400, {}));
route('POST /mobile/deposit_clan_bank/', (req, res, body, a) => {
	const amount = Number(body.amount || 0);
	if (a.coin < amount) { send(res, 400, {}); return; }
	a.coin -= amount;
	saveState();
	send(res, 200, { coin: a.coin, bank: amount });
});
route('POST /mobile/clan_bank_leaderboard/', (req, res) => send(res, 200, { ranks: [] }));
route('POST /mobile/clan_leaderboard/', (req, res) => send(res, 200, { clans: [] }));
route('POST /mobile/list_clan_members/', (req, res) => send(res, 200, { members: [] }));
route('POST /mobile/list_clan_transactions/', (req, res) => send(res, 200, { transactions: [] }));
route('POST /mobile/list_friends/', (req, res) => send(res, 200, { friends: [] }));
route('POST /mobile/change_friendship/', (req, res) => send(res, 200, {}));
route('POST /mobile/invite_friend/', (req, res) => send(res, 200, {}));
route('POST /mobile/list_invites/', (req, res) => send(res, 200, { invites: [] }));
route('POST /mobile/purchase_mobile/', (req, res, body, a) => send(res, 200, { coin: a.coin }));

route('POST /game/ban_user/', (req, res) => send(res, 200, {}));
route('POST /game/report_message/', (req, res) => send(res, 200, {}));
route('POST /game/free_admin_ban/', (req, res) => send(res, 200, {}));
route('POST /game/free_admin_unban/', (req, res) => send(res, 200, {}));
route('POST /game/free_admin_set_title/', (req, res) => send(res, 200, {}));
route('POST /voice/access_token/', (req, res) => send(res, 403, {}));
route('POST /voice/end_room/', (req, res) => send(res, 200, {}));
route('POST /voice/kick_participant/', (req, res) => send(res, 200, {}));

loadState();
const server = http.createServer(async (req, res) => {
	let body = {};
	try { body = await readBody(req); } catch (e) {}
	const key = req.method + ' ' + req.url;
	const r = routes.find((x) => x.match === key);
	if (!r) {
		log('?? UNHANDLED ' + key);
		send(res, 200, {});
		return;
	}
	let a = null;
	try { a = auth(req); } catch (e) {}
	try {
		await r.handler(req, res, body, a);
	} catch (e) {
		log('ERROR ' + key + ': ' + (e && e.message));
		try { send(res, 200, {}); } catch (e2) {}
	}
});

server.listen(PORT, '127.0.0.1', () => {
	log('Animal Rush local backend listening on http://127.0.0.1:' + PORT);
	fs.writeFileSync(path.join(__dirname, 'backend.pid'), String(process.pid));
});
server.on('error', (e) => {
	if (e && e.code === 'EADDRINUSE') {
		log('backend already running on 8899 - exiting this extra copy.');
		process.exit(0);
	}
	log('SERVER ERROR: ' + e.message);
	process.exit(1);
});
process.on('SIGINT', () => { saveState(); process.exit(0); });
