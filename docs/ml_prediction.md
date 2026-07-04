# Encrypted Diabetes Risk Prediction

This demo shows how the Medicrypt AI architecture can support a simple logistic regression model on encrypted medical features.

## Model

The server uses a fixed logistic regression model derived from a diabetes-style feature set:

- age
- glucose
- blood pressure
- BMI
- insulin

Weights and bias are hard-coded for a proof-of-concept:

- coefficients: [2, 3, 2, 5, 1]
- bias: -500

The server computes the encrypted linear combination and applies an encrypted comparison against `0`.

## Workflow

1. Client encrypts each medical feature locally with the existing Concrete-Python-compatible payload.
2. Client uploads encrypted payloads to the server.
3. Server runs `encrypted_logistic_regression` using only encrypted add/multiply/compare operations.
4. Server returns an encrypted binary prediction ciphertext.
5. Client decrypts the result locally.

## Run

From the `client` folder:

```powershell
python ml_prediction_app.py
```

## Notes

- This is intentionally a proof-of-concept model. It uses a simplified plaintext-backed FHE emulation on the server and a fixed logistic regression weight set.
- The current implementation preserves the existing encrypted transport and server-only ciphertext arithmetic.
- A real Concrete-Python deployment requires a supported interpreter and the `concrete-python` package.
