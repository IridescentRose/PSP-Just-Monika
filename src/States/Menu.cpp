#include "Menu.h"
#include <Utilities/Logger.h>
#include <Utilities/JSON.h>

MenuState::MenuState()
{
}
Audio::AudioClip* adc;

void MenuState::init()
{
	dialog = new Dialogue();
	dial = new DialogStack(dialog);
	spr = new Sprite(TextureUtil::LoadPng("./assets/images/monika.png"));
	bg = new Sprite(TextureUtil::LoadPng("./assets/images/room.png"));
	spr->SetPosition(240, 136);
	bg->SetPosition(240, 136);

	Json::Value v = Utilities::JSON::openJSON("info.json");
	bool playThrough = v["firstPlayed"].asBool();
	triggerIntro = false;

	adc = NULL;
	athr = new Utilities::Thread(audio_thread);
	athr->Start(0);


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
		Dialog* d = new Dialog();
		d->interactionType = INTERACTION_TYPE_NONE;
		d->text = "Re-entry Sequence";
		dial->addDialog(d);
	}

	Json::Value v2;
	v2["firstPlayed"] = true;

	std::ofstream f("firstplay.json");
	//f << v2;
	f.close();

}

void MenuState::cleanup()
{
}



void MenuState::update(GameStateManager* st)
{
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
		dialog->update();
	}
}

void MenuState::draw(GameStateManager* st)
{
	if (triggerIntro) {
		spr->Draw();
	}
	else {
		bg->Draw();
	}


	dialog->draw();
}

int MenuState::audio_thread(unsigned int, void*)
{
	int stage = rand() % 13;
	int numTicksLeft = 0;
	while (1) {

		numTicksLeft--;

		if (numTicksLeft <= 0) {
			std::stringstream strStream;
			strStream << "./assets/music/" << stage << ".bgm";

			if (adc != NULL) {
				adc->Stop();
				delete adc;
			}

			adc = new Audio::AudioClip(strStream.str(), true);
			adc->Play();

			switch (stage) {
			case 0: {numTicksLeft = 240; break; }
			case 1: {numTicksLeft = 131; break; }
			case 2: {numTicksLeft = 80; break; }
			case 3: {numTicksLeft = 100; break; }
			case 4: {numTicksLeft = 122; break; }
			case 5: {numTicksLeft = 91; break; }
			case 6: {numTicksLeft = 90; break; }
			case 7: {numTicksLeft = 71; break; }
			case 8: {numTicksLeft = 92; break; }
			case 9: {numTicksLeft = 60; break; }
			case 10: {numTicksLeft = 94; break; }
			case 11: {numTicksLeft = 41; break; }
			case 12: {numTicksLeft = 181; break; }
			}

			stage++;
			if (stage > 12) {
				stage = 0;
			}

		}

		sceKernelDelayThread(1000 * 1000); //One tick per second
	}
	return 0;
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