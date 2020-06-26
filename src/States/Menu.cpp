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
	dayTime = 0;

	Json::Value v = Utilities::JSON::openJSON("info.json");
	bool playThrough = v["firstPlayed"].asBool();
	triggerIntro = false;
	reloads = v["numReload"].asInt();

	int mainChoice = 0;

	adc = NULL;
	athr = new Utilities::Thread(audio_thread);
	athr->Start(0);
	messageRoot = Utilities::JSON::openJSON("./assets/script/facts.json");
	username = v["username"].asString();

	livingBG = new Monika::LivingBackground();
	livingBG->body->setExprFilter("1esa");
	if (!playThrough) {
		//INTRO SEQUENCE
		triggerIntro = true;
		introPhase = 0;
		introSeq = Utilities::JSON::openJSON("./assets/script/introduction.json")["intro"];

		sendIntroDialog(introPhase);
	}
	else {
		//TRIGGER RE-ENTRY
		awaken();
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

	timeTilNextMessage = 300;
	speaking = true;

	srand(time(0));
	stage = rand() % 13;
	PFL_Init(false);
	PFL_BeginCPURecord();

	txt = new UI::UIText({12, 12}, "example");
	lookAtChat = true;
}

void MenuState::cleanup()
{
}

#include <Utilities/Input.h>

bool audioPlayFlag = false;
void MenuState::update(GameStateManager* st)
{
	if (Utilities::KeyPressed(PSP_CTRL_CIRCLE)) {
		lookAtChat = !lookAtChat;
	}

	livingBG->update();

	if(lookAtChat)
		dial->update();

	if (dialog->isEngaged() && triggerIntro && lookAtChat) {

		dialog->update();

		if (!dialog->isEngaged()) {
			if (introPhase < 70) {
				introPhase++;
				sendIntroDialog(introPhase);
				dial->update();
				dialog->update();
			}
			else {
				triggerIntro = false;
			}
		}
	}
	else {
		if (dialog->isEngaged() && lookAtChat) {
			dialog->update();

			if (!dialog->isEngaged()) {
				if (introPhase < mainSize) {
					sendMainDialog();
					dial->update();
					dialog->update();
				}
			}
		}

		if (speaking && !dialog->isEngaged()) {
			speaking = false;
			lookAtChat = true;
		}
		else {

			if (lookAtChat){
				dialog->update();
				dial->update();
				dialog->update();
			}
		}
	}

	if (!speaking) {

		livingBG->body->setExprFilter("1esa");

		timeTilNextMessage--;

		if (timeTilNextMessage <= 0) {
			randomPick();
			timeTilNextMessage = 300 + rand() % 900;
			speaking = true;
		}
	}

	if (Utilities::KeyPressed(PSP_CTRL_SQUARE)) {
		stage++;
		stage = stage % 13;
		if (adc != NULL) {
			adc->Stop();
		}
		audioPlayFlag = true;
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

	sceGuEnable(GU_BLEND);
	livingBG->draw();

	if (lookAtChat)
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
	mainChoice = rand() % messageRoot["facts"].size();
	introPhase = 0;
	mainSize = messageRoot["facts"][mainChoice].size();
	sendMainDialog();
}

void MenuState::sendIntroDialog(int phase)
{
	livingBG->body->setExprFilter(introSeq[phase]["pose"].asString());

	Dialog* d = new Dialog();
	d->interactionType = INTERACTION_TYPE_NONE;
	d->text = introSeq[phase]["msg"].asString();
	dial->addDialog(d);
}

void MenuState::sendMainDialog()
{
	livingBG->body->setExprFilter(messageRoot["facts"][mainChoice][introPhase++].asString());
	Dialog* d = new Dialog();
	d->interactionType = INTERACTION_TYPE_NONE;
	d->text = messageRoot["facts"][mainChoice][introPhase++].asString();
	dial->addDialog(d);
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