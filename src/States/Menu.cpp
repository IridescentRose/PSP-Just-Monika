#include "Menu.h"
#include <Utilities/Logger.h>


MenuState::MenuState()
{
}

void MenuState::init()
{
	dialog = new Dialogue();
	dial = new DialogStack(dialog);
	Dialog* d = new Dialog();
	d->interactionType = INTERACTION_TYPE_NONE;
	d->text = "Doki Doki Test Test!\n\nLine 2\n\nAnd of course line 3!~";
	dial->addDialog(d);
	spr = new Sprite(TextureUtil::LoadPng("./assets/images/monika.png"));
	spr->SetPosition(240, 136);
}

void MenuState::cleanup()
{
}



void MenuState::update(GameStateManager* st)
{
	dial->update();
	dialog->update();
}

void MenuState::draw(GameStateManager* st)
{
	spr->Draw();
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