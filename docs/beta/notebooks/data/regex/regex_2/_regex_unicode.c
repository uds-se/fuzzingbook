/* For Unicode version 11.0.0 */

#include "_regex_unicode.h"

#define RE_BLANK_MASK ((1 << RE_PROP_ZL) | (1 << RE_PROP_ZP))
#define RE_GRAPH_MASK ((1 << RE_PROP_CC) | (1 << RE_PROP_CS) | (1 << RE_PROP_CN))
#define RE_WORD_MASK (RE_PROP_M_MASK | (1 << RE_PROP_ND) | (1 << RE_PROP_PC))

typedef struct RE_ScriptExt {
    RE_UINT8 scripts[RE_MAX_SCX];
} RE_ScriptExt;

typedef struct RE_AllCases {
    RE_INT32 diffs[RE_MAX_CASES - 1];
} RE_AllCases;

typedef struct RE_FullCaseFolding {
    RE_INT32 diff;
    RE_UINT16 codepoints[RE_MAX_FOLDED - 1];
} RE_FullCaseFolding;

/* strings. */

char* re_strings[] = {
    "-1/2",
    "0",
    "1",
    "1/10",
    "1/12",
    "1/16",
    "1/160",
    "1/2",
    "1/20",
    "1/3",
    "1/4",
    "1/40",
    "1/5",
    "1/6",
    "1/7",
    "1/8",
    "1/9",
    "10",
    "100",
    "1000",
    "10000",
    "100000",
    "1000000",
    "10000000",
    "100000000",
    "10000000000",
    "1000000000000",
    "103",
    "107",
    "11",
    "11/12",
    "11/2",
    "118",
    "12",
    "122",
    "129",
    "13",
    "13/2",
    "130",
    "132",
    "133",
    "14",
    "15",
    "15/2",
    "16",
    "17",
    "17/2",
    "18",
    "19",
    "2",
    "2/3",
    "2/5",
    "20",
    "200",
    "2000",
    "20000",
    "200000",
    "20000000",
    "202",
    "21",
    "214",
    "216",
    "216000",
    "218",
    "22",
    "220",
    "222",
    "224",
    "226",
    "228",
    "23",
    "230",
    "232",
    "233",
    "234",
    "24",
    "240",
    "25",
    "26",
    "27",
    "28",
    "29",
    "3",
    "3/16",
    "3/2",
    "3/20",
    "3/4",
    "3/5",
    "3/8",
    "3/80",
    "30",
    "300",
    "3000",
    "30000",
    "300000",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "4",
    "4/5",
    "40",
    "400",
    "4000",
    "40000",
    "400000",
    "41",
    "42",
    "43",
    "432000",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "5",
    "5/12",
    "5/2",
    "5/6",
    "5/8",
    "50",
    "500",
    "5000",
    "50000",
    "500000",
    "6",
    "60",
    "600",
    "6000",
    "60000",
    "600000",
    "7",
    "7/12",
    "7/2",
    "7/8",
    "70",
    "700",
    "7000",
    "70000",
    "700000",
    "8",
    "80",
    "800",
    "8000",
    "80000",
    "800000",
    "84",
    "9",
    "9/2",
    "90",
    "900",
    "9000",
    "90000",
    "900000",
    "91",
    "A",
    "ABOVE",
    "ABOVELEFT",
    "ABOVERIGHT",
    "ADLAM",
    "ADLM",
    "AEGEANNUMBERS",
    "AFRICANFEH",
    "AFRICANNOON",
    "AFRICANQAF",
    "AGHB",
    "AHEX",
    "AHOM",
    "AI",
    "AIN",
    "AL",
    "ALAPH",
    "ALCHEMICAL",
    "ALCHEMICALSYMBOLS",
    "ALEF",
    "ALETTER",
    "ALNUM",
    "ALPHA",
    "ALPHABETIC",
    "ALPHABETICPF",
    "ALPHABETICPRESENTATIONFORMS",
    "ALPHANUMERIC",
    "AMBIGUOUS",
    "AN",
    "ANATOLIANHIEROGLYPHS",
    "ANCIENTGREEKMUSIC",
    "ANCIENTGREEKMUSICALNOTATION",
    "ANCIENTGREEKNUMBERS",
    "ANCIENTSYMBOLS",
    "ANY",
    "AR",
    "ARAB",
    "ARABIC",
    "ARABICEXTA",
    "ARABICEXTENDEDA",
    "ARABICLETTER",
    "ARABICMATH",
    "ARABICMATHEMATICALALPHABETICSYMBOLS",
    "ARABICNUMBER",
    "ARABICPFA",
    "ARABICPFB",
    "ARABICPRESENTATIONFORMSA",
    "ARABICPRESENTATIONFORMSB",
    "ARABICSUP",
    "ARABICSUPPLEMENT",
    "ARMENIAN",
    "ARMI",
    "ARMN",
    "ARROWS",
    "ASCII",
    "ASCIIHEXDIGIT",
    "ASSIGNED",
    "AT",
    "ATA",
    "ATAR",
    "ATB",
    "ATBL",
    "ATERM",
    "ATTACHEDABOVE",
    "ATTACHEDABOVERIGHT",
    "ATTACHEDBELOW",
    "ATTACHEDBELOWLEFT",
    "AVAGRAHA",
    "AVESTAN",
    "AVST",
    "B",
    "B2",
    "BA",
    "BALI",
    "BALINESE",
    "BAMU",
    "BAMUM",
    "BAMUMSUP",
    "BAMUMSUPPLEMENT",
    "BASICLATIN",
    "BASS",
    "BASSAVAH",
    "BATAK",
    "BATK",
    "BB",
    "BC",
    "BEH",
    "BELOW",
    "BELOWLEFT",
    "BELOWRIGHT",
    "BENG",
    "BENGALI",
    "BETH",
    "BHAIKSUKI",
    "BHKS",
    "BIDIC",
    "BIDICLASS",
    "BIDICONTROL",
    "BIDIM",
    "BIDIMIRRORED",
    "BINDU",
    "BK",
    "BL",
    "BLANK",
    "BLK",
    "BLOCK",
    "BLOCKELEMENTS",
    "BN",
    "BOPO",
    "BOPOMOFO",
    "BOPOMOFOEXT",
    "BOPOMOFOEXTENDED",
    "BOTTOM",
    "BOTTOMANDLEFT",
    "BOTTOMANDRIGHT",
    "BOUNDARYNEUTRAL",
    "BOXDRAWING",
    "BR",
    "BRAH",
    "BRAHMI",
    "BRAHMIJOININGNUMBER",
    "BRAI",
    "BRAILLE",
    "BRAILLEPATTERNS",
    "BREAKAFTER",
    "BREAKBEFORE",
    "BREAKBOTH",
    "BREAKSYMBOLS",
    "BUGI",
    "BUGINESE",
    "BUHD",
    "BUHID",
    "BURUSHASKIYEHBARREE",
    "BYZANTINEMUSIC",
    "BYZANTINEMUSICALSYMBOLS",
    "C",
    "C&",
    "CAKM",
    "CAN",
    "CANADIANABORIGINAL",
    "CANADIANSYLLABICS",
    "CANONICAL",
    "CANONICALCOMBININGCLASS",
    "CANS",
    "CANTILLATIONMARK",
    "CARI",
    "CARIAN",
    "CARRIAGERETURN",
    "CASED",
    "CASEDLETTER",
    "CASEIGNORABLE",
    "CAUCASIANALBANIAN",
    "CB",
    "CC",
    "CCC",
    "CCC10",
    "CCC103",
    "CCC107",
    "CCC11",
    "CCC118",
    "CCC12",
    "CCC122",
    "CCC129",
    "CCC13",
    "CCC130",
    "CCC132",
    "CCC133",
    "CCC14",
    "CCC15",
    "CCC16",
    "CCC17",
    "CCC18",
    "CCC19",
    "CCC20",
    "CCC21",
    "CCC22",
    "CCC23",
    "CCC24",
    "CCC25",
    "CCC26",
    "CCC27",
    "CCC28",
    "CCC29",
    "CCC30",
    "CCC31",
    "CCC32",
    "CCC33",
    "CCC34",
    "CCC35",
    "CCC36",
    "CCC84",
    "CCC91",
    "CF",
    "CHAKMA",
    "CHAM",
    "CHANGESWHENCASEFOLDED",
    "CHANGESWHENCASEMAPPED",
    "CHANGESWHENLOWERCASED",
    "CHANGESWHENTITLECASED",
    "CHANGESWHENUPPERCASED",
    "CHER",
    "CHEROKEE",
    "CHEROKEESUP",
    "CHEROKEESUPPLEMENT",
    "CHESSSYMBOLS",
    "CI",
    "CIRCLE",
    "CJ",
    "CJK",
    "CJKCOMPAT",
    "CJKCOMPATFORMS",
    "CJKCOMPATIBILITY",
    "CJKCOMPATIBILITYFORMS",
    "CJKCOMPATIBILITYIDEOGRAPHS",
    "CJKCOMPATIBILITYIDEOGRAPHSSUPPLEMENT",
    "CJKCOMPATIDEOGRAPHS",
    "CJKCOMPATIDEOGRAPHSSUP",
    "CJKEXTA",
    "CJKEXTB",
    "CJKEXTC",
    "CJKEXTD",
    "CJKEXTE",
    "CJKEXTF",
    "CJKRADICALSSUP",
    "CJKRADICALSSUPPLEMENT",
    "CJKSTROKES",
    "CJKSYMBOLS",
    "CJKSYMBOLSANDPUNCTUATION",
    "CJKUNIFIEDIDEOGRAPHS",
    "CJKUNIFIEDIDEOGRAPHSEXTENSIONA",
    "CJKUNIFIEDIDEOGRAPHSEXTENSIONB",
    "CJKUNIFIEDIDEOGRAPHSEXTENSIONC",
    "CJKUNIFIEDIDEOGRAPHSEXTENSIOND",
    "CJKUNIFIEDIDEOGRAPHSEXTENSIONE",
    "CJKUNIFIEDIDEOGRAPHSEXTENSIONF",
    "CL",
    "CLOSE",
    "CLOSEPARENTHESIS",
    "CLOSEPUNCTUATION",
    "CM",
    "CN",
    "CNTRL",
    "CO",
    "COM",
    "COMBININGDIACRITICALMARKS",
    "COMBININGDIACRITICALMARKSEXTENDED",
    "COMBININGDIACRITICALMARKSFORSYMBOLS",
    "COMBININGDIACRITICALMARKSSUPPLEMENT",
    "COMBININGHALFMARKS",
    "COMBININGMARK",
    "COMBININGMARKSFORSYMBOLS",
    "COMMON",
    "COMMONINDICNUMBERFORMS",
    "COMMONSEPARATOR",
    "COMPAT",
    "COMPATJAMO",
    "COMPLEXCONTEXT",
    "CONDITIONALJAPANESESTARTER",
    "CONNECTORPUNCTUATION",
    "CONSONANT",
    "CONSONANTDEAD",
    "CONSONANTFINAL",
    "CONSONANTHEADLETTER",
    "CONSONANTINITIALPOSTFIXED",
    "CONSONANTKILLER",
    "CONSONANTMEDIAL",
    "CONSONANTPLACEHOLDER",
    "CONSONANTPRECEDINGREPHA",
    "CONSONANTPREFIXED",
    "CONSONANTSUBJOINED",
    "CONSONANTSUCCEEDINGREPHA",
    "CONSONANTWITHSTACKER",
    "CONTINGENTBREAK",
    "CONTROL",
    "CONTROLPICTURES",
    "COPT",
    "COPTIC",
    "COPTICEPACTNUMBERS",
    "COUNTINGROD",
    "COUNTINGRODNUMERALS",
    "CP",
    "CPRT",
    "CR",
    "CS",
    "CUNEIFORM",
    "CUNEIFORMNUMBERS",
    "CUNEIFORMNUMBERSANDPUNCTUATION",
    "CURRENCYSYMBOL",
    "CURRENCYSYMBOLS",
    "CWCF",
    "CWCM",
    "CWL",
    "CWT",
    "CWU",
    "CYPRIOT",
    "CYPRIOTSYLLABARY",
    "CYRILLIC",
    "CYRILLICEXTA",
    "CYRILLICEXTB",
    "CYRILLICEXTC",
    "CYRILLICEXTENDEDA",
    "CYRILLICEXTENDEDB",
    "CYRILLICEXTENDEDC",
    "CYRILLICSUP",
    "CYRILLICSUPPLEMENT",
    "CYRILLICSUPPLEMENTARY",
    "CYRL",
    "D",
    "DA",
    "DAL",
    "DALATHRISH",
    "DASH",
    "DASHPUNCTUATION",
    "DB",
    "DE",
    "DECIMAL",
    "DECIMALNUMBER",
    "DECOMPOSITIONTYPE",
    "DEFAULTIGNORABLECODEPOINT",
    "DEP",
    "DEPRECATED",
    "DESERET",
    "DEVA",
    "DEVANAGARI",
    "DEVANAGARIEXT",
    "DEVANAGARIEXTENDED",
    "DI",
    "DIA",
    "DIACRITIC",
    "DIACRITICALS",
    "DIACRITICALSEXT",
    "DIACRITICALSFORSYMBOLS",
    "DIACRITICALSSUP",
    "DIGIT",
    "DINGBATS",
    "DOGR",
    "DOGRA",
    "DOMINO",
    "DOMINOTILES",
    "DOUBLEABOVE",
    "DOUBLEBELOW",
    "DOUBLEQUOTE",
    "DQ",
    "DSRT",
    "DT",
    "DUALJOINING",
    "DUPL",
    "DUPLOYAN",
    "E",
    "EA",
    "EARLYDYNASTICCUNEIFORM",
    "EASTASIANWIDTH",
    "EB",
    "EBASE",
    "EBASEGAZ",
    "EBG",
    "EGYP",
    "EGYPTIANHIEROGLYPHS",
    "ELBA",
    "ELBASAN",
    "EM",
    "EMODIFIER",
    "EMOJI",
    "EMOJICOMPONENT",
    "EMOJIMODIFIER",
    "EMOJIMODIFIERBASE",
    "EMOJIPRESENTATION",
    "EMOTICONS",
    "EN",
    "ENC",
    "ENCLOSEDALPHANUM",
    "ENCLOSEDALPHANUMERICS",
    "ENCLOSEDALPHANUMERICSUPPLEMENT",
    "ENCLOSEDALPHANUMSUP",
    "ENCLOSEDCJK",
    "ENCLOSEDCJKLETTERSANDMONTHS",
    "ENCLOSEDIDEOGRAPHICSUP",
    "ENCLOSEDIDEOGRAPHICSUPPLEMENT",
    "ENCLOSINGMARK",
    "ES",
    "ET",
    "ETHI",
    "ETHIOPIC",
    "ETHIOPICEXT",
    "ETHIOPICEXTA",
    "ETHIOPICEXTENDED",
    "ETHIOPICEXTENDEDA",
    "ETHIOPICSUP",
    "ETHIOPICSUPPLEMENT",
    "EUROPEANNUMBER",
    "EUROPEANSEPARATOR",
    "EUROPEANTERMINATOR",
    "EX",
    "EXCLAMATION",
    "EXT",
    "EXTEND",
    "EXTENDEDPICTOGRAPHIC",
    "EXTENDER",
    "EXTENDNUMLET",
    "F",
    "FALSE",
    "FARSIYEH",
    "FE",
    "FEH",
    "FIN",
    "FINAL",
    "FINALPUNCTUATION",
    "FINALSEMKATH",
    "FIRSTSTRONGISOLATE",
    "FO",
    "FONT",
    "FORMAT",
    "FRA",
    "FRACTION",
    "FSI",
    "FULLWIDTH",
    "GAF",
    "GAMAL",
    "GAZ",
    "GC",
    "GCB",
    "GEMINATIONMARK",
    "GENERALCATEGORY",
    "GENERALPUNCTUATION",
    "GEOMETRICSHAPES",
    "GEOMETRICSHAPESEXT",
    "GEOMETRICSHAPESEXTENDED",
    "GEOR",
    "GEORGIAN",
    "GEORGIANEXT",
    "GEORGIANEXTENDED",
    "GEORGIANSUP",
    "GEORGIANSUPPLEMENT",
    "GL",
    "GLAG",
    "GLAGOLITIC",
    "GLAGOLITICSUP",
    "GLAGOLITICSUPPLEMENT",
    "GLUE",
    "GLUEAFTERZWJ",
    "GONG",
    "GONM",
    "GOTH",
    "GOTHIC",
    "GRAN",
    "GRANTHA",
    "GRAPH",
    "GRAPHEMEBASE",
    "GRAPHEMECLUSTERBREAK",
    "GRAPHEMEEXTEND",
    "GRAPHEMELINK",
    "GRBASE",
    "GREEK",
    "GREEKANDCOPTIC",
    "GREEKEXT",
    "GREEKEXTENDED",
    "GREK",
    "GREXT",
    "GRLINK",
    "GUJARATI",
    "GUJR",
    "GUNJALAGONDI",
    "GURMUKHI",
    "GURU",
    "H",
    "H2",
    "H3",
    "HAH",
    "HALFANDFULLFORMS",
    "HALFMARKS",
    "HALFWIDTH",
    "HALFWIDTHANDFULLWIDTHFORMS",
    "HAMZAONHEHGOAL",
    "HAN",
    "HANG",
    "HANGUL",
    "HANGULCOMPATIBILITYJAMO",
    "HANGULJAMO",
    "HANGULJAMOEXTENDEDA",
    "HANGULJAMOEXTENDEDB",
    "HANGULSYLLABLES",
    "HANGULSYLLABLETYPE",
    "HANI",
    "HANIFIROHINGYA",
    "HANIFIROHINGYAKINNAYA",
    "HANIFIROHINGYAPA",
    "HANO",
    "HANUNOO",
    "HATR",
    "HATRAN",
    "HE",
    "HEBR",
    "HEBREW",
    "HEBREWLETTER",
    "HEH",
    "HEHGOAL",
    "HETH",
    "HEX",
    "HEXDIGIT",
    "HIGHPRIVATEUSESURROGATES",
    "HIGHPUSURROGATES",
    "HIGHSURROGATES",
    "HIRA",
    "HIRAGANA",
    "HL",
    "HLUW",
    "HMNG",
    "HRKT",
    "HST",
    "HUNG",
    "HY",
    "HYPHEN",
    "ID",
    "IDC",
    "IDCONTINUE",
    "IDEO",
    "IDEOGRAPHIC",
    "IDEOGRAPHICDESCRIPTIONCHARACTERS",
    "IDEOGRAPHICSYMBOLS",
    "IDEOGRAPHICSYMBOLSANDPUNCTUATION",
    "IDS",
    "IDSB",
    "IDSBINARYOPERATOR",
    "IDST",
    "IDSTART",
    "IDSTRINARYOPERATOR",
    "IMPERIALARAMAIC",
    "IN",
    "INDICNUMBERFORMS",
    "INDICPOSITIONALCATEGORY",
    "INDICSIYAQNUMBERS",
    "INDICSYLLABICCATEGORY",
    "INFIXNUMERIC",
    "INHERITED",
    "INIT",
    "INITIAL",
    "INITIALPUNCTUATION",
    "INPC",
    "INSC",
    "INSCRIPTIONALPAHLAVI",
    "INSCRIPTIONALPARTHIAN",
    "INSEPARABLE",
    "INSEPERABLE",
    "INVISIBLESTACKER",
    "IOTASUBSCRIPT",
    "IPAEXT",
    "IPAEXTENSIONS",
    "IS",
    "ISO",
    "ISOLATED",
    "ITAL",
    "JAMO",
    "JAMOEXTA",
    "JAMOEXTB",
    "JAVA",
    "JAVANESE",
    "JG",
    "JL",
    "JOINC",
    "JOINCAUSING",
    "JOINCONTROL",
    "JOINER",
    "JOININGGROUP",
    "JOININGTYPE",
    "JT",
    "JV",
    "KA",
    "KAF",
    "KAITHI",
    "KALI",
    "KANA",
    "KANAEXTA",
    "KANAEXTENDEDA",
    "KANASUP",
    "KANASUPPLEMENT",
    "KANAVOICING",
    "KANBUN",
    "KANGXI",
    "KANGXIRADICALS",
    "KANNADA",
    "KAPH",
    "KATAKANA",
    "KATAKANAEXT",
    "KATAKANAORHIRAGANA",
    "KATAKANAPHONETICEXTENSIONS",
    "KAYAHLI",
    "KHAPH",
    "KHAR",
    "KHAROSHTHI",
    "KHMER",
    "KHMERSYMBOLS",
    "KHMR",
    "KHOJ",
    "KHOJKI",
    "KHUDAWADI",
    "KNDA",
    "KNOTTEDHEH",
    "KTHI",
    "KV",
    "L",
    "L&",
    "LAM",
    "LAMADH",
    "LANA",
    "LAO",
    "LAOO",
    "LATIN",
    "LATIN1",
    "LATIN1SUP",
    "LATIN1SUPPLEMENT",
    "LATINEXTA",
    "LATINEXTADDITIONAL",
    "LATINEXTB",
    "LATINEXTC",
    "LATINEXTD",
    "LATINEXTE",
    "LATINEXTENDEDA",
    "LATINEXTENDEDADDITIONAL",
    "LATINEXTENDEDB",
    "LATINEXTENDEDC",
    "LATINEXTENDEDD",
    "LATINEXTENDEDE",
    "LATN",
    "LB",
    "LC",
    "LE",
    "LEADINGJAMO",
    "LEFT",
    "LEFTANDRIGHT",
    "LEFTJOINING",
    "LEFTTORIGHT",
    "LEFTTORIGHTEMBEDDING",
    "LEFTTORIGHTISOLATE",
    "LEFTTORIGHTOVERRIDE",
    "LEPC",
    "LEPCHA",
    "LETTER",
    "LETTERLIKESYMBOLS",
    "LETTERNUMBER",
    "LF",
    "LIMB",
    "LIMBU",
    "LINA",
    "LINB",
    "LINEARA",
    "LINEARB",
    "LINEARBIDEOGRAMS",
    "LINEARBSYLLABARY",
    "LINEBREAK",
    "LINEFEED",
    "LINESEPARATOR",
    "LISU",
    "LL",
    "LM",
    "LO",
    "LOE",
    "LOGICALORDEREXCEPTION",
    "LOWER",
    "LOWERCASE",
    "LOWERCASELETTER",
    "LOWSURROGATES",
    "LRE",
    "LRI",
    "LRO",
    "LT",
    "LU",
    "LV",
    "LVSYLLABLE",
    "LVT",
    "LVTSYLLABLE",
    "LYCI",
    "LYCIAN",
    "LYDI",
    "LYDIAN",
    "M",
    "M&",
    "MAHAJANI",
    "MAHJ",
    "MAHJONG",
    "MAHJONGTILES",
    "MAKA",
    "MAKASAR",
    "MALAYALAM",
    "MALAYALAMBHA",
    "MALAYALAMJA",
    "MALAYALAMLLA",
    "MALAYALAMLLLA",
    "MALAYALAMNGA",
    "MALAYALAMNNA",
    "MALAYALAMNNNA",
    "MALAYALAMNYA",
    "MALAYALAMRA",
    "MALAYALAMSSA",
    "MALAYALAMTTA",
    "MAND",
    "MANDAIC",
    "MANDATORYBREAK",
    "MANI",
    "MANICHAEAN",
    "MANICHAEANALEPH",
    "MANICHAEANAYIN",
    "MANICHAEANBETH",
    "MANICHAEANDALETH",
    "MANICHAEANDHAMEDH",
    "MANICHAEANFIVE",
    "MANICHAEANGIMEL",
    "MANICHAEANHETH",
    "MANICHAEANHUNDRED",
    "MANICHAEANKAPH",
    "MANICHAEANLAMEDH",
    "MANICHAEANMEM",
    "MANICHAEANNUN",
    "MANICHAEANONE",
    "MANICHAEANPE",
    "MANICHAEANQOPH",
    "MANICHAEANRESH",
    "MANICHAEANSADHE",
    "MANICHAEANSAMEKH",
    "MANICHAEANTAW",
    "MANICHAEANTEN",
    "MANICHAEANTETH",
    "MANICHAEANTHAMEDH",
    "MANICHAEANTWENTY",
    "MANICHAEANWAW",
    "MANICHAEANYODH",
    "MANICHAEANZAYIN",
    "MARC",
    "MARCHEN",
    "MARK",
    "MASARAMGONDI",
    "MATH",
    "MATHALPHANUM",
    "MATHEMATICALALPHANUMERICSYMBOLS",
    "MATHEMATICALOPERATORS",
    "MATHOPERATORS",
    "MATHSYMBOL",
    "MAYANNUMERALS",
    "MAYBE",
    "MB",
    "MC",
    "ME",
    "MED",
    "MEDEFAIDRIN",
    "MEDF",
    "MEDIAL",
    "MEEM",
    "MEETEIMAYEK",
    "MEETEIMAYEKEXT",
    "MEETEIMAYEKEXTENSIONS",
    "MEND",
    "MENDEKIKAKUI",
    "MERC",
    "MERO",
    "MEROITICCURSIVE",
    "MEROITICHIEROGLYPHS",
    "MIAO",
    "MIDLETTER",
    "MIDNUM",
    "MIDNUMLET",
    "MIM",
    "MISCARROWS",
    "MISCELLANEOUSMATHEMATICALSYMBOLSA",
    "MISCELLANEOUSMATHEMATICALSYMBOLSB",
    "MISCELLANEOUSSYMBOLS",
    "MISCELLANEOUSSYMBOLSANDARROWS",
    "MISCELLANEOUSSYMBOLSANDPICTOGRAPHS",
    "MISCELLANEOUSTECHNICAL",
    "MISCMATHSYMBOLSA",
    "MISCMATHSYMBOLSB",
    "MISCPICTOGRAPHS",
    "MISCSYMBOLS",
    "MISCTECHNICAL",
    "ML",
    "MLYM",
    "MN",
    "MODI",
    "MODIFIERLETTER",
    "MODIFIERLETTERS",
    "MODIFIERSYMBOL",
    "MODIFIERTONELETTERS",
    "MODIFYINGLETTER",
    "MONG",
    "MONGOLIAN",
    "MONGOLIANSUP",
    "MONGOLIANSUPPLEMENT",
    "MRO",
    "MROO",
    "MTEI",
    "MULT",
    "MULTANI",
    "MUSIC",
    "MUSICALSYMBOLS",
    "MYANMAR",
    "MYANMAREXTA",
    "MYANMAREXTB",
    "MYANMAREXTENDEDA",
    "MYANMAREXTENDEDB",
    "MYMR",
    "N",
    "N&",
    "NA",
    "NABATAEAN",
    "NAN",
    "NAR",
    "NARB",
    "NARROW",
    "NB",
    "NBAT",
    "NCHAR",
    "ND",
    "NEUTRAL",
    "NEWA",
    "NEWLINE",
    "NEWTAILUE",
    "NEXTLINE",
    "NFCQC",
    "NFCQUICKCHECK",
    "NFDQC",
    "NFDQUICKCHECK",
    "NFKCQC",
    "NFKCQUICKCHECK",
    "NFKDQC",
    "NFKDQUICKCHECK",
    "NK",
    "NKO",
    "NKOO",
    "NL",
    "NO",
    "NOBLOCK",
    "NOBREAK",
    "NOJOININGGROUP",
    "NONCHARACTERCODEPOINT",
    "NONE",
    "NONJOINER",
    "NONJOINING",
    "NONSPACINGMARK",
    "NONSTARTER",
    "NOON",
    "NOTAPPLICABLE",
    "NOTREORDERED",
    "NR",
    "NS",
    "NSHU",
    "NSM",
    "NT",
    "NU",
    "NUKTA",
    "NUMBER",
    "NUMBERFORMS",
    "NUMBERJOINER",
    "NUMERIC",
    "NUMERICTYPE",
    "NUMERICVALUE",
    "NUN",
    "NUSHU",
    "NV",
    "NYA",
    "OALPHA",
    "OCR",
    "ODI",
    "OGAM",
    "OGHAM",
    "OGREXT",
    "OIDC",
    "OIDS",
    "OLCHIKI",
    "OLCK",
    "OLDHUNGARIAN",
    "OLDITALIC",
    "OLDNORTHARABIAN",
    "OLDPERMIC",
    "OLDPERSIAN",
    "OLDSOGDIAN",
    "OLDSOUTHARABIAN",
    "OLDTURKIC",
    "OLETTER",
    "OLOWER",
    "OMATH",
    "ON",
    "OP",
    "OPENPUNCTUATION",
    "OPTICALCHARACTERRECOGNITION",
    "ORIYA",
    "ORKH",
    "ORNAMENTALDINGBATS",
    "ORYA",
    "OSAGE",
    "OSGE",
    "OSMA",
    "OSMANYA",
    "OTHER",
    "OTHERALPHABETIC",
    "OTHERDEFAULTIGNORABLECODEPOINT",
    "OTHERGRAPHEMEEXTEND",
    "OTHERIDCONTINUE",
    "OTHERIDSTART",
    "OTHERLETTER",
    "OTHERLOWERCASE",
    "OTHERMATH",
    "OTHERNEUTRAL",
    "OTHERNUMBER",
    "OTHERPUNCTUATION",
    "OTHERSYMBOL",
    "OTHERUPPERCASE",
    "OUPPER",
    "OV",
    "OVERLAY",
    "OVERSTRUCK",
    "P",
    "P&",
    "PAHAWHHMONG",
    "PALM",
    "PALMYRENE",
    "PARAGRAPHSEPARATOR",
    "PATSYN",
    "PATTERNSYNTAX",
    "PATTERNWHITESPACE",
    "PATWS",
    "PAUC",
    "PAUCINHAU",
    "PC",
    "PCM",
    "PD",
    "PDF",
    "PDI",
    "PE",
    "PERM",
    "PF",
    "PHAG",
    "PHAGSPA",
    "PHAISTOS",
    "PHAISTOSDISC",
    "PHLI",
    "PHLP",
    "PHNX",
    "PHOENICIAN",
    "PHONETICEXT",
    "PHONETICEXTENSIONS",
    "PHONETICEXTENSIONSSUPPLEMENT",
    "PHONETICEXTSUP",
    "PI",
    "PLAYINGCARDS",
    "PLRD",
    "PO",
    "POPDIRECTIONALFORMAT",
    "POPDIRECTIONALISOLATE",
    "POSIXALNUM",
    "POSIXDIGIT",
    "POSIXPUNCT",
    "POSIXXDIGIT",
    "POSTFIXNUMERIC",
    "PP",
    "PR",
    "PREFIXNUMERIC",
    "PREPEND",
    "PREPENDEDCONCATENATIONMARK",
    "PRINT",
    "PRIVATEUSE",
    "PRIVATEUSEAREA",
    "PRTI",
    "PS",
    "PSALTERPAHLAVI",
    "PUA",
    "PUNCT",
    "PUNCTUATION",
    "PUREKILLER",
    "QAAC",
    "QAAI",
    "QAF",
    "QAPH",
    "QMARK",
    "QU",
    "QUOTATION",
    "QUOTATIONMARK",
    "R",
    "RADICAL",
    "REGIONALINDICATOR",
    "REGISTERSHIFTER",
    "REH",
    "REJANG",
    "REVERSEDPE",
    "RI",
    "RIGHT",
    "RIGHTJOINING",
    "RIGHTTOLEFT",
    "RIGHTTOLEFTEMBEDDING",
    "RIGHTTOLEFTISOLATE",
    "RIGHTTOLEFTOVERRIDE",
    "RJNG",
    "RLE",
    "RLI",
    "RLO",
    "ROHG",
    "ROHINGYAYEH",
    "RUMI",
    "RUMINUMERALSYMBOLS",
    "RUNIC",
    "RUNR",
    "S",
    "S&",
    "SA",
    "SAD",
    "SADHE",
    "SAMARITAN",
    "SAMR",
    "SARB",
    "SAUR",
    "SAURASHTRA",
    "SB",
    "SC",
    "SCONTINUE",
    "SCRIPT",
    "SCRIPTEXTENSIONS",
    "SCX",
    "SD",
    "SE",
    "SEEN",
    "SEGMENTSEPARATOR",
    "SEMKATH",
    "SENTENCEBREAK",
    "SENTENCETERMINAL",
    "SEP",
    "SEPARATOR",
    "SG",
    "SGNW",
    "SHARADA",
    "SHAVIAN",
    "SHAW",
    "SHIN",
    "SHORTHANDFORMATCONTROLS",
    "SHRD",
    "SIDD",
    "SIDDHAM",
    "SIGNWRITING",
    "SIND",
    "SINGLEQUOTE",
    "SINH",
    "SINHALA",
    "SINHALAARCHAICNUMBERS",
    "SK",
    "SM",
    "SMALL",
    "SMALLFORMS",
    "SMALLFORMVARIANTS",
    "SML",
    "SO",
    "SOFTDOTTED",
    "SOGD",
    "SOGDIAN",
    "SOGO",
    "SORA",
    "SORASOMPENG",
    "SOYO",
    "SOYOMBO",
    "SP",
    "SPACE",
    "SPACESEPARATOR",
    "SPACINGMARK",
    "SPACINGMODIFIERLETTERS",
    "SPECIALS",
    "SQ",
    "SQR",
    "SQUARE",
    "ST",
    "STERM",
    "STRAIGHTWAW",
    "SUB",
    "SUND",
    "SUNDANESE",
    "SUNDANESESUP",
    "SUNDANESESUPPLEMENT",
    "SUP",
    "SUPARROWSA",
    "SUPARROWSB",
    "SUPARROWSC",
    "SUPER",
    "SUPERANDSUB",
    "SUPERSCRIPTSANDSUBSCRIPTS",
    "SUPMATHOPERATORS",
    "SUPPLEMENTALARROWSA",
    "SUPPLEMENTALARROWSB",
    "SUPPLEMENTALARROWSC",
    "SUPPLEMENTALMATHEMATICALOPERATORS",
    "SUPPLEMENTALPUNCTUATION",
    "SUPPLEMENTALSYMBOLSANDPICTOGRAPHS",
    "SUPPLEMENTARYPRIVATEUSEAREAA",
    "SUPPLEMENTARYPRIVATEUSEAREAB",
    "SUPPUAA",
    "SUPPUAB",
    "SUPPUNCTUATION",
    "SUPSYMBOLSANDPICTOGRAPHS",
    "SURROGATE",
    "SUTTONSIGNWRITING",
    "SWASHKAF",
    "SY",
    "SYLLABLEMODIFIER",
    "SYLO",
    "SYLOTINAGRI",
    "SYMBOL",
    "SYRC",
    "SYRIAC",
    "SYRIACSUP",
    "SYRIACSUPPLEMENT",
    "SYRIACWAW",
    "T",
    "TAGALOG",
    "TAGB",
    "TAGBANWA",
    "TAGS",
    "TAH",
    "TAILE",
    "TAITHAM",
    "TAIVIET",
    "TAIXUANJING",
    "TAIXUANJINGSYMBOLS",
    "TAKR",
    "TAKRI",
    "TALE",
    "TALU",
    "TAMIL",
    "TAML",
    "TANG",
    "TANGUT",
    "TANGUTCOMPONENTS",
    "TAVT",
    "TAW",
    "TEHMARBUTA",
    "TEHMARBUTAGOAL",
    "TELU",
    "TELUGU",
    "TERM",
    "TERMINALPUNCTUATION",
    "TETH",
    "TFNG",
    "TGLG",
    "THAA",
    "THAANA",
    "THAI",
    "TIBETAN",
    "TIBT",
    "TIFINAGH",
    "TIRH",
    "TIRHUTA",
    "TITLECASELETTER",
    "TONELETTER",
    "TONEMARK",
    "TOP",
    "TOPANDBOTTOM",
    "TOPANDBOTTOMANDRIGHT",
    "TOPANDLEFT",
    "TOPANDLEFTANDRIGHT",
    "TOPANDRIGHT",
    "TRAILINGJAMO",
    "TRANSPARENT",
    "TRANSPORTANDMAP",
    "TRANSPORTANDMAPSYMBOLS",
    "TRUE",
    "U",
    "UCAS",
    "UCASEXT",
    "UGAR",
    "UGARITIC",
    "UIDEO",
    "UNASSIGNED",
    "UNIFIEDCANADIANABORIGINALSYLLABICS",
    "UNIFIEDCANADIANABORIGINALSYLLABICSEXTENDED",
    "UNIFIEDIDEOGRAPH",
    "UNKNOWN",
    "UP",
    "UPPER",
    "UPPERCASE",
    "UPPERCASELETTER",
    "V",
    "VAI",
    "VAII",
    "VARIATIONSELECTOR",
    "VARIATIONSELECTORS",
    "VARIATIONSELECTORSSUPPLEMENT",
    "VEDICEXT",
    "VEDICEXTENSIONS",
    "VERT",
    "VERTICAL",
    "VERTICALFORMS",
    "VIRAMA",
    "VISARGA",
    "VISUALORDERLEFT",
    "VOWEL",
    "VOWELDEPENDENT",
    "VOWELINDEPENDENT",
    "VOWELJAMO",
    "VR",
    "VS",
    "VSSUP",
    "W",
    "WARA",
    "WARANGCITI",
    "WAW",
    "WB",
    "WHITESPACE",
    "WIDE",
    "WJ",
    "WORD",
    "WORDBREAK",
    "WORDJOINER",
    "WS",
    "WSEGSPACE",
    "WSPACE",
    "XDIGIT",
    "XIDC",
    "XIDCONTINUE",
    "XIDS",
    "XIDSTART",
    "XPEO",
    "XSUX",
    "XX",
    "Y",
    "YEH",
    "YEHBARREE",
    "YEHWITHTAIL",
    "YES",
    "YI",
    "YIII",
    "YIJING",
    "YIJINGHEXAGRAMSYMBOLS",
    "YIRADICALS",
    "YISYLLABLES",
    "YUDH",
    "YUDHHE",
    "Z",
    "Z&",
    "ZAIN",
    "ZANABAZARSQUARE",
    "ZANB",
    "ZHAIN",
    "ZINH",
    "ZL",
    "ZP",
    "ZS",
    "ZW",
    "ZWJ",
    "ZWSPACE",
    "ZYYY",
    "ZZZZ",
};

/* strings: 13426 bytes. */

/* properties. */

RE_Property re_properties[] = {
    { 583,  0,  0},
    { 580,  0,  0},
    { 266,  1,  1},
    { 265,  1,  1},
    {1172,  2,  2},
    {1170,  2,  2},
    {1173,  3,  2},
    {1174,  3,  2},
    {1363,  4,  3},
    {1358,  4,  3},
    { 609,  5,  4},
    { 581,  5,  4},
    {1180,  6,  5},
    {1169,  6,  5},
    { 891,  7,  6},
    { 184,  8,  6},
    { 183,  8,  6},
    { 819,  9,  6},
    { 818,  9,  6},
    {1331, 10,  6},
    {1330, 10,  6},
    { 309, 11,  6},
    { 311, 12,  6},
    { 366, 12,  6},
    { 358, 13,  6},
    { 452, 13,  6},
    { 360, 14,  6},
    { 454, 14,  6},
    { 359, 15,  6},
    { 453, 15,  6},
    { 356, 16,  6},
    { 450, 16,  6},
    { 357, 17,  6},
    { 451, 17,  6},
    { 685, 18,  6},
    { 681, 18,  6},
    { 675, 19,  6},
    { 674, 19,  6},
    {1372, 20,  6},
    {1371, 20,  6},
    {1370, 21,  6},
    {1369, 21,  6},
    { 479, 22,  6},
    { 487, 22,  6},
    { 610, 23,  6},
    { 618, 23,  6},
    { 608, 24,  6},
    { 612, 24,  6},
    { 611, 25,  6},
    { 619, 25,  6},
    {1359, 26,  6},
    {1367, 26,  6},
    {1216, 26,  6},
    { 258, 27,  6},
    { 256, 27,  6},
    { 721, 28,  6},
    { 719, 28,  6},
    { 472, 29,  6},
    { 672, 30,  6},
    {1134, 31,  6},
    {1131, 31,  6},
    {1292, 32,  6},
    {1291, 32,  6},
    {1059, 33,  6},
    {1038, 33,  6},
    { 659, 34,  6},
    { 658, 34,  6},
    { 216, 35,  6},
    { 172, 35,  6},
    {1052, 36,  6},
    {1018, 36,  6},
    { 677, 37,  6},
    { 676, 37,  6},
    { 489, 38,  6},
    { 488, 38,  6},
    { 558, 39,  6},
    { 555, 39,  6},
    {1058, 40,  6},
    {1037, 40,  6},
    {1064, 41,  6},
    {1065, 41,  6},
    { 992, 42,  6},
    { 969, 42,  6},
    {1054, 43,  6},
    {1023, 43,  6},
    { 683, 44,  6},
    { 682, 44,  6},
    { 686, 45,  6},
    { 684, 45,  6},
    {1136, 46,  6},
    {1327, 47,  6},
    {1323, 47,  6},
    {1053, 48,  6},
    {1020, 48,  6},
    { 481, 49,  6},
    { 480, 49,  6},
    {1207, 50,  6},
    {1175, 50,  6},
    { 817, 51,  6},
    { 816, 51,  6},
    {1056, 52,  6},
    {1025, 52,  6},
    {1055, 53,  6},
    {1024, 53,  6},
    {1181, 54,  6},
    {1225, 54,  6},
    {1336, 55,  6},
    {1352, 55,  6},
    {1077, 56,  6},
    {1078, 56,  6},
    {1076, 57,  6},
    {1075, 57,  6},
    {1116, 58,  6},
    {1082, 58,  6},
    {1137, 59,  6},
    {1142, 59,  6},
    { 642, 60,  7},
    { 669, 60,  7},
    { 257, 61,  8},
    { 246, 61,  8},
    { 303, 62,  9},
    { 315, 62,  9},
    { 478, 63, 10},
    { 505, 63, 10},
    { 512, 64, 11},
    { 510, 64, 11},
    { 723, 65, 12},
    { 717, 65, 12},
    { 724, 66, 13},
    { 725, 66, 13},
    { 809, 67, 14},
    { 784, 67, 14},
    {1012, 68, 15},
    {1005, 68, 15},
    {1013, 69, 16},
    {1016, 69, 16},
    { 260, 70,  6},
    { 259, 70,  6},
    { 690, 71, 17},
    { 698, 71, 17},
    { 692, 72, 18},
    { 699, 72, 18},
    { 523, 73, 19},
    { 527, 74, 19},
    { 525, 75, 19},
    { 526, 76, 19},
    { 524, 77, 19},
    { 557, 78, 19},
    { 979, 79, 20},
    { 978, 79, 20},
    { 977, 80, 21},
    { 976, 80, 21},
    { 983, 81, 20},
    { 982, 81, 20},
    { 981, 82, 21},
    { 980, 82, 21},
    { 187, 83,  6},
    { 182, 83,  6},
    { 195, 84,  6},
    { 264, 85,  6},
    { 607, 86,  6},
    {1117, 87,  6},
    {1362, 88,  6},
    {1368, 89,  6},
    {1108, 90,  6},
    {1107, 91,  6},
    {1109, 92,  6},
    {1110, 93,  6},
};

/* properties: 672 bytes. */

/* property values. */

RE_PropertyValue re_property_values[] = {
    {1324,  0,   0},
    { 401,  0,   0},
    {1332,  0,   1},
    { 826,  0,   1},
    { 820,  0,   2},
    { 813,  0,   2},
    {1304,  0,   3},
    { 825,  0,   3},
    { 937,  0,   4},
    { 814,  0,   4},
    {1057,  0,   5},
    { 815,  0,   5},
    { 996,  0,   6},
    { 935,  0,   6},
    { 539,  0,   7},
    { 901,  0,   7},
    {1218,  0,   8},
    { 900,  0,   8},
    { 477,  0,   9},
    { 970,  0,   9},
    { 494,  0,   9},
    { 799,  0,  10},
    { 987,  0,  10},
    {1061,  0,  11},
    { 988,  0,  11},
    {1217,  0,  12},
    {1398,  0,  12},
    { 811,  0,  13},
    {1396,  0,  13},
    {1074,  0,  14},
    {1397,  0,  14},
    { 434,  0,  15},
    { 314,  0,  15},
    { 402,  0,  15},
    { 572,  0,  16},
    { 353,  0,  16},
    {1118,  0,  17},
    { 403,  0,  17},
    {1252,  0,  18},
    { 444,  0,  18},
    { 473,  0,  19},
    {1083,  0,  19},
    {1041,  0,  20},
    {1121,  0,  20},
    { 399,  0,  21},
    {1086,  0,  21},
    { 419,  0,  22},
    {1081,  0,  22},
    {1062,  0,  23},
    {1104,  0,  23},
    { 896,  0,  24},
    {1201,  0,  24},
    { 448,  0,  25},
    {1170,  0,  25},
    { 939,  0,  26},
    {1200,  0,  26},
    {1063,  0,  27},
    {1206,  0,  27},
    { 697,  0,  28},
    {1101,  0,  28},
    { 567,  0,  29},
    {1088,  0,  29},
    {1051,  0,  30},
    { 296,  0,  30},
    { 297,  0,  30},
    { 797,  0,  31},
    { 760,  0,  31},
    { 761,  0,  31},
    { 889,  0,  32},
    { 835,  0,  32},
    { 410,  0,  32},
    { 836,  0,  32},
    {1008,  0,  33},
    { 959,  0,  33},
    { 960,  0,  33},
    {1125,  0,  34},
    {1069,  0,  34},
    {1124,  0,  34},
    {1070,  0,  34},
    {1259,  0,  35},
    {1159,  0,  35},
    {1160,  0,  35},
    {1183,  0,  36},
    {1389,  0,  36},
    {1390,  0,  36},
    { 310,  0,  37},
    { 785,  0,  37},
    { 217,  0,  38},
    { 989,  1,   0},
    { 967,  1,   0},
    { 240,  1,   1},
    { 215,  1,   1},
    { 770,  1,   2},
    { 769,  1,   2},
    { 768,  1,   2},
    { 777,  1,   3},
    { 771,  1,   3},
    { 779,  1,   4},
    { 773,  1,   4},
    { 707,  1,   5},
    { 706,  1,   5},
    {1219,  1,   6},
    { 938,  1,   6},
    { 405,  1,   7},
    { 490,  1,   7},
    { 614,  1,   8},
    { 613,  1,   8},
    { 457,  1,   9},
    { 465,  1,  10},
    { 464,  1,  10},
    { 466,  1,  10},
    { 211,  1,  11},
    { 653,  1,  12},
    { 198,  1,  13},
    {1261,  1,  14},
    { 210,  1,  15},
    { 209,  1,  15},
    {1297,  1,  16},
    { 985,  1,  17},
    {1164,  1,  18},
    { 856,  1,  19},
    {1263,  1,  20},
    {1262,  1,  20},
    { 200,  1,  21},
    { 199,  1,  21},
    { 484,  1,  22},
    { 252,  1,  23},
    { 623,  1,  24},
    { 620,  1,  25},
    {1043,  1,  26},
    {1280,  1,  27},
    {1290,  1,  28},
    { 740,  1,  29},
    { 843,  1,  30},
    {1198,  1,  31},
    {1298,  1,  32},
    { 765,  1,  33},
    {1299,  1,  34},
    { 953,  1,  35},
    { 589,  1,  36},
    { 638,  1,  37},
    { 712,  1,  37},
    { 543,  1,  38},
    { 549,  1,  39},
    { 548,  1,  39},
    { 362,  1,  40},
    {1325,  1,  41},
    {1319,  1,  41},
    { 301,  1,  41},
    {1022,  1,  42},
    {1157,  1,  43},
    {1266,  1,  44},
    { 648,  1,  45},
    { 292,  1,  46},
    {1268,  1,  47},
    { 750,  1,  48},
    { 943,  1,  49},
    {1326,  1,  50},
    {1320,  1,  50},
    { 802,  1,  51},
    {1271,  1,  52},
    { 974,  1,  53},
    { 751,  1,  54},
    { 290,  1,  55},
    {1272,  1,  56},
    { 406,  1,  57},
    { 491,  1,  57},
    { 235,  1,  58},
    {1229,  1,  59},
    { 243,  1,  60},
    { 796,  1,  61},
    {1026,  1,  62},
    { 463,  1,  63},
    { 460,  1,  63},
    { 591,  1,  64},
    { 590,  1,  64},
    {1231,  1,  65},
    {1230,  1,  65},
    {1340,  1,  66},
    {1339,  1,  66},
    {1098,  1,  67},
    {1097,  1,  67},
    {1099,  1,  68},
    {1100,  1,  68},
    { 408,  1,  69},
    { 493,  1,  69},
    { 778,  1,  70},
    { 772,  1,  70},
    { 616,  1,  71},
    { 615,  1,  71},
    { 584,  1,  72},
    {1125,  1,  72},
    {1238,  1,  73},
    {1237,  1,  73},
    { 449,  1,  74},
    { 407,  1,  75},
    { 492,  1,  75},
    { 411,  1,  75},
    { 798,  1,  76},
    {1009,  1,  77},
    { 214,  1,  78},
    { 894,  1,  79},
    { 895,  1,  79},
    { 927,  1,  80},
    { 932,  1,  80},
    { 435,  1,  81},
    {1042,  1,  82},
    {1019,  1,  82},
    { 532,  1,  83},
    { 531,  1,  83},
    { 277,  1,  84},
    { 267,  1,  85},
    { 585,  1,  86},
    { 924,  1,  87},
    { 931,  1,  87},
    { 495,  1,  88},
    { 922,  1,  89},
    { 928,  1,  89},
    {1240,  1,  90},
    {1233,  1,  90},
    { 284,  1,  91},
    { 283,  1,  91},
    {1241,  1,  92},
    {1234,  1,  92},
    { 923,  1,  93},
    { 929,  1,  93},
    {1243,  1,  94},
    {1239,  1,  94},
    { 925,  1,  95},
    { 921,  1,  95},
    { 596,  1,  96},
    { 780,  1,  97},
    { 774,  1,  97},
    { 437,  1,  98},
    { 593,  1,  99},
    { 592,  1,  99},
    {1301,  1, 100},
    { 546,  1, 101},
    { 544,  1, 101},
    { 461,  1, 102},
    { 458,  1, 102},
    {1244,  1, 103},
    {1250,  1, 103},
    { 385,  1, 104},
    { 384,  1, 104},
    { 739,  1, 105},
    { 738,  1, 105},
    { 678,  1, 106},
    { 674,  1, 106},
    { 388,  1, 107},
    { 387,  1, 107},
    { 664,  1, 108},
    { 742,  1, 109},
    { 270,  1, 110},
    { 637,  1, 111},
    { 416,  1, 111},
    { 737,  1, 112},
    { 272,  1, 113},
    { 271,  1, 113},
    { 386,  1, 114},
    { 745,  1, 115},
    { 743,  1, 115},
    { 536,  1, 116},
    { 535,  1, 116},
    { 372,  1, 117},
    { 370,  1, 117},
    { 390,  1, 118},
    { 378,  1, 118},
    {1384,  1, 119},
    {1383,  1, 119},
    { 389,  1, 120},
    { 369,  1, 120},
    {1386,  1, 121},
    {1385,  1, 122},
    { 812,  1, 123},
    {1334,  1, 124},
    { 462,  1, 125},
    { 459,  1, 125},
    { 237,  1, 126},
    { 940,  1, 127},
    { 781,  1, 128},
    { 775,  1, 128},
    {1258,  1, 129},
    { 413,  1, 130},
    { 689,  1, 130},
    {1090,  1, 131},
    {1168,  1, 132},
    { 486,  1, 133},
    { 485,  1, 133},
    { 746,  1, 134},
    {1140,  1, 135},
    { 639,  1, 136},
    { 713,  1, 136},
    { 716,  1, 137},
    { 957,  1, 138},
    { 955,  1, 138},
    { 355,  1, 139},
    { 956,  1, 140},
    { 954,  1, 140},
    {1273,  1, 141},
    { 909,  1, 142},
    { 908,  1, 142},
    { 547,  1, 143},
    { 545,  1, 143},
    { 782,  1, 144},
    { 776,  1, 144},
    { 364,  1, 145},
    { 363,  1, 145},
    { 907,  1, 146},
    { 641,  1, 147},
    { 636,  1, 147},
    { 640,  1, 148},
    { 714,  1, 148},
    { 662,  1, 149},
    { 660,  1, 150},
    { 661,  1, 150},
    { 821,  1, 151},
    {1119,  1, 152},
    {1123,  1, 152},
    {1118,  1, 152},
    { 374,  1, 153},
    { 376,  1, 153},
    { 186,  1, 154},
    { 185,  1, 154},
    { 207,  1, 155},
    { 205,  1, 155},
    {1337,  1, 156},
    {1352,  1, 156},
    {1343,  1, 157},
    { 409,  1, 158},
    { 630,  1, 158},
    { 373,  1, 159},
    { 371,  1, 159},
    {1204,  1, 160},
    {1203,  1, 160},
    { 208,  1, 161},
    { 206,  1, 161},
    { 632,  1, 162},
    { 629,  1, 162},
    {1220,  1, 163},
    { 808,  1, 164},
    { 807,  1, 165},
    { 167,  1, 166},
    { 193,  1, 167},
    { 194,  1, 168},
    {1092,  1, 169},
    {1091,  1, 169},
    { 832,  1, 170},
    { 307,  1, 171},
    { 438,  1, 172},
    {1029,  1, 173},
    { 604,  1, 174},
    {1031,  1, 175},
    {1322,  1, 176},
    {1032,  1, 177},
    { 482,  1, 178},
    {1187,  1, 179},
    {1050,  1, 180},
    {1047,  1, 181},
    { 520,  1, 182},
    { 312,  1, 183},
    { 805,  1, 184},
    { 456,  1, 185},
    { 687,  1, 186},
    {1073,  1, 187},
    { 962,  1, 188},
    { 650,  1, 189},
    {1096,  1, 190},
    { 834,  1, 191},
    { 915,  1, 192},
    { 914,  1, 193},
    { 749,  1, 194},
    {1034,  1, 195},
    {1030,  1, 196},
    { 859,  1, 197},
    { 229,  1, 198},
    { 701,  1, 199},
    { 700,  1, 200},
    {1122,  1, 201},
    {1035,  1, 202},
    {1028,  1, 203},
    { 644,  1, 204},
    {1156,  1, 205},
    {1155,  1, 205},
    {1033,  1, 206},
    {1209,  1, 207},
    { 280,  1, 208},
    { 729,  1, 209},
    {1212,  1, 210},
    { 354,  1, 211},
    { 837,  1, 212},
    {1186,  1, 213},
    {1199,  1, 214},
    { 754,  1, 215},
    { 950,  1, 216},
    { 755,  1, 217},
    { 606,  1, 218},
    { 972,  1, 219},
    {1303,  1, 220},
    {1193,  1, 221},
    { 936,  1, 222},
    { 945,  1, 223},
    { 944,  1, 223},
    {1277,  1, 224},
    { 173,  1, 225},
    { 497,  1, 226},
    {1356,  1, 227},
    {1392,  1, 228},
    {1214,  1, 229},
    {1080,  1, 230},
    { 254,  1, 231},
    { 888,  1, 232},
    { 890,  1, 233},
    { 622,  1, 234},
    { 842,  1, 235},
    { 445,  1, 236},
    { 447,  1, 237},
    { 446,  1, 237},
    { 511,  1, 238},
    { 518,  1, 239},
    { 190,  1, 240},
    { 239,  1, 241},
    { 238,  1, 241},
    { 946,  1, 242},
    { 242,  1, 243},
    {1071,  1, 244},
    { 903,  1, 245},
    { 916,  1, 246},
    { 680,  1, 247},
    { 679,  1, 247},
    {1283,  1, 248},
    {1284,  1, 249},
    { 735,  1, 250},
    { 734,  1, 250},
    { 733,  1, 251},
    { 732,  1, 251},
    {1015,  1, 252},
    { 508,  1, 253},
    {1190,  1, 254},
    { 295,  1, 255},
    { 294,  1, 255},
    { 952,  1, 256},
    { 951,  1, 256},
    { 192,  1, 257},
    { 191,  1, 257},
    { 897,  1, 258},
    {1275,  1, 259},
    {1274,  1, 259},
    { 440,  1, 260},
    { 439,  1, 260},
    { 893,  1, 261},
    { 892,  1, 261},
    {1253,  1, 262},
    { 598,  1, 263},
    { 597,  1, 263},
    { 911,  1, 264},
    { 165,  1, 265},
    { 691,  1, 266},
    { 203,  1, 267},
    { 202,  1, 267},
    { 840,  1, 268},
    { 839,  1, 268},
    { 499,  1, 269},
    { 498,  1, 269},
    {1102,  1, 270},
    { 533,  1, 271},
    { 534,  1, 271},
    { 538,  1, 272},
    { 537,  1, 272},
    { 926,  1, 273},
    { 930,  1, 273},
    { 528,  1, 274},
    {1045,  1, 275},
    {1316,  1, 276},
    {1315,  1, 276},
    { 179,  1, 277},
    { 178,  1, 277},
    { 587,  1, 278},
    { 586,  1, 278},
    {1242,  1, 279},
    {1235,  1, 279},
    {1245,  1, 280},
    {1251,  1, 280},
    { 365,  1, 281},
    { 391,  1, 282},
    { 379,  1, 282},
    { 392,  1, 283},
    { 380,  1, 283},
    { 393,  1, 284},
    { 381,  1, 284},
    { 394,  1, 285},
    { 382,  1, 285},
    { 395,  1, 286},
    { 383,  1, 286},
    { 375,  1, 287},
    { 377,  1, 287},
    {1269,  1, 288},
    {1338,  1, 289},
    {1353,  1, 289},
    {1246,  1, 290},
    {1248,  1, 290},
    {1247,  1, 291},
    {1249,  1, 291},
    {1328,  2,   0},
    {1403,  2,   0},
    { 412,  2,   1},
    {1402,  2,   1},
    { 767,  2,   2},
    { 783,  2,   2},
    { 613,  2,   3},
    { 617,  2,   3},
    { 457,  2,   4},
    { 467,  2,   4},
    { 211,  2,   5},
    { 213,  2,   5},
    { 653,  2,   6},
    { 652,  2,   6},
    { 198,  2,   7},
    { 197,  2,   7},
    {1261,  2,   8},
    {1260,  2,   8},
    {1297,  2,   9},
    {1296,  2,   9},
    { 484,  2,  10},
    { 483,  2,  10},
    { 252,  2,  11},
    { 251,  2,  11},
    { 623,  2,  12},
    { 624,  2,  12},
    { 620,  2,  13},
    { 621,  2,  13},
    {1043,  2,  14},
    {1046,  2,  14},
    {1280,  2,  15},
    {1281,  2,  15},
    {1290,  2,  16},
    {1289,  2,  16},
    { 740,  2,  17},
    { 756,  2,  17},
    { 843,  2,  18},
    { 934,  2,  18},
    {1198,  2,  19},
    {1197,  2,  19},
    {1298,  2,  20},
    { 765,  2,  21},
    { 766,  2,  21},
    {1299,  2,  22},
    {1300,  2,  22},
    { 953,  2,  23},
    { 958,  2,  23},
    { 589,  2,  24},
    { 588,  2,  24},
    { 636,  2,  25},
    { 635,  2,  25},
    { 543,  2,  26},
    { 542,  2,  26},
    { 362,  2,  27},
    { 361,  2,  27},
    { 300,  2,  28},
    { 304,  2,  28},
    {1022,  2,  29},
    {1021,  2,  29},
    {1157,  2,  30},
    {1158,  2,  30},
    { 750,  2,  31},
    { 752,  2,  31},
    { 943,  2,  32},
    { 942,  2,  32},
    { 664,  2,  33},
    { 663,  2,  33},
    { 742,  2,  34},
    { 731,  2,  34},
    { 270,  2,  35},
    { 269,  2,  35},
    { 634,  2,  36},
    { 643,  2,  36},
    {1381,  2,  37},
    {1382,  2,  37},
    {1029,  2,  38},
    { 711,  2,  38},
    { 604,  2,  39},
    { 603,  2,  39},
    { 482,  2,  40},
    { 504,  2,  40},
    { 694,  2,  41},
    {1395,  2,  41},
    {1128,  2,  41},
    {1266,  2,  42},
    {1295,  2,  42},
    { 648,  2,  43},
    { 647,  2,  43},
    { 292,  2,  44},
    { 291,  2,  44},
    {1268,  2,  45},
    {1267,  2,  45},
    { 802,  2,  46},
    { 801,  2,  46},
    {1271,  2,  47},
    {1278,  2,  47},
    { 806,  2,  48},
    { 804,  2,  48},
    {1322,  2,  49},
    {1321,  2,  49},
    {1187,  2,  50},
    {1188,  2,  50},
    {1050,  2,  51},
    {1049,  2,  51},
    { 455,  2,  52},
    { 442,  2,  52},
    { 283,  2,  53},
    { 282,  2,  53},
    { 290,  2,  54},
    { 289,  2,  54},
    { 437,  2,  55},
    { 436,  2,  55},
    {1127,  2,  55},
    { 974,  2,  56},
    {1279,  2,  56},
    { 596,  2,  57},
    { 595,  2,  57},
    {1301,  2,  58},
    {1294,  2,  58},
    {1258,  2,  59},
    {1257,  2,  59},
    {1032,  2,  60},
    {1373,  2,  60},
    { 749,  2,  61},
    { 748,  2,  61},
    { 235,  2,  62},
    { 234,  2,  62},
    { 445,  2,  63},
    {1374,  2,  63},
    {1096,  2,  64},
    {1095,  2,  64},
    {1090,  2,  65},
    {1089,  2,  65},
    { 985,  2,  66},
    { 986,  2,  66},
    {1229,  2,  67},
    {1228,  2,  67},
    { 796,  2,  68},
    { 795,  2,  68},
    {1026,  2,  69},
    {1027,  2,  69},
    {1334,  2,  70},
    {1335,  2,  70},
    {1168,  2,  71},
    {1167,  2,  71},
    { 746,  2,  72},
    { 730,  2,  72},
    {1140,  2,  73},
    {1149,  2,  73},
    { 832,  2,  74},
    { 831,  2,  74},
    { 307,  2,  75},
    { 306,  2,  75},
    { 834,  2,  76},
    { 833,  2,  76},
    { 355,  2,  77},
    {1272,  2,  78},
    { 764,  2,  78},
    {1273,  2,  79},
    {1285,  2,  79},
    { 229,  2,  80},
    { 230,  2,  80},
    { 518,  2,  81},
    { 517,  2,  81},
    {1164,  2,  82},
    {1165,  2,  82},
    { 812,  2,  83},
    { 237,  2,  84},
    { 236,  2,  84},
    { 716,  2,  85},
    { 715,  2,  85},
    { 907,  2,  86},
    { 948,  2,  86},
    { 687,  2,  87},
    { 212,  2,  87},
    {1034,  2,  88},
    {1166,  2,  88},
    { 701,  2,  89},
    {1120,  2,  89},
    { 700,  2,  90},
    {1093,  2,  90},
    {1035,  2,  91},
    {1044,  2,  91},
    { 729,  2,  92},
    { 758,  2,  92},
    { 243,  2,  93},
    { 244,  2,  93},
    { 280,  2,  94},
    { 279,  2,  94},
    { 856,  2,  95},
    { 855,  2,  95},
    { 354,  2,  96},
    { 298,  2,  96},
    { 914,  2,  97},
    { 912,  2,  97},
    { 915,  2,  98},
    { 913,  2,  98},
    { 916,  2,  99},
    {1103,  2,  99},
    {1186,  2, 100},
    {1191,  2, 100},
    {1212,  2, 101},
    {1211,  2, 101},
    {1277,  2, 102},
    {1276,  2, 102},
    { 312,  2, 103},
    { 171,  2, 103},
    { 242,  2, 104},
    { 241,  2, 104},
    { 508,  2, 105},
    { 507,  2, 105},
    { 520,  2, 106},
    { 519,  2, 106},
    { 606,  2, 107},
    { 605,  2, 107},
    {1071,  2, 108},
    { 667,  2, 108},
    { 754,  2, 109},
    { 753,  2, 109},
    { 805,  2, 110},
    { 803,  2, 110},
    { 837,  2, 111},
    { 838,  2, 111},
    { 859,  2, 112},
    { 858,  2, 112},
    { 911,  2, 113},
    { 910,  2, 113},
    { 936,  2, 114},
    { 946,  2, 115},
    { 947,  2, 115},
    {1030,  2, 116},
    { 965,  2, 116},
    { 962,  2, 117},
    { 968,  2, 117},
    {1073,  2, 118},
    {1072,  2, 118},
    {1080,  2, 119},
    {1079,  2, 119},
    {1031,  2, 120},
    {1087,  2, 120},
    {1122,  2, 121},
    {1094,  2, 121},
    {1193,  2, 122},
    {1192,  2, 122},
    { 755,  2, 123},
    {1195,  2, 123},
    {1303,  2, 124},
    {1302,  2, 124},
    {1356,  2, 125},
    {1355,  2, 125},
    { 173,  2, 126},
    { 190,  2, 127},
    { 666,  2, 127},
    { 650,  2, 128},
    { 649,  2, 128},
    { 950,  2, 129},
    { 949,  2, 129},
    {1028,  2, 130},
    { 670,  2, 130},
    {1194,  2, 131},
    {1185,  2, 131},
    { 165,  2, 132},
    { 166,  2, 132},
    { 254,  2, 133},
    { 255,  2, 133},
    { 888,  2, 134},
    { 887,  2, 134},
    { 972,  2, 135},
    {1047,  2, 136},
    {1048,  2, 136},
    {1283,  2, 137},
    {1282,  2, 137},
    { 890,  2, 138},
    { 602,  2, 138},
    {1015,  2, 139},
    {1003,  2, 139},
    {1214,  2, 140},
    {1213,  2, 140},
    {1392,  2, 141},
    {1393,  2, 141},
    { 497,  2, 142},
    { 496,  2, 142},
    { 622,  2, 143},
    { 601,  2, 143},
    { 842,  2, 144},
    { 841,  2, 144},
    { 903,  2, 145},
    { 904,  2, 145},
    { 644,  2, 146},
    {1153,  2, 146},
    {1209,  2, 147},
    {1208,  2, 147},
    {1033,  2, 148},
    {1210,  2, 148},
    { 744,  2, 149},
    { 668,  2, 149},
    {1051,  3,   0},
    {1375,  3,   0},
    { 502,  3,   1},
    { 503,  3,   1},
    {1196,  3,   2},
    {1221,  3,   2},
    { 654,  3,   3},
    { 665,  3,   3},
    { 443,  3,   4},
    { 800,  3,   5},
    { 973,  3,   6},
    { 987,  3,   6},
    { 556,  3,   7},
    {1137,  3,   8},
    {1142,  3,   8},
    { 572,  3,   9},
    { 570,  3,   9},
    { 742,  3,  10},
    { 727,  3,  10},
    { 181,  3,  11},
    { 786,  3,  11},
    { 917,  3,  12},
    { 933,  3,  12},
    { 918,  3,  13},
    { 935,  3,  13},
    { 919,  3,  14},
    { 899,  3,  14},
    {1011,  3,  15},
    {1006,  3,  15},
    { 559,  3,  16},
    { 553,  3,  16},
    {1400,  3,  17},
    {1366,  3,  18},
    { 514,  3,  19},
    { 513,  3,  19},
    { 515,  3,  20},
    { 516,  3,  20},
    { 522,  3,  21},
    { 521,  3,  21},
    { 600,  3,  22},
    { 579,  3,  22},
    {1051,  4,   0},
    {1375,  4,   0},
    {1115,  4,   1},
    {1112,  4,   1},
    { 443,  4,   2},
    { 800,  4,   3},
    { 434,  4,   4},
    { 401,  4,   4},
    { 556,  4,   5},
    { 553,  4,   5},
    {1137,  4,   6},
    {1142,  4,   6},
    {1218,  4,   7},
    {1201,  4,   7},
    { 760,  4,   8},
    {1333,  4,   9},
    {1265,  4,  10},
    { 827,  4,  11},
    { 829,  4,  12},
    {1400,  4,  13},
    { 514,  4,  14},
    { 513,  4,  14},
    { 515,  4,  15},
    { 516,  4,  15},
    { 522,  4,  16},
    { 521,  4,  16},
    { 600,  4,  17},
    { 579,  4,  17},
    {1051,  5,   0},
    {1375,  5,   0},
    { 443,  5,   1},
    { 800,  5,   2},
    { 556,  5,   3},
    { 553,  5,   3},
    {1182,  5,   4},
    {1176,  5,   4},
    { 572,  5,   5},
    { 570,  5,   5},
    {1215,  5,   6},
    { 818,  5,   7},
    { 815,  5,   7},
    {1330,  5,   8},
    {1329,  5,   8},
    {1036,  5,   9},
    { 786,  5,   9},
    {1011,  5,  10},
    {1006,  5,  10},
    { 223,  5,  11},
    { 218,  5,  11},
    {1225,  5,  12},
    {1224,  5,  12},
    { 397,  5,  13},
    { 396,  5,  13},
    {1171,  5,  14},
    {1170,  5,  14},
    { 988,  6,   0},
    { 959,  6,   0},
    { 560,  6,   0},
    { 561,  6,   0},
    {1380,  6,   1},
    {1376,  6,   1},
    {1265,  6,   1},
    {1317,  6,   1},
    { 999,  7,   0},
    { 961,  7,   0},
    { 787,  7,   1},
    { 760,  7,   1},
    {1350,  7,   2},
    {1333,  7,   2},
    {1313,  7,   3},
    {1265,  7,   3},
    { 828,  7,   4},
    { 827,  7,   4},
    { 830,  7,   5},
    { 829,  7,   5},
    { 791,  8,   0},
    { 760,  8,   0},
    {1145,  8,   1},
    {1135,  8,   1},
    { 550,  8,   2},
    { 529,  8,   2},
    { 551,  8,   3},
    { 540,  8,   3},
    { 552,  8,   4},
    { 541,  8,   4},
    { 204,  8,   5},
    { 189,  8,   5},
    { 414,  8,   6},
    { 444,  8,   6},
    {1074,  8,   7},
    { 231,  8,   7},
    {1178,  8,   8},
    {1159,  8,   8},
    {1359,  8,   9},
    {1365,  8,   9},
    {1060,  8,  10},
    {1039,  8,  10},
    { 276,  8,  11},
    { 268,  8,  11},
    { 996,  8,  12},
    {1004,  8,  12},
    { 201,  8,  13},
    { 176,  8,  13},
    { 794,  8,  14},
    { 824,  8,  14},
    {1148,  8,  15},
    {1152,  8,  15},
    { 792,  8,  16},
    { 822,  8,  16},
    {1146,  8,  17},
    {1150,  8,  17},
    {1105,  8,  18},
    {1084,  8,  18},
    { 793,  8,  19},
    { 823,  8,  19},
    {1147,  8,  20},
    {1151,  8,  20},
    { 569,  8,  21},
    { 575,  8,  21},
    {1106,  8,  22},
    {1085,  8,  22},
    {1000,  9,   0},
    {   1,  9,   0},
    {1001,  9,   0},
    {1067,  9,   1},
    {   2,  9,   1},
    {1066,  9,   1},
    {1007,  9,   2},
    { 137,  9,   2},
    { 984,  9,   2},
    { 736,  9,   3},
    { 146,  9,   3},
    { 759,  9,   3},
    {1344,  9,   4},
    { 153,  9,   4},
    {1351,  9,   4},
    { 316,  9,   5},
    {  17,  9,   5},
    { 319,  9,   6},
    {  29,  9,   6},
    { 321,  9,   7},
    {  33,  9,   7},
    { 324,  9,   8},
    {  36,  9,   8},
    { 328,  9,   9},
    {  41,  9,   9},
    { 329,  9,  10},
    {  42,  9,  10},
    { 330,  9,  11},
    {  44,  9,  11},
    { 331,  9,  12},
    {  45,  9,  12},
    { 332,  9,  13},
    {  47,  9,  13},
    { 333,  9,  14},
    {  48,  9,  14},
    { 334,  9,  15},
    {  52,  9,  15},
    { 335,  9,  16},
    {  59,  9,  16},
    { 336,  9,  17},
    {  64,  9,  17},
    { 337,  9,  18},
    {  70,  9,  18},
    { 338,  9,  19},
    {  75,  9,  19},
    { 339,  9,  20},
    {  77,  9,  20},
    { 340,  9,  21},
    {  78,  9,  21},
    { 341,  9,  22},
    {  79,  9,  22},
    { 342,  9,  23},
    {  80,  9,  23},
    { 343,  9,  24},
    {  81,  9,  24},
    { 344,  9,  25},
    {  90,  9,  25},
    { 345,  9,  26},
    {  95,  9,  26},
    { 346,  9,  27},
    {  96,  9,  27},
    { 347,  9,  28},
    {  97,  9,  28},
    { 348,  9,  29},
    {  98,  9,  29},
    { 349,  9,  30},
    {  99,  9,  30},
    { 350,  9,  31},
    { 100,  9,  31},
    { 351,  9,  32},
    { 152,  9,  32},
    { 352,  9,  33},
    { 160,  9,  33},
    { 317,  9,  34},
    {  27,  9,  34},
    { 318,  9,  35},
    {  28,  9,  35},
    { 320,  9,  36},
    {  32,  9,  36},
    { 322,  9,  37},
    {  34,  9,  37},
    { 323,  9,  38},
    {  35,  9,  38},
    { 325,  9,  39},
    {  38,  9,  39},
    { 326,  9,  40},
    {  39,  9,  40},
    { 226,  9,  41},
    {  58,  9,  41},
    { 221,  9,  41},
    { 224,  9,  42},
    {  60,  9,  42},
    { 219,  9,  42},
    { 225,  9,  43},
    {  61,  9,  43},
    { 220,  9,  43},
    { 249,  9,  44},
    {  63,  9,  44},
    { 263,  9,  44},
    { 248,  9,  45},
    {  65,  9,  45},
    { 231,  9,  45},
    { 250,  9,  46},
    {  66,  9,  46},
    { 278,  9,  46},
    { 788,  9,  47},
    {  67,  9,  47},
    { 760,  9,  47},
    {1143,  9,  48},
    {  68,  9,  48},
    {1135,  9,  48},
    { 163,  9,  49},
    {  69,  9,  49},
    { 176,  9,  49},
    { 162,  9,  50},
    {  71,  9,  50},
    { 161,  9,  50},
    { 164,  9,  51},
    {  72,  9,  51},
    { 196,  9,  51},
    { 501,  9,  52},
    {  73,  9,  52},
    { 474,  9,  52},
    { 500,  9,  53},
    {  74,  9,  53},
    { 469,  9,  53},
    { 705,  9,  54},
    {  76,  9,  54},
    { 708,  9,  54},
    { 327,  9,  55},
    {  40,  9,  55},
    { 227,  9,  56},
    {  53,  9,  56},
    { 222,  9,  56},
    { 993, 10,   0},
    { 302, 10,   1},
    { 299, 10,   1},
    { 415, 10,   2},
    { 404, 10,   2},
    { 571, 10,   3},
    { 990, 10,   4},
    { 967, 10,   4},
    { 696, 10,   5},
    { 695, 10,   5},
    { 905, 10,   6},
    { 902, 10,   6},
    { 566, 10,   7},
    { 565, 10,   7},
    { 710, 10,   8},
    { 709, 10,   8},
    { 367, 10,   9},
    { 530, 10,   9},
    {1236, 10,  10},
    {1232, 10,  10},
    {1227, 10,  11},
    {1342, 10,  12},
    {1341, 10,  12},
    {1360, 10,  13},
    { 966, 10,  14},
    { 964, 10,  14},
    {1202, 10,  15},
    {1205, 10,  15},
    {1223, 10,  16},
    {1222, 10,  16},
    { 574, 10,  17},
    { 573, 10,  17},
    { 971, 11,   0},
    { 959, 11,   0},
    { 188, 11,   1},
    { 161, 11,   1},
    { 631, 11,   2},
    { 625, 11,   2},
    {1360, 11,   3},
    {1354, 11,   3},
    { 576, 11,   4},
    { 560, 11,   4},
    { 966, 11,   5},
    { 961, 11,   5},
    { 991, 12,   0},
    { 175, 12,   1},
    { 177, 12,   2},
    { 180, 12,   3},
    { 247, 12,   4},
    { 253, 12,   5},
    { 470, 12,   6},
    { 471, 12,   7},
    { 509, 12,   8},
    { 564, 12,   9},
    { 568, 12,  10},
    { 577, 12,  11},
    { 578, 12,  12},
    { 628, 12,  13},
    { 633, 12,  14},
    {1288, 12,  14},
    { 651, 12,  15},
    { 655, 12,  16},
    { 656, 12,  17},
    { 657, 12,  18},
    { 728, 12,  19},
    { 741, 12,  20},
    { 757, 12,  21},
    { 762, 12,  22},
    { 763, 12,  23},
    { 906, 12,  24},
    { 920, 12,  25},
    { 998, 12,  26},
    {1014, 12,  27},
    {1086, 12,  28},
    {1129, 12,  29},
    {1130, 12,  30},
    {1139, 12,  31},
    {1141, 12,  32},
    {1162, 12,  33},
    {1163, 12,  34},
    {1177, 12,  35},
    {1179, 12,  36},
    {1189, 12,  37},
    {1254, 12,  38},
    {1270, 12,  39},
    {1286, 12,  40},
    {1287, 12,  41},
    {1293, 12,  42},
    {1357, 12,  43},
    {1264, 12,  44},
    {1377, 12,  45},
    {1378, 12,  46},
    {1379, 12,  47},
    {1387, 12,  48},
    {1388, 12,  49},
    {1391, 12,  50},
    {1394, 12,  51},
    { 747, 12,  52},
    { 563, 12,  53},
    { 293, 12,  54},
    { 562, 12,  55},
    {1017, 12,  56},
    {1154, 12,  57},
    {1226, 12,  58},
    { 860, 12,  59},
    { 861, 12,  60},
    { 862, 12,  61},
    { 863, 12,  62},
    { 864, 12,  63},
    { 865, 12,  64},
    { 866, 12,  65},
    { 867, 12,  66},
    { 868, 12,  67},
    { 869, 12,  68},
    { 870, 12,  69},
    { 871, 12,  70},
    { 872, 12,  71},
    { 873, 12,  72},
    { 874, 12,  73},
    { 875, 12,  74},
    { 876, 12,  75},
    { 877, 12,  76},
    { 878, 12,  77},
    { 879, 12,  78},
    { 880, 12,  79},
    { 881, 12,  80},
    { 882, 12,  81},
    { 883, 12,  82},
    { 884, 12,  83},
    { 885, 12,  84},
    { 886, 12,  85},
    { 168, 12,  86},
    { 170, 12,  87},
    { 169, 12,  88},
    { 848, 12,  89},
    { 845, 12,  90},
    { 851, 12,  91},
    { 854, 12,  92},
    { 849, 12,  93},
    { 850, 12,  94},
    { 844, 12,  95},
    { 852, 12,  96},
    { 846, 12,  97},
    { 847, 12,  98},
    { 853, 12,  99},
    { 646, 12, 100},
    { 645, 12, 101},
    { 995, 13,   0},
    {1318, 13,   0},
    { 720, 13,   1},
    { 296, 13,   1},
    { 506, 13,   2},
    { 468, 13,   2},
    {1144, 13,   3},
    {1135, 13,   3},
    { 790, 13,   4},
    { 760, 13,   4},
    {1314, 13,   5},
    {1265, 13,   5},
    {1328, 14,   0},
    {1375, 14,   0},
    {1041, 14,   1},
    {1040, 14,   1},
    { 399, 14,   2},
    { 396, 14,   2},
    {1133, 14,   3},
    {1132, 14,   3},
    { 599, 14,   4},
    { 594, 14,   4},
    { 997, 14,   5},
    {1002, 14,   5},
    { 554, 14,   6},
    { 553, 14,   6},
    { 288, 14,   7},
    {1255, 14,   7},
    { 693, 14,   8},
    { 708, 14,   8},
    {1114, 14,   9},
    {1113, 14,   9},
    {1111, 14,  10},
    {1104, 14,  10},
    {1011, 14,  11},
    {1006, 14,  11},
    { 184, 14,  12},
    { 176, 14,  12},
    { 677, 14,  13},
    { 673, 14,  13},
    { 702, 14,  14},
    { 688, 14,  14},
    { 703, 14,  14},
    { 672, 14,  15},
    { 671, 14,  15},
    { 410, 14,  16},
    { 400, 14,  16},
    { 286, 14,  17},
    { 245, 14,  17},
    { 285, 14,  18},
    { 233, 14,  18},
    {1216, 14,  19},
    {1215, 14,  19},
    { 857, 14,  20},
    { 262, 14,  20},
    { 308, 14,  21},
    { 443, 14,  21},
    { 810, 14,  22},
    { 800, 14,  22},
    { 433, 14,  23},
    { 313, 14,  23},
    { 417, 14,  24},
    {1161, 14,  24},
    { 188, 14,  25},
    { 174, 14,  25},
    { 287, 14,  26},
    { 232, 14,  26},
    {1252, 14,  27},
    {1184, 14,  27},
    {1401, 14,  28},
    {1399, 14,  28},
    { 975, 14,  29},
    { 987, 14,  29},
    {1364, 14,  30},
    {1361, 14,  30},
    { 718, 14,  31},
    { 726, 14,  32},
    { 725, 14,  33},
    { 626, 14,  34},
    { 627, 14,  35},
    { 398, 14,  36},
    { 441, 14,  36},
    { 654, 14,  37},
    { 665, 14,  37},
    { 418, 14,  38},
    { 368, 14,  38},
    {1137, 14,  39},
    {1142, 14,  39},
    { 514, 14,  40},
    { 513, 14,  40},
    { 522, 14,  41},
    { 521, 14,  41},
    {1400, 14,  42},
    { 993, 15,   0},
    {1011, 15,   1},
    {1006, 15,   1},
    { 494, 15,   2},
    { 487, 15,   2},
    { 476, 15,   3},
    { 475, 15,   3},
    { 963, 16,   0},
    {   0, 16,   1},
    {   1, 16,   2},
    {   6, 16,   3},
    {  11, 16,   4},
    {  89, 16,   5},
    {   8, 16,   6},
    {   5, 16,   7},
    {   4, 16,   8},
    {   3, 16,   9},
    {  16, 16,  10},
    {  15, 16,  11},
    {  14, 16,  12},
    {  85, 16,  13},
    {  13, 16,  14},
    {  83, 16,  15},
    {  12, 16,  16},
    {  10, 16,  17},
    {   9, 16,  18},
    {  88, 16,  19},
    {  51, 16,  20},
    { 122, 16,  21},
    {   7, 16,  22},
    { 138, 16,  23},
    {  87, 16,  24},
    { 125, 16,  25},
    {  50, 16,  26},
    {  86, 16,  27},
    { 105, 16,  28},
    { 124, 16,  29},
    { 140, 16,  30},
    {  30, 16,  31},
    {   2, 16,  32},
    {  84, 16,  33},
    {  49, 16,  34},
    { 123, 16,  35},
    {  82, 16,  36},
    { 139, 16,  37},
    { 104, 16,  38},
    { 154, 16,  39},
    { 121, 16,  40},
    {  31, 16,  41},
    { 131, 16,  42},
    {  37, 16,  43},
    { 137, 16,  44},
    {  43, 16,  45},
    { 146, 16,  46},
    {  46, 16,  47},
    { 153, 16,  48},
    {  17, 16,  49},
    {  29, 16,  50},
    {  33, 16,  51},
    {  36, 16,  52},
    {  41, 16,  53},
    {  42, 16,  54},
    {  44, 16,  55},
    {  45, 16,  56},
    {  47, 16,  57},
    {  48, 16,  58},
    {  52, 16,  59},
    {  59, 16,  60},
    {  64, 16,  61},
    {  70, 16,  62},
    {  75, 16,  63},
    {  77, 16,  64},
    {  78, 16,  65},
    {  79, 16,  66},
    {  80, 16,  67},
    {  81, 16,  68},
    {  90, 16,  69},
    {  95, 16,  70},
    {  96, 16,  71},
    {  97, 16,  72},
    {  98, 16,  73},
    {  99, 16,  74},
    { 100, 16,  75},
    { 101, 16,  76},
    { 102, 16,  77},
    { 103, 16,  78},
    { 106, 16,  79},
    { 111, 16,  80},
    { 112, 16,  81},
    { 113, 16,  82},
    { 115, 16,  83},
    { 116, 16,  84},
    { 117, 16,  85},
    { 118, 16,  86},
    { 119, 16,  87},
    { 120, 16,  88},
    { 126, 16,  89},
    { 132, 16,  90},
    { 141, 16,  91},
    { 147, 16,  92},
    { 155, 16,  93},
    {  18, 16,  94},
    {  53, 16,  95},
    {  91, 16,  96},
    { 107, 16,  97},
    { 127, 16,  98},
    { 133, 16,  99},
    { 142, 16, 100},
    { 148, 16, 101},
    { 156, 16, 102},
    {  19, 16, 103},
    {  54, 16, 104},
    {  92, 16, 105},
    { 108, 16, 106},
    { 128, 16, 107},
    { 134, 16, 108},
    { 143, 16, 109},
    { 149, 16, 110},
    { 157, 16, 111},
    {  20, 16, 112},
    {  55, 16, 113},
    {  93, 16, 114},
    { 109, 16, 115},
    { 129, 16, 116},
    { 135, 16, 117},
    { 144, 16, 118},
    { 150, 16, 119},
    { 158, 16, 120},
    {  21, 16, 121},
    {  56, 16, 122},
    {  62, 16, 123},
    {  94, 16, 124},
    { 110, 16, 125},
    { 114, 16, 126},
    { 130, 16, 127},
    { 136, 16, 128},
    { 145, 16, 129},
    { 151, 16, 130},
    { 159, 16, 131},
    {  22, 16, 132},
    {  23, 16, 133},
    {  57, 16, 134},
    {  24, 16, 135},
    {  25, 16, 136},
    {  26, 16, 137},
    { 961, 17,   0},
    {1143, 17,   1},
    { 788, 17,   2},
    {1346, 17,   3},
    { 789, 17,   4},
    {1307, 17,   5},
    { 273, 17,   6},
    {1308, 17,   7},
    {1312, 17,   8},
    {1310, 17,   9},
    {1311, 17,  10},
    { 275, 17,  11},
    { 274, 17,  12},
    {1309, 17,  13},
    {1068, 17,  14},
    {1051, 18,   0},
    { 261, 18,   1},
    {1345, 18,   2},
    { 228, 18,   3},
    {1007, 18,   4},
    {1344, 18,   5},
    {1126, 18,   6},
    { 704, 18,   7},
    {1349, 18,   8},
    {1348, 18,   9},
    {1347, 18,  10},
    { 427, 18,  11},
    { 420, 18,  12},
    { 421, 18,  13},
    { 432, 18,  14},
    { 429, 18,  15},
    { 428, 18,  16},
    { 424, 18,  17},
    { 431, 18,  18},
    { 430, 18,  19},
    { 426, 18,  20},
    { 422, 18,  21},
    { 423, 18,  22},
    { 941, 18,  23},
    {1305, 18,  24},
    {1306, 18,  25},
    { 582, 18,  26},
    { 305, 18,  27},
    {1138, 18,  28},
    {1256, 18,  29},
    { 425, 18,  30},
    { 994, 18,  31},
    { 722, 18,  32},
    {1010, 18,  33},
    {1008, 18,  34},
    { 281, 18,  35},
    { 988, 19,   0},
    {1380, 19,   1},
    {1380, 20,   0},
    {1376, 20,   0},
    { 988, 20,   1},
    { 959, 20,   1},
    {1380, 21,   0},
    {1376, 21,   0},
    { 988, 21,   1},
    { 959, 21,   1},
    { 898, 21,   2},
    { 835, 21,   2},
};

/* property values: 6172 bytes. */

/* Codepoints which expand on full case-folding. */

RE_UINT16 re_expand_on_folding[] = {
      223,   304,   329,   496,   912,   944,  1415,  7830,
     7831,  7832,  7833,  7834,  7838,  8016,  8018,  8020,
     8022,  8064,  8065,  8066,  8067,  8068,  8069,  8070,
     8071,  8072,  8073,  8074,  8075,  8076,  8077,  8078,
     8079,  8080,  8081,  8082,  8083,  8084,  8085,  8086,
     8087,  8088,  8089,  8090,  8091,  8092,  8093,  8094,
     8095,  8096,  8097,  8098,  8099,  8100,  8101,  8102,
     8103,  8104,  8105,  8106,  8107,  8108,  8109,  8110,
     8111,  8114,  8115,  8116,  8118,  8119,  8124,  8130,
     8131,  8132,  8134,  8135,  8140,  8146,  8147,  8150,
     8151,  8162,  8163,  8164,  8166,  8167,  8178,  8179,
     8180,  8182,  8183,  8188, 64256, 64257, 64258, 64259,
    64260, 64261, 64262, 64275, 64276, 64277, 64278, 64279,
};

/* expand_on_folding: 208 bytes. */

/* General_Category. */

static RE_UINT8 re_general_category_stage_1[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  9, 10, 11,  7,  7,  7,  7, 12, 13, 14, 14, 14, 15,
    16, 17, 18, 19, 20, 21, 22, 21, 23, 21, 21, 21, 21, 24,  7,  7,
    25, 26, 21, 21, 21, 21, 27, 28, 21, 21, 29, 30, 31, 32, 33, 34,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7, 35,  7, 36, 37,  7, 38,  7,  7,  7, 39, 21, 40,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    41, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 42,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 42,
};

static RE_UINT8 re_general_category_stage_2[] = {
      0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,
     16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  31,
     32,  33,  34,  34,  35,  36,  37,  38,  39,  34,  34,  34,  40,  41,  42,  43,
     44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,  56,  57,  58,  59,
     60,  61,  62,  63,  64,  64,  65,  66,  67,  68,  69,  70,  71,  69,  72,  73,
     69,  69,  64,  74,  64,  64,  75,  76,  77,  78,  79,  80,  81,  82,  69,  83,
     84,  85,  86,  87,  88,  89,  69,  69,  34,  34,  34,  34,  34,  34,  34,  34,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  90,  34,  34,  34,  34,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  91,
     92,  34,  34,  34,  34,  34,  34,  34,  34,  93,  34,  34,  94,  95,  96,  97,
     98,  99, 100, 101, 102, 103, 104, 105,  34,  34,  34,  34,  34,  34,  34,  34,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34, 106,
    107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107,
    108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108,
    108, 108,  34,  34, 109, 110, 111, 112,  34,  34, 113, 114, 115, 116, 117, 118,
    119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 123,  34,  34, 130, 123,
    131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 123, 142, 123, 143, 123,
    144, 145, 146, 147, 148, 149, 150, 123, 151, 152, 123, 153, 154, 155, 156, 123,
    157, 158, 123, 123, 159, 160, 123, 123, 161, 162, 163, 164, 123, 165, 123, 123,
     34,  34,  34,  34,  34,  34,  34, 166, 167,  34, 168, 123, 123, 123, 123, 123,
    123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123,
     34,  34,  34,  34,  34,  34,  34,  34, 169, 123, 123, 123, 123, 123, 123, 123,
    123, 123, 123, 123, 123, 123, 123, 123,  34,  34,  34,  34, 170, 123, 123, 123,
     34,  34,  34,  34, 171, 172, 173, 174, 123, 123, 123, 123, 175, 176, 177, 178,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34, 179,
     34,  34,  34,  34,  34, 180, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123,
     34,  34, 181,  34,  34, 182, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123,
    123, 123, 123, 123, 123, 123, 123, 123, 183, 184, 123, 123, 123, 123, 123, 123,
     69, 185, 186, 187, 188, 189, 190, 123, 191, 192, 193, 194, 195, 196, 197, 198,
     69,  69,  69,  69, 199, 200, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123,
    201, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123,
     34, 202, 203, 123, 123, 123, 123, 123, 204, 205, 123, 123, 206, 207, 123, 123,
    208, 209, 210, 211, 212, 123,  69, 213,  69,  69,  69,  69,  69, 214, 215, 216,
    217, 218, 219, 220, 221, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34, 222,  34,  34,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34, 223,  34,
    224,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34, 225,  34,  34,
     34,  34,  34,  34,  34,  34,  34, 226, 123, 123, 123, 123, 123, 123, 123, 123,
     34,  34,  34,  34, 227, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123,
    228, 123, 229, 230, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123,
    108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 231,
};

static RE_UINT16 re_general_category_stage_3[] = {
      0,   0,   1,   2,   3,   4,   5,   6,   0,   0,   7,   8,   9,  10,  11,  12,
     13,  13,  13,  14,  15,  13,  13,  16,  17,  18,  19,  20,  21,  22,  13,  23,
     13,  13,  13,  24,  25,  11,  11,  11,  11,  26,  11,  27,  28,  29,  30,  31,
     32,  32,  32,  32,  32,  32,  32,  33,  34,  35,  36,  11,  37,  38,  13,  39,
      9,   9,   9,  11,  11,  11,  13,  13,  40,  13,  13,  13,  41,  13,  13,  13,
     13,  13,  13,  42,   9,  43,  11,  11,  44,  45,  32,  46,  47,  48,  49,  50,
     51,  52,  48,  48,  53,  32,  54,  55,  48,  48,  48,  48,  48,  56,  57,  58,
     59,  60,  48,  32,  61,  48,  48,  48,  48,  48,  62,  63,  64,  48,  65,  66,
     48,  67,  68,  69,  48,  70,  71,  72,  72,  72,  48,  73,  72,  74,  75,  32,
     76,  48,  48,  77,  78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,
     90,  83,  84,  91,  92,  93,  94,  95,  96,  97,  84,  98,  99, 100,  88, 101,
    102,  83,  84, 103, 104, 105,  88, 106, 107, 108, 109, 110, 111, 112,  94, 113,
    114, 115,  84, 116, 117, 118,  88, 119, 120, 115,  84, 121, 122, 123,  88, 124,
    125, 115,  48, 126, 127, 128,  88, 129, 130, 131,  48, 132, 133, 134,  94, 135,
    136,  48,  48, 137, 138, 139,  72,  72, 140, 141, 142, 143, 144, 145,  72,  72,
    146, 147, 148, 149, 150,  48, 151, 152, 153, 154,  32, 155, 156, 157,  72,  72,
     48,  48, 158, 159, 160, 161, 162, 163, 164, 165,   9,   9, 166,  11,  11, 167,
     48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48, 168, 169,  48,  48,
    168,  48,  48, 170, 171, 172,  48,  48,  48, 171,  48,  48,  48, 173, 174, 175,
     48, 176,   9,   9,   9,   9,   9, 177, 178,  48,  48,  48,  48,  48,  48,  48,
     48,  48,  48,  48,  48,  48, 179,  48, 180, 181,  48,  48,  48,  48, 182, 183,
    184, 185,  48, 186,  48, 187, 184, 188,  48,  48,  48, 189, 190, 191, 192, 193,
    194, 192,  48,  48, 195,  48,  48, 196, 197,  48, 198,  48,  48,  48,  48, 199,
     48, 200, 201, 202, 203,  48, 204, 205,  48,  48, 206,  48, 207, 208, 209, 209,
     48, 210,  48,  48,  48, 211, 212, 213, 192, 192, 214, 215,  72,  72,  72,  72,
    216,  48,  48, 217, 218, 160, 219, 220, 221,  48, 222,  64,  48,  48, 223, 224,
     48,  48, 225, 226, 227,  64,  48, 228, 229,   9,   9, 230, 231, 232, 233, 234,
     11,  11, 235,  27,  27,  27, 236, 237,  11, 238,  27,  27,  32,  32,  32, 239,
     13,  13,  13,  13,  13,  13,  13,  13,  13, 240,  13,  13,  13,  13,  13,  13,
    241, 242, 241, 241, 242, 243, 241, 244, 245, 245, 245, 246, 247, 248, 249, 250,
    251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 261,  72, 262, 263, 264,
    265, 266, 267, 268, 269, 270, 271, 271, 272, 273, 274, 209, 275, 276, 209, 277,
    278, 278, 278, 278, 278, 278, 278, 278, 279, 209, 280, 209, 209, 209, 209, 281,
    209, 282, 278, 283, 209, 284, 285, 209, 209, 209, 286,  72, 287,  72, 270, 270,
    270, 288, 209, 209, 209, 209, 289, 270, 209, 209, 209, 209, 209, 209, 209, 209,
    209, 209, 209, 290, 291, 209, 209, 292, 209, 209, 209, 209, 209, 209, 293, 209,
    209, 209, 209, 209, 209, 209, 294, 295, 270, 296, 209, 209, 297, 278, 298, 278,
    299, 300, 278, 278, 278, 301, 278, 302, 209, 209, 209, 278, 303, 209, 209, 304,
    209, 305, 209, 209, 306, 209, 209, 307,   9,   9, 308,  11,  11, 309, 310, 311,
     13,  13,  13,  13,  13,  13, 312, 313,  11,  11, 314,  48,  48,  48, 315, 316,
     48, 317, 318, 318, 318, 318,  32,  32, 319, 320, 321, 322, 323,  72,  72,  72,
    209, 324, 209, 209, 209, 209, 209, 325, 209, 209, 209, 209, 209, 326,  72, 327,
    328, 329, 330, 331, 136,  48,  48,  48,  48, 332, 178,  48,  48,  48,  48, 333,
    334,  48,  48, 136,  48,  48,  48,  48, 200, 335,  48,  71, 209, 209, 325,  48,
    209, 307, 336, 209, 337, 338, 209, 209, 336, 209, 209, 338, 209, 209, 209, 307,
     48,  48,  48, 199, 209, 209, 209, 209,  48,  48,  48,  48,  48,  48,  48,  72,
     48, 339,  48,  48,  48,  48,  48,  48, 151, 209, 209, 209, 286,  48,  48, 228,
    340,  48, 341,  72,  13,  13, 342, 343,  13, 344,  48,  48,  48,  48, 345, 346,
     31, 347, 348, 349,  13,  13,  13, 350, 351, 352, 353, 354,  72,  72,  72, 355,
    356,  48, 357, 358,  48,  48,  48, 359, 360,  48,  48, 361, 362, 192,  32, 363,
     64,  48, 364,  48, 365, 366,  48, 151,  76,  48,  48, 367, 368, 369, 370, 371,
     48,  48, 372, 373, 374, 375,  48, 376,  48,  48,  48, 377, 378, 379, 380, 381,
    382, 383, 318,  11,  11, 384, 385,  11,  11,  11,  11,  11,  48,  48, 386, 192,
     48,  48, 387,  48, 388,  48,  48, 206, 389, 389, 389, 389, 389, 389, 389, 389,
    390, 390, 390, 390, 390, 390, 390, 390,  48,  48,  48,  48,  48,  48, 204,  48,
     48,  48,  48,  48,  48, 207,  72,  72, 391, 392, 393, 394, 395,  48,  48,  48,
     48,  48,  48, 396, 397, 398,  48,  48,  48,  48,  48, 399,  72,  48,  48,  48,
     48, 400,  48,  48, 401,  72,  72, 402,  32, 403,  32, 404, 405, 406, 407, 408,
     48,  48,  48,  48,  48,  48,  48, 409, 410,   2,   3,   4,   5, 411, 412, 413,
     48, 414,  48, 200, 415, 416, 417, 418, 419,  48, 172, 420, 204, 204,  72,  72,
     48,  48,  48,  48,  48,  48,  48,  71, 421, 270, 270, 422, 271, 271, 271, 423,
    424, 327, 425,  72,  72, 209, 209, 426,  72,  72,  72,  72,  72,  72,  72,  72,
     48, 151,  48,  48,  48, 100, 427, 428,  48,  48, 429,  48, 430,  48,  48, 431,
     48, 432,  48,  48, 433, 434,  72,  72,   9,   9, 435,  11,  11,  48,  48,  48,
     48, 204, 192,   9,   9, 436,  11, 437,  48,  48, 401,  48,  48,  48, 438,  72,
     48,  48,  48, 317,  48, 199, 401,  72, 439,  48,  48, 440,  48, 441,  48, 442,
     48, 200, 443,  72,  72,  72,  48, 444,  48, 445,  48, 446,  72,  72,  72,  72,
     48,  48,  48, 447, 270, 448, 270, 270, 449, 450,  48, 451, 452, 453,  48, 454,
     48, 455,  72,  72, 456,  48, 457, 458,  48,  48,  48, 459,  48, 460,  48, 461,
     48, 462, 463,  72,  72,  72,  72,  72,  48,  48,  48,  48, 196,  72,  72,  72,
      9,   9,   9, 464,  11,  11,  11, 465,  48,  48, 466, 192,  72,  72,  72,  72,
     72,  72,  72,  72,  72,  72, 270, 467,  48, 455, 468,  48,  62, 469,  72,  72,
    470,  48,  48, 471, 472, 448, 473, 474, 221,  48,  48, 475, 476,  48, 196, 192,
    477,  48, 478, 479, 480,  48,  48, 481, 221,  48,  48, 482, 483, 484, 485, 486,
     48,  97, 487, 488,  72,  72,  72,  72, 489, 490, 491,  48,  48, 492, 493, 192,
    494,  83,  84, 495, 496, 497, 498, 499,  48,  48,  48, 500, 501, 502,  72,  72,
     48,  48,  48, 503, 504, 192,  72,  72,  48,  48, 505, 506, 507, 508,  72,  72,
     48,  48,  48, 509, 510, 192, 511,  72,  48,  48, 512, 513, 192,  72,  72,  72,
     48, 173, 514, 515,  72,  72,  72,  72,  48,  48, 487, 516,  72,  72,  72,  72,
     72,  72,   9,   9,  11,  11, 148, 517, 518,  48,  48, 519, 520, 521,  48,  48,
    522, 523, 524,  72,  48,  48,  48, 196,  84,  48, 505, 525, 526, 148, 175, 527,
     48, 528, 529, 530,  72,  72,  72,  72, 531,  48,  48, 532, 533, 192, 534,  48,
    535, 536, 192,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  48, 537,
     48, 207,  72,  72,  72,  72,  72,  72, 271, 271, 271, 271, 271, 271, 538, 539,
     48,  48,  48,  48, 387,  72,  72,  72,  48,  48, 200,  72,  72,  72,  72,  72,
     48,  48,  48,  48, 317,  72,  72,  72,  48,  48,  48, 196,  48, 200, 369,  72,
     72,  72,  72,  72,  72,  48, 204, 540,  48,  48,  48, 541, 542, 543, 544, 545,
     48,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,   9,   9,  11,  11,
    270, 546,  72,  72,  72,  72,  72,  72,  48,  48,  48,  48, 205, 547, 548, 549,
    474, 550,  72,  72,  72,  72, 551,  72,  48,  48,  48,  48,  48,  48,  48, 552,
     48,  48,  48,  48,  48,  48,  48, 553,  48, 200,  72,  72,  72,  72,  72,  48,
     48,  48,  48,  48,  48,  48,  48, 206,  48,  48,  48,  48,  48,  48,  71, 151,
    196, 554, 555,  72,  72,  72,  72,  72, 209, 209, 209, 209, 209, 209, 209, 326,
    209, 209, 556, 209, 209, 209, 557, 558, 559, 209, 560, 209, 209, 209, 561,  72,
    209, 209, 209, 209, 562,  72,  72,  72,  72,  72,  72,  72,  72,  72, 270, 563,
    209, 209, 209, 209, 209, 286, 270, 452,   9, 564,  11, 565, 566, 567, 241,   9,
    568, 569, 570, 571, 572,   9, 564,  11, 573, 574,  11, 575, 576, 577, 578,   9,
    579,  11,   9, 564,  11, 565, 566,  11, 241,   9, 568, 578,   9, 579,  11,   9,
    564,  11, 580,   9, 581, 582, 583, 584,  11, 585,   9, 586, 587, 588, 589,  11,
    590,   9, 591,  11, 592, 593, 593, 593,  32,  32,  32, 594,  32,  32, 595, 596,
    597, 598,  45,  72,  72,  72,  72,  72, 599, 600, 601,  72,  72,  72,  72,  72,
     48,  48,  48,  48, 602, 603,  72,  72,   9,   9, 568,  11, 604, 369,  72,  72,
     72,  72,  72,  72,  72,  72,  72, 485, 270, 270, 605, 606,  72,  72,  72,  72,
    607,  48, 608, 609, 610, 611, 612, 613, 614, 206, 615, 206,  72,  72,  72, 616,
    209, 209, 327, 209, 209, 209, 209, 209, 209, 325, 307, 617, 617, 617, 209, 326,
    175, 209, 209, 209, 209, 209, 327, 209, 209, 209, 618,  72,  72,  72, 619, 209,
    620, 209, 209, 327, 561, 621, 326,  72, 209, 209, 209, 209, 209, 209, 209, 622,
    209, 209, 209, 209, 209, 623, 618, 176, 209, 209, 209, 209, 209, 209, 209, 325,
    209, 209, 209, 209, 209, 561,  72,  72, 327, 209, 209, 209, 624, 176, 209, 209,
    624, 209, 625,  72,  72,  72,  72,  72, 327, 209, 209, 307, 209, 209, 209, 626,
    209, 209, 620, 176, 620, 209, 209, 209,  72,  72,  72,  72,  72,  72, 625,  72,
     48,  48,  48,  48,  48, 317,  72,  72,  48,  48,  48, 205,  48,  48,  48,  48,
     48, 204,  48,  48,  48,  48,  48,  48,  48,  48, 552,  48,  48,  48,  48,  48,
     48,  48,  48,  48,  48,  48, 100,  72,  48, 204,  72,  72,  72,  72,  72,  72,
    627,  72, 628, 628, 628, 628, 628, 628,  32,  32,  32,  32,  32,  32,  32,  32,
     32,  32,  32,  32,  32,  32,  32,  72, 390, 390, 390, 390, 390, 390, 390, 629,
};

static RE_UINT8 re_general_category_stage_4[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   1,   2,   3,   2,   4,   5,   6,   2,
      7,   7,   7,   7,   7,   2,   8,   9,  10,  11,  11,  11,  11,  11,  11,  11,
     11,  11,  11,  11,  11,  12,  13,  14,  15,  16,  16,  16,  16,  16,  16,  16,
     16,  16,  16,  16,  16,  17,  18,  19,   1,  20,  20,  21,  22,  23,  24,  25,
     26,  27,  15,   2,  28,  29,  27,  30,  11,  11,  11,  11,  11,  11,  11,  11,
     11,  11,  11,  31,  11,  11,  11,  32,  16,  16,  16,  16,  16,  16,  16,  16,
     16,  16,  16,  33,  16,  16,  16,  16,  32,  32,  32,  32,  32,  32,  32,  32,
     32,  32,  32,  32,  34,  34,  34,  34,  34,  34,  34,  34,  16,  32,  32,  32,
     32,  32,  32,  32,  11,  34,  34,  16,  34,  32,  32,  11,  34,  11,  16,  11,
     11,  34,  32,  11,  32,  16,  11,  34,  32,  32,  32,  11,  34,  16,  32,  11,
     34,  11,  34,  34,  32,  35,  32,  16,  36,  36,  37,  34,  38,  37,  34,  34,
     34,  34,  34,  34,  34,  34,  16,  32,  34,  38,  32,  11,  32,  32,  32,  32,
     32,  32,  16,  16,  16,  11,  34,  32,  34,  34,  11,  32,  32,  32,  32,  32,
     16,  16,  39,  16,  16,  16,  16,  16,  40,  40,  40,  40,  40,  40,  40,  40,
     40,  41,  41,  40,  40,  40,  40,  40,  40,  41,  41,  41,  41,  41,  41,  41,
     40,  40,  42,  41,  41,  41,  42,  42,  41,  41,  41,  41,  41,  41,  41,  41,
     43,  43,  43,  43,  43,  43,  43,  43,  32,  32,  42,  32,  44,  45,  16,  10,
     44,  44,  41,  46,  11,  47,  47,  11,  34,  11,  11,  11,  11,  11,  11,  11,
     11,  48,  11,  11,  11,  11,  16,  16,  16,  16,  16,  16,  16,  16,  16,  34,
     16,  11,  32,  16,  32,  32,  32,  32,  16,  16,  32,  49,  34,  32,  34,  11,
     32,  50,  43,  43,  51,  32,  32,  32,  11,  34,  34,  34,  34,  34,  34,  16,
     48,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  47,  52,   2,   2,   2,
     16,  16,  16,  16,  53,  54,  55,  56,  57,  43,  43,  43,  43,  43,  43,  43,
     43,  43,  43,  43,  43,  43,  43,  58,  59,  60,  43,  59,  44,  44,  44,  44,
     36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  61,  44,  62,
     36,  63,  64,  44,  44,  44,  44,  44,  65,  65,  65,   8,   9,  66,   2,  67,
     43,  43,  43,  43,  43,  60,  68,   2,  69,  36,  36,  36,  36,  70,  43,  43,
      7,   7,   7,   7,   7,   2,   2,  36,  71,  36,  36,  36,  36,  36,  36,  36,
     36,  36,  72,  43,  43,  43,  73,  50,  43,  43,  74,  75,  76,  43,  43,  36,
      7,   7,   7,   7,   7,  36,  77,  78,   2,   2,   2,   2,   2,   2,   2,  79,
     70,  36,  36,  36,  36,  36,  36,  36,  43,  43,  43,  43,  43,  80,  62,  36,
     36,  36,  36,  43,  43,  43,  43,  43,  71,  44,  44,  44,  44,  44,  44,  44,
      7,   7,   7,   7,   7,  36,  36,  36,  36,  36,  36,  36,  36,  70,  43,  43,
     43,  43,  40,  21,   2,  81,  57,  20,  36,  36,  36,  43,  43,  75,  43,  43,
     43,  43,  75,  43,  75,  43,  43,  44,   2,   2,   2,   2,   2,   2,   2,  64,
     36,  36,  36,  36,  70,  43,  44,  64,  36,  36,  36,  36,  36,  61,  44,  44,
     44,  44,  44,  44,  44,  44,  44,  44,  36,  36,  61,  36,  36,  36,  36,  44,
     44,  57,  43,  43,  43,  43,  43,  43,  43,  82,  43,  43,  43,  43,  43,  43,
     43,  83,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  83,  71,  84,
     85,  43,  43,  43,  83,  84,  85,  84,  70,  43,  43,  43,  36,  36,  36,  36,
     36,  43,   2,   7,   7,   7,   7,   7,  86,  36,  36,  36,  36,  36,  36,  36,
     70,  84,  62,  36,  36,  36,  61,  62,  61,  62,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  61,  36,  36,  36,  61,  61,  44,  36,  36,  44,  71,  84,
     85,  43,  80,  87,  88,  87,  85,  61,  44,  44,  44,  87,  44,  44,  36,  62,
     36,  43,  44,   7,   7,   7,   7,   7,  36,  20,  27,  27,  27,  56,  63,  80,
     57,  83,  62,  36,  36,  61,  44,  62,  61,  36,  62,  61,  36,  44,  80,  84,
     85,  80,  44,  57,  80,  57,  43,  44,  57,  44,  44,  44,  62,  36,  61,  61,
     44,  44,  44,   7,   7,   7,   7,   7,  43,  36,  70,  64,  44,  44,  44,  44,
     57,  83,  62,  36,  36,  36,  36,  62,  36,  62,  36,  36,  36,  36,  36,  36,
     61,  36,  62,  36,  36,  44,  71,  84,  85,  43,  43,  57,  83,  87,  85,  44,
     61,  44,  44,  44,  44,  44,  44,  44,  66,  44,  44,  44,  62,  43,  43,  43,
     57,  84,  62,  36,  36,  36,  61,  62,  61,  36,  62,  36,  36,  44,  71,  85,
     85,  43,  80,  87,  88,  87,  85,  44,  44,  44,  44,  83,  44,  44,  36,  62,
     78,  27,  27,  27,  44,  44,  44,  44,  44,  71,  62,  36,  36,  61,  44,  36,
     61,  36,  36,  44,  62,  61,  61,  36,  44,  62,  61,  44,  36,  61,  44,  36,
     36,  36,  36,  36,  36,  44,  44,  84,  83,  88,  44,  84,  88,  84,  85,  44,
     61,  44,  44,  87,  44,  44,  44,  44,  27,  89,  67,  67,  56,  90,  44,  44,
     83,  84,  71,  36,  36,  36,  61,  36,  61,  36,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  44,  62,  43,  83,  84,  88,  43,  80,  43,  43,  44,
     44,  44,  57,  80,  36,  61,  44,  44,  44,  44,  44,  44,  27,  27,  27,  89,
     70,  84,  72,  36,  36,  36,  61,  36,  36,  36,  62,  36,  36,  44,  71,  85,
     84,  84,  88,  83,  88,  84,  43,  44,  44,  44,  87,  88,  44,  44,  44,  61,
     62,  61,  44,  44,  44,  44,  44,  44,  43,  84,  62,  36,  36,  36,  61,  36,
     36,  36,  36,  36,  36,  70,  71,  84,  85,  43,  80,  84,  88,  84,  85,  77,
     44,  44,  36,  91,  27,  27,  27,  92,  27,  27,  27,  27,  89,  36,  36,  36,
     44,  84,  62,  36,  36,  36,  36,  36,  36,  36,  36,  61,  44,  36,  36,  36,
     36,  62,  36,  36,  36,  36,  62,  44,  36,  36,  36,  61,  44,  80,  44,  87,
     84,  43,  80,  80,  84,  84,  84,  84,  44,  84,  64,  44,  44,  44,  44,  44,
     62,  36,  36,  36,  36,  36,  36,  36,  70,  36,  43,  43,  43,  80,  44,  93,
     36,  36,  36,  75,  43,  43,  43,  60,   7,   7,   7,   7,   7,   2,  44,  44,
     62,  61,  61,  62,  61,  61,  62,  44,  44,  44,  36,  36,  62,  36,  36,  36,
     62,  36,  62,  62,  44,  36,  62,  36,  70,  36,  43,  43,  43,  57,  71,  44,
     36,  36,  61,  81,  43,  43,  43,  44,   7,   7,   7,   7,   7,  44,  36,  36,
     77,  67,   2,   2,   2,   2,   2,   2,   2,  94,  94,  67,  43,  67,  67,  67,
      7,   7,   7,   7,   7,  27,  27,  27,  27,  27,  50,  50,  50,   4,   4,  84,
     36,  36,  36,  36,  62,  36,  36,  36,  36,  36,  36,  36,  36,  36,  61,  44,
     57,  43,  43,  43,  43,  43,  43,  83,  43,  43,  60,  43,  36,  36,  70,  43,
     43,  43,  43,  43,  57,  43,  43,  43,  43,  43,  43,  43,  43,  43,  80,  67,
     67,  67,  67,  76,  67,  67,  90,  67,   2,   2,  94,  67,  21,  64,  44,  44,
     36,  36,  36,  36,  36,  91,  85,  43,  83,  43,  43,  43,  85,  83,  85,  71,
      7,   7,   7,   7,   7,   2,   2,   2,  36,  36,  36,  84,  43,  36,  36,  43,
     71,  84,  95,  91,  84,  84,  84,  36,  70,  43,  71,  36,  36,  36,  36,  36,
     36,  83,  85,  83,  84,  84,  85,  91,   7,   7,   7,   7,   7,  84,  85,  67,
     11,  11,  11,  48,  44,  44,  48,  44,  16,  16,  16,  16,  16,  53,  45,  16,
     36,  36,  36,  36,  61,  36,  36,  44,  36,  36,  36,  61,  61,  36,  36,  44,
     61,  36,  36,  44,  36,  36,  36,  61,  61,  36,  36,  44,  36,  36,  36,  36,
     36,  36,  36,  61,  36,  36,  36,  36,  36,  36,  36,  36,  36,  61,  57,  43,
      2,   2,   2,   2,  96,  27,  27,  27,  27,  27,  27,  27,  27,  27,  97,  44,
     67,  67,  67,  67,  67,  44,  44,  44,  11,  11,  11,  44,  16,  16,  16,  44,
     98,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  63,  72,
     99,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36, 100, 101,  44,
     36,  36,  36,  36,  36,  63,   2, 102, 103,  36,  36,  36,  61,  44,  44,  44,
     36,  36,  36,  36,  36,  36,  61,  36,  36,  43,  80,  44,  44,  44,  44,  44,
     36,  43,  60,  64,  44,  44,  44,  44,  36,  43,  44,  44,  44,  44,  44,  44,
     61,  43,  44,  44,  44,  44,  44,  44,  36,  36,  43,  85,  43,  43,  43,  84,
     84,  84,  84,  83,  85,  43,  43,  43,  43,  43,   2,  86,   2,  66,  70,  44,
      7,   7,   7,   7,   7,  44,  44,  44,  27,  27,  27,  27,  27,  44,  44,  44,
      2,   2,   2, 104,   2,  59,  43,  68,  36, 105,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  61,  44,  44,  44,  36,  36,  70,  71,  36,  36,  36,  36,
     36,  36,  36,  36,  70,  61,  44,  44,  36,  36,  36,  44,  44,  44,  44,  44,
     36,  36,  36,  36,  36,  36,  36,  61,  43,  83,  84,  85,  83,  84,  44,  44,
     84,  83,  84,  84,  85,  43,  44,  44,  90,  44,   2,   7,   7,   7,   7,   7,
     36,  36,  36,  36,  36,  36,  36,  44,  36,  36,  61,  44,  44,  44,  44,  44,
     36,  36,  36,  36,  36,  36,  44,  44,  36,  36,  36,  36,  36,  44,  44,  44,
      7,   7,   7,   7,   7,  97,  44,  67,  67,  67,  67,  67,  67,  67,  67,  67,
     36,  36,  36,  70,  83,  85,  44,   2,  36,  36,  91,  83,  43,  43,  43,  80,
     83,  83,  85,  43,  43,  43,  83,  84,  84,  85,  43,  43,  43,  43,  80,  57,
      2,   2,   2,  86,   2,   2,   2,  44,  43,  43,  43,  43,  43,  43,  43, 106,
     43,  43,  95,  36,  36,  36,  36,  36,  36,  36,  83,  43,  43,  83,  83,  84,
     84,  83,  95,  36,  36,  36,  44,  44,  94,  67,  67,  67,  67,  50,  43,  43,
     43,  43,  67,  67,  67,  67,  90,  44,  43,  95,  36,  36,  36,  36,  36,  36,
     91,  43,  43,  84,  43,  85,  43,  36,  36,  36,  36,  83,  43,  84,  85,  85,
     43,  84,  44,  44,  44,  44,   2,   2,  36,  36,  84,  84,  84,  84,  43,  43,
     43,  43,  84,  43,  44, 107,   2,   2,   7,   7,   7,   7,   7,  44,  62,  36,
     36,  36,  36,  36,  40,  40,  40,   2,  16,  16,  16,  16, 108,  44,  44,  44,
     11,  11,  11,  11,  11,  47,  48,  11,   2,   2,   2,   2,  44,  44,  44,  44,
     43,  60,  43,  43,  43,  43,  43,  43,  83,  43,  43,  43,  71,  36,  70,  36,
     36,  84,  71,  91,  43,  44,  44,  44,  16,  16,  16,  16,  16,  16,  40,  40,
     40,  40,  40,  40,  40,  45,  16,  16,  16,  16,  16,  16,  45,  16,  16,  16,
     16,  16,  16,  16,  16, 109,  40,  40,  43,  43,  43,  43,  43,  57,  43,  43,
     32,  32,  32,  16,  16,  16,  16,  32,  16,  16,  16,  16,  11,  11,  11,  11,
     16,  16,  16,  44,  11,  11,  11,  44,  16,  16,  16,  16,  48,  48,  48,  48,
     16,  16,  16,  16,  16,  16,  16,  44,  16,  16,  16,  16, 110, 110, 110, 110,
     16,  16, 108,  16,  11,  11, 111, 112,  41,  16, 108,  16,  11,  11, 111,  41,
     16,  16,  44,  16,  11,  11, 113,  41,  16,  16,  16,  16,  11,  11, 114,  41,
     44,  16, 108,  16,  11,  11, 111, 115, 116, 116, 116, 116, 116, 117,  65,  65,
    118, 118, 118,   2, 119, 120, 119, 120,   2,   2,   2,   2, 121,  65,  65, 122,
      2,   2,   2,   2, 123, 124,   2, 125, 126,   2, 127, 128,   2,   2,   2,   2,
      2,   9, 126,   2,   2,   2,   2, 129,  65,  65,  68,  65,  65,  65,  65,  65,
    130,  44,  27,  27,  27,   8, 127, 131,  27,  27,  27,  27,  27,   8, 127, 101,
     40,  40,  40,  40,  40,  40,  81,  44,  20,  20,  20,  20,  20,  20,  20,  20,
     43,  43,  43,  43,  43,  43, 132,  51, 133,  51, 133,  43,  43,  43,  43,  43,
     80,  44,  44,  44,  44,  44,  44,  44,  67, 134,  67, 135,  67,  34,  11,  16,
     11,  32, 135,  67,  49,  11,  11,  67,  67,  67, 134, 134, 134,  11,  11, 136,
     11,  11,  35,  36,  39,  67,  16,  11,   8,   8,  49,  16,  16,  26,  67, 137,
     27,  27,  27,  27,  27,  27,  27,  27, 102, 102, 102, 102, 102, 102, 102, 102,
    102, 138, 139, 102, 140,  67,  44,  44,   8,   8, 141,  67,  67,   8,  67,  67,
    141,  26,  67, 141,  67,  67,  67, 141,  67,  67,  67,  67,  67,  67,  67,   8,
     67, 141, 141,  67,  67,  67,  67,  67,  67,  67,   8,   8,   8,   8,   8,   8,
      8,   8,   8,   8,   8,   8,   8,   8,  67,  67,  67,  67,   4,   4,  67,  67,
      8,  67,  67,  67, 142, 143,  67,  67,  67,  67,  67,  67,  67,  67, 141,  67,
     67,  67,  67,  67,  67,  26,   8,   8,   8,   8,  67,  67,  67,  67,  67,  67,
     67,  67,  67,  67,  67,  67,   8,   8,   8,  67,  67,  67,  67,  67,  67,  67,
     67,  67,  67,  90,  44,  44,  44,  44,  67,  67,  67,  67,  67,  90,  44,  44,
     27,  27,  27,  27,  27,  27,  67,  67,  67,  67,  67,  67,  67,  27,  27,  27,
     67,  67,  67,  26,  67,  67,  67,  67,  26,  67,  67,  67,  67,  67,  67,  67,
     67,  67,  67,  67,   8,   8,   8,   8,  67,  67,  67,  67,  67,  67,  67,  26,
     67,  67,  67,  67,   4,   4,   4,   4,   4,   4,   4,  27,  27,  27,  27,  27,
     27,  27,  67,  67,  67,  67,  67,  67,   8,   8, 127, 144,   8,   8,   8,   8,
      8,   8,   8,   4,   4,   4,   4,   4,   8, 127, 145, 145, 145, 145, 145, 145,
    145, 145, 145, 145, 144,   8,   8,   8,   8,   8,   8,   8,   4,   4,   8,   8,
      8,   8,   8,   8,   8,   8,   4,   8,   8,   8, 141,  26,   8,   8, 141,  67,
     67,  67,  44,  67,  67,  67,  67,  67,  67,  67,  67,  44,  67,  67,  67,  67,
     67,  67,  67,  67,  90,  67,  67,  67,  67,  67,  67,  67,  67,  67,  67,  90,
     11,  11,  11,  11,  11,  11,  11,  47,  16,  16,  16,  16,  16,  16,  16, 108,
     32,  11,  32,  34,  34,  34,  34,  11,  32,  32,  34,  16,  16,  16,  40,  11,
     32,  32, 137,  67,  67, 135,  34, 146,  43,  32,  44,  44, 107,   2,  96,   2,
     16,  16,  16, 147,  44,  44, 147,  44,  36,  36,  36,  36,  44,  44,  44,  52,
     64,  44,  44,  44,  44,  44,  44,  57,  36,  36,  36,  61,  44,  44,  44,  44,
     36,  36,  36,  61,  36,  36,  36,  61,   2, 119, 119,   2, 123, 124, 119,   2,
      2,   2,   2,   6,   2, 104, 119,   2, 119,   4,   4,   4,   4,   2,   2,  86,
      2,   2,   2,   2,   2, 118,   2,   2, 104, 148,   2,   2,   2,   2,   2,  64,
     67,  67,  67,  67,  67,  55,  67,  67,  67,  67,  44,  44,  44,  44,  44,  44,
     67,  67,  67,  44,  44,  44,  44,  44,  67,  67,  67,  67,  67,  67,  44,  44,
      1,   2, 149, 150,   4,   4,   4,   4,   4,  67,   4,   4,   4,   4, 151, 152,
    153, 102, 102, 102, 102,  43,  43,  84, 154,  40,  40,  67, 102, 155,  63,  67,
     36,  36,  36,  61,  57, 156, 157,  69,  36,  36,  36,  36,  36,  63,  40,  69,
     44,  44,  62,  36,  36,  36,  36,  36,  67,  27,  27,  67,  67,  67,  67,  67,
     27,  27,  27,  27,  27,  67,  67,  67,  67,  67,  67,  67,  27,  27,  27,  27,
    158,  27,  27,  27,  27,  27,  27,  27,  36,  36, 105,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  36, 159,   2,   7,   7,   7,   7,   7,  36,  44,  44,
     32,  32,  32,  32,  32,  32,  32,  70,  51, 160,  43,  43,  43,  43,  43,  86,
     32,  32,  32,  32,  32,  32,  40,  43,  36,  36,  36, 102, 102, 102, 102, 102,
     43,   2,   2,   2,  44,  44,  44,  44,  41,  41,  41, 157,  40,  40,  40,  40,
     41,  32,  32,  32,  32,  32,  32,  32,  16,  32,  32,  32,  32,  32,  32,  32,
     45,  16,  16,  16,  34,  34,  34,  32,  32,  32,  32,  32,  42, 161,  34,  35,
     32,  32,  16,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  11,  11,  32,
     11,  11,  32,  32,  32,  44,  44,  44,  44,  44,  44,  62,  40,  35,  36,  36,
     36,  71,  36,  71,  36,  70,  36,  36,  36,  91,  85,  83,  67,  67,  44,  44,
     27,  27,  27,  67, 162,  44,  44,  44,  36,  36,   2,   2,  44,  44,  44,  44,
     84,  36,  36,  36,  36,  36,  36,  36,  36,  36,  84,  84,  84,  84,  84,  84,
     84,  84,  43,  44,  44,  44,  44,   2,  43,  36,  36,  36,   2,  72,  72,  70,
     36,  36,  36,  43,  43,  43,  43,   2,  36,  36,  36,  70,  43,  43,  43,  43,
     43,  84,  44,  44,  44,  44,  44, 107,  36,  70,  84,  43,  43,  84,  83,  84,
    163,   2,   2,   2,   2,   2,   2,  52,   7,   7,   7,   7,   7,  44,  44,   2,
     36,  36,  70,  69,  36,  36,  36,  36,   7,   7,   7,   7,   7,  36,  36,  61,
     36,  36,  36,  36,  70,  43,  43,  83,  85,  83,  85,  80,  44,  44,  44,  44,
     36,  70,  36,  36,  36,  36,  83,  44,   7,   7,   7,   7,   7,  44,   2,   2,
     69,  36,  36,  77,  67,  91,  83,  36,  71,  43,  71,  70,  71,  36,  36,  43,
     70,  61,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  62, 105,   2,
     36,  36,  36,  36,  36,  91,  43,  84,   2, 105, 164,  80,  44,  44,  44,  44,
     62,  36,  36,  61,  62,  36,  36,  61,  62,  36,  36,  61,  44,  44,  44,  44,
     16,  16,  16,  16,  16, 112,  40,  40,  16,  16,  16,  44,  44,  44,  44,  44,
     36,  91,  85,  84,  83, 163,  85,  44,  36,  36,  44,  44,  44,  44,  44,  44,
     36,  36,  36,  61,  44,  62,  36,  36, 165, 165, 165, 165, 165, 165, 165, 165,
    166, 166, 166, 166, 166, 166, 166, 166,  16,  16,  16, 108,  44,  44,  44,  44,
     44, 147,  16,  16,  44,  44,  62,  71,  36,  36,  36,  36, 167,  36,  36,  36,
     36,  36,  36,  61,  36,  36,  61,  61,  36,  62,  61,  36,  36,  36,  36,  36,
     36,  41,  41,  41,  41,  41,  41,  41,  41,  44,  44,  44,  44,  44,  44,  44,
     44,  62,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36, 145,
     44,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  44,  44,  44,  44,
     36,  36,  36,  36,  36,  36, 162,  44,   2,   2,   2, 168, 128,  44,  44,  44,
      6, 169, 170, 145, 145, 145, 145, 145, 145, 145, 128, 168, 128,   2, 125, 171,
      2,  64,   2,   2, 151, 145, 145, 128,   2, 172,   8, 173,  66,   2,  44,  44,
     36,  36,  61,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  61,  79,
    107,   2,   3,   2,   4,   5,   6,   2,  16,  16,  16,  16,  16,  17,  18, 127,
    128,   4,   2,  36,  36,  36,  36,  36,  69,  36,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  36,  36,  40,  44,  36,  36,  36,  44,  36,  36,  36,
     44,  36,  36,  36,  44,  36,  61,  44,  20, 174,  56, 175,  26,   8, 141,  90,
     44,  44,  44,  44,  79,  65,  67,  44,  36,  36,  36,  36,  36,  36,  62,  36,
     36,  36,  36,  36,  36,  61,  36,  62,   2,  64,  44, 176,  27,  27,  27,  27,
     27,  27,  44,  55,  67,  67,  67,  67, 102, 102, 140,  27,  89,  67,  67,  67,
     67,  67,  67,  67,  67,  27,  67,  90,  90,  44,  44,  44,  44,  44,  44,  44,
     67,  67,  67,  67,  67,  67,  50,  44, 177,  27,  27,  27,  27,  27,  27,  27,
     27,  27,  27,  27,  27,  27,  44,  44,  27,  27,  44,  44,  44,  44,  62,  36,
    150,  36,  36,  36,  36, 178,  44,  44,  36,  36,  36,  43,  43,  80,  44,  44,
     36,  36,  36,  36,  36,  36,  36, 107,  36,  36,  44,  44,  36,  36,  36,  36,
    179, 102, 102,  44,  44,  44,  44,  44,  11,  11,  11,  11,  16,  16,  16,  16,
     11,  11,  44,  44,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  44,  44,
     36,  36,  44,  44,  44,  44,  44, 107,  36,  36,  36,  44,  61,  36,  36,  36,
     36,  36,  36,  62,  61,  44,  61,  62,  36,  36,  36, 107,  27,  27,  27,  27,
     36,  36,  36,  77, 158,  27,  27,  27,  44,  44,  44, 176,  27,  27,  27,  27,
     36,  61,  36,  44,  44, 176,  27,  27,  36,  36,  36,  27,  27,  27,  44, 107,
     36,  36,  36,  36,  36,  44,  44, 107,  36,  36,  36,  36,  44,  44,  27,  36,
     44,  27,  27,  27,  27,  27,  27,  27,  70,  43,  57,  80,  44,  44,  43,  43,
     36,  36,  62,  36,  62,  36,  36,  36,  36,  36,  36,  44,  43,  80,  44,  57,
     27,  27,  27,  27,  97,  44,  44,  44,   2,   2,   2,   2,  64,  44,  44,  44,
     36,  36,  36,  36,  36,  36, 180,  30,  36,  36,  36,  36,  36,  36, 180,  27,
     36,  36,  36,  36,  78,  36,  36,  36,  36,  36,  70,  80,  44, 176,  27,  27,
      2,   2,   2,  64,  44,  44,  44,  44,  36,  36,  36,  44, 107,   2,   2,   2,
     36,  36,  36,  44,  27,  27,  27,  27,  36,  61,  44,  44,  27,  27,  27,  27,
     36,  44,  44,  44, 107,   2,  64,  44,  44,  44,  44,  44, 176,  27,  27,  27,
     11,  47,  44,  44,  44,  44,  44,  44,  16, 108,  44,  44,  44,  27,  27,  27,
     36,  36,  43,  43,  44,  44,  44,  44,  27,  27,  27,  27,  27,  27,  27,  97,
     27,  27,  27,  92,  44,  44,  44,  44, 177,  27,  30,   2,   2,  44,  44,  44,
     85,  95,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  43,  43,  43,  43,
     43,  43,  43,  60,   2,   2,   2,  44,  27,  27,  27,   7,   7,   7,   7,   7,
     44,  44,  44,  44,  44,  44,  44,  57,  84,  85,  43,  83,  85,  60, 181,   2,
      2,  44,  44,  44,  44,  44,  79,  44,  43,  71,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  70,  43,  43,  85,  43,  43,  43,  80,   7,   7,   7,   7,   7,
      2,   2,  91,  88,  44,  44,  44,  44,  36,  70,   2,  61,  44,  44,  44,  44,
     36,  91,  84,  43,  43,  43,  43,  83,  95,  36,  63,   2,  59,  43,  60,  44,
      7,   7,   7,   7,   7,  63,  63,   2, 176,  27,  27,  27,  27,  27,  27,  27,
     27,  27,  97,  44,  44,  44,  44,  44,  36,  36,  36,  36,  36,  36,  84,  85,
     43,  84,  83,  43,   2,   2,   2,  80,  36,  36,  36,  61,  61,  36,  36,  62,
     36,  36,  36,  36,  36,  36,  36,  62,  36,  36,  36,  36,  63,  44,  44,  44,
     36,  36,  36,  36,  36,  36,  36,  70,  84,  85,  43,  43,  43,  80,  44,  44,
     43,  84,  62,  36,  36,  36,  61,  62,  61,  36,  62,  36,  36,  57,  71,  84,
     83,  84,  88,  87,  88,  87,  84,  44,  61,  44,  44,  87,  44,  44,  62,  36,
     36,  84,  44,  43,  43,  43,  80,  44,  43,  43,  80,  44,  44,  44,  44,  44,
     36,  36,  91,  84,  43,  43,  43,  43,  84,  43,  83,  71,  36,  63,   2,   2,
      7,   7,   7,   7,   7, 107, 107,  80,  84,  85,  43,  43,  83,  83,  84,  85,
     83,  43,  36,  72,  44,  44,  44,  44,  36,  36,  36,  36,  36,  36,  36,  91,
     84,  43,  43,  44,  84,  84,  43,  85,  60,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,  36,  36,  43,  44,  84,  85,  43,  43,  43,  83,  85,  85,
     60,   2,  61,  44,  44,  44,  44,  44,   2,   2,   2,   2,   2,   2,  64,  44,
     36,  36,  36,  36,  36,  70,  85,  84,  43,  43,  43,  85,  44,  44,  44,  44,
     84,  43,  43,  85,  43,  43,  44,  44,   7,   7,   7,   7,   7,  27,   2,  94,
     43,  43,  43,  43,  85,  60,  44,  44,  27,  97,  44,  44,  44,  44,  44,  62,
     70,  43,  43,  43,  43,  71,  36,  36,  36,  70,  43,  43,  83,  70,  43,  60,
      2,   2,   2,  59,  44,  44,  44,  44,  70,  43,  43,  83,  85,  43,  36,  36,
     36,  36,  44,  36,  36,  43,  43,  43,  43,  43,  43,  83,  43,   2,  72,   2,
      2,  64,  44,  44,  44,  44,  44,  44,  43,  43,  43,  80,  43,  43,  43,  85,
     63,   2,   2,  44,  44,  44,  44,  44,   2,  36,  36,  36,  36,  36,  36,  36,
     44,  43,  43,  43,  43,  43,  43,  43,  43,  43,  43,  43,  87,  43,  43,  43,
     83,  43,  85,  80,  44,  44,  44,  44,  36,  36,  36,  61,  36,  62,  36,  36,
     70,  43,  43,  80,  44,  80,  43,  57,  43,  43,  43,  70,  44,  44,  44,  44,
     36,  36,  36,  62,  61,  36,  36,  36,  36,  36,  36,  36,  36,  84,  84,  88,
     43,  87,  85,  85,  61,  44,  44,  44,  36,  70,  83, 163,  64,  44,  44,  44,
    102, 102, 102, 102, 102, 102, 102, 178,   2,   2,  64,  44,  44,  44,  44,  44,
     43,  43,  60,  44,  44,  44,  44,  44,  43,  43,  43,  60,   2,   2,  67,  67,
     40,  40,  94,  44,  44,  44,  44,  44,   7,   7,   7,   7,   7, 176,  27,  27,
     27,  62,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  44,  44,  62,  36,
     27,  27,  27,  30,   2,  64,  44,  44,  91,  84,  84,  84,  84,  84,  84,  84,
     84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  88,
     43,  74,  40,  40,  40,  40,  40,  40,  40,  44,  44,  44,  44,  44,  44,  44,
     36,  44,  44,  44,  44,  44,  44,  44,  36,  61,  44,  44,  44,  44,  44,  44,
     36,  36,  36,  36,  36,  44,  50,  60,  65,  65,  44,  44,  44,  44,  44,  44,
     67,  67,  67,  90,  55,  67,  67,  67,  67,  67, 182,  85,  43,  67, 182,  84,
     84, 183,  65,  65,  65,  82,  43,  43,  43,  76,  50,  43,  43,  43,  67,  67,
     67,  67,  67,  67,  67,  43,  43,  67,  67,  67,  67,  67,  90,  44,  44,  44,
     67,  43,  76,  44,  44,  44,  44,  44,  27,  27,  44,  44,  44,  44,  44,  44,
     11,  11,  11,  11,  11,  16,  16,  16,  16,  16,  11,  11,  11,  11,  11,  11,
     11,  11,  11,  11,  11,  11,  11,  16,  16,  16, 108,  16,  16,  16,  16,  16,
     11,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  47,  11,
     44,  47,  48,  47,  48,  11,  47,  11,  11,  11,  11,  16,  16, 147, 147,  16,
     16,  16, 147,  16,  16,  16,  16,  16,  16,  16,  11,  48,  11,  47,  48,  11,
     11,  11,  47,  11,  11,  11,  47,  16,  16,  16,  16,  16,  11,  48,  11,  47,
     11,  11,  47,  47,  44,  11,  11,  11,  47,  16,  16,  16,  16,  16,  16,  16,
     16,  16,  16,  16,  16,  16,  11,  11,  11,  11,  11,  16,  16,  16,  16,  16,
     16,  16,  16,  44,  11,  11,  11,  11,  31,  16,  16,  16,  16,  16,  16,  16,
     16,  16,  16,  16,  16,  33,  16,  16,  16,  11,  11,  11,  11,  11,  11,  11,
     11,  11,  11,  11,  11,  31,  16,  16,  16,  16,  33,  16,  16,  16,  11,  11,
     11,  11,  31,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  33,
     16,  16,  16,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  31,
     16,  16,  16,  16,  33,  16,  16,  16,  11,  11,  11,  11,  31,  16,  16,  16,
     16,  33,  16,  16,  16,  32,  44,   7,   7,   7,   7,   7,   7,   7,   7,   7,
     43,  43,  43,  76,  67,  50,  43,  43,  43,  43,  43,  43,  43,  43,  76,  67,
     67,  67,  50,  67,  67,  67,  67,  67,  67,  67,  76,  21,   2,   2,  44,  44,
     44,  44,  44,  44,  44,  57,  43,  43,  43,  43,  43,  80,  43,  43,  43,  43,
     43,  43,  43,  43,  80,  57,  43,  43,  43,  57,  80,  43,  43,  80,  44,  44,
     36,  36,  61, 176,  27,  27,  27,  27,  43,  43,  43,  80,  44,  44,  44,  44,
     16,  16,  43,  43,  43,  80,  44,  44,  27,  27,  27,  27,  27,  27, 158,  27,
    184,  27,  97,  44,  44,  44,  44,  44,  36,  36,  62,  36,  36,  36,  36,  36,
     62,  61,  61,  62,  62,  36,  36,  36,  36,  61,  36,  36,  62,  62,  44,  44,
     44,  61,  44,  62,  62,  62,  62,  36,  62,  61,  61,  62,  62,  62,  62,  62,
     62,  61,  61,  62,  36,  61,  36,  36,  36,  61,  36,  36,  62,  36,  61,  61,
     36,  36,  36,  36,  36,  62,  36,  36,  62,  36,  62,  36,  36,  62,  36,  36,
      8,  44,  44,  44,  44,  44,  44,  44,  55,  67,  67,  67,  67,  67,  67,  67,
     67,  67,  67,  67,  67,  67,  90,  44,  44,  44,  44,  67,  67,  67,  67,  67,
     67,  90,  44,  44,  44,  44,  44,  44,  67,  44,  44,  44,  44,  44,  44,  44,
     67,  67,  67,  67,  67,  25,  41,  41,  67,  67,  90,  44,  44,  44,  44,  44,
     67,  67,  67,  67,  44,  44,  44,  44,  67,  67,  67,  67,  67,  67,  67,  44,
     90,  55,  67,  90,  44,  90,  67,  67,  79,  44,  44,  44,  44,  44,  44,  44,
     65,  65,  65,  65,  65,  65,  65,  65, 166, 166, 166, 166, 166, 166, 166,  44,
};

static RE_UINT8 re_general_category_stage_5[] = {
    15, 15, 12, 23, 23, 23, 25, 23, 20, 21, 23, 24, 23, 19,  9,  9,
    24, 24, 24, 23, 23,  1,  1,  1,  1, 20, 23, 21, 26, 22, 26,  2,
     2,  2,  2, 20, 24, 21, 24, 15, 25, 25, 27, 23, 26, 27,  5, 28,
    24, 16, 27, 26, 27, 24, 11, 11, 26, 11,  5, 29, 11, 23,  1, 24,
     1,  2,  2, 24,  2,  1,  2,  5,  5,  5,  1,  3,  3,  2,  5,  2,
     4,  4, 26, 26,  4, 26,  6,  6,  0,  0,  4,  2,  1, 23,  1,  0,
     0,  1, 24,  1, 27,  6,  7,  7,  0,  4,  2, 23, 19,  0,  0, 27,
    27, 25,  0,  6, 19,  6, 23,  6,  6, 23,  5,  0,  0,  5,  5, 23,
    23,  0, 16, 16, 23, 25, 27, 27, 16,  0,  4,  5,  5,  6,  6,  5,
    23,  5,  6, 16,  6,  4,  4,  6,  6, 27,  5, 27, 27,  5,  0, 16,
     6,  0,  4,  0, 16,  6,  6,  8,  8,  8,  8,  6, 23,  4,  0,  8,
     8,  0, 11, 27, 27,  0,  5,  8, 11,  5,  0, 25, 23, 27,  8,  5,
    23, 11, 11,  0, 19,  5, 12,  5,  5, 20, 21,  0, 10, 10, 10,  5,
    19, 23,  5,  4,  7,  0,  0, 23,  2,  0,  2,  4,  3,  3,  3, 26,
     2, 26,  0, 26,  1, 26, 26,  0, 12, 12, 12, 16, 19, 19, 28, 29,
    20, 28, 13, 14, 16, 12, 23, 28, 29, 23, 23, 22, 22, 23, 24, 20,
    21, 23, 23, 12, 11,  4, 21,  4,  6,  7,  7,  6,  1, 27, 27,  1,
    27,  2,  2, 27, 10,  1,  2, 10, 10, 11, 24, 27, 27, 20, 21, 27,
    21, 24, 21, 20,  2,  6,  0,  2, 20, 23, 27,  4,  5, 10, 19, 20,
    21, 21, 27, 10, 19,  4, 10,  4,  6, 26, 26,  4, 27, 11,  4, 23,
     7, 23, 26,  1, 25, 27,  8, 23,  4,  8, 18, 18, 17, 17,  5, 24,
    23, 20, 19, 22, 22, 20, 22, 22, 24, 19, 24,  0, 24, 26, 25,  0,
     0, 11,  6, 11, 10,  0, 23, 10,  5, 11, 23, 16, 27,  8,  8, 16,
    25, 11,
};

/* General_Category: 10354 bytes. */

RE_UINT32 re_get_general_category(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 11;
    code = ch ^ (f << 11);
    pos = (RE_UINT32)re_general_category_stage_1[f] << 4;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_general_category_stage_2[pos + f] << 3;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_general_category_stage_3[pos + f] << 3;
    f = code >> 1;
    code ^= f << 1;
    pos = (RE_UINT32)re_general_category_stage_4[pos + f] << 1;
    value = re_general_category_stage_5[pos + code];

    return value;
}

/* Block. */

static RE_UINT8 re_block_stage_1[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9, 10, 11, 12, 12, 12, 12, 13, 14, 15, 15, 15, 16,
    17, 18, 19, 20, 21, 22, 23, 22, 24, 22, 22, 22, 22, 25, 26, 26,
    26, 27, 22, 22, 22, 22, 28, 29, 22, 22, 30, 31, 32, 33, 34, 35,
    36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
    36, 36, 36, 36, 37, 38, 39, 40, 41, 42, 43, 43, 43, 44, 22, 45,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    46, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47,
    47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47,
    48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
    48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
};

static RE_UINT8 re_block_stage_2[] = {
      0,   1,   2,   3,   4,   5,   6,   7,   8,   8,   9,  10,  11,  11,  12,  13,
     14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  28,
     29,  30,  31,  31,  32,  32,  32,  33,  34,  34,  34,  34,  34,  35,  36,  37,
     38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  50,  51,  51,
     52,  53,  54,  55,  56,  56,  57,  57,  58,  59,  60,  61,  62,  62,  63,  64,
     65,  65,  66,  67,  68,  68,  69,  69,  70,  71,  72,  73,  74,  75,  76,  77,
     78,  79,  80,  81,  82,  82,  83,  83,  84,  84,  84,  84,  84,  84,  84,  84,
     84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,
     84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  85,  86,  86,  86,  86,
     86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,
     87,  87,  87,  87,  87,  87,  87,  87,  87,  88,  89,  89,  90,  91,  92,  93,
     94,  95,  96,  97,  98,  99, 100, 101, 102, 102, 102, 102, 102, 102, 102, 102,
    102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102,
    102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 103,
    104, 104, 104, 104, 104, 104, 104, 105, 106, 106, 106, 106, 106, 106, 106, 106,
    107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107,
    107, 107, 108, 108, 108, 108, 109, 110, 110, 110, 110, 110, 111, 112, 113, 114,
    115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 119, 126, 126, 126, 119,
    127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 119, 138, 119, 139, 119,
    140, 141, 142, 143, 144, 145, 146, 119, 147, 148, 119, 149, 150, 151, 152, 119,
    153, 154, 119, 119, 155, 156, 119, 119, 157, 158, 159, 160, 119, 161, 119, 119,
    162, 162, 162, 162, 162, 162, 162, 162, 163, 164, 165, 119, 119, 119, 119, 119,
    119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119,
    166, 166, 166, 166, 166, 166, 166, 166, 167, 119, 119, 119, 119, 119, 119, 119,
    119, 119, 119, 119, 119, 119, 119, 119, 168, 168, 168, 168, 168, 119, 119, 119,
    169, 169, 169, 169, 170, 171, 172, 173, 119, 119, 119, 119, 174, 175, 176, 177,
    178, 178, 178, 178, 178, 178, 178, 178, 178, 178, 178, 178, 178, 178, 178, 178,
    179, 179, 179, 179, 179, 179, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119,
    180, 180, 181, 182, 182, 182, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119,
    119, 119, 119, 119, 119, 119, 119, 119, 183, 184, 119, 119, 119, 119, 119, 119,
    185, 185, 186, 186, 187, 188, 189, 119, 190, 190, 190, 190, 190, 190, 190, 190,
    191, 191, 191, 191, 191, 192, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119,
    193, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119,
    194, 195, 196, 119, 119, 119, 119, 119, 197, 198, 119, 119, 199, 199, 119, 119,
    200, 201, 202, 202, 203, 203, 204, 204, 204, 204, 204, 204, 205, 206, 207, 208,
    209, 209, 210, 210, 211, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119,
    212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212,
    212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 213, 214, 214,
    214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214,
    214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 215, 216,
    217, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218,
    218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218,
    218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 218, 219, 220, 220,
    220, 220, 220, 220, 220, 220, 220, 220, 220, 220, 220, 220, 220, 220, 220, 220,
    220, 220, 220, 220, 220, 220, 220, 221, 119, 119, 119, 119, 119, 119, 119, 119,
    222, 222, 222, 222, 223, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119,
    224, 119, 225, 226, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119,
    227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227,
    228, 228, 228, 228, 228, 228, 228, 228, 228, 228, 228, 228, 228, 228, 228, 228,
};

static RE_UINT16 re_block_stage_3[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1,   1,
      2,   2,   2,   2,   2,   2,   2,   2,   3,   3,   3,   3,   3,   3,   3,   3,
      3,   3,   3,   3,   3,   4,   4,   4,   4,   4,   4,   5,   5,   5,   5,   5,
      6,   6,   6,   6,   6,   6,   6,   7,   7,   7,   7,   7,   7,   7,   7,   7,
      8,   8,   8,   8,   8,   8,   8,   8,   9,   9,   9,  10,  10,  10,  10,  10,
     10,  11,  11,  11,  11,  11,  11,  11,  12,  12,  12,  12,  12,  12,  12,  12,
     13,  13,  13,  13,  13,  14,  14,  14,  15,  15,  15,  15,  16,  16,  16,  16,
     17,  17,  17,  17,  18,  18,  19,  20,  20,  20,  21,  21,  21,  21,  21,  21,
     22,  22,  22,  22,  22,  22,  22,  22,  23,  23,  23,  23,  23,  23,  23,  23,
     24,  24,  24,  24,  24,  24,  24,  24,  25,  25,  25,  25,  25,  25,  25,  25,
     26,  26,  26,  26,  26,  26,  26,  26,  27,  27,  27,  27,  27,  27,  27,  27,
     28,  28,  28,  28,  28,  28,  28,  28,  29,  29,  29,  29,  29,  29,  29,  29,
     30,  30,  30,  30,  30,  30,  30,  30,  31,  31,  31,  31,  31,  31,  31,  31,
     32,  32,  32,  32,  32,  32,  32,  32,  33,  33,  33,  33,  33,  33,  33,  33,
     34,  34,  34,  34,  34,  34,  34,  34,  35,  35,  35,  35,  35,  35,  35,  35,
     35,  35,  36,  36,  36,  36,  36,  36,  37,  37,  37,  37,  37,  37,  37,  37,
     38,  38,  38,  38,  38,  38,  38,  38,  39,  39,  40,  40,  40,  40,  40,  40,
     41,  41,  41,  41,  41,  41,  41,  41,  42,  42,  43,  43,  43,  43,  43,  43,
     44,  44,  45,  45,  46,  46,  47,  47,  48,  48,  48,  48,  48,  48,  48,  48,
     49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  50,  50,  50,  50,  50,
     51,  51,  51,  51,  51,  52,  52,  52,  53,  53,  53,  53,  53,  53,  54,  54,
     55,  55,  56,  56,  56,  56,  56,  56,  56,  56,  56,  57,  57,  57,  57,  57,
     58,  58,  58,  58,  58,  58,  58,  58,  59,  59,  59,  59,  60,  60,  60,  60,
     61,  61,  61,  61,  61,  62,  62,  62,  63,  64,  64,  64,  65,  66,  66,  66,
     67,  67,  67,  67,  67,  67,  67,  67,  68,  68,  68,  68,  69,  69,  69,  69,
     70,  70,  70,  70,  70,  70,  70,  70,  71,  71,  71,  71,  71,  71,  71,  71,
     72,  72,  72,  72,  72,  72,  72,  73,  73,  73,  74,  74,  74,  75,  75,  75,
     76,  76,  76,  76,  76,  77,  77,  77,  77,  78,  78,  78,  78,  78,  78,  78,
     79,  79,  79,  79,  79,  79,  79,  79,  80,  80,  80,  80,  80,  80,  80,  80,
     81,  81,  81,  81,  82,  82,  83,  83,  83,  83,  83,  83,  83,  83,  83,  83,
     84,  84,  84,  84,  84,  84,  84,  84,  85,  85,  86,  86,  86,  86,  86,  86,
     87,  87,  87,  87,  87,  87,  87,  87,  88,  88,  88,  88,  88,  88,  88,  88,
     88,  88,  88,  88,  89,  89,  89,  90,  91,  91,  91,  91,  91,  91,  91,  91,
     92,  92,  92,  92,  92,  92,  92,  92,  93,  93,  93,  93,  93,  93,  93,  93,
     94,  94,  94,  94,  94,  94,  94,  94,  95,  95,  95,  95,  95,  95,  95,  95,
     96,  96,  96,  96,  96,  96,  97,  97,  98,  98,  98,  98,  98,  98,  98,  98,
     99,  99,  99, 100, 100, 100, 100, 100, 101, 101, 101, 101, 101, 101, 102, 102,
    103, 103, 103, 103, 103, 103, 103, 103, 104, 104, 104, 104, 104, 104, 104, 104,
    105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105,  20, 106,
    107, 107, 107, 107, 108, 108, 108, 108, 108, 108, 109, 109, 109, 109, 109, 109,
    110, 110, 110, 111, 111, 111, 111, 111, 111, 112, 113, 113, 114, 114, 114, 115,
    116, 116, 116, 116, 116, 116, 116, 116, 117, 117, 117, 117, 117, 117, 117, 117,
    118, 118, 118, 118, 118, 118, 118, 118, 118, 118, 118, 118, 119, 119, 119, 119,
    120, 120, 120, 120, 120, 120, 120, 120, 121, 121, 121, 121, 121, 121, 121, 121,
    121, 122, 122, 122, 122, 123, 123, 123, 124, 124, 124, 124, 124, 124, 124, 124,
    124, 124, 124, 124, 125, 125, 125, 125, 125, 125, 126, 126, 126, 126, 126, 126,
    127, 127, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128,
    129, 129, 129, 130, 131, 131, 131, 131, 132, 132, 132, 132, 132, 132, 133, 133,
    134, 134, 134, 135, 135, 135, 136, 136, 137, 137, 137, 137, 137, 137, 138, 138,
    139, 139, 139, 139, 139, 139, 140, 140, 141, 141, 141, 141, 141, 141, 142, 142,
    143, 143, 143, 144, 144, 144, 144, 145, 145, 145, 145, 145, 146, 146, 146, 146,
    147, 147, 147, 147, 147, 147, 147, 147, 147, 147, 147, 148, 148, 148, 148, 148,
    149, 149, 149, 149, 149, 149, 149, 149, 150, 150, 150, 150, 150, 150, 150, 150,
    151, 151, 151, 151, 151, 151, 151, 151, 152, 152, 152, 152, 152, 152, 152, 152,
    153, 153, 153, 153, 153, 153, 153, 153, 154, 154, 154, 154, 154, 155, 155, 155,
    155, 155, 155, 155, 155, 155, 155, 155, 156, 157, 158, 159, 159, 160, 160, 161,
    161, 161, 161, 161, 161, 161, 161, 161, 162, 162, 162, 162, 162, 162, 162, 162,
    162, 162, 162, 162, 162, 162, 162, 163, 164, 164, 164, 164, 164, 164, 164, 164,
    165, 165, 165, 165, 165, 165, 165, 165, 166, 166, 166, 166, 167, 167, 167, 167,
    167, 168, 168, 168, 168, 169, 169, 169,  20,  20,  20,  20,  20,  20,  20,  20,
    170, 170, 171, 171, 171, 171, 172, 172, 173, 173, 173, 174, 174, 175, 175, 175,
    176, 176, 177, 177, 177, 177,  20,  20, 178, 178, 178, 178, 178, 179, 179, 179,
    180, 180, 180, 181, 181, 181, 181, 181, 182, 182, 182, 183, 183, 183, 183,  20,
    184, 184, 184, 184, 184, 184, 184, 184, 185, 185, 185, 185, 186, 186, 187, 187,
    188, 188, 188,  20,  20,  20, 189, 189, 190, 190, 191, 191,  20,  20,  20,  20,
    192, 192, 193, 193, 193, 193, 193, 193, 194, 194, 194, 194, 194, 194, 195, 195,
    196, 196,  20,  20, 197, 197, 197, 197, 198, 198, 198, 198, 199, 199, 200, 200,
    201, 201, 201,  20,  20,  20,  20,  20, 202, 202, 202, 202, 202,  20,  20,  20,
    203, 203, 203, 203, 203, 203, 203, 203, 204, 204, 204, 204,  20,  20,  20,  20,
     20,  20,  20,  20,  20,  20, 205, 205, 206, 206, 206, 207, 207, 207, 207,  20,
    208, 208, 208, 208, 208, 208, 208, 208, 209, 209, 209, 209, 209, 210, 210, 210,
    211, 211, 211, 211, 211, 212, 212, 212, 213, 213, 213, 213, 213, 213, 214, 214,
    215, 215, 215, 215, 215,  20,  20,  20, 216, 216, 216, 217, 217, 217, 217, 217,
    218, 218, 218, 218, 218, 218, 218, 218, 219, 219, 219, 219, 219, 219, 219, 219,
    220, 220, 220, 220, 220, 220,  20,  20, 221, 221, 221, 221, 221, 221, 221, 221,
    222, 222, 222, 222, 222, 222, 223, 223, 224, 224, 224, 224, 224,  20,  20,  20,
    225, 225, 225, 225,  20,  20,  20,  20, 226, 226, 226, 226, 226,  20,  20,  20,
     20,  20, 227, 227, 227, 227, 227, 227, 228, 228, 228, 228, 228, 229, 229, 229,
    229, 229, 229,  20, 230, 230, 230, 230, 231, 231, 231, 231, 231, 231, 231, 232,
    232, 232, 232, 232,  20,  20,  20,  20, 233, 233, 233, 233, 233, 233, 234, 234,
    234, 234, 234,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20, 235, 235,
    236, 236, 236, 236, 236, 236, 236, 236, 237, 237, 237, 237, 237, 237, 237, 237,
    238, 238, 238, 238, 238, 238, 238, 238, 238, 238, 238, 238, 238,  20,  20,  20,
    239, 239, 239, 239, 239, 239, 239, 239, 239, 239, 239,  20,  20,  20,  20,  20,
    240, 240, 240, 240, 240, 240, 240, 240, 241, 241, 241, 241, 241, 241, 241, 241,
    241, 241, 241, 241, 242, 242, 242,  20,  20,  20,  20,  20,  20, 243, 243, 243,
    244, 244, 244, 244, 244, 244, 244, 244, 244,  20,  20,  20,  20,  20,  20,  20,
     20,  20,  20,  20, 245, 245, 245, 245, 245, 245,  20,  20,  20,  20,  20,  20,
    246, 246, 246, 246, 246, 246, 246, 246, 246, 246,  20,  20,  20,  20, 247, 247,
    248, 248, 248, 248, 248, 248, 248, 248, 249, 249, 249, 249, 249, 249, 249, 249,
    250, 250, 250, 250, 250, 250, 250, 250, 251, 251, 251,  20,  20,  20,  20, 252,
    252, 252, 252, 252, 252, 252, 252, 252, 253, 253, 253, 253, 253, 253, 253, 253,
    253, 253, 254,  20,  20,  20,  20,  20, 255, 255, 255, 255, 255, 255, 255, 255,
    256, 256, 256, 256, 256, 256, 256, 256, 257, 257, 257, 257, 257,  20,  20,  20,
     20,  20,  20,  20,  20,  20, 258, 258, 259, 259, 259, 259, 259, 259, 260, 260,
    261, 261, 261, 261, 261, 261, 261, 261, 262, 262, 262, 262, 262, 262, 262, 262,
    262, 262, 262,  20,  20,  20,  20,  20, 263, 263, 263,  20,  20,  20,  20,  20,
    264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264,  20,  20,
    265, 265, 265, 265, 265, 265,  20,  20,  20,  20,  20,  20,  20,  20,  20, 266,
    266, 266, 266, 266,  20,  20,  20,  20, 267, 267, 267, 267, 267, 267, 267, 267,
    268, 268, 268, 269, 269, 269, 269, 269, 269, 269, 270, 270, 270, 270, 270, 270,
    271, 271, 271, 271, 271, 271, 271, 271, 272, 272, 272, 272, 272, 272, 272, 272,
    273, 273, 273, 273, 273, 273, 273, 273, 274, 274, 274, 274, 274, 275, 275, 275,
    276, 276, 276, 276, 276, 276, 276, 276, 277, 277, 277, 277, 277, 277, 277, 277,
    278, 278, 278, 278, 278, 278, 278, 278, 279, 279, 279, 279, 279, 279, 279, 279,
    280, 280, 280, 280, 280, 280, 280, 280, 281, 281, 281, 281, 281, 281, 281,  20,
    282, 282, 282, 282, 282, 282, 282, 282, 282, 282, 282, 282, 282, 282,  20,  20,
    283, 283, 283, 283, 283, 283, 283, 283, 283, 283, 283, 283, 284, 284, 284, 284,
    284, 284, 284, 284, 284, 284, 284, 284, 284, 284, 285, 285, 285, 285, 285, 285,
    285, 285, 285, 285, 285, 285, 285, 285, 285, 285, 285, 286, 286, 286, 286, 286,
    286, 286, 286, 286, 286, 286, 286, 286, 286, 286, 286, 286, 286, 286, 286,  20,
    287, 287, 287, 287, 287, 287, 287, 287, 287, 287,  20,  20,  20,  20,  20,  20,
    288, 288, 288, 288, 288, 288, 288, 288, 289, 289, 289, 289, 289, 289, 289, 289,
    289, 289, 289, 289, 289, 289, 289,  20, 290, 290, 290, 290, 290, 290, 290, 290,
    291, 291, 291, 291, 291, 291, 291, 291,
};

static RE_UINT16 re_block_stage_4[] = {
      0,   0,   0,   0,   1,   1,   1,   1,   2,   2,   2,   2,   3,   3,   3,   3,
      4,   4,   4,   4,   5,   5,   5,   5,   6,   6,   6,   6,   7,   7,   7,   7,
      8,   8,   8,   8,   9,   9,   9,   9,  10,  10,  10,  10,  11,  11,  11,  11,
     12,  12,  12,  12,  13,  13,  13,  13,  14,  14,  14,  14,  15,  15,  15,  15,
     16,  16,  16,  16,  17,  17,  17,  17,  18,  18,  18,  18,  19,  19,  19,  19,
     20,  20,  20,  20,  21,  21,  21,  21,  22,  22,  22,  22,  23,  23,  23,  23,
     24,  24,  24,  24,  25,  25,  25,  25,  26,  26,  26,  26,  27,  27,  27,  27,
     28,  28,  28,  28,  29,  29,  29,  29,  30,  30,  30,  30,  31,  31,  31,  31,
     32,  32,  32,  32,  33,  33,  33,  33,  34,  34,  34,  34,  35,  35,  35,  35,
     36,  36,  36,  36,  37,  37,  37,  37,  38,  38,  38,  38,  39,  39,  39,  39,
     40,  40,  40,  40,  41,  41,  41,  41,  42,  42,  42,  42,  43,  43,  43,  43,
     44,  44,  44,  44,  45,  45,  45,  45,  46,  46,  46,  46,  47,  47,  47,  47,
     48,  48,  48,  48,  49,  49,  49,  49,  50,  50,  50,  50,  51,  51,  51,  51,
     52,  52,  52,  52,  53,  53,  53,  53,  54,  54,  54,  54,  55,  55,  55,  55,
     56,  56,  56,  56,  57,  57,  57,  57,  58,  58,  58,  58,  59,  59,  59,  59,
     60,  60,  60,  60,  61,  61,  61,  61,  62,  62,  62,  62,  63,  63,  63,  63,
     64,  64,  64,  64,  65,  65,  65,  65,  66,  66,  66,  66,  67,  67,  67,  67,
     68,  68,  68,  68,  69,  69,  69,  69,  70,  70,  70,  70,  71,  71,  71,  71,
     72,  72,  72,  72,  73,  73,  73,  73,  74,  74,  74,  74,  75,  75,  75,  75,
     76,  76,  76,  76,  77,  77,  77,  77,  78,  78,  78,  78,  79,  79,  79,  79,
     80,  80,  80,  80,  81,  81,  81,  81,  82,  82,  82,  82,  83,  83,  83,  83,
     84,  84,  84,  84,  85,  85,  85,  85,  86,  86,  86,  86,  87,  87,  87,  87,
     88,  88,  88,  88,  89,  89,  89,  89,  90,  90,  90,  90,  91,  91,  91,  91,
     92,  92,  92,  92,  93,  93,  93,  93,  94,  94,  94,  94,  95,  95,  95,  95,
     96,  96,  96,  96,  97,  97,  97,  97,  98,  98,  98,  98,  99,  99,  99,  99,
    100, 100, 100, 100, 101, 101, 101, 101, 102, 102, 102, 102, 103, 103, 103, 103,
    104, 104, 104, 104, 105, 105, 105, 105, 106, 106, 106, 106, 107, 107, 107, 107,
    108, 108, 108, 108, 109, 109, 109, 109, 110, 110, 110, 110, 111, 111, 111, 111,
    112, 112, 112, 112, 113, 113, 113, 113, 114, 114, 114, 114, 115, 115, 115, 115,
    116, 116, 116, 116, 117, 117, 117, 117, 118, 118, 118, 118, 119, 119, 119, 119,
    120, 120, 120, 120, 121, 121, 121, 121, 122, 122, 122, 122, 123, 123, 123, 123,
    124, 124, 124, 124, 125, 125, 125, 125, 126, 126, 126, 126, 127, 127, 127, 127,
    128, 128, 128, 128, 129, 129, 129, 129, 130, 130, 130, 130, 131, 131, 131, 131,
    132, 132, 132, 132, 133, 133, 133, 133, 134, 134, 134, 134, 135, 135, 135, 135,
    136, 136, 136, 136, 137, 137, 137, 137, 138, 138, 138, 138, 139, 139, 139, 139,
    140, 140, 140, 140, 141, 141, 141, 141, 142, 142, 142, 142, 143, 143, 143, 143,
    144, 144, 144, 144, 145, 145, 145, 145, 146, 146, 146, 146, 147, 147, 147, 147,
    148, 148, 148, 148, 149, 149, 149, 149, 150, 150, 150, 150, 151, 151, 151, 151,
    152, 152, 152, 152, 153, 153, 153, 153, 154, 154, 154, 154, 155, 155, 155, 155,
    156, 156, 156, 156, 157, 157, 157, 157, 158, 158, 158, 158, 159, 159, 159, 159,
    160, 160, 160, 160, 161, 161, 161, 161, 162, 162, 162, 162, 163, 163, 163, 163,
    164, 164, 164, 164, 165, 165, 165, 165, 166, 166, 166, 166, 167, 167, 167, 167,
    168, 168, 168, 168, 169, 169, 169, 169, 170, 170, 170, 170, 171, 171, 171, 171,
    172, 172, 172, 172, 173, 173, 173, 173, 174, 174, 174, 174, 175, 175, 175, 175,
    176, 176, 176, 176, 177, 177, 177, 177, 178, 178, 178, 178, 179, 179, 179, 179,
    180, 180, 180, 180, 181, 181, 181, 181, 182, 182, 182, 182, 183, 183, 183, 183,
    184, 184, 184, 184, 185, 185, 185, 185, 186, 186, 186, 186, 187, 187, 187, 187,
    188, 188, 188, 188, 189, 189, 189, 189, 190, 190, 190, 190, 191, 191, 191, 191,
    192, 192, 192, 192, 193, 193, 193, 193, 194, 194, 194, 194, 195, 195, 195, 195,
    196, 196, 196, 196, 197, 197, 197, 197, 198, 198, 198, 198, 199, 199, 199, 199,
    200, 200, 200, 200, 201, 201, 201, 201, 202, 202, 202, 202, 203, 203, 203, 203,
    204, 204, 204, 204, 205, 205, 205, 205, 206, 206, 206, 206, 207, 207, 207, 207,
    208, 208, 208, 208, 209, 209, 209, 209, 210, 210, 210, 210, 211, 211, 211, 211,
    212, 212, 212, 212, 213, 213, 213, 213, 214, 214, 214, 214, 215, 215, 215, 215,
    216, 216, 216, 216, 217, 217, 217, 217, 218, 218, 218, 218, 219, 219, 219, 219,
    220, 220, 220, 220, 221, 221, 221, 221, 222, 222, 222, 222, 223, 223, 223, 223,
    224, 224, 224, 224, 225, 225, 225, 225, 226, 226, 226, 226, 227, 227, 227, 227,
    228, 228, 228, 228, 229, 229, 229, 229, 230, 230, 230, 230, 231, 231, 231, 231,
    232, 232, 232, 232, 233, 233, 233, 233, 234, 234, 234, 234, 235, 235, 235, 235,
    236, 236, 236, 236, 237, 237, 237, 237, 238, 238, 238, 238, 239, 239, 239, 239,
    240, 240, 240, 240, 241, 241, 241, 241, 242, 242, 242, 242, 243, 243, 243, 243,
    244, 244, 244, 244, 245, 245, 245, 245, 246, 246, 246, 246, 247, 247, 247, 247,
    248, 248, 248, 248, 249, 249, 249, 249, 250, 250, 250, 250, 251, 251, 251, 251,
    252, 252, 252, 252, 253, 253, 253, 253, 254, 254, 254, 254, 255, 255, 255, 255,
    256, 256, 256, 256, 257, 257, 257, 257, 258, 258, 258, 258, 259, 259, 259, 259,
    260, 260, 260, 260, 261, 261, 261, 261, 262, 262, 262, 262, 263, 263, 263, 263,
    264, 264, 264, 264, 265, 265, 265, 265, 266, 266, 266, 266, 267, 267, 267, 267,
    268, 268, 268, 268, 269, 269, 269, 269, 270, 270, 270, 270, 271, 271, 271, 271,
    272, 272, 272, 272, 273, 273, 273, 273, 274, 274, 274, 274, 275, 275, 275, 275,
    276, 276, 276, 276, 277, 277, 277, 277, 278, 278, 278, 278, 279, 279, 279, 279,
    280, 280, 280, 280, 281, 281, 281, 281, 282, 282, 282, 282, 283, 283, 283, 283,
    284, 284, 284, 284, 285, 285, 285, 285, 286, 286, 286, 286, 287, 287, 287, 287,
    288, 288, 288, 288, 289, 289, 289, 289, 290, 290, 290, 290, 291, 291, 291, 291,
};

static RE_UINT16 re_block_stage_5[] = {
      1,   1,   1,   1,   2,   2,   2,   2,   3,   3,   3,   3,   4,   4,   4,   4,
      5,   5,   5,   5,   6,   6,   6,   6,   7,   7,   7,   7,   8,   8,   8,   8,
      9,   9,   9,   9,  10,  10,  10,  10,  11,  11,  11,  11,  12,  12,  12,  12,
     13,  13,  13,  13,  14,  14,  14,  14,  15,  15,  15,  15,  16,  16,  16,  16,
     17,  17,  17,  17,  18,  18,  18,  18,  19,  19,  19,  19,  20,  20,  20,  20,
      0,   0,   0,   0,  21,  21,  21,  21,  22,  22,  22,  22,  23,  23,  23,  23,
     24,  24,  24,  24,  25,  25,  25,  25,  26,  26,  26,  26,  27,  27,  27,  27,
     28,  28,  28,  28,  29,  29,  29,  29,  30,  30,  30,  30,  31,  31,  31,  31,
     32,  32,  32,  32,  33,  33,  33,  33,  34,  34,  34,  34,  35,  35,  35,  35,
     36,  36,  36,  36,  37,  37,  37,  37,  38,  38,  38,  38,  39,  39,  39,  39,
     40,  40,  40,  40,  41,  41,  41,  41,  42,  42,  42,  42,  43,  43,  43,  43,
     44,  44,  44,  44,  45,  45,  45,  45,  46,  46,  46,  46,  47,  47,  47,  47,
     48,  48,  48,  48,  49,  49,  49,  49,  50,  50,  50,  50,  51,  51,  51,  51,
     52,  52,  52,  52,  53,  53,  53,  53,  54,  54,  54,  54,  55,  55,  55,  55,
     56,  56,  56,  56,  57,  57,  57,  57,  58,  58,  58,  58,  59,  59,  59,  59,
     60,  60,  60,  60,  61,  61,  61,  61,  62,  62,  62,  62,  63,  63,  63,  63,
     64,  64,  64,  64,  65,  65,  65,  65,  66,  66,  66,  66,  67,  67,  67,  67,
     68,  68,  68,  68,  69,  69,  69,  69,  70,  70,  70,  70,  71,  71,  71,  71,
     72,  72,  72,  72,  73,  73,  73,  73,  74,  74,  74,  74,  75,  75,  75,  75,
     76,  76,  76,  76,  77,  77,  77,  77,  78,  78,  78,  78,  79,  79,  79,  79,
     80,  80,  80,  80,  81,  81,  81,  81,  82,  82,  82,  82,  83,  83,  83,  83,
     84,  84,  84,  84,  85,  85,  85,  85,  86,  86,  86,  86,  87,  87,  87,  87,
     88,  88,  88,  88,  89,  89,  89,  89,  90,  90,  90,  90,  91,  91,  91,  91,
     92,  92,  92,  92,  93,  93,  93,  93,  94,  94,  94,  94,  95,  95,  95,  95,
     96,  96,  96,  96,  97,  97,  97,  97,  98,  98,  98,  98,  99,  99,  99,  99,
    100, 100, 100, 100, 101, 101, 101, 101, 102, 102, 102, 102, 103, 103, 103, 103,
    104, 104, 104, 104, 105, 105, 105, 105, 106, 106, 106, 106, 107, 107, 107, 107,
    108, 108, 108, 108, 109, 109, 109, 109, 110, 110, 110, 110, 111, 111, 111, 111,
    112, 112, 112, 112, 113, 113, 113, 113, 114, 114, 114, 114, 115, 115, 115, 115,
    116, 116, 116, 116, 117, 117, 117, 117, 118, 118, 118, 118, 119, 119, 119, 119,
    120, 120, 120, 120, 121, 121, 121, 121, 122, 122, 122, 122, 123, 123, 123, 123,
    124, 124, 124, 124, 125, 125, 125, 125, 126, 126, 126, 126, 127, 127, 127, 127,
    128, 128, 128, 128, 129, 129, 129, 129, 130, 130, 130, 130, 131, 131, 131, 131,
    132, 132, 132, 132, 133, 133, 133, 133, 134, 134, 134, 134, 135, 135, 135, 135,
    136, 136, 136, 136, 137, 137, 137, 137, 138, 138, 138, 138, 139, 139, 139, 139,
    140, 140, 140, 140, 141, 141, 141, 141, 142, 142, 142, 142, 143, 143, 143, 143,
    144, 144, 144, 144, 145, 145, 145, 145, 146, 146, 146, 146, 147, 147, 147, 147,
    148, 148, 148, 148, 149, 149, 149, 149, 150, 150, 150, 150, 151, 151, 151, 151,
    152, 152, 152, 152, 153, 153, 153, 153, 154, 154, 154, 154, 155, 155, 155, 155,
    156, 156, 156, 156, 157, 157, 157, 157, 158, 158, 158, 158, 159, 159, 159, 159,
    160, 160, 160, 160, 161, 161, 161, 161, 162, 162, 162, 162, 163, 163, 163, 163,
    164, 164, 164, 164, 165, 165, 165, 165, 166, 166, 166, 166, 167, 167, 167, 167,
    168, 168, 168, 168, 169, 169, 169, 169, 170, 170, 170, 170, 171, 171, 171, 171,
    172, 172, 172, 172, 173, 173, 173, 173, 174, 174, 174, 174, 175, 175, 175, 175,
    176, 176, 176, 176, 177, 177, 177, 177, 178, 178, 178, 178, 179, 179, 179, 179,
    180, 180, 180, 180, 181, 181, 181, 181, 182, 182, 182, 182, 183, 183, 183, 183,
    184, 184, 184, 184, 185, 185, 185, 185, 186, 186, 186, 186, 187, 187, 187, 187,
    188, 188, 188, 188, 189, 189, 189, 189, 190, 190, 190, 190, 191, 191, 191, 191,
    192, 192, 192, 192, 193, 193, 193, 193, 194, 194, 194, 194, 195, 195, 195, 195,
    196, 196, 196, 196, 197, 197, 197, 197, 198, 198, 198, 198, 199, 199, 199, 199,
    200, 200, 200, 200, 201, 201, 201, 201, 202, 202, 202, 202, 203, 203, 203, 203,
    204, 204, 204, 204, 205, 205, 205, 205, 206, 206, 206, 206, 207, 207, 207, 207,
    208, 208, 208, 208, 209, 209, 209, 209, 210, 210, 210, 210, 211, 211, 211, 211,
    212, 212, 212, 212, 213, 213, 213, 213, 214, 214, 214, 214, 215, 215, 215, 215,
    216, 216, 216, 216, 217, 217, 217, 217, 218, 218, 218, 218, 219, 219, 219, 219,
    220, 220, 220, 220, 221, 221, 221, 221, 222, 222, 222, 222, 223, 223, 223, 223,
    224, 224, 224, 224, 225, 225, 225, 225, 226, 226, 226, 226, 227, 227, 227, 227,
    228, 228, 228, 228, 229, 229, 229, 229, 230, 230, 230, 230, 231, 231, 231, 231,
    232, 232, 232, 232, 233, 233, 233, 233, 234, 234, 234, 234, 235, 235, 235, 235,
    236, 236, 236, 236, 237, 237, 237, 237, 238, 238, 238, 238, 239, 239, 239, 239,
    240, 240, 240, 240, 241, 241, 241, 241, 242, 242, 242, 242, 243, 243, 243, 243,
    244, 244, 244, 244, 245, 245, 245, 245, 246, 246, 246, 246, 247, 247, 247, 247,
    248, 248, 248, 248, 249, 249, 249, 249, 250, 250, 250, 250, 251, 251, 251, 251,
    252, 252, 252, 252, 253, 253, 253, 253, 254, 254, 254, 254, 255, 255, 255, 255,
    256, 256, 256, 256, 257, 257, 257, 257, 258, 258, 258, 258, 259, 259, 259, 259,
    260, 260, 260, 260, 261, 261, 261, 261, 262, 262, 262, 262, 263, 263, 263, 263,
    264, 264, 264, 264, 265, 265, 265, 265, 266, 266, 266, 266, 267, 267, 267, 267,
    268, 268, 268, 268, 269, 269, 269, 269, 270, 270, 270, 270, 271, 271, 271, 271,
    272, 272, 272, 272, 273, 273, 273, 273, 274, 274, 274, 274, 275, 275, 275, 275,
    276, 276, 276, 276, 277, 277, 277, 277, 278, 278, 278, 278, 279, 279, 279, 279,
    280, 280, 280, 280, 281, 281, 281, 281, 282, 282, 282, 282, 283, 283, 283, 283,
    284, 284, 284, 284, 285, 285, 285, 285, 286, 286, 286, 286, 287, 287, 287, 287,
    288, 288, 288, 288, 289, 289, 289, 289, 290, 290, 290, 290, 291, 291, 291, 291,
};

/* Block: 9664 bytes. */

RE_UINT32 re_get_block(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 11;
    code = ch ^ (f << 11);
    pos = (RE_UINT32)re_block_stage_1[f] << 4;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_block_stage_2[pos + f] << 3;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_block_stage_3[pos + f] << 2;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_block_stage_4[pos + f] << 2;
    value = re_block_stage_5[pos + code];

    return value;
}

/* Script. */

static RE_UINT8 re_script_stage_1[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  9, 10, 11, 12, 12, 12, 12, 13, 14, 14, 14, 14, 15,
    16, 17, 18, 19, 20, 14, 21, 14, 22, 14, 14, 14, 14, 23, 24, 24,
    25, 26, 14, 14, 14, 14, 27, 28, 14, 14, 29, 30, 31, 32, 33, 34,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7, 35,  7, 36, 37,  7, 38,  7,  7,  7, 39, 14, 40,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    41, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
};

static RE_UINT8 re_script_stage_2[] = {
      0,   1,   2,   2,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,
     14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,
     30,  31,  32,  32,  33,  34,  35,  36,  37,  37,  37,  37,  37,  38,  39,  40,
     41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,   2,   2,  53,  54,
     55,  56,  57,  58,  59,  59,  59,  59,  60,  59,  59,  59,  59,  59,  59,  59,
     61,  61,  59,  59,  59,  59,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,
     72,  73,  74,  75,  76,  77,  78,  59,  70,  70,  70,  70,  70,  70,  70,  70,
     70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,
     70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  79,  70,  70,  70,  70,
     70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  80,
     81,  81,  81,  81,  81,  81,  81,  81,  81,  82,  83,  83,  84,  85,  86,  87,
     88,  89,  90,  91,  92,  93,  94,  95,  32,  32,  32,  32,  32,  32,  32,  32,
     32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,
     32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  96,
     97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,
     97,  97,  70,  70,  98,  99, 100, 101, 102, 102, 103, 104, 105, 106, 107, 108,
    109, 110, 111, 112,  97, 113, 114, 115, 116, 117, 118,  97, 119, 119, 120,  97,
    121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131,  97, 132,  97, 133,  97,
    134, 135, 136, 137, 138, 139, 140,  97, 141, 142,  97, 143, 144, 145, 146,  97,
    147, 148,  97,  97, 149, 150,  97,  97, 151, 152, 153, 154,  97, 155,  97,  97,
    156, 156, 156, 156, 156, 156, 156, 157, 158, 156, 159,  97,  97,  97,  97,  97,
    160, 160, 160, 160, 160, 160, 160, 160, 161,  97,  97,  97,  97,  97,  97,  97,
     97,  97,  97,  97,  97,  97,  97,  97, 162, 162, 162, 162, 163,  97,  97,  97,
    164, 164, 164, 164, 165, 166, 167, 168,  97,  97,  97,  97, 169, 170, 171, 172,
    173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173,
    173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 174,
    173, 173, 173, 173, 173, 175,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,
    176, 177, 178, 179, 179, 180,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,
     97,  97,  97,  97,  97,  97,  97,  97, 181, 182,  97,  97,  97,  97,  97,  97,
     59, 183, 184, 185, 186, 187, 188,  97, 189, 190, 191,  59,  59, 192,  59, 193,
    194, 194, 194, 194, 194, 195,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,
    196,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,
    197, 198, 199,  97,  97,  97,  97,  97, 200, 201,  97,  97, 202, 203,  97,  97,
    204, 205, 206, 207, 208,  97,  59,  59,  59,  59,  59,  59,  59, 209, 210, 211,
    212, 213, 214, 215, 216,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,
     70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70, 217,  70,  70,
     70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70, 218,  70,
    219,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,
     70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70, 220,  70,  70,
     70,  70,  70,  70,  70,  70,  70, 221,  97,  97,  97,  97,  97,  97,  97,  97,
     70,  70,  70,  70, 222,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,
    223,  97, 224, 225,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,
};

static RE_UINT16 re_script_stage_3[] = {
      0,   0,   0,   0,   1,   2,   1,   2,   0,   0,   3,   3,   4,   5,   4,   5,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   6,   0,   0,   7,   0,
      8,   8,   8,   8,   8,   8,   8,   9,  10,  11,  12,  11,  11,  11,  13,  11,
     14,  14,  14,  14,  14,  14,  14,  14,  15,  14,  14,  14,  14,  14,  14,  14,
     14,  14,  14,  16,  17,  18,  17,  17,  19,  20,  21,  21,  22,  21,  23,  24,
     25,  26,  27,  27,  28,  29,  27,  30,  27,  27,  27,  27,  27,  31,  27,  27,
     32,  33,  33,  33,  34,  27,  27,  27,  35,  35,  35,  36,  37,  37,  37,  38,
     39,  39,  40,  41,  42,  43,  44,  45,  45,  45,  27,  46,  45,  47,  48,  27,
     49,  49,  49,  49,  49,  50,  51,  49,  52,  53,  54,  55,  56,  57,  58,  59,
     60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,
     76,  77,  78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,
     92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103, 104, 105, 106, 107,
    108, 109, 110, 110, 111, 112, 113, 110, 114, 115, 116, 117, 118, 119, 120, 121,
    122, 123, 123, 124, 123, 125,  45,  45, 126, 127, 128, 129, 130, 131,  45,  45,
    132, 132, 132, 132, 133, 132, 134, 135, 132, 133, 132, 136, 136, 137,  45,  45,
    138, 138, 138, 138, 138, 138, 138, 138, 138, 138, 139, 139, 140, 139, 139, 141,
    142, 142, 142, 142, 142, 142, 142, 142, 143, 143, 143, 143, 144, 145, 143, 143,
    144, 143, 143, 146, 147, 148, 143, 143, 143, 147, 143, 143, 143, 149, 143, 150,
    143, 151, 152, 152, 152, 152, 152, 153, 154, 154, 154, 154, 154, 154, 154, 154,
    155, 156, 157, 157, 157, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167,
    168, 168, 168, 168, 168, 169, 170, 170, 171, 172, 173, 173, 173, 173, 173, 174,
    173, 173, 175, 154, 154, 154, 154, 176, 177, 178, 179, 179, 180, 181, 182, 183,
    184, 184, 185, 184, 186, 187, 168, 168, 188, 189, 190, 190, 190, 191, 190, 192,
    193, 193, 194, 195,  45,  45,  45,  45, 196, 196, 196, 196, 197, 196, 196, 198,
    199, 199, 199, 199, 200, 200, 200, 201, 202, 202, 202, 203, 204, 205, 205, 205,
    206, 139, 139, 207, 208, 209, 210, 211,   4,   4, 212,   4,   4, 213, 214, 215,
      4,   4,   4, 216,   8,   8,   8, 217,  11, 218,  11,  11, 218, 219,  11, 220,
     11,  11,  11, 221, 221, 222,  11, 223, 224,   0,   0,   0,   0,   0, 225, 226,
    227, 228,   0,   0,  45,   8,   8, 229,   0,   0, 230, 231, 232,   0,   4,   4,
    233,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0, 234,  45, 235,  45,   0,   0, 236, 236, 236, 236, 236, 236, 236, 236,
      0,   0,   0,   0,   0,   0,   0, 237,   0, 238,   0,   0, 239,   0,   0, 227,
    240, 240, 241, 240, 240, 241,   4,   4, 242, 242, 242, 242, 242, 242, 242, 243,
    139, 139, 140, 244, 244, 244, 245, 246, 143, 247, 248, 248, 248, 248,  14,  14,
      0,   0,   0,   0, 227,  45,  45,  45, 249, 250, 249, 249, 249, 249, 249, 251,
    249, 249, 249, 249, 249, 249, 249, 249, 249, 249, 249, 249, 249, 252,  45, 253,
    254,   0, 255, 256, 257, 258, 258, 258, 258, 259, 260, 261, 261, 261, 261, 262,
    263, 264, 264, 265, 142, 142, 142, 142, 266,   0, 264, 267,   0,   0, 268, 261,
    142, 266,   0,   0,   0,   0, 142, 269,   0,   0,   0,   0,   0, 261, 261, 270,
    261, 261, 261, 261, 261, 271,   0,   0, 249, 249, 249, 252,   0,   0,   0,   0,
    249, 249, 249, 249, 249, 249, 249,  45, 272, 272, 272, 272, 272, 272, 272, 272,
    273, 272, 272, 272, 274, 275, 275, 275, 276, 276, 276, 276, 276, 276, 276, 276,
    276, 276, 277,  45,  14,  14,  14,  14,  14,  14, 278, 278, 278, 278, 278, 279,
      0,   0, 280,   4,   4,   4,   4,   4, 281,   4,   4, 282,  45,  45,  45, 283,
    284, 284, 285, 286, 287, 287, 287, 288, 289, 289, 289, 289, 290, 291,  49,  49,
    292, 292, 293, 294, 294, 295, 142, 296, 297, 297, 297, 297, 298, 299, 138, 300,
    301, 301, 301, 302, 303, 304, 138, 138, 305, 305, 305, 305, 306, 307, 308, 309,
    310, 311, 248,   4,   4, 312, 313, 152, 152, 152, 152, 152, 308, 308, 314, 315,
    142, 142, 316, 142, 317, 142, 142, 318,  45,  45,  45,  45,  45,  45,  45,  45,
    249, 249, 249, 249, 249, 249, 319, 249, 249, 249, 249, 249, 249, 320,  45,  45,
    321, 322,  21, 323, 324,  27,  27,  27,  27,  27,  27,  27, 325,  47,  27,  27,
     27,  27,  27,  27,  27,  27,  27,  27,  27,  27,  27, 326,  45,  27,  27,  27,
     27, 327,  27,  27, 328,  45,  45, 329,   8, 286, 330,   0,   0, 331, 332, 333,
     27,  27,  27,  27,  27,  27,  27, 334, 335,   0,   1,   2,   1,   2, 336, 260,
    261, 337, 142, 266, 338, 339, 340, 341, 342, 343, 344, 345, 346, 346,  45,  45,
    343, 343, 343, 343, 343, 343, 343, 347, 348,   0,   0, 349,  11,  11,  11,  11,
    350, 253, 351,  45,  45,   0,   0, 352, 353, 354, 355, 355, 355, 356, 357, 253,
    358, 358, 359, 360, 361, 362, 362, 363, 364, 365, 366, 366, 367, 368,  45,  45,
    369, 369, 369, 369, 369, 370, 370, 370, 371, 372, 373, 374, 374, 375, 374, 376,
    377, 377, 378, 379, 379, 379, 380,  45, 381, 381, 381, 381, 381, 381, 381, 381,
    381, 381, 381, 382, 381, 383, 384,  45, 385, 386, 386, 387, 388, 389, 390, 390,
    391, 392, 393,  45,  45,  45, 394, 395, 396, 397, 398, 399,  45,  45,  45,  45,
    400, 400, 401, 402, 401, 403, 401, 401, 404, 405, 406, 407, 408, 408, 409, 409,
    410, 410,  45,  45, 411, 411, 412, 413, 414, 414, 414, 415, 416, 417, 418, 419,
    420, 421, 422,  45,  45,  45,  45,  45, 423, 423, 423, 423, 424,  45,  45,  45,
    425, 425, 425, 426, 425, 425, 425, 427, 428, 428, 429, 430,  45,  45,  45,  45,
     45,  45,  45,  45,  45,  45,  27, 431, 432, 432, 433, 434, 434, 435,  45,  45,
    436, 436, 436, 436, 437, 438, 436, 439, 440, 440, 440, 440, 441, 442, 443, 444,
    445, 445, 445, 446, 447, 448, 448, 449, 450, 450, 450, 450, 451, 450, 452, 453,
    454, 455, 454, 456,  45,  45,  45,  45, 457, 458, 459, 460, 460, 460, 461, 462,
    463, 464, 465, 466, 467, 468, 469, 470, 471, 471, 471, 471, 471, 472,  45,  45,
    473, 473, 473, 473, 474, 475,  45,  45, 476, 476, 476, 477, 476, 478,  45,  45,
    479, 479, 479, 479, 480, 481, 482,  45, 483, 483, 483, 484, 485,  45,  45,  45,
    486, 487, 488, 486,  45,  45,  45,  45, 489, 489, 489, 490,  45,  45,  45,  45,
     45,  45, 491, 491, 491, 491, 491, 492, 493, 493, 493, 493, 494, 495, 495, 495,
    496, 495, 497,  45, 498, 498, 498, 499, 500, 501, 501, 502, 503, 501, 504, 505,
    505, 506, 507, 508,  45,  45,  45,  45, 509, 510, 510, 511, 512, 513, 514, 515,
    516, 517, 518,  45,  45,  45,  45,  45,  45,  45,  45,  45,  45,  45, 519, 520,
    521, 521, 521, 521, 521, 521, 521, 521, 521, 522,  45,  45,  45,  45,  45,  45,
    521, 521, 521, 521, 521, 521, 523, 524, 521, 521, 521, 521, 525,  45,  45,  45,
    526, 526, 526, 526, 526, 526, 526, 526, 526, 526, 527,  45,  45,  45,  45,  45,
    528, 528, 528, 528, 528, 528, 528, 528, 528, 528, 528, 528, 529,  45,  45,  45,
    278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 530, 531, 532, 533,  45,
     45,  45,  45,  45,  45, 534, 535, 536, 537, 537, 537, 537, 538, 539, 540, 541,
    537,  45,  45,  45,  45,  45,  45,  45,  45,  45,  45,  45, 542, 542, 542, 542,
    542, 543,  45,  45,  45,  45,  45,  45, 544, 544, 544, 544, 545, 544, 544, 546,
    547, 544,  45,  45,  45,  45, 548,  45, 549, 549, 549, 549, 549, 549, 549, 549,
    549, 549, 549, 549, 549, 549, 549, 550, 549, 549, 549, 549, 549, 549, 549, 551,
    552, 258, 258, 258, 258, 258, 258, 258, 258, 258, 258, 258, 258, 258, 258, 258,
    258, 553,  45,  45,  45,  45,  45, 554, 554, 554, 554, 554, 554, 554, 554, 554,
    554, 554, 554, 554, 554, 554, 554, 555, 556, 556, 556, 556, 556, 556, 557, 558,
    559, 560, 268,  45,  45,  45,  45,  45,   0,   0,   0,   0,   0,   0,   0, 561,
      0,   0, 562,   0,   0,   0, 563, 564, 565,   0, 566,   0,   0,   0, 567,  45,
     11,  11,  11,  11, 568,  45,  45,  45,  45,  45,  45,  45,  45,  45,   0, 268,
      0,   0,   0,   0,   0, 234,   0, 567,   0,   0,   0,   0,   0, 225,   0,   0,
      0, 569, 570, 571, 572,   0,   0,   0, 573, 574,   0, 575, 576, 577,   0,   0,
      0,   0, 238,   0,   0,   0,   0,   0,   0,   0,   0,   0, 578,   0,   0,   0,
    579, 579, 579, 579, 579, 579, 579, 579, 580, 581, 582,  45,  45,  45,  45,  45,
    583, 584, 585,  45,  45,  45,  45,  45, 586, 586, 586, 586, 586, 586, 586, 586,
    586, 586, 586, 586, 587, 588,  45,  45, 589, 589, 589, 589, 590, 591,  45,  45,
     45,  45,  45,  45,  45,  45,  45, 335,   0,   0,   0, 592,  45,  45,  45,  45,
    593,  27, 594, 595, 596, 597, 598, 599, 600, 601, 602, 601,  45,  45,  45, 325,
      0,   0, 253,   0,   0,   0,   0,   0,   0, 268, 227, 335, 335, 335,   0, 561,
    603,   0,   0,   0,   0,   0, 253,   0,   0,   0, 603,  45,  45,  45, 604,   0,
    605,   0,   0, 253, 567, 606, 561,  45,   0,   0,   0,   0,   0, 592, 603, 286,
      0,   0,   0,   0,   0,   0,   0, 268,   0,   0,   0,   0,   0, 567,  45,  45,
    253,   0,   0,   0, 607, 286,   0,   0, 607,   0, 608,  45,  45,  45,  45,  45,
    253,   0,   0, 227,   0,   0,   0, 609,   0,   0, 610, 286, 610,   0,   0,   0,
     45,  45,  45,  45,  45,  45, 608,  45, 249, 249, 249, 249, 249, 611,  45,  45,
    249, 249, 249, 612, 249, 249, 249, 249, 249, 319, 249, 249, 249, 249, 249, 249,
    249, 249, 613, 249, 249, 249, 249, 249, 249, 249, 249, 249, 249, 249, 614,  45,
    249, 319,  45,  45,  45,  45,  45,  45, 615,  45,   0,   0,   0,   0,   0,   0,
      8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,  45,
};

static RE_UINT16 re_script_stage_4[] = {
      0,   0,   0,   0,   1,   2,   2,   2,   2,   2,   3,   0,   0,   0,   4,   0,
      2,   2,   2,   2,   2,   3,   2,   2,   2,   2,   5,   0,   2,   5,   6,   0,
      7,   7,   7,   7,   8,   9,  10,  11,  12,  13,  14,  15,   8,   8,   8,   8,
     16,   8,   8,   8,  17,  18,  18,  18,  19,  19,  19,  19,  19,  20,  19,  19,
     21,  22,  22,  22,  22,  22,  22,  22,  22,  23,  21,  22,  22,  22,  24,  21,
     25,  26,  26,  26,  26,  26,  26,  26,  26,  26,  12,  12,  26,  26,  27,  28,
     26,  29,  12,  12,  30,  31,  30,  32,  30,  30,  33,  34,  30,  30,  30,  30,
     32,  30,  35,   7,   7,  36,  30,  30,  37,  30,  30,  30,  30,  30,  30,  31,
     38,  38,  38,  39,  38,  38,  38,  38,  38,  38,  40,  41,  42,  42,  42,  42,
     43,  12,  12,  12,  44,  44,  44,  44,  44,  44,  45,  46,  47,  47,  47,  47,
     47,  47,  47,  48,  47,  47,  47,  49,  50,  50,  50,  50,  50,  50,  50,  51,
     38,  38,  40,  12,  12,  12,  12,  12,  30,  52,  30,  53,  54,  30,  30,  30,
     55,  30,  30,  30,  56,  56,  56,  56,  57,  56,  56,  56,  56,  58,  56,  56,
     59,  60,  59,  61,  61,  59,  59,  59,  59,  59,  62,  59,  63,  64,  65,  59,
     59,  61,  61,  66,  12,  67,  12,  68,  59,  64,  59,  59,  59,  59,  59,  66,
     69,  69,  70,  71,  72,  73,  73,  73,  73,  73,  74,  73,  74,  75,  76,  74,
     70,  71,  72,  76,  77,  12,  69,  78,  12,  79,  73,  73,  73,  70,  12,  12,
     80,  80,  81,  82,  82,  81,  81,  81,  81,  81,  83,  81,  83,  80,  84,  81,
     81,  82,  82,  84,  85,  12,  12,  12,  81,  86,  81,  81,  84,  12,  80,  81,
     87,  87,  88,  89,  89,  88,  88,  88,  88,  88,  90,  88,  90,  87,  91,  88,
     88,  89,  89,  91,  12,  92,  12,  93,  88,  92,  88,  88,  88,  88,  12,  12,
     94,  95,  96,  94,  97,  98,  99,  97, 100, 101,  96,  94, 102, 102,  98,  94,
     96,  94,  97,  98, 101, 100,  12,  12,  12,  94, 102, 102, 102, 102,  96,  12,
    103, 103, 103, 104, 104, 103, 103, 103, 103, 103, 104, 103, 103, 103, 105, 106,
    103, 104, 104, 105,  12, 107, 108,  12, 103, 109, 103, 103,  12,  12, 103, 103,
    110, 110, 110, 111, 111, 110, 110, 110, 110, 110, 111, 110, 110, 112, 113, 110,
    110, 111, 111, 113,  12, 114,  12, 115, 110, 116, 110, 110, 114,  12,  12,  12,
    117, 118, 117, 119, 119, 117, 117, 117, 117, 117, 117, 117, 117, 119, 119, 117,
     12, 117, 117, 117, 117, 120, 117, 117, 121, 122, 123, 123, 123, 124, 121, 123,
    123, 123, 123, 123, 125, 123, 123, 126, 123, 124, 127, 128, 123, 129, 123, 123,
     12, 121, 123, 123, 121, 130,  12,  12, 131, 132, 132, 132, 132, 132, 132, 132,
    132, 132, 133, 134, 132, 132, 132,  12, 135, 136, 137, 138,  12, 139, 140, 139,
    140, 141, 142, 140, 139, 139, 143, 144, 139, 137, 139, 144, 139, 139, 144, 139,
    145, 145, 145, 145, 145, 145, 146, 145, 145, 145, 145, 147, 146, 145, 145, 145,
    145, 145, 145, 148, 145, 149, 150,  12, 151, 151, 151, 151, 152, 152, 152, 152,
    152, 153,  12, 154, 152, 152, 155, 152, 156, 156, 156, 156, 157, 157, 157, 157,
    157, 157, 158, 159, 157, 160, 158, 159, 158, 159, 157, 160, 158, 159, 157, 157,
    157, 160, 157, 157, 157, 157, 160, 161, 157, 157, 157, 162, 157, 157, 159,  12,
    163, 163, 163, 163, 163, 164, 163, 164, 165, 165, 165, 165, 166, 166, 166, 166,
    166, 166, 166, 167, 168, 168, 168, 168, 168, 168, 169, 170, 168, 168, 171,  12,
    172, 172, 172, 173, 172, 174,  12,  12, 175, 175, 175, 175, 175, 176,  12,  12,
    177, 177, 177, 177, 177,  12,  12,  12, 178, 178, 178, 179, 179,  12,  12,  12,
    180, 180, 180, 180, 180, 180, 180, 181, 180, 180, 181,  12, 182, 183, 184, 185,
    184, 184, 186,  12, 184, 184, 184, 184, 184, 184, 187,  12, 184, 184, 185,  12,
    165, 188,  12,  12, 189, 189, 189, 189, 189, 189, 189, 190, 189, 189, 189,  12,
    191, 189, 189, 189, 192, 192, 192, 192, 192, 192, 192, 193, 192, 194,  12,  12,
    195, 195, 195, 195, 195, 195, 195,  12, 195, 195, 196,  12, 195, 195, 197, 198,
    199, 199, 199, 199, 199, 199, 199, 200, 201, 201, 201, 201, 201, 201, 201, 202,
    201, 201, 201, 203, 201, 201, 204,  12, 201, 201, 201, 204,   7,   7,   7, 205,
    206, 206, 206, 206, 206, 206, 206,  12, 206, 206, 206, 207, 208, 208, 208, 208,
    209, 209, 209, 209, 209,  12,  12, 209, 210, 210, 210, 210, 210, 210, 211, 210,
    210, 210, 212, 213, 214, 214, 214, 214,  19,  19, 215,  12, 152, 152, 216, 217,
    208, 208,  12,  12, 218,   7,   7,   7, 219,   7, 220, 221,   0, 220, 222,  12,
      2, 223, 224,   2,   2,   2,   2, 225, 226, 223, 227,   2,   2,   2, 228,   2,
      2,   2,   2, 229,   7,   7, 230,   7,   8, 231,   8, 231,   8,   8, 232, 232,
      8,   8,   8, 231,   8,  15,   8,   8,   8,  10,   8, 233,  10,  15,   8,  14,
      0,   0,   0, 234,   0, 235,   0,   0, 236,   0,   0, 237,   0,   0,   0, 238,
      2,   2,   2, 239, 240,  12,  12,  12,   0, 241, 242,   0,   4,   0,   0,   0,
      0,   0,   0,   4,   2,   2,   5,  12,   0, 238,  12,  12,   0,   0, 238,  12,
    243, 243, 243, 243,   0, 244,   0,   0,   0, 245,   0,   0,   0,   0, 235,   0,
    246, 246, 246, 246, 246, 246, 246, 247,  18,  18,  18,  18,  18,  12, 248,  18,
    249, 249, 249, 249, 249, 249,  12, 250, 251,  12,  12, 250, 157, 160,  12,  12,
    157, 160, 157, 160, 252, 252, 252, 252, 252, 252, 253, 252, 252,  12,  12,  12,
    252, 254,  12,  12,   0,   0,   0,  12,   0, 255,   0,   0, 256, 252, 257, 258,
      0,   0, 252,   0, 259, 260, 260, 260, 260, 260, 260, 260, 260, 261, 262, 263,
    264, 265, 265, 265, 265, 265, 265, 265, 265, 265, 266, 264,  12, 267, 268, 268,
    268, 268, 268, 268, 269, 156, 156, 156, 156, 156, 156, 270, 268, 268, 271,  12,
      0,  12,  12,  12, 156, 156, 156, 272, 265, 265, 265, 273, 265, 265,   0,   0,
    274, 274, 274, 274, 274, 274, 274, 275, 274, 276,  12,  12, 277, 277, 277, 277,
    278, 278, 278, 278, 278, 278, 278,  12, 279, 279, 279, 279, 279, 279,  12,  12,
    242,   2,   2,   2,   2,   2, 237,   2,   2,   2, 280,  12,  12, 281,   2,   2,
    282, 282, 282, 282, 282, 282, 282,  12,   0,   0, 245,  12, 283, 283, 283, 283,
    283, 283,  12,  12, 284, 284, 284, 284, 284, 285,  12, 286, 284, 284, 285,  12,
    287, 287, 287, 287, 287, 287, 287, 288, 289, 289, 289, 289, 289,  12,  12, 290,
    156, 156, 156, 291, 292, 292, 292, 292, 292, 292, 292, 293, 292, 292, 294, 295,
    151, 151, 151, 296, 297, 297, 297, 297, 297, 298,  12,  12, 297, 297, 297, 299,
    297, 297, 299, 297, 300, 300, 300, 300, 301,  12,  12,  12,  12,  12, 302, 300,
    303, 303, 303, 303, 303, 304,  12,  12, 161, 160, 161, 160, 161, 160,  12,  12,
      2,   2,   3,   2,   2, 305,  12,  12, 303, 303, 303, 306, 303, 303, 306,  12,
    156,  12,  12,  12, 156, 270, 307, 156, 156, 156, 156,  12, 252, 252, 252, 254,
    252, 252, 254,  12,   2, 308,  12,  12, 309,  22,  12,  25,  26,  27,  26, 310,
    311, 312,  26,  26,  53,  12,  12,  12,  30,  30,  30, 313, 314,  30,  30,  30,
     30,  30,  12,  12,  30,  30,  30,  53,   7,   7,   7, 315, 238,   0,   0,   0,
      0, 238,   0,  12,  30,  52,  30,  30,  30,  30,  30, 316, 317,   0,   0,   0,
      0, 318, 265, 265, 265, 265, 265, 319, 320, 156, 320, 156, 320, 156, 320, 291,
      0, 238,   0, 238,  12,  12, 317, 245, 321, 321, 321, 322, 321, 321, 321, 321,
    321, 323, 321, 321, 321, 321, 323, 324, 321, 321, 321, 325, 321, 321, 323,  12,
    238, 134,   0,   0,   0, 134,   0,   0,   8,   8,   8,  14, 326,  12,  12,  12,
      0,   0,   0, 327, 328, 328, 328, 328, 328, 328, 328, 329, 330, 330, 330, 330,
    331,  12,  12,  12, 220,   0,   0,   0, 332, 332, 332, 332, 332,  12,  12, 333,
    334, 334, 334, 334, 334, 334, 335,  12, 336, 336, 336, 336, 336, 336, 337,  12,
    338, 338, 338, 338, 338, 338, 338, 339, 340, 340, 340, 340, 340,  12, 340, 340,
    340, 341,  12,  12, 342, 342, 342, 342, 343, 343, 343, 343, 344, 344, 344, 344,
    344, 344, 344, 345, 344, 344, 345,  12, 346, 346, 346, 346, 346,  12, 346, 346,
    346, 346, 346,  12, 347, 347, 347, 347, 347, 347,  12,  12, 348, 348, 348, 348,
    348,  12,  12, 349, 350, 350, 350, 350, 350, 351,  12,  12, 350, 352,  12,  12,
    350, 350,  12,  12, 353, 354, 355, 353, 353, 353, 353, 353, 353, 356, 357, 358,
    359, 359, 359, 359, 359, 360, 359, 359, 361, 361, 361, 361, 362, 362, 362, 362,
    362, 362, 362, 363,  12, 364, 362, 362, 365, 365, 365, 365, 366, 367, 368, 365,
    369, 369, 369, 369, 369, 369, 369, 370, 371, 371, 371, 371, 371, 371, 372, 373,
    374, 374, 374, 374, 375, 375, 375, 375, 375, 375,  12, 375, 376, 375, 375, 375,
    377, 378,  12, 377, 377, 379, 379, 377, 377, 377, 377, 377, 377, 380, 381, 382,
    377, 377, 383,  12, 384, 384, 384, 384, 385, 385, 385, 385, 386, 386, 386, 386,
    386, 387, 388, 386, 386, 387,  12,  12, 389, 389, 389, 389, 389, 390, 391, 389,
    392, 392, 392, 392, 392, 393, 392, 392, 394, 394, 394, 394, 395,  12, 394, 394,
    396, 396, 396, 396, 397,  12, 398, 399,  12,  12, 398, 396, 400, 400, 400, 400,
    400, 400, 401,  12, 402, 402, 402, 402, 403,  12,  12,  12, 403,  12, 404, 402,
    405, 405, 405, 405, 405, 405,  12,  12, 405, 405, 406,  12,  30,  30,  30, 407,
    408, 408, 408, 408, 408, 408,  12,  12, 409, 409, 409, 409, 409, 409, 410,  12,
    411, 411, 411, 411, 411, 411, 411, 412, 413, 411, 411, 411,  12,  12,  12, 414,
    415, 415, 415, 415, 416,  12,  12, 417, 418, 418, 418, 418, 418, 418, 419,  12,
    418, 418, 420,  12, 421, 421, 421, 421, 421, 422, 421, 421, 421, 423,  12,  12,
    424, 424, 424, 424, 424, 425,  12,  12, 426, 426, 426, 426, 426, 426, 426, 427,
    122, 123, 123, 123, 123, 130,  12,  12, 428, 428, 428, 428, 429, 428, 428, 428,
    428, 428, 428, 430, 431, 432, 433, 434, 431, 431, 431, 434, 431, 431, 435,  12,
    436, 436, 436, 436, 436, 436, 437,  12, 436, 436, 438,  12, 439, 440, 439, 441,
    441, 439, 439, 439, 439, 439, 442, 439, 442, 440, 443, 439, 439, 441, 441, 444,
    445, 446,  12, 440, 439, 447, 439, 445, 439, 445,  12,  12, 448, 448, 448, 448,
    448, 448, 449, 450, 451, 451, 451, 451, 451, 451,  12,  12, 451, 451, 452,  12,
    453, 453, 453, 453, 453, 454, 453, 453, 453, 453, 453, 454, 455, 455, 455, 455,
    455, 456,  12,  12, 455, 455, 457,  12, 184, 184, 184, 187, 458, 458, 458, 458,
    458, 458,  12,  12, 458, 458, 459,  12, 460, 460, 460, 460, 460, 460, 461, 462,
    460, 460, 460,  12, 463, 463, 463, 463, 463, 463, 463,  12, 464, 464, 464, 464,
    465,  12,  12, 466, 467, 467, 467, 467, 467, 467,  12,  12, 468, 468, 468, 468,
    468, 469, 468, 468, 470,  12,  12,  12, 471, 471, 471, 471, 471, 471, 472,  12,
    473, 473, 474, 473, 473, 473, 473, 473, 473, 475, 473, 473, 473, 476,  12,  12,
    473, 473, 473, 477, 478, 478, 478, 478, 479, 478, 478, 478, 478, 478, 480, 478,
    478, 481,  12,  12, 482, 483, 484, 482, 482, 482, 482, 482, 482, 483, 485, 484,
    482, 482,  12,  12, 482, 482, 486,  12, 487, 488, 489, 487, 487, 487, 487, 487,
    487, 487, 487, 490, 488, 487, 491,  12, 487, 487, 492,  12, 493, 493, 493, 493,
    493, 493, 494,  12, 495, 495, 495, 495, 495, 495, 496,  12, 495, 495, 495, 497,
    495, 498,  12,  12, 495,  12,  12,  12, 499, 499, 499, 499, 499, 499, 499, 500,
    501, 501, 501, 501, 501, 502,  12,  12, 279, 279, 503,  12, 504, 504, 504, 504,
    504, 504, 504, 505, 504, 504, 506, 507, 508, 508, 508, 508, 508, 508, 508, 509,
    508, 509,  12,  12, 510, 510, 510, 510, 510, 511,  12,  12, 510, 510, 512, 510,
    512, 510, 510, 510, 510, 510,  12, 513, 514, 514, 514, 514, 514, 514, 515,  12,
    516, 516, 516, 516, 516, 517,  12,  12, 516, 516, 516, 518,  12,  12,  12, 519,
    520,  12,  12,  12, 521, 521, 521, 521, 522,  12,  12,  12, 523,  12,  12,  12,
    524, 260, 260, 260, 260, 260, 260, 261, 525, 525, 525, 525, 525, 525, 525,  12,
    526, 526, 526, 526, 526, 526, 527,  12, 526, 526, 526, 528, 526, 526, 528,  12,
    526, 526, 529, 526,   0, 245,  12,  12,   0, 238, 317,   0,   0, 530, 234,   0,
      0,   0, 530,   7, 218, 531,   7,   0,   0,   0, 532, 234,   0,   0, 533,  12,
      8, 231,  12,  12,   0,   0,   0, 235, 534, 535, 317, 235,   0,   0, 536, 317,
      0, 317,   0,   0,   0, 536, 238, 317,   0, 235,   0, 235,   0,   0, 536, 238,
      0, 537, 244,   0, 235,   0,   0,   0,   0,   0,   0, 244, 538, 538, 538, 538,
    538, 538, 538,  12,  12,  12, 539, 538, 540, 538, 538, 538, 246, 247, 246, 246,
    246, 246, 541, 246, 542, 543, 247,  12, 544, 544, 544, 544, 544, 545, 544, 544,
    544, 546,  12,  12, 547, 547, 547, 547, 547, 547, 548,  12, 547, 547, 549, 550,
      0, 533,  12,  12,  30, 551,  30,  30, 552, 553, 551,  30, 407,  30, 554,  12,
    555,  54, 554, 551, 552, 553, 554, 554, 552, 553, 407,  30, 407,  30, 551, 556,
     30,  30, 557,  30,  30,  30,  30,  12, 551, 551, 557,  30,   0,   0,   0, 533,
     12, 244,   0,   0, 558,  12,  12,  12, 245,  12,  12,  12,   0,   0,  12,  12,
      0,   0,   0, 245, 559, 238, 534,   0, 238,  12,  12,  12, 252, 560,  12,  12,
    252, 561,  12,  12, 254,  12,  12,  12, 561,  12,  12,  12, 562,  12,  12,  12,
};

static RE_UINT8 re_script_stage_5[] = {
      1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1,
      1,   1,   2,   1,   2,   1,   1,   1,   1,   1,  35,  35,  41,  41,  41,  41,
      3,   3,   3,   3,   1,   3,   3,   3,   0,   0,   3,   3,   3,   3,   1,   3,
      0,   0,   0,   0,   3,   1,   3,   1,   3,   3,   3,   0,   3,   0,   3,   3,
      3,   3,   0,   3,   3,   3,  55,  55,  55,  55,  55,  55,   4,   4,   4,   4,
      4,  41,  41,   4,   0,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   0,
      5,   1,   5,   0,   0,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   0,
      0,   0,   0,   6,   6,   0,   0,   0,   7,   7,   7,   7,   7,   1,   7,   7,
      1,   7,   7,   7,   7,   7,   7,   1,   7,   0,   7,   1,   7,   7,   7,  41,
     41,  41,   7,   7,  41,   7,   7,   7,   8,   8,   8,   8,   8,   8,   0,   8,
      8,   8,   8,   0,   0,   8,   8,   8,   9,   9,   9,   9,   9,   9,   0,   0,
     66,  66,  66,  66,  66,  66,  66,   0,   0,  66,  66,  66,  82,  82,  82,  82,
     82,  82,   0,   0,  82,  82,  82,   0,  95,  95,  95,  95,   0,   0,  95,   0,
      7,   0,   7,   7,   7,   7,   0,   0,   0,   0,   0,   7,   7,   7,   1,   7,
     10,  10,  10,  10,  10,  41,  41,  10,   1,   1,  10,  10,  11,  11,  11,  11,
      0,  11,  11,  11,  11,   0,   0,  11,  11,   0,  11,  11,  11,   0,  11,   0,
      0,   0,  11,  11,  11,  11,   0,   0,  11,  11,  11,   0,   0,   0,   0,  11,
     11,  11,   0,  11,   0,  12,  12,  12,  12,  12,  12,   0,   0,   0,   0,  12,
     12,   0,   0,  12,  12,  12,  12,  12,  12,   0,  12,  12,   0,  12,  12,   0,
     12,  12,   0,   0,   0,  12,   0,   0,  12,   0,  12,   0,   0,   0,  12,  12,
      0,  13,  13,  13,  13,  13,  13,  13,  13,  13,   0,  13,  13,   0,  13,  13,
     13,  13,   0,   0,  13,   0,   0,   0,   0,   0,  13,  13,   0,  14,  14,  14,
     14,  14,  14,  14,  14,   0,   0,  14,  14,   0,  14,  14,  14,  14,   0,   0,
      0,   0,  14,  14,  14,  14,   0,  14,   0,   0,  15,  15,   0,  15,  15,  15,
     15,  15,  15,   0,  15,   0,  15,  15,  15,  15,   0,   0,   0,  15,  15,   0,
      0,   0,   0,  15,  15,   0,   0,   0,  15,  15,  15,  15,  16,  16,  16,  16,
     16,   0,  16,  16,  16,  16,   0,   0,   0,  16,  16,  16,   0,  16,  16,   0,
     16,  16,  16,   0,   0,   0,  16,  16,  17,  17,  17,  17,  17,   0,  17,  17,
      0,  17,  17,  17,  17,  17,   0,   0,   0,  17,  17,   0,   0,   0,  17,   0,
      0,   0,  17,  17,  18,  18,  18,  18,   0,  18,  18,  18,  18,   0,  18,  18,
      0,   0,  18,  18,   0,   0,  19,  19,   0,  19,  19,  19,  19,  19,  19,  19,
     19,  19,  19,   0,  19,  19,   0,  19,   0,  19,   0,   0,   0,   0,  19,   0,
      0,   0,   0,  19,  19,   0,  19,   0,  19,   0,   0,   0,   0,  20,  20,  20,
     20,  20,  20,  20,  20,  20,  20,   0,   0,   0,   0,   1,   0,  21,  21,   0,
     21,   0,   0,  21,  21,   0,  21,   0,   0,  21,   0,   0,  21,  21,  21,  21,
      0,  21,  21,  21,   0,  21,   0,  21,   0,   0,  21,  21,  21,  21,   0,  21,
     21,  21,   0,   0,  22,  22,  22,  22,   0,  22,  22,  22,  22,   0,   0,   0,
     22,   0,  22,  22,  22,   1,   1,   1,   1,  22,  22,   0,  23,  23,  23,  23,
     24,  24,  24,  24,  24,  24,   0,  24,   0,  24,   0,   0,  24,  24,  24,   1,
     25,  25,  25,  25,  26,  26,  26,  26,  26,   0,  26,  26,  26,  26,   0,   0,
     26,  26,  26,   0,   0,  26,  26,  26,  26,   0,   0,   0,  27,  27,  27,  27,
     27,  27,   0,   0,  28,  28,  28,  28,  29,  29,  29,  29,  29,   0,   0,   0,
     30,  30,  30,  30,  30,  30,  30,   1,   1,   1,  30,  30,  30,   0,   0,   0,
     42,  42,  42,  42,  42,   0,  42,  42,  42,   0,   0,   0,  43,  43,  43,  43,
     43,   1,   1,   0,  44,  44,  44,  44,  45,  45,  45,  45,  45,   0,  45,  45,
     31,  31,  31,  31,  31,  31,   0,   0,  32,  32,   1,   1,  32,   1,  32,  32,
     32,  32,  32,  32,  32,  32,  32,   0,  32,  32,   0,   0,  32,   0,   0,   0,
     28,  28,   0,   0,  46,  46,  46,  46,  46,  46,  46,   0,  46,   0,   0,   0,
     47,  47,  47,  47,  47,  47,   0,   0,  47,   0,   0,   0,  56,  56,  56,  56,
     56,  56,   0,   0,  56,  56,  56,   0,   0,   0,  56,  56,  54,  54,  54,  54,
      0,   0,  54,  54,  78,  78,  78,  78,  78,  78,  78,   0,  78,   0,   0,  78,
     78,  78,   0,   0,  41,  41,  41,   0,  62,  62,  62,  62,  62,   0,   0,   0,
     67,  67,  67,  67,  93,  93,  93,  93,  68,  68,  68,  68,   0,   0,   0,  68,
     68,  68,   0,   0,   0,  68,  68,  68,  69,  69,  69,  69,   4,   0,   0,   0,
     24,  24,  24,   0,   0,  24,  24,  24,  41,  41,  41,   1,  41,   1,  41,  41,
     41,   1,   1,   1,   1,  41,   1,   1,  41,  41,   0,   0,   2,   2,   3,   3,
      3,   3,   3,   4,   2,   3,   3,   3,   3,   3,   2,   2,   3,   3,   3,   2,
      4,   2,   2,   2,   2,   2,   2,   3,  41,  41,   0,  41,   3,   3,   0,   0,
      0,   3,   0,   3,   0,   3,   3,   3,  41,  41,   1,   1,   1,   0,   1,   1,
      1,   2,   0,   0,   1,   1,   1,   2,   1,   1,   1,   0,   2,   0,   0,   0,
     41,   0,   0,   0,   1,   1,   3,   1,   1,   1,   2,   2,  53,  53,  53,  53,
      0,   0,   1,   1,   1,   1,   0,   0,  57,  57,  57,  57,  57,  57,  57,   0,
      0,  55,  55,  55,  58,  58,  58,  58,   0,   0,   0,  58,  58,   0,   0,   0,
     36,  36,  36,  36,  36,  36,   0,  36,  36,  36,   0,   0,   1,  36,   1,  36,
      1,  36,  36,  36,  36,  36,  41,  41,  41,  41,  25,  25,   0,  33,  33,  33,
     33,  33,  33,  33,  33,  33,  33,   0,   0,  41,  41,   1,   1,  33,  33,  33,
      1,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,   1,   0,  35,  35,  35,
     35,  35,  35,  35,   0,  25,  25,  25,  25,  25,  25,   0,  35,  35,  35,   0,
     25,  25,  25,   1,  34,  34,  34,   0,  37,  37,  37,  37,  37,   0,   0,   0,
     37,  37,  37,   0,  83,  83,  83,  83,  70,  70,  70,  70,  84,  84,  84,  84,
      2,   2,   0,   0,   0,   0,   0,   2,  59,  59,  59,  59,  65,  65,  65,  65,
     71,  71,  71,  71,  71,  71,   0,   0,   0,   0,  71,  71,  72,  72,  72,  72,
     72,  72,   1,  72,  73,  73,  73,  73,   0,   0,   0,  73,  25,   0,   0,   0,
     85,  85,  85,  85,  85,  85,   0,   1,  85,  85,   0,   0,   0,   0,  85,  85,
     23,  23,  23,   0,  77,  77,  77,  77,  77,  77,  77,   0,  77,  77,   0,   0,
     79,  79,  79,  79,  79,  79,  79,   0,   0,   0,   0,  79,  86,  86,  86,  86,
     86,  86,  86,   0,   2,   3,   0,   0,  86,  86,   0,   0,   0,   0,   0,  25,
      2,   2,   2,   0,   0,   0,   0,   5,   6,   0,   6,   0,   6,   6,   0,   6,
      6,   0,   6,   6,   7,   7,   1,   1,   0,   0,   7,   7,  41,  41,   4,   4,
      7,   0,   0,   1,   0,   1,   1,   1,   1,   1,  34,  34,  34,  34,   1,   1,
      0,   0,  25,  25,  48,  48,  48,  48,   0,  48,  48,  48,  48,  48,  48,   0,
     48,  48,   0,  48,  48,  48,   0,   0,   3,   0,   0,   0,   1,  41,   0,   0,
     74,  74,  74,  74,  74,   0,   0,   0,  75,  75,  75,  75,  75,   0,   0,   0,
     38,  38,  38,  38,   0,  38,  38,  38,  39,  39,  39,  39,  39,  39,  39,   0,
    120, 120, 120, 120, 120, 120, 120,   0,  49,  49,  49,  49,  49,  49,   0,  49,
     60,  60,  60,  60,  60,  60,   0,   0,  40,  40,  40,  40,  50,  50,  50,  50,
     51,  51,  51,  51,  51,  51,   0,   0, 136, 136, 136, 136, 106, 106, 106, 106,
    103, 103, 103, 103,   0,   0,   0, 103, 110, 110, 110, 110, 110, 110, 110,   0,
    110, 110,   0,   0,  52,  52,  52,  52,  52,  52,   0,   0,  52,   0,  52,  52,
     52,  52,   0,  52,  52,   0,   0,   0,  52,   0,   0,  52,  87,  87,  87,  87,
     87,  87,   0,  87, 118, 118, 118, 118, 117, 117, 117, 117, 117, 117, 117,   0,
      0,   0,   0, 117, 128, 128, 128, 128, 128, 128, 128,   0, 128, 128,   0,   0,
      0,   0,   0, 128,  64,  64,  64,  64,   0,   0,   0,  64,  76,  76,  76,  76,
     76,  76,   0,   0,   0,   0,   0,  76,  98,  98,  98,  98,  97,  97,  97,  97,
      0,   0,  97,  97,  61,  61,  61,  61,   0,  61,  61,   0,   0,  61,  61,  61,
     61,  61,   0,   0,  61,  61,  61,   0,   0,   0,   0,  61,  61,   0,   0,   0,
     88,  88,  88,  88, 116, 116, 116, 116, 112, 112, 112, 112, 112, 112, 112,   0,
      0,   0,   0, 112,  80,  80,  80,  80,  80,  80,   0,   0,   0,  80,  80,  80,
     89,  89,  89,  89,  89,  89,   0,   0,  90,  90,  90,  90,  90,  90,  90,   0,
    121, 121, 121, 121, 121, 121,   0,   0,   0, 121, 121, 121, 121,   0,   0,   0,
     91,  91,  91,  91,  91,   0,   0,   0, 130, 130, 130, 130, 130, 130, 130,   0,
      0,   0, 130, 130, 146, 146, 146, 146, 146, 146,   0,   0,   7,   7,   7,   0,
    148, 148, 148, 148, 147, 147, 147, 147, 147, 147,   0,   0,  94,  94,  94,  94,
     94,  94,   0,   0,   0,   0,  94,  94,   0,   0,   0,  94,  92,  92,  92,  92,
     92,  92,   0,   0,   0,  92,   0,   0, 101, 101, 101, 101, 101,   0,   0,   0,
    101, 101,   0,   0,  96,  96,  96,  96,  96,   0,  96,  96,  96,  96,  96,   0,
    111, 111, 111, 111, 111, 111, 111,   0, 100, 100, 100, 100, 100, 100,   0,   0,
    109, 109, 109, 109, 109, 109,   0, 109, 109, 109, 109,   0, 129, 129, 129, 129,
    129, 129, 129,   0, 129,   0, 129, 129, 129, 129,   0, 129, 129, 129,   0,   0,
    123, 123, 123, 123, 123, 123, 123,   0, 123, 123,   0,   0, 107, 107, 107, 107,
      0, 107, 107, 107, 107,   0,   0, 107, 107,   0, 107, 107, 107, 107,   0,  41,
    107, 107,   0,   0, 107,   0,   0,   0,   0,   0,   0, 107,   0,   0, 107, 107,
    135, 135, 135, 135, 135, 135,   0, 135,   0, 135, 135,   0, 124, 124, 124, 124,
    124, 124,   0,   0, 122, 122, 122, 122, 122, 122,   0,   0, 114, 114, 114, 114,
    114,   0,   0,   0, 114, 114,   0,   0, 102, 102, 102, 102, 102, 102,   0,   0,
    126, 126, 126, 126, 126, 126, 126,   0,   0, 126, 126, 126, 142, 142, 142, 142,
    125, 125, 125, 125, 125, 125, 125,   0,   0,   0,   0, 125, 141, 141, 141, 141,
    140, 140, 140, 140,   0,   0, 140, 140, 140, 140, 140,   0, 119, 119, 119, 119,
    119,   0,   0,   0, 133, 133, 133, 133, 133,   0, 133, 133, 133, 133, 133,   0,
    133, 133,   0,   0, 133,   0,   0,   0, 134, 134, 134, 134,   0,   0, 134, 134,
      0, 134, 134, 134, 134, 134, 134,   0, 138, 138, 138, 138, 138, 138, 138,   0,
    138, 138,   0, 138,   0,   0, 138,   0, 138, 138,   0,   0, 143, 143, 143, 143,
    143, 143,   0, 143, 143,   0, 143, 143, 143, 143, 143,   0, 143,   0,   0,   0,
    143, 143,   0,   0, 144, 144, 144, 144, 144,   0,   0,   0,  63,  63,  63,  63,
     63,  63,   0,   0,  63,  63,  63,   0,  63,   0,   0,   0,  81,  81,  81,  81,
     81,  81,  81,   0, 127, 127, 127, 127, 127, 127, 127,   0,  84,   0,   0,   0,
    115, 115, 115, 115, 115, 115, 115,   0, 115, 115,   0,   0,   0,   0, 115, 115,
    104, 104, 104, 104, 104, 104,   0,   0, 108, 108, 108, 108, 108, 108,   0,   0,
    108, 108,   0, 108,   0, 108, 108, 108, 145, 145, 145, 145, 145, 145, 145,   0,
     99,  99,  99,  99,  99,   0,   0,   0,  99,  99,  99,   0,   0,   0,   0,  99,
    137, 139,   0,   0, 137, 137, 137, 137, 137, 137,   0,   0, 137, 137, 137,   0,
     34,  33,  33,  33, 139, 139, 139, 139, 105, 105, 105, 105, 105, 105, 105,   0,
    105,   0,   0,   0, 105, 105,   0,   0,   1,   1,   1,  41,   1,  41,  41,  41,
      1,   1,  41,  41,   1,   0,   0,   0,   0,   0,   1,   0,   0,   1,   1,   0,
      1,   1,   0,   1,   1,   0,   1,   0, 131, 131, 131, 131,   0,   0,   0, 131,
      0, 131, 131, 131,  57,   0,   0,  57,  57,  57,   0,  57,  57,   0,  57,  57,
    113, 113, 113, 113, 113,   0,   0, 113, 113, 113, 113,   0, 132, 132, 132, 132,
    132, 132, 132,   0, 132, 132,   0,   0,   0,   0, 132, 132,   0,   7,   7,   7,
      0,   7,   7,   0,   7,   0,   0,   7,   0,   7,   0,   7,   0,   0,   7,   0,
      7,   0,   7,   0,   7,   7,   0,   7,  33,   1,   1,   0,   1,   0,   0,   1,
     36,  36,  36,   0,  36,   0,   0,   0,   0,   1,   0,   0,
};

/* Script: 12012 bytes. */

RE_UINT32 re_get_script(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 11;
    code = ch ^ (f << 11);
    pos = (RE_UINT32)re_script_stage_1[f] << 4;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_script_stage_2[pos + f] << 3;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_script_stage_3[pos + f] << 2;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_script_stage_4[pos + f] << 2;
    value = re_script_stage_5[pos + code];

    return value;
}

/* Script_Extensions. */

static RE_UINT8 re_script_extensions_stage_1[] = {
    0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 3,
    3,
};

static RE_UINT8 re_script_extensions_stage_2[] = {
     0,  1,  2,  3,  4,  5,  5,  5,  5,  6,  7,  8,  8,  9, 10, 11,
    12, 13, 14, 15, 16, 10, 17, 18, 19, 10, 10, 20, 10, 21, 22, 23,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 24, 25, 26,  5, 27, 28,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    29, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
};

static RE_UINT8 re_script_extensions_stage_3[] = {
      0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,
     16,  17,  18,  19,  20,  20,  21,  22,  23,  24,  25,  26,  27,  28,   1,  29,
     30,  31,  32,  32,  33,  32,  32,  32,  34,  32,  32,  35,  36,  37,  38,  39,
     40,  41,  42,  43,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,
     44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  45,  44,  44,
     44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,
     44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  46,
     47,  47,  47,  47,  48,  49,  50,  51,  52,  53,  54,  55,  17,  17,  17,  17,
     17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,
     17,  17,  17,  17,  17,  17,  17,  56,  57,  57,  57,  57,  57,  57,  57,  57,
     57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,
     57,  57,  57,  57,  57,  57,  57,  57,  57,  44,  58,  59,  60,  61,  62,  63,
     64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,
     80,  81,  82,  83,  84,  85,  86,  87,  88,  57,  89,  57,  90,  91,  92,  57,
     93,  93,  93,  94,  95,  96,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,
     97,  97,  97,  97,  98,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,
     57,  57,  57,  57,  99,  99, 100,  57,  57,  57,  57,  57,  57,  57,  57,  57,
     57,  57,  57,  57,  57,  57,  57,  57, 101, 101, 102, 103,  57,  57, 104, 105,
    106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106,
    106, 106, 106, 106, 106, 106, 106, 107, 106, 106, 108,  57,  57,  57,  57,  57,
    109, 110, 111,  57,  57,  57,  57,  57,  57,  57,  57,  57, 112,  57,  57,  57,
    113, 114, 115, 116, 117, 118, 119, 120, 121, 121, 122,  57,  57,  57,  57,  57,
    123,  57,  57,  57,  57,  57,  57,  57, 124, 125,  57,  57, 126,  57, 127,  57,
    128, 129, 130,  32,  32,  32, 131, 132, 133, 134, 135,  57,  57,  57,  57,  57,
     44,  44,  44,  44,  44,  44, 136,  44,  44,  44,  44,  44,  44,  44,  44,  44,
     44,  44,  44,  44,  44,  44,  44, 137, 138,  44,  44,  44,  44,  44,  44,  44,
     44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44, 139,  44,
     44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44, 140,  57,  57,  57,  57,
     57,  57,  57,  57,  57,  57,  57,  57,  44,  44, 141,  57,  57,  57,  57,  57,
    142, 143,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,
};

static RE_UINT16 re_script_extensions_stage_4[] = {
      0,   0,   0,   0,   1,   2,   1,   2,   0,   0,   3,   3,   4,   5,   4,   5,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   6,   0,   0,   7,   0,
      8,   8,   8,   8,   9,   8,  10,  11,  12,  13,  14,  13,  13,  13,  15,  13,
     16,  16,  16,  16,  16,  16,  16,  16,  17,  16,  16,  16,  16,  16,  16,  16,
     16,  16,  16,  18,  19,  20,  19,  19,  21,  22,  23,  23,  24,  23,  25,  26,
     27,  28,  29,  29,  30,  31,  32,  33,  29,  29,  29,  29,  29,  34,  29,  29,
     35,  36,  36,  36,  37,  29,  29,  29,  38,  38,  38,  39,  40,  40,  40,  41,
     42,  42,  43,  44,  45,  46,  47,  48,  48,  48,  29,  49,  48,  50,  51,  29,
     52,  52,  52,  52,  52,  53,  54,  52,  55,  56,  57,  58,  59,  60,  61,  62,
     63,  64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,
     79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,
     95,  96,  97,  98,  99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
    111, 112, 113, 113, 114, 115, 116, 113, 117, 118, 119, 120, 121, 122, 123, 124,
    125, 126, 126, 127, 126, 128,  48,  48, 129, 130, 131, 132, 133, 134,  48,  48,
    135, 135, 135, 135, 136, 135, 137, 138, 135, 136, 135, 139, 139, 140,  48,  48,
    141, 141, 141, 141, 142, 141, 141, 141, 141, 141, 143, 143, 144, 143, 143, 145,
    146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146,
    147, 147, 147, 147, 148, 149, 147, 147, 148, 147, 147, 150, 151, 152, 147, 147,
    147, 151, 147, 147, 147, 153, 147, 154, 147, 155, 156, 156, 156, 156, 156, 157,
    158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158,
    158, 158, 158, 158, 158, 158, 158, 158, 159, 160, 161, 161, 161, 161, 162, 163,
    164, 165, 166, 167, 168, 169, 170, 171, 172, 172, 172, 172, 172, 173, 174, 174,
    175, 176, 177, 177, 177, 177, 177, 178, 177, 177, 179, 158, 158, 158, 158, 180,
    181, 182, 183, 183, 184, 185, 186, 187, 188, 188, 189, 188, 190, 191, 172, 172,
    192, 193, 194, 194, 194, 195, 194, 196, 197, 197, 198, 199,  48,  48,  48,  48,
    200, 200, 200, 200, 201, 200, 200, 202, 203, 203, 203, 203, 204, 204, 204, 205,
    206, 206, 206, 207, 208, 209, 209, 209, 210, 143, 143, 211, 212, 213, 214, 215,
      4,   4, 216,   4,   4, 217, 218, 219,   4,   4,   4, 220, 221,   8,   8, 222,
     13, 223,  13,  13, 223, 224,  13, 225,  13,  13,  13, 226, 226, 227,  13, 228,
    229,   0,   0,   0,   0,   0, 230, 231, 232, 233,   0,   0,  48,   8,   8, 234,
      0,   0, 235, 236, 237,   0,   4,   4, 238,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0, 239,  48, 240,  48,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    241, 241, 241, 241, 241, 241, 241, 241, 241, 241, 241, 241, 241, 241, 241, 241,
      0,   0,   0,   0,   0,   0,   0, 242,   0, 243,   0,   0, 244,   0,   0, 232,
    245, 245, 246, 245, 245, 246,   4,   4, 247, 247, 247, 247, 247, 247, 247, 248,
    143, 143, 144, 249, 249, 249, 250, 251, 147, 252, 253, 253, 253, 253,  16,  16,
      0,   0,   0,   0, 254,  48,  48,  48, 255, 256, 255, 255, 255, 255, 255, 257,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 258,  48, 259,
    260, 261, 262, 263, 264, 265, 265, 265, 265, 266, 267, 268, 268, 268, 268, 269,
    270, 271, 271, 272, 146, 146, 146, 146, 273, 255, 271, 274, 255, 255, 257, 268,
    146, 273, 255, 255, 275,   0, 146, 276, 255, 255, 255, 277, 278, 268, 268, 279,
    268, 268, 268, 268, 268, 280, 255, 281,   0,   0,   0,   0,   0,   0, 255, 282,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 258,   0,   0,   0,   0,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,  48,
    283, 283, 283, 283, 283, 283, 283, 283, 283, 283, 283, 283, 283, 283, 283, 283,
    283, 283, 283, 283, 283, 283, 283, 283, 284, 283, 283, 283, 285, 286, 286, 286,
    287, 287, 287, 287, 287, 287, 287, 287, 287, 287, 287, 287, 287, 287, 287, 287,
    287, 287, 288,  48,  16,  16, 289,  16,  16,  16, 290, 290, 290, 290, 290, 291,
      0,   0, 292,   4,   4,   4,   4,   4, 293,   4,   4, 294,  48,  48,  48, 295,
    296, 296, 297, 298, 299, 299, 299, 300, 301, 301, 301, 301, 302, 303,  52, 304,
    305, 305, 306, 307, 307, 308, 146, 309, 310, 310, 310, 310, 311, 312, 141, 313,
    314, 314, 314, 315, 316, 317, 141, 141, 318, 318, 318, 318, 319, 320, 321, 322,
    323, 324, 253,   4,   4, 325, 326, 156, 156, 156, 156, 156, 321, 321, 327, 328,
    146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 329, 146, 330, 146, 146, 331,
     48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,
    255, 255, 255, 255, 255, 255, 332, 255, 255, 255, 255, 255, 255, 333,  48,  48,
    334, 335,  23, 336, 337,  29,  29,  29,  29,  29,  29,  29, 338,  50,  29,  29,
     29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,
     29,  29,  29, 339,  48,  29,  29,  29,  29, 340,  29,  29, 341,  48,  48, 342,
      8, 343, 344,   0, 345, 346, 347, 348,  29,  29,  29,  29,  29,  29,  29, 349,
    350,   0,   1,   2,   1,   2, 351, 267, 268, 352, 146, 273, 353, 354, 355, 356,
    357, 358, 359, 360, 361, 361,  48,  48, 358, 358, 358, 358, 358, 358, 358, 362,
    363, 364, 364, 365,  13,  13,  13,  13, 366, 259, 367,  48,  48,   0,   0, 368,
     48,  48,  48,  48,  48,  48,  48,  48, 369, 370, 371, 371, 371, 372, 373, 374,
    375, 375, 376, 377, 378, 379, 379, 380, 381, 382, 383, 383, 384, 385,  48,  48,
    386, 386, 386, 386, 386, 387, 387, 387, 388, 389, 390, 391, 391, 392, 391, 393,
    394, 394, 395, 396, 396, 396, 397,  48,  48,  48,  48,  48,  48,  48,  48,  48,
    398, 398, 398, 398, 398, 398, 398, 398, 398, 398, 398, 398, 398, 398, 398, 398,
    398, 398, 398, 399, 398, 400, 401,  48,  48,  48,  48,  48,  48,  48,  48,  48,
    402, 403, 403, 404, 405, 406, 407, 407, 408, 409, 410,  48,  48,  48, 411, 412,
    413, 414, 415, 416,  48,  48,  48,  48, 417, 417, 418, 419, 418, 420, 418, 418,
    421, 422, 423, 424, 425, 425, 426, 426, 427, 427,  48,  48, 428, 428, 429, 430,
    431, 431, 431, 432, 433, 434, 435, 436, 437, 438, 439,  48,  48,  48,  48,  48,
    440, 440, 440, 440, 441,  48,  48,  48, 442, 442, 442, 443, 442, 442, 442, 444,
    445, 445, 446, 447,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,
     48,  48,  48,  48,  48,  48,  29, 448,  48,  48,  48,  48,  48,  48,  48,  48,
    449, 449, 450, 451, 451, 452,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,
    453, 453, 453, 453, 454, 455, 453, 456, 457, 457, 457, 457, 458, 459, 460, 461,
    462, 462, 462, 463, 464, 465, 465, 466, 467, 467, 467, 467, 468, 467, 469, 470,
    471, 472, 471, 473,  48,  48,  48,  48, 474, 475, 476, 477, 477, 477, 478, 479,
    480, 481, 482, 483, 484, 485, 486, 487,  48,  48,  48,  48,  48,  48,  48,  48,
    488, 488, 488, 488, 488, 489,  48,  48, 490, 490, 490, 490, 491, 492,  48,  48,
     48,  48,  48,  48,  48,  48,  48,  48, 493, 493, 493, 494, 493, 495,  48,  48,
    496, 496, 496, 496, 497, 498, 499,  48, 500, 500, 500, 501, 502,  48,  48,  48,
    503, 504, 505, 503,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,
    506, 506, 506, 507,  48,  48,  48,  48,  48,  48, 508, 508, 508, 508, 508, 509,
    510, 510, 510, 510, 511, 512, 512, 512, 513, 512, 514,  48, 515, 515, 515, 516,
    517, 518, 518, 519, 520, 518, 521, 522, 522, 523, 524, 525,  48,  48,  48,  48,
    526, 527, 527, 528, 529, 530, 531, 532, 533, 534, 535,  48,  48,  48,  48,  48,
     48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48, 536, 537,
    538, 538, 538, 538, 538, 538, 538, 538, 538, 538, 538, 538, 538, 538, 538, 538,
    538, 538, 538, 538, 538, 538, 538, 538, 538, 539,  48,  48,  48,  48,  48,  48,
    538, 538, 538, 538, 538, 538, 540, 541, 538, 538, 538, 538, 538, 538, 538, 538,
    538, 538, 538, 538, 542,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,
    543, 543, 543, 543, 543, 543, 543, 543, 543, 543, 543, 543, 543, 543, 543, 543,
    543, 543, 544,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,
    545, 545, 545, 545, 545, 545, 545, 545, 545, 545, 545, 545, 545, 545, 545, 545,
    545, 545, 545, 545, 546,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,
    290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 290,
    290, 290, 290, 547, 548, 549, 550,  48,  48,  48,  48,  48,  48, 551, 552, 553,
    554, 554, 554, 554, 555, 556, 557, 558, 554,  48,  48,  48,  48,  48,  48,  48,
     48,  48,  48,  48, 559, 559, 559, 559, 559, 560,  48,  48,  48,  48,  48,  48,
    561, 561, 561, 561, 562, 561, 561, 563, 564, 561,  48,  48,  48,  48, 565,  48,
    566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566,
    566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 567,
    566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 566, 568,
    569, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265,
    265, 570,  48,  48,  48,  48,  48, 571, 571, 571, 571, 571, 571, 571, 571, 571,
    571, 571, 571, 571, 571, 571, 571, 571, 571, 571, 571, 571, 571, 571, 571, 572,
    573, 573, 573, 573, 573, 573, 574, 575, 576, 577, 578,  48,  48,  48,  48,  48,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 579,
      0,   0, 580,   0,   0,   0, 581, 582, 583,   0, 584,   0,   0,   0, 585,  48,
     13,  13,  13,  13, 586,  48,  48,  48,  48,  48,  48,  48,  48,  48,   0, 587,
      0,   0,   0,   0,   0, 239, 255, 588,  48,  48,  48,  48,  48,  48,  48,  48,
      0,   0,   0,   0,   0, 230,   0,   0,   0, 589, 590, 591, 592,   0,   0,   0,
    593, 594,   0, 595, 596, 597,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 243,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 598,   0,   0,   0,
    599, 599, 599, 599, 599, 599, 599, 599, 599, 599, 599, 599, 599, 599, 599, 599,
    599, 599, 599, 599, 599, 599, 599, 599, 600, 601, 602,  48,  48,  48,  48,  48,
    603, 604, 605,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,
    606, 606, 606, 606, 606, 606, 606, 606, 606, 606, 606, 606, 607, 608,  48,  48,
    609, 609, 609, 609, 610, 611,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,
     48,  48,  48,  48,  48,  48,  48, 350,   0,   0,   0, 612,  48,  48,  48,  48,
    613,  29, 614, 615, 616, 617, 618, 619, 620, 621, 622, 621,  48,  48,  48, 338,
      0,   0, 259,   0,   0,   0,   0,   0,   0, 587, 232, 350, 350, 350,   0, 579,
    623,   0,   0,   0,   0,   0, 259,   0,   0,   0, 623,  48,  48,  48, 624,   0,
    625,   0,   0, 259, 585, 626, 579,  48,  48,  48,  48,  48,  48,  48,  48,  48,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 612, 623, 343,
      0,   0,   0,   0,   0,   0,   0, 587,   0,   0,   0,   0,   0, 585,  48,  48,
    259,   0,   0,   0, 627, 343,   0,   0, 627,   0, 628,  48,  48,  48,  48,  48,
    259,   0,   0, 232,   0,   0,   0, 629,   0,   0, 630, 343, 630,   0,   0,   0,
     48,  48,  48,  48,  48,  48, 628,  48,  48,  48,  48,  48,  48,  48,  48,  48,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 631,  48,  48,
    255, 255, 255, 632, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 332, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 626, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 633,  48,
    255, 332,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,
    634,  48,   0,   0,   0,   0,   0,   0,  48,  48,  48,  48,  48,  48,  48,  48,
      8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,  48,
};

static RE_UINT8 re_script_extensions_stage_5[] = {
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   1,   1,   1,   1,   1,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   1,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,
      2,   2,   2,   2,   2,   1,   1,   1,   1,   1,  35,  35,   1,   1,   1,   1,
     41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,
     41,  41,   3,  41,  41,   3,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,
     41,  41,  41,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      3,   3,   3,   3,   1,   3,   3,   3,   0,   0,   3,   3,   3,   3,   1,   3,
      0,   0,   0,   0,   3,   1,   3,   1,   3,   3,   3,   0,   3,   0,   3,   3,
      3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,
      3,   3,   0,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,
      3,   3,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4, 160, 158, 159, 159, 158,   4,   4,   4,   4,   4,   4,   4,   4,
      0,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,
      5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,
      5,   5,   5,   5,   5,   5,   5,   0,   0,   5,   5,   5,   5,   5,   5,   5,
      5,   5,   5,   5,   5,   5,   5,   5,   5, 153,   5,   0,   0,   5,   5,   5,
      0,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,
      6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,
      6,   6,   6,   6,   6,   6,   6,   6,   0,   0,   0,   0,   0,   0,   0,   0,
      6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   0,   0,   0,   0,   6,
      6,   6,   6,   6,   6,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      7,   7,   7,   7,   7,   1,   7,   7,   7,   7,   7,   7, 178,   7,   7,   7,
      7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7, 178, 170,   0,   7, 178,
      7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
    185,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7, 151, 151, 151, 151, 151,
    151, 151, 151, 151, 151, 151,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
    152, 152, 152, 152, 152, 152, 152, 152, 152, 152,   7,   7,   7,   7,   7,   7,
    151,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
      7,   7,   7,   7, 150,   7,   7,   7,   7,   7,   7,   7,   7,   1,   7,   7,
      8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   0,   8,
      8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,
      8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   0,   0,   8,   8,   8,
      9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,
      9,   9,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     66,  66,  66,  66,  66,  66,  66,  66,  66,  66,  66,  66,  66,  66,  66,  66,
     66,  66,  66,  66,  66,  66,  66,  66,  66,  66,  66,   0,   0,  66,  66,  66,
     82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,
     82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,   0,   0,
     82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,   0,
     95,  95,  95,  95,  95,  95,  95,  95,  95,  95,  95,  95,  95,  95,  95,  95,
     95,  95,  95,  95,  95,  95,  95,  95,  95,  95,  95,  95,   0,   0,  95,   0,
      8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      7,   7,   7,   7,   7,   0,   7,   7,   7,   7,   7,   7,   7,   7,   0,   0,
      0,   0,   0,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
      7,   7,   1,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
     10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,
     10, 189, 187,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,
     10,  10,  10,  10, 191, 192, 181, 181, 181, 181, 181, 181, 181, 181, 181, 181,
     11,  11,  11,  11,   0,  11,  11,  11,  11,  11,  11,  11,  11,   0,   0,  11,
     11,   0,   0,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,
     11,  11,  11,  11,  11,  11,  11,  11,  11,   0,  11,  11,  11,  11,  11,  11,
     11,   0,  11,   0,   0,   0,  11,  11,  11,  11,   0,   0,  11,  11,  11,  11,
     11,  11,  11,  11,  11,   0,   0,  11,  11,   0,   0,  11,  11,  11,  11,   0,
      0,   0,   0,   0,   0,   0,   0,  11,   0,   0,   0,   0,  11,  11,   0,  11,
     11,  11,  11,  11,   0,   0, 171, 171, 171, 171, 171, 171, 171, 171, 171, 171,
     11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,  11,   0,
      0,  12,  12,  12,   0,  12,  12,  12,  12,  12,  12,   0,   0,   0,   0,  12,
     12,   0,   0,  12,  12,  12,  12,  12,  12,  12,  12,  12,  12,  12,  12,  12,
     12,  12,  12,  12,  12,  12,  12,  12,  12,   0,  12,  12,  12,  12,  12,  12,
     12,   0,  12,  12,   0,  12,  12,   0,  12,  12,   0,   0,  12,   0,  12,  12,
     12,  12,  12,   0,   0,   0,   0,  12,  12,   0,   0,  12,  12,  12,   0,   0,
      0,  12,   0,   0,   0,   0,   0,   0,   0,  12,  12,  12,  12,   0,  12,   0,
      0,   0,   0,   0,   0,   0, 167, 167, 167, 167, 167, 167, 167, 167, 167, 167,
     12,  12,  12,  12,  12,  12,  12,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,  13,  13,  13,   0,  13,  13,  13,  13,  13,  13,  13,  13,  13,   0,  13,
     13,  13,   0,  13,  13,  13,  13,  13,  13,  13,  13,  13,  13,  13,  13,  13,
     13,  13,  13,  13,  13,  13,  13,  13,  13,   0,  13,  13,  13,  13,  13,  13,
     13,   0,  13,  13,   0,  13,  13,  13,  13,  13,   0,   0,  13,  13,  13,  13,
     13,  13,  13,  13,  13,  13,   0,  13,  13,  13,   0,  13,  13,  13,   0,   0,
     13,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     13,  13,  13,  13,   0,   0, 166, 166, 166, 166, 166, 166, 166, 166, 166, 166,
     13,  13,   0,   0,   0,   0,   0,   0,   0,  13,  13,  13,  13,  13,  13,  13,
      0,  14,  14,  14,   0,  14,  14,  14,  14,  14,  14,  14,  14,   0,   0,  14,
     14,   0,   0,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,
     14,  14,  14,  14,  14,  14,  14,  14,  14,   0,  14,  14,  14,  14,  14,  14,
     14,   0,  14,  14,   0,  14,  14,  14,  14,  14,   0,   0,  14,  14,  14,  14,
     14,  14,  14,  14,  14,   0,   0,  14,  14,   0,   0,  14,  14,  14,   0,   0,
      0,   0,   0,   0,   0,   0,  14,  14,   0,   0,   0,   0,  14,  14,   0,  14,
     14,  14,  14,  14,   0,   0,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,
     14,  14,  14,  14,  14,  14,  14,  14,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,  15,  15,   0,  15,  15,  15,  15,  15,  15,   0,   0,   0,  15,  15,
     15,   0,  15,  15,  15,  15,   0,   0,   0,  15,  15,   0,  15,   0,  15,  15,
      0,   0,   0,  15,  15,   0,   0,   0,  15,  15,  15,   0,   0,   0,  15,  15,
     15,  15,  15,  15,  15,  15,  15,  15,  15,  15,   0,   0,   0,   0,  15,  15,
     15,  15,  15,   0,   0,   0,  15,  15,  15,   0,  15,  15,  15,  15,   0,   0,
     15,   0,   0,   0,   0,   0,   0,  15,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165,
    165, 165, 165, 165,  15,  15,  15,  15,  15,  15,  15,   0,   0,   0,   0,   0,
     16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,   0,  16,  16,
     16,   0,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,
     16,  16,  16,  16,  16,  16,  16,  16,  16,   0,  16,  16,  16,  16,  16,  16,
     16,  16,  16,  16,  16,  16,  16,  16,  16,  16,   0,   0,   0,  16,  16,  16,
     16,  16,  16,  16,  16,   0,  16,  16,  16,   0,  16,  16,  16,  16,   0,   0,
      0,   0,   0,   0,   0,  16,  16,   0,  16,  16,  16,   0,   0,   0,   0,   0,
     16,  16,  16,  16,   0,   0,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,
      0,   0,   0,   0,   0,   0,   0,   0,  16,  16,  16,  16,  16,  16,  16,  16,
     17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,   0,  17,  17,
     17,   0,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,
     17,  17,  17,  17,  17,  17,  17,  17,  17,   0,  17,  17,  17,  17,  17,  17,
     17,  17,  17,  17,   0,  17,  17,  17,  17,  17,   0,   0,  17,  17,  17,  17,
     17,  17,  17,  17,  17,   0,  17,  17,  17,   0,  17,  17,  17,  17,   0,   0,
      0,   0,   0,   0,   0,  17,  17,   0,   0,   0,   0,   0,   0,   0,  17,   0,
     17,  17,  17,  17,   0,   0,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,
      0,  17,  17,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     18,  18,  18,  18,   0,  18,  18,  18,  18,  18,  18,  18,  18,   0,  18,  18,
     18,   0,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,
     18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,
     18,  18,  18,  18,  18,   0,  18,  18,  18,   0,  18,  18,  18,  18,  18,  18,
      0,   0,   0,   0,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,
     18,  18,  18,  18,   0,   0,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,
      0,   0,  19,  19,   0,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,
     19,  19,  19,  19,  19,  19,  19,   0,   0,   0,  19,  19,  19,  19,  19,  19,
     19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,
     19,  19,   0,  19,  19,  19,  19,  19,  19,  19,  19,  19,   0,  19,   0,   0,
     19,  19,  19,  19,  19,  19,  19,   0,   0,   0,  19,   0,   0,   0,   0,  19,
     19,  19,  19,  19,  19,   0,  19,   0,  19,  19,  19,  19,  19,  19,  19,  19,
      0,   0,   0,   0,   0,   0,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,
      0,   0,  19,  19,  19,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,
     20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,
     20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,   0,   0,   0,   0,   1,
     20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,   0,   0,   0,   0,
      0,  21,  21,   0,  21,   0,   0,  21,  21,   0,  21,   0,   0,  21,   0,   0,
      0,   0,   0,   0,  21,  21,  21,  21,   0,  21,  21,  21,  21,  21,  21,  21,
      0,  21,  21,  21,   0,  21,   0,  21,   0,   0,  21,  21,   0,  21,  21,  21,
     21,  21,  21,  21,  21,  21,  21,  21,  21,  21,   0,  21,  21,  21,   0,   0,
     21,  21,  21,  21,  21,   0,  21,   0,  21,  21,  21,  21,  21,  21,   0,   0,
     21,  21,  21,  21,  21,  21,  21,  21,  21,  21,   0,   0,  21,  21,  21,  21,
     22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,
     22,  22,  22,  22,  22,  22,  22,  22,   0,  22,  22,  22,  22,  22,  22,  22,
     22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,   0,   0,   0,
      0,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,
     22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,   0,  22,  22,
     22,  22,  22,  22,  22,   1,   1,   1,   1,  22,  22,   0,   0,   0,   0,   0,
     23,  23,  23,  23,  23,  23,  23,  23,  23,  23,  23,  23,  23,  23,  23,  23,
    172, 172, 172, 172, 172, 172, 172, 172, 172, 172,  23,  23,  23,  23,  23,  23,
     24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24,
     24,  24,  24,  24,  24,  24,   0,  24,   0,   0,   0,   0,   0,  24,   0,   0,
     24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24, 164,  24,  24,  24,  24,
     25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,
     26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,
     26,  26,  26,  26,  26,  26,  26,  26,  26,   0,  26,  26,  26,  26,   0,   0,
     26,  26,  26,  26,  26,  26,  26,   0,  26,   0,  26,  26,  26,  26,   0,   0,
     26,   0,  26,  26,  26,  26,   0,   0,  26,  26,  26,  26,  26,  26,  26,   0,
     26,   0,  26,  26,  26,  26,   0,   0,  26,  26,  26,  26,  26,  26,  26,  26,
     26,  26,  26,  26,  26,  26,  26,   0,  26,  26,  26,  26,  26,  26,  26,  26,
     26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,   0,   0,  26,  26,  26,
     26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,  26,   0,   0,   0,
     26,  26,  26,  26,  26,  26,  26,  26,  26,  26,   0,   0,   0,   0,   0,   0,
     27,  27,  27,  27,  27,  27,  27,  27,  27,  27,  27,  27,  27,  27,  27,  27,
     27,  27,  27,  27,  27,  27,   0,   0,  27,  27,  27,  27,  27,  27,   0,   0,
     28,  28,  28,  28,  28,  28,  28,  28,  28,  28,  28,  28,  28,  28,  28,  28,
     29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,
     29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,  29,   0,   0,   0,
     30,  30,  30,  30,  30,  30,  30,  30,  30,  30,  30,  30,  30,  30,  30,  30,
     30,  30,  30,  30,  30,  30,  30,  30,  30,  30,  30,   1,   1,   1,  30,  30,
     30,  30,  30,  30,  30,  30,  30,  30,  30,   0,   0,   0,   0,   0,   0,   0,
     42,  42,  42,  42,  42,  42,  42,  42,  42,  42,  42,  42,  42,   0,  42,  42,
     42,  42,  42,  42,  42,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     43,  43,  43,  43,  43,  43,  43,  43,  43,  43,  43,  43,  43,  43,  43,  43,
     43,  43,  43,  43,  43, 180, 180,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,
     44,  44,  44,  44,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     45,  45,  45,  45,  45,  45,  45,  45,  45,  45,  45,  45,  45,   0,  45,  45,
     45,   0,  45,  45,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,   0,   0,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,   0,   0,   0,   0,   0,   0,
     32,  32, 169, 169,  32, 169,  32,  32,  32,  32,  32,  32,  32,  32,  32,   0,
     32,  32,  32,  32,  32,  32,  32,  32,  32,  32,   0,   0,   0,   0,   0,   0,
     32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,
     32,  32,  32,  32,  32,  32,  32,  32,  32,   0,   0,   0,   0,   0,   0,   0,
     32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,   0,   0,   0,   0,   0,
     28,  28,  28,  28,  28,  28,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,
     46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,   0,
     46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,   0,   0,   0,   0,
     46,   0,   0,   0,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,
     47,  47,  47,  47,  47,  47,  47,  47,  47,  47,  47,  47,  47,  47,  47,  47,
     47,  47,  47,  47,  47,  47,  47,  47,  47,  47,  47,  47,  47,  47,   0,   0,
     47,  47,  47,  47,  47,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     56,  56,  56,  56,  56,  56,  56,  56,  56,  56,  56,  56,  56,  56,  56,  56,
     56,  56,  56,  56,  56,  56,  56,  56,  56,  56,  56,  56,   0,   0,   0,   0,
     56,  56,  56,  56,  56,  56,  56,  56,  56,  56,   0,   0,   0,   0,   0,   0,
     56,  56,  56,  56,  56,  56,  56,  56,  56,  56,  56,   0,   0,   0,  56,  56,
     54,  54,  54,  54,  54,  54,  54,  54,  54,  54,  54,  54,  54,  54,  54,  54,
     54,  54,  54,  54,  54,  54,  54,  54,  54,  54,  54,  54,   0,   0,  54,  54,
     78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,
     78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,   0,
     78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,   0,   0,  78,
     78,  78,  78,  78,  78,  78,  78,  78,  78,  78,   0,   0,   0,   0,   0,   0,
     78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,  78,   0,   0,
     41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,   0,
     62,  62,  62,  62,  62,  62,  62,  62,  62,  62,  62,  62,  62,  62,  62,  62,
     62,  62,  62,  62,  62,  62,  62,  62,  62,  62,  62,  62,   0,   0,   0,   0,
     62,  62,  62,  62,  62,  62,  62,  62,  62,  62,  62,  62,  62,   0,   0,   0,
     67,  67,  67,  67,  67,  67,  67,  67,  67,  67,  67,  67,  67,  67,  67,  67,
     93,  93,  93,  93,  93,  93,  93,  93,  93,  93,  93,  93,  93,  93,  93,  93,
     93,  93,  93,  93,   0,   0,   0,   0,   0,   0,   0,   0,  93,  93,  93,  93,
     68,  68,  68,  68,  68,  68,  68,  68,  68,  68,  68,  68,  68,  68,  68,  68,
     68,  68,  68,  68,  68,  68,  68,  68,   0,   0,   0,  68,  68,  68,  68,  68,
     68,  68,  68,  68,  68,  68,  68,  68,  68,  68,   0,   0,   0,  68,  68,  68,
     69,  69,  69,  69,  69,  69,  69,  69,  69,  69,  69,  69,  69,  69,  69,  69,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   0,   0,   0,   0,   0,   0,   0,
     24,  24,  24,  24,  24,  24,  24,  24,  24,  24,  24,   0,   0,  24,  24,  24,
     67,  67,  67,  67,  67,  67,  67,  67,   0,   0,   0,   0,   0,   0,   0,   0,
    179,  10, 179, 161,  10, 154, 154, 162, 154, 162, 184,  10, 162, 162,  10,  10,
    162, 154,  10,  10,  10,  10,  10,  10,  10,  10, 154,  10,  10, 154,  10,  10,
     10,  10, 161, 161, 174, 154, 154,  11, 161, 161,   0,   0,   0,   0,   0,   0,
      2,   2,   2,   2,   2,   2,   3,   3,   3,   3,   3,   4,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   3,   3,   3,
      3,   3,   2,   2,   2,   2,   3,   3,   3,   3,   3,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   4,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   3,
      3,   3,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,
     41,  41,  41,  41,  41,  41,  41,  41,  41,  41,   0,  41,  41,  41,  41,  41,
      3,   3,   3,   3,   3,   3,   0,   0,   3,   3,   3,   3,   3,   3,   0,   0,
      3,   3,   3,   3,   3,   3,   3,   3,   0,   3,   0,   3,   0,   3,   0,   3,
      3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   0,   0,
      3,   3,   3,   3,   3,   0,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,
      3,   3,   3,   3,   0,   0,   3,   3,   3,   3,   3,   3,   0,   3,   3,   3,
      0,   0,   3,   3,   3,   0,   3,   3,   3,   3,   3,   3,   3,   3,   3,   0,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,  41,  41,   1,   1,
      1,   1,   1,   1,   1,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   2,   0,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   0,   0,   0,
    175,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   3,   1,   1,   1,   2,   2,   1,   1,   1,   1,
      1,   1,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   1,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   0,
     53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,
      1,   1,   1,   1,   0,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   0,   0,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   1,   1,   1,   1,   1,   1,
     57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,
     57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,  57,   0,
     55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,
     55,  55,  55,  55,   0,   0,   0,   0,   0,  55,  55,  55,  55,  55,  55,  55,
     58,  58,  58,  58,  58,  58,  58,  58,  58,  58,  58,  58,  58,  58,  58,  58,
     58,  58,  58,  58,  58,  58,  58,  58,   0,   0,   0,   0,   0,   0,   0,  58,
     58,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  58,
     26,  26,  26,  26,  26,  26,  26,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     26,  26,  26,  26,  26,  26,  26,   0,  26,  26,  26,  26,  26,  26,  26,   0,
      1,   1,   1, 158,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,
     36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  36,  36,  36,  36,  36,   0,  36,  36,  36,  36,  36,
     36,  36,  36,  36,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     36,  36,  36,  36,  36,  36,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0,
      1, 183, 183, 182,   1,  36,  36,  36, 183, 183, 183, 183, 183, 183, 183, 183,
    183, 183,   1, 182, 183, 183, 183, 183, 183, 183, 183, 183, 182, 182, 182, 182,
      1,  36,  36,  36,  36,  36,  36,  36,  36,  36, 155, 155, 155, 155,  25,  25,
    182, 168, 168, 168, 168, 168,   1, 182,  36,  36,  36,  36, 176, 176,  36,  36,
      0,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,
     33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,
     33,  33,  33,  33,  33,  33,  33,   0,   0, 168, 168, 168, 168,  33,  33,  33,
    168,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34, 183, 168,  34,  34,  34,
      0,   0,   0,   0,   0,  35,  35,  35,  35,  35,  35,  35,  35,  35,  35,  35,
     35,  35,  35,  35,  35,  35,  35,  35,  35,  35,  35,  35,  35,  35,  35,  35,
      0,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,
     25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,   0,
     35,  35,  35,  35,  35,  35,  35,  35,  35,  35,  35,   0,   0,   0,   0,   0,
     36,  36,  36,  36,  36,  36,  36,  36,   1,   1,   1,   1,   1,   1,   1,   1,
     25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,   1,
     36,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
     36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,   1,   1,   1,   1,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,   0,
     34,  34,  34,  34,  34,  34,  34,  34,  36,  36,  36,  36,  36,  36,  36,  36,
     36,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,   1,
     37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,
     37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,   0,   0,   0,
     37,  37,  37,  37,  37,  37,  37,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     83,  83,  83,  83,  83,  83,  83,  83,  83,  83,  83,  83,  83,  83,  83,  83,
     70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,
     70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,  70,   0,   0,   0,   0,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 158,
     84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,  84,
     84,  84,  84,  84,  84,  84,  84,  84,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   2,   2,   2,   2,   2,   2,   2,   2,   2,
     59,  59,  59,  59,  59,  59,  59,  59,  59,  59,  59,  59,  59,  59,  59,  59,
     59,  59,  59,  59,  59,  59,  59,  59,  59,  59,  59,  59,   0,   0,   0,   0,
    190, 190, 190, 188, 188, 188, 186, 186, 186, 186,   0,   0,   0,   0,   0,   0,
     65,  65,  65,  65,  65,  65,  65,  65,  65,  65,  65,  65,  65,  65,  65,  65,
     65,  65,  65,  65,  65,  65,  65,  65,   0,   0,   0,   0,   0,   0,   0,   0,
     71,  71,  71,  71,  71,  71,  71,  71,  71,  71,  71,  71,  71,  71,  71,  71,
     71,  71,  71,  71,  71,  71,   0,   0,   0,   0,   0,   0,   0,   0,  71,  71,
     71,  71,  71,  71,  71,  71,  71,  71,  71,  71,   0,   0,   0,   0,   0,   0,
     10, 154,  10, 163,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,
     72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,
     72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72, 177,  72,
     73,  73,  73,  73,  73,  73,  73,  73,  73,  73,  73,  73,  73,  73,  73,  73,
     73,  73,  73,  73,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  73,
     25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,   0,   0,   0,
     85,  85,  85,  85,  85,  85,  85,  85,  85,  85,  85,  85,  85,  85,  85,  85,
     85,  85,  85,  85,  85,  85,  85,  85,  85,  85,  85,  85,  85,  85,   0, 156,
     85,  85,  85,  85,  85,  85,  85,  85,  85,  85,   0,   0,   0,   0,  85,  85,
     23,  23,  23,  23,  23,  23,  23,  23,  23,  23,  23,  23,  23,  23,  23,   0,
     77,  77,  77,  77,  77,  77,  77,  77,  77,  77,  77,  77,  77,  77,  77,  77,
     77,  77,  77,  77,  77,  77,  77,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     77,  77,  77,  77,  77,  77,  77,  77,  77,  77,  77,  77,  77,  77,   0,   0,
     77,  77,  77,  77,  77,  77,  77,  77,  77,  77,   0,   0,  77,  77,  77,  77,
     79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,
     79,  79,  79,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  79,  79,  79,  79,  79,
     86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,
     86,  86,  86,  86,  86,  86,  86,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,  26,  26,  26,  26,  26,  26,   0,   0,  26,  26,  26,  26,  26,  26,   0,
      0,  26,  26,  26,  26,  26,  26,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   3,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,   0,   0,
     86,  86,  86,  86,  86,  86,  86,  86,  86,  86,   0,   0,   0,   0,   0,   0,
     25,  25,  25,  25,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     25,  25,  25,  25,  25,  25,  25,   0,   0,   0,   0,  25,  25,  25,  25,  25,
     25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,   0,   0,   0,   0,
     36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,   0,   0,
     36,  36,  36,  36,  36,  36,  36,  36,  36,  36,   0,   0,   0,   0,   0,   0,
      2,   2,   2,   2,   2,   2,   2,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   5,   5,   5,   5,   5,   0,   0,   0,   0,   0,   6,   6,   6,
      6,   6,   6,   6,   6,   6,   6,   0,   6,   6,   6,   6,   6,   0,   6,   0,
      6,   6,   0,   6,   6,   0,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,
      7,   7,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   1,   1,
      0,   0,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
      7,   7,   7,   7,   7,   7,   7,   7,   0,   0,   0,   0,   0,   0,   0,   0,
      7,   7, 152,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7, 152,   0,   0,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   0,   0,
     41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,  41,   4,   4,
      1,   1,   1,   1,   1, 182, 182,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   0,   1,   1,   1,   1,   0,   0,   0,   0,
      7,   7,   7,   7,   7,   0,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
      7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   0,   0,   1,
      0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1, 183, 183, 183, 183, 183,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,
     34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34,  34, 168, 168,
      0,   0,  25,  25,  25,  25,  25,  25,   0,   0,  25,  25,  25,  25,  25,  25,
      0,   0,  25,  25,  25,  25,  25,  25,   0,   0,  25,  25,  25,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   1,   0,   1,   1,   1,   1,   1,   1,   1,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   0,   0,
     48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,   0,  48,  48,  48,
     48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,
     48,  48,  48,  48,  48,  48,  48,   0,  48,  48,  48,  48,  48,  48,  48,  48,
     48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,   0,  48,  48,   0,  48,
     48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,   0,   0,
     48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,   0,   0,   0,   0,   0,
    157, 157, 157,   0,   0,   0,   0, 173, 173, 173, 173, 173, 173, 173, 173, 173,
    173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173,
    173, 173, 173, 173,   0,   0,   0, 157, 157, 157, 157, 157, 157, 157, 157, 157,
      3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   0,
      3,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,  41,   0,   0,
     74,  74,  74,  74,  74,  74,  74,  74,  74,  74,  74,  74,  74,  74,  74,  74,
     74,  74,  74,  74,  74,  74,  74,  74,  74,  74,  74,  74,  74,   0,   0,   0,
     75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,
     75,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149,
    149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149,   0,   0,   0,   0,
     38,  38,  38,  38,  38,  38,  38,  38,  38,  38,  38,  38,  38,  38,  38,  38,
     38,  38,  38,  38,   0,   0,   0,   0,   0,   0,   0,   0,   0,  38,  38,  38,
     39,  39,  39,  39,  39,  39,  39,  39,  39,  39,  39,  39,  39,  39,  39,  39,
     39,  39,  39,  39,  39,  39,  39,  39,  39,  39,  39,   0,   0,   0,   0,   0,
    120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120,
    120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120,   0,   0,   0,   0,   0,
     49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,
     49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,  49,   0,  49,
     60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,
     60,  60,  60,  60,   0,   0,   0,   0,  60,  60,  60,  60,  60,  60,  60,  60,
     60,  60,  60,  60,  60,  60,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,
     50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,
     51,  51,  51,  51,  51,  51,  51,  51,  51,  51,  51,  51,  51,  51,  51,  51,
     51,  51,  51,  51,  51,  51,  51,  51,  51,  51,  51,  51,  51,  51,   0,   0,
     51,  51,  51,  51,  51,  51,  51,  51,  51,  51,   0,   0,   0,   0,   0,   0,
    136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 136,
    136, 136, 136, 136,   0,   0,   0,   0, 136, 136, 136, 136, 136, 136, 136, 136,
    136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 136,   0,   0,   0,   0,
    106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106,
    106, 106, 106, 106, 106, 106, 106, 106,   0,   0,   0,   0,   0,   0,   0,   0,
    103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103,
    103, 103, 103, 103,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 103,
    110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
    110, 110, 110, 110, 110, 110, 110,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    110, 110, 110, 110, 110, 110,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    110, 110, 110, 110, 110, 110, 110, 110,   0,   0,   0,   0,   0,   0,   0,   0,
     52,  52,  52,  52,  52,  52,   0,   0,  52,   0,  52,  52,  52,  52,  52,  52,
     52,  52,  52,  52,  52,  52,  52,  52,  52,  52,  52,  52,  52,  52,  52,  52,
     52,  52,  52,  52,  52,  52,   0,  52,  52,   0,   0,   0,  52,   0,   0,  52,
     87,  87,  87,  87,  87,  87,  87,  87,  87,  87,  87,  87,  87,  87,  87,  87,
     87,  87,  87,  87,  87,  87,   0,  87,  87,  87,  87,  87,  87,  87,  87,  87,
    118, 118, 118, 118, 118, 118, 118, 118, 118, 118, 118, 118, 118, 118, 118, 118,
    117, 117, 117, 117, 117, 117, 117, 117, 117, 117, 117, 117, 117, 117, 117, 117,
    117, 117, 117, 117, 117, 117, 117, 117, 117, 117, 117, 117, 117, 117, 117,   0,
      0,   0,   0,   0,   0,   0,   0, 117, 117, 117, 117, 117, 117, 117, 117, 117,
    128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128,
    128, 128, 128,   0, 128, 128,   0,   0,   0,   0,   0, 128, 128, 128, 128, 128,
     64,  64,  64,  64,  64,  64,  64,  64,  64,  64,  64,  64,  64,  64,  64,  64,
     64,  64,  64,  64,  64,  64,  64,  64,  64,  64,  64,  64,   0,   0,   0,  64,
     76,  76,  76,  76,  76,  76,  76,  76,  76,  76,  76,  76,  76,  76,  76,  76,
     76,  76,  76,  76,  76,  76,  76,  76,  76,  76,   0,   0,   0,   0,   0,  76,
     98,  98,  98,  98,  98,  98,  98,  98,  98,  98,  98,  98,  98,  98,  98,  98,
     97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,
     97,  97,  97,  97,  97,  97,  97,  97,   0,   0,   0,   0,  97,  97,  97,  97,
      0,   0,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,  97,
     61,  61,  61,  61,   0,  61,  61,   0,   0,   0,   0,   0,  61,  61,  61,  61,
     61,  61,  61,  61,   0,  61,  61,  61,   0,  61,  61,  61,  61,  61,  61,  61,
     61,  61,  61,  61,  61,  61,  61,  61,  61,  61,  61,  61,  61,  61,  61,  61,
     61,  61,  61,  61,  61,  61,   0,   0,  61,  61,  61,   0,   0,   0,   0,  61,
     61,  61,  61,  61,  61,  61,  61,  61,  61,   0,   0,   0,   0,   0,   0,   0,
     88,  88,  88,  88,  88,  88,  88,  88,  88,  88,  88,  88,  88,  88,  88,  88,
    116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116,
    112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112,
    112, 112, 112, 112, 112, 112, 112,   0,   0,   0,   0, 112, 112, 112, 112, 112,
    112, 112, 112, 112, 112, 112, 112,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     80,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,
     80,  80,  80,  80,  80,  80,   0,   0,   0,  80,  80,  80,  80,  80,  80,  80,
     89,  89,  89,  89,  89,  89,  89,  89,  89,  89,  89,  89,  89,  89,  89,  89,
     89,  89,  89,  89,  89,  89,   0,   0,  89,  89,  89,  89,  89,  89,  89,  89,
     90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,
     90,  90,  90,   0,   0,   0,   0,   0,  90,  90,  90,  90,  90,  90,  90,  90,
    121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121,
    121, 121,   0,   0,   0,   0,   0,   0,   0, 121, 121, 121, 121,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0, 121, 121, 121, 121, 121, 121, 121,
     91,  91,  91,  91,  91,  91,  91,  91,  91,  91,  91,  91,  91,  91,  91,  91,
     91,  91,  91,  91,  91,  91,  91,  91,  91,   0,   0,   0,   0,   0,   0,   0,
    130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130,
    130, 130, 130,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    130, 130, 130,   0,   0,   0,   0,   0,   0,   0, 130, 130, 130, 130, 130, 130,
    146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146, 146,
    146, 146, 146, 146, 146, 146, 146, 146,   0,   0,   0,   0,   0,   0,   0,   0,
    146, 146, 146, 146, 146, 146, 146, 146, 146, 146,   0,   0,   0,   0,   0,   0,
      7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   0,
    148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148,
    148, 148, 148, 148, 148, 148, 148, 148,   0,   0,   0,   0,   0,   0,   0,   0,
    147, 147, 147, 147, 147, 147, 147, 147, 147, 147, 147, 147, 147, 147, 147, 147,
    147, 147, 147, 147, 147, 147, 147, 147, 147, 147,   0,   0,   0,   0,   0,   0,
     94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,
     94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,   0,   0,
      0,   0,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,  94,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  94,
     92,  92,  92,  92,  92,  92,  92,  92,  92,  92,  92,  92,  92,  92,  92,  92,
     92,  92,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  92,   0,   0,
    101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101,
    101, 101, 101, 101, 101, 101, 101, 101, 101,   0,   0,   0,   0,   0,   0,   0,
    101, 101, 101, 101, 101, 101, 101, 101, 101, 101,   0,   0,   0,   0,   0,   0,
     96,  96,  96,  96,  96,  96,  96,  96,  96,  96,  96,  96,  96,  96,  96,  96,
     96,  96,  96,  96,  96,   0,  96,  96,  96,  96,  96,  96,  96,  96,  96,  96,
     96,  96,  96,  96,  96,  96,  96,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111,
    111, 111, 111, 111, 111, 111, 111,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
    100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,   0,   0,
      0,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,
     19,  19,  19,  19,  19,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109,
    109, 109,   0, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109,
    109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109,   0,
    129, 129, 129, 129, 129, 129, 129,   0, 129,   0, 129, 129, 129, 129,   0, 129,
    129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129,   0, 129,
    129, 129, 129, 129, 129, 129, 129, 129, 129, 129,   0,   0,   0,   0,   0,   0,
    123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123,
    123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123,   0,   0,   0,   0,   0,
    123, 123, 123, 123, 123, 123, 123, 123, 123, 123,   0,   0,   0,   0,   0,   0,
    107, 165, 107, 165,   0, 107, 107, 107, 107, 107, 107, 107, 107,   0,   0, 107,
    107,   0,   0, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107,
    107, 107, 107, 107, 107, 107, 107, 107, 107,   0, 107, 107, 107, 107, 107, 107,
    107,   0, 107, 107,   0, 107, 107, 107, 107, 107,   0, 165, 165, 107, 107, 107,
    107, 107, 107, 107, 107,   0,   0, 107, 107,   0,   0, 107, 107, 107,   0,   0,
    107,   0,   0,   0,   0,   0,   0, 107,   0,   0,   0,   0,   0, 107, 107, 107,
    107, 107, 107, 107,   0,   0, 107, 107, 107, 107, 107, 107, 107,   0,   0,   0,
    107, 107, 107, 107, 107,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135,
    135, 135, 135, 135, 135, 135, 135, 135, 135, 135,   0, 135,   0, 135, 135,   0,
    124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124,
    124, 124, 124, 124, 124, 124, 124, 124,   0,   0,   0,   0,   0,   0,   0,   0,
    124, 124, 124, 124, 124, 124, 124, 124, 124, 124,   0,   0,   0,   0,   0,   0,
    122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122,
    122, 122, 122, 122, 122, 122,   0,   0, 122, 122, 122, 122, 122, 122, 122, 122,
    122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122,   0,   0,
    114, 114, 114, 114, 114, 114, 114, 114, 114, 114, 114, 114, 114, 114, 114, 114,
    114, 114, 114, 114, 114,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    114, 114, 114, 114, 114, 114, 114, 114, 114, 114,   0,   0,   0,   0,   0,   0,
     32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32,   0,   0,   0,
    102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102,
    102, 102, 102, 102, 102, 102, 102, 102,   0,   0,   0,   0,   0,   0,   0,   0,
    102, 102, 102, 102, 102, 102, 102, 102, 102, 102,   0,   0,   0,   0,   0,   0,
    126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126,
    126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126,   0,   0, 126, 126, 126,
    126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126,   0,   0,   0,   0,
    142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142,
    142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142,   0,   0,   0,   0,
    125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125,
    125, 125, 125,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 125,
    141, 141, 141, 141, 141, 141, 141, 141, 141, 141, 141, 141, 141, 141, 141, 141,
    141, 141, 141, 141, 141, 141, 141, 141,   0,   0,   0,   0,   0,   0,   0,   0,
    140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140,
    140, 140, 140, 140,   0,   0, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140,
    140, 140, 140,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119,
    119, 119, 119, 119, 119, 119, 119, 119, 119,   0,   0,   0,   0,   0,   0,   0,
    133, 133, 133, 133, 133, 133, 133, 133, 133,   0, 133, 133, 133, 133, 133, 133,
    133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133,
    133, 133, 133, 133, 133, 133, 133,   0, 133, 133, 133, 133, 133, 133, 133, 133,
    133, 133, 133, 133, 133, 133,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133,   0,   0,   0,
    134, 134, 134, 134, 134, 134, 134, 134, 134, 134, 134, 134, 134, 134, 134, 134,
      0,   0, 134, 134, 134, 134, 134, 134, 134, 134, 134, 134, 134, 134, 134, 134,
    134, 134, 134, 134, 134, 134, 134, 134,   0, 134, 134, 134, 134, 134, 134, 134,
    134, 134, 134, 134, 134, 134, 134,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    138, 138, 138, 138, 138, 138, 138,   0, 138, 138,   0, 138, 138, 138, 138, 138,
    138, 138, 138, 138, 138, 138, 138, 138, 138, 138, 138, 138, 138, 138, 138, 138,
    138, 138, 138, 138, 138, 138, 138,   0,   0,   0, 138,   0, 138, 138,   0, 138,
    138, 138, 138, 138, 138, 138, 138, 138,   0,   0,   0,   0,   0,   0,   0,   0,
    138, 138, 138, 138, 138, 138, 138, 138, 138, 138,   0,   0,   0,   0,   0,   0,
    143, 143, 143, 143, 143, 143,   0, 143, 143,   0, 143, 143, 143, 143, 143, 143,
    143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143,
    143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143,   0,
    143, 143,   0, 143, 143, 143, 143, 143, 143,   0,   0,   0,   0,   0,   0,   0,
    143, 143, 143, 143, 143, 143, 143, 143, 143, 143,   0,   0,   0,   0,   0,   0,
    144, 144, 144, 144, 144, 144, 144, 144, 144, 144, 144, 144, 144, 144, 144, 144,
    144, 144, 144, 144, 144, 144, 144, 144, 144,   0,   0,   0,   0,   0,   0,   0,
     63,  63,  63,  63,  63,  63,  63,  63,  63,  63,  63,  63,  63,  63,  63,  63,
     63,  63,  63,  63,  63,  63,  63,  63,  63,  63,   0,   0,   0,   0,   0,   0,
     63,  63,  63,  63,  63,  63,  63,  63,  63,  63,  63,  63,  63,  63,  63,   0,
     63,  63,  63,  63,  63,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     63,  63,  63,  63,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     81,  81,  81,  81,  81,  81,  81,  81,  81,  81,  81,  81,  81,  81,  81,  81,
     81,  81,  81,  81,  81,  81,  81,  81,  81,  81,  81,  81,  81,  81,  81,   0,
    127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
    127, 127, 127, 127, 127, 127, 127,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     84,  84,  84,  84,  84,  84,  84,  84,  84,   0,   0,   0,   0,   0,   0,   0,
    115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115,
    115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115,   0,
    115, 115, 115, 115, 115, 115, 115, 115, 115, 115,   0,   0,   0,   0, 115, 115,
    104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104,
    104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104,   0,   0,
    104, 104, 104, 104, 104, 104,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108,
    108, 108, 108, 108, 108, 108,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    108, 108, 108, 108, 108, 108, 108, 108, 108, 108,   0, 108, 108, 108, 108, 108,
    108, 108,   0, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108,
    108, 108, 108, 108, 108, 108, 108, 108,   0,   0,   0,   0,   0, 108, 108, 108,
    145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145,
    145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145,   0,   0,   0,   0,   0,
     99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,
     99,  99,  99,  99,  99,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  99,
    137, 139,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137,
    137, 137,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    137, 137, 137,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     34,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,
     33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,   0,
    139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139,
    139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139,   0,   0,   0,   0,
    105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105,
    105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105,   0,   0,   0,   0,   0,
    105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105,   0,   0,   0,
    105, 105, 105, 105, 105, 105, 105, 105, 105,   0,   0,   0,   0,   0,   0,   0,
    105, 105, 105, 105, 105, 105, 105, 105, 105, 105,   0,   0, 105, 105, 105, 105,
    105, 105, 105, 105,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   1,   0,   0,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,  41,  41,  41,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,  41,  41,  41,  41,  41,
     41,  41,  41,   1,   1,  41,  41,  41,  41,  41,  41,  41,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,  41,  41,  41,  41,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,
      3,   3,   3,   3,   3,   3,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     36,  36,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   1,   1,
      0,   0,   1,   0,   0,   1,   1,   0,   0,   1,   1,   1,   1,   0,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   1,   0,   1,   1,   1,
      1,   1,   1,   1,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   0,   1,   1,   1,   1,   0,   0,   1,   1,   1,
      1,   1,   1,   1,   1,   0,   1,   1,   1,   1,   1,   1,   1,   0,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   1,   1,   1,   1,   0,
      1,   1,   1,   1,   1,   0,   1,   0,   0,   0,   1,   1,   1,   1,   1,   1,
      1,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   1,   1,
    131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131,
    131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 131, 131, 131, 131, 131,
      0, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131,
     57,  57,  57,  57,  57,  57,  57,   0,  57,  57,  57,  57,  57,  57,  57,  57,
     57,  57,  57,  57,  57,  57,  57,  57,  57,   0,   0,  57,  57,  57,  57,  57,
     57,  57,   0,  57,  57,   0,  57,  57,  57,  57,  57,   0,   0,   0,   0,   0,
    113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113,
    113, 113, 113, 113, 113,   0,   0, 113, 113, 113, 113, 113, 113, 113, 113, 113,
    113, 113, 113, 113, 113, 113, 113,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132,
    132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132,   0,   0,   0,   0,   0,
    132, 132, 132, 132, 132, 132, 132, 132, 132, 132,   0,   0,   0,   0, 132, 132,
      1,   1,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      7,   7,   7,   7,   0,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
      0,   7,   7,   0,   7,   0,   0,   7,   0,   7,   7,   7,   7,   7,   7,   7,
      7,   7,   7,   0,   7,   7,   7,   7,   0,   7,   0,   7,   0,   0,   0,   0,
      0,   0,   7,   0,   0,   0,   0,   7,   0,   7,   0,   7,   0,   7,   7,   7,
      0,   7,   7,   0,   7,   0,   0,   7,   0,   7,   0,   7,   0,   7,   0,   7,
      0,   7,   7,   0,   7,   0,   0,   7,   7,   7,   7,   0,   7,   7,   7,   7,
      7,   7,   7,   0,   7,   7,   7,   7,   0,   7,   7,   7,   7,   0,   7,   0,
      7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   0,   7,   7,   7,   7,   7,
      7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   0,   0,   0,   0,
      0,   7,   7,   7,   0,   7,   7,   7,   7,   7,   0,   7,   7,   7,   7,   7,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
     33,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     36,  36,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   0,
      1,   0,   0,   1,   1,   1,   1,   0,   0,   0,   1,   0,   1,   1,   1,   1,
      1,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     36,  36,  36,  36,  36,  36,  36,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     36,  36,  36,  36,  36,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     36,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
};

/* Script_Extensions: 15345 bytes. */

static RE_ScriptExt re_scripts_extensions_table[] = {
    {{  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  2,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  3,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  4,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  5,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  6,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  7,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  8,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  9,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 10,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 11,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 12,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 13,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 14,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 15,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 16,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 17,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 18,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 19,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 20,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 21,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 22,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 23,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 24,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 25,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 26,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 27,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 28,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 29,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 30,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 31,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 32,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 33,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 34,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 35,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 36,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 37,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 38,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 39,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 40,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 41,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 42,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 43,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 44,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 45,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 46,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 47,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 48,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 49,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 50,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 51,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 52,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 53,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 54,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 55,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 56,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 57,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 58,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 59,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 60,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 61,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 62,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 63,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 64,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 65,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 66,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 67,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 68,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 69,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 70,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 71,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 72,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 73,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 74,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 75,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 76,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 77,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 78,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 79,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 80,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 81,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 82,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 83,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 84,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 85,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 86,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 87,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 88,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 89,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 90,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 91,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 92,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 93,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 94,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 95,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 96,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 97,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 98,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 99,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{100,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{101,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{102,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{103,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{104,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{105,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{106,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{107,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{108,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{109,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{110,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{111,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{112,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{113,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{114,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{115,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{116,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{117,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{118,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{119,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{120,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{121,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{122,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{123,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{124,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{125,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{126,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{127,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{128,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{129,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{130,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{131,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{132,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{133,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{134,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{135,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{136,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{137,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{138,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{139,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{140,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{141,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{142,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{143,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{144,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{145,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{146,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{147,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{148,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  7,  55,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  7, 146,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  7,   8,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  7,   9,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  5,  24,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 10,  11,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 35,  36,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 54,  85,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 48,  52,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  4,  57,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  2,   4,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  4, 120,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 10, 107,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 10, 100,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 10,  15,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  2,  24,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 15, 107,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 13, 109,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 12, 129,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 33,  34,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 32,  65,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  7,   8,   9,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 11,  59,  96,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 23,  47,  96,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 48,  52, 110,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 10,  17, 107,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  2,  10, 107,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 33,  34,  36,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  2,  23,  72,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  7,   8,   9, 146,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 10,  11,  17, 107,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 42,  43,  44,  45,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 10,  92, 111, 142,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 25,  33,  34,  35,  36,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 25,  33,  34,  35,  36,  37,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 10,  14,  15,  16,  17,  18,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  7,   8,  95, 112, 121, 132, 146, 147,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{ 10,  12,  13,  92, 102, 109, 111, 114, 123, 124, 142,   0,   0,   0,   0,   0,   0,   0,   0}},
    {{  2,  10,  11,  12,  13,  14,  15,  16,  17,  18, 107, 124,   0,   0,   0,   0,   0,   0,   0}},
    {{ 10,  12,  13,  17,  92, 102, 109, 111, 114, 123, 124, 142,   0,   0,   0,   0,   0,   0,   0}},
    {{  2,  10,  11,  12,  13,  14,  15,  16,  17,  18, 100, 107, 124,   0,   0,   0,   0,   0,   0}},
    {{ 10,  12,  13,  17,  18,  92, 102, 109, 111, 114, 123, 124, 142,   0,   0,   0,   0,   0,   0}},
    {{ 10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  59, 102, 107, 111, 123, 124, 142, 143,   0}},
    {{ 10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  46,  59, 102, 107, 111, 123, 124, 142, 143}}
};

int re_get_script_extensions(RE_UINT32 ch, RE_UINT8* scripts) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;
    RE_UINT8* scr;
    int count;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_script_extensions_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_script_extensions_stage_2[pos + f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_script_extensions_stage_3[pos + f] << 4;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_script_extensions_stage_4[pos + f] << 4;
    value = re_script_extensions_stage_5[pos + code];

    scr = re_scripts_extensions_table[value].scripts;
    scripts[0] = scr[0];
    count = 1;

    if (scr[0] != 0) {
        while (count < RE_MAX_SCX && scr[count] != 0) {
            scripts[count] = scr[count];
            ++count;
        }
    }

    return count;
}

/* Word_Break. */

static RE_UINT8 re_word_break_stage_1[] = {
     0,  1,  2,  2,  2,  3,  4,  5,  6,  7,  8,  9,  2, 10, 11, 12,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
    13,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,
};

static RE_UINT8 re_word_break_stage_2[] = {
      0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,
     16,   1,  17,  18,  19,   1,  20,  21,  22,  23,  24,  25,  26,  27,   1,  28,
     29,  30,  31,  31,  32,  31,  31,  31,  31,  31,  31,  31,  33,  34,  35,  31,
     36,  37,  38,  39,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
      1,   1,   1,   1,  40,   1,  41,  42,  43,  44,  45,  46,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,  47,  31,  31,  31,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  48,   1,  49,  50,  51,
     52,  53,  54,  55,  56,  57,   1,  58,  59,  60,  61,  62,  63,  64,  31,  65,
     66,  67,  68,  69,  70,  71,  72,  73,  74,  31,  75,  31,  76,  77,  78,  31,
      1,   1,   1,  79,  80,  81,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
      1,   1,   1,   1,  82,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
     31,  31,  31,  31,   1,   1,  83,  31,  31,  31,  31,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  31,  31,  31,  31,   1,   1,  84,  85,  31,  31,  86,  87,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
     88,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  89,  31,  31,  31,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
     31,  90,  91,  31,  92,  93,  94,  95,  31,  31,  96,  31,  31,  31,  31,  31,
     97,  31,  31,  31,  31,  31,  31,  31,  98,  99,  31,  31,  31,  31, 100,  31,
     31, 101,  31, 102,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
    103, 104,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,
};

static RE_UINT16 re_word_break_stage_3[] = {
      0,   1,   2,   3,   4,   5,   6,   6,   7,   7,   7,   7,   7,   7,   7,   7,
      7,   7,   7,   7,   7,   7,   8,   9,  10,  10,  10,  11,  12,  13,   7,  14,
      7,   7,   7,   7,  15,   7,   7,   7,   7,  16,  17,   7,  18,  19,  20,  21,
     22,   7,  23,  24,   7,   7,  25,  26,  27,  28,  29,   7,   7,  30,  31,  32,
     33,  34,  35,  36,  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,
     49,  50,  51,  52,  53,  54,  55,  56,  57,  54,  58,  59,  60,  61,  62,  63,
     64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,
     37,  80,  81,  37,  37,  82,  83,  37,  84,  85,  86,  87,  88,  89,  90,  37,
     37,  91,  92,  93,  94,   7,  95,  96,   7,   7,  97,   7,  98,  99, 100,   7,
    101,   7, 102,  37, 103,   7,   7, 104, 105,   7,   7,   7,   7,   7,   7,   7,
      7,   7,   7, 106, 107,   7,   7, 108, 109, 110, 111, 112,  37, 113, 114, 115,
    116,   7,   7, 117, 118, 119,   7, 120, 121, 122,  63,  37,  37,  37, 123,  37,
    124,  37, 125, 126, 127, 128,  37,  37, 129, 130, 131, 132, 133, 134,   7, 135,
      7, 136, 137, 138, 139, 140, 141, 142,   7,   7,   7,   7,   7,   7,  10, 143,
    104,   7, 144, 138,   7, 145, 146, 147, 148, 149, 150, 151, 152,  37, 153, 154,
    155, 156, 157,   7, 158,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,
     37,  37,  37,  37,  37, 159,   7, 160,   7, 161, 121,   7,   7,   7,   7, 162,
      7,  95,   7, 163, 164, 165, 165,  10,  37, 166,  37,  37,  37,  37,  37,  37,
    167, 168,  37,  37, 169, 170, 170, 171, 172,  16,   7,   7, 173, 174,  37, 175,
     37,  37,  37,  37,  37,  37, 175, 176, 170, 170, 177,  37,  37,  37,  37,  37,
      7,   7,   7,   7, 178,  37, 179, 138, 180, 181,   7, 182, 183,   7,   7, 184,
    185,   7,   7,   7,   7, 186,  37, 185, 187, 188,   7, 189, 190, 130, 191, 192,
     31, 193, 194, 195,  41, 196, 197, 198,   7, 199, 200, 201,  37, 202, 203, 204,
    205, 206,   7, 207,   7,   7,   7, 208,   7,   7,   7,   7,   7, 209, 210, 211,
    212, 213, 214,   7,   7, 215, 216,   7,   7, 138, 179,   7, 217,   7, 218, 219,
    220, 221, 222, 223,   7,   7,   7, 224, 225,   2,   3, 226, 227, 121, 228, 229,
    230, 231, 232,  37,   7,   7,   7, 174,  37,  37,   7, 233,  37,  37,  37, 234,
     37,  37,  37,  37, 195,   7, 235, 236,   7, 237, 238, 239, 138,   7, 240,  37,
      7,   7,   7,   7, 138, 241, 242, 211,   7, 243,   7, 244,  37,  37,  37,  37,
      7, 164, 120, 218,  37,  37,  37,  37, 245, 246, 120, 164, 121,  37,  37, 247,
    120, 186,  37,  37,   7,   8,  37,  37, 248, 249,  37, 195, 195,  37,  86, 250,
      7, 120, 120, 251, 215,  37,  37,  37,   7,   7, 158,  37,   7, 251,   7, 251,
      7, 252,  37,  37,  37,  37,  37,  37, 195, 253, 254,  37,  37,  37,  37,  37,
    133, 255, 256, 257, 133, 258, 259, 260, 133, 261, 262, 263, 133, 196, 264,  37,
    265, 266,  37,  37, 267, 139, 268, 269, 270, 271, 272, 273,  37,  37,  37,  37,
      7, 274, 275,  37,   7,  28, 276,  37,  37,  37,  37,  37,   7, 277, 278,  37,
      7,  28, 279,  37,   7, 280, 115,  37, 281, 282,  37,  37,  37,  37,  37,  37,
      7, 283,  37,  37,  37,   7,   7, 284, 285, 286, 287,   7, 288,  37,   7, 117,
    289, 290, 291, 292, 293, 294,  37,  37, 295, 296, 297, 298, 299, 115,  37,  37,
     37,  37,  37,  37,  37,  37,  37, 300,   7,   7,   7,   7, 186,  37,  37,  37,
      7,   7,   7, 173,   7,   7,   7,   7,   7,   7, 244,  37,  37,  37,  37,  37,
      7, 173,  37,  37,  37,  37,  37,  37,   7,   7, 301,  37,  37,  37,  37,  37,
      7, 117, 121, 115,  37,  37, 179, 302,   7, 303, 304, 305, 103,  37,  37,  37,
     37,  37,   7,   7,  37,  37,  37,  37,   7,   7, 306, 307, 308,  37,  37, 309,
    310,  37,  37,  37,  37,  37,  37,  37,   7,   7,   7, 311, 312, 313,  37,  37,
     37,  37,  37, 314, 315, 316,  37,  37,  37,  37, 317,  37,  37,  37,  37,  37,
      7,   7, 318,   7, 319, 320, 321,   7, 322, 323, 324,   7,   7,   7,   7,   7,
      7,   7,   7,   7,   7, 325, 326,  96, 318, 318, 161, 161, 289, 289, 327, 328,
     10, 329,  10, 330, 331, 332,  37,  37, 333, 334,  37,  37,  37,  37,  37,  37,
      7,   7,   7,   7,   7,   7, 335,  37,   7,   7, 336,  37,  37,  37,  37,  37,
    321, 337, 338, 339, 340, 341,  37,  37,  37, 179, 342, 342, 160,  37,  37, 343,
     37,  37,  37,  37,  37,  37,  37, 344, 345,  10,  10,  10,  37,  37,  37,  37,
     10,  10,  10,  10,  10,  10,  10, 346,
};

static RE_UINT8 re_word_break_stage_4[] = {
      0,   0,   1,   2,   0,   0,   0,   0,   3,   4,   0,   5,   6,   6,   7,   0,
      8,   9,   9,   9,   9,   9,  10,  11,   8,   9,   9,   9,   9,   9,  10,   0,
      0,  12,   0,   0,   0,   0,   0,   0,   0,   0,  13,  14,   0,  15,  13,   0,
      9,   9,   9,   9,   9,  10,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,
      9,   9,   9,   9,   9,   9,   0,  16,   9,  17,   0,   9,   9,   9,   9,   9,
     18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,   9,  19,  16,  20,
      0,  21,  10,  19,   9,   9,   9,   9,  22,   9,   9,   9,   9,   9,   9,   9,
      9,   9,   9,   9,   9,  22,   9,   9,  23,  18,  24,   9,   9,   9,   9,   9,
      9,   9,   9,   9,   8,   9,   9,   9,   9,   9,   9,   9,   9,  10,  25,  26,
      9,   9,  27,   0,  28,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  29,
     30,  29,   0,   0,  31,  31,  31,  31,  31,  31,  32,  33,  34,  35,   0,   0,
     36,  37,   0,  38,  18,  18,  39,  40,   9,   9,  41,  18,  18,  18,  18,  18,
      6,   6,  42,  43,  44,   9,   9,   9,   9,   9,   9,   9,   9,  45,  18,  46,
     18,  47,  48,  24,   6,   6,  49,  50,   0,   0,   0,  51,  52,   9,   9,   9,
      9,   9,   9,   9,  18,  18,  18,  18,  18,  18,  39,   8,   9,   9,   9,   9,
      9,  53,  18,  18,  54,   0,   0,   0,   6,   6,  49,   9,   9,   9,   9,   9,
      9,   9,  41,  18,  18,  55,  56,  57,   9,   9,   9,   9,   9,  53,  58,  18,
     18,  59,  59,  60,   0,   0,   0,   0,   9,   9,   9,   9,   9,   9,  59,   0,
      9,   9,  10,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      9,   9,   9,   9,   9,  19,   9,  55,   0,   0,   0,   0,  61,  18,  18,  18,
     62,  18,  18,  18,  18,  18,  18,  18,  18,   9,   9,   9,   9,   9,   9,   9,
      9,   9,   9,   9,   9,   9,  53,  63,  18,  18,  18,  18,  59,  18,   9,   9,
     53,  64,   6,   6,   8,   9,   9,   9,  59,   8,   9,  50,  50,   9,   9,   9,
      9,   9,  19,   9,  26,  16,  55,  63,  18,  65,  65,  66,   0,  61,   0,  22,
     53,  64,   6,   6,  55,   0,   0,  67,  28,   8,  10,  68,  50,   9,   9,   9,
      9,   9,  19,   9,  19,  69,  55,  48,  39,  61,  65,  60,  57,   0,   8,  26,
      0,  64,   6,   6,  24,  70,   0,   0,  28,   8,   9,  22,  22,   9,   9,   9,
      9,   9,  19,   9,  19,   8,  55,  63,  18,  29,  29,  60,  17,   0,   0,   0,
     53,  64,   6,   6,   0,   0,  45,  18,  28,   8,   9,  50,  50,   9,   9,   9,
     18,  65,  65,  60,   0,  71,   0,  22,  53,  64,   6,   6,  72,   0,   0,   0,
     73,   8,  10,  16,  19,  55,  69,  19,  68,  17,  10,  16,   9,   9,  55,  71,
     39,  71,  48,  60,  17,  61,   0,   0,   0,  64,   6,   6,   0,   0,   0,   0,
     18,  44,   9,  19,  19,   9,   9,   9,   9,   9,  19,   9,   9,   9,  55,  45,
     18,  48,  48,  60,   0,  30,  10,   0,  53,  64,   6,   6,   0,   0,   0,   0,
     59,   8,   9,  19,  19,   9,   9,   9,   9,   9,  19,   9,   9,   8,  55,  63,
     18,  48,  48,  60,   0,  30,   0,  13,  53,  64,   6,   6,  69,   0,   0,   0,
     18,   8,   9,  19,  19,   9,   9,   9,   9,   9,   9,   9,   9,   9,  41,  63,
     18,  48,  48,  66,   0,  41,   0,  68,  53,  64,   6,   6,   0,   0,  16,   9,
     71,   8,   9,   9,   9,  10,  16,   9,   9,   9,   9,   9,  22,   9,   9,  72,
      9,  10,  74,  61,  18,  75,  18,  18,   0,  64,   6,   6,  71,   0,   0,   0,
      0,   0,   0,   0,  57,  18,  39,   0,   0,  61,  18,  39,   6,   6,  76,   0,
      0,   0,   0,   0,  57,  18,  29,  77,   0,   0,  18,  60,   6,   6,  76,   0,
     17,   0,   0,   0,   0,   0,  60,   0,   6,   6,  76,   0,   0,  78,  57,  71,
      9,   9,   8,   9,   9,   9,   9,   9,   9,   9,   9,  17,  28,  18,  18,  18,
     18,  48,   9,  59,  18,  18,  28,  18,  18,  18,  18,  18,  18,  18,  18,  77,
      0,  74,   0,   0,   0,   0,   0,   0,   0,   0,  61,  18,  18,  18,  18,  39,
      6,   6,  76,   0,   0,  71,  60,  71,  48,  65,  18,  60,  28,  77,   0,   0,
     71,  18,  18,  29,   6,   6,  79,  60,   9,  22,   0,  72,   9,   9,   9,   9,
      9,   9,   9,   9,   9,   9,  10,   9,   9,   9,  19,  55,   9,  10,  19,  55,
      9,   9,  19,  55,   9,   9,   9,   9,   9,   9,   9,   9,  19,  55,   9,  10,
     19,  55,   9,   9,   9,  10,   9,   9,   9,   9,   9,   9,  19,  55,   9,   9,
      9,   9,   9,   9,   9,   9,  10,  28,   9,   9,   9,   9,   0,   0,   0,   0,
      9,   9,   9,   9,   9,  55,   9,  55,   8,   9,   9,   9,   9,   9,   9,   9,
      9,   9,   9,  50,   9,   9,   9,   9,  80,   9,   9,   9,   9,   9,  10,   0,
      9,   9,  10,  16,   9,   9,  17,   0,   9,   9,   9,  19,  53,  77,   0,   0,
      9,   9,   9,   9,  53,  77,   0,   0,   9,   9,   9,   9,  53,   0,   0,   0,
      9,   9,   9,  19,  81,   0,   0,   0,   0,   0,   0,   0,   0,  18,  18,  18,
     18,  18,  18,  18,  18,   0,   0,  57,   6,   6,  76,   0,   0,   0,   0,   0,
      0,   0,  61,  82,   6,   6,  76,   0,   9,   9,   9,   9,   9,   9,  17,   0,
      9,  83,   9,   9,   9,   9,   9,   9,   9,   9,  84,   0,   9,   9,   9,   9,
      9,   9,   9,   9,   9,  55,   0,   0,   9,   9,   9,   9,   9,   9,   9,  10,
     18,  18,  18,   0,  18,  18,  18,   0,   0,   0,   0,   0,   6,   6,  76,   0,
      9,   9,   9,   9,   9,  41,  18,   0,   0,   0,   0,   0,   0,  28,  18,  39,
     18,  18,  18,  18,  18,  18,  18,  65,   6,   6,  76,   0,   6,   6,  76,   0,
      0,   0,   0,   0,  18,  18,  18,  39,  18,  44,   9,   9,   9,   9,   9,   9,
      9,   9,   9,   9,   9,  18,  18,  18,  18,  44,   9,   0,   6,   6,  76,   0,
      0,   0,  61,  18,  18,   0,   0,   0,  85,   9,   9,   9,   9,   9,   9,   9,
     59,  18,  18,  24,   6,   6,  49,   9,   9,  53,  18,  18,  18,   0,   0,   0,
      9,  18,  18,  18,  18,  18,   0,   0,   6,   6,  76,   8,   6,   6,  49,   9,
      9,   9,   9,   9,   9,   9,   9,  55,   9,   9,  17,   0,   9,   9,   9,   9,
      9,   9,   9,   9,   9,   9,  10,   8,   0,   0,   0,   0,  39,  18,  18,  18,
     18,  18,  44,  52,  53,  47,  60,   0,  18,  18,  18,  18,  18,  18,  29,  18,
      9,  55,   9,  55,   9,   9,  25,  25,   9,   9,   9,   9,   9,  19,   9,  26,
     16,  19,   9,  17,   9,  16,   9,   0,   9,   9,   9,  17,  16,  19,   9,  17,
     86,  87,  87,  88,   0,   0,  89,   0,   0,  90,  91,  92,   0,   0,   0,  11,
     93,  94,   0,   0,   0,  93,   0,  95,  36,  96,  36,  36,  72,   0,   0,  68,
      0,   0,   0,   0,   9,   9,   9,  17,   0,   0,   0,   0,  18,  18,  18,  18,
     18,  18,  18,  18,  77,   0,   0,   0,  13,  68,  16,   9,   9,  72,   8,  55,
      0,  26,  19,  22,   9,   9,  55,   9,   0,   8,  55,  13,   0,   0,   0,   0,
      9,   9,  17,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  16,   9,   9,
      9,   9,  55,   0,   0,   0,   0,   0,   9,   9,   9,  10,   9,   9,   9,   9,
      9,  17,  68,  41,  24,   0,   0,   0,   9,   9,   0,  68,   0,   0,   0,  61,
      9,   9,   9,   9,   9,  10,   0,   0,   9,  10,   9,  10,   9,  10,   9,  10,
      0,   0,   0,  68,   0,   0,   0,   0,  97,  72,   0,   0,   0,   0,   0,   0,
      0,   0,  71,  18,  98,  99,  68,  17,   0,   0,   0,   0,   0,   0, 100, 101,
    102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 103, 102,
      0,   8,   9,   9,   9,   9,   9,   9,   9,   9,   9,  10,   0,   0,   0,   0,
      9,   9,   9,   9,   9,   9,  10,   0,   0,   0,   0,   0, 102, 102, 102, 102,
    102, 102, 102, 102, 102, 102, 102, 103, 102, 102, 102, 102, 102, 102,   0,   0,
      9,   9,   9,  17,   0,   0,   0,   0,   0,   0,   0,   0,   9,   9,   9,   9,
      9,   9,   9,  17,   9,   9,   9,   9,   6,   6,  49,   0,   0,   0,   0,   0,
      9,   9,   9,  41,  39,  18,  18, 104,   9,   9,   9,   9,   9,   9,   9,  53,
      9,   9,   9,   9,  60,   0,   0,   0,   0,   0,   0,   0,   0,  68,   9,   9,
      9,   9,   9,   9,   9,   9,  55,   0, 105, 105,  41,   9,   9,   9,   9,   9,
     41,  18,   0,   0,   0,   0,   0,   0,   9,   9,   9,   9,   9,   0,   0,   0,
     24,   9,   9,   9,   9,   9,   9,   9,  18,  60,   0,   0,   6,   6,  76,   0,
     18,  18,  18,  18,  24,   9,  68, 106,   9,  53,  18,  60,   9,   9,   9,   9,
      9,  41,  18,  18,  18,   0,   0,   0,   9,   9,   9,   9,   9,   9,   9,  17,
      9,   9,   9,   9,  41,  18,  18,  18,  77,   0,   0,  68,   6,   6,  76,   0,
      0,  57,   0,   0,   6,   6,  76,   0,   9,   9,  59,  18,  18,  39,   0,   0,
     41,   9,   9,  60,   6,   6,  76,   0,   0,   0,   0,   0,   0,   0,  61,  60,
      0,   0,   0,   0,  48,  65,  77,  71,  57,   0,   0,   0,   0,   0,   0,   0,
      9,   9,  41,  18,  16, 107,   0,   0,   8,  10,   8,  10,   8,  10,   0,   0,
      9,  10,   9,  10,   9,   9,   9,   9,   9,  55,   0,   0,   9,   9,   9,   9,
     41,  18,  39,  60,   6,   6,  76,   0,   9,   0,   0,   0,   9,   9,   9,   9,
      9,  10,  68,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   0,
      9,  10,   0,   0,  68,   9,   0, 108,  31,  31, 109,  31,  31,  32,  31, 110,
    111, 109,  31,  31,   9,   9,   9,   9,   9,   9,   9,   9,  55,   0,   0,   0,
      0,   0,   0,   0,  68,   9,   9,   9,   9,   9,   9,   9,  16,   9,   9,   9,
      9,   9,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   9,   9,   9,   0,
     18,  18,  18,  18, 112,  94,   0,   0,  18,  18,  18,  18,  11,  93,   0,   0,
      0,   0,   0, 113,   5, 114,   0,   0,   0,   0,   0,   0,   9,  19,   9,   9,
      9,   9,   9,   9,   9,   9,   9, 115,   0, 116,   0,   5,   0,   0, 117,   0,
      0, 118, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 119,
     16,   9,  16,   9,  16,   9,  16,  17,   0,   0,   0,   0,   0,   0, 120,   0,
      9,   9,   9,   8,   9,   9,   9,   9,   9,  10,   9,   9,   9,   9,  10,  22,
      9,   9,   9,  55,   9,   9,   9,  55,   9,   9,   9,   9,   9,  17,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  57,   9,   9,   9,   9,  17,   0,   0,   0,
     77,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   8,   9,   9,   9,   9,
      9,   9,  10,   0,   9,   9,   9,   9,   9,   9,   9,   9,   9,  53,  39,   0,
      9,   0,   9,   9,   8,  55,   0,   0,   6,   6,  76,   0,   9,   9,   9,   9,
      9,   9,   9,   9,   9,   0,   9,   9,   9,   9,   0,   0,   9,   9,   9,   9,
      9,   0,   0,   0,   0,   0,   0,   0,   9,  55,  19,   9,   9,   9,   9,   9,
      9,   9,   9,   9,   9,  22,  17,  50,   9,   9,   9,   9,  10,  55,   0,   0,
     59,  30,   0,  18,   9,   8,   8,   9,   9,   9,   9,   9,   9,  55,  39,  61,
      9, 107,   0,   0,   0,   0,   0,   0,   9,   9,   9,   9,  10,   0,   0,   0,
      9,  18,   0,   0,   6,   6,  76,   0,   0,  68,   0,   0,   9,   9,   9,   9,
      9,  53,  18,  18,  77,   0,   0,   0,   9,   9,   9,   9,   9,   9,  18,  18,
     18,  39,   0,   0,   0,   0,   0,   0,   0,  64,   6,   6,   0,   0,   0,  61,
      9,   9,   9,   9,  18,  18,  39,  14,   0,   0,   0,  14,   9,   9,   9,   9,
      9,   9,  17,   0,   6,   6,  76,   0,   9,  41,  18,  18,  18, 121,   6,   6,
      0, 107,   0,   0,   9,   9,   9,   9,   9,   9,   9,   9,  41,  13,   0,   0,
     44,  17,  28,  77,   6,   6, 122,  17,   9,   9,   9,   9,  22,   9,   9,   9,
      9,   9,   9,  18,  18,  18,   0,  74,   9,  10,  19,  22,   9,   9,   9,  22,
      9,   9,   9,   9,   9,   9,   9,  41,  18,  18,  39,   0,   6,   6,  76,   0,
     18,   8,   9,  50,  50,   9,   9,   9,   9,   9,  19,   9,  19,   8,  23,  63,
     18,  65,  65,  60,  17,  61,   0,   8,  53,  71,  18,  77,  18,  77,   0,   0,
      9,   9,   9,   9,   9,  59,  18,  18,  18,  85,  10,   0,   6,   6,  76,  74,
     18,  22,   0,   0,   6,   6,  76,   0,   9,   9,   9,  41,  18,  60,  18,  18,
     77,   0,   0,   0,   0,   0,   9,  60,  77,  17,   0,   0,   6,   6,  76,   0,
      9,   9,  41,  18,  18,  18,   0,   0,   0,   0,   0,   0,   0,   0,   0,  28,
     18,  18,  18,   0,   6,   6,  76,   0,   9,   9,   9,  18,  18,  18,  39,   0,
      6,   6,  76,   0,   0,   0,   0,  68,  59,  18,  85,   9,   9,   9,   9,   9,
      9,   9,   9,   9,  41,  18,  58,  39,   0,  61,   0,   0,  59,  18,  18,   9,
      9,  16,  53,  18,  18,  18,  60,  72,   9,   9,  19,   9,   9,   9,   9,   9,
      9,   9,   9,  41,  18,  39,  18,  18,  17,   0,   0,   0,   6,   6,  76,   0,
      0,   0,   0,   0,  16,   9,   9,   9,   9,   9,   9,   9,  71,  18,  18,  18,
     18,  18,  28,  18,  18,  39,   0,   0,   9,  10,  22,   9,   9,   9,   9,   9,
      9,   9,   9,   9,  59,  39,  74,  29,  18,  58,   0,   0,   6,   6,  76,   0,
      9,  22,  19,   9,   9,   9,   9,   9,   9,   9,  53,  39,  29,  18,  17,   0,
      9,   9,   9,   9,  41,  39,   0,   0,   9,  10,   0,   0,   0,   0,   0,   0,
      9,   9,   9,  55,  18,  77,   0,   0,   9,   9,   9,   9,  18,  39,   0,   0,
      9,   0,   0,   0,   6,   6,  76,   0,  68,   9,   9,   9,   9,   9,   0,   8,
      9,  17,   0,   0,  59,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  39,
      0,   0,   0,  61,  85,   9,   9,   9,  55,   0,   0,   0,   0,   0,   0,   0,
    101,   0,   0,   0,   0,   0,   0,   0,   9,   9,  10,   0,   9,   9,   9,  17,
      9,   9,  17,   0,   9,   9,  55,  30,  36,   0,   0,   0,   0,   0,   0,   0,
      0,  28,  60,  28, 123,  36, 124,  18,  39,  28,  18,   0,   0,   0,   0,   0,
      0,   0,  71,  60,   0,   0,   0,   0,  71,  77,   0,   0,   0,   0,   0,   0,
      9,   9,   9,   9,   9,  19,   9,   9,   9,   9,   9,   9,   9,   9,   9,  19,
     13,  69,   8,  19,   9,   9,  22,   8,   9,   8,   9,   9,   9,   9,   9,   9,
      9,  22,  10,   8,   9,  19,   9,  19,   9,   9,   9,   9,   9,   9,  22,  10,
      9,  26,  16,   9,  19,   9,   9,   9,   9,  55,   9,   9,   9,   9,   9,   9,
     19,   9,   9,   9,   9,   9,  10,   9,  10,   9,   9,  64,   6,   6,   6,   6,
      6,   6,   6,   6,   6,   6,   6,   6,  18,  18,  18,  18,  18,  39,  61,  18,
     18,  18,  18,  77,   0,  57,   0,   0,   0,  77,   0,   0,   0,   0,  61,  18,
     28,  18,  18,  18,   0,   0,   0,   0,  18,  39,  18,  18,  18,  18,  65,  18,
     29,  48,  39,   0,   0,   0,   0,   0,   9,  17,   0,   0,  18,  39,   0,   0,
      9,  18,  39,   0,   6,   6,  76,   0,  69,  50,   8,   9,  10,   9,  25,   0,
     13,  68,  25,   8,  69,  50,  25,  25,  69,  50,  10,   9,  10,   9,   8,  26,
      9,   9,  22,   9,   9,   9,   9,   0,   8,   8,  22,   9,   9,   9,   9,   0,
      9,   9,  55,   0,   9,   9,   9,   9,   0, 125, 126, 126, 126, 126, 126, 126,
      0,   0,   0,   0,   0,   0,  61,  18,  14,   0,   0,   0,   0,   0,   0,   0,
     18,  18,  18,  18,   0,   0,   0,   0,
};

static RE_UINT8 re_word_break_stage_5[] = {
     0,  0,  0,  0,  0,  0,  5,  6,  6,  4,  0,  0, 18,  0,  1,  0,
     0,  0,  0,  2, 13,  0, 14,  0, 15, 15, 15, 15, 15, 15, 12, 13,
     0, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,  0,  0,  0,  0, 16,
     0,  6,  0,  0,  0,  0, 11,  0,  0,  9,  0,  0,  0, 11,  0, 12,
     0,  0, 11, 11, 11,  0,  0,  0,  7,  7,  7,  7, 11,  0, 11, 11,
    11, 11, 13, 11,  0,  0, 11, 12, 11, 11,  0, 11, 11, 11,  0,  7,
     7,  7, 11, 11,  0, 11,  0, 11, 11,  0, 11,  0, 11, 13,  0,  0,
     0,  7,  7,  7,  7,  7,  0,  7,  0,  7,  7,  0,  3,  3,  3,  3,
     3,  3,  3,  0,  0,  0,  0,  3,  3,  3,  3, 11, 12,  0,  0,  0,
     9,  9,  9,  9,  9,  9,  0,  0, 13, 13,  0,  0,  7,  7,  7,  0,
     9,  0,  0,  0, 11, 11, 11,  7, 15, 15,  0, 15, 13,  0, 11, 11,
     7, 11, 11, 11,  0, 11,  7,  7,  7,  9,  0,  7,  7, 11, 11,  7,
     7,  0,  7,  7, 15, 15, 11, 11, 11,  0,  0, 11,  0,  0,  0,  9,
    11,  7, 11, 11, 11, 11,  7,  7,  7, 11,  0,  0, 11, 11,  0,  0,
    13,  0, 11,  0,  0,  7,  0,  0,  7,  7, 11,  7, 11,  7,  7,  7,
     7,  7,  0,  0,  0,  0,  0,  7,  7,  7,  9,  7,  7, 11,  7,  7,
     0,  0, 15, 15,  7,  0,  0,  7,  7,  7, 11,  0, 11,  0,  7,  0,
     0,  0,  0, 11,  0, 11, 11,  0, 11,  7,  0,  0,  0,  0,  7,  7,
     0, 11,  0,  0,  0,  0,  7, 11,  0,  0,  7,  0,  7,  0,  7,  0,
    15, 15,  0,  0,  7,  0,  0,  0,  0,  7,  0,  7, 15, 15,  7,  7,
    18, 11, 11, 11, 11,  0,  7,  7,  7,  7,  9,  0, 11,  7,  7, 11,
    11,  7, 11,  0,  7,  7,  7, 11, 18, 18, 18, 18, 18, 18, 18,  0,
     7, 17,  9,  9, 14, 14,  0,  0, 14,  0,  0, 12,  6,  6,  9,  9,
     9,  9,  9, 16, 16,  0,  0,  0, 13,  0,  0,  0,  0,  0,  0, 18,
     9,  0,  9,  9, 18,  0,  0,  0,  0, 10, 10, 10, 10, 10,  0,  0,
     0,  7,  7, 10, 10,  0,  0,  0, 10, 10, 10, 10, 10, 10, 10,  0,
     7,  7,  0, 11, 11, 11,  7, 11,  0, 11, 11,  7, 11,  7,  7,  0,
     0,  3,  7,  3,  3,  0,  3,  3,  3,  0,  3,  0,  3,  3,  0,  3,
    13,  0,  0, 12,  0, 16, 16, 16, 13, 12,  0,  0, 11,  0,  0,  9,
     0,  0,  0, 14,  0,  0, 12, 13,  0,  0, 10, 10, 10, 10,  7,  7,
     0,  9,  9,  9,  7,  0, 15, 15, 15, 15, 11,  0,  7,  7,  7,  9,
     9,  9,  9,  7,  0,  0,  8,  8,  8,  8,  8,  8,
};

/* Word_Break: 5548 bytes. */

RE_UINT32 re_get_word_break(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 13;
    code = ch ^ (f << 13);
    pos = (RE_UINT32)re_word_break_stage_1[f] << 5;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_word_break_stage_2[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_word_break_stage_3[pos + f] << 3;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_word_break_stage_4[pos + f] << 2;
    value = re_word_break_stage_5[pos + code];

    return value;
}

/* Grapheme_Cluster_Break. */

static RE_UINT8 re_grapheme_cluster_break_stage_1[] = {
     0,  1,  2,  2,  2,  3,  4,  5,  6,  2,  2,  7,  2,  8,  9, 10,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
    11,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,
};

static RE_UINT8 re_grapheme_cluster_break_stage_2[] = {
     0,  1,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14,
    15, 16,  1, 17,  1,  1,  1, 18, 19, 20, 21, 22, 23, 24,  1,  1,
    25,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26, 27,  1,  1,
    28,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1, 29,  1, 30, 31, 32, 33, 34, 35, 36, 37,
    38, 39, 40, 34, 35, 36, 37, 38, 39, 40, 34, 35, 36, 37, 38, 39,
    40, 34, 35, 36, 37, 38, 39, 40, 34, 35, 36, 37, 38, 39, 40, 34,
    35, 36, 37, 38, 39, 40, 34, 41, 42, 42, 42, 42, 42, 42, 42, 42,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 43,  1,  1, 44, 45,
     1, 46, 47, 48,  1,  1,  1,  1,  1,  1, 49,  1,  1, 50,  1, 51,
    52, 53, 54, 55, 56, 57, 58, 59, 60,  1, 61,  1, 62, 63, 64,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 65, 66,  1,  1,  1, 67,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 68,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1, 69, 70,  1,  1,  1,  1,  1,  1,  1, 71,  1,  1,  1,  1,  1,
    72,  1,  1,  1,  1,  1,  1,  1, 73, 74,  1,  1,  1,  1,  1,  1,
     1, 75,  1, 76,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
    77, 78, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_grapheme_cluster_break_stage_3[] = {
      0,   1,   2,   2,   2,   2,   2,   3,   1,   1,   4,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      5,   5,   5,   5,   5,   5,   5,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   6,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   7,   5,   8,   9,   2,   2,   2,
     10,  11,   2,   2,  12,   5,   2,  13,   2,   2,   2,   2,   2,  14,  15,   2,
     16,  17,   2,   5,  18,   2,   2,   2,   2,   2,  19,  13,   2,   2,  12,  20,
      2,  21,  22,   2,   2,  23,   2,   2,   2,   2,   2,   2,   2,  24,  25,   5,
     26,   2,   2,  27,  28,  29,  30,   2,  31,   2,   2,  32,  33,  34,  30,  35,
     36,   2,   2,  37,  38,  17,   2,  39,  36,   2,   2,  37,  40,   2,  30,  41,
     31,   2,   2,  42,  33,  43,  30,   2,  44,   2,   2,  45,  46,  34,   2,   2,
     47,   2,   2,  48,  49,  50,  30,   2,  31,   2,   2,  51,  52,  50,  30,   2,
     53,   2,   2,  54,  55,  34,  30,   2,  56,   2,   2,   2,  57,  58,   2,  56,
      2,   2,   2,  59,  60,   2,   2,   2,   2,   2,   2,  61,  62,   2,   2,   2,
      2,  63,   2,  64,   2,   2,   2,  65,  66,  67,   5,  68,  69,   2,   2,   2,
      2,   2,  70,  71,   2,  72,  13,  73,  74,  75,   2,   2,   2,   2,   2,   2,
     76,  76,  76,  76,  76,  76,  77,  77,  77,  77,  78,  79,  79,  79,  79,  79,
      2,   2,   2,   2,   2,  70,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,  80,   2,  80,   2,  30,   2,  30,   2,   2,   2,  81,  82,  20,   2,   2,
     83,   2,   2,   2,   2,   2,   2,   2,  50,   2,  84,   2,   2,   2,   2,   2,
      2,   2,  85,  86,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,  87,   2,   2,   2,  88,  89,  90,   2,   2,   2,  91,   2,   2,   2,   2,
     92,   2,   2,  93,  94,   2,  12,  95,  96,   2,  97,   2,   2,   2,  98,  53,
      2,   2,  99, 100,   2,   2,   2,   2,   2,   2,   2,   2,   2, 101, 102, 103,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   5,   5,   5, 104,
    105,   2, 106,   2,   2,   2,   1,   2,   2,   2,   2,   2,   2,   5,   5,  13,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2, 107, 108,
      2,   2,   2,   2,   2,   2,   2, 107,   2,   2,   2,   2,   2,   2,   5,   5,
      2,   2,  41,   2,   2,   2,   2,   2,   2, 109,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2, 107, 110,   2,  48,   2,   2,   2,   2,   2, 108,
    111,   2, 112,   2,   2,   2,   2,   2, 113,   2,   2, 114, 115,   2,   5, 116,
      2,   2, 117,   2, 118,  53,  76, 119,  26,   2,   2, 120, 121,   2, 122,   2,
      2,   2, 123, 124, 125,   2,   2, 126,   2,   2,   2, 127,  17,   2, 128, 129,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2, 130,   2,
    131, 132, 133, 134, 133, 135, 133, 131, 132, 133, 134, 133, 135, 133, 131, 132,
    133, 134, 133, 135, 133, 131, 132, 133, 134, 133, 135, 133, 131, 132, 133, 134,
    133, 135, 133, 131, 132, 133, 134, 133, 135, 133, 131, 132, 133, 134, 133, 135,
    133, 131, 132, 133, 134, 133, 135, 133, 131, 132, 133, 134, 133, 135, 133, 131,
    132, 133, 134, 133, 135, 133, 131, 132, 133, 134, 133, 135, 133, 131, 132, 133,
    134, 133, 135, 133, 131, 132, 133, 134, 133, 135, 133, 131, 132, 133, 134, 133,
    135, 133, 131, 132, 133, 134, 133, 135, 133, 131, 132, 133, 134, 133, 135, 133,
    133, 134, 133, 135, 133, 131, 132, 133, 134, 133, 136,  77, 137,  79,  79, 138,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      2,  35,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      5,   2,   5,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   3,
      2,   2,   2,   2,   2,   2,   2,   2,   2,  48,   2,   2,   2,   2,   2, 139,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,  75,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,  13,   2,
      2,   2,   2,   2,   2,   2,   2, 140,   2,   2,   2,   2,   2,   2,   2,   2,
    141,   2,   2, 142,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,  50,   2,
      2,   2, 143,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,  19,  13,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
    144,   2,   2, 145, 146,   2,   2, 107,  96,   2,   2, 147, 148,   2,   2,   2,
    149,   2, 150, 151, 152,   2,   2, 153,  96,   2,   2, 154, 155,   2,   2,   2,
      2,   2, 156, 157,   2,   2,   2,   2,   2,   2,   2,   2,   2, 107, 158,   2,
     53,   2,   2,  54, 159,  34, 160, 151,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2, 161, 162,  35,   2,   2,   2,   2,   2, 163, 164,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2, 107, 165,  13, 166,   2,   2,
      2,   2,   2, 167,  13,   2,   2,   2,   2,   2, 168, 169,   2,   2,   2,   2,
      2,  70, 170,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2, 156, 171,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
    172,   2,   2, 173,  34, 174,   2,   2, 175, 176,   2,   2,   2,   2,   2,   2,
      2,   2, 177, 178,   2,   2,   2,   2,   2, 179, 180, 181,   2,   2,   2,   2,
      2,   2,   2, 182, 183,   2,   2,   2, 184, 185,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2, 186,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2, 151,
      2,   2,   2, 146,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2, 187, 188, 189, 107, 149,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2, 190, 191,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2, 192, 193, 194,   2, 195,   2,   2,   2,   2,   2,
      2,   2,   2,   2,  80,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      5,   5,   5, 196,   5,   5,  68, 122, 197,  12,   7,   2,   2,   2,   2,   2,
    198, 199, 200,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2, 146,   2,   2,
      2,   2,   2,   2, 201,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2, 202, 203,
      2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,  12,
      1,   1,   5,   5,   5,   5,   5,   5,   1,   1,   1,   1,   1,   1,   1,   1,
      5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   1,
};

static RE_UINT8 re_grapheme_cluster_break_stage_4[] = {
     0,  0,  1,  2,  0,  0,  0,  0,  3,  3,  3,  3,  3,  3,  3,  4,
     3,  3,  3,  5,  6,  6,  6,  6,  7,  6,  8,  3,  9,  6,  6,  6,
     6,  6,  6, 10, 11, 10,  3,  3, 12, 13,  3,  3,  6,  6, 14, 15,
     3,  3,  7,  6, 16,  3,  3,  3,  3, 17,  6, 18,  6, 19, 20,  8,
     3,  3,  3, 21, 22,  3,  3,  3,  6,  6, 14,  3,  3, 17,  6,  6,
     6,  3,  3, 22,  3, 17, 10,  6,  6,  9,  9,  8,  3,  3,  9,  3,
     7,  6,  6,  6, 23,  6,  6,  6, 24,  3,  3,  3,  3,  3, 25, 26,
    27,  6, 28, 29,  9,  6,  3,  3, 17,  3,  3,  3, 30,  3,  3,  3,
     3,  3,  3, 31, 27, 32, 33, 34,  3,  7,  3,  3,  3,  3,  3, 35,
    36,  3,  3,  3,  3,  3,  3, 26, 37,  7, 19,  8,  8, 22,  3,  3,
    27, 10, 38, 34,  3,  3, 17,  6,  3,  3,  3, 20,  3, 17,  3,  3,
    35,  3,  3,  3,  3,  3,  3, 25, 39, 40, 41, 34, 28, 16,  3,  3,
     3,  3,  3, 17, 28, 42, 20,  8,  3, 11,  3,  3,  3,  3,  3, 43,
    44, 45, 41,  8, 46,  3,  3,  3,  3,  3,  7, 31, 27, 26, 41, 47,
    40,  3,  3,  3,  3,  3, 35,  7, 48, 49, 50, 51, 52,  6, 14,  3,
     3,  7,  6, 14, 52,  6, 10, 16,  3,  3,  6,  8,  3,  3,  8,  3,
     3, 53, 22, 40,  9,  6,  6, 24,  6, 20,  3,  9,  6,  6,  9,  6,
     6,  6,  6, 16,  3, 35,  3,  3,  3,  3,  3,  9, 54,  6, 36, 37,
     3, 40,  8, 17,  9, 16,  3,  3, 35, 37,  3, 22,  3,  3,  3, 22,
    55, 55, 55, 55, 56, 56, 56, 56, 56, 56, 57, 57, 57, 57, 57, 57,
    17, 16,  3,  3,  3, 58,  6, 46, 50, 44, 27,  6,  3,  3,  7, 59,
     3,  3, 22,  3, 24, 51, 28,  3, 44, 50, 27,  3,  3,  7, 60,  3,
     3, 61,  6, 14, 49,  9,  6, 28, 51,  6,  6, 19,  6,  6,  6, 14,
     6, 62,  3,  3,  3, 54, 24, 28, 44, 62,  3,  3,  6,  3,  3,  3,
    63,  3,  3,  3, 64, 46, 58,  8,  3, 25, 46, 65,  3, 50, 50,  6,
     6, 48,  3,  3, 14,  6,  6,  6, 54,  6, 16, 22, 40, 32,  8,  3,
     6,  6, 10,  6,  3,  3,  4, 66,  3,  3,  0, 67,  3,  3,  3,  7,
     8,  3,  3,  3,  3,  3, 11,  3, 14,  6,  6,  8, 35, 35,  7,  3,
    68, 69,  3,  3, 70,  3,  3,  3,  3, 50, 50, 50, 50,  8,  3,  3,
     8,  3,  3,  7,  3, 17,  6,  8,  3,  7,  6,  6, 55, 55, 55, 71,
     7, 48, 46, 28, 62,  3,  3,  3,  3, 22,  3,  3,  3,  3,  9, 24,
    69, 37,  3,  3,  7,  3,  3, 72,  3,  3,  3, 16, 20, 19, 16, 17,
     3,  3, 68, 46,  3, 73,  3,  3, 68, 29, 39, 34, 74, 75, 75, 75,
    75, 75, 75, 74, 75, 75, 75, 75, 75, 75, 74, 75, 75, 74, 75, 75,
    75,  3,  3,  3, 56, 76, 77, 57, 57, 57, 57,  3,  0,  0,  0,  3,
     3, 17, 14,  3,  9, 11,  3,  6,  3,  3, 14,  7,  3,  6,  3,  3,
    78,  3,  3,  3,  3,  3,  6,  6,  6, 14,  3,  3, 51, 24, 37, 79,
     3,  3,  3, 79, 14,  3,  3,  3,  3,  7,  6, 27,  6, 16,  3,  3,
     3, 80,  3,  3,  7,  3,  3,  3, 68, 48,  6, 24, 81,  3,  9, 16,
     3,  3,  3, 51, 46, 54,  3, 35, 51,  6, 14,  3, 28, 33, 33, 70,
    40, 17,  6, 16,  3, 82,  6,  6, 48, 83,  3,  3, 60,  6, 84, 65,
    54,  3,  3,  3, 48,  8, 50, 58,  3,  3,  3,  8, 51,  6, 24, 65,
     3,  3,  7, 29,  6, 58,  3,  3, 48, 58,  6,  3,  6,  6, 37,  3,
     9,  6, 14,  3,  7,  6, 85, 14,  9, 24, 27,  3,  3, 86, 87,  6,
     6, 24,  8,  3,  3,  3,  3, 68,  6, 14,  6, 58, 17,  6,  6,  6,
     6,  6, 64,  6, 54, 37,  3,  3,  9, 14, 35, 10,  6, 23,  3,  3,
     3,  3, 40, 88, 89, 65,  3,  3,  7, 39,  3,  3, 82, 50, 50, 50,
    50, 50, 50, 50, 50, 50, 50, 88,  3,  3,  3, 11,  0,  3,  3,  3,
     3, 90,  8, 64, 91,  0, 92,  6, 14,  9,  6,  3,  3,  3, 17,  8,
     6, 14,  7,  6,  3, 16,  3,  3,  6, 14,  6,  6,  6,  6, 19,  6,
    10, 20, 14,  3,  3,  6, 14,  3,  3, 93, 94, 94, 94, 94, 94, 94,
};

static RE_UINT8 re_grapheme_cluster_break_stage_5[] = {
     4,  4,  4,  4,  4,  4,  3,  4,  4,  2,  4,  4,  0,  0,  0,  0,
     0,  0,  0,  4,  0,  4,  0,  0,  5,  5,  5,  5,  0,  0,  0,  5,
     5,  5,  0,  0,  0,  5,  5,  5,  5,  5,  0,  5,  0,  5,  5,  0,
     1,  1,  1,  1,  1,  1,  0,  0,  5,  5,  5,  0,  4,  0,  0,  0,
     5,  0,  0,  0,  0,  0,  5,  5,  5,  1,  0,  5,  5,  0,  0,  5,
     5,  0,  5,  5,  0,  0,  0,  1,  0,  5,  0,  0,  5,  5,  1,  5,
     5,  5,  5,  7,  0,  0,  5,  7,  5,  0,  7,  7,  7,  5,  5,  5,
     5,  7,  7,  7,  7,  5,  7,  7,  0,  5,  7,  7,  5,  0,  5,  7,
     5,  0,  0,  7,  7,  0,  0,  7,  7,  5,  0,  0,  0,  0,  5,  0,
     0,  5,  5,  7,  7,  5,  5,  0,  5,  7,  0,  7,  5,  7,  7,  0,
     0,  0,  7,  7,  7,  0,  7,  7,  7,  0,  5,  5,  5,  0,  7,  5,
     7,  7,  5,  7,  7,  0,  5,  7,  5,  5,  7,  7,  7,  5,  1,  0,
     7,  7,  5,  5,  5,  0,  5,  0,  7,  7,  7,  7,  7,  7,  7,  5,
     0,  5,  0,  7,  0,  5,  0,  5,  5,  7,  5,  5,  8,  8,  8,  8,
     9,  9,  9,  9, 10, 10, 10, 10,  5,  5,  7,  5,  5,  5,  4,  0,
     5,  7,  7,  5,  0,  7,  5,  7,  7,  0,  0,  0,  5,  5,  7,  0,
     0,  7,  5,  5,  7,  5,  7,  5,  5, 13,  4,  4,  4,  4,  4,  0,
     0,  0,  0,  7,  7,  5,  5,  7,  7,  7,  0,  0,  8,  0,  0,  0,
     5,  7,  0,  0,  0,  7,  5,  0, 11, 12, 12, 12, 12, 12, 12, 12,
     9,  9,  9,  0,  0,  0,  0, 10,  7,  5,  7,  0,  0,  1,  0,  0,
     0,  7,  7,  0,  7,  0,  1,  1,  0,  7,  7,  7,  5,  7,  5,  0,
     5,  7,  5,  7,  5,  7,  1,  5,  0,  0,  1,  1,  1,  1,  5,  5,
     7,  7,  7,  0,  5,  5,  0,  7,  0,  5,  7,  5,  5,  5,  5,  4,
     4,  4,  4,  5,  0,  0,  6,  6,  6,  6,  6,  6,
};

/* Grapheme_Cluster_Break: 2980 bytes. */

RE_UINT32 re_get_grapheme_cluster_break(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 13;
    code = ch ^ (f << 13);
    pos = (RE_UINT32)re_grapheme_cluster_break_stage_1[f] << 5;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_grapheme_cluster_break_stage_2[pos + f] << 4;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_grapheme_cluster_break_stage_3[pos + f] << 2;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_grapheme_cluster_break_stage_4[pos + f] << 2;
    value = re_grapheme_cluster_break_stage_5[pos + code];

    return value;
}

/* Sentence_Break. */

static RE_UINT8 re_sentence_break_stage_1[] = {
     0,  1,  2,  3,  4,  5,  5,  5,  5,  6,  7,  5,  5,  8,  9, 10,
    11, 12, 13, 14, 15,  9, 16,  5, 17,  9,  9, 18,  9, 19, 20, 21,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 22, 23, 24,  5, 25, 26,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
    27,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
};

static RE_UINT8 re_sentence_break_stage_2[] = {
      0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,
     16,  17,  18,  19,  20,  17,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,
     31,  32,  33,  34,  35,  33,  33,  36,  33,  37,  33,  33,  38,  39,  40,  33,
     41,  42,  33,  33,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,
     17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  43,  17,  17,
     17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,
     17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  44,
     17,  17,  17,  17,  45,  17,  46,  47,  48,  49,  50,  51,  17,  17,  17,  17,
     17,  17,  17,  17,  17,  17,  17,  52,  33,  33,  33,  33,  33,  33,  33,  33,
     33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,
     33,  33,  33,  33,  33,  33,  33,  33,  33,  17,  53,  54,  17,  55,  56,  57,
     58,  59,  60,  61,  62,  63,  17,  64,  65,  66,  67,  68,  69,  70,  33,  71,
     72,  73,  74,  75,  76,  77,  78,  79,  80,  33,  81,  33,  82,  83,  84,  33,
     17,  17,  17,  85,  86,  87,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,
     17,  17,  17,  17,  88,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,
     33,  33,  33,  33,  17,  17,  89,  33,  33,  33,  33,  33,  33,  33,  33,  33,
     33,  33,  33,  33,  33,  33,  33,  33,  17,  17,  90,  91,  33,  33,  92,  93,
     17,  17,  17,  17,  17,  17,  17,  94,  17,  17,  95,  33,  33,  33,  33,  33,
     17,  96,  97,  33,  33,  33,  33,  33,  33,  33,  33,  33,  98,  33,  33,  33,
     33,  99, 100,  33, 101, 102, 103, 104,  33,  33, 105,  33,  33,  33,  33,  33,
    106,  33,  33,  33,  33,  33,  33,  33, 107, 108,  33,  33,  33,  33, 109,  33,
     33, 110,  33,  33,  33,  33, 111,  33,  33,  33,  33,  33,  33,  33,  33,  33,
     17,  17,  17,  17,  17,  17, 112,  17,  17,  17,  17,  17,  17,  17,  17,  17,
     17,  17,  17,  17,  17,  17,  17, 113, 114,  17,  17,  17,  17,  17,  17,  17,
     17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17, 115,  17,
     17,  17,  17,  17,  17,  17,  17,  17,  17,  17,  17, 116,  33,  33,  33,  33,
     33,  33,  33,  33,  33,  33,  33,  33,  17,  17, 117,  33,  33,  33,  33,  33,
    118, 119,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,  33,
};

static RE_UINT16 re_sentence_break_stage_3[] = {
      0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,
      8,  16,  17,  18,  19,  20,  21,  22,  23,  23,  23,  24,  25,  26,  27,  28,
     29,  30,  18,   8,  31,   8,  32,   8,   8,  33,  34,  18,  35,  36,  37,  38,
     39,  40,  41,  42,  40,  40,  43,  44,  45,  46,  47,  40,  40,  48,  49,  50,
     51,  52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,
     67,  68,  69,  70,  71,  72,  73,  74,  75,  72,  76,  77,  78,  79,  80,  81,
     82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97,
     98,  99, 100,  55, 101, 102, 103,  55, 104, 105, 106, 107, 108, 109, 110,  55,
     40, 111, 112, 113, 114,  29, 115, 116,  40,  40,  40,  40,  40,  40,  40,  40,
     40,  40, 117,  40, 118, 119, 120,  40, 121,  40, 122, 123, 124,  29,  29, 125,
     98,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40, 126, 127,  40,  40, 128,
    129, 130, 131, 132,  40, 133, 134, 135, 136,  40,  40, 137, 138, 139,  40, 140,
    141, 142, 143, 144,  40, 145, 146,  55, 147,  40, 148, 149, 150, 151,  55,  55,
    152, 133, 153, 154, 155, 156,  40, 157,  40, 158, 159, 160, 161, 162, 163, 164,
     18,  18,  18,  18,  18,  18,  23, 165,   8,   8,   8,   8, 166,   8,   8,   8,
    167, 168, 169, 170, 168, 171, 172, 173, 174, 175, 176, 177, 178,  55, 179, 180,
    181, 182, 183,  30, 184,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,
    185, 186,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55,  55, 187,  30, 188,
     55,  55, 189, 190,  55,  55, 191, 192,  55,  55,  55,  55, 193,  55, 194, 195,
     29, 196, 197, 198,   8,   8,   8, 199,  18, 200,  40, 201, 202, 203, 203,  23,
    204, 205, 206,  55,  55,  55,  55,  55, 207, 208,  98,  40, 209,  98,  40, 210,
    211, 212,  40,  40, 213, 214,  55, 215,  40,  40,  40,  40,  40, 140,  55,  55,
     40,  40,  40,  40,  40,  40,  40, 124,  40,  40,  40,  40, 216,  55, 215, 217,
    218, 219,   8, 220, 221,  40,  40, 222, 223, 224,   8, 225, 226, 227,  55, 228,
    229, 230,  40, 231, 232, 133, 233, 234,  49, 235, 236, 237,  59, 238, 239, 240,
     40, 241, 242, 243,  40, 244, 245, 246, 247, 248, 249, 250,  18,  18,  40, 251,
     40,  40,  40,  40,  40, 252, 253, 254,  40,  40,  40, 255,  40,  40, 256,  55,
    257, 258, 259,  40,  40, 260, 261,  40,  40, 262, 215,  40, 263,  40, 264, 265,
    266, 267, 268, 269,  40,  40,  40, 270, 271,   2, 272, 273, 274, 141, 275, 276,
    277, 278, 279,  55,  40,  40,  40, 214,  55,  55,  40, 280,  55,  55,  55, 281,
     55,  55,  55,  55, 237,  40, 282, 283,  40, 284, 285, 286, 287,  40, 288,  55,
     29, 289, 290,  40, 287, 291, 292, 293,  40, 294,  40, 295,  55,  55,  55,  55,
     40, 202, 140, 264,  55,  55,  55,  55, 296, 297, 140, 202, 141,  55,  55, 298,
    140, 256,  55,  55,  40, 299,  55,  55, 300, 301, 302, 237, 237,  55, 106, 303,
     40, 140, 140, 304, 260,  55,  55,  55,  40,  40, 305,  55,  29, 306,  18, 307,
     40, 308,  55,  55,  55,  55,  55,  55, 237, 309, 310,  55,  55,  55,  55,  55,
    155, 311, 312, 313, 155, 314, 315, 316, 155, 317, 318, 319, 155, 238, 320,  55,
    321, 322,  55,  55, 323, 324, 325, 326, 327, 328, 329, 330,  55,  55,  55,  55,
     40, 331, 332,  55,  40,  46, 333,  55,  55,  55,  55,  55,  40, 334, 335,  55,
     40,  46, 336,  55,  40, 337, 135,  55, 122, 338,  55,  55,  55,  55,  55,  55,
     40, 339,  55,  55,  55,  29,  18, 340, 341, 342, 343,  40, 344,  55,  40, 137,
    345, 346, 347, 348, 349, 350,  55,  55, 351, 352, 353, 354, 355, 135,  55,  55,
     55,  55,  55,  55,  55,  55,  55, 356,  40,  40,  40,  40, 256,  55,  55,  55,
     40,  40,  40, 213,  40,  40,  40,  40,  40,  40, 295,  55,  55,  55,  55,  55,
     40, 213,  55,  55,  55,  55,  55,  55,  40,  40, 357,  55,  55,  55,  55,  55,
     40, 137, 141, 358,  55,  55, 215, 359,  40, 360, 361, 362, 124,  55,  55,  55,
     55,  55,  29,  18, 363,  55,  55,  55,  40,  40, 364, 365, 366,  55,  55, 367,
     40,  40,  40,  40,  40,  40,  40, 260,  40,  40,  40,  40,  40,  40,  40, 304,
    141,  55,  55, 215,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40, 254,
     40,  40,  40, 368, 369, 370,  55,  55,  55,  55,  55, 371, 372, 373,  55,  55,
     55,  55, 374,  55,  55,  55,  55,  55, 375, 376, 377, 378, 379, 380, 381, 382,
    383, 384, 385, 386, 387, 375, 376, 388, 378, 389, 390, 391, 382, 392, 393, 394,
    395, 396, 397, 196, 398, 399, 400, 401,  23, 402,  23, 403, 404, 405,  55,  55,
    406, 407,  55,  55,  55,  55,  55,  55,  40,  40,  40,  40,  40,  40, 408,  55,
     29, 409, 410,  55,  55,  55,  55,  55, 411, 412, 413, 414, 415, 416,  55,  55,
     55, 417, 418, 418, 419,  55,  55,  55,  55,  55,  55, 420,  55,  55,  55,  55,
     40,  40,  40,  40,  40,  40, 202,  55,  40, 280,  40,  40,  40,  40,  40,  40,
    287,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40, 421,  40,  40,
     40,  40,  40,  40,  40,  40,  40, 422, 287,  55,  55,  55,  55,  55,  55,  55,
    423,  23,  23,  23,  55,  55,  55,  55,  23,  23,  23,  23,  23,  23,  23, 424,
};

static RE_UINT8 re_sentence_break_stage_4[] = {
      0,   0,   1,   2,   0,   0,   0,   0,   3,   4,   5,   6,   7,   7,   8,   9,
     10,  11,  11,  11,  11,  11,  12,  13,  14,  15,  15,  15,  15,  15,  16,  13,
      0,  17,   0,   0,   0,   0,   0,   0,  18,   0,  19,  20,   0,  21,  19,   0,
     11,  11,  11,  11,  11,  22,  11,  23,  15,  15,  15,  15,  15,  24,  15,  15,
     25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  26,  26,
     26,  26,  27,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  28,  29,
     30,  31,  32,  33,  28,  31,  34,  28,  25,  31,  29,  31,  32,  26,  35,  34,
     36,  28,  31,  26,  26,  26,  26,  27,  25,  25,  25,  25,  30,  31,  25,  25,
     25,  25,  25,  25,  25,  15,  33,  30,  26,  23,  25,  25,  15,  15,  15,  15,
     15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  37,  15,  15,
     15,  15,  15,  15,  15,  15,  38,  36,  39,  40,  36,  36,  41,   0,   0,   0,
     15,  42,   0,  43,   0,   0,   0,   0,  44,  44,  44,  44,  44,  44,  44,  44,
     44,  44,  44,  44,  25,  45,  46,  47,   0,  48,  22,  49,  32,  11,  11,  11,
     50,  11,  11,  15,  15,  15,  15,  15,  15,  15,  15,  51,  33,  34,  25,  25,
     25,  25,  25,  25,  15,  52,  30,  32,  11,  11,  11,  11,  11,  11,  11,  11,
     11,  11,  11,  11,  15,  15,  15,  15,  53,  44,  54,  25,  25,  25,  25,  25,
     28,  26,  26,  29,  25,  25,  25,  25,  25,  25,  25,  25,  10,  11,  11,  11,
     11,  11,  11,  11,  11,  22,  55,  56,  15,  15,  57,   0,  58,  44,  44,  44,
     44,  44,  44,  44,  44,  44,  44,  59,  60,  59,   0,   0,  36,  36,  36,  36,
     36,  36,  61,  62,  36,   0,   0,   0,  63,  64,   0,  65,  44,  44,  66,  67,
     36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  68,  44,  44,  44,  44,  44,
      7,   7,  69,  70,  71,  36,  36,  36,  36,  36,  36,  36,  36,  72,  44,  73,
     44,  74,  75,  76,   7,   7,  77,  78,  79,   0,   0,  80,  81,  36,  36,  36,
     36,  36,  36,  36,  44,  44,  44,  44,  44,  44,  66,  82,  36,  36,  36,  36,
     36,  83,  44,  44,  84,   0,   0,   0,   7,   7,  77,  36,  36,  36,  36,  36,
     36,  36,  68,  44,  44,  41,  85,  86,  36,  36,  36,  36,  36,  83,  87,  44,
     44,  88,  88,  89,   0,   9,  90,  91,  36,  36,  36,  36,  36,  36,  88,   0,
     36,  36,  61,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     36,  36,  36,  36,  36,  92,  36,  41,   0,   0,   0,   0,  93,  44,  44,  44,
     94,  44,  44,  44,  44,  44,  44,  44,  44,  36,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  36,  83,  95,  44,  44,  44,  44,  88,  44,  36,  36,
     83,  96,   7,   7,  82,  36,  36,  36,  88,  82,  36,  78,  78,  36,  36,  36,
     36,  36,  92,  36,  43,  40,  41,  95,  44,  97,  97,  98,   0,  93,   0,  99,
     83, 100,   7,   7,  41,   0,   0, 101,  58,  82,  61,  62,  78,  36,  36,  36,
     36,  36,  92,  36,  92, 102,  41,  75,  66,  93,  97,  89,  86,   0,  82,  43,
      0, 100,   7,   7,  76, 103,   0,   0,  58,  82,  36,  99,  99,  36,  36,  36,
     36,  36,  92,  36,  92,  82,  41,  95,  44,  59,  59,  89, 104,   0,   0,   0,
     83, 100,   7,   7,   0,   0, 105,  44,  58,  82,  36,  78,  78,  36,  36,  36,
     44,  97,  97,  89,   0, 106,   0,  99,  83, 100,   7,   7,  55,   0,   0,   0,
    107,  82,  61,  40,  92,  41, 102,  92,  62, 104,  61,  40,  36,  36,  41, 106,
     66, 106,  75,  89, 104,  93,   0,   0,   0, 100,   7,   7,   0,   0,   0,   0,
     44,  71,  36,  92,  92,  36,  36,  36,  36,  36,  92,  36,  36,  36,  41, 105,
     44,  75,  75,  89,   0,  60,  61,   0,  83, 100,   7,   7,   0,   0,   0,   0,
     88,  82,  36,  92,  92,  36,  36,  36,  36,  36,  92,  36,  36,  82,  41,  95,
     44,  75,  75,  89,   0,  60,   0, 108,  83, 100,   7,   7, 102,   0,   0,   0,
     44,  82,  36,  92,  92,  36,  36,  36,  36,  36,  36,  36,  36,  36,  68,  95,
     44,  75,  75,  98,   0,  68,   0,  62,  83, 100,   7,   7,   0,   0,  40,  36,
    106,  82,  36,  36,  36,  61,  40,  36,  36,  36,  36,  36,  99,  36,  36,  55,
     36,  61, 109,  93,  44, 110,  44,  44,   0, 100,   7,   7, 106,   0,   0,   0,
     82,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  81,  44,  66,   0,
     36,  68,  44,  66,   7,   7, 111,   0, 102,  78,  43,  55,   0,  36,  82,  36,
     82, 112,  40,  82,  81,  44,  59,  84,  36,  43,  44,  89,   7,   7, 111,  36,
    104,   0,   0,   0,   0,   0,  89,   0,   7,   7, 111,   0,   0, 113, 114, 115,
     36,  36,  82,  36,  36,  36,  36,  36,  36,  36,  36, 104,  58,  44,  44,  44,
     44,  75,  36,  88,  44,  44,  58,  44,  44,  44,  44,  44,  44,  44,  44, 116,
      0, 109,   0,   0,   0,   0,   0,   0,  36,  36,  68,  44,  44,  44,  44, 117,
      7,   7, 118,   0,  36,  83,  76,  83,  95,  74,  44,  76,  88,  71,  36,  36,
     83,  44,  44,  87,   7,   7, 119,  89,  11,  50,   0, 120,  15,  15,  15,  15,
     15,  15,  15,  15,  15,  15,  24,  37,  36,  36,  92,  41,  36,  61,  92,  41,
     36,  36,  92,  41,  36,  36,  36,  36,  36,  36,  36,  36,  92,  41,  36,  61,
     92,  41,  36,  36,  36,  61,  36,  36,  36,  36,  36,  36,  92,  41,  36,  36,
     36,  36,  36,  36,  36,  36,  61,  58, 121,   9, 122,   0,   0,   0,   0,   0,
     36,  36,  36,  36,   0,   0,   0,   0,  11,  11,  11,  11,  11, 123,  15,  39,
     36,  36,  36, 124,  36,  36,  36,  36, 125,  36,  36,  36,  36,  36, 126, 127,
     36,  36,  61,  40,  36,  36, 104,   0,  36,  36,  36,  92,  83, 116,   0,   0,
     36,  36,  36,  36,  83, 128,   0,   0,  36,  36,  36,  36,  83,   0,   0,   0,
     36,  36,  36,  92, 129,   0,   0,   0,  36,  36,  36,  36,  36,  44,  44,  44,
     44,  44,  44,  44,  44,  62,   0, 103,   7,   7, 111,   0,   0,   0,   0,   0,
    130,   0, 131, 132,   7,   7, 111,   0,  36,  36,  36,  36,  36,  36, 104,   0,
     36, 133,  36,  36,  36,  36,  36,  36,  36,  36, 134,   0,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  41,   0,   0,  36,  36,  36,  36,  36,  36,  36,  61,
     44,  44,  44,   0,  44,  44,  44,   0,   0,  96,   7,   7,  36,  36,  36,  36,
     36,  36,  36,  41,  36, 104,   0,   0,  36,  36,  36,   0,  36,  36,  36,  36,
     36,  36,  41,   0,   7,   7, 111,   0,  36,  36,  36,  36,  36,  68,  44,   0,
     36,  36,  36,  36,  36,  88,  44,  66,  44,  44,  44,  44,  44,  44,  44,  97,
      7,   7, 111,   0,   7,   7, 111,   0,   0,  62, 135,   0,  44,  44,  44,  66,
     44,  71,  36,  36,  36,  36,  36,  36,  44,  71,  36,   0,   7,   7, 118, 136,
      0,   0,  93,  44,  44,   0,   0,   0, 117,  36,  36,  36,  36,  36,  36,  36,
     88,  44,  44,  76,   7,   7,  77,  36,  36,  83,  44,  44,  44,   0,   0,   0,
     36,  44,  44,  44,  44,  44,   9, 122,   7,   7, 111,  82,   7,   7,  77,  36,
     36,  36,  36,  36,  36,  36,  36, 137,  15,  15,  42,   0,  11,  11,  11,  11,
     11,  11,  11,  11,  11,  11,  22,  10,   0,   0,   0,   0,  66,  44,  44,  44,
     44,  44,  71,  81,  83,  74,  89,   0,  44,  44,  44,  44,  44,  44,  59,  44,
     25,  25,  25,  25,  25,  34,  15,  27,  15,  15,  11,  11,  15,  39,  11, 123,
     15,  15,  11,  11,  15,  15,  11,  11,  15,  39,  11, 123,  15,  15, 138, 138,
     15,  15,  11,  11,  15,  15,  15,  39,  15,  15,  11,  11,  15, 139,  11, 140,
     46, 139,  11, 141,  15,  46,  11,   0,  15,  15,  11, 141,  46, 139,  11, 141,
    142, 142, 143, 144, 145, 146, 147, 147,   0, 148, 149, 150,   0,   0, 151, 152,
      0, 153, 152,   0,   0,   0,   0, 154,  63, 155,  63,  63,  21,   0,   0, 156,
      0,   0,   0, 151,  15,  15,  15,  42,   0,   0,   0,   0,  44,  44,  44,  44,
     44,  44,  44,  44, 116,   0,   0,   0,  48, 157, 158, 159,  23, 120,  10, 123,
      0, 160,  49, 161,  11,  38, 162,  33,   0, 163,  39, 164,   0,   0,   0,   0,
    165,  38, 104,   0,   0,   0,   0,   0,   0,   0, 147,   0,   0,   0,   0,   0,
      0,   0, 151,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 166,  11,  11,
     15,  15,  39,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   4, 147,
    127,   0, 147, 147, 147,   5,   0,   0,   0, 151,   0,   0,   0,   0,   0,   0,
      0, 167, 147, 147,   0,   0,   0,   0,   4, 147, 147, 147, 147, 147, 127,   0,
      0,   0,   0,   0,   0,   0, 147,   0,   0,   0,   0,   0,   0,   0,   0,   5,
     11,  11,  11,  22,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  24,
     31, 168,  26,  32,  25,  29,  15,  33,  25,  42, 157, 169,  54,   0,   0,   0,
     15, 170,   0,  21,  36,  36,  36,  36,  36,  36,   0,  62,   0,   0,   0,  93,
     36,  36,  36,  36,  36,  61,   0,   0,  36,  61,  36,  61,  36,  61,  36,  61,
    147, 147, 147,   5,   0,   0,   0,   5, 147, 147,   5, 171,   0,   0,   0, 122,
    172,   0,   0,   0,   0,   0,   0,   0, 173,  82, 147, 147,   5, 147, 147, 174,
     82,  36,  83,  44,  82,  41,  36, 104,  36,  36,  36,  36,  36,  61,  60,  82,
     36,  36,  36,  36,  36,  36,  61,  36,   0,  82,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  82,  36,  36,  36,  36,  36,  36,  61,   0,   0,   0,   0,
     36,  36,  36,  36,  36,  36,  61,   0,   0,   0,   0,   0,  36,  36,  36,  36,
     36,  36,  36, 104,   0,   0,   0,   0,  36,  36,  36,  36,  36,  36,  36, 175,
     36,  36,  36, 176,  36,  36,  36,  36,   7,   7,  77,   0,   0,   0,   0,   0,
     25,  25,  25, 177,  66,  44,  44, 178,  25,  25,  25,  25,  25,  25,  25, 179,
     36,  36,  36,  36, 180,   9,   0,   0,   0,   0,   0,   0,   0,  62,  36,  36,
    181,  25,  25,  25,  27,  25,  25,  25,  25,  25,  25,  25,  15,  15,  26,  30,
     25,  25, 182, 183,  25,  27,  25,  25,  25,  25,  31,  23,  11,  25, 184,   0,
      0,   0,   0,   0,   0,  62, 185,  36, 186, 186,  68,  36,  36,  36,  36,  36,
     68,  44,   0,   0,   0,   0,   0,   0,  36,  36,  36,  36,  36, 136,   0,   0,
     76,  36,  36,  36,  36,  36,  36,  36,  44,  89,   0, 136,   7,   7, 111,   0,
     44,  44,  44,  44,  76,  36,  62, 187,  36,  83,  44, 180,  36,  36,  36,  36,
     36,  68,  44,  44,  44,   0,   0,   0,  36,  36,  36,  36,  36,  36,  36, 104,
     36,  36,  36,  36,  68,  44,  44,  44, 116,   0, 152,  62,   7,   7, 111,   0,
     36,  81,  36,  36,   7,   7,  77,  61,  36,  36,  88,  44,  44,  66,   0,   0,
     68,  36,  36,  89,   7,   7, 111, 188,  36,  36,  36,  36,  36,  61, 189,  76,
     36,  36,  36,  36,  95,  74,  71,  83, 134,   0,   0,   0,   0,   0,  62,  41,
     36,  36,  68,  44, 190, 191,   0,   0,  82,  61,  82,  61,  82,  61,   0,   0,
     36,  61,  36,  61,  15,  15,  15,  15,  15,  15,  15,  15,  15,  15,  24,  15,
     15,  39,   0,   0,  15,  15,  15,  15,  68,  44, 192,  89,   7,   7, 111,   0,
     36,   0,   0,   0,  36,  36,  36,  36,  36,  61,  62,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  36,  36,   0,  36,  36,  36,  41,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  36,  41,   0,  15,  24,   0,   0, 193,  15,   0, 194,
     36,  36,  92,  36,  36,  61,  36,  43,  99,  92,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  41,   0,   0,   0,   0,   0,   0,   0,  62,  36,  36,  36,
     36,  36,  36,  36,  36,  36,  36, 195,  36,  36,  36,  36,  40,  36,  36,  36,
     36,  36,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  36,  36,  36,   0,
     44,  44,  44,  44, 196,   4, 127,   0,  44,  44,  44,  44, 197, 174, 147, 147,
    147, 198, 127,   0,   6, 199, 200, 201, 145,   0,   0,   0,  36,  92,  36,  36,
     36,  36,  36,  36,  36,  36,  36, 202,  90,   0,   5,   6,   0,   0, 203,   9,
     14,  15,  15,  15,  15,  15,  16, 204, 205, 206,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  36,  36,  83,  40,  36,  40,  36,  40,  36,  40, 104,
      0,   0,   0,   0,   0,   0, 207,   0,  36,  36,  36,  82,  36,  36,  36,  36,
     36,  61,  36,  36,  36,  36,  61,  99,  36,  36,  36,  41,  36,  36,  36,  41,
     36,  36,  36,  36,  36, 104,   0,   0,   0,   0,   0,   0,   0,   0,   0,  86,
     36,  36,  36,  36, 104,   0,   0,   0, 116,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,  82,  36,  36,  36,  36,  36,  36,  61,   0,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  83,  66,   0,  36,  36,  36,  36,  36,  36,  36,  41,
     36,   0,  36,  36,  82,  41,   0,   0,  11,  11,  15,  15,  15,  15,  15,  15,
     15,  15,  15,  15,  36,  36,  36,  36,   7,   7, 111,   0,  11,  11,  11,  11,
     11,  11,  11,  11,  11,   0,  15,  15,  15,  15,  15,  15,  15,  15,  15,   0,
     36,  36,   0,   0,  36,  36,  36,  36,  36,   0,   0,   0,   0,   0,   0,   0,
     36,  41,  92,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  99, 104,  78,
     36,  36,  36,  36,  61,  41,   0,   0,  36,  36,  36,  36,  36,  36,   0,  40,
     88,  60,   0,  44,  36,  82,  82,  36,  36,  36,  36,  36,  36,  41,  66,  93,
      0,   0,   0,   0,   0, 136,   0,   0,  36, 191,   0,   0,   0,   0,   0,   0,
     36,  36,  36,  36,  61,   0,   0,   0,  36,  36, 104,   0,   0,   0,   0,   0,
     11,  11,  11,  11,  22,   0,   0,   0,  15,  15,  15,  15,  24,   0,   0,   0,
     36,  44,   0,   0,   7,   7, 111,   0,   0,  62,   0,   0,  36,  36,  36,  36,
     36,  83,  44,  44, 116, 188, 152,   0,  36,  36,  36,  36,  36,  36,  44,  44,
     44, 192, 122,   0,   0,   0,   0,   0,   0, 100,   7,   7,   0,   0,   0,  93,
     36,  36,  36,  36,  44,  44,  66, 208, 152,   0,   0,  20,  36,  36,  36,  36,
     36,  36, 104,   0,   7,   7, 111,   0,  36,  68,  44,  44,  44, 209,   7,   7,
    188, 191,   0,   0,  36,  36,  36,  36,  36,  36,  36,  36,  68, 108,   0,   0,
     71, 210,  58, 211,   7,   7, 212, 176,  36,  36,  36,  36,  99,  36,  36,  36,
     36,  36,  36,  44,  44,  44, 213, 214,  36,  61,  92,  99,  36,  36,  36,  99,
     36,  36, 215,   0,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  68,
     44,  44,  66,   0,   7,   7, 111,   0,  44,  82,  36,  78,  78,  36,  36,  36,
     36,  36,  92,  36,  92,  82, 216,  95,  44,  97,  97,  89, 104,  93,   0,  82,
     83, 106,  44, 116,  44, 116,   0,   0,  36,  36,  36,  36,  36,  88,  44,  44,
     44, 117, 217, 122,   7,   7, 111, 109,  44,  99,   0,   0,   7,   7, 111,   0,
     36,  36,  36,  68,  44,  89,  44,  44, 218,   0, 188, 135, 135, 135,  36,  89,
    128, 104,   0,   0,   7,   7, 111,   0,  36,  36,  68,  44,  44,  44,   0,   0,
     44,  44,  44,   0,   7,   7, 111,  79,  36,  36,  36,  44,  44,  44,  66,   0,
      7,   7, 111,   0,   0,   0,   0,  62,  88,  44, 117,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  68,  44,  87,  66, 136,  93,   0,   0,  88,  44,  44,  36,
     36,  40,  83,  44,  44,  44, 180, 219,  36,  36,  92,  36,  36,  36,  36,  36,
     36,  36,  36,  68,  44,  66,  44,  44, 210,   0,   0,   0,   7,   7, 111,   0,
      0,   0,   0,   0,  40,  36,  36,  36,  36,  36,  36,  36, 106,  44,  44,  44,
     44,  44,  58,  44,  44,  66,   0,   0,  36,  61,  99,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  88,  66, 109,  59,  44,  87,   0,   0,   7,   7, 111,   0,
     36,  99,  92,  36,  36,  36,  36,  36,  36,  36,  83,  66,  59,  44, 104,   0,
     36,  36,  36,  36,  68, 192, 122,   0,  36,  61,   0,   0,   0,   0,   0,   0,
      7,   7, 111, 136,   0,   0,   0,   0,  36,  36,  36,  41,  44, 211,   0,   0,
     36,  36,  36,  36,  44, 192, 122,   0,  36, 122,   0,   0,   7,   7, 111,   0,
     62,  36,  36,  36,  36,  36,   0,  82,   0,   0,   0,   0,   0,   0, 122,   0,
     36, 104,   0,   0,  88,  44,  44,  44,  44,  44,  44,  44,  44,  44,  44,  66,
      0,   0,   0,  93, 117,  36,  36,  36,  41,   0,   0,   0,   0,   0,   0,   0,
     36,  36,  61,   0,  36,  36,  36, 104,  36,  36, 104,   0,  36,  36,  41, 220,
     63,   0,   0,   0,   0,   0,   0,   0,   0,  58,  89,  58, 221,  63, 222,  44,
     66,  58,  44,   0,   0,   0,   0,   0,   0,   0, 106,  89,   0,   0,   0,   0,
    106, 116,   0,   0,   0,   0,   0,   0,  11,  11,  11,  11,  11,  11, 159,  15,
     15,  15,  15,  15,  15,  11,  11,  11,  11,  11,  11, 159,  15, 139,  15,  15,
     15,  15,  11,  11,  11,  11,  11,  11, 159,  15,  15,  15,  15,  15,  15,  49,
     48, 223,  10,  49,  11, 159, 170,  14,  15,  14,  15,  15,  11,  11,  11,  11,
     11,  11, 159,  15,  15,  15,  15,  15,  15,  50,  22,  10,  11,  49,  11, 224,
     15,  15,  15,  15,  15,  15,  50,  22,  11, 160, 166,  11, 224,  15,  15,  15,
     15,  15,  15,  11,  11,  11,  11,  11,  11, 159,  15,  15,  15,  15,  15,  15,
     11,  11,  11, 159,  15,  15,  15,  15, 159,  15,  15,  15,  15,  15,  15,  11,
     11,  11,  11,  11,  11, 159,  15,  15,  15,  15,  15,  15,  11,  11,  11,  11,
     15,  39,  11,  11,  11,  11,  11,  11, 224,  15,  15,  15,  15,  15,  24,  15,
     33,  11,  11,  11,  11,  11,  22,  15,  15,  15,  15,  15,  15, 139,  15,  11,
     11,  11,  11,  11,  11, 224,  15,  15,  15,  15,  15,  24,  15,  33,  11,  11,
     15,  15, 139,  15,  11,  11,  11,  11,  11,  11, 224,  15,  15,  15,  15,  15,
     24,  15,  27, 100,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
     44,  44,  44,  44,  44,  66,  93,  44,  44,  44,  44, 116,   0,  86,   0,   0,
      0, 116, 122,   0,   0,   0,  93,  44,  58,  44,  44,  44,   0,   0,   0,   0,
     44,  66,  44,  44,  44,  44,  97,  44,  59,  75,  66,   0,   0,   0,   0,   0,
     36, 104,   0,   0,  44,  66,   0,   0, 159,  15,  15,  15,  15,  15,  15,  15,
     15,  44,  66,   0,   7,   7, 111,   0,  36,  82,  36,  36,  36,  36,  36,  36,
    102,  78,  82,  36,  61,  36, 112,   0, 108,  62, 112,  82, 102,  78, 112, 112,
    102,  78,  61,  36,  61,  36,  82,  43,  36,  36,  99,  36,  36,  36,  36,   0,
     82,  82,  99,  36,  36,  36,  36,   0,   0,   0,   0,   0,  11,  11,  11,  11,
     11,  11, 123,   0,  11,  11,  11,  11,  11,  11, 123,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0, 167, 127,   0,  41,   0,   0,   0,  36,  36,  36,  36,
    104,   0,   0,   0,   0,   0,   0,   0,  20,   0,   0,   0,   0,   0,   0,   0,
     44,  44,  44,  44,   0,   0,   0,   0,
};

static RE_UINT8 re_sentence_break_stage_5[] = {
     0,  0,  0,  0,  0,  6,  2,  6,  6,  1,  0,  0,  6, 12, 13,  0,
     0,  0,  0, 13, 13, 13,  0,  0, 14, 14, 11,  0, 10, 10, 10, 10,
    10, 10, 14,  0,  0,  0,  0, 12,  0,  8,  8,  8,  8,  8,  8,  8,
     8,  8,  8, 13,  0, 13,  0,  0,  0,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7, 13,  0,  4,  0,  0,  6,  0,  0,  0,  0,  0,  7, 13,
     0,  5,  0,  0,  0,  7,  0,  0,  8,  8,  8,  0,  8,  8,  8,  7,
     7,  7,  7,  0,  8,  7,  8,  7,  7,  8,  7,  8,  7,  7,  8,  7,
     8,  8,  7,  8,  7,  8,  7,  7,  7,  8,  8,  7,  8,  7,  8,  8,
     7,  8,  8,  8,  7,  7,  8,  8,  8,  7,  7,  7,  8,  7,  7,  9,
     9,  9,  9,  9,  9,  7,  7,  7,  7,  9,  9,  9,  7,  7,  0,  0,
     0,  0,  9,  9,  9,  9,  0,  0,  7,  0,  0,  0,  9,  0,  9,  0,
     3,  3,  3,  3,  9,  0,  8,  7,  0,  0,  7,  7,  7,  7,  0,  8,
     0,  0,  8,  0,  8,  0,  8,  8,  8,  8,  0,  8,  7,  7,  7,  8,
     8,  7,  0,  8,  8,  7,  0,  3,  3,  3,  8,  7,  0,  9,  0,  0,
     0, 14,  0,  0,  7, 12,  0,  0,  0,  3,  3,  3,  3,  3,  0,  3,
     0,  3,  3,  0,  9,  9,  9,  0,  0,  0,  0,  9,  5,  5,  5,  5,
     5,  5,  0,  0, 14, 14,  0,  0,  3,  3,  3,  0,  5,  0, 12, 12,
     9,  9,  9,  3, 10, 10,  0, 10, 10,  0,  9,  9,  3,  9,  9,  9,
    12,  9,  3,  3,  3,  5,  0,  3,  3,  9,  9,  3,  3,  0,  3,  3,
     3,  3,  9,  9, 10, 10,  9,  9,  9,  0,  0,  9, 12, 12, 12,  0,
     0,  0,  0,  5,  9,  3,  9,  9,  0,  9,  9,  9,  9,  9,  3,  3,
     3,  9,  0,  0, 14, 12,  9,  0,  0,  3,  0,  0,  3,  3,  9,  3,
     9,  3,  3,  3,  3,  3,  0,  0,  0, 12,  0,  0,  0, 12, 12,  0,
     9,  0,  9,  9,  0,  0,  0,  3,  3,  3,  5,  3,  3,  9,  3,  3,
    12, 12, 10, 10,  3,  0,  0,  3,  3,  3,  9,  0,  9,  9,  0,  9,
     0,  0, 10, 10,  9,  0,  3,  0,  0,  9,  9,  0,  9,  3,  0,  0,
     9,  0,  0,  0,  0,  9,  3,  3,  0,  0,  3,  3,  0,  0,  3,  9,
     0,  0,  9,  0,  0,  0,  3,  0,  3,  0,  3,  0, 10, 10,  0,  0,
     0,  9,  0,  9,  0,  3,  0,  3,  0,  3, 13, 13, 13, 13,  3,  3,
     3,  0,  0,  0,  3,  3,  3,  9, 10, 10, 12, 12, 10, 10,  3,  3,
     0,  8,  0,  0,  0,  0, 12,  0, 12,  0,  0,  0,  8,  8,  0,  0,
     9,  0, 12,  9,  6,  9,  9,  9,  9,  9,  9, 13, 13,  0,  0,  0,
     3, 12, 12,  0,  9,  0,  3,  3,  0,  0, 14, 12, 14, 12,  0,  3,
     3,  3,  5,  0,  9,  3,  3,  9,  9,  3,  9,  0, 12, 12, 12, 12,
     0,  0, 12, 12,  9,  9, 12, 12,  0,  8,  0,  8,  7,  0,  7,  7,
     8,  0,  7,  0,  8,  0,  0,  0,  6,  6,  6,  6,  6,  6,  6,  5,
     3,  3,  5,  5,  0,  0,  0, 14, 14,  0,  0,  0, 13, 13, 13, 13,
    11,  0,  0,  0,  4,  4,  5,  5,  5,  5,  5,  6,  0, 13, 13,  0,
    12, 12,  0,  0,  0, 13, 13, 12,  0,  0,  0,  6,  5,  0,  5,  5,
     0, 13, 13,  7,  0,  0,  0,  8,  0,  0,  7,  8,  8,  8,  7,  7,
     8,  0,  8,  0,  8,  8,  0,  7,  9,  7,  0,  0,  0,  8,  7,  7,
     0,  0,  7,  0,  9,  9,  9,  8,  0,  0,  8,  8,  0,  0, 13, 13,
     8,  7,  7,  8,  7,  8,  7,  3,  7,  7,  0,  7,  0,  0, 12,  9,
     0,  0, 13,  0,  6, 14, 12,  0,  0, 13, 13, 13,  9,  9,  0, 12,
     9,  0, 12, 12,  8,  7,  9,  3,  3,  3,  0,  9,  7,  7,  3,  3,
     3,  3,  0, 12,  0,  0,  8,  7,  9,  0,  0,  8,  7,  8,  7,  9,
     8,  7,  0,  0,  7,  7,  7,  9,  9,  9,  3,  9,  0,  9,  9,  3,
     0, 12, 12, 12,  0,  0,  9,  3, 12, 12,  9,  9,  9,  3,  3,  0,
     3,  3,  3, 12,  0,  0,  0,  7,  0,  9,  3,  9,  9,  9, 13, 13,
    14, 14,  0, 14,  0, 14, 14,  0, 13,  0,  0, 13,  0, 14, 12, 12,
    14, 13, 13, 13, 13, 13, 13,  0,  9,  0,  0,  5,  0,  0, 14,  0,
     0, 13,  0, 13, 13, 12, 13, 13, 14,  0,  9,  9,  0,  5,  5,  5,
     0,  5, 12, 12,  3,  0, 10, 10,  9, 12, 12,  0,  3, 12,  0,  0,
    10, 10,  9,  0, 12, 12,  0, 12, 12,  0,  3,  0,  9, 12,  0,  0,
     9,  9,  0,  3,  9,  9,  9, 12,  3,  0, 12, 12, 12,  9,  0,  0,
     0,  3,  3, 12,  3,  3,  3,  5,  5,  5,  5,  3,  0,  8,  8,  0,
     8,  0,  7,  7,
};

/* Sentence_Break: 6940 bytes. */

RE_UINT32 re_get_sentence_break(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 12;
    code = ch ^ (f << 12);
    pos = (RE_UINT32)re_sentence_break_stage_1[f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_sentence_break_stage_2[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_sentence_break_stage_3[pos + f] << 3;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_sentence_break_stage_4[pos + f] << 2;
    value = re_sentence_break_stage_5[pos + code];

    return value;
}

/* Math. */

static RE_UINT8 re_math_stage_1[] = {
    0, 1, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2,
};

static RE_UINT8 re_math_stage_2[] = {
    0, 1, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 6, 1, 1,
};

static RE_UINT8 re_math_stage_3[] = {
     0,  1,  1,  2,  1,  1,  3,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     4,  5,  6,  7,  1,  8,  9, 10,  1,  6,  6, 11,  1,  1,  1,  1,
     1,  1,  1, 12,  1,  1, 13, 14,  1,  1,  1,  1, 15, 16, 17, 18,
     1,  1,  1,  1,  1,  1, 19,  1,
};

static RE_UINT8 re_math_stage_4[] = {
     0,  1,  2,  3,  0,  4,  5,  5,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  6,  7,  8,  0,  0,  0,  0,  0,  0,  0,
     9, 10, 11, 12, 13,  0, 14, 15, 16, 17, 18,  0, 19, 20, 21, 22,
    23, 23, 23, 23, 23, 23, 23, 23, 24, 25,  0, 26, 27, 28, 29, 30,
     0,  0,  0,  0,  0, 31, 32, 33, 34,  0, 35, 36,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 23, 23,  0, 19, 37,  0,  0,  0,  0,  0,
     0, 38,  0,  0,  0,  0,  0,  0,  0,  0,  0, 39,  0,  0,  0,  0,
     1,  3,  3,  0,  0,  0,  0, 40, 23, 23, 41, 23, 42, 43, 44, 23,
    45, 46, 47, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 48, 23, 23,
    23, 23, 23, 23, 23, 23, 49, 23, 44, 50, 51, 52, 53, 54,  0, 55,
};

static RE_UINT8 re_math_stage_5[] = {
      0,   0,   0,   0,   0,   8,   0, 112,   0,   0,   0,  64,   0,   0,   0,  80,
      0,  16,   2,   0,   0,   0, 128,   0,   0,   0,  39,   0,   0,   0, 115,   0,
    192,   1,   0,   0,   0,   0,  64,   0,   0,   0,  28,   0,  17,   0,   4,   0,
     30,   0,   0, 124,   0, 124,   0,   0,   0,   0, 255,  31,  98, 248,   0,   0,
    132, 252,  47,  63,  16, 179, 251, 241, 255,  11,   0,   0,   0,   0, 255, 255,
    255, 126, 195, 240, 255, 255, 255,  47,  48,   0, 240, 255, 255, 255, 255, 255,
      0,  15,   0,   0,   3,   0,   0,   0,   0,   0,   0,  16,   0,   0,   0, 248,
    255, 255, 191,   0,   0,   0,   1, 240,   7,   0,   0,   0,   3, 192, 255, 240,
    195, 140,  15,   0, 148,  31,   0, 255,  96,   0,   0,   0,   5,   0,   0,   0,
     15, 224,   0,   0, 159,  31,   0,   0,   0,   2,   0,   0, 126,   1,   0,   0,
      4,  30,   0,   0, 255, 255, 223, 255, 255, 255, 255, 223, 100, 222, 255, 235,
    239, 255, 255, 255, 191, 231, 223, 223, 255, 255, 255, 123,  95, 252, 253, 255,
     63, 255, 255, 255, 255, 207, 255, 255, 150, 254, 247,  10, 132, 234, 150, 170,
    150, 247, 247,  94, 255, 251, 255,  15, 238, 251, 255,  15,   0,   0,   3,   0,
};

/* Math: 538 bytes. */

RE_UINT32 re_get_math(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_math_stage_1[f] << 4;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_math_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_math_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_math_stage_4[pos + f] << 5;
    pos += code;
    value = (re_math_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Alphabetic. */

static RE_UINT8 re_alphabetic_stage_1[] = {
    0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3,
};

static RE_UINT8 re_alphabetic_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  9, 10, 11,  7,  7,  7,  7, 12, 13, 13, 13, 13, 14,
    15, 16, 17, 18, 19, 13, 20, 13, 21, 13, 13, 13, 13, 22,  7,  7,
    23, 24, 13, 13, 13, 13, 25, 26, 13, 13, 27, 13, 28, 29, 30, 13,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7, 31,  7, 32, 33,  7, 34,  7,  7,  7, 35, 13, 36,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
};

static RE_UINT8 re_alphabetic_stage_3[] = {
      0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,
     16,   1,  17,  18,  19,   1,  20,  21,  22,  23,  24,  25,  26,  27,   1,  28,
     29,  30,  31,  31,  32,  31,  31,  31,  31,  31,  31,  31,  33,  34,  35,  31,
     36,  37,  31,  31,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,  38,   1,   1,   1,   1,   1,   1,   1,   1,   1,  39,
      1,   1,   1,   1,  40,   1,  41,  42,  43,  44,  45,  46,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,  47,  31,  31,  31,  31,  31,  31,  31,  31,
     31,   1,  48,  49,   1,  50,  51,  52,  53,  54,  55,  56,  57,  58,   1,  59,
     60,  61,  62,  63,  64,  65,  31,  66,  67,  68,  69,  70,  71,  72,  73,  74,
     75,  31,  76,  31,  77,  78,  79,  31,   1,   1,   1,  80,  81,  82,  31,  31,
      1,   1,   1,   1,  83,  31,  31,  31,  31,  31,  31,  31,   1,   1,  84,  31,
      1,   1,  85,  86,  31,  31,  87,  88,   1,   1,   1,   1,   1,   1,   1,  89,
      1,   1,  90,  31,  31,  31,  31,  31,   1,  91,  92,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  93,  31,  31,  31,  31,  31,  31,  31,  94,  95,  96,  97,
     98,  31,  31,  31,  31,  31,  31,  31,  99, 100,  31,  31,  31,  31, 101,  31,
     31, 102,  31,  31,  31,  31,  31,  31,   1,   1,   1,   1,   1,   1, 103,   1,
      1,   1,   1,   1,   1,   1,   1, 104, 105,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1, 106,   1,   1,   1,   1, 107,  31,  31,  31,  31,
      1,   1, 108,  31,  31,  31,  31,  31,
};

static RE_UINT8 re_alphabetic_stage_4[] = {
      0,   0,   1,   1,   0,   2,   3,   3,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   5,   6,   0,   0,   7,   8,   9,  10,   4,  11,
      4,   4,   4,   4,  12,   4,   4,   4,   4,  13,  14,   4,  15,  16,  17,  18,
     19,   4,  20,  21,   4,   4,  22,  23,  24,   4,  25,   4,   4,  26,  27,  28,
     29,  30,  31,  32,   0,  33,  34,  35,   4,  36,  37,  38,  39,  40,  41,  42,
     43,  44,  45,  46,  47,  48,  49,  50,  51,  48,  52,  53,  54,  55,  56,   0,
     57,  58,  59,  60,  57,  61,  62,  63,  57,  64,  65,  66,  67,  68,  69,  70,
     71,  72,  73,   0,  74,  75,  76,   0,  77,   0,  78,  79,  80,  81,   0,   0,
      4,  82,  24,  83,  84,   4,  85,  86,   4,   4,  87,   4,  88,  89,  90,   4,
     91,   4,  92,   0,  93,   4,   4,  94,  71,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,  95,   1,   4,   4,  96,  97,  98,  98,  99,   4, 100, 101,   0,
      0,   4,   4,  31,   4, 102,   4, 103, 104, 105,  24, 106,   4, 107, 108,   0,
    109,   4, 104, 110,   0, 111,   0,   0,   4, 112, 113,   0,   4, 114,   4, 115,
      4, 103, 116, 117, 118,  64,   0, 119,   4,   4,   4,   4,   4,   4,   0, 120,
     94,   4, 121, 117,   4, 122, 123, 124,   0,   0,   0, 125, 126,   0,   0,   0,
    127, 128, 129,   4,  15,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0, 130,   4, 108,   4, 131, 104,   4,   4,   4,   4, 132,
      4,  85,   4, 133, 134, 135, 135,   4,   0, 136,   0,   0,   0,   0,   0,   0,
    137, 138,  71,   4, 139,  71,   4,  86, 140,  13,   4,   4, 141,  72,   0,  24,
      4,   4,   4,   4,   4, 103,   0,   0,   4,   4,   4,   4,   4,   4,   4,  93,
      4,   4,   4,   4,  30,   0,  24, 117, 142, 143,   4, 144,   4,   4,   4,  93,
    145, 146,   4,   4, 147, 148,   0, 145, 149, 150,   4,  98,   4,   4, 151, 152,
     27, 102, 153,  81,   4, 154, 136, 155,   4, 134, 156, 157,   4, 104, 158, 159,
    160, 161,  86, 162,   4,   4,   4,  32,   4,   4,   4,   4,   4, 163, 164, 109,
      4,   4,   4, 165,   4,   4, 148,   0, 166, 167, 168,   4,   4,  26, 169,   4,
      4, 117,  24,   4, 170,   4, 150, 171,   0,   0,   0, 172,   4,   4,   4,  81,
      0,   1,   1, 173,   4, 104, 174,   0, 175, 176, 177,   0,   4,   4,   4,  72,
      0,   0,   4, 178,   0,   0,   0,   0,   0,   0,   0,   0,  81,   4, 179,   0,
      4,  25, 102,  72, 117,   4, 180,   0,   4,   4,   4,   4, 117,  24, 181, 109,
      4, 182,   4,  60,   0,   0,   0,   0,   4, 134, 103, 150,   0,   0,   0,   0,
    183, 184, 103, 134, 104,   0,   0, 185, 103, 148,   0,   0,   4, 186,   0,   0,
    187, 103,   0,  81,  81,   0,  78, 188,   4, 103, 103, 153,  26,   0,   0,   0,
      4,   4,  15,   0,   4, 153,   4, 153,   4, 150,   0,   0,   0,   0,   0,   0,
     81, 189, 190,   0,   0,   0,   0,   0,   4,   4, 190,   0, 146,  31,  24,  15,
      4, 153, 191, 192,   4,   4, 193,   0, 194, 195,   0,   0, 196, 118,   4,  15,
     39,  48, 197,  60,   0,   0,   0,   0,   4,   4, 198,   0,   4,   4, 199,   0,
      0,   0,   0,   0,   4, 200, 201,   0,   4, 104, 202,   0,   4, 103,   0,   0,
     64,  32,   0,   0,   0,   0,   0,   0,   4,  31,   0,   0,   0,   4,   4, 203,
      4, 204,  24,   4, 205,   0,   4,  31, 206, 207,  77, 208, 170, 209,   0,   0,
    210, 211, 212, 213, 214,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 134,
      4,   4,   4,   4, 148,   0,   0,   0,   4,   4,   4, 141,   4,   4,   4,   4,
      4,   4,  60,   0,   0,   0,   0,   0,   4, 141,   0,   0,   0,   0,   0,   0,
      4,   4, 215,   0,   0,   0,   0,   0,   4,  31, 104,   0,   0,   0,  24, 156,
      4, 134,  60, 216,  93,   0,   0,   0,   0,   0,   4,   4,   0,   0,   0,   0,
      4,   4, 217, 104, 169,   0,   0, 218,   4,   4,   4,   4,   4,   4,   4,  26,
      4,   4,   4,   4,   4,   4,   4, 153, 104,   0,   0,  24,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4, 109,   4,   4,   4, 219, 220,   0,   0,   0,
      4,   4, 221,   4, 222, 223, 224,   4, 225, 226, 227,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4, 228, 229,  86, 221, 221, 131, 131, 206, 206, 230,   0,
    231, 232,   0,   0,   0,   0,   0,   0,   4,   4,   4,   4,   4,   4, 188,   0,
      4,   4, 233,   0,   0,   0,   0,   0, 224, 234, 235, 236, 237, 238,   0,   0,
      0,  24, 239, 239, 108,   0,   0,   0,   4,   4,   4,   4,   4,   4, 134,   0,
      4, 178,   4,   4,   4,   4,   4,   4, 117,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4, 240,   4,   4,   4,   4,   4,   4,   4,   4,   4,  77,
    117,   0,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_alphabetic_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255,   7,   0,   4,  32,   4, 255, 255, 127, 255,
    255, 255, 255, 255, 195, 255,   3,   0,  31,  80,   0,   0,  32,   0,   0,   0,
      0,   0, 223, 188,  64, 215, 255, 255, 251, 255, 255, 255, 255, 255, 191, 255,
      3, 252, 255, 255, 255, 255, 254, 255, 255, 255, 127,   2, 255,   1,   0,   0,
      0,   0, 255, 191, 182,   0, 255, 255, 255, 135,   7,   0,   0,   0, 255,   7,
    255, 255, 255, 254,   0, 192, 255, 255, 255, 255, 239,  31, 254, 225,   0, 156,
      0,   0, 255, 255,   0, 224, 255, 255, 255, 255,   3,   0,   0, 252, 255, 255,
    255,   7,  48,   4, 255, 255, 255, 252, 255,  31,   0,   0, 255, 255, 255,   1,
    255,   7,   0,   0, 255, 255, 223,  63,   0,   0, 240, 255, 248,   3, 255, 255,
    255, 255, 255, 239, 255, 223, 225, 255,  15,   0, 254, 255, 239, 159, 249, 255,
    255, 253, 197, 227, 159,  89, 128, 176,  15,   0,   3,  16, 238, 135, 249, 255,
    255, 253, 109, 195, 135,  25,   2,  94,   0,   0,  63,   0, 238, 191, 251, 255,
    255, 253, 237, 227, 191,  27,   1,   0,  15,   0,   0,  30, 238, 159, 249, 255,
    159,  25, 192, 176,  15,   0,   2,   0, 236, 199,  61, 214,  24, 199, 255, 195,
    199,  29, 129,   0, 239, 223, 253, 255, 255, 253, 255, 227, 223,  29,  96,   7,
     15,   0,   0,   0, 255, 253, 239, 227, 223,  29,  96,  64,  15,   0,   6,   0,
    255, 255, 255, 231, 223,  93, 240, 128,  15,   0,   0, 252, 236, 255, 127, 252,
    255, 255, 251,  47, 127, 128,  95, 255,   0,   0,  12,   0, 254, 255, 255, 255,
    255, 255, 255,   7, 127,  32,   0,   0, 150,  37, 240, 254, 174, 236, 255,  59,
     95,  32,   0, 240,   1,   0,   0,   0, 255, 254, 255, 255, 255,  31, 254, 255,
      3, 255, 255, 254, 255, 255, 255,  31, 255, 255, 127, 249, 231, 193, 255, 255,
    127,  64,   0,  48, 191,  32, 255, 255, 255, 255, 255, 247, 255,  61, 127,  61,
    255,  61, 255, 255, 255, 255,  61, 127,  61, 255, 127, 255, 255, 255,  61, 255,
    255, 255, 255, 135, 255, 255,   0,   0, 255, 255,  63,  63, 255, 159, 255, 255,
    255, 199, 255,   1, 255, 223,  15,   0, 255, 255,  15,   0, 255, 223,  13,   0,
    255, 255, 207, 255, 255,   1, 128,  16, 255,   7, 255, 255, 255, 255,  63,   0,
    255, 255, 255, 127, 255,  15, 255,   1, 255,  63,  31,   0, 255,  15, 255, 255,
    255,   3,   0,   0, 255, 255, 255,  15, 254, 255,  31,   0, 128,   0,   0,   0,
    255, 255, 239, 255, 239,  15,   0,   0, 255, 243,   0, 252, 191, 255,   3,   0,
      0, 224,   0, 252, 255, 255, 255,  63, 255,   1, 255, 255,   0, 222, 111,   0,
    128, 255,  31,   0,  63,  63, 255, 170, 255, 255, 223,  95, 220,  31, 207,  15,
    255,  31, 220,  31,   0,   0,   2, 128,   0,   0, 255,  31, 132, 252,  47,  62,
     80, 189, 255, 243, 224,  67,   0,   0,   0,   0, 192, 255, 255, 127, 255, 255,
     31, 120,  12,   0, 255, 128,   0,   0, 255, 255, 127,   0, 127, 127, 127, 127,
      0, 128,   0,   0, 224,   0,   0,   0, 254,   3,  62,  31, 255, 255, 127, 224,
    224, 255, 255, 255, 255, 127,   0,   0, 255,  31, 255, 255,   0,  12,   0,   0,
    255, 127, 240, 143,   0,   0, 128, 255, 252, 255, 255, 255, 255, 249, 255, 255,
    255, 255, 255,   3, 187, 247, 255, 255, 255,   0,   0,   0,  47,   0,   0,   0,
      0,   0, 252, 104, 255, 255,   7,   0, 255, 255, 247, 255, 223, 255,   0, 124,
    255,  63,   0,   0, 255, 255, 127, 196,   5,   0,   0,  56, 255, 255,  60,   0,
    126, 126, 126,   0, 127, 127, 255, 255,  63,   0, 255, 255,  15,   0, 255, 255,
    127, 248, 255, 255, 255,  63, 255, 255, 127,   0, 248, 224, 255, 253, 127,  95,
    219, 255, 255, 255,   0,   0, 248, 255, 255, 255, 252, 255,   0,   0, 255,  15,
      0,   0, 223, 255, 192, 255, 255, 255, 252, 252, 252,  28, 255, 239, 255, 255,
    127, 255, 255, 183, 255,  63, 255,  63, 255, 255,  31,   0, 255, 255,   1,   0,
     15, 255,  62,   0, 255, 255,  15, 255, 255,   0, 255, 255,  63, 253, 255, 255,
    255, 255, 191, 145, 255, 255,  55,   0, 255, 255, 255, 192, 111, 240, 239, 254,
     31,   0,   0,   0, 128,   0, 255, 255,  63,   0,   0,   0, 112,   0, 255, 255,
    255, 255,  71,   0,  30,   0,   0,  20, 255, 255, 251, 255, 255, 255, 159,  64,
    127, 189, 255, 191, 159,  25, 129, 224, 187,   7,   0,   0, 179,   0,   0,   0,
    255, 255,  63, 127,   0,   0,   0,  63,  17,   0,   0,   0,   0,   0,   0, 128,
    255, 255, 231, 127, 207, 255, 255,  32, 255, 253, 255, 255, 255, 255, 127, 127,
      0,   0, 252, 255, 255, 254, 127,   0, 127, 251, 255, 255, 255, 255, 127, 180,
    203,   0,   0,   0, 191, 253, 255, 255, 255, 127, 123,   1, 127,   0,   0,   0,
    248, 255, 255, 224,  31,   0, 255, 255,   3,   0,   0,   0, 255,   7, 255,  31,
    255,   1, 255,  67, 255, 255, 223, 255, 255, 255, 255, 223, 100, 222, 255, 235,
    239, 255, 255, 255, 191, 231, 223, 223, 255, 255, 255, 123,  95, 252, 253, 255,
     63, 255, 255, 255, 253, 255, 255, 247, 247,  15,   0,   0, 127, 255, 255, 249,
    219,   7,   0,   0, 143,   0,   0,   0, 150, 254, 247,  10, 132, 234, 150, 170,
    150, 247, 247,  94, 255, 251, 255,  15, 238, 251, 255,  15, 255,   3, 255, 255,
      3,   0, 255, 255,
};

/* Alphabetic: 2277 bytes. */

RE_UINT32 re_get_alphabetic(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_alphabetic_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_alphabetic_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_alphabetic_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_alphabetic_stage_4[pos + f] << 5;
    pos += code;
    value = (re_alphabetic_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Lowercase. */

static RE_UINT8 re_lowercase_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_lowercase_stage_2[] = {
     0,  1,  2,  3,  4,  5,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  6,  7,  1,  1,  1,  1,  1,  1,  1,  1,  1,  8,
     9, 10,  1, 11,  1,  1,  1,  1,  1,  1,  1,  1,  1, 12,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 13,  1,  1, 14,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_lowercase_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     7,  6,  6,  8,  6,  6,  6,  6,  6,  6,  6,  6,  9, 10, 11, 12,
    13, 14,  6,  6, 15,  6,  6,  6,  6,  6,  6,  6, 16, 17,  6,  6,
     6,  6,  6,  6,  6,  6, 18, 19,  6,  6,  6, 20,  6,  6,  6,  6,
     6,  6,  6, 21,  6,  6,  6, 22,  6,  6,  6,  6, 23,  6,  6,  6,
     6,  6,  6,  6, 24,  6,  6,  6, 25,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 26,  6,  6,  6,  6,  6, 27, 28, 29, 30,
     6, 31,  6,  6,  6,  6,  6,  6,
};

static RE_UINT8 re_lowercase_stage_4[] = {
     0,  0,  0,  1,  0,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12,
     5, 13, 14, 15, 16, 17, 18, 19,  0,  0, 20, 21, 22, 23, 24, 25,
     0, 26, 15,  5, 27,  5, 28,  5,  5, 29,  0, 15, 30,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 26, 31,
     0,  0,  0,  0,  0,  0,  0, 32,  0,  0,  0,  0, 30,  0,  0,  0,
    15, 15, 15, 15, 15, 15,  0,  0,  5,  5,  5,  5, 33,  5,  5,  5,
    34, 35, 36, 37, 35, 38, 39, 40,  0,  0,  0, 41, 42,  0,  0,  0,
    43, 44, 45, 26, 46,  0,  0,  0,  0,  0,  0,  0,  0,  0, 26, 47,
     0, 26, 48, 49,  5,  5,  5, 50, 15, 51,  0,  0,  0,  0,  0,  0,
     0,  0,  5, 52, 53,  0,  0,  0,  0, 54,  5, 55, 56, 57,  0, 58,
     0, 26, 59, 60, 15, 15,  0,  0, 61,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  1,  0,  0,  0,  0,  0,  0, 62, 63,  0,  0,  0, 64, 65,
     0,  0,  0,  0,  0,  0, 15, 66,  0,  0,  0,  0,  0,  0, 15,  0,
     0,  0,  0, 15,  0,  0,  0,  0, 67, 68, 69, 70, 71, 72, 73, 74,
    75, 76, 77, 78, 79, 67, 68, 80, 70, 71, 81, 63, 74, 82, 83, 84,
    85, 81, 86, 26, 87, 74, 88,  0,  0, 89, 90,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_lowercase_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255,   7,   0,   4,  32,   4,   0,   0,   0, 128,
    255, 255, 127, 255, 170, 170, 170, 170, 170, 170, 170,  85,  85, 171, 170, 170,
    170, 170, 170, 212,  41,  49,  36,  78,  42,  45,  81, 230,  64,  82,  85, 181,
    170, 170,  41, 170, 170, 170, 250, 147, 133, 170, 255, 255, 255, 255, 255, 255,
    255, 255, 239, 255, 255, 255, 255,   1,   3,   0,   0,   0,  31,   0,   0,   0,
     32,   0,   0,   0,   0,   0, 138,  60,   0,   0,   1,   0,   0, 240, 255, 255,
    255, 127, 227, 170, 170, 170,  47,  25,   0,   0, 255, 255,   2, 168, 170, 170,
     84, 213, 170, 170, 170, 170,   0,   0, 255,   1,   0,   0, 255, 255, 255, 231,
      0,   0,   0,  63, 170, 170, 234, 191, 255,   0,  63,   0, 255,   0, 255,   0,
     63,   0, 255,   0, 255,   0, 255,  63, 255,   0, 223,  64, 220,   0, 207,   0,
    255,   0, 220,   0,   0,   0,   2, 128,   0,   0, 255,  31,   0, 196,   8,   0,
      0, 128,  16,  50, 192,  67,   0,   0,  16,   0,   0,   0, 255,   3,   0,   0,
    255, 255, 255, 127,  98,  21, 218,  63,  26,  80,   8,   0, 191,  32,   0,   0,
    170,  42,   0,   0, 170, 170, 170,  58, 168, 170, 171, 170, 170, 170, 255, 149,
    170,  80, 186, 170, 170, 130, 160,   2,   0,   0,   0,   7, 255, 255, 255, 247,
     63,   0, 255, 255, 127,   0, 248,   0,   0, 255, 255, 255, 255, 255,   0,   0,
      0,   0,   0, 255, 255, 255, 255,  15, 255, 255,   7,   0,   0,   0,   0, 252,
    255, 255,  15,   0,   0, 192, 223, 255, 255,   0,   0,   0, 252, 255, 255,  15,
      0,   0, 192, 235, 239, 255,   0,   0,   0, 252, 255, 255,  15,   0,   0, 192,
    255, 255, 255,   0,   0,   0, 252, 255, 255,  15,   0,   0, 192, 255, 255, 255,
      0, 192, 255, 255,   0,   0, 192, 255,  63,   0,   0,   0, 252, 255, 255, 247,
      3,   0,   0, 240, 255, 255, 223,  15, 255, 127,  63,   0, 255, 253,   0,   0,
    247,  11,   0,   0, 252, 255, 255, 255,  15,   0,   0,   0,
};

/* Lowercase: 853 bytes. */

RE_UINT32 re_get_lowercase(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_lowercase_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_lowercase_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_lowercase_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_lowercase_stage_4[pos + f] << 5;
    pos += code;
    value = (re_lowercase_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Uppercase. */

static RE_UINT8 re_uppercase_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_uppercase_stage_2[] = {
     0,  1,  2,  3,  4,  5,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  6,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  7,
     8,  9,  1, 10,  1,  1,  1,  1,  1,  1,  1,  1,  1, 11,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 12,  1,  1, 13, 14,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_uppercase_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     7,  6,  6,  8,  6,  6,  6,  6,  6,  6,  6,  6,  9,  6, 10, 11,
     6, 12,  6,  6, 13,  6,  6,  6,  6,  6,  6,  6, 14,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 15, 16,  6,  6,  6,  6,  6,  6,  6, 17,
     6,  6,  6,  6, 18,  6,  6,  6,  6,  6,  6,  6, 19,  6,  6,  6,
    20,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6, 21,  6,
     6,  6,  6,  6, 22, 23, 24, 25,  6, 26,  6,  6,  6,  6,  6,  6,
     6, 27,  6,  6,  6,  6,  6,  6,
};

static RE_UINT8 re_uppercase_stage_4[] = {
     0,  0,  1,  0,  0,  0,  2,  0,  3,  4,  5,  6,  7,  8,  9, 10,
     3, 11, 12,  0,  0,  0,  0,  0,  0,  0,  0, 13, 14, 15, 16, 17,
    18, 19,  0,  3, 20,  3, 21,  3,  3, 22, 23,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 18, 24,  0,
     0,  0,  0,  0,  0, 18, 18, 25,  0,  0,  0,  0, 26, 27,  0,  0,
     3,  3,  3,  3, 28,  3,  3,  3, 29, 30, 31, 32,  0, 33, 34, 35,
    36, 37, 38, 19, 39,  0,  0,  0,  0,  0,  0,  0,  0, 40, 19,  0,
    18, 41,  0, 42,  3,  3,  3, 43,  0,  0,  3, 44, 45,  0,  0,  0,
     0, 46,  3, 47, 48, 49,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,
    18, 50,  0,  0,  0, 26, 51,  0,  0,  0,  0,  0, 18, 52,  0,  0,
     0,  0,  0,  0,  0, 18,  0,  0,  0,  0, 18,  0,  0,  0,  0,  0,
    53, 54, 55, 56, 57, 58, 26, 59, 60, 61, 62, 63, 64, 53, 54, 55,
    56, 65, 25, 26, 59, 56, 66, 67, 68, 69, 40, 41, 26, 70, 71,  0,
    18, 72,  0,  0,  0,  0,  0,  0,  0, 26, 73, 73, 59,  0,  0,  0,
};

static RE_UINT8 re_uppercase_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255,   7, 255, 255, 127, 127,  85,  85,  85,  85,
     85,  85,  85, 170, 170,  84,  85,  85,  85,  85,  85,  43, 214, 206, 219, 177,
    213, 210, 174,  17, 144, 164, 170,  74,  85,  85, 210,  85,  85,  85,   5, 108,
    122,  85,   0,   0,   0,   0,  69, 128,  64, 215, 254, 255, 251,  15,   0,   0,
      0, 128,  28,  85,  85,  85, 144, 230, 255, 255, 255, 255, 255, 255,   0,   0,
      1,  84,  85,  85, 171,  42,  85,  85,  85,  85, 254, 255, 255, 255, 127,   0,
    191,  32,   0,   0, 255, 255,  63,   0,   0,   0, 255, 255, 255, 255, 255, 231,
     85,  85,  21,  64,   0, 255,   0,  63,   0, 255,   0, 255,   0,  63,   0, 170,
      0, 255,   0,   0,   0,   0,   0,  15,   0,  15,   0,  15,   0,  31,   0,  15,
    132,  56,  39,  62,  80,  61,  15, 192,  32,   0,   0,   0,   8,   0,   0,   0,
      0,   0, 192, 255, 255, 127,   0,   0, 157, 234,  37, 192,   5,  40,   4,   0,
     85,  21,   0,   0,  85,  85,  85,   5,  84,  85,  84,  85,  85,  85,   0, 106,
     85,  40,  69,  85,  85, 125,  95,   1, 255,   0,   0,   0, 255, 255,  15,   0,
    255, 255,   7,   0, 255, 255, 255,   3,   0,   0, 240, 255, 255,  63,   0,   0,
      0, 255, 255, 255,   3,   0,   0, 208, 100, 222,  63,   0, 255,   3,   0,   0,
    176, 231, 223,  31,   0,   0,   0, 123,  95, 252,   1,   0,   0, 240, 255, 255,
     63,   0,   0,   0,   3,   0,   0, 240,   1,   0,   0,   0, 252, 255, 255,   7,
      0,   0,   0, 240, 255, 255,  31,   0, 255,   1,   0,   0,   0,   4,   0,   0,
      3,   0,   0,   0, 255,   3, 255, 255,
};

/* Uppercase: 753 bytes. */

RE_UINT32 re_get_uppercase(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_uppercase_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_uppercase_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_uppercase_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_uppercase_stage_4[pos + f] << 5;
    pos += code;
    value = (re_uppercase_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Cased. */

static RE_UINT8 re_cased_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_cased_stage_2[] = {
     0,  1,  2,  3,  4,  5,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  6,  7,  1,  1,  1,  1,  1,  1,  1,  1,  1,  8,
     9, 10,  1, 11,  1,  1,  1,  1,  1,  1,  1,  1,  1, 12,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 13,  1,  1, 14, 15,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_cased_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     7,  6,  6,  8,  6,  6,  6,  6,  6,  6,  6,  6,  9, 10, 11, 12,
    13, 14,  6,  6, 15,  6,  6,  6,  6,  6,  6,  6, 16, 17,  6,  6,
     6,  6,  6,  6,  6,  6, 18, 19,  6,  6,  6, 20,  6,  6,  6,  6,
     6,  6,  6, 21,  6,  6,  6, 22,  6,  6,  6,  6, 23,  6,  6,  6,
     6,  6,  6,  6, 24,  6,  6,  6, 25,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 26,  6,  6,  6,  6,  6, 27, 28, 29, 30,
     6, 31,  6,  6,  6,  6,  6,  6,  6, 32,  6,  6,  6,  6,  6,  6,
};

static RE_UINT8 re_cased_stage_4[] = {
     0,  0,  1,  1,  0,  2,  3,  3,  4,  4,  4,  4,  4,  5,  6,  4,
     4,  4,  4,  4,  7,  8,  9, 10,  0,  0, 11, 12, 13, 14,  4, 15,
     4,  4,  4,  4, 16,  4,  4,  4,  4, 17, 18,  4, 19,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4, 20, 21,
     0,  0,  0,  0,  0,  4,  4, 22,  0,  0,  0,  0, 23, 21,  0,  0,
     4,  4,  4,  4,  4,  4,  0,  0,  4,  4,  4,  4,  4,  4,  4,  4,
    22,  4, 24, 25,  4, 26, 27, 28,  0,  0,  0, 29, 30,  0,  0,  0,
    31, 32, 33,  4, 34,  0,  0,  0,  0,  0,  0,  0,  0, 35,  4, 36,
     4, 37, 38,  4,  4,  4,  4, 39,  4, 40,  0,  0,  0,  0,  0,  0,
     0,  0,  4, 41, 25,  0,  0,  0,  0, 42,  4,  4, 43, 44,  0, 45,
     0, 46,  5, 47,  4,  4,  0,  0, 48,  0,  0,  0,  0,  0,  0,  0,
     0,  1,  1,  0,  0,  0,  0,  0,  4,  4, 49,  0,  0, 46, 50, 51,
     0,  0,  0,  0,  4, 52,  4, 52,  0,  0,  0,  0,  0,  4,  4,  0,
     0,  0,  4,  4,  0,  0,  0,  0,  4,  4, 53,  4, 54, 55, 56,  4,
    57, 58, 59,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4, 60, 61,  5,
    53, 53, 37, 37, 62, 62, 63,  0,  4,  4, 64,  0,  0,  0,  0,  0,
     0, 46, 65, 65, 36,  0,  0,  0,
};

static RE_UINT8 re_cased_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255,   7,   0,   4,  32,   4, 255, 255, 127, 255,
    255, 255, 255, 255, 255, 255, 255, 247, 240, 255, 255, 255, 255, 255, 239, 255,
    255, 255, 255,   1,   3,   0,   0,   0,  31,   0,   0,   0,  32,   0,   0,   0,
      0,   0, 207, 188,  64, 215, 255, 255, 251, 255, 255, 255, 255, 255, 191, 255,
      3, 252, 255, 255, 255, 255, 254, 255, 255, 255, 127,   0, 255,   1,   0,   0,
    191,  32, 255, 255, 255, 255, 255, 231, 255, 255,  63,  63, 255,   1, 255, 255,
     63,  63, 255, 170, 255, 255, 255,  63, 255, 255, 223,  95, 220,  31, 207,  15,
    255,  31, 220,  31,   0,   0,   2, 128,   0,   0, 255,  31, 132, 252,  47,  62,
     80, 189,  31, 242, 224,  67,   0,   0,  24,   0,   0,   0,   0,   0, 192, 255,
    255,   3,   0,   0, 255, 127, 255, 255, 255, 255, 255, 127,  31, 120,  12,   0,
    191,  32,   0,   0, 255,  63,   0,   0, 252, 255, 255, 255, 255, 120, 255, 255,
    255, 255, 255,   3,   0,   0,   0,   7,   0,   0, 255, 255,  63,   0, 255, 255,
    127,   0, 248,   0, 255, 255,   0,   0, 255, 255,  15, 255, 255, 255, 255,  15,
    255, 255,   7,   0, 255, 255, 223, 255, 255, 255, 255, 223, 100, 222, 255, 235,
    239, 255, 255, 255, 191, 231, 223, 223, 255, 255, 255, 123,  95, 252, 253, 255,
     63, 255, 255, 255, 253, 255, 255, 247, 255, 253, 255, 255, 247,  15,   0,   0,
     15,   0,   0,   0, 255,   3, 255, 255,
};

/* Cased: 769 bytes. */

RE_UINT32 re_get_cased(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_cased_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_cased_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_cased_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_cased_stage_4[pos + f] << 5;
    pos += code;
    value = (re_cased_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Case_Ignorable. */

static RE_UINT8 re_case_ignorable_stage_1[] = {
    0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4,
    4, 4,
};

static RE_UINT8 re_case_ignorable_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  8,  9,  7,  7,  7,  7,  7,  7,  7,  7,  7, 10,
    11, 12, 13, 14,  7,  7,  7,  7,  7,  7,  7,  7,  7, 15,  7,  7,
     7,  7,  7,  7,  7,  7,  7, 16,  7,  7, 17, 18, 19, 20, 21,  7,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
    22,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
};

static RE_UINT8 re_case_ignorable_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
    16,  1,  1, 17,  1,  1,  1, 18, 19, 20, 21, 22, 23, 24,  1, 25,
    26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 27, 28, 29,  1,
    30,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
    31,  1,  1,  1, 32,  1, 33, 34, 35, 36, 37, 38,  1,  1,  1,  1,
     1,  1,  1, 39,  1,  1, 40, 41,  1, 42, 43, 44,  1,  1,  1,  1,
     1,  1, 45,  1,  1, 46,  1, 47, 48, 49, 50, 51, 52, 53, 54, 55,
    56,  1, 57,  1, 58, 59, 60,  1,  1,  1, 61, 62,  1,  1,  1, 63,
     1,  1,  1,  1, 64,  1,  1,  1,  1, 65, 66,  1,  1,  1,  1,  1,
     1,  1, 67,  1,  1,  1,  1,  1, 68,  1,  1,  1,  1,  1,  1,  1,
    69, 70,  1,  1,  1,  1,  1,  1,  1,  1,  1, 71,  1,  1,  1,  1,
    72, 73,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_case_ignorable_stage_4[] = {
      0,   1,   2,   3,   0,   4,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   5,   6,   6,   6,   6,   6,   7,   8,   0,   0,   0,
      0,   0,   0,   0,   9,   0,   0,   0,   0,   0,  10,   0,  11,  12,  13,  14,
     15,   0,  16,  17,   0,   0,  18,  19,  20,   5,  21,   0,   0,  22,   0,  23,
     24,  25,  26,   0,   0,   0,  27,   6,  28,  29,  30,  31,  32,  33,  34,  35,
     36,  33,  37,  38,  36,  33,  39,  40,  32,  41,  42,  43,  44,   0,  45,   0,
     46,  47,  48,  43,  32,  41,  49,  43,  50,  51,  34,  43,   0,   0,  52,   0,
      0,  53,  54,   0,   0,  55,  56,   0,  57,  58,   0,  59,  60,  61,  62,   0,
      0,  63,  64,  65,  66,   0,   0,  33,   0,   0,  67,   0,   0,   0,   0,   0,
     68,  68,  69,  69,   0,  70,  71,   0,  72,   0,  73,   0,  74,  75,   0,   0,
      0,  76,   0,   0,   0,   0,   0,   0,  77,   0,  78,  79,   0,  80,   0,   0,
     81,  82,  44,  83,  50,  84,   0,  85,   0,  86,   0,  87,   0,   0,  88,  89,
      0,  90,   6,  91,  92,   6,   6,  93,   0,   0,   0,   0,   0,  94,  95,  96,
     97,  98,   0,  99, 100,   0,   5, 101,   0,   0,   0, 102,   0,   0,   0, 103,
      0,   0,   0, 104,   0,   0,   0,   6,   0, 105,   0,   0,   0,   0,   0,   0,
    106, 107,   0,   0, 108,   0,   0, 109, 110,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  87, 111,   0,   0, 112, 113,   0,   0, 114,
      6,  50,   0,  17, 115,   0,   0,  57, 116,  74,   0,   0,   0,   0, 117, 118,
      0, 119, 120,   0,  28, 121, 105,  74,   0, 122, 123, 124,   0, 125, 126, 127,
      0,   0,  92,   0,   0,   0,   0, 128,   2,   0,   0,   0,   0, 129,  50,   0,
    130, 131, 132,   0,   0,   0,   0, 133,   1,   2,   3,  17,  47,   0,   0, 134,
      0,   0,   0,   0,   0,   0,   0, 135,   0,   0,   0,   0,   0,   0,   0,   3,
      0,   0,   0, 136,   0,   0,   0,   0, 137, 138,   0,   0,   0,   0,   0,  74,
      0, 139,   0,   0,   0,   0,   0,   0,   0,   0,  22,   0,   0,   0,   0,   0,
     32, 140, 141, 133,  50, 142, 143,   0,  28, 144,   0, 145,  50, 146, 147,   0,
      0, 148,   0,   0,   0,   0, 133, 149,  50,  51,   3, 150,   0,   0,   0,   0,
      0, 140, 151,   0,   0, 152, 153,   0,   0,   0,   0,   0,   0, 154, 155,   0,
      0, 156,   3,   0,   0, 157,   0,   0,  67, 158,   0,   0,   0,   0,   0,   0,
      0, 159,   0,   0,   0,   0,   0,   0, 160, 161, 162,   0, 163,   0,   0,   0,
      0, 164,   0,   0, 129, 165,   0,   0,   0, 166, 167,   0, 168,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0, 169,   0,   0,   0,   0,   0,   0,   0, 170,
      0, 171,  81,   0,   0,   0,   0,   0,   0,   0,   0,   0, 172,   0,   0,  50,
      0,   0,   0,   0, 173,  81,   0,   0,   0,   0,   0, 174, 175, 176,   0,   0,
      0,   0, 177,   0,   0,   0,   0,   0,   6, 178,   6, 179, 180, 181,   0,   0,
    182, 183,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 171,   0,
      0,   0, 184,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  92,
     32,   6,   6,   6,   0,   0,   0,   0,   6,   6,   6,   6,   6,   6,   6, 131,
};

static RE_UINT8 re_case_ignorable_stage_5[] = {
      0,   0,   0,   0, 128,  64,   0,   4,   0,   0,   0,  64,   1,   0,   0,   0,
      0, 161, 144,   1,   0,   0, 255, 255, 255, 255, 255, 255, 255, 255,  48,   4,
    176,   0,   0,   0, 248,   3,   0,   0,   0,   0,   0,   2,   0,   0, 254, 255,
    255, 255, 255, 191, 182,   0,   0,   0,   0,   0,  16,   0,  63,   0, 255,  23,
      1, 248, 255, 255,   0,   0,   1,   0,   0,   0, 192, 191, 255,  61,   0,   0,
      0, 128,   2,   0, 255,   7,   0,   0, 192, 255,   1,   0,   0, 248,  63,  36,
      0,   0, 192, 255, 255,  63,   0,   0,   0,   0,   0,  14,   0,   0, 248, 255,
      7,   0,   0,   0,   0,   0,   0,  20, 254,  33, 254,   0,  12,   0,   2,   0,
      2,   0,   0,   0,   0,   0,   0,  16,  30,  32,   0,   0,  12,   0,   0,  64,
      6,   0,   0,   0, 134,  57,   2,   0,   0,   0,  35,   0, 190,  33,   0,   0,
     12,   0,   0, 252,   0,   0,   0, 144,  30,  32,  64,   0,  12,   0,   0,   0,
      4,   0,   0,   0,   1,  32,   0,   0,  17,   0,   0,   0,   0,   0,   0, 192,
    193,  61,  96,   0,  64,  48,   0,   0,   3,   0,   0,   0,   0,   0,   0,  24,
      0,   4,  92,   0,   0,   0, 242,   7, 192, 127,   0,   0,   0,   0, 242,  27,
     64,  63,   0,   0,   0,   0,   0,   3,   0,   0, 160,   2,   0,   0, 254, 127,
    223, 224, 255, 254, 255, 255, 255,  31,  64,   0,   0,   0,   0, 224, 253, 102,
      0,   0,   0, 195,   1,   0,  30,   0, 100,  32,   0,  32,   0,   0,   0, 224,
      0,   0,  28,   0,   0,   0,  12,   0,   0,   0, 176,  63,  64, 254, 143,  32,
      0, 120,   0,   0,   8,   0,   0,   0,  96,   0,   0,   0,   0,   2,   0,   0,
    135,   1,   4,  14,   0,   0, 128,   9,   0,   0,  64, 127, 229,  31, 248, 159,
    128,   0, 255, 127,  15,   0,   0,   0,   0,   0, 208,  23,   0, 248,  15,   0,
     60,  59,   0,   0,  64, 163,   3,   0,   0, 240, 207,   0,   0,   0,   0,  63,
      0,   0, 247, 255, 253,  33,  16,   3,   0, 240, 255, 255, 255,   7,   0,   1,
      0,   0,   0, 248, 255, 255, 255, 251,   0,   0,   0, 160,   3, 224,   0, 224,
      0, 224,   0,  96,   0, 248,   0,   3, 144, 124,   0,   0, 223, 255,   2, 128,
      0,   0, 255,  31, 255, 255,   1,   0,   0,   0,   0,  48,   0, 128,   3,   0,
      0, 128,   0, 128,   0, 128,   0,   0,  32,   0,   0,   0,   0,  60,  62,   8,
      0,   0,   0, 126,   0,   0,   0, 112,   0,   0,  32,   0,   0,  16,   0,   0,
      0, 128, 247, 191,   0,   0,   0, 240,   0,   0,   3,   0,   0,   7,   0,   0,
     68,   8,   0,   0,  48,   0,   0,   0, 255, 255,   3, 128, 192,  63,   0,   0,
    128, 255,   3,   0,   0,   0, 200,  19,   0, 126, 102,   0,   8,  16,   0,   0,
      0,   0,   1,  16,   0,   0, 157, 193,   2,   0,   0,  32,   0,  48,  88,   0,
     32,  33,   0,   0,   0,   0, 252, 255, 255, 255,   8,   0, 255, 255,   0,   0,
      0,   0,  36,   0,   0,   0,   0, 128,   8,   0,   0,  14,   0,   0,   0,  32,
      0,   0, 192,   7, 110, 240,   0,   0,   0,   0,   0, 135, 240,   0,   0,   0,
      0,   0,   0, 255, 127,   0,   0,   0,   0,   0, 120,  38,   0,  32,   0,   0,
    128, 239,  31,   0,   0,   0,   8,   0,   0,   0, 192, 127,   0,  30,   0,   0,
      0, 128, 211,  64, 248,   7,   0,   0, 192,  31,  31,   0,  92,   0,   0,  64,
      0,   0, 248, 133,  13,   0,   0,   0,   0,   0,  60, 176,   1,   0,   0,  48,
      0,   0, 248, 167,   0,  40, 191,   0, 188,  15,   0,   0,   0, 128, 255,   6,
    254,   7,   0,   0,   0,   0, 248, 121, 128,   0, 126,  14,   0, 252, 127,   3,
      0,   0, 127, 191, 255, 252, 109,   0,   0,   0, 126, 180, 191,   0,   0,   0,
      0,   0, 163,   0,   0,   0,  24,   0,   0,   0,  31,   0,   0,   0, 127,   0,
      0, 128, 255, 255,   0,   0,   0,  96, 128,   3, 248, 255, 231,  15,   0,   0,
      0,  60,   0,   0,  28,   0,   0,   0, 255, 255, 127, 248, 255,  31,  32,   0,
     16,   0,   0, 248, 254, 255,   0,   0, 127, 255, 255, 249, 219,   7,   0,   0,
    240,   7,   0,   0,
};

/* Case_Ignorable: 1646 bytes. */

RE_UINT32 re_get_case_ignorable(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_case_ignorable_stage_1[f] << 4;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_case_ignorable_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_case_ignorable_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_case_ignorable_stage_4[pos + f] << 5;
    pos += code;
    value = (re_case_ignorable_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Changes_When_Lowercased. */

static RE_UINT8 re_changes_when_lowercased_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_changes_when_lowercased_stage_2[] = {
     0,  1,  2,  3,  4,  5,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  6,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  7,
     8,  9,  1, 10,  1,  1,  1,  1,  1,  1,  1,  1,  1, 11,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 12,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_changes_when_lowercased_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     7,  6,  6,  8,  6,  6,  6,  6,  6,  6,  6,  6,  9,  6, 10, 11,
     6, 12,  6,  6, 13,  6,  6,  6,  6,  6,  6,  6, 14,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 15, 16,  6,  6,  6,  6,  6,  6,  6, 17,
     6,  6,  6,  6, 18,  6,  6,  6,  6,  6,  6,  6, 19,  6,  6,  6,
    20,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6, 21,  6,
     6, 22,  6,  6,  6,  6,  6,  6,
};

static RE_UINT8 re_changes_when_lowercased_stage_4[] = {
     0,  0,  1,  0,  0,  0,  2,  0,  3,  4,  5,  6,  7,  8,  9, 10,
     3, 11, 12,  0,  0,  0,  0,  0,  0,  0,  0, 13, 14, 15, 16, 17,
    18, 19,  0,  3, 20,  3, 21,  3,  3, 22, 23,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 18, 24,  0,
     0,  0,  0,  0,  0, 18, 18, 25,  0,  0,  0,  0, 26, 27,  0,  0,
     3,  3,  3,  3, 28,  3,  3,  3, 29, 30, 31, 32, 30, 33, 34, 35,
     0, 36,  0, 19, 37,  0,  0,  0,  0,  0,  0,  0,  0, 38, 19,  0,
    18, 39,  0, 40,  3,  3,  3, 41,  0,  0,  3, 42, 43,  0,  0,  0,
     0, 44,  3, 45, 46, 47,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,
    18, 48,  0,  0,  0, 26, 49,  0,  0,  0,  0,  0, 18, 50,  0,  0,
     0,  0,  0,  0,  0, 18,  0,  0,  0,  0, 18,  0,  0,  0,  0,  0,
    18, 51,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_changes_when_lowercased_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255,   7, 255, 255, 127, 127,  85,  85,  85,  85,
     85,  85,  85, 170, 170,  84,  85,  85,  85,  85,  85,  43, 214, 206, 219, 177,
    213, 210, 174,  17, 176, 173, 170,  74,  85,  85, 214,  85,  85,  85,   5, 108,
    122,  85,   0,   0,   0,   0,  69, 128,  64, 215, 254, 255, 251,  15,   0,   0,
      0, 128,   0,  85,  85,  85, 144, 230, 255, 255, 255, 255, 255, 255,   0,   0,
      1,  84,  85,  85, 171,  42,  85,  85,  85,  85, 254, 255, 255, 255, 127,   0,
    191,  32,   0,   0, 255, 255,  63,   0,   0,   0, 255, 255, 255, 255, 255, 231,
     85,  85,  21,  64,   0, 255,   0,  63,   0, 255,   0, 255,   0,  63,   0, 170,
      0, 255,   0,   0,   0, 255,   0,  31,   0,  31,   0,  15,   0,  31,   0,  31,
     64,  12,   4,   0,   8,   0,   0,   0,   0,   0, 192, 255, 255, 127,   0,   0,
    157, 234,  37, 192,   5,  40,   4,   0,  85,  21,   0,   0,  85,  85,  85,   5,
     84,  85,  84,  85,  85,  85,   0, 106,  85,  40,  69,  85,  85, 125,  95,   1,
    255,   0,   0,   0, 255, 255,  15,   0, 255, 255,   7,   0,   3,   0,   0,   0,
};

/* Changes_When_Lowercased: 609 bytes. */

RE_UINT32 re_get_changes_when_lowercased(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_changes_when_lowercased_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_changes_when_lowercased_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_changes_when_lowercased_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_changes_when_lowercased_stage_4[pos + f] << 5;
    pos += code;
    value = (re_changes_when_lowercased_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Changes_When_Uppercased. */

static RE_UINT8 re_changes_when_uppercased_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_changes_when_uppercased_stage_2[] = {
     0,  1,  2,  3,  4,  5,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  6,  7,  1,  1,  1,  1,  1,  1,  1,  1,  1,  8,
     9, 10,  1, 11,  1,  1,  1,  1,  1,  1,  1,  1,  1, 12,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 13,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_changes_when_uppercased_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     7,  6,  6,  8,  6,  6,  6,  6,  6,  6,  6,  6,  9, 10, 11, 12,
     6, 13,  6,  6, 14,  6,  6,  6,  6,  6,  6,  6, 15, 16,  6,  6,
     6,  6,  6,  6,  6,  6, 17, 18,  6,  6,  6, 19,  6,  6,  6,  6,
     6,  6,  6, 20,  6,  6,  6, 21,  6,  6,  6,  6, 22,  6,  6,  6,
     6,  6,  6,  6, 23,  6,  6,  6, 24,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 25,  6,  6, 26,  6,  6,  6,  6,  6,  6,
};

static RE_UINT8 re_changes_when_uppercased_stage_4[] = {
     0,  0,  0,  1,  0,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12,
     5, 13, 14, 15, 16,  0,  0,  0,  0,  0, 17, 18, 19, 20, 21, 22,
     0, 23, 24,  5, 25,  5, 26,  5,  5, 27,  0, 28, 29,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 23, 30,
     0,  0,  0,  0,  0,  0,  0, 31,  0,  0,  0,  0, 32,  0,  0,  0,
     0,  0,  0, 33,  0,  0,  0,  0,  5,  5,  5,  5, 34,  5,  5,  5,
    35, 36, 37, 38, 24, 39, 40, 41,  0,  0, 42, 23, 43,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 23, 44,  0, 23, 45, 46,  5,  5,  5, 47,
    24, 48,  0,  0,  0,  0,  0,  0,  0,  0,  5, 49, 50,  0,  0,  0,
     0, 51,  5, 52, 53, 54,  0,  0,  0,  0, 55, 23, 24, 24,  0,  0,
    56,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,
     0, 57, 58,  0,  0,  0, 59, 60,  0,  0,  0,  0,  0,  0, 24, 61,
     0,  0,  0,  0,  0,  0, 24,  0,  0,  0,  0, 24,  0,  0,  0,  0,
     0, 62, 63,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_changes_when_uppercased_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255,   7,   0,   0,  32,   0,   0,   0,   0, 128,
    255, 255, 127, 255, 170, 170, 170, 170, 170, 170, 170,  84,  85, 171, 170, 170,
    170, 170, 170, 212,  41,  17,  36,  70,  42,  33,  81, 162,  96,  91,  85, 181,
    170, 170,  45, 170, 168, 170,  10, 144, 133, 170, 223,  26, 107, 159,  38,  32,
    137,  31,   4,  96,  32,   0,   0,   0,   0,   0, 138,  56,   0,   0,   1,   0,
      0, 240, 255, 255, 255, 127, 227, 170, 170, 170,  47,   9,   0,   0, 255, 255,
    255, 255, 255, 255,   2, 168, 170, 170,  84, 213, 170, 170, 170, 170,   0,   0,
    254, 255, 255, 255, 255,   0,   0,   0, 255, 255, 255, 231,   0,   0,   0,  63,
    255,   1,   0,   0,   0,   0,   0,  34, 170, 170, 234,  15, 255,   0,  63,   0,
    255,   0, 255,   0,  63,   0, 255,   0, 255,   0, 255,  63, 255, 255, 223,  80,
    220,  16, 207,   0, 255,   0, 220,  16,   0,  64,   0,   0,  16,   0,   0,   0,
    255,   3,   0,   0, 255, 255, 255, 127,  98,  21,  72,   0,  10,  80,   8,   0,
    191,  32,   0,   0, 170,  42,   0,   0, 170, 170, 170,  10, 168, 170, 168, 170,
    170, 170,   0, 148, 170,  16, 138, 170, 170,   2, 160,   2,   0,   0,   8,   0,
    127,   0, 248,   0,   0, 255, 255, 255, 255, 255,   0,   0,   0,   0,   0, 255,
    255, 255, 255,  15, 255, 255,   7,   0, 252, 255, 255, 255,  15,   0,   0,   0,
};

/* Changes_When_Uppercased: 697 bytes. */

RE_UINT32 re_get_changes_when_uppercased(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_changes_when_uppercased_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_changes_when_uppercased_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_changes_when_uppercased_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_changes_when_uppercased_stage_4[pos + f] << 5;
    pos += code;
    value = (re_changes_when_uppercased_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Changes_When_Titlecased. */

static RE_UINT8 re_changes_when_titlecased_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_changes_when_titlecased_stage_2[] = {
     0,  1,  2,  3,  4,  5,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  6,  7,  1,  1,  1,  1,  1,  1,  1,  1,  1,  8,
     9, 10,  1, 11,  1,  1,  1,  1,  1,  1,  1,  1,  1, 12,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 13,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_changes_when_titlecased_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  7,  6,  6,  6,  6,  6,  6,  6,  6,  8,  9, 10, 11,
     6, 12,  6,  6, 13,  6,  6,  6,  6,  6,  6,  6, 14, 15,  6,  6,
     6,  6,  6,  6,  6,  6, 16, 17,  6,  6,  6, 18,  6,  6,  6,  6,
     6,  6,  6, 19,  6,  6,  6, 20,  6,  6,  6,  6, 21,  6,  6,  6,
     6,  6,  6,  6, 22,  6,  6,  6, 23,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 24,  6,  6, 25,  6,  6,  6,  6,  6,  6,
};

static RE_UINT8 re_changes_when_titlecased_stage_4[] = {
     0,  0,  0,  1,  0,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12,
     5, 13, 14, 15, 16,  0,  0,  0,  0,  0, 17, 18, 19, 20, 21, 22,
     0, 23, 24,  5, 25,  5, 26,  5,  5, 27,  0, 28, 29,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 30,
     0,  0,  0,  0, 31,  0,  0,  0,  0,  0,  0, 32,  0,  0,  0,  0,
     5,  5,  5,  5, 33,  5,  5,  5, 34, 35, 36, 37, 35, 38, 39, 40,
     0,  0, 41, 23, 42,  0,  0,  0,  0,  0,  0,  0,  0,  0, 23, 43,
     0, 23, 44, 45,  5,  5,  5, 46, 24, 47,  0,  0,  0,  0,  0,  0,
     0,  0,  5, 48, 49,  0,  0,  0,  0, 50,  5, 51, 52, 53,  0,  0,
     0,  0, 54, 23, 24, 24,  0,  0, 55,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  1,  0,  0,  0,  0,  0,  0, 56, 57,  0,  0,  0, 58, 59,
     0,  0,  0,  0,  0,  0, 24, 60,  0,  0,  0,  0,  0,  0, 24,  0,
     0,  0,  0, 24,  0,  0,  0,  0,  0, 61, 62,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_changes_when_titlecased_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255,   7,   0,   0,  32,   0,   0,   0,   0, 128,
    255, 255, 127, 255, 170, 170, 170, 170, 170, 170, 170,  84,  85, 171, 170, 170,
    170, 170, 170, 212,  41,  17,  36,  70,  42,  33,  81, 162, 208,  86,  85, 181,
    170, 170,  43, 170, 168, 170,  10, 144, 133, 170, 223,  26, 107, 159,  38,  32,
    137,  31,   4,  96,  32,   0,   0,   0,   0,   0, 138,  56,   0,   0,   1,   0,
      0, 240, 255, 255, 255, 127, 227, 170, 170, 170,  47,   9,   0,   0, 255, 255,
    255, 255, 255, 255,   2, 168, 170, 170,  84, 213, 170, 170, 170, 170,   0,   0,
    254, 255, 255, 255, 255,   0,   0,   0,   0,   0,   0,  63, 255,   1,   0,   0,
      0,   0,   0,  34, 170, 170, 234,  15, 255,   0,  63,   0, 255,   0, 255,   0,
     63,   0, 255,   0, 255,   0, 255,  63, 255,   0, 223,  64, 220,   0, 207,   0,
    255,   0, 220,   0,   0,  64,   0,   0,  16,   0,   0,   0, 255,   3,   0,   0,
    255, 255, 255, 127,  98,  21,  72,   0,  10,  80,   8,   0, 191,  32,   0,   0,
    170,  42,   0,   0, 170, 170, 170,  10, 168, 170, 168, 170, 170, 170,   0, 148,
    170,  16, 138, 170, 170,   2, 160,   2,   0,   0,   8,   0, 127,   0, 248,   0,
      0, 255, 255, 255, 255, 255,   0,   0,   0,   0,   0, 255, 255, 255, 255,  15,
    255, 255,   7,   0, 252, 255, 255, 255,  15,   0,   0,   0,
};

/* Changes_When_Titlecased: 685 bytes. */

RE_UINT32 re_get_changes_when_titlecased(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_changes_when_titlecased_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_changes_when_titlecased_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_changes_when_titlecased_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_changes_when_titlecased_stage_4[pos + f] << 5;
    pos += code;
    value = (re_changes_when_titlecased_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Changes_When_Casefolded. */

static RE_UINT8 re_changes_when_casefolded_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_changes_when_casefolded_stage_2[] = {
     0,  1,  2,  3,  4,  5,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  6,  7,  1,  1,  1,  1,  1,  1,  1,  1,  1,  8,
     9, 10,  1, 11,  1,  1,  1,  1,  1,  1,  1,  1,  1, 12,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 13,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_changes_when_casefolded_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     7,  6,  6,  8,  6,  6,  6,  6,  6,  6,  6,  6,  9,  6, 10, 11,
     6, 12,  6,  6, 13,  6,  6,  6,  6,  6,  6,  6, 14,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 15, 16,  6,  6,  6, 17,  6,  6,  6,  6,
     6,  6,  6, 18,  6,  6,  6, 19,  6,  6,  6,  6, 20,  6,  6,  6,
     6,  6,  6,  6, 21,  6,  6,  6, 22,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 23,  6,  6, 24,  6,  6,  6,  6,  6,  6,
};

static RE_UINT8 re_changes_when_casefolded_stage_4[] = {
     0,  0,  1,  0,  0,  2,  3,  0,  4,  5,  6,  7,  8,  9, 10, 11,
     4, 12, 13,  0,  0,  0,  0,  0,  0,  0, 14, 15, 16, 17, 18, 19,
    20, 21,  0,  4, 22,  4, 23,  4,  4, 24, 25,  0, 26,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 20, 27,  0,
     0,  0,  0,  0,  0,  0,  0, 28,  0,  0,  0,  0, 29, 30,  0,  0,
     4,  4,  4,  4, 31,  4,  4,  4, 32, 33, 34, 35, 20, 36, 37, 38,
     0, 39,  0, 21, 40,  0,  0,  0,  0,  0,  0,  0,  0, 41, 21,  0,
    20, 42,  0, 43,  4,  4,  4, 44,  0,  0,  4, 45, 46,  0,  0,  0,
     0, 47,  4, 48, 49, 50,  0,  0,  0,  0,  0, 51, 20, 20,  0,  0,
    52,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,
    20, 53,  0,  0,  0, 51, 54,  0,  0,  0,  0,  0, 20, 55,  0,  0,
     0,  0,  0,  0,  0, 20,  0,  0,  0,  0, 20,  0,  0,  0,  0,  0,
    20, 56,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_changes_when_casefolded_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255,   7,   0,   0,  32,   0, 255, 255, 127, 255,
     85,  85,  85,  85,  85,  85,  85, 170, 170,  86,  85,  85,  85,  85,  85, 171,
    214, 206, 219, 177, 213, 210, 174,  17, 176, 173, 170,  74,  85,  85, 214,  85,
     85,  85,   5, 108, 122,  85,   0,   0,  32,   0,   0,   0,   0,   0,  69, 128,
     64, 215, 254, 255, 251,  15,   0,   0,   4, 128,  99,  85,  85,  85, 179, 230,
    255, 255, 255, 255, 255, 255,   0,   0,   1,  84,  85,  85, 171,  42,  85,  85,
     85,  85, 254, 255, 255, 255, 127,   0, 128,   0,   0,   0, 191,  32,   0,   0,
      0,   0,   0,  63, 255,   1, 255, 255, 255, 255, 255, 231,  85,  85,  21,  76,
      0, 255,   0,  63,   0, 255,   0, 255,   0,  63,   0, 170,   0, 255,   0,   0,
    255, 255, 156,  31, 156,  31,   0,  15,   0,  31, 156,  31,  64,  12,   4,   0,
      8,   0,   0,   0,   0,   0, 192, 255, 255, 127,   0,   0, 157, 234,  37, 192,
      5,  40,   4,   0,  85,  21,   0,   0,  85,  85,  85,   5,  84,  85,  84,  85,
     85,  85,   0, 106,  85,  40,  69,  85,  85, 125,  95,   1,   0,   0, 255, 255,
    127,   0, 248,   0, 255,   0,   0,   0, 255, 255,  15,   0, 255, 255,   7,   0,
      3,   0,   0,   0,
};

/* Changes_When_Casefolded: 653 bytes. */

RE_UINT32 re_get_changes_when_casefolded(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_changes_when_casefolded_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_changes_when_casefolded_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_changes_when_casefolded_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_changes_when_casefolded_stage_4[pos + f] << 5;
    pos += code;
    value = (re_changes_when_casefolded_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Changes_When_Casemapped. */

static RE_UINT8 re_changes_when_casemapped_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_changes_when_casemapped_stage_2[] = {
     0,  1,  2,  3,  4,  5,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  6,  7,  1,  1,  1,  1,  1,  1,  1,  1,  1,  8,
     9, 10,  1, 11,  1,  1,  1,  1,  1,  1,  1,  1,  1, 12,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 13,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_changes_when_casemapped_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     7,  6,  6,  8,  6,  6,  6,  6,  6,  6,  6,  6,  9, 10, 11, 12,
     6, 13,  6,  6, 14,  6,  6,  6,  6,  6,  6,  6, 15, 16,  6,  6,
     6,  6,  6,  6,  6,  6, 17, 18,  6,  6,  6, 19,  6,  6,  6,  6,
     6,  6,  6, 20,  6,  6,  6, 21,  6,  6,  6,  6, 22,  6,  6,  6,
     6,  6,  6,  6, 23,  6,  6,  6, 24,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 25,  6,  6, 26,  6,  6,  6,  6,  6,  6,
};

static RE_UINT8 re_changes_when_casemapped_stage_4[] = {
     0,  0,  1,  1,  0,  2,  3,  3,  4,  5,  4,  4,  6,  7,  8,  4,
     4,  9, 10, 11, 12,  0,  0,  0,  0,  0, 13, 14, 15, 16, 17, 18,
     4,  4,  4,  4, 19,  4,  4,  4,  4, 20, 21, 22, 23,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4, 24, 25,
     0,  0,  0,  0,  0,  4,  4, 26,  0,  0,  0,  0, 27, 25,  0,  0,
     0,  0,  0, 28,  0,  0,  0,  0,  4,  4,  4,  4, 29,  4,  4,  4,
    26,  4, 30, 31,  4, 32, 33, 34,  0, 35, 36,  4, 37,  0,  0,  0,
     0,  0,  0,  0,  0, 38,  4, 39,  4, 40, 41, 42,  4,  4,  4, 43,
     4, 44,  0,  0,  0,  0,  0,  0,  0,  0,  4, 45, 46,  0,  0,  0,
     0, 47,  4, 48, 49, 50,  0,  0,  0,  0, 51, 52,  4,  4,  0,  0,
    53,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  0,  0,  0,  0,  0,
     4,  4, 54,  0,  0, 52, 55, 46,  0,  0,  0,  0,  4, 56,  4, 56,
     0,  0,  0,  0,  0,  4,  4,  0,  0,  0,  4,  4,  0,  0,  0,  0,
     4,  4, 57,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_changes_when_casemapped_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255,   7,   0,   0,  32,   0, 255, 255, 127, 255,
    255, 255, 255, 255, 255, 255, 255, 254, 255, 223, 255, 247, 255, 243, 255, 179,
    240, 255, 255, 255, 253, 255,  15, 252, 255, 255, 223,  26, 107, 159,  38,  32,
    137,  31,   4,  96,  32,   0,   0,   0,   0,   0, 207, 184,  64, 215, 255, 255,
    251, 255, 255, 255, 255, 255, 227, 255, 255, 255, 191, 239,   3, 252, 255, 255,
    255, 255, 254, 255, 255, 255, 127,   0, 254, 255, 255, 255, 255,   0,   0,   0,
    191,  32, 255, 255, 255, 255, 255, 231, 255, 255,  63,  63, 255,   1, 255, 255,
      0,   0,   0,  34, 255, 255, 255,  79,  63,  63, 255, 170, 255, 255, 255,  63,
    255, 255, 223,  95, 220,  31, 207,  15, 255,  31, 220,  31,  64,  12,   4,   0,
      0,  64,   0,   0,  24,   0,   0,   0,   0,   0, 192, 255, 255,   3,   0,   0,
    255, 127, 255, 255, 255, 255, 255, 127, 255, 255, 109, 192,  15, 120,  12,   0,
    191,  32,   0,   0, 255,  63,   0,   0, 255, 255, 255,  15, 252, 255, 252, 255,
    255, 255,   0, 254, 255,  56, 207, 255, 255, 127, 255,   3,   0,   0,   8,   0,
      0,   0, 255, 255, 127,   0, 248,   0, 255, 255,   0,   0, 255, 255,  15, 255,
    255, 255,   7,   0,  15,   0,   0,   0,
};

/* Changes_When_Casemapped: 673 bytes. */

RE_UINT32 re_get_changes_when_casemapped(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_changes_when_casemapped_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_changes_when_casemapped_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_changes_when_casemapped_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_changes_when_casemapped_stage_4[pos + f] << 5;
    pos += code;
    value = (re_changes_when_casemapped_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* ID_Start. */

static RE_UINT8 re_id_start_stage_1[] = {
    0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3,
};

static RE_UINT8 re_id_start_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  9, 10, 11,  7,  7,  7,  7, 12, 13, 13, 13, 13, 14,
    15, 16, 17, 18, 19, 13, 20, 13, 21, 13, 13, 13, 13, 22,  7,  7,
    23, 24, 13, 13, 13, 13, 25, 26, 13, 13, 27, 13, 13, 28, 13, 13,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7, 29,  7, 30, 31,  7, 32,  7,  7,  7, 33, 13, 34,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
};

static RE_UINT8 re_id_start_stage_3[] = {
      0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,
     16,   1,  17,  18,  19,   1,  20,  21,  22,  23,  24,  25,  26,  27,   1,  28,
     29,  30,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  32,  33,  31,  31,
     34,  35,  31,  31,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,  36,   1,   1,   1,   1,   1,   1,   1,   1,   1,  37,
      1,   1,   1,   1,  38,   1,  39,  40,  41,  42,  43,  44,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,  45,  31,  31,  31,  31,  31,  31,  31,  31,
     31,   1,  46,  47,   1,  48,  49,  50,  51,  52,  53,  54,  55,  56,   1,  57,
     58,  59,  60,  61,  62,  63,  31,  64,  65,  66,  67,  68,  69,  70,  71,  72,
     73,  31,  74,  31,  75,  76,  77,  31,   1,   1,   1,  78,  79,  80,  31,  31,
      1,   1,   1,   1,  81,  31,  31,  31,  31,  31,  31,  31,   1,   1,  82,  31,
      1,   1,  83,  84,  31,  31,  85,  86,   1,   1,   1,   1,   1,   1,   1,  87,
      1,   1,  88,  31,  31,  31,  31,  31,   1,  89,  90,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  91,  31,  31,  31,  31,  31,  31,  31,  92,  93,  94,  95,
     96,  80,  31,  31,  31,  31,  97,  31,   1,   1,   1,   1,   1,   1,  98,   1,
      1,   1,   1,   1,   1,   1,   1,  99, 100,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1, 101,   1,   1,   1,   1, 102,  31,  31,  31,  31,
      1,   1, 103,  31,  31,  31,  31,  31,
};

static RE_UINT8 re_id_start_stage_4[] = {
      0,   0,   1,   1,   0,   2,   3,   3,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   5,   6,   0,   0,   0,   7,   8,   9,   4,  10,
      4,   4,   4,   4,  11,   4,   4,   4,   4,  12,  13,   4,  14,   0,  15,  16,
      0,   4,  17,  18,   4,   4,  19,  20,  21,  22,  23,   4,   4,  24,  25,  26,
     27,  28,  29,  17,   0,  30,   0,   0,  31,  32,  33,  34,  35,  36,  37,  38,
     39,  40,  41,  42,  43,  44,  45,  46,  47,  44,  48,  49,  50,  51,  45,   0,
     52,  53,  54,  55,  56,  57,  58,  59,  52,  60,  61,  62,  63,  64,  65,   0,
     66,  67,  65,   0,  68,  69,  70,   0,  71,   0,  72,  73,  74,   0,   0,   0,
      4,  75,  76,  77,  78,   4,  79,  80,   4,   4,  81,   4,  82,  83,  84,   4,
     85,   4,  86,   0,  22,   4,   4,  87,  66,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,  88,   1,   4,   4,  89,  90,  91,  91,  92,   4,  93,  94,   0,
      0,   4,   4,  29,   4,  95,   4,  96,  97,   0,  15,  98,   4,  99, 100,   0,
    101,   4, 102,   0,   0, 103,   0,   0, 104,  93, 105,   0, 106, 107,   4, 108,
      4, 109, 110, 111, 112, 113,   0, 114,   4,   4,   4,   4,   4,   4,   0,   0,
     87,   4, 115, 111,   4, 116, 117, 118,   0,   0,   0, 119, 120,   0,   0,   0,
    121, 122, 123,   4,  14,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      4, 124,  97,   4,   4,   4,   4, 125,   4,  79,   4, 126, 101, 127, 127,   0,
    128, 129,  66,   4, 130,  66,   4,  80, 104,  12,   4,   4, 131,  86,   0,  15,
      4,   4,   4,   4,   4,  96,   0,   0,   4,   4,   4,   4,   4,   4,   4,  22,
      4,   4,   4,   4,  73,   0,  15, 111, 132, 133,   4, 134, 111,   4,   4,  22,
    135, 136,   4,   4, 137, 138,   0, 135, 139, 140,   4,  93, 136,  93,   0, 141,
     25, 142,  65, 143,  31, 144, 145, 146,   4,  14, 147, 148,   4, 149, 150, 151,
    152, 153,  80, 142,   4,   4,   4, 140,   4,   4,   4,   4,   4, 154, 155, 156,
      4,   4,   4, 157,   4,   4, 138,   0, 158, 159, 160,   4,   4,  91, 161,   4,
      4, 111,  15,   4, 162,   4, 163, 164,   0,   0,   0, 165,   4,   4,   4, 143,
      0,   1,   1, 166,   4,  97, 167,   0, 168, 169, 170,   0,   4,   4,   4,  86,
      0,   0,   4, 102,   0,   0,   0,   0,   0,   0,   0,   0, 143,   4, 171,   0,
      4,  23, 172,  96, 111,   4, 173,   0,   4,   4,   4,   4, 111,  15, 174, 156,
      4, 175,   4, 109,   0,   0,   0,   0,   4, 101,  96, 163,   0,   0,   0,   0,
    176, 177,  96, 101,  97,   0,   0, 178,  96, 138,   0,   0,   4, 179,   0,   0,
    180,  96,   0, 143, 143,   0,  72, 181,   4,  96,  96, 144,  91,   0,   0,   0,
      4,   4,  14,   0,   4, 144,   4, 144,   4, 109,   0,   0,   0,   0,   0,   0,
    143, 182, 108,   0,   0,   0,   0,   0, 106, 183,   0,   0, 106,  22,  15,  14,
    106,  65, 184, 185, 106, 144, 186,   0, 187, 188,   0,   0, 189, 112,  97,   0,
     47,  44, 190,  55,   0,   0,   0,   0,   4, 102, 191,   0,   4,  22, 192,   0,
      0,   0,   0,   0,   4, 131, 193,   0,   4,  22, 194,   0,   4,  17,   0,   0,
     86,   0,   0,   0,   0,   0,   0,   0,   4, 188,   0,   0,   0,   4,   4, 195,
    196, 197, 198,   4, 199,   0,   4,  29, 200, 131,  71, 201,  22,   0,   0,   0,
    202, 171, 203, 204, 205,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 144,
      4,   4,   4,   4, 138,   0,   0,   0,   4,   4,   4, 131,   4,   4,   4,   4,
      4,   4, 109,   0,   0,   0,   0,   0,   4, 131,   0,   0,   0,   0,   0,   0,
      4,   4,  65,   0,   0,   0,   0,   0,   4,  29,  97,   0,   0,   0,  15, 206,
      4,  22, 109, 207,  22,   0,   0,   0,   0,   0,   4,   4,   0,   0,   0,   0,
      4,   4, 208,   0, 161,   0,   0,  55,   4,   4,   4,   4,   4,   4,   4,  91,
      4,   4,   4,   4,   4,   4,   4, 144,  97,   0,   0,  15,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4, 156,   4,   4,   4, 209, 210,   0,   0,   0,
      4,   4, 211,   4, 212, 213, 214,   4, 215, 216, 217,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4, 218, 219,  80, 211, 211, 124, 124, 200, 200, 147,   0,
      4,   4,   4,   4,   4,   4, 181,   0, 214, 220, 221, 222, 223, 224,   0,   0,
      4,   4,   4,   4,   4,   4, 101,   0,   4, 102,   4,   4,   4,   4,   4,   4,
    111,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 225,   4,   4,
      4,   4,   4,   4,   4,   4,   4,  71, 111,   0,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_id_start_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255,   7,   0,   4,  32,   4, 255, 255, 127, 255,
    255, 255, 255, 255, 195, 255,   3,   0,  31,  80,   0,   0,   0,   0, 223, 188,
     64, 215, 255, 255, 251, 255, 255, 255, 255, 255, 191, 255,   3, 252, 255, 255,
    255, 255, 254, 255, 255, 255, 127,   2, 255,   1,   0,   0,   0,   0, 255, 255,
    255, 135,   7,   0, 255,   7,   0,   0,   0, 192, 254, 255, 255, 255,  47,   0,
     96, 192,   0, 156,   0,   0, 253, 255, 255, 255,   0,   0,   0, 224, 255, 255,
     63,   0,   2,   0,   0, 252, 255, 255, 255,   7,  48,   4, 255, 255,  63,   4,
     16,   1,   0,   0, 255, 255, 255,   1, 255, 255, 223,  63, 240, 255, 255, 255,
    255, 255, 255,  35,   0,   0,   1, 255,   3,   0, 254, 255, 225, 159, 249, 255,
    255, 253, 197,  35,   0,  64,   0, 176,   3,   0,   3,  16, 224, 135, 249, 255,
    255, 253, 109,   3,   0,   0,   0,  94,   0,   0,  28,   0, 224, 191, 251, 255,
    255, 253, 237,  35,   0,   0,   1,   0,   3,   0,   0,   2, 224, 159, 249, 255,
      0,   0,   0, 176,   3,   0,   2,   0, 232, 199,  61, 214,  24, 199, 255,   3,
    224, 223, 253, 255, 255, 253, 255,  35,   0,   0,   0,   7,   3,   0,   0,   0,
    225, 223, 253, 255, 255, 253, 239,  35,   0,   0,   0,  64,   3,   0,   6,   0,
    255, 255, 255,  39,   0,  64, 112, 128,   3,   0,   0, 252, 224, 255, 127, 252,
    255, 255, 251,  47, 127,   0,   0,   0, 254, 255, 255, 255, 255, 255,  13,   0,
    150,  37, 240, 254, 174, 236,  13,  32,  95,   0,   0, 240,   1,   0,   0,   0,
    255, 254, 255, 255, 255,  31,   0,   0,   0,  31,   0,   0, 255,   7,   0, 128,
      0,   0,  63,  60,  98, 192, 225, 255,   3,  64,   0,   0, 191,  32, 255, 255,
    255, 255, 255, 247, 255,  61, 127,  61, 255,  61, 255, 255, 255, 255,  61, 127,
     61, 255, 127, 255, 255, 255,  61, 255, 255, 255, 255,   7, 255, 255,  63,  63,
    255, 159, 255, 255, 255, 199, 255,   1, 255, 223,   3,   0, 255, 255,   3,   0,
    255, 223,   1,   0, 255, 255,  15,   0,   0,   0, 128,  16, 255,   5, 255, 255,
    255, 255,  63,   0, 255, 255, 255, 127, 255,  63,  31,   0, 255,  15, 255, 255,
    255,   3,   0,   0, 255, 255, 127,   0, 255, 255,  31,   0, 128,   0,   0,   0,
    224, 255, 255, 255, 224,  15,   0,   0, 248, 255, 255, 255,   1, 192,   0, 252,
     63,   0,   0,   0,  15,   0,   0,   0,   0, 224,   0, 252, 255, 255, 255,  63,
    255,   1, 255, 255, 255, 255, 255, 231,   0, 222,  99,   0,  63,  63, 255, 170,
    255, 255, 223,  95, 220,  31, 207,  15, 255,  31, 220,  31,   0,   0,   2, 128,
      0,   0, 255,  31, 132, 252,  47,  63,  80, 253, 255, 243, 224,  67,   0,   0,
    255, 127, 255, 255,  31, 120,  12,   0, 255, 128,   0,   0, 127, 127, 127, 127,
    224,   0,   0,   0, 254,   3,  62,  31, 255, 255, 127, 248, 255, 127,   0,   0,
    255,  31, 255, 255,   0,  12,   0,   0, 255, 127,   0, 128,   0,   0, 128, 255,
    252, 255, 255, 255, 255, 249, 255, 255, 255, 255, 255,   3, 187, 247, 255, 255,
      7,   0,   0,   0,   0,   0, 252, 104,  63,   0, 255, 255, 255, 255, 255,  31,
    255, 255,   7,   0,   0, 128,   0,   0, 223, 255,   0, 124, 247,  15,   0,   0,
    255, 255, 127, 196, 255, 255,  98,  62,   5,   0,   0,  56, 255,   7,  28,   0,
    126, 126, 126,   0, 127, 127, 255, 255,  15,   0, 255, 255, 127, 248, 255, 255,
    255, 255, 255,  15, 255,  63, 255, 255, 127,   0, 248, 160, 255, 253, 127,  95,
    219, 255, 255, 255,   0,   0, 248, 255, 255, 255, 252, 255, 255,   0,   0,   0,
      0,   0, 255,  15,   0,   0, 223, 255, 192, 255, 255, 255, 252, 252, 252,  28,
    255, 239, 255, 255, 127, 255, 255, 183, 255,  63, 255,  63, 255, 255,   1,   0,
    255,   7, 255, 255,  15, 255,  62,   0, 255, 255,  15, 255, 255,   0, 255, 255,
     63, 253, 255, 255, 255, 255, 191, 145, 255, 255,  55,   0, 255, 255, 255, 192,
      1,   0, 239, 254,  31,   0,   0,   0, 128,   0, 255, 255, 255, 255, 255,   0,
     16,   0, 255, 255, 255, 255,  71,   0,  30,   0,   0,  20, 255, 255, 251, 255,
    255,  15,   0,   0, 127, 189, 255, 191,   0,   0,   1, 224, 128,   7,   0,   0,
    176,   0,   0,   0,   0,   0,   0,  15,  16,   0,   0,   0,   0,   0,   0, 128,
      1, 248, 255, 255, 255, 255,   7,   4,   0,   0,   1, 240, 207,   3,   0,  32,
    255, 253, 255, 255,   0,   0, 252, 255, 127, 251, 255, 255,  64,   0,   0,   0,
    191, 253, 255, 255, 255,   3,   0,   1, 255,  63,   0,   0, 248, 255, 255, 224,
     31,   0,   1,   0, 255,   7, 255,  31, 255,   1, 255,   3, 255, 255, 223, 255,
    255, 255, 255, 223, 100, 222, 255, 235, 239, 255, 255, 255, 191, 231, 223, 223,
    255, 255, 255, 123,  95, 252, 253, 255,  63, 255, 255, 255, 253, 255, 255, 247,
    150, 254, 247,  10, 132, 234, 150, 170, 150, 247, 247,  94, 255, 251, 255,  15,
    238, 251, 255,  15,   3,   0, 255, 255,
};

/* ID_Start: 2161 bytes. */

RE_UINT32 re_get_id_start(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_id_start_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_id_start_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_id_start_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_id_start_stage_4[pos + f] << 5;
    pos += code;
    value = (re_id_start_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* ID_Continue. */

static RE_UINT8 re_id_continue_stage_1[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
     3,  3,  3,  3,  3, 16, 17, 18, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    20, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19,
};

static RE_UINT8 re_id_continue_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
    16, 17, 17, 17, 17, 17, 18, 17, 19, 17, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 21, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 22,
    20, 20, 23, 24, 25, 26, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 27, 17, 17, 17, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 28, 29, 30, 31,
    32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
    20, 48, 49, 17, 17, 17, 17, 17, 20, 20, 50, 17, 17, 17, 17, 17,
    17, 17, 20, 51, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
    17, 17, 17, 17, 20, 52, 17, 53, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 54, 20, 55, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 56, 57, 17, 17, 17, 17, 58, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 59, 60, 61, 62, 17, 63, 17, 17,
    64, 17, 17, 17, 65, 17, 17, 66, 17, 17, 17, 17, 17, 17, 17, 17,
    20, 20, 20, 67, 20, 20, 20, 20, 20, 20, 20, 68, 69, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 70, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 71, 17, 17, 17, 17, 17, 17, 20, 72, 17, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
    73, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
};

static RE_UINT8 re_id_continue_stage_3[] = {
      0,   1,   2,   3,   4,   4,   4,   4,   4,   4,   4,   5,   4,   6,   7,   8,
      4,   4,   9,   4,  10,  11,  12,  13,  14,  15,   4,  16,  17,  18,  19,  20,
     21,  22,  23,  24,   4,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,
     36,  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,
      4,  52,  53,  54,   4,   4,   4,   4,   4,  55,  56,  57,  58,  59,  60,  61,
     62,   4,   4,   4,   4,   4,   4,   4,   4,  63,  64,  65,  66,  67,   4,  68,
     69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,   4,  81,   4,  82,
     83,  84,  85,  86,   4,   4,   4,  87,   4,   4,   4,   4,  88,  89,  90,  91,
     92,  93,  94,  95,  96,  97,  98,  80,  80,  80,  80,  80,  80,  80,  80,  80,
     99, 100,   4, 101, 102, 103, 104, 105, 106,  62, 107, 108, 109,   4, 110, 111,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,  72,  80,
      4,   4,   4,   4,   4,   4,   4, 112,   4,   4, 113, 114,   4,   4,   4,   4,
    115, 116,   4,  19, 117,   4, 118, 119, 120,  82,   4, 121, 122, 123,   4, 124,
    125, 126,   4, 127, 128, 129,   4, 130,   4,   4,   4,   4,   4,   4, 131, 132,
     80,  80,  80,  80,   4,   4,   4,   4,   4, 122,   4, 133, 134, 135,  19, 136,
      4,   4,   4,   4, 137,  17, 138, 139, 140, 141,   4, 142, 143, 144, 145, 146,
    147, 148,   4, 149,  80, 150,  80, 151,  80,  80, 152, 153, 154, 155,  53, 156,
      4,   4, 157, 158, 159, 160,  80,  80,   4,   4,   4,   4, 125, 161,  80,  80,
    162, 163, 164, 165, 166,  80, 167,  80, 168, 169, 170, 171,  72, 172, 173,  80,
      4,  98, 174, 174, 175,  80,  80,  80,  80,  80,  80,  80, 176, 177,  80,  80,
      4, 178, 149, 179, 180, 181,   4, 182, 183,  80, 184, 185, 186, 187,  80,  80,
      4, 188,   4, 189,  80,  80, 190, 191,   4, 192,  83, 193, 194,  80,  80,  80,
    149,  80, 195, 196,  80,  80,  80,  80, 145, 197, 198,  70,  80,  80,  80,  80,
    199, 200, 201,  80, 202, 203, 204,  80,  80,  80,  80, 205,  80,  80,  80,  80,
      4,   4,   4,   4,   4,   4, 133,  80,   4, 206,   4,   4,   4, 207,  80,  80,
    206,  80,  80,  80,  80,  80,  80,  80,   4, 208,  80,  80,  80,  80,  80,  80,
     70, 209,  80, 210, 125, 211, 212,  80,  80,   4,  80,  80,   4, 213, 214, 215,
      4,   4,   4,   4,   4,   4,   4,  19,   4,   4,   4, 174,  80,  80,  80,  80,
      4,   4,   4,   4, 164, 111,   4,   4,   4,   4,   4, 216,  80,  80,  80,  80,
      4, 217, 218,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80, 219, 220,  80,
     80, 221,  80,  80,  80,  80,  80,  80,   4, 222, 223, 224, 225, 226,   4,   4,
      4,   4, 227, 228, 229, 230, 231, 232, 233, 234, 235,  80,  80,  80,  80,  80,
    236,  80,  80,  80,  80,  80,  80,  80,   4,   4,   4, 237,   4, 238,  80,  80,
    239, 240, 241,  80,  80,  80,  80,  80,   4,   4,   4, 242,   4,   4,   4,   4,
      4,   4,   4,   4, 150,   4,   4,   4,  53,   4,   4,   4,   4,   4,   4,   4,
      4,   4, 243,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 244,
    245,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,   4,   4,   4, 112,
};

static RE_UINT8 re_id_continue_stage_4[] = {
      0,   0,   0,   1,   2,   3,   2,   4,   0,   0,   5,   6,   7,   8,   7,   8,
      7,   7,   7,   7,   9,  10,  11,   0,   7,   7,   7,  12,  13,   7,  14,   7,
      7,   7,   7,  15,  16,   7,   7,   7,   7,   7,   7,   2,   7,  17,   7,   7,
     18,   2,   7,  19,  20,   7,   3,  21,   0,   4,   7,   7,   7,   7,  22,   7,
      7,  23,  24,  25,   0,   7,   7,   7,  26,   7,   7,   7,   7,   7,   7,  10,
      7,   7,   7,  27,   7,   7,  28,   0,   7,  29,   4,   0,   0,   0,   7,  30,
      0,  31,  14,   7,   7,   7,  32,   2,  23,  33,  24,  34,  35,  36,  32,  37,
     38,  33,  24,  39,  40,  41,  42,  43,  44,  14,  24,  45,  46,  47,  32,  48,
     49,  33,  24,  45,  50,  51,  32,  52,  53,  54,  55,  22,  56,  57,  42,   0,
     58,  59,  24,  60,  61,  62,  32,   0,  63,  59,  24,  64,  61,  65,  32,  66,
     63,  59,   7,   7,  67,  68,  32,  69,  70,  71,   7,  72,  73,  74,  42,  75,
      2,   7,   7,   4,  76,   1,   0,   0,  77,  78,  79,  80,  81,  82,   0,   0,
     47,  83,   1,  84,  85,   7,  86,   2,  87,  85,   7,  86,  88,   0,   0,   0,
      1,   7,   7,   7,   7,  28,   7,   7,  89,   7,   7,  90,  91,  92,   7,   7,
     91,   7,   7,  93,  94,   8,   7,   7,   7,  94,   7,   7,   7,  26,  48,  10,
      7,   0,   7,   7,   7,   7,   7,  95,   2,   7,   7,   7,   7,   7,  25,   7,
      2,   4,   7,   7,   7,   7,  96,  18,  58,  97,   7,  97,   7,  98,  58,  99,
      7, 100,   1,   0, 101,   1,   7,   7,   7,   7,   7,  18,   7,   7,   4,   7,
      7,   7,   7,  43,   7,  76,  29,  29,  42,   7,  28,  97,   7,   7,  29,   7,
      1,   4,   0,   0,   7,  29,   7,   7,   7,  76,   7,  25,   1,   1, 102,  28,
      0,   0,   0,   0,  29,   1, 103,  98,   7,   7,   7,  98,   7,   7,   7, 104,
     60,   7,   7,  28,  18,   7,   7,  26,   0, 105,   7,   1,   7,   7,   7, 106,
      7,  95,   7,   7,  95, 107,   7,  28,   7,   7,   7, 108, 109, 110,  86, 109,
      0,   0,   0, 111,  47, 112,   0, 113,   0,  86,   0,   0,   0,  86, 114,  47,
    115, 116, 117,  82, 118,   0,   7,   7,  18,   0,   0,   0,   7,   7,  76,   7,
      7,  76,   7,   7,   7,   7, 119,  98,   7,   7,  89,   7,   7,   7, 120, 111,
      7, 121, 122, 122, 122, 122,   7,   7, 123,   0,   2, 124,   7, 125,   2,   7,
      7,   7,   7,  90, 126,   7,   7,   2,  76,   0,   7,   4,   0,   0,   0,   7,
      7,   7,   7,   0,  86,   0,   0,   0,   0,   7,   7,  28,  86,   7,  29,   0,
      7,   7,   7, 127,   0, 128, 129,   7, 130,   7,   7,   1,   0,   0,   0, 128,
      7,   7, 104,   0,  43,   1,   7, 131,   7,   7,  28,   7,   7,  98,   7,  86,
    132,   1,   7,  76,   7,   7,   7, 121,  28,   1,   7,  71,  21, 101,   7, 133,
    134, 135, 122,   7,   7,  90,  43,   7,   7,   7, 136,   1,   7,   7,  98,   7,
    137,   7,   7,  29,   7,   1,   0,   0, 121, 138,  24, 139, 140,   7,   7,   7,
      0,  31,   7,   7,   7,   7,   7,  28,   7, 129,   7,   7, 104,   0,   0,  29,
      7,   0,   7, 141, 142,   0,   0,  87,   7,   7,   7,  86,   0,   1,   2,   3,
      2,   4,  42,   7,   7,   7,   7,  76, 143, 144,   0,   0, 145,   7,   8, 146,
     28,  28,   0,   0,   7,   7,   7,   4,   7,   7,   7,  97,   0,   0,   0, 147,
      7,  86,   7,   7,   7,  47,  47,   0,   7,   7, 142,   7,   4,   7,   7,   4,
    148, 149,   0,   0,   7,  28,   1,   7,   7, 148,   7,  29,   7,   7, 104,   7,
      7,   7,  98,   0,   7,  43, 104,   0, 150,   7,   7, 151,   7,  43,   7, 121,
      7,  76,   0,   0,   0,   0,   7, 152,   7,  43,   7,   1,   7,   7,   7, 153,
    154, 155,   7, 156,   0,   0,   7,  86,   7,  86,   0,   0,  85,   7, 121,   0,
      7,  43,   7,  21,   7,  10,   0,   0,   7,   7,   7,  21,   7,   7, 104,   1,
      7,  86, 102,   7,   7,  47,   0,   0, 121,   0,  42, 111,   0,   7,  18,   1,
      7,   7,   7,  87, 157,   7,   7, 158, 159, 160,   0,   0,   7,  14,   7, 161,
    162,  19,  18,   7,   7,   7,   4,   1,  23,  33,  24, 163,  50, 164, 165,  97,
      4, 166,   0,   0, 167,   1,   0,   0,   7,   7,   7, 168,  47, 169,   0,   0,
    170,   1,   0,   0,   1,   0,   0,   0,   7,  26,  29,   1,   0,   0,   7,   7,
      7,   7,   1, 111, 102,   7,   7,   7,  32, 171,   0,   0,  24,   7,   7,   8,
     47,   1,   0, 129,   7, 129,  85, 121, 172,   7,   7, 173, 104,   1, 174,   7,
     76, 175,   1,   0,   0,   0,   7, 121,   7,   7,  76,   0,  98,   0,   0,   0,
    121,   0,   0,   0,   7,  76,   1,   0,   0,   7,  28,  97,  98,   1,  31, 176,
      7,   0,   0,   0,  97,   7,   7,  76, 111,   7,   0,   0,   0,   0,  10,   0,
      7,   7,   7,  29,   7,   7,   4,  86,  18, 177,   0,   0,   0,   0, 178, 179,
    180,   0, 181,   0, 182,   0,   0,   0,   7,  87,   7,   7,   7,  58, 183, 184,
    185,   7,   7,   7, 186, 187,   7, 188, 189,  59,   7,   7,   7,   7, 168,   7,
     59,  90,   7,  90,   7,  87,   7,  87,  76,   7,  76,   7,  24,   7,  24,   7,
    190,   7,   7,   7,   7,   7,   7, 137,   7,   7,  86, 191, 112, 103,   2,   0,
      8, 130, 192,   0,  97, 121,   0,   0,   4,   1,   0,   0, 185,   7, 193, 194,
    195, 196, 197, 198, 106,  29, 199,  29,   7, 121,   0,   0,   7,   7,  10,   7,
      7,   7,  47,   0,   7,  28,   0,   0,
};

static RE_UINT8 re_id_continue_stage_5[] = {
      0,   0, 255,   3, 254, 255, 255, 135, 255,   7,   0,   4, 160,   4, 255, 255,
    127, 255, 195, 255,   3,   0,  31,  80, 223, 188, 192, 215, 251, 255, 191, 255,
    251, 252, 127,   2, 255,   1, 255, 191, 182,   0,   7,   0, 255, 195, 239, 159,
    255, 253, 255, 159, 255, 231,  63,  36, 255,  63, 255,  15, 223,  63, 248, 255,
    207, 255, 249, 255, 197, 243, 159, 121, 128, 176,   3,  80, 238, 135, 109, 211,
    135,  57,   2,  94, 192, 255,  63,   0, 238, 191, 237, 243, 191,  59,   1,   0,
      0, 254, 238, 159, 159,  57, 192, 176,   2,   0, 236, 199,  61, 214,  24, 199,
    199,  61, 129,   0, 255, 223, 253, 255, 255, 227, 223,  61,  96,   7, 239, 223,
    239, 243,  96,  64,   6,   0, 223, 125, 240, 128,   0, 252, 236, 255, 127, 252,
    251,  47, 127, 132,  95, 255,  12,   0, 255, 127, 150,  37, 240, 254, 174, 236,
    255,  59,  95,  63, 255, 243,   0,   3, 160, 194, 255, 254, 255,  31, 223, 255,
     64,   0, 191,  32, 255, 247, 255,  61, 127,  61,  61, 127,  61, 255,  63,  63,
    255, 199,  31,   0,  15,   0,  13,   0, 143,  48,   0,  56, 128,   0,   0, 248,
    255,   0, 247, 255, 255, 251, 255, 170, 223,  95, 220,  31, 207,  15,   0, 128,
     16,   0,   2, 128, 226, 255, 132, 252,  47,  63,  80, 253, 224,  67,  31, 248,
    255, 128, 127,   0, 127, 127, 224,   0,  62,  31, 127, 254, 224, 255, 240, 191,
    128, 255, 252, 255, 255, 249, 255, 232,   1, 128, 124,   0, 126, 126, 126,   0,
    255,  55, 127, 248, 248, 224, 127,  95, 219, 255,  24,   0,   0, 224, 252, 252,
    252,  28, 255, 239, 255, 183,   0,  32,  15, 255,  62,   0,  63, 253, 191, 145,
     55,   0, 255, 192, 111, 240, 239, 254,  63, 135, 112,   0,  79,   0,  31,  30,
    255,  23, 255,  64, 127, 189, 237, 251, 129, 224, 207,  31, 255,  67, 191,   0,
     63, 255,   0,  63,  17,   0, 255,  35, 127, 251, 127, 180, 191, 253, 251,   1,
    255, 224, 255,  99, 224, 227,   7, 248, 231,  15,   0,  60,  28,   0, 100, 222,
    255, 235, 239, 255, 191, 231, 223, 223, 255, 123,  95, 252, 247, 207,  32,   0,
    219,   7, 150, 254, 247,  10, 132, 234, 150, 170, 150, 247, 247,  94, 238, 251,
};

/* ID_Continue: 2448 bytes. */

RE_UINT32 re_get_id_continue(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 13;
    code = ch ^ (f << 13);
    pos = (RE_UINT32)re_id_continue_stage_1[f] << 4;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_id_continue_stage_2[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_id_continue_stage_3[pos + f] << 2;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_id_continue_stage_4[pos + f] << 4;
    pos += code;
    value = (re_id_continue_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* XID_Start. */

static RE_UINT8 re_xid_start_stage_1[] = {
    0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3,
};

static RE_UINT8 re_xid_start_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  9, 10, 11,  7,  7,  7,  7, 12, 13, 13, 13, 13, 14,
    15, 16, 17, 18, 19, 13, 20, 13, 21, 13, 13, 13, 13, 22,  7,  7,
    23, 24, 13, 13, 13, 13, 25, 26, 13, 13, 27, 13, 13, 28, 13, 13,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7, 29,  7, 30, 31,  7, 32,  7,  7,  7, 33, 13, 34,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
};

static RE_UINT8 re_xid_start_stage_3[] = {
      0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,
     16,   1,  17,  18,  19,   1,  20,  21,  22,  23,  24,  25,  26,  27,   1,  28,
     29,  30,  31,  31,  31,  31,  31,  31,  31,  31,  31,  31,  32,  33,  31,  31,
     34,  35,  31,  31,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,  36,   1,   1,   1,   1,   1,   1,   1,   1,   1,  37,
      1,   1,   1,   1,  38,   1,  39,  40,  41,  42,  43,  44,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,  45,  31,  31,  31,  31,  31,  31,  31,  31,
     31,   1,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,  56,  57,   1,  58,
     59,  60,  61,  62,  63,  64,  31,  65,  66,  67,  68,  69,  70,  71,  72,  73,
     74,  31,  75,  31,  76,  77,  78,  31,   1,   1,   1,  79,  80,  81,  31,  31,
      1,   1,   1,   1,  82,  31,  31,  31,  31,  31,  31,  31,   1,   1,  83,  31,
      1,   1,  84,  85,  31,  31,  86,  87,   1,   1,   1,   1,   1,   1,   1,  88,
      1,   1,  89,  31,  31,  31,  31,  31,   1,  90,  91,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  92,  31,  31,  31,  31,  31,  31,  31,  93,  94,  95,  96,
     97,  81,  31,  31,  31,  31,  98,  31,   1,   1,   1,   1,   1,   1,  99,   1,
      1,   1,   1,   1,   1,   1,   1, 100, 101,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1, 102,   1,   1,   1,   1, 103,  31,  31,  31,  31,
      1,   1, 104,  31,  31,  31,  31,  31,
};

static RE_UINT8 re_xid_start_stage_4[] = {
      0,   0,   1,   1,   0,   2,   3,   3,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   5,   6,   0,   0,   0,   7,   8,   9,   4,  10,
      4,   4,   4,   4,  11,   4,   4,   4,   4,  12,  13,   4,  14,   0,  15,  16,
      0,   4,  17,  18,   4,   4,  19,  20,  21,  22,  23,   4,   4,  24,  25,  26,
     27,  28,  29,  17,   0,  30,   0,   0,  31,  32,  33,  34,  35,  36,  37,  38,
     39,  40,  41,  42,  43,  44,  45,  46,  47,  44,  48,  49,  50,  51,  45,   0,
     52,  53,  54,  55,  56,  57,  58,  59,  52,  60,  61,  62,  63,  64,  65,   0,
     66,  67,  65,   0,  68,  69,  70,   0,  71,   0,  72,  73,  74,   0,   0,   0,
      4,  75,  76,  77,  78,   4,  79,  80,   4,   4,  81,   4,  82,  83,  84,   4,
     85,   4,  86,   0,  22,   4,   4,  87,  66,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,  88,   1,   4,   4,  89,  90,  91,  91,  92,   4,  93,  94,   0,
      0,   4,   4,  29,   4,  95,   4,  96,  97,   0,  15,  98,   4,  99, 100,   0,
    101,   4, 102,   0,   0, 103,   0,   0, 104,  93, 105,   0, 106, 107,   4, 108,
      4, 109, 110, 111, 112, 113,   0, 114,   4,   4,   4,   4,   4,   4,   0,   0,
     87,   4, 115, 111,   4, 116, 117, 118,   0,   0,   0, 119, 120,   0,   0,   0,
    121, 122, 123,   4,  14,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      4, 124,  97,   4,   4,   4,   4, 125,   4,  79,   4, 126, 101, 127, 127,   0,
    128, 129,  66,   4, 130,  66,   4,  80, 104,  12,   4,   4, 131,  86,   0,  15,
      4,   4,   4,   4,   4,  96,   0,   0,   4,   4,   4,   4,   4,   4,   4,  22,
      4,   4,   4,   4,  73,   0,  15, 111, 132, 133,   4, 134, 111,   4,   4,  22,
    135, 136,   4,   4, 137, 138,   0, 135, 139, 140,   4,  93, 136,  93,   0, 141,
     25, 142,  65, 143,  31, 144, 145, 146,   4,  14, 147, 148,   4, 149, 150, 151,
    152, 153,  80, 142,   4,   4,   4, 140,   4,   4,   4,   4,   4, 154, 155, 156,
      4,   4,   4, 157,   4,   4, 138,   0, 158, 159, 160,   4,   4,  91, 161,   4,
      4,   4, 111,  31,   4,   4,   4,   4,   4, 111,  15,   4, 162,   4, 163, 164,
      0,   0,   0, 165,   4,   4,   4, 143,   0,   1,   1, 166, 111,  97, 167,   0,
    168, 169, 170,   0,   4,   4,   4,  86,   0,   0,   4, 102,   0,   0,   0,   0,
      0,   0,   0,   0, 143,   4, 171,   0,   4,  23, 172,  96, 111,   4, 173,   0,
      4,   4,   4,   4, 111,  15, 174, 156,   4, 175,   4, 109,   0,   0,   0,   0,
      4, 101,  96, 163,   0,   0,   0,   0, 176, 177,  96, 101,  97,   0,   0, 178,
     96, 138,   0,   0,   4, 179,   0,   0, 180,  96,   0, 143, 143,   0,  72, 181,
      4,  96,  96, 144,  91,   0,   0,   0,   4,   4,  14,   0,   4, 144,   4, 144,
      4, 109,   0,   0,   0,   0,   0,   0, 143, 182, 108,   0,   0,   0,   0,   0,
    106, 183,   0,   0, 106,  22,  15,  14, 106,  65, 184, 185, 106, 144, 186,   0,
    187, 188,   0,   0, 189, 112,  97,   0,  47,  44, 190,  55,   0,   0,   0,   0,
      4, 102, 191,   0,   4,  22, 192,   0,   0,   0,   0,   0,   4, 131, 193,   0,
      4,  22, 194,   0,   4,  17,   0,   0,  86,   0,   0,   0,   0,   0,   0,   0,
      4, 188,   0,   0,   0,   4,   4, 195, 196, 197, 198,   4, 199,   0,   4,  29,
    200, 131,  71, 201,  22,   0,   0,   0, 202, 171, 203, 204, 205,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0, 144,   4,   4,   4,   4, 138,   0,   0,   0,
      4,   4,   4, 131,   4,   4,   4,   4,   4,   4, 109,   0,   0,   0,   0,   0,
      4, 131,   0,   0,   0,   0,   0,   0,   4,   4,  65,   0,   0,   0,   0,   0,
      4,  29,  97,   0,   0,   0,  15, 206,   4,  22, 109, 207,  22,   0,   0,   0,
      0,   0,   4,   4,   0,   0,   0,   0,   4,   4, 208,   0, 161,   0,   0,  55,
      4,   4,   4,   4,   4,   4,   4,  91,   4,   4,   4,   4,   4,   4,   4, 144,
     97,   0,   0,  15,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 156,
      4,   4,   4, 209, 210,   0,   0,   0,   4,   4, 211,   4, 212, 213, 214,   4,
    215, 216, 217,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 218, 219,  80,
    211, 211, 124, 124, 200, 200, 147,   0,   4,   4,   4,   4,   4,   4, 181,   0,
    214, 220, 221, 222, 223, 224,   0,   0,   4,   4,   4,   4,   4,   4, 101,   0,
      4, 102,   4,   4,   4,   4,   4,   4, 111,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4, 225,   4,   4,   4,   4,   4,   4,   4,   4,   4,  71,
    111,   0,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_xid_start_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255,   7,   0,   4,  32,   4, 255, 255, 127, 255,
    255, 255, 255, 255, 195, 255,   3,   0,  31,  80,   0,   0,   0,   0, 223, 184,
     64, 215, 255, 255, 251, 255, 255, 255, 255, 255, 191, 255,   3, 252, 255, 255,
    255, 255, 254, 255, 255, 255, 127,   2, 255,   1,   0,   0,   0,   0, 255, 255,
    255, 135,   7,   0, 255,   7,   0,   0,   0, 192, 254, 255, 255, 255,  47,   0,
     96, 192,   0, 156,   0,   0, 253, 255, 255, 255,   0,   0,   0, 224, 255, 255,
     63,   0,   2,   0,   0, 252, 255, 255, 255,   7,  48,   4, 255, 255,  63,   4,
     16,   1,   0,   0, 255, 255, 255,   1, 255, 255, 223,  63, 240, 255, 255, 255,
    255, 255, 255,  35,   0,   0,   1, 255,   3,   0, 254, 255, 225, 159, 249, 255,
    255, 253, 197,  35,   0,  64,   0, 176,   3,   0,   3,  16, 224, 135, 249, 255,
    255, 253, 109,   3,   0,   0,   0,  94,   0,   0,  28,   0, 224, 191, 251, 255,
    255, 253, 237,  35,   0,   0,   1,   0,   3,   0,   0,   2, 224, 159, 249, 255,
      0,   0,   0, 176,   3,   0,   2,   0, 232, 199,  61, 214,  24, 199, 255,   3,
    224, 223, 253, 255, 255, 253, 255,  35,   0,   0,   0,   7,   3,   0,   0,   0,
    225, 223, 253, 255, 255, 253, 239,  35,   0,   0,   0,  64,   3,   0,   6,   0,
    255, 255, 255,  39,   0,  64, 112, 128,   3,   0,   0, 252, 224, 255, 127, 252,
    255, 255, 251,  47, 127,   0,   0,   0, 254, 255, 255, 255, 255, 255,   5,   0,
    150,  37, 240, 254, 174, 236,   5,  32,  95,   0,   0, 240,   1,   0,   0,   0,
    255, 254, 255, 255, 255,  31,   0,   0,   0,  31,   0,   0, 255,   7,   0, 128,
      0,   0,  63,  60,  98, 192, 225, 255,   3,  64,   0,   0, 191,  32, 255, 255,
    255, 255, 255, 247, 255,  61, 127,  61, 255,  61, 255, 255, 255, 255,  61, 127,
     61, 255, 127, 255, 255, 255,  61, 255, 255, 255, 255,   7, 255, 255,  63,  63,
    255, 159, 255, 255, 255, 199, 255,   1, 255, 223,   3,   0, 255, 255,   3,   0,
    255, 223,   1,   0, 255, 255,  15,   0,   0,   0, 128,  16, 255,   5, 255, 255,
    255, 255,  63,   0, 255, 255, 255, 127, 255,  63,  31,   0, 255,  15, 255, 255,
    255,   3,   0,   0, 255, 255, 127,   0, 255, 255,  31,   0, 128,   0,   0,   0,
    224, 255, 255, 255, 224,  15,   0,   0, 248, 255, 255, 255,   1, 192,   0, 252,
     63,   0,   0,   0,  15,   0,   0,   0,   0, 224,   0, 252, 255, 255, 255,  63,
    255,   1, 255, 255, 255, 255, 255, 231,   0, 222,  99,   0,  63,  63, 255, 170,
    255, 255, 223,  95, 220,  31, 207,  15, 255,  31, 220,  31,   0,   0,   2, 128,
      0,   0, 255,  31, 132, 252,  47,  63,  80, 253, 255, 243, 224,  67,   0,   0,
    255, 127, 255, 255,  31, 120,  12,   0, 255, 128,   0,   0, 127, 127, 127, 127,
    224,   0,   0,   0, 254,   3,  62,  31, 255, 255, 127, 224, 255, 127,   0,   0,
    255,  31, 255, 255,   0,  12,   0,   0, 255, 127,   0, 128,   0,   0, 128, 255,
    252, 255, 255, 255, 255, 249, 255, 255, 255, 255, 255,   3, 187, 247, 255, 255,
      7,   0,   0,   0,   0,   0, 252, 104,  63,   0, 255, 255, 255, 255, 255,  31,
    255, 255,   7,   0,   0, 128,   0,   0, 223, 255,   0, 124, 247,  15,   0,   0,
    255, 255, 127, 196, 255, 255,  98,  62,   5,   0,   0,  56, 255,   7,  28,   0,
    126, 126, 126,   0, 127, 127, 255, 255,  15,   0, 255, 255, 127, 248, 255, 255,
    255, 255, 255,  15, 255,  63, 255, 255, 127,   0, 248, 160, 255, 253, 127,  95,
    219, 255, 255, 255,   0,   0, 248, 255, 255, 255, 252, 255, 255,   0,   0,   0,
      0,   0, 255,   3,   0,   0, 138, 170, 192, 255, 255, 255, 252, 252, 252,  28,
    255, 239, 255, 255, 127, 255, 255, 183, 255,  63, 255,  63, 255, 255,   1,   0,
    255,   7, 255, 255,  15, 255,  62,   0, 255, 255,  15, 255, 255,   0, 255, 255,
     63, 253, 255, 255, 255, 255, 191, 145, 255, 255,  55,   0, 255, 255, 255, 192,
      1,   0, 239, 254,  31,   0,   0,   0, 128,   0, 255, 255, 255, 255, 255,   0,
     16,   0, 255, 255, 255, 255,  71,   0,  30,   0,   0,  20, 255, 255, 251, 255,
    255,  15,   0,   0, 127, 189, 255, 191,   0,   0,   1, 224, 128,   7,   0,   0,
    176,   0,   0,   0,   0,   0,   0,  15,  16,   0,   0,   0,   0,   0,   0, 128,
      1, 248, 255, 255, 255, 255,   7,   4,   0,   0,   1, 240, 207,   3,   0,  32,
    255, 253, 255, 255,   0,   0, 252, 255, 127, 251, 255, 255,  64,   0,   0,   0,
    191, 253, 255, 255, 255,   3,   0,   1, 255,  63,   0,   0, 248, 255, 255, 224,
     31,   0,   1,   0, 255,   7, 255,  31, 255,   1, 255,   3, 255, 255, 223, 255,
    255, 255, 255, 223, 100, 222, 255, 235, 239, 255, 255, 255, 191, 231, 223, 223,
    255, 255, 255, 123,  95, 252, 253, 255,  63, 255, 255, 255, 253, 255, 255, 247,
    150, 254, 247,  10, 132, 234, 150, 170, 150, 247, 247,  94, 255, 251, 255,  15,
    238, 251, 255,  15,   3,   0, 255, 255,
};

/* XID_Start: 2169 bytes. */

RE_UINT32 re_get_xid_start(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_xid_start_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_xid_start_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_xid_start_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_xid_start_stage_4[pos + f] << 5;
    pos += code;
    value = (re_xid_start_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* XID_Continue. */

static RE_UINT8 re_xid_continue_stage_1[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
     3,  3,  3,  3,  3, 16, 17, 18, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    20, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19,
};

static RE_UINT8 re_xid_continue_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
    16, 17, 17, 17, 17, 17, 18, 17, 19, 17, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 21, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 22,
    20, 20, 23, 24, 25, 26, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 27, 17, 17, 17, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 28, 29, 30, 31,
    32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
    20, 48, 49, 17, 17, 17, 17, 17, 20, 20, 50, 17, 17, 17, 17, 17,
    17, 17, 20, 51, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
    17, 17, 17, 17, 20, 52, 17, 53, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 54, 20, 55, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 56, 57, 17, 17, 17, 17, 58, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 59, 60, 61, 62, 17, 63, 17, 17,
    64, 17, 17, 17, 65, 17, 17, 66, 17, 17, 17, 17, 17, 17, 17, 17,
    20, 20, 20, 67, 20, 20, 20, 20, 20, 20, 20, 68, 69, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 70, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 71, 17, 17, 17, 17, 17, 17, 20, 72, 17, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
    73, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
};

static RE_UINT8 re_xid_continue_stage_3[] = {
      0,   1,   2,   3,   4,   4,   4,   4,   4,   4,   4,   5,   4,   6,   7,   8,
      4,   4,   9,   4,  10,  11,  12,  13,  14,  15,   4,  16,  17,  18,  19,  20,
     21,  22,  23,  24,   4,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,
     36,  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,
      4,  52,  53,  54,   4,   4,   4,   4,   4,  55,  56,  57,  58,  59,  60,  61,
     62,   4,   4,   4,   4,   4,   4,   4,   4,  63,  64,  65,  66,  67,   4,  68,
     69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,   4,  81,   4,  82,
     83,  84,  85,  86,   4,   4,   4,  87,   4,   4,   4,   4,  88,  89,  90,  91,
     92,  93,  94,  95,  96,  97,  98,  80,  80,  80,  80,  80,  80,  80,  80,  80,
     99, 100,   4, 101, 102, 103, 104, 105, 106,  62, 107, 108, 109,   4, 110, 111,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,  72,  80,
      4,   4,   4,   4,   4,   4,   4, 112,   4,   4, 113, 114,   4,   4,   4,   4,
    115, 116,   4,  19, 117,   4, 118, 119, 120,  82,   4, 121, 122, 123,   4, 124,
    125, 126,   4, 127, 128, 129,   4, 130,   4,   4,   4,   4,   4,   4, 131, 132,
     80,  80,  80,  80,   4,   4,   4,   4,   4, 122,   4, 133, 134, 135,  19, 136,
      4, 137,   4,   4, 138,  17, 139, 140, 141, 142,   4, 143, 144, 145, 146, 147,
    148, 149,   4, 150,  80, 151,  80, 152,  80,  80, 153, 154, 155, 156,  53, 157,
      4,   4, 158, 159, 160, 161,  80,  80,   4,   4,   4,   4, 125, 162,  80,  80,
    163, 164, 165, 166, 167,  80, 168,  80, 169, 170, 171, 172,  72, 173, 174,  80,
      4,  98, 175, 175, 176,  80,  80,  80,  80,  80,  80,  80, 177, 178,  80,  80,
      4, 179, 150, 180, 181, 182,   4, 183, 184,  80, 185, 186, 187, 188,  80,  80,
      4, 189,   4, 190,  80,  80, 191, 192,   4, 193,  83, 194, 195,  80,  80,  80,
    150,  80, 196, 197,  80,  80,  80,  80, 146, 198, 199,  70,  80,  80,  80,  80,
    200, 201, 202,  80, 203, 204, 205,  80,  80,  80,  80, 206,  80,  80,  80,  80,
      4,   4,   4,   4,   4,   4, 133,  80,   4, 207,   4,   4,   4, 208,  80,  80,
    207,  80,  80,  80,  80,  80,  80,  80,   4, 209,  80,  80,  80,  80,  80,  80,
     70, 210,  80, 211, 125, 212, 213,  80,  80,   4,  80,  80,   4, 214, 215, 216,
      4,   4,   4,   4,   4,   4,   4,  19,   4,   4,   4, 175,  80,  80,  80,  80,
      4,   4,   4,   4, 165, 111,   4,   4,   4,   4,   4, 217,  80,  80,  80,  80,
      4, 218, 219,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80, 220, 221,  80,
     80, 222,  80,  80,  80,  80,  80,  80,   4, 223, 224, 225, 226, 227,   4,   4,
      4,   4, 228, 229, 230, 231, 232, 233, 234, 235, 236,  80,  80,  80,  80,  80,
    237,  80,  80,  80,  80,  80,  80,  80,   4,   4,   4, 238,   4, 239,  80,  80,
    240, 241, 242,  80,  80,  80,  80,  80,   4,   4,   4, 243,   4,   4,   4,   4,
      4,   4,   4,   4, 151,   4,   4,   4,  53,   4,   4,   4,   4,   4,   4,   4,
      4,   4, 244,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 245,
    246,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80,   4,   4,   4, 112,
};

static RE_UINT8 re_xid_continue_stage_4[] = {
      0,   0,   0,   1,   2,   3,   2,   4,   0,   0,   5,   6,   7,   8,   7,   8,
      7,   7,   7,   7,   9,  10,  11,   0,   7,   7,   7,  12,  13,   7,  14,   7,
      7,   7,   7,  15,  16,   7,   7,   7,   7,   7,   7,   2,   7,  17,   7,   7,
     18,   2,   7,  19,  20,   7,   3,  21,   0,   4,   7,   7,   7,   7,  22,   7,
      7,  23,  24,  25,   0,   7,   7,   7,  26,   7,   7,   7,   7,   7,   7,  10,
      7,   7,   7,  27,   7,   7,  28,   0,   7,  29,   4,   0,   0,   0,   7,  30,
      0,  31,  14,   7,   7,   7,  32,   2,  23,  33,  24,  34,  35,  36,  32,  37,
     38,  33,  24,  39,  40,  41,  42,  43,  44,  14,  24,  45,  46,  47,  32,  48,
     49,  33,  24,  45,  50,  51,  32,  52,  53,  54,  55,  22,  56,  57,  42,   0,
     58,  59,  24,  60,  61,  62,  32,   0,  63,  59,  24,  64,  61,  65,  32,  66,
     63,  59,   7,   7,  67,  68,  32,  69,  70,  71,   7,  72,  73,  74,  42,  75,
      2,   7,   7,   4,  76,   1,   0,   0,  77,  78,  79,  80,  81,  82,   0,   0,
     47,  83,   1,  84,  85,   7,  86,   2,  87,  85,   7,  86,  88,   0,   0,   0,
      1,   7,   7,   7,   7,  28,   7,   7,  89,   7,   7,  90,  91,  92,   7,   7,
     91,   7,   7,  93,  94,   8,   7,   7,   7,  94,   7,   7,   7,  26,  48,  10,
      7,   0,   7,   7,   7,   7,   7,  95,   2,   7,   7,   7,   7,   7,  25,   7,
      2,   4,   7,   7,   7,   7,  96,  18,  58,  97,   7,  97,   7,  98,  58,  99,
      7, 100,   1,   0, 101,   1,   7,   7,   7,   7,   7,  18,   7,   7,   4,   7,
      7,   7,   7,  43,   7,  76,  29,  29,  42,   7,  28,  97,   7,   7,  29,   7,
      1,   4,   0,   0,   7,  29,   7,   7,   7,  76,   7,  25,   1,   1, 102,  28,
      0,   0,   0,   0,  29,   1, 103,  98,   7,   7,   7,  98,   7,   7,   7, 104,
     60,   7,   7,  28,  18,   7,   7,  26,   0, 105,   7,   1,   7,   7,   7, 106,
      7,  95,   7,   7,  95, 107,   7,  28,   7,   7,   7, 108, 109, 110,  86, 109,
      0,   0,   0, 111,  47, 112,   0, 113,   0,  86,   0,   0,   0,  86, 114,  47,
    115, 116, 117,  82, 118,   0,   7,   7,  18,   0,   0,   0,   7,   7,  76,   7,
      7,  76,   7,   7,   7,   7, 119,  98,   7,   7,  89,   7,   7,   7, 120, 111,
      7, 121, 122, 122, 122, 122,   7,   7, 123,   0,   2, 124,   7, 125,   2,   7,
      7,   7,   7,  90, 126,   7,   7,   2,  76,   0,   7,   4,   0,   0,   0,   7,
      7,   7,   7,   0,  86,   0,   0,   0,   0,   7,   7,  28,  86,   7,  29,   0,
      7,   7,   7, 127,   0, 128, 129,   7, 130,   7,   7,   1,   0,   0,   0, 128,
      7,   7, 104,   0,  43,   1,   7, 131,   7,   7,  28,   7,   7,  98,   7,  86,
    132,   1,   7,  76,   7,   7,   7, 121,  28,   1,   7,  71,  21, 101,   7, 133,
    134, 135, 122,   7,   7,  90,  43,   7,   7,   7, 136,   1,   7,   7,  98,   7,
    137,   7,   7,  29,   7,   1,   0,   0, 121, 138,  24, 139, 140,   7,   7,   7,
      0,  31,   7,   7,   7,  28, 141,   7,   7,   7,   7,  28,   7, 129,   7,   7,
    104,   0,   0,   1,   7,   0,   7, 142, 143,   0,   0, 144,   7,   7,   7,  86,
      0,   1,   2,   3,   2,   4,  42,   7,   7,   7,   7,  76, 145, 146,   0,   0,
    147,   7,   8, 148,  28,  28,   0,   0,   7,   7,   7,   4,   7,   7,   7,  97,
      0,   0,   0, 149,   7,  86,   7,   7,   7,  47,  47,   0,   7,   7, 143,   7,
      4,   7,   7,   4, 150, 151,   0,   0,   7,  28,   1,   7,   7, 150,   7,  29,
      7,   7, 104,   7,   7,   7,  98,   0,   7,  43, 104,   0, 152,   7,   7, 153,
      7,  43,   7, 121,   7,  76,   0,   0,   0,   0,   7, 154,   7,  43,   7,   1,
      7,   7,   7, 155, 156, 157,   7, 158,   0,   0,   7,  86,   7,  86,   0,   0,
     85,   7, 121,   0,   7,  43,   7,  21,   7,  10,   0,   0,   7,   7,   7,  21,
      7,   7, 104,   1,   7,  86, 102,   7,   7,  47,   0,   0, 121,   0,  42, 111,
      0,   7,  18,   1,   7,   7,   7,  87, 159,   7,   7, 160, 161, 162,   0,   0,
      7,  14,   7, 163, 164,  19,  18,   7,   7,   7,   4,   1,  23,  33,  24, 165,
     50, 166, 167,  97,   4, 168,   0,   0, 169,   1,   0,   0,   7,   7,   7, 170,
     47, 171,   0,   0, 172,   1,   0,   0,   1,   0,   0,   0,   7,  26,  29,   1,
      0,   0,   7,   7,   7,   7,   1, 111, 102,   7,   7,   7,  32, 173,   0,   0,
     24,   7,   7,   8,  47,   1,   0, 129,   7, 129,  85, 121, 174,   7,   7, 175,
    104,   1, 176,   7,  76, 177,   1,   0,   0,   0,   7, 121,   7,   7,  76,   0,
     98,   0,   0,   0, 121,   0,   0,   0,   7,  76,   1,   0,   0,   7,  28,  97,
     98,   1,  31, 178,   7,   0,   0,   0,  97,   7,   7,  76, 111,   7,   0,   0,
      0,   0,  10,   0,   7,   7,   7,  29,   7,   7,   4,  86,  18, 179,   0,   0,
      0,   0, 180, 181, 182,   0, 183,   0, 184,   0,   0,   0,   7,  87,   7,   7,
      7,  58, 185, 186, 187,   7,   7,   7, 188, 189,   7, 190, 191,  59,   7,   7,
      7,   7, 170,   7,  59,  90,   7,  90,   7,  87,   7,  87,  76,   7,  76,   7,
     24,   7,  24,   7, 192,   7,   7,   7,   7,   7,   7, 137,   7,   7,  86, 193,
    112, 103,   2,   0,   8, 130, 194,   0,  97, 121,   0,   0,   4,   1,   0,   0,
    187,   7, 195, 196, 197, 198, 199, 200, 106,  29, 201,  29,   7, 121,   0,   0,
      7,   7,  10,   7,   7,   7,  47,   0,   7,  28,   0,   0,
};

static RE_UINT8 re_xid_continue_stage_5[] = {
      0,   0, 255,   3, 254, 255, 255, 135, 255,   7,   0,   4, 160,   4, 255, 255,
    127, 255, 195, 255,   3,   0,  31,  80, 223, 184, 192, 215, 251, 255, 191, 255,
    251, 252, 127,   2, 255,   1, 255, 191, 182,   0,   7,   0, 255, 195, 239, 159,
    255, 253, 255, 159, 255, 231,  63,  36, 255,  63, 255,  15, 223,  63, 248, 255,
    207, 255, 249, 255, 197, 243, 159, 121, 128, 176,   3,  80, 238, 135, 109, 211,
    135,  57,   2,  94, 192, 255,  63,   0, 238, 191, 237, 243, 191,  59,   1,   0,
      0, 254, 238, 159, 159,  57, 192, 176,   2,   0, 236, 199,  61, 214,  24, 199,
    199,  61, 129,   0, 255, 223, 253, 255, 255, 227, 223,  61,  96,   7, 239, 223,
    239, 243,  96,  64,   6,   0, 223, 125, 240, 128,   0, 252, 236, 255, 127, 252,
    251,  47, 127, 132,  95, 255,  12,   0, 255, 127, 150,  37, 240, 254, 174, 236,
    255,  59,  95,  63, 255, 243,   0,   3, 160, 194, 255, 254, 255,  31, 223, 255,
     64,   0, 191,  32, 255, 247, 255,  61, 127,  61,  61, 127,  61, 255,  63,  63,
    255, 199,  31,   0,  15,   0,  13,   0, 143,  48,   0,  56, 128,   0,   0, 248,
    255,   0, 247, 255, 255, 251, 255, 170, 223,  95, 220,  31, 207,  15,   0, 128,
     16,   0,   2, 128, 226, 255, 132, 252,  47,  63,  80, 253, 224,  67,  31, 248,
    255, 128, 127,   0, 127, 127, 224,   0,  62,  31, 127, 230, 224, 255, 240, 191,
    128, 255, 252, 255, 255, 249, 255, 232,   1, 128, 124,   0, 126, 126, 126,   0,
    255,  55, 127, 248, 248, 224, 127,  95, 219, 255, 240, 255,  24,   0,   0, 224,
    138, 170, 252, 252, 252,  28, 255, 239, 255, 183,   0,  32,  15, 255,  62,   0,
     63, 253, 191, 145,  55,   0, 255, 192, 111, 240, 239, 254,  63, 135, 112,   0,
     79,   0,  31,  30, 255,  23, 255,  64, 127, 189, 237, 251, 129, 224, 207,  31,
    255,  67, 191,   0,  63, 255,   0,  63,  17,   0, 255,  35, 127, 251, 127, 180,
    191, 253, 251,   1, 255, 224, 255,  99, 224, 227,   7, 248, 231,  15,   0,  60,
     28,   0, 100, 222, 255, 235, 239, 255, 191, 231, 223, 223, 255, 123,  95, 252,
    247, 207,  32,   0, 219,   7, 150, 254, 247,  10, 132, 234, 150, 170, 150, 247,
    247,  94, 238, 251,
};

/* XID_Continue: 2456 bytes. */

RE_UINT32 re_get_xid_continue(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 13;
    code = ch ^ (f << 13);
    pos = (RE_UINT32)re_xid_continue_stage_1[f] << 4;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_xid_continue_stage_2[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_xid_continue_stage_3[pos + f] << 2;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_xid_continue_stage_4[pos + f] << 4;
    pos += code;
    value = (re_xid_continue_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Default_Ignorable_Code_Point. */

static RE_UINT8 re_default_ignorable_code_point_stage_1[] = {
    0, 1, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2,
    2, 2,
};

static RE_UINT8 re_default_ignorable_code_point_stage_2[] = {
    0, 1, 2, 3, 4, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 7, 1, 1, 8, 1, 1, 1, 1, 1,
    9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_default_ignorable_code_point_stage_3[] = {
     0,  1,  1,  2,  1,  1,  3,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  4,  1,  1,  1,  1,  1,  5,  6,  1,  1,  1,  1,  1,  1,  1,
     7,  1,  1,  1,  1,  1,  1,  1,  1,  8,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  9, 10,  1,  1,  1,  1, 11,  1,  1,  1,
     1, 12,  1,  1,  1,  1,  1,  1, 13, 13, 13, 13, 13, 13, 13, 13,
};

static RE_UINT8 re_default_ignorable_code_point_stage_4[] = {
     0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  2,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  4,  5,  0,  0,  0,  0,  0,  0,  0,  0,  0,  6,  0,  0,
     7,  0,  0,  0,  0,  0,  0,  0,  8,  9,  0, 10,  0,  0,  0,  0,
     0,  0,  0, 11,  0,  0,  0,  0, 10,  0,  0,  0,  0,  0,  0,  4,
     0,  0,  0,  0,  0,  5,  0, 12,  0,  0,  0,  0,  0, 13,  0,  0,
     0,  0,  0, 14,  0,  0,  0,  0, 15, 15, 15, 15, 15, 15, 15, 15,
};

static RE_UINT8 re_default_ignorable_code_point_stage_5[] = {
      0,   0,   0,   0,   0,  32,   0,   0,   0, 128,   0,   0,   0,   0,   0,  16,
      0,   0,   0, 128,   1,   0,   0,   0,   0,   0,  48,   0,   0, 120,   0,   0,
      0, 248,   0,   0,   0, 124,   0,   0, 255, 255,   0,   0,  16,   0,   0,   0,
      0,   0, 255,   1,  15,   0,   0,   0,   0,   0, 248,   7, 255, 255, 255, 255,
};

/* Default_Ignorable_Code_Point: 370 bytes. */

RE_UINT32 re_get_default_ignorable_code_point(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_default_ignorable_code_point_stage_1[f] << 4;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_default_ignorable_code_point_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_default_ignorable_code_point_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_default_ignorable_code_point_stage_4[pos + f] << 5;
    pos += code;
    value = (re_default_ignorable_code_point_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Grapheme_Extend. */

static RE_UINT8 re_grapheme_extend_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2,
    2,
};

static RE_UINT8 re_grapheme_extend_stage_2[] = {
     0,  1,  2,  3,  4,  4,  4,  4,  4,  4,  5,  4,  4,  4,  4,  6,
     7,  8,  4,  4,  4,  4,  9,  4,  4,  4,  4, 10,  4, 11, 12,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
    13,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
};

static RE_UINT8 re_grapheme_extend_stage_3[] = {
     0,  0,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13,
    14,  0,  0, 15,  0,  0,  0, 16, 17, 18, 19, 20, 21, 22,  0,  0,
    23,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 24, 25,  0,  0,
    26,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 27,  0, 28, 29, 30, 31,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 32,  0,  0, 33, 34,
     0, 35, 36, 37,  0,  0,  0,  0,  0,  0, 38,  0,  0, 39,  0, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49,  0, 50,  0, 51, 52, 53,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 54, 55,  0,  0,  0, 56,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 57,  0,  0,  0,
     0, 58, 59,  0,  0,  0,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0,
    61,  0,  0,  0,  0,  0,  0,  0, 62, 63,  0,  0,  0,  0,  0,  0,
    64, 65,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_grapheme_extend_stage_4[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   2,   0,   0,   0,   0,
      0,   0,   0,   0,   3,   0,   0,   0,   0,   0,   0,   0,   4,   5,   6,   0,
      7,   0,   8,   9,   0,   0,  10,  11,  12,  13,  14,   0,   0,  15,   0,  16,
     17,  18,  19,   0,   0,   0,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,
     30,  31,  32,  33,  30,  31,  34,  35,  26,  36,  37,  25,  38,  39,  40,   0,
     41,  42,  43,  25,  26,  44,  45,  25,  46,  47,  28,  25,   0,   0,  48,   0,
      0,  49,  50,   0,   0,  51,  52,   0,  53,  54,   0,  55,  56,  57,  58,   0,
      0,  59,  60,  61,  62,   0,   0,   0,   0,   0,  63,   0,   0,   0,   0,   0,
     64,  64,  65,  65,   0,  66,  67,   0,  68,   0,   0,   0,  69,  70,   0,   0,
      0,  71,   0,   0,   0,   0,   0,   0,  72,   0,  73,  74,   0,  75,   0,   0,
     76,  77,  38,  78,  46,  79,   0,  80,   0,  81,   0,   0,   0,   0,  82,  83,
      0,   0,   0,   0,   0,   0,   1,  84,  85,   0,   0,   0,   0,   0,  13,  86,
      0,   0,   0,   0,   0,   0,   0,  87,   0,   0,   0,  88,   0,   0,   0,   1,
      0,  89,   0,   0,  90,   0,   0,   0,   0,   0,   0,  91,  42,   0,   0,  92,
     93,  69,   0,   0,   0,   0,  94,  95,   0,  96,  97,   0,  22,  98,   0,  99,
      0, 100, 101,  31,   0, 102,  26, 103,   0,   0,   0,   0,   0,   0,   0, 104,
     39,   0,   0,   0,   0,   0,   0,   0,   2,   2,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  42,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 105,
      0,   0,   0,   0,   0,   0,   0, 106,   0,   0,   0, 107,   0,   0,   0,   0,
    108, 109,   0,   0,   0,   0,   0,  69,   0, 110,   0,   0,   0,   0,   0,   0,
      0,   0,  15,   0,   0,   0,   0,   0,  26, 111, 112,  88,  46, 113,   0,   0,
     22, 114,   0, 115,  46, 116, 117,   0,   0, 118,   0,   0,   0,   0,  88, 119,
     46,  47, 120, 121,   0,   0,   0,   0,   0, 111, 122,   0,   0, 123, 124,   0,
      0,   0,   0,   0,   0, 125, 126,   0,   0, 127, 106,   0,   0, 128,   0,   0,
     63, 129,   0,   0,   0,   0,   0,   0,   0, 130,   0,   0,   0,   0,   0,   0,
    131, 132, 133,   0, 134,   0,   0,   0,   0, 135,   0,   0, 136, 137,   0,   0,
      0, 138, 139,   0, 140,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 141,
      0,   0,   0,   0,   0,   0,   0, 142,   0, 143,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0, 144,   0,   0,   0,   0,   0,   0,   0, 145,   0,   0,   0,
      0,   0,   0, 146, 147, 148,   0,   0,   0,   0, 149,   0,   0,   0,   0,   0,
      1, 150,   1, 151, 152, 153,   0,   0, 154, 155,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 143,   0,   0,   0, 156,   0,   0,   0,   0,   0,
      0,   1,   1,   1,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1,   2,
};

static RE_UINT8 re_grapheme_extend_stage_5[] = {
      0,   0,   0,   0, 255, 255, 255, 255, 255, 255,   0,   0, 248,   3,   0,   0,
      0,   0, 254, 255, 255, 255, 255, 191, 182,   0,   0,   0,   0,   0, 255,   7,
      0, 248, 255, 255,   0,   0,   1,   0,   0,   0, 192, 159, 159,  61,   0,   0,
      0,   0,   2,   0,   0,   0, 255, 255, 255,   7,   0,   0, 192, 255,   1,   0,
      0, 248,  15,  32,   0,   0, 192, 251, 239,  62,   0,   0,   0,   0,   0,  14,
      0,   0, 248, 255, 251, 255, 255, 255,   7,   0,   0,   0,   0,   0,   0,  20,
    254,  33, 254,   0,  12,   0,   0,   0,   2,   0,   0,   0,   0,   0,   0,  80,
     30,  32, 128,   0,  12,   0,   0,  64,   6,   0,   0,   0,   0,   0,   0,  16,
    134,  57,   2,   0,   0,   0,  35,   0, 190,  33,   0,   0,  12,   0,   0, 252,
      0,   0,   0, 208,  30,  32, 192,   0,   4,   0,   0,   0,   0,   0,   0,  64,
      1,  32, 128,   0,  17,   0,   0,   0,   0,   0,   0, 192, 193,  61,  96,   0,
      0,   0,   0, 144,  68,  48,  96,   0,   3,   0,   0,   0,   0,   0,   0,  88,
      0, 132,  92, 128,   0,   0, 242,   7, 128, 127,   0,   0,   0,   0, 242,  27,
      0,  63,   0,   0,   0,   0,   0,   3,   0,   0, 160,   2,   0,   0, 254, 127,
    223, 224, 255, 254, 255, 255, 255,  31,  64,   0,   0,   0,   0, 224, 253, 102,
      0,   0,   0, 195,   1,   0,  30,   0, 100,  32,   0,  32,   0,   0,   0, 224,
      0,   0,  28,   0,   0,   0,  12,   0,   0,   0, 176,  63,  64, 254,  15,  32,
      0,  56,   0,   0,  96,   0,   0,   0,   0,   2,   0,   0, 135,   1,   4,  14,
      0,   0, 128,   9,   0,   0,  64, 127, 229,  31, 248, 159,   0,   0, 255, 127,
     15,   0,   0,   0,   0,   0, 208,  23,   0, 248,  15,   0,  60,  59,   0,   0,
     64, 163,   3,   0,   0, 240, 207,   0,   0,   0, 247, 255, 253,  33,  16,   3,
    255, 255, 255, 251,   0,  16,   0,   0, 255, 255,   1,   0,   0, 128,   3,   0,
      0,   0,   0, 128,   0, 252,   0,   0,   0,   0,   0,   6,   0, 128, 247,  63,
      0,   0,   3,   0,  68,   8,   0,   0,  48,   0,   0,   0, 255, 255,   3, 128,
    192,  63,   0,   0, 128, 255,   3,   0,   0,   0, 200,  19,  32,   0,   0,   0,
      0, 126, 102,   0,   8,  16,   0,   0,   0,   0, 157, 193,   0,  48,  64,   0,
     32,  33,   0,   0,   0,   0,   0,  32,   1,   0,   0,   0,   0,   0, 192,   7,
    110, 240,   0,   0,   0,   0,   0, 135, 240,   0,   0,   0,   0,   0,   0, 255,
    127,   0,   0,   0,   0,   0, 120,   6, 128, 239,  31,   0,   0,   0,   8,   0,
      0,   0, 192, 127,   0,  30,   0,   0,   0, 128, 211,  64, 248,   7,   0,   0,
      1,   0, 128,   0, 192,  31,  31,   0,  92,   0,   0,  64,   0,   0, 249, 165,
     13,   0,   0,   0,   0, 128,  60, 176,   1,   0,   0,  48,   0,   0, 248, 167,
      0,  40, 191,   0, 188,  15,   0,   0,   0, 128, 255,   6, 254,   7,   0,   0,
      0,   0, 248, 121, 128,   0, 126,  14,   0, 252, 127,   3,   0,   0, 127, 191,
      0,   0, 252, 255, 255, 252, 109,   0,   0,   0, 126, 180, 191,   0,   0,   0,
      0,   0, 163,   0,   0,   0,  24,   0,   0,   0,  31,   0,   0,   0, 127,   0,
      0, 128,   7,   0,   0,   0,   0,  96, 160, 195,   7, 248, 231,  15,   0,   0,
      0,  60,   0,   0,  28,   0,   0,   0, 255, 255, 127, 248, 255,  31,  32,   0,
     16,   0,   0, 248, 254, 255,   0,   0, 127, 255, 255, 249, 219,   7,   0,   0,
    240,   7,   0,   0,
};

/* Grapheme_Extend: 1461 bytes. */

RE_UINT32 re_get_grapheme_extend(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_grapheme_extend_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_grapheme_extend_stage_2[pos + f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_grapheme_extend_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_grapheme_extend_stage_4[pos + f] << 5;
    pos += code;
    value = (re_grapheme_extend_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Grapheme_Base. */

static RE_UINT8 re_grapheme_base_stage_1[] = {
    0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    6, 6,
};

static RE_UINT8 re_grapheme_base_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 13, 13,
    13, 13, 13, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
    13, 13, 13, 13, 13, 13, 13, 15, 13, 16, 17, 13, 13, 13, 13, 13,
    13, 13, 13, 13, 13, 18, 19, 19, 19, 19, 19, 19, 19, 19, 20, 21,
    22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 19, 19, 13, 32, 19, 19,
    19, 33, 19, 19, 19, 19, 19, 19, 19, 19, 34, 35, 13, 13, 13, 13,
    13, 36, 37, 19, 19, 19, 19, 19, 19, 19, 19, 19, 38, 19, 19, 39,
    19, 19, 19, 19, 40, 41, 42, 19, 19, 19, 43, 44, 45, 46, 47, 19,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 48, 13, 13, 13, 49, 50, 13,
    13, 13, 13, 51, 13, 13, 13, 13, 13, 13, 52, 19, 19, 19, 53, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
};

static RE_UINT8 re_grapheme_base_stage_3[] = {
      0,   1,   2,   2,   2,   2,   3,   4,   2,   5,   6,   7,   8,   9,  10,  11,
     12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,
     28,  29,   2,   2,  30,  31,  32,  33,   2,   2,   2,   2,   2,  34,  35,  36,
     37,  38,  39,  40,  41,  42,  43,  44,  45,  46,   2,  47,   2,   2,  48,  49,
     50,  51,   2,  52,   2,   2,   2,   2,  53,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2,   2,  54,  55,  56,  57,  58,  59,  60,  61,   2,  62,
     63,  64,  65,  66,  67,  68,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,  69,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,  70,
      2,  71,   2,   2,  72,  73,   2,  74,  75,  76,  77,  78,  79,  80,  81,  82,
      2,   2,   2,   2,   2,   2,   2,  83,  84,  84,  84,  84,  84,  84,  84,  84,
     84,  84,   2,   2,  85,  86,  87,  88,   2,   2,  89,  90,  91,  92,  93,  94,
     95,  96,  97,  98,  84,  99, 100, 101,   2, 102, 103,  84,   2,   2, 104,  84,
    105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115,  84, 116,  84, 117,  84,
    118, 119, 120, 121, 122, 123, 124,  84, 125, 126,  84, 127, 128, 129, 130,  84,
    131, 132,  84,  84, 133, 134,  84,  84, 135, 136, 137, 138,  84, 139,  84,  84,
      2,   2,   2,   2,   2,   2,   2, 140, 141,   2, 142,  84,  84,  84,  84,  84,
    143,  84,  84,  84,  84,  84,  84,  84,   2,   2,   2,   2, 144,  84,  84,  84,
      2,   2,   2,   2, 145, 146, 147, 148,  84,  84,  84,  84, 149, 150, 151, 152,
      2,   2,   2,   2,   2,   2,   2, 153,   2,   2,   2,   2,   2, 154,  84,  84,
      2,   2, 155,   2,   2, 156,  84,  84, 157, 158,  84,  84,  84,  84,  84,  84,
      2, 159, 160, 161, 162, 163, 164,  84, 165, 166, 167,   2,   2, 168,   2, 169,
      2,   2,   2,   2, 170, 171,  84,  84,   2, 172, 173,  84,  84,  84,  84,  84,
    174, 175,  84,  84, 176, 177,  84,  84, 178, 179, 180, 181, 182,  84,   2,   2,
      2,   2,   2,   2,   2, 183, 184, 185, 186, 187, 188, 189, 190,  84,  84,  84,
      2,   2,   2,   2,   2, 191,   2,   2,   2,   2,   2,   2,   2,   2, 192,   2,
    193,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2, 194,   2,   2,
      2,   2,   2,   2,   2,   2,   2, 195,   2,   2,   2,   2, 196,  84,  84,  84,
};

static RE_UINT8 re_grapheme_base_stage_4[] = {
      0,   0,   1,   1,   1,   1,   1,   2,   0,   0,   3,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,   4,
      5,   1,   6,   1,   1,   1,   1,   1,   7,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   8,   1,   9,   1,   1,  10,   0,   0,  11,  12,   1,  13,  14,
     15,  16,   1,   1,  17,   0,   1,   8,   1,   1,   1,   1,   1,  18,  19,   1,
     20,  21,   1,   0,  22,   1,   1,   1,   1,   1,  23,  24,   1,   1,  17,  25,
      1,  26,  27,   2,   1,  28,  17,   0,   0,   0,   1,  29,   0,   0,   0,   0,
     30,   1,   1,  31,  32,  33,  34,   1,  35,  36,  37,  38,  39,  40,  41,  20,
     42,  36,  37,  43,  44,  45,  15,  46,  47,   6,  37,  48,  49,  44,  41,  50,
     51,  36,  37,  52,  53,  40,  41,  54,  55,  56,  57,  58,  59,  44,  15,  17,
     60,  21,  37,  61,  62,  63,  41,  64,  65,  21,  37,  66,  67,  11,  41,  68,
     69,  21,   1,  70,  71,  72,  41,   1,  73,  74,   1,  75,  76,  77,  15,  78,
      8,   1,   1,  79,  80,  81,   0,   0,  82,  83,  84,  85,  86,  87,   0,   0,
      1,   4,   1,  88,  89,   1,  90,  91,  92,   0,   0,  93,  94,  17,   0,   0,
      1,   1,  90,  95,   1,  96,   8,  97,  98,   3,   1,   1,  99,   1,   1,   1,
      1,   1,   1,   1, 100, 101,   1,   1, 100,   1,   1, 102, 103, 104,   1,   1,
      1, 103,   1,   1,   1,  17,   1,  90,   1, 105,   1,   1,   1,   1,   1, 106,
      1,  90,   1,   1,   1,   1,   1, 107,   3, 108,   1, 109,   1, 108,   3,  44,
      1,   1,   1, 110, 111, 112, 105, 105,  17, 105,   1,   1,   1,   1,   1, 107,
    113,   1, 114,   1,   1,   1,   1,  23,   1,   2, 115, 116, 117,   1,  20,  14,
      1,   1,  81,   1, 105, 118,   1,   1,   1, 119,   1,   1,   1, 120, 121, 122,
    105, 105,  20,   0,   0,   0,   0,   0, 123,   1,   1, 124, 125,   1,  17, 112,
    126,   1, 127,   1,   1,   1, 128, 129,   1,   1,  81, 130, 131,   1,   1,   1,
    107,   1,   1,  10,  54, 132, 133, 134,   1,   1,   1,   1,   0,   0,   0,   0,
      1, 106,   1,   1, 106, 135,   1,  20,   1,   1,   1, 136, 136, 137,   1, 138,
     17,   1, 139,   1,   1,   1,   0,  34,   2,  90,   1,   1,   0,   0,   0,   0,
     81,   1,   1,   1,   1,   1,   1,   1,   1,   1,  76,   0,  17,   0,   1,   1,
      1,   1,   1,   1,   1,   1,   1, 140,   1, 141,   1,   1,  37,   1,   1,   2,
      1,   1,   2,   1,   1,   2,   1,   1,   1,   1,   1,   1,   1,   1,   2, 142,
      1,   1,  99,   1,   1,   1, 139,  44,   1,  76, 143, 143, 143, 143,   0,   0,
      1,   1,   1,   1,   2,   0,   0,   0,   1, 144,   1,   1,   1,   1,   1, 145,
      1,   1,   1,   1,   1,  23,   0,  81,   1,   1, 105,   1,   8,   1,   1,   1,
      1, 146,   1,   1,   1,   1,   1,   1, 147,   1,   1,   8,   1,   1,   1,   1,
      2,   1,   1,  17,   1,   1, 145,   1,   1,   2,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   2,   1,   1,   1,  23,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   0,  90,   1,   1,   1,  76,   1,   1,   1,
      1,   1,  81,   0,   1,   1,   2, 148,   1,  20,   1,   1,   1,   1,   1, 149,
      1,   1,   1, 105,   0,   0,   0, 150, 151,   1, 152, 105,   1,   1,   1,  54,
      1,   1,   1,   1, 153, 105,   0, 154,   1,   1, 155,   1,  76, 156,   1,  90,
     30,   1,   1, 157, 158, 159, 136,   2,   1,   1, 160, 161, 162,  87,   1, 163,
      1,   1,   1, 164, 165, 166, 167,  23, 168, 169, 143,   1,   1,   1,  23,   1,
      1,   1,   1,   1,   1,   1, 170, 105,   1,   1, 145,   1, 146,   1,   1,  81,
      0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,  20,   1,
      1,   1,   1,   1,   1, 105,   0,   0,  76, 171,   1, 172, 173,   1,   1,   1,
      1,   1,   1,   1, 108,  30,   1,   1,   1,   1,   1,   1,   0,   1,   1,   1,
      1, 126,   1,   1,  54,   0,   0,  20,   0, 105,   0,   1,   1, 174, 175, 136,
      1,   1,   1,   1,   1,   1,   1,  90,   8,   1,   1,   1,   1,   1,   1,   1,
      1,  20,   1,   2, 176, 177, 143, 178, 163,   1, 104, 179,  20,  20,   0,   0,
      1,   1,   1,   1,   1,   1,   1,  17, 180,   1,   1, 181,   1,   1,   1,   1,
      2,  81,  44,   0,   0,   1,   1,  90,   1,  90,   1,   1,   1,  44,   8,  81,
      1,   1, 182,   1,  17,   1,   1,  23,   1, 158,   1,   1, 183,  23,   0,   0,
      1,  20, 105,   1,   1, 183,   1,  81,   1,   1,  54,   1,   1,   1, 184,   0,
      1,   1,   1,  76,   1,  23,  54,   0, 185,   1,   1, 186,   1, 187,   1,   1,
      1,   2, 150,   0,   0,   0,   1, 188,   1, 189,   1,  58,   0,   0,   0,   0,
      1,   1,   1, 190,   1, 126,   1,   1,  44, 191,   1,  23, 107, 107,   1,   1,
      1,   1,   0,   0,   1,   1, 192,  76,   1,   1,   1, 193,   1, 141,   1, 194,
      1, 195, 196,   0,   0,   0,   0,   0,   1,   1,   1,   1, 107,   0,   0,   0,
      1,   1,   1, 122,   1,   1,   1,   7,   1,   1, 145, 105,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   1,   2,   1,   1,  54,   1,  23, 197,   0,   0,
     21,   1,   1,  54, 198, 126,   1,   0, 126,   1,   1, 199, 108,   1, 107, 105,
     30,   1, 200,  15,  76,   1,   1, 201, 126,   1,   1, 202, 203,   1,   8,  14,
      1,   6,   2, 204,   0,   0,   0,   0, 205, 158, 105,   1,   1,   2, 122, 105,
     51,  36,  37, 206, 207, 208, 145,   0,   1,   1,   1,  54, 209, 210,   0,   0,
      1,   1,   1, 211, 212, 105,   0,   0,   1,   1,   2, 213,   8,  81,   0,   0,
      1,   1,   1, 214,  62, 105,  90,   0,   1,   1, 215, 216, 105,   0,   0,   0,
      1,  17, 217,   1,   0,   0,   0,   0,   1,   1,   2, 218,   0,   0,   0,   0,
      0,   0,   1,   1,   1,   1,   1, 219, 220,   1,   1, 221,  76, 222,   1,   1,
    223, 224, 122,   0,   1,   1,   1, 107,  37,   1,   1,  11,  23,   1,  90,   1,
      1,   0, 225, 226,   0,   0,   0,   0, 227,   1,   1,  44, 216, 105, 228,   1,
      2, 229, 105,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1, 230,
      1, 105,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,   2,  14,
      1,   1,   1,   1, 145,   0,   0,   0,   1,   1,   2,   0,   0,   0,   0,   0,
      1,   1,   1,   1,  76,   0,   0,   0,   1,   1,   1, 107,   1,   2, 159,   0,
      0,   0,   0,   0,   0,   1,  20, 231,   1,   1,   1, 150,  23, 144,   6, 232,
      1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,
      1,  17,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,  14,   1,   1,   2,
      0,  30,   0,   0,   0,   0, 108,   0,   1,   1,   1,   1,   1,   1,   1, 108,
      1,   1,   1,   1,   1,   1,   1, 122,   1,   2,   0,   0,   0,   0,   0,   1,
      1,   1,   1,   1,   1,   1,   1,  81,   1,   1,   1,   1,   1,   1,  17,  90,
    107, 233,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1,  23,
      1,   1,   9,   1,   1,   1, 234,   0, 235,   1, 159,   1,   1,   1, 107,   0,
      1,   1,   1,   1, 236,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1, 145,
      1,   1,   1,   1,   1,  76,   1, 107,   1,   1,   1,   1,   1, 136,   1,   1,
      1,   3, 237,  31, 238,   1,   1,   1, 239, 240,   1, 241, 242,  21,   1,   1,
      1,   1, 141,   1,   1,   1,   1,   1,   1,   1,   1,   1, 167,   1,   1,   1,
      0,   0,   0, 243,   0,   0,  22, 136, 244,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1,   1, 113,   0,   0,   0,   1,   1,   1,   1, 145, 159,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   8,   1,   1,   1,  14,   0,   0,   0,   0,
    238,   1, 245, 246, 247, 248, 249, 250, 144,  81, 251,  81,   0,   0,   0, 108,
      1,   1,  81,   1,   1,   1,   1,   1,   1, 145,   2,   8,   8,   8,   1,  23,
     90,   1,   1,   1,   1,   1,  81,   1,   1,   1,  90,   0,   0,   0,  15,   1,
    122,   1,   1,  81, 107, 108,  23,   0,   1,   1,   1,   1,   1,  14,  90, 105,
      1,   1,   1,   1,   1,   1,   1, 145,   1,   1,   1,   1,   1, 107,   0,   0,
     81,   1,   1,   1,  54, 105,   1,   1,  54,   1,  20,   0,   0,   0,   0,   0,
     81,   1,   1,   2,   1,   1,   1, 252,   1,   1, 122, 105, 122,   1,   1,   1,
      0,   0,   0,   0,   0,   0,  20,   0,   1,   1,   1,   1,   1,  76,   0,   0,
      1,   1,   1,  14,   1,   1,   1,   1,   1,  20,   1,   1,   1,   1,   1,   1,
      1,   1, 108,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,  44,   0,
      1,  20,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_grapheme_base_stage_5[] = {
      0,   0, 255, 255, 255, 127, 255, 223, 255, 252, 240, 215, 251, 255,   7, 252,
    254, 255, 127, 254, 255, 231,   0,  64,  73,   0, 255, 135,  31,   0, 192, 255,
      0, 200, 255,   7,  63,  64,  96, 194, 255,  63, 253, 255,   0, 224,  63,   0,
      2,   0, 240, 199,  63,   4,  16,   1, 255,  65, 223,  63, 248, 255, 255, 235,
      1, 222,   1, 255, 243, 255, 237, 159, 249, 255, 255, 253, 197, 163, 129,  89,
      0, 176, 195, 255, 232, 135, 109, 195,   1,   0,   0,  94,  92,   0, 232, 191,
    237, 227,   1,  26,   3,   2, 236, 159, 237,  35, 129,  25, 255,   0, 232, 199,
     61, 214,  24, 199, 255, 131, 198,  29, 238, 223, 255,  35,  30,   0,   0,   7,
      0, 255, 253, 223, 239,  99, 155,  13,   6,   0, 236, 223, 255, 167, 193, 221,
    112, 255, 236, 255, 127, 252, 251,  47, 127,   0,   3, 127,  28,   0,  13, 128,
    127, 128, 255,  15, 150,  37, 240, 254, 174, 236,  13,  32,  95,   0, 255, 243,
     95, 253, 255, 254, 255,  31,   0, 128,  32,  31,   0, 192, 191, 223,   2, 153,
    255,  60, 225, 255, 155, 223, 191,  32, 255,  61, 127,  61,  61, 127,  61, 255,
    127, 255, 255,   3,  63,  63, 255,   1,   3,   0,  99,   0,  79, 192, 191,   1,
    240,  31, 159, 255, 255,   5, 120,  14, 251,   1, 241, 255, 255, 199, 127, 198,
    191,   0,  26, 224,   7,   0, 240, 255,  47, 232, 251,  15, 252, 255, 195, 196,
    191,  92,  12, 240,  48, 248, 255, 227,   8,   0,   2, 222, 239,   0, 255, 170,
    223, 255, 207, 239, 220, 127, 255, 128, 207, 255,  63, 255,  12, 254, 127, 127,
    255, 251,  15,   0, 127, 248, 224, 255,   8, 192, 252,   0, 128, 255, 187, 247,
    159,  15,  15, 192, 252, 127,  63, 192,  12, 128,  55, 236, 255, 191, 255, 195,
    255, 129,  25,   0, 247,  47, 255, 239,  98,  62,   5,   0,   0, 248, 255, 207,
    126, 126, 126,   0, 223,  30, 248, 160, 127,  95, 219, 255, 247, 255, 127,  15,
    252, 252, 252,  28,   0,  48, 255, 183, 135, 255, 143, 255,  15, 224,  15, 255,
     15, 128,  63, 253, 191, 145, 191, 255,  55, 248, 255, 143, 255, 240, 239, 254,
     31, 248,  63, 254,   7, 255,   3,  30,   0, 254, 254,   3, 128,  63, 135, 217,
    127,  16, 119,   0,  63, 128, 255,  33,  44,  63, 127, 189, 237, 163, 158,  57,
      1, 224, 163, 255, 255,  43,   6,  90, 242,   0,   3,  79,   7,  88, 255, 215,
     64,   0,  67,   0,   0,   9,   7, 128,   1, 248,   7, 134, 129, 241, 207,   3,
    128, 252,   0,   2,  18,   0, 127, 251, 191, 253,  88,   1, 231,   1,  32,   0,
    255, 224, 255, 147,  95,  60,  24, 240,  35,   0, 100, 222, 239, 255, 191, 231,
    223, 223, 255, 123,  95, 252, 128,   7, 239,  15, 150, 254, 247,  10, 132, 234,
    150, 170, 150, 247, 247,  94, 238, 251, 121, 244,
};

/* Grapheme_Base: 2772 bytes. */

RE_UINT32 re_get_grapheme_base(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_grapheme_base_stage_1[f] << 5;
    f = code >> 10;
    code ^= f << 10;
    pos = (RE_UINT32)re_grapheme_base_stage_2[pos + f] << 3;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_grapheme_base_stage_3[pos + f] << 3;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_grapheme_base_stage_4[pos + f] << 4;
    pos += code;
    value = (re_grapheme_base_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Grapheme_Link. */

static RE_UINT8 re_grapheme_link_stage_1[] = {
    0, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1,
};

static RE_UINT8 re_grapheme_link_stage_2[] = {
     0,  0,  1,  2,  3,  4,  5,  0,  0,  0,  0,  6,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7,  0,  0,  0,  0,  0,
     0,  0,  8,  0,  9, 10, 11, 12,  0,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_grapheme_link_stage_3[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,
     1,  1,  2,  3,  4,  0,  0,  5,  6,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  7,  8,  0,  0,  0,  0,  9,  0, 10, 11,
     0,  0, 12,  0,  0,  0,  0,  0, 13, 10, 14, 15,  0, 16,  0, 17,
     0,  0,  0,  0, 18,  0,  0,  0, 19, 20, 21, 15, 22, 23,  1,  0,
    24, 24,  0, 18, 18, 25, 26,  0, 20,  0,  0,  0, 27, 28,  0,  0,
    18,  0, 29, 30,  0,  0,  0,  0,
};

static RE_UINT8 re_grapheme_link_stage_4[] = {
     0,  0,  0,  0,  0,  0,  1,  0,  0,  2,  1,  0,  0,  0,  3,  0,
     0,  4,  0,  0,  5,  0,  0,  0,  0,  6,  0,  0,  7,  7,  0,  0,
     0,  0,  8,  0,  0,  0,  0,  9,  0,  0,  5,  0,  0, 10,  0, 11,
     0,  0,  0, 12, 13,  0,  0,  0,  0,  0, 14,  0,  0,  0,  9,  0,
     0,  0,  0, 15,  0,  0,  0,  1,  0, 12,  0,  0,  0,  0, 13, 12,
     0, 16,  0,  0,  0, 17,  0,  0,  0, 18,  0,  0,  0,  0,  0,  3,
     0,  0, 19,  0,  0, 15,  0,  0,  0, 20,  0,  0,  0,  7, 21,  0,
    16,  0,  0,  0,  0,  0, 22,  0, 23,  0,  0,  0,
};

static RE_UINT8 re_grapheme_link_stage_5[] = {
      0,   0,   0,   0,   0,  32,   0,   0,   0,   0,   0,  24,   0,   4,   0,   0,
      0,   0,   0,   4,  16,   0,   0,   0,   0,   0,   0,   6,   0,   0,  16,   0,
      0,   0,   4,   0,   1,   0,   0,   0,   0,  12,   0,   0,   0,   0,  12,   0,
      0,   0,   0, 128,  64,   0,   0,   0,   0,   0,   8,   0,   0,   0,  64,   0,
      0,   0,   0,   2,   0,   0,  24,   0,   0,   0,  32,   0,   4,   0,   0,   0,
      0,   8,   0,   0, 128,   0,   0,   0,  48,   0,   0,   0,   0,   0, 128,   0,
};

/* Grapheme_Link: 456 bytes. */

RE_UINT32 re_get_grapheme_link(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 14;
    code = ch ^ (f << 14);
    pos = (RE_UINT32)re_grapheme_link_stage_1[f] << 4;
    f = code >> 10;
    code ^= f << 10;
    pos = (RE_UINT32)re_grapheme_link_stage_2[pos + f] << 3;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_grapheme_link_stage_3[pos + f] << 2;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_grapheme_link_stage_4[pos + f] << 5;
    pos += code;
    value = (re_grapheme_link_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* White_Space. */

static RE_UINT8 re_white_space_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_white_space_stage_2[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
};

static RE_UINT8 re_white_space_stage_3[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1,
    3, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_white_space_stage_4[] = {
    0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 3, 1, 1, 1, 1, 1, 4, 5, 1, 1, 1, 1, 1, 1,
    3, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_white_space_stage_5[] = {
      0,  62,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     32,   0,   0,   0,   1,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,
    255,   7,   0,   0,   0, 131,   0,   0,   0,   0,   0, 128,   0,   0,   0,   0,
};

/* White_Space: 169 bytes. */

RE_UINT32 re_get_white_space(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_white_space_stage_1[f] << 3;
    f = code >> 13;
    code ^= f << 13;
    pos = (RE_UINT32)re_white_space_stage_2[pos + f] << 4;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_white_space_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_white_space_stage_4[pos + f] << 6;
    pos += code;
    value = (re_white_space_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Bidi_Control. */

static RE_UINT8 re_bidi_control_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_bidi_control_stage_2[] = {
    0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_bidi_control_stage_3[] = {
    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    2, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_bidi_control_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    2, 3, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_bidi_control_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  16,   0,   0,   0,   0,
      0, 192,   0,   0,   0, 124,   0,   0,   0,   0,   0,   0, 192,   3,   0,   0,
};

/* Bidi_Control: 129 bytes. */

RE_UINT32 re_get_bidi_control(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_bidi_control_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_bidi_control_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_bidi_control_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_bidi_control_stage_4[pos + f] << 6;
    pos += code;
    value = (re_bidi_control_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Join_Control. */

static RE_UINT8 re_join_control_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_join_control_stage_2[] = {
    0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_join_control_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_join_control_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_join_control_stage_5[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0, 48,  0,  0,  0,  0,  0,  0,
};

/* Join_Control: 97 bytes. */

RE_UINT32 re_get_join_control(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_join_control_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_join_control_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_join_control_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_join_control_stage_4[pos + f] << 6;
    pos += code;
    value = (re_join_control_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Dash. */

static RE_UINT8 re_dash_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_dash_stage_2[] = {
    0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
};

static RE_UINT8 re_dash_stage_3[] = {
    0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 4, 1, 1, 1,
    5, 6, 1, 1, 1, 1, 1, 7, 8, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9,
};

static RE_UINT8 re_dash_stage_4[] = {
     0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  2,  1,  3,  1,  1,  1,  1,  1,  1,  1,
     4,  1,  1,  1,  1,  1,  1,  1,  5,  6,  7,  1,  1,  1,  1,  1,
     8,  1,  1,  1,  1,  1,  1,  1,  9,  3,  1,  1,  1,  1,  1,  1,
    10,  1, 11,  1,  1,  1,  1,  1, 12, 13,  1,  1, 14,  1,  1,  1,
};

static RE_UINT8 re_dash_stage_5[] = {
      0,   0,   0,   0,   0,  32,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   4,   0,   0,   0,   0,   0,  64,   1,   0,   0,   0,   0,   0,   0,   0,
     64,   0,   0,   0,   0,   0,   0,   0,   0,   0,  63,   0,   0,   0,   0,   0,
      0,   0,   8,   0,   0,   0,   0,   8,   0,   8,   0,   0,   0,   0,   0,   0,
      0,   0,   4,   0,   0,   0,   0,   0,   0,   0, 128,   4,   0,   0,   0,  12,
      0,   0,   0,  16,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   6,   0,   0,   0,   0,   1,   8,   0,   0,   0,
      0,  32,   0,   0,   0,   0,   0,   0,
};

/* Dash: 297 bytes. */

RE_UINT32 re_get_dash(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_dash_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_dash_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_dash_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_dash_stage_4[pos + f] << 6;
    pos += code;
    value = (re_dash_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Hyphen. */

static RE_UINT8 re_hyphen_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_hyphen_stage_2[] = {
    0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
};

static RE_UINT8 re_hyphen_stage_3[] = {
    0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1,
    4, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7,
};

static RE_UINT8 re_hyphen_stage_4[] = {
    0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1,
    4, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 6, 1, 1, 1, 1, 1, 7, 1, 1, 8, 9, 1, 1,
};

static RE_UINT8 re_hyphen_stage_5[] = {
      0,   0,   0,   0,   0,  32,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   4,   0,   0,   0,   0,   0,   0,  64,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   3,   0,   0,   0,   0,   0,   0,   0, 128,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   8,   0,   0,   0,   0,   8,   0,   0,   0,
      0,  32,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  32,   0,   0,   0,
};

/* Hyphen: 241 bytes. */

RE_UINT32 re_get_hyphen(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_hyphen_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_hyphen_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_hyphen_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_hyphen_stage_4[pos + f] << 6;
    pos += code;
    value = (re_hyphen_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Quotation_Mark. */

static RE_UINT8 re_quotation_mark_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_quotation_mark_stage_2[] = {
    0, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_quotation_mark_stage_3[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    2, 1, 1, 1, 1, 1, 1, 3, 4, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 5,
};

static RE_UINT8 re_quotation_mark_stage_4[] = {
    0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    3, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1,
    5, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 7, 8, 1, 1,
};

static RE_UINT8 re_quotation_mark_stage_5[] = {
      0,   0,   0,   0, 132,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   8,   0,   8,   0,   0,   0, 255,   0,   0,   0,   6,
      4,   0,   0,   0,   0,   0,   0,   0,   0, 240,   0, 224,   0,   0,   0,   0,
     30,   0,   0,   0,   0,   0,   0,   0, 132,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  12,   0,   0,   0,
};

/* Quotation_Mark: 209 bytes. */

RE_UINT32 re_get_quotation_mark(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_quotation_mark_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_quotation_mark_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_quotation_mark_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_quotation_mark_stage_4[pos + f] << 6;
    pos += code;
    value = (re_quotation_mark_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Terminal_Punctuation. */

static RE_UINT8 re_terminal_punctuation_stage_1[] = {
    0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 4,
};

static RE_UINT8 re_terminal_punctuation_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  9, 10, 11,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9, 12, 13,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9, 14,
    15,  9, 16, 17, 18, 19, 20, 21,  9, 22,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9, 23, 24,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9, 25,
     9,  9,  9,  9,  9,  9, 26,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
     9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,
};

static RE_UINT8 re_terminal_punctuation_stage_3[] = {
     0,  1,  1,  1,  1,  1,  2,  3,  1,  1,  1,  4,  5,  6,  7,  8,
     9,  1, 10,  1,  1,  1,  1,  1,  1,  1,  1,  1, 11,  1, 12,  1,
    13,  1,  1,  1,  1,  1, 14,  1,  1,  1,  1,  1, 15, 16, 17, 18,
    19,  1, 20,  1,  1, 21, 22,  1, 23,  1,  1,  1,  1,  1,  1,  1,
    24,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1, 25,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,
     1, 27,  1,  1, 28, 29,  1,  1, 30, 31, 32, 33, 34, 35,  1, 36,
     1,  1,  1,  1, 37,  1, 38,  1,  1,  1,  1,  1,  1,  1,  1, 39,
    40,  1, 41,  1, 42, 43, 44, 45,  1,  1,  1,  1,  1,  1, 46,  1,
    47, 48, 49, 50, 51, 52,  1,  1, 53,  1,  1, 54, 55,  1, 56,  1,
     1,  1,  1,  1, 57, 58,  1,  1, 59,  1,  1,  1,  1, 60,  1,  1,
    61,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 62, 63, 64,  1,
     1,  1,  1,  1,  1, 65,  1,  1,  1, 41,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1, 66,  1,  1,
};

static RE_UINT8 re_terminal_punctuation_stage_4[] = {
     0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,  3,  0,  0,  0,
     4,  0,  5,  0,  6,  0,  0,  0,  0,  0,  7,  0,  8,  0,  0,  0,
     0,  0,  0,  9,  0, 10,  2,  0,  0,  0,  0, 11,  0,  0, 12,  0,
    13,  0,  0,  0,  0,  0, 14,  0,  0,  0,  0, 15,  0,  0,  0, 16,
     0,  0,  0, 17,  0, 18,  0,  0,  0,  0, 19,  0, 20,  0,  0,  0,
     0,  0, 11,  0,  0, 21,  0,  0,  0,  0, 22,  0,  0, 23,  0, 24,
     0, 25, 26,  0,  0, 27, 28,  0, 29,  0,  0,  0,  0,  0,  0, 24,
    30,  0,  0,  0,  0,  0,  0, 31,  0,  0,  0, 32,  0,  0, 33,  0,
     0, 34,  0,  0,  0,  0, 26,  0,  0,  0, 35,  0,  0,  0, 36, 37,
     0,  0,  0, 38,  0,  0, 39,  0,  1,  0,  0, 40, 36,  0, 41,  0,
     0,  0, 42,  0, 36,  0,  0,  0,  0,  0, 32,  0,  0,  0,  0, 43,
     0, 44,  0,  0, 45,  0,  0,  0,  0,  0, 46,  0,  0,  0, 47,  0,
     0, 24, 48,  0,  0,  0, 49,  0,  0,  0, 50,  0,  0, 51,  0,  0,
     0,  4,  0,  0,  0,  0, 52,  0,  0,  0, 53,  0,  0,  0, 29,  0,
     0, 54,  0,  0,  0,  0, 55,  0, 56, 29,  0,  0,  0,  0, 49, 57,
     0,  0,  0, 58,  0,  0,  0, 59,  0,  0,  0, 33,  0,  0,  0, 60,
     0, 61, 62,  0, 58,  0,  0,  0, 63,  0,  0,  0,
};

static RE_UINT8 re_terminal_punctuation_stage_5[] = {
      0,   0,   0,   0,   2,  80,   0, 140,   0,   0,   0,  64, 128,   0,   0,   0,
      0,   2,   0,   0,   8,   0,   0,   0,   0,  16,   0, 200,   0,   0,  16,   0,
    255,  23,   0,   0,   0,   0,   0,   3,   0,   0, 255, 127,  48,   0,   0,   0,
      0,   0,   0,  12,   0, 225,   7,   0,   0,  12,   0,   0, 254,   1,   0,   0,
      0,  96,   0,   0,   0,  56,   0,   0,   0,   0,  96,   0,   0,   0, 112,   4,
     60,   3,   0,   0,   0,  15,   0,   0,   0,   0,   0, 236,   0,   0,   0, 248,
      0,   0,   0, 192,   0,   0,   0,  48, 128,   3,   0,   0,   0,  64,   0,  16,
      2,  80,   0,   0,   6,   0,   0,   0,   0, 224,   0,   0,   0,   0, 248,   0,
      0,   0, 192,   0,   0, 192,   0,   0,   0, 128,   0,   0,   0,   0,   0, 224,
      0,   0,   0, 128,   0,   0,   3,   0,   0,   8,   0,   0,   0,   0, 247,   0,
     18,   0,   0,   0,   0,   0,   1,   0,   0,   0, 128,   0,   0,   0,  63,   0,
      0,   0,   0, 252,   0,   0,   0,  30,   0,   0, 224,   3, 128,  63,   0,   0,
      3,   0,   0,   0,  14,   0,   0,   0,  96,  32,   0, 192,   0,   0,   0,  31,
      0,  56,   0,   8,  60, 254, 255,   0,   0,   0,   0, 112,  12,   0,   0,   0,
      0,   0,   0,  24,   0,   0,   2,   0,   0,   0, 128,   1,   0,   0,  31,   0,
      0,   0,  32,   0,   0,   0, 128,   3,  16,   0,   0,   0, 128,   7,   0,   0,
};

/* Terminal_Punctuation: 934 bytes. */

RE_UINT32 re_get_terminal_punctuation(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_terminal_punctuation_stage_1[f] << 5;
    f = code >> 10;
    code ^= f << 10;
    pos = (RE_UINT32)re_terminal_punctuation_stage_2[pos + f] << 3;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_terminal_punctuation_stage_3[pos + f] << 2;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_terminal_punctuation_stage_4[pos + f] << 5;
    pos += code;
    value = (re_terminal_punctuation_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Other_Math. */

static RE_UINT8 re_other_math_stage_1[] = {
    0, 1, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2,
};

static RE_UINT8 re_other_math_stage_2[] = {
    0, 1, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 6, 1, 1,
};

static RE_UINT8 re_other_math_stage_3[] = {
     0,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     3,  4,  1,  5,  1,  6,  7,  8,  1,  9,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1, 10, 11,  1,  1,  1,  1, 12, 13, 14, 15,
     1,  1,  1,  1,  1,  1, 16,  1,
};

static RE_UINT8 re_other_math_stage_4[] = {
     0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  2,  3,  4,  5,  6,  7,  8,  0,  9, 10,
    11, 12, 13,  0, 14, 15, 16, 17, 18,  0,  0,  0,  0, 19, 20, 21,
     0,  0,  0,  0,  0, 22, 23, 24, 25,  0, 26, 27,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 25, 28,  0,  0,  0,  0, 29,  0, 30, 31,
     0,  0,  0, 32,  0,  0,  0,  0,  0, 33,  0,  0,  0,  0,  0,  0,
    34, 34, 35, 34, 36, 37, 38, 34, 39, 40, 41, 34, 34, 34, 34, 34,
    34, 34, 34, 34, 34, 42, 43, 44, 35, 35, 45, 45, 46, 46, 47, 34,
    38, 48, 49, 50, 51, 52,  0,  0,
};

static RE_UINT8 re_other_math_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,  64,   0,   0,  39,   0,   0,   0,  51,   0,
      0,   0,  64,   0,   0,   0,  28,   0,   1,   0,   0,   0,  30,   0,   0,  96,
      0,  96,   0,   0,   0,   0, 255,  31,  98, 248,   0,   0, 132, 252,  47,  62,
     16, 179, 251, 241, 224,   3,   0,   0,   0,   0, 224, 243, 182,  62, 195, 240,
    255,  63, 235,  47,  48,   0,   0,   0,   0,  15,   0,   0,   0,   0, 176,   0,
      0,   0,   1,   0,   4,   0,   0,   0,   3, 192, 127, 240, 193, 140,  15,   0,
    148,  31,   0,   0,  96,   0,   0,   0,   5,   0,   0,   0,  15,  96,   0,   0,
    192, 255,   0,   0, 248, 255, 255,   1,   0,   0,   0,  15,   0,   0,   0,  48,
     10,   1,   0,   0,   0,   0,   0,  80, 255, 255, 255, 255, 255, 255, 223, 255,
    255, 255, 255, 223, 100, 222, 255, 235, 239, 255, 255, 255, 191, 231, 223, 223,
    255, 255, 255, 123,  95, 252, 253, 255,  63, 255, 255, 255, 253, 255, 255, 247,
    255, 255, 255, 247, 255, 127, 255, 255, 255, 253, 255, 255, 247, 207, 255, 255,
    150, 254, 247,  10, 132, 234, 150, 170, 150, 247, 247,  94, 255, 251, 255,  15,
    238, 251, 255,  15,
};

/* Other_Math: 502 bytes. */

RE_UINT32 re_get_other_math(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_other_math_stage_1[f] << 4;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_other_math_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_other_math_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_other_math_stage_4[pos + f] << 5;
    pos += code;
    value = (re_other_math_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Hex_Digit. */

static RE_UINT8 re_hex_digit_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_hex_digit_stage_2[] = {
    0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_hex_digit_stage_3[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 2,
};

static RE_UINT8 re_hex_digit_stage_4[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 2, 1,
};

static RE_UINT8 re_hex_digit_stage_5[] = {
      0,   0,   0,   0,   0,   0, 255,   3, 126,   0,   0,   0, 126,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0, 255,   3, 126,   0,   0,   0, 126,   0,   0,   0,   0,   0,   0,   0,
};

/* Hex_Digit: 129 bytes. */

RE_UINT32 re_get_hex_digit(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_hex_digit_stage_1[f] << 3;
    f = code >> 13;
    code ^= f << 13;
    pos = (RE_UINT32)re_hex_digit_stage_2[pos + f] << 3;
    f = code >> 10;
    code ^= f << 10;
    pos = (RE_UINT32)re_hex_digit_stage_3[pos + f] << 3;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_hex_digit_stage_4[pos + f] << 7;
    pos += code;
    value = (re_hex_digit_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* ASCII_Hex_Digit. */

static RE_UINT8 re_ascii_hex_digit_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_ascii_hex_digit_stage_2[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_ascii_hex_digit_stage_3[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_ascii_hex_digit_stage_4[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_ascii_hex_digit_stage_5[] = {
      0,   0,   0,   0,   0,   0, 255,   3, 126,   0,   0,   0, 126,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
};

/* ASCII_Hex_Digit: 97 bytes. */

RE_UINT32 re_get_ascii_hex_digit(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_ascii_hex_digit_stage_1[f] << 3;
    f = code >> 13;
    code ^= f << 13;
    pos = (RE_UINT32)re_ascii_hex_digit_stage_2[pos + f] << 3;
    f = code >> 10;
    code ^= f << 10;
    pos = (RE_UINT32)re_ascii_hex_digit_stage_3[pos + f] << 3;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_ascii_hex_digit_stage_4[pos + f] << 7;
    pos += code;
    value = (re_ascii_hex_digit_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Other_Alphabetic. */

static RE_UINT8 re_other_alphabetic_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_other_alphabetic_stage_2[] = {
     0,  1,  2,  3,  3,  3,  3,  3,  3,  3,  4,  3,  3,  3,  3,  5,
     6,  7,  3,  3,  3,  3,  8,  3,  3,  3,  3,  9,  3,  3, 10, 11,
     3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,
};

static RE_UINT8 re_other_alphabetic_stage_3[] = {
     0,  0,  0,  1,  0,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12,
    13,  0,  0, 14,  0,  0,  0, 15, 16, 17, 18, 19, 20, 21,  0,  0,
     0,  0,  0,  0, 22,  0,  0,  0,  0,  0,  0,  0,  0, 23,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 24,  0, 25, 26, 27, 28,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 29,  0,  0,  0,  0,
     0,  0,  0, 30,  0,  0,  0,  0,  0,  0, 31,  0,  0, 32,  0,  0,
    33, 34, 35, 36, 37, 38, 39, 40, 41,  0, 42,  0, 43, 44, 45,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 46,  0,  0,  0, 47,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 48,  0,  0,  0,
    49,  0,  0,  0,  0,  0,  0,  0,  0, 50,  0,  0,  0,  0,  0,  0,
     0, 51,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_other_alphabetic_stage_4[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   2,   3,   0,   4,   0,   5,   6,   0,   0,   7,   8,
      9,  10,   0,   0,   0,  11,   0,   0,  12,  13,   0,   0,   0,   0,  14,  15,
     16,  17,  18,  19,  20,  21,  22,  19,  20,  21,  23,  24,  20,  21,  25,  26,
     20,  21,  27,  19,  28,  21,  29,   0,  16,  21,  30,  19,  20,  21,  30,  19,
     16,  21,  31,  19,  19,   0,  32,  33,   0,  34,  35,   0,   0,  36,  35,   0,
      0,   0,   0,  37,  38,  39,   0,   0,   0,  40,  41,  42,  43,   0,   0,   0,
      0,   0,  44,   0,   0,   0,   0,   0,  33,  33,  33,  33,   0,  45,  46,   0,
      0,   0,   0,   0,  47,  48,   0,   0,   0,  49,   0,   0,   0,   0,   0,   0,
     50,   0,  51,  52,   0,   0,   0,   0,  53,  54,  16,   0,  55,  56,   0,  57,
      0,  58,   0,   0,   0,   0,   0,  33,   0,   0,   0,   0,   0,   0,   0,  59,
      0,   0,   0,   0,   0,  45,  60,  61,   0,   0,   0,   0,   0,   0,   0,  60,
      0,   0,   0,  62,  21,   0,   0,   0,   0,  63,   0,   0,  64,  14,  65,   0,
      0,  66,  67,   0,  16,  14,   0,   0,   0,  68,  69,   0,   0,  70,   0,  71,
      0,   0,   0,   0,   0,   0,   0,  72,  73,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,  74,   0,   0,   0,   0,  75,   0,   0,   0,   0,   0,   0,   0,
      0,  76,   0,   0,   0,   0,   0,   0,  55,  77,  78,   0,  28,  79,   0,   0,
     55,  67,  47,   0,  55,  80,   0,   0,   0,  81,   0,   0,   0,   0,  44,  46,
     16,  21,  22,  19,   0,   0,   0,   0,   0,  54,  82,   0,   0,  10,  64,   0,
      0,   0,   0,   0,   0,  83,  84,   0,   0,  85,  86,   0,   0,  87,   0,   0,
     88,  89,   0,   0,   0,   0,   0,   0,   0,  90,   0,   0,   0,   0,   0,   0,
     91,  92,  93,   0,  94,   0,   0,   0,   0,  95,   0,   0,  96,  97,   0,   0,
      0,  98,  99,   0, 100,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 101,
      0, 102,   0,   0,   0,   0,   0,   0,   0,   0,  37, 103,   0,   0,   0,   0,
      0,   0,   0,   0,  73,   0,   0,   0, 104, 105,   0,   0,   0,   0,   0,   0,
      0,   0, 106,   0,   0,   0,   0,   0,   0,  10, 107, 107,  61,   0,   0,   0,
};

static RE_UINT8 re_other_alphabetic_stage_5[] = {
      0,   0,   0,   0,  32,   0,   0,   0,   0,   0, 255, 191, 182,   0,   0,   0,
      0,   0, 255,   7,   0, 248, 255, 254,   0,   0,   1,   0,   0,   0, 192,  31,
    158,  33,   0,   0,   0,   0,   2,   0,   0,   0, 255, 255, 192, 255,   1,   0,
      0,   0, 192, 248, 239,  30,   0,   0,   0,   0, 240, 255, 248,   3, 255, 255,
     15,   0,   0,   0,   0,   0,   0, 204, 255, 223, 224,   0,  12,   0,   0,   0,
     14,   0,   0,   0,   0,   0,   0, 192, 159,  25, 128,   0, 135,  25,   2,   0,
      0,   0,  35,   0, 191,  27,   0,   0,  12,   0,   0,  28, 159,  25, 192,   0,
      4,   0,   0,   0, 199,  29, 128,   0, 223,  29,  96,   0, 223,  29, 128,   0,
      0, 128,  95, 255,   0,   0,  12,   0,   0,   0, 242,   7,   0,  32,   0,   0,
      0,   0, 242,  27,   0,   0, 254, 255,   3, 224, 255, 254, 255, 255, 255,  31,
      0, 248, 127, 121,   0,   0, 192, 195, 133,   1,  30,   0, 124,   0,   0,  48,
      0,   0,   0, 128,   0,   0, 192, 255, 255,   1,   0,   0,  96,   0,   0,   0,
      0,   2,   0,   0, 255,  15, 255,   1,   0,   0, 128,  15,   0,   0, 224, 127,
    254, 255,  31,   0,  31,   0,   0,   0,   0,   0, 224, 255,   7,   0,   0,   0,
    254,  51,   0,   0, 128, 255,   3,   0, 240, 255,  63,   0, 128, 255,  31,   0,
    255, 255, 255, 255, 255,   3,   0,   0,   0,   0, 240,  15, 248,   0,   0,   0,
      3,   0,   0,   0,  47,   0,   0,   0, 192,   7,   0,   0, 128, 255,   7,   0,
      0, 254, 127,   0,   8,  48,   0,   0,   0,   0, 157,  65,   0, 248,  32,   0,
    248,   7,   0,   0,   0,   0,   0,  64,   0,   0, 192,   7, 110, 240,   0,   0,
    240,   0,   0,   0,   0,   0,   0, 255,  63,   0,   0,   0,   0,   0, 255,   1,
      0,   0, 248, 255,   0, 240, 159,  64,  59,   0,   0,   0,   0, 128,  63, 127,
      0,   0,   0,  48,   0,   0, 255, 127,   1,   0,   0,   0,   0, 248,  63,   0,
      0,   0,   0, 224, 255,   7,   0,   0,   0, 240, 255,   1, 254,   7,   0,   0,
      0,   0, 224, 123,   0,   0, 254,  15,   0, 252, 255,   0,   0, 128, 127, 127,
      0,   0, 252, 255, 255, 254, 127,   0,   0,   0, 126, 180, 139,   0,   0,   0,
      0, 124, 123,   0,   0,   0, 120,   0,   0,   0, 127,   0, 255, 255, 255, 127,
    127, 255, 255, 249, 219,   7,   0,   0, 128,   0,   0,   0, 255,   3, 255, 255,
};

/* Other_Alphabetic: 1105 bytes. */

RE_UINT32 re_get_other_alphabetic(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_other_alphabetic_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_other_alphabetic_stage_2[pos + f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_other_alphabetic_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_other_alphabetic_stage_4[pos + f] << 5;
    pos += code;
    value = (re_other_alphabetic_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Ideographic. */

static RE_UINT8 re_ideographic_stage_1[] = {
    0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3,
};

static RE_UINT8 re_ideographic_stage_2[] = {
     0,  0,  0,  1,  2,  3,  3,  3,  3,  4,  0,  0,  0,  0,  0,  5,
     0,  0,  0,  0,  0,  0,  0,  3,  6,  0,  0,  7,  0,  0,  0,  0,
     3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  8,  9, 10,  3, 11, 12,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_ideographic_stage_3[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  3,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  4,  0,  0,  0,  0,  5,  6,  0,  0,
     2,  2,  2,  7,  2,  8,  0,  0,  9, 10,  0,  0,  0,  0,  0,  0,
     2,  2,  2, 11,  2,  2,  2,  2,  2,  2,  2, 12, 13,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2, 14,  2,  2,  2,  2,  2, 15,  0,  0,
     0,  0,  0,  0,  2, 16,  0,  0,
};

static RE_UINT8 re_ideographic_stage_4[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  3,  0,
     2,  2,  2,  2,  2,  2,  2,  4,  0,  0,  0,  0,  2,  2,  2,  2,
     2,  5,  2,  6,  0,  0,  0,  0,  2,  2,  2,  2,  2,  2,  2,  7,
     2,  2,  2,  8,  0,  0,  0,  0,  0,  0,  0,  0,  0,  9,  2,  2,
     2,  2,  2, 10,  0,  0,  0,  0,  2,  2,  2, 11,  2,  2,  2,  2,
     2,  2,  2,  2, 12,  2,  2,  2, 13,  2,  2,  2,  2,  2,  2,  2,
     2,  2, 14,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2, 15,
    16,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_ideographic_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0, 192,   0,   0,   0, 254,   3,   0,   7,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,  63,   0,
    255, 255, 255, 255, 255, 255,   0,   0, 255, 255, 255, 255, 255,  63, 255, 255,
    255, 255, 255,   3,   0,   0,   0,   0, 255, 255, 255, 255, 255, 255,   3,   0,
    255, 255, 255, 255, 255, 255,   7,   0,   0,   0,   0,   0,   0,   0, 255, 255,
    255, 255, 255, 255, 255, 255, 255,  15, 255, 255, 127,   0,   0,   0,   0,   0,
    255, 255, 255, 255, 255, 255,  31,   0, 255, 255, 255,  63, 255, 255, 255, 255,
    255, 255, 255, 255,   3,   0, 255, 255, 255, 255, 255, 255,   1,   0,   0,   0,
    255, 255, 255,  63,   0,   0,   0,   0,
};

/* Ideographic: 457 bytes. */

RE_UINT32 re_get_ideographic(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_ideographic_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_ideographic_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_ideographic_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_ideographic_stage_4[pos + f] << 6;
    pos += code;
    value = (re_ideographic_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Diacritic. */

static RE_UINT8 re_diacritic_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_diacritic_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  7,  8,  4,  4,  4,  4,  4,  4,  4,  4,  4,  9,
    10, 11, 12, 13,  4,  4,  4,  4,  4,  4,  4,  4,  4, 14,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4, 15,  4,  4, 16,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
};

static RE_UINT8 re_diacritic_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
    16,  1,  1,  1,  1,  1,  1, 17,  1, 18, 19, 20, 21, 22,  1, 23,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 24,  1, 25,  1,
    26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 27, 28,
    29, 30, 31, 32,  1,  1,  1,  1,  1,  1,  1, 33,  1,  1, 34, 35,
     1,  1, 36,  1,  1,  1,  1,  1,  1,  1, 37,  1,  1, 38,  1, 39,
    40, 41, 42, 43, 44, 45, 46, 47, 48,  1, 49,  1, 50, 51,  1,  1,
     1,  1, 52,  1,  1,  1,  1, 53,  1, 54,  1,  1,  1,  1,  1,  1,
    55, 56,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_diacritic_stage_4[] = {
     0,  0,  1,  2,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  4,  5,  5,  5,  5,  6,  7,  8,  0,  0,  0,
     0,  0,  0,  0,  9,  0,  0,  0,  0,  0, 10,  0, 11, 12, 13,  0,
     0,  0, 14,  0,  0,  0, 15, 16,  0,  4, 17,  0,  0, 18,  0, 19,
    20,  0,  0,  0,  0,  0,  0, 21,  0, 22, 23, 24,  0, 22, 25,  0,
     0, 22, 25,  0,  0, 22, 25, 26,  0, 22, 25,  0,  0,  0, 25,  0,
     0,  0, 25,  0,  0, 22, 25,  0,  0, 27, 25,  0,  0,  0, 28,  0,
     0,  0, 29,  0,  0,  0, 30,  0, 20, 31,  0,  0, 32,  0, 33,  0,
     0, 34,  0,  0, 35,  0,  0,  0,  0,  0,  0,  0,  0,  0, 36,  0,
     0, 37,  0,  0,  0,  0,  0,  0,  0,  0,  0, 38,  0, 39,  0,  0,
     0, 40, 41, 42,  0, 43,  0,  0,  0, 44,  0, 45,  0,  0,  4, 46,
     0, 47,  5, 17,  0,  0, 48, 49,  0,  0,  0,  0,  0, 50, 51, 52,
     0,  0,  0,  0,  0,  0,  0, 53,  0, 54,  0,  0,  0,  0,  0,  0,
     0, 55,  0,  0, 56,  0,  0, 22,  0,  0,  0, 57, 58,  0,  0, 59,
    60, 61,  0,  0, 62,  0,  0, 20,  0,  0,  0,  0,  0,  0, 41, 63,
     0, 64, 65,  0,  0, 65,  2, 66,  0,  0,  0, 67,  0, 15, 68, 69,
     0,  0, 70,  0,  0,  0,  0, 71,  1,  0,  0,  0,  0,  0,  0,  0,
     0, 72,  0,  0,  0,  0,  0,  0,  0,  1,  2, 73, 74,  0,  0, 75,
     0,  0,  0,  0,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0, 76,
     0, 77,  0,  0,  0,  0,  0,  0,  0,  0, 18,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0, 78,  0,  0,  0, 79,  0, 65,  0,  0, 80,  0,
     0, 81,  0,  0,  0,  0,  0, 82,  0, 22, 25, 83,  0,  0,  0,  0,
     0,  0, 84,  0,  0,  0, 85,  0,  0,  0,  0,  0,  0, 15,  2,  0,
     0, 15,  0,  0,  0, 44,  0,  0,  0, 86,  0,  0,  0,  0,  0,  0,
     0, 78,  0,  0,  0,  0,  0,  0,  0, 40, 87,  0, 10,  0,  0,  0,
     0, 15,  0,  0,  0,  0,  0,  0,  0,  0, 88,  0, 89,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0, 90,  0,  0,  0,  0, 91,  0,  0,  0,
     0,  0,  0, 92, 93, 94,  0,  0,  0,  0,  0,  0,  0,  0, 95,  0,
     0,  0, 96,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_diacritic_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,  64,   1,   0,   0,   0,   0, 129, 144,   1,
      0,   0, 255, 255, 255, 255, 255, 255, 255, 127, 255, 224,   7,   0,  48,   4,
     48,   0,   0,   0, 248,   0,   0,   0,   0,   0,   0,   2,   0,   0, 254, 255,
    251, 255, 255, 191,  22,   0,   0,   0,   0, 248, 135,   1,   0,   0,   0, 128,
     97,  28,   0,   0, 255,   7,   0,   0, 192, 255,   1,   0,   0, 248,  63,   0,
      0,   0,   0,   3, 248, 255, 255, 127,   0,   0,   0,  16,   0,  32,  30,   0,
      0,   0,   2,   0,   0,  32,   0,   0,   0,   0,   0, 224,   0,   0,   0,  24,
      0,   4,   0,   0, 128,  95,   0,   0,   0,  31,   0,   0,   0,   0, 160, 194,
    220,   0,   0,   0,  64,   0,   0,   0,   0,   0, 128,   6, 128, 191,   0,  12,
      0, 254,  15,  32,   0,   0,   0,  14,   0,   0, 224, 159,   0,   0, 255,  63,
      0,   0,  16,   0,  16,   0,   0,   0,   0, 248,  15,   0,   0,  12,   0,   0,
      0,   0, 192,   0,   0,   0,   0,  63, 255,  33, 144,   3,   0, 240, 255, 255,
    240, 255,   0,   0,   0,   0, 224, 227,   0,   0,   0, 160,   3, 224,   0, 224,
      0, 224,   0,  96,   0, 128,   3,   0,   0, 128,   0,   0,   0, 252,   0,   0,
      0,   0,   0,  30,   0, 128,   0, 176,   0,   0,   0,  48,   0,   0,   3,   0,
      0,   0, 128, 255,   3,   0,   0,   0,   0,   1,   0,   0, 255, 255,   3,   0,
      0, 120,   0,   0,   0,   0,   8,   0,  32,   0,   0,   0,   0,   0,   0,  56,
      7,   0,   0,   0,   0,   0,  64,   0,   0,   0,   0, 248,   0,  48,   0,   0,
    255, 255,   0,   0,   0,   0,   1,   0,   0,   0,   0, 192,   8,   0,   0,   0,
     96,   0,   0,   0, 252,   0,   0,   0,   0,   0,   0,   6,   0,   0,  24,   0,
      1,  28,   0,   0,   0,   0,  96,   0,   0,   6,   0,   0, 192,  31,  31,   0,
     68,   0,   0,   0,  12,   0,   0,   0,   0,   8,   0,   0, 128,   0,   0,   0,
     52,   0,   0,   0,   0,   0, 128,   0,   0,   0,  31,   0,   0, 128, 255, 255,
    128, 227,   7, 248, 231,  15,   0,   0,   0,  60,   0,   0,   0,   0, 127,   0,
    112,   7,   0,   0,
};

/* Diacritic: 1093 bytes. */

RE_UINT32 re_get_diacritic(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_diacritic_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_diacritic_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_diacritic_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_diacritic_stage_4[pos + f] << 5;
    pos += code;
    value = (re_diacritic_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Extender. */

static RE_UINT8 re_extender_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_extender_stage_2[] = {
     0,  1,  2,  3,  2,  2,  4,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  5,  6,  2,  2,  2,  2,  2,  2,  2,  2,  2,  7,
     2,  2,  8,  9,  2,  2,  2,  2,  2,  2,  2,  2,  2, 10,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2, 11,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
};

static RE_UINT8 re_extender_stage_3[] = {
     0,  1,  2,  1,  1,  1,  3,  4,  1,  1,  1,  1,  1,  1,  5,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  6,  1,  7,  1,  8,  1,  1,  1,
     9,  1,  1,  1,  1,  1,  1,  1, 10,  1,  1,  1,  1,  1, 11,  1,
     1, 12, 13,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 14,
     1,  1,  1, 15,  1, 16,  1,  1,  1,  1, 17,  1,  1,  1,  1,  1,
     1,  1,  1, 18,  1,  1,  1, 19,  1, 20,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_extender_stage_4[] = {
     0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  2,  0,  0,  0,  3,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  4,  0,  0,  5,  0,  0,  0,  5,  0,
     6,  0,  7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  8,  0,  0,
     0,  9,  0, 10,  0,  0,  0,  0, 11, 12,  0,  0, 13,  0,  0, 14,
    15,  0,  0,  0,  0,  0,  0,  0, 16,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 17,  5,  0,  0,  0, 18,  0,  0, 19, 20,
     0,  0,  0, 18,  0,  0,  0,  0,  0,  0, 19,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 21,  0,  0,  0,  0,  0, 22,  0,  0,  0,
     0,  0, 23,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 24,
     0,  0, 25,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_extender_stage_5[] = {
      0,   0,   0,   0,   0,   0, 128,   0,   0,   0,   3,   0,   1,   0,   0,   0,
      0,   0,   0,   4,  64,   0,   0,   0,   0,   4,   0,   0,   8,   0,   0,   0,
    128,   0,   0,   0,   0,   0,  64,   0,   0,   0,   0,   8,  32,   0,   0,   0,
      0,   0,  62,   0,   0,   0,   0,  96,   0,   0,   0, 112,   0,   0,  32,   0,
      0,  16,   0,   0,   0, 128,   0,   0,   0,   0,   1,   0,   0,   0,   0,  32,
      0,   0,  24,   0, 192,   1,   0,   0,   0,   0,   0,   1,  12,   0,   0,   0,
      3,   0,   0,   0, 112,   0,   0,   0,
};

/* Extender: 481 bytes. */

RE_UINT32 re_get_extender(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_extender_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_extender_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_extender_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_extender_stage_4[pos + f] << 5;
    pos += code;
    value = (re_extender_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Other_Lowercase. */

static RE_UINT8 re_other_lowercase_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_other_lowercase_stage_2[] = {
    0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
};

static RE_UINT8 re_other_lowercase_stage_3[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2,
    4, 2, 5, 2, 2, 2, 6, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 7, 2, 8, 2, 2,
};

static RE_UINT8 re_other_lowercase_stage_4[] = {
     0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  2,  3,  0,  4,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  6,  7,  0,
     0,  8,  9,  0,  0, 10,  0,  0,  0,  0,  0, 11,  0,  0,  0,  0,
     0, 12,  0,  0,  0,  0,  0,  0,  0,  0, 13,  0,  0, 14,  0, 15,
     0,  0,  0,  0,  0, 16,  0,  0,
};

static RE_UINT8 re_other_lowercase_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   4,   0,   4,
      0,   0,   0,   0,   0,   0, 255,   1,   3,   0,   0,   0,  31,   0,   0,   0,
     32,   0,   0,   0,   0,   0,   0,   4,   0,   0,   0,   0,   0, 240, 255, 255,
    255, 255, 255, 255, 255,   7,   0,   1,   0,   0,   0, 248, 255, 255, 255, 255,
      0,   0,   0,   0,   0,   0,   2, 128,   0,   0, 255,  31,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 255, 255,   0,   0, 255, 255, 255,   3,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  48,   0,   0,   0,  48,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   3,
      0,   0,   0, 240,   0,   0,   0,   0,
};

/* Other_Lowercase: 297 bytes. */

RE_UINT32 re_get_other_lowercase(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_other_lowercase_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_other_lowercase_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_other_lowercase_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_other_lowercase_stage_4[pos + f] << 6;
    pos += code;
    value = (re_other_lowercase_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Other_Uppercase. */

static RE_UINT8 re_other_uppercase_stage_1[] = {
    0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1,
};

static RE_UINT8 re_other_uppercase_stage_2[] = {
    0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
};

static RE_UINT8 re_other_uppercase_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0,
    0, 3, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_other_uppercase_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 2, 1, 0, 0, 3, 4, 4, 5, 0, 0, 0,
};

static RE_UINT8 re_other_uppercase_stage_5[] = {
      0,   0,   0,   0, 255, 255,   0,   0,   0,   0, 192, 255,   0,   0, 255, 255,
    255,   3, 255, 255, 255,   3,   0,   0,
};

/* Other_Uppercase: 162 bytes. */

RE_UINT32 re_get_other_uppercase(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_other_uppercase_stage_1[f] << 4;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_other_uppercase_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_other_uppercase_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_other_uppercase_stage_4[pos + f] << 5;
    pos += code;
    value = (re_other_uppercase_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Noncharacter_Code_Point. */

static RE_UINT8 re_noncharacter_code_point_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_noncharacter_code_point_stage_2[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
};

static RE_UINT8 re_noncharacter_code_point_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
    0, 0, 0, 0, 0, 0, 0, 2,
};

static RE_UINT8 re_noncharacter_code_point_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0, 0, 2,
};

static RE_UINT8 re_noncharacter_code_point_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255, 255, 255,   0,   0,
      0,   0,   0,   0,   0,   0,   0, 192,
};

/* Noncharacter_Code_Point: 121 bytes. */

RE_UINT32 re_get_noncharacter_code_point(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_noncharacter_code_point_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_noncharacter_code_point_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_noncharacter_code_point_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_noncharacter_code_point_stage_4[pos + f] << 6;
    pos += code;
    value = (re_noncharacter_code_point_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Other_Grapheme_Extend. */

static RE_UINT8 re_other_grapheme_extend_stage_1[] = {
    0, 1, 1, 2, 3, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1,
};

static RE_UINT8 re_other_grapheme_extend_stage_2[] = {
    0, 1, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 5, 0, 0, 0, 0, 0,
    0, 0, 6, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_other_grapheme_extend_stage_3[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  2,  3,  4,  0,  0,
     5,  0,  0,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  7,  0,  0,  0,  8,  9, 10,  0,  0,
     0, 11,  0,  0,  0,  0,  0,  0, 12,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_other_grapheme_extend_stage_4[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  2,  0,
     0,  1,  2,  0,  0,  1,  2,  0,  0,  0,  0,  0,  0,  0,  3,  0,
     0,  1,  2,  0,  0,  0,  4,  0,  5,  0,  0,  0,  0,  0,  0,  0,
     0,  6,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7,  0,  0,  0,
     0,  1,  2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  8,  0,  0,
     0,  0,  0,  0,  0,  9,  0,  0,  0,  0,  0, 10,  0,  0,  0,  0,
     0, 11, 11, 11,  0,  0,  0,  0,
};

static RE_UINT8 re_other_grapheme_extend_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,  64,   0,   0, 128,   0,   4,   0,  96,   0,
      0, 128,   0, 128,   0,  16,   0,   0,   0, 192,   0,   0,   0,   0,   0, 192,
      0,   0,   1,  32,   0, 128,   0,   0,  32, 192,   7,   0, 255, 255, 255, 255,
};

/* Other_Grapheme_Extend: 332 bytes. */

RE_UINT32 re_get_other_grapheme_extend(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 14;
    code = ch ^ (f << 14);
    pos = (RE_UINT32)re_other_grapheme_extend_stage_1[f] << 3;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_other_grapheme_extend_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_other_grapheme_extend_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_other_grapheme_extend_stage_4[pos + f] << 5;
    pos += code;
    value = (re_other_grapheme_extend_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* IDS_Binary_Operator. */

static RE_UINT8 re_ids_binary_operator_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_ids_binary_operator_stage_2[] = {
    0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_ids_binary_operator_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
};

static RE_UINT8 re_ids_binary_operator_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
};

static RE_UINT8 re_ids_binary_operator_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 243,  15,
};

/* IDS_Binary_Operator: 97 bytes. */

RE_UINT32 re_get_ids_binary_operator(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_ids_binary_operator_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_ids_binary_operator_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_ids_binary_operator_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_ids_binary_operator_stage_4[pos + f] << 6;
    pos += code;
    value = (re_ids_binary_operator_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* IDS_Trinary_Operator. */

static RE_UINT8 re_ids_trinary_operator_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_ids_trinary_operator_stage_2[] = {
    0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_ids_trinary_operator_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
};

static RE_UINT8 re_ids_trinary_operator_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
};

static RE_UINT8 re_ids_trinary_operator_stage_5[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 12,  0,
};

/* IDS_Trinary_Operator: 97 bytes. */

RE_UINT32 re_get_ids_trinary_operator(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_ids_trinary_operator_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_ids_trinary_operator_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_ids_trinary_operator_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_ids_trinary_operator_stage_4[pos + f] << 6;
    pos += code;
    value = (re_ids_trinary_operator_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Radical. */

static RE_UINT8 re_radical_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_radical_stage_2[] = {
    0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_radical_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
};

static RE_UINT8 re_radical_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 2, 2, 3, 2, 2, 2, 2, 2, 2, 4, 0,
};

static RE_UINT8 re_radical_stage_5[] = {
      0,   0,   0,   0, 255, 255, 255, 251, 255, 255, 255, 255, 255, 255,  15,   0,
    255, 255,  63,   0,
};

/* Radical: 117 bytes. */

RE_UINT32 re_get_radical(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_radical_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_radical_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_radical_stage_3[pos + f] << 4;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_radical_stage_4[pos + f] << 5;
    pos += code;
    value = (re_radical_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Unified_Ideograph. */

static RE_UINT8 re_unified_ideograph_stage_1[] = {
    0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_unified_ideograph_stage_2[] = {
    0, 0, 0, 1, 2, 3, 3, 3, 3, 4, 0, 0, 0, 0, 0, 5,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 6, 7, 8, 3, 9, 0,
};

static RE_UINT8 re_unified_ideograph_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 4, 0, 0,
    1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 6, 7, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 9, 0, 0,
};

static RE_UINT8 re_unified_ideograph_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 2, 0, 1, 1, 1, 1, 1, 1, 1, 3,
    4, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 5, 1, 1, 1, 1,
    1, 1, 1, 1, 6, 1, 1, 1, 7, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9,
};

static RE_UINT8 re_unified_ideograph_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255,  63,   0, 255, 255, 255, 255, 255, 255,   0,   0,
      0, 192,  26, 128, 154,   3,   0,   0, 255, 255, 127,   0,   0,   0,   0,   0,
    255, 255, 255, 255, 255, 255,  31,   0, 255, 255, 255,  63, 255, 255, 255, 255,
    255, 255, 255, 255,   3,   0, 255, 255, 255, 255, 255, 255,   1,   0,   0,   0,
};

/* Unified_Ideograph: 305 bytes. */

RE_UINT32 re_get_unified_ideograph(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_unified_ideograph_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_unified_ideograph_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_unified_ideograph_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_unified_ideograph_stage_4[pos + f] << 6;
    pos += code;
    value = (re_unified_ideograph_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Other_Default_Ignorable_Code_Point. */

static RE_UINT8 re_other_default_ignorable_code_point_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1,
};

static RE_UINT8 re_other_default_ignorable_code_point_stage_2[] = {
    0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
};

static RE_UINT8 re_other_default_ignorable_code_point_stage_3[] = {
    0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0,
    4, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,
    7, 8, 8, 8, 8, 8, 8, 8,
};

static RE_UINT8 re_other_default_ignorable_code_point_stage_4[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,
     0,  0,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,
     0,  4,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  0,  0,
     0,  0,  0,  0,  0,  0,  6,  7,  8,  0,  9,  9,  0,  0,  0, 10,
     9,  9,  9,  9,  9,  9,  9,  9,
};

static RE_UINT8 re_other_default_ignorable_code_point_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0, 128,   0,   0,   0,   0,   0,   0,
      0,   0,   0, 128,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,  48,   0,
      0,   0,   0,   0,  32,   0,   0,   0,   0,   0,   0,   0,  16,   0,   0,   0,
      0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255,   1,
    253, 255, 255, 255,   0,   0,   0,   0, 255, 255, 255, 255, 255, 255, 255, 255,
      0,   0,   0,   0,   0,   0, 255, 255,
};

/* Other_Default_Ignorable_Code_Point: 281 bytes. */

RE_UINT32 re_get_other_default_ignorable_code_point(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_other_default_ignorable_code_point_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_other_default_ignorable_code_point_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_other_default_ignorable_code_point_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_other_default_ignorable_code_point_stage_4[pos + f] << 6;
    pos += code;
    value = (re_other_default_ignorable_code_point_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Deprecated. */

static RE_UINT8 re_deprecated_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1,
    1, 1,
};

static RE_UINT8 re_deprecated_stage_2[] = {
    0, 1, 2, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
};

static RE_UINT8 re_deprecated_stage_3[] = {
    0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3,
    0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0,
    5, 0, 0, 6, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_deprecated_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
    0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
    0, 6, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_deprecated_stage_5[] = {
      0,   0,   0,   0,   0,   2,   0,   0,   0,   0,   8,   0,   0,   0, 128,   2,
     24,   0,   0,   0,   0, 252,   0,   0,   0,   6,   0,   0,   2,   0,   0,   0,
};

/* Deprecated: 226 bytes. */

RE_UINT32 re_get_deprecated(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_deprecated_stage_1[f] << 4;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_deprecated_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_deprecated_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_deprecated_stage_4[pos + f] << 5;
    pos += code;
    value = (re_deprecated_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Soft_Dotted. */

static RE_UINT8 re_soft_dotted_stage_1[] = {
    0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1,
};

static RE_UINT8 re_soft_dotted_stage_2[] = {
    0, 1, 1, 2, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_soft_dotted_stage_3[] = {
     0,  1,  2,  3,  4,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,
     5,  5,  5,  5,  5,  6,  7,  5,  8,  9,  5,  5,  5,  5,  5,  5,
     5,  5,  5,  5, 10,  5,  5,  5,  5,  5,  5,  5, 11, 12, 13,  5,
};

static RE_UINT8 re_soft_dotted_stage_4[] = {
     0,  0,  0,  1,  0,  0,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,
     0,  0,  3,  4,  5,  6,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7,
     0,  0,  8,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  9, 10, 11,  0,  0,  0, 12,  0,  0,  0,  0, 13,  0,
     0,  0,  0, 14,  0,  0,  0,  0,  0,  0, 15,  0,  0,  0,  0,  0,
     0,  0,  0, 16,  0,  0,  0,  0,  0, 17, 18,  0, 19, 20,  0, 21,
     0, 22, 23,  0, 24,  0, 17, 18,  0, 19, 20,  0, 21,  0,  0,  0,
};

static RE_UINT8 re_soft_dotted_stage_5[] = {
      0,   0,   0,   0,   0,   6,   0,   0,   0, 128,   0,   0,   0,   2,   0,   0,
      0,   1,   0,   0,   0,   0,   0,  32,   0,   0,   4,   0,   0,   0,   8,   0,
      0,   0,  64,   1,   4,   0,   0,   0,   0,   0,  64,   0,  16,   1,   0,   0,
      0,  32,   0,   0,   0,   8,   0,   0,   0,   0,   2,   0,   0,   3,   0,   0,
      0,   0,   0,  16,  12,   0,   0,   0,   0,   0, 192,   0,   0,  12,   0,   0,
      0,   0,   0, 192,   0,   0,  12,   0, 192,   0,   0,   0,   0,   0,   0,  12,
      0, 192,   0,   0,
};

/* Soft_Dotted: 342 bytes. */

RE_UINT32 re_get_soft_dotted(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_soft_dotted_stage_1[f] << 4;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_soft_dotted_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_soft_dotted_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_soft_dotted_stage_4[pos + f] << 5;
    pos += code;
    value = (re_soft_dotted_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Logical_Order_Exception. */

static RE_UINT8 re_logical_order_exception_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_logical_order_exception_stage_2[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
};

static RE_UINT8 re_logical_order_exception_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0,
};

static RE_UINT8 re_logical_order_exception_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_logical_order_exception_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0,  31,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 224,   4,   0,   0,   0,   0,   0,   0,  96,  26,
};

/* Logical_Order_Exception: 145 bytes. */

RE_UINT32 re_get_logical_order_exception(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_logical_order_exception_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_logical_order_exception_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_logical_order_exception_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_logical_order_exception_stage_4[pos + f] << 6;
    pos += code;
    value = (re_logical_order_exception_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Other_ID_Start. */

static RE_UINT8 re_other_id_start_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_other_id_start_stage_2[] = {
    0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_other_id_start_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
    2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_other_id_start_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_other_id_start_stage_5[] = {
     0,  0,  0,  0,  0,  0,  0,  0, 96,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  1,  0, 64,  0,  0,  0,  0,  0, 24,  0,  0,  0,  0,
};

/* Other_ID_Start: 145 bytes. */

RE_UINT32 re_get_other_id_start(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_other_id_start_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_other_id_start_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_other_id_start_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_other_id_start_stage_4[pos + f] << 6;
    pos += code;
    value = (re_other_id_start_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Other_ID_Continue. */

static RE_UINT8 re_other_id_continue_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_other_id_continue_stage_2[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_other_id_continue_stage_3[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 4, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
};

static RE_UINT8 re_other_id_continue_stage_4[] = {
    0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 4,
};

static RE_UINT8 re_other_id_continue_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 128,   0,
    128,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 254,   3,   0,
      0,   0,   0,   4,   0,   0,   0,   0,
};

/* Other_ID_Continue: 145 bytes. */

RE_UINT32 re_get_other_id_continue(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_other_id_continue_stage_1[f] << 3;
    f = code >> 13;
    code ^= f << 13;
    pos = (RE_UINT32)re_other_id_continue_stage_2[pos + f] << 4;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_other_id_continue_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_other_id_continue_stage_4[pos + f] << 6;
    pos += code;
    value = (re_other_id_continue_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Sentence_Terminal. */

static RE_UINT8 re_sentence_terminal_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_sentence_terminal_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  8,  9,  7,  7,  7,  7,  7,  7,  7,  7,  7, 10,
     7, 11, 12, 13,  7,  7,  7,  7,  7,  7,  7,  7,  7, 14,  7,  7,
     7,  7,  7,  7,  7,  7,  7, 15,  7,  7,  7, 16,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
};

static RE_UINT8 re_sentence_terminal_stage_3[] = {
     0,  1,  1,  1,  1,  2,  3,  4,  5,  6,  1,  1,  1,  1,  1,  1,
     7,  1,  1,  8,  1,  1,  9, 10, 11, 12, 13, 14, 15,  1,  1,  1,
    16,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 17,  1,
    18,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1, 19,  1, 20,  1, 21, 22, 23, 24,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1, 25, 26,  1,  1, 27,  1,  1,  1,  1, 28,
    29, 30, 31,  1, 32, 33, 34, 35,  1,  1, 36,  1, 34,  1, 37,  1,
     1,  1, 38, 39,  1,  1, 40,  1,  1,  1,  1,  1, 41,  1,  1,  1,
     1,  1, 42,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_sentence_terminal_stage_4[] = {
     0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  2,  0,  0,  0,  3,  0,  0,  0,  0,  0,  4,  0,
     5,  0,  0,  0,  0,  0,  0,  6,  0,  7,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  8,  0,  0,  0,  0,  0,  0,  9,  0,  0,  0,  0,  0,
     0,  0,  0, 10,  0,  0,  0,  0,  0,  0,  0, 11,  0,  0,  0,  0,
     0, 12,  0,  0,  0,  0,  0,  0, 13,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  8,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 14,  0,  0,
     0,  0, 15,  0,  0,  0,  0,  0,  0, 16,  0,  3,  0,  0,  0,  0,
     0, 17, 18,  0,  0,  0,  0,  0,  0, 19,  0,  0,  0,  0,  0,  0,
    20,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 21,
    22,  0,  0,  0,  0,  0,  0, 23,  0,  0,  0, 24,  0,  0, 22,  0,
     0, 25,  0,  0,  0,  0, 26,  0,  0,  0, 27,  0,  0,  0,  0, 28,
     0,  0,  0,  0,  0,  0,  0, 29,  0,  0, 30,  0,  0,  0,  0,  0,
     1,  0,  0, 31,  0,  0,  0,  0,  0,  0, 24,  0,  0,  0,  0,  0,
     0,  0, 32,  0,  0,  0,  0,  0,  0,  0, 33,  0,  0,  3, 34,  0,
     0,  0, 35,  0,  0,  0, 36,  0,  0, 37,  0,  0,  0,  2,  0,  0,
     0,  0, 38,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 39,  0,
     0,  0, 40,  0,  0,  0,  0,  0,  0, 41,  0,  0,  0,  0,  0,  0,
     0,  0, 42,  0, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 43,
     0,  0,  0, 22,  0,  0,  0, 44,  0, 43, 45,  0,  0,  0,  0,  0,
     0,  0,  0,  0, 46,  0,  0,  0,  0,  0,  0,  0, 21,  0,  0,  0,
     0,  0,  0,  0, 47,  0,  0,  0,
};

static RE_UINT8 re_sentence_terminal_stage_5[] = {
      0,   0,   0,   0,   2,  64,   0, 128,   0,   2,   0,   0,   0,   0,   0, 192,
      0,   0,  16,   0,   7,   0,   0,   0,   0,   0,   0,   2,   0,   0, 128,  98,
     48,   0,   0,   0,   0,  12,   0,   0, 132,   1,   0,   0,   0,  64,   0,   0,
      0,   0,  96,   0,   8,   2,   0,   0,   0,  15,   0,   0,   0,   0,   0, 204,
      0,   0,   0,  24,   0,   0,   0,  48, 128,   3,   0,   0,   0,  64,   0,  16,
      4,   0,   0,   0,   0,   0,   0, 128,   0, 192,   0,   0,   0,   0, 136,   0,
      0,   0, 192,   0,   0, 128,   0,   0,   0,   3,   0,   0,   0,   0,   0, 224,
      0,   0,   3,   0,   0,   8,   0,   0,   0,   0, 196,   0,   2,   0,   0,   0,
      0,   0, 224,   3, 128,   1,   0,   0,   3,   0,   0,   0,  14,   0,   0,   0,
     96,  32,   0, 192,   0,   0,   0,  27,   0,  24,   0,   0,  12, 254, 255,   0,
      6,   0,   0,   0,   0,   0,   0, 112,  12,   0,   0,   0,   0,   0, 128,   1,
      0,   0,  32,   0,  16,   0,   0,   0,   0,   0,   0,   1,   0,   1,   0,   0,
};

/* Sentence_Terminal: 785 bytes. */

RE_UINT32 re_get_sentence_terminal(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_sentence_terminal_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_sentence_terminal_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_sentence_terminal_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_sentence_terminal_stage_4[pos + f] << 5;
    pos += code;
    value = (re_sentence_terminal_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Variation_Selector. */

static RE_UINT8 re_variation_selector_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1,
};

static RE_UINT8 re_variation_selector_stage_2[] = {
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_variation_selector_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_variation_selector_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 4,
};

static RE_UINT8 re_variation_selector_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,  56,   0,   0,   0,   0,   0,   0,
    255, 255,   0,   0,   0,   0,   0,   0, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255,   0,   0,
};

/* Variation_Selector: 169 bytes. */

RE_UINT32 re_get_variation_selector(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_variation_selector_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_variation_selector_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_variation_selector_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_variation_selector_stage_4[pos + f] << 6;
    pos += code;
    value = (re_variation_selector_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Pattern_White_Space. */

static RE_UINT8 re_pattern_white_space_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_pattern_white_space_stage_2[] = {
    0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_pattern_white_space_stage_3[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    2, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_pattern_white_space_stage_4[] = {
    0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    3, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_pattern_white_space_stage_5[] = {
      0,  62,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     32,   0,   0,   0,   0,   0,   0,   0,   0, 192,   0,   0,   0,   3,   0,   0,
};

/* Pattern_White_Space: 129 bytes. */

RE_UINT32 re_get_pattern_white_space(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_pattern_white_space_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_pattern_white_space_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_pattern_white_space_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_pattern_white_space_stage_4[pos + f] << 6;
    pos += code;
    value = (re_pattern_white_space_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Pattern_Syntax. */

static RE_UINT8 re_pattern_syntax_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_pattern_syntax_stage_2[] = {
    0, 1, 1, 1, 2, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_pattern_syntax_stage_3[] = {
     0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     2,  3,  4,  4,  5,  4,  4,  6,  4,  4,  4,  4,  1,  1,  7,  1,
     8,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  9, 10,  1,
};

static RE_UINT8 re_pattern_syntax_stage_4[] = {
     0,  1,  2,  2,  0,  3,  4,  4,  0,  0,  0,  0,  0,  0,  0,  0,
     5,  6,  7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  8,  8,  8,
     8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  0,  0,  0,  0,  0,
     8,  8,  8,  9, 10,  8,  8,  8,  8,  8,  8,  8,  0,  0,  0,  0,
    11, 12,  0,  0,  0,  0,  0,  0,  0, 13,  0,  0,  0,  0,  0,  0,
     0,  0, 14,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_pattern_syntax_stage_5[] = {
      0,   0,   0,   0, 254, 255,   0, 252,   1,   0,   0, 120, 254,  90,  67, 136,
      0,   0, 128,   0,   0,   0, 255, 255, 255,   0, 255, 127, 254, 255, 239, 127,
    255, 255, 255, 255, 255, 255,  63,   0,   0,   0, 240, 255,  14, 255, 255, 255,
      1,   0,   1,   0,   0,   0,   0, 192,  96,   0,   0,   0,
};

/* Pattern_Syntax: 277 bytes. */

RE_UINT32 re_get_pattern_syntax(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_pattern_syntax_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_pattern_syntax_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_pattern_syntax_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_pattern_syntax_stage_4[pos + f] << 5;
    pos += code;
    value = (re_pattern_syntax_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Prepended_Concatenation_Mark. */

static RE_UINT8 re_prepended_concatenation_mark_stage_1[] = {
    0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1,
};

static RE_UINT8 re_prepended_concatenation_mark_stage_2[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 2, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_prepended_concatenation_mark_stage_3[] = {
    0, 0, 0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_prepended_concatenation_mark_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0,
    3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
    0, 0, 0, 0, 0, 2, 5, 0,
};

static RE_UINT8 re_prepended_concatenation_mark_stage_5[] = {
      0,   0,   0,   0,  63,   0,   0,   0,   0,   0,   0,  32,   0, 128,   0,   0,
      4,   0,   0,   0,   0,  32,   0,   0,
};

/* Prepended_Concatenation_Mark: 170 bytes. */

RE_UINT32 re_get_prepended_concatenation_mark(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_prepended_concatenation_mark_stage_1[f] << 3;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_prepended_concatenation_mark_stage_2[pos + f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_prepended_concatenation_mark_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_prepended_concatenation_mark_stage_4[pos + f] << 5;
    pos += code;
    value = (re_prepended_concatenation_mark_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Regional_Indicator. */

static RE_UINT8 re_regional_indicator_stage_1[] = {
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0,
};

static RE_UINT8 re_regional_indicator_stage_2[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
};

static RE_UINT8 re_regional_indicator_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_regional_indicator_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
};

static RE_UINT8 re_regional_indicator_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 192, 255, 255, 255,
};

/* Regional_Indicator: 97 bytes. */

RE_UINT32 re_get_regional_indicator(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_regional_indicator_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_regional_indicator_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_regional_indicator_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_regional_indicator_stage_4[pos + f] << 6;
    pos += code;
    value = (re_regional_indicator_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Hangul_Syllable_Type. */

static RE_UINT8 re_hangul_syllable_type_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_hangul_syllable_type_stage_2[] = {
    0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_hangul_syllable_type_stage_3[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  1,  2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  3,  0,  0,  0,  0,  0,  4,  5,  6,  7,  8,  9, 10,  4,
     5,  6,  7,  8,  9, 10,  4,  5,  6,  7,  8,  9, 10,  4,  5,  6,
     7,  8,  9, 10,  4,  5,  6,  7,  8,  9, 10,  4,  5,  6,  7,  8,
     9, 10,  4,  5,  6,  7,  8,  9, 10,  4,  5,  6,  7,  8,  9, 10,
     4,  5,  6,  7,  8,  9, 10,  4,  5,  6,  7,  8,  9, 10,  4,  5,
     6,  7,  8,  9, 10,  4,  5,  6,  7,  8,  9, 10,  4,  5,  6, 11,
};

static RE_UINT8 re_hangul_syllable_type_stage_4[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,
     2,  2,  2,  2,  2,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  4,
     5,  6,  6,  7,  6,  6,  6,  5,  6,  6,  7,  6,  6,  6,  5,  6,
     6,  7,  6,  6,  6,  5,  6,  6,  7,  6,  6,  6,  5,  6,  6,  7,
     6,  6,  6,  5,  6,  6,  7,  6,  6,  6,  5,  6,  6,  7,  6,  6,
     6,  5,  6,  6,  7,  6,  6,  6,  5,  6,  6,  7,  6,  6,  6,  5,
     6,  6,  7,  6,  6,  6,  5,  6,  6,  7,  6,  6,  6,  5,  6,  6,
     7,  6,  6,  6,  5,  6,  6,  7,  6,  6,  6,  5,  6,  6,  7,  6,
     6,  6,  5,  6,  6,  7,  6,  6,  6,  5,  6,  6,  7,  6,  6,  6,
     6,  5,  6,  6,  8,  0,  2,  2,  9, 10,  3,  3,  3,  3,  3, 11,
};

static RE_UINT8 re_hangul_syllable_type_stage_5[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
    1, 1, 1, 1, 1, 0, 0, 0, 4, 5, 5, 5, 5, 5, 5, 5,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5,
    5, 5, 5, 5, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0,
    0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0,
};

/* Hangul_Syllable_Type: 497 bytes. */

RE_UINT32 re_get_hangul_syllable_type(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_hangul_syllable_type_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_hangul_syllable_type_stage_2[pos + f] << 4;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_hangul_syllable_type_stage_3[pos + f] << 4;
    f = code >> 3;
    code ^= f << 3;
    pos = (RE_UINT32)re_hangul_syllable_type_stage_4[pos + f] << 3;
    value = re_hangul_syllable_type_stage_5[pos + code];

    return value;
}

/* Bidi_Class. */

static RE_UINT8 re_bidi_class_stage_1[] = {
     0,  1,  2,  3,  4,  5,  5,  5,  5,  5,  6,  5,  5,  5,  5,  7,
     8,  9,  5,  5,  5,  5, 10,  5,  5,  5,  5, 11,  5, 12, 13, 14,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
    16,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
};

static RE_UINT8 re_bidi_class_stage_2[] = {
      0,   1,   2,   3,   4,   4,   4,   4,   4,   4,   5,   6,   7,   8,   9,  10,
      4,   4,  11,   4,   4,   4,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,
     22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  30,  32,  33,  34,  35,  36,
     37,  38,  28,  39,  40,  41,   4,  42,  43,  44,  45,  46,  47,  48,  49,  50,
     51,  52,  53,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,  54,  55,   4,
     56,   4,   4,   4,   4,   4,   4,   4,   4,   4,  57,   4,  58,  59,  60,  61,
     62,   4,  63,   4,  64,  65,   4,  66,  67,  68,  69,   4,  70,  71,  72,  73,
     74,   4,   4,  75,   4,   4,   4,  76,   4,   4,   4,   4,   4,   4,  77,  78,
     79,  80,  81,  82,  83,  84,  85,  86,  87,  86,  86,  86,  88,  89,  90,  86,
     91,  92,  93,  94,  86,  86,  86,  86,  86,  86,  95,  86,  86,  86,  86,  86,
      4,   4,   4,   4,  86,  86,  86,  86,  86,  86,  86,  86,  86,  96,  97,  98,
      4,   4,   4,  99,   4, 100,   4, 101,  86, 102, 103, 104,  86,  86,  86, 105,
    106,   4, 107, 108,   4,   4,   4, 109, 110, 111, 112, 113,   4, 114,   4, 115,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,  86,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4, 116, 117,   4,   4,   4,   4, 118, 119, 120, 121, 122,   4, 123,   4,
    124, 125,   4, 126, 127, 128, 129, 130, 131, 132, 133, 134,   4,   4,   4, 135,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 136, 137,  16,  16,
     16,  16,  16,  16, 138,  16,  16, 139, 140, 141,  16, 142, 143, 144,   4, 145,
      4,   4,   4,   4, 146,  86, 147, 148,   4,   4,   4, 149,   4, 150,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
    151, 151, 151, 151, 152, 151, 151, 151, 153, 151, 151, 154, 155, 151, 151, 151,
    151, 151, 151, 151, 156, 151, 151, 151, 151, 157, 151, 151, 158, 159, 151, 151,
    160, 161, 162,   4, 163, 164, 165, 166, 167,   4,   4, 168,  40, 169,   4,   4,
    170, 171, 172, 173,   4,   4, 174, 175, 176, 177, 178,   4, 179,   4,   4,   4,
    180,   4,   4,   4,   4,   4,   4,   4, 181, 182, 183,   4,   4,   4,   4,   4,
    184,   4, 185,   4, 186, 187, 188,   4,   4,   4,   4, 189,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 190, 191,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 192,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4, 193,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4, 194, 195,   4,  86, 196,   4,   4,  86, 197,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 198, 199, 200, 201, 202,
      4,   4,   4,   4,   4,   4,   4,   4, 203, 204, 205,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
    206,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
    151, 151, 151, 207, 151, 208, 151, 151, 151, 151, 151, 151, 151, 151, 151, 151,
    151, 158,  16, 151, 151, 151, 151, 151,  16,  16,  16, 209, 151, 151, 151, 151,
    210,  86, 211, 212, 213, 214,   4,   4,   4, 215,   4,   4,  86,  86,  86,  86,
     86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86, 216,  86, 104,  86, 217,
    218, 219, 220,   4, 221, 222, 223, 224,   4, 225,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 226,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 226,
    227, 227, 227, 227,   7,   7,   7, 228, 227, 227, 227, 227, 227, 227, 227, 227,
    227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227,
    227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227,
    227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227,
};

static RE_UINT8 re_bidi_class_stage_3[] = {
      0,   1,   0,   2,   3,   4,   5,   6,   7,   8,   8,   9,   7,   8,   8,  10,
     11,   0,   0,   0,  12,  13,  14,  15,   8,   8,  16,   8,   8,   8,  16,   8,
      8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,  17,
     18,  19,  18,  19,  20,  21,  19,  19,  22,  22,  22,  22,  22,  22,  22,  22,
     22,  22,  22,  22,  22,  22,  23,  24,  25,   8,   8,   8,   8,   8,   8,   8,
      8,   8,   8,   8,   8,   8,  24,   8,  26,  27,   8,   8,   8,   8,   8,   8,
      8,  28,  29,  22,  22,  22,  22,  30,  31,  32,  32,  32,  32,  32,  32,  32,
     33,  34,  22,  35,  36,  36,  36,  36,  36,  37,  22,  22,  38,  39,  40,  36,
     36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  41,  42,  43,  44,   5,  45,
     36,  36,  46,  36,  36,  36,  22,  22,  22,  35,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  41,  22,  40,  36,  32,  32,  32,  32,  32,  47,  48,  49,
     32,  32,  50,  51,  52,  53,  32,  32,  32,  32,  32,  54,  36,  36,  32,  32,
     32,  32,  32,  32,  36,  36,  36,  36,  36,  36,  37,  22,  55,  22,  22,  22,
     56,   8,   8,   8,   8,   8,   8,  57,  58,  59,  58,   8,  60,   8,   8,   8,
     61,   8,   8,   8,   8,   8,   8,  62,  63,  64,   8,   8,  60,   8,  65,  66,
     67,   8,   8,   8,   8,   8,   8,  62,  68,  69,  61,   8,   8,   8,  70,   8,
     71,  59,   8,   8,  60,   8,  72,  73,  61,   8,   8,   8,   8,   8,   8,  74,
     63,  64,  75,   8,  60,   8,   8,   8,  76,   8,   8,   8,   8,   8,   8,   8,
     77,  64,   8,   8,   8,   8,   9,  78,  79,   8,   8,   8,   8,   8,   8,  80,
     81,  82,  83,   8,  60,   8,   8,  84,   8,  85,   8,   8,  60,   8,   8,   8,
     27,   8,   8,   8,   8,   8,   8,  86,  63,  64,   8,   8,  60,   8,   8,   8,
      8,  76,  87,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,  88,  89,
     90,  91,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,  88,  92,
      8,  93,   8,   8,   8,   8,   8,   8,   8,   8,   8,  27,   8,   8,  94,  95,
      8,   8,   8,   8,   8,   8,  58,  91,  96,  97,  22,  58,  22,  22,  22,  98,
     75,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,  97,  99, 100,
      8,   8,   8, 101,  77,   8,  63,   8, 102,  64,   8,  64,   8,   8,   8,   8,
      8,   8,   8,  97,   8,   8,   8,   8,   8,   8,  19, 103,   8,   8,   8,   8,
      7,   8,   8,   8,   8,   8,   8,   8, 104,   8,   8, 105,   8,   8,   8,   8,
      8,   8, 106,   8,   8,   8, 106,   8,   8,   8,  60,   8,   8,   8,  60,   8,
      8,   8,   8,   8,   8,   8, 107,  93,  75,  58, 108, 109,   8,   8,  19, 103,
     19, 110,   8,   8,   8,   8,   8,   8,  83,   8,   8,   8,   8,  61,   8,   8,
      8,   8,   8,   8, 111,  77,  76, 112, 113,   8,   8,   8,   8,   8,   8,   8,
      8,   8,   8, 114,  19,  19,  19,  19,   8,   8,  90, 115,   8,   8,   8,   8,
      8,   8,  75,  91, 116,  98,  26, 117,   8,   8,   8,   8,   8,   8,  22,  91,
    108,   8,   8,   8,   8,   8, 118, 119,  76,   8,   8,   8,   8,  26, 108,   8,
     27,   8,   8,   8, 120, 121,   8,   8,   8,   8,   8,   8,  75, 122,  27,   8,
      8,   8,   8,   8,   8, 123, 124,   8,   8,   8, 125,  22,  99,  59,  62,  27,
     22,  22,  22,  22,  22,  22,  22, 126,   8,   8,   8,   8,   8,   8,   8, 127,
    103,  20,   8,  20,   8,  20,   8, 128, 129, 130,  19,  19,  19, 131, 132,  19,
    133,  19,  19, 134, 135, 136, 137, 138,   5, 138,   8,   8, 139, 139, 139, 139,
    139, 139,  22,  22,  22,  22,  77,   8, 140, 103, 141, 142, 143, 144,   8, 145,
    146, 147,  19,  19,   8,   8,   8,   8,   8, 148,  19,  19,  19,  19,  19,  19,
     19,  19,  19,  19,  19,  19,  19,  19,  19,  19, 149,  19,  19,  19,  19,  19,
     19,  19,  19,  19,  19,  19, 150,   8,   8,   8,   8,   8,   8,   8,   8,   9,
     19,  19, 151,  19,  19,  19,  19,  19,  19,  19,  19,  19,  84,   8,   8,   8,
     19, 152,   8,   8,  19,  19,  19,  19,  19,   5,   5, 153,   8,   8,   8,   8,
      8,   8,   8,   8,   8,  18,  19,  19,  19,  19,  19,  19,  19, 154,  19,  19,
     19,  19,  19,  19,  19,  19, 155,  19,  19,  19, 150,  19,  19,  19,  19,  19,
     19, 156,  19,  19,  19,  19,  19,  84,   8,   8,   8,   8,  20, 157,  27, 158,
      8,   8,   8,   8,   8,   8,   8,  90,   8,   8,   8,   8,  22,  22,  22,  22,
     19,  84,   8,   8,   8,   8,   8,   8,  19,  19,  19, 159,  19,  19,  19,  19,
     19,  19,  19,  19,  19,  19, 160,   8,  19,  19, 150,   8,   8,   8,  19, 160,
    161,  19,  19,  19,   7, 120, 142,  20,   8,   8,   8, 162,   7,   8,   8,   8,
      8,   8,   8,   8,   8,   8,   8, 163,  19,  19,  19,  19, 160,   8,   8,   8,
      8,   8,   8, 128,   8,   8,   8,   8,   8,   8,  19,  19,   8,   8,   8, 164,
      8,   8,   8,   8,   8,   8, 158,  19,   8, 165,   8,   8,   8,   8,   8,   8,
      8,   8,   8,   8,   8,   8,  16, 152,   8,   8,   8, 114,   8,   8,   8,  16,
      8,   8,  19,  19,  19,  19,  19,  19,  84,   8,   8,   8,   8,   8,   8,   8,
      8,  20,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,  90, 166, 167,
      8,   8,   8,  80,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,  27,   8,
     19,  19,  19,  19, 103,   8,   8,   8,   8,   7,   8,   8,   8,   8,   8,   8,
    168, 169,   8,   8,  83, 160,   8, 170,   8,   8,   8,   8,   8,   8, 165,   8,
     85,   8,   8,   8,  22,  22,  27,  90,   8,   8,   8,   8,  80,  93,   8,   8,
     90,  22,  27,   8,   8,   8,   8,   8,  56,   8,   8,   8,   8,   8, 171, 172,
      8,   8,   8,   8,  64,   8,   8,   8,   8,   8,   8,   8,   8, 173, 100,   8,
    169,  62,   8,   8,   8,   8,   8,  62,   8,   8,   8,   8,   8,   8, 174,  81,
     61,   8,   8,   8,   8,  85,  75,   8,   8,   8,   8,   8,  64,  59,   8,   8,
      8,   8,   8, 175,  32, 176,  32,  32,  32,  32,  36,  36,  36,  36,  36,  36,
     36,  36,  36,  36,  36,  36,  36, 177,  36,  36,   0,   0,   0,   0,  36, 178,
     22,  22,  19, 103,  22,  22,  19,  19,  19,  19, 179, 180, 181, 182,  36,  36,
     36,  36,  36,  36,  36,  36,  36, 183, 184,   4,   5,   6,   7,   8,   8,   9,
      7,   8,   8,   9, 150,   8,   8,   8,   8,   8,   8,   8, 185,  84,   0, 186,
    187,   8,   8,   8,   8,   8,   8,   8,  19, 146,  19, 160,   7,   8,   8,   8,
      8,   8,   8,   8,   8,   8,   8,  64,   8,   8,   8,   8, 188,   5,   5, 153,
      8,   8,   8,   8,   8,   8,  80,  56,  32,  32,  32,  32,  32,  32,  32,  32,
     32,  32,  32, 189,  32,  32,  32,  32, 190, 191,  32,  32,  32,  32,  32, 192,
     32,  32,  32,  32, 193,  32,  32,  32,  32,  32,  32,  32,  32,  32,  32, 194,
     36,  36,  36,  36, 195,  36,  38, 196,  32,  32,  32,  32,  38,  38,  38, 197,
     32,  32,  32,  32,  32,  32,  36,  36,  41,  22,  40,  36,  36,  36,  32,  32,
     61,   8,   8,   8,   8,   8,   8,  22,  91,   8,  18,  19, 150,   8,   8,  90,
     27,   8,   8,   8,   8,   8, 198,  67,  56,   8,   8,   8,  90, 199,  98,   8,
      8,   8,   8,   8,   8,   8, 169,   8,  27,   8,   8,   8,   8,   8,  80,  91,
      8,  63,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,  90, 200,  75,
      8,   8,   8,  90,  26,  56,   8,   8,  77,   8,   8,   8,  80,  98,  98,   8,
      8,   8,   8,   8,   8,   8,   8,  22,  87,   8,   8,  75,   8,   8,   8,   8,
      8,   8,   8,   8,   8,   8,  26, 201, 202,   8,   8,   8,   8,   8,   8,   8,
      8,   8,   8,   8,   8,   8, 120, 107,  77,   8,   8,  85,   8,   8,   8,   8,
      8,   8,   8,   8,   8,   8,  26, 203,  77,   8,   8,   8,  19, 146,   8,   8,
      8,   8,   8,   8,   8, 204, 205,   8,   8,   8,   8,  97, 206, 108,   8,   8,
      8,   8,   8,   8,   8,  90,  22,  67, 173,  67,   8,   8,   8,   8,  26, 207,
     90,   8, 173, 112,   8,   8,   8,   8,   8,  73,  91,  27,   8,   8,   8,   8,
      8,   8,   8,   8,   8,   8,  91,  93,   8,   8,  73,  22,  22,  73, 208,   8,
      8,   8,   8,   8,   8,   8, 173, 209, 205,   8,   8,   8,   8,   8,   8,   8,
      8,   8, 122,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,  86,   8,
      8,   8,   8,   8,   8,   8,  98,   8,   8,   8,   8,   8,   8,   8,  91,   8,
      8,  90,  56,   8,   8,   8,   8,   8,   8,   8,   8,  83, 210,   8,   8,   8,
      8,   8,   8,   8,  90,  27, 211, 212, 213, 108,   8,   8,   8, 120,   8,   8,
    214,   8,   8,   8,   8,   8,   8,   8,  19,  19,  84,   8,   8,   8,   8,   8,
      8,   8,   8, 163,   8,   8,   8,   8,   8,   8, 215,   8,   8,   8,   8,   8,
      8,  16,   8,   8,   8,   8,   8,   8,   8, 187,   8,   8,   8,   8,   8,   8,
    163, 216,   5,   5,   5,   5,   5,   5,  22,  22,  22,  22,  22,  22,  91,  26,
     22,  22,  22,  22,  22,  98,  64,   8,  62,   8,   8,  26,  58,  22,   8,   8,
     91,  22,  22, 217, 218,  56,   8,   8,  32,  32, 219,  32,  32,  32,  32,  32,
    191, 220,  32,  32,  32,  32,  32,  32,  36,  36,  36,  36,  36,  36, 221,  36,
     19,  19,  19,  19,  19, 160,  19,  19,  19,  19, 160,   8,  19,  84, 158,  19,
    158,  19, 158,  19,  19,  19, 150,   8,   5, 222,   8,   8,   8,  16,   8,   8,
      8,   8,   8,   8,   8, 145,   8,   8,   8,   8,   8,   8, 150,   8,   8,   8,
     19,  19, 146,   8,  19, 146,  19, 103,  19,  19,  19,   7,   8,   8,   8,   8,
     19, 160,  19,  19,  19,  19,  19,  19,  19,   8,  19, 103,  19,  19,  19,  19,
     19,   8,  19,  19,  19, 150,   8,   8,  19, 160,  19,  19,  19,  19,  19,  84,
     19,  19,  19,  19,  19,  19, 223, 224,  19,  19,  19,  19, 152,   8,  19, 103,
    152,   8,  19,  19,  19,  19,  19,  19,   8,   8,   8,   8,  19, 150,   8,   8,
      8,   8,   8,   8,   8,   8,   8, 225,   0,   0,   0,   0,   0,   0,   0,   0,
     22,  22,  22,  22,  22,  22,   0,   0,
};

static RE_UINT8 re_bidi_class_stage_4[] = {
      0,   0,   1,   2,   0,   3,   4,   5,   6,   7,   8,   8,   9,  10,  11,  12,
     12,  12,  13,  10,  13,  14,   0,  15,  16,   5,  17,  18,  19,  20,  21,  10,
     12,  13,  22,  12,  23,  10,  10,  10,  12,  24,  10,  17,  25,  25,  12,  26,
     12,  27,  12,  17,  28,  25,  29,  12,  27,  30,  31,  25,  25,  32,  33,  32,
     34,  34,  35,  36,  37,  38,  39,  40,  40,  40,  41,  25,  35,  35,  42,  43,
     44,  40,  40,  45,  25,  46,  25,  47,  48,  49,  50,  40,  51,  40,  52,  25,
     25,  53,  54,  55,  34,  56,  32,  25,  25,  31,  31,  57,  31,  34,  58,  25,
     59,  12,  60,  61,  62,  25,  61,  63,  64,  12,  63,  12,  12,  61,  62,  61,
     12,  63,  65,  12,  66,  60,  67,  12,  67,  28,  68,  29,  29,  63,  62,  69,
     70,  12,  64,  25,  12,  68,  12,  60,  60,  12,  61,  12,  71,  12,  61,  61,
     12,  64,  61,  64,  72,  29,  12,  67,  10,  73,  12,  29,  28,  61,  64,  74,
     63,  25,  59,  66,  12,  28,  25,  59,  69,  61,  25,  29,  12,  75,  76,  26,
     25,  72,  12,  62,  25,  61,  72,  25,  67,  67,  29,  64,  60,  67,  26,  12,
     77,  12,  13,  11,  64,  61,  12,  69,  25,  12,  66,  63,  78,  79,  59,  28,
     62,  12,  11,  26,  12,  23,  68,  12,  74,  62,  25,  68,  12,  72,  59,  61,
     64,  29,  69,  29,  29,  75,  12,  25,  25,  64,  59,  25,  69,  25,  12,  80,
     12,  22,  81,  81,  82,  83,  84,  85,  86,  87,  10,  88,  10,  89,   0,  90,
     91,   0,  92,   8,  93,  73,  86,  86,  17,  73,  12,  20,  11,  23,  10,  80,
     94,  95,  23,  12,  10,  11,  23,  26,  24,  12,  96,  10,  10,  26,  10,  20,
     73,  12,   8,  12,  10,  24,  10,  23,  20,  10,  73,  28,  24,  10,  17,  10,
     10,  12,  97,  11,  98,  11,  13,  12,  12,  73,  12,  10,  99,  25,  25, 100,
     60,  60,  28,  12, 101,  12,  28,  64,  29,  61,  62,  59,  72,  68,  12, 102,
    103,  34,  40, 104,  40, 105, 106, 107,  10, 108, 109,  73, 110,  12,  40, 111,
     30,   5,   5, 112, 113, 114,  94,  12, 115,   8,  34, 116,  31,  33,  34,  25,
    117,  52,  34,  33, 118,  10,  40,  25, 119,  40,  35, 120,  28,  59,  25,  62,
     29,  72,  74,  28,  72,  12,  59,  75,  28,  63,  25,  69,  64,  69,  68,  59,
     72,  67,  60,  69,   0,  12, 121,   0, 122,  25,  59,  62, 123, 124,  12,  94,
     12, 125,  68,  25,  69,  72,  25, 117, 117,  34, 126,  40, 127,  11, 128,  73,
     27,  10,  12, 129,
};

static RE_UINT8 re_bidi_class_stage_5[] = {
    11, 11, 11, 11, 11,  8,  7,  8,  9,  7, 11, 11,  7,  7,  7,  8,
     9, 10, 10,  4,  4,  4, 10, 10, 10, 10, 10,  3,  6,  3,  6,  6,
     2,  2,  2,  2,  2,  2,  6, 10, 10, 10, 10, 10, 10,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0, 10, 10, 10, 10, 11, 11,  7, 11, 11,
     6, 10,  4,  4, 10, 10,  0, 10, 10, 11, 10, 10,  4,  4,  2,  2,
    10,  0, 10, 10, 10,  2,  0, 10,  0, 10, 10,  0,  0,  0, 10, 10,
     0, 10, 10, 10, 12, 12, 12, 12, 10, 10,  0,  0,  0,  0, 10,  0,
     0,  0,  0, 12, 12, 12,  0,  0,  0, 10, 10,  4,  1, 12, 12, 12,
    12, 12,  1, 12,  1, 12, 12,  1,  1,  1,  1,  1,  5,  5,  5,  5,
     5,  5, 10, 10, 13,  4,  4, 13,  6, 13, 10, 10, 12, 12, 12, 13,
    13, 13, 13, 13, 13, 13, 13, 12,  5,  5,  4,  5,  5, 13, 13, 13,
    12, 13, 13, 13, 13, 13, 12, 12, 12,  5, 10, 12, 12, 13, 13, 12,
    12, 10, 12, 12, 12, 12, 13, 13,  2,  2, 13, 13, 13, 12, 13, 13,
     1,  1,  1, 12,  1,  1, 10, 10, 10, 10,  1,  1,  1, 12,  1,  1,
     1,  1, 12, 12, 12, 12,  1,  1, 12, 12,  5, 12, 12, 12, 12,  0,
     0,  0, 12,  0, 12,  0,  0,  0,  0, 12, 12, 12,  0, 12,  0,  0,
     0,  0, 12, 12,  0,  0,  4,  4,  0,  0,  0,  4,  0, 12, 12,  0,
    12,  0,  0, 12, 12, 12,  0, 12,  0,  4,  0,  0, 10,  4, 10,  0,
    12,  0, 12, 12, 10, 10, 10,  0, 12,  0, 12,  0,  0, 12,  0, 12,
     0, 12, 10, 10,  9,  0,  0,  0, 10, 10, 10, 12, 12, 12, 11,  0,
     0, 10,  0, 10,  9,  9,  9,  9,  9,  9,  9, 11, 11, 11,  0,  1,
     9,  7, 16, 17, 18, 14, 15,  6,  4,  4,  4,  4,  4, 10, 10, 10,
     6, 10, 10, 10, 10, 10, 10,  9, 11, 11, 19, 20, 21, 22, 11, 11,
     2,  0,  0,  0,  2,  2,  3,  3,  0, 10,  0,  0,  0,  0,  4,  0,
    10, 10,  3,  4,  9, 10, 10, 10,  0, 12, 12, 10, 12, 12, 12, 10,
    12, 12, 10, 10,  4,  4,  0,  0,  0,  1, 12,  1,  1,  3,  1,  1,
    13, 13, 10, 10, 13, 10, 13, 13,  6, 10,  6,  0, 10,  6, 10, 10,
    10, 10, 10,  4, 10, 10,  3,  3, 10,  4,  4, 10, 13, 13, 13, 11,
    10,  4,  4,  0, 11, 10, 10, 10, 10, 10, 11, 11, 12,  2,  2,  2,
     1,  1,  1, 10, 12, 12, 12,  1,  1, 10, 10, 10,  5,  5, 13, 13,
     5,  5,  5,  1,  0,  0,  0, 11, 11, 11, 11, 12, 10, 10, 12, 12,
    12, 10,  0,  0,  0,  0,  2,  2, 10, 10, 13, 13,  2,  2,  2, 10,
    10,  0,  0, 10,  0,  0, 11, 11,
};

/* Bidi_Class: 4164 bytes. */

RE_UINT32 re_get_bidi_class(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 12;
    code = ch ^ (f << 12);
    pos = (RE_UINT32)re_bidi_class_stage_1[f] << 6;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_bidi_class_stage_2[pos + f] << 3;
    f = code >> 3;
    code ^= f << 3;
    pos = (RE_UINT32)re_bidi_class_stage_3[pos + f] << 1;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_bidi_class_stage_4[pos + f] << 2;
    value = re_bidi_class_stage_5[pos + code];

    return value;
}

/* Canonical_Combining_Class. */

static RE_UINT8 re_canonical_combining_class_stage_1[] = {
     0,  1,  2,  3,  4,  4,  4,  4,  4,  4,  5,  4,  4,  4,  4,  6,
     7,  8,  4,  4,  4,  4,  9,  4,  4,  4,  4, 10,  4, 11, 12,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
};

static RE_UINT8 re_canonical_combining_class_stage_2[] = {
     0,  0,  0,  0,  0,  0,  1,  0,  0,  2,  0,  3,  4,  5,  6,  7,
     8,  9, 10, 11, 12, 12, 12, 13, 14, 12, 15, 16, 17, 18, 19, 20,
    21, 22,  0,  0,  0,  0, 23,  0,  0,  0,  0,  0,  0,  0, 24, 25,
     0, 26, 27,  0, 28, 29, 30, 31, 32, 33,  0, 34,  0,  0,  0,  0,
     0, 35,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0, 36, 37, 38,  0,  0,  0,  0,
    39, 40,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 41, 42,  0,  0,
    43, 44, 45, 46,  0, 47,  0, 48,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 49,  0,  0,  0,  0,  0, 50,  0,  0,  0,
     0,  0,  0, 51,  0, 52, 53,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0, 54, 55,  0,  0,  0,  0, 56,  0,  0,  0, 57,  0,
    58, 59, 60, 61, 62, 63, 64,  0, 65, 66,  0, 67, 68, 69, 70,  0,
    59,  0,  0,  0, 71, 72,  0,  0, 68,  0, 73, 74,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0, 75, 76,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0, 77,  0,  0,  0,  0,  0,  0,
     0,  0, 78, 79, 80,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    81,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0, 82, 83,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_canonical_combining_class_stage_3[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   1,   2,   3,   4,   5,   6,   7,   0,
      8,   0,   0,   0,   0,   0,   0,   0,   0,   9,  10,  11,  12,   0,   0,   0,
      0,  13,   0,   0,  14,  15,   0,  16,   0,   0,   0,   0,   0,  17,  18,   0,
      0,  19,   0,  20,  21,   0,   0,   0,   0,   0,   0,   0,   0,   0,  22,  23,
      0,  24,  25,   0,   0,  26,   0,   0,   0,   0,   0,   0,   0,  27,  28,  29,
      0,   0,   0,  30,  31,  32,   0,   0,   0,   0,   0,  30,  31,   0,   0,  33,
      0,   0,   0,  30,  31,   0,   0,   0,   0,   0,   0,   0,  31,   0,   0,   0,
      0,   0,   0,   0,  31,  34,   0,   0,   0,   0,   0,  35,  31,   0,   0,   0,
      0,   0,   0,   0,  36,   0,   0,   0,   0,   0,   0,  37,  38,   0,   0,   0,
      0,   0,   0,  39,  40,   0,   0,   0,   0,  41,   0,  42,   0,   0,   0,  43,
     44,   0,   0,   0,  45,   0,   0,   0,   0,   0,   0,  46,   0,   0,   0,   0,
     47,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  48,   0,   0,
      0,  49,   0,  49,   0,   0,   0,   0,   0,   0,   0,   0,   0,  50,   0,   0,
      0,   0,  51,   0,   0,   0,   0,   0,   0,   0,   0,  52,   0,   0,   0,   0,
      0,  53,   0,   0,   0,   0,  54,  55,   0,   0,   0,  56,   0,   0,   0,   0,
      0,   0,   0,  57,  49,   0,  58,  59,   0,   0,  60,   0,   0,   0,  61,  62,
      0,   0,   0,  63,   0,   0,   0,   0,   0,   0,   0,   0,   0,  64,  65,  66,
      0,   0,   0,   0,  67,  68,   1,  69,   0,   0,   0,   0,   0,  70,  71,  72,
      0,   0,   0,   0,   0,   0,  73,  74,   0,   0,   0,   0,   0,   0,   0,  75,
      0,   0,   0,   0,   0,   0,   1,   1,   0,   0,  76,   0,   0,   0,   0,   0,
      0,  77,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  73,  78,
      0,  79,   0,   0,   0,   0,   0,  74,  80,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  49,   0,   1,  74,   0,   0,  81,   0,   0,  82,   0,   0,
      0,   0,   0,  83,  54,   0,   0,   0,   0,   0,   0,  84,  85,   0,   0,  80,
      0,   0,   0,   0,   0,   0,  31,   0,   0,  86,   0,   0,   0,   0,   0,   0,
      0,   0,  87,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  47,
      0,   0,   0,   0,   0,   0,  88,   0,   0,   0,   0,   0,   0,   0,   0,  89,
     90,   0,   0,  91,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  92,   0,
      0,   0,  93,   0,   0,   0,   0,   0,   0,   0,   0,   0,  94,  88,   0,   0,
      0,   0,   0,   0,  80,   0,   0,  75,   0,   0,   0,  95,   0,   0,   0,   0,
     96,   0,   0,  97,   0,   0,   0,  83,   0,   0,   0,   0,  98,   0,   0,   0,
      0,   0,   0,  99,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 100,   0,
      0,   0,   0, 101,  31,   0, 102, 103,   0,   0,   0,   0, 104,  33,   0,   0,
      0,   0,   0,   0, 105,   0,   0,   0,   0,   0,   0,  75, 106,   0,   0,   0,
      0,   0,   0,  75,   0,   0,   0,   0,   0,   0,   0, 107,   0,   0,   0,   0,
      0,   0, 108,   0,   0,   0,   0,   0,   0,   0,   0,  49, 109,   0,   0,   0,
      0, 110,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 111,   0,   0,   0,
      0, 109,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 112,
      0,   0,   0, 113,   0,   0,   0,   0,   0, 114,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 115, 116, 117,   0, 118,   0,   0,   0,   0,   0,
      0,   0,   0,   0, 119,   0,   0,   0, 120, 121, 122,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0, 123,   0,   0,   0,   0,   0,   0, 124,   0,   0,   0,
};

static RE_UINT8 re_canonical_combining_class_stage_4[] = {
      0,   0,   0,   0,   1,   1,   1,   1,   1,   2,   3,   4,   5,   6,   7,   4,
      4,   8,   9,  10,   1,  11,  12,  13,  14,  15,  16,  17,  18,   1,   1,   1,
     19,   1,   0,   0,  20,  21,  22,   1,  23,   4,  21,  24,  25,  26,  27,  28,
     29,  30,   0,   0,   1,   1,  31,   0,   0,   0,  32,  33,  34,  35,   1,  36,
     37,   0,   0,   0,   0,  38,   1,  39,  14,  39,  40,  41,  42,   0,   0,   0,
     43,  36,  44,  45,  21,  45,  46,   0,   0,   0,  19,   1,  21,   0,   0,  47,
      0,  38,  48,   1,   1,  49,  49,  50,   0,   0,  51,   0,  52,   1,   1,   1,
     53,  21,  43,  54,  55,  21,  35,   1,   0,   0,   0,  56,   0,   0,   0,  57,
     58,  59,   0,   0,   0,   0,   0,  60,   0,  61,   0,   0,   0,   0,  62,  63,
      0,   0,  64,   0,   0,   0,  65,   0,   0,   0,  66,   0,   0,   0,  67,   0,
      0,   0,  68,   0,   0,   0,  69,   0,   0,  70,  71,   0,  72,  73,  74,  75,
     76,  77,   0,   0,   0,  78,   0,   0,   0,  79,  80,   0,   0,   0,   0,  47,
      0,   0,   0,  49,   0,  63,   0,   0,  64,   0,   0,  81,   0,   0,  82,   0,
      0,   0,  83,   0,   0,  19,  84,   0,  63,   0,   0,   0,   0,  49,   1,  85,
      1,  54,  15,  41,   0,  56,   0,   0,   0,   0,  19,  10,   1,   0,   0,   0,
      0,   0,  86,   0,   0,  87,   0,   0,  86,   0,   0,   0,   0,  79,   0,   0,
     88,   9,  12,   4,  89,   8,  90,  47,   0,  59,  50,   0,  21,   1,  21,  91,
     92,   1,   1,   1,   1,  93,  94,  95,  96,   1,  97,  59,  81,  98,  99,   4,
     59,   0,   0,   0,   0,   0,   0,  19,  50,   0,   0,   0,   0,   0,   0,  62,
      0,   0, 100, 101,   0,   0, 102,   0,   0,   1,   1,  50,   0,   0,   0,  38,
      0,  64,   0,   0,   0,   0,  52,  69,  62,   0,   0,   0,  79,   0,   0,   0,
    103, 104,  59,  38,  81,   0,   0,   0,   0,   0,   0, 105,   1,  14,   4,  12,
     84,   0,   0,   0,   0,  38,  88,   0,   0,   0,   0, 106,   0,   0, 107,  62,
      0, 108,   0,   0,   0,   1,   0,   0,   0, 109,  14,  54,   0,   0, 110,   0,
     88,   0,   0,   0,  62,  63,   0,   0,  63,   0,  87,   0,   0, 110,   0,   0,
      0,   0, 111,   0,   0,   0,  79,  56,   0,  38,   1,  59,   1,  59,   0,   0,
     64,  87,   0,   0, 112,   0,   0,   0,  56,   0,   0,   0,   0, 112,   0,   0,
      0,   0,  62,   0,   0,  62,   0,   0,   0,   0,  57,   0,  87, 113,   0,   0,
      8,  90,   0,   0,   1,  88,   0,   0,   0,   0,   0, 114,   0, 115, 116, 117,
    118,   0,  52,   4, 119,  49,  23,   0,   0,   0,  38,  50,  38,  59,   0,   0,
      1,  88,   1,   1,   1,   1,  39,   1,  48, 103,  88,   0,   4, 119,   0,   0,
      0,   1, 120,   0,
};

static RE_UINT8 re_canonical_combining_class_stage_5[] = {
     0,  0,  0,  0, 50, 50, 50, 50, 50, 51, 45, 45, 45, 45, 51, 43,
    45, 45, 45, 45, 45, 41, 41, 45, 45, 45, 45, 41, 41, 45, 45, 45,
     1,  1,  1,  1,  1, 45, 45, 45, 45, 50, 50, 50, 50, 54, 50, 45,
    45, 45, 50, 50, 50, 45, 45,  0, 50, 50, 50, 45, 45, 45, 45, 50,
    51, 45, 45, 50, 52, 53, 53, 52, 53, 53, 52, 50,  0,  0,  0, 50,
     0, 45, 50, 50, 50, 50, 45, 50, 50, 50, 46, 45, 50, 50, 45, 45,
    50, 46, 49, 50,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 14, 15,
    16, 17,  0, 18,  0, 19, 20,  0, 50, 45,  0, 13, 25, 26, 27,  0,
     0,  0,  0, 22, 23, 24, 25, 26, 27, 28, 29, 50, 50, 45, 45, 50,
    45, 50, 50, 45, 30,  0,  0,  0,  0,  0, 50, 50, 50,  0,  0, 50,
    50,  0, 45, 50, 50, 45,  0,  0,  0, 31,  0,  0, 50, 45, 50, 50,
    45, 45, 50, 45, 45, 50, 45, 50, 45, 50, 50,  0,  0, 45,  0,  0,
    50, 50,  0, 50,  0, 50, 50, 50, 50, 50,  0,  0,  0, 45, 45, 45,
     0,  0,  0, 45, 50, 50,  0, 45, 50, 45, 45, 45, 22, 23, 24, 50,
     2,  0,  0,  0,  0,  4,  0,  0,  0, 50, 45, 50, 50,  0,  0,  0,
     0,  0, 50,  0,  0, 32, 33,  0,  0,  0,  0,  4,  4,  0,  0,  0,
     0,  0,  4,  0, 34, 34,  4,  0, 35, 35, 35, 35, 36, 36,  0,  0,
    37, 37, 37, 37, 45, 45,  0,  0,  0, 45,  0, 45,  0, 43,  0,  0,
     0, 38, 39,  0, 40,  0,  0,  0,  0,  0, 39, 39, 39, 39,  0,  0,
    39,  0, 50, 50,  4,  0, 50, 50,  0,  0, 45,  0,  0,  0,  0,  2,
     0,  4,  4,  0,  0, 50,  0,  0,  0, 49,  0,  0,  0, 46, 50, 45,
    45,  0,  0,  0, 50,  0,  0, 45,  0,  0,  4,  4,  0,  0,  2,  0,
    50, 50, 50,  0, 50,  0,  1,  1,  1,  0,  0,  0, 50, 53, 42, 45,
    41, 50, 50, 50, 50, 50, 51, 49, 49, 45,  0, 50, 52, 45, 50, 45,
    50, 50,  1,  1,  1,  1,  1, 50,  0,  1,  1, 50, 45, 50,  1,  1,
     0,  0, 44, 49, 51, 46, 47, 47,  0,  3,  3,  0, 50,  0, 50, 50,
    45,  0,  0, 50,  0,  0, 21,  0,  0, 45,  0, 50, 50,  1, 45,  0,
     0, 50, 45,  0,  0,  0, 45, 45,  0,  4,  2,  0,  0,  2,  4,  0,
     0,  0,  4,  2,  4,  4,  0,  0,  0,  0,  1,  0,  0, 43, 43,  1,
     1,  1,  0,  0,  0, 48, 43, 43, 43, 43, 43,  0, 45, 45, 45,  0,
    50, 50,  2,  0,
};

/* Canonical_Combining_Class: 2344 bytes. */

RE_UINT32 re_get_canonical_combining_class(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 12;
    code = ch ^ (f << 12);
    pos = (RE_UINT32)re_canonical_combining_class_stage_1[f] << 5;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_canonical_combining_class_stage_2[pos + f] << 3;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_canonical_combining_class_stage_3[pos + f] << 2;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_canonical_combining_class_stage_4[pos + f] << 2;
    value = re_canonical_combining_class_stage_5[pos + code];

    return value;
}

/* Decomposition_Type. */

static RE_UINT8 re_decomposition_type_stage_1[] = {
    0, 1, 2, 2, 2, 3, 4, 5, 6, 2, 2, 2, 2, 2, 7, 8,
    2, 2, 2, 2, 2, 2, 2, 9, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2,
};

static RE_UINT8 re_decomposition_type_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  9, 10, 11, 12, 13, 14,
    15,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7, 16,  7, 17, 18, 19,
    20, 21, 22, 23, 24,  7,  7,  7,  7,  7, 25,  7, 26, 27, 28, 29,
    30, 31, 32, 33,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7, 34, 35,  7,  7,  7, 36, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 38,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7,  7,  7, 37, 39, 40, 41, 42, 43, 44,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
    45, 46,  7, 47, 48, 49,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7, 50,  7,  7, 51, 52, 53, 54,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7, 55,  7,
     7, 56, 57,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7,  7, 37, 37, 58,  7,  7,  7,  7,  7,
};

static RE_UINT8 re_decomposition_type_stage_3[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   2,   3,   4,   3,   5,
      6,   7,   8,   9,  10,  11,   8,  12,   0,   0,  13,  14,  15,  16,  17,  18,
      6,  19,  20,  21,   0,   0,   0,   0,   0,   0,   0,  22,   0,  23,  24,   0,
      0,   0,   0,   0,  25,   0,   0,  26,  27,  14,  28,  14,  29,  30,   0,  31,
     32,  33,   0,  33,   0,  32,   0,  34,   0,   0,   0,   0,  35,  36,  37,  38,
      0,   0,   0,   0,   0,   0,   0,   0,  39,   0,   0,   0,   0,   0,   0,   0,
      0,   0,  40,   0,   0,   0,   0,  41,   0,   0,   0,   0,  42,  43,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,  33,  44,   0,  45,   0,   0,   0,   0,   0,   0,  46,  47,   0,   0,
      0,   0,   0,  48,   0,  49,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  50,  51,   0,   0,   0,  52,   0,   0,  53,   0,   0,   0,
      0,   0,   0,   0,  54,   0,   0,   0,   0,   0,   0,   0,  55,   0,   0,   0,
      0,   0,   0,   0,  53,   0,   0,   0,   0,   0,   0,   0,   0,  56,   0,   0,
      0,   0,   0,  57,   0,   0,   0,   0,   0,   0,   0,  57,   0,  58,   0,   0,
     59,   0,   0,   0,  60,  61,  33,  62,  63,  60,  61,  33,   0,   0,   0,   0,
      0,   0,  64,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  65,
     66,  67,   0,  68,  69,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,  70,  71,  72,  73,  74,  75,   0,  76,  73,  73,   0,   0,   0,   0,
      6,   6,   6,   6,   6,   6,   6,   6,   6,  77,   6,   6,   6,   6,   6,  78,
      6,  79,   6,   6,  79,  80,   6,  81,   6,   6,   6,  82,  83,  84,   6,  85,
     86,  87,  88,  89,  90,  91,   0,  92,  93,  94,  95,   0,   0,   0,   0,   0,
     96,  97,  98,  99, 100, 101, 102, 102, 103, 104, 105,   0, 106,   0,   0,   0,
    107,   0, 108, 109, 110,   0, 111, 112, 112,   0, 113,   0,   0,   0, 114,   0,
      0,   0, 115,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 116, 117, 102, 102, 102, 118, 116, 116, 119,   0,
    120,   0,   0,   0,   0,   0,   0, 121,   0,   0,   0,   0,   0, 122,   0,   0,
      0,   0,   0,   0,   0,   0,   0, 123,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 124,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0, 125,   0,   0,   0,   0,   0,  57,
    102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 126,   0,   0,
    127,   0,   0, 128, 129, 130, 131, 132,   0, 133, 129, 130, 131, 132,   0, 134,
      0,   0,   0, 135, 102, 102, 102, 102, 136, 137,   0,   0,   0,   0,   0,   0,
    102, 136, 102, 102, 138, 139, 116, 140, 116, 116, 116, 116, 141, 116, 116, 140,
    142, 142, 142, 142, 142, 143, 102, 144, 142, 142, 142, 142, 142, 142, 102, 145,
      0,   0,   0,   0,   0,   0,   0,   0,   0, 146,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0, 147,   0,   0,   0,   0,   0,   0,   0, 148,
      0,   0,   0,   0,   0, 149,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,
      6,   6,   6,   6,   6,   6,   6,   6,   6,   6,  21,   0,   0,   0,   0,   0,
     81, 150, 151,   6,   6,   6,  81,   6,   6,   6,   6,   6,   6,  78,   0,   0,
    152, 153, 154, 155, 156, 157, 158, 158, 159, 158, 160, 161,   0, 162, 163, 164,
    165, 165, 165, 165, 165, 165, 166, 167, 167, 168, 169, 169, 169, 170, 171, 172,
    165, 173, 174, 175,   0, 176, 177, 178, 179, 180, 167, 181, 182,   0,   0, 183,
      0, 184,   0, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 194, 195, 196,
    197, 198, 198, 198, 198, 198, 199, 200, 200, 200, 200, 201, 202, 203, 204,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0, 205, 206,   0,   0,   0,   0,   0,
      0,   0, 207,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  46,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 208,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 104,   0,   0,   0,   0,
      0,   0,   0,   0,   0, 207, 209,   0,   0,   0,   0, 210,  14,   0,   0,   0,
    211, 211, 211, 211, 211, 212, 211, 211, 211, 213, 214, 215, 216, 211, 211, 211,
    217, 218, 211, 219, 220, 221, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211,
    211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 222, 211, 211, 211, 211, 211,
    211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 211, 223, 211, 211, 211,
    216, 211, 224, 225, 226, 227, 228, 229, 230, 231, 232, 231,   0,   0,   0,   0,
    233, 102, 234, 142, 142,   0, 235,   0,   0, 236,   0,   0,   0,   0,   0,   0,
    237, 142, 142, 238, 239, 240,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      6,  81,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_decomposition_type_stage_4[] = {
      0,   0,   0,   0,   1,   0,   2,   3,   4,   5,   6,   7,   8,   9,   8,   8,
     10,  11,  10,  12,  10,  11,  10,   9,   8,   8,   8,   8,  13,   8,   8,   8,
      8,  12,   8,   8,  14,   8,  10,  15,  16,   8,  17,   8,  12,   8,   8,   8,
      8,   8,   8,  15,  12,   0,   0,  18,  19,   0,   0,   0,   0,  20,  20,  21,
      8,   8,   8,  22,   8,  13,   8,   8,  23,  12,   8,   8,   8,   8,   8,  13,
      0,  13,   8,   8,   8,   0,   0,   0,  24,  24,  25,   0,   0,   0,  20,   5,
     24,  25,   0,   0,   9,  19,   0,   0,   0,  19,  26,  27,   0,  21,  11,  22,
      0,   0,  13,   8,   0,   0,  13,  11,  28,  29,   0,   0,  30,   5,  31,   0,
      9,  18,   0,  11,   0,   0,  32,   0,   0,  13,   0,   0,  33,   0,   0,   0,
      8,  13,  13,   8,  13,   8,  13,   8,   8,  12,  12,   0,   0,   3,   0,   0,
     13,  11,   0,   0,   0,  34,  35,   0,  36,   0,   0,   0,  18,   0,   0,   0,
     32,  19,   0,   0,   0,   0,   8,   8,   0,   0,  18,  19,   0,   0,   0,   9,
     18,  27,   0,   0,   0,   0,  10,  27,   0,   0,  37,  19,   0,   0,   0,  12,
      0,  19,   0,   0,   0,   0,  13,  19,   0,   0,  19,   0,  19,  18,  22,   0,
      0,   0,  27,  11,   3,   0,   0,   0,   0,   0,   0,   5,   0,   0,   0,   1,
     18,   0,   0,  32,  27,  18,   0,  19,  18,  38,  17,   0,  32,   0,   0,   0,
      0,  27,   0,   0,   0,   0,   0,  25,   0,  27,  36,  36,  27,   0,   0,   0,
      0,   0,  18,  32,   9,   0,   0,   0,   0,   0,   0,  39,  24,  24,  39,  24,
     24,  24,  24,  40,  24,  24,  24,  24,  41,  42,  43,   0,   0,   0,  25,   0,
      0,   0,  44,  24,   8,   8,  45,   0,   8,   8,  12,   0,   8,  12,   8,  12,
      8,   8,  46,  46,   8,   8,   8,  12,   8,  22,   8,  47,  21,  22,   8,   8,
      8,  13,   8,  10,  13,  22,   8,  48,  49,  50,  30,   0,  51,   3,   0,   0,
      0,  30,   0,  52,   3,  53,   0,  54,   0,   3,   5,   0,   0,   3,   0,   3,
     55,  24,  24,  24,  42,  42,  42,  43,  42,  42,  42,  56,   0,   0,  35,   0,
     57,  34,  58,  59,  59,  60,  61,  62,  63,  64,  65,  66,  66,  67,  68,  59,
     69,  61,  62,   0,  70,  70,  70,  70,  20,  20,  20,  20,   0,   0,  71,   0,
      0,   0,  13,   0,   0,   0,   0,  27,   0,   0,   0,  10,   0,  19,  32,  19,
      0,  36,   0,  72,  35,   0,   0,   0,  32,  37,  32,   0,  36,   0,   0,  10,
     12,  12,  12,   0,   0,   0,   0,   8,   8,   0,  13,  12,   0,   0,  33,   0,
     73,  73,  73,  73,  73,  20,  20,  20,  20,  74,  73,  73,  73,  73,  75,   0,
      0,   0,   0,  35,   0,  30,   0,   0,   0,   0,   0,  19,   0,   0,   0,  76,
      0,   0,   0,  44,   0,   0,   0,   3,  20,   5,   0,   0,  77,   0,   0,   0,
      0,  26,  30,   0,   0,   0,   0,  36,  36,  36,  36,  36,  36,  46,  32,   0,
      9,  22,  33,  12,   0,  19,   3,  78,   0,  37,  11,  79,  34,  20,  20,  20,
     20,  20,  20,  30,   4,  24,  24,  24,  20,  73,   0,   0,  80,  73,  73,  73,
     73,  73,  73,  75,  20,  20,  20,  81,  81,  81,  81,  81,  81,  81,  20,  20,
     82,  81,  81,  81,  20,  20,  20,  83,   0,   0,   0,  55,  25,   0,   0,   0,
      0,   0,  55,   0,   0,   0,   0,  24,  36,  10,   8,  11,  36,  33,  13,   8,
     20,  30,   0,   0,   3,  20,   0,  46,  59,  59,  84,   8,   8,  11,   8,  36,
      9,  22,   8,  15,  85,  86,  86,  86,  86,  86,  86,  86,  86,  85,  85,  85,
     87,  85,  86,  86,  88,   0,   0,   0,  89,  90,  91,  92,  85,  87,  86,  85,
     85,  85,  93,  87,  94,  94,  94,  94,  94,  95,  95,  95,  95,  95,  95,  95,
     95,  96,  97,  97,  97,  97,  97,  97,  97,  97,  97,  98,  99,  99,  99,  99,
     99, 100,  94,  94, 101,  95,  95,  95,  95,  95,  95, 102,  97,  99,  99, 103,
    104,  97, 105, 106, 107, 105, 108, 105, 104,  96,  95, 105,  96, 109, 110,  97,
    111, 106, 112, 105,  95, 106, 113,  95,  96, 106,   0,   0,  94,  94,  94, 114,
    115, 115, 116,   0, 115, 115, 115, 115, 115, 117, 118,  20, 119, 120, 120, 120,
    120, 119, 120,   0, 121, 122, 123, 123, 124,  91, 125, 126,  90, 125, 127, 127,
    127, 127, 126,  91, 125, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 126,
    125, 126,  91, 128, 129, 130, 130, 130, 130, 130, 130, 130, 131, 132, 132, 132,
    132, 132, 132, 132, 132, 132, 132, 133, 134, 132, 134, 132, 134, 132, 134, 135,
    130, 136, 132, 133,   0,   0,  27,  19,   0,   0,  18,   0,   0,   0,   0,  13,
      0,   0,  18,  36,   8,  19,   0,   0,   0,   0,  18,   8,  59,  59,  59,  59,
     59, 137,  59,  59,  59,  59,  59, 137, 138, 139,  61, 137,  59,  59,  66,  61,
     59,  61,  59,  59,  59,  66, 140,  61,  59, 137,  59, 137,  59,  59,  66, 140,
     59, 141, 142,  59, 137,  59,  59,  59,  59,  62,  59,  59,  59,  59,  59, 142,
    139, 143,  61,  59, 140,  59, 144,   0, 138, 145, 144,  61, 139, 143, 144, 144,
    139, 143, 140,  59, 140,  59,  61, 141,  59,  59,  66,  59,  59,  59,  59,   0,
     61,  61,  66,  59,  20,  20,  30,   0,  20,  20, 146,  75,   0,   0,   4,   0,
    147,   0,   0,   0, 148,   0,   0,   0,  81,  81,  81,   0,  20,  20,  35,   0,
    149,   0,   0,   0,
};

static RE_UINT8 re_decomposition_type_stage_5[] = {
     0,  0,  0,  0,  4,  0,  0,  0,  2,  0, 10,  0,  0,  0,  0,  2,
     0,  0, 10, 10,  2,  2,  0,  0,  2, 10, 10,  0, 17, 17, 17,  0,
     1,  1,  1,  1,  1,  1,  0,  1,  0,  1,  1,  1,  1,  1,  1,  0,
     1,  1,  0,  0,  0,  0,  1,  1,  1,  0,  2,  2,  1,  1,  1,  2,
     2,  0,  0,  1,  1,  2,  0,  0,  0,  0,  0,  1,  1,  0,  0,  0,
     2,  2,  2,  2,  2,  1,  1,  1,  1,  0,  1,  1,  1,  2,  2,  2,
    10, 10, 10, 10, 10,  0,  0,  0,  0,  0,  2,  0,  0,  0,  1,  0,
     2,  2,  2,  1,  1,  2,  2,  0,  2,  2,  2,  0,  0,  2,  0,  0,
     0,  1,  0,  0,  0,  1,  1,  0,  0,  2,  2,  2,  2,  0,  0,  0,
     1,  0,  1,  0,  1,  0,  0,  1,  0,  1,  1,  2, 10, 10, 10,  0,
    10, 10,  0, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11,  0,
     0,  0,  0, 10,  1,  1,  2,  1,  0,  1,  0,  1,  1,  2,  1,  2,
     1,  1,  2,  0,  1,  1,  2,  2,  2,  2,  2,  4,  0,  4,  0,  0,
     0,  0,  0,  4,  2,  0,  2,  2,  2,  0,  2,  0, 10, 10,  0,  0,
    11,  0,  0,  0,  2,  2,  3,  2,  0,  2,  3,  3,  3,  3,  3,  3,
     0,  3,  2,  0,  0,  3,  3,  3,  3,  3,  0,  0, 10,  2, 10,  0,
     3,  0,  1,  0,  3,  0,  1,  1,  3,  3,  0,  3,  3,  2,  2,  2,
     2,  3,  0,  2,  3,  0,  0,  0, 17, 17, 17, 17,  0, 17,  0,  0,
     2,  2,  0,  2,  9,  9,  9,  9,  2,  2,  9,  9,  9,  9,  9,  0,
    11, 10,  0,  0, 13,  0,  0,  0,  2,  0,  1, 12,  0,  0,  1, 12,
    16,  9,  9,  9, 16, 16, 16, 16,  2, 16, 16, 16,  2,  2,  2, 16,
     3,  3,  1,  1,  8,  7,  8,  7,  5,  6,  8,  7,  8,  7,  5,  6,
     8,  7,  0,  0,  0,  0,  0,  8,  7,  5,  6,  8,  7,  8,  7,  8,
     7,  8,  8,  7,  5,  8,  7,  5,  8,  8,  8,  8,  7,  7,  7,  7,
     7,  7,  7,  5,  5,  5,  5,  5,  5,  5,  5,  6,  6,  6,  6,  6,
     6,  8,  8,  8,  8,  7,  7,  7,  7,  5,  5,  5,  7,  8,  0,  0,
     5,  7,  5,  5,  7,  5,  7,  7,  5,  5,  7,  7,  5,  5,  7,  5,
     5,  7,  7,  5,  7,  7,  5,  7,  5,  5,  5,  7,  0,  0,  5,  5,
     5,  7,  7,  7,  5,  7,  5,  7,  8,  0,  0,  0, 12, 12, 12, 12,
    12, 12,  0,  0, 12,  0,  0, 12, 12,  2,  2,  2, 15, 15, 15,  0,
    15, 15, 15, 15,  8,  6,  8,  0,  8,  0,  8,  6,  8,  6,  8,  6,
     8,  8,  7,  8,  7,  8,  7,  5,  6,  8,  7,  8,  6,  8,  7,  5,
     7,  0,  0,  0,  0, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 14,  0,  0,  0, 14, 14, 14,  0,  0,  0,
    13, 13, 13,  0,  3,  0,  3,  3,  0,  0,  3,  0,  0,  3,  3,  0,
     3,  3,  3,  0,  3,  0,  3,  0,  0,  0,  3,  3,  3,  0,  0,  3,
     0,  3,  0,  3,  0,  0,  0,  3,  2,  2,  2,  9, 16,  0,  0,  0,
    16, 16, 16,  0,  9,  9,  0,  0,
};

/* Decomposition_Type: 2964 bytes. */

RE_UINT32 re_get_decomposition_type(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 13;
    code = ch ^ (f << 13);
    pos = (RE_UINT32)re_decomposition_type_stage_1[f] << 5;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_decomposition_type_stage_2[pos + f] << 4;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_decomposition_type_stage_3[pos + f] << 2;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_decomposition_type_stage_4[pos + f] << 2;
    value = re_decomposition_type_stage_5[pos + code];

    return value;
}

/* East_Asian_Width. */

static RE_UINT8 re_east_asian_width_stage_1[] = {
     0,  1,  2,  3,  4,  5,  5,  5,  5,  5,  6,  5,  5,  7,  8,  9,
    10, 10, 10, 10, 10, 10, 11,  5, 12, 10, 10, 13, 10, 10, 10, 14,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 15,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    16, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
     8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8, 17,
     8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8, 17,
};

static RE_UINT8 re_east_asian_width_stage_2[] = {
     0,  1,  2,  3,  4,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,
     5,  6,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,
     7,  8,  9, 10, 11, 12, 13, 14,  5, 15,  5, 16,  5,  5, 17, 18,
    19, 20, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 24,  5,  5,  5,  5, 25,  5,  5, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 26,  5,  5,  5,  5,  5,  5,  5,  5,
    27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27,
    27, 27, 27, 27, 27, 27, 27, 27, 27, 22, 22,  5,  5,  5, 28, 29,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 30,
    22, 22, 22, 22, 22, 22, 22, 31, 22, 22, 32,  5,  5,  5,  5,  5,
    22, 33, 34,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,
    35, 36, 37, 38, 39, 40, 41,  5,  5, 42,  5,  5,  5,  5,  5,  5,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 43,
     5, 44,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,
    27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 45,
};

static RE_UINT8 re_east_asian_width_stage_3[] = {
      0,   0,   1,   1,   1,   1,   1,   2,   0,   0,   3,   4,   5,   6,   7,   8,
      9,  10,  11,  12,  13,  14,  11,   0,   0,   0,   0,   0,  15,  16,   0,   0,
      0,   0,   0,   0,   0,   9,   9,   0,   0,   0,   0,   0,  17,  18,   0,   0,
     19,  19,  19,  19,  19,  19,  19,   0,   0,  20,  21,  20,  21,   0,   0,   0,
      9,  19,  19,  19,  19,   9,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     22,  22,  22,  22,  22,  22,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,  23,  24,  25,   0,   0,   0,  26,  27,   0,  28,   0,   0,   0,   0,   0,
     29,  30,  31,   0,   0,  32,  33,  34,  35,  34,   0,  36,   0,  37,  38,   0,
     39,  40,  41,  42,  43,  44,  45,   0,  46,  47,  48,  49,   0,   0,   0,   0,
      0,  50,  51,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  52,  53,
      0,   0,   0,   0,   0,   0,  19,  19,  19,  19,  19,  19,  19,  19,  54,  19,
     19,  19,  19,  19,  33,  19,  19,  55,  19,  56,  21,  57,  58,  59,  60,  61,
     62,  63,   0,   0,  64,  65,  66,  67,   0,  68,  69,  70,  71,  72,  73,  74,
     75,   0,  76,  77,  78,  79,   0,  80,   0,  81,   0,  82,   0,   0,  83,   0,
      0,   0,   0,   0,   0,   0,   0,   0,  84,   0,   0,   0,   0,   0,   0,   0,
      0,  85,   0,   0,   0,  86,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,  22,  87,  22,  22,  22,  22,  22,  65,
     22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  88,   0,  89,
     90,  22,  22,  91,  92,  22,  22,  22,  22,  93,  22,  22,  22,  22,  22,  22,
     94,  22,  22,  92,  22,  22,  22,  22,  91,  22,  22,  95,  22,  22,  65,  22,
     22,  91,  22,  22,  96,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  91,
     22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,
     22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,   0,   0,   0,   0,
     22,  22,  22,  22,  22,  22,  22,  22,  97,  22,  22,  22,  98,   0,   0,   0,
      0,   0,   0,   0,   0,   0,  22,  97,   0,   0,   0,   0,   0,   0,   0,   0,
     22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  65,   0,   0,   0,   0,   0,
     19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,
     19,  99,   0,  22,  22, 100, 101,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    102, 103, 103, 103, 103, 103, 104, 105, 105, 105, 105, 106, 107, 108, 109,  77,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 110,   0,
     22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22, 110,
     22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22, 111,
     22,  91,   0,   0,   0,   0,   0,  22,  22,  22,  22,  22,  22,  22,  22,  22,
     22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  89,
    112,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  67,   0,   0,   0,
    113,  19, 114,  19,  19,  19,  34,  19, 115, 116, 117,   0,   0,   0,   0,   0,
    111,  22,  22,  89, 118, 110,  88,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     22,  22, 119, 120,  22,  22,  22, 121,  22,  65,  22,  22, 122,  65,  22, 123,
     22,  22,  22,  91, 124,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22, 125,
     22,  22,  22, 126, 127,  22, 128, 129,   0, 130, 112,   0,   0,   0,   0, 131,
     22,  22,  22,  22,  22,   0,   0,   0,  22,  22,  22,  22, 132, 111,  85, 133,
      0,  22,  22,  91,  22,  22,  22, 134,  22,  22, 111,  99, 111,  22,  22,  22,
     22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22,  22, 126,
     19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,   0,
     19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19, 114,
};

static RE_UINT8 re_east_asian_width_stage_4[] = {
     0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  2,  3,  4,  5,  6,
     7,  8,  9,  7,  0, 10,  0,  0, 11, 12, 11, 13, 14, 10,  9, 14,
     8, 12,  9,  5, 15,  0,  0,  0, 16,  0, 12,  0,  0, 13, 12,  0,
    17,  0, 11, 12,  9, 11,  7, 15, 13,  0,  0,  0,  0,  0,  0, 10,
     5,  5,  5, 11,  0, 18, 17, 15, 11,  0,  7, 16,  7,  7,  7,  7,
    17,  7,  7,  7, 19,  7, 14,  0, 20, 20, 20, 20, 18,  9, 14, 14,
     9,  7,  0,  0,  8, 15, 12, 10,  0, 11,  0, 12, 17, 11,  0,  0,
     0,  0, 21, 11, 12, 15, 15,  0, 12, 10,  0,  0, 22, 10, 12,  0,
    12, 11, 12,  9,  7,  7,  7,  0,  7,  7, 14,  0,  0,  0, 15,  0,
     0,  0, 14,  0, 10, 11,  0,  0,  0, 12,  0,  0,  8, 12, 18, 12,
    15, 15, 10, 17, 18, 16,  7,  5,  0,  7,  0, 14,  0,  0, 11, 11,
    10,  0,  0,  0, 14,  7, 13, 13, 13, 13,  0,  0,  0, 15, 15,  0,
     0, 15,  0,  0,  0,  0,  0, 12, 10,  0, 23,  0,  0,  0, 24,  0,
     0,  0, 25, 26, 27,  0,  0,  0,  7,  7, 19,  7,  7,  0,  0,  0,
    13, 14,  0,  0, 13, 13,  0, 14, 14, 13, 18, 13, 14,  0,  0,  0,
    13, 14,  0, 12,  0,  0,  0, 24,  0, 22, 15, 13,  0, 28,  0,  5,
     5,  0, 20, 20, 20,  0,  0,  0, 19, 19,  9, 19,  0,  0,  0, 29,
    29,  0,  0, 13, 30,  0, 23,  0,  0,  0,  0, 31,  0, 32,  7, 33,
     7, 34,  7,  7, 19,  0, 33,  7, 35, 36, 33, 36,  0, 30, 23,  0,
     0,  0, 26,  0,  0,  0,  0, 15,  0,  0,  0, 37, 29, 38,  0,  0,
     0, 13,  7,  7,  0, 25,  0,  0, 26,  0,  0, 29,  0, 39,  1, 40,
     0, 41,  0,  0,  0,  0, 29, 26, 26, 42, 14,  0, 20, 20, 38, 20,
    20, 28,  0,  0, 20, 20, 20,  0, 43, 20, 20, 20, 20, 20, 20, 44,
    25, 20, 20, 20, 20, 44, 25, 20,  0, 25, 20, 20, 20, 20, 44,  0,
    20, 20,  7,  7, 20, 20, 20, 26, 20, 44,  0,  0, 20, 20, 28,  0,
    44, 20, 20, 20, 20, 44, 20,  0, 45, 46, 46, 46, 46, 46, 46, 46,
    47, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 49, 50, 48, 50, 48,
    50, 48, 50, 51, 46, 52, 48, 49, 28,  0,  0,  0, 44,  0,  0,  0,
     0, 26,  0,  0,  7,  7,  9,  0,  7,  7,  7, 14,  7,  7,  7, 33,
    53, 20, 54,  7,  7,  7,  7, 11, 20, 20, 26,  0, 26,  0,  0, 25,
    20, 38, 20, 20, 20, 20, 20, 55, 20, 20, 44, 29, 26, 26, 20, 20,
    55, 20, 20, 20, 20, 20, 20, 27, 20, 20, 20, 28,  0,  0, 29, 44,
    20, 20,  0,  0,  0,  0, 56,  0,  0, 24,  0,  0,  0,  0, 29, 20,
    20, 28,  0, 26,  0, 20, 28,  0, 27, 44, 56, 20,
};

static RE_UINT8 re_east_asian_width_stage_5[] = {
    0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 0, 1, 5, 5,
    1, 5, 5, 1, 1, 0, 1, 0, 5, 1, 1, 5, 1, 1, 1, 1,
    1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0,
    0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0,
    0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1,
    3, 3, 3, 3, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 3, 3,
    0, 3, 3, 0, 0, 3, 3, 3, 3, 0, 0, 0, 3, 0, 0, 3,
    3, 3, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 3, 3, 1,
    3, 3, 1, 1, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 3, 3,
    1, 3, 1, 1, 3, 0, 3, 0, 3, 3, 0, 3, 0, 0, 5, 5,
    5, 5, 0, 0, 0, 5, 5, 0, 0, 3, 1, 1, 4, 3, 3, 3,
    3, 3, 3, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0,
    4, 4, 4, 0, 1, 3, 3, 3, 3, 3, 3, 1, 3, 0, 3, 3,
    0, 0, 3, 0,
};

/* East_Asian_Width: 2064 bytes. */

RE_UINT32 re_get_east_asian_width(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 12;
    code = ch ^ (f << 12);
    pos = (RE_UINT32)re_east_asian_width_stage_1[f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_east_asian_width_stage_2[pos + f] << 4;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_east_asian_width_stage_3[pos + f] << 2;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_east_asian_width_stage_4[pos + f] << 2;
    value = re_east_asian_width_stage_5[pos + code];

    return value;
}

/* Joining_Group. */

static RE_UINT8 re_joining_group_stage_1[] = {
    0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1,
};

static RE_UINT8 re_joining_group_stage_2[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    2, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_joining_group_stage_3[] = {
    0, 0, 0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 5, 0, 0,
};

static RE_UINT8 re_joining_group_stage_4[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  1,  2,  3,  0,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13,
     0, 14, 15,  0, 16, 17, 18, 19,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 20,  0,  0,  0, 21, 22,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 23, 24, 25,  0,
    26, 27, 28,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_joining_group_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     45,   0,   3,   3,  43,   3,  45,   3,   4,  41,   4,   4,  13,  13,  13,   6,
      6,  31,  31,  35,  35,  33,  33,  39,  39,   1,   1,  11,  11,  55,  55,  55,
      0,   9,  29,  19,  22,  24,  26,  16,  43,  45,  45,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   4,  29,
      0,   3,   3,   3,   0,   3,  43,  43,  45,   4,   4,   4,   4,   4,   4,   4,
      4,  13,  13,  13,  13,  13,  13,  13,   6,   6,   6,   6,   6,   6,   6,   6,
      6,  31,  31,  31,  31,  31,  31,  31,  31,  31,  35,  35,  35,  33,  33,  39,
      1,   9,   9,   9,   9,   9,   9,  29,  29,  11,  38,  11,  19,  19,  19,  11,
     11,  11,  11,  11,  11,  22,  22,  22,  22,  26,  26,  26,  26,  56,  21,  13,
     41,  17,  17,  14,  43,  43,  43,  43,  43,  43,  43,  43,  55,  47,  55,  43,
     45,  45,  46,  46,   0,  41,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   6,  31,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  35,  33,   1,   0,   0,  21,
      2,   0,   5,  12,  12,   7,   7,  15,  44,  50,  18,  42,  42,  48,  49,  20,
     23,  25,  27,  36,  10,   8,  28,  32,  34,  30,   7,  37,  40,   5,  12,   7,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  51,  52,  53,
      4,   4,   4,   4,   4,   4,   4,  13,  13,   6,   6,  31,  35,   1,   1,   1,
      9,   9,  11,  11,  11,  24,  24,  26,  26,  26,  22,  31,  31,  35,  13,  13,
     35,  31,  13,   3,   3,  55,  55,  45,  43,  43,  54,  54,  13,  35,  35,  19,
     89,  90,  91,  92,  93,  94,  95,  96,  97,  98,  99,   0,   0,   0,   0,   0,
      4,   4,  13,  39,   9,  29,  22,  24,  45,  45,  31,  43,  57,   0,   6,  33,
     11,  58,  31,   1,  19,   0,   4,   4,   4,  31,  45,  86,  87,  88,   0,   0,
     59,  61,  61,  65,  65,  62,   0,  83,   0,  85,  85,   0,   0,  66,  80,  84,
     68,  68,  68,  69,  63,  81,  70,  71,  77,  60,  60,  73,  73,  76,  74,  74,
     74,  75,   0,   0,  78,   0,   0,   0,   0,   0,   0,  72,  64,  79,  82,  67,
      0,   0, 100,   0,   0,   0,   0,   0,   0, 100,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0, 101,   0,   0, 100,   0, 101,   0,
    101,   0,   0, 101,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
};

/* Joining_Group: 666 bytes. */

RE_UINT32 re_get_joining_group(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_joining_group_stage_1[f] << 3;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_joining_group_stage_2[pos + f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_joining_group_stage_3[pos + f] << 4;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_joining_group_stage_4[pos + f] << 4;
    value = re_joining_group_stage_5[pos + code];

    return value;
}

/* Joining_Type. */

static RE_UINT8 re_joining_type_stage_1[] = {
     0,  1,  2,  3,  4,  4,  4,  4,  4,  4,  5,  4,  4,  4,  4,  6,
     7,  8,  4,  4,  4,  4,  9,  4,  4,  4,  4, 10,  4, 11, 12,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
    13,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
};

static RE_UINT8 re_joining_type_stage_2[] = {
      0,   1,   0,   0,   0,   0,   2,   0,   0,   3,   0,   4,   5,   6,   7,   8,
      9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,
     25,  26,   0,   0,   0,   0,  27,   0,   0,   0,   0,   0,   0,   0,  28,  29,
     30,  31,  32,   0,  33,  34,  35,  36,  37,  38,   0,  39,   0,   0,   0,   0,
     40,  41,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,  42,  43,  44,   0,   0,   0,   0,
     45,  46,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  47,  48,   0,   0,
     49,  50,  51,  52,  53,  54,   0,  55,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,  56,   0,   0,   0,   0,   0,  57,  43,   0,  58,
      0,   0,   0,  59,   0,  60,  61,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  62,  63,   0,  64,   0,   0,  65,   0,   0,   0,  66,   0,
     67,  68,  69,  70,  71,  72,  73,   0,  74,  75,   0,  76,  77,  78,  79,   0,
     80,   0,   0,   0,  81,  82,   0,   0,  83,  84,  85,  86,   0,  87,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,  88,  89,   0,   0,   0,   0,   0,   0,   0,   0,  90,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,  91,   0,   0,   0,   0,   0,   0,
      0,   0,  92,  93,  94,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  95,  96,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     97,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,  98,  99,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    100,   0, 101,   2,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_joining_type_stage_3[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,
      2,   2,   2,   2,   2,   2,   2,   0,   3,   0,   0,   0,   0,   0,   0,   0,
      0,   4,   2,   5,   6,   0,   0,   0,   0,   7,   8,   9,  10,   2,  11,  12,
     13,  14,  15,  15,  16,  17,  18,  19,  20,  21,  22,   2,  23,  24,  25,  26,
      0,   0,  27,  28,  29,  15,  30,  31,   0,  32,  33,   0,  34,  35,  36,   0,
      0,   0,  37,  38,   0,  39,  40,   2,  41,   0,   0,  42,  43,  44,  45,   0,
     46,   0,   0,  47,  48,   0,  45,  49,  50,   0,   0,  47,  51,  46,   0,  52,
     50,   0,   0,  47,  53,   0,  45,  54,  46,   0,   0,  55,  48,  56,  45,   0,
     57,   0,   0,   0,  58,   0,   0,   0,  59,   0,   0,  60,  61,  62,  45,   0,
     46,   0,   0,  55,  63,   0,  45,   0,  64,   0,   0,  65,  48,   0,  45,   0,
      0,   0,   0,   0,  66,  67,   0,   0,   0,   0,   0,  68,  69,   0,   0,   0,
      0,   0,   0,  70,  71,   0,   0,   0,   0,  72,   0,  73,   0,   0,   0,  74,
     75,  76,   2,  77,  56,   0,   0,   0,   0,   0,  78,  79,   0,  80,  28,  81,
     82,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  78,   0,   0,
      0,  83,   0,  83,   0,  45,   0,  45,   0,   0,   0,  84,  85,  86,   0,   0,
     87,   0,  15,  15,  15,  15,  15,  88,  89,  15,  90,   0,   0,   0,   0,   0,
      0,   0,  91,  92,   0,   0,   0,   0,   0,  93,   0,   0,   0,  94,  95,  96,
      0,   0,   0,  97,   0,   0,   0,   0,  98,   0,   0,  99,  57,   0, 100,  98,
     64,   0, 101,   0,   0,   0, 102,  64,   0,   0, 103, 104,   0,   0,   0,   0,
      0,   0,   0,   0,   0, 105, 106, 107,   0,   0,   0,   0,   2,   2,   2, 108,
    109,   0, 110,   0,   0,   0, 111,   0,   0,   0,   0,   0,   0,   2,   2,  28,
      0,   0,   0,   0,   0,   0,  20,  64,   0,   0,   0,   0,   0,   0,   0,  20,
      0,   0,   0,   0,   0,   0,   2,   2,   0,   0, 112,   0,   0,   0,   0,   0,
      0, 113,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  20, 114,
      0,  60,   0,   0,   0,   0,   0,  64, 115,   0,  62,   0,  15,  15,  15, 116,
      0,   0,   0,   0, 117,   0,   2, 118,   0,   0, 119,   0, 120,  64,   0,   0,
     41,   0,   0, 121,   0,   0, 122,   0,   0,   0, 123, 124, 125,   0,   0,  47,
      0,   0,   0, 126,  46,   0, 127,  56,   0,   0,   0,   0,   0,   0, 128,   0,
      0,  49,   0,   0,   0,   0,   0,   0,   2,   0,   2,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0, 129,   0,   0,   0,   0,   0,   0,   0,   1,
      0,   0,   0,   0,   0,   0,  28,   0,   0,   0,   0,   0,   0,   0,   0, 130,
    131,   0,   0, 132,   0,   0,   0,   0,   0,   0,   0,   0, 133, 134, 135,   0,
    136, 137, 138,   0,   0,   0,   0,   0, 139,  15, 140,   0,   0,   0,   0,   0,
      0,   0,   0, 141, 142, 143,   0,   0,  46,   0,   0, 144, 145,   0,   0,  20,
     64,   0,   0, 146,   0,   0,   0,   0,  41,   0, 147, 148,   0,   0,   0, 149,
     64,   0,   0, 150, 151,   0,   0,   0,   0,   0,  20, 152,   0,   0,   0,   0,
      0,   0,   0,   0,   0,  20, 153,   0,  64,   0,   0,  65,  28,   0, 154, 148,
      0,   0,   0, 144,  67,  49,   0,   0,   0,   0,   0, 155, 156,   0,   0,   0,
      0,   0,   0, 157,  28, 127,   0,   0,   0,   0,   0, 158,  28,   0,   0,   0,
      0,   0, 159, 160,   0,   0,   0,   0,   0,  78, 161,   0,   0,   0,   0,   0,
      0,   0,  20, 162,   0,   0,   0,   0, 163,   0,   0, 164, 165, 166,   0,   0,
     54, 167,   0,   0,   0,   0,   0,   0,   0,   0,   0, 168,   0,   0,   0,   0,
      0, 169, 170, 171,   0,   0,   0,   0,   0,   0,   0, 172, 160,   0,   0,   0,
      0, 173,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 174,
      0,   0,   0,   0,   0,   0,   0, 148,   0,   0,   0, 145,   0,   0,   0,   0,
     20,  41,   0,   0,   0,   0,   0,   0,   0, 175,  98,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 176,  39, 177,   0, 112,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  83,   0,   0,   0,   2,   2,   2, 178,   2,   2,  77, 122,
    179, 100,   4,   0,   0,   0,   0,   0, 180, 181, 182,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0, 145,   0,   0,  15,  15,  15,  15, 183,   0,   0,   0,
     46,   0,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
};

static RE_UINT8 re_joining_type_stage_4[] = {
     0,  0,  0,  0,  0,  0,  0,  1,  2,  2,  2,  2,  3,  2,  4,  0,
     5,  2,  2,  2,  2,  2,  2,  6,  7,  6,  0,  0,  2,  2,  8,  9,
    10, 11, 12, 13, 14, 15, 15, 15, 16, 15, 17,  2,  0,  0,  0, 18,
    19, 20, 15, 15, 15, 15, 21, 21, 21, 21, 22, 15, 15, 15, 15, 15,
    23, 21, 21, 24, 25, 26,  2, 27,  2, 27, 28, 29,  0,  0, 18, 30,
     0,  0,  0,  3, 31, 32, 22, 33, 15, 15, 34, 23,  2,  2,  8, 35,
    15, 15, 32, 15, 15, 15, 13, 36, 24, 36, 22, 15,  0, 37,  2,  2,
     9,  0,  0,  0,  0,  0, 18, 15, 15, 15, 38,  2,  2,  0, 39,  1,
     0, 37,  6,  2,  2,  5,  5,  4, 36, 25, 12, 15, 15, 40,  5,  0,
    41, 42, 43,  0, 15, 15, 25, 44, 45, 41, 12, 46,  3,  2,  2,  2,
     6,  2,  2,  2,  8,  0,  0,  0,  0,  0, 47,  9,  5,  2,  9,  1,
     5,  2,  0,  0, 37,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  9,
     5,  9,  0,  1,  0,  0,  0, 47,  7,  0,  0,  0,  7,  3, 27,  4,
     4,  1,  0,  0,  5,  6,  9,  1,  0,  0, 37,  2,  0,  0,  0, 27,
     0, 47,  0,  0, 47,  0,  0,  0,  9,  0,  0,  1,  9,  9,  0,  0,
     0,  0,  0, 37,  9, 37, 28,  4,  0,  7,  0,  0,  0, 47,  0,  4,
     4,  0,  0,  0,  0,  0,  3,  9,  0,  0, 47,  0, 37, 48,  0,  0,
     1,  2,  8,  0,  0,  3,  2,  8,  1,  2,  6,  9,  0,  0,  2,  4,
     0,  0,  4,  0,  0, 49,  1,  0,  5,  2,  2,  8,  2, 28,  0,  5,
     2,  2,  5,  2,  2,  2,  2,  9,  0,  0,  0,  5, 28,  2,  7,  7,
     0,  0,  4, 37,  5,  9,  0,  0, 47,  7,  0,  1, 37,  9,  0,  0,
     0,  6,  2,  4,  0, 47,  5,  2,  2,  0,  0,  1,  0, 50, 51,  4,
    15, 15, 52,  0,  0, 53, 15, 15, 15, 15, 54,  0,  8,  3,  9,  0,
    47,  0,  5,  0,  0,  3, 27,  0,  0, 47,  2,  8, 48,  5,  2,  9,
     3,  2,  2, 27,  2,  2,  2,  8,  2,  0,  0,  0,  0, 28,  8,  9,
     0,  0,  3,  2, 37,  4,  6,  4,  0, 47,  4, 49,  0,  0,  0,  2,
     2, 37,  0,  0,  8,  2,  2,  2, 28,  2,  9,  1,  0,  9,  4,  0,
     2,  2,  6,  2,  0,  0,  3, 55,  0,  0, 37,  8,  2,  9, 37,  2,
     0,  0, 37,  4,  0,  0,  7,  0,  8,  2,  2,  4, 47, 47,  3,  0,
    56,  0,  0,  0,  0,  4,  0,  0,  4,  0,  0,  3,  0, 37,  2,  4,
     0,  3,  2,  2,  3, 37,  4,  9,  0,  1,  0,  0,  0,  0,  5,  8,
     7,  7,  0,  0,  3,  0,  0,  9, 28, 27,  9, 37,  0,  0,  0,  4,
     0,  1,  9,  1,  0,  0,  5,  0,  0, 37,  8,  0,  5,  7,  0,  2,
     0,  0,  8,  3, 15, 57, 58, 59, 14, 60, 15, 12, 61, 62, 50, 13,
    24, 22, 12, 63, 61,  0,  0,  0,  0,  0, 20, 64, 65, 15, 15, 15,
    33,  2,  0,  0, 13, 15, 15, 15, 15, 66,  2,  2, 67, 68,  0,  0,
     0,  0,  2,  2,  2,  8,  0,  0,  3,  8,  7,  0,  0,  3,  2,  5,
     2,  9,  0,  0,  3,  0,  0,  0,  0, 37,  2,  8,  0,  0,  5,  9,
     4, 28,  0, 47,  3,  2,  8,  0,  0, 37,  2,  9,  3,  2, 48,  3,
    28,  0,  0,  0, 37,  4,  0,  6,  3,  2,  8, 49,  0,  0,  3,  1,
     2,  6,  0,  0, 37,  6,  2,  0,  2,  2,  7,  0,  5,  2,  8,  0,
     3,  2, 27,  8,  0,  3,  0,  0,  5,  8,  5,  0,  2,  8,  4,  0,
     2,  8,  2,  6, 37,  2,  2,  2,  2,  2, 37,  2, 28,  7,  0,  0,
     5,  8, 47,  6,  4, 49,  0,  0,  3,  9,  0,  0,  0,  0,  0,  7,
     0,  3,  4,  0,  8,  5,  2,  0,  2,  8,  3,  2,  0,  9,  0,  0,
     2,  8,  2,  2,  2,  2, 27,  2,  6, 28,  8,  0, 15,  2,  8,  0,
};

static RE_UINT8 re_joining_type_stage_5[] = {
    0, 0, 0, 0, 0, 5, 0, 0, 5, 5, 5, 5, 0, 0, 0, 5,
    5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 5, 0,
    5, 5, 5, 0, 5, 0, 0, 0, 2, 0, 3, 3, 3, 3, 2, 3,
    2, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 3, 2, 2, 5, 0, 0, 2, 2, 5, 3, 3, 3,
    0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 2, 2, 3,
    2, 3, 2, 3, 2, 2, 3, 3, 0, 3, 5, 5, 5, 0, 0, 5,
    5, 0, 5, 5, 5, 5, 3, 3, 2, 0, 0, 2, 3, 5, 2, 2,
    2, 3, 3, 3, 2, 2, 3, 2, 3, 2, 3, 2, 0, 3, 2, 2,
    3, 2, 2, 2, 0, 0, 5, 5, 2, 2, 2, 5, 0, 0, 1, 0,
    3, 2, 0, 0, 2, 0, 2, 2, 2, 2, 0, 3, 2, 3, 3, 0,
    3, 0, 3, 2, 2, 3, 3, 2, 2, 2, 0, 0, 0, 0, 5, 0,
    5, 0, 5, 0, 0, 5, 0, 5, 0, 0, 0, 2, 0, 0, 1, 5,
    2, 0, 0, 0, 0, 5, 5, 2, 2, 5, 2, 0, 0, 1, 5, 5,
    2, 2, 4, 0, 2, 3, 0, 3, 0, 3, 3, 0, 0, 4, 3, 3,
    2, 2, 2, 4, 2, 3, 0, 0, 3, 5, 5, 0, 3, 2, 3, 3,
    3, 2, 2, 0, 4, 2, 2, 2, 2, 0, 5, 5, 5, 2, 2, 2,
    3, 0, 0, 0,
};

/* Joining_Type: 2548 bytes. */

RE_UINT32 re_get_joining_type(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 12;
    code = ch ^ (f << 12);
    pos = (RE_UINT32)re_joining_type_stage_1[f] << 5;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_joining_type_stage_2[pos + f] << 3;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_joining_type_stage_3[pos + f] << 2;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_joining_type_stage_4[pos + f] << 2;
    value = re_joining_type_stage_5[pos + code];

    return value;
}

/* Line_Break. */

static RE_UINT8 re_line_break_stage_1[] = {
     0,  1,  2,  3,  4,  5,  5,  5,  5,  5,  6,  7,  8,  9, 10, 11,
    12, 13, 14, 15, 16, 10, 17,  5, 18, 10, 10, 19, 10, 20, 21, 22,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 23,
     5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 23,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    24, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
};

static RE_UINT8 re_line_break_stage_2[] = {
      0,   1,   2,   2,   2,   3,   4,   5,   2,   6,   7,   8,   9,  10,  11,  12,
     13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,
     29,  30,  31,  32,  33,  34,  35,  36,  37,   2,   2,   2,   2,  38,  39,  40,
     41,  42,  43,  44,  45,  46,  47,  48,  49,  50,   2,  51,   2,   2,  52,  53,
     54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,
      2,   2,   2,  70,   2,   2,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,
     81,  82,  83,  84,  85,  86,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,
     79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,
     79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,
     79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  87,  79,  79,  79,  79,
     79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,
     79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,
     88,  79,  79,  79,  79,  79,  79,  79,  79,  89,   2,   2,  90,  91,   2,  92,
     93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103, 104, 105, 106, 107, 101,
    102, 103, 104, 105, 106, 107, 101, 102, 103, 104, 105, 106, 107, 101, 102, 103,
    104, 105, 106, 107, 101, 102, 103, 104, 105, 106, 107, 101, 102, 103, 104, 105,
    106, 107, 101, 102, 103, 104, 105, 106, 107, 101, 102, 103, 104, 105, 106, 107,
    101, 102, 103, 104, 105, 106, 107, 101, 102, 103, 104, 105, 106, 107, 101, 102,
    103, 104, 105, 106, 107, 101, 102, 103, 104, 105, 106, 107, 101, 102, 103, 108,
    109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109,
    110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
    110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
    110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
    110, 110,  79,  79,  79,  79, 111, 112,   2,   2, 113, 114, 115, 116, 117, 118,
    119, 120, 121, 122, 110, 123, 124, 125,   2, 126, 127, 110,   2,   2, 128, 110,
    129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 110, 140, 110, 141, 110,
    142, 143, 144, 145, 146, 147, 148, 110, 149, 150, 110, 151, 152, 153, 154, 110,
    155, 156, 110, 110, 157, 158, 110, 110, 159, 160, 161, 162, 110, 163, 110, 110,
      2,   2,   2,   2,   2,   2,   2, 164, 165,   2, 166, 110, 110, 110, 110, 110,
    110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
      2,   2,   2,   2, 167, 168, 169,   2, 170, 110, 110, 110, 110, 110, 110, 110,
    110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
    110, 110, 110, 110, 110, 110, 110, 110,   2,   2,   2, 171, 172, 110, 110, 110,
    110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
    110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
      2,   2,   2,   2, 173, 174, 175, 176, 110, 110, 110, 110, 177, 178, 179, 180,
     79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79, 181,
     79,  79,  79,  79,  79, 182, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
     79,  79, 183,  79,  79, 184, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
    110, 110, 110, 110, 110, 110, 110, 110, 185, 186, 110, 110, 110, 110, 110, 110,
      2, 187, 188, 189, 190, 191, 192, 110, 193, 194, 195,   2,   2, 196,   2, 197,
      2,   2,   2,   2, 198, 199, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
    200, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
      2, 201, 202, 110, 110, 110, 110, 110, 203, 204, 110, 110, 205, 206, 110, 110,
     79,  79, 207, 208,  79,  79,  79, 209, 210, 211, 212, 213, 214, 215, 216, 217,
    218, 219, 220, 221,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79, 222,
     79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,
     79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79,  79, 222,
    223, 110, 224, 225, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
    110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
};

static RE_UINT16 re_line_break_stage_3[] = {
      0,   1,   2,   3,   4,   5,   4,   6,   7,   1,   8,   9,   4,  10,   4,  10,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,  11,  12,   4,   4,
      1,   1,   1,   1,  13,  14,  15,  16,  17,   4,  18,   4,   4,   4,   4,   4,
     19,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,  20,   4,  21,   4,   4,
     22,  23,   1,  24,  25,  26,  27,  28,  29,  30,   4,   4,  31,   1,  32,  33,
      4,   4,   4,   4,   4,  34,  35,  36,  37,  38,   4,   1,  39,   4,   4,   4,
      4,   4,  40,  41,  36,   4,  31,  42,   4,  43,  44,  45,   4,  46,  47,  48,
     48,  48,   4,  49,  48,  50,  51,   1,  52,   4,   4,  53,   1,  54,  55,   4,
     56,  57,  58,  59,  60,  61,  62,  63,  64,  57,  58,  65,  66,  67,  68,  69,
     70,  18,  58,  71,  72,  73,  62,  74,  75,  57,  58,  71,  76,  77,  62,  78,
     79,  80,  81,  82,  83,  84,  68,  85,  86,  87,  58,  88,  89,  90,  62,  91,
     92,  87,  58,  93,  89,  94,  62,  95,  96,  87,   4,  97,  98,  99,  62, 100,
    101, 102,   4, 103, 104, 105,  68, 106, 107, 108, 108, 109, 110, 111,  48,  48,
    112, 113, 114, 115, 116, 117,  48,  48, 118, 119,  36, 120, 121,   4, 122, 123,
    124, 125,   1, 126, 127, 128,  48,  48, 108, 108, 108, 108, 129, 108, 108, 108,
    108, 130,   4,   4, 131,   4,   4,   4, 132, 132, 132, 132, 132, 132, 133, 133,
    133, 133, 134, 135, 135, 135, 135, 135,   4,   4,   4,   4, 136, 137,   4,   4,
    136,   4,   4, 138, 139, 140,   4,   4,   4, 139,   4,   4,   4, 141, 142, 122,
      4, 143,   4,   4,   4,   4,   4, 144, 145,   4,   4,   4,   4,   4,   4,   4,
    145, 146,   4,   4,   4,   4, 147, 148, 149, 150,   4, 151,   4, 152, 149, 153,
    108, 108, 108, 108, 108, 154, 155, 143, 156, 155,   4,   4,   4,   4,   4, 148,
    157,   4, 158,   4,   4,   4,   4, 159,   4,  45, 160, 160, 161, 108, 162, 163,
    108, 108, 164, 108, 165, 166,   4,   4,   4, 167, 108, 108, 108, 168, 108, 169,
    155, 155, 162, 170,  48,  48,  48,  48, 171,   4,   4, 172, 173, 174, 175, 176,
    177,   4, 178,  36,   4,   4,  40, 179,   4,   4, 172, 180, 181,  36,   4, 182,
    148,   4,   4, 183,  78, 184, 185, 186,   4,   4,   4,   4,   1,   1,   1, 187,
      4, 144,   4,   4, 144, 188,   4, 189,   4,   4,   4, 190, 190, 191,   4, 192,
    193, 194, 195, 196, 197, 198, 199, 200, 201, 122, 202, 203, 204,   1,   1, 205,
    206, 207, 208,   4,   4, 209, 210, 211, 212, 211,   4,   4,   4, 213,   4,   4,
    214, 215, 216, 217, 218, 219, 220,   4, 221, 222, 223, 224,   4,   4, 225,   4,
    226, 227, 228,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 229,
      4,   4, 230,  48,  47,  48, 231, 231, 231, 231, 231, 231, 231, 231, 231, 232,
    231, 231, 231, 231, 210, 231, 231, 233, 231, 234, 235, 236, 237, 238, 239,   4,
    240, 241,   4, 242, 243,   4, 244, 245,   4, 246,   4, 247, 248, 249, 250, 251,
    252,   4,   4,   4,   4, 253, 254, 255, 231, 256,   4,   4, 257,   4, 258,   4,
    259, 260,   4,   4,   4, 226,   4, 261,   4,   4,   4,   4,   4, 262,   4, 263,
      4, 264,   4,   4,  58,   4,   4,  45,   4,   4,  45,   4,   4,  45,   4,   4,
      4,   4,   4,   4,   4,   4, 265, 266,   4,   4, 131,   4,   4,   4, 267, 268,
      4, 230, 269, 269, 269, 269,   1,   1, 270, 271, 272, 273, 274,  48,  48,  48,
    275, 276, 275, 275, 275, 275, 275, 277, 275, 275, 275, 275, 275, 275, 275, 275,
    275, 275, 275, 275, 275, 278,  48, 279, 280, 281, 282, 283, 284, 275, 285, 275,
    286, 287, 288, 275, 285, 275, 286, 289, 290, 275, 275, 291, 275, 275, 275, 275,
    292, 275, 275, 293, 275, 275, 277, 294, 275, 292, 275, 275, 295, 275, 275, 275,
    275, 275, 275, 275, 275, 275, 275, 292, 275, 275, 275, 275,   4,   4,   4,   4,
    275, 296, 275, 275, 275, 275, 275, 275, 297, 275, 275, 275, 298,   4,   4, 182,
    299,   4, 300,  48,   4,   4, 265, 301,   4, 302,   4,   4,   4,   4,   4, 303,
      4,   4,   4, 143,  48,  48,  48, 304, 305,   4, 306, 307,   4,   4,   4, 308,
    309,   4,   4, 172, 310, 155,   1, 311,  36,   4, 312,   4, 313, 314, 132, 315,
     52,   4,   4, 316, 317, 318, 108, 319,   4,   4, 320, 321, 322, 323, 108, 108,
    108, 108, 108, 108, 324, 325,  31, 326, 327, 328, 269,   4,   4,   4, 159,   4,
      4,   4,   4,   4,   4,   4, 329, 155, 330, 331, 332, 333, 332, 334, 332, 330,
    331, 332, 333, 332, 334, 332, 330, 331, 332, 333, 332, 334, 332, 330, 331, 332,
    333, 332, 334, 332, 330, 331, 332, 333, 332, 334, 332, 330, 331, 332, 333, 332,
    334, 332, 330, 331, 332, 333, 332, 334, 332, 330, 331, 332, 333, 332, 334, 332,
    333, 332, 335, 133, 336, 135, 135, 337, 338, 338, 338, 338, 338, 338, 338, 338,
     48,  48,  48,  48,  48,  48,  48,  48, 230, 339, 340, 341, 342,   4,   4,   4,
      4,   4,   4,   4, 343, 344,   4,   4,   4,   4,   4, 345,  48,   4,   4,   4,
      4, 346,   4,   4,  78,  48,  48, 347,   1, 348,   1, 349, 350, 351, 352, 190,
      4,   4,   4,   4,   4,   4,   4, 353, 354, 355, 275, 356, 275, 357, 358, 359,
    275, 360, 275, 292, 361, 362, 363, 364, 365,   4, 140, 366, 189, 189,  48,  48,
      4,   4,   4,   4,   4,   4,   4,  47, 367,   4,   4, 368,   4,   4,   4,   4,
     45, 369,  73,  48,  48,   4,   4, 370,   4, 122,   4,   4,   4,  73,  33, 369,
      4,   4, 371,   4,  47,   4,   4, 372,   4, 373,   4,   4, 374, 375,  48,  48,
      4, 189, 155,   4,   4, 374,   4, 369,   4,   4,  78,   4,   4,   4, 376,  48,
      4,   4,   4, 230,   4, 159,  78,  48, 377,   4,   4, 378,   4, 379,   4,   4,
      4,  45, 304,  48,  48,  48,   4, 380,   4, 381,   4, 382,  48,  48,  48,  48,
      4,   4,   4, 383,   4, 346,   4,   4, 384, 385,   4, 386, 148, 387,   4,   4,
      4,   4,  48,  48,   4,   4, 388, 389,   4,   4,   4, 390,   4, 264,   4, 391,
      4, 392, 393,  48,  48,  48,  48,  48,   4,   4,   4,   4, 148,  48,  48,  48,
      4,   4,   4, 394,   4,   4,   4, 395,   4,   4, 396, 155,  48,  48,  48,  48,
     48,  48,  48,  48,  48,  48,   4,  45,   4,   4,  78,   4,  40, 397,  48,  48,
    177,   4,   4, 398, 399, 346, 400, 401, 177,   4,   4, 402, 403,   4, 148, 155,
    177,   4, 313, 404, 405,   4,   4, 406, 177,   4,   4, 316, 407, 408,  20, 409,
      4,  18, 410, 411,  48,  48,  48,  48, 412,  37, 413,   4,   4, 265, 414, 155,
    415,  57,  58, 416,  76, 417, 418, 419,   4,   4,   4, 420, 421, 422,  48,  48,
      4,   4,   4,   1, 423, 155,  48,  48,   4,   4, 265, 424, 425, 426,  48,  48,
      4,   4,   4,   1, 427, 155, 428,  48,   4,   4,  31, 429, 155,  48,  48,  48,
    108, 430, 164, 431,  48,  48,  48,  48,   4,   4, 410, 432,  48,  48,  48,  48,
     48,  48,   4,   4,   4,   4,  36, 433, 434,   4,   4, 435, 436, 437,   4,   4,
    438, 439, 440,  48,   4,   4,   4, 148,  58,   4, 265, 441, 442,  36, 122, 443,
      4, 444, 125, 321,  48,  48,  48,  48, 445,   4,   4, 446, 447, 155, 448,   4,
    449, 450, 155,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,   4, 451,
      4, 143,  48,  48,  48,  48,  48,  48,   4,   4,   4,   4,   4,   4,  45, 452,
      4,   4,   4,   4, 453,  48,  48,  48,   4,   4,   4,   4,   4, 454,   4,   4,
    455,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4, 456,
      4,   4,  45,  48,  48,  48,  48,  48,   4,   4,   4,   4, 457,   4,   4,   4,
      4,   4,   4,   4, 230,  48,  48,  48,   4,   4,   4, 148,   4,  45, 458,  48,
     48,  48,  48,  48,  48,   4, 189, 459,   4,   4,   4, 460, 461, 462,  18, 463,
      4,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,  48,   4,   4,   4,   4,
      4, 464,  48,  48,  48,  48,  48,  48,   4,   4,   4,   4, 409, 465,   1, 170,
    401, 177,  48,  48,  48,  48, 466,  48, 275, 275, 275, 275, 275, 275, 275, 467,
    275, 275, 275, 275, 275, 275, 275, 468, 275, 292,  48,  48,  48,  48,  48, 275,
    275, 275, 275, 275, 275, 275, 275, 279,   4,   4,   4,   4,   4,   4,  47, 122,
    148, 469, 470,  48,  48,  48,  48,  48,   4,   4,   4,   4,   4,   4,   4, 159,
      4,   4,  21,   4,   4,   4, 471,   1, 472,   4, 473,   4,   4,   4, 148,  48,
      4,   4,   4,   4, 474,  48,  48,  48,  48,  48,  48,  48,  48,  48,   4, 453,
      4,   4,   4,   4,   4, 230,   4, 148,   4,   4,   4,   4,   4, 190,   4,   4,
      4, 149, 475, 476, 477,   4,   4,   4, 478, 479,   4, 480, 481,  87,   4,   4,
      4,   4, 264,   4,   4,   4,   4,   4,   4,   4,   4,   4, 482, 483, 483, 483,
      1,   1,   1, 484,   1,   1, 485, 486, 487, 488,  23,  48,  48,  48,  48,  48,
    441, 489, 490,  48,  48,  48,  48,  48,   4,   4,   4,   4, 491, 321,  48,  48,
      4,   4,   4,   4, 492, 493,  48,  48,  48,  48,  48,  48,  48,  48,  48,  20,
      4,   4, 494, 495,  48,  48,  48,  48, 477,   4, 496, 497, 498, 499, 500, 501,
    502, 369, 503, 369,  48,  48,  48, 343, 504, 231, 505, 231, 231, 231, 506, 231,
    231, 231, 504, 275, 275, 275, 507, 508, 509, 510, 275, 511, 512, 275, 275, 513,
    275, 275, 275, 275, 514, 515, 516, 517, 518, 275, 519, 520, 275, 275, 275, 275,
    521, 522, 523, 524, 525, 275, 275, 526, 275, 527, 275, 275, 275, 528, 275, 529,
    275, 275, 275, 275, 530,   4,   4, 531, 275, 275, 532, 533, 534, 275, 275, 275,
      4,   4,   4,   4,   4,   4,   4, 535,   4,   4,   4,   4,   4, 523, 275, 275,
    536,   4,   4,   4, 537, 525,   4,   4, 537,   4, 538, 275, 275, 275, 275, 275,
    536, 539, 540, 541, 275, 275, 275, 275, 275, 275, 275, 542, 275, 543, 275, 275,
    275, 275, 275, 275, 275, 275, 275, 544, 545,  48,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,  48,
};

static RE_UINT8 re_line_break_stage_4[] = {
      0,   0,   0,   0,   1,   2,   3,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      4,   5,   6,   7,   8,   9,  10,  11,  12,  12,  12,  12,  12,  13,  14,  15,
     14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  16,  17,  14,
     14,  14,  14,  14,  14,  16,  18,  19,   0,   0,  20,   0,   0,   0,   0,   0,
     21,  22,  23,  24,  25,  26,  27,  14,  22,  28,  29,  28,  28,  26,  28,  30,
     14,  14,  14,  24,  14,  14,  14,  14,  14,  14,  14,  24,  31,  28,  31,  14,
     25,  14,  14,  14,  28,  28,  24,  32,   0,   0,   0,   0,   0,   0,   0,  33,
      0,   0,   0,   0,   0,   0,  34,  34,  34,  35,   0,   0,   0,   0,   0,   0,
     14,  14,  14,  14,  36,  14,  14,  37,  36,  36,  14,  14,  14,  38,  38,  14,
     14,  39,  14,  14,  14,  14,  14,  14,  14,  19,   0,   0,   0,  14,  14,  14,
     39,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  38,  39,  14,  14,  14,
     14,  14,  14,  14,  40,  41,  39,   9,  42,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  43,  19,  44,   0,  45,  36,  36,  36,  36,
     46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  46,  47,  36,  48,
     46,  49,  38,  36,  36,  36,  36,  36,  14,  14,  14,  14,  50,  51,  13,  14,
      0,   0,   0,   0,   0,  52,  53,  54,  14,  14,  14,  14,  14,  19,   0,   0,
     12,  12,  12,  12,  12,  55,  56,  14,  44,  14,  14,  14,  14,  14,  14,  14,
     14,  14,  57,   0,   0,   0,  44,  19,   0,   0,  44,  19,  44,   0,   0,  14,
     12,  12,  12,  12,  12,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  39,
     19,  14,  14,  14,  14,  14,  14,  14,   0,   0,   0,   0,   0,  53,  39,  14,
     14,  14,  14,   0,   0,   0,   0,   0,  44,  36,  36,  36,  36,  36,  36,  36,
      0,   0,  14,  14,  58,  38,  42,  23,  14,  14,  14,   0,   0,  19,   0,   0,
      0,   0,  19,   0,  19,   0,   0,  36,  14,  14,  14,  14,  14,  14,  14,  38,
     14,  14,  14,  14,  19,   0,  36,  38,  14,  14,  14,  14,  14,  38,  36,  36,
     36,  36,  36,  36,  36,  36,  36,  36,  14,  14,  38,  14,  14,  14,  14,  36,
     36,  42,   0,   0,   0,   0,   0,   0,   0,  19,   0,   0,   0,   0,   0,   0,
      0,   0,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,   0,  44,   0,
     19,   0,   0,   0,  14,  14,  14,  14,  14,   0,  59,  12,  12,  12,  12,  12,
     19,   0,  39,  14,  14,  14,  38,  39,  38,  39,  14,  14,  14,  14,  14,  14,
     14,  14,  14,  14,  38,  14,  14,  14,  38,  38,  36,  14,  14,  36,  44,   0,
      0,   0,  53,  42,  53,  42,   0,  38,  36,  36,  36,  42,  36,  36,  14,  39,
     14,   0,  36,  12,  12,  12,  12,  12,  14,  51,  14,  14,  50,   9,  14,  53,
     42,   0,  39,  14,  14,  38,  36,  39,  38,  14,  39,  38,  14,  36,  53,   0,
      0,  53,  36,  42,  53,  42,   0,  36,  42,  36,  36,  36,  39,  14,  38,  38,
     36,  36,  36,  12,  12,  12,  12,  12,   0,  14,  19,  38,  36,  36,  36,  36,
     42,   0,  39,  14,  14,  14,  14,  39,  38,  14,  39,  14,  14,  36,  44,   0,
      0,   0,   0,  42,   0,  42,   0,  36,  38,  36,  36,  36,  36,  36,  36,  36,
      9,  36,  36,  36,  39,   0,   0,   0,  42,   0,  39,  14,  14,  14,  38,  39,
      0,   0,  53,  42,  53,  42,   0,  36,  36,  36,  36,   0,  36,  36,  14,  39,
     14,  14,  14,  14,  36,  36,  36,  36,  36,  44,  39,  14,  14,  38,  36,  14,
     38,  14,  14,  36,  39,  38,  38,  14,  36,  39,  38,  36,  14,  38,  36,  14,
     14,  14,  14,  14,  14,  36,  36,   0,   0,  53,  36,   0,  53,   0,   0,  36,
     38,  36,  36,  42,  36,  36,  36,  36,  14,  14,  14,  14,   9,  38,  36,  36,
      0,   0,  44,  14,  14,  14,  38,  14,  38,  14,  14,  14,  14,  14,  14,  14,
     14,  14,  14,  14,  14,  36,  39,   0,   0,   0,  53,   0,  53,   0,   0,  36,
     36,  36,  42,  53,  14,  38,  36,  36,  36,  36,  36,  36,  14,  14,  14,  14,
     19,   0,  29,  14,  14,  14,  38,  14,  14,  14,  39,  14,  14,  36,  44,   0,
     36,  36,  42,  53,  36,  36,  36,  38,  39,  38,  36,  36,  36,  36,  36,  36,
      0,   0,  39,  14,  14,  14,  38,  14,  14,  14,  14,  14,  14,  19,  44,   0,
      0,   0,  53,   0,  53,   0,   0,  14,  36,  36,  14,  19,  14,  14,  14,  14,
     14,  14,  14,  14,  50,  14,  14,  14,  36,   0,  39,  14,  14,  14,  14,  14,
     14,  14,  14,  38,  36,  14,  14,  14,  14,  39,  14,  14,  14,  14,  39,  36,
     14,  14,  14,  38,  36,  53,  36,  42,   0,   0,  53,  53,   0,   0,   0,   0,
     36,   0,  38,  36,  36,  36,  36,  36,  60,  61,  61,  61,  61,  61,  61,  61,
     61,  61,  61,  61,  61,  61,  61,  61,  61,  61,  61,  61,  61,  62,  36,  63,
     61,  61,  61,  61,  61,  61,  61,  64,  12,  12,  12,  12,  12,  59,  36,  36,
     60,  62,  62,  60,  62,  62,  60,  36,  36,  36,  61,  61,  60,  61,  61,  61,
     60,  61,  60,  60,  36,  61,  60,  61,  61,  61,  61,  61,  61,  60,  61,  36,
     61,  61,  62,  62,  61,  61,  61,  36,  12,  12,  12,  12,  12,  36,  61,  61,
     32,  65,  29,  65,  66,  67,  68,  54,  54,  69,  57,  14,   0,  14,  14,  14,
     14,  14,  43,  19,  19,  70,  70,   0,  14,  14,  14,  14,  39,  14,  14,  14,
     14,  14,  14,  14,  14,  14,  38,  36,  42,   0,   0,   0,   0,   0,   0,   1,
      0,   0,   1,   0,  14,  14,  19,   0,   0,   0,   0,   0,  42,   0,   0,   0,
      0,   0,   0,   0,   0,   0,  53,  59,  14,  14,  14,  44,  14,  14,  38,  14,
     65,  71,  14,  14,  72,  73,  36,  36,  12,  12,  12,  12,  12,  59,  14,  14,
     12,  12,  12,  12,  12,  61,  61,  61,  14,  14,  14,  39,  36,  36,  39,  36,
     74,  74,  74,  74,  74,  74,  74,  74,  75,  75,  75,  75,  75,  75,  75,  75,
     75,  75,  75,  75,  76,  76,  76,  76,  76,  76,  76,  76,  76,  76,  76,  76,
     14,  14,  14,  14,  38,  14,  14,  36,  14,  14,  14,  38,  38,  14,  14,  36,
     38,  14,  14,  36,  14,  14,  14,  38,  38,  14,  14,  36,  14,  14,  14,  14,
     14,  14,  14,  38,  14,  14,  14,  14,  14,  14,  14,  14,  14,  38,  42,   0,
     27,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  36,  36,  36,
     14,  14,  14,  36,  14,  14,  14,  36,  77,  14,  14,  14,  14,  14,  14,  14,
     14,  14,  14,  14,  14,  16,  78,  36,  14,  14,  14,  14,  14,  27,  59,  14,
     14,  14,  14,  14,  38,  36,  36,  36,  14,  14,  14,  14,  14,  14,  38,  14,
     14,   0,  53,  36,  36,  36,  36,  36,  14,   0,   1,  41,  36,  36,  36,  36,
     14,   0,  36,  36,  36,  36,  36,  36,  38,   0,  36,  36,  36,  36,  36,  36,
     61,  61,  59,  79,  77,  80,  61,  36,  12,  12,  12,  12,  12,  36,  36,  36,
     14,  54,  59,  29,  54,  19,   0,  73,  14,  14,  19,  44,  14,  14,  14,  14,
     14,  14,  14,  14,  19,  38,  36,  36,  14,  14,  14,  36,  36,  36,  36,  36,
      0,   0,   0,   0,   0,   0,  36,  36,  38,  36,  54,  12,  12,  12,  12,  12,
     61,  61,  61,  61,  61,  61,  61,  36,  61,  61,  62,  36,  36,  36,  36,  36,
     61,  61,  61,  61,  61,  61,  36,  36,  61,  61,  61,  61,  61,  36,  36,  36,
     12,  12,  12,  12,  12,  62,  36,  61,  14,  14,  14,  19,   0,   0,  36,  14,
     61,  61,  61,  61,  61,  61,  61,  62,  61,  61,  61,  61,  61,  61,  62,  42,
      0,   0,   0,   0,   0,   0,   0,  53,   0,   0,  44,  14,  14,  14,  14,  14,
     14,  14,   0,   0,   0,   0,   0,   0,   0,   0,  44,  14,  14,  14,  36,  36,
     12,  12,  12,  12,  12,  59,  27,  59,  77,  14,  14,  14,  14,  19,   0,   0,
      0,   0,  14,  14,  14,  14,  38,  36,   0,  44,  14,  14,  14,  14,  14,  14,
     19,   0,   0,   0,   0,   0,   0,  14,   0,   0,  36,  36,  36,  36,  14,  14,
      0,   0,   0,   0,  36,  81,  59,  59,  12,  12,  12,  12,  12,  36,  39,  14,
     14,  14,  14,  14,  14,  14,  14,  59,  14,  14,  14,  14,  14,  38,  39,  14,
      0,  44,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  44,  14,  19,  14,
     14,   0,  44,  19,   0,  36,  36,  36,   0,   0,   0,   0,   0,  42,   0,   0,
     14,  14,  14,  14,  39,  39,  39,  39,  14,  14,  14,  14,  14,  14,  14,  36,
     14,  14,  38,  14,  14,  14,  14,  14,  14,  14,  36,  14,  14,  14,  39,  14,
     36,  14,  38,  14,  14,  14,  32,  38,  59,  59,  59,  82,  59,  83,  84,   0,
     82,  59,  85,  25,  86,  87,  86,  87,  28,  14,  88,  89,  90,   0,   0,  33,
     51,  51,  51,  51,   7,  91,  92,  14,  14,  14,  93,  94,  92,  14,  14,  14,
     14,  14,  14,  77,  59,  59,  27,  59,  95,  14,  38,   0,   0,   0,   0,   0,
     14,  36,  25,  14,  14,  14,  16,  96,  24,  28,  25,  14,  14,  14,  16,  78,
     23,  23,  23,   6,  23,  23,  23,  23,  23,  23,  23,  22,  23,   6,  23,  22,
     23,  23,  23,  23,  23,  23,  23,  23,  53,  36,  36,  36,  36,  36,  36,  36,
     14,  50,  24,  14,  50,  14,  14,  14,  14,  24,  14,  97,  14,  14,  14,  14,
     24,  25,  14,  14,  14,  24,  14,  14,  14,  14,  28,  14,  14,  24,  14,  25,
     28,  28,  28,  28,  28,  28,  14,  14,  28,  28,  28,  28,  28,  14,  14,  14,
     14,  14,  14,  14,  24,  14,  36,  36,  14,  25,  25,  14,  14,  14,  14,  14,
     25,  28,  14,  24,  25,  24,  14,  24,  24,  23,  24,  14,  14,  25,  24,  28,
     25,  24,  24,  24,  28,  28,  25,  25,  14,  14,  28,  28,  14,  14,  28,  14,
     14,  14,  14,  14,  25,  14,  25,  14,  14,  25,  14,  14,  14,  14,  14,  14,
     28,  14,  28,  28,  14,  28,  14,  28,  14,  28,  14,  28,  14,  14,  14,  14,
     14,  14,  24,  14,  24,  14,  14,  14,  14,  14,  24,  14,  14,  14,  14,  14,
     14,  14,  14,  14,  14,  14,  14,  24,  14,  14,  14,  14,  14,  14,  14,  98,
     14,  14,  14,  14,  70,  70,  14,  14,  14,  25,  14,  14,  14,  99,  14,  14,
     14,  14,  14,  14,  16, 100,  14,  14,  99,  99,  14,  14,  14,  14,  14,  14,
     14,  14,  14,  38,  36,  36,  36,  36,  28,  28,  28,  28,  28,  28,  28,  28,
     28,  28,  28,  28,  28,  28,  28,  25,  28,  28,  25,  14,  14,  14,  14,  14,
     14,  28,  28,  14,  14,  14,  14,  14,  28,  24,  28,  28,  28,  14,  14,  14,
     14,  28,  14,  28,  14,  14,  28,  14,  28,  14,  14,  28,  25,  24,  14,  28,
     28,  14,  14,  14,  14,  14,  14,  14,  14,  28,  28,  14,  14,  14,  14,  24,
     99,  99,  24,  25,  24,  14,  14,  28,  14,  14,  99,  28, 101,  99, 102,  99,
     14,  14,  14,  14, 103,  99,  14,  14,  25,  25,  14,  14,  14,  14,  14,  14,
     28,  24,  28,  24, 104,  25,  28,  24,  14,  14,  14,  14,  14,  14,  14, 103,
     14,  14,  14,  14,  14,  14,  14,  28,  14,  14,  14,  14,  14,  14, 103,  99,
     99,  99,  99,  99, 104,  28, 105, 103,  99, 105, 104,  28,  99,  28, 104, 105,
     99,  24,  14,  14,  28, 104,  28,  28, 105,  99,  99, 105, 102, 104, 105,  99,
     99,  99, 101,  14,  99, 106, 106,  14,  14,  14,  14,  24,  14,   7,  86,  86,
      5,  54, 101,  14,  70,  70,  70,  70,  70,  70,  70,  28,  28,  28,  28,  28,
     28,  28,  14,  14,  14,  14,  14,  14,  14,  14,  16, 100,  14,  14,  14,  14,
     14,  14,  14,  70,  70,  70,  70,  70,  14,  16, 107, 107, 107, 107, 107, 107,
    107, 107, 107, 107, 100,  14,  14,  14,  14,  14,  14,  14,  14,  14,  70,  14,
     14,  14,  24,  28,  28,  14,  14,  14,  14,  14,  36,  14,  14,  14,  14,  14,
     14,  14,  14,  36,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  19,
      0,  14,  36,  36, 108,  59,  77, 109,  14,  14,  14,  14,  36,  36,  36,  39,
     41,  36,  36,  36,  36,  36,  36,  42,  14,  14,  14,  38,  14,  14,  14,  38,
     86,  86,  86,  86,  86,  86,  86,  59,  59,  59,  59,  27, 110,  14,  86,  14,
     86,  70,  70,  70,  70,  59,  59,  57,  59,  27,  77,  14,  14, 111,  59,  77,
     59, 110,  59,  59,  59,  77,  77,  41,  99,  99,  99,  99,  99,  99,  99,  99,
     99,  99,  99,  99,  99, 112,  99,  99,  99,  99,  36,  36,  36,  36,  36,  36,
     99,  99,  99,  36,  36,  36,  36,  36,  99,  99,  99,  99,  99,  99,  36,  36,
     18, 113, 114,  99,  70,  70,  70,  70,  70,  99,  70,  70,  70,  70, 115, 116,
     99,  99,  99,  99,  99,   0,   0,   0,  99,  99, 117,  99,  99, 114, 118,  99,
    119, 120, 120, 120, 120,  99,  99,  99,  99, 120,  99,  99,  99,  99,  99,  99,
     99, 120, 120, 120,  99,  99,  99, 121,  99,  99, 120, 122,  42, 123,  92, 118,
    124, 120, 120, 120, 120,  99,  99,  99,  99,  99, 120, 121,  99, 114, 125, 118,
     36,  36, 112,  99,  99,  99,  99,  99, 112,  99,  99,  99,  99,  99,  99,  99,
     99,  99,  99,  99,  99,  99,  99, 126,  99,  99,  99,  99,  99, 126,  36,  36,
    127, 127, 127, 127, 127, 127, 127, 127,  99,  99,  99,  99,  28,  28,  28,  28,
     99,  99, 114,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99,  99, 126,  36,
     99,  99,  99, 126,  36,  36,  36,  36,  14,  14,  14,  14,  14,  14,  27, 109,
     12,  12,  12,  12,  12,  14,  36,  36,   0,  44,   0,   0,   0,   0,   0,  14,
     14,  14,  14,  14,  14,  14,  14,   0,   0,  27,  59,  59,  36,  36,  36,  36,
     36,  36,  36,  39,  14,  14,  14,  14,  14,  44,  14,  44,  14,  19,  14,  14,
     14,  19,   0,   0,  14,  14,  36,  36,  14,  14,  14,  14, 128,  36,  36,  36,
     14,  14,  65,  54,  36,  36,  36,  36,   0,  14,  14,  14,  14,  14,  14,  14,
      0,   0,   0,  36,  36,  36,  36,  59,   0,  14,  14,  14,  14,  14,  29,  19,
     14,  14,  14,   0,   0,   0,   0,  59,  14,  14,  14,  19,   0,   0,   0,   0,
      0,   0,  36,  36,  36,  36,  36,  39,  74,  74,  74,  74,  74,  74, 129,  36,
     14,  19,   0,   0,   0,   0,   0,   0,  44,  14,  14,  27,  59,  14,  14,  39,
     12,  12,  12,  12,  12,  36,  36,  14,  12,  12,  12,  12,  12,  61,  61,  62,
     14,  14,  14,  14,  19,   0,   0,   0,   0,   0,   0,  53,  36,  36,  36,  36,
     14,  19,  14,  14,  14,  14,   0,  36,  12,  12,  12,  12,  12,  36,  27,  59,
     61,  62,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  36,  60,  61,  61,
     59,  14,  19,  53,  36,  36,  36,  36,  39,  14,  14,  38,  39,  14,  14,  38,
     39,  14,  14,  38,  36,  36,  36,  36,  14,  19,   0,   0,   0,   1,   0,  36,
    130, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 130, 131,
    131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 130, 131, 131, 131,
    131, 131, 130, 131, 131, 131, 131, 131, 131, 131,  36,  36,  36,  36,  36,  36,
     75,  75,  75, 132,  36, 133,  76,  76,  76,  76,  76,  76,  76,  76,  36,  36,
    134, 134, 134, 134, 134, 134, 134, 134,  36,  39,  14,  14,  36,  36,  48, 135,
     46,  46,  46,  46,  49,  46,  46,  46,  46,  46,  46,  47,  46,  46,  47,  47,
     46,  48,  47,  46,  46,  46,  46,  46,  14,  36,  36,  36,  36,  36,  36,  36,
     36,  39,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14, 107,
     36,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14, 128,  36,
    136, 137,  58, 138, 139,  36,  36,  36,  99,  99, 140, 107, 107, 107, 107, 107,
    107, 107, 113, 140, 113,  99,  99,  99, 113,  78,  92,  54, 140, 107, 107, 113,
     99,  99,  99, 126, 141, 142,  36,  36,  14,  14,  14,  14,  14,  14,  38, 143,
    108,  99,   6,  99,  70,  99, 113, 113,  99,  99,  99,  99,  99,  92,  99, 144,
     99,  99,  99,  99,  99, 140, 145,  99,  99,  99,  99,  99,  99, 140, 145, 140,
    116,  70,  94, 120, 127, 127, 127, 127, 121,  99,  99,  99,  99,  99,  99,  99,
     99,  99,  99,  99,  99,  99,  99,  92,  36,  99,  99,  99,  36,  99,  99,  99,
     36,  99,  99,  99,  36,  99, 126,  36,  22,  99, 141, 146,  14,  14,  14,  38,
     36,  36,  36,  36,  42,   0, 147,  36,  14,  14,  14,  14,  14,  14,  39,  14,
     14,  14,  14,  14,  14,  38,  14,  39,  59,  41,  36,  39,  14,  14,  14,  14,
     14,  14,  36,  39,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  36,  36,
     14,  14,  14,  14,  14,  14,  19,  36,  14,  14,  36,  36,  36,  36,  39,  14,
     14,  14,  14,   0,   0,  53,  36,  36,  14,  14,  14,  14,  14,  14,  14,  81,
     14,  14,  36,  36,  14,  14,  14,  14,  77,  14,  14,  36,  36,  36,  36,  36,
     14,  14,  36,  36,  36,  36,  36,  39,  14,  14,  14,  36,  38,  14,  14,  14,
     14,  14,  14,  39,  38,  36,  38,  39,  14,  14,  14,  81,  14,  14,  14,  14,
     14,  38,  14,  36,  36,  39,  14,  14,  14,  14,  14,  14,  14,  14,  36,  81,
     14,  14,  14,  14,  14,  36,  36,  39,  14,  14,  14,  14,  36,  36,  14,  14,
     19,   0,  42,  53,  36,  36,   0,   0,  14,  14,  39,  14,  39,  14,  14,  14,
     14,  14,  14,  36,   0,  53,  36,  42,  59,  59,  59,  59,  38,  36,  36,  36,
     14,  14,  19,  53,  36,  39,  14,  14,  59,  59,  59, 148,  36,  36,  36,  36,
     14,  14,  14,  36,  81,  59,  59,  59,  14,  38,  36,  36,  14,  14,  14,  14,
     14,  36,  36,  36,  39,  14,  38,  36,  36,  36,  36,  36,  39,  14,  14,  14,
     14,  38,  36,  36,  36,  36,  36,  36,  14,  38,  36,  36,  36,  14,  14,  14,
     14,  14,   0,   0,  36,  36,  36,  36,  44,  14,  14,  14,  14,  36,  36,  36,
     14,  14,  14,  14,   0,   0,   0,   0,   0,   0,   0,   1,  77,  14,  14,  36,
     14,  14,  14,  12,  12,  12,  12,  12,  36,  36,  36,  36,  36,  36,  36,  42,
      0,   0,   0,   0,   0,  44,  14,  59,  59,  36,  36,  36,  36,  36,  39,  36,
      0,   0,  53,  12,  12,  12,  12,  12,  59,  59,  19,  53,  36,  36,  36,  36,
     14,  19,  32,  38,  36,  36,  36,  36,  44,  14,  27,  77,  43,   0,  44,  36,
     12,  12,  12,  12,  12,  32,  27,  59,  14,  14,  38,  36,  36,  36,  36,  36,
     14,  14,  14,  14,  14,  14,   0,   0,   0,   0,   0,   0,  59,  27,  77,  53,
     14,  14,  14,  38,  38,  14,  14,  39,  14,  14,  14,  14,  27,  36,  36,  36,
      0,   0,   0,   0,   0,  53,  36,  36,   0,   0,  39,  14,  14,  14,  38,  39,
     38,  14,  39,  14,  14,  42,  44,   0,  38,  36,  36,  42,  36,  36,  39,  14,
     14,   0,  36,   0,   0,   0,  53,  36,   0,   0,  53,  36,  36,  36,  36,  36,
     14,  14,  19,   0,   0,   0,   0,   0,   0,   0,   0,  44,  14,  27,  59,  77,
     12,  12,  12,  12,  12,  81,  39,  53,   0,   0,  14,  14,  36,  36,  36,  36,
      0,   0,   0,  36,   0,   0,   0,   0, 149,  59,  54,  14,  27,  59,  59,  59,
     59,  59,  59,  59,  14,  14,   0,  36,   1,  77,  38,  36,  36,  36,  36,  36,
     65,  65,  65,  65,  65,  65, 150,  36,   0,   0,   0,   0,  36,  36,  36,  36,
     61,  61,  61,  61,  61,  62,  60,  61,  12,  12,  12,  12,  12,  61,  59, 151,
      0,   0,   0,   0,   0,  44,  36,  36,  14,  38,  36,  36,  36,  36,  36,  39,
     19,   0,   0,   0,   0,  44,  14,  14,  14,  19,   0,   0,   0,  19,   0, 149,
     27,  59,  71,  19,  36,  36,  36,  36,  19,   0,   0,   0,   0,   0,  14,  14,
     14,  14,  36,  14,  14,   0,   0,   0,   0,   0,   0,   0,   0,  59,  77,  65,
     67,  41,  36,  36,  36,  36,  36,  36,   0,   0,   0,  53,   0,   0,   0,   0,
     27,  59,  59,  36,  36,  36,  36,  36, 152,  14,  14,  14,  14,  14,  14,  14,
     36,   0,   0,   0,   0,   0,   0,   0,  14,  14,  14,  38,  14,  39,  14,  14,
     19,   0,   0,  53,  36,  53,   0,  42,   0,   0,   0,  19,  36,  36,  36,  36,
     14,  14,  14,  39,  38,  14,  14,  14,  14,  14,  14,  14,  14,   0,   0,  53,
      0,  42,   0,   0,  38,  36,  36,  36,  14,  19,   0,  44,  38,  36,  36,  36,
     59,  59,  41,  36,  36,  36,  36,  36,  14,  14,  36,  36,  36,  36,  36,  36,
     14,  14,  14,  14, 153,  70, 116,  14,  14, 100,  14,  70,  70,  14,  14,  14,
     14,  14,  14,  14,  16, 116,  14,  14,  14,  14,  14,  14,  14,  14,  14,  70,
     12,  12,  12,  12,  12,  36,  36,  59,   0,   0,   1,  36,  36,  36,  36,  36,
      0,   0,   0,   1,  59,  14,  14,  14,  14,  14,  77,  36,  36,  36,  36,  36,
     12,  12,  12,  12,  12,  39,  14,  14,  14,  14,  14,  14,  36,  36,  39,  14,
     14,  14,  14,  27,  77,  38,  36,  36,  19,   0,   0,   0,   0,   0,   0,   0,
     92,  36,  36,  36,  36,  36,  36,  36,  99,  36,  36,  36,  36,  36,  36,  36,
     99, 126,  36,  36,  36,  36,  36,  36,  14,  14,  14,  14,  14,  36,  19,   1,
      0,   0,  36,  36,  36,  36,  36,  36,  14,  14,  19,   0,   0,  14,  19,   0,
      0,  44,  19,   0,   0,   0,  14,  14,  14,  14,  14,  14,  14,   0,   0,  14,
     14,   0,  44,  36,  36,  36,  36,  36,  36,  38,  39,  38,  39,  14,  38,  14,
     14,  14,  14,  14,  14,  39,  39,  14,  14,  14,  39,  14,  14,  14,  14,  14,
     14,  14,  14,  39,  14,  38,  39,  14,  14,  14,  38,  14,  14,  14,  38,  14,
     14,  14,  14,  14,  14,  39,  14,  38,  14,  14,  38,  38,  36,  14,  14,  14,
     14,  14,  14,  14,  14,  14,  36,  12,  12,  12,  12,  12,  12,  12,  12,  12,
      0,   0,   0,  44,  14,  19,   0,   0,   0,   0,   0,   0,   0,   0,  44,  14,
     14,  14,  19,  14,  14,  14,  14,  14,  14,  14,  44,  27,  59,  77,  36,  36,
     36,  36,  36,  36,  36,  42,   0,   0,   0,   0,   0,   0,  53,  42,   0,   0,
      0,  42,  53,   0,   0,  53,  36,  36,  14,  14,  38,  39,  14,  14,  14,  14,
     14,  14,   0,   0,   0,  53,  36,  36,  12,  12,  12,  12,  12,  36,  36, 153,
     14,  14,  14,  14,  14,  14, 128,  14, 128,  14,  38,  36,  36,  36,  36,  36,
     39,  38,  38,  39,  39,  14,  14,  14,  14,  38,  14,  14,  39,  39,  36,  36,
     36,  38,  36,  39,  39,  39,  39,  14,  39,  38,  38,  39,  39,  39,  39,  39,
     39,  38,  38,  39,  14,  38,  14,  14,  14,  38,  14,  14,  39,  14,  38,  38,
     14,  14,  14,  14,  14,  39,  14,  14,  39,  14,  39,  14,  14,  39,  14,  14,
     28,  28,  28,  28,  28,  28, 105,  99,  28,  28,  28,  28,  28,  28,  28,  14,
     28,  28,  28,  28,  28,  14,  99,  99,  99,  99,  99, 154, 154, 154, 154, 154,
    154, 154, 154, 154, 154, 154, 154, 154,  99,  99, 102,  99,  99,  99,  99,  99,
     99,  99,  99,  99,  99,  99,  14,  99,  99,  99, 101, 103,  99,  99, 103,  99,
     99, 106, 155, 102,  99, 106, 155,  99,  99,  99,  99,  99,  99, 156, 157, 157,
     99, 106,  99, 106, 106, 106, 106, 106, 155,  99,  99,  99,  99,  99,  99,  99,
     99,  99,  99, 106, 106,  99,  99, 155, 106, 106, 106, 106, 155,  99, 155,  99,
    102, 106, 102, 106,  99,  99,  99,  99, 103, 103, 103,  99,  99, 155,  99, 101,
    101, 103,  99,  99,  99,  99,  99,  99,  14,  14,  14, 103,  99,  99,  99,  99,
     99,  99,  99, 101,  14,  14,  14,  14,  14,  14, 103,  99,  99,  99,  99,  99,
     99,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  99,  99,  99,
     99,  99, 106,  99,  99, 155,  99,  99, 155,  99, 102, 155,  99,  99,  99,  99,
     99,  99,  14,  14,  14,  14,  99,  99,  99,  99,  14,  14,  14,  99,  99,  99,
     99,  99, 102, 106,  99, 102, 106, 106,  14,  14,  14,  86, 158,  92,  14,  14,
     99, 102,  99,  99,  99,  99,  99,  99,  99,  99, 106, 155,  99,  99,  99,  99,
    155,  99,  99,  99,  99,  99, 155,  99,  14,  14,  99,  99,  99,  99,  99,  99,
     14,  14,  14,  14,  14,  14,  99,  99,  14,  14,  14,  14,  99,  99,  99,  99,
     14,  14,  14,  14,  14,  14,  14,  99,  99,  99,  99,  99, 106, 106, 155, 106,
     99,  99,  99, 155,  99,  99,  99,  99, 106, 106, 106, 106, 106,  99, 102, 155,
     99,  99, 102, 155, 106,  99,  99,  99, 102, 106, 106, 106, 106, 106, 106,  99,
     99,  99,  99,  99,  99,  99,  99,  36,  42,  36,  36,  36,  36,  36,  36,  36,
};

static RE_UINT8 re_line_break_stage_5[] = {
    16, 16, 16, 18, 22, 20, 20, 21, 19,  6,  3, 12,  9, 10, 12,  3,
     1, 36, 12,  9,  8, 15,  8,  7, 11, 11,  8,  8, 12, 12, 12,  6,
    12,  1,  9, 36, 18,  2, 12, 16, 16, 29,  4,  1, 10,  9,  9,  9,
    12, 25, 25, 12, 25,  3, 12, 18, 25, 25, 17, 12, 25,  1, 17, 25,
    12, 17, 16,  4,  4,  4,  4, 16,  0,  0,  8, 12, 12,  0,  0, 12,
    12,  8, 18,  0,  0, 16, 18, 16, 16, 12,  6, 16, 37, 37, 37,  0,
     0, 37, 37, 12, 12, 10, 10, 10, 16,  6, 16,  0,  6,  6, 10, 11,
    11, 12,  6, 12,  8,  6, 18, 18,  0, 24, 24, 24, 24,  0,  0,  9,
    24, 12, 17, 17,  4, 17, 17, 18,  4,  6,  4, 12,  1,  2, 18, 17,
    12,  4,  4,  0, 31, 31, 32, 32, 33, 33, 18, 12,  2,  0,  5, 24,
    18,  9,  0, 18, 18,  4, 18, 28, 16, 42, 26, 25,  3,  3,  1,  3,
    14, 14, 14, 18, 20, 20,  3, 25,  5,  5,  8,  1,  2,  5, 30, 12,
     2, 25,  9, 12, 12, 14, 13, 13,  2, 12, 13, 12, 13, 40, 12, 13,
    13, 25, 25, 13, 40, 40,  2,  1,  0,  6,  6, 18,  1, 18, 26, 26,
     0, 13,  2, 13, 13,  5,  5,  1,  2,  2, 13, 16,  5, 13,  0, 38,
    13, 38, 38, 13, 38,  0, 16,  5,  5, 38, 38,  5, 13,  0, 38, 38,
    10, 12, 31,  0, 34, 35, 35, 35, 32,  0,  0, 33, 27, 27, 16, 37,
     8,  2,  2,  8,  6,  1,  2, 14, 13,  1, 13,  9, 10, 13,  0, 30,
    13,  6, 13,  2,  9,  0, 23, 25, 14,  0, 16, 17, 17,  0, 18, 24,
    17,  6,  1,  1, 39, 39, 40, 13, 13, 41, 41, 41,  3,  5,
};

/* Line_Break: 9374 bytes. */

RE_UINT32 re_get_line_break(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 12;
    code = ch ^ (f << 12);
    pos = (RE_UINT32)re_line_break_stage_1[f] << 5;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_line_break_stage_2[pos + f] << 3;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_line_break_stage_3[pos + f] << 3;
    f = code >> 1;
    code ^= f << 1;
    pos = (RE_UINT32)re_line_break_stage_4[pos + f] << 1;
    value = re_line_break_stage_5[pos + code];

    return value;
}

/* Numeric_Type. */

static RE_UINT8 re_numeric_type_stage_1[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 11, 11, 11, 12,
    13, 14, 15, 11, 11, 11, 16, 11, 11, 11, 11, 11, 11, 17, 18, 19,
    20, 11, 21, 22, 11, 11, 23, 11, 11, 11, 11, 11, 11, 11, 11, 24,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
};

static RE_UINT8 re_numeric_type_stage_2[] = {
     0,  1,  1,  1,  1,  1,  2,  3,  1,  4,  5,  6,  7,  8,  9, 10,
    11,  1,  1, 12,  1,  1, 13, 14, 15, 16, 17, 18, 19,  1,  1,  1,
    20, 21,  1,  1, 22,  1,  1, 23,  1,  1,  1,  1, 24,  1,  1,  1,
    25, 26, 27,  1, 28,  1,  1,  1, 29,  1,  1, 30,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 31, 32,
     1, 33,  1, 34,  1,  1, 35,  1, 36,  1,  1,  1,  1,  1, 37, 38,
     1,  1, 39, 40,  1,  1,  1, 41,  1,  1,  1,  1,  1,  1,  1, 42,
     1,  1,  1, 43,  1,  1, 44,  1,  1,  1,  1,  1,  1,  1,  1,  1,
    45,  1,  1,  1, 46,  1,  1,  1,  1,  1,  1,  1, 47, 48,  1,  1,
     1,  1,  1,  1,  1,  1, 49,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1, 50,  1, 51, 52, 53, 54,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1, 55,  1,  1,  1,  1,  1, 15,
     1, 56, 57, 58, 59,  1,  1,  1, 60, 61, 62, 63, 64, 65, 66, 67,
    68, 69, 54,  1,  9,  1, 70, 71, 72,  1,  1,  1, 73, 74,  1,  1,
     1,  1,  1,  1, 75,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 76, 77,  1,  1, 78,  1,
     1,  1, 79, 80,  1,  1,  1, 81,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1, 82, 53,  1,  1, 83,  1,  1,  1,
     1, 84,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
    85, 86,  1,  1,  1,  1,  1,  1,  1, 87, 88, 89,  1,  1,  1,  1,
     1,  1,  1, 90,  1,  1,  1,  1,  1, 91,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 92,  1,  1,  1,  1,
     1,  1, 93,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1, 90,  1,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_numeric_type_stage_3[] = {
      0,   1,   0,   0,   0,   2,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   3,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   3,   0,
      0,   0,   0,   4,   0,   0,   0,   5,   0,   0,   0,   4,   0,   0,   0,   4,
      0,   0,   0,   6,   0,   0,   0,   7,   0,   0,   0,   8,   0,   0,   0,   4,
      0,   0,   9,  10,   0,   0,   0,   4,   0,   0,   1,   0,   0,   0,   1,   0,
      0,  11,   0,   0,   0,   0,   0,   0,   0,   0,   3,   0,   1,   0,   0,   0,
      0,   0,   0,  12,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  13,
      0,   0,   0,   0,   0,   0,   0,  14,   1,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   4,   0,   0,   0,  15,   0,   0,   0,   0,   0,  16,   0,   0,   0,
      0,   0,   1,   0,   0,   1,   0,   0,   0,   0,  16,   0,   0,   0,   0,   0,
      0,   0,   0,  17,  18,   0,   0,   0,   0,   0,  19,  20,  21,   0,   0,   0,
      0,   0,   0,  22,  23,   0,   0,  24,   0,   0,   0,  25,  26,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  27,  28,  29,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  30,   0,   0,   0,   0,  31,  32,   0,  31,  33,   0,   0,
     34,   0,   0,   0,  35,   0,   0,   0,   0,  36,   0,   0,   0,   0,   0,   0,
      0,   0,  37,   0,   0,   0,   0,   0,  38,   0,  27,   0,  39,  40,  41,  42,
     37,   0,   0,  43,   0,   0,   0,   0,  44,   0,  45,  46,   0,   0,   0,   0,
      0,   0,  47,   0,   0,   0,  48,   0,   0,   0,   0,   0,   0,   0,  49,   0,
      0,   0,   0,   0,   0,   0,   0,  50,   0,   0,   0,  51,   0,   0,   0,  52,
     53,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  54,
      0,   0,  55,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  56,   0,
     45,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  57,   0,   0,   0,
      0,   0,   0,  54,   0,   0,   0,   0,   0,   0,   0,   0,  45,   0,   0,   0,
      0,  55,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  58,   0,   0,
      0,  43,   0,   0,   0,   0,   0,   0,   0,  59,  60,  61,   0,   0,   0,  57,
      0,   3,   0,   0,   0,   0,   0,  62,   0,  63,   0,   0,   0,   0,   1,   0,
      3,   0,   0,   0,   0,   0,   1,   1,   0,   0,   1,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,  64,   0,  56,  65,  27,
     66,  67,  20,  68,  69,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  70,
      0,  71,  72,   0,   0,   0,  73,   0,   0,   0,   0,   0,   0,   3,   0,   0,
      0,   0,  74,  75,   0,  76,   0,  77,  78,   0,   0,   0,   0,  79,  80,  20,
      0,   0,  81,  82,  83,   0,   0,  84,   0,   0,  74,  74,   0,  85,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  86,   0,   1,   0,   0,   0,   0,   0,   0,
      0,   0,   0,  87,   0,   0,   0,   0,  83,  88,  89,   0,   0,   0,   0,   0,
      0,   0,  90,  91,   0,   0,   0,   1,   0,  92,   0,   0,   0,   0,   1,  93,
      0,   0,   1,   0,   0,   0,   3,   0,   0,  94,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  95,   0,   0,  96,  97,   0,   0,   0,   0,
      0,   0,   1,   0,   0,   3,   0,   0,  20,  20,  20,  98,   0,   0,   0,   0,
      0,   0,   0,   3,   0,   0,   0,   0,   0,   0,  99, 100,   0,   0,   0,   0,
      0,   0,   0,   0, 101,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  67,
      0,   0,   0,  68,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 102, 103,
      0,   0,   0,   0,   0,   0,  76,   0,   0,   0,   0,  33,  20, 104,   0,   0,
    105,   0,   0,   0,   0,   0,   0,   0,  59,   0,   0,  44,   0,   0,   0, 106,
      0,  59,   0,   0,   0,   0,   0,   0,   0,  36,   0,   0, 107,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0, 108, 109,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  43,   0,   0,   0,   0,   0,   0,   0,  61,   0,   0,   0,
     49,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  37,   0,   0,   0,   0,
};

static RE_UINT8 re_numeric_type_stage_4[] = {
     0,  0,  0,  0,  0,  0,  1,  2,  0,  0,  3,  4,  1,  2,  0,  0,
     5,  1,  0,  0,  5,  1,  6,  7,  5,  1,  8,  0,  5,  1,  9,  0,
     5,  1,  0, 10,  0,  0,  0, 10,  5,  1, 11, 12,  1, 13, 14,  0,
     0, 15, 16, 17,  0, 18, 12,  0,  1,  2, 11,  7,  0,  0,  1, 19,
     1,  2,  1,  2,  0,  0, 20, 21, 22, 21,  0,  0,  0,  0, 11, 11,
    11, 11, 11, 11, 23,  7,  0,  0, 22, 24, 25, 26, 11, 22, 24, 14,
     0, 27, 28, 29,  0,  0, 30, 31, 22, 32, 33,  0,  0,  0,  0, 34,
    35,  0,  0,  0, 36,  7,  0,  9,  0,  0, 37,  0, 11,  7,  0,  0,
     0, 11, 36, 11,  0,  0, 36, 11, 34,  0,  0,  0, 38,  0,  0,  0,
     0, 39,  0,  0,  0, 34,  0,  0, 40, 41,  0,  0,  0, 42, 43,  0,
     0,  0,  0, 35, 12,  0,  0, 35,  0, 12,  0,  0,  0,  0, 12,  0,
    42,  0,  0,  0, 44,  0,  0,  0,  0, 45,  0,  0, 46, 42,  0,  0,
    47,  0,  0,  0,  0,  0,  0, 38,  0,  0, 41, 41,  0,  0,  0, 39,
     0,  0,  0, 18,  0, 48, 12,  0,  0,  0,  0, 44,  0, 42,  0,  0,
     0,  0, 39,  0,  0,  0, 44,  0,  0, 44, 38,  0, 41,  0,  0,  0,
    44, 42,  0,  0,  0,  0,  0, 12, 18, 11,  0,  0,  0,  0, 49,  0,
     0, 38, 38, 12,  0,  0, 50,  0, 35, 11, 11, 11, 11, 11, 14,  0,
    11, 11, 11, 12,  0, 51,  0,  0, 36, 11, 11, 14, 14,  0,  0,  0,
    41, 39,  0,  0,  0,  0, 52,  0,  0,  0,  0, 11,  0,  0,  0, 36,
    35, 11,  0,  0,  0,  0,  0, 53,  0,  0, 18, 14,  0,  0,  0, 54,
    11, 11,  8, 11, 55, 12,  0,  0,  0,  0,  0, 56,  0,  0,  0, 57,
     0, 53,  0,  0,  0, 36,  0,  0,  0,  0,  0,  8, 22, 24, 11, 10,
    10,  0,  0,  0,  0,  0, 47,  0,  0,  0, 58, 59, 60,  1,  0,  0,
     0,  0,  5,  1, 36, 11, 17,  0,  0,  0,  1, 61,  1, 13,  9,  0,
     0,  0,  1, 13, 11, 17,  0,  0, 11, 10,  0,  0,  0,  0,  1, 62,
     7,  0,  0,  0, 11, 11, 10,  0,  0,  5,  1,  1,  1,  1,  1,  1,
    11, 63, 47,  0, 22, 64,  0,  0, 39,  0,  0,  0, 38, 42,  0, 42,
     0, 39,  0, 34,  0,  0,  0, 41,
};

static RE_UINT8 re_numeric_type_stage_5[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0,
    0, 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3, 3,
    0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 1, 3, 3, 2, 0, 0, 0, 0, 0,
    2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0,
    2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 1, 1, 1,
    2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 2, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2,
    0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
    2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0,
    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
    1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,
    0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0,
    0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0,
    0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 1, 1, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1,
    0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 1, 1, 0, 0, 0, 0,
    3, 3, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
    2, 2, 2, 1, 1, 0, 0, 0,
};

/* Numeric_Type: 2384 bytes. */

RE_UINT32 re_get_numeric_type(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 12;
    code = ch ^ (f << 12);
    pos = (RE_UINT32)re_numeric_type_stage_1[f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_numeric_type_stage_2[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_numeric_type_stage_3[pos + f] << 2;
    f = code >> 3;
    code ^= f << 3;
    pos = (RE_UINT32)re_numeric_type_stage_4[pos + f] << 3;
    value = re_numeric_type_stage_5[pos + code];

    return value;
}

/* Numeric_Value. */

static RE_UINT8 re_numeric_value_stage_1[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 11, 11, 11, 12,
    13, 14, 15, 11, 11, 11, 16, 11, 11, 11, 11, 11, 11, 17, 18, 19,
    20, 11, 21, 22, 11, 11, 23, 11, 11, 11, 11, 11, 11, 11, 11, 24,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
};

static RE_UINT8 re_numeric_value_stage_2[] = {
     0,  1,  1,  1,  1,  1,  2,  3,  1,  4,  5,  6,  7,  8,  9, 10,
    11,  1,  1, 12,  1,  1, 13, 14, 15, 16, 17, 18, 19,  1,  1,  1,
    20, 21,  1,  1, 22,  1,  1, 23,  1,  1,  1,  1, 24,  1,  1,  1,
    25, 26, 27,  1, 28,  1,  1,  1, 29,  1,  1, 30,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 31, 32,
     1, 33,  1, 34,  1,  1, 35,  1, 36,  1,  1,  1,  1,  1, 37, 38,
     1,  1, 39, 40,  1,  1,  1, 41,  1,  1,  1,  1,  1,  1,  1, 42,
     1,  1,  1, 43,  1,  1, 44,  1,  1,  1,  1,  1,  1,  1,  1,  1,
    45,  1,  1,  1, 46,  1,  1,  1,  1,  1,  1,  1, 47, 48,  1,  1,
     1,  1,  1,  1,  1,  1, 49,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1, 50,  1, 51, 52, 53, 54,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1, 55,  1,  1,  1,  1,  1, 15,
     1, 56, 57, 58, 59,  1,  1,  1, 60, 61, 62, 63, 64, 65, 66, 67,
    68, 69, 54,  1,  9,  1, 70, 71, 72,  1,  1,  1, 73, 74,  1,  1,
     1,  1,  1,  1, 75,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 76, 77,  1,  1, 78,  1,
     1,  1, 79, 80,  1,  1,  1, 81,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1, 82, 53,  1,  1, 83,  1,  1,  1,
     1, 84,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
    85, 86,  1,  1,  1,  1,  1,  1,  1, 87, 88, 89,  1,  1,  1,  1,
     1,  1,  1, 90,  1,  1,  1,  1,  1, 91,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 92,  1,  1,  1,  1,
     1,  1, 93,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1, 94,  1,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_numeric_value_stage_3[] = {
      0,   1,   0,   0,   0,   2,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   3,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   3,   0,
      0,   0,   0,   4,   0,   0,   0,   5,   0,   0,   0,   4,   0,   0,   0,   4,
      0,   0,   0,   6,   0,   0,   0,   7,   0,   0,   0,   8,   0,   0,   0,   4,
      0,   0,   9,  10,   0,   0,   0,   4,   0,   0,   1,   0,   0,   0,   1,   0,
      0,  11,   0,   0,   0,   0,   0,   0,   0,   0,   3,   0,   1,   0,   0,   0,
      0,   0,   0,  12,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  13,
      0,   0,   0,   0,   0,   0,   0,  14,   1,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   4,   0,   0,   0,  15,   0,   0,   0,   0,   0,  14,   0,   0,   0,
      0,   0,   1,   0,   0,   1,   0,   0,   0,   0,  14,   0,   0,   0,   0,   0,
      0,   0,   0,  16,   3,   0,   0,   0,   0,   0,  17,  18,  19,   0,   0,   0,
      0,   0,   0,  20,  21,   0,   0,  22,   0,   0,   0,  23,  24,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  25,  26,  27,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  28,   0,   0,   0,   0,  29,  30,   0,  29,  31,   0,   0,
     32,   0,   0,   0,  33,   0,   0,   0,   0,  34,   0,   0,   0,   0,   0,   0,
      0,   0,  35,   0,   0,   0,   0,   0,  36,   0,  37,   0,  38,  39,  40,  41,
     42,   0,   0,  43,   0,   0,   0,   0,  44,   0,  45,  46,   0,   0,   0,   0,
      0,   0,  47,   0,   0,   0,  48,   0,   0,   0,   0,   0,   0,   0,  49,   0,
      0,   0,   0,   0,   0,   0,   0,  50,   0,   0,   0,  51,   0,   0,   0,  52,
     53,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  54,
      0,   0,  55,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  56,   0,
     57,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  58,   0,   0,   0,
      0,   0,   0,  59,   0,   0,   0,   0,   0,   0,   0,   0,  60,   0,   0,   0,
      0,  61,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  62,   0,   0,
      0,  63,   0,   0,   0,   0,   0,   0,   0,  64,  65,  66,   0,   0,   0,  67,
      0,   3,   0,   0,   0,   0,   0,  68,   0,  69,   0,   0,   0,   0,   1,   0,
      3,   0,   0,   0,   0,   0,   1,   1,   0,   0,   1,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,  70,   0,  71,  72,  73,
     74,  75,  76,  77,  78,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  79,
      0,  80,  81,   0,   0,   0,  82,   0,   0,   0,   0,   0,   0,   3,   0,   0,
      0,   0,  83,  84,   0,  85,   0,  86,  87,   0,   0,   0,   0,  88,  89,  90,
      0,   0,  91,  92,  93,   0,   0,  94,   0,   0,  95,  95,   0,  96,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  97,   0,   1,   0,   0,   0,   0,   0,   0,
      0,   0,   0,  98,   0,   0,   0,   0,  99, 100, 101,   0,   0,   0,   0,   0,
      0,   0, 102, 103,   0,   0,   0,   1,   0, 104,   0,   0,   0,   0,   1, 105,
      0,   0,   1,   0,   0,   0,   3,   0,   0, 106,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0, 107,   0,   0, 108, 109,   0,   0,   0,   0,
      0,   0,   1,   0,   0,   3,   0,   0, 110, 111, 112, 113,   0,   0,   0,   0,
      0,   0,   0,   3,   0,   0,   0,   0,   0,   0, 114, 115,   0,   0,   0,   0,
      0,   0,   0,   0, 116,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 117,
      0,   0,   0, 118,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 119, 120,
      0,   0,   0,   0,   0,   0, 121,   0,   0,   0,   0, 122, 123, 124,   0,   0,
    125,   0,   0,   0,   0,   0,   0,   0, 126,   0,   0, 127,   0,   0,   0, 128,
      0, 129,   0,   0,   0,   0,   0,   0,   0, 130,   0,   0, 131,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0, 132, 133,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  63,   0,   0,   0,   0,   0,   0,   0, 134,   0,   0,   0,
    135,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 136,   0,   0,   0,   0,
      0,   0,   0,   0, 137,   0,   0,   0,
};

static RE_UINT8 re_numeric_value_stage_4[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   2,   3,   0,
      0,   0,   0,   0,   4,   0,   5,   6,   1,   2,   3,   0,   0,   0,   0,   0,
      0,   7,   8,   9,   0,   0,   0,   0,   0,   7,   8,   9,   0,  10,  11,   0,
      0,   7,   8,   9,  12,  13,   0,   0,   0,   7,   8,   9,  14,   0,   0,   0,
      0,   7,   8,   9,   0,   0,   1,  15,   0,   0,   0,   0,   0,   0,  16,  17,
      0,   7,   8,   9,  18,  19,  20,   0,   1,   2,  21,  22,  23,   0,   0,   0,
      0,   0,  24,   2,  25,  26,  27,  28,   0,   0,   0,  29,  30,   0,   0,   0,
      1,   2,   3,   0,   1,   2,   3,   0,   0,   0,   0,   0,   1,   2,  31,   0,
      0,   0,   0,   0,  32,   2,   3,   0,   0,   0,   0,   0,  33,  34,  35,  36,
     37,  38,  39,  40,  37,  38,  39,  40,  41,  42,  43,   0,   0,   0,   0,   0,
     37,  38,  39,  44,  45,  37,  38,  39,  44,  45,  37,  38,  39,  44,  45,   0,
      0,   0,  46,  47,  48,  49,   2,  50,   0,   0,   0,   0,   0,  51,  52,  53,
     37,  38,  54,  52,  53,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  55,
      0,  56,   0,   0,   0,   0,   0,   0,  24,   2,   3,   0,   0,   0,  57,   0,
      0,   0,   0,   0,  51,  58,   0,   0,  37,  38,  59,   0,   0,   0,   0,   0,
      0,   0,  60,  61,  62,  63,  64,  65,   0,   0,   0,   0,  66,  67,  68,  69,
      0,  70,   0,   0,   0,   0,   0,   0,  71,   0,   0,   0,   0,   0,   0,   0,
      0,   0,  72,   0,   0,   0,   0,   0,   0,   0,   0,  73,   0,   0,   0,   0,
     74,  75,  76,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  77,
      0,   0,   0,  78,   0,  79,   0,   0,   0,   0,   0,   0,   0,   0,   0,  80,
     81,   0,   0,   0,   0,   0,   0,  82,   0,   0,  83,   0,   0,   0,   0,   0,
      0,   0,   0,  70,   0,   0,   0,   0,   0,   0,   0,   0,  84,   0,   0,   0,
      0,  85,   0,   0,   0,   0,   0,   0,   0,  86,   0,   0,   0,   0,   0,   0,
      0,   0,  87,  88,   0,   0,   0,   0,  89,  90,   0,  91,   0,   0,   0,   0,
     92,  83,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  93,   0,
      0,   0,   0,   0,   5,   0,   5,   0,   0,   0,   0,   0,   0,   0,  94,   0,
      0,   0,   0,   0,   0,   0,   0,  95,   0,   0,   0,  15,  78,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  96,   0,   0,   0,  97,   0,   0,   0,   0,
      0,   0,   0,   0,  98,   0,   0,   0,   0,  98,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,  99,   0,   0,   0,   0,   0,   0,   0,   0,   0, 100,
      0, 101,   0,   0,   0,   0,   0,   0,   0,   0,   0,  28,   0,   0,   0,   0,
      0,   0,   0, 102,  71,   0,   0,   0,   0,   0,   0,   0,  78,   0,   0,   0,
    103,   0,   0,   0,   0,   0,   0,   0,   0, 104,   0,  84,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 105,   0,   0,   0,   0,   0,   0, 106,   0,   0,
      0,  51,  52, 107,   0,   0,   0,   0,   0,   0,   0,   0, 108, 109,   0,   0,
      0,   0, 110,   0, 111,   0,  78,   0,   0,   0,   0,   0, 106,   0,   0,   0,
      0,   0,   0,   0, 112,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 113,
      0, 114,   8,   9,  60,  61, 115, 116, 117, 118, 119, 120, 121,   0,   0,   0,
    122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 125, 134, 135,   0,
      0,   0, 136,   0,   0,   0,   0,   0,  24,   2,  25,  26,  27, 137, 138,   0,
    139,   0,   0,   0,   0,   0,   0,   0, 140,   0, 141,   0,   0,   0,   0,   0,
      0,   0,   0,   0, 142, 143,   0,   0,   0,   0,   0,   0,   0,   0, 144, 145,
      0,   0,   0,   0,   0,   0,  24, 146,   0, 114, 147, 148,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 114, 148,   0,   0,   0,   0,   0, 149, 150,   0,
      0,   0,   0,   0,   0,   0,   0, 151,  37,  38, 152, 153, 154, 155, 156, 157,
    158, 159, 160, 161, 162, 163, 164, 165,  37, 166, 167,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0, 168,   0,   0,   0,   0,   0,   0,   0, 169,
      0,   0, 114, 148,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  37, 166,
      0,   0,  24, 170,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 171, 172,
     37,  38, 152, 153, 173, 155, 174, 175,   0,   0,   0,   0,   0,   0,   0,  24,
    146, 176,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 169,  84,   0,   0,
      0,   0,   0,   0,  51,  52,  53, 177, 178, 179,   8,   9,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   7,   8,   9,  24,   2,  25,  26,  27, 180,   0,   0,
      0,   0,   0,   0,   1,   2,  25,   0,   1,   2,  25,  26, 181,   0,   0,   0,
      0,   0,   0,   0,   1,   2, 182,  52,  53, 177, 178,  84,   0,   0,   0,   0,
      8,   9,  52, 183,  38, 184,   2, 182, 185, 186,   9, 187, 188, 187, 189, 190,
    191, 192, 193, 194, 147, 195, 196, 197, 198, 199, 200, 201,   0,   0,   0,   0,
      0,   0,   0,   0,   1,   2, 202, 203, 204,   0,   0,   0,   0,   0,   0,   0,
      1,   2, 205,  47,  48,  15,   0,   0,   1,   2, 205,  47,  48,   0,   0,   0,
     37,  38, 152, 153, 206, 207, 208,   0,   0,   0,   0,   7,   8,   9,   1,   2,
    209,   8,   9,   1,   2, 209,   8,   9,   0, 114,   8,   9,   0,   0,   0,   0,
      0,   0,   0,   0,  24,   2,  25,  26,  27, 137, 138, 210, 211, 212, 213, 214,
    215,   8,   9, 216, 217, 218,   0,   0, 219,  52, 107,  32,   0,   0,   0,   0,
     73,   0,   0,   0,   0,   0,   0,   0,   0, 220,   0,   0,   0,   0,   0,   0,
    101,   0,   0,   0,   0,   0,   0,   0,  70,   0,   0,   0,   0,   0,   0,   0,
      0,   0,  94,   0,   0,   0,   0,   0, 221,   0,   0,  91,   0,   0,   0,  91,
      0,   0, 104,   0,   0,   0,   0,  76,   0,   0,   0,   0,   0,   0,  76,   0,
      0,   0,   0,   0,   0,   0,  83,   0,   0,   0,   0,   0,   0,   0, 110,   0,
      0,   0,   0, 222,   0,   0,   0,   0,   0,   0,   0,   0, 223,   0,   0,   0,
};

static RE_UINT8 re_numeric_value_stage_5[] = {
      0,   0,   0,   0,   2,  32,  34,  36,  38,  40,  42,  44,  46,  48,   0,   0,
      0,   0,  34,  36,   0,  32,   0,   0,  17,  22,  27,   0,   0,   0,   2,  32,
     34,  36,  38,  40,  42,  44,  46,  48,   7,  11,  15,  17,  27,  55,   0,   0,
      0,   0,  17,  22,  27,   7,  11,  15,  49,  94, 103,   0,  32,  34,  36,   0,
      3,   4,   5,   6,   9,  13,  16,   0,  49,  94, 103,  17,  22,  27,   7,  11,
     15,   0,   0,   0,  46,  48,  22,  33,  35,  37,  39,  41,  43,  45,  47,   1,
      0,  32,  34,  36,  46,  48,  49,  59,  69,  79,  89,  90,  91,  92,  93,  94,
    112,   0,   0,   0,   0,   0,  56,  57,  58,   0,   0,   0,  46,  48,  32,   0,
      2,   0,   0,   0,  12,  10,   9,  18,  26,  16,  20,  24,  28,  14,  29,  11,
     19,  25,  30,  32,  32,  34,  36,  38,  40,  42,  44,  46,  48,  49,  50,  51,
     89,  94,  98, 103, 103, 107, 112,   0,   0,  42,  89, 116, 121,   2,   0,   0,
     52,  53,  54,  55,  56,  57,  58,  59,   0,   0,   2,  50,  51,  52,  53,  54,
     55,  56,  57,  58,  59,  32,  34,  36,  46,  48,  49,   2,   0,   0,  32,  34,
     36,  38,  40,  42,  44,  46,  48,  49,  48,  49,  32,  34,   0,  22,   0,   0,
      0,   0,   0,   2,  49,  59,  69,   0,  36,  38,   0,   0,  48,  49,   0,   0,
     49,  59,  69,  79,  89,  90,  91,  92,   0,  60,  61,  62,  63,  64,  65,  66,
     67,  68,  69,  70,  71,  72,  73,  74,   0,  75,  76,  77,  78,  79,  80,  81,
     82,  83,  84,  85,  86,  87,  88,  89,   0,  40,   0,   0,   0,   0,   0,  34,
      0,   0,  40,   0,   0,  44,   0,   0,  32,   0,   0,  44,   0,   0,   0, 112,
      0,  36,   0,   0,   0,  48,   0,   0,  34,   0,   0,   0,  40,   0,  38,   0,
      0,   0,   0, 135,  49,   0,   0,   0,   0,   0,   0, 103,  36,   0,   0,   0,
     94,   0,   0,   0, 135,   0,   0,   0,   0,   0, 137,   0,   0,  34,   0,  46,
      0,  42,   0,   0,   0,  49,   0, 103,  59,  69,   0,   0,  79,   0,   0,   0,
      0,  36,  36,  36,   0,   0,   0,  38,   0,   0,  32,   0,   0,   0,  48,  59,
      0,   0,  49,   0,  46,   0,   0,   0,   0,   0,  44,   0,   0,   0,  48,   0,
      0,   0,  94,   0,   0,   0,  38,   0,   0,   0,  34,   0,   0, 103,   0,   0,
      0,   0,  42,   0,  42,   0,   0,   0,   0,   0,   2,   0,  44,  46,  48,   2,
     17,  22,  27,   7,  11,  15,   0,   0,   0,   0,   0,  36,   0,   0,   0,  49,
      0,  42,   0,  42,   0,  49,   0,   0,   0,   0,   0,  32,  93,  94,  95,  96,
     97,  98,  99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112,
    113, 114, 115, 116, 117, 118, 119, 120,  17,  22,  32,  40,  89,  98, 107, 116,
     40,  49,  89,  94,  98, 103, 107,  40,  49,  89,  94,  98, 103, 112, 116,  49,
     32,  32,  32,  34,  34,  34,  34,  40,  49,  49,  49,  49,  49,  69,  89,  89,
     89,  89,  94,  96,  98,  98,  98,  98,  89,  22,  22,  26,  27,   0,   0,   0,
      0,   0,   2,  17,  95,  96,  97,  98,  99, 100, 101, 102,  32,  40,  49,  89,
      0,  93,   0,   0,   0,   0, 102,   0,   0,  32,  34,  49,  59,  94,   0,   0,
     32,  34,  36,  49,  59,  94, 103, 112,  38,  40,  49,  59,  34,  36,  38,  38,
     40,  49,  59,  94,   0,   0,  32,  49,  59,  94,  34,  36,  31,  22,   0,   0,
     48,  49,  59,  69,  79,  89,  90,  91,   0,   0,  94,  95,  96,  97,  98,  99,
    100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115,
    116, 117, 118, 119, 120, 121, 122, 124, 125, 127, 128, 129, 130, 131,   8,  14,
     17,  18,  21,  22,  23,  26,  27,  29,  49,  59,  94, 103,  22,   0,   0,   0,
      0,  32,  89,   0,   0,  32,  49,  59,  38,  49,  59,  94,   0,   0,  32,  40,
     49,  89,  94, 103,  92,  93,  94,  95, 100, 101, 102,  22,  17,  18,  26,   0,
     69,  94,  22,   0,  59,  69,  79,  89,  90,  91,  92,  93,  94, 103,   2,  32,
    103,   0,   0,   0,  91,  92,  93,   0,  46,  48,  32,  34,  44,  46,  48,  38,
     48,  32,  34,  36,  36,  38,  40,  34,  36,  36,  38,  40,  32,  34,  36,  36,
     38,  40, 123, 126,  38,  40,  36,  36,  38,  38,  38,  38,  42,  44,  44,  44,
     46,  46,  48,  48,  48,  48,  34,  36,  38,  40,  42,  32,  40,  40,  34,  36,
     32,  34,  18,  26,  29,  18,  26,  11,  17,  14,  17,  17,  22,  18,  26,  79,
     89,  38,  40,  42,  44,  46,  48,   0,  46,  48,   0,  49,  94, 112, 132, 135,
    136, 137,   0,   0,  46,  48,  49,  50,  92,  93,  32,  34,  36,  38,  40,  32,
     40,   0,   0,   0,  46,  48,   2,  32, 103, 104, 105, 106, 107, 108, 109, 110,
    111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 121, 133, 134,  32,
      0,  17,  22,  27,   0,  32,  34, 112, 121,   0,   0,   0,   2,   2,  32,  34,
     38,   0,   0,   0,   0,   0,   0,  69,   0,  38,   0,   0,  48,   0,   0,   0,
};

/* Numeric_Value: 3432 bytes. */

RE_UINT32 re_get_numeric_value(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 12;
    code = ch ^ (f << 12);
    pos = (RE_UINT32)re_numeric_value_stage_1[f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_numeric_value_stage_2[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_numeric_value_stage_3[pos + f] << 3;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_numeric_value_stage_4[pos + f] << 2;
    value = re_numeric_value_stage_5[pos + code];

    return value;
}

/* Bidi_Mirrored. */

static RE_UINT8 re_bidi_mirrored_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_bidi_mirrored_stage_2[] = {
    0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6, 4, 4,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
};

static RE_UINT8 re_bidi_mirrored_stage_3[] = {
     0,  1,  1,  1,  1,  1,  1,  2,  1,  1,  1,  3,  1,  1,  1,  1,
     4,  5,  1,  6,  7,  8,  1,  9, 10,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 11,
     1,  1,  1, 12,  1,  1,  1,  1,
};

static RE_UINT8 re_bidi_mirrored_stage_4[] = {
     0,  1,  2,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,
     3,  3,  3,  3,  4,  3,  3,  3,  3,  3,  5,  3,  3,  3,  3,  3,
     6,  7,  8,  3,  3,  9,  3,  3, 10, 11, 12, 13, 14,  3,  3,  3,
     3,  3,  3,  3,  3, 15,  3, 16,  3,  3,  3,  3,  3,  3, 17, 18,
    19, 20, 21, 22,  3,  3,  3, 23, 24,  3,  3,  3,  3,  3,  3,  3,
    25,  3,  3,  3,  3,  3,  3,  3,  3, 26,  3,  3, 27, 28,  3,  3,
     3,  3,  3, 29, 30, 31, 32, 33,
};

static RE_UINT8 re_bidi_mirrored_stage_5[] = {
      0,   0,   0,   0,   0,   3,   0,  80,   0,   0,   0,  40,   0,   0,   0,  40,
      0,   0,   0,   0,   0,   8,   0,   8,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  60,   0,   0,   0,  24,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   6,  96,   0,   0,   0,   0,   0,   0,  96,
      0,  96,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,
     30,  63,  98, 188,  87, 248,  15, 250, 255,  31,  60, 128, 245, 207, 255, 255,
    255, 159,   7,   1, 204, 255, 255, 193,   0,  62, 195, 255, 255,  63, 255, 255,
      0,  15,   0,   0,   3,   6,   0,   0,   0,   0,   0,   0,   0, 255,  63,   0,
    121,  59, 120, 112, 252, 255,   0,   0, 248, 255, 255, 249, 253, 255,   0,   1,
     63, 194,  55,  31,  58,   3, 240,  51,   0, 252, 255, 223,  83, 122,  48, 112,
      0,   0, 128,   1,  48, 188,  25, 254, 255, 255, 255, 255, 207, 191, 255, 255,
    255, 255, 127,  80, 124, 112, 136,  47,   0,   0,   0,   0,   0,   0,   0,  64,
     60,  54,   0,  48, 255,   3,   0,   0,   0, 255, 243,  15,   0,   0,   0,   0,
      0,   0,   0, 126,  48,   0,   0,   0,   0,   3,   0,  80,   0,   0,   0,  40,
      0,   0,   0, 168,  13,   0,   0,   0,   0,   0,   0,   8,   0,   0,   0,   0,
      0,   0,  32,   0,   0,   0,   0,   0,   0, 128,   0,   0,   0,   0,   0,   0,
      0,   2,   0,   0,   0,   0,   0,   0,   8,   0,   0,   0,   0,   0,   0,   0,
};

/* Bidi_Mirrored: 497 bytes. */

RE_UINT32 re_get_bidi_mirrored(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_bidi_mirrored_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_bidi_mirrored_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_bidi_mirrored_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_bidi_mirrored_stage_4[pos + f] << 6;
    pos += code;
    value = (re_bidi_mirrored_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Indic_Positional_Category. */

static RE_UINT8 re_indic_positional_category_stage_1[] = {
    0, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_indic_positional_category_stage_2[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  2,  3,  4,  5,  6,  7,
     8,  0,  0,  0,  0,  0,  0,  9,  0, 10, 11, 12, 13, 14,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0, 15, 16, 17, 18,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 19,  0,  0,  0,  0,  0,
    20, 21, 22, 23, 24, 25, 26, 27, 28,  0, 29,  0, 30, 31, 32,  0,
};

static RE_UINT8 re_indic_positional_category_stage_3[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   0,   0,   2,   3,   4,   5,   0,   6,   0,   0,   7,   8,   9,   5,  10,
     11,   0,   0,   7,  12,   0,   0,  13,  11,   0,   0,   7,  14,   0,   5,  15,
      6,   0,   0,  16,  17,  18,   5,   0,  19,   0,   0,  20,  21,   9,   0,   0,
     22,   0,   0,  23,  24,  25,   5,   0,   6,   0,   0,  16,  26,  27,   5,   0,
     28,   0,   0,  29,  30,   9,   5,   0,  31,   0,   0,   0,  32,  33,   0,  31,
      0,   0,   0,  34,  35,   0,   0,   0,   0,   0,   0,  36,  37,   0,   0,   0,
      0,  38,   0,  39,   0,   0,   0,  40,  41,  42,  43,  44,  45,   0,   0,   0,
      0,   0,  46,  47,   0,  48,  49,  50,  51,  52,   0,   0,   0,   0,   0,   0,
      0,  53,   0,  53,   0,  54,   0,  54,   0,   0,   0,  55,  56,  57,   0,   0,
      0,   0,  58,  59,   0,   0,   0,   0,   0,   0,   0,  60,  61,   0,   0,   0,
      0,  62,   0,   0,   0,  63,  64,  65,   0,   0,   0,   0,   0,   0,   0,   0,
     66,   0,   0,  67,  68,   0,  69,  70,  71,   0,  72,   0,   0,   0,  73,  28,
      0,   0,  74,  75,   0,   0,   0,   0,   0,   0,   0,   0,   0,  76,  77,  78,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  79,
     80,   0,  81,   0,   0,   0,   0,   0,  82,   0,   0,  83,  84,   0,  85,  86,
      0,   0,  87,   0,  88,  28,   0,   0,   1,   0,   0,  89,  90,   0,  91,   0,
      0,   0,  92,  93,  94,   0,   0,  95,   0,   0,   0,  96,  97,   0,  98,  99,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 100,   0,
    101,   0,   0, 102,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    103,   0,   0, 104, 105,   0,   0,   0,  71,   0,   0, 106,   0,   0,   0,   0,
    107,   0, 108, 109,  27,   0,   0, 110,  71,   0,   0, 111, 112,   0,   0,   0,
      0,   0, 113, 114,   0,   0,   0,   0,   0,   0,   0,   0,   0, 115, 116,   0,
      6,   0,   0, 117, 118,   9, 119, 120,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0, 121, 122,  10,   0,   0,   0,   0,   0, 123, 124,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 125, 126, 127, 128,   0,   0,
      0,   0,   0, 129, 130,   0,   0,   0,   0,   0, 131, 132,   0,   0,   0,   0,
      0, 133, 134,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0, 135, 136,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    137,   0,   0, 138,   0, 139,   0,   0, 140, 141,   0,   0,   0,   0,   0,   0,
      0,   0, 125, 142,   0,   0,   0,   0,   0, 143, 144, 145,   0,   0,   0,   0,
      0,   0,   0, 146, 147,   0,   0,   0, 148, 149,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 150,
};

static RE_UINT8 re_indic_positional_category_stage_4[] = {
      0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   2,   3,   4,   5,   6,   7,
      8,   9,   0,   0,  10,   0,   0,   0,  11,   0,   0,   0,   0,   0,   0,   3,
      4,  12,  13,  14,   0,  15,   0,   0,   0,   0,   0,  16,  17,   0,   0,   0,
     18,  19,  20,  21,  22,  23,   0,   0,   4,  24,  25,  26,   0,   0,  27,  28,
      0,   0,   0,  29,   4,  12,  30,  31,   0,  32,   0,   0,  16,   0,   0,   0,
      0,   0,   0,  33,  34,  35,  36,  37,   6,  38,   0,   0,   0,   0,   0,  27,
      6,  39,  40,  22,   0,  41,   0,   0,  42,  43,  44,  22,   0,  45,   0,   0,
     46,   0,   0,   0,   0,   0,  19,  47,  48,  49,  36,  37,  33,   0,   0,   0,
      0,   0,  16,  15,  50,  51,  52,  53,  54,  28,  55,   0,  56,  57,  28,  58,
     54,  28,  59,  60,  56,  61,  28,  22,   0,   0,  62,   0,   0,  63,  64,  65,
     66,  67,  68,   1,  69,  70,   0,  71,  72,  72,  71,  72,  72,  72,  72,  72,
     72,  72,  72,  60,   0,  73,   0,   0,   0,   0,  15,  74,  75,  76,  77,  78,
      0,  33,  62,  10,  79,  80,  81,  82,  83,  38,   0,   0,  84,  85,  81,  86,
      0,   0,  33,  87,  88,  60,   0,   0,  88,   0,   0,   0,   0,  89,  76,  90,
     91,  92,  93,  28,  94,   0,   0,  64,  95,  96,   6,   0,  97,  81,  98,   0,
     81,  99, 100,  81, 101,   0,  82,   0,   0,  19, 102,   0,   0, 103,  76,  55,
    104,  93, 105, 106, 107,  28,  28, 108,  28, 101,   0,   0,   0, 109, 110, 111,
    112, 101,   0,   0,   0,   0,  19,   5,  28,   0,   0,   0, 113,   0,   0,   0,
    114, 115, 113,  62,   0,   2,  46, 116,   0, 117, 118,   5,  28, 119,   0,   0,
     58, 120, 121,  72, 122, 123, 124,  23,   0, 125,   0,   0,   0,   0,  19,   0,
      0,  16,  19,   0,  15, 126,   0,   0,  82,   0,   0,   0,   0,  81,  81,  81,
     81, 127,   0,   0,  28,  28,  28,  28,  22,   0,   0,  19,   0,   0, 128,  62,
      0, 128, 129, 130,  19,  50, 131, 132, 133,   0,   0,   0,   0,  64,   0,   0,
      0,   0,  83, 134, 135, 136,   0,   0,  19,   0,   0, 137,   0,   0,  15, 137,
    109, 138, 139, 140,  64,   0,   0,   0,   0,   0, 141, 142,   0, 143,   0,   0,
     15,  54, 144,  26, 145, 146,   0, 130,   0,   0, 147,   0, 148,   0,   0,   0,
      0,   0,  28,  72, 121,  58,   0,   0, 149, 150,  18,   0,  58,   0,   0,   0,
      0,  19,   9, 151, 147,  38,   0,   0, 128,   0,   0,   0,  15, 152,  72, 153,
    101,   0, 154,  60,   0,   0,   0,  48, 155, 109,   0,  16,   0,   0,   0,  19,
    149,   5, 147,   0,   0,   0, 128,  79,   6, 156,  13, 157,  33,  27,  28,  38,
     28,  38,   0,   0,   0, 158,  72, 121, 159, 160,   0,   0, 149,  72, 161, 162,
    163,   0,   0,   0,   0,   0,   0,  15, 152,  62, 164, 165,  60,   0,   0,   0,
      0,   0,   0,  62,  48,  72, 150, 166,  38,   0,   0,   0,   0,   0,  19, 167,
    121, 165,   0,   0,   0,   0,   0, 154,  50, 168,   5,   0,   0,   0,   0, 149,
    130,  28,  18,   0, 169,  28, 170,   0, 128,   5, 171,  55, 169,   1,   4,   0,
      0,   0,  10,  72,  72, 172,  38,   0,   9,  55,  28, 165,  10,  72,  72,  72,
     72,  72, 114,  72, 173, 174,   0,   0,  83, 170,  16,  94, 175, 176,   0,   0,
      0,   0,  33, 177, 178, 148,   0,   0,  19, 179,   0,   0,
};

static RE_UINT8 re_indic_positional_category_stage_5[] = {
     0,  0,  0,  0,  5,  5,  5,  1,  0,  0,  5,  1,  6,  0,  1,  2,
     1,  6,  6,  6,  6,  5,  5,  5,  5,  1,  1,  1,  1,  6,  2,  1,
     0,  5,  6,  5,  5,  5,  6,  6,  0,  0,  6,  6,  0,  5,  1,  1,
     6,  0,  0,  2,  2,  0,  0,  4,  4,  6,  0,  0,  0,  0,  0,  1,
     0,  0,  5,  0,  0,  5,  5,  1,  1,  6,  6,  0,  0,  0,  0,  5,
     5,  0,  0,  5,  5,  6,  0,  0,  5,  5,  0,  0,  0,  6,  0,  0,
     6,  5,  0,  5,  5,  8,  0,  1,  1,  6,  0,  0,  0,  0,  5,  5,
     5,  5,  5,  5,  6,  0,  1,  5,  9,  0,  0,  4, 10,  6,  0,  0,
     0,  0,  5,  8,  0,  0,  1,  1,  5,  1,  1,  0,  0,  0,  2,  2,
     2,  0,  4,  4,  4,  5,  0,  0,  5,  0,  0,  0,  1,  0,  5,  5,
     7,  0,  5,  5,  0,  5,  6,  0,  8,  1,  1,  1,  1,  0,  5,  8,
     8,  0,  8,  8,  0,  1,  1,  0,  5,  5,  1,  1,  5,  0,  1,  1,
     1,  1,  1,  6,  6,  0,  2,  2,  1,  1,  5,  5,  6,  0,  6,  0,
     1,  2,  9,  2,  4, 10,  4,  1,  1,  5,  1,  1,  6,  6,  6,  0,
     3,  3,  3,  3,  3,  1,  0,  5,  5,  5,  5,  0,  6,  6,  0,  5,
     6,  0,  0,  0,  3,  0,  0,  0,  6,  6,  0,  0,  0,  6,  0,  6,
     0,  5,  0,  0,  0,  0,  1,  2,  0,  6,  5,  7,  6,  6,  7,  7,
     7,  7,  5,  5,  5,  7,  5,  5,  6,  0,  5,  5,  0,  6,  6,  6,
     6,  6,  6,  6,  0,  0,  6,  0,  1,  5,  5,  6,  6,  2,  5,  5,
     5,  5,  5,  6,  1,  0,  5,  1,  0,  6,  6,  0,  6,  0,  1,  1,
     1,  0,  0,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  5,  5,  5,
     0,  0,  6,  1,  2,  5,  5,  1,  1,  6,  0,  1,  1,  5,  0,  0,
     0,  0,  5,  6,  0,  0,  1,  5,  6,  6,  9, 10,  4,  2,  2,  2,
     4,  4,  5,  1,  1,  5,  5,  5,  5,  5,  0,  5,  5,  5,  6,  1,
     1,  8,  8,  5,  1,  1,  6,  1,  1,  6,  5,  6,  1,  3,  3,  3,
     1,  1,  3,  1,  1,  0,  0,  0,  6,  2,  1,  5,  0,  2,  6,  1,
     0,  1,  5,  1,  5,  6,  6,  5,  6,  1,  2,  2,  2,  2,  2,  5,
     5,  0,  0,  6,  5,  1,  5,  5,  6,  6,  6, 11,  7, 13,  2,  2,
     4,  4,  5,  8,  5,  5,  1,  0,  0,  1,  6,  6,  5,  6,  2,  1,
     1,  5,  1,  5,  1,  1,  1,  2,  2,  9,  1,  1,  2,  2,  5,  6,
    14,  6,  6,  6,  6,  6,  5,  5,  5,  1, 14, 14, 14, 14, 14, 14,
    14,  0,  0,  0,  5,  0,  0,  1,  1,  6,  5,  1,  6,  5,  0,  0,
     0,  0,  0,  6,  6,  6,  5,  6,  6,  6,  6,  5,  6,  6,  2,  2,
     5,  1,  1, 12, 11,  0,  0,  0,  5,  6,  5,  2,  2,  5,  6,  1,
     2,  6,  6,  0,  5,  1,  0,  0,  6,  3,  3,  5,  5,  3,  1,  3,
     3,  1,  5,  5,  0,  0,  0,  2,  6,  5,  2,  1,  0,  1,  0,  0,
     6,  1,  1,  0,  0, 14,  6,  6,  0,  5, 14,  0,  5,  6,  6,  0,
     1,  5,  1,  0,  1,  2,  1,  6,  6,  5,  5,  1,  2,  5,  7,  7,
     2,  1,  6,  6,  5,  5,  5,  8,  0,  6,  0,  5,  5,  5,  8,  8,
     1,  0,  0,  2,  4,  1,  0,  0,  0,  1,  2,  1,  1,  1,  6,  5,
     5,  1,  6,  0,  6,  2,  5,  9,  4,  1,  4,  5,  5,  1,  6,  6,
     2,  9,  4, 10,  5,  5,  1,  6,  1,  5,  1,  6,  1,  5,  2,  1,
     6,  6,  2,  5,  0,  5,  6,  6,  5,  5,  6,  0,  5,  1,  0,  6,
     6,  6,  5,  1,  6,  2,  6,  5,  1,  5,  5,  0,  5,  5,  6,  5,
     6,  0,  0,  6,  1,  1,  1,  0,  5,  5,  0,  1,  6,  2,  1,  0,
};

/* Indic_Positional_Category: 2116 bytes. */

RE_UINT32 re_get_indic_positional_category(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 13;
    code = ch ^ (f << 13);
    pos = (RE_UINT32)re_indic_positional_category_stage_1[f] << 5;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_indic_positional_category_stage_2[pos + f] << 4;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_indic_positional_category_stage_3[pos + f] << 2;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_indic_positional_category_stage_4[pos + f] << 2;
    value = re_indic_positional_category_stage_5[pos + code];

    return value;
}

/* Indic_Syllabic_Category. */

static RE_UINT8 re_indic_syllabic_category_stage_1[] = {
    0, 1, 2, 2, 2, 3, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2,
};

static RE_UINT8 re_indic_syllabic_category_stage_2[] = {
     0,  1,  1,  1,  1,  1,  1,  1,  1,  2,  3,  4,  5,  6,  7,  8,
     9,  1,  1,  1,  1,  1,  1, 10,  1, 11, 12, 13, 14, 15,  1,  1,
    16,  1,  1,  1,  1, 17,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1, 18, 19, 20, 21,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 22,  1,  1,  1,  1,  1,
    23, 24, 25, 26, 27, 28, 29, 30, 31,  1, 32,  1, 33, 34, 35,  1,
};

static RE_UINT8 re_indic_syllabic_category_stage_3[] = {
      0,   0,   1,   2,   0,   0,   0,   0,   0,   0,   3,   4,   0,   5,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      6,   7,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  12,  20,
     21,  15,  16,  22,  23,  24,  25,  26,  27,  28,  16,  29,  30,   0,  12,  31,
     32,  15,  16,  29,  33,  34,  12,  35,  36,  37,  38,  39,  40,  41,  25,   0,
     42,  43,  16,  44,  45,  46,  12,   0,  47,  43,  16,  48,  45,  49,  12,  50,
     51,  43,   8,  52,  53,  54,  12,  55,  56,  57,   8,  58,  59,  60,  25,  61,
     62,   8,  63,  64,  65,   2,   0,   0,  66,  67,  68,  69,  70,  71,   0,   0,
      0,   0,  72,  73,  74,   8,  75,  76,  77,  78,  79,  80,  81,   0,   0,   0,
      8,   8,  82,  83,  84,  85,  86,  87,  88,  89,   0,   0,   0,   0,   0,   0,
     90,  91,  92,  91,  92,  93,  90,  94,   8,   8,  95,  96,  97,  98,   2,   0,
     99,  63, 100, 101,  25,   8, 102, 103,   8,   8, 104, 105, 106,   2,   0,   0,
      8, 107,   8,   8, 108, 109, 110, 111,   2,   2,   0,   0,   0,   0,   0,   0,
    112,  92,   8, 113, 114,   2,   0,   0, 115,   8, 116, 117,   8,   8, 118, 119,
      8,   8, 120, 121, 122,   0,   0,   0,   0,   0,   0,   0,   0, 123, 124, 125,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 126,
    127, 128,   0,   0,   0,   0,   0, 129, 130,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 131,   0,   0,   0,
    132,   8, 133,   0,   8, 134, 135, 136, 137, 138,   8, 139, 140,   2, 141, 142,
    143,   8, 144,   8, 145, 146,   0,   0, 147,   8,   8, 148, 149,   2, 150, 151,
    152,   8, 153, 154, 155,   2,   8, 156,   8,   8,   8, 157, 158,   0, 159, 160,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 161, 162, 163,   2,
    164, 165,   8, 166, 167,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    168,  92,   8, 169, 170, 171, 172, 173, 174,   8,   8, 175,   0,   0,   0,   0,
    176,   8, 177, 178, 179, 180,   8, 181, 182, 183,   8, 184, 185,   2, 186, 187,
    188, 189, 190, 191,   0,   0,   0,   0, 192, 193, 194, 195,   8, 196, 197,   2,
    198,  15,  16, 199,  33, 200, 201, 202,   0,   0,   0,   0,   0,   0,   0,   0,
    203,   8,   8, 204, 205, 206,   0,   0, 207,   8,   8, 208, 209,   2,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0, 203,   8, 210, 211, 212, 213,   0,   0,
    203,   8,   8, 214, 215,   2,   0,   0, 195,   8, 216, 217,   2,   0,   0,   0,
      8, 218, 219, 220,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    195,   8, 190, 221,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    222,   8,   8, 223, 224, 225,   8,   8, 226, 227,   0,   0,   0,   0,   0,   0,
    228,   8, 210, 229, 230,  72, 231, 232,   8, 233,  78, 234,   0,   0,   0,   0,
    235,   8,   8, 236, 237,   2, 238,   8, 239, 240,   2,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   8, 241,
};

static RE_UINT8 re_indic_syllabic_category_stage_4[] = {
      0,   0,   0,   0,   0,   0,   0,   1,   2,   2,   3,   0,   4,   0,   0,   0,
      5,   0,   0,   0,   0,   6,   0,   0,   7,   8,   8,   8,   8,   9,  10,  10,
     10,  10,  10,  10,  10,  10,  11,  12,  13,  13,  13,  14,  15,  16,  10,  10,
     17,  18,   2,   2,  19,   8,  10,  10,  20,  21,   8,  22,  22,   9,  10,  10,
     10,  10,  23,  10,  24,  25,  26,  12,  13,  27,  27,  28,   0,  29,   0,  30,
     26,   0,   0,  31,  32,  21,  33,  34,  23,  35,  26,  36,  37,  29,  27,  38,
     39,   0,  40,  24,   0,  18,   2,   2,  41,  42,   0,   0,  32,  21,   8,  43,
     43,   9,  10,  10,  23,  40,  26,  12,  13,  44,  44,  38,   0,   0,  45,  46,
     32,  21,   8,  22,  13,  27,  27,  38,   0,  47,   0,  30,  48,   0,   0,   0,
     49,  21,  33,  19,  50,  51,  35,  23,  52,  53,  54,  25,  10,  10,  26,  47,
     37,  47,  55,  38,   0,  29,   0,   0,   7,  56,   8,  50,  50,   9,  10,  10,
     10,  10,  26,  57,  13,  55,  55,  38,   0,  58,  54,   0,  32,  21,   8,  50,
     10,  40,  26,  12,   0,  58,   0,  59,  60,   0,   0,   0,   7,  21,   8,  50,
     10,  10,  61,  62,  13,  55,  55,  63,   0,  64,   0,  34,   0,   0,  65,  66,
     67,  21,   8,   8,   8,  33,  25,  10,  30,  10,  10,  48,  10,  54,  68,  29,
     13,  69,  13,  13,  47,   0,   0,   0,  40,  10,  10,  10,  10,  10,  10,  54,
     13,  13,  70,   0,  13,  44,  71,  72,  35,  73,  24,  48,   0,  10,  40,  10,
     40,  74,  25,  35,  13,  13,  44,  75,  13,  76,  71,  77,   2,   2,   3,  10,
      2,   2,   2,   2,   2,  78,  79,   0,  10,  10,  40,  10,  10,  10,  10,  53,
     16,  13,  13,  80,  81,  82,  83,  84,  85,  85,  86,  85,  85,  85,  85,  85,
     85,  85,  85,  87,   0,  88,   0,   0,  89,   8,  90,  13,  13,  91,  92,  93,
      2,   2,  94,  95,  96,  17,  97,  98,  99, 100, 101, 102, 103, 104,  10,  10,
    105, 106,  71, 107,   2,   2, 108, 109, 110,  10,  10,  23,  11, 111,   0,   0,
    110,  10,  10,  10,  11,   0,   0,   0, 112,   0,   0,   0, 113,   8,   8,   8,
      8,  47,  13,  13,  13,  80, 114, 115, 116,   0,   0, 117, 118,  10,  10,  10,
     13,  13, 119,   0, 120, 121, 122,   0, 123, 124, 124, 125, 126, 127,   0,   0,
     10,  10,  10,   0,  13,  13,  13,  13, 128, 121, 129,   0,  10, 130,  13,   0,
     10,  10,  10,  89, 110, 131, 132, 133, 134,  13,  13,  13,  13, 135, 136, 137,
    138, 139,   8,   8,  10, 140,  13,  13,  13, 141,  10,   0, 142,   8, 143,  10,
    144,  13, 145, 146,   2,   2, 147, 148,  10, 149,  13,  13, 150,   0,   0,   0,
     10, 151,  13, 128, 121, 152,   0,   0,   2,   2,   3,  40, 153, 154, 154, 154,
    155,   0,   0,   0, 156, 157, 155,   0,   0,   0, 158,   0,   0,   0,   0, 159,
    160,   4,   0,   0,   0, 161,   0,   0,   5, 161,   0,   0,   0,   0,   0,   4,
     43, 162, 163,  10, 130,  13,   0,   0,  10,  10,  10, 164, 165, 166, 167,  10,
    168,   0,   0,   0, 169,   8,   8,   8, 143,  10,  10,  10,  10, 170,  13,  13,
     13, 171,   0,   0, 154, 154, 154, 154, 172,   0,   0, 173,   2,   2, 174,  10,
    164, 124, 175, 129,  10, 130,  13, 176, 177,   0,   0,   0, 178,   8,   9, 110,
    179,  13,  13, 180, 181,   0,   0,   0,  10, 182,  10,  10,   2,   2, 174,  54,
      8, 143,  10,  10,  10,  10, 103,  13, 183, 184,   0,   0, 121, 121, 121, 185,
     40, 186, 187, 102,  13,  13,  13, 106, 188,   0,   0,   0, 143,  10, 130,  13,
      0, 189,   0,   0,  10,  10,  10,  96, 190,  10, 191, 121, 192,  13,  37, 193,
    103,  58,   0,  80,  10,  40,  40,  10,  10,  26, 194, 195,   2,   2, 196,   0,
    197, 198,   8,   8,  10,  10,  13,  13,  13, 199,   0,   0, 200, 201, 201, 201,
    201, 202,   2,   2,   0,   0,   0, 203, 204,   8,   8,   9,  13,  13, 205,   0,
    204, 110,  10,  10,  10, 130,  13,  13, 206, 207,   2,   2,   0, 208,   0,   0,
    124, 209,  10,  10, 179,   0,   0,   0, 204,   8,   8,   8,   9,  10,  10,  10,
    130,  13,  13,  13, 210,   0, 211,  76, 212,   2,   2,   2,   2, 196,   0,   0,
      8,   8,  10,  10,  30,  10,  10,  10,  10,  10,  10,  13,  13, 213,   0, 214,
      8,  54,  23,  30,  10,  10,  10,  30,  10,  10,  53,   0,   8,   8, 143,  10,
     10,  10,  10, 163,  13,  13, 215,   0,   7,  21,   8,  22,  23,  40, 216,  12,
      0,  29,   0, 217,  17, 218, 154, 219, 154, 219,   0,   0,   8,   8,   8, 143,
     10, 103,  13,  13, 220, 221,   0,   0,   2,   2,   3,  88,  21,   8,   8, 110,
     13,  13,  13, 222, 223, 224,   0,   0,  10,  10,  10, 130,  13, 109,  13, 225,
    226,   0,   0,   0,   0,   0,   8, 109,  13,  13,  13, 227,  76,   0,   0,   0,
     10,  10, 163, 228,  13, 229,   0,   0,  10,  10,  54, 230,  13,  13, 231,   0,
      2,   2,   2,   0,  13, 222, 232,   0, 233,  13, 234,  10, 235, 236, 237, 238,
      0, 239,   0,   0, 233,  13,  13,  10,  10, 240, 241, 121, 121, 242, 243, 244,
      8,   8,  50, 143,  13,  37,  13, 225, 224,   0,   0,   0,   2,   2,   2, 196,
     25,  10,  10,  10, 245,  85,  85,  85,  13, 246,   0,   0,   8,  33,  43,  10,
    103,  37, 247,  44, 248, 249,   0,   0,   8,  43,  50,  10,  10,  10,  11,  37,
     44, 250,   0,   0, 251,  37,   0,   0,
};

static RE_UINT8 re_indic_syllabic_category_stage_5[] = {
     0,  0,  0,  0,  0, 11,  0,  0, 34, 34, 34, 34, 34, 34,  0,  0,
    11,  0,  0,  0,  0,  0, 29, 29,  0,  0,  0, 11,  1,  1,  1,  2,
     8,  8,  8,  8,  8, 12, 12, 12, 12, 12, 12, 12, 12, 12,  9,  9,
     4,  3,  9,  9,  9,  9,  9,  9,  9,  5,  9,  9,  0, 27, 27,  0,
     0,  9,  9,  9,  8,  8,  9,  9,  0,  0, 34, 34,  0,  0,  8,  8,
    11,  1,  1,  2,  0,  8,  8,  8,  8,  0,  0,  8, 12,  0, 12, 12,
    12,  0, 12,  0,  0,  0, 12, 12, 12, 12,  0,  0,  9,  0,  0,  9,
     9,  5, 13,  0,  0,  0,  0,  9, 12, 12,  0, 12,  1,  0, 29,  0,
     0,  1,  1,  2,  8,  8,  8,  0,  0,  0,  0,  8,  0, 12, 12,  0,
     4,  0,  9,  9,  9,  9,  9,  0,  9,  5,  0,  0,  0, 27,  0,  0,
     0, 12, 12, 12,  1, 26, 11, 11,  0, 20,  0,  0,  8,  8,  0,  8,
     9,  9,  0,  9,  0, 12, 27, 27, 27,  4,  4,  4,  0,  0,  9,  9,
     0, 12,  0,  0,  0,  0,  1, 23,  8,  0,  8,  8,  8, 12,  0,  0,
     0,  0,  0, 12, 12,  0,  0,  0, 12, 12, 12,  0,  9,  0,  9,  9,
     1,  8,  8,  8,  0,  3,  9,  9,  0,  9,  9,  0,  0,  0, 12,  0,
     0, 14, 14,  0, 12, 12, 12,  6,  6,  3,  9,  9,  9,  5, 16,  0,
    13, 13, 13,  9,  0,  0, 13, 13, 13, 13, 13, 13,  0,  0,  1,  2,
     0,  0,  5,  0,  9,  0,  9,  0,  9,  9,  6,  0, 25, 25, 25, 25,
    30,  1,  6,  0, 12,  0,  0, 12,  0, 12,  0, 12, 20, 20,  0,  0,
     9,  0,  0,  0,  0,  1,  0,  0,  0, 29,  0, 29,  0,  4,  0,  0,
     9,  9,  1,  2,  9,  9,  1,  1,  6,  3,  0,  0, 22, 22, 22, 22,
    22, 19, 19, 19, 19, 19, 19, 19,  0, 19, 19, 19, 19,  0,  0,  0,
     0,  0, 29,  0, 12,  8,  8,  8,  8,  8,  8,  9,  9,  9,  1, 25,
     2,  7,  6, 20, 20, 20, 20, 12, 34, 34,  0, 11,  0,  0, 11,  0,
    12, 12,  8,  8,  9,  9, 12, 12, 12, 12, 20, 20, 20, 12,  9, 25,
    25, 12, 12,  9,  9, 25, 25, 25, 25, 25, 12, 12, 12,  9,  9,  9,
     9, 12, 12, 12, 12, 12, 20,  9,  9,  9,  9, 25, 25, 25, 12, 25,
    34, 34, 25, 25,  9,  9,  0,  0,  8,  8,  8, 12,  6,  0,  0,  0,
    12,  0,  9,  9, 12, 12, 12,  8,  9, 28, 28, 29, 18, 30, 29, 29,
    29,  6,  7, 29,  3, 29,  0,  0, 11, 12, 12, 12,  9, 19, 19, 19,
    21, 21,  1, 21, 21, 21, 21, 21, 21, 21,  9, 29, 12, 12, 12, 10,
    10, 10, 10, 10, 10, 10,  0,  0, 24, 24, 24, 24, 24,  0,  0,  0,
     9, 21, 21, 21, 25, 25,  0,  0, 12, 12, 12,  9, 12, 20, 20, 19,
    21, 21, 17, 19, 19, 19, 19,  0,  7,  9,  9,  9,  1, 25, 25, 25,
    25, 25,  6, 29, 29,  0,  0, 29,  1,  1,  1, 18,  2,  8,  8,  8,
     4,  9,  9,  9,  5, 12, 12, 12,  1, 18,  2,  8,  8,  8, 12, 12,
    12, 19, 19, 19,  9,  9,  6,  7, 19, 19, 12, 12, 34, 34,  3, 12,
    12, 12, 21, 21,  8,  8,  4,  9, 21, 21,  6,  6, 19, 19,  9,  9,
     1,  1, 29,  4, 27, 27, 27,  0, 27, 27, 27, 27, 27, 27,  0,  0,
     0,  0,  2,  2, 27, 14, 14, 27,  0,  0,  0, 29, 31, 32,  0,  0,
    11, 11, 11, 11, 29,  0,  0,  0,  8,  8,  6, 12, 12, 12, 12,  1,
    12, 12, 10, 10, 10, 10, 12, 12, 12, 12, 10, 19, 19, 12, 12, 12,
    12, 19, 12,  1,  1,  2,  8,  8, 20,  9,  9,  9,  5,  1,  0,  0,
    27, 27,  1,  1,  0,  0,  8,  9, 34, 34, 12, 12, 10, 10, 10, 25,
     9,  9,  9, 21, 21, 21, 21,  6,  1,  1, 18,  2, 12, 12, 12,  4,
     9, 19, 20, 20,  5,  0,  0,  0, 12,  9,  0, 12,  9,  9,  9, 20,
    20, 20, 20,  0, 21, 21,  0,  0, 11, 11, 11,  0,  0,  0, 12, 25,
    24, 25, 24,  0,  0,  2,  7,  0, 12,  8, 12, 12, 12, 12, 12, 21,
    21, 21, 21,  9, 25,  6,  0,  0,  4,  4,  4,  0,  0,  0,  0,  7,
    34,  0,  0,  0,  1,  1,  2, 14, 14,  8,  8,  8,  9,  9,  5,  0,
     0,  0, 35, 35, 35, 35, 35, 35, 35, 35, 34, 34,  0,  0,  0, 33,
     1,  1,  2,  8,  9,  5,  4,  0,  9,  9,  9,  7,  6,  0, 34, 34,
    12,  9,  9,  0, 10, 12, 12, 12,  5,  3, 15, 15,  0, 29,  4,  9,
     0, 34, 34, 34,  1,  5,  4, 26,  0,  0, 27,  0,  9,  4,  6,  0,
    12, 12,  0,  4,  0,  0,  1,  1,  0,  0, 27, 27, 27,  0,  0,  0,
     9,  9,  5,  1,  1,  2,  4,  3,  9,  9,  9,  1,  1,  2,  5,  4,
     3,  0,  0,  0,  1,  1,  2,  5,  4,  0,  0,  0,  9,  1,  2,  5,
     2,  9,  9,  9,  9,  9,  5,  4,  0, 20, 20, 20,  9,  9,  9,  6,
     2,  5,  4,  0,  8,  9,  9,  9,  9,  9,  9, 12, 12, 12, 12, 29,
     6,  1,  1,  1,  1,  2, 15, 20, 20, 20, 20, 11,  0, 11,  0,  7,
     0,  0, 15, 15, 15, 15, 21, 21, 21, 21,  1,  2, 26,  7,  0,  0,
     0,  3,  0,  0,  0,  0, 19, 19,  9,  1,  1,  0,  0,  0,  9,  0,
     1,  2,  4,  9,  6,  7, 16, 20,  9,  1,  2,  7, 12, 12, 11,  9,
};

/* Indic_Syllabic_Category: 2848 bytes. */

RE_UINT32 re_get_indic_syllabic_category(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 13;
    code = ch ^ (f << 13);
    pos = (RE_UINT32)re_indic_syllabic_category_stage_1[f] << 5;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_indic_syllabic_category_stage_2[pos + f] << 4;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_indic_syllabic_category_stage_3[pos + f] << 2;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_indic_syllabic_category_stage_4[pos + f] << 2;
    value = re_indic_syllabic_category_stage_5[pos + code];

    return value;
}

/* Emoji. */

static RE_UINT8 re_emoji_stage_1[] = {
    0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1,
};

static RE_UINT8 re_emoji_stage_2[] = {
    0, 1, 1, 1, 2, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 6,
};

static RE_UINT8 re_emoji_stage_3[] = {
     0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     2,  3,  1,  4,  5,  6,  7,  8,  1,  9,  1, 10,  1,  1,  1,  1,
    11,  1, 12,  1,  1,  1,  1,  1, 13, 14, 15, 16, 17, 18, 19,  1,
     1, 20,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_emoji_stage_4[] = {
     0,  1,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  3,  4,  0,  0,  0,  0,  0,  0,  5,  0,  0,  6,  7,  0,  0,
     8,  9,  0,  0,  0,  0, 10, 11,  0,  0,  0,  0,  0,  0, 12,  0,
     0,  0,  0,  0,  0, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
    24, 25, 26, 27, 28, 29,  0,  0,  0, 30,  0,  0,  0,  0,  0,  0,
    31,  0, 32,  0,  0,  0,  0,  0,  0, 33,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0, 34,  0,  0,  0, 35,  0,  0,  0,  0,  0, 10,  0,
     0,  0,  0, 36, 37,  0,  0, 38, 39, 40, 41,  0,  0,  0,  0,  0,
    42, 43, 42, 42, 44, 42, 42, 45, 42, 42, 42, 42, 42, 42, 42, 46,
    42, 47, 48, 49, 50, 51, 52, 53, 42, 42, 54,  0, 42, 42, 55, 56,
    57, 58, 59, 60, 42, 61, 62, 42,
};

static RE_UINT8 re_emoji_stage_5[] = {
      0,   0,   0,   0,   8,   4, 255,   3,   0,  66,   0,   0,   0,   0,   0,  16,
      0,   2,   0,   0,   4,   0,   0,   2,   0,   0, 240,   3,   0,   6,   0,   0,
      0,   0,   0,  12,   0,   1,   0,   0,   0, 128,   0,   0,   0, 254,  15,   7,
      4,   0,   0,   0,   0,  12,  64,   0,   1,   0,   0,   0,   0,   0,   0, 120,
     31,  64,  50,  33,  77, 196,   0,   7,   5, 255,  15, 128, 105,   1,   0, 200,
      0,   0, 252,  26,   3,  12,   3,  96,  48, 193,  26,   0,   0,   6, 191,  39,
     36, 191,  84,  32,   2,   1,  24,   0, 144,  80, 184,   0,  24,   0,   0,   0,
      0,   0, 224,   0,   2,   0,   1, 128,   0,   0,  48,   0, 224,   0,   0,  24,
      0,   0,  33,   0,   0,   0,   1,  32,   0,   0, 128,   2,  16,   0,   0,   0,
      0,   0,   3, 192,   0,  64, 254,   7, 192, 255, 255, 255,   6,   0,   0,   4,
      0, 128, 252,   7,   0,   0,   3,   0, 255, 255, 255, 255, 243, 255, 255, 255,
    255, 255, 207, 206, 255, 255, 185, 255, 255, 255, 255, 191, 255, 255, 255,  63,
      0, 126, 255, 255, 255, 128, 249,   7, 128,  60,  97,   0,  48,   1,   6,  16,
     28,   0,  14, 112,  10, 129,   8, 252, 255, 255,   0,   0,  63, 248,   7,   0,
     63,  26, 249,   3,   0,   0, 255, 255, 255, 255, 255, 119, 191, 255, 255, 255,
    255, 255, 121, 244,   7,   0, 255,   3,   7,   0, 255, 255,
};

/* Emoji: 558 bytes. */

RE_UINT32 re_get_emoji(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_emoji_stage_1[f] << 4;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_emoji_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_emoji_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_emoji_stage_4[pos + f] << 5;
    pos += code;
    value = (re_emoji_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Emoji_Presentation. */

static RE_UINT8 re_emoji_presentation_stage_1[] = {
    0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1,
};

static RE_UINT8 re_emoji_presentation_stage_2[] = {
    0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 2,
};

static RE_UINT8 re_emoji_presentation_stage_3[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  1,  0,  2,  3,  4,  0,  0,  0,  5,  0,  0,  0,  0,
     6,  7,  8,  9, 10, 11, 12,  0,  0, 13,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_emoji_presentation_stage_4[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  2,
     0,  0,  0,  0,  0,  0,  0,  3,  4,  0,  5,  6,  7,  8,  9, 10,
    11, 12, 13,  0, 14, 15,  0,  0, 16,  0, 17,  0,  0,  0,  0,  0,
    18,  0,  0,  0,  0,  0, 19,  0,  0,  0,  0,  0, 20,  0,  0, 21,
    22, 23, 24,  0,  0,  0,  0,  0, 25, 26, 25, 27, 28, 25, 29, 30,
    25, 31, 32, 25, 25, 25, 25, 33, 25, 34, 35, 36, 37, 18,  0, 38,
    25, 25, 39,  0, 25, 25, 40, 41, 42, 43, 44, 45, 25, 46, 47, 25,
};

static RE_UINT8 re_emoji_presentation_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,  12,   0,  30,   9,   0,   0,   0,   0,  96,
      0,   0,  48,   0,   0, 255,  15,   0,   0,   0,   0, 128,   0,   0,   8,   0,
      2,  12,   0,  96,  48,  64,  16,   0,   0,   4,  44,  36,  32,  12,   0,   0,
      0,   1,   0,   0,   0,  80, 184,   0,   0,   0, 224,   0,   0,   0,   1, 128,
      0,   0,   0,  24,   0,   0,  33,   0,  16,   0,   0,   0,   0, 128,   0,   0,
      0,  64, 254,   7, 192, 255, 255, 255,   2,   0,   0,   4,   0, 128, 124,   7,
      0,   0,   3,   0, 255, 255, 255, 255,   1, 224, 191, 255, 255, 255, 255, 223,
    255, 255,  15,   0, 255, 135,  15,   0, 255, 255,  17, 255, 255, 255, 255, 127,
    253, 255, 255, 255, 255, 255, 255, 159, 255, 255, 255,  63,   0, 120, 255, 255,
    255,   0,   0,   4,   0,   0,  96,   0,   0,   0,   0, 248, 255, 255,   0,   0,
     63,  16,   7,   0,   0,  24, 240,   3,   0,   0, 255, 255, 255, 255, 255, 119,
    191, 255, 255, 255, 255, 255, 121, 244,   7,   0, 255,   3,   7,   0, 255, 255,
};

/* Emoji_Presentation: 410 bytes. */

RE_UINT32 re_get_emoji_presentation(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_emoji_presentation_stage_1[f] << 3;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_emoji_presentation_stage_2[pos + f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_emoji_presentation_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_emoji_presentation_stage_4[pos + f] << 5;
    pos += code;
    value = (re_emoji_presentation_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Emoji_Modifier. */

static RE_UINT8 re_emoji_modifier_stage_1[] = {
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0,
};

static RE_UINT8 re_emoji_modifier_stage_2[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
};

static RE_UINT8 re_emoji_modifier_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_emoji_modifier_stage_4[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
};

static RE_UINT8 re_emoji_modifier_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 248,
};

/* Emoji_Modifier: 97 bytes. */

RE_UINT32 re_get_emoji_modifier(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_emoji_modifier_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_emoji_modifier_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_emoji_modifier_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_emoji_modifier_stage_4[pos + f] << 6;
    pos += code;
    value = (re_emoji_modifier_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Emoji_Modifier_Base. */

static RE_UINT8 re_emoji_modifier_base_stage_1[] = {
    0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1,
};

static RE_UINT8 re_emoji_modifier_base_stage_2[] = {
    0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 2,
};

static RE_UINT8 re_emoji_modifier_base_stage_3[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 3, 4, 5, 6, 0, 0, 7, 0, 0, 0, 0, 0, 0,
};

static RE_UINT8 re_emoji_modifier_base_stage_4[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  2,
     3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  0,  5,  0,
     0,  0,  6,  7,  8,  9,  0,  0,  0,  0,  0, 10, 11,  0,  0,  0,
     0,  0, 12,  0,  0, 13, 14,  0, 15, 16,  0,  0,  0, 17, 18,  0,
};

static RE_UINT8 re_emoji_modifier_base_stage_5[] = {
      0,   0,   0,   0,   0,   0,   0,  32,   0,   0,   0,   2,   0,  60,   0,   0,
     32,   0,   0,   0, 156,  28,   0,   0, 204, 255,   1,   0, 192,  67, 255,  17,
    238,   0,   0,   0,   0,   4,   0,   0,   0,   0,  48,   4,   0,   0,  97,   0,
    224, 248,   0,   0,   8,   0, 112,   0,   1,  16,   0,   0,   0,   0,   0, 223,
     64,   0, 255,  99,   0,   0,  96,   3,   0,   0, 254,  63,
};

/* Emoji_Modifier_Base: 246 bytes. */

RE_UINT32 re_get_emoji_modifier_base(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_emoji_modifier_base_stage_1[f] << 3;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_emoji_modifier_base_stage_2[pos + f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_emoji_modifier_base_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_emoji_modifier_base_stage_4[pos + f] << 5;
    pos += code;
    value = (re_emoji_modifier_base_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Emoji_Component. */

static RE_UINT8 re_emoji_component_stage_1[] = {
    0, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1,
};

static RE_UINT8 re_emoji_component_stage_2[] = {
    0, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 4, 5,
    6, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_emoji_component_stage_3[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1,
    1, 4, 1, 5, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1,
    7, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_emoji_component_stage_4[] = {
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    2, 0, 0, 0, 0, 0, 0, 3, 4, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 6,
    0, 0, 0, 0, 0, 7, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0,
};

static RE_UINT8 re_emoji_component_stage_5[] = {
      0,   0,   0,   0,   8,   4, 255,   3,   0,  32,   0,   0,   8,   0,   0,   0,
      0, 128,   0,   0, 192, 255, 255, 255,   0,   0,   0, 248,   0,   0,  15,   0,
    255, 255, 255, 255,
};

/* Emoji_Component: 264 bytes. */

RE_UINT32 re_get_emoji_component(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 14;
    code = ch ^ (f << 14);
    pos = (RE_UINT32)re_emoji_component_stage_1[f] << 3;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_emoji_component_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_emoji_component_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_emoji_component_stage_4[pos + f] << 5;
    pos += code;
    value = (re_emoji_component_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Extended_Pictographic. */

static RE_UINT8 re_extended_pictographic_stage_1[] = {
    0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1,
};

static RE_UINT8 re_extended_pictographic_stage_2[] = {
    0, 1, 1, 1, 2, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 6,
};

static RE_UINT8 re_extended_pictographic_stage_3[] = {
     0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     2,  0,  3,  4,  0,  0,  5,  6,  0,  7,  0,  8,  9, 10, 11, 12,
     0,  0, 13,  0,  0,  0, 14,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    15,  0,  0,  0,  0, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    17, 17, 18, 19, 20, 17, 17, 21, 17, 17, 22, 17, 23, 17, 24, 25,
    26, 27, 28, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 29,
};

static RE_UINT8 re_extended_pictographic_stage_4[] = {
     0,  0,  0,  0,  0,  1,  0,  0,  0,  2,  3,  0,  0,  4,  0,  0,
     5,  6,  0,  0,  7,  8,  0,  0,  8,  0,  9, 10,  0,  0, 11,  0,
     0, 12, 13, 14, 15, 16, 16, 16, 17, 16, 16, 16, 18, 19, 20, 21,
    22, 23,  0,  0,  0, 24,  0,  0, 25,  0, 26,  0,  0, 27,  0,  0,
    28,  0,  0,  0, 16, 16, 16, 16, 29,  9,  0, 30, 31, 32, 16, 33,
    34, 35, 36, 16, 16, 16, 16, 37, 16, 38, 39, 16, 16, 16, 40,  0,
     0,  0,  0, 41,  0,  0, 42, 16, 43,  0, 44,  0, 45, 46, 16, 16,
    47, 48, 49, 16, 16, 16, 16, 38,
};

static RE_UINT8 re_extended_pictographic_stage_5[] = {
      0,   0,   0,   0,   0,  66,   0,   0,   0,   0,   0,  16,   0,   2,   0,   0,
      4,   0,   0,   2,   0,   0, 240,   3,   0,   6,   0,   0,   0,   0,   0,  12,
      0,   1,   0,   0,   0, 128,   0,   0,   0, 254,  15,   7,   4,   0,   0,   0,
      0,  12,  64,   0,   1,   0,   0,   0,   0,   0,   0, 120, 191, 255, 247, 255,
    255, 255, 255, 255,  63,   0, 255, 255,  63, 255,  87,  32,   2,   1,  24,   0,
    144,  80, 184,   0, 248,   0,   0,   0,   0,   0, 224,   0,   2,   0,   1, 128,
      0,   0,  48,   0, 224,   0,   0,  24,   0,   0,  33,   0,   0,   0,   1,  32,
      0,   0, 128,   2,   0, 224,   0,   0,   0, 240,   3, 192,   0,  64, 254,   7,
      0, 224, 255, 255,  63,   0,   0,   0, 254, 255,   0,   4,   0, 128, 252, 247,
      0, 254, 255, 255, 255, 255, 255,   7, 255, 255, 255,  63, 192, 255, 255, 255,
    255, 255,   0,   0,   0,   0, 240, 255,   0,   0, 224, 255,   0, 240,   0,   0,
      0, 255,   0, 252,   0, 255,   0,   0,   0, 192, 255, 255,   0, 240, 255, 255,
    255, 255, 255, 247, 191, 255, 255, 255,
};

/* Extended_Pictographic: 514 bytes. */

RE_UINT32 re_get_extended_pictographic(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_extended_pictographic_stage_1[f] << 4;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_extended_pictographic_stage_2[pos + f] << 4;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_extended_pictographic_stage_3[pos + f] << 2;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_extended_pictographic_stage_4[pos + f] << 5;
    pos += code;
    value = (re_extended_pictographic_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* NFD_Quick_Check. */

static RE_UINT8 re_nfd_quick_check_stage_1[] = {
    0, 1, 2, 3, 4, 1, 1, 5, 1, 1, 1, 6, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1,
};

static RE_UINT8 re_nfd_quick_check_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  8,  9,  9,  9,  9, 10,  7,  7,  7,  7, 11,
     7,  7, 12,  7,  7,  7,  7,  7,  7,  7, 13,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7, 14,
};

static RE_UINT8 re_nfd_quick_check_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  5,  5,  7,  8,  9, 10, 11,  5, 12,
    13,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5, 14,  5,  5, 15, 16,
    17, 18, 19, 20,  5,  5,  5,  5,  5,  5, 21,  5,  5,  5,  5,  5,
    22,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,
     5,  5,  5,  5, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23,
    23, 23, 23, 23, 23, 23, 23, 24,  5, 23, 25, 26,  5,  5,  5,  5,
    27, 28,  5, 29, 30, 31,  5,  5,  5, 32,  5,  5,  5,  5,  5,  5,
    23, 23, 33,  5,  5,  5,  5,  5,
};

static RE_UINT8 re_nfd_quick_check_stage_4[] = {
     0,  0,  0,  0,  0,  0,  1,  2,  3,  4,  5,  6,  0,  7,  8,  9,
    10, 11,  0,  0,  0,  0,  0,  0,  0,  0, 12, 13, 14, 15, 16,  0,
    17, 18, 19, 20,  0,  0, 21, 22,  0,  0,  0,  0,  0,  0,  0,  0,
     0, 23,  0,  0,  0,  0, 24,  0,  0, 25, 26,  0,  0,  0, 27,  0,
     0, 28, 29,  0,  0,  0,  0,  0,  0,  0, 30,  0, 31,  0, 32,  0,
     0,  0, 33,  0,  0,  0, 34,  0,  0,  0, 32,  0,  0,  0, 35,  0,
     0,  0, 36, 37, 38, 39,  0,  0,  0, 40,  0,  0,  0,  0,  0,  0,
    41, 42, 43,  0,  0,  0,  0,  0, 44, 44, 44, 44, 45, 44, 44, 46,
    47, 44, 48, 49, 44, 50, 51, 52, 53,  0,  0,  0,  0,  0,  0,  0,
     0, 54,  0,  0, 55, 56, 57,  0, 58, 59, 60, 61, 62, 63,  0, 64,
     0, 65,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 66,  0,
     0,  0, 67, 68, 13, 67, 68, 69, 44, 44, 44, 44, 44, 44, 44, 44,
    44, 44, 44, 44, 44, 70,  0,  0, 71, 72, 44, 73, 44, 44, 46,  0,
    74, 75, 76,  0,  0,  0,  0,  0,  0,  0,  0,  0, 77, 78,  0,  0,
     0, 79,  0,  0,  0,  0,  0,  0,  0,  0, 80,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0, 81,  0,  0,  0,  0,  0,  0,  0, 55,  0,  0,
     0,  0, 82, 83,  0, 84, 85,  0, 49,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_nfd_quick_check_stage_5[] = {
      0,   0,   0,   0, 191, 255, 126,  62, 191, 255, 126, 190, 255, 255, 252, 255,
     63, 255, 241, 126, 248, 241, 243, 255,  63, 255, 255, 127,   3, 128,   1,   0,
      0, 224, 255, 223, 207, 255,  49, 255, 255, 255, 255, 207, 192, 255,  15,   0,
     27,   0,   0,   0,   0,   0,  16,  64, 224, 215,   1,   0,   0, 252,   1,   0,
      0, 124,  24,   0, 139, 112,   0,   2,   0,   0,   0,   2,   0,   0, 139, 112,
      0,   0, 192,   0,   6,   0, 207, 252, 252, 252,  63,   3, 124,   0,   0,   0,
      5,   0,   8,   0,   0,   2,  18,   0,   0,   0,   0, 255,   0,  24,   0, 176,
      0,   0,  72,   0,   0,   0,   0,  78,   0,  25,   0,  48,   0,   0,  16,   0,
      0,  28,   0,   0,   0,   1,   0,   0, 129,  13,   0,   0,   0,   0,   0, 116,
      8,  32, 132,  16,   0,   2, 104,   1,   2,   0,   8,  32, 132,  16,   0,   2,
     64,   0,   0,   0,  64,  85,   4,   0,   0,   0,   0,  40,  11,   0,   0,   0,
    255, 255, 255, 255, 255, 255, 255,  11, 255, 255, 255,   3, 255, 255,  63,  63,
     63,  63, 255, 170, 255, 255, 255,  63, 255, 255, 223,  95, 222, 255, 207, 239,
    255, 255, 220,  63,   3,   0,   0,   0,  64,  12,   0,   0,   0,   0,   0,  12,
      0,  64,   0,   0,   0, 224,   0,   0,  16,  18,   0,   0,  80,   0,   0,   0,
    146,   2,   0,   0,   5, 224,  51,   3,  51,   3,   0,   0,   0, 240,   0,   0,
     15,  60,   0,   0,   0,   6,   0,   0,   0,   0,   0,  16,   0,  80,  85,  85,
    165,   2, 219,  54,   0,   0, 144,  71,  15,   0,   0,   0, 255,  63, 229, 127,
    101, 252, 255, 255, 255,  63, 255, 255,   0,   0,   0, 160,   0, 252, 127,  95,
    219, 127,   0,   0,   0,   0,   0,  20,   0,   8,   0,   0,   0, 192,   0,   0,
      0,  24,   0,   0,   0,   0,   0,  88,   0,   0,   0, 192,  31,   0,   0,   0,
      0,   0,   0, 248,   1,   0,   0,   0,
};

/* NFD_Quick_Check: 860 bytes. */

RE_UINT32 re_get_nfd_quick_check(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 14;
    code = ch ^ (f << 14);
    pos = (RE_UINT32)re_nfd_quick_check_stage_1[f] << 3;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_nfd_quick_check_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_nfd_quick_check_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_nfd_quick_check_stage_4[pos + f] << 5;
    pos += code;
    value = (re_nfd_quick_check_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* NFC_Quick_Check. */

static RE_UINT8 re_nfc_quick_check_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 3, 4, 2, 2, 2, 2, 2, 5, 2,
    2, 2, 2, 2, 2, 2, 2, 6, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2,
};

static RE_UINT8 re_nfc_quick_check_stage_2[] = {
     0,  0,  0,  1,  0,  0,  2,  0,  0,  3,  4,  5,  6,  7,  0,  8,
     9, 10,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11,  0,  0,  0, 12,
    13, 14,  0, 15,  0,  0,  0,  0,  0,  0, 16,  0,  0,  0,  0,  0,
    17,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0, 18, 19, 20,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    21, 22,  0, 23, 24, 25,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0, 26,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0, 18, 18, 27,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_nfc_quick_check_stage_3[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  1,  2,  3,  4,  5,  0,  0,  0,
     0,  0,  6,  0,  0,  0,  0,  0,  0,  7,  8,  0,  0,  9, 10,  0,
     0, 11, 12,  0,  0,  0,  0,  0,  0,  9, 13,  0,  0,  9, 14,  0,
     0,  0, 15,  0,  0,  0, 16,  0,  0,  9, 14,  0,  0,  0, 17,  0,
     0,  0, 18, 19, 20, 21,  0,  0,  0, 22,  0,  0,  0,  0,  0,  0,
     0,  0,  0, 23,  0, 24, 25,  0,  0, 26,  0,  0,  0,  0,  0,  0,
     0,  0,  0, 27,  0, 28, 29, 30, 31,  0,  0,  0,  0,  0,  0,  0,
     0, 32,  0,  0,  0,  0,  0,  0,  0, 33,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 34,  0,  0,  0,  0,  0, 35,  0,  0,  0,
    36, 36, 36, 36, 36, 36, 36, 36, 37, 38, 36, 39, 36, 36, 40,  0,
    41, 42, 43,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 44,  0,  0,
     0, 45,  0,  0,  0,  0,  0,  0,  0,  9, 14,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0, 46,  0,  0,  0,  0,  0,  0,  0, 47,  0,  0,
     0,  0, 48, 49,  0, 50, 51,  0, 52,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_nfc_quick_check_stage_4[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  1,  2,  1,  3,  4,  5,  6,  0,
     6,  1,  5,  7,  8,  0,  5,  0,  9, 10,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0, 11,  0, 12,  0, 13,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  6,  8,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,
     0,  0,  0,  0,  0,  0, 14, 14,  0,  0,  0,  0,  0,  0,  0, 15,
     0,  0,  0,  0,  0,  6,  0, 16,  0,  0,  0,  0, 13, 12,  0,  0,
     0,  0,  0,  0,  0,  0, 17, 12,  0,  0,  0,  0,  0, 18,  0, 19,
     0,  0,  0,  0,  0,  6,  0,  0,  0,  0,  0,  0,  0, 15,  0,  0,
    15,  0,  0,  0,  0,  7,  0,  0,  0,  0, 15,  6,  0,  0,  0,  6,
    13,  0,  0, 20, 12, 13,  0, 11,  0,  0, 20,  0, 13, 21, 11,  0,
    20,  0,  0,  0, 13,  0,  0, 20, 12, 13,  0, 11,  0,  0, 20,  0,
     0,  0,  0, 15,  0,  0,  0,  0, 22,  1,  1,  1,  1,  8,  0,  0,
     0,  0,  1,  1,  1,  1,  1,  1, 23,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0, 24,  0,  0,  0,  0,  0,  0, 25, 25, 25, 20,
     0,  0,  0,  0,  0,  0, 13, 12,  0,  0, 25,  0, 13,  0, 13,  0,
    13,  0, 13, 26,  0,  0, 25, 20, 19,  0,  0,  0,  0,  0,  0,  0,
     0, 12, 26,  0,  0,  0,  0,  0,  0,  0, 21,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0, 11,  0,  0,  0,  0,  0,  0,  7,  0,
    14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 19, 27, 17, 14, 28,
    27, 21, 26, 14, 14, 14, 14, 14, 14, 14, 14, 19, 14, 14, 14, 14,
    14, 14, 14, 14, 14, 14, 19,  0,  0,  0,  0,  0,  0,  0,  0, 25,
     0,  0, 26, 14, 14, 28, 14, 27, 16, 29, 14, 28,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 15,  0,  0,  6,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  5,  0, 15, 24,  0,  0,  0,  6,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0, 26, 14, 11,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 13, 14, 11,  0,  0,  0,  0,  0,  0,  0,
    14, 14, 14, 14, 14, 14, 14, 19,
};

static RE_UINT8 re_nfc_quick_check_stage_5[] = {
    0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2,
    0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0,
    2, 2, 0, 0, 1, 1, 2, 1, 1, 2, 0, 0, 1, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 2, 0,
    1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 2, 2, 1, 1, 0, 0,
    0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0,
    0, 2, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0,
    1, 1, 1, 0, 1, 0, 1, 1,
};

/* NFC_Quick_Check: 1128 bytes. */

RE_UINT32 re_get_nfc_quick_check(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 13;
    code = ch ^ (f << 13);
    pos = (RE_UINT32)re_nfc_quick_check_stage_1[f] << 5;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_nfc_quick_check_stage_2[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_nfc_quick_check_stage_3[pos + f] << 3;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_nfc_quick_check_stage_4[pos + f] << 2;
    value = re_nfc_quick_check_stage_5[pos + code];

    return value;
}

/* NFKD_Quick_Check. */

static RE_UINT8 re_nfkd_quick_check_stage_1[] = {
    0, 1, 2, 3, 4, 1, 1, 5, 1, 1, 1, 6, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1,
};

static RE_UINT8 re_nfkd_quick_check_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  8,  9, 10, 10, 10, 10, 11,  7,  7,  7,  7, 12,
     7,  7, 13,  7,  7,  7,  7,  7,  7,  7, 14,  7,  7, 15, 16,  7,
     7,  7,  7,  7,  7,  7,  7, 17,
};

static RE_UINT8 re_nfkd_quick_check_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  9, 10, 11, 12, 13, 14,
    15,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7, 16,  7, 17, 18, 19,
    20, 21, 22, 23, 24,  7,  7,  7,  7,  7, 25,  7, 26, 27, 28, 29,
    30, 31, 32, 33,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7, 34, 35,  7,  7,  7, 36, 33, 33, 33, 33,
    33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 37,
     7, 33, 38, 39, 33, 40, 41, 42, 43, 44,  7, 45, 46, 47,  7,  7,
     7, 48,  7,  7, 49, 50, 51, 52,  7,  7,  7,  7,  7,  7, 53,  7,
     7, 54, 55,  7,  7,  7,  7,  7, 33, 33, 56,  7,  7,  7,  7,  7,
};

static RE_UINT8 re_nfkd_quick_check_stage_4[] = {
      0,   0,   0,   0,   0,   1,   2,   3,   4,   5,   6,   7,   0,   8,   9,  10,
     11,  12,   0,   0,   0,  13,  14,  15,   0,   0,  16,  17,  18,  19,  20,  21,
     22,  23,  24,  25,   0,   0,  26,  27,   0,   0,   0,   0,  28,   0,   0,   0,
      0,  29,   0,  30,   0,   0,  31,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,  32,  33,   0,   0,   0,  34,   0,   0,  35,  36,   0,   0,   0,   0,   0,
      0,   0,  37,   0,  38,   0,  39,   0,   0,   0,  40,   0,   0,   0,  41,   0,
      0,   0,  39,   0,   0,   0,  42,   0,   0,  43,   0,   0,   0,  43,  44,   0,
     45,   0,  46,  47,  48,  49,   0,   0,   0,  50,   0,   0,   0,   0,   0,  51,
     52,  53,  54,   0,   0,   0,   0,   0,   0,  55,  56,  57,  58,  59,   0,   0,
     59,  59,  59,  59,  60,  59,  59,  61,  62,  59,  63,  64,  59,  65,  66,  67,
     68,  69,  70,  71,  72,  40,   0,   0,  73,  74,  75,  59,  76,  77,  78,   0,
     79,  80,  81,  82,  83,  84,   0,  85,   0,  86,   0,   0,   0,   0,   0,   0,
      0,   0,   0,  59,  59,  59,  59,  87,  45,   0,   0,  88,   0,   0,  51,   0,
      0,   0,   0,  44,   0,   0,   0,   0,   0,   0,   0,  89,   0,   0,   0,   0,
      0,   0,   0,   0,  90,   0,   0,  43,  59,  59,  59,  59,  59,  59,  91,   0,
     92,  93,  94,  95,  96,  94,  95,  97,   0,  98,  59,  59,  99,   0,   0,   0,
    100,  59, 101, 100,  59,  59,  59, 100,  59,  59,  59,  59,  59,  59,  59,  59,
      0,   0,   0,   0,  44,   0,   0,   0,   0,   0,   0, 102,   0,   0,   0, 103,
      0,   0, 104,   0,   0,   0,   0,   0,  59,  59,  59,  59,  59, 105,   0,   0,
    106, 107,  59, 108,  59,  59,  61,   0, 109, 110, 111,  59,  59, 112, 113,  59,
     59,  64, 114,  59,   4,  59, 115, 116, 117, 114, 118, 119,  59,  59,  59, 120,
    121,  59,  59,  59,  59, 100, 122, 123,   0,   0,   0,   0, 124, 125,   0,   0,
      0, 126,   0,   0,   0,   0,   0,   0,   0,   0, 127,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0, 128,   0,   0,   0,   0,   0,   0,   0, 129,   0,   0,
      0,   0, 130,  15,   0,  58,  92,   0,  59,  59,  65,  59, 131, 132, 133,  59,
    134, 135, 136,  59,  59,  59,  59,  59,  59,  59,  59,  59,  59,   7,  59,  59,
     59,  59,  59,  59,  59,  59, 137,  59, 133, 138, 139, 140, 141, 142,   0,   0,
    143, 144, 145, 146, 102,   0,   0,   0, 147,  60, 148,   0,   0,   0,   0,   0,
     64,   0,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_nfkd_quick_check_stage_5[] = {
      0,   0,   0,   0,   1, 133,  60, 119, 191, 255, 126,  62, 191, 255, 126, 190,
    255, 255, 252, 255,  63, 255, 253, 254, 249, 243, 243, 255,  63, 255, 255, 255,
      3, 128,   1,   0, 240, 255, 255, 223, 207, 255,  63, 255, 255, 255, 255, 207,
    192, 255,  15,   0,   0,   0, 255,   1,   0,   0,   0,  63,  31,   0,   0,   0,
     27,   0,   0,   0,   0,   0,  16,  68, 240, 215,   1,   0,   0, 252,   1,   0,
      0, 124, 127,   0,   0,   0,  55,   2, 139, 112,   0,   2,   0,   0,   0,   2,
      0,   0, 139, 112,   0,   0, 192,   0,   6,   0, 207, 252, 252, 252,  63,   3,
    128,   0,   0,   0, 124,   0,   0,   0,   0,   0, 224,   1,   5,   0,   8,   0,
      0,   2,  18,   0,   0,   0,   0, 255,   0,  24,   0, 176,   0,   0,  72,   0,
      0,   0,   0,  78,   0,  25,   0,  48,   0,   0,  16,   0,   0,  28,   0,   0,
      0,   1,   0,   0, 129,  13,   0,   0,   0,   0,   0, 116,   0,   0,   8,   0,
      0,   0,   0,  48,   0,  16,   0,   0,   8,  32, 132,  16,   0,   2, 232,   3,
      2,   0,   8,  32, 132,  16,   0,   2,  64,   0,   0,   0,   0,   0,   0,  16,
     64,  85,   4,   0,   0,   0,   0,  40,  11,   0,   0,   0,   0, 112, 255, 247,
    255, 191, 255, 255, 255,   7,   0,   1,   0,   0,   0, 248, 255, 255, 255, 255,
    255, 255, 255,  15, 255, 255, 255,   3, 255, 255,  63,  63,  63,  63, 255, 170,
    255, 255, 255,  63, 255, 255, 223, 255, 223, 255, 207, 239, 255, 255, 220, 127,
    255,   7, 130,   0, 112, 128, 216,  80, 128,   3, 128, 128,   0,   0, 243, 255,
    255, 127, 255,  31, 239, 254, 111,  62,  87, 189, 251, 251, 225,   3, 255, 255,
      0,   2,   0,  12,   0,  64,   0,   0,   0, 224,   0,   0,  16,  18,   0,   0,
     80, 176,   1,   0, 146,   2,   0,   0,   5, 224,  51,   3,  51,   3,   0,   0,
      0, 240,   0,   0,  15,  60,   0,   0,   0,   6,   0,   0, 255,   7,   0,   0,
      0,   0, 112,   0,   0, 128,   0,   0,   0,   0,   0, 128, 255, 255,  63,   0,
      1,   0,   0,   0,   0,   0,  64,   7,   0,  80,  85,  85, 165,   2, 219,  54,
      0,   0,  16, 216,   0,   0, 144, 199,   0,   0, 254, 255, 255, 127, 252, 255,
    255, 255, 255, 127, 255,   0, 255, 255,   0,   0,   1,   0,   0,   0,   0,   3,
      0,   0,   0, 240,  15,   0,   0,   0, 255,  63, 229, 127, 101, 252, 255, 255,
    255,  63, 255, 255, 127,   0, 248, 160, 255, 255, 127,  95, 219, 255, 255, 255,
    255, 255,   3,   0,   0,   0, 248, 255,   0,   0, 255, 255, 255,   0,   0,   0,
      0,   0, 255,  31,   0,   0, 255,   3, 159, 255, 247, 255, 127,  15, 215, 255,
    255, 255, 255,  31, 254, 255, 255, 255, 252, 252, 252,  28, 127, 127,   0,   0,
      0,   0,   0,  20,   0,   8,   0,   0,   0, 192,   0,   0,   0,  24,   0,   0,
      0,   0,   0,  88,   0,   0,   0,  12,   0,   0,   0, 192, 255, 255, 255, 223,
    100, 222, 255, 235, 239, 255, 255, 255, 191, 231, 223, 223, 255, 255, 255, 123,
     95, 252, 253, 255, 255, 207, 255, 255, 150, 254, 247,  10, 132, 234, 150, 170,
    150, 247, 247,  94, 255, 251, 255,  15, 238, 251, 255,  15, 255,   7, 255, 255,
    255, 127, 255, 255, 255, 255,   0,   0,   0,  12,   0,   0,   7,   0, 255, 255,
    255,   1,   3,   0,
};

/* NFKD_Quick_Check: 1320 bytes. */

RE_UINT32 re_get_nfkd_quick_check(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 14;
    code = ch ^ (f << 14);
    pos = (RE_UINT32)re_nfkd_quick_check_stage_1[f] << 3;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_nfkd_quick_check_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_nfkd_quick_check_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_nfkd_quick_check_stage_4[pos + f] << 5;
    pos += code;
    value = (re_nfkd_quick_check_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* NFKC_Quick_Check. */

static RE_UINT8 re_nfkc_quick_check_stage_1[] = {
     0,  1,  2,  3,  4,  4,  4,  4,  4,  4,  5,  4,  4,  4,  4,  6,
     4,  7,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  8,  9, 10,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4, 11,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
     4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
};

static RE_UINT8 re_nfkc_quick_check_stage_2[] = {
     0,  1,  2,  3,  0,  4,  5,  6,  0,  0,  0,  7,  8,  0,  0,  0,
     0,  0,  9, 10, 11,  0, 12, 13, 14, 15, 13, 16, 17, 18, 19, 20,
    21, 22, 23, 24,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 25,  0,  0,  0, 26, 27,  0, 28, 29, 30,
    31, 32, 33, 34, 35,  0, 36,  0, 37, 38,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0, 39, 40,  0,  0, 41,  0, 42,  0,  0, 43, 44, 45,
    46, 47, 48, 49, 50, 51, 44, 44,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 52, 53, 54,
     0,  0,  0,  0,  0,  0, 55,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0, 44, 44, 56, 57, 58, 59, 44, 44, 60, 61, 62, 63, 64, 65,
     0, 66, 67,  0,  0,  0, 13,  0,  0, 68,  0, 69,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0, 70, 71,  0,  0,  0,  0, 72, 73, 74, 44, 44, 75, 44, 76,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 77, 78,  0,  0,
     0,  0, 79, 80, 81,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    44, 44, 44, 44, 82,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_nfkc_quick_check_stage_3[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   2,   0,   0,   0,   0,
      0,   0,   0,   3,   4,   0,   0,   5,   0,   0,   0,   0,   6,   0,   0,   7,
      0,   0,   0,   8,   0,   9,  10,   0,  11,  12,  13,  14,  15,   0,   0,  16,
     17,   0,   0,   0,   0,  18,   0,  19,  20,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,  21,   0,  22,   0,   0,   0,  23,   0,  24,   0,   0,
      0,   0,   0,  25,   0,  26,   0,   0,   0,   0,   0,  27,   0,  28,   0,   0,
      0,   0,   0,  25,   0,  29,   0,   0,   0,   0,   0,  25,   0,  30,   0,   0,
      0,   0,   0,   0,   0,  31,   0,   0,   0,   0,   0,   0,  32,  33,   0,   0,
      0,   0,   0,   0,  34,  35,   0,   0,   0,   0,   0,  36,   0,   0,   0,   0,
      0,   0,   0,  36,   0,  37,   0,   0,  38,   0,   0,   0,  39,  40,  41,  42,
     43,  39,  40,  41,   0,   0,   0,   0,   0,   0,  25,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  38,   0,   0,   0,   0,   0,   0,  44,  45,
      0,   0,  46,  47,  48,   0,   0,   0,   0,   0,   0,  49,   0,   0,   0,   0,
      0,   0,  50,  51,  52,  53,  54,  55,   0,  56,  53,  53,   0,   0,   0,   0,
      0,  57,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  58,
      0,   0,   0,  59,  60,  61,  61,  62,  54,  63,  64,  65,  66,  67,   0,  68,
     69,  70,  55,   0,   0,   0,   0,   0,  71,  72,  73,  74,  75,  53,  53,  53,
     41,   0,   0,   0,   0,   0,   0,   0,   0,   0,  76,  77,   0,   0,   0,   0,
      0,   0,  78,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  53,  53,
     53,  53,  53,  53,  53,  53,  54,   0,  38,   0,   0,   0,   0,   0,   0,  79,
      0,   0,   0,   0,   0,  38,   0,   0,   0,   0,   0,   0,   0,   0,   0,  37,
      0,   0,   0,   0,   0,   0,   5,   0,   0,   5,   0,   0,   0,   0,   0,  36,
     53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  80,   0,   0,
     77,   0,   0,  81,   0,   0,   0,   0,   0,  82,   0,   0,   0,   0,   0,   5,
      0,   0,   0,  83,  53,  53,  53,  53,  69,  84,   0,   0,   0,   0,   0,   0,
     53,  69,  53,  53,  85,  53,  53,  69,  53,  53,  53,  53,  53,  53,  53,  69,
      0,  37,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  77,
      0,   0,   0,   0,   0,   0,   0,  86,   0,   0,   0,   0,   0,  87,   0,   0,
     88,  89,  90,  53,  53,  53,  88,  53,  53,  53,  53,  53,  53,  91,   0,   0,
     18,  92,  53,  93,  94,  53,  53,  53,  53,  53,  53,  95,   0,  96,  53,  53,
     53,  53,  53,  88,   0,  53,  53,  53,  53,  84,  53,  53,  85,   0,   0,  70,
      0,  91,   0,  53,  97,  98,  99, 100,  53,  53,  53,  53,  53,  53,  53,  70,
     83,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  69, 101, 102, 103,   0,
      0,   0,   0, 104,   0,   0,   0,   0,   0,   0,  30,   0,   0,   0,   0,   0,
      0,   0,   0, 105,   0,   0,   0,   0,   0,   0,  35,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0, 106,  10,   0,   0,   0,   0,  56,  77,   0,   0,   0,
     53,  53,  53,  53,  53, 107,  53,  53,  53, 108, 109, 110, 111,  53,  53,  53,
    112, 113,  53, 114, 115, 116,  53,  53,  53,  53, 117,  53,  53,  53,  53,  53,
     53,  53,  53,  53, 118,  53,  53,  53, 111,  53, 119, 120, 121, 122, 123, 124,
    125, 126, 127, 126,   0,   0,   0,   0,  54,  53,  69,  53,  53,   0,  57,   0,
      0,  77,   0,   0,   0,   0,   0,   0, 128,  53,  53, 126,   8,  95,   0,   0,
     53,  88,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_nfkc_quick_check_stage_4[] = {
     0,  0,  0,  0,  1,  0,  2,  3,  4,  5,  6,  6,  4,  0,  0,  3,
     1,  0,  7,  0,  0,  0,  0,  3,  0,  8,  8,  1,  9,  0,  0,  0,
     8,  8,  1,  0,  0,  0,  8,  5,  8,  1,  0,  0, 10, 11, 10, 12,
    13, 14, 15,  0, 15, 10, 14, 16, 17,  0, 14,  0, 18, 19,  0,  0,
     0,  1, 20, 20,  0, 21,  0,  0,  8,  6,  0,  0,  6,  5,  7,  0,
     0,  3,  0,  0, 15, 17,  0,  0,  0,  9,  1,  0,  0,  0,  0, 14,
     0,  0,  8,  8,  0,  0,  0, 22,  0, 15,  0, 21,  3, 20,  0,  0,
     0,  0,  9, 20,  0, 23,  0,  5,  0, 15,  0,  0,  0, 22,  0,  0,
    22,  0,  0,  0,  0, 16,  0,  0,  0,  0, 22, 15,  0,  0,  0, 15,
     3,  0,  0,  0,  0,  0,  0,  5,  0,  0,  0,  1,  3,  0,  0,  7,
    20,  3,  0,  1,  0,  0,  7,  0,  3,  9,  5,  0,  7,  0,  0,  0,
    24, 10, 10, 10, 10, 17,  0,  0,  0,  0, 10, 10, 10, 10, 10, 10,
    25,  0,  0,  0,  0, 26,  0,  0,  0,  0,  0,  6,  8,  8,  6,  8,
     8,  8,  8, 21,  8,  8,  8,  8,  8,  8,  6,  0,  0,  0,  1,  0,
     0,  0,  3,  8,  0,  0,  4,  0, 27, 27, 27,  7,  0,  0,  3,  9,
     5,  0, 27,  9,  3,  0,  3,  9,  0,  0, 27, 28,  7,  3,  0,  0,
     0,  6,  0,  3,  3, 29,  0,  2,  0,  3,  5,  0,  0,  3,  0,  3,
     5,  8,  8,  8,  8,  8,  8,  6,  8,  8,  8,  1,  8,  9,  9,  8,
     8, 28,  9,  5,  6,  2, 29, 21, 21,  8, 21,  8,  1,  9,  5,  0,
     0,  0,  0, 21,  1,  0,  0,  0,  0,  0, 28,  0,  0,  6,  0,  0,
     8,  5,  0,  0,  0, 20,  6,  0,  0,  0, 30, 31,  9,  8,  8,  8,
     4,  8,  8,  8,  8,  8,  0,  0,  0,  0,  5,  0,  0,  0,  0,  8,
     8,  8,  8,  5,  2,  9,  8,  6,  2, 28,  4,  8,  8,  8,  5,  0,
     3,  8,  0, 27,  8,  6,  8,  2, 21, 29,  8,  8,  5,  0,  0,  0,
     3,  8,  8,  8,  8, 31,  8,  8,  6,  8,  8,  8,  8,  6,  8,  0,
     6, 29,  8,  8,  4,  8,  4,  8,  4,  8,  4,  1,  8,  6,  8,  6,
     0,  0, 22,  0, 14,  0, 22, 26,  0,  0,  0,  4,  8, 29,  8,  8,
     8,  8,  8, 29, 20, 28,  9, 29,  8,  8, 21,  9,  8,  9,  8,  8,
     8, 21,  6,  9,  8, 29,  8, 29,  8,  8, 21,  6,  8,  2,  4,  8,
    29,  8,  8,  8,  8,  5,  8,  8,  8,  8,  8,  4, 28, 31,  9,  8,
     6,  8, 27,  0, 20,  3, 27,  9, 28, 31, 27, 27, 28, 31,  6,  8,
     6,  8,  9,  2,  8,  8, 21,  8,  8,  8,  8,  0,  9,  9, 21,  8,
     6,  0,  0,  0,
};

static RE_UINT8 re_nfkc_quick_check_stage_5[] = {
    0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1,
    0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0,
    1, 1, 1, 1, 0, 1, 1, 1, 2, 2, 2, 2, 2, 0, 2, 2,
    2, 0, 0, 2, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 2,
    0, 2, 2, 0, 2, 2, 0, 0, 1, 1, 2, 1, 1, 2, 0, 0,
    0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 2, 0, 0, 0, 2, 2,
    0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 1, 0, 1,
    0, 1, 1, 0, 1, 0, 1, 1, 0, 2, 2, 1, 1, 0, 0, 1,
};

/* NFKC_Quick_Check: 1964 bytes. */

RE_UINT32 re_get_nfkc_quick_check(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 12;
    code = ch ^ (f << 12);
    pos = (RE_UINT32)re_nfkc_quick_check_stage_1[f] << 5;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_nfkc_quick_check_stage_2[pos + f] << 3;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_nfkc_quick_check_stage_3[pos + f] << 2;
    f = code >> 2;
    code ^= f << 2;
    pos = (RE_UINT32)re_nfkc_quick_check_stage_4[pos + f] << 2;
    value = re_nfkc_quick_check_stage_5[pos + code];

    return value;
}

/* Alphanumeric. */

static RE_UINT8 re_alphanumeric_stage_1[] = {
    0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3,
};

static RE_UINT8 re_alphanumeric_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  9, 10, 11,  7,  7,  7,  7, 12, 13, 13, 13, 13, 14,
    15, 16, 17, 18, 19, 13, 20, 13, 21, 13, 13, 13, 13, 22,  7,  7,
    23, 24, 13, 13, 13, 13, 25, 26, 13, 13, 27, 13, 28, 29, 30, 13,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7, 31,  7, 32, 33,  7, 34,  7,  7,  7, 35, 13, 36,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
};

static RE_UINT8 re_alphanumeric_stage_3[] = {
      0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,
     16,   1,  17,  18,  19,   1,  20,  21,  22,  23,  24,  25,  26,  27,   1,  28,
     29,  30,  31,  31,  32,  31,  31,  31,  31,  31,  31,  31,  33,  34,  35,  31,
     36,  37,  31,  31,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,  38,   1,   1,   1,   1,   1,   1,   1,   1,   1,  39,
      1,   1,   1,   1,  40,   1,  41,  42,  43,  44,  45,  46,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,  47,  31,  31,  31,  31,  31,  31,  31,  31,
     31,   1,  48,  49,   1,  50,  51,  52,  53,  54,  55,  56,  57,  58,   1,  59,
     60,  61,  62,  63,  64,  65,  31,  66,  67,  68,  69,  70,  71,  72,  73,  74,
     75,  31,  76,  31,  77,  78,  79,  31,   1,   1,   1,  80,  81,  82,  31,  31,
      1,   1,   1,   1,  83,  31,  31,  31,  31,  31,  31,  31,   1,   1,  84,  31,
      1,   1,  85,  86,  31,  31,  87,  88,   1,   1,   1,   1,   1,   1,   1,  89,
      1,   1,  90,  31,  31,  31,  31,  31,   1,  91,  92,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  93,  31,  31,  31,  31,  31,  31,  31,  94,  95,  96,  97,
     98,  31,  31,  31,  31,  31,  31,  31,  99, 100,  31,  31,  31,  31, 101,  31,
     31, 102,  31,  31,  31,  31,  31,  31,   1,   1,   1,   1,   1,   1, 103,   1,
      1,   1,   1,   1,   1,   1,   1, 104, 105,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1, 106,   1,   1,   1,   1, 107,  31,  31,  31,  31,
      1,   1, 108,  31,  31,  31,  31,  31,
};

static RE_UINT8 re_alphanumeric_stage_4[] = {
      0,   1,   2,   2,   0,   3,   4,   4,   5,   5,   5,   5,   5,   5,   5,   5,
      5,   5,   5,   5,   5,   5,   6,   7,   0,   0,   8,   9,  10,  11,   5,  12,
      5,   5,   5,   5,  13,   5,   5,   5,   5,  14,  15,   5,  16,  17,  18,  19,
     20,   5,  21,  22,   5,   5,  23,  24,  25,   5,  26,   5,   5,  27,   5,  28,
     29,  30,  31,  32,   0,  33,  34,  35,   5,  36,  37,  38,  39,  40,  41,  42,
     43,  44,  45,  46,  47,  48,  49,  50,  51,  48,  52,  53,  54,  55,  56,  57,
     58,  59,  60,  61,  58,  62,  63,  64,  58,  65,  66,  67,  68,  69,  70,  71,
     72,  73,  74,   0,  75,  76,  77,   0,  78,  79,  80,  81,  82,  83,   0,   0,
      5,  84,  85,  86,  87,   5,  88,  89,   5,   5,  90,   5,  91,  92,  93,   5,
     94,   5,  95,   0,  96,   5,   5,  97,  72,   5,   5,   5,   5,   5,   5,   5,
      5,   5,   5,  98,   2,   5,   5,  99, 100, 101, 101, 102,   5, 103, 104,  79,
      1,   5,   5,  31,   5, 105,   5, 106, 107, 108, 109, 110,   5, 111, 112,   0,
    113,   5, 107, 114, 112, 115,   0,   0,   5, 116, 117,   0,   5, 118,   5, 119,
      5, 106, 120, 121, 122,  65,   0, 123,   5,   5,   5,   5,   5,   5,   0, 124,
     97,   5, 125, 121,   5, 126, 127, 128,   0,   0,   0, 129, 130,   0,   0,   0,
    131, 132, 133,   5,  16,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0, 134,   5,  79,   5, 135, 107,   5,   5,   5,   5, 136,
      5,  88,   5, 137, 138, 139, 139,   5,   0, 140,   0,   0,   0,   0,   0,   0,
    141, 142,  72,   5, 143,  72,   5,  89, 144,  14,   5,   5, 145,  73,   0,  25,
      5,   5,   5,   5,   5, 106,   0,   0,   5,   5,   5,   5,   5,   5,   5,  96,
      5,   5,   5,   5,  30,   0,  25, 121, 146, 147,   5, 148,   5,   5,   5,  96,
    149, 150,   5,   5, 151, 152,   0, 149, 153, 154,   5, 101,   5,   5, 155, 156,
      5, 105, 157,  83,   5, 158, 159, 160,   5, 138, 161, 162,   5, 107, 163, 164,
    165, 166,  89, 167,   5,   5,   5, 168,   5,   5,   5,   5,   5, 169, 170, 113,
      5,   5,   5, 171,   5,   5, 152,   0, 172, 173, 174,   5,   5,  27, 175,   5,
      5, 121,  25,   5, 176,   5, 154, 177,   0,   0,   0, 178,   5,   5,   5,  83,
      1,   2,   2, 109,   5, 107, 179,   0, 180, 181, 182,   0,   5,   5,   5,  73,
      0,   0,   5, 183,   0,   0,   0,   0,   0,   0,   0,   0,  83,   5, 184,   0,
      5,  26, 105,  73, 121,   5, 185,   0,   5,   5,   5,   5, 121,  85, 186, 113,
      5, 187,   5, 188,   0,   0,   0,   0,   5, 138, 106, 154,   0,   0,   0,   0,
    189, 190, 106, 138, 107,   0,   0, 191, 106, 152,   0,   0,   5, 192,   0,   0,
    193, 106,   0,  83,  83,   0,  80, 194,   5, 106, 106, 157,  27,   0,   0,   0,
      5,   5,  16,   0,   5, 157,   5, 157,   5, 195,   0,   0,   0,   0,   0,   0,
     83, 196, 197,   0,   0,   0,   0,   0,   5,   5, 197,  57, 150,  31,  25, 198,
      5, 199, 200, 201,   5,   5, 202,   0, 203, 204,   0,   0, 205, 122,   5, 198,
     39,  48, 206, 188,   0,   0,   0,   0,   5,   5, 207,   0,   5,   5, 208,   0,
      0,   0,   0,   0,   5, 209, 210,   0,   5, 107, 211,   0,   5, 106,  79,   0,
     65, 168,   0,   0,   0,   0,   0,   0,   5,  31,   0,   0,   0,   5,   5, 212,
      5, 213,  25,   5, 214,   0,   5,  31, 215, 216, 217, 218, 176, 219,   0,   0,
    220, 221, 222, 223, 224,  79,   0,   0,   0,   0,   0,   0,   0,   0,   0, 138,
      5,   5,   5,   5, 152,   0,   0,   0,   5,   5,   5, 145,   5,   5,   5,   5,
      5,   5, 188,   0,   0,   0,   0,   0,   5, 145,   0,   0,   0,   0,   0,   0,
      5,   5, 225,   0,   0,   0,   0,   0,   5,  31, 107,  79,   0,   0,  25, 226,
      5, 138, 227, 228,  96,   0,   0,   0,   0,   0,   5,   5,   0,   0,   0,   0,
      5,   5, 229, 107, 175,   0,   0, 230,   5,   5,   5,   5,   5,   5,   5,  27,
      5,   5,   5,   5,   5,   5,   5, 157, 107,   0,   0,  25,   5,   5,   5,   5,
      5,   5,   5,   5,   5,   5,   5, 113,   5,   5,   5, 231, 232,   0,   0,   0,
      5,   5, 233,   5, 234, 235, 236,   5, 237, 238, 239,   5,   5,   5,   5,   5,
      5,   5,   5,   5,   5, 240, 241,  89, 233, 233, 135, 135, 215, 215, 242,   5,
    243, 244,   0,   0,   0,   0,   0,   0,   5,   5,   5,   5,   5,   5, 194,   0,
      5,   5, 245,   0,   0,   0,   0,   0, 236, 246, 247, 248, 249, 250,   0,   0,
      0,  25,  85,  85,  79,   0,   0,   0,   5,   5,   5,   5,   5,   5, 138,   0,
      5, 183,   5,   5,   5,   5,   5,   5, 121,   5,   5,   5,   5,   5,   5,   5,
      5,   5,   5,   5,   5, 251,   5,   5,   5,   5,   5,   5,   5,   5,   5,  78,
    121,   0,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_alphanumeric_stage_5[] = {
      0,   0,   0,   0,   0,   0, 255,   3, 254, 255, 255,   7,   0,   4,  32,   4,
    255, 255, 127, 255, 255, 255, 255, 255, 195, 255,   3,   0,  31,  80,   0,   0,
     32,   0,   0,   0,   0,   0, 223, 188,  64, 215, 255, 255, 251, 255, 255, 255,
    255, 255, 191, 255,   3, 252, 255, 255, 255, 255, 254, 255, 255, 255, 127,   2,
    255,   1,   0,   0,   0,   0, 255, 191, 182,   0, 255, 255, 255, 135,   7,   0,
      0,   0, 255,   7, 255, 255, 255, 254, 255, 195, 255, 255, 255, 255, 239,  31,
    254, 225, 255, 159,   0,   0, 255, 255,   0, 224, 255, 255, 255, 255,   3,   0,
    255,   7,  48,   4, 255, 255, 255, 252, 255,  31,   0,   0, 255, 255, 255,   1,
    255,   7,   0,   0, 255, 255, 223,  63,   0,   0, 240, 255, 248,   3, 255, 255,
    255, 255, 255, 239, 255, 223, 225, 255, 207, 255, 254, 255, 239, 159, 249, 255,
    255, 253, 197, 227, 159,  89, 128, 176, 207, 255,   3,  16, 238, 135, 249, 255,
    255, 253, 109, 195, 135,  25,   2,  94, 192, 255,  63,   0, 238, 191, 251, 255,
    255, 253, 237, 227, 191,  27,   1,   0, 207, 255,   0,  30, 238, 159, 249, 255,
    159,  25, 192, 176, 207, 255,   2,   0, 236, 199,  61, 214,  24, 199, 255, 195,
    199,  29, 129,   0, 192, 255,   0,   0, 239, 223, 253, 255, 255, 253, 255, 227,
    223,  29,  96,   7, 207, 255,   0,   0, 255, 253, 239, 227, 223,  29,  96,  64,
    207, 255,   6,   0, 255, 255, 255, 231, 223,  93, 240, 128, 207, 255,   0, 252,
    236, 255, 127, 252, 255, 255, 251,  47, 127, 128,  95, 255, 192, 255,  12,   0,
    254, 255, 255, 255, 255, 255, 255,   7, 127,  32, 255,   3, 150,  37, 240, 254,
    174, 236, 255,  59,  95,  32, 255, 243,   1,   0,   0,   0, 255,   3,   0,   0,
    255, 254, 255, 255, 255,  31, 254, 255,   3, 255, 255, 254, 255, 255, 255,  31,
    255, 255, 127, 249, 255,   3, 255, 255, 231, 193, 255, 255, 127,  64, 255,  51,
    191,  32, 255, 255, 255, 255, 255, 247, 255,  61, 127,  61, 255,  61, 255, 255,
    255, 255,  61, 127,  61, 255, 127, 255, 255, 255,  61, 255, 255, 255, 255, 135,
    255, 255,   0,   0, 255, 255,  63,  63, 255, 159, 255, 255, 255, 199, 255,   1,
    255, 223,  15,   0, 255, 255,  15,   0, 255, 223,  13,   0, 255, 255, 207, 255,
    255,   1, 128,  16, 255,   7, 255, 255, 255, 255,  63,   0, 255, 255, 255, 127,
    255,  15, 255,   1, 192, 255, 255, 255, 255,  63,  31,   0, 255,  15, 255, 255,
    255,   3, 255,   3, 255, 255, 255,  15, 254, 255,  31,   0, 128,   0,   0,   0,
    255, 255, 239, 255, 239,  15, 255,   3, 255, 243, 255, 255, 191, 255,   3,   0,
    255, 227, 255, 255, 255, 255, 255,  63, 255,   1, 255, 255,   0, 222, 111,   0,
    128, 255,  31,   0,  63,  63, 255, 170, 255, 255, 223,  95, 220,  31, 207,  15,
    255,  31, 220,  31,   0,   0,   2, 128,   0,   0, 255,  31, 132, 252,  47,  62,
     80, 189, 255, 243, 224,  67,   0,   0,   0,   0, 192, 255, 255, 127, 255, 255,
     31, 120,  12,   0, 255, 128,   0,   0, 255, 255, 127,   0, 127, 127, 127, 127,
      0, 128,   0,   0, 224,   0,   0,   0, 254,   3,  62,  31, 255, 255, 127, 224,
    224, 255, 255, 255, 255, 127,   0,   0, 255,  31, 255, 255, 255,  15,   0,   0,
    255, 127, 240, 143,   0,   0, 128, 255, 252, 255, 255, 255, 255, 249, 255, 255,
    255, 255, 255,   3, 187, 247, 255, 255, 255,   0,   0,   0,  47,   0, 255,   3,
      0,   0, 252, 104, 255, 255,   7,   0, 255, 255, 247, 255,   0, 128, 255,   3,
    223, 255, 255, 127, 255,  63, 255,   3, 255, 255, 127, 196,   5,   0,   0,  56,
    255, 255,  60,   0, 126, 126, 126,   0, 127, 127, 255, 255,  63,   0, 255, 255,
    255,   7, 255,   3,  15,   0, 255, 255, 127, 248, 255, 255, 255,  63, 255, 255,
    127,   0, 248, 224, 255, 253, 127,  95, 219, 255, 255, 255,   0,   0, 248, 255,
    255, 255, 252, 255,   0,   0, 255,  15,   0,   0, 223, 255, 252, 252, 252,  28,
    255, 239, 255, 255, 127, 255, 255, 183, 255,  63, 255,  63, 255, 255,  31,   0,
    255, 255,   1,   0,  15, 255,  62,   0, 255, 255,  15, 255, 255,   0, 255, 255,
     15,   0,   0,   0,  63, 253, 255, 255, 255, 255, 191, 145, 255, 255,  55,   0,
    255, 255, 255, 192, 111, 240, 239, 254,  31,   0,   0,   0, 255,   0, 255,   3,
    128,   0, 255, 255,  63,   0,   0,   0, 255,   1, 255,   3, 255, 255, 199, 255,
    112,   0, 255, 255, 255, 255,  71,   0,  30,   0, 255,  23, 255, 255, 251, 255,
    255, 255, 159,  64, 127, 189, 255, 191, 159,  25, 129, 224, 187,   7, 255,   3,
    179,   0, 255,   3, 255, 255,  63, 127,   0,   0,   0,  63,  17,   0, 255,   3,
    255,   3,   0, 128, 255, 255, 231, 127, 207, 255, 255,  32, 255, 253, 255, 255,
    255, 255, 127, 127,   1,   0, 255,   3,   0,   0, 252, 255, 255, 254, 127,   0,
    127, 251, 255, 255, 255, 255, 127, 180, 203,   0, 255,   3, 191, 253, 255, 255,
    255, 127, 123,   1, 127,   0,   0,   0, 255,  63,   0,   0,  15,   0, 255,   3,
    248, 255, 255, 224,  31,   0, 255, 255,   3,   0,   0,   0, 255,   7, 255,  31,
    255,   1, 255,  67, 255, 255, 223, 255, 255, 255, 255, 223, 100, 222, 255, 235,
    239, 255, 255, 255, 191, 231, 223, 223, 255, 255, 255, 123,  95, 252, 253, 255,
     63, 255, 255, 255, 253, 255, 255, 247, 247, 207, 255, 255, 127, 255, 255, 249,
    219,   7,   0,   0, 143,   0, 255,   3, 150, 254, 247,  10, 132, 234, 150, 170,
    150, 247, 247,  94, 255, 251, 255,  15, 238, 251, 255,  15,   3,   0, 255, 255,
};

/* Alphanumeric: 2321 bytes. */

RE_UINT32 re_get_alphanumeric(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_alphanumeric_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_alphanumeric_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_alphanumeric_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_alphanumeric_stage_4[pos + f] << 5;
    pos += code;
    value = (re_alphanumeric_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Any. */

RE_UINT32 re_get_any(RE_UINT32 ch) {
    return 1;
}

/* Blank. */

static RE_UINT8 re_blank_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_blank_stage_2[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
};

static RE_UINT8 re_blank_stage_3[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1,
    3, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_blank_stage_4[] = {
    0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 3, 1, 1, 1, 1, 1, 4, 5, 1, 1, 1, 1, 1, 1,
    3, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_blank_stage_5[] = {
      0,   2,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   1,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,
    255,   7,   0,   0,   0, 128,   0,   0,   0,   0,   0, 128,   0,   0,   0,   0,
};

/* Blank: 169 bytes. */

RE_UINT32 re_get_blank(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_blank_stage_1[f] << 3;
    f = code >> 13;
    code ^= f << 13;
    pos = (RE_UINT32)re_blank_stage_2[pos + f] << 4;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_blank_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_blank_stage_4[pos + f] << 6;
    pos += code;
    value = (re_blank_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Graph. */

static RE_UINT8 re_graph_stage_1[] = {
    0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 6, 4, 8,
    4, 8,
};

static RE_UINT8 re_graph_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  9, 10, 11,  7,  7,  7,  7, 12, 13,  7,  7,  7, 14,
    15, 16, 17, 18, 19, 13, 20, 13, 21, 13, 13, 13, 13, 22,  7,  7,
    23, 24, 13, 13, 13, 13, 25, 26, 13, 13, 27, 28, 29, 30, 31, 32,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7, 33,  7, 34, 35,  7, 36,  7,  7,  7, 37, 13, 38,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
    39, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7, 40,
};

static RE_UINT8 re_graph_stage_3[] = {
      0,   1,   1,   2,   1,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,
     14,   1,  15,  16,   1,   1,  17,  18,  19,  20,  21,  22,  23,  24,   1,  25,
     26,  27,   1,   1,  28,   1,   1,   1,   1,   1,   1,  29,  30,  31,  32,  33,
     34,  35,  36,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,  37,   1,   1,   1,   1,   1,   1,   1,   1,   1,  38,
      1,   1,   1,   1,  39,   1,  40,  41,  42,  43,  44,  45,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,  46,  47,  47,  47,  47,  47,  47,  47,  47,
      1,   1,  48,  49,   1,  50,  51,  52,  53,  54,  55,  56,  57,  58,   1,  59,
     60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,
     76,  47,  77,  47,  78,  79,  80,  47,   1,   1,   1,  81,  82,  83,  47,  47,
      1,   1,   1,   1,  84,  47,  47,  47,  47,  47,  47,  47,   1,   1,  85,  47,
      1,   1,  86,  87,  47,  47,  88,  89,   1,   1,   1,   1,   1,   1,   1,  90,
      1,   1,  91,  47,  47,  47,  47,  47,   1,  92,  93,  47,  47,  47,  47,  47,
     47,  47,  47,  47,  94,  47,  47,  47,  95,  96,  97,  98,  99, 100, 101, 102,
      1,   1, 103,  47,  47,  47,  47,  47, 104,  47,  47,  47,  47,  47,  47,  47,
    105, 106,  47,  47, 107,  47, 108,  47, 109, 110, 111,   1,   1,   1, 112, 113,
    114, 115, 116,  47,  47,  47,  47,  47,   1,   1,   1,   1,   1,   1, 117,   1,
      1,   1,   1,   1,   1,   1,   1, 118, 119,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1, 120,   1,   1,   1,   1, 121,  47,  47,  47,  47,
      1,   1, 122,  47,  47,  47,  47,  47, 123,  38,  47,  47,  47,  47,  47,  47,
      1,   1,   1,   1,   1,   1,   1, 124,
};

static RE_UINT8 re_graph_stage_4[] = {
      0,   1,   2,   3,   0,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   4,   5,   6,   2,   2,   2,   7,   8,   2,   9,   2,  10,  11,
     12,   2,   2,   2,   2,   2,   2,   2,  13,   2,  14,   2,   2,  15,   2,  16,
      2,  17,  18,  19,   0,  20,  21,   2,   2,   2,   2,   2,  22,  23,  24,  25,
     26,  27,  28,  29,  30,  31,  32,  33,  34,  31,  35,  36,  37,  38,  39,  40,
     41,  42,  43,  44,  41,  45,  46,  47,  48,   2,  49,  50,  51,  52,  53,  54,
      1,  55,  56,   0,  57,  58,  59,   0,   2,   2,  60,  61,  62,  12,  63,   0,
      2,   2,   2,   2,   2,   2,  64,   2,   2,   2,  65,   2,  66,  67,  68,   2,
     69,   2,  16,  70,  71,   2,   2,  72,   2,   2,   2,   2,  73,   2,   2,  74,
     75,  76,  77,  78,   2,   2,  79,  80,  81,   2,   2,  74,   2,  82,   2,  83,
      3,  84,  85,  86,   2,  87,  88,   2,  89,   2,   3,  90,  80,  17,   0,   0,
      2,   2,  87,  70,   2,   2,   2,  91,   2,  92,  93,   2,  94,  16,  10,  71,
      2,   2,   2,   2,   2,   2,   2,  95,  72,   2,  96,  79,   2,  97,  98,  99,
    100, 101,   3, 102, 103,   2, 104, 105,   2,   2,   2,   2,  87,   2,   2,   2,
      2, 106,  19,   2,   2,   2,   2,   2,   2,   2,   2, 107, 108,   2, 109,   3,
      2, 110,   3,   2,   2,   2,   2, 111,   2,  64,   2, 112,  76, 113, 113,   2,
      2,   2, 114,   0,  95,   2,   2,  77,   2,   2,   2,   2,   2,   2,  83, 115,
      1,   2,   1,   2,   8,   2,   2,   2, 116,   7,   2,   2, 110, 117,   2, 118,
      3,   2,   2,   2,   2,   2,   2,   3,   2,   2,   2,   2,   2,  83,   2,   2,
      2,   2,   2,   2,   2,   2,   2, 119,   2,   2,   2,   2, 120,   2, 121,   2,
      2, 122,   2,   2,   2,   2,   2, 123,   2,   2,   2,   2,   2,  71,   0, 124,
      2, 125,   2, 123,   2,   2, 126,   2,   2,   2, 127,  70,   2,   2, 128,   3,
      2,  76, 129,   2,   2,   2, 130,  76, 131, 132,   2, 133,   2,   2,   2, 134,
      2,   2,   2,   2,   2, 118, 135,  56,   0,   0,   0,   0,   0,   0,   0,   0,
      2,   2,   2, 136,   2,   2,  71,   0, 137, 138, 139,   2,   2,   2, 140,   2,
      2,   2, 104,   2, 141,   2, 142, 143,  71,   2, 144, 145,   2,   2,   2,  90,
      1,   2,   2,   2,   2,   3, 146, 147, 148, 149, 150,   0,   2,   2,   2, 117,
    151, 152,   2,   2, 153, 154, 104,  79,   0,   0,   0,   0,  70,   2, 105,  56,
      2, 155,  82, 117, 156,   2, 157,   0,   2,   2,   2,   2,  79, 158, 159,  56,
      2,  10,   2, 160,   0,   0,   0,   0,   2,  76,  83, 142,   0,   0,   0,   0,
    161, 162, 163,   2,   3, 164,   0, 165, 166, 167,   0,   0,   2, 168, 141,   2,
    169, 170, 171,   2,   2,   0,   2, 172,   2, 173, 108, 174, 175, 176,   0,   0,
      2,   2, 177,   0,   2, 178,   2, 179,   2, 180,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   3,   0,   0,   0,   0,   2,  10,  71,   0,   0,   0,   0,   0,
      2,   2, 181, 182,   2,   2, 183, 184,   2,  97, 121,  76,   2,   2, 136, 185,
    186,   3,   0,   0, 187, 158,   2, 188,  22, 189, 190, 191,   0,   0,   0,   0,
      2,   2, 192,   0,   2,   2, 180,   0,   0,   0,   0,   0,   2, 108,  79,   0,
      2,   2, 193, 194,   2, 123, 195,   0,  16,  87,   0,   0,   0,   0,   0,   0,
      2,  56,   0,   0,   0,   2,   2, 196,   2,   2,  10,   2,  50, 197,   2,  74,
    109, 198, 133, 120, 141, 199,   0,   0, 200, 201, 180, 202, 203, 195,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  74,   2,   2,   2,   2,  71,   0,   0,   0,
      2,   2,   2, 204,   2,   2,   2,   2,   2,   2, 205,   0,   0,   0,   0,   0,
      2, 114,   0,   0,   0,   0,   0,   0,   2,   2, 106,   0,   0,   0,   0,   0,
      2,  74,   3, 206,   0,   0, 104, 207,   2,   2, 208, 209, 119,   0,   0,   0,
      0,   0,   2,   2, 117,   0,   0,   0,   2,   2, 210,   3, 211,   0,   0, 212,
      2,   2,   2,   2,   2,   2,   2,  15,   2,   2,   2,   2,   2,   2,   2, 178,
      3,   0,   0, 104,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,  56,
      2,   2,   2, 213, 214, 205,   0,   0,   2,   2,   2,   2,   2,   2,   2,  83,
      2, 215,   2,   2,   2,   2,   2, 177,   2,   2, 216,   0,   0,   0,   0,  77,
      2,   2,  76,  74,   0,   0,   0,   0,   2,   2,  97,   2,  12, 217, 218,   2,
    219, 220, 221,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2, 222,   2,   2,
      2,   2,   2,   2,   2,   2, 223,   2,   2,   2,   2,   2, 224, 225,   0,   0,
    226, 227,   0,   0,   0,   0,   0,   0,   2,   2,   2,   2,   2,   2, 228,   0,
      2,   2, 229,   0,   0,   0,   0,   0,   0,   0,   0, 230,   2, 231,   0,   0,
    218, 232, 233, 234, 235, 236,   0, 237,   2,  87,   2,   2,  77, 238, 239,  83,
    120,   2,   2,  87,   2, 194,   0, 240, 241,  56, 242, 216,   0,   0,   0,   0,
      2,   2,   2,   2,   2,   2, 231, 243,   2,   2,   2,  77,   2,   2,  74,   0,
     87,   2, 180,   2,  10, 244,   0,   0,  87,   3,   2, 245,   2, 246, 241,   2,
      0,   0,   0, 244,   0,   0,   0,   0,   2,   2,   2,   2,   2,   2,  76,   0,
      2, 231,   2,   2,   2,   2,   2,   2,  79,   2,   2,   2,   2,   2,   2,   2,
      2,   2,   2,   2,   2, 247,   2,   2,   2,   2,   2,   2,   2,   2,   2, 154,
     79,   0,   0,   0,   0,   0,   0,   0, 248,   2,   2,   2,   0,   0,   0,   0,
      2,   2,   2,   2,   2,   2,   2,  79,
};

static RE_UINT8 re_graph_stage_5[] = {
      0,   0,   0,   0, 254, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127,
    255, 255, 255, 252, 240, 215, 255, 255, 251, 255, 255, 255, 255, 255, 254, 255,
    255, 255, 127, 254, 255, 231, 254, 255, 255,   0, 255, 255, 255, 135,  31,   0,
    255, 255, 255, 223, 255, 191, 255, 255, 255, 231, 255, 255, 255, 255,   3,   0,
    255, 255, 255, 231, 255,  63, 255, 127, 255, 255, 255,  79, 255,   7,   0,   0,
    255, 255, 223,  63,   0,   0, 248, 255, 239, 159, 249, 255, 255, 253, 197, 243,
    159, 121, 128, 176, 207, 255, 255, 127, 238, 135, 249, 255, 255, 253, 109, 211,
    135,  57,   2,  94, 192, 255, 127,   0, 238, 191, 251, 255, 255, 253, 237, 243,
    191,  59,   1,   0, 207, 255,   3, 254, 238, 159, 249, 255, 159,  57, 192, 176,
    207, 255, 255,   0, 236, 199,  61, 214,  24, 199, 255, 195, 199,  61, 129,   0,
    192, 255, 255,   7, 255, 223, 253, 255, 255, 253, 255, 227, 223,  61,  96,   7,
    207, 255,   0, 255, 255, 253, 239, 243, 223,  61,  96,  64, 207, 255,   6,   0,
    239, 223, 253, 255, 223, 253, 240, 255, 207, 255, 255, 255, 236, 255, 127, 252,
    255, 255, 251,  47, 127, 132,  95, 255, 192, 255,  28,   0, 255, 255, 255, 135,
    255, 255, 255,  15, 150,  37, 240, 254, 174, 236, 255,  59,  95,  63, 255, 243,
    255, 254, 255, 255, 255,  31, 254, 255, 255, 255, 255, 254, 255, 223, 255,   7,
    191,  32, 255, 255, 255,  61, 127,  61, 255,  61, 255, 255, 255, 255,  61, 127,
     61, 255, 127, 255, 255, 255,  61, 255, 255, 255, 255,  31, 255, 255, 255,   3,
    255, 255,  63,  63, 254, 255, 255,  31, 255, 255, 255,   1, 255, 223,  31,   0,
    255, 255, 127,   0, 255, 255,  15,   0, 255, 223,  13,   0, 255, 255, 255,  63,
    255,   3, 255,   3, 255, 127, 255,   3, 255,   7, 255, 255, 255, 255,  63,   0,
    255,  15, 255,  15, 241, 255, 255, 255, 255,  63,  31,   0, 255,  15, 255, 255,
    255,   3, 255, 199, 255, 255, 255, 207, 255, 255, 255, 159, 255, 255,  15, 240,
    255, 255, 255, 248, 255, 227, 255, 255, 255,   1, 255, 255, 255, 255, 255, 251,
     63,  63, 255, 170, 255, 255, 223, 255, 223, 255, 207, 239, 255, 255, 220, 127,
      0, 248, 255, 255, 255, 124, 255, 255, 223, 255, 243, 255, 255, 127, 255,  31,
      0,   0, 255, 255, 255, 255,   1,   0, 127,   0,   0,   0, 255, 255, 207, 255,
    255, 255,  63, 255, 255, 253, 255, 255, 255, 127, 255, 255, 255, 255,  15, 254,
    255, 128,   1, 128, 127, 127, 127, 127, 255, 127,   0,   0,   0,   0, 255,  15,
    224, 255, 255, 255, 255, 255, 255,   7,  15,   0, 255, 255, 255, 255,   0,   0,
    255,  31, 255, 255, 127,   0, 255, 255, 255,  15,   0,   0, 255, 255, 255,   0,
      0,   0, 128, 255, 255,  15, 255,   3,  63, 192, 255,   3, 255, 255,  15, 128,
    255, 191, 255, 195, 255,  63, 255, 243,   7,   0,   0, 248, 126, 126, 126,   0,
    127, 127, 255, 255,  63,   0, 255, 255, 255,  63, 255,   3, 127, 248, 255, 255,
    255,  63, 255, 255, 127,   0, 248, 224, 255, 255, 127,  95, 219, 255, 255, 255,
      3,   0, 248, 255, 255, 255, 252, 255, 255,   0,   0,   0,   0,   0, 255,  63,
    255, 255, 247, 255, 127,  15, 223, 255, 252, 252, 252,  28, 127, 127,   0,  62,
    255, 239, 255, 255, 127, 255, 255, 183, 255,  63, 255,  63, 135, 255, 255, 255,
    255, 255, 143, 255, 255, 127, 255,  15,   1,   0,   0,   0,  15, 224, 255, 255,
    255, 255, 255, 191,  15, 255,  63,   0, 255,   3, 255, 255, 255, 255,  15, 255,
     15, 128,   0,   0,  63, 253, 255, 255, 255, 255, 191, 145, 255, 255, 191, 255,
    128, 255,   0,   0, 255, 255,  55, 248, 255, 255, 255, 143, 255, 255, 255, 131,
    255, 255, 255, 240, 111, 240, 239, 254, 255, 255,  63, 135, 255,   1, 255,   1,
    127, 248, 127,   0, 255, 255,  63, 254, 255, 255,   7, 255, 255, 255,   3,  30,
      0, 254,   0,   0, 255,   1,   0,   0, 255, 255,   7,   0, 255, 255,   7, 252,
    255,   0, 255,   3, 255,  63, 252, 255, 255, 255,   0, 128,   3,  32, 255, 255,
    255,   1, 255,   3, 254, 255,  31,   0, 255, 255, 251, 255, 127, 189, 255, 191,
    255,   7, 255,   3, 255, 253, 237, 251, 159,  57, 129, 224, 207,  31,  31,   0,
    255, 255, 255, 107,  31,   0, 255,   3, 255,  31,   0,   0, 255,   3,   0,   0,
    255, 255,   7, 128,   7,   0,   0,   0, 255, 255, 127, 255, 255, 254, 127,   0,
    127, 251, 255, 255, 255, 255, 127, 180, 191, 253, 255, 255, 255, 127, 251,   1,
    255, 127,  31,   0,  15,   0,   0,   0, 255, 195,   0,   0, 255,  63,  63,   0,
     63,   0, 255, 251, 251, 255, 255, 224,  31,   0, 255, 255,   0, 128, 255, 255,
      3,   0,   0,   0, 255,   7, 255,  31, 255,   1, 255, 243, 127, 254, 255, 255,
     63,   0,   0,   0, 100, 222, 255, 235, 239, 255, 255, 255, 191, 231, 223, 223,
    255, 255, 255, 123,  95, 252, 253, 255,  63, 255, 255, 255, 255, 207, 255, 255,
    255,  15,   0, 248, 254, 255,   0,   0, 127, 255, 255, 249, 219,   7,   0,   0,
    159, 255, 127,   0, 255,   7, 255, 195,   0,   0, 254, 255, 255, 255,  31,   0,
    150, 254, 247,  10, 132, 234, 150, 170, 150, 247, 247,  94, 255, 251, 255,  15,
    238, 251, 255,  15,   0,   0,   3,   0, 255, 127, 254, 255, 254, 255, 254, 255,
    192, 255, 255, 255,   7,   0, 255, 255, 255,   1,   3,   0, 255,  31, 255,   3,
    255,  63,   0,   0, 255, 255, 121, 244,   7,   0, 255,   3,   3,   0, 255, 255,
      2,   0,   0,   0,
};

/* Graph: 2502 bytes. */

RE_UINT32 re_get_graph(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_graph_stage_1[f] << 4;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_graph_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_graph_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_graph_stage_4[pos + f] << 5;
    pos += code;
    value = (re_graph_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Print. */

static RE_UINT8 re_print_stage_1[] = {
    0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 6, 4, 8,
    4, 8,
};

static RE_UINT8 re_print_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  9, 10, 11,  7,  7,  7,  7, 12, 13,  7,  7,  7, 14,
    15, 16, 17, 18, 19, 13, 20, 13, 21, 13, 13, 13, 13, 22,  7,  7,
    23, 24, 13, 13, 13, 13, 25, 26, 13, 13, 27, 28, 29, 30, 31, 32,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7, 33,  7, 34, 35,  7, 36,  7,  7,  7, 37, 13, 38,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
    39, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7, 40,
};

static RE_UINT8 re_print_stage_3[] = {
      0,   1,   1,   2,   1,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,
     14,   1,  15,  16,   1,   1,  17,  18,  19,  20,  21,  22,  23,  24,   1,  25,
     26,  27,   1,   1,  28,   1,   1,   1,   1,   1,   1,  29,  30,  31,  32,  33,
     34,  35,  36,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,  37,   1,   1,   1,   1,   1,   1,   1,   1,   1,  38,
      1,   1,   1,   1,  39,   1,  40,  41,  42,  43,  44,  45,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,  46,  47,  47,  47,  47,  47,  47,  47,  47,
      1,   1,  48,  49,   1,  50,  51,  52,  53,  54,  55,  56,  57,  58,   1,  59,
     60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,
     76,  47,  77,  47,  78,  79,  80,  47,   1,   1,   1,  81,  82,  83,  47,  47,
      1,   1,   1,   1,  84,  47,  47,  47,  47,  47,  47,  47,   1,   1,  85,  47,
      1,   1,  86,  87,  47,  47,  88,  89,   1,   1,   1,   1,   1,   1,   1,  90,
      1,   1,  91,  47,  47,  47,  47,  47,   1,  92,  93,  47,  47,  47,  47,  47,
     47,  47,  47,  47,  94,  47,  47,  47,  95,  96,  97,  98,  99, 100, 101, 102,
      1,   1, 103,  47,  47,  47,  47,  47, 104,  47,  47,  47,  47,  47,  47,  47,
    105, 106,  47,  47, 107,  47, 108,  47, 109, 110, 111,   1,   1,   1, 112, 113,
    114, 115, 116,  47,  47,  47,  47,  47,   1,   1,   1,   1,   1,   1, 117,   1,
      1,   1,   1,   1,   1,   1,   1, 118, 119,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1, 120,   1,   1,   1,   1, 121,  47,  47,  47,  47,
      1,   1, 122,  47,  47,  47,  47,  47, 123,  38,  47,  47,  47,  47,  47,  47,
      1,   1,   1,   1,   1,   1,   1, 124,
};

static RE_UINT8 re_print_stage_4[] = {
      0,   1,   1,   2,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   3,   4,   5,   1,   1,   1,   6,   7,   1,   8,   1,   9,  10,
     11,   1,   1,   1,   1,   1,   1,   1,  12,   1,  13,   1,   1,  14,   1,  15,
      1,  16,  17,  18,   0,  19,  20,   1,   1,   1,   1,   1,  21,  22,  23,  24,
     25,  26,  27,  28,  29,  30,  31,  32,  33,  30,  34,  35,  36,  37,  38,  39,
     40,  41,  42,  43,  40,  44,  45,  46,  47,   1,  48,  49,  50,  51,  52,  53,
     54,  55,  56,   0,  57,  58,  59,   0,   1,   1,  60,  61,  62,  11,  63,   0,
      1,   1,   1,   1,   1,   1,  64,   1,   1,   1,  65,   1,  66,  67,  68,   1,
     69,   1,  15,  70,  71,   1,   1,  72,   1,   1,   1,   1,  70,   1,   1,  73,
     74,  75,  76,  77,   1,   1,  78,  79,  80,   1,   1,  73,   1,  81,   1,  82,
      2,  83,  84,  85,   1,  86,  87,   1,  88,   1,   2,  89,  79,  16,   0,   0,
      1,   1,  86,  70,   1,   1,   1,  90,   1,  91,  92,   1,  93,  15,   9,  71,
      1,   1,   1,   1,   1,   1,   1,  94,  72,   1,  95,  78,   1,  96,  97,  98,
      1,  99,   1, 100, 101,   1, 102, 103,   1,   1,   1,   1,  86,   1,   1,   1,
      1, 104,  18,   1,   1,   1,   1,   1,   1,   1,   1, 105, 106,   1, 107,   2,
      1, 108,   2,   1,   1,   1,   1, 109,   1,  64,   1, 110,  75, 111, 111,   1,
      1,   1, 112,   0,  94,   1,   1,  76,   1,   1,   1,   1,   1,   1,  82, 113,
      1,   1,  54,   1,   7,   1,   1,   1, 114,   6,   1,   1, 108, 115,   1, 116,
      2,   1,   1,   1,   1,   1,   1,   2,   1,   1,   1,   1,   1,  82,   1,   1,
      1,   1,   1,   1,   1,   1,   1, 117,   1,   1,   1,   1, 118,   1, 119,   1,
      1, 120,   1,   1,   1,   1,   1, 121,   1,   1,   1,   1,   1,  71,   0, 122,
      1, 123,   1, 121,   1,   1, 124,   1,   1,   1, 125,  70,   1,   1, 126,   2,
      1,  75, 127,   1,   1,   1, 128,  75, 129, 130,   1, 131,   1,   1,   1, 132,
      1,   1,   1,   1,   1, 116, 133,  56,   0,   0,   0,   0,   0,   0,   0,   0,
      1,   1,   1, 134,   1,   1,  71,   0, 135, 136, 137,   1,   1,   1, 138,   1,
      1,   1, 102,   1, 139,   1, 140, 141,  71,   1, 142, 143,   1,   1,   1,  89,
     54,   1,   1,   1,   1,   2, 144, 145, 146, 147, 148,   0,   1,   1,   1, 115,
    149, 150,   1,   1, 151, 152, 102,  78,   0,   0,   0,   0,  70,   1, 103,  56,
      1, 153,  81, 115, 154,   1, 155,   0,   1,   1,   1,   1,  78, 156, 157,  56,
      1,   9,   1, 158,   0,   0,   0,   0,   1,  75,  82, 140,   0,   0,   0,   0,
    159, 160, 161,   1,   2, 162,   0, 163, 164, 165,   0,   0,   1, 166, 139,   1,
    167, 168, 169,   1,   1,   0,   1, 170,   1, 171, 106, 172, 173, 174,   0,   0,
      1,   1, 175,   0,   1, 176,   1, 177,   1, 178,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   2,   0,   0,   0,   0,   1,   9,  71,   0,   0,   0,   0,   0,
      1,   1, 179, 180,   1,   1, 181, 182,   1,  96, 119,  75,   1,   1, 134, 183,
    184,   2,   0,   0, 185, 156,   1, 186,  21, 187, 188, 189,   0,   0,   0,   0,
      1,   1, 190,   0,   1,   1, 178,   0,   0,   0,   0,   0,   1, 106,  78,   0,
      1,   1, 191, 192,   1, 121, 193,   0,  15,  86,   0,   0,   0,   0,   0,   0,
      1,  56,   0,   0,   0,   1,   1, 194,   1,   1,   9,   1,  49, 195,   1,  73,
    107, 196, 131, 118, 139, 197,   0,   0, 198, 199, 178, 200, 201, 193,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  73,   1,   1,   1,   1,  71,   0,   0,   0,
      1,   1,   1, 202,   1,   1,   1,   1,   1,   1, 203,   0,   0,   0,   0,   0,
      1, 112,   0,   0,   0,   0,   0,   0,   1,   1, 104,   0,   0,   0,   0,   0,
      1,  73,   2, 204,   0,   0, 102, 205,   1,   1, 206, 207, 117,   0,   0,   0,
      0,   0,   1,   1, 115,   0,   0,   0,   1,   1, 208,   2, 209,   0,   0, 210,
      1,   1,   1,   1,   1,   1,   1,  14,   1,   1,   1,   1,   1,   1,   1, 176,
      2,   0,   0, 102,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,  56,
      1,   1,   1, 211, 212, 203,   0,   0,   1,   1,   1,   1,   1,   1,   1,  82,
      1, 213,   1,   1,   1,   1,   1, 175,   1,   1, 214,   0,   0,   0,   0,  76,
      1,   1,  75,  73,   0,   0,   0,   0,   1,   1,  96,   1,  11, 215, 216,   1,
    217, 218, 219,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 220,   1,   1,
      1,   1,   1,   1,   1,   1, 221,   1,   1,   1,   1,   1, 222, 223,   0,   0,
    224, 225,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1, 226,   0,
      1,   1, 227,   0,   0,   0,   0,   0,   0,   0,   0, 228,   1, 229,   0,   0,
    216, 230, 231, 232, 233, 234,   0, 235,   1,  86,   1,   1,  76, 236, 237,  82,
    118,   1,   1,  86,   1, 192,   0, 238, 239,  56, 240, 214,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1, 229, 241,   1,   1,   1,  76,   1,   1,  73,   0,
     86,   1, 178,   1,   9, 242,   0,   0,  86,   2,   1, 243,   1, 244, 239,   1,
      0,   0,   0, 242,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,  75,   0,
      1, 229,   1,   1,   1,   1,   1,   1,  78,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1, 245,   1,   1,   1,   1,   1,   1,   1,   1,   1, 152,
     78,   0,   0,   0,   0,   0,   0,   0, 246,   1,   1,   1,   0,   0,   0,   0,
      1,   1,   1,   1,   1,   1,   1,  78,
};

static RE_UINT8 re_print_stage_5[] = {
      0,   0,   0,   0, 255, 255, 255, 255, 255, 255, 255, 127, 255, 255, 255, 252,
    240, 215, 255, 255, 251, 255, 255, 255, 255, 255, 254, 255, 255, 255, 127, 254,
    255, 231, 254, 255, 255,   0, 255, 255, 255, 135,  31,   0, 255, 255, 255, 223,
    255, 191, 255, 255, 255, 231, 255, 255, 255, 255,   3,   0, 255, 255, 255, 231,
    255,  63, 255, 127, 255, 255, 255,  79, 255,   7,   0,   0, 255, 255, 223,  63,
      0,   0, 248, 255, 239, 159, 249, 255, 255, 253, 197, 243, 159, 121, 128, 176,
    207, 255, 255, 127, 238, 135, 249, 255, 255, 253, 109, 211, 135,  57,   2,  94,
    192, 255, 127,   0, 238, 191, 251, 255, 255, 253, 237, 243, 191,  59,   1,   0,
    207, 255,   3, 254, 238, 159, 249, 255, 159,  57, 192, 176, 207, 255, 255,   0,
    236, 199,  61, 214,  24, 199, 255, 195, 199,  61, 129,   0, 192, 255, 255,   7,
    255, 223, 253, 255, 255, 253, 255, 227, 223,  61,  96,   7, 207, 255,   0, 255,
    255, 253, 239, 243, 223,  61,  96,  64, 207, 255,   6,   0, 239, 223, 253, 255,
    223, 253, 240, 255, 207, 255, 255, 255, 236, 255, 127, 252, 255, 255, 251,  47,
    127, 132,  95, 255, 192, 255,  28,   0, 254, 255, 255, 255, 255, 255, 255, 135,
    255, 255, 255,  15, 150,  37, 240, 254, 174, 236, 255,  59,  95,  63, 255, 243,
    255, 254, 255, 255, 255,  31, 254, 255, 255, 255, 255, 254, 255, 223, 255,   7,
    191,  32, 255, 255, 255,  61, 127,  61, 255,  61, 255, 255, 255, 255,  61, 127,
     61, 255, 127, 255, 255, 255,  61, 255, 255, 255, 255,  31, 255, 255, 255,   3,
    255, 255,  63,  63, 255, 255, 255,   1, 255, 223,  31,   0, 255, 255, 127,   0,
    255, 255,  15,   0, 255, 223,  13,   0, 255, 255, 255,  63, 255,   3, 255,   3,
    255, 127, 255,   3, 255,   7, 255, 255, 255, 255,  63,   0, 255,  15, 255,  15,
    241, 255, 255, 255, 255,  63,  31,   0, 255,  15, 255, 255, 255,   3, 255, 199,
    255, 255, 255, 207, 255, 255, 255, 159, 255, 255,  15, 240, 255, 255, 255, 248,
    255, 227, 255, 255, 255,   1, 255, 255, 255, 255, 255, 251,  63,  63, 255, 170,
    255, 255, 223, 255, 223, 255, 207, 239, 255, 255, 220, 127, 255, 252, 255, 255,
    223, 255, 243, 255, 255, 127, 255,  31,   0,   0, 255, 255, 255, 255,   1,   0,
    127,   0,   0,   0, 255, 255, 207, 255, 255, 255,  63, 255, 255, 253, 255, 255,
    255, 127, 255, 255, 255, 255,  15, 254, 255, 128,   1, 128, 127, 127, 127, 127,
    255, 127,   0,   0,   0,   0, 255,  15, 224, 255, 255, 255, 255, 255, 255,   7,
     15,   0, 255, 255, 255, 255,   0,   0, 255,  31, 255, 255, 127,   0, 255, 255,
    255,  15,   0,   0, 255, 255, 255,   0,   0,   0, 128, 255, 255,  15, 255,   3,
     63, 192, 255,   3, 255, 255,  15, 128, 255, 191, 255, 195, 255,  63, 255, 243,
      7,   0,   0, 248, 126, 126, 126,   0, 127, 127, 255, 255,  63,   0, 255, 255,
    255,  63, 255,   3, 127, 248, 255, 255, 255,  63, 255, 255, 127,   0, 248, 224,
    255, 255, 127,  95, 219, 255, 255, 255,   3,   0, 248, 255, 255, 255, 252, 255,
    255,   0,   0,   0,   0,   0, 255,  63, 255, 255, 247, 255, 127,  15, 223, 255,
    252, 252, 252,  28, 127, 127,   0,  62, 255, 239, 255, 255, 127, 255, 255, 183,
    255,  63, 255,  63, 135, 255, 255, 255, 255, 255, 143, 255, 255, 127, 255,  15,
      1,   0,   0,   0,  15, 224, 255, 255, 255, 255, 255, 191,  15, 255,  63,   0,
    255,   3, 255, 255, 255, 255,  15, 255,  15, 128,   0,   0,  63, 253, 255, 255,
    255, 255, 191, 145, 255, 255, 191, 255, 128, 255,   0,   0, 255, 255,  55, 248,
    255, 255, 255, 143, 255, 255, 255, 131, 255, 255, 255, 240, 111, 240, 239, 254,
    255, 255,  63, 135, 255,   1, 255,   1, 127, 248, 127,   0, 255, 255,  63, 254,
    255, 255,   7, 255, 255, 255,   3,  30,   0, 254,   0,   0, 255,   1,   0,   0,
    255, 255,   7,   0, 255, 255,   7, 252, 255,   0, 255,   3, 255,  63, 252, 255,
    255, 255,   0, 128,   3,  32, 255, 255, 255,   1, 255,   3, 254, 255,  31,   0,
    255, 255, 251, 255, 127, 189, 255, 191, 255,   7, 255,   3, 255, 253, 237, 251,
    159,  57, 129, 224, 207,  31,  31,   0, 255, 255, 255, 107,  31,   0, 255,   3,
    255,  31,   0,   0, 255,   3,   0,   0, 255, 255,   7, 128,   7,   0,   0,   0,
    255, 255, 127, 255, 255, 254, 127,   0, 127, 251, 255, 255, 255, 255, 127, 180,
    191, 253, 255, 255, 255, 127, 251,   1, 255, 127,  31,   0,  15,   0,   0,   0,
    255, 195,   0,   0, 255,  63,  63,   0,  63,   0, 255, 251, 251, 255, 255, 224,
     31,   0, 255, 255,   0, 128, 255, 255,   3,   0,   0,   0, 255,   7, 255,  31,
    255,   1, 255, 243, 127, 254, 255, 255,  63,   0,   0,   0, 100, 222, 255, 235,
    239, 255, 255, 255, 191, 231, 223, 223, 255, 255, 255, 123,  95, 252, 253, 255,
     63, 255, 255, 255, 255, 207, 255, 255, 255,  15,   0, 248, 254, 255,   0,   0,
    127, 255, 255, 249, 219,   7,   0,   0, 159, 255, 127,   0, 255,   7, 255, 195,
      0,   0, 254, 255, 255, 255,  31,   0, 150, 254, 247,  10, 132, 234, 150, 170,
    150, 247, 247,  94, 255, 251, 255,  15, 238, 251, 255,  15,   0,   0,   3,   0,
    255, 127, 254, 255, 254, 255, 254, 255, 192, 255, 255, 255,   7,   0, 255, 255,
    255,   1,   3,   0, 255,  31, 255,   3, 255,  63,   0,   0, 255, 255, 121, 244,
      7,   0, 255,   3,   3,   0, 255, 255,   2,   0,   0,   0,
};

/* Print: 2494 bytes. */

RE_UINT32 re_get_print(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 15;
    code = ch ^ (f << 15);
    pos = (RE_UINT32)re_print_stage_1[f] << 4;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_print_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_print_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_print_stage_4[pos + f] << 5;
    pos += code;
    value = (re_print_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Word. */

static RE_UINT8 re_word_stage_1[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
     3,  3,  3,  3,  3, 16, 17, 18, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    20, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
    19, 19, 19, 19, 19, 19, 19, 19,
};

static RE_UINT8 re_word_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
    16, 17, 18, 17, 17, 17, 19, 20, 21, 17, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 24,
    22, 22, 25, 26, 27, 28, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 29, 17, 17, 17, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 30, 31, 32, 33,
    34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
    22, 50, 51, 17, 17, 17, 17, 17, 22, 22, 52, 17, 17, 17, 17, 17,
    17, 17, 22, 53, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
    17, 17, 17, 17, 22, 54, 17, 55, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 56, 22, 57, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 58, 59, 17, 17, 17, 17, 60, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 61, 62, 63, 64, 17, 65, 17, 17,
    66, 17, 17, 17, 67, 17, 17, 68, 69, 17, 17, 17, 17, 17, 17, 17,
    22, 22, 22, 70, 22, 22, 22, 22, 22, 22, 22, 71, 72, 22, 22, 22,
    22, 22, 22, 22, 22, 22, 22, 73, 22, 22, 22, 22, 22, 22, 22, 22,
    22, 22, 22, 22, 22, 74, 17, 17, 17, 17, 17, 17, 22, 75, 17, 17,
    17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
    76, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
};

static RE_UINT8 re_word_stage_3[] = {
      0,   1,   2,   3,   4,   4,   4,   4,   4,   4,   4,   5,   4,   6,   7,   8,
      4,   4,   9,   4,  10,  11,  12,  13,  14,  15,   4,  16,  17,  18,  19,  20,
     21,  22,  23,  24,   4,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,
     36,  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,
      4,  52,  53,  54,   4,   4,   4,   4,   4,  55,  56,  57,  58,  59,  60,  61,
     62,   4,   4,   4,   4,   4,   4,   4,   4,  63,  64,  65,  66,  67,   4,  68,
     69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,   4,  81,   4,  82,
     83,  84,  85,  86,   4,   4,   4,  87,   4,   4,   4,   4,  88,  89,  90,  91,
     92,  93,  94,  95,  96,  97,  98,  80,  80,  80,  80,  80,  80,  80,  80,  80,
     80,  80,  99, 100,  80,  80,  80,  80, 101, 102,   4, 103, 104, 105, 106, 107,
    108,  80,  80,  80,  80,  80,  80,  80, 109,  62, 110, 111, 112,   4, 113, 114,
      4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,  72,  80,
      4,   4,   4,   4,   4,   4,   4, 115,   4,   4, 116, 117,   4,   4,   4,   4,
    118, 119,   4,  19, 120,   4, 121, 122, 123,  82,   4, 124, 125, 126,   4, 127,
    128, 129,   4, 130, 131, 132,   4, 133,   4,   4,   4,   4,   4,   4, 134, 135,
     80,  80,  80,  80,   4,   4,   4,   4,   4, 125,   4, 136, 137, 138,  19, 139,
      4,   4,   4,   4, 140,  17, 141, 142, 143, 144,   4, 145, 146, 147, 148, 149,
    150, 151,   4, 152,  80, 153,  80, 154,  80,  80, 155, 156, 157, 158,  53, 159,
      4,   4, 160, 161, 162, 163,  80,  80,   4,   4,   4,   4, 128, 164,  80,  80,
    165, 166, 167, 168, 169,  80, 170,  80, 171, 172, 173, 174,  72, 175, 176,  80,
      4,  98, 177, 177, 178,  80,  80,  80,  80,  80,  80,  80, 179, 180,  80,  80,
      4, 181, 152, 182, 183, 184,   4, 185, 186,  80, 187, 188, 189, 190,  80,  80,
      4, 191,   4, 192,  80,  80, 193, 194,   4, 195,  83, 196, 197,  80,  80,  80,
    152,  80, 198, 199,  80,  80,  80,  80, 148, 200, 201,  70,  80,  80,  80,  80,
    202, 203, 204,  80, 205, 206, 207,  80,  80,  80,  80, 208,  80,  80,  80,  80,
      4,   4,   4,   4,   4,   4, 136,  80,   4, 209,   4,   4,   4, 210,  80,  80,
    209,  80,  80,  80,  80,  80,  80,  80,   4, 211,  80,  80,  80,  80,  80,  80,
     70, 212,  80, 213, 128, 214, 215,  80,  80,   4,  80,  80,   4, 216, 217, 218,
      4,   4,   4,   4,   4,   4,   4,  19,   4,   4,   4, 177,  80,  80,  80,  80,
      4,   4,   4,   4, 167, 114,   4,   4,   4,   4,   4, 219,  80,  80,  80,  80,
      4, 220, 221,  80,  80,  80,  80,  80,  80,  80,  80,  80,  80, 222, 223,  80,
     80, 224,  80,  80,  80,  80,  80,  80,   4, 225, 226, 227, 228, 229,   4,   4,
      4,   4, 230, 231, 232, 233, 234, 235, 236, 237, 238,  80,  80,  80,  80,  80,
    239,  80,  80,  80,  80,  80,  80,  80,   4,   4,   4, 240,   4, 241,  80,  80,
    242, 243, 244,  80,  80,  80,  80,  80,  80,  80,  80,  80, 114, 245, 196,  80,
      4,   4,   4, 246,   4,   4,   4,   4,   4,   4,   4,   4, 153,   4,   4,   4,
     53,   4,   4,   4,   4,   4,   4,   4,   4,   4, 247,   4,   4,   4,   4,   4,
      4,   4,   4,   4,   4,   4,   4, 248, 249,  80,  80,  80,  80,  80,  80,  80,
     80,  80,  80,  80,   4,   4,   4, 115,
};

static RE_UINT8 re_word_stage_4[] = {
      0,   0,   0,   1,   2,   3,   2,   4,   0,   0,   5,   6,   7,   8,   7,   8,
      7,   7,   7,   7,   9,  10,  11,   0,   7,   7,   7,  12,  13,   7,  14,   7,
      7,   7,   7,  15,  14,   7,   7,   7,   7,   7,   7,   2,   7,  16,   7,   7,
     17,   2,   7,  18,  19,   7,   3,  20,   0,   4,   7,   7,   7,   7,  21,   7,
      7,  22,  23,  24,   0,   7,   7,   7,  25,   7,   7,   7,   7,   7,   7,  10,
      7,   7,   7,  26,   7,   7,  27,   0,   7,  28,   4,   0,   0,   0,   7,  29,
      0,  30,  14,   7,   7,   7,  31,   2,  22,  32,  23,  33,  34,  35,  31,  36,
     37,  32,  23,  38,  39,  40,  41,  42,  43,  14,  23,  44,  45,  46,  31,  47,
     48,  32,  23,  44,  49,  50,  31,  51,  52,  53,  54,  21,  55,  56,  41,   0,
     57,  58,  23,  59,  60,  61,  31,   0,  62,  58,  23,  63,  60,  64,  31,  65,
     62,  58,   7,   7,  66,  67,  31,  68,  69,  70,   7,  71,  72,  73,  41,  74,
      2,   7,   7,   4,  75,   1,   0,   0,  76,  77,  78,  79,  80,  81,   0,   0,
     46,  82,   1,  83,  84,   7,  85,   2,  86,  84,   7,  85,  87,   0,   0,   0,
      1,   7,   7,   7,   7,  27,   7,   7,  88,   7,   7,  89,  90,  91,   7,   7,
     90,   7,   7,  92,  93,   8,   7,   7,   7,  93,   7,   7,   7,  25,   0,   0,
      7,   0,   7,   7,   7,   7,   7,  94,   2,   7,   7,   7,   7,   7,  24,   7,
      2,   4,   7,   7,   7,   7,  95,  17,  57,  96,   7,  96,   7,  97,  57,  98,
      7,  99,   1,   0, 100,   1,   7,   7,   7,   7,   7,  17,   7,   7,   4,   7,
      7,   7,   7,  42,   7,  75,  28,  28,  41,   7,  27,  96,   7,   7,  28,   7,
      1,   1,   0,   0,   7,  28,   7,   7,   7,  75,   7,  24,   1,   1, 101,  75,
      0,   0,   0,   0,  28,   1, 102,  97,   7,   7,   7,  97,   7,   7,   7, 103,
     59,   7,   7,  27,  17,   7,   7,  25,   0, 104,   7,   1,   7,   7,   7, 105,
      7,  94,   7,   7,  94, 106,   7,  27,   7,   7,   7, 107, 108, 109,  85, 108,
    110,   0,   0, 111,  46, 112,   0, 113,   0,  85,   0,   0,   0,   7,   7,  46,
    114, 115, 116,  81, 117,   0,   7,   7,  17,   0,   0,   0,   0,   0,   0,  41,
      7,   7,   1,   0,   7,   7,  75,   7,   7,  75,   7,   7,   7,   7, 118,  97,
      7,   7,  88,   7,   7,   7, 119, 111,   7, 120, 121, 121, 121, 121,   7,   7,
      0,   0, 111,   0, 122,   0,   2, 123,   7, 124,   2,   7,   7,   7,   7,  89,
    125,   7,   7,   2,  75,   0,   7,   4,   0,   0,   0,   7,   7,   7,   7,   0,
     85,   0,   0,   0,   0,   7,   7,  27,  85,   7,  28,   0,   7,   7,   7, 126,
      0, 127, 128,   7, 129,   7,   7,   1,   0,   0,   0, 127,   7,   7, 103,   0,
     42,   1,   7, 130,   7,   7,  27,   7,   7,  97,   7,  85, 131,   1,   7,  75,
      7,   7,   7, 120,  27,   1,   7,  70,  20, 100,   7, 132, 133, 134, 121,   7,
      7,  89,  42,   7,   7,   7, 135,   1,   7,   7,  97,   7, 136,   7,   7,  28,
      7,   1,   0,   0, 120, 137,  23, 138, 139,   7,   7,   7,   0,  30,   7,   7,
      7,   7,   7,  27,   7, 128,   7,   7, 103,   0,   0,  28,   7,   0,   7, 140,
    141,   0,   0,  86,   7,   7,   7,  85,   0,   1,   2,   3,   2,   4,  41,   7,
      7,   7,   7,  75, 142, 143,   0,   0, 144,   7,   8, 145,  27,  27,   0,   0,
      7,   7,   7,   4,   7,   7,   7,  96,   0,   0,   0, 146,   7,  85,   7,   7,
      7,  46,  46,   0,   7,   7, 141,   7,   4,   7,   7,   4, 147, 148,   0,   0,
      7,  27,   1,   7,   7, 147,   7,  28,   7,   7, 103,   7,   7,   7,  97,   0,
      7,  42, 103,   0, 149,   7,   7, 150,   7,  42,   7, 120,   7,  75,   0,   0,
      0,   0,   7, 151,   7,  42,   7,   1,   7,   7,   7, 152, 153, 154,   7, 155,
      0,   0,   7,  85,   7,  85,   0,   0,  84,   7, 120,   0,   7,  42,   7,  20,
      7,  10,   0,   0,   7,   7,   7,  20,   7,   7, 103,   1,   7,  85, 101,   7,
      7,  46,   0,   0, 120,   0,  41, 111,   0,   7,  17,   1,   7,   7,   7,  86,
    156,   7,   7, 157, 158, 159,   0,   0,   7,  14,   7, 160, 161,  18,  17,   7,
      7,   7,   4,   1,  22,  32,  23, 162,  49, 163, 164,  96,   4, 165,   0,   0,
    166,   1,   0,   0,   7,   7,   7, 167,  46, 168,   0,   0, 169,   1,   0,   0,
      1,   0,   0,   0,   7,  25,  28,   1,   0,   0,   7,   7,   7,   7,   1, 111,
    101,   7,   7,   7,  31, 170,   0,   0,  23,   7,   7,   8,  46,   1,   0, 128,
      7, 128,  84, 120, 171,   7,   7, 172, 103,   1, 173,   7,  75, 174,   1,   0,
      0,   0,   7, 120,   7,   7,  75,   0,  97,   0,   0,   0, 120,   0,   0,   0,
      7,  75,   1,   0,   0,   7,  27,  96,  97,   1,  30, 175,   7,   0,   0,   0,
     96,   7,   7,  75, 111,   7,   0,   0,   0,   0,  10,   0,   7,   7,   7,  28,
      7,   7,   4,  85,  17, 176,   0,   0,   0,   0, 177, 178, 179,   0, 180,   0,
    181,   0,   0,   0,   7,  86,   7,   7,   7,  57, 182, 183, 184,   7,   7,   7,
    185, 186,   7, 187, 188,  58,   7,   7,   7,   7, 167,   7,  58,  89,   7,  89,
      7,  86,   7,  86,  75,   7,  75,   7,  23,   7,  23,   7, 189,   7,   7,   7,
      7,   7,   7, 136,   7,   7,  85, 190, 112, 102,   2,   0,   8, 129, 191,   0,
     96, 120,   0,   0,   4,   1,   0,   0, 184,   7, 192, 193, 194, 195, 196, 197,
    105,  28, 198,  28,   1,   7,   1,   7,   7, 120,   0,   0,   7,   7,  10,   7,
      7,   7,  46,   0,   7,  27,   0,   0,
};

static RE_UINT8 re_word_stage_5[] = {
      0,   0, 255,   3, 254, 255, 255, 135, 255,   7,   0,   4,  32,   4, 255, 255,
    127, 255, 195, 255,   3,   0,  31,  80, 223, 188,  64, 215, 251, 255, 191, 255,
    127,   2, 255,   1, 255, 191, 182,   0,   7,   0, 255, 195, 239, 159, 255, 253,
    255, 159, 255, 231,  63,  36, 255,  63, 255,  15, 223,  63, 248, 255, 207, 255,
    249, 255, 197, 243, 159, 121, 128, 176,   3,  80, 238, 135, 109, 211, 135,  57,
      2,  94, 192, 255,  63,   0, 238, 191, 237, 243, 191,  59,   1,   0,   0, 254,
    238, 159, 159,  57, 192, 176,   2,   0, 236, 199,  61, 214,  24, 199, 199,  61,
    129,   0, 255, 223, 253, 255, 255, 227, 223,  61,  96,   7, 239, 223, 239, 243,
     96,  64,   6,   0, 223, 125, 240, 128,   0, 252, 236, 255, 127, 252, 251,  47,
    127, 132,  95, 255,  12,   0, 255, 127, 150,  37, 240, 254, 174, 236, 255,  59,
     95,  63, 255, 243,   0,   3, 160, 194, 255, 254, 255,  31, 223, 255,  64,   0,
    191,  32, 255, 247, 255,  61, 127,  61,  61, 127,  61, 255,  63,  63, 255, 199,
     31,   0,  15,   0,  13,   0, 143,  48,   0,  56, 128,   0,   0, 248, 255,   0,
    247, 255, 255, 251, 255, 170, 223,  95, 220,  31, 207,  15,   0,  48,   0, 128,
     16,   0,   2, 128, 132, 252,  47,  62,  80, 189, 224,  67,  31, 248, 255, 128,
    127,   0, 127, 127, 224,   0,  62,  31, 127, 230, 224, 255, 247, 191, 128, 255,
    252, 255, 255, 249, 255, 232,   1, 128, 124,   0, 126, 126, 126,   0, 255,  55,
    127, 248, 248, 224, 127,  95, 219, 255,  24,   0,   0, 224, 252, 252, 252,  28,
    255, 239, 255, 183,   0,  32,  15, 255,  62,   0,  63, 253, 191, 145,  55,   0,
    255, 192, 111, 240, 239, 254,  63, 135, 112,   0,  79,   0,  31,  30, 255,  23,
    255,  64, 127, 189, 237, 251, 129, 224, 207,  31, 255,  67, 191,   0,  63, 255,
      0,  63,  17,   0, 255,  35, 127, 251, 127, 180, 191, 253, 251,   1, 255, 224,
    255,  99, 224, 227,   7, 248, 231,  15,   0,  60,  28,   0, 100, 222, 255, 235,
    239, 255, 191, 231, 223, 223, 255, 123,  95, 252, 247, 207,  32,   0, 219,   7,
    150, 254, 247,  10, 132, 234, 150, 170, 150, 247, 247,  94, 238, 251,
};

/* Word: 2486 bytes. */

RE_UINT32 re_get_word(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 13;
    code = ch ^ (f << 13);
    pos = (RE_UINT32)re_word_stage_1[f] << 4;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_word_stage_2[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_word_stage_3[pos + f] << 2;
    f = code >> 4;
    code ^= f << 4;
    pos = (RE_UINT32)re_word_stage_4[pos + f] << 4;
    pos += code;
    value = (re_word_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* XDigit. */

static RE_UINT8 re_xdigit_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_xdigit_stage_2[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 4,
    5, 6, 2, 2, 2, 2, 7, 2, 2, 2, 2, 2, 2, 8, 9, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
};

static RE_UINT8 re_xdigit_stage_3[] = {
     0,  1,  1,  1,  1,  1,  2,  3,  1,  4,  4,  4,  4,  4,  5,  6,
     7,  1,  1,  1,  1,  1,  1,  8,  9, 10, 11, 12, 13,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  6,  1, 14, 15, 16, 17,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 18,
     1,  1,  1,  1, 19,  1,  1,  1,  1,  1,  1,  1,  1, 20,  1,  1,
    21, 22, 17,  1,  5,  1, 23, 20,  8,  1,  1,  1, 16, 24,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 25, 16,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1, 16,  1,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_xdigit_stage_4[] = {
     0,  1,  2,  2,  2,  2,  2,  2,  2,  3,  2,  0,  2,  2,  2,  4,
     2,  5,  2,  5,  2,  6,  2,  6,  3,  2,  2,  2,  2,  4,  6,  2,
     2,  2,  2,  3,  6,  2,  2,  2,  2,  7,  2,  6,  2,  2,  8,  2,
     2,  6,  0,  2,  2,  8,  2,  2,  2,  2,  2,  6,  4,  2,  2,  9,
     2,  6,  2,  2,  2,  2,  2,  0, 10, 11,  2,  2,  2,  2,  3,  2,
     0,  2,  2,  2,  2,  5,  2,  0, 12,  2,  2,  6,  2,  6,  2,  4,
     2,  6,  3,  2,  2,  3,  2,  2,  2,  2,  2, 13,
};

static RE_UINT8 re_xdigit_stage_5[] = {
      0,   0,   0,   0,   0,   0, 255,   3, 126,   0,   0,   0, 126,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255,   3,   0,   0,
    255,   3,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 192, 255,   0,   0,
      0,   0, 255,   3,   0,   0,   0,   0, 192, 255,   0,   0,   0,   0,   0,   0,
    255,   3, 255,   3,   0,   0,   0,   0,   0,   0, 255,   3,   0,   0, 255,   3,
      0,   0, 255,   3, 126,   0,   0,   0, 126,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 192, 255,   0, 192, 255, 255, 255, 255, 255, 255,
};

/* XDigit: 445 bytes. */

RE_UINT32 re_get_xdigit(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_xdigit_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_xdigit_stage_2[pos + f] << 4;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_xdigit_stage_3[pos + f] << 2;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_xdigit_stage_4[pos + f] << 6;
    pos += code;
    value = (re_xdigit_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Posix_Digit. */

static RE_UINT8 re_posix_digit_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_posix_digit_stage_2[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_posix_digit_stage_3[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_posix_digit_stage_4[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_posix_digit_stage_5[] = {
      0,   0,   0,   0,   0,   0, 255,   3,   0,   0,   0,   0,   0,   0,   0,   0,
};

/* Posix_Digit: 97 bytes. */

RE_UINT32 re_get_posix_digit(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_posix_digit_stage_1[f] << 4;
    f = code >> 12;
    code ^= f << 12;
    pos = (RE_UINT32)re_posix_digit_stage_2[pos + f] << 3;
    f = code >> 9;
    code ^= f << 9;
    pos = (RE_UINT32)re_posix_digit_stage_3[pos + f] << 3;
    f = code >> 6;
    code ^= f << 6;
    pos = (RE_UINT32)re_posix_digit_stage_4[pos + f] << 6;
    pos += code;
    value = (re_posix_digit_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Posix_AlNum. */

static RE_UINT8 re_posix_alnum_stage_1[] = {
    0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3,
};

static RE_UINT8 re_posix_alnum_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  9, 10, 11,  7,  7,  7,  7, 12, 13, 13, 13, 13, 14,
    15, 16, 17, 18, 19, 13, 20, 13, 21, 13, 13, 13, 13, 22,  7,  7,
    23, 24, 13, 13, 13, 13, 25, 26, 13, 13, 27, 13, 28, 29, 30, 13,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7, 31,  7, 32, 33,  7, 34,  7,  7,  7, 35, 13, 36,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
};

static RE_UINT8 re_posix_alnum_stage_3[] = {
      0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,
     16,   1,  17,  18,  19,   1,  20,  21,  22,  23,  24,  25,  26,  27,   1,  28,
     29,  30,  31,  31,  32,  31,  31,  31,  31,  31,  31,  31,  33,  34,  35,  31,
     36,  37,  31,  31,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,  38,   1,   1,   1,   1,   1,   1,   1,   1,   1,  39,
      1,   1,   1,   1,  40,   1,  41,  42,  43,  44,  45,  46,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,  47,  31,  31,  31,  31,  31,  31,  31,  31,
     31,   1,  48,  49,   1,  50,  51,  52,  53,  54,  55,  56,  57,  58,   1,  59,
     60,  61,  62,  63,  64,  65,  31,  66,  67,  68,  69,  70,  71,  72,  73,  74,
     75,  31,  76,  31,  77,  78,  79,  31,   1,   1,   1,  80,  81,  82,  31,  31,
      1,   1,   1,   1,  83,  31,  31,  31,  31,  31,  31,  31,   1,   1,  84,  31,
      1,   1,  85,  86,  31,  31,  87,  88,   1,   1,   1,   1,   1,   1,   1,  89,
      1,   1,  90,  31,  31,  31,  31,  31,   1,  91,  92,  31,  31,  31,  31,  31,
     31,  31,  31,  31,  93,  31,  31,  31,  31,  31,  31,  31,  94,  95,  96,  97,
     98,  31,  31,  31,  31,  31,  31,  31,  99, 100,  31,  31,  31,  31, 101,  31,
     31, 102,  31,  31,  31,  31,  31,  31,   1,   1,   1,   1,   1,   1, 103,   1,
      1,   1,   1,   1,   1,   1,   1, 104, 105,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1, 106,   1,   1,   1,   1, 107,  31,  31,  31,  31,
      1,   1, 108,  31,  31,  31,  31,  31,
};

static RE_UINT8 re_posix_alnum_stage_4[] = {
      0,   1,   2,   2,   0,   3,   4,   4,   5,   5,   5,   5,   5,   5,   5,   5,
      5,   5,   5,   5,   5,   5,   6,   7,   0,   0,   8,   9,  10,  11,   5,  12,
      5,   5,   5,   5,  13,   5,   5,   5,   5,  14,  15,   5,  16,  17,  18,  19,
     20,   5,  21,  22,   5,   5,  23,  24,  25,   5,  26,   5,   5,  27,  28,  29,
     30,  31,  32,  33,   0,  34,  35,  36,   5,  37,  38,  39,  40,  41,  42,  43,
     44,  45,  46,  47,  48,  49,  50,  51,  52,  49,  53,  54,  55,  56,  57,   0,
     58,  59,  60,  61,  58,  62,  63,  64,  58,  65,  66,  67,  68,  69,  70,  71,
     72,  73,  74,   0,  75,  76,  77,   0,  78,   0,  79,  80,  81,  82,   0,   0,
      5,  83,  25,  84,  85,   5,  86,  87,   5,   5,  88,   5,  89,  90,  91,   5,
     92,   5,  93,   0,  94,   5,   5,  95,  72,   5,   5,   5,   5,   5,   5,   5,
      5,   5,   5,  96,   2,   5,   5,  97,  98,  99,  99, 100,   5, 101, 102,   0,
      0,   5,   5,  32,   5, 103,   5, 104, 105, 106,  25, 107,   5, 108, 109,   0,
    110,   5, 105, 111,   0, 112,   0,   0,   5, 113, 114,   0,   5, 115,   5, 116,
      5, 104, 117, 118, 119,  65,   0, 120,   5,   5,   5,   5,   5,   5,   0, 121,
     95,   5, 122, 118,   5, 123, 124, 125,   0,   0,   0, 126, 127,   0,   0,   0,
    128, 129, 130,   5,  16,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0, 131,   5, 109,   5, 132, 105,   5,   5,   5,   5, 133,
      5,  86,   5, 134, 135, 136, 136,   5,   0, 137,   0,   0,   0,   0,   0,   0,
    138, 139,  72,   5, 140,  72,   5,  87, 141,  14,   5,   5, 142,  73,   0,  25,
      5,   5,   5,   5,   5, 104,   0,   0,   5,   5,   5,   5,   5,   5,   5,  94,
      5,   5,   5,   5,  31,   0,  25, 118, 143, 144,   5, 145,   5,   5,   5,  94,
    146, 147,   5,   5, 148, 149,   0, 146, 150, 151,   5,  99,   5,   5, 152, 153,
     28, 103, 154,  82,   5, 155, 137, 156,   5, 135, 157, 158,   5, 105, 159, 160,
    161, 162,  87, 163,   5,   5,   5,  33,   5,   5,   5,   5,   5, 164, 165, 110,
      5,   5,   5, 166,   5,   5, 149,   0, 167, 168, 169,   5,   5,  27, 170,   5,
      5, 118,  25,   5, 171,   5, 151, 172,   0,   0,   0, 173,   5,   5,   5,  82,
      0,   2,   2, 174,   5, 105, 175,   0, 176, 177, 178,   0,   5,   5,   5,  73,
      0,   0,   5, 179,   0,   0,   0,   0,   0,   0,   0,   0,  82,   5, 180,   0,
      5,  26, 103,  73, 118,   5, 181,   0,   5,   5,   5,   5, 118,  25, 182, 110,
      5, 183,   5,  61,   0,   0,   0,   0,   5, 135, 104, 151,   0,   0,   0,   0,
    184, 185, 104, 135, 105,   0,   0, 186, 104, 149,   0,   0,   5, 187,   0,   0,
    188, 104,   0,  82,  82,   0,  79, 189,   5, 104, 104, 154,  27,   0,   0,   0,
      5,   5,  16,   0,   5, 154,   5, 154,   5, 151,   0,   0,   0,   0,   0,   0,
     82, 190, 191,   0,   0,   0,   0,   0,   5,   5, 191,   0, 147,  32,  25,  16,
      5, 154, 192, 193,   5,   5, 194,   0, 195, 196,   0,   0, 197, 119,   5,  16,
     40,  49, 198,  61,   0,   0,   0,   0,   5,   5, 199,   0,   5,   5, 200,   0,
      0,   0,   0,   0,   5, 201, 202,   0,   5, 105, 203,   0,   5, 104,   0,   0,
     65,  33,   0,   0,   0,   0,   0,   0,   5,  32,   0,   0,   0,   5,   5, 204,
      5, 205,  25,   5, 206,   0,   5,  32, 207, 208,  78, 209, 171, 210,   0,   0,
    211, 212, 213, 214, 215,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 135,
      5,   5,   5,   5, 149,   0,   0,   0,   5,   5,   5, 142,   5,   5,   5,   5,
      5,   5,  61,   0,   0,   0,   0,   0,   5, 142,   0,   0,   0,   0,   0,   0,
      5,   5, 216,   0,   0,   0,   0,   0,   5,  32, 105,   0,   0,   0,  25, 157,
      5, 135,  61, 217,  94,   0,   0,   0,   0,   0,   5,   5,   0,   0,   0,   0,
      5,   5, 218, 105, 170,   0,   0, 219,   5,   5,   5,   5,   5,   5,   5,  27,
      5,   5,   5,   5,   5,   5,   5, 154, 105,   0,   0,  25,   5,   5,   5,   5,
      5,   5,   5,   5,   5,   5,   5, 110,   5,   5,   5, 220, 221,   0,   0,   0,
      5,   5, 222,   5, 223, 224, 225,   5, 226, 227, 228,   5,   5,   5,   5,   5,
      5,   5,   5,   5,   5, 229, 230,  87, 222, 222, 132, 132, 207, 207, 231,   0,
    232, 233,   0,   0,   0,   0,   0,   0,   5,   5,   5,   5,   5,   5, 189,   0,
      5,   5, 234,   0,   0,   0,   0,   0, 225, 235, 236, 237, 238, 239,   0,   0,
      0,  25, 240, 240, 109,   0,   0,   0,   5,   5,   5,   5,   5,   5, 135,   0,
      5, 179,   5,   5,   5,   5,   5,   5, 118,   5,   5,   5,   5,   5,   5,   5,
      5,   5,   5,   5,   5, 241,   5,   5,   5,   5,   5,   5,   5,   5,   5,  78,
    118,   0,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_posix_alnum_stage_5[] = {
      0,   0,   0,   0,   0,   0, 255,   3, 254, 255, 255,   7,   0,   4,  32,   4,
    255, 255, 127, 255, 255, 255, 255, 255, 195, 255,   3,   0,  31,  80,   0,   0,
     32,   0,   0,   0,   0,   0, 223, 188,  64, 215, 255, 255, 251, 255, 255, 255,
    255, 255, 191, 255,   3, 252, 255, 255, 255, 255, 254, 255, 255, 255, 127,   2,
    255,   1,   0,   0,   0,   0, 255, 191, 182,   0, 255, 255, 255, 135,   7,   0,
      0,   0, 255,   7, 255, 255, 255, 254,   0, 192, 255, 255, 255, 255, 239,  31,
    254, 225,   0, 156,   0,   0, 255, 255,   0, 224, 255, 255, 255, 255,   3,   0,
      0, 252, 255, 255, 255,   7,  48,   4, 255, 255, 255, 252, 255,  31,   0,   0,
    255, 255, 255,   1, 255,   7,   0,   0, 255, 255, 223,  63,   0,   0, 240, 255,
    248,   3, 255, 255, 255, 255, 255, 239, 255, 223, 225, 255,  15,   0, 254, 255,
    239, 159, 249, 255, 255, 253, 197, 227, 159,  89, 128, 176,  15,   0,   3,  16,
    238, 135, 249, 255, 255, 253, 109, 195, 135,  25,   2,  94,   0,   0,  63,   0,
    238, 191, 251, 255, 255, 253, 237, 227, 191,  27,   1,   0,  15,   0,   0,  30,
    238, 159, 249, 255, 159,  25, 192, 176,  15,   0,   2,   0, 236, 199,  61, 214,
     24, 199, 255, 195, 199,  29, 129,   0, 239, 223, 253, 255, 255, 253, 255, 227,
    223,  29,  96,   7,  15,   0,   0,   0, 255, 253, 239, 227, 223,  29,  96,  64,
     15,   0,   6,   0, 255, 255, 255, 231, 223,  93, 240, 128,  15,   0,   0, 252,
    236, 255, 127, 252, 255, 255, 251,  47, 127, 128,  95, 255,   0,   0,  12,   0,
    254, 255, 255, 255, 255, 255, 255,   7, 127,  32,   0,   0, 150,  37, 240, 254,
    174, 236, 255,  59,  95,  32,   0, 240,   1,   0,   0,   0, 255, 254, 255, 255,
    255,  31, 254, 255,   3, 255, 255, 254, 255, 255, 255,  31, 255, 255, 127, 249,
    231, 193, 255, 255, 127,  64,   0,  48, 191,  32, 255, 255, 255, 255, 255, 247,
    255,  61, 127,  61, 255,  61, 255, 255, 255, 255,  61, 127,  61, 255, 127, 255,
    255, 255,  61, 255, 255, 255, 255, 135, 255, 255,   0,   0, 255, 255,  63,  63,
    255, 159, 255, 255, 255, 199, 255,   1, 255, 223,  15,   0, 255, 255,  15,   0,
    255, 223,  13,   0, 255, 255, 207, 255, 255,   1, 128,  16, 255,   7, 255, 255,
    255, 255,  63,   0, 255, 255, 255, 127, 255,  15, 255,   1, 255,  63,  31,   0,
    255,  15, 255, 255, 255,   3,   0,   0, 255, 255, 255,  15, 254, 255,  31,   0,
    128,   0,   0,   0, 255, 255, 239, 255, 239,  15,   0,   0, 255, 243,   0, 252,
    191, 255,   3,   0,   0, 224,   0, 252, 255, 255, 255,  63, 255,   1, 255, 255,
      0, 222, 111,   0, 128, 255,  31,   0,  63,  63, 255, 170, 255, 255, 223,  95,
    220,  31, 207,  15, 255,  31, 220,  31,   0,   0,   2, 128,   0,   0, 255,  31,
    132, 252,  47,  62,  80, 189, 255, 243, 224,  67,   0,   0,   0,   0, 192, 255,
    255, 127, 255, 255,  31, 120,  12,   0, 255, 128,   0,   0, 255, 255, 127,   0,
    127, 127, 127, 127,   0, 128,   0,   0, 224,   0,   0,   0, 254,   3,  62,  31,
    255, 255, 127, 224, 224, 255, 255, 255, 255, 127,   0,   0, 255,  31, 255, 255,
      0,  12,   0,   0, 255, 127, 240, 143,   0,   0, 128, 255, 252, 255, 255, 255,
    255, 249, 255, 255, 255, 255, 255,   3, 187, 247, 255, 255, 255,   0,   0,   0,
     47,   0,   0,   0,   0,   0, 252, 104, 255, 255,   7,   0, 255, 255, 247, 255,
    223, 255,   0, 124, 255,  63,   0,   0, 255, 255, 127, 196,   5,   0,   0,  56,
    255, 255,  60,   0, 126, 126, 126,   0, 127, 127, 255, 255,  63,   0, 255, 255,
     15,   0, 255, 255, 127, 248, 255, 255, 255,  63, 255, 255, 127,   0, 248, 224,
    255, 253, 127,  95, 219, 255, 255, 255,   0,   0, 248, 255, 255, 255, 252, 255,
      0,   0, 255,  15,   0,   0, 223, 255, 192, 255, 255, 255, 252, 252, 252,  28,
    255, 239, 255, 255, 127, 255, 255, 183, 255,  63, 255,  63, 255, 255,  31,   0,
    255, 255,   1,   0,  15, 255,  62,   0, 255, 255,  15, 255, 255,   0, 255, 255,
     63, 253, 255, 255, 255, 255, 191, 145, 255, 255,  55,   0, 255, 255, 255, 192,
    111, 240, 239, 254,  31,   0,   0,   0, 128,   0, 255, 255,  63,   0,   0,   0,
    112,   0, 255, 255, 255, 255,  71,   0,  30,   0,   0,  20, 255, 255, 251, 255,
    255, 255, 159,  64, 127, 189, 255, 191, 159,  25, 129, 224, 187,   7,   0,   0,
    179,   0,   0,   0, 255, 255,  63, 127,   0,   0,   0,  63,  17,   0,   0,   0,
      0,   0,   0, 128, 255, 255, 231, 127, 207, 255, 255,  32, 255, 253, 255, 255,
    255, 255, 127, 127,   0,   0, 252, 255, 255, 254, 127,   0, 127, 251, 255, 255,
    255, 255, 127, 180, 203,   0,   0,   0, 191, 253, 255, 255, 255, 127, 123,   1,
    127,   0,   0,   0, 248, 255, 255, 224,  31,   0, 255, 255,   3,   0,   0,   0,
    255,   7, 255,  31, 255,   1, 255,  67, 255, 255, 223, 255, 255, 255, 255, 223,
    100, 222, 255, 235, 239, 255, 255, 255, 191, 231, 223, 223, 255, 255, 255, 123,
     95, 252, 253, 255,  63, 255, 255, 255, 253, 255, 255, 247, 247,  15,   0,   0,
    127, 255, 255, 249, 219,   7,   0,   0, 143,   0,   0,   0, 150, 254, 247,  10,
    132, 234, 150, 170, 150, 247, 247,  94, 255, 251, 255,  15, 238, 251, 255,  15,
    255,   3, 255, 255,   3,   0, 255, 255,
};

/* Posix_AlNum: 2281 bytes. */

RE_UINT32 re_get_posix_alnum(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_posix_alnum_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_posix_alnum_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_posix_alnum_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_posix_alnum_stage_4[pos + f] << 5;
    pos += code;
    value = (re_posix_alnum_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Posix_Punct. */

static RE_UINT8 re_posix_punct_stage_1[] = {
    0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2,
};

static RE_UINT8 re_posix_punct_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  7,  8,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  9, 10,  7,  7,  7,  7,  7,  7,  7,  7,  7, 11,
    12, 13, 14, 15, 16,  7,  7,  7,  7,  7,  7,  7,  7, 17,  7,  7,
     7,  7,  7,  7,  7,  7,  7, 18,  7,  7, 19, 20,  7, 21, 22, 23,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
     7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
};

static RE_UINT8 re_posix_punct_stage_3[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
    16,  1,  1, 17, 18,  1, 19, 20, 21, 22, 23, 24, 25,  1,  1, 26,
    27, 28, 29, 29, 30, 29, 29, 31, 29, 29, 29, 32, 33, 34, 35, 36,
    37, 38, 39, 29,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1, 40,  1,  1,  1,  1,  1,  1, 41,  1, 42, 43,
    44, 45, 46, 47,  1,  1,  1,  1,  1,  1,  1, 48,  1, 49, 50, 51,
     1, 52,  1, 53,  1, 54,  1,  1, 55, 56, 57, 58,  1,  1,  1, 59,
    60, 61, 62,  1, 63, 64, 65, 66, 67,  1, 68,  1, 69,  1, 70,  1,
     1,  1,  1,  1, 71,  1,  1,  1,  1,  1, 72, 73,  1,  1, 74,  1,
     1,  1,  1,  1, 75,  1,  1,  1, 76, 77, 78, 79,  1,  1, 80, 81,
    29, 29, 82,  1,  1,  1,  1,  1,  1, 83,  1,  1, 84,  1, 85,  1,
    86, 87, 88, 29, 29, 29, 89, 90, 91, 92, 93,  1,  1,  1,  1,  1,
};

static RE_UINT8 re_posix_punct_stage_4[] = {
      0,   1,   2,   3,   0,   4,   5,   5,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   6,   7,   0,   0,   0,   8,   9,   0,   0,  10,
      0,   0,   0,   0,  11,   0,   0,   0,   0,   0,  12,   0,  13,  14,  15,  16,
     17,   0,   0,  18,   0,   0,  19,  20,  21,   0,   0,   0,   0,   0,   0,  22,
      0,  23,  14,   0,   0,   0,   0,   0,   0,   0,   0,  24,   0,   0,   0,  25,
      0,   0,   0,  10,   0,   0,   0,  26,   0,   0,   0,  27,   0,   0,   0,  28,
      0,   0,   0,  29,  30,   0,   0,   0,   0,   0,  31,  32,   0,   0,   0,  33,
      0,  29,  34,   0,   0,   0,   0,   0,  35,  36,   0,   0,  37,  38,  39,   0,
      0,   0,  40,   0,  38,   0,   0,  41,   0,   0,   0,  42,  43,   0,   0,   0,
     44,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  45,  46,   0,   0,  47,
      0,  48,   0,   0,   0,   0,  49,   0,  50,   0,   0,   0,   0,   0,   0,   0,
      0,   0,  51,   0,   0,   0,  38,  52,  38,   0,   0,   0,   0,  53,   0,   0,
      0,   0,  12,  54,   0,   0,   0,  55,   0,  56,   0,  38,   0,   0,  57,   0,
      0,   0,   0,   0,   0,  58,  59,  60,  61,  62,  63,  64,  65,  52,   0,   0,
     66,  67,  68,   0,  69,  52,  52,  52,  52,  52,  52,  52,  52,  52,  52,  52,
     52,  70,  50,   0,  55,  71,   0,   0,  52,  52,  52,  71,  72,  52,  52,  52,
     52,  52,  52,  73,  74,  52,  75,  63,   0,   0,   0,   0,   0,   0,   0,  76,
      0,   0,   0,  27,   0,   0,   0,   0,  52,  77,  78,   0,  79,  52,  52,  80,
     52,  52,  52,  52,  52,  52,  71,  81,  82,  83,   0,   0,  46,  44,   0,  41,
      0,   0,   0,   0,  84,   0,  52,  85,  63,  86,  87,  52,  86,  88,  52,  63,
      0,   0,   0,   0,   0,   0,  52,  52,   0,   0,   0,   0,  61,  52,  70,  38,
     89,   0,   0,  90,   0,   0,   0,  91,  92,  93,   0,   0,  94,   0,   0,   0,
      0,  95,   0,  96,   0,   0,  97,  98,   0,  97,  29,   0,   0,   0,  99,   0,
      0,   0,  55, 100,   0,   0,  38,  26,   0,   0,  41,   0,   0,   0,   0, 101,
      0, 102,   0,   0,   0, 103,  93,   0,   0,  38,   0,   0,   0,   0,   0, 104,
     43,  61, 105, 106,   0,   0,   0,   0,   1,   2,   2, 107,   0,   0,   0, 108,
    109, 110,   0, 111, 112,  44,  61, 113,   0,   0,   0,   0,  29,   0,  27,   0,
      0,   0,   0,  31,   0,   0,   0,   0,   0,   0,   5, 114,   0,   0,   0,   0,
     29,  29,   0,   0,   0,   0,   0,   0,   0,   0, 115,  29,   0,   0, 116, 117,
      0, 111,   0,   0, 118,   0,   0,   0,   0,   0, 119,   0,   0,   0,   0,   0,
      0,   0, 120,   0,   0, 121,  93,   0,   0,   0,  85, 122,   0,   0, 123,   0,
      0, 124,   0,   0,   0, 102,   0,   0,   0,   0, 125,   0,   0,   0, 126,   0,
      0,   0,   0,   0,   0,   0, 127,   0,   0,   0, 128, 129,   0,   0,   0,   0,
      0,  55,   0,   0,   0,   0,   0,   0,   0,  41,   0,   0,   0,   0,   0,   0,
      0,  29,  70,   0, 130, 109,   0,   0,   0,   0, 131,  26,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0, 114,   0,   0,   0, 132,   0,   0,   0,   0,
      0,   0,   0,  97,   0,   0,   0, 133,   0, 110, 134,   0,   0,   0,   0,   0,
      0,   0,   0,   0, 135,   0,   0,   0,   0,   0,   0,   0, 136,   0,   0,   0,
     52,  52,  52,  52,  52,  52,  52,  71,  52, 137,  52, 138, 139, 140,  52,  42,
     52,  52, 141,   0,   0,   0,   0,   0,  52,  52,  92,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 142,  41, 133, 133,  31,  31, 102, 102, 143,   0,
      0, 135,   0, 144, 145,   0,   0,   0,   0,   0,  38,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0, 146,   0,   0,   0,   0,   0,   0,   0,   0,   0,  26,
     52, 147,  52,  52,  80, 148, 149,  71,  61, 150,  40, 151,  86, 129,   0, 152,
    153, 154, 155, 107,   0,   0,   0,   0,  52,  52,  52,  52,  52,  52, 156, 157,
     52,  52,  52,  80,  52,  52, 158,   0, 147,  52, 159,  52,  62,  21,   0,   0,
    147,  63,  52, 160,  52, 161, 153,  52,   0,   0,   0,  21,   0,   0,   0,   0,
};

static RE_UINT8 re_posix_punct_stage_5[] = {
      0,   0,   0,   0, 254, 255,   0, 252,   1,   0,   0, 248,   1,   0,   0, 120,
    254, 219, 211, 137,   0,   0, 128,   0,  60,   0, 252, 255, 224, 175, 255, 255,
      0,   0,  32,  64, 176,   0,   0,   0,   0,   0,  64,   0,   4,   0,   0,   0,
      0,   0,   0, 252,   0, 230,   0,   0,   0,   0,   0,  64,  73,   0,   0,   0,
      0,   0,  24,   0, 192, 255,   0, 200,   0,  60,   0,   0,   0,   0,  16,  64,
      0,   2,   0,  96, 255,  63,   0,   0,   0,   0, 192, 195,   0,   0, 255, 127,
     48,   0,   1,   0,   0,   0,  12,  44,   0,   0,   3,   0,   0,   0,   1,   0,
      0,   0, 248,   7,   0,   0,   0, 128,  16,   0,   0,   0,   0, 128,   0,   0,
      0,   0,   0,   2,   0,   0,  16,   0,   0, 128,   0,  12, 254, 255, 255, 252,
      0,   0,  80,  61,  32,   0,   0,   0,   0,   0,   0, 192, 191, 223, 255,   7,
      0, 252,   0,   0,   0,   0,   0,   8, 255,   1,   0,   0,   0,   0, 255,   3,
      1,   0,   0,   0,   0,  96,   0,   0,   0,   0,   0,  24,   0,  56,   0,   0,
      0,   0,  96,   0,   0,   0, 112,  15, 255,   7,   0,   0,  49,   0,   0,   0,
    255, 255, 255, 255, 127,  63,   0,   0, 255,   7, 240,  31,   0,   0,   0, 240,
      0,   0,   0, 248, 255,   0,   8,   0,   0,   0,   0, 160,   3, 224,   0, 224,
      0, 224,   0,  96,   0,   0, 255, 255, 255,   0, 255, 255, 255, 255, 255, 127,
      0,   0,   0, 124,   0, 124,   0,   0, 123,   3, 208, 193, 175,  66,   0,  12,
     31, 188,   0,   0,   0,  12, 255, 255, 127,   0,   0,   0, 255, 255,  63,   0,
      0,   0, 240, 255, 255, 255, 207, 255, 255, 255,  63, 255, 255, 253, 255, 255,
    224,   7,   0, 222, 255, 127, 255, 255, 255, 127,   0,   0, 255, 255, 255, 251,
    255, 255,  15,   0,   0,   0, 255,  15,  30, 255, 255, 255,   1,   0, 193, 224,
      0,   0, 195, 255,  15,   0,   0,   0,   0, 252, 255, 255, 255,   0,   1,   0,
    255, 255,   1,   0,   0, 224,   0,   0,   0,   0,   8,  64,   0,   0, 252,   0,
    255, 255, 127,   0,   3,   0,   0,   0,   0,   6,   0,   0,   0,  15, 192,   3,
      0,   0, 240,   0,   0, 192,   0,   0,   0,   0,   0,  23, 254,  63,   0, 192,
      0,   0, 128,   3,   0,   8,   0,   0,   0,   2,   0,   0,   0,   0, 252, 255,
      0,   0,   0,  48, 255, 255, 247, 255, 127,  15,   0,   0,  63,   0,   0,   0,
    127, 127,   0,  48,   7,   0,   0,   0,   0,   0, 128, 255,   0,   0,   0, 254,
    255, 115, 255,  15, 255, 255, 255,  31,   0,   0, 128,   1,   0,   0, 255,   1,
      0,   1,   0,   0,   0,   0, 127,   0,   0,   0,   0,  30,   0,   0, 224,   3,
    128,  63,   0,   0,   0,   0,   0, 216,   0,   0,  48,   0, 224,  33,   0, 232,
      0,   0,   0,  63,   0, 248,   0,  40,  64,   0,   0,   0, 254, 255, 255,   0,
     14,   0,   0,   0, 255,  31,   0,   0,   0,   0,   0, 220,  62,   0,   0,   0,
      0,   0,  31,   0,   0,   0,  32,   0,  48,   0,   0,   0,   0,   0, 128,   7,
      0,   0,   0, 144, 127, 254, 255, 255,  31,  28,   0,   0,  24, 240, 255, 255,
    255, 195, 255, 255,  35,   0,   0,   0,   2,   0,   0,   8,   8,   0,   0,   0,
      0, 224, 223, 255, 239,  15,   0,   0,   0,  16,   1,   0, 255,  15, 255, 255,
    255, 127, 254, 255, 254, 255, 254, 255, 255, 255,   0,   0,   0,  12,   0,   0,
    192, 255, 255, 255,   7,   0, 255, 255, 255, 255, 255,  15, 255,   1,   3,   0,
    255, 255,  31,   0, 255,  31, 255,   3, 255, 255, 255,   1, 255,   0, 255,   3,
    255, 255, 121, 244,   7,   0, 255,   3,
};

/* Posix_Punct: 1705 bytes. */

RE_UINT32 re_get_posix_punct(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_posix_punct_stage_1[f] << 5;
    f = code >> 11;
    code ^= f << 11;
    pos = (RE_UINT32)re_posix_punct_stage_2[pos + f] << 3;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_posix_punct_stage_3[pos + f] << 3;
    f = code >> 5;
    code ^= f << 5;
    pos = (RE_UINT32)re_posix_punct_stage_4[pos + f] << 5;
    pos += code;
    value = (re_posix_punct_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* Posix_XDigit. */

static RE_UINT8 re_posix_xdigit_stage_1[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,
};

static RE_UINT8 re_posix_xdigit_stage_2[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_posix_xdigit_stage_3[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_posix_xdigit_stage_4[] = {
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

static RE_UINT8 re_posix_xdigit_stage_5[] = {
      0,   0,   0,   0,   0,   0, 255,   3, 126,   0,   0,   0, 126,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
};

/* Posix_XDigit: 97 bytes. */

RE_UINT32 re_get_posix_xdigit(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;

    f = ch >> 16;
    code = ch ^ (f << 16);
    pos = (RE_UINT32)re_posix_xdigit_stage_1[f] << 3;
    f = code >> 13;
    code ^= f << 13;
    pos = (RE_UINT32)re_posix_xdigit_stage_2[pos + f] << 3;
    f = code >> 10;
    code ^= f << 10;
    pos = (RE_UINT32)re_posix_xdigit_stage_3[pos + f] << 3;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_posix_xdigit_stage_4[pos + f] << 7;
    pos += code;
    value = (re_posix_xdigit_stage_5[pos >> 3] >> (pos & 0x7)) & 0x1;

    return value;
}

/* All_Cases. */

static RE_UINT8 re_all_cases_stage_1[] = {
    0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 5,
    6, 7, 3, 3, 3, 3, 8, 3, 3, 3, 3, 3, 3, 3, 9, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
};

static RE_UINT8 re_all_cases_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
    12, 13, 12, 12, 12, 12, 12, 14, 12, 12, 12, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 15, 16, 12, 17, 18, 19, 20,
    12, 12, 21, 22, 12, 12, 12, 12, 12, 23, 12, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 24, 25, 26, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 27, 28, 29, 30,
    12, 12, 12, 12, 12, 12, 31, 32, 12, 12, 12, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 33, 12, 12, 12, 12, 12, 12, 12, 34, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 35, 36, 12, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 37, 12, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
    12, 38, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 39, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
    12, 12, 40, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
};

static RE_UINT8 re_all_cases_stage_3[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   1,   2,   3,   4,   5,   6,   7,   8,
      0,   0,   0,   0,   0,   0,   9,   0,  10,  11,  12,  13,  14,  15,  16,  17,
     18,  18,  18,  18,  18,  18,  19,  20,  21,  22,  18,  18,  18,  18,  18,  23,
     24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  21,  34,  18,  18,  35,  18,
     18,  18,  18,  18,  36,  18,  37,  38,  39,  18,  40,  41,  42,  43,  44,  45,
     46,  47,  48,  49,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,  50,   0,   0,   0,   0,   0,  51,  52,
     53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  18,  18,  18,  64,  65,
     66,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  75,  76,  18,  18,  18,
     77,  78,  18,  18,  18,  18,  18,  18,  79,  80,  18,  18,  18,  18,  18,  18,
     18,  18,  18,  18,  18,  18,  81,  82,  82,  82,  83,   0,  84,  85,  85,  85,
     86,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  87,  87,  87,  87,  88,  89,  90,  90,  90,  90,  90,  91,
      0,   0,   0,   0,  92,  92,  92,  92,  92,  92,  92,  92,  92,  92,  93,  94,
     95,  96,  97,  97,  97,  97,  97,  98,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  99,
     18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18, 100,  18,  18,  18,
     18,  18, 101, 102,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,
    103, 104,  93,  94, 103, 104, 103, 104,  93,  94, 105, 106, 103, 104, 107, 108,
    103, 104, 103, 104, 103, 104, 109, 110, 111, 112, 113, 114, 115, 116, 111, 117,
      0,   0,   0,   0, 118, 119, 120,   0,   0, 121,   0,   0, 122, 122, 123, 123,
    124,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 125, 126, 126, 126, 127, 127, 127, 128,   0,   0,
     82,  82,  82,  82,  82,  83,  85,  85,  85,  85,  85,  86, 129, 130, 131, 132,
     18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  18,  37, 133, 134,   0,
    135, 135, 135, 135, 136, 137,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,  18, 138,  18,  18,  18, 101,   0,   0,
     18,  18,  18,  37,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  78,  18,  78,  18,  18,  18,  18,  18,  18,  18,   0, 139,
     18, 140,  51,  18,  18, 141, 142,  77,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 143,   0,   0,   0, 144, 144,
    144, 144, 144, 144, 144, 144, 144, 144,   0,   0,   0,   0,   0,   0,   0,   0,
    145,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   1,  11,  11,   4,   5,  15,  15,   8,   0,   0,   0,   0,
    146, 146, 146, 146, 146, 147, 147, 147, 147, 147,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 146, 146, 146, 146, 148, 147, 147, 147, 147, 149,
    150, 150, 150, 150, 150, 150, 151,   0, 152, 152, 152, 152, 152, 152, 153,   0,
      0,   0,   0,   0,  11,  11,  11,  11,  15,  15,  15,  15,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,  11,  11,  11,  11,  15,  15,  15,  15,
    154, 154, 154, 154, 155, 156, 156, 156, 157,   0,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_all_cases_stage_4[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1,
      1,   2,   1,   3,   1,   1,   1,   1,   1,   1,   1,   4,   1,   1,   1,   1,
      1,   1,   1,   0,   0,   0,   0,   0,   0,   5,   5,   5,   5,   5,   5,   5,
      5,   6,   5,   7,   5,   5,   5,   5,   5,   5,   5,   8,   5,   5,   5,   5,
      5,   5,   5,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   9,   0,   0,
      1,   1,   1,   1,   1,  10,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   0,   1,   1,   1,   1,   1,   1,   1,  11,
      5,   5,   5,   5,   5,  12,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,
      5,   5,   5,   5,   5,   5,   5,   0,   5,   5,   5,   5,   5,   5,   5,  13,
     14,  15,  14,  15,  14,  15,  14,  15,  16,  17,  14,  15,  14,  15,  14,  15,
      0,  14,  15,  14,  15,  14,  15,  14,  15,  14,  15,  14,  15,  14,  15,  14,
     15,   0,  14,  15,  14,  15,  14,  15,  18,  14,  15,  14,  15,  14,  15,  19,
     20,  21,  14,  15,  14,  15,  22,  14,  15,  23,  23,  14,  15,   0,  24,  25,
     26,  14,  15,  23,  27,  28,  29,  30,  14,  15,  31,   0,  29,  32,  33,  34,
     14,  15,  14,  15,  14,  15,  35,  14,  15,  35,   0,   0,  14,  15,  35,  14,
     15,  36,  36,  14,  15,  14,  15,  37,  14,  15,   0,   0,  14,  15,   0,  38,
      0,   0,   0,   0,  39,  40,  41,  39,  40,  41,  39,  40,  41,  14,  15,  14,
     15,  14,  15,  14,  15,  42,  14,  15,   0,  39,  40,  41,  14,  15,  43,  44,
     45,   0,  14,  15,  14,  15,  14,  15,  14,  15,  14,  15,   0,   0,   0,   0,
      0,   0,  46,  14,  15,  47,  48,  49,  49,  14,  15,  50,  51,  52,  14,  15,
     53,  54,  55,  56,  57,   0,  58,  58,   0,  59,   0,  60,  61,   0,   0,   0,
     58,  62,   0,  63,   0,  64,  65,   0,  66,  67,  65,  68,  69,   0,   0,  67,
      0,  70,  71,   0,   0,  72,   0,   0,   0,   0,   0,   0,   0,  73,   0,   0,
     74,   0,   0,  74,   0,   0,   0,  75,  74,  76,  77,  77,  78,   0,   0,   0,
      0,   0,  79,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  80,  81,   0,
      0,   0,   0,   0,   0,  82,   0,   0,  14,  15,  14,  15,   0,   0,  14,  15,
      0,   0,   0,  33,  33,  33,   0,  83,   0,   0,   0,   0,   0,   0,  84,   0,
     85,  85,  85,   0,  86,   0,  87,  87,  88,   1,  89,   1,   1,  90,   1,   1,
     91,  92,  93,   1,  94,   1,   1,   1,  95,  96,   0,  97,   1,   1,  98,   1,
      1,  99,   1,   1, 100, 101, 101, 101, 102,   5, 103,   5,   5, 104,   5,   5,
    105, 106, 107,   5, 108,   5,   5,   5, 109, 110, 111, 112,   5,   5, 113,   5,
      5, 114,   5,   5, 115, 116, 116, 117, 118, 119,   0,   0,   0, 120, 121, 122,
    123, 124, 125, 126, 127, 128,   0,  14,  15, 129,  14,  15,   0,  45,  45,  45,
    130, 130, 130, 130, 130, 130, 130, 130,   1,   1, 131,   1, 132,   1,   1,   1,
      1,   1,   1,   1,   1,   1, 133,   1,   1, 134, 135,   1,   1,   1,   1,   1,
      1,   1, 136,   1,   1,   1,   1,   1,   5,   5, 137,   5, 138,   5,   5,   5,
      5,   5,   5,   5,   5,   5, 139,   5,   5, 140, 141,   5,   5,   5,   5,   5,
      5,   5, 142,   5,   5,   5,   5,   5, 143, 143, 143, 143, 143, 143, 143, 143,
     14,  15, 144, 145,  14,  15,  14,  15,  14,  15,   0,   0,   0,   0,   0,   0,
      0,   0,  14,  15,  14,  15,  14,  15, 146,  14,  15,  14,  15,  14,  15,  14,
     15,  14,  15,  14,  15,  14,  15, 147,   0, 148, 148, 148, 148, 148, 148, 148,
    148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148,   0,
      0, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149,
    149, 149, 149, 149, 149, 149, 149,   0, 150, 150, 150, 150, 150, 150, 150, 150,
    150, 150, 150, 150, 150, 150,   0, 150,   0,   0,   0,   0,   0, 150,   0,   0,
    151, 151, 151, 151, 151, 151, 151, 151, 151, 151, 151,   0,   0, 151, 151, 151,
    152, 152, 152, 152, 152, 152, 152, 152, 117, 117, 117, 117, 117, 117,   0,   0,
    122, 122, 122, 122, 122, 122,   0,   0, 153, 154, 155, 156, 157, 158, 159, 160,
    161,   0,   0,   0,   0,   0,   0,   0, 162, 162, 162, 162, 162, 162, 162, 162,
    162, 162, 162,   0,   0, 162, 162, 162,   0, 163,   0,   0,   0, 164,   0,   0,
    165, 166,  14,  15,  14,  15,  14,  15,  14,  15,  14,  15,  14,  15,   0,   0,
      0,   0,   0, 167,   0,   0, 168,   0, 117, 117, 117, 117, 117, 117, 117, 117,
    122, 122, 122, 122, 122, 122, 122, 122,   0, 117,   0, 117,   0, 117,   0, 117,
      0, 122,   0, 122,   0, 122,   0, 122, 169, 169, 170, 170, 170, 170, 171, 171,
    172, 172, 173, 173, 174, 174,   0,   0, 117, 117,   0, 175,   0,   0,   0,   0,
    122, 122, 176, 176, 177,   0, 178,   0,   0,   0,   0, 175,   0,   0,   0,   0,
    179, 179, 179, 179, 177,   0,   0,   0, 117, 117,   0, 180,   0,   0,   0,   0,
    122, 122, 181, 181,   0,   0,   0,   0, 117, 117,   0, 182,   0, 125,   0,   0,
    122, 122, 183, 183, 129,   0,   0,   0, 184, 184, 185, 185, 177,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 186,   0,   0,   0, 187, 188,   0,   0,   0,   0,
      0,   0, 189,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 190,   0,
    191, 191, 191, 191, 191, 191, 191, 191, 192, 192, 192, 192, 192, 192, 192, 192,
      0,   0,   0,  14,  15,   0,   0,   0,   0,   0,   0,   0,   0,   0, 193, 193,
    193, 193, 193, 193, 193, 193, 193, 193, 194, 194, 194, 194, 194, 194, 194, 194,
    194, 194,   0,   0,   0,   0,   0,   0,  14,  15, 195, 196, 197, 198, 199,  14,
     15,  14,  15,  14,  15, 200, 201, 202, 203,   0,  14,  15,   0,  14,  15,   0,
      0,   0,   0,   0,   0,   0, 204, 204,   0,   0,   0,  14,  15,  14,  15,   0,
      0,   0,  14,  15,   0,   0,   0,   0, 205, 205, 205, 205, 205, 205, 205, 205,
    205, 205, 205, 205, 205, 205,   0, 205,   0,   0,   0,   0,   0, 205,   0,   0,
     14,  15, 206, 207,  14,  15,  14,  15,   0,  14,  15,  14,  15, 208,  14,  15,
      0,   0,   0,  14,  15, 209,   0,   0,  14,  15, 210, 211, 212, 213, 210,   0,
    214, 215, 216, 217,  14,  15,  14,  15,   0,   0,   0, 218,   0,   0,   0,   0,
    219, 219, 219, 219, 219, 219, 219, 219,   0,   0,   0,   0,   0,  14,  15,   0,
    220, 220, 220, 220, 220, 220, 220, 220, 221, 221, 221, 221, 221, 221, 221, 221,
    220, 220, 220, 220,   0,   0,   0,   0, 221, 221, 221, 221,   0,   0,   0,   0,
     86,  86,  86,  86,  86,  86,  86,  86,  86,  86,  86,   0,   0,   0,   0,   0,
    115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115,   0,   0,   0,   0,   0,
    222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 223, 223, 223, 223, 223, 223,
    223, 223, 223, 223, 223, 223, 223, 223, 223, 223, 223, 223,   0,   0,   0,   0,
};

/* All_Cases: 2512 bytes. */

static RE_AllCases re_all_cases_table[] = {
    {{     0,     0,     0}},
    {{    32,     0,     0}},
    {{    32,   232,     0}},
    {{    32,  8415,     0}},
    {{    32,   300,     0}},
    {{   -32,     0,     0}},
    {{   -32,   199,     0}},
    {{   -32,  8383,     0}},
    {{   -32,   268,     0}},
    {{   743,   775,     0}},
    {{    32,  8294,     0}},
    {{  7615,     0,     0}},
    {{   -32,  8262,     0}},
    {{   121,     0,     0}},
    {{     1,     0,     0}},
    {{    -1,     0,     0}},
    {{  -199,     0,     0}},
    {{  -232,     0,     0}},
    {{  -121,     0,     0}},
    {{  -300,  -268,     0}},
    {{   195,     0,     0}},
    {{   210,     0,     0}},
    {{   206,     0,     0}},
    {{   205,     0,     0}},
    {{    79,     0,     0}},
    {{   202,     0,     0}},
    {{   203,     0,     0}},
    {{   207,     0,     0}},
    {{    97,     0,     0}},
    {{   211,     0,     0}},
    {{   209,     0,     0}},
    {{   163,     0,     0}},
    {{   213,     0,     0}},
    {{   130,     0,     0}},
    {{   214,     0,     0}},
    {{   218,     0,     0}},
    {{   217,     0,     0}},
    {{   219,     0,     0}},
    {{    56,     0,     0}},
    {{     1,     2,     0}},
    {{    -1,     1,     0}},
    {{    -2,    -1,     0}},
    {{   -79,     0,     0}},
    {{   -97,     0,     0}},
    {{   -56,     0,     0}},
    {{  -130,     0,     0}},
    {{ 10795,     0,     0}},
    {{  -163,     0,     0}},
    {{ 10792,     0,     0}},
    {{ 10815,     0,     0}},
    {{  -195,     0,     0}},
    {{    69,     0,     0}},
    {{    71,     0,     0}},
    {{ 10783,     0,     0}},
    {{ 10780,     0,     0}},
    {{ 10782,     0,     0}},
    {{  -210,     0,     0}},
    {{  -206,     0,     0}},
    {{  -205,     0,     0}},
    {{  -202,     0,     0}},
    {{  -203,     0,     0}},
    {{ 42319,     0,     0}},
    {{ 42315,     0,     0}},
    {{  -207,     0,     0}},
    {{ 42280,     0,     0}},
    {{ 42308,     0,     0}},
    {{  -209,     0,     0}},
    {{  -211,     0,     0}},
    {{ 10743,     0,     0}},
    {{ 42305,     0,     0}},
    {{ 10749,     0,     0}},
    {{  -213,     0,     0}},
    {{  -214,     0,     0}},
    {{ 10727,     0,     0}},
    {{  -218,     0,     0}},
    {{ 42282,     0,     0}},
    {{   -69,     0,     0}},
    {{  -217,     0,     0}},
    {{   -71,     0,     0}},
    {{  -219,     0,     0}},
    {{ 42261,     0,     0}},
    {{ 42258,     0,     0}},
    {{    84,   116,  7289}},
    {{   116,     0,     0}},
    {{    38,     0,     0}},
    {{    37,     0,     0}},
    {{    64,     0,     0}},
    {{    63,     0,     0}},
    {{  7235,     0,     0}},
    {{    32,    62,     0}},
    {{    32,    96,     0}},
    {{    32,    57,    92}},
    {{   -84,    32,  7205}},
    {{    32,    86,     0}},
    {{  -743,    32,     0}},
    {{    32,    54,     0}},
    {{    32,    80,     0}},
    {{    31,    32,     0}},
    {{    32,    47,     0}},
    {{    32,  7549,     0}},
    {{   -38,     0,     0}},
    {{   -37,     0,     0}},
    {{  7219,     0,     0}},
    {{   -32,    30,     0}},
    {{   -32,    64,     0}},
    {{   -32,    25,    60}},
    {{  -116,   -32,  7173}},
    {{   -32,    54,     0}},
    {{  -775,   -32,     0}},
    {{   -32,    22,     0}},
    {{   -32,    48,     0}},
    {{   -31,     1,     0}},
    {{   -32,    -1,     0}},
    {{   -32,    15,     0}},
    {{   -32,  7517,     0}},
    {{   -64,     0,     0}},
    {{   -63,     0,     0}},
    {{     8,     0,     0}},
    {{   -62,   -30,     0}},
    {{   -57,   -25,    35}},
    {{   -47,   -15,     0}},
    {{   -54,   -22,     0}},
    {{    -8,     0,     0}},
    {{   -86,   -54,     0}},
    {{   -80,   -48,     0}},
    {{     7,     0,     0}},
    {{  -116,     0,     0}},
    {{   -92,   -60,   -35}},
    {{   -96,   -64,     0}},
    {{    -7,     0,     0}},
    {{    80,     0,     0}},
    {{    32,  6254,     0}},
    {{    32,  6253,     0}},
    {{    32,  6244,     0}},
    {{    32,  6242,     0}},
    {{    32,  6242,  6243}},
    {{    32,  6236,     0}},
    {{   -32,  6222,     0}},
    {{   -32,  6221,     0}},
    {{   -32,  6212,     0}},
    {{   -32,  6210,     0}},
    {{   -32,  6210,  6211}},
    {{   -32,  6204,     0}},
    {{   -80,     0,     0}},
    {{     1,  6181,     0}},
    {{    -1,  6180,     0}},
    {{    15,     0,     0}},
    {{   -15,     0,     0}},
    {{    48,     0,     0}},
    {{   -48,     0,     0}},
    {{  7264,     0,     0}},
    {{  3008,     0,     0}},
    {{ 38864,     0,     0}},
    {{ -6254, -6222,     0}},
    {{ -6253, -6221,     0}},
    {{ -6244, -6212,     0}},
    {{ -6242, -6210,     0}},
    {{ -6242, -6210,     1}},
    {{ -6243, -6211,    -1}},
    {{ -6236, -6204,     0}},
    {{ -6181, -6180,     0}},
    {{ 35266, 35267,     0}},
    {{ -3008,     0,     0}},
    {{ 35332,     0,     0}},
    {{  3814,     0,     0}},
    {{     1,    59,     0}},
    {{    -1,    58,     0}},
    {{   -59,   -58,     0}},
    {{ -7615,     0,     0}},
    {{    74,     0,     0}},
    {{    86,     0,     0}},
    {{   100,     0,     0}},
    {{   128,     0,     0}},
    {{   112,     0,     0}},
    {{   126,     0,     0}},
    {{     9,     0,     0}},
    {{   -74,     0,     0}},
    {{    -9,     0,     0}},
    {{ -7289, -7205, -7173}},
    {{   -86,     0,     0}},
    {{ -7235,     0,     0}},
    {{  -100,     0,     0}},
    {{ -7219,     0,     0}},
    {{  -112,     0,     0}},
    {{  -128,     0,     0}},
    {{  -126,     0,     0}},
    {{ -7549, -7517,     0}},
    {{ -8415, -8383,     0}},
    {{ -8294, -8262,     0}},
    {{    28,     0,     0}},
    {{   -28,     0,     0}},
    {{    16,     0,     0}},
    {{   -16,     0,     0}},
    {{    26,     0,     0}},
    {{   -26,     0,     0}},
    {{-10743,     0,     0}},
    {{ -3814,     0,     0}},
    {{-10727,     0,     0}},
    {{-10795,     0,     0}},
    {{-10792,     0,     0}},
    {{-10780,     0,     0}},
    {{-10749,     0,     0}},
    {{-10783,     0,     0}},
    {{-10782,     0,     0}},
    {{-10815,     0,     0}},
    {{ -7264,     0,     0}},
    {{-35266,     1,     0}},
    {{-35267,    -1,     0}},
    {{-35332,     0,     0}},
    {{-42280,     0,     0}},
    {{-42308,     0,     0}},
    {{-42319,     0,     0}},
    {{-42315,     0,     0}},
    {{-42305,     0,     0}},
    {{-42258,     0,     0}},
    {{-42282,     0,     0}},
    {{-42261,     0,     0}},
    {{   928,     0,     0}},
    {{  -928,     0,     0}},
    {{-38864,     0,     0}},
    {{    40,     0,     0}},
    {{   -40,     0,     0}},
    {{    34,     0,     0}},
    {{   -34,     0,     0}},
};

/* All_Cases: 2688 bytes. */

int re_get_all_cases(RE_UINT32 ch, RE_UINT32* codepoints) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;
    RE_AllCases* all_cases;
    int count;

    f = ch >> 12;
    code = ch ^ (f << 12);
    pos = (RE_UINT32)re_all_cases_stage_1[f] << 5;
    f = code >> 7;
    code ^= f << 7;
    pos = (RE_UINT32)re_all_cases_stage_2[pos + f] << 4;
    f = code >> 3;
    code ^= f << 3;
    pos = (RE_UINT32)re_all_cases_stage_3[pos + f] << 3;
    value = re_all_cases_stage_4[pos + code];

    all_cases = &re_all_cases_table[value];

    codepoints[0] = ch;
    count = 1;

    while (count < RE_MAX_CASES && all_cases->diffs[count - 1] != 0) {
        codepoints[count] = (RE_UINT32)((RE_INT32)ch + all_cases->diffs[count -
          1]);
        ++count;
    }

    return count;
}

/* Simple_Case_Folding. */

static RE_UINT8 re_simple_case_folding_stage_1[] = {
    0, 1, 2, 2, 2, 3, 2, 4, 5, 2, 2, 6, 2, 2, 2, 7,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2,
};

static RE_UINT8 re_simple_case_folding_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     7,  6,  6,  8,  6,  6,  6,  6,  6,  6,  6,  6,  9,  6, 10, 11,
     6, 12,  6,  6, 13,  6,  6,  6,  6,  6,  6,  6, 14,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 15, 16,  6,  6,  6, 17,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6, 18,
     6,  6,  6,  6, 19,  6,  6,  6,  6,  6,  6,  6, 20,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6, 21,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6, 22,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6, 23,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
};

static RE_UINT8 re_simple_case_folding_stage_3[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  1,  2,  2,  3,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  4,  0,  2,  2,  5,  5,  0,  0,  0,  0,
     6,  6,  6,  6,  6,  6,  7,  8,  8,  7,  6,  6,  6,  6,  6,  9,
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19,  8, 20,  6,  6, 21,  6,
     6,  6,  6,  6, 22,  6, 23, 24, 25,  6,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0, 26,  0,  0,  0,  0,  0, 27, 28,
    29, 30,  1,  2, 31, 32,  0,  0, 33, 34, 35,  6,  6,  6, 36, 37,
    38, 38,  2,  2,  2,  2,  0,  0,  0,  0,  0,  0,  6,  6,  6,  6,
    39,  7,  6,  6,  6,  6,  6,  6, 40, 41,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 42, 43, 43, 43, 44,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0, 45, 45, 45, 45, 46, 47,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 48,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    49, 50, 51, 51, 51, 51, 51, 52,  0,  0,  0,  0,  0,  0,  0,  0,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6, 53, 54,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     0, 55,  0, 48,  0, 55,  0, 55,  0, 48,  0, 56,  0, 55,  0,  0,
     0, 55,  0, 55,  0, 55,  0, 57,  0, 58,  0, 59,  0, 60,  0, 61,
     0,  0,  0,  0, 62, 63, 64,  0,  0,  0,  0,  0, 65, 65,  0,  0,
    66,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 67, 68, 68, 68,  0,  0,  0,  0,  0,  0,
    43, 43, 43, 43, 43, 44,  0,  0,  0,  0,  0,  0, 69, 70, 71, 72,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6, 23, 73, 33,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  6,  6,  6,  6,  6, 53,  0,  0,
     6,  6,  6, 23,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  7,  6,  7,  6,  6,  6,  6,  6,  6,  6,  0, 74,
     6, 75, 27,  6,  6, 76, 77, 39,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 78, 78,
    78, 78, 78, 78, 78, 78, 78, 78,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  1,  2,  2,  3,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    79, 79, 79, 79, 79,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 79, 79, 79, 79, 80,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    81, 81, 81, 81, 81, 81, 82,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  2,  2,  2,  2,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  2,  2,  2,  2,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    83, 83, 83, 83, 84,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
};

static RE_UINT8 re_simple_case_folding_stage_4[] = {
     0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  2,  0,  0,  1,  1,  1,  1,  1,  1,  1,  0,
     3,  0,  3,  0,  3,  0,  3,  0,  0,  0,  3,  0,  3,  0,  3,  0,
     0,  3,  0,  3,  0,  3,  0,  3,  4,  3,  0,  3,  0,  3,  0,  5,
     0,  6,  3,  0,  3,  0,  7,  3,  0,  8,  8,  3,  0,  0,  9, 10,
    11,  3,  0,  8, 12,  0, 13, 14,  3,  0,  0,  0, 13, 15,  0, 16,
     3,  0,  3,  0,  3,  0, 17,  3,  0, 17,  0,  0,  3,  0, 17,  3,
     0, 18, 18,  3,  0,  3,  0, 19,  3,  0,  0,  0,  3,  0,  0,  0,
     0,  0,  0,  0, 20,  3,  0, 20,  3,  0, 20,  3,  0,  3,  0,  3,
     0,  3,  0,  3,  0,  0,  3,  0,  0, 20,  3,  0,  3,  0, 21, 22,
    23,  0,  3,  0,  3,  0,  3,  0,  3,  0,  3,  0,  0,  0,  0,  0,
     0,  0, 24,  3,  0, 25, 26,  0,  0,  3,  0, 27, 28, 29,  3,  0,
     0,  0,  0,  0,  0, 30,  0,  0,  3,  0,  3,  0,  0,  0,  3,  0,
     0,  0,  0,  0,  0,  0,  0, 30,  0,  0,  0,  0,  0,  0, 31,  0,
    32, 32, 32,  0, 33,  0, 34, 34,  1,  1,  0,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0, 35, 36, 37,  0,  0,  0, 38, 39,  0,
    40, 41,  0,  0, 42, 43,  0,  3,  0, 44,  3,  0,  0, 23, 23, 23,
    45, 45, 45, 45, 45, 45, 45, 45,  3,  0,  0,  0,  0,  0,  0,  0,
    46,  3,  0,  3,  0,  3,  0,  3,  0,  3,  0,  3,  0,  3,  0,  0,
     0, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47,
    47, 47, 47, 47, 47, 47, 47,  0, 48, 48, 48, 48, 48, 48, 48, 48,
    48, 48, 48, 48, 48, 48,  0, 48,  0,  0,  0,  0,  0, 48,  0,  0,
    49, 49, 49, 49, 49, 49,  0,  0, 50, 51, 52, 53, 53, 54, 55, 56,
    57,  0,  0,  0,  0,  0,  0,  0, 58, 58, 58, 58, 58, 58, 58, 58,
    58, 58, 58,  0,  0, 58, 58, 58,  3,  0,  3,  0,  3,  0,  0,  0,
     0,  0,  0, 59,  0,  0, 60,  0, 49, 49, 49, 49, 49, 49, 49, 49,
     0, 49,  0, 49,  0, 49,  0, 49, 49, 49, 61, 61, 62,  0, 63,  0,
    64, 64, 64, 64, 62,  0,  0,  0, 49, 49, 65, 65,  0,  0,  0,  0,
    49, 49, 66, 66, 44,  0,  0,  0, 67, 67, 68, 68, 62,  0,  0,  0,
     0,  0,  0,  0,  0,  0, 69,  0,  0,  0, 70, 71,  0,  0,  0,  0,
     0,  0, 72,  0,  0,  0,  0,  0, 73, 73, 73, 73, 73, 73, 73, 73,
     0,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 74, 74,
    74, 74, 74, 74, 74, 74, 74, 74,  3,  0, 75, 76, 77,  0,  0,  3,
     0,  3,  0,  3,  0, 78, 79, 80, 81,  0,  3,  0,  0,  3,  0,  0,
     0,  0,  0,  0,  0,  0, 82, 82,  0,  0,  0,  3,  0,  3,  0,  0,
     0,  3,  0,  3,  0, 83,  3,  0,  0,  0,  0,  3,  0, 84,  0,  0,
     3,  0, 85, 86, 87, 88, 85,  0, 89, 90, 91, 92,  3,  0,  3,  0,
    93, 93, 93, 93, 93, 93, 93, 93, 94, 94, 94, 94, 94, 94, 94, 94,
    94, 94, 94, 94,  0,  0,  0,  0, 33, 33, 33, 33, 33, 33, 33, 33,
    33, 33, 33,  0,  0,  0,  0,  0, 95, 95, 95, 95, 95, 95, 95, 95,
    95, 95,  0,  0,  0,  0,  0,  0,
};

/* Simple_Case_Folding: 1840 bytes. */

static RE_INT32 re_simple_case_folding_table[] = {
         0,
        32,
       775,
         1,
      -121,
      -268,
       210,
       206,
       205,
        79,
       202,
       203,
       207,
       211,
       209,
       213,
       214,
       218,
       217,
       219,
         2,
       -97,
       -56,
      -130,
     10795,
      -163,
     10792,
      -195,
        69,
        71,
       116,
        38,
        37,
        64,
        63,
         8,
       -30,
       -25,
       -15,
       -22,
       -54,
       -48,
       -60,
       -64,
        -7,
        80,
        15,
        48,
      7264,
        -8,
     -6222,
     -6221,
     -6212,
     -6210,
     -6211,
     -6204,
     -6180,
     35267,
     -3008,
       -58,
     -7615,
       -74,
        -9,
     -7173,
       -86,
      -100,
      -112,
      -128,
      -126,
     -7517,
     -8383,
     -8262,
        28,
        16,
        26,
    -10743,
     -3814,
    -10727,
    -10780,
    -10749,
    -10783,
    -10782,
    -10815,
    -35332,
    -42280,
    -42308,
    -42319,
    -42315,
    -42305,
    -42258,
    -42282,
    -42261,
       928,
    -38864,
        40,
        34,
};

/* Simple_Case_Folding: 384 bytes. */

RE_UINT32 re_get_simple_case_folding(RE_UINT32 ch) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;
    RE_INT32 diff;

    f = ch >> 13;
    code = ch ^ (f << 13);
    pos = (RE_UINT32)re_simple_case_folding_stage_1[f] << 5;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_simple_case_folding_stage_2[pos + f] << 5;
    f = code >> 3;
    code ^= f << 3;
    pos = (RE_UINT32)re_simple_case_folding_stage_3[pos + f] << 3;
    value = re_simple_case_folding_stage_4[pos + code];

    diff = re_simple_case_folding_table[value];

    return (RE_UINT32)((RE_INT32)ch + diff);
}

/* Full_Case_Folding. */

static RE_UINT8 re_full_case_folding_stage_1[] = {
    0, 1, 2, 2, 2, 3, 2, 4, 5, 2, 2, 6, 2, 2, 2, 7,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2,
};

static RE_UINT8 re_full_case_folding_stage_2[] = {
     0,  1,  2,  3,  4,  5,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     7,  6,  6,  8,  6,  6,  6,  6,  6,  6,  6,  6,  9,  6, 10, 11,
     6, 12,  6,  6, 13,  6,  6,  6,  6,  6,  6,  6, 14,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6, 15, 16,  6,  6,  6, 17,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6, 18,  6,  6,  6, 19,
     6,  6,  6,  6, 20,  6,  6,  6,  6,  6,  6,  6, 21,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6, 22,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6, 23,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6, 24,  6,  6,  6,  6,  6,  6,
     6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
};

static RE_UINT8 re_full_case_folding_stage_3[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   1,   2,   2,   3,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   4,   0,   2,   2,   5,   6,   0,   0,   0,   0,
      7,   7,   7,   7,   7,   7,   8,   9,   9,  10,   7,   7,   7,   7,   7,  11,
     12,  13,  14,  15,  16,  17,  18,  19,  20,  21,   9,  22,   7,   7,  23,   7,
      7,   7,   7,   7,  24,   7,  25,  26,  27,   7,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,  28,   0,   0,   0,   0,   0,  29,  30,
     31,  32,  33,   2,  34,  35,  36,   0,  37,  38,  39,   7,   7,   7,  40,  41,
     42,  42,   2,   2,   2,   2,   0,   0,   0,   0,   0,   0,   7,   7,   7,   7,
     43,  44,   7,   7,   7,   7,   7,   7,  45,  46,   7,   7,   7,   7,   7,   7,
      7,   7,   7,   7,   7,   7,  47,  48,  48,  48,  49,   0,   0,   0,   0,   0,
     50,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  51,  51,  51,  51,  52,  53,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  54,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
     55,  56,  57,  57,  57,  57,  57,  58,   0,   0,   0,   0,   0,   0,   0,   0,
      7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
      7,   7,  59,  60,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
      0,  61,   0,  54,   0,  61,   0,  61,   0,  54,  62,  63,   0,  61,   0,   0,
     64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,
      0,   0,   0,   0,  80,  81,  82,   0,   0,   0,   0,   0,  83,  83,   0,   0,
     84,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,  85,  86,  86,  86,   0,   0,   0,   0,   0,   0,
     48,  48,  48,  48,  48,  49,   0,   0,   0,   0,   0,   0,  87,  88,  89,  90,
      7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,  25,  91,  37,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   7,   7,   7,   7,   7,  92,   0,   0,
      7,   7,   7,  25,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,  44,   7,  44,   7,   7,   7,   7,   7,   7,   7,   0,  93,
      7,  94,  29,   7,   7,  95,  96,  43,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  97,  97,
     97,  97,  97,  97,  97,  97,  97,  97,   0,   0,   0,   0,   0,   0,   0,   0,
     98,   0,  99,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   1,   2,   2,   3,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    100, 100, 100, 100, 100,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 100, 100, 100, 100, 101,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    102, 102, 102, 102, 102, 102, 103,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   2,   2,   2,   2,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   2,   2,   2,   2,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    104, 104, 104, 104, 105,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
};

static RE_UINT8 re_full_case_folding_stage_4[] = {
      0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   2,   0,   0,   1,   1,   1,   1,   1,   1,   1,   0,
      1,   1,   1,   1,   1,   1,   1,   3,   4,   0,   4,   0,   4,   0,   4,   0,
      5,   0,   4,   0,   4,   0,   4,   0,   0,   4,   0,   4,   0,   4,   0,   4,
      0,   6,   4,   0,   4,   0,   4,   0,   7,   4,   0,   4,   0,   4,   0,   8,
      0,   9,   4,   0,   4,   0,  10,   4,   0,  11,  11,   4,   0,   0,  12,  13,
     14,   4,   0,  11,  15,   0,  16,  17,   4,   0,   0,   0,  16,  18,   0,  19,
      4,   0,   4,   0,   4,   0,  20,   4,   0,  20,   0,   0,   4,   0,  20,   4,
      0,  21,  21,   4,   0,   4,   0,  22,   4,   0,   0,   0,   4,   0,   0,   0,
      0,   0,   0,   0,  23,   4,   0,  23,   4,   0,  23,   4,   0,   4,   0,   4,
      0,   4,   0,   4,   0,   0,   4,   0,  24,  23,   4,   0,   4,   0,  25,  26,
     27,   0,   4,   0,   4,   0,   4,   0,   4,   0,   4,   0,   0,   0,   0,   0,
      0,   0,  28,   4,   0,  29,  30,   0,   0,   4,   0,  31,  32,  33,   4,   0,
      0,   0,   0,   0,   0,  34,   0,   0,   4,   0,   4,   0,   0,   0,   4,   0,
      0,   0,   0,   0,   0,   0,   0,  34,   0,   0,   0,   0,   0,   0,  35,   0,
     36,  36,  36,   0,  37,   0,  38,  38,  39,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0,
     40,   0,   0,   0,   0,   0,   0,   0,   0,   0,   4,   0,   0,   0,   0,   0,
      0,   0,   0,   0,   0,   0,   0,  41,  42,  43,   0,   0,   0,  44,  45,   0,
     46,  47,   0,   0,  48,  49,   0,   4,   0,  50,   4,   0,   0,  27,  27,  27,
     51,  51,  51,  51,  51,  51,  51,  51,   4,   0,   0,   0,   0,   0,   0,   0,
      0,   0,   4,   0,   4,   0,   4,   0,  52,   4,   0,   4,   0,   4,   0,   4,
      0,   4,   0,   4,   0,   4,   0,   0,   0,  53,  53,  53,  53,  53,  53,  53,
     53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,  53,   0,
      0,   0,   0,   0,   0,   0,   0,  54,  55,  55,  55,  55,  55,  55,  55,  55,
     55,  55,  55,  55,  55,  55,   0,  55,   0,   0,   0,   0,   0,  55,   0,   0,
     56,  56,  56,  56,  56,  56,   0,   0,  57,  58,  59,  60,  60,  61,  62,  63,
     64,   0,   0,   0,   0,   0,   0,   0,  65,  65,  65,  65,  65,  65,  65,  65,
     65,  65,  65,   0,   0,  65,  65,  65,   4,   0,   4,   0,   4,   0,  66,  67,
     68,  69,  70,  71,   0,   0,  72,   0,  56,  56,  56,  56,  56,  56,  56,  56,
     73,   0,  74,   0,  75,   0,  76,   0,   0,  56,   0,  56,   0,  56,   0,  56,
     77,  77,  77,  77,  77,  77,  77,  77,  78,  78,  78,  78,  78,  78,  78,  78,
     79,  79,  79,  79,  79,  79,  79,  79,  80,  80,  80,  80,  80,  80,  80,  80,
     81,  81,  81,  81,  81,  81,  81,  81,  82,  82,  82,  82,  82,  82,  82,  82,
      0,   0,  83,  84,  85,   0,  86,  87,  56,  56,  88,  88,  89,   0,  90,   0,
      0,   0,  91,  92,  93,   0,  94,  95,  96,  96,  96,  96,  97,   0,   0,   0,
      0,   0,  98,  99,   0,   0, 100, 101,  56,  56, 102, 102,   0,   0,   0,   0,
      0,   0, 103, 104, 105,   0, 106, 107,  56,  56, 108, 108,  50,   0,   0,   0,
      0,   0, 109, 110, 111,   0, 112, 113, 114, 114, 115, 115, 116,   0,   0,   0,
      0,   0,   0,   0,   0,   0, 117,   0,   0,   0, 118, 119,   0,   0,   0,   0,
      0,   0, 120,   0,   0,   0,   0,   0, 121, 121, 121, 121, 121, 121, 121, 121,
      0,   0,   0,   4,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 122, 122,
    122, 122, 122, 122, 122, 122, 122, 122,   4,   0, 123, 124, 125,   0,   0,   4,
      0,   4,   0,   4,   0, 126, 127, 128, 129,   0,   4,   0,   0,   4,   0,   0,
      0,   0,   0,   0,   0,   0, 130, 130,   0,   0,   0,   4,   0,   4,   0,   0,
      4,   0,   4,   0,   4,   0,   0,   0,   0,   4,   0,   4,   0, 131,   4,   0,
      0,   0,   0,   4,   0, 132,   0,   0,   4,   0, 133, 134, 135, 136, 133,   0,
    137, 138, 139, 140,   4,   0,   4,   0, 141, 141, 141, 141, 141, 141, 141, 141,
    142, 143, 144, 145, 146, 147, 148,   0,   0,   0,   0, 149, 150, 151, 152, 153,
    154, 154, 154, 154, 154, 154, 154, 154, 154, 154, 154, 154,   0,   0,   0,   0,
     37,  37,  37,  37,  37,  37,  37,  37,  37,  37,  37,   0,   0,   0,   0,   0,
    155, 155, 155, 155, 155, 155, 155, 155, 155, 155,   0,   0,   0,   0,   0,   0,
};

/* Full_Case_Folding: 2040 bytes. */

static RE_FullCaseFolding re_full_case_folding_table[] = {
    {     0, {   0,   0}},
    {    32, {   0,   0}},
    {   775, {   0,   0}},
    {  -108, { 115,   0}},
    {     1, {   0,   0}},
    {  -199, { 775,   0}},
    {   371, { 110,   0}},
    {  -121, {   0,   0}},
    {  -268, {   0,   0}},
    {   210, {   0,   0}},
    {   206, {   0,   0}},
    {   205, {   0,   0}},
    {    79, {   0,   0}},
    {   202, {   0,   0}},
    {   203, {   0,   0}},
    {   207, {   0,   0}},
    {   211, {   0,   0}},
    {   209, {   0,   0}},
    {   213, {   0,   0}},
    {   214, {   0,   0}},
    {   218, {   0,   0}},
    {   217, {   0,   0}},
    {   219, {   0,   0}},
    {     2, {   0,   0}},
    {  -390, { 780,   0}},
    {   -97, {   0,   0}},
    {   -56, {   0,   0}},
    {  -130, {   0,   0}},
    { 10795, {   0,   0}},
    {  -163, {   0,   0}},
    { 10792, {   0,   0}},
    {  -195, {   0,   0}},
    {    69, {   0,   0}},
    {    71, {   0,   0}},
    {   116, {   0,   0}},
    {    38, {   0,   0}},
    {    37, {   0,   0}},
    {    64, {   0,   0}},
    {    63, {   0,   0}},
    {    41, { 776, 769}},
    {    21, { 776, 769}},
    {     8, {   0,   0}},
    {   -30, {   0,   0}},
    {   -25, {   0,   0}},
    {   -15, {   0,   0}},
    {   -22, {   0,   0}},
    {   -54, {   0,   0}},
    {   -48, {   0,   0}},
    {   -60, {   0,   0}},
    {   -64, {   0,   0}},
    {    -7, {   0,   0}},
    {    80, {   0,   0}},
    {    15, {   0,   0}},
    {    48, {   0,   0}},
    {   -34, {1410,   0}},
    {  7264, {   0,   0}},
    {    -8, {   0,   0}},
    { -6222, {   0,   0}},
    { -6221, {   0,   0}},
    { -6212, {   0,   0}},
    { -6210, {   0,   0}},
    { -6211, {   0,   0}},
    { -6204, {   0,   0}},
    { -6180, {   0,   0}},
    { 35267, {   0,   0}},
    { -3008, {   0,   0}},
    { -7726, { 817,   0}},
    { -7715, { 776,   0}},
    { -7713, { 778,   0}},
    { -7712, { 778,   0}},
    { -7737, { 702,   0}},
    {   -58, {   0,   0}},
    { -7723, { 115,   0}},
    { -7051, { 787,   0}},
    { -7053, { 787, 768}},
    { -7055, { 787, 769}},
    { -7057, { 787, 834}},
    {  -128, { 953,   0}},
    {  -136, { 953,   0}},
    {  -112, { 953,   0}},
    {  -120, { 953,   0}},
    {   -64, { 953,   0}},
    {   -72, { 953,   0}},
    {   -66, { 953,   0}},
    { -7170, { 953,   0}},
    { -7176, { 953,   0}},
    { -7173, { 834,   0}},
    { -7174, { 834, 953}},
    {   -74, {   0,   0}},
    { -7179, { 953,   0}},
    { -7173, {   0,   0}},
    {   -78, { 953,   0}},
    { -7180, { 953,   0}},
    { -7190, { 953,   0}},
    { -7183, { 834,   0}},
    { -7184, { 834, 953}},
    {   -86, {   0,   0}},
    { -7189, { 953,   0}},
    { -7193, { 776, 768}},
    { -7194, { 776, 769}},
    { -7197, { 834,   0}},
    { -7198, { 776, 834}},
    {  -100, {   0,   0}},
    { -7197, { 776, 768}},
    { -7198, { 776, 769}},
    { -7203, { 787,   0}},
    { -7201, { 834,   0}},
    { -7202, { 776, 834}},
    {  -112, {   0,   0}},
    {  -118, { 953,   0}},
    { -7210, { 953,   0}},
    { -7206, { 953,   0}},
    { -7213, { 834,   0}},
    { -7214, { 834, 953}},
    {  -128, {   0,   0}},
    {  -126, {   0,   0}},
    { -7219, { 953,   0}},
    { -7517, {   0,   0}},
    { -8383, {   0,   0}},
    { -8262, {   0,   0}},
    {    28, {   0,   0}},
    {    16, {   0,   0}},
    {    26, {   0,   0}},
    {-10743, {   0,   0}},
    { -3814, {   0,   0}},
    {-10727, {   0,   0}},
    {-10780, {   0,   0}},
    {-10749, {   0,   0}},
    {-10783, {   0,   0}},
    {-10782, {   0,   0}},
    {-10815, {   0,   0}},
    {-35332, {   0,   0}},
    {-42280, {   0,   0}},
    {-42308, {   0,   0}},
    {-42319, {   0,   0}},
    {-42315, {   0,   0}},
    {-42305, {   0,   0}},
    {-42258, {   0,   0}},
    {-42282, {   0,   0}},
    {-42261, {   0,   0}},
    {   928, {   0,   0}},
    {-38864, {   0,   0}},
    {-64154, { 102,   0}},
    {-64155, { 105,   0}},
    {-64156, { 108,   0}},
    {-64157, { 102, 105}},
    {-64158, { 102, 108}},
    {-64146, { 116,   0}},
    {-64147, { 116,   0}},
    {-62879, {1398,   0}},
    {-62880, {1381,   0}},
    {-62881, {1387,   0}},
    {-62872, {1398,   0}},
    {-62883, {1389,   0}},
    {    40, {   0,   0}},
    {    34, {   0,   0}},
};

/* Full_Case_Folding: 1248 bytes. */

int re_get_full_case_folding(RE_UINT32 ch, RE_UINT32* codepoints) {
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;
    RE_FullCaseFolding* case_folding;
    int count;

    f = ch >> 13;
    code = ch ^ (f << 13);
    pos = (RE_UINT32)re_full_case_folding_stage_1[f] << 5;
    f = code >> 8;
    code ^= f << 8;
    pos = (RE_UINT32)re_full_case_folding_stage_2[pos + f] << 5;
    f = code >> 3;
    code ^= f << 3;
    pos = (RE_UINT32)re_full_case_folding_stage_3[pos + f] << 3;
    value = re_full_case_folding_stage_4[pos + code];

    case_folding = &re_full_case_folding_table[value];

    codepoints[0] = (RE_UINT32)((RE_INT32)ch + case_folding->diff);
    count = 1;

    while (count < RE_MAX_FOLDED && case_folding->codepoints[count - 1] != 0) {
        codepoints[count] = case_folding->codepoints[count - 1];
        ++count;
    }

    return count;
}

/* Property function table. */

RE_GetPropertyFunc re_get_property[] = {
    re_get_general_category,
    re_get_block,
    re_get_script,
    0,
    re_get_word_break,
    re_get_grapheme_cluster_break,
    re_get_sentence_break,
    re_get_math,
    re_get_alphabetic,
    re_get_lowercase,
    re_get_uppercase,
    re_get_cased,
    re_get_case_ignorable,
    re_get_changes_when_lowercased,
    re_get_changes_when_uppercased,
    re_get_changes_when_titlecased,
    re_get_changes_when_casefolded,
    re_get_changes_when_casemapped,
    re_get_id_start,
    re_get_id_continue,
    re_get_xid_start,
    re_get_xid_continue,
    re_get_default_ignorable_code_point,
    re_get_grapheme_extend,
    re_get_grapheme_base,
    re_get_grapheme_link,
    re_get_white_space,
    re_get_bidi_control,
    re_get_join_control,
    re_get_dash,
    re_get_hyphen,
    re_get_quotation_mark,
    re_get_terminal_punctuation,
    re_get_other_math,
    re_get_hex_digit,
    re_get_ascii_hex_digit,
    re_get_other_alphabetic,
    re_get_ideographic,
    re_get_diacritic,
    re_get_extender,
    re_get_other_lowercase,
    re_get_other_uppercase,
    re_get_noncharacter_code_point,
    re_get_other_grapheme_extend,
    re_get_ids_binary_operator,
    re_get_ids_trinary_operator,
    re_get_radical,
    re_get_unified_ideograph,
    re_get_other_default_ignorable_code_point,
    re_get_deprecated,
    re_get_soft_dotted,
    re_get_logical_order_exception,
    re_get_other_id_start,
    re_get_other_id_continue,
    re_get_sentence_terminal,
    re_get_variation_selector,
    re_get_pattern_white_space,
    re_get_pattern_syntax,
    re_get_prepended_concatenation_mark,
    re_get_regional_indicator,
    re_get_hangul_syllable_type,
    re_get_bidi_class,
    re_get_canonical_combining_class,
    re_get_decomposition_type,
    re_get_east_asian_width,
    re_get_joining_group,
    re_get_joining_type,
    re_get_line_break,
    re_get_numeric_type,
    re_get_numeric_value,
    re_get_bidi_mirrored,
    re_get_indic_positional_category,
    re_get_indic_syllabic_category,
    re_get_emoji,
    re_get_emoji_presentation,
    re_get_emoji_modifier,
    re_get_emoji_modifier_base,
    re_get_emoji_component,
    re_get_extended_pictographic,
    re_get_nfd_quick_check,
    re_get_nfc_quick_check,
    re_get_nfkd_quick_check,
    re_get_nfkc_quick_check,
    re_get_alphanumeric,
    re_get_any,
    re_get_blank,
    re_get_graph,
    re_get_print,
    re_get_word,
    re_get_xdigit,
    re_get_posix_digit,
    re_get_posix_alnum,
    re_get_posix_punct,
    re_get_posix_xdigit,
};
