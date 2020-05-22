#pragma once
#include "../State/GameState.h"
#include "../Dialogue.h"
#include <Graphics/2D/SpriteBase.h>
#include <Utilities/Timer.h>
#include <Audio/AudioClip.h>
#include <Utilities/Thread.h>

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

private:
	Dialogue* dialog;
	bool triggerIntro;
	DialogStack* dial;
	int reloads;
	Sprite* spr, *bg;
	Utilities::Thread* athr;

	bool speaking;
	int timeTilNextMessage;
};

extern Audio::AudioClip* adc;
extern std::string username;