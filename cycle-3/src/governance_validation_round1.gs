
/**
 * ER-CyRIS Governance Expert Validation — Round 1
 * Purpose:
 *   Empirically assess governance mechanisms for explainable cybersecurity decisions.
 *
 * IMPORTANT:
 *   - This is NOT a technical alert-validation form.
 *   - This is NOT a dashboard usability form.
 *   - ER-CyRIS is used only as a cybersecurity decision-support context.
 *
 * Run:
 *   createGovernanceValidationRound1()
 *
 * The script creates:
 *   1) Google Form
 *   2) Google Sheet destination for responses
 *   3) A small index spreadsheet with respondent/edit URLs
 */

const GOV_FORM_TITLE =
  "Expert Governance Validation for Accountable Cybersecurity Risk Intelligence — Round 1";

const STUDY_CONTEXT = `
Tujuan studi ini adalah mengevaluasi mekanisme tata kelola (governance) untuk penggunaan
cybersecurity risk intelligence yang didukung AI/XAI.

ER-CyRIS digunakan hanya sebagai konteks penerapan cybersecurity decision support.
Penilaian ini TIDAK meminta Bapak/Ibu menilai akurasi model, dashboard, atau 50 alert
yang mungkin telah dinilai pada studi teknis sebelumnya.

Fokus penilaian adalah:
• apakah evidence dapat ditelusuri dan dipahami;
• siapa yang berhak menginterpretasikan dan mengambil keputusan;
• kapan rekomendasi AI boleh ditantang, dioverride, atau dieskalasi;
• bagaimana disagreement/override menjadi organizational learning;
• apakah governance benar-benar dijalankan dalam praktik, bukan hanya tertulis di kebijakan.

Estimasi waktu pengisian: ±10–15 menit.
Penilaian dilakukan secara independen. Kritik dan ketidaksetujuan sangat diharapkan.
`;

const CONSENT_TEXT = `
Saya memahami bahwa:
1) partisipasi bersifat sukarela;
2) saya diminta menilai mekanisme governance, bukan mengesahkan ER-CyRIS;
3) jawaban dapat digunakan dalam analisis ilmiah secara agregat;
4) identitas pribadi tidak akan dipublikasikan tanpa persetujuan tersendiri;
5) saya dapat menyampaikan kritik atau ketidaksetujuan terhadap model yang diajukan.
`;

const LIKERT_5 = [
  "1 — Sangat rendah / sangat tidak sesuai",
  "2 — Rendah / tidak sesuai",
  "3 — Sedang",
  "4 — Tinggi / sesuai",
  "5 — Sangat tinggi / sangat sesuai"
];

const CONSTRUCTS = [
  "C1 — Evidence Traceability",
  "C2 — Sensemaking Adequacy",
  "C3 — Decision-Authority Alignment",
  "C4 — Contestability and Escalation",
  "C5 — Learning from Overrides",
  "C6 — Institutional Enactment",
  "C7 — Accountable Reliance"
];

const CONSTRUCT_DEFINITIONS = `
C1 Evidence Traceability:
Kemampuan reviewer yang berwenang untuk menelusuri kembali data, transformasi,
konteks, explanation, uncertainty, dan human rationale yang mendasari suatu rekomendasi.

C2 Sensemaking Adequacy:
Kemampuan aktor yang bertanggung jawab untuk menghubungkan evidence teknis dengan
konteks organisasi, alternatif penjelasan, uncertainty, dan konsekuensi.

C3 Decision-Authority Alignment:
Kesesuaian antara tanggung jawab, akses evidence, kompetensi, dan kewenangan untuk
menerima, menunda, menolak, override, atau eskalasi rekomendasi.

C4 Contestability and Escalation:
Kemampuan aktor berwenang untuk mempertanyakan, menunda, override, meminta review
tambahan, atau mengeskalasi rekomendasi.

C5 Learning from Overrides:
Pemanfaatan override, disagreement, false alarm, missed threat, dan incident outcome
sebagai evidence untuk perbaikan proses teknis maupun governance.

C6 Institutional Enactment:
Sejauh mana kebijakan governance formal benar-benar diwujudkan dalam praktik harian,
decision rights, dokumentasi, review, dan konsekuensi.

C7 Accountable Reliance:
Penggunaan rekomendasi AI yang proporsional terhadap kemampuan sistem, uncertainty,
konteks, dan konsekuensi, serta tetap dapat ditinjau dan dipertanyakan.
`;

