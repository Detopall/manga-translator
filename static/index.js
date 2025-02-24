"use strict";

const fileInput = document.getElementById("fileInput");
const translateButton = document.getElementById("translateButton");
const spinner = document.getElementById("spinner");
const inputImage = document.getElementById("inputImage");
const outputImage = document.getElementById("outputImage");
const downloadButton = document.getElementById("downloadButton");
const downloadLink = document.getElementById("downloadLink");

downloadButton.style.display = "none";

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

		const response = await fetch("/predict", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ image: base64Image }),
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
