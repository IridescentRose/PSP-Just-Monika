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
		std::string currentEyebrows;
		std::string currentMouth;
		std::string currentBlush;
		std::string currentTears;

	private:
		std::map<std::string, Sprite*> sprts;
		std::map<std::string, Sprite*> sprtsc;
		std::map<std::string, Sprite*> eyes;
		std::map<std::string, Sprite*> eyebrows;
		std::map<std::string, Sprite*> mouths;
		std::map<std::string, Sprite*> blushes;
		std::map<std::string, Sprite*> tears;


		int filter;
		std::vector<std::vector<std::string>> filters;

		Sprite* hairF, * hairB, * leanHairF, * leanHairB;
	};
}