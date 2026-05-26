const form = document.getElementById('predictionForm');
const result = document.getElementById('result');
const priceText = document.getElementById('priceText');
const confidenceText = document.getElementById('confidenceText');
const ageChip = document.getElementById('ageChip');
const mileChip = document.getElementById('mileChip');
const ownerChip = document.getElementById('ownerChip');
const explanationList = document.getElementById('explanationList');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());

  const btn = form.querySelector('button[type="submit"]');
  btn.textContent = 'Predicting...';
  btn.disabled = true;

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const json = await res.json();

    priceText.textContent = `? ${json.estimated_price_text}`;
    confidenceText.textContent = `Confidence: ${json.confidence}%`;
    ageChip.textContent = `Age: ${json.analytics.car_age} years`;
    mileChip.textContent = `Mileage Band: ${json.analytics.mileage_band}`;
    ownerChip.textContent = `Owner Risk: ${json.analytics.owner_risk}`;

    explanationList.innerHTML = '';
    json.explanation.forEach((point) => {
      const li = document.createElement('li');
      li.textContent = point;
      explanationList.appendChild(li);
    });

    result.classList.remove('hidden');
    result.scrollIntoView({ behavior: 'smooth', block: 'center' });
  } catch (err) {
    priceText.textContent = 'Prediction failed. Try again.';
    result.classList.remove('hidden');
  } finally {
    btn.textContent = 'Predict Price';
    btn.disabled = false;
  }
});

