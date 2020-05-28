#include "LivingBackground2.h"
#include <psprtc.h>
#include <pspmath.h>
#include <iostream>
#include <Utilities/Logger.h>

pspTime* myCurrentTime;

Monika::LivingBackground::LivingBackground()
{
	myCurrentTime = new pspTime();
	randomTick = 0;
	sceRtcGetCurrentClockLocalTime(myCurrentTime);

	daySprite = NULL;
	nightSprite = NULL;
	rain_sound = new Audio::AudioClip("./assets/music/storm/rain_2.wav", false);
	rain_sound->SetLoop(true);
	thunder1 = new Audio::AudioClip("./assets/music/storm/thunder.wav", false);
	thunder2 = new Audio::AudioClip("./assets/music/storm/thunder_1.wav", false);

	//DETERMINE WEATHER PATTERNS
	calculateWeatherDay();

	//DETERMINE SUNRISE / SUNSET TIME
	calculateSunRiseSet();

	body = new Body();
}
void Monika::LivingBackground::update()
{
	body->update();
	sceRtcGetCurrentClockLocalTime(myCurrentTime);
	if (myCurrentTime->day != day) {
		calculateSunRiseSet();
	}
	day = myCurrentTime->day;


	dayTime = myCurrentTime->hour * 3600 + myCurrentTime->minutes * 60 + myCurrentTime->seconds;

	if (rain) {
		randomTick--;
		if (randomTick <= 0) {
			srand(time(0));
			rand() % 2 == 0 ? thunder1->Play(1) : thunder2->Play(1);

			randomTick = (rand() * 41) % 6000 + 600;
		}
	}
}

void Monika::LivingBackground::draw()
{
	int sunsetTime = (sunSet.hour * 3600 + sunSet.minutes * 60);
	int sunriseTime = (sunRise.hour * 3600 + sunRise.minutes * 60);

	Utilities::app_Logger->log(std::to_string(dayTime));
	Utilities::app_Logger->log(std::to_string(sunsetTime));
	Utilities::app_Logger->log(std::to_string(sunriseTime));

	if (dayTime >= sunriseTime + 3600 && dayTime < sunsetTime - 3600) {
		daySprite->Alpha(255);
		daySprite->Draw();

		body->draw();
		
		tableSprite->Alpha(255);
		tableSprite->Draw();
	}
	else if (dayTime >= sunsetTime - 3600 && dayTime < sunsetTime + 3600) {
		daySprite->Alpha(255);
		daySprite->Draw();

		nightSprite->Alpha(255 * ((float)(dayTime - (sunsetTime - 3600))/7200.0f));
		nightSprite->Draw();

		body->draw();
		
		tableSprite->Alpha(255);
		tableSprite->Draw();

		tableSpriteN->Alpha(255 * ((float)(dayTime - (sunsetTime - 3600)) / 7200.0f));
		tableSpriteN->Draw();
	}
	else if (dayTime >= sunsetTime + 3600 || dayTime < sunriseTime - 3600) {
		nightSprite->Alpha(255);
		nightSprite->Draw();

		body->draw();
		
		tableSpriteN->Alpha(255);
		tableSpriteN->Draw();
	}
	else if (dayTime >= sunriseTime - 3600 && dayTime < sunriseTime + 3600) {
		nightSprite->Alpha(255);
		nightSprite->Draw();

		daySprite->Alpha(255 * ((float)(dayTime - (sunriseTime - 3600)) / 7200.0f));
		daySprite->Draw();

		body->draw();
	
		tableSpriteN->Alpha(255);
		tableSpriteN->Draw();

		tableSprite->Alpha(255 * ((float)(dayTime - (sunriseTime - 3600)) / 7200.0f));
		tableSprite->Draw();
	}
	else {
		daySprite->Alpha(255);
		daySprite->Draw();

		body->draw();
		
		tableSprite->Alpha(255);
		tableSprite->Draw();
	}

}

void Monika::LivingBackground::calculateSunRiseSet()
{
	int dayApproximationYear = myCurrentTime->month * 30 + myCurrentTime->day;

	float approximateInterval = vfpu_cosf(((float)dayApproximationYear / 180.5f * 2 * 3.14159f)) * 1.5f;

	int hourSunrise = 6.5f - approximateInterval;
	int minuteSunrise = (approximateInterval - (float)(hourSunrise)) * 60;
	sunRise = { hourSunrise, minuteSunrise };


	int hourSunset = 18.5f + approximateInterval;
	int minuteSunset = (approximateInterval - (float)(hourSunrise)) * 60;
	sunSet = { hourSunset, minuteSunset };
}

void Monika::LivingBackground::calculateWeatherDay()
{
	if (nightSprite != NULL) {
		delete nightSprite;
	}

	if (nightSprite != NULL) {
		delete nightSprite;
	}


	
	int rnd = myCurrentTime->month * 30 + myCurrentTime->day + myCurrentTime->year * 367;


	if (rnd % 3 == 0) {
		//Overcast 33% chance rain
		if (rnd % 2 == 0) {
			//Rain
			if (myCurrentTime->month < 3 || myCurrentTime->month >= 11) {
				daySprite = new Sprite(TextureUtil::LoadPng("./assets/images/room/day/spaceroom_snow.png"));
				nightSprite = new Sprite(TextureUtil::LoadPng("./assets/images/room/night/spaceroom_snow-n.png"));
				rain = false;
			}
			else {
				daySprite = new Sprite(TextureUtil::LoadPng("./assets/images/room/day/spaceroom_rain.png"));
				nightSprite = new Sprite(TextureUtil::LoadPng("./assets/images/room/night/spaceroom_rain-n.png"));
				rain = true;

				rain_sound->Play(4);
				thunder1->Play(1);
			}
		}
		else {
			daySprite = new Sprite(TextureUtil::LoadPng("./assets/images/room/day/spaceroom_overcast.png"));
			nightSprite = new Sprite(TextureUtil::LoadPng("./assets/images/room/night/spaceroom_overcast-n.png"));
			rain = false;
		}
	}
	else {
		daySprite = new Sprite(TextureUtil::LoadPng("./assets/images/room/day/spaceroom.png"));
		nightSprite = new Sprite(TextureUtil::LoadPng("./assets/images/room/night/spaceroom-n.png"));
		rain = false;
	}

	tableSprite = new Sprite(TextureUtil::LoadPng("./assets/images/room/day/desk.png"));
	tableSpriteN = new Sprite(TextureUtil::LoadPng("./assets/images/room/night/desk-n.png"));

	daySprite->SetPosition(240, 136);
	nightSprite->SetPosition(240, 136);


	tableSprite->SetPosition(248, 272 - 64);
	tableSpriteN->SetPosition(248, 272 - 64);
}
