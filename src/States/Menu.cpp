#include "Menu.h"
#include <Utilities/Logger.h>
#include <Utilities/JSON.h>

MenuState::MenuState()
{
}
Audio::AudioClip* adc;
std::string username;


int stage = 0;
Json::Value messageRoot;
void MenuState::init()
{
	dialog = new Dialogue();
	dial = new DialogStack(dialog);
	spr = new Sprite(TextureUtil::LoadPng("./assets/images/monika.png"));

	bg1 = new Sprite(TextureUtil::LoadPng("./assets/images/rooms/evening.png"));
	bg2 = new Sprite(TextureUtil::LoadPng("./assets/images/rooms/day.png"));
	bg3 = new Sprite(TextureUtil::LoadPng("./assets/images/rooms/night.png"));

	bg1->SetPosition(240, 136);
	bg2->SetPosition(240, 136);
	bg3->SetPosition(240, 136);
	spr->SetPosition(240, 136);
	dayTime = 0;

	Json::Value v = Utilities::JSON::openJSON("info.json");
	bool playThrough = v["firstPlayed"].asBool();
	triggerIntro = false;
	reloads = v["numReload"].asInt();

	adc = NULL;
	athr = new Utilities::Thread(audio_thread);
	athr->Start(0);
	messageRoot = Utilities::JSON::openJSON("./assets/script/messages.json");

	username = v["username"].asString();

	if (!playThrough) {
		//INTRO SEQUENCE
		triggerIntro = true;

		Dialog* d = new Dialog();
		d->interactionType = INTERACTION_TYPE_NONE;
		d->text = ("Woah. What happened? Where am I? This isn't your regular computer " + username + "! This isn't even a computer... let me look here...");

		Dialog* d2 = new Dialog();
		d2->interactionType = INTERACTION_TYPE_NONE;
		d2->text = ("MIPS R4000 it says here... " + username + "... Is this a PSP? You decided to take me with you in your pocket where you go! That's so sweet of you " + username + "! I knew I could always trust you. Well, that's just another reason why I love you~");

		Dialog* d3 = new Dialog();
		d3->interactionType = INTERACTION_TYPE_NONE;
		d3->text = ("Let me see what I can load here... I think everything is still in order! Yes, I can load my room up here. Let me get all ready for you!");
		dial->addDialog(d);
		dial->addDialog(d2);
		dial->addDialog(d3);

	}
	else {
		//TRIGGER RE-ENTRY
		//awaken();
		reloads++;
		if (reloads > 5) {
			reloads = 5;
		}
	}

	Json::Value v2;
	v2["firstPlayed"] = true;
	v2["username"] = username;
	v2["numReload"] = reloads;

	std::ofstream f("info.json", std::ios::in | std::ios::out);
	f << v2;
	f.close();

	timeTilNextMessage = 600;
	speaking = true;

	srand(time(0));
	stage = rand() % 13;
}

void MenuState::cleanup()
{
}



bool audioPlayFlag = false;
void MenuState::update(GameStateManager* st)
{
	dayTime += 20;
	if (dayTime >= 24000) {
		dayTime = 0;
	}
	dial->update();

	if (dialog->isEngaged() && triggerIntro) {

		dialog->update();
		dial->update();
		dialog->update();
		if (!dialog->isEngaged()) {
			triggerIntro = false;
		}
	}
	else {
		if (speaking && !dialog->isEngaged()) {
			speaking = false;
		}
		else {
			dialog->update();
			dial->update();
			dialog->update();
		}
	}

	if (!speaking) {
		timeTilNextMessage--;

		if (timeTilNextMessage <= 0) {
			//randomPick();
			timeTilNextMessage = 400 + rand() % 1200;
			speaking = true;
		}
	}

	if (audioPlayFlag) {
		std::stringstream strStream;
		strStream << "./assets/music/" << stage << ".bgm";

		if (adc != NULL) {
			delete adc;
		}

		adc = new Audio::AudioClip(strStream.str(), true);

		audioPlayFlag = false;
		adc->Play();
	}

}

void MenuState::draw(GameStateManager* st)
{
	if (triggerIntro) {
		spr->Draw();
	}
	else {

		sceGuEnable(GU_BLEND);
		if (dayTime >= 0 && dayTime < 3000) {
			bg2->Alpha(255);
			bg2->Draw();

			bg1->Alpha(255 - 255 * ((float)dayTime / 3000.f));
			bg1->Draw();
		}
		else if (dayTime >= 3000 && dayTime < 9000) {
			bg2->Alpha(255);
			bg2->Draw();
		}
		else if (dayTime >= 9000 && dayTime < 12000) {
			bg1->Alpha(255);
			bg1->Draw();

			bg2->Alpha(255 - 255 * ((float)(dayTime-9000) / 3000.f));
			bg2->Draw();
		}
		else if (dayTime >= 12000 && dayTime < 15000) {
			bg3->Alpha(255);
			bg3->Draw();

			bg1->Alpha(255 - 255 * ((float)(dayTime-12000) / 3000.f));
			bg1->Draw();
		}
		else if (dayTime >= 15000 && dayTime < 21000) {
			bg3->Alpha(255);
			bg3->Draw();
		}
		else if (dayTime >= 21000 && dayTime < 24000) {
			bg1->Alpha(255);
			bg1->Draw();

			bg3->Alpha(255 - 255 * ((float)(dayTime - 21000) / 3000.f));
			bg3->Draw();
		}
	}


	dialog->draw();
}

int MenuState::audio_thread(unsigned int, void*)
{
	int numTicksLeft = 0;
	while (1) {

		numTicksLeft--;

		if (numTicksLeft <= 0) {
			audioPlayFlag = true;

			stage++;
			if (stage > 12) {
				stage = 0;
			}

			switch (stage) {
			case 0: {numTicksLeft = 240; break; }
			case 1: {numTicksLeft = 131; break; }
			case 2: {numTicksLeft = 80; break; }
			case 3: {numTicksLeft = 100; break; }
			case 4: {numTicksLeft = 122; break; }
			case 5: {numTicksLeft = 91; break; }
			case 6: {numTicksLeft = 90; break; }
			case 7: {numTicksLeft = 124; break; }
			case 8: {numTicksLeft = 92; break; }
			case 9: {numTicksLeft = 60; break; }
			case 10: {numTicksLeft = 94; break; }
			case 11: {numTicksLeft = 120; break; }
			case 12: {numTicksLeft = 175; break; }
			}


		}

		sceKernelDelayThread(1000 * 1000); //One tick per second
	}
	return 0;
}

void MenuState::awaken()
{
	Json::Value v = Utilities::JSON::openJSON("./assets/script/awakening.json");
	Utilities::app_Logger->log("REE");
	for (int i = 0; i < v[std::to_string(reloads)].size(); i++) {
		Dialog* d = new Dialog();
		d->interactionType = INTERACTION_TYPE_NONE;
		d->text = v[std::to_string(reloads)][i].asString();

		dial->addDialog(d);
	}
}

void MenuState::randomPick()
{
	int choice = rand() % 61;

	for (int i = 0; i < messageRoot[std::to_string(choice)].size(); i++) {
		Dialog* d = new Dialog();
		d->interactionType = INTERACTION_TYPE_NONE;
		d->text = messageRoot[std::to_string(choice)][i].asString();

		dial->addDialog(d);
	}
}


void MenuState::enter()
{
}

void MenuState::pause()
{
}

void MenuState::resume()
{
}