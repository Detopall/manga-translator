"use strict";

const fileInput = document.getElementById("fileInput");
const translateButton = document.getElementById("translateButton");
const spinner = document.getElementById("spinner");
const inputImage = document.getElementById("inputImage");
const outputImage = document.getElementById("outputImage");
const downloadButton = document.getElementById("downloadButton");
const downloadLink = document.getElementById("downloadLink");

downloadButton.style.display = "none";

const languages = {
	acehnese: "ace-ID",
	afrikaans: "af-ZA",
	akan: "ak-GH",
	albanian: "sq-AL",
	amharic: "am-ET",
	"antigua and barbuda creole english": "aig-AG",
	arabic: "ar-SA",
	"arabic egyptian": "ar-EG",
	aragonese: "an-ES",
	armenian: "hy-AM",
	assamese: "as-IN",
	asturian: "ast-ES",
	"austrian german": "de-AT",
	awadhi: "awa-IN",
	"ayacucho quechua": "quy-PE",
	azerbaijani: "az-AZ",
	"bahamas creole english": "bah-BS",
	bajan: "bjs-BB",
	balinese: "ban-ID",
	"balkan gipsy": "rm-RO",
	bambara: "bm-ML",
	banjar: "bjn-ID",
	bashkir: "ba-RU",
	basque: "eu-ES",
	belarusian: "be-BY",
	"belgian french": "fr-BE",
	bemba: "bem-ZM",
	bengali: "bn-IN",
	bhojpuri: "bho-IN",
	bihari: "bh-IN",
	bislama: "bi-VU",
	borana: "gax-KE",
	bosnian: "bs-BA",
	"bosnian (cyrillic)": "bs-Cyrl-BA",
	breton: "br-FR",
	buginese: "bug-ID",
	bulgarian: "bg-BG",
	burmese: "my-MM",
	catalan: "ca-ES",
	"catalan valencian": "cav-ES",
	cebuano: "ceb-PH",
	"central atlas tamazight": "tzm-MA",
	"central aymara": "ayr-BO",
	"central kanuri (latin script)": "knc-NG",
	"chadian arabic": "shu-TD",
	chamorro: "ch-GU",
	cherokee: "chr-US",
	chhattisgarhi: "hne-IN",
	"chinese simplified": "zh-CN",
	"chinese trad. (hong kong)": "zh-HK",
	"chinese traditional": "zh-TW",
	"chinese traditional macau": "zh-MO",
	chittagonian: "ctg-BD",
	chokwe: "cjk-AO",
	"classical greek": "grc-GR",
	"comorian ngazidja": "zdj-KM",
	coptic: "cop-EG",
	"crimean tatar": "crh-RU",
	"crioulo upper guinea": "pov-GW",
	croatian: "hr-HR",
	czech: "cs-CZ",
	danish: "da-DK",
	dari: "prs-AF",
	dimli: "diq-TR",
	dutch: "nl-NL",
	dyula: "dyu-CI",
	dzongkha: "dz-BT",
	"eastern yiddish": "ydd-US",
	emakhuwa: "vmw-MZ",
	english: "en-GB",
	"english australia": "en-AU",
	"english canada": "en-CA",
	"english india": "en-IN",
	"english ireland": "en-IE",
	"english new zealand": "en-NZ",
	"english singapore": "en-SG",
	"english south africa": "en-ZA",
	"english us": "en-US",
	esperanto: "eo-EU",
	estonian: "et-EE",
	ewe: "ee-GH",
	fanagalo: "fn-FNG",
	faroese: "fo-FO",
	fijian: "fj-FJ",
	filipino: "fil-PH",
	finnish: "fi-FI",
	flemish: "nl-BE",
	fon: "fon-BJ",
	french: "fr-FR",
	"french canada": "fr-CA",
	"french swiss": "fr-CH",
	friulian: "fur-IT",
	fula: "ff-FUL",
	galician: "gl-ES",
	gamargu: "mfi-NG",
	garo: "grt-IN",
	georgian: "ka-GE",
	german: "de-DE",
	gilbertese: "gil-KI",
	glavda: "glw-NG",
	greek: "el-GR",
	"grenadian creole english": "gcl-GD",
	guarani: "gn-PY",
	gujarati: "gu-IN",
	"guyanese creole english": "gyn-GY",
	"haitian creole french": "ht-HT",
	"halh mongolian": "khk-MN",
	hausa: "ha-NE",
	hawaiian: "haw-US",
	hebrew: "he-IL",
	higi: "hig-NG",
	hiligaynon: "hil-PH",
	"hill mari": "mrj-RU",
	hindi: "hi-IN",
	hmong: "hmn-CN",
	hungarian: "hu-HU",
	icelandic: "is-IS",
	"igbo ibo": "ibo-NG",
	"igbo ig": "ig-NG",
	ilocano: "ilo-PH",
	indonesian: "id-ID",
	"inuktitut greenlandic": "kl-GL",
	"irish gaelic": "ga-IE",
	italian: "it-IT",
	"italian swiss": "it-CH",
	"jamaican creole english": "jam-JM",
	japanese: "ja-JP",
	javanese: "jv-ID",
	jingpho: "kac-MM",
	"k'iche'": "quc-GT",
	kabiyè: "kbp-TG",
	kabuverdianu: "kea-CV",
	kabylian: "kab-DZ",
	kalenjin: "kln-KE",
	kamba: "kam-KE",
	kannada: "kn-IN",
	kanuri: "kr-KAU",
	karen: "kar-MM",
	"kashmiri (devanagari script)": "ks-IN",
	"kashmiri (arabic script)": "kas-IN",
	kazakh: "kk-KZ",
	khasi: "kha-IN",
	khmer: "km-KH",
	"kikuyu kik": "kik-KE",
	"kikuyu ki": "ki-KE",
	kimbundu: "kmb-AO",
	kinyarwanda: "rw-RW",
	kirundi: "rn-BI",
	kisii: "guz-KE",
	kongo: "kg-CG",
	konkani: "kok-IN",
	korean: "ko-KR",
	"northern kurdish": "kmr-TR",
	"kurdish sorani": "ckb-IQ",
	kyrgyz: "ky-KG",
	lao: "lo-LA",
	latgalian: "ltg-LV",
	latin: "la-XN",
	latvian: "lv-LV",
	ligurian: "lij-IT",
	limburgish: "li-NL",
	lingala: "ln-LIN",
	lithuanian: "lt-LT",
	lombard: "lmo-IT",
	"luba-kasai": "lua-CD",
	luganda: "lg-UG",
	luhya: "luy-KE",
	luo: "luo-KE",
	luxembourgish: "lb-LU",
	maa: "mas-KE",
	macedonian: "mk-MK",
	magahi: "mag-IN",
	maithili: "mai-IN",
	malagasy: "mg-MG",
	malay: "ms-MY",
	malayalam: "ml-IN",
	maldivian: "dv-MV",
	maltese: "mt-MT",
	mandara: "mfi-CM",
	manipuri: "mni-IN",
	"manx gaelic": "gv-IM",
	maori: "mi-NZ",
	marathi: "mr-IN",
	margi: "mrt-NG",
	mari: "mhr-RU",
	marshallese: "mh-MH",
	mende: "men-SL",
	meru: "mer-KE",
	mijikenda: "nyf-KE",
	minangkabau: "min-ID",
	mizo: "lus-IN",
	mongolian: "mn-MN",
	montenegrin: "sr-ME",
	morisyen: "mfe-MU",
	"moroccan arabic": "ar-MA",
	mossi: "mos-BF",
	ndau: "ndc-MZ",
	ndebele: "nr-ZA",
	nepali: "ne-NP",
	"nigerian fulfulde": "fuv-NG",
	niuean: "niu-NU",
	"north azerbaijani": "azj-AZ",
	sesotho: "nso-ZA",
	"northern uzbek": "uzn-UZ",
	"norwegian bokmål": "nb-NO",
	"norwegian nynorsk": "nn-NO",
	nuer: "nus-SS",
	nyanja: "ny-MW",
	occitan: "oc-FR",
	"occitan aran": "oc-ES",
	odia: "or-IN",
	oriya: "ory-IN",
	urdu: "ur-PK",
	palauan: "pau-PW",
	pali: "pi-IN",
	pangasinan: "pag-PH",
	papiamentu: "pap-CW",
	pashto: "ps-PK",
	persian: "fa-IR",
	pijin: "pis-SB",
	"plateau malagasy": "plt-MG",
	polish: "pl-PL",
	portuguese: "pt-PT",
	"portuguese brazil": "pt-BR",
	potawatomi: "pot-US",
	punjabi: "pa-IN",
	"punjabi (pakistan)": "pnb-PK",
	quechua: "qu-PE",
	rohingya: "rhg-MM",
	rohingyalish: "rhl-MM",
	romanian: "ro-RO",
	romansh: "roh-CH",
	rundi: "run-BI",
	russian: "ru-RU",
	"saint lucian creole french": "acf-LC",
	samoan: "sm-WS",
	sango: "sg-CF",
	sanskrit: "sa-IN",
	santali: "sat-IN",
	sardinian: "sc-IT",
	"scots gaelic": "gd-GB",
	sena: "seh-ZW",
	"serbian cyrillic": "sr-Cyrl-RS",
	"serbian latin": "sr-Latn-RS",
	"seselwa creole french": "crs-SC",
	"setswana (south africa)": "tn-ZA",
	shan: "shn-MM",
	shona: "sn-ZW",
	sicilian: "scn-IT",
	silesian: "szl-PL",
	"sindhi snd": "snd-PK",
	"sindhi sd": "sd-PK",
	sinhala: "si-LK",
	slovak: "sk-SK",
	slovenian: "sl-SI",
	somali: "so-SO",
	"sotho southern": "st-LS",
	"south azerbaijani": "azb-AZ",
	"southern pashto": "pbt-PK",
	"southwestern dinka": "dik-SS",
	spanish: "es-ES",
	"spanish argentina": "es-AR",
	"spanish colombia": "es-CO",
	"spanish latin america": "es-419",
	"spanish mexico": "es-MX",
	"spanish united states": "es-US",
	"sranan tongo": "srn-SR",
	"standard latvian": "lvs-LV",
	"standard malay": "zsm-MY",
	sundanese: "su-ID",
	swahili: "sw-KE",
	swati: "ss-SZ",
	swedish: "sv-SE",
	"swiss german": "de-CH",
	"syriac (aramaic)": "syc-TR",
	tagalog: "tl-PH",
	tahitian: "ty-PF",
	tajik: "tg-TJ",
	"tamashek (tuareg)": "tmh-DZ",
	tamasheq: "taq-ML",
	"tamil india": "ta-IN",
	"tamil sri lanka": "ta-LK",
	taroko: "trv-TW",
	tatar: "tt-RU",
	telugu: "te-IN",
	tetum: "tet-TL",
	thai: "th-TH",
	tibetan: "bo-CN",
	tigrinya: "ti-ET",
	"tok pisin": "tpi-PG",
	tokelauan: "tkl-TK",
	tongan: "to-TO",
	"tosk albanian": "als-AL",
	tsonga: "ts-ZA",
	tswa: "tsc-MZ",
	tswana: "tn-BW",
	tumbuka: "tum-MW",
	turkish: "tr-TR",
	turkmen: "tk-TM",
	tuvaluan: "tvl-TV",
	twi: "tw-GH",
	udmurt: "udm-RU",
	ukrainian: "uk-UA",
	uma: "ppk-ID",
	umbundu: "umb-AO",
	"uyghur uig": "uig-CN",
	"uyghur ug": "ug-CN",
	uzbek: "uz-UZ",
	venetian: "vec-IT",
	vietnamese: "vi-VN",
	"vincentian creole english": "svc-VC",
	"virgin islands creole english": "vic-US",
	wallisian: "wls-WF",
	"waray (philippines)": "war-PH",
	welsh: "cy-GB",
	"west central oromo": "gaz-ET",
	"western persian": "pes-IR",
	wolof: "wo-SN",
	xhosa: "xh-ZA",
	yiddish: "yi-YD",
	yoruba: "yo-NG",
	zulu: "zu-ZA",
};

