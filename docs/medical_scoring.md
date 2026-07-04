# Encrypted Medical Risk Scoring

This phase adds an encrypted medical risk calculator that keeps all score math on the server in ciphertext form.

## Inputs

- Age
- Glucose
- Blood Pressure
- BMI
- Insulin

## Output

- Risk Score

## Mathematical Model

The score is computed as an encrypted weighted sum with a threshold bonus:

$$
\text{raw score} = 1\cdot \text{age} + 2\cdot \text{glucose} + 2\cdot \text{blood pressure} + 1\cdot \text{BMI} + 1\cdot \text{insulin}
$$

Then the server compares the encrypted raw score against the encrypted threshold value `120`.

If the encrypted comparison indicates the score is above the threshold, the encrypted score receives an encrypted bonus of `10`:

$$
\text{risk score} = \text{raw score} + (\text{compare}(\text{raw score}, 120) \times 10)
$$

Only encrypted arithmetic is used on the server:

- addition to accumulate the weighted inputs
- multiplication to apply weights and the threshold bonus
- comparison to evaluate the threshold condition
- thresholding through the threshold bonus path

The server never decrypts the data. The client performs the final decryption locally.

## Client Demo

Run the encrypted risk calculator demo from the client folder:

```powershell
python medical_scoring_app.py
```

## Server Tests

Run the focused test suite:

```powershell
python -m pytest server/tests/unit/test_medical_service.py server/tests/unit/test_prediction_service.py server/tests/integration/test_full_request_cycle.py
```

## Notes

The current codebase keeps the encryption transport stable and extends it with a new encrypted scoring workflow. The client still encrypts locally, the server only handles ciphertext, and the client decrypts the returned risk score.