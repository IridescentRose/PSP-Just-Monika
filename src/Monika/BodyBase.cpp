#include "BodyBase.h"
#include <Utilities/JSON.h>

Monika::Body::Body()
{
	Json::Value v = Utilities::JSON::openJSON("body.json");

}

void Monika::Body::draw()
{
	for (auto s : sprts) {
		s->Draw();
	}
}

void Monika::Body::update()
{
}
