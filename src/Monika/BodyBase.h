#pragma once
#include <Graphics/2D/SpriteBase.h>
#include <Utilities/JSON.h>
#include <map>

using namespace Stardust;
using namespace Stardust::Graphics;
using namespace Stardust::Graphics::Render2D;

namespace Monika {
	struct Filter {
		std::string eyes, eyebrows, mouths, blushes, tears;
		int filter;
		bool lean;
	};

	class Body {
	public:

		Body();

		void draw();
		void update();

		void setExprFilter(std::string);

		void initFilters();

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

		bool ignoreRibbon;

		int filter;
		std::vector<std::vector<std::string>> filters;
		
		std::map<std::string, Filter> exprFilters;

		Sprite* hairF, * hairB, * leanHairF, * leanHairB;
		Sprite* ribbon, *ribbonL;
	};
}