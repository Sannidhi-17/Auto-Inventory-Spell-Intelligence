# 🚗 Automotive Part Spell Checker

A Streamlit-based application to help automotive businesses quickly validate and correct automotive part names using a combination of **fuzzy matching, AI/LLM correction, and manual review**. The app maintains a **master parts list** that gets updated automatically for future reference.

---

## Table of Contents

- [Features](#features)
- [Project Workflow](#project-workflow)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)

---

## Features

1. **Fuzzy Matching (RapidFuzz)**  
   Quickly matches user input against a master parts list with confidence scoring.

2. **Generative AI / LLM Correction**  
   Medium-confidence entries are sent to a small LLaMA-based model for smarter spelling correction.

3. **Manual Review**  
   Low-confidence entries are manually reviewed. Users can confirm or correct the part name, which is then added to the master list.

4. **Master Parts List**  
   Automatically updated with new or confirmed correct parts.

5. **Download CSV**  
   Users can download the current master parts list at any time.

---

## Project Workflow

```text
User Input (Part Name)
        ↓
Tier 1 → Fuzzy Match (RapidFuzz)
        ↓
If confidence > 85 → Accept
If 60–85 → Send to GenAI
If <60 → Manual Review
        ↓
Tier 2 → LLM Correction + Confidence
        ↓
If confident → Accept
Else → Manual Queue
        ↓
Tier 3 → Human Corrects
        ↓
Master List Updated
```
