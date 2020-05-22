#include "Intro.h"
#include <Utilities/Logger.h>


IntroState::IntroState()
{
}

void IntroState::init()
{
	dialog = new GameDialog("Made by");
	dialog->setOptions({ 1.0f, 0xFF000000, INTRAFONT_ALIGN_CENTER });
	dialog->setSpeed(8);
	dialog->setPosition({ 240, 136 });
	dialog->reset();

	timer = new Stardust::Utilities::Timer();
	timer->reset();

	tex = TextureUtil::LoadPng("assets/images/splash.png");
	logo = new Render2D::Sprite(tex);
	logo->SetPosition(240, 136);
	sceGuEnable(GU_BLEND);

	g_RenderCore.SetClearColor(255, 255, 255, 255);
	stage = 0;

}

void IntroState::cleanup()
{
	delete dialog;
	delete tex;
	delete logo;
}



void IntroState::update(GameStateManager* st)
{
}

void IntroState::draw(GameStateManager* st)
{
	timer->deltaTime();

	
	if (timer->elapsed() > 2.0f && timer->elapsed() < 4.0f) {
		logo->Draw();

		dialog->setText("Ported by Iridescence");
		dialog->reset();
	}else {
		dialog->animateStep();
		dialog->draw();

		if (timer->elapsed() > 8.0f) {
			//CHANGE STATE
			MenuState* m = new MenuState();
			m->init();

			st->changeState(m);
		}
	}

}


void IntroState::enter()
{
}

void IntroState::pause()
{
}

void IntroState::resume()
{
}