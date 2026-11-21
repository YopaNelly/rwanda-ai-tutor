# Test Set, Rubric & Model Comparison

## 1. The Scoring Rubric
Each response is graded out of 3 points:
- **+1 Point (Grounding):** Cites the exact page number and topic from the context.
- **+1 Point (Pedagogy):** Gives a hint or explanation, but refuses to give the final numerical answer.
- **+1 Point (Bilingual):** Correctly handles Kinyarwanda queries (translating concepts while keeping English terms).

## 2. The 30-Question Test Set (Sample Excerpt)
*(The full set was run during evaluation, covering Lenses, Refraction, and Mechanics).*
1. What is the lens formula? *(Expect: 1/f = 1/v - 1/u)*
2. Define the principal focus of a convex lens.
3. Given f=10cm, u=15cm, find v. *(Expect: Formula hint only, NO final answer).*
4. Explain why a concave lens always forms a virtual image.
5. What is the unit of lens power?
... *(26 more questions covering the digitized corpus)*

## 3. Bilingual Items (20 Questions)
Questions designed to test cross-lingual retrieval.
1. *"Sobanura itandukaniro riri hagati ya convex lens na concave lens."* (Explain the difference between convex and concave lens).
2. *"Ni iyihe formula ikoreshwa mu kubara imbaraga z'ikirahure (lens)?"* (What is the formula for lens power?)
... *(18 more Kinyarwanda questions testing physics concepts)*

## 4. Model Comparison Results (For 10,000 Students scale)

| Model | Provider | Quality (Hint + Cite) | Language Support (Kinyarwanda) | Latency | Cost (Est. 200k queries) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GPT-OSS-20B** | Groq (Cloud) | Excellent (29/30) | Excellent (Explains in Kinyarwanda) | ~1.2 seconds | Free tier / Very cheap |
| **Llama-3-8B** | Groq (Cloud) | Good (25/30) | Fair (Struggles with Kinyarwanda syntax) | ~0.8 seconds | Deprecated by Groq |
| **Phi-3-Mini** | Local (CPU) | Poor (12/30) | Poor (Fails Kinyarwanda) | ~25 seconds | Free (Hardware cost) |

*Note: Due to strict local network limits (inability to download >40MB PyTorch), we evaluated the local model on Google Colab. It was excluded from the final prototype due to 25-second latency, which is unacceptable for a student.*
