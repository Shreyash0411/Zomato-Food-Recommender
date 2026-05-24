# Evaluation Criteria by Phase

This document defines the evaluation criteria (success metrics) for each phase of the implementation plan to ensure the project stays on track and meets quality standards.

## Phase 1: Project Setup and Data Ingestion
**Evaluation Criteria:**
* **Successful Download:** The dataset is reliably downloaded from Hugging Face programmatically.
* **Data Quality Check:** The resulting structured file (CSV/DB) has no Null values in critical columns (Name, Location, Cuisine, Rating).
* **Data Types:** Numerical columns (Cost, Rating) are strictly parsed as integers or floats, ready for mathematical filtering.
* **Reproducibility:** A single script or notebook can run end-to-end to generate the cleaned dataset from scratch.

## Phase 2: Backend Integration & Data Filtering Layer
**Evaluation Criteria:**
* **Filtering Accuracy:** Given a set of test parameters (e.g., "Delhi", "Italian", "Rating >= 4.0"), the function returns only records that strictly match these conditions.
* **Boundary Handling:** The filtering logic gracefully handles cases where 0 records match, without throwing unhandled exceptions.
* **Performance Check:** Filtering operations on the dataset execute in under 1 second to maintain low latency before the LLM step.
* **Data Formatting:** The output of the filter is correctly serialized into a JSON or Markdown string suitable for LLM context injection.

## Phase 3: LLM Engine Integration & Prompt Engineering
**Evaluation Criteria:**
* **API Reliability:** The application successfully authenticates and communicates with the LLM API provider.
* **Instruction Following:** The LLM consistently picks restaurants *only* from the provided filtered context and does not hallucinate outside options.
* **Output Formatting:** The LLM's output consistently follows the required structure (e.g., Restaurant Name, Rating, Explanation) without breaking the parsing logic.
* **Reasoning Quality:** The generated explanations logically connect the user's specific preferences (e.g., "family-friendly") to the chosen restaurant.

## Phase 4: User Interface (UI) Development
**Evaluation Criteria:**
* **Input Validation:** The UI successfully prevents invalid submissions (e.g., submitting without selecting a location).
* **State Management:** User inputs are preserved correctly, and the UI doesn't unnecessarily refresh and lose data.
* **Responsiveness:** The app displays a clear loading state while waiting for the LLM to return results.
* **Visual Clarity:** The final recommendations are easy to read, appropriately formatted (e.g., bold names, clear costs), and visually distinct from one another.

## Phase 5: Polish, Optimization, and Deployment
**Evaluation Criteria:**
* **End-to-End Functionality:** A user can open the app, input data, and receive a sensible recommendation without encountering any crashes or blank screens.
* **Error Resilience:** Simulated API failures or empty data queries result in user-friendly error messages rather than stack traces.
* **Documentation:** The `README.md` is complete, allowing a new developer to clone, setup, and run the project locally within 10 minutes.
