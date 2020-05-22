#pragma once
#include <Graphics/2D/SpriteBase.h>
#include "GameDialog.h"
#include <Audio/AudioClip.h>

using namespace Stardust;
using namespace Stardust::Graphics;
using namespace Stardust::Graphics::Render2D;

enum InteractionType {
	INTERACTION_TYPE_NONE,
};

struct Dialog{
	std::string text;
	char interactionType;
};


class Dialogue {
public:
	Dialogue();

	void reset();
	void setDialogue(Dialog* d);

	void show();
	void hide();

	void update();
	void draw();

	bool isEngaged();

private:
	Sprite* dialogueBox;
	Texture* dialog;
	bool display;
	int selIndex;
	int selPos;
	int selFrame;
	int exitIndex;

	GameDialog* main;
	Dialog* info;
	Audio::AudioClip* sel;
};

class DialogStack {
public:

	DialogStack(Dialogue* d);

	void addDialog(Dialog* d);
	void clearDialog();

	void update();

private:
	Dialogue* dial;
	std::queue<Dialog*> dialogs;

};