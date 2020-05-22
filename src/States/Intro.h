#pragma once
#include "../State/GameState.h"
#include "../GameDialog.h"
#include <Graphics/2D/SpriteBase.h>
#include <Utilities/Timer.h>

using namespace Stardust::Graphics;

class IntroState : public GameState {
public:
	IntroState();

	void init();
	void cleanup();

	void enter();
	void pause();
	void resume();

	void update(GameStateManager* st);
	void draw(GameStateManager* st);

private:
	Stardust::Utilities::Timer* timer;
	GameDialog* dialog;
	Render2D::Sprite* logo;
	Texture* tex;
	int stage;
};