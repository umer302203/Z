"""Fix gloss_map.json -> data/gloss_final.json (display policy).

Layers:
  1. HI_FIX   : Devanagari garbles/misses -> correct English (context-verified)
  2. HI_BLANK : Devanagari function words that must never display
  3. Latin rule: [a-z]+ words -> identity UNLESS in EN_STOP / HI_LATIN_STOP
  4. HI_LATIN_MAP: Latin-script Hindi words -> english (pehle->first ...)
  5. Sanity: lowercase, [a-z0-9-]+ only, length 2..18
"""
import json
import re

BASE = "/home/z/my-project"

HI_FIX = {
    # --- context-verified corrections of wrong glosses ---
    "सर्जन": "surgeon", "गोल": "goal", "कोट": "code", "पेशन": "patient",
    "पेश्ँन्ट": "patient", "प्रिजवर": "preserve", "जूट": "lie",
    "दिसाइट": "decide", "देडलाई": "deadline", "दमज": "damage",
    "चीज़िंग": "choosing", "पलन्र": "planner", "चोटी": "small",
    "फ्रगेटिख": "fragile", "बोन": "bone", "दिमाग": "brain",
    "याद": "remember", "सवाल": "question", "देट": "data", "देटा": "data",
    "दून": "", "दूँन": "", "थ्रा": "", "त्रपर": "", "तोर": "", "दर": "",
    "जबाब": "answer", "ठीक": "ok", "चीज़ें": "things",
    # --- seeing / showing ---
    "दिखा": "show", "दिखाईए": "show", "दीखना": "show", "देखना": "see",
    "देखने": "see", "देखता": "see", "देखकर": "see", "देकता": "see",
    # --- time / order / degree ---
    "दिन": "day", "दिनो": "days", "पहले": "first", "पहली": "first",
    "पिछले": "previous", "पुरानी": "old", "पुराने": "old", "पुरा": "full",
    "पूरी": "full", "जल्दी": "soon", "दूसरे": "other", "नया": "new",
    "नाम": "name", "नीचे": "below", "नेक्स": "next", "आगा": "next",
    "आगी": "next", "ज़ोरत": "need", "जरुरत": "need", "जयादा": "more",
    "जादा": "more", "महीने": "month", "सात": "seven", "धीरे": "slow",
    "वक्त": "time", "वाखत": "time", "सेकंड": "second", "सीकून्स": "seconds",
    "लांगटर": "long-term", "लोंक्टाम": "long-term", "लोंग्टाम": "long-term",
    "लोंग्टोम": "long-term", "लेटिस्ट": "latest", "बाखी": "remaining",
    # --- core ASR garbles of technical loanwords ---
    "अटेन्चन": "attention", "अतेशन": "attention", "अंटलगेंस": "intelligence",
    "अंड़्टान्टिं": "understanding", "अंश्रूमेंट्स": "assumptions",
    "अंसर्टेंटी": "uncertainty", "अईद्या": "idea", "अईट्या": "idea",
    "अईप्ट": "input", "अक्षन": "action", "आक्षिन": "action",
    "आक्ष्चन": "action", "अच्टरनल": "internal", "अटमातिकली": "automatically",
    "अटोमातिक": "automatic", "अबजर्व": "observe", "अबजेक्त्स": "objects",
    "अबज़्ेट": "objects", "अबडेट": "update", "अबदेट": "update",
    "अब्टेट": "update", "अर्गनाईज": "organize", "असिस्ट्टन्": "assistant",
    "आंसर": "answer", "आंसर्स": "answers", "आनसर": "answer",
    "आखितेक्च्छा": "architecture", "इंटरनल": "internal", "इंपूट": "input",
    "इन्पूट": "input", "इंपोट्टन्स": "important", "इंप्रुव": "improve",
    "इंप्लोई": "employ", "इगनोर": "ignore", "इन्फोमेशन": "information",
    "इमजज़": "images", "एकजाम्ठल": "example", "एकजाम्पल": "example",
    "एकसपर्ट्स": "experts", "एकसपीरेंज": "experience",
    "ठेक्सपीरियंज": "experience", "एकसिस्टिँन": "existence",
    "एक्छिकुष्टूल": "execute", "एजीआई": "AGI", "एवविदेन्स": "evidence",
    "एविदेन": "evidence", "कंटिशन्स": "conditions", "कनेक्त": "connect",
    "कनेक्षिन्स": "connections", "कनेख्छन": "connection",
    "कन्तिन्ट्यूल": "continual", "कमपनी": "company", "कम्पनी": "company",
    "कमपयर": "compare", "कम्पलीट": "complete", "कमूनिकेशन": "communication",
    "कम्जोर": "weak", "कुनवासेशन": "conversation",
    "कोन्वसेश्टिन्स": "conversations", "कुन्फलिक्त": "conflict",
    "केपिपिलिटीज": "capabilities", "कोच्छसनिस": "consciousness",
    "नूलज": "knowledge", "नूलिच": "knowledge", "नफोमेशन": "information",
    "न्फोमिशन": "information", "न्फोमेशन": "information",
    "नम्बर्स": "numbers", "नोटेस": "notes", "पमिशन्स": "permissions",
    "प्रमिश्यन्स": "permissions", "परामेटर्स": "parameters",
    "पाटरन्स": "patterns", "पाट्टन": "pattern", "पाट्टुन्स": "patterns",
    "पावोफुल": "powerful", "प्रँडन्त": "", "प्रटिक्छन": "",
    "प्रटिक्षन": "", "प्रटिक्त": "", "प्रफ्रिफ्रन्षेज": "",
    "प्रबलम": "problem", "प्रमनेंट": "permanent", "प्राईटीख": "privacy",
    "प्रोग्राम": "program", "प्रोग्रेज": "progress", "प्रोजट": "project",
    "प्रोजेक": "project", "प्रोज्ट": "project", "प्लन": "plan",
    "प्लनिग": "planning", "प्लानिँग": "planning", "प्लानिग": "planning",
    "फाट्यल": "factual", "फाट्यल्स": "factual", "फैक्ट्स": "facts",
    "फलक्सबल": "flexible", "फिल": "feel", "फुछर": "future",
    "फीटबाख": "feedback", "फीटबाग": "feedback", "फेल": "fail",
    "फेल्लिर": "failure", "फिसिक्स": "physics", "तेक्स्त": "text",
    "तेबल": "table", "तूल": "tool", "तूल्स": "tools", "तिंक": "think",
    "ट्रान्सफोरमर": "transformer", "त्राँस्वाँर": "transformer",
    "त्रान्सफोमर": "transformer", "त्रान्स्फामर": "transformer",
    "त्रान्स्फोमर": "transformer", "तेमठ्रच्यर": "transformer",
    "त्रीनिग": "training", "त्रेनिग": "training", "थि": "",
    "थींटेंता": "attention", "दून्या": "world", "जानता": "knows",
    "दाएगनोसिस": "diagnosis", "दिस्टन्स": "distance", "देटाबेस": "database",
    "देपार्टमेंस": "departments", "देडलाई": "deadline", "दोक्छर": "doctor",
    "दोक्तर": "doctor", "दूनिया": "world", "दूँनिया": "world",
    "दूड़ेगा": "", "धीछा": "", "नजा": "", "नाग": "", "निस्तम": "",
    "नहींज़ंसखा": "", "नेई": "", "नेक": "", "निए": "", "नूं": "",
    "पहुटवन्त": "", "पहुट्टवन्त": "", "पुछनेचाँने": "", "पूँब्योंगे": "",
    "देखलाप": "", "दिख्रन": "", "दिसाइट": "decide", "दोरान": "during",
    "दोगन्गर्ट्स": "", "दर्वीसात्तीम": "", "देडलाई": "deadline",
    "डायग्राम": "diagram", "डिसिचन": "decision", "टीचर": "teacher",
    "टेक्स्ट": "text", "टेस्ट": "test", "तेस्त": "test", "थेज्ट": "test",
    "ट्राफिक": "traffic", "नजा": "", "परसन": "person", "परस्ट्षन": "person",
    "पिछले": "previous", "पेश्थ": "past", "पास्ट": "past",
    "फोकस": "focus", "फोलो": "follow", "फ्लुएंट": "fluent",
    "फ्लूएण्ट": "fluent", "ब्रेन": "brain", "बहेविर": "behavior",
    "बूक्स": "books", "बदरना": "change", "बना": "build",
    "बनाएगा": "build", "बनाएंगी": "build", "बहतरीन": "best",
    "बीसिक": "basic", "बेसिख": "basic", "बता": "tell", "बताती": "tell",
    "भरोसा": "trust", "भूलता": "forget", "मतलप": "meaning",
    "मतलब": "meaning", "मत्लब": "meaning", "मप्टलप": "meaning",
    "मदद": "help", "मस्ला": "problem", "मशला": "problem",
    "मिसाल": "example", "मीटिंग": "meeting", "मी्तिख": "meeting",
    "मुमकिन": "possible", "मुम्किन": "possible", "मुख्तलिफ": "different",
    "मूनिटरिंग": "monitoring", "मेटिकल": "medical", "मैट्स": "math",
    "मैमरी": "memory", "मुडल": "model", "मुडल्स": "models",
    "मुढ्ल": "model", "मुद्यूल्दा": "model", "मोडल": "model",
    "मोड्वूल्स": "modules", "मोड्टूल्स": "", "यूज": "use", "यूस": "use",
    "यूस्फुल": "useful", "रखना": "keep", "रखा": "keep", "रकता": "keep",
    "रकही": "keep", "रिजल्त": "result", "रिजाल्ट": "result",
    "रिज़्ाल्ट": "result", "रिजल्टा": "result", "रीजाल्ट": "result",
    "रिलएबल": "reliable", "रिलायबल": "reliable", "रिलीशन्स": "relations",
    "रिलेटिड": "related", "रीशच": "research", "रीसोर्सिएज": "resources",
    "रूम": "room", "रूल्ज": "rules", "रेकोट्च": "records",
    "रेट्रीव": "retrieve", "रेप्रिश्टेशन्स": "representations",
    "रेलिवेंट": "relevant", "रेलेवंट": "relevant", "रेलेविंट": "relevant",
    "रेलेवेंट": "relevant", "रेलेटी": "relevant",
    "रेलायाबिलीटी": "reliability", "रोबाट": "robot", "रवकिग": "working",
    "लंगविज": "language", "लंगवेज": "language", "लबूरीट्री": "laboratory",
    "लाज़र": "laser", "लिस्ट": "list", "लूप": "loop",
    "लिखना": "write", "लिखते": "write", "लिखेगा": "write",
    "वरीफिकेशन": "verification", "वल्ट": "vault", "वुल्ट": "vault",
    "वल्ड": "world", "वोल्ड": "world", "वीकनेस": "weakness",
    "वुरकिं": "working", "वोकिं": "working", "वोकिंट": "working",
    "वोकिम": "working", "वोगिं": "working", "वूमन": "woman",
    "वेप्साइट": "website", "वेप": "web", "वेरिफाइ": "verify",
    "वेरिफाई": "verify", "वोस्पितल": "hospital", "संटंस": "sentences",
    "सब्ज्ट्स": "subjects", "सब्ज्ट्": "subject", "समच": "understand",
    "समज": "understand", "समझ": "understand", "समजजाए": "understand",
    "समचकर": "understanding", "समरी": "summary", "समार्ट": "smart",
    "सिंपल": "simple", "सिस्तम": "system", "सिस्तम्स": "systems",
    "सीकता": "learn", "सीखे": "learn", "सूर्सिज": "sources",
    "सेंट्रल": "central", "सेंसर": "sensor", "सेल्फ": "self",
    "सेव": "save", "सोर्से": "source", "स्खिल": "skill", "स्टेप": "step",
    "स्टेप्स": "steps", "स्थेपस": "steps", "स्तूड़न्त": "student",
    "स्त्य迅लिस्ट": "specialist", "स्पेशलिस्त": "specialist",
    "स्लूशन": "solution", "हाजारो": "thousands", "हिस्सों": "parts",
    "हुमन": "human", "हैल्प": "help", "चूस": "choose", "चेंच": "change",
    "चेक्करना": "check", "जवाप": "answer", "गरन्टी": "guarantee",
    "गरन्ति": "guarantee", "गाडी": "car", "कुन्टेक्स्त": "context",
    "कोंतेक्स्त": "context", "अखिटेक्चर": "architecture",
    "क्यल्कूलेटर": "calculator", "काल्कौलेटर": "calculator",
    "हलुसिनेशन": "hallucination", "ग्रूंटिंग": "grounding",
    "कोडीनेशन": "coordination", "कोर": "core", "क्लीन": "clean",
    "क्लीर": "clear", "क्रिएट": "create", "जनरेट": "generate",
    "गारेंटी": "guarantee", "अंदाजा": "estimate", "जरूरी": "necessary",
    "गलत": "wrong", "चेक": "check", "चेकिंग": "checking",
    "अंग्रेज़ी": "english", "स्पष्ट्यालिए": "", "स्छाएगिते": "",
    "स्टनल": "", "स्टन्टंस": "", "स्वर": "", "स्व्ट": "",
    "मुवम्म्ड": "", "मुषकिल": "difficult", "मिक्छाु": "",
    "स्पेक्टूलेशन": "speculation", "शाटेशन": "", "संसर": "",
    "साँड": "", "साद": "", "सामडे": "", "सामने": "", "सरच": "",
    "सहीं": "", "सींग": "", "सुचता": "", "सुन्ने": "", "सिण्": "",
    "सित्मन": "", "हवतों": "", "हिस्वोंपर": "", "ह्ब": "", "ृृृृृृृृ": "",
    "분들": "", "스": "", "यॐस": "use", "रँट": "", "रक": "",
    "रदवार": "", "रप्रिजन्त": "", "रब": "", "रभ": "", "रशागे": "",
    "रों": "", "रोग": "", "रोट": "", "रील": "", "वोर्ट्स": "",
    "वोडल्ठ": "", "वीट": "", "वेम्रि": "", "शकिल": "skill",
    "शाइत": "", "शाए": "", "बआगेर": "", "बईलागागागाजोंगेद": "",
    "बगयार": "", "बग़े": "", "बड़ल": "", "बलकी": "", "बसरट्यागेगाधा": "",
    "बाननिक": "", "बावद": "", "बिगर": "", "बुलाया": "", "ब्रुड़े": "",
    "ब्रूव्ट": "", "भीचता": "", "भीात": "", "भ्ब्लू": "", "मंगता": "",
    "मच": "", "मर्द": "", "मुआ": "", "मुकिन": "", "मैच": "",
    "म्ठमातक्स": "math", "यवईंट्स": "", "याई": "", "यार": "", "यी": "",
    "येएएएएएएएएएएएएएए": "", "रिपोड": "", "रिल": "", "रीच": "",
    "रीजनिग": "reasoning", "रेल": "", "लंबी": "", "लक": "",
    "लकता": "", "लगा": "", "लगाने": "", "लगता": "", "लव्स": "",
    "लाएक्ली": "", "लाको": "", "लिएट": "", "लिएिनिएमपूट": "",
    "लिकन": "", "लिकिन": "", "लिग": "", "लिटर": "", "लियर": "",
    "लिये": "", "लीना": "", "ले": "", "लेएिएएएगार": "", "लेक": "",
    "लेकिन": "", "लेकोट्स": "", "लेगाची": "", "लेता": "", "लेर": "",
    "लेरनें": "", "वापस": "", "सकता": "", "सकती": "", "सकते": "",
    "सके": "", "सक्ता": "", "सब": "", "सबसे": "", "सही": "correct",
    "समहाल": "", "सरफ": "", "सर्फ": "", "साथ": "", "हमारे": "",
    "हर": "", "हुना": "", "हुने": "", "हूं": "", "हूए": "", "था": "",
    "न": "", "नहीं": "", "ना": "", "ने": "", "पर": "", "प्वेख": "",
    "फर": "", "फरुन": "", "फिर": "", "तक": "", "तन": "", "तभीगार": "",
    "तभीर्आर": "", "तमप्ररी": "", "तरता": "", "तूट": "", "तेखल": "",
    "तो": "", "गर": "", "गर्ठी": "", "गर्प": "", "गुप": "",
    "चन्टलेन": "", "चलीज": "", "चाहीग": "", "चालिएँ": "", "जगा": "",
    "जबा": "", "जबाद": "", "ज़ा्ता": "", "ख़ट्छूली": "", "खाम": "",
    "खीटने": "", "ख़द्म": "", "गंटों": "", "कॆत": "", "कुछ्टन": "",
    "कुन्सा": "", "काई": "", "काईर": "", "काप": "", "कम्रा": "",
    "करी": "", "करूं": "", "करे": "", "करें": "", "करो": "",
    "कह": "", "कहा": "", "कहाजाए": "", "कहुना": "", "कि": "",
    "किसम": "", "किसी": "", "कैसे": "", "क्या": "", "क्योंके": "",
    "कब": "", "कभी": "", "कोई": "", "कोईर": "", "कोस": "",
    "क्यम्रा": "", "क्रज्ट्तेरा": "", "केवदिगद": "", "केटिस्ट्रो": "",
    "कच्च्चनेस": "", "कच्ऽक्पाश्टनेचन": "", "कन्तिन्यूल": "continual",
    "कप": "", "कम्ठीत": "", "कैमरा": "", "ज़रूरत": "need",
    "एएएएएएएएएएएएएएएएएएएएएएएएएएएए": "", "एक": "", "एगाईएगा": "",
    "एन्फ": "", "एसी": "", "ओल": "", "और": "", "ओए": "",
    "उएा": "", "उठाया": "", "उपुनिன": "", "उस": "", "उसका": "",
    "उसके": "", "उसे": "", "आई": "", "आईई": "", "आकोला": "",
    "आक्त": "", "आजा": "", "आजे": "", "आता": "", "आद": "",
    "आपकी": "", "आबस्ट्ट्ख्चन": "", "आम": "", "आसकती": "",
    "इं": "", "इस": "", "इसका": "", "इसके": "", "इसलिये": "",
    "इसी": "", "इसे": "", "अईटिल": "", "अईट्या": "idea",
    "अकेली": "", "अक्षें": "", "अग": "", "अगरे": "", "अगी": "",
    "अच्टूड़ेंट": "", "अच्धाम": "", "अजी": "", "अजुद": "", "अज्टर": "",
    "अथा": "", "अध्फुट": "", "अनसेथ": "", "अन्सर": "answer",
    "अपना": "", "अपनी": "", "अपने": "", "अपास": "", "अब": "",
    "अबजेक्त्स": "objects", "अभ": "", "अभी": "", "अर": "",
    "अरेट्टेक्छीर": "", "अवाविर": "", "असाभाanishiloveachyaakshana": "",
    "असिस्ट्टन्": "assistant", "आख्चन्स": "", "आगर": "",
}

