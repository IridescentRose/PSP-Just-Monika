#include <Platform/Platform.h>
#include <Graphics/RendererCore.h>
#include <Utilities/Logger.h>
#include "Application.h"

PSP_MODULE_INFO("Just Monika", 0, 1, 0);
PSP_MAIN_THREAD_ATTR(THREAD_ATTR_VFPU | THREAD_ATTR_USER);
PSP_HEAP_SIZE_KB(-1024);

using namespace Stardust;
using namespace Stardust::Utilities;
using namespace Stardust::Graphics;

#include <oslib/oslib.h>

int main() {
	Platform::initPlatform("DDLC_DEMO");
	oslInitAudioME(oslInitAudioME_formats::OSL_FMT_ALL);


	Application* app = new Application();
	app->run();

	Graphics::g_RenderCore.Set2DMode();

	while (app->isRunning()) {
		Graphics::g_RenderCore.BeginCommands();
		Graphics::g_RenderCore.Clear();

		app->update();
		app->draw();

		Platform::platformUpdate();
		Graphics::g_RenderCore.EndCommands();
	}

	delete app;
	Platform::exitPlatform();
	return 0;
}