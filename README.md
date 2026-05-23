#  Alzheimer's Diagnostic Intelligence Dashboard: Clinical Insights

## 📌 Project Overview
This dashboard provides a clinical deep-dive into Alzheimer's diagnostic data. By separating cognitive, functional, and lifestyle markers, the tool helps identify the strongest predictors of the disease.

---

##  Cognitive & Functional Analysis (Tab 1)

### 1. MMSE Score Density
**The Question:** *What is the cognitive "threshold" where most diagnoses occur?*

![MMSE Distribution](images/Mini-Mental%20State%20Exam%20Score.png)

**Insight:**
The Mini-Mental State Exam (MMSE) is a core diagnostic tool. In this chart, the **Orange** curve represents diagnosed patients. You will notice the peak is significantly shifted toward the lower score range (0-15), while the **Navy** (Control) peak sits higher (20-30). This visualizes the clear cognitive decline associated with a positive diagnosis.

---

### 2. Functional Assessment vs ADL
**The Question:** *Is there a linear relationship between daily activities and clinical assessment?*

![Functional vs ADL Scatter](images/Activities%20of%20Daily%20Livings%20(ADL).png)

**Insight:**
This scatter plot maps Activities of Daily Living (ADL) against the Clinical Functional Assessment. The concentration of **Orange** dots at the lower end of both axes confirms that as a patient's independence in daily life decreases, their clinical functional score drops simultaneously.

---

##  Risk Factors (Tab 2)

### 3. Symptom Prevalence
**The Question:** *Beyond memory loss, what behavioral symptoms are most frequent?*

![Symptom Prevalence Bar Chart](images/Symptom%20Prevalence%20(Diagnosed).png)

**Insight:**
This chart profiles the diagnosed cohort. While **Memory Complaints** are the most frequent, the high prevalence of **Forgetfulness** and **Confusion** highlights the multifaceted nature of the disease. Clinicians can use this to prioritize symptom management.

---

### 4. Diagnosis Rate by Education
**The Question:** *Does education level influence the probability of diagnosis?*

![Education Diagnosis Rate](images/Diagnosis%20Rate%20by%20Education.png)

**Insight:**
This visualization tests the "Cognitive Reserve" theory. It displays the percentage of patients within each educational tier who have been diagnosed, helping to identify if higher education levels act as a protective factor against early symptom onset.

---

##  Lifestyle & Trends (Tab 3)

### 5. Diagnosis Rate by Age Group
**The Question:** *At what age does the risk of Alzheimer's increase most sharply?*

![Age Group Trends](images/Diagnosis%20Rate%20by%20Age%20Group.png)

**Insight:**
Age is the primary risk factor. This bar chart tracks the diagnosis rate across 10-year brackets. It provides a clear visual representation of how the probability of a positive diagnosis scales with biological aging.

---

### 6. Sleep Quality Distribution
**The Question:** *Is poor sleep quality a consistent characteristic of diagnosed patients?*

![Sleep Quality Boxplot](images/Sleep%20Quality%20Distribution.png)

**Insight:**
By using a boxplot, we see the distribution of sleep scores. If the **Orange** box is positioned lower than the **Navy** box, it indicates that Alzheimer's patients in this dataset generally report lower quality sleep, suggesting a link between neurological health and rest patterns.

---

## 🛠 Setup & Technical Specs

* **Run Command:** `streamlit run alzheimers_dashboard.py`
* **Primary Colors:** `#BD7849` (Diagnosed) | `#2E4053` (Control)
* **Libraries:** Streamlit, Pandas, Seaborn, Matplotlib