# Devanagari function words that leaked through with LLM glosses -> blank
HI_BLANK = set("""
अगर दे किस पास जाता जाते देना कुछ जो जब तब तभी किया गया चला चाही
दिया देता देती दो जैसा गिरा दुबारा दीन थाद्टर पो� परमनेंगेई
साथ लिए फिर भी ही बहुत सब सबसे बाद बारे वापस सरफ सर्फ शायएद शाएद
कर करना करने करता करती करते सकता सकती सकते रहा रही रहे रहें रहेगा रहेगी
लेता लेना देंगे देंगी जाएगा जाएगी जाने करेगा करेगी होगा होगी होगे
""".split())

# Devanagari function words that leaked through with LLM glosses -> blank
HI_BLANK = set("""
अगर दे किस पास जाता जाते देना कुछ जो जब तब तभी किया गया चला चाही
दिया देता देती दो जैसा गिरा दुबारा दीन थाद्टर परमनेंगेई
साथ लिए फिर भी ही बहुत सब सबसे बाद बारे वापस सरफ सर्फ शायएद शाएद
कर करना करने करता करती करते सकता सकती सकते रहा रही रहे रहें रहेगा रहेगी
लेता लेना जाएगा जाएगी जाने करेगा करेगी होगा होगी होगे
""".split())

