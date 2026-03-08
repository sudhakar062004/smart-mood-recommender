---
description: how to retrain the mood detection model
---

1. Ensure the training data in `dataset/moods.csv` is updated as desired.
2. Run the training script:
// turbo
```powershell
python train_model.py
```
3. The script will generate updated `mood_model.pkl` and `tfidf_vectorizer.pkl` files.
