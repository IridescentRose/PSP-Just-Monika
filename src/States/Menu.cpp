#include "Menu.h"
#include <Utilities/Logger.h>
#include <Utilities/JSON.h>

MenuState::MenuState()
{
}

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


void MenuState::enter()
{
}

void MenuState::pause()
{
}

void MenuState::resume()
{
}