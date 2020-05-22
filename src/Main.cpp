#include <Platform/Platform.h>
#include <Graphics/RendererCore.h>
#include <Utilities/Logger.h>

PSP_MODULE_INFO("Just Monika", 0, 1, 0);
PSP_MAIN_THREAD_ATTR(THREAD_ATTR_VFPU | THREAD_ATTR_USER);
PSP_HEAP_SIZE_KB(-1024);

using namespace Stardust;
using namespace Stardust::Utilities;
using namespace Stardust::Graphics;

int main() {
	Platform::initPlatform("DDLC_DEMO");

	while (true) {
		Platform::platformUpdate();
	}

	Platform::exitPlatform();
	return 0;
}