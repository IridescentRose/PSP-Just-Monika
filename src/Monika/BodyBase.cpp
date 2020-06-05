#include "BodyBase.h"
#include <Utilities/Logger.h>
#include <Utilities/Input.h>
#include <iostream>
#include "../RAM.h"

Monika::Body::Body()
{
	initFilters();
	filter = 0;
	Json::Value v = Utilities::JSON::openJSON("./assets/body.json")["data"];

	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();

		Sprite* spr = new Sprite(TextureUtil::LoadPng(v[i]["file"].asString()));
		spr->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr->setLayer(v[i]["position"]["z"].asInt());
		spr->Scale(1.8f, 1.8f);
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
	std::string clothingChoice = v["outfit"].asString();
	currentEyes = "normal";
	currentEyebrows = "mid";
	currentMouth = "smirk";
	currentBlush = "none";
	currentTears = "none";

	std::string rib = v["ribbon"].asString();

	std::string poseParse = v["pose"].asString();
	if (poseParse == "crossed") { filter = 0; }
	if (poseParse == "down") { filter = 1; }
	if (poseParse == "point") { filter = 2; }
	if (poseParse == "rest") { filter = 3; }
	if (poseParse == "steepling") { filter = 4; }
	if (poseParse == "lean") { filter = 5; }


	v = Utilities::JSON::openJSON("./assets/outfits.json")["data"];
	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();

		std::string filename = v[i]["file"].asString();
		size_t start_pos = filename.find("[name]");
		if (start_pos != std::string::npos) {
			filename.replace(start_pos, std::string("[name]").length(), clothingChoice);
		}

		Sprite* spr = new Sprite(TextureUtil::LoadPng(filename));
		spr->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr->setLayer(v[i]["position"]["z"].asInt());
		spr->Scale(0.9f * 2.0f, 0.9f * 2.0f);
		sprtsc.emplace(str, spr);
	}

	ignoreRibbon = true;
	if(hairChoice == 0){
		hairF = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/default/default-f.png"));
		hairB = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/default/default-b.png"));
		leanHairF = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/lean/default-f.png"));
		leanHairB = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/lean/default-b.png"));
		hairF->Scale(0.9f * 2.0f, 0.9f * 2.0f);
		hairB->Scale(0.9f * 2.0f, 0.9f * 2.0f);
		leanHairF->Scale(0.9f * 2.0f, 0.9f * 2.0f);
		leanHairB->Scale(0.9f * 2.0f, 0.9f * 2.0f);
		hairF->SetPosition(240, 96);
		hairF->setLayer(1);
		hairB->SetPosition(280, 128);
		hairB->setLayer(0);
		leanHairF->SetPosition(240, 124);
		leanHairF->setLayer(1);
		leanHairB->SetPosition(264, 164);
		leanHairB->setLayer(0);
		ignoreRibbon = false;
	}else if(hairChoice == 1){
		hairF = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/default/down-f.png"));
		hairB = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/default/down-b.png"));
		leanHairF = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/lean/down-f.png"));
		leanHairB = new Sprite(TextureUtil::LoadPng("./assets/images/monika/hair/lean/down-b.png"));
		hairF->Scale(0.9f * 2.0f, 0.9f * 2.0f);
		hairB->Scale(0.9f * 2.0f, 0.9f * 2.0f);
		leanHairF->Scale(0.9f * 2.0f, 0.9f * 2.0f);
		leanHairB->Scale(0.9f * 2.0f, 0.9f * 2.0f);
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
		hairF->Scale(0.9f * 2.0f, 0.9f * 2.0f);
		hairB->Scale(0.9f * 2.0f, 0.9f * 2.0f);
		leanHairF->Scale(0.9f * 2.0f, 0.9f * 2.0f);
		leanHairB->Scale(0.9f * 2.0f, 0.9f * 2.0f);
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
		spr->Scale(0.85f * 2.0f, 0.85f * 2.0f);

		eyes.emplace(str, spr);

		Sprite* spr2 = new Sprite(TextureUtil::LoadPng(v[i]["file2"].asString()));
		spr2->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr2->setLayer(v[i]["position"]["z"].asInt());
		spr2->Scale(0.85f * 2.0f, 0.85f * 2.0f);

		eyes.emplace(str + "-lean", spr2);
	}

	v = Utilities::JSON::openJSON("./assets/face.json")["eyebrows"];
	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();

		Sprite* spr = new Sprite(TextureUtil::LoadPng(v[i]["file1"].asString()));
		spr->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr->setLayer(v[i]["position"]["z"].asInt());
		spr->Scale(0.85f * 2.0f, 0.85f * 2.0f);

		eyebrows.emplace(str, spr);

		Sprite* spr2 = new Sprite(TextureUtil::LoadPng(v[i]["file2"].asString()));
		spr2->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr2->setLayer(v[i]["position"]["z"].asInt());
		spr2->Scale(0.85f * 2.0f, 0.85f * 2.0f);

		eyebrows.emplace(str + "-lean", spr2);
	}

	v = Utilities::JSON::openJSON("./assets/face.json")["mouths"];
	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();

		Sprite* spr = new Sprite(TextureUtil::LoadPng(v[i]["file1"].asString()));
		spr->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr->setLayer(v[i]["position"]["z"].asInt());
		spr->Scale(0.85f * 2.0f, 0.85f * 2.0f);

		mouths.emplace(str, spr);

		Sprite* spr2 = new Sprite(TextureUtil::LoadPng(v[i]["file2"].asString()));
		spr2->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr2->setLayer(v[i]["position"]["z"].asInt());
		spr2->Scale(0.85f * 2.0f, 0.85f * 2.0f);

		mouths.emplace(str + "-lean", spr2);
	}


	v = Utilities::JSON::openJSON("./assets/face.json")["blushes"];
	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();


		Sprite* spr = new Sprite(TextureUtil::LoadPng(v[i]["file1"].asString()));
		spr->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr->setLayer(v[i]["position"]["z"].asInt());
		spr->Scale(0.8f * 2.0f, 0.8f * 2.0f);

		blushes.emplace(str, spr);

		Sprite* spr2 = new Sprite(TextureUtil::LoadPng(v[i]["file2"].asString()));
		spr2->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr2->setLayer(v[i]["position"]["z"].asInt());
		spr2->Scale(0.8f * 2.0f, 0.8f * 2.0f);

		blushes.emplace(str + "-lean", spr2);
	}

	v = Utilities::JSON::openJSON("./assets/face.json")["tears"];
	for (int i = 0; i < v.size(); i++) {
		std::string str = v[i]["name"].asString();

		Sprite* spr = new Sprite(TextureUtil::LoadPng(v[i]["file1"].asString()));
		spr->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr->setLayer(v[i]["position"]["z"].asInt());
		spr->Scale(0.85f, 0.85f);

		tears.emplace(str, spr);

		Sprite* spr2 = new Sprite(TextureUtil::LoadPng(v[i]["file2"].asString()));
		spr2->SetPosition(v[i]["position"]["x"].asInt(), v[i]["position"]["y"].asInt());
		spr2->setLayer(v[i]["position"]["z"].asInt());
		spr2->Scale(0.85f, 0.85f);

		tears.emplace(str + "-lean", spr2);
	}

	ribbon = NULL;
	ribbonL = NULL;

	if (!ignoreRibbon) {
		v = Utilities::JSON::openJSON("./assets/accessories.json")["ribbons"][rib];



		ribbon = new Sprite(TextureUtil::LoadPng(v["file1"].asString()));
		ribbon->setLayer(v["position"]["z"].asInt());
		ribbon->SetPosition(v["position"]["x"].asInt(), v["position"]["y"].asInt());
		ribbon->Scale(0.85f * 2.0f, 0.85f * 2.0f);



		ribbonL = new Sprite(TextureUtil::LoadPng(v["file2"].asString()));
		ribbonL->setLayer(v["position"]["z"].asInt());
		ribbonL->SetPosition(v["position"]["x"].asInt(), v["position"]["y"].asInt());
		ribbonL->Scale(0.85f * 2.0f, 0.85f * 2.0f);

	}

	u32 ramA = freeMemory();
	Utilities::app_Logger->log(std::to_string((float)ramA / 1024.f / 1024.f) + "MB");
}

void Monika::Body::draw()
{
	if (filter != 5) {
		hairB->Draw(true);
	}
	else {
		leanHairB->Draw(true);
	}

	sceGuAlphaFunc(GU_GEQUAL, 64, 0xFFFFFFFF);
	sceGuEnable(GU_ALPHA_TEST);
	sceGuEnable(GU_BLEND);
	for (auto [str, s] : sprts) {
		for (auto strs : filters[filter]) {


			if (str == strs) {
				s->Draw(true);
				sprtsc[str]->Draw(true);
				if (strs == "base" || strs == "base2") {
					if (!ignoreRibbon) {
						if (filter != 5) {
							if (ribbon != NULL)
								ribbon->Draw(true);
						}
						else {
							if (ribbonL != NULL)
								ribbonL->Draw(true);
						}
					}

					if (filter != 5) {
						hairF->Draw(true);
					}
					else {
						leanHairF->Draw(true);
					}
				}
			}

			
		}
	}

	if (filter != 5) {
		eyes[currentEyes]->Draw(true);
	}
	else {
		eyes[currentEyes + "-lean"]->Draw(true);
	}
	
	if (filter != 5) {
		eyebrows[currentEyebrows]->Draw(true);
	}
	else {
		eyebrows[currentEyebrows + "-lean"]->Draw(true);
	}

	if (filter != 5) {
		mouths[currentMouth]->Draw(true);
	}
	else {
		mouths[currentMouth + "-lean"]->Draw(true);
	}

	if (currentBlush != "none") {
		if (filter != 5) {
			blushes[currentBlush]->Draw(true);
		}
		else {
			blushes[currentBlush + "-lean"]->Draw(true);
		}
	}

	if (currentTears != "none") {
		if (filter != 5) {
			tears[currentTears]->Draw(true);
		}
		else {
			tears[currentTears + "-lean"]->Draw(true);
		}
	}

}

