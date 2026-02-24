
![PsyGemma Interface](./psygemma.jpg)


## Project Overview
**PsyGemma** is an advanced clinical support tool that transforms raw patient diary entries into structured medical documentation. By leveraging the **MedGemma** model, the system identifies depressive markers and maps them directly to **DSM-5-TR criteria**, enabling clinicians to monitor mental health trajectories with evidence-based precision.


## 1. Core Workflow
1.	Record: Users record diary entries which the system tracks chronologically.
2.	Process: Using targeted prompting, MedGemma reconstructs raw narratives into structured clinical documentation.
3.	Structure: Each entry receives a structured summary, a risk probability, and highlighted evidence segments.
4.	Visualize: The UI displays daily status using intuitive color coding: Green (no significant signals), Orange (mild/emerging concern), and Red (high-risk linguistic signals).


## 2. Key Interface Features
* **Interactive Timeline**: Visualizing the persistence of clinical symptoms over time to track recovery or decline.
* **Clinical Evidence Dashboard**: Aggregating bookmarked diary segments into consolidated DSM-5-TR clinical reports.
* **Smart Diaries**: Automatically highlighting clinical evidence within raw logs. 
    * *Interaction*: Users can **click highlights** or **drag to select** new sentences to bookmark for deeper analysis.


## 3. PsyGemma allows clinicians to:
* Manually highlight key sentences and assign a status—critical, moderate, or normal—to each daily entry
* Synthesis a DSM-5-TR-based clinical report based only on selected evidence
  
**Key Innovation & Impact**: PsyGemma shifts from static classification to temporal risk monitoring, visualizing diary evolution through color-coded signals. Rather than acting as a one-time sentiment analyzer, it functions as a continuous mental health signal interpreter designed for ethical, clinician-centered decision support.
