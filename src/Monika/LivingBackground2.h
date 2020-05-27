#pragma once
#include <cstdint>
#include <Graphics/2D/SpriteBase.h>
using namespace Stardust::Graphics::Render2D;
using namespace Stardust::Graphics;

namespace Monika {


	struct DayTime {
		uint8_t hour;
		uint8_t minutes;
	};

	class LivingBackground {
	public:
		LivingBackground();

		void update();
		void draw();

	private:
		void calculateSunRiseSet();

		DayTime sunRise, sunSet;
		bool newDay;

		bool rain;
		DayTime overCastTime[3];
		DayTime rainTime;
		
		int dayTime;
		uint8_t day;

		Sprite* daySprite, *nightSprite;

	};
}