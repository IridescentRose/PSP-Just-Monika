#include "Dialogue.h"
#include <Utilities/Input.h>
#include <Utilities/Logger.h>
Dialogue::Dialogue()
{
	dialog = TextureUtil::LoadPng("./assets/game/dialog.png");

	dialogueBox = new Sprite(dialog);

	main = new GameDialog("example");
	main->reset();

	main->setOptions({ 0.5f, 0xFF000000, INTRAFONT_ALIGN_LEFT });
	main->setPosition({48, 184});
	main->setSpeed(1);

	dialogueBox->SetPosition(240, 200);

	selPos = 0;
	display = false;
}

void Dialogue::reset()
{
	main->reset();
	display = false;
}

void Dialogue::setDialogue(Dialog* d)
{
	info = d;
	main->setText(d->text);
	selIndex = 0;
	selPos = 0;
	
	reset();
}

void Dialogue::show()
{
	display = true;
}

void Dialogue::hide()
{
	display = false;
}
void Dialogue::update()
{
	if (display) {
		main->animateStep();

		if (main->isDone()) {
			switch (info->interactionType) {
			case INTERACTION_TYPE_NONE: {
				if (Utilities::KeyPressed(PSP_CTRL_CROSS)) {
					hide();
				}
				break;
			}

			}

		}
	}
}

void Dialogue::draw()
{
	if (display) {
		dialogueBox->Draw();
		main->draw();
	}
}

bool Dialogue::isEngaged()
{
	return display;
}

DialogStack::DialogStack(Dialogue* d)
{
	dial = d;
}

void DialogStack::addDialog(Dialog* d)
{
	dialogs.push(d);
}

void DialogStack::clearDialog()
{
	for (int i = 0; i < dialogs.size(); i++) {
		dialogs.pop();
	}
}

void DialogStack::update()
{
	if (!dial->isEngaged()) {
		if (dialogs.size() > 0) {
			dial->setDialogue(dialogs.front());
			dial->show();
			dialogs.pop();
		}
	}
}
