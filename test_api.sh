#!/bin/bash

echo "🧪 Testování Joke API..."
echo ""

BASE_URL="http://localhost:8000"

echo "1️⃣ Test základních informací (GET /):"
curl -s $BASE_URL | python3 -m json.tool
echo ""
echo ""

echo "2️⃣ Test českého normálního vtipu:"
curl -s "$BASE_URL/joke?lang=cz&category=normal" | python3 -m json.tool
echo ""
echo ""

echo "3️⃣ Test českého explicitního vtipu:"
curl -s "$BASE_URL/joke?lang=cz&category=explicit" | python3 -m json.tool
echo ""
echo ""

echo "4️⃣ Test slovenského vtipu:"
curl -s "$BASE_URL/joke?lang=sk&category=normal" | python3 -m json.tool
echo ""
echo ""

echo "5️⃣ Test anglického vtipu (UK):"
curl -s "$BASE_URL/joke?lang=en-gb&category=normal" | python3 -m json.tool
echo ""
echo ""

echo "6️⃣ Test anglického vtipu (US):"
curl -s "$BASE_URL/joke?lang=en-us&category=normal" | python3 -m json.tool
echo ""
echo ""

echo "7️⃣ Test seznamu jazyků:"
curl -s "$BASE_URL/languages" | python3 -m json.tool
echo ""
echo ""

echo "8️⃣ Test seznamu kategorií:"
curl -s "$BASE_URL/categories" | python3 -m json.tool
echo ""
echo ""

echo "9️⃣ Test health check:"
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""
echo ""

echo "🔟 Test neplatného jazyka (očekává se error):"
curl -s "$BASE_URL/joke?lang=invalid" | python3 -m json.tool
echo ""
echo ""

echo "✅ Testy dokončeny!"
