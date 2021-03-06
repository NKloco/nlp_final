# -*- coding: utf-8 -*-
"""
Created on Tues Oct 16 23:33:04 2018
@author: Ken Huang
"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from afinn import Afinn
from collections import Counter
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer

common_words = {"an", "alcohol", "storm", "colleague", "ethics", "cheese", "blame", "regulatory", "parental", "doubt",
                "among", "interaction", "asset", "rapidly", "sail", "mobile", "builder", "desperate", "top", "dramatic",
                "extension", "fold", "cow", "government", "pat", "turkey", "conclude", "presidential", "cell",
                "suffering", "occupy", "cover", "voter", "hang", "photo", "consent", "mask", "instead", "secret",
                "solution", "term", "score", "afterward", "donate", "mexican", "club", "moral", "argue", "motivation",
                "another", "academic", "borrow", "tendency", "hunting", "lie", "develop", "steady", "busy", "thick",
                "hispanic", "sudden", "opinion", "source", "canvas", "politician", "hay", "host", "invite", "work",
                "stone", "lap", "leg", "convince", "careful", "few", "married", "trade", "settle", "machine",
                "strategy", "episode", "mud", "compromise", "crawl", "onion", "environmental", "clean", "van",
                "embarrassed", "thus", "visitor", "proposed", "forever", "threat", "wait", "scare", "row",
                "surveillance", "evident", "note", "height", "electric", "jeans", "sunlight", "gender", "participation",
                "nowhere", "timber", "iron", "aside", "dismiss", "columnist", "emphasis", "pure", "shade", "actually",
                "routinely", "southern", "nest", "organic", "police", "crucial", "vital", "beautiful", "proud",
                "amount", "edge", "fool", "argument", "leather", "flour", "remote", "surgery", "cord", "actively",
                "mistake", "etc", "clip", "animal", "want", "notion", "health-care", "congressional", "cite",
                "strategic", "sustainable", "tomato", "quiet", "loss", "pregnant", "prize", "update", "reliability",
                "toe", "floor", "tuck", "jazz", "pc", "rapid", "similar", "daughter", "region", "rescue", "generate",
                "ear", "extreme", "playoff", "poster", "extensive", "reading", "altogether", "intention", "pulse",
                "comment", "medical", "wheel", "learn", "north", "color", "mixture", "mall", "lost", "collector",
                "extremely", "huh", "contest", "crisis", "morning", "available", "amendment", "rule", "knowledge",
                "familiar", "journal", "foster", "operate", "slightly", "teaspoon", "church", "mentor", "stretch",
                "road", "brown", "longtime", "resemble", "programming", "camp", "hook", "firm", "cargo", "increasingly",
                "unless", "demand", "judgment", "rocket", "offer", "high-tech", "quick", "address", "hers",
                "competitor", "component", "board", "payment", "sick", "guy", "gather", "whatever", "comprise",
                "expertise", "constant", "collaboration", "hurry", "through", "easy", "economically", "situation",
                "house", "gang", "core", "screen", "market", "accomplishment", "scan", "suggestion", "triumph",
                "clothing", "exercise", "difference", "recover", "popularity", "tablespoon", "resist", "to",
                "literally", "committee", "silver", "grandmother", "although", "ass", "feather", "fine", "appropriate",
                "cruel", "partially", "bag", "cookie", "internal", "approach", "expansion", "bid", "choice", "field",
                "grace", "sight", "election", "implementation", "exhibition", "restrict", "growing", "whether", "input",
                "breast", "elbow", "group", "veteran", "overwhelming", "piece", "dock", "guess", "rat", "once",
                "salmon", "call", "column", "beside", "administration", "same", "application", "relation", "why",
                "nine", "kiss", "legal", "removal", "liver", "target", "chinese", "cooperate", "modify", "dessert",
                "accuse", "collection", "pine", "exceed", "plunge", "killer", "occur", "debris", "founder", "beard",
                "earthquake", "pioneer", "wet", "bat", "calendar", "kit", "yellow", "regulation", "administrative",
                "blank", "sun", "endure", "commonly", "pregnancy", "escape", "wander", "costly", "sacred", "complexity",
                "soul", "chase", "train", "future", "sea", "criticize", "act", "separation", "valid", "after",
                "accurately", "coast", "controversy", "concerning", "crime", "deer", "deserve", "nut", "pitch",
                "traditionally", "crop", "dear", "dialogue", "enterprise", "explicit", "dam", "what", "tired",
                "diabetes", "influence", "marry", "location", "stick", "home", "tongue", "hunger", "look", "crew",
                "responsibility", "capability", "vary", "girl", "development", "decorate", "fifty", "fill", "bed",
                "code", "cooperative", "name", "relevant", "skirt", "canadian", "instruct", "bow", "traffic", "casino",
                "author", "pet", "clinical", "lay", "chance", "resident", "produce", "inspector", "black", "heaven",
                "educational", "transit", "emotion", "trim", "hello", "roughly", "originally", "should", "homeless",
                "exclusively", "jewish", "volunteer", "restriction", "wall", "bread", "bother", "presentation",
                "regional", "seemingly", "around", "yesterday", "discourse", "belong", "concert", "dangerous",
                "president", "loan", "sensitive", "relatively", "deliberately", "adolescent", "literature", "guitar",
                "defeat", "movement", "universe", "urban", "sweep", "wage", "success", "allegedly", "ranch", "bill",
                "personality", "impressive", "vocal", "lover", "occasionally", "cry", "rather", "violence", "symptom",
                "undertake", "hostile", "inevitably", "traveler", "theology", "sleeve", "dead", "serving", "back",
                "gently", "meaning", "cup", "tackle", "break", "accommodate", "attorney", "crowded", "senator", "giant",
                "spend", "diverse", "participate", "dog", "dignity", "steam", "acquire", "beauty", "surprisingly",
                "imply", "school", "roof", "wherever", "rally", "prevent", "surprise", "correct", "initially", "effect",
                "laugh", "sigh", "fabric", "compound", "cancer", "butter", "ethnic", "alongside", "grandparent",
                "undermine", "count", "hard", "rental", "none", "comfortable", "element", "highlight", "existence",
                "hold", "underlying", "surgeon", "enable", "rely", "municipal", "execution", "observe", "isolated",
                "solve", "discipline", "outlet", "campaign", "collect", "contribution", "function", "essay", "fraction",
                "automatically", "alive", "silly", "steal", "regular", "department", "defend", "oven", "asian",
                "and/or", "bone", "conscious", "vision", "importantly", "insist", "these", "likely", "less", "awful",
                "mostly", "whenever", "band", "teenager", "civilian", "build", "molecule", "digital", "harvest", "army",
                "lovely", "bend", "coordinator", "bold", "testimony", "roman", "under", "glove", "rich", "teaching",
                "port", "little", "kingdom", "legislator", "association", "persist", "tall", "timing", "thanks",
                "extend", "conference", "carve", "exit", "troubled", "auto", "least", "boyfriend", "equivalent",
                "brutal", "probably", "reception", "recognition", "theater", "defensive", "silence", "print", "stem",
                "away", "item", "return", "coffee", "behalf", "processor", "import", "jail", "scenario", "value",
                "legally", "companion", "following", "street", "expectation", "effective", "blink", "breathe",
                "therefore", "unemployment", "bull", "delay", "label", "mild", "identical", "factor", "indeed",
                "positive", "alternative", "several", "lead", "tribe", "patrol", "half", "lightning", "sculpture",
                "teen", "homeland", "wish", "fair", "eat", "virtue", "implication", "given", "ugly", "empire",
                "without", "ego", "opera", "gathering", "clear", "southeast", "meter", "cable", "particularly", "happy",
                "integrate", "detail", "arrange", "delight", "better", "destination", "colorful", "metal", "wilderness",
                "official", "procedure", "terrain", "ought", "variety", "reason", "dying", "matter", "spanish",
                "sentence", "dot", "merely", "can", "earnings", "online", "provision", "national", "fiscal", "descend",
                "closer", "separate", "documentary", "frequently", "size", "money", "grandchild", "bond", "patent",
                "visual", "team", "organism", "recommendation", "trace", "tree", "wonder", "party", "fluid", "helpful",
                "alien", "planet", "reaction", "drunk", "certain", "hero", "learning", "plain", "soccer", "anxious",
                "southwest", "town", "discount", "inspiration", "steep", "performer", "candy", "bloody", "outcome",
                "supreme", "biology", "strongly", "convey", "distribute", "brief", "idea", "sexuality", "coin",
                "consult", "constitutional", "ms", "intend", "cooperation", "investigate", "administrator", "next",
                "where", "realistic", "northern", "praise", "manager", "christianity", "last", "upon", "full", "rabbit",
                "symbolic", "border", "create", "distant", "regularly", "slice", "while", "glimpse", "prosecutor",
                "attach", "palestinian", "background", "darkness", "suddenly", "body", "withdraw", "jet", "tile",
                "coastal", "sock", "ourselves", "news", "ah", "actor", "comedy", "hockey", "depression", "marine",
                "adviser", "ceremony", "plenty", "serve", "complete", "suggest", "festival", "toward", "protest", "us",
                "drift", "encourage", "tolerate", "coverage", "employer", "obstacle", "uncle", "installation",
                "israeli", "shortly", "vacation", "invasion", "substantial", "alarm", "threaten", "singer", "halfway",
                "scary", "because", "portion", "crack", "loop", "cliff", "franchise", "stay", "imagine", "my", "noon",
                "blast", "harm", "tonight", "pleasant", "insurance", "satisfaction", "transaction", "epidemic",
                "bitter", "grin", "citizen", "remind", "star", "deliver", "guideline", "respondent", "ban", "message",
                "director", "waist", "west", "opposition", "marketplace", "corporate", "unknown", "reliable", "detect",
                "activist", "increase", "straighten", "sad", "raw", "technological", "speak", "someone", "gasoline",
                "wound", "severely", "perspective", "possess", "beyond", "eating", "painting", "give", "engineering",
                "likewise", "nominee", "remaining", "economic", "ceiling", "example", "chunk", "initial", "ship", "de",
                "intent", "forest", "affair", "frown", "staff", "tale", "person", "from", "globe", "practically",
                "concentration", "diet", "twentieth", "fog", "favorable", "champion", "heel", "user", "need", "nasty",
                "recovery", "debut", "limitation", "faint", "wave", "bike", "publication", "apart", "course",
                "independent", "courtroom", "complicated", "option", "final", "illness", "exclusive", "dad", "cool",
                "ritual", "examination", "e-mail", "coalition", "secretary", "avoid", "bit", "recipient", "waste",
                "written", "undergo", "appreciate", "structural", "mysterious", "instant", "medium", "quest",
                "remarkable", "though", "require", "layer", "artifact", "duck", "shine", "fourth", "sector", "flavor",
                "donation", "delicate", "overnight", "tolerance", "two-thirds", "gate", "realize", "encounter", "folk",
                "obtain", "cling", "lamp", "prospect", "presumably", "brick", "achieve", "lock", "listen", "textbook",
                "dimension", "position", "let", "rock", "aware", "contemporary", "annual", "iraqi", "facilitate",
                "shuttle", "diversity", "improvement", "program", "radar", "assert", "fare", "myth", "basement",
                "critical", "frustration", "intact", "hence", "shoe", "nationwide", "anniversary", "rice", "sneak",
                "protocol", "twin", "improve", "reporter", "reality", "fisherman", "criminal", "along", "sexually",
                "spending", "transform", "mystery", "efficient", "furthermore", "radio", "quit", "unfortunately",
                "arrest", "formation", "popular", "vs", "reluctant", "fighter", "earn", "nightmare", "plus", "violate",
                "except", "actual", "spin", "index", "island", "clothes", "random", "immediate", "significance",
                "portfolio", "nor", "verbal", "widespread", "budget", "tribal", "lifestyle", "jacket", "personally",
                "retain", "bare", "mountain", "assembly", "researcher", "elephant", "french", "thirty", "comparable",
                "proposal", "combat", "perfectly", "yes", "unlikely", "operating", "check", "coup", "hike", "purse",
                "virtually", "accident", "save", "beg", "continent", "desperately", "diagnose", "essentially", "eleven",
                "limit", "restore", "implement", "shower", "fan", "entity", "advance", "flash", "increasing",
                "extended", "effort", "assistance", "attend", "expression", "stir", "finish", "celebrity", "risky",
                "imagination", "corporation", "head", "confident", "lend", "food", "slope", "grocery", "independence",
                "victim", "observer", "actress", "negotiation", "yet", "tooth", "acknowledge", "soak", "solely",
                "drink", "father", "satisfy", "cage", "nevertheless", "evolution", "scared", "bake", "village", "peak",
                "judicial", "dancer", "steel", "confront", "mouth", "drum", "fairly", "shout", "funeral", "complex",
                "narrative", "headache", "controversial", "thumb", "previous", "atop", "spine", "however", "fresh",
                "aggression", "dominate", "network", "hair", "economics", "sufficient", "honey", "presidency",
                "difficulty", "attribute", "dust", "cloud", "premium", "translate", "regret", "across", "grow",
                "stimulate", "second", "such", "constraint", "chemistry", "british", "method", "frontier", "besides",
                "acceptable", "relieve", "total", "vegetable", "pop", "coming", "no", "son", "inside", "fact", "boy",
                "curriculum", "uncomfortable", "comprehensive", "tennis", "surrounding", "capital", "portrait",
                "majority", "chocolate", "pipe", "bacteria", "grip", "emergency", "mm-hmm", "below", "career", "cycle",
                "developing", "extra", "locate", "slight", "roll", "error", "end", "quarter", "hospital", "privacy",
                "sample", "aisle", "adjustment", "this", "conscience", "resign", "garlic", "native", "weak",
                "substance", "consist", "suburban", "bottle", "autonomy", "myself", "departure", "monument", "sodium",
                "fraud", "song", "business", "fishing", "happiness", "discourage", "wrong", "disabled", "towards",
                "ecosystem", "nearby", "task", "intervention", "walk", "wake", "inner", "wife", "television",
                "sanction", "historian", "expect", "ours", "housing", "estimate", "confess", "freeze", "card", "shock",
                "assault", "religion", "writing", "consumption", "punch", "both", "typical", "square", "worker",
                "behavioral", "cemetery", "appeal", "replace", "prefer", "including", "college", "proper", "initiative",
                "middle", "so", "than", "lord", "female", "cope", "ability", "wild", "mandate", "confuse", "ownership",
                "prison", "regime", "pattern", "definitely", "small", "short-term", "equation", "result", "immune",
                "straw", "danger", "consideration", "reduction", "writer", "air", "version", "distinguish", "zone",
                "musical", "ministry", "explosion", "industrial", "external", "membership", "concept", "articulate",
                "trash", "supposed", "egg", "brilliant", "society", "subsidy", "investigator", "convert", "limited",
                "install", "electronics", "sharp", "type", "handful", "starter", "uncertainty", "contributor", "dinner",
                "divine", "bishop", "perceive", "blue", "coat", "executive", "producer", "dictate", "social", "all",
                "eastern", "script", "either", "chaos", "broadcast", "smile", "string", "recipe", "collar", "political",
                "anymore", "casualty", "cute", "recognize", "sword", "seek", "arm", "straight", "recession", "data",
                "everybody", "opt", "click", "rare", "stack", "corn", "touch", "salad", "supervisor", "also",
                "contrast", "screw", "embrace", "peel", "fee", "hide", "large", "fantasy", "adventure", "mixed",
                "entrepreneur", "list", "traditional", "bee", "observation", "read", "relative", "process", "battle",
                "technician", "hotel", "rough", "baby", "governor", "muslim", "thousand", "resort", "ideology",
                "intense", "circuit", "airline", "infrastructure", "outsider", "circumstance", "reach", "statute",
                "tension", "win", "hole", "pride", "photographer", "purchase", "cheer", "reputation", "supplier",
                "protein", "might", "cigarette", "ladder", "heat", "skilled", "analysis", "find", "ghost", "works",
                "set", "empty", "worth", "sign", "rate", "output", "rural", "bug", "promote", "operation", "sum",
                "dance", "whereas", "session", "religious", "kick", "brave", "take", "compensation", "south", "current",
                "sale", "building", "adjust", "apartment", "otherwise", "representation", "attendance", "completely",
                "belly", "structure", "disappear", "orientation", "barrel", "hi", "provider", "critic", "garbage",
                "indicator", "her", "afford", "sheet", "arab", "vehicle", "depending", "recording", "best", "widow",
                "too", "engage", "thanksgiving", "respond", "letter", "via", "bible", "concentrate", "possibility",
                "disability", "privately", "orbit", "endorse", "smell", "odds", "storage", "hopefully", "stair", "gain",
                "civic", "banker", "flight", "acid", "liquid", "educate", "temperature", "lung", "publicly", "ensure",
                "protect", "specialize", "growth", "media", "decent", "retreat", "so-called", "action", "barn",
                "bubble", "cluster", "elegant", "contemplate", "mental", "custody", "male", "philosophy", "arrive",
                "innovative", "management", "bury", "restaurant", "industry", "walking", "anyway", "variable", "mirror",
                "fence", "apparently", "interest", "wrap", "text", "like", "declare", "menu", "slap", "lesson",
                "license", "fruit", "pain", "evaluate", "elsewhere", "domestic", "equipment", "ocean", "ten", "exam",
                "glance", "see", "preserve", "partly", "united", "invisible", "juice", "could", "winner", "shot",
                "publisher", "survival", "sphere", "failure", "pitcher", "awake", "those", "conviction", "confidence",
                "annually", "chain", "formal", "diary", "killing", "mineral", "makeup", "theme", "there", "balanced",
                "sales", "persian", "similarity", "atmosphere", "legend", "add", "gray", "satellite", "territory",
                "shark", "die", "spectacular", "attitude", "boss", "pick", "seem", "corridor", "sand", "physical",
                "lab", "prove", "request", "emotional", "spell", "striking", "depth", "league", "vote", "ruin", "god",
                "european", "yard", "innovation", "province", "allegation", "unexpected", "struggle", "catch",
                "perceived", "mess", "capacity", "fail", "predict", "associated", "neither", "sure", "norm", "within",
                "servant", "advanced", "forget", "consumer", "discovery", "booth", "shooting", "astronomer", "advise",
                "legitimate", "realm", "whisper", "define", "airplane", "correctly", "curve", "lane", "totally",
                "involve", "thing", "deficit", "awareness", "sometimes", "yours", "personnel", "deputy", "shame",
                "cloth", "fortune", "persuade", "activity", "constitute", "become", "bullet", "unusual", "lots",
                "bonus", "hostage", "interested", "softly", "workout", "plea", "mass", "cook", "ecological", "grasp",
                "pass", "necessarily", "offender", "fur", "belief", "lemon", "fiber", "healthy", "tag", "importance",
                "known", "modern", "streak", "re", "spouse", "badly", "planner", "aide", "mrs", "genetic",
                "statistical", "play", "pork", "remember", "dozen", "grass", "penalty", "congress", "practitioner",
                "guilt", "acceptance", "chill", "edition", "connection", "may", "in", "advocate", "construct",
                "assemble", "hunter", "apologize", "whip", "wheat", "greek", "month", "scholar", "drama", "trunk",
                "slam", "refuge", "novel", "selection", "blessing", "horror", "damn", "poor", "purple", "defender",
                "vanish", "bedroom", "visible", "accent", "punish", "criteria", "tea", "must", "dissolve", "very",
                "yeah", "dynamic", "cartoon", "exploit", "t-shirt", "she", "progressive", "would", "interact", "terms",
                "parking", "pan", "migration", "victory", "discover", "interrupt", "managing", "politically",
                "flexibility", "indigenous", "design", "revolution", "midst", "parent", "them", "twist", "military",
                "permanent", "service", "artificial", "harassment", "pale", "excuse", "shape", "racism", "cast",
                "weekly", "flip", "plate", "mutual", "severe", "bathroom", "council", "doctrine", "distance", "me",
                "milk", "breath", "peasant", "date", "mate", "bell", "decide", "sing", "percentage", "permit",
                "tremendous", "winter", "class", "show", "fiction", "jewelry", "golf", "library", "versus", "extent",
                "anxiety", "framework", "pit", "driving", "medication", "soviet", "celebrate", "sofa", "sky", "being",
                "environment", "opposite", "sophisticated", "skip", "passage", "supply", "swear", "counseling",
                "wealth", "anger", "reporting", "contract", "reject", "adapt", "beam", "render", "enforce", "speech",
                "possibly", "openly", "important", "outdoor", "warrior", "soap", "horn", "it", "bush", "change", "or",
                "obvious", "cut", "sort", "creative", "painter", "database", "anticipate", "log", "according", "boom",
                "pad", "pleased", "shadow", "chicken", "stance", "description", "devil", "ultimately", "overall",
                "slide", "battery", "open", "passenger", "tank", "riot", "patience", "trait", "prayer", "treat",
                "laughter", "article", "feeling", "okay", "experiment", "burn", "general", "setting", "ash", "meat",
                "poverty", "information", "lifetime", "corner", "quote", "american", "drop", "internet", "will",
                "deadline", "eligible", "verdict", "unfold", "appoint", "historic", "initiate", "still", "line",
                "grave", "run", "scholarship", "forty", "surely", "door", "assist", "fever", "tropical", "african",
                "introduction", "fight", "accompany", "dramatically", "heal", "good", "offering", "desire", "word",
                "presence", "someday", "inmate", "dose", "scope", "summit", "minority", "injury", "punishment",
                "balance", "pollution", "have", "cab", "regulator", "pasta", "planning", "newspaper", "downtown",
                "billion", "mine", "spill", "ill", "stuff", "sweet", "income", "competitive", "ancient", "reply",
                "people", "ankle", "irish", "conversion", "trail", "represent", "face", "gesture", "emission",
                "predator", "officially", "engagement", "nothing", "content", "accept", "incredible", "protection",
                "captain", "twenty", "apple", "move", "arrangement", "forehead", "painful", "fat", "gifted", "shelf",
                "fist", "impossible", "institutional", "cattle", "anywhere", "area", "farmer", "moon", "pair",
                "nomination", "maintain", "characterize", "delivery", "disaster", "thread", "spirit", "surround",
                "guidance", "strain", "ceo", "professional", "whole", "safety", "flexible", "habitat", "rid", "yield",
                "unprecedented", "isolate", "density", "justify", "increased", "witness", "meantime", "telephone",
                "angle", "pray", "your", "disappointed", "palace", "pepper", "reveal", "simply", "propose",
                "missionary", "lobby", "trainer", "infant", "legislative", "nuclear", "narrow", "approval", "nervous",
                "inquiry", "minor", "instructor", "recommend", "beginning", "investigation", "concrete", "collective",
                "refrigerator", "lip", "tomorrow", "dough", "enjoy", "trading", "everything", "athletic", "tradition",
                "dumb", "interesting", "conceive", "conflict", "plead", "rod", "dedicate", "export", "electricity",
                "ignore", "personal", "wash", "steadily", "northeast", "truck", "translation", "feel", "ok", "regain",
                "partner", "art", "marker", "reminder", "ease", "logic", "agreement", "newly", "pill", "hunt", "shut",
                "leave", "climate", "tightly", "time", "use", "variation", "hill", "civilization", "combination",
                "intensity", "ie", "russian", "sorry", "light", "stop", "notebook", "attractive", "sixth", "able",
                "store", "mushroom", "classify", "queen", "free", "manner", "democrat", "minimal", "soon", "sense",
                "businessman", "temporary", "politics", "property", "spark", "million", "write", "runner", "seller",
                "dip", "artist", "voluntary", "subtle", "execute", "smoke", "slip", "marketing", "everyone",
                "manipulate", "disturb", "fundamental", "device", "herb", "arise", "accessible", "noise", "bounce",
                "powerful", "blade", "day", "toss", "bear", "indicate", "agenda", "colony", "consider", "shoulder",
                "trust", "late", "regulate", "assume", "object", "by", "ago", "image", "loyal", "feed", "sunny",
                "cooking", "significant", "opening", "beat", "long", "asleep", "denial", "discuss", "hear", "transfer",
                "pickup", "discrimination", "report", "insight", "himself", "stadium", "phone", "pace", "shop",
                "obligation", "safely", "terrible", "human", "conversation", "pond", "condemn", "undergraduate",
                "youngster", "shorts", "faith", "await", "young", "negative", "concerned", "qualify", "university",
                "unfair", "angel", "allow", "ask", "segment", "dirty", "factory", "always", "cash", "somebody",
                "audience", "athlete", "elaborate", "clearly", "squeeze", "hire", "existing", "receive", "apparent",
                "mechanical", "sandwich", "bench", "benefit", "immigrant", "distinct", "exhaust", "drag", "privilege",
                "serious", "fashion", "ambitious", "study", "ad", "whoever", "stroke", "educator", "bunch", "first",
                "communicate", "moment", "education", "primary", "fragile", "accounting", "functional", "faster",
                "sport", "guilty", "hormone", "advice", "flying", "objection", "bottom", "put", "squad", "excited",
                "worldwide", "file", "shall", "behavior", "genre", "mortgage", "early", "mechanic", "great", "nod",
                "own", "maintenance", "chin", "unity", "load", "junior", "miracle", "wind", "currency", "that",
                "strong", "doll", "owe", "terrorism", "signature", "shareholder", "automobile", "jungle", "oxygen",
                "wheelchair", "wrist", "pant", "buddy", "join", "fierce", "soil", "obviously", "upstairs", "neck",
                "revolutionary", "pot", "charge", "lean", "page", "enforcement", "cross", "site", "unable", "refugee",
                "high", "format", "broad", "inherent", "flood", "wire", "scale", "placement", "advantage", "abuse",
                "long-term", "oil", "against", "hip", "cabinet", "ideological", "forum", "solar", "insect", "instance",
                "warehouse", "shell", "hungry", "classic", "active", "promising", "ribbon", "derive", "salary", "enter",
                "outline", "swimming", "brush", "addition", "nature", "pump", "leader", "spare", "instinct",
                "disappointment", "river", "vaccine", "crowd", "distribution", "global", "community", "window",
                "treasure", "side", "stomach", "major", "green", "again", "publish", "scratch", "transportation",
                "phenomenon", "mayor", "utilize", "office", "investor", "valuable", "since", "arrow", "step", "concern",
                "motivate", "press", "century", "theory", "smooth", "unhappy", "clay", "weakness", "angry", "sweat",
                "rape", "shift", "instantly", "admission", "division", "productivity", "bias", "equal", "trauma",
                "award", "suffer", "spite", "latter", "continue", "shit", "largely", "truly", "favorite", "degree",
                "dynamics", "trailer", "county", "yourself", "lecture", "potato", "friend", "relax", "world", "fit",
                "reserve", "exploration", "thigh", "point", "direct", "cart", "subsequent", "special", "policeman",
                "attract", "average", "order", "therapy", "landing", "interval", "journalism", "summary", "living",
                "surprised", "premise", "pursue", "correspondent", "investment", "he", "alike", "connect", "nobody",
                "sexy", "principle", "fleet", "pm", "pound", "near", "question", "stupid", "nearly", "accountability",
                "domain", "organized", "divide", "additional", "rack", "contractor", "occupation", "invade", "japanese",
                "helmet", "gene", "match", "toy", "puzzle", "trouble", "rider", "silk", "metaphor", "simple", "freedom",
                "daily", "room", "rhetoric", "many", "doctor", "shoot", "disc", "snake", "flee", "islamic", "enough",
                "soldier", "fantastic", "revelation", "desert", "upset", "definition", "our", "elder", "owner",
                "lawyer", "perhaps", "psychology", "jurisdiction", "recall", "yell", "bolt", "soft", "case", "palm",
                "continued", "differently", "pay", "christian", "literary", "pursuit", "assistant", "customer",
                "organizational", "continuous", "exactly", "decade", "compare", "lack", "shallow", "chair", "muscle",
                "talk", "harmony", "any", "cotton", "bride", "shelter", "honestly", "therapist", "intelligence",
                "appreciation", "draw", "advertising", "whale", "practical", "destroy", "status", "enhance", "born",
                "garden", "residence", "fix", "dispute", "devote", "conventional", "ideal", "knee", "deep", "thank",
                "welcome", "weird", "interfere", "handle", "utility", "beer", "o'clock", "evaluation", "commercial",
                "minister", "loyalty", "shore", "shirt", "divorce", "damage", "vacuum", "significantly", "employee",
                "sound", "parade", "greet", "launch", "girlfriend", "meaningful", "never", "injure", "the", "murder",
                "mix", "weaken", "sit", "swell", "gut", "respectively", "we", "command", "counsel", "know", "frustrate",
                "candidate", "fate", "constantly", "miss", "sponsor", "impulse", "you", "journalist", "elect", "bulb",
                "bet", "capture", "disorder", "necessary", "hurricane", "computer", "boundary", "till", "table",
                "tragic", "attempt", "deck", "banana", "mathematics", "german", "decline", "ambassador", "but", "view",
                "unit", "overwhelm", "true", "intimate", "child", "consequence", "toilet", "thereby", "poem", "provide",
                "organization", "museum", "bless", "similarly", "rhythm", "flower", "basis", "dilemma", "photography",
                "false", "needle", "operator", "coach", "wedding", "terrific", "transition", "exist", "invention",
                "not", "then", "pretty", "come", "beast", "beneath", "single", "melt", "recently", "herself", "aid",
                "hit", "difficult", "tour", "stimulus", "test", "suspicious", "fuel", "their", "foundation", "hate",
                "lens", "attraction", "liability", "alter", "bath", "provoke", "diplomatic", "supportive", "scientist",
                "physics", "buyer", "compliance", "diagnosis", "some", "buck", "attention", "superior", "everywhere",
                "hearing", "breeze", "dirt", "prime", "tunnel", "faculty", "olympic", "truth", "hand", "korean", "ski",
                "nutrient", "replacement", "modest", "filter", "specify", "relief", "normal", "northwest", "wipe",
                "burden", "consensus", "overlook", "am", "origin", "missing", "amazing", "training", "hypothesis",
                "signal", "hour", "architect", "bite", "section", "whom", "abroad", "slave", "tighten", "stability",
                "breakfast", "box", "couple", "birthday", "series", "wine", "spectrum", "admit", "emerge", "motor",
                "marble", "poet", "gym", "afternoon", "keep", "mother", "speculate", "loose", "outfit", "speed",
                "fifth", "mainstream", "indication", "poll", "rational", "center", "considerably", "differ", "football",
                "attack", "opposed", "bank", "offensive", "integrated", "grape", "western", "appearance", "tumor",
                "greatest", "passion", "secondary", "conservation", "contribute", "edit", "incentive", "invent",
                "criticism", "something", "neat", "software", "six", "trend", "juror", "chief", "rifle", "treaty",
                "candle", "precious", "pocket", "east", "oral", "repair", "experienced", "exposure", "retire",
                "transformation", "mean", "stock", "suite", "whose", "his", "blind", "well-being", "used", "cognitive",
                "isolation", "meet", "radical", "romance", "gift", "legislation", "defense", "belt", "vessel",
                "happily", "hazard", "dump", "pro", "accurate", "phrase", "citizenship", "sheer", "before", "precise",
                "afraid", "cue", "changing", "developmental", "strict", "two", "explore", "psychologist", "deal",
                "wealthy", "every", "curtain", "brain", "announce", "huge", "firmly", "explain", "ruling", "bean",
                "into", "olympics", "liberal", "pension", "present", "rival", "register", "rush", "vulnerable",
                "scatter", "conspiracy", "glass", "specialty", "cottage", "full-time", "others", "plane", "carrot",
                "steak", "screening", "sauce", "switch", "peanut", "chairman", "follow", "really", "joint", "socially",
                "land", "flow", "welfare", "dense", "barrier", "accusation", "rub", "skin", "ridiculous", "wonderful",
                "urge", "life", "pole", "cake", "jaw", "mechanism", "calculate", "state", "pressure", "pizza",
                "coordinate", "illegal", "adoption", "emotionally", "validity", "international", "fortunately",
                "legacy", "seat", "energy", "abandon", "horrible", "dress", "solid", "park", "tight", "game", "virtual",
                "brake", "naked", "lawmaker", "exclude", "secure", "throw", "availability", "designer", "automatic",
                "consistent", "bucket", "substantially", "prevention", "grade", "survivor", "troop", "retail",
                "individual", "assure", "book", "excessive", "fifteen", "preparation", "confirm", "prosecution", "butt",
                "repeatedly", "record", "pilot", "decision", "absence", "household", "fucking", "film", "kind",
                "speaker", "psychological", "bureau", "gaze", "ticket", "alliance", "at", "identification", "fighting",
                "entitle", "grandfather", "safe", "affect", "particular", "price", "equality", "tough", "cave",
                "preach", "instruction", "old", "teenage", "reward", "mom", "basketball", "taste", "fall", "latin",
                "pull", "track", "equally", "mortality", "sink", "deadly", "expected", "go", "aspect", "confusion",
                "exchange", "terror", "magnetic", "friendship", "relationship", "knife", "bomb", "man", "prevail",
                "slowly", "sugar", "interview", "round", "particle", "believe", "sell", "symbol", "ally", "mail",
                "gentleman", "somewhere", "threshold", "quality", "push", "during", "pin", "missile", "suit",
                "frequent", "lose", "counselor", "chest", "later", "prediction", "medicine", "fund", "plan", "exhibit",
                "contend", "category", "perception", "curious", "until", "assumption", "jury", "confession",
                "touchdown", "shy", "slavery", "helicopter", "knock", "carbon", "dna", "parish", "comfort", "commodity",
                "frequency", "galaxy", "hidden", "crush", "convict", "how", "distract", "explanation", "lawsuit",
                "title", "joke", "maybe", "achievement", "electrical", "which", "genuine", "uncover", "generally",
                "thoroughly", "diamond", "representative", "foot", "old-fashioned", "pastor", "weather", "impact",
                "web", "shrimp", "texture", "holiday", "determine", "suspend", "identify", "statistics", "vitamin",
                "tend", "expand", "shortage", "stress", "space", "video", "scream", "vertical", "past", "editor",
                "branch", "govern", "shared", "trigger", "neighbor", "expense", "numerous", "jew", "harsh", "role",
                "tide", "lightly", "goat", "super", "earth", "path", "carry", "creativity", "seventh", "member",
                "cause", "remove", "scheme", "king", "foreigner", "haul", "mode", "driveway", "drawer", "rebel",
                "selected", "incredibly", "demonstration", "wisdom", "specialist", "slot", "down", "fade", "turn",
                "flesh", "partnership", "left", "interior", "sympathy", "eventually", "protective", "forward",
                "bankruptcy", "physically", "liberty", "eliminate", "envision", "naturally", "unlike", "only", "happen",
                "for", "today", "classical", "rolling", "when", "crash", "simultaneously", "pie", "exact", "sidewalk",
                "devastating", "unite", "despite", "technique", "monster", "passing", "more", "phase", "anything",
                "homework", "seven", "understand", "visit", "ambition", "enthusiasm", "medal", "frame", "adult",
                "basically", "system", "almost", "cocaine", "artistic", "i", "assign", "please", "cream", "smart",
                "consume", "likelihood", "laser", "player", "trip", "donor", "care", "form", "well", "direction",
                "suck", "display", "counter", "stream", "professor", "abstract", "gas", "toll", "finally", "withdrawal",
                "briefly", "corruption", "trial", "talented", "added", "graduation", "eyebrow", "movie", "ground",
                "snow", "about", "identity", "lake", "bring", "jump", "disclose", "rail", "wear", "nose", "patron",
                "brother", "refer", "exciting", "cure", "stiff", "honor", "cold", "pour", "concede", "consistently",
                "memory", "monitor", "voting", "skull", "panel", "merchant", "throat", "talent", "outside", "even",
                "racial", "heritage", "dutch", "specific", "rain", "temple", "generous", "receiver", "organize", "sex",
                "toxic", "depart", "universal", "emerging", "draft", "say", "four", "chip", "bowl", "tax", "dish",
                "upper", "incident", "most", "fully", "warning", "fascinating", "gear", "mouse", "doorway", "funny",
                "if", "recent", "essence", "snap", "interpretation", "integrity", "widely", "depressed", "convention",
                "powder", "bad", "consecutive", "destruction", "workplace", "trick", "post", "depict", "ballot",
                "often", "african-american", "year", "bar", "expedition", "sue", "willing", "circle", "now", "entire",
                "diminish", "normally", "prohibit", "preference", "deem", "warmth", "night", "monkey", "suburb",
                "complaint", "and", "power", "union", "context", "aluminum", "royal", "somehow", "tail", "commit",
                "balloon", "projection", "hardware", "each", "express", "fork", "absorb", "meeting", "inherit",
                "various", "spring", "carbohydrate", "front", "absolute", "strengthen", "continuing", "summer", "youth",
                "hardly", "aim", "italian", "health", "expert", "basic", "airport", "station", "mansion", "piano",
                "viewer", "technology", "clue", "select", "occasion", "spray", "proclaim", "chart", "assess", "rose",
                "optimistic", "romantic", "choose", "retired", "mind", "residential", "plastic", "midnight", "behind",
                "musician", "beach", "sleep", "history", "immediately", "violent", "answer", "elite", "weight", "big",
                "priority", "leaf", "consciousness", "dealer", "demographic", "be", "container", "holy", "limb",
                "death", "statue", "help", "silent", "cruise", "part", "cholesterol", "neighboring", "terribly",
                "impose", "who", "justice", "thin", "effectiveness", "fellow", "guest", "counterpart", "patch", "court",
                "seize", "cost", "found", "everyday", "flat", "graduate", "mount", "flame", "float", "biological",
                "entry", "bridge", "composition", "shake", "survive", "opportunity", "dream", "standard", "orange",
                "portray", "experimental", "commissioner", "aesthetic", "blow", "greatly", "required", "prescription",
                "equity", "taxpayer", "different", "wolf", "throughout", "way", "infection", "stable", "usual",
                "motive", "tap", "typically", "commission", "porch", "valley", "provided", "place", "running", "figure",
                "rumor", "collapse", "contain", "lift", "finger", "close", "formula", "previously", "echo", "week",
                "performance", "endless", "as", "salt", "childhood", "family", "evolve", "rear", "deposit", "reform",
                "well-known", "credit", "laboratory", "three", "proceed", "entertainment", "surface", "uncertain",
                "else", "usually", "drill", "thrive", "surprising", "principal", "alley", "eager", "car", "camera",
                "pig", "strike", "chew", "landscape", "bronze", "freely", "send", "nonetheless", "luck", "improved",
                "reflect", "federal", "supporter", "proportion", "itself", "forgive", "fire", "cheat", "outstanding",
                "story", "broker", "pool", "suppose", "ancestor", "transmission", "inspire", "favor", "frankly",
                "transport", "leadership", "spread", "inspection", "tourism", "gradually", "potential", "scientific",
                "confrontation", "photograph", "incorporate", "accelerate", "hallway", "chef", "philosophical",
                "massive", "clock", "slow", "prior", "sometime", "mainly", "establish", "subject", "architecture",
                "hundred", "compete", "react", "charity", "panic", "grand", "length", "handsome", "manage", "seriously",
                "blend", "worry", "music", "wide", "spit", "drive", "describe", "shrink", "elderly", "regardless",
                "appear", "stumble", "rage", "prisoner", "mentally", "oppose", "supposedly", "authorize", "fatal",
                "fault", "resolve", "soften", "historically", "enact", "railroad", "problem", "maker", "occasional",
                "shove", "repeat", "remark", "onto", "master", "sacrifice", "sake", "sin", "hot", "key", "virus", "tip",
                "channel", "job", "pack", "instrument", "deeply", "certainly", "habit", "colonial", "real", "character",
                "hug", "estimated", "insert", "gravity", "potentially", "appointment", "sibling", "admire", "auction",
                "rim", "crazy", "scramble", "stare", "consequently", "offense", "rarely", "rebuild", "watch",
                "carefully", "teammate", "sensation", "combined", "company", "cabin", "priest", "ever", "scene", "odd",
                "butterfly", "style", "mill", "saving", "fixed", "n't", "a", "strictly", "hint", "inform", "evidence",
                "cultural", "standing", "plot", "minimize", "pleasure", "weigh", "testify", "examine", "garage",
                "transmit", "hey", "monthly", "cousin", "hurt", "ultimate", "try", "reportedly", "sister", "remain",
                "regard", "oak", "uniform", "exotic", "other", "strip", "seal", "pink", "questionnaire", "momentum",
                "swing", "fewer", "essential", "legislature", "intellectual", "testing", "peaceful", "blood",
                "distinction", "judge", "root", "theological", "ordinary", "lawn", "spokesman", "profile", "debt",
                "experience", "democratic", "boot", "steer", "rehabilitation", "reinforce", "detailed", "agency",
                "fear", "useful", "student", "self", "capable", "pillow", "mark", "enemy", "picture", "landmark",
                "climb", "developer", "rope", "seldom", "resource", "syndrome", "amid", "travel", "commander",
                "product", "lately", "original", "peer", "treatment", "live", "tent", "love", "minute", "duty",
                "estate", "charm", "block", "peace", "abortion", "kill", "lucky", "bicycle", "culture", "apply",
                "brand", "control", "prepare", "publicity", "eight", "voice", "map", "lid", "pose", "drown", "disagree",
                "illusion", "soup", "sentiment", "clerk", "on", "neighborhood", "neutral", "unique", "support", "tube",
                "engineer", "nurse", "engine", "competition", "joy", "introduce", "pretend", "resistance",
                "specifically", "fast", "mr", "reduce", "tender", "processing", "entirely", "perfect", "arrival", "sir",
                "journey", "respect", "economist", "husband", "do", "boost", "requirement", "physician", "make",
                "nation", "grateful", "studio", "tiny", "wildlife", "agree", "dried", "carpet", "thought", "readily",
                "due", "comparison", "birth", "extraordinary", "commitment", "dare", "organ", "one", "chapter",
                "crystal", "innocent", "effectively", "especially", "campus", "season", "district", "involved", "bulk",
                "tool", "cancel", "tournament", "sensitivity", "acquisition", "honest", "custom", "relate", "resume",
                "sovereignty", "preliminary", "closed", "employ", "establishment", "sweater", "possible", "lady",
                "civil", "reflection", "understanding", "mission", "permission", "conservative", "access", "far",
                "hall", "paint", "warn", "boil", "multiple", "currently", "leading", "route", "war", "charter",
                "private", "bind", "boring", "promise", "fly", "settlement", "adequate", "feminist", "senior", "hat",
                "security", "conception", "impression", "stranger", "over", "album", "related", "precisely", "common",
                "right", "sheep", "properly", "city", "weed", "intelligent", "credibility", "magnitude", "focus",
                "material", "spy", "behave", "out", "contact", "account", "gap", "refuse", "paper", "convenience",
                "excellent", "coal", "swim", "dependent", "dry", "age", "ha", "reference", "topic", "woman",
                "conclusion", "population", "double", "race", "swallow", "ridge", "couch", "invitation", "desk",
                "quantity", "model", "chamber", "bird", "tourist", "finding", "quite", "christmas", "pen", "teach",
                "overcome", "towel", "suspect", "lighting", "magic", "twice", "vendor", "responsible", "blanket",
                "strength", "accuracy", "central", "guard", "start", "country", "they", "backyard", "include", "warm",
                "explode", "anyone", "main", "interpret", "analyst", "catalog", "tray", "raise", "discussion",
                "elevator", "integration", "guarantee", "labor", "quickly", "english", "ingredient", "routine", "adopt",
                "possession", "rent", "up", "robot", "low", "financial", "tragedy", "humanity", "purpose", "schedule",
                "evil", "jar", "wooden", "progress", "moreover", "law", "icon", "eye", "shopping", "march", "seed",
                "seminar", "fragment", "fun", "already", "compel", "together", "math", "here", "challenge", "golden",
                "foreign", "invest", "demonstrate", "share", "measure", "poke", "ice", "sprinkle", "stand", "anybody",
                "pencil", "gross", "listener", "announcement", "tape", "plant", "hell", "rest", "drinking", "casual",
                "chemical", "chop", "costume", "response", "successful", "ongoing", "authority", "illustrate",
                "horizon", "comply", "deny", "regarding", "practice", "democracy", "depend", "broken", "approximately",
                "margin", "get", "think", "much", "goal", "risk", "clinic", "proof", "arena", "stage", "base",
                "violation", "enroll", "wing", "alone", "search", "meanwhile", "of", "meal", "rise", "easily",
                "statement", "grab", "headquarters", "quietly", "manufacturing", "accomplish", "policy", "impress",
                "closest", "debate", "boast", "involvement", "ride", "rubber", "expose", "spot", "suitable", "marriage",
                "detective", "poetry", "number", "survey", "wise", "decrease", "ball", "research", "leap", "science",
                "excitement", "considerable", "correlation", "inflation", "ethical", "merit", "efficiency", "nail",
                "defendant", "former", "prominent", "dancing", "retirement", "cease", "array", "boat", "natural",
                "barely", "five", "shed", "profit", "kneel", "feedback", "disk", "local", "blond", "distinctive",
                "cheek", "furniture", "platform", "heavily", "drug", "catholic", "off", "willingness", "successfully",
                "mutter", "review", "heart", "aunt", "associate", "theoretical", "funding", "self-esteem", "grief",
                "breathing", "maximum", "sexual", "cuban", "suspicion", "determination", "constitution", "chronic",
                "guide", "genius", "aids", "compelling", "above", "weave", "third", "shrug", "creature", "driver",
                "secular", "cheap", "eighth", "fitness", "period", "white", "revenue", "promotion", "minimum", "farm",
                "glory", "sack", "tire", "workshop", "informal", "metropolitan", "condition", "pile", "twelve",
                "supermarket", "tell", "consultant", "bus", "weekend", "directly", "entrance", "inventory", "evening",
                "ring", "combine", "cat", "dig", "objective", "quarterback", "armed", "enormous", "celebration",
                "anonymous", "agricultural", "tie", "headline", "spoon", "friendly", "necessity", "encouraging", "copy",
                "kitchen", "spiritual", "document", "calculation", " ", "sharply", "project", "sustain", "release",
                "worried", "cap", "working", "weapon", "famous", "tissue", "venture", "sole", "scent", "lunch",
                "thinking", "inevitable", "ratio", "dawn", "drain", "rib", "humor", "recruit", "nice", "frozen",
                "one-third", "oh", "succeed", "grant", "communication", "pause", "language", "forth", "him", "forbid",
                "public", "reasonable", "beef", "complain", "lonely", "administer", "species", "dark", "primarily",
                "construction", "historical", "formerly", "tune", "terrorist", "prompt", "convinced", "level", "just",
                "between", "influential", "tv", "drawing", "suicide", "themselves", "ahead", "rating", "grain", "stake",
                "gold", "aggressive", "nonprofit", "tactic", "technical", "reservation", "analyze", "opponent", "wood",
                "telescope", "institution", "economy", "emphasize", "craft", "somewhat", "disturbing", "speculation",
                "measurement", "electronic", "mention", "lion", "patient", "finance", "logical", "assignment",
                "banking", "closely", "generation", "moderate", "disease", "facility", "agent", "equip", "courage",
                "bright", "fish", "agriculture", "event", "package", "per", "islam", "with", "gentle", "short", "wow",
                "championship", "water", "expensive", "conduct", "dining", "negotiate", "freshman", "kid", "profession",
                "production", "deploy", "bay", "resolution", "teacher", "calm", "lot", "notice", "fame", "ironically",
                "buy", "diplomat", "biography", "cop", "alleged", "uh", "closet", "oversee", "starting", "rank",
                "tower", "motion", "characteristic", "volume", "curiosity", "elementary", "feature", "lower",
                "absolutely", "immigration", "fatigue", "button", "gun", "highly", "its", "retailer", "claim", "basket",
                "republican", "red", "glad", "trap", "reader", "tobacco", "baseball", "link", "issue", "indian",
                "carrier", "outer", "envelope", "hope", "dominant", "horse", "gay", "submit", "begin", "aircraft",
                "highway", "participant", "scandal", "sequence", "mad", "profound", "hesitate", "employment",
                "assessment", "exception", "instructional", "productive", "radiation", "skill", "bombing", "classroom",
                "new", "burning", "era", "creation", "ready", "officer", "partial", "tone", "flag", "manufacturer",
                "mere", "wagon", "tear", "magazine", "approve", "gallery", "senate", "range", "soar", "republic",
                "force", "rip", "perform", "heavy", "net", "vast", "split", "stove", "nerve", "strange", "irony",
                "compose", "mood", "client", "reverse", "loud", "the", "cloak"}


def flatten(input_list):
    '''
    A function to flatten complex list.
    :param input_list: The list to be flatten
    :return: the flattened list.
    '''

    flat_list = []
    for i in input_list:
        if type(i) == list:
            flat_list += flatten(i)
        else:
            flat_list += [i]

    return flat_list


# def common_words(path):
#     '''
#     A function to read-in the top common words from external .txt document.
#     :param path: The path where the common words info is stored.
#     :return: A set of the top common words.
#     '''
#
#     with codecs.open(path) as f:
#         words = f.read()
#         words = json.loads(words)
#
#     return set(common_words)


def read_text(novel_folder, novel_name):
    '''
    This function reads the text into python from a text file.
    When you read in your own file, replace 'corpus/hp1.txt' with the path
    to your file.
    '''
    with open(f"{novel_folder}/{novel_name}", 'r') as f:
        book = f.read().replace('\r', ' ').replace('\n', ' ').replace("\'", "'")
    return book


def name_entity_recognition(nlp_func, sentence, labels=None):
    '''
    A function to retrieve name entities in a sentence.
    :param sentence: the sentence to retrieve names from.
    :return: a name entity list of the sentence.
    '''
    flag = False
    if labels is None:
        flag = True
        labels = ['PERSON', 'ORG']
    doc = nlp_func(sentence)
    # retrieve person and organization's name from the sentence
    name_entity = [x for x in doc.ents if x.label_ in labels]
    # convert all names to lowercase and remove 's in names
    name_entity = [str(x).lower().replace("'s", "") for x in name_entity]
    # split names into single words ('Harry Potter' -> ['Harry', 'Potter'])
    if flag:
        name_entity = [x.split(' ') for x in name_entity]
        # flatten the name list
        name_entity = flatten(name_entity)

    # remove name words that are less than 3 letters to raise recognition accuracy
    name_entity = [x for x in name_entity if len(x) >= 3]
    # remove name words that are in the set of 4000 common words
    name_entity = [x for x in name_entity if x not in common_words]

    return name_entity


def iterative_NER(nlp_func, sentence_list, threshold_rate=0.0005):
    '''
    A function to execute the name entity recognition function iteratively. The purpose of this
    function is to recognise all the important names while reducing recognition errors.
    :param sentence_list: the list of sentences from the novel
    :param threshold_rate: the per sentence frequency threshold, if a word's frequency is lower than this
    threshold, it would be removed from the list because there might be recognition errors.
    :return: a non-duplicate list of names in the novel.
    '''

    output = []
    for i in sentence_list:
        name_list = name_entity_recognition(nlp_func, i)
        if name_list != []:
            output.append(name_list)
    output = flatten(output)
    from collections import Counter
    output = Counter(output)
    output = [x for x in output if output[x] >= threshold_rate * len(sentence_list)]

    return output


def process_sentences(funcs, sentence_list, threshold_rate=0.0005):
    '''
    A function to execute the name entity recognition function iteratively. The purpose of this
    function is to recognise all the important names while reducing recognition errors.
    :param funcs: dict {'func name': (func, labels)}
    :param sentence_list: the list of sentences from the novel
    :param threshold_rate: the per sentence frequency threshold, if a word's frequency is lower than this
    threshold, it would be removed from the list because there might be recognition errors.
    :return: a non-duplicate list of names in the novel.
    '''
    afinn = Afinn()
    sentiment_score = []
    
    output = {func: [] for func in funcs}

    print("Iterating the sentences:")
    start_time = datetime.now()
    percents_prints = 5
    chunk_size = round(len(sentence_list)/100) * percents_prints
    for index, sentence in enumerate(sentence_list):

        if index % chunk_size == 0:
            print("Processed {}% of the sentences. ({} seconds passed)".format(round(index/chunk_size)*percents_prints, (datetime.now()-start_time).seconds))

        sentiment_score.append(afinn.score(sentence))

        for func in funcs:
            name_list = name_entity_recognition(funcs[func][0], sentence, funcs[func][1])

            if name_list != []:
                output[func].append(name_list)

    align_rate = np.sum(sentiment_score) / len(np.nonzero(sentiment_score)[0]) * -2
    print("Align rate is {}.".format(align_rate))

    for func in funcs:
        output[func] = flatten(output[func])
        output[func] = Counter(output[func])
        output[func] = [x for x in output[func] if output[func][x] >= threshold_rate * len(sentence_list)]
        print("Number of words found in {}: {}.".format(func, len(output[func])))

    return output, align_rate


def top_names(name_list, novel, top_num=20):
    '''
    A function to return the top names in a novel and their frequencies.
    :param name_list: the non-duplicate list of names of a novel.
    :param novel: the novel text.
    :param top_num: the number of names the function finally output.
    :return: the list of top names and the list of top names' frequency.
    '''

    vect = CountVectorizer(vocabulary=name_list, stop_words='english')
    name_frequency = vect.fit_transform([novel.lower()])
    name_frequency = pd.DataFrame(name_frequency.toarray(), columns=vect.get_feature_names())
    name_frequency = name_frequency.T
    name_frequency = name_frequency.sort_values(by=0, ascending=False)
    name_frequency = name_frequency[0:top_num]
    names = list(name_frequency.index)
    name_frequency = list(name_frequency[0])

    return name_frequency, names


def calculate_matrix(name_list, sentence_list, align_rate):
    '''
    Function to calculate the co-occurrence matrix and sentiment matrix among all the top characters
    :param name_list: the list of names of the top characters in the novel.
    :param sentence_list: the list of sentences in the novel.
    :param align_rate: the sentiment alignment rate to align the sentiment score between characters due to the writing style of
    the author. Every co-occurrence will lead to an increase or decrease of one unit of align_rate.
    :return: the co-occurrence matrix and sentiment matrix.
    '''
    # calculate a sentiment score for each sentence in the novel
    afinn = Afinn()
    sentiment_score = [afinn.score(x) for x in sentence_list]
    # calculate occurrence matrix and sentiment matrix among the top characters
    name_vect = CountVectorizer(vocabulary=name_list, binary=True)
    occurrence_each_sentence = name_vect.fit_transform(sentence_list).toarray()
    cooccurrence_matrix = np.dot(occurrence_each_sentence.T, occurrence_each_sentence)
    sentiment_matrix = np.dot(occurrence_each_sentence.T, (occurrence_each_sentence.T * sentiment_score).T)
    sentiment_matrix += align_rate * cooccurrence_matrix
    
    cooccurrence_matrix = np.tril(cooccurrence_matrix)
    # diagonals of the matrices are set to be 0 (co-occurrence of name itself is meaningless)
    shape = cooccurrence_matrix.shape[0]
    cooccurrence_matrix[[range(shape)], [range(shape)]] = 0

    sentiment_matrix = np.tril(sentiment_matrix)
    sentiment_matrix[[range(shape)], [range(shape)]] = 0

    return cooccurrence_matrix, sentiment_matrix


def matrix_to_edge_list(matrix, mode, name_list):
    '''
    Function to convert matrix (co-occurrence/sentiment) to edge list of the network graph. It determines the
    weight and color of the edges in the network graph.
    :param matrix: co-occurrence matrix or sentiment matrix.
    :param mode: 'co-occurrence' or 'sentiment'
    :param name_list: the list of names of the top characters in the novel.
    :return: the edge list with weight and color param.
    '''
    edge_list = []
    shape = matrix.shape[0]
    lower_tri_loc = list(zip(*np.where(np.triu(np.ones([shape, shape])) == 0)))
    normalized_matrix = matrix / np.max(np.abs(matrix))
    if mode == 'co-occurrence':
        weight = np.log(2000 * normalized_matrix + 1) * 0.7
        color = np.log(2000 * normalized_matrix + 1)
    if mode == 'sentiment':
        weight = np.log(np.abs(1000 * normalized_matrix) + 1) * 0.7
        color = 2000 * normalized_matrix
    for i in lower_tri_loc:
        edge_list.append((name_list[i[0]], name_list[i[1]], {'weight': weight[i], 'color': color[i]}))

    return edge_list


def matrix_to_edge_list_v2(matrix, mode, name_list, place_list):
    '''
    Function to convert matrix (co-occurrence/sentiment) to edge list of the network graph. It determines the
    weight and color of the edges in the network graph.
    :param matrix: co-occurrence matrix or sentiment matrix.
    :param mode: 'co-occurrence' or 'sentiment'
    :param name_list: the list of names of the top characters in the novel.
    :return: the edge list with weight and color param.
    '''
    edge_list = []
    shape = matrix.shape[0]
    A = np.ones([shape, shape])
    middle = len(name_list)
    A[0:middle, 0:middle] = np.zeros([middle, middle])
    A[middle:shape, middle:shape] = np.zeros([shape-middle, shape-middle])
    lower_tri_loc = list(zip(*np.where(A == 1)))

    normalized_matrix = matrix / np.max(np.abs(matrix))
    if mode == 'co-occurrence':
        weight = np.log(2000 * normalized_matrix + 1) * 0.7
        color = np.log(2000 * normalized_matrix + 1)
    else: # mode == 'sentiment'
        weight = np.log(np.abs(1000 * normalized_matrix) + 1) * 0.7
        color = 2000 * normalized_matrix
    combined_list = name_list + place_list
    for i in lower_tri_loc:
        if weight[i] != 0.0:
            edge_list.append((combined_list[i[0]], combined_list[i[1]], {'weight': weight[i], 'color': color[i]}))

    return edge_list


def plot_graph(name_list, name_frequency, matrix, plt_name, mode, path=''):
    '''
    Function to plot the network graph (co-occurrence network or sentiment network).
    :param name_list: the list of top character names in the novel.
    :param name_frequency: the list containing the frequencies of the top names.
    :param matrix: co-occurrence matrix or sentiment matrix.
    :param plt_name: the name of the plot (PNG file) to output.
    :param mode: 'co-occurrence' or 'sentiment'
    :param path: the path to output the PNG file.
    :return: a PNG file of the network graph.
    '''

    label = {i: i for i in name_list}
    edge_list = matrix_to_edge_list(matrix, mode, name_list)
    normalized_frequency = np.array(name_frequency) / np.max(name_frequency)

    plt.figure(figsize=(20, 20))
    G = nx.Graph()
    G.add_nodes_from(name_list)
    G.add_edges_from(edge_list)
    pos = nx.circular_layout(G)
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    colors = [G[u][v]['color'] for u, v in edges]
    if mode == 'co-occurrence':
        nx.draw(G, pos, node_color='#A0CBE2', node_size=np.sqrt(normalized_frequency) * 4000, edge_cmap=plt.cm.Blues,
                linewidths=10, font_size=35, labels=label, edge_color=colors, with_labels=True, width=weights)
    elif mode == 'sentiment':
        nx.draw(G, pos, node_color='#A0CBE2', node_size=np.sqrt(normalized_frequency) * 4000,
                linewidths=10, font_size=35, labels=label, edge_color=colors, with_labels=True,
                width=weights, edge_vmin=-1000, edge_vmax=1000)
    else:
        raise ValueError("mode should be either 'co-occurrence' or 'sentiment'")

    plt.savefig("output/" + path + plt_name + '.png')


def plot_graph_v2(name_list, name_frequency, place_list, place_frequency, matrix, plt_name, mode, path=''):
    '''
    Function to plot the network graph (co-occurrence network or sentiment network).
    :param name_list: the list of top character names in the novel.
    :param name_frequency: the list containing the frequencies of the top names.
    :param matrix: co-occurrence matrix or sentiment matrix.
    :param plt_name: the name of the plot (PNG file) to output.
    :param mode: 'co-occurrence' or 'sentiment'
    :param path: the path to output the PNG file.
    :return: a PNG file of the network graph.
    '''

    label = {i: i for i in name_list + place_list}
    edge_list = matrix_to_edge_list_v2(matrix, mode, name_list, place_list)
    normalized_frequency = np.array(name_frequency + place_frequency) / np.max(name_frequency + place_frequency)

    plt.figure(figsize=(20, 20))
    G = nx.Graph()
    name_list_with_attr = [(n, {"color": "red"}) for n in name_list]
    G.add_nodes_from(name_list_with_attr)
    place_list_with_attr = [(p, {"color": 'blue'}) for p in place_list]
    combined = name_list_with_attr + place_list_with_attr
    G.add_nodes_from(combined)
    G.add_edges_from(edge_list)
    pos = nx.circular_layout(G)

    edges = G.edges()
    edge_colors = [G[u][v]['color'] for u, v in edges]

    if mode == 'co-occurrence':
        nx.draw(G, pos, node_size=np.sqrt(normalized_frequency) * 4000, edge_cmap=plt.cm.Blues,
                linewidths=10, font_size=35, labels=label, edge_color=edge_colors, with_labels=True)
    elif mode == 'sentiment':
        nx.draw(G, pos, node_size=np.sqrt(normalized_frequency) * 4000,
                linewidths=10, font_size=35, labels=label, edge_color=edge_colors, with_labels=True,
                edge_vmin=-1000, edge_vmax=1000)
    else:
        raise ValueError("mode should be either 'co-occurrence' or 'sentiment'")

    plt.savefig("output/" + path + plt_name + '.png')
    plt.show()


def plot_graph_v3(name_list, name_frequency, place_list, place_frequency, matrix, plt_name, mode, path=''):
    '''
    Function to plot the network graph (co-occurrence network or sentiment network).
    :param name_list: the list of top character names in the novel.
    :param name_frequency: the list containing the frequencies of the top names.
    :param matrix: co-occurrence matrix or sentiment matrix.
    :param plt_name: the name of the plot (PNG file) to output.
    :param mode: 'co-occurrence' or 'sentiment'
    :param path: the path to output the PNG file.
    :return: a PNG file of the network graph.
    '''
    labels = {i: i for i in name_list + place_list}
    edge_list = matrix_to_edge_list_v2(matrix, mode, name_list, place_list)
    print(edge_list)
    normalized_frequency = np.array(name_frequency + place_frequency) / np.max(name_frequency + place_frequency)

    plt.figure(figsize=(20, 20))
    G = nx.Graph()
    name_list_with_attr = [(n, {"color": "red", "pos": [0, i]}) for i,n in enumerate(name_list)]
    G.add_nodes_from(name_list_with_attr)

    place_list_with_attr = [(p, {"color": 'blue', "pos": [1, i]}) for i, p in enumerate(place_list)]
    combined = name_list_with_attr + place_list_with_attr
    G.add_nodes_from(combined)
    G.add_edges_from(edge_list)
    pos = nx.get_node_attributes(G, 'pos')
    edges = G.edges()

    weights = [G[u][v]['weight'] for u, v in edges]
    colors = [G[u][v]['color'] for u, v in edges]

    
    nx.draw(G, pos, node_color='#A0CBE2', node_size=np.sqrt(normalized_frequency) * 4000, edge_cmap=plt.cm.Blues,
                linewidths=10, font_size=35, edge_color=colors, with_labels=False, width=weights)
    
    comb = name_list + place_list
    for i in range(len(comb)):
        labels[comb[i]] = comb[i]

    for loc in pos:
        pos[loc][1] += 0.2
    nx.draw_networkx_labels(G, pos, labels, font_size=16)
    
    plt.show()
    return


synonym = dict()
harry = ['harry', 'harry potter', 'potter']
ron = ['ron weasley', 'ron', 'weasley']
Hermione = ['hermione granger', 'miss granger', 'hermione', 'granger']
snape = ['professor snape', 'snape', 'severus', 'severus snape', 'professor severus snape']
dumbledore = ['dumbledore', 'albus dumbledore', 'albus', 'professor dumbledore', 'professor albus dumbledore', 'headmaster']
hagrid = ['rubeus Hagrid', 'professor rubeus hagrid', 'hagrid', 'professor hagrid']
malfoy = ['malfoy', 'draco', 'draco malfoy', 'draco lucius malfoy']
mcgonagall = ['mcgonagall', 'professor mcgonagall']
neville = ['neville longbottom', 'neville']
places = ["Majorca", "Tibbles, Snowy", "Hogwarts", "Mount", "Blackpool", "Privet Drive --'", "Underground", "Flint", "the Black Forest", "yeh'll", "Pince", "Great Britain", "Yorkshire", "Firenze", "Dundee", "Brazil", "Gryffindor tower", "the Famous Witches and Wizards", "England", "London", "Quidditch", "the Golden Snitch", "Easter", "Yeh'll", "Stick", "Pewter", "Romania", "the London Underground", "Devon", "Ireland", "the Great Hall", "turkey", "Quidditch cup", "the Isle of Wight", "Gringotts", "the Leg-Locker Curse", "The Great Hall", "Diagon Alley", "Uncle Vernon", "Brass", "Vernon", "Mars", "Bristol", "Apothecary", "Snitch", "Muggle", "Smelting stick", "Mars Bars", "Paddington", "Galleon", "Egg to Inferno", "Dursley", "Britain", "Jupiter", "the Sahara Desert", "Gryffindor Tower", "Tawny", "phoenix", "the Smelting stick", "Prewetts", "Kent", "Uncle Vernon's", "Beechwood", "-the Great Hall", "the Dark Side", "the Leaky Cauldron", "Privet Drive"]
