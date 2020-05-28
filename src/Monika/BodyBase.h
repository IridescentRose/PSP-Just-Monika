#pragma once
#include <Graphics/2D/SpriteBase.h>
#include <map>

using namespace Stardust;
using namespace Stardust::Graphics;
using namespace Stardust::Graphics::Render2D;

namespace Monika {
	class Body {
	public:

		Body();

		void draw();
		void update();

	private:
		std::map<std::string, Sprite*> sprts;
	};
}