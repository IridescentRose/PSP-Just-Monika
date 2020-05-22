#include "Dialogue.h"
#include <Utilities/Input.h>
#include <Utilities/Logger.h>
Dialogue::Dialogue()
{
	dialog = TextureUtil::LoadPng("./assets/images/textbox.png");

	dialogueBox = new Sprite(dialog);

	main = new GameDialog("example");
	main->reset();

	g_RenderCore.SetClearColor(0, 0, 0, 255);

	main->setOptions({ 1.15f, 0xFFFFFFFF, INTRAFONT_ALIGN_LEFT });
	main->setPosition({26, 208});
	main->setSpeed(4);

	dialogueBox->SetPosition(240, 216);
	dialogueBox->Scale(1.15f, 1.15f);

	selPos = 0;
	display = false;
	sel = new Audio::AudioClip("./assets/music/sel.wav");
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
					sel->Play(5);
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

		sceGuEnable(GU_BLEND);
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

#include "States/Menu.h"
std::string textWrap(std::string str, int location) {
	// your other code
	int n = str.rfind(' ', location);
	if (n != std::string::npos) {
		str.at(n) = '\n';
	}
	// your other code
	return str;
}

void DialogStack::addDialog(Dialog* d)
{
	size_t start_pos = d->text.find("[player]");
	if (start_pos != std::string::npos) {
		d->text.replace(start_pos, std::string("[player]").length(), username);
	}
	
	//Wrap text function
	int minWraps = d->text.size() / 52;

	for (int i = 0; i < minWraps; i++) {
		d->text = textWrap(d->text, 52 * (i+1));
	}


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