void Monika::Body::update()
{
	
}

void Monika::Body::setExprFilter(std::string str)
{
	if (str.length() >= 4) {
		switch (str.at(0)) {
		case '1': {
			filter = 4;
			break;
		}
		case '6': {
			filter = 1;
			break;
		}

		case '2': {
			filter = 0;
			break;
		}
		case '5': {
			filter = 5;
			break;
		}

		case '3': {}
		case '4': {
			filter = 3;
			break;
		}
		case '7': {
			filter = 2;
			break;
		}

		default: {
			filter = 4;
			break;
		}

		}

		switch (str.at(1)) {
		case 'd': {
			currentEyes = "closed-sad";
			break;
		}
		case 'h': {
			currentEyes = "closed-happy";
			break;
		}
		case 'e': {
			currentEyes = "normal";
			break;
		}

		case 'l': {
			currentEyes = "left";
			break;
		}
		case 'r': {
			currentEyes = "right";
			break;
		}
		case 'c': {
			currentEyes = "crazy";
			break;
		}
		case 's': {
			currentEyes = "sparkle";
			break;
		}
		case 't': {
			currentEyes = "smug";
			break;
		}
		case 'w': {
			currentEyes = "wide";
			break;
		}
		case 'f': {
			currentEyes = "soft";
			break;
		}
		case 'k': {
			currentEyes = "wink-left";
			break;
		}

		default: {
			currentEyes = "normal";
			break;
		}
		}

		switch (str.at(2)) {
		case 'k': {
			currentEyebrows = "knit";
			break;
		}
		case 'f': {
			currentEyebrows = "furrowed";
			break;
		}
		case 's': {
			currentEyebrows = "mid";
			break;
		}
		case 'u': {
			currentEyebrows = "up";
			break;
		}
		case 't': {
			currentEyebrows = "think";
			break;
		}
		default: {
			currentEyebrows = "mid";
			break;
		}

		}

		//Well now we have the basics, we have optional blush, tears, and sweatdrops. Our app doesn't care about sweatdrops (look nearly invisible!)
		//A regular line will be 4

		int finalPos = str.length() - 1;

		if (str.length() == 6) {
			//Could be a sweat drop, blush, or tears
			if (str.at(3) == 'b') {
				//Blush
				if (str.at(4) == 'f') {
					currentBlush = "full";
				}
				else if (str.at(4) == 's') {
					currentBlush = "shade";
				}
				else if (str.at(4) == 'l') {
					currentBlush = "lines";
				}
				else {
					currentBlush = "none";
				}
			}else if (str.at(3) == 't') {
				//Tears
				switch (str.at(4)) {
				case 's': {
					currentTears = "streaming";
					if (currentEyes == "closed-happy" || currentEyes == "closed-sad" || currentEyes == "wink-left") {
						currentTears += "-" + currentEyes;
					}
					break;
				}
				case 'u': {
					currentTears = "up";
					if (currentEyes == "closed-happy" || currentEyes == "closed-sad" || currentEyes == "wink-left") {
						currentTears += "-" + currentEyes;
					}
					break;
				}
				case 'd': {
					currentTears = "dried";
					break;
				}

				case 'p': {
					currentTears = "pooled";
					if (currentEyes == "closed-happy") {
						currentTears += "-" + currentEyes;
					}
					break;
				}
				}
			}
		}
		else if (str.length() == 8) {
			//Could be a combination
			if (str.at(3) == 'b') {
				//Blush
				if (str.at(4) == 'f') {
					currentBlush = "full";
				}
				else if (str.at(4) == 's') {
					currentBlush = "shade";
				}
				else if (str.at(4) == 'l') {
					currentBlush = "lines";
				}
				else {
					currentBlush = "none";
				}
			}

			if (str.at(5) == 't') {
				//Tears
				switch (str.at(4)) {
				case 's': {
					currentTears = "streaming";
					if (currentEyes == "closed-happy" || currentEyes == "closed-sad" || currentEyes == "wink-left") {
						currentTears += "-" + currentEyes;
					}
					break;
				}
				case 'u': {
					currentTears = "up";
					if (currentEyes == "closed-happy" || currentEyes == "closed-sad" || currentEyes == "wink-left") {
						currentTears += "-" + currentEyes;
					}
					break;
				}
				case 'd': {
					currentTears = "dried";
					break;
				}

				case 'p': {
					currentTears = "pooled";
					if (currentEyes == "closed-happy") {
						currentTears += "-" + currentEyes;
					}
					break;
				}
				}
			}
		}
		else {
			currentBlush = "none";
			currentTears = "none";
		}


		//Mouth is final
		switch (str.at(finalPos)) {
		case 'a': {
			currentMouth = "smile";
			break;
		}

		case 'b': {
			currentMouth = "big";
			break;
		}
		case 'c': {
			currentMouth = "smirk";
			break;
		}
		case 'u': {
			currentMouth = "smug";
			break;
		}
		case 'd': {
			currentMouth = "small";
			break;
		}
		case 'w': {
			currentMouth = "wide";
			break;
		}
		case 't': {
			currentMouth = "triangle";
			break;
		}
		case 'p': {
			currentMouth = "pout";
			break;
		}
		case 'o': {
			currentMouth = "gasp";
			break;
		}
		case 'x': {
			currentMouth = "angry";
			break;
		}

		default: {
			currentMouth = "smile";
			break;
		}
		}
	}
	else {
		Utilities::app_Logger->log("ERROR: UNKOWN POSE " + str + "!");
	}
	
}

/*
struct Filter {
		std::string eyes, eyebrows, mouths, blushes, tears;
		int filter;
		bool lean;
};
*/
void Monika::Body::initFilters()
{
	
}
