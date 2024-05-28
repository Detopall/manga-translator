"use strict";

async function predict() {
	const fileInput = document.getElementById('fileInput');
	const translateButton = document.getElementById('translateButton');
	const spinner = document.getElementById('spinner');
	const inputImage = document.getElementById('inputImage');
	const outputImage = document.getElementById('outputImage');
	const downloadButton = document.getElementById('downloadButton');

	downloadButton.style.display = 'none';

	if (fileInput.files.length === 0) {
		alert('Please select an image file.');
		return;
	}

	const file = fileInput.files[0];
	const reader = new FileReader();

	reader.onload = function () {
		const base64Image = reader.result.split(',')[1];
		inputImage.src = `data:image/jpeg;base64,${base64Image}`;
		inputImage.style.display = 'block';
	};

	reader.readAsDataURL(file);

	translateButton.style.display = 'none';
	spinner.style.display = 'block';

	reader.onloadend = async function () {
		const base64Image = reader.result.split(',')[1];

		const response = await fetch('/predict', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ image: base64Image })
		});

		const result = await response.json();
		if (response.status !== 200) {
			alert(result.error);
			return;
		}
		outputImage.src = `data:image/jpeg;base64,${result.image}`;
		outputImage.style.display = 'block';
		downloadButton.href = outputImage.src;
		downloadButton.style.display = 'block';

		translateButton.style.display = 'inline-block';
		spinner.style.display = 'none';

	};
}
