#pragma once
#include "../State/GameState.h"
#include "../Dialogue.h"
#include <Graphics/2D/SpriteBase.h>
#include <Utilities/Timer.h>
#include <Audio/AudioClip.h>
#include <Utilities/Thread.h>
#include "../Monika/LivingBackground2.h"

using namespace Stardust::Graphics;

class MenuState : public GameState {
public:
	MenuState();

	void init();
	void cleanup();

	void enter();
	void pause();
	void resume();

	void update(GameStateManager* st);
	void draw(GameStateManager* st);

	static int audio_thread(unsigned int, void*);

	void awaken();
	void randomPick();

	void sendIntroDialog(int phase);

private:
	Dialogue* dialog;
	DialogStack* dial;
	int reloads;
	Monika::LivingBackground* livingBG;
	Utilities::Thread* athr;
	UI::UIText* txt;
	int dayTime;

	bool lookAtChat;

	Json::Value introSeq;
	bool triggerIntro;
	int introPhase;

	bool speaking;
	int timeTilNextMessage;
};

extern Audio::AudioClip* adc;
extern std::string username;