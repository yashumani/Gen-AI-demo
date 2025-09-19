I have to take a few step back and redefine the prompts to use in this process. I am think I should use the Output of each Prompt to do deep dive analysis.

Prompt 1 

STEP 1: Surface-Level Analysis (Lines Table Only)
	•	Input: Just the Lines Table (Weekly + MTD) from Google Sheet
	•	Prompt Goal: Extract biggest changes in metrics (WoW, MTD)
	•	Output: Ranked Top 5 metrics by materiality of change

Prompt 2 

STEP 2: Top 5 Takeaways
	•	Input: Use the Step 1 output and enrich slightly using benchmarks (vs. Forecast, PY)
	•	Prompt Goal: Summarize top 5 insights with context on movement
	•	Output: Bulletized top 5 takeaways
	•	Optionally cache this in your final document.

Prompt 3
STEP 3: Deep Dive Analysis (Per Metric in Top 5)
	•	Loop over each metric in the Top 5
	•	Input:
	•	Metric’s raw data
	•	Associated rows from Data Dictionary
	•	Any matching Promotions, Price Plans, Business Knowledge, Channel Attribution, and News
	•	Prompt Goal: For each metric, explain root causes of change, with quantification and cross-reference

Prompt 4 

STEP 4: Channel-Level Attribution
	•	Input: Channel tables + filtered top metrics
	•	Prompt Goal: Attribute performance drivers to specific channels
	•	Output: Attribution summary for each relevant metric

Prompt 5 
STEP 5: Interdependency & Correlation
	Input:
	•	Top 5 metric movements
	•	Their interactions from business knowledge + dictionary
	•	Prompt Goal:
	•	Describe logical metric-to-metric influence
	•	Provide 5 correlation bullets across:
	•	Promotions
	•	Price Plans
	•	News Events
	•	Channel Trends
	•	Business Logic

Prompt 6 

You then stitch together:
	•	Step 2 (Top 5 Takeaways)
	•	Step 3 (Metric Commentary)
	•	Step 4 (Channel Attribution)
	•	Step 5 (Interdependency & Correlation)

 Prompt Engineering Techniques Used

Step	Technique Used	Description
1-2	Zero-shot	Extracting key changes without training
3	Chain-of-Thought	Sequential reasoning from data to cause
3-5	Tree-of-Thoughts	Branching through promotions/news/business logic
5	Cross-context Retrieval (manual RAG)	You emulate RAG by explicitly pulling reference chunks into each metric prompt
