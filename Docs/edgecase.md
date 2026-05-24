# Edge Cases and Mitigation Strategies

This document outlines potential edge cases that may arise during the execution of the AI-Powered Restaurant Recommendation System, along with strategies to mitigate them.

## 1. Data Ingestion & Preprocessing Edge Cases
* **Missing or Malformed Data:** 
  * *Scenario:* The Hugging Face dataset has missing values for crucial fields like 'Cuisine', 'Cost', or 'Rating', or incorrect data types (e.g., text in a numeric cost column).
  * *Mitigation:* Implement robust data cleaning during Phase 1. Drop records with missing critical fields or impute them (e.g., setting a default rating of 0). Use regex to clean strings containing numbers (like "₹500 for two").
* **API Rate Limits / Unavailability:**
  * *Scenario:* The Hugging Face dataset API is temporarily down or rate-limited.
  * *Mitigation:* Cache the downloaded dataset locally. The application should only attempt to download if the local file does not exist.

## 2. User Input & Filtering Edge Cases
* **Over-Constrained Inputs (Zero Results):**
  * *Scenario:* A user selects conflicting or highly restrictive preferences (e.g., Budget: Low, Rating: >4.9, Cuisine: Caviar, Location: Small Village). The hard filter returns 0 candidates.
  * *Mitigation:* Detect empty filter results before querying the LLM. Display a friendly message asking the user to broaden their search criteria, or automatically relax the strictness of constraints (e.g., lower the minimum rating or expand the budget slightly) and notify the user.
* **Under-Constrained Inputs (Too Many Results):**
  * *Scenario:* A user simply selects "Delhi" and "Medium Budget," returning 10,000 restaurants. Feeding this to the LLM will exceed token limits.
  * *Mitigation:* Limit the filtered output sent to the LLM to the top N (e.g., top 10 or 20) by sorting based on rating or popularity before prompt injection.
* **Ambiguous or Invalid Text Input:**
  * *Scenario:* A user enters gibberish or harmful prompt injections into the "Additional Preferences" text area.
  * *Mitigation:* Sanitize text inputs. The LLM prompt should include system instructions to ignore harmful or irrelevant text.

## 3. LLM Integration Edge Cases
* **Token Limit Exceeded:**
  * *Scenario:* The prompt size grows too large due to too many restaurant candidates or overly long user preferences.
  * *Mitigation:* Truncate the list of candidate restaurants dynamically based on the token context window of the chosen LLM.
* **Hallucinations:**
  * *Scenario:* The LLM recommends a restaurant that isn't in the provided candidate list or fabricates menu items/prices.
  * *Mitigation:* Use strict prompt engineering instructions (e.g., "ONLY recommend restaurants from the provided list. Do not invent information.").
* **LLM API Latency or Timeout:**
  * *Scenario:* The LLM takes too long to respond, leading to a poor user experience or timeout error.
  * *Mitigation:* Implement asynchronous calls, display a loading indicator in the UI, and configure reasonable timeout thresholds with fallback generic messages.

## 4. User Interface Edge Cases
* **Concurrent Users / Load:**
  * *Scenario:* Multiple users query the app simultaneously, exhausting the LLM API rate limits.
  * *Mitigation:* Implement basic caching (e.g., `st.cache_data` in Streamlit) for identical queries to save API calls. Handle 429 Too Many Requests errors gracefully.
