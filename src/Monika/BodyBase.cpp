#include "BodyBase.h"
#include <Utilities/JSON.h>
#include <Utilities/Logger.h>
#include <Utilities/Input.h>

Monika::Body::Body()
{
	filter = 0;
	Utilities::app_Logger->log("A");
	Json::Value v = Utilities::JSON::openJSON("body.json")["data"];

	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();

		Sprite* spr = new Sprite(TextureUtil::LoadPng(v[i]["file"].asString()));
		spr->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr->setLayer(v[i]["position"]["z"].asInt());
		spr->Scale(0.9f, 0.9f);
		sprts.emplace(str, spr);
	}
	v = Utilities::JSON::openJSON("poses.json")["data"];

	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();

		std::vector<std::string> strs;

		for (int x = 0; x < v[i]["required"].size(); x++) {
			strs.push_back(v[i]["required"][x].asString());
		}

		filters.push_back(strs);
	}
}

void Monika::Body::draw()
{
	sceGuEnable(GU_ALPHA_TEST);
	for (auto [str, s] : sprts) {
		for (auto strs : filters[filter]) {
			if (str == strs) {
				s->Draw();
			}
		}
	}
}

void Monika::Body::update()
{
	if (Utilities::KeyPressed(PSP_CTRL_LEFT)) {
		filter--;
		if (filter < 0) {
			filter = 0;
		}
	}
	if (Utilities::KeyPressed(PSP_CTRL_RIGHT)) {
		filter++;
		if (filter > filters.size() - 1) {
			filter = filters.size() - 1;
		}
	}
}
