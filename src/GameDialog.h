#pragma once
#include <Graphics/UI/UIText.h>
#include <Graphics/2D/SpriteAdvanced.h>

using namespace Stardust::Graphics;

class GameDialog {
public:
	GameDialog(std::string text);
	~GameDialog();

	void setPosition(glm::vec2 position);
	void setSpeed(int s);

	void setText(std::string);
	void reset();

	bool isDone() {
		return index == txt.size();
	}

	void animateStep();
	void draw();

	void setOptions(UI::FontStyle fs);

private:

	UI::UIText* ui;
	
	std::string txt;
	int index;
	int speed;

};