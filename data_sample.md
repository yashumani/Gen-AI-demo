### Minutes of Meeting

**Topic:** Automation of Data Processes (SAP, GCP, Alteryx, and ClickSense)

**Attendees:**
- Verander Verma
- Hariharan Marimuthu
- Preetham Gopal K
- Karthik Pingali
- Venkataramana Reddy Adapa
- Yashu Sharma

**Key Discussion Points:**

#### 1. Current Process & Challenges
- Existing manual process involves downloading three files manually (single source file, SCP file, and others), and additional SAP data to perform operations using Alteryx.
- SAP data extraction currently involves manual intervention, presenting a challenge for complete automation.
- Discussion about transitioning to fully automated sourcing from legacy sources (e.g., Tridica, IBM TridEager) to Google Cloud Platform (GCP).

#### 2. Potential Automation Solutions
- Automation through bot processes is planned to replicate manual processes, manage downloads, file storage, and processing automatically.
- Consideration of interim solutions like placing downloaded files on network drives (G-drive) accessible by Alteryx, bridging manual and fully automated stages.
- Exploring direct data sourcing methods (e.g., ClickSense and PMR) to streamline processes, reduce file handling, and eliminate redundancy.

#### 3. Data Processing & Integration Approach
- Files currently downloaded manually will be input to Alteryx for operations, generating final outputs.
- Interim plan: Maintain a manual or semi-automated data file (BYOD approach) until a fully automated sourcing solution is available.
- Consider merging related DTPs to simplify automation.
- Discussed leveraging Google Sheets extensively for easy and centralized access to processed data.

#### 4. SAP Integration
- Long-term plan discussed for SAP to GCP direct connectivity, currently facing timeline uncertainties.
- Two SAP automation approaches considered:
  - Bot-based automation (short-term).
  - Direct SAP-GCP connectivity (long-term).
- Team to coordinate with CSG team for SAP data timeline clarity.

#### 5. Immediate Responsibilities & Ownership
- Karthik Pingali and offshore team confirmed ongoing support and file handling for upcoming March close process (workday minus three timeline: March 26th).
- Verander Verma to provide necessary source files (Tridica, SAP, monthly project IDs) to offshore team by March 26th.
- Yashu Sharma to initiate communication and documentation efforts:
  - For SAP bot process with Shruti’s team.
  - For PMR and ClickSense sourcing discussions with Vashnavi.
  - Follow-up on Tridica availability and queries with Nathan.

#### 6. Timeline and Automation Roadmap
- Current quarter (Q1): Focus on transferring processes to interim solutions (manual/bot-based).
- Next quarter (Q2): Full automation phase with support from a third-party vendor and internal automation teams.
- Hariharan Marimuthu to revert by Monday with timeline updates after internal team discussion.

#### 7. Action Items:
- Yashu Sharma:
  - Initiate and document communications on SAP automation.
  - Follow-up on GCP availability of Tridica tables.
  - Coordinate with automation teams (Shruti, Vashnavi).
- Hariharan Marimuthu:
  - Confirm timelines by Monday.
  - Coordinate internal resources and third-party automation vendors.
- Karthik Pingali:
  - Ensure support and handling of files for March close.
  - Provide confirmation of responsibilities coverage.
- Verander Verma:
  - Share required files and facilitate offshore team operations.
  - Document process steps clearly.

**Meeting Adjourned:**
- Participants to ensure communication and documentation completion before next follow-up meeting.
- Minutes requested by Hariharan Marimuthu to avoid missing any action items.