const PROPOSITIONS = [
  {
    id: "P1",
    title: "Evidence Traceability under Cybersecurity Uncertainty",
    text:
      "Dalam kondisi ketidakpastian cybersecurity yang tinggi, evidence yang traceable dan disajikan sesuai kebutuhan peran dapat meningkatkan interpretasi alert dengan mengurangi information asymmetry antara technical analyst dan risk owner. Manfaat ini dapat melemah ketika terjadi information overload, provenance yang buruk, atau keterbatasan expertise."
  },
  {
    id: "P2",
    title: "Sensemaking Adequacy",
    text:
      "Explainable evidence dapat meningkatkan cybersecurity risk judgment ketika membantu analis memahami konteks, alternative explanations, dan uncertainty. Namun explanation juga dapat meningkatkan over-reliance jika diperlakukan sebagai kesimpulan yang dianggap benar dengan sendirinya."
  },
  {
    id: "P3",
    title: "Decision Authority and Contestability",
    text:
      "Accountable reliance diperkuat ketika aktor yang bertanggung jawab atas keputusan cybersecurity memiliki evidence yang cukup, kompetensi yang sesuai, serta kewenangan eksplisit untuk menerima, menunda, mempertanyakan, override, atau mengeskalasi rekomendasi otomatis."
  },
  {
    id: "P4",
    title: "Learning from Overrides",
    text:
      "Override, disagreement, false alarm, missed threat, dan incident outcome yang terdokumentasi dapat meningkatkan organizational learning apabila secara periodik diagregasi dan digunakan untuk memperbaiki rule, threshold, workflow, explanation, atau model teknis."
  },
  {
    id: "P5",
    title: "Institutional Enactment",
    text:
      "Safeguard cybersecurity/AI governance formal hanya berkontribusi nyata terhadap accountability ketika benar-benar dijalankan dalam recurring routines, decision rights, documentation, review, dan consequences. Governance yang hanya tertulis di kebijakan dapat memiliki dampak operasional yang terbatas."
  },
  {
    id: "P6",
    title: "Accountable Reliance",
    text:
      "Accountable reliance terhadap AI-supported cybersecurity risk intelligence muncul dari kombinasi evidence traceability, human sensemaking yang memadai, decision-authority alignment, contestability, organizational learning, dan governance yang benar-benar enacted."
  }
];

