#include "BodyBase.h"
#include <Utilities/JSON.h>
#include <Utilities/Logger.h>

Monika::Body::Body()
{
	Utilities::app_Logger->log("A");
	Json::Value v = Utilities::JSON::openJSON("body.json")["data"];

	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();

		Sprite* spr = new Sprite(TextureUtil::LoadPng(v[i]["file"].asString()));
		spr->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());

		sprts.emplace(str, spr);
	}
}

void Monika::Body::draw()
{
	for (auto [str, s] : sprts) {
		s->Draw();
	}
}

void Monika::Body::update()
{
}