# Latin-script words that are really Hindi function words (blank)
HI_LATIN_STOP = set("""
wo bhi hai hain hota hote hotha hui ho hoGi hoti ka ke ki ko kya kuch kis
karna karne kare karta karte karein krta kar sakta sakti sakte se mein me
liye lakin lekin aur ya agar jo jab tak sab bilkul nahi aisa jaisi iske
usse wala yey ek ab hi ge tak ubharta vakti rehte samajie sumja situati
seekhi seekne seekta nazaate pothata kisaad lagane lagata darmean deekta
dekta detast divite basedin betaay bhedh aari aasakta aasani aksar apni
baad baath chalana hameesha memor isliye phrhir likin wo woGu woGu
darmean aksar Isi Likin Phrhir Wo Neden Isi wo yey Wo
pehle pahle purani porani purane pichle dosre duniya dhire matlab rozana
zyada madad deta naath betaay khas kitni kyu kuyn
""".split())

# English function words (blank)
EN_STOP = set("""
the a an and or but if so as of to in on at by for with from is are was
were be been am do does did done go goes gone went have has had can cannot
could will would shall should may might must this that these those there
here than then when while what which who whom whose how why where all
every each some any no not none you i we they he she it him her them his
its their our my your me us of off up down out over under again further
once only own same too very just also than about into through during
before after above below between out off over under more most other such
nor own s t don now d ll m o re ve y ain aren couldn didn doesn hadn
haven isn ma mightn mustn needn shan shouldn wasn weren won wouldn
""".split())


