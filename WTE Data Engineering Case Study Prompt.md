# WisdomTree Europe Data Engineering Case Study, January 2025

### **Data Summary**

In the attached file, you will find several datasets:  
- Two years of **NAV history**, by day, for four WisdomTree products. Net Asset Value represents the unit price of an ETF/ETC/ETP at market close for a respective day.   
- Rolling 1-year files containing **holdings of clients**, provided quarterly. The reporting partnership started in December 2023 and is received on each quarter-end. Each reporting covers the preceding 12 months, so restatements or alterations to previous months will be handled in a subsequent reporting cycle.  

### **WisdomTree Products Included in the Case Study**

| WT ID   | Ticker | Product Name                                            |
|---------|--------|---------------------------------------------------------|
| 1001310 | CRUD   | WisdomTree WTI Crude Oil                                |
| 1001513 | BRNT   | WisdomTree Brent Crude Oil                              |
| 1001656 | GGRA   | WisdomTree Global Quality Dividend Growth UCITS ETF     |
| 3105371 | WCLD   | WisdomTree Cloud Computing UCITS ETF                    |

---

### **Expense Ratios**

WisdomTree accrues revenue equal to the product of the daily adjusted MER against the assets for each day.  

| Expense Ratio | WT ID   |
|---------------|---------|
| 0.38%         | 1001656 |
| 0.49%         | 1001310 |
| 0.49%         | 1001513 |
| 0.40%         | 3105371 |

---

### **Corporate Actions**

Two WisdomTree products underwent recent corporate actions:  
- **GGRA**: Expense ratio changed from 28 to 38 basis points on **30 June 2024**.  
- **WCLD**: Underwent a **1:3 stock split** on **31 March 2024**.  

---

### **Case Study Instructions:**
1. **Structure a Python ETL** to load the data.  
2. The steps below may either be performed in **SQL** or **Python**.
3. **Develop a quality assurance program** to identify and resolve data quality issues. Document and implement required data curation.  
4. **Identify and architect** the best way to store rolling data.  
5. Structure a way to **retrieve the best reported AUM history per client** for each month in **2023** and **2024**.  
6. **Calculate the revenue contribution** per client, per month.  
7. Based on the AUM history, **identify monthly inflows/outflows** per product, per client. Be prepared to discuss your methodology here as well. 

---

### **Above & Beyond**

Perform a **cosine similarity analysis** to determine which client is most similar to Client 1 based on overall trading activity (**product agnostic**).

---

# **Deliverable**

The final deliverable will include:  

1. A **production-level script**, to be handed in alongside an **LLM Prompt document**, if used.  
2. Production **data frames** or **tables** that provide the following:  
   - Monthly AUM history per client.  
   - Monthly revenue contribution per client.  
   - Monthly net inflows/outflows per client.  

---

### **Additional Information**
- Upon receiving and reviewing the case study, you are welcome to email Jonathan Campbell at **jcampbell@wisdomtree.com** to set up a 15-minute chat to discuss any questions you might have. 
- There is no requirement on Python IDE to be used. If using SQL, please feel free to download a free version of SQL Server Developer Edition or SQL Server Express Edition from Microsoft.
- Your submitted code should follow **PEP 8 standards**.
- Your code should be submitted via private bitbucket repository and shared with **jcampbell@wisdomtree.com** and **gharibabu@wisdomtree.com**.
- You are encouraged to submit meaningful commits while developing the python portion of your case study. 
- Please include useful function tests to confirm dynamic, scalabale, and consistent function performance. 
- You will present your script and logic during a **60-minute call**, where you may be asked to update or adjust your work in real-time.  
- External resources are permitted, but relying too heavily on them may hinder your ability to demonstrate your knowledge during the presentation.  
- If using **Chat-GPT** or any other **LLM**, store your prompts in a separate Word document and submit it as a **PDF** alongside your assignment.

