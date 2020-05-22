#include "Application.h"
#include "States/Intro.h"

Application::Application()
{

}

Application::~Application()
{
}

void Application::run()
{
	//We'll initialize stuff here.
	gsm = new GameStateManager();

	//Set Up Some Sort of chain loading
	IntroState* st = new IntroState();
	st->init();
	gsm->changeState(st);
}

void Application::update()
{
	gsm->update();
}

void Application::draw()
{
	gsm->draw();
}