def clean_gloss(g):
    g = str(g).strip().lower()
    g = re.sub(r"[^a-z0-9-]", "", g)
    if not g or len(g) < 2 or len(g) > 18:
        return ""
    return g


def main():
    gloss = json.load(open(f"{BASE}/data/gloss_map.json", encoding="utf-8"))
    final = {}
    stats = {"hi_fix": 0, "latin_id": 0, "latin_blank": 0, "kept": 0, "blank": 0}

    for w, g in gloss.items():
        # 0. explicit blank list wins
        if w in HI_BLANK:
            final[w] = ""
            stats["latin_blank"] += 1
            continue
        # 1. explicit Devanagari overrides
        if w in HI_FIX:
            v = clean_gloss(HI_FIX[w])
            final[w] = v
            stats["hi_fix"] += 1
            continue
        # 2. latin-script handling
        if re.fullmatch(r"[A-Za-z]+", w):
            lw = w.lower()
            if lw in HI_LATIN_STOP:
                final[w] = ""
                stats["latin_blank"] += 1
            elif lw in EN_STOP:
                final[w] = ""
                stats["latin_blank"] += 1
            else:
                final[w] = clean_gloss(lw)
                stats["latin_id"] += 1
            continue
        # 3. Devanagari from LLM gloss
        v = clean_gloss(g)
        final[w] = v
        if v:
            stats["kept"] += 1
        else:
            stats["blank"] += 1

    with open(f"{BASE}/data/gloss_final.json", "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=0)

    n_disp = sum(1 for v in final.values() if v)
    print(f"[glossfix] {stats}")
    print(f"[glossfix] displayable: {n_disp}/{len(final)}")


if __name__ == "__main__":
    main()