function createGovernanceValidationRound1() {
  const form = FormApp.create(GOV_FORM_TITLE);

  form
    .setDescription(STUDY_CONTEXT)
    .setProgressBar(true)
    .setShuffleQuestions(false)
    .setAcceptingResponses(true)
    .setConfirmationMessage(
      "Terima kasih. Respons Bapak/Ibu telah direkam sebagai Round 1 Governance Expert Validation. " +
      "Apabila terdapat item yang masih sangat diperdebatkan, peneliti dapat mengirim Round 2 yang jauh lebih singkat dan hanya memuat contested items."
    );

  // -----------------------------
  // SECTION 0 — Consent
  // -----------------------------
  form.addSectionHeaderItem()
    .setTitle("Persetujuan Partisipasi")
    .setHelpText(CONSENT_TEXT);

  form.addCheckboxItem()
    .setTitle("Persetujuan")
    .setChoiceValues([
      "Saya telah membaca penjelasan di atas dan bersedia berpartisipasi secara sukarela."
    ])
    .setRequired(true);

  // -----------------------------
  // SECTION A — Expert Profile
  // -----------------------------
  form.addPageBreakItem()
    .setTitle("A. Profil Pakar")
    .setHelpText("Informasi ini digunakan untuk mendeskripsikan keragaman panel pakar, bukan untuk menilai individu.");

  form.addTextItem()
    .setTitle("A1. Nama / Inisial")
    .setRequired(true);

  form.addTextItem()
    .setTitle("A2. Institusi / Organisasi")
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("A3. Peran profesional utama")
    .setChoiceValues([
      "SOC Analyst",
      "SOC / CSIRT Lead",
      "Cybersecurity Manager",
      "Information Security Manager",
      "IT Risk Manager",
      "IT Governance / IT Audit",
      "Academic / Researcher",
      "IT / System Manager",
      "Consultant / Advisor"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("A4. Lama pengalaman profesional yang relevan")
    .setChoiceValues([
      "< 3 tahun",
      "3–5 tahun",
      "6–10 tahun",
      "11–15 tahun",
      "> 15 tahun"
    ])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle("A5. Bidang keahlian / pengalaman yang relevan")
    .setChoiceValues([
      "Cybersecurity",
      "SOC / CSIRT",
      "Incident Response",
      "Information Security Risk Management",
      "IT Governance",
      "IT Audit",
      "ISO/IEC 27001",
      "NIST Cybersecurity / Risk Framework",
      "Machine Learning / Artificial Intelligence",
      "Explainable AI (XAI)",
      "Responsible AI / AI Governance",
      "Institutional IT Management"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("A6. Sektor utama")
    .setChoiceValues([
      "Higher Education / Education",
      "Government / Public Sector",
      "Telecommunication",
      "Financial / Banking",
      "Technology / IT Services",
      "Consulting",
      "Industry / Enterprise"
    ])
    .showOtherOption(true)
    .setRequired(true);

  // -----------------------------
  // SECTION B — Constructs
  // -----------------------------
  form.addPageBreakItem()
    .setTitle("B. Validasi Konstruk Governance")
    .setHelpText(
      "Nilai tujuh konstruk berikut berdasarkan relevansi, kejelasan, dan realismenya dalam lingkungan cybersecurity/SOC/IT governance.\n\n" +
      CONSTRUCT_DEFINITIONS
    );

  form.addGridItem()
    .setTitle("B1. RELEVANSI — Seberapa relevan setiap konstruk untuk accountable cybersecurity decision-making?")
    .setRows(CONSTRUCTS)
    .setColumns(LIKERT_5)
    .setRequired(true);

  form.addGridItem()
    .setTitle("B2. KEJELASAN — Seberapa jelas dan mudah dipahami setiap konstruk?")
    .setRows(CONSTRUCTS)
    .setColumns(LIKERT_5)
    .setRequired(true);

  form.addGridItem()
    .setTitle("B3. OPERATIONAL REALISM — Seberapa realistis setiap konstruk diterapkan dalam lingkungan cybersecurity/SOC/IT governance?")
    .setRows(CONSTRUCTS)
    .setColumns(LIKERT_5)
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("B4. Apakah ada konstruk yang perlu dihapus, digabungkan, dipisahkan, atau didefinisikan ulang? Jelaskan.")
    .setRequired(false);

  // -----------------------------
  // SECTION C — Propositions
  // -----------------------------
  form.addPageBreakItem()
    .setTitle("C. Validasi Causal Propositions")
    .setHelpText(
      "Fokus bagian ini bukan sekadar 'setuju/tidak setuju', tetapi apakah hubungan sebab/mekanisme yang diajukan masuk akal dalam praktik."
    );

  PROPOSITIONS.forEach(function(p) {
    form.addSectionHeaderItem()
      .setTitle(p.id + " — " + p.title)
      .setHelpText(p.text);

    form.addScaleItem()
      .setTitle(p.id + ".1 — Causal plausibility: seberapa masuk akal hubungan/mekanisme di atas?")
      .setBounds(1, 5)
      .setLabels("1 — Sangat tidak plausible", "5 — Sangat plausible")
      .setRequired(true);

    form.addScaleItem()
      .setTitle(p.id + ".2 — Operational realism: seberapa realistis mekanisme ini terjadi dalam organisasi?")
      .setBounds(1, 5)
      .setLabels("1 — Sangat tidak realistis", "5 — Sangat realistis")
      .setRequired(true);

    form.addScaleItem()
      .setTitle(p.id + ".3 — Boundary-condition realism: seberapa realistis kondisi kegagalan/batasan yang disebutkan?")
      .setBounds(1, 5)
      .setLabels("1 — Sangat tidak realistis", "5 — Sangat realistis")
      .setRequired(true);

    form.addParagraphTextItem()
      .setTitle(p.id + ".4 — Dalam kondisi apa hubungan ini dapat gagal, menjadi lemah, atau perlu dimodifikasi?")
      .setRequired(false);
  });

  // -----------------------------
  // SECTION D — Role Architecture
  // -----------------------------
  form.addPageBreakItem()
    .setTitle("D. Validasi Role Architecture dan Decision Rights")
    .setHelpText(
      "Pilih tanggung jawab/kewenangan yang menurut Bapak/Ibu realistis untuk setiap peran. " +
      "Satu orang dapat memegang lebih dari satu peran pada organisasi kecil, tetapi fungsi accountability tetap perlu jelas."
    );

  form.addCheckboxItem()
    .setTitle("D1. Cybersecurity Analyst — decision rights / responsibilities yang seharusnya tersedia")
    .setChoiceValues([
      "Review technical evidence",
      "Request additional evidence",
      "Accept system recommendation",
      "Reject system recommendation",
      "Defer decision",
      "Override technical priority",
      "Escalate to SOC/CSIRT lead or risk owner",
      "Trigger incident investigation",
      "Document alternative hypothesis / rationale"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle("D2. Risk Owner / Security Manager — decision rights / responsibilities yang seharusnya tersedia")
    .setChoiceValues([
      "Assess organizational impact",
      "Determine response proportionality",
      "Approve risk response",
      "Request second review",
      "Override operational priority",
      "Escalate cross-unit consequences",
      "Accept / reject residual risk",
      "Require additional contextual evidence"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle("D3. System / Data / Model Owner — responsibilities yang seharusnya tersedia")
    .setChoiceValues([
      "Maintain data provenance",
      "Define intended use and limitations",
      "Maintain model/system documentation",
      "Monitor drift / instability",
      "Manage feature/rule definitions",
      "Manage change control",
      "Suspend system use when necessary",
      "Request or authorize redesign"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle("D4. Governance / Oversight Function — kondisi yang seharusnya menjadi objek review")
    .setChoiceValues([
      "Repeated analyst overrides",
      "Material governance failure",
      "Unexplained model/system instability",
      "Contested high-impact decision",
      "Policy violation",
      "Audit finding",
      "Use outside intended scope",
      "Repeated disagreement between analyst and system",
      "Repeated disagreement between operational and risk-management roles"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("D5. Apakah pembagian role atau decision rights di atas tidak realistis? Jelaskan bagian yang perlu diperbaiki.")
    .setRequired(false);

  // -----------------------------
  // SECTION E — Escalation Scenarios
  // -----------------------------
  form.addPageBreakItem()
    .setTitle("E. Validasi Escalation Rules")
    .setHelpText("Nilai bagaimana organisasi seharusnya menangani konflik atau uncertainty dalam AI-supported cybersecurity decisions.");

  addEscalationQuestion_(
    form,
    "E1. Sistem memberi risk level VERY HIGH, tetapi analyst menilai evidence belum cukup. Apakah wajib second review / escalation?"
  );

  addEscalationQuestion_(
    form,
    "E2. Model memiliki confidence rendah, tetapi potensi organizational impact sangat tinggi. Apakah wajib escalation?"
  );

  addEscalationQuestion_(
    form,
    "E3. System recommendation bertentangan dengan contextual evidence yang dimiliki analyst. Apakah wajib escalation?"
  );

  form.addMultipleChoiceItem()
    .setTitle("E4. Beberapa analyst berulang kali meng-override tipe alert yang sama. Apa tindakan yang paling tepat?")
    .setChoiceValues([
      "Tidak perlu tindakan tambahan",
      "Review hanya pada level analyst",
      "Trigger technical/model review",
      "Trigger governance/process review",
      "Trigger technical + governance review"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("E5. High-risk recommendation tidak dapat direkonstruksi karena provenance/evidence tidak lengkap. Apakah high-impact automated action boleh dilakukan?")
    .setChoiceValues([
      "Ya",
      "Tidak",
      "Hanya dengan second-level approval",
      "Tergantung consequence severity"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("E6. SOC analyst dan risk owner tidak sepakat mengenai response priority. Siapa yang seharusnya memiliki final decision authority?")
    .setChoiceValues([
      "SOC analyst",
      "SOC / CSIRT lead",
      "Risk owner",
      "CISO / Information Security Manager",
      "Joint decision",
      "Governance / oversight forum",
      "Tergantung consequence / asset criticality"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("E7. Sebutkan escalation trigger lain yang menurut Bapak/Ibu penting tetapi belum tercakup.")
    .setRequired(false);

  // -----------------------------
  // SECTION F — Learning & Institutional Enactment
  // -----------------------------
  form.addPageBreakItem()
    .setTitle("F. Organizational Learning dan Governance Enactment");

  form.addGridItem()
    .setTitle("F1. Seberapa setuju Bapak/Ibu dengan pernyataan berikut?")
    .setRows([
      "Alasan override terhadap rekomendasi otomatis harus didokumentasikan.",
      "Pola repeated overrides harus dianalisis secara periodik untuk technical/process redesign.",
      "Governance committee tidak efektif jika tidak memiliki authority untuk meminta remediation atau menghentikan penggunaan.",
      "Cybersecurity/AI governance dapat menjadi ceremonial jika tidak terintegrasi ke workflow operasional.",
      "Analyst harus dapat menantang rekomendasi otomatis tanpa penalti hanya karena berbeda pendapat."
    ])
    .setColumns([
      "1 — Sangat tidak setuju",
      "2 — Tidak setuju",
      "3 — Netral / tergantung",
      "4 — Setuju",
      "5 — Sangat setuju"
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("F2. Menurut pengalaman Bapak/Ibu, apa hambatan praktis terbesar untuk accountable use of AI-assisted cybersecurity risk intelligence?")
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("F3. Bagian apa dari governance model ini yang menurut Bapak/Ibu paling tidak realistis, belum lengkap, atau sulit diterapkan?")
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("F4. Saran perbaikan lain untuk governance mechanism, role, escalation, atau organizational learning.")
    .setRequired(false);

  // -----------------------------
  // Create response spreadsheet
  // -----------------------------
  const responseSS = SpreadsheetApp.create(
    "Responses — " + GOV_FORM_TITLE
  );

  form.setDestination(
    FormApp.DestinationType.SPREADSHEET,
    responseSS.getId()
  );

  // -----------------------------
  // Create index spreadsheet
  // -----------------------------
  const indexSS = SpreadsheetApp.create(
    "INDEX — " + GOV_FORM_TITLE
  );

  const sh = indexSS.getSheets()[0];
  sh.setName("INDEX");
  sh.getRange("A1:B7").setValues([
    ["Item", "Value"],
    ["Form title", GOV_FORM_TITLE],
    ["Respondent URL", form.getPublishedUrl()],
    ["Edit URL", form.getEditUrl()],
    ["Response Spreadsheet", responseSS.getUrl()],
    ["Index Spreadsheet", indexSS.getUrl()],
    ["Created at", new Date()]
  ]);
  sh.getRange("A1:B1").setFontWeight("bold");
  sh.autoResizeColumns(1, 2);

  Logger.log("FORM RESPONDENT URL: " + form.getPublishedUrl());
  Logger.log("FORM EDIT URL: " + form.getEditUrl());
  Logger.log("RESPONSE SHEET: " + responseSS.getUrl());
  Logger.log("INDEX: " + indexSS.getUrl());

  return {
    respondentUrl: form.getPublishedUrl(),
    editUrl: form.getEditUrl(),
    responseSpreadsheetUrl: responseSS.getUrl(),
    indexSpreadsheetUrl: indexSS.getUrl()
  };
}

function addEscalationQuestion_(form, title) {
  form.addMultipleChoiceItem()
    .setTitle(title)
    .setChoiceValues([
      "Ya — wajib escalation / second review",
      "Tidak — tidak wajib",
      "Conditional — tergantung context / impact / evidence"
    ])
    .setRequired(true);
}
