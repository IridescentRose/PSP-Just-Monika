#include "LivingBackground2.h"
#include <psprtc.h>
#include <pspmath.h>

pspTime* myCurrentTime;

Monika::LivingBackground::LivingBackground()
{
	myCurrentTime = new pspTime();
	sceRtcGetCurrentClockLocalTime(myCurrentTime);

	daySprite = new Sprite(TextureUtil::LoadPng("./assets/images/room/day/spaceroom.png"));
	daySprite->SetPosition(240, 136);
	nightSprite = new Sprite(TextureUtil::LoadPng("./assets/images/room/night/spaceroom-n.png"));
	nightSprite->SetPosition(240, 136);
	//DETERMINE WEATHER PATTERNS

	//DETERMINE SUNRISE / SUNSET TIME

	//Very approximate, no real good way of calculating otherwise... maximum value is 361
	calculateSunRiseSet();
}
#include <Utilities/Logger.h>
void Monika::LivingBackground::update()
{
	sceRtcGetCurrentClockLocalTime(myCurrentTime);
	if (myCurrentTime->day != day) {
		calculateSunRiseSet();
	}
	day = myCurrentTime->day;


	dayTime = myCurrentTime->hour * 3600 + myCurrentTime->minutes * 60 + myCurrentTime->seconds;
}

void Monika::LivingBackground::draw()
{
	int sunsetTime = (sunSet.hour * 3600 + sunSet.minutes * 60);
	int sunriseTime = (sunRise.hour * 3600 + sunRise.minutes * 60);



	if (dayTime >= sunriseTime + 3600 && dayTime < sunsetTime - 3600) {
		daySprite->Alpha(255);
		daySprite->Draw();
	}
	else if (dayTime >= sunsetTime - 3600 && dayTime < sunsetTime + 3600) {
		daySprite->Alpha(255);
		daySprite->Draw();

		nightSprite->Alpha(255 * ((float)(dayTime - (sunsetTime - 3600))/7200.0f));
		nightSprite->Draw();
	}
	else if (dayTime >= sunsetTime + 3600 || dayTime < sunriseTime - 3600) {
		nightSprite->Alpha(255);
		nightSprite->Draw();
	}
	else if (dayTime >= sunriseTime - 3600 && dayTime < sunriseTime + 3600) {
		nightSprite->Alpha(255);
		nightSprite->Draw();

		daySprite->Alpha(255 * ((float)(dayTime - (sunriseTime - 3600)) / 7200.0f));
		daySprite->Draw();
	}
	else {
		daySprite->Alpha(255);
		daySprite->Draw();
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
