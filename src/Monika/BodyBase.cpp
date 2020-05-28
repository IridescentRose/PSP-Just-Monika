#include "BodyBase.h"
#include <Utilities/JSON.h>
#include <Utilities/Logger.h>
#include <Utilities/Input.h>
#include <iostream>

Monika::Body::Body()
{
	filter = 0;
	Utilities::app_Logger->log("A");
	Json::Value v = Utilities::JSON::openJSON("./assets/body.json")["data"];

	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();

		Sprite* spr = new Sprite(TextureUtil::LoadPng(v[i]["file"].asString()));
		spr->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr->setLayer(v[i]["position"]["z"].asInt());
		spr->Scale(0.9f, 0.9f);
		sprts.emplace(str, spr);
	}
	v = Utilities::JSON::openJSON("./assets/poses.json")["data"];

	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();

		std::vector<std::string> strs;

		for (int x = 0; x < v[i]["required"].size(); x++) {
			strs.push_back(v[i]["required"][x].asString());
		}

		filters.push_back(strs);
	}

	v = Utilities::JSON::openJSON("./customize.json");
	int hairChoice = v["hair"].asInt();

	currentEyes = v["eyes"].asString();

	if(hairChoice == 0){
		hairF = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/default/default-f.png"));
		hairB = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/default/default-b.png"));
		leanHairF = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/lean/default-f.png"));
		leanHairB = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/lean/default-b.png"));
		hairF->Scale(0.9f, 0.9f);
		hairB->Scale(0.9f, 0.9f);
		leanHairF->Scale(0.9f, 0.9f);
		leanHairB->Scale(0.9f, 0.9f);
		hairF->SetPosition(240, 96);
		hairF->setLayer(1);
		hairB->SetPosition(280, 128);
		hairB->setLayer(0);
		leanHairF->SetPosition(240, 124);
		leanHairF->setLayer(1);
		leanHairB->SetPosition(264, 164);
		leanHairB->setLayer(0);
	}else if(hairChoice == 1){
		hairF = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/default/down-f.png"));
		hairB = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/default/down-b.png"));
		leanHairF = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/lean/down-f.png"));
		leanHairB = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/lean/down-b.png"));
		hairF->Scale(0.9f, 0.9f);
		hairB->Scale(0.9f, 0.9f);
		leanHairF->Scale(0.9f, 0.9f);
		leanHairB->Scale(0.9f, 0.9f);
		hairF->SetPosition(240, 96);
		hairF->setLayer(1);
		hairB->SetPosition(240, 124);
		hairB->setLayer(0);
		leanHairF->SetPosition(240, 124);
		leanHairF->setLayer(1);
		leanHairB->SetPosition(244, 154);
		leanHairB->setLayer(0);
	}else{
		hairF = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/default/strand-f.png"));
		hairB = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/default/strand-b.png"));
		leanHairF = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/lean/strand-f.png"));
		leanHairB = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/lean/strand-b.png"));
		hairF->Scale(0.9f, 0.9f);
		hairB->Scale(0.9f, 0.9f);
		leanHairF->Scale(0.9f, 0.9f);
		leanHairB->Scale(0.9f, 0.9f);
		hairF->SetPosition(240, 96);
		hairF->setLayer(1);
		hairB->SetPosition(240, 124);
		hairB->setLayer(0);
		leanHairF->SetPosition(240, 124);
		leanHairF->setLayer(1);
		leanHairB->SetPosition(248, 150);
		leanHairB->setLayer(0);
	}


	v = Utilities::JSON::openJSON("./assets/face.json")["eyes"];
	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();

		Sprite* spr = new Sprite(TextureUtil::LoadPng(v[i]["file1"].asString()));
		spr->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr->setLayer(v[i]["position"]["z"].asInt());
		spr->Scale(0.85f, 0.85f);

		eyes.emplace(str, spr);

		Sprite* spr2 = new Sprite(TextureUtil::LoadPng(v[i]["file2"].asString()));
		spr2->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr2->setLayer(v[i]["position"]["z"].asInt());
		spr2->Scale(0.85f, 0.85f);

		eyes.emplace(str + "-lean", spr2);
	}
}

void Monika::Body::draw()
{
	if (filter != 5) {
		hairB->Draw();
	}
	else {
		leanHairB->Draw();
	}

	sceGuEnable(GU_ALPHA_TEST);
	for (auto [str, s] : sprts) {
		for (auto strs : filters[filter]) {


			if (str == strs) {
				s->Draw();
			}

			if (str == "base" || str == "base2") {
				if (filter != 5) {
					hairF->Draw();
				}
				else {
					leanHairF->Draw();
				}
			}
		}
	}

	if (filter != 5) {
		eyes[currentEyes]->Draw();
	}
	else {
		eyes[currentEyes + "-lean"]->Draw();
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