document.addEventListener("DOMContentLoaded", () => {
	const selectContainer = document.getElementById("targetLanguage");
	let languageOptions = "";
	for (const language in languages) {
		languageOptions += `<option value="${languages[language]}">${language}</option>`;
	}
	selectContainer.insertAdjacentHTML("beforeend", languageOptions);
});

fileInput.addEventListener("change", () => {
	if (fileInput.files.length === 0) {
		alert("Please select an image file.");
		return;
	}

	// Clear the previous images
	inputImage.src = "";
	outputImage.src = "";

	const file = fileInput.files[0];
	const reader = new FileReader();

	reader.onload = function () {
		const base64Image = reader.result.split(",")[1];
		inputImage.src = `data:image/jpeg;base64,${base64Image}`;
		inputImage.style.display = "block";
	};

	reader.readAsDataURL(file);
});

async function predict() {
	if (fileInput.files.length === 0) {
		alert("Please select an image file.");
		return;
	}

	const file = fileInput.files[0];
	const reader = new FileReader();

	reader.onloadend = async function () {
		const base64Image = reader.result.split(",")[1];
		const target_lang = document.getElementById("targetLanguage").value;

		const response = await fetch("/predict", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ image: base64Image, target_lang: target_lang }),
		});

		const result = await response.json();
		console.log(result);

		if (response.status !== 200) {
			alert(result.message);

			// Reset the input
			fileInput.value = "";
			inputImage.style.display = "none";
			outputImage.style.display = "none";
			spinner.style.display = "none";
			downloadButton.style.display = "none";
			translateButton.style.display = "block";
			return;
		}

		outputImage.src = `data:image/jpeg;base64,${result.image}`;
		outputImage.style.display = "block";

		// Generate timestamp for the download link
		const timestamp = new Date().toISOString().replace(/[^\w\s]/gi, "-");
		downloadLink.href = outputImage.src;
		downloadLink.download = `MangaTranslator-${timestamp}.jpg`;

		downloadButton.style.display = "block";

		translateButton.style.display = "inline-block";
		spinner.style.display = "none";
	};

	reader.readAsDataURL(file);

	translateButton.style.display = "none";
	spinner.style.display = "block";
}
