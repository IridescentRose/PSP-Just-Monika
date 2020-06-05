#pragma once
#include <cstdint>
#include <Graphics/2D/SpriteBase.h>
#include <Audio/AudioClip.h>
#include "BodyBase.h"
using namespace Stardust::Graphics::Render2D;
using namespace Stardust::Graphics;
using namespace Stardust;

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
		Body* body;

	private:
		void calculateSunRiseSet();
		void calculateWeatherDay();


		DayTime sunRise, sunSet;
		bool newDay;

		Audio::AudioClip *rain_sound, *thunder1, *thunder2;
		int randomTick;

		bool rain;
		
		int dayTime;
		uint8_t day;

		Sprite* daySprite, * nightSprite;
		Sprite* tableSprite, * tableSpriteN;
		Sprite* layer1, *layer2;
		bool specialDay;

	};
}