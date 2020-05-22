#pragma once
#include "../State/GameState.h"
#include "../Dialogue.h"
#include <Graphics/2D/SpriteBase.h>
#include <Utilities/Timer.h>

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

private:
	Dialogue* dialog;
	bool triggerIntro;
	DialogStack* dial;
	Sprite* spr, *bg;
	std::string username;
};