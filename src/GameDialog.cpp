#include "GameDialog.h"

GameDialog::GameDialog(std::string text)
{
	ui = new UI::UIText({ 0, 0 }, "");
	setText(text);
}

GameDialog::~GameDialog()
{
	delete ui;
}

void GameDialog::setPosition(glm::vec2 position)
{
	ui->setPosition(position);
}

void GameDialog::setSpeed(int s)
{
	speed = s;
}

void GameDialog::setText(std::string t)
{
	ui->setContent(t);
	txt = t;
	index = t.length();
}

void GameDialog::reset()
{
	index = 0;
}

int count = 0;

void GameDialog::animateStep()
{
	count++;
	if (count % speed == 0) {
		index++;
	}

	if (index > txt.size()) {
		index = txt.size();
	}
}

void GameDialog::draw()
{
	ui->setContent(txt.substr(0, index));
	ui->draw();
}

void GameDialog::setOptions(UI::FontStyle fs)
{
	ui->setOptions(fs);
}
