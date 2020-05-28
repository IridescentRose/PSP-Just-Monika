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

		std::string currentEyes;
	private:
		std::map<std::string, Sprite*> sprts;
		std::map<std::string, Sprite*> eyes;
		int filter;
		std::vector<std::vector<std::string>> filters;

		Sprite* hairF, * hairB, * leanHairF, * leanHairB;
	};
}