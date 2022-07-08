// Example of using API4AI image anonymization API.

// Use 'demo' mode just to try api4ai for free. Free demo is rate limited.
// For more details visit:
//   https://api4.ai
// Use 'rapidapi' if you want to try api4ai via RapidAPI marketplace.
// For more details visit:
//   https://rapidapi.com/api4ai-api4ai-default/api/image-anonymization/details
const MODE = 'demo'

// Your RapidAPI key. Fill this variable with the proper value if you want
// to try api4ai via RapidAPI marketplace.
const RAPIDAPI_KEY = ''

const OPTIONS = {
  demo: {
    url: 'https://demo.api4ai.cloud/img-anonymization/v1/results',
    headers: { 'A4A-CLIENT-APP-ID': 'sample' }
  },
  rapidapi: {
    url: 'https://image-anonymization.p.rapidapi.com/v1/results',
    headers: { 'X-RapidAPI-Key': RAPIDAPI_KEY }
  }
}

document.addEventListener('DOMContentLoaded', function (event) {
  const input = document.getElementById('file')
  const resultImage = document.getElementById('result-image')
  const sectionParsedImage = document.getElementById('sectionParsedImage')
  const sectionParsedObjects = document.getElementById('sectionParsedObjects')
  const parsedObjects = document.getElementById('parsedObjects')
  const spinner = document.getElementById('spinner')

  input.addEventListener('change', (event) => {
    const file = event.target.files[0]
    if (!file) {
      return false
    }

    sectionParsedImage.hidden = true
    sectionParsedObjects.hidden = true
    spinner.hidden = false

    // Preapare request: form.
    const form = new FormData()
    form.append('image', file)
    const requestOptions = {
      method: 'POST',
      body: form,
      headers: OPTIONS[MODE].headers
    }

    // Make request.
    fetch(OPTIONS[MODE].url, requestOptions)
      .then(response => response.json())
      .then(function (response) {
        // Parse response and show result image.
        const responseEntities = response.results[0].entities
        const imgBase64 = responseEntities[0].image
        const imgFormat = responseEntities[0].format.toLowerCase()
        resultImage.src = `data:image/${imgFormat};base64,` + imgBase64
        parsedObjects.textContent = JSON.stringify(responseEntities[1].objects, undefined, 2)
        sectionParsedImage.hidden = false
        sectionParsedObjects.hidden = false
      })
      .catch(function (error) {
        // Error can be handled here.
        console.error(error)
      })
      .then(function () {
        spinner.hidden = true
      })
  })
})
