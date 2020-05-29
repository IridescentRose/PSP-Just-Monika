#include "Menu.h"
#include <Utilities/Logger.h>
#include <Utilities/JSON.h>
#include <perflib.h>

MenuState::MenuState()
{
}
Audio::AudioClip* adc;
std::string username;


int stage = 0;
Json::Value messageRoot;
#include <iostream>

void MenuState::init()
{
	

	dialog = new Dialogue();
	dial = new DialogStack(dialog);
	spr = new Sprite(TextureUtil::LoadPng("./assets/images/monika.png"));


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
		awaken();
		reloads++;
		if (reloads > 5) {
			reloads = 5;
		}
		if (spr != NULL) {
			delete spr;
			spr = NULL;
		}
	}

	Json::Value v2;
	v2["firstPlayed"] = true;
	v2["username"] = username;
	v2["numReload"] = reloads;

	std::ofstream f("info.json", std::ios::in | std::ios::out);
	f << v2;
	f.close();

	timeTilNextMessage = 300;
	speaking = true;

	srand(time(0));
	stage = rand() % 13;
	livingBG = new Monika::LivingBackground();
	PFL_Init(false);
	PFL_BeginCPURecord();

	txt = new UI::UIText({12, 12}, "example");
}

void MenuState::cleanup()
{
}



bool audioPlayFlag = false;
void MenuState::update(GameStateManager* st)
{
	livingBG->update();


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
			randomPick();
			timeTilNextMessage = 300 + rand() % 900;
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
	PFL_EndCPURecord();

	float time = PFL_GetCPUTime();
	float fps = 1000.0f / time;
	int fpsI = fps;

	txt->setContent(std::to_string(fpsI));

	PFL_BeginCPURecord();


	if (triggerIntro) {
		spr->Draw();
	}
	else {
		sceGuEnable(GU_BLEND);
		livingBG->draw();


	}

	dialog->draw();
	txt->draw();
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

			numTicksLeft = 300;


		}

		sceKernelDelayThread(1000 * 1000); //One tick per second
	}
	return 0;
}

void MenuState::awaken()
{
	Json::Value v = Utilities::JSON::openJSON("./assets/script/awakening.json");
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