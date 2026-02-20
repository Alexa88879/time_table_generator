/********************************************
 * MINI PROJECT REPORT GENERATOR – PART 1
 * Front Matter: Cover, Certificate, Acknowledgement, Synopsis
 ********************************************/

const TEMPLATE_ID = "1vX6IgFdYjzlBRLBbDqQsIs6MskD7TsIBILbtq0im6J4"; // Your sample report/template Doc ID

function generateCompleteReport() {
  // 1. Copy template doc
  const templateFile = DriveApp.getFileById(TEMPLATE_ID);
  const newFile = templateFile.makeCopy("Mini Project Report - Automatic Timetable Generator");
  const newDocId = newFile.getId();

  const doc = DocumentApp.openById(newDocId);
  const body = doc.getBody();

  // 2. Clear existing content from copied template (keep page setup/margins)
  clearBody(body);

  // 3. Generate Content Sequence
  writeCoverPage(body);
  body.appendPageBreak();

  writeCertificatePage(body);
  body.appendPageBreak();

  writeAcknowledgement(body);
  body.appendPageBreak();

  writeSynopsis(body);
  body.appendPageBreak();

  writeTableOfContentsPage(body);
  body.appendPageBreak();

  writeListOfTablesPage(body);
  body.appendPageBreak();

  writeListOfFiguresPage(body);
  body.appendPageBreak();

  writeChapter1_Introduction(body);
  body.appendPageBreak();

  writeChapter2_Requirements(body);
  body.appendPageBreak();

  writeChapter3_SRS(body);
  body.appendPageBreak();

  writeChapter4_SystemDesign(body);
  body.appendPageBreak();

  writeChapter5_ModulesAndDB(body);
  body.appendPageBreak();

  writeChapter6_Snapshots(body);
  body.appendPageBreak();

  writeChapter7_Limitations(body);
  body.appendPageBreak();

  writeChapter8_FutureScope(body);
  body.appendPageBreak();

  writeConclusionAndReferences(body);

  doc.saveAndClose();
  Logger.log("Complete Report generated successfully with ID: " + newDocId);
  Logger.log("URL: " + newFile.getUrl());
}

/**
 * Removes all existing elements from the document body
 */
function clearBody(body) {
  // Remove everything except the last element
  while (body.getNumChildren() > 1) {
    body.removeChild(body.getChild(0));
  }

  // Now safely "reset" the last remaining element
  var last = body.getChild(0);

  if (last.getType() == DocumentApp.ElementType.PARAGRAPH) {
    // Use a single space instead of "" to avoid "empty text element" error
    var text = last.editAsText();
    text.setText(" "); 
  } else {
    // If the last element is not a paragraph (e.g. table), replace it with a blank paragraph
    last.removeFromParent();
    body.appendParagraph(" "); // again, single space, not empty string
  }
}



/**
 * Helper: add a blank line
 */
function addEmptyLine(body, count) {
  count = count || 1;
  for (var i = 0; i < count; i++) {
    body.appendParagraph("").setLineSpacing(1.0).setFontSize(12);
  }
}

/**
 * COVER PAGE
 * Format as per RKGIT mini-project template
 */
function writeCoverPage(body) {
  // Institute header
  var p;

  p = body.appendParagraph("RAJ KUMAR GOEL INSTITUTE OF TECHNOLOGY, GHAZIABAD");
  p.setFontFamily("Times New Roman").setFontSize(16).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  
  p = body.appendParagraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING");
  p.setFontFamily("Times New Roman").setFontSize(14).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 2);

  // Mini project line
  p = body.appendParagraph("MINI PROJECT REPORT (BCC-351)");
  p.setFontFamily("Times New Roman").setFontSize(16).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 1);

  // Project title
  p = body.appendParagraph("on");
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 1);

  p = body.appendParagraph("AUTOMATIC TIMETABLE GENERATOR USING HYBRID AI (CSP + GENETIC ALGORITHM)");
  p.setFontFamily("Times New Roman").setFontSize(16).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 2);

  // Degree line
  p = body.appendParagraph("Submitted in partial fulfillment for award of");
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 1);

  p = body.appendParagraph("BACHELOR OF TECHNOLOGY");
  p.setFontFamily("Times New Roman").setFontSize(14).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  p = body.appendParagraph("Degree");
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 1);

  p = body.appendParagraph("In");
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  p = body.appendParagraph("COMPUTER SCIENCE & ENGINEERING");
  p.setFontFamily("Times New Roman").setFontSize(14).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 2);

  // Session
  p = body.appendParagraph("SESSION 2024-25");
  p.setFontFamily("Times New Roman").setFontSize(12).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 3);

  // Under guidance & submitted by (left & right)
  var table = body.appendTable([
    [
      "Under the Guidance of:", 
      "Submitted By:"
    ],
    [
      "Dr. [GUIDE NAME]\nAssistant Professor\nDepartment of Computer Science & Engineering",
      "[STUDENT NAME]\nUniversity Roll No.: [ROLL NUMBER]\nB.Tech CSE, 6th Semester"
    ]
  ]);

  table.setBorderWidth(0);

  // Style the cells
  for (var r = 0; r < table.getNumRows(); r++) {
    var row = table.getRow(r);
    for (var c = 0; c < row.getNumCells(); c++) {
      var cell = row.getCell(c);
      cell.getChild(0)
        .asParagraph()
        .setFontFamily("Times New Roman")
        .setFontSize(12)
        .setAlignment(c === 0 ? DocumentApp.HorizontalAlignment.LEFT : DocumentApp.HorizontalAlignment.RIGHT);
    }
  }

  addEmptyLine(body, 4);

  // Institute footer
  p = body.appendParagraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING");
  p.setFontFamily("Times New Roman").setFontSize(12).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  p = body.appendParagraph("RAJ KUMAR GOEL INSTITUTE OF TECHNOLOGY");
  p.setFontFamily("Times New Roman").setFontSize(12).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  p = body.appendParagraph("DELHI-MEERUT ROAD, GHAZIABAD");
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  p = body.appendParagraph("Affiliated to Dr. A.P.J. Abdul Kalam Technical University, Lucknow");
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);
}

/**
 * CERTIFICATE PAGE
 */
function writeCertificatePage(body) {
  var p;

  p = body.appendParagraph("CERTIFICATE");
  p.setFontFamily("Times New Roman").setFontSize(16).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 2);

  var certText =
    "This is to certify that the mini project report entitled\n\n" +
    "\"AUTOMATIC TIMETABLE GENERATOR USING HYBRID AI (CSP + GENETIC ALGORITHM)\"\n\n" +
    "submitted by [STUDENT NAME] (University Roll No.: [ROLL NUMBER]) in partial fulfillment of the " +
    "requirements for the award of the degree of BACHELOR OF TECHNOLOGY in COMPUTER SCIENCE & ENGINEERING " +
    "during the Session 2024–25 is a bonafide record of work carried out by him/her under my supervision and guidance.\n\n" +
    "The work embodied in this report has not been submitted to any other University or Institute for the award of any degree or diploma.";

  p = body.appendParagraph(certText);
  p.setFontFamily("Times New Roman").setFontSize(12).setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 3);

  // Signature layout: Guide, HOD, Director/Principal
  var table = body.appendTable([
    [
      "_________________________", 
      "_________________________"
    ],
    [
      "Project Guide\nDr. [GUIDE NAME]\nAssistant Professor\nDept. of CSE",
      "Head of Department\nDr. [HOD NAME]\nProfessor & Head\nDept. of CSE"
    ],
    [
      "", 
      "_________________________"
    ],
    [
      "",
      "Director/Principal\n[DIRECTOR / PRINCIPAL NAME]\nRaj Kumar Goel Institute of Technology"
    ]
  ]);
  table.setBorderWidth(0);

  // style each cell
  for (var r = 0; r < table.getNumRows(); r++) {
    var row = table.getRow(r);
    for (var c = 0; c < row.getNumCells(); c++) {
      var cell = row.getCell(c);
      cell.getChild(0)
        .asParagraph()
        .setFontFamily("Times New Roman")
        .setFontSize(12)
        .setAlignment(c === 0 ? DocumentApp.HorizontalAlignment.LEFT : DocumentApp.HorizontalAlignment.RIGHT);
    }
  }

  addEmptyLine(body, 2);

  // Place/date
  p = body.appendParagraph("Place: Ghaziabad");
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setAlignment(DocumentApp.HorizontalAlignment.LEFT);

  p = body.appendParagraph("Date: ____________");
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setAlignment(DocumentApp.HorizontalAlignment.LEFT);
}

/**
 * ACKNOWLEDGEMENT
 */
function writeAcknowledgement(body) {
  var p;

  p = body.appendParagraph("ACKNOWLEDGEMENT");
  p.setFontFamily("Times New Roman").setFontSize(16).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 2);

  var ackText =
    "I would like to express my sincere gratitude to Dr. [GUIDE NAME], Assistant Professor, " +
    "Department of Computer Science & Engineering, Raj Kumar Goel Institute of Technology, " +
    "for his/her invaluable guidance, continuous encouragement, and constructive feedback throughout " +
    "the development of this mini project titled \"Automatic Timetable Generator using Hybrid AI (CSP + Genetic Algorithm)\".\n\n" +
    "I am also thankful to Dr. [HOD NAME], Head of Department, CSE, for providing the necessary facilities, " +
    "academic environment, and support to carry out this work.\n\n" +
    "I extend my heartfelt thanks to all faculty members and staff of the Department of Computer Science & Engineering " +
    "for their support and motivation.\n\n" +
    "Finally, I am deeply grateful to my parents, friends, and well-wishers for their constant encouragement and moral support.";

  p = body.appendParagraph(ackText);
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 3);

  p = body.appendParagraph("[STUDENT NAME]");
  p.setFontFamily("Times New Roman").setFontSize(12).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.RIGHT);

  p = body.appendParagraph("University Roll No.: [ROLL NUMBER]");
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setAlignment(DocumentApp.HorizontalAlignment.RIGHT);
}

/**
 * SYNOPSIS (2–3 pages)
 * Based on your project documentation (Hybrid GA+CSP Timetable Generator)
 */
function writeSynopsis(body) {
  var p;

  p = body.appendParagraph("SYNOPSIS");
  p.setFontFamily("Times New Roman").setFontSize(16).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 2);

  // 1. Background
  p = body.appendParagraph("1. Background");
  p.setFontFamily("Times New Roman").setFontSize(14).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.LEFT);

  var bgText =
    "Timetable preparation in engineering colleges is a complex administrative task that involves allocating " +
    "courses, faculty members, classrooms, and time slots while satisfying multiple academic and logistical " +
    "constraints. Under the AKTU CSE NEP 2020 curriculum, the number of theory courses, labs, elective options, " +
    "and batch-wise practical sessions has increased, which further complicates manual timetable generation. " +
    "Traditional approaches using spreadsheets or static tools are time-consuming, prone to human error, and often " +
    "lead to suboptimal schedules with clashes, uneven workload distribution, and poor utilization of rooms and labs.";

  p = body.appendParagraph(bgText);
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  // 2. Problem Statement
  p = body.appendParagraph("2. Problem Statement");
  p.setFontFamily("Times New Roman").setFontSize(14).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.LEFT);

  var psText =
    "The project focuses on the University Course Timetabling Problem (UCTP), which is a well-known NP-hard " +
    "combinatorial optimization problem. The task is to assign a set of courses to available time slots and rooms " +
    "for different sections such that no faculty member, room, or section is double-booked at any time and all " +
    "institutional constraints are respected. In addition to producing a conflict-free timetable, the system must " +
    "also consider soft constraints such as faculty time preferences, balanced day-wise workload, proper placement " +
    "of lab sessions, and minimization of gaps in student schedules.";

  p = body.appendParagraph(psText);
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  // 3. Objectives
  p = body.appendParagraph("3. Objectives");
  p.setFontFamily("Times New Roman").setFontSize(14).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.LEFT);

  var objText =
    "The major objectives of the mini project are as follows:\n" +
    "• To develop an intelligent timetable generator that produces conflict-free schedules for theory and lab courses.\n" +
    "• To integrate Constraint Satisfaction Problem (CSP) techniques with a Genetic Algorithm (GA) so that hard\n" +
    "  constraints are strictly satisfied while soft constraints are optimized.\n" +
    "• To design a user-friendly web-based interface through which department coordinators can manage faculty,\n" +
    "  rooms, courses, sections, and batch-wise lab allocations.\n" +
    "• To support export of generated timetables in printable formats such as PDF and Excel for official use.";

  p = body.appendParagraph(objText);
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  // 4. Scope of the Work
  p = body.appendParagraph("4. Scope of the Work");
  p.setFontFamily("Times New Roman").setFontSize(14).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.LEFT);

  var scopeText =
    "The scope of the project is limited to academic timetable generation for regular theory and laboratory " +
    "classes at the department level. The system supports faculty-wise and section-wise timetables, lab batch " +
    "allocations (G1/G2), room capacity checks, and adherence to predefined working hours and lunch breaks. " +
    "Exam scheduling, student-specific elective registration, and institute-wide global timetabling are considered " +
    "outside the present scope and can be taken up as part of future enhancements.";

  p = body.appendParagraph(scopeText);
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  // 5. Methodology / Technology Used
  p = body.appendParagraph("5. Methodology and Technology Used");
  p.setFontFamily("Times New Roman").setFontSize(14).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.LEFT);

  var methodText =
    "The system follows a two-phase Hybrid AI approach. In the first phase, a Constraint Satisfaction Problem (CSP) " +
    "solver based on backtracking and heuristic ordering (such as Minimum Remaining Values) is used to construct an " +
    "initial timetable that satisfies all hard constraints like faculty clash, room clash, section clash, lab " +
    "continuity, and room capacity. This valid solution acts as a seed for the second phase, where a Genetic " +
    "Algorithm is applied to iteratively improve the timetable with respect to soft constraints. The GA encodes each " +
    "timetable as a chromosome and applies selection, crossover, mutation, and elitism to evolve higher-quality schedules.\n\n" +
    "The complete solution is implemented as a full-stack web application using Python and Flask on the backend, " +
    "with SQLite as the database and HTML5, CSS, Bootstrap, and JavaScript on the frontend. Additional libraries such " +
    "as SQLAlchemy, Pandas, and ReportLab are used for database interaction, Excel handling, and PDF generation respectively.";

  p = body.appendParagraph(methodText);
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  // 6. Expected Outcomes
  p = body.appendParagraph("6. Expected Outcomes");
  p.setFontFamily("Times New Roman").setFontSize(14).setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.LEFT);

  var outText =
    "The expected outcome of the mini project is a working prototype of an Automatic Timetable Generator that can " +
    "generate feasible, high-quality timetables for a Computer Science & Engineering department following the AKTU " +
    "NEP 2020 structure. The system will significantly reduce the manual effort required for scheduling, minimize " +
    "clashes and inconsistencies, improve resource utilization, and provide a practical demonstration of applying " +
    "Hybrid Artificial Intelligence techniques to a real-world academic problem.";

  p = body.appendParagraph(outText);
  p.setFontFamily("Times New Roman").setFontSize(12)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);
}







/********************************************
 * PART 2: TOC + LISTS + CHAPTER 1
 ********************************************/

// Part 2 function removed - integrated into generateCompleteReport


/**
 * TABLE OF CONTENTS PAGE
 * Uses Google Docs auto TOC for headings.
 */
function writeTableOfContentsPage(body) {
  var p = body.appendParagraph("TABLE OF CONTENTS");
  p.setFontFamily("Times New Roman")
    .setFontSize(16)
    .setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 2);

  // Header row
  var table = body.appendTable([
    ["Chapter No.", "Title", "Page No."]
  ]);
  table.setBorderWidth(1);

  var rows = [
    ["1", "INTRODUCTION", ""],
    ["2", "HARDWARE AND SOFTWARE REQUIREMENTS", ""],
    ["3", "SOFTWARE REQUIREMENTS SPECIFICATION (SRS)", ""],
    ["4", "SYSTEM DESIGN (DFD, ER DIAGRAM, ARCHITECTURE)", ""],
    ["5", "MODULE DESIGN AND DATABASE TABLES", ""],
    ["6", "PROJECT SNAPSHOTS", ""],
    ["7", "LIMITATIONS", ""],
    ["8", "FUTURE SCOPE", ""],
    ["-", "CONCLUSION", ""],
    ["-", "REFERENCES", ""]
  ];

  // Append rows properly
  for (var i = 0; i < rows.length; i++) {
    var rowData = rows[i];
    var row = table.appendTableRow();
    for (var j = 0; j < rowData.length; j++) {
      row.appendTableCell(String(rowData[j]));
    }
  }

  // Style cells
  for (var r = 0; r < table.getNumRows(); r++) {
    var row = table.getRow(r);
    for (var c = 0; c < row.getNumCells(); c++) {
      var cell = row.getCell(c);
      cell.getChild(0)
        .asParagraph()
        .setFontFamily("Times New Roman")
        .setFontSize(12)
        .setAlignment(c === 2 ? DocumentApp.HorizontalAlignment.RIGHT
                              : DocumentApp.HorizontalAlignment.LEFT);
    }
  }
}



/**
 * LIST OF TABLES PAGE (formatted like college template)
 * You can update titles/page nos later after everything is final.
 */
function writeListOfTablesPage(body) {
  var p = body.appendParagraph("LIST OF TABLES");
  p.setFontFamily("Times New Roman")
    .setFontSize(16)
    .setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 2);

  var table = body.appendTable([
    ["Chapter No.", "Table No.", "Title", "Page No."]
  ]);
  table.setBorderWidth(1);

  var rows = [
    ["3", "Table 3.1", "Functional Requirements of the System", ""],
    ["3", "Table 3.2", "Non-Functional Requirements", ""],
    ["5", "Table 5.1", "Database Tables Description", ""],
    ["7", "Table 7.1", "Test Cases and Results", ""]
  ];

  for (var i = 0; i < rows.length; i++) {
    var rowData = rows[i];
    var row = table.appendTableRow();
    for (var j = 0; j < rowData.length; j++) {
      row.appendTableCell(String(rowData[j]));
    }
  }

  // Style cells
  for (var r = 0; r < table.getNumRows(); r++) {
    var row = table.getRow(r);
    for (var c = 0; c < row.getNumCells(); c++) {
      var cell = row.getCell(c);
      cell.getChild(0)
        .asParagraph()
        .setFontFamily("Times New Roman")
        .setFontSize(12)
        .setAlignment(DocumentApp.HorizontalAlignment.LEFT);
    }
  }
}


/**
 * LIST OF FIGURES PAGE
 */
function writeListOfFiguresPage(body) {
  var p = body.appendParagraph("LIST OF FIGURES");
  p.setFontFamily("Times New Roman")
    .setFontSize(16)
    .setBold(true)
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 2);

  var table = body.appendTable([
    ["Chapter No.", "Figure No.", "Title", "Page No."]
  ]);
  table.setBorderWidth(1);

  var rows = [
    ["4", "Figure 4.1", "System Architecture of Timetable Generator", ""],
    ["4", "Figure 4.2", "Level 0 Data Flow Diagram", ""],
    ["4", "Figure 4.3", "Level 1 Data Flow Diagram", ""],
    ["4", "Figure 4.4", "ER Diagram of Database Design", ""],
    ["6", "Figure 6.1", "Dashboard Screen", ""],
    ["6", "Figure 6.2", "Faculty Management Screen", ""],
    ["6", "Figure 6.3", "Timetable Generation Screen", ""],
    ["6", "Figure 6.4", "Section-wise Timetable View", ""]
  ];

  for (var i = 0; i < rows.length; i++) {
    var rowData = rows[i];
    var row = table.appendTableRow();
    for (var j = 0; j < rowData.length; j++) {
      row.appendTableCell(String(rowData[j]));
    }
  }

  // Style cells
  for (var r = 0; r < table.getNumRows(); r++) {
    var row = table.getRow(r);
    for (var c = 0; c < row.getNumCells(); c++) {
      var cell = row.getCell(c);
      cell.getChild(0)
        .asParagraph()
        .setFontFamily("Times New Roman")
        .setFontSize(12)
        .setAlignment(DocumentApp.HorizontalAlignment.LEFT);
    }
  }
}


/**
 * CHAPTER 1 – INTRODUCTION
 * 1.1 Background
 * 1.2 Problem Definition
 * 1.3 Objectives
 * 1.4 Scope of Project
 * 1.5 Motivation
 * 1.6 Organization of Report
 */
function writeChapter1_Introduction(body) {
  // Chapter heading
  var p = body.appendParagraph("CHAPTER 1");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING1);
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(16);
  p.setBold(true);

  p = body.appendParagraph("INTRODUCTION");
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(14);
  p.setBold(true);

  addEmptyLine(body, 1);

  // 1.1 Background
  p = body.appendParagraph("1.1 Background");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  var text = 
    "Timetabling is a fundamental academic and administrative activity in every educational institution. " +
    "It involves assigning a set of courses to available time slots, rooms, and faculty members in such a way " +
    "that all academic, physical, and institutional constraints are satisfied. In the context of engineering " +
    "colleges following the AKTU CSE NEP 2020 curriculum, the complexity of timetable preparation has increased " +
    "due to the presence of multiple theory subjects, laboratory courses, elective options, and batch-wise lab " +
    "rotations. Manual timetable creation using spreadsheets or paper-based methods is time-consuming, error-prone, " +
    "and often results in conflicts such as faculty clashes, room clashes, and unbalanced workload distributions.\n\n" +
    "The University Course Timetabling Problem (UCTP) is widely recognized as a combinatorial optimization problem " +
    "that is NP-hard in nature. As the number of courses, rooms, and constraints increases, the search space grows " +
    "exponentially, making naive or brute-force approaches impractical. This has led to the adoption of intelligent " +
    "algorithms and heuristic techniques for timetable generation in modern academic systems.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  // 1.2 Problem Definition
  p = body.appendParagraph("1.2 Problem Definition");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "The core problem addressed in this mini project is the automatic generation of feasible and optimized " +
    "timetables for a Computer Science & Engineering department. Formally, the problem can be stated as:\n\n" +
    "Given:\n" +
    "• A set of courses with their respective lecture and lab hours.\n" +
    "• A set of faculty members along with their availability and workload limits.\n" +
    "• A set of rooms and laboratories with their capacities and types.\n" +
    "• A set of sections and batches to which these courses must be allocated.\n\n" +
    "Find an allocation of courses to time slots, rooms, and faculty members such that:\n" +
    "• No faculty member, room, or section is allocated to more than one class at the same time.\n" +
    "• Lab sessions are scheduled in appropriate lab rooms and occupy consecutive time slots.\n" +
    "• Room capacities are not violated.\n" +
    "• Institutional constraints like working hours and lunch breaks are respected.\n\n" +
    "In addition to satisfying all such hard constraints, the system should aim to optimize soft constraints " +
    "such as faculty preferences for specific time periods, minimization of gaps in student schedules, and " +
    "balanced distribution of lectures across the week.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);
  // 1.3 Objectives
  p = body.appendParagraph("1.3 Objectives");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  body.appendParagraph(
      "The main objectives of the mini project are as follows:")
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  var objList = [
    "To design and develop an Automatic Timetable Generator for the CSE department that produces conflict-free timetables.",
    "To apply a Hybrid Artificial Intelligence approach that combines Constraint Satisfaction Problem (CSP) techniques with a Genetic Algorithm (GA) in order to balance feasibility and optimization.",
    "To model and enforce hard constraints such as faculty clash, room clash, section clash, lab continuity, and room capacity.",
    "To incorporate soft constraints including faculty time preferences, evenly spread lectures, and reduction of idle gaps for students.",
    "To provide a user-friendly web interface for managing faculty, rooms, courses, sections, and for generating and viewing timetables.",
    "To support export of generated timetables in PDF and Excel formats for official use and record-keeping."
  ];

  for (var i = 0; i < objList.length; i++) {
    body.appendListItem(objList[i])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }

  // 1.4 Scope of the Project
  p = body.appendParagraph("1.4 Scope of the Project");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "The scope of the mini project is limited to the generation of weekly academic timetables for regular theory " +
    "and laboratory classes at the department level. The system supports:\n" +
    "• Section-wise and faculty-wise timetable views.\n" +
    "• Batch-wise lab allocation (e.g., G1/G2 batches for practical sessions).\n" +
    "• Enforcement of predefined working hours and lunch breaks.\n" +
    "• Handling of room capacities and lab-specific room constraints.\n\n" +
    "Exam scheduling, student-specific elective registration, ad-hoc event scheduling, and institute-wide " +
    "centralized timetabling are outside the current scope and can be considered for future extension of the system.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);
  // 1.5 Motivation
  p = body.appendParagraph("1.5 Motivation");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "The motivation behind this project arises from the practical difficulties faced by academic coordinators and " +
    "departmental timetable in-charges while preparing timetables manually. Even a small mistake in assigning a " +
    "course to an incorrect time slot or room can lead to significant disruptions in the teaching-learning process. " +
    "As the number of sections, elective courses, and laboratory batches increases, it becomes extremely challenging " +
    "to manually ensure that no conflicts occur and that faculty members have a balanced and convenient schedule.\n\n" +
    "At the same time, the field of Artificial Intelligence offers powerful tools for solving constraint-based and " +
    "optimization problems. Combining CSP with Genetic Algorithms provides a robust framework that can guarantee " +
    "feasible solutions while also improving overall timetable quality. This project thus provides an opportunity " +
    "to apply AI techniques to a real-world, high-impact academic problem.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  // 1.6 Organization of the Report
  p = body.appendParagraph("1.6 Organization of the Report");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "The remainder of this report is organized as follows:\n" +
    "• Chapter 2 describes the hardware and software requirements of the proposed system.\n" +
    "• Chapter 3 presents the Software Requirements Specification (SRS), including functional and non-functional requirements.\n" +
    "• Chapter 4 explains the system design using Data Flow Diagrams (DFD), ER diagram, and overall architecture.\n" +
    "• Chapter 5 discusses the detailed module design, database tables, and key software features.\n" +
    "• Chapter 6 provides screenshots of the implemented system and explains the major user interfaces.\n" +
    "• Chapter 7 highlights the limitations of the current implementation.\n" +
    "• Chapter 8 outlines the future scope and possible enhancements to the system.\n\n" +
    "Finally, the report concludes with a summary of the work and references to the literature and tools used.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);
}




/********************************************
 * PART 3: CHAPTER 2 + CHAPTER 3
 ********************************************/

// Part 3 function removed - integrated into generateCompleteReport



/**
 * CHAPTER 2 – HARDWARE AND SOFTWARE REQUIREMENTS
 */
function writeChapter2_Requirements(body) {
  // Chapter heading
  var p = body.appendParagraph("CHAPTER 2");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING1);
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(16);
  p.setBold(true);

  p = body.appendParagraph("HARDWARE AND SOFTWARE REQUIREMENTS");
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(14);
  p.setBold(true);

  addEmptyLine(body, 1);

  // 2.1 Hardware Requirements
  p = body.appendParagraph("2.1 Hardware Requirements");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  var text =
    "The Automatic Timetable Generator is a lightweight web-based application and does not require high-end " +
    "hardware. The following hardware configuration is sufficient for development and deployment at the " +
    "department level.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  // 2.1.1 Server / Developer Machine
  p = body.appendParagraph("2.1.1 Server / Developer Machine");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  var hwServer = [
    "Processor: Intel Core i5 or equivalent (2.4 GHz or higher).",
    "RAM: Minimum 8 GB (recommended 16 GB for smooth multitasking).",
    "Storage: Minimum 20 GB free disk space.",
    "Display: 1366 × 768 resolution or higher.",
    "Network: Basic LAN/Internet connectivity for browser access."
  ];
  for (var i = 0; i < hwServer.length; i++) {
    body.appendListItem(hwServer[i])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }

  addEmptyLine(body, 1);

  // 2.1.2 Client Machine (End-User)
  p = body.appendParagraph("2.1.2 Client Machine (End-User)");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  var hwClient = [
    "Processor: Any modern CPU capable of running a web browser.",
    "RAM: Minimum 4 GB.",
    "Storage: Sufficient for OS and browser.",
    "Browser: Latest version of Chrome / Firefox / Edge.",
    "Network: Access to local network or server hosting the application."
  ];
  for (var j = 0; j < hwClient.length; j++) {
    body.appendListItem(hwClient[j])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }

  addEmptyLine(body, 1);
  // 2.2 Software Requirements
  p = body.appendParagraph("2.2 Software Requirements");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "The software stack used in the development and deployment of the Automatic Timetable Generator is based " +
    "on open-source technologies. This reduces cost and improves flexibility in customization and maintenance.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);
  // 2.2.1 Operating System
  p = body.appendParagraph("2.2.1 Operating System");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  var osList = [
    "Windows 10 / 11 (64-bit), or",
    "Linux distributions (Ubuntu, Debian, etc.), or",
    "Any OS capable of running Python 3.11 and a modern web browser."
  ];
  for (var k = 0; k < osList.length; k++) {
    body.appendListItem(osList[k])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }

  addEmptyLine(body, 1);
  // 2.2.2 Backend Technologies
  p = body.appendParagraph("2.2.2 Backend Technologies");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  var backendList = [
    "Programming Language: Python 3.11 or higher.",
    "Web Framework: Flask (lightweight Python web framework).",
    "ORM: SQLAlchemy for database interaction.",
    "Database: SQLite (development); can be migrated to MySQL/PostgreSQL in production.",
    "Additional Libraries: NumPy, Pandas, OpenPyXL, ReportLab, etc."
  ];
  for (var b = 0; b < backendList.length; b++) {
    body.appendListItem(backendList[b])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }

  addEmptyLine(body, 1);
  // 2.2.3 Frontend Technologies
  p = body.appendParagraph("2.2.3 Frontend Technologies");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  var frontendList = [
    "Markup: HTML5 for structuring the web pages.",
    "Styling: CSS3 and Bootstrap 5 for responsive design.",
    "Scripting: JavaScript for client-side interactivity.",
    "UI Enhancements: Chart.js, DataTables, and icon libraries."
  ];
  for (var f = 0; f < frontendList.length; f++) {
    body.appendListItem(frontendList[f])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }

  // 2.2.4 Development Tools
  p = body.appendParagraph("2.2.4 Development Tools");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  var devTools = [
    "Integrated Development Environment (IDE): Visual Studio Code / PyCharm.",
    "Version Control: Git and GitHub for source code management.",
    "Package Manager: pip for Python libraries.",
    "Browser Developer Tools for debugging frontend issues."
  ];
  for (var d = 0; d < devTools.length; d++) {
    body.appendListItem(devTools[d])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }
}


/**
 * CHAPTER 3 – SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
 */
function writeChapter3_SRS(body) {
  // Chapter heading
  var p = body.appendParagraph("CHAPTER 3");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING1);
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(16);
  p.setBold(true);

  p = body.appendParagraph("SOFTWARE REQUIREMENTS SPECIFICATION");
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(14);
  p.setBold(true);

  addEmptyLine(body, 1);

  // 3.1 Introduction
  p = body.appendParagraph("3.1 Introduction");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  var text =
    "The Software Requirements Specification (SRS) defines the complete set of functional and non-functional " +
    "requirements of the Automatic Timetable Generator. It serves as a formal document that describes what the " +
    "system is expected to do, the constraints under which it must operate, and the quality attributes it should " +
    "exhibit. The SRS acts as a reference for developers, testers, and stakeholders to ensure a common understanding " +
    "of the system before and during implementation.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  // 3.2 Overall Description
  p = body.appendParagraph("3.2 Overall Description");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "The Automatic Timetable Generator is a web-based application designed for use by department coordinators and " +
    "timetable in-charges. The system replaces manual spreadsheet-based scheduling with an intelligent, automated " +
    "approach. Users can define master data such as faculty, rooms, courses, sections, and lab batches, and then " +
    "invoke the Hybrid AI scheduler to generate timetables. The generated timetables can be viewed, validated, and " +
    "exported in different formats for circulation.\n\n" +
    "The system is deployed on a local or departmental server and accessed through a standard web browser on client " +
    "machines. Only authorized users can log in and perform operations such as data entry, timetable generation, " +
    "and export.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  // 3.3 Functional Requirements
  p = body.appendParagraph("3.3 Functional Requirements");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text = "The major functional requirements of the system are listed below:";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  var frList = [
    "FR-1: User Authentication – The system shall provide a secure login mechanism for authorized users (e.g., timetable in-charge, coordinator).",
    "FR-2: Faculty Management – The system shall allow users to add, update, and delete faculty details, including name, code, department, availability, and maximum workload.",
    "FR-3: Room and Lab Management – The system shall manage rooms and laboratories with attributes such as room code, capacity, and type (theory room or lab room).",
    "FR-4: Course Management – The system shall allow entry of course details including course code, course name, L-T-P structure, semester, and whether it is a lab or theory course.",
    "FR-5: Section and Batch Management – The system shall support creation of sections and lab batches (e.g., G1, G2) with student strength information.",
    "FR-6: Faculty–Course–Section Mapping – The system shall allow mapping of faculty to courses and sections, including specification of lecture and lab hours per week.",
    "FR-7: Constraint Configuration – The system shall allow enabling/disabling of certain soft constraints where applicable.",
    "FR-8: Timetable Generation – The system shall generate conflict-free timetables for selected sections using the Hybrid AI scheduler.",
    "FR-9: Timetable Viewing – The system shall provide views for section-wise and faculty-wise timetables in tabular form.",
    "FR-10: Timetable Export – The system shall support export of generated timetables as PDF and Excel files.",
    "FR-11: Logging and Status Reporting – The system shall display progress and status messages during timetable generation."
  ];

  for (var fr = 0; fr < frList.length; fr++) {
    body.appendListItem(frList[fr])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }

  // 3.4 Non-Functional Requirements
  p = body.appendParagraph("3.4 Non-Functional Requirements");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "Non-functional requirements specify the quality attributes and constraints that the system must satisfy " +
    "in addition to performing its fundamental functions.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  var nfrList = [
    "NFR-1: Performance – The system should be able to generate timetables for a typical department (multiple sections and courses) within a reasonable time, preferably under 60 seconds.",
    "NFR-2: Reliability – The system shall ensure that no hard constraints (faculty clash, room clash, section clash, lab continuity, and room capacity) are violated in the final timetable.",
    "NFR-3: Usability – The user interface shall be simple, intuitive, and easy to use for non-technical academic staff.",
    "NFR-4: Scalability – The system shall support addition of more sections, courses, and faculty members without major redesign.",
    "NFR-5: Security – Only authenticated users shall be allowed to modify master data or generate timetables.",
    "NFR-6: Maintainability – The codebase shall be modular, with clear separation between UI, business logic, and scheduling algorithms.",
    "NFR-7: Portability – The application shall be deployable on different operating systems with minimal configuration changes."
  ];

  for (var nfr = 0; nfr < nfrList.length; nfr++) {
    body.appendListItem(nfrList[nfr])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }

  // 3.5 System Constraints
  p = body.appendParagraph("3.5 System Constraints");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "The following constraints apply to the design and operation of the Automatic Timetable Generator:";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  var consList = [
    "SC-1: The timetable must strictly avoid faculty, room, and section clashes at any time slot.",
    "SC-2: Lab sessions must be scheduled in appropriate lab rooms and should occupy consecutive periods.",
    "SC-3: Room capacities must not be exceeded by the assigned section strength.",
    "SC-4: Classes must be scheduled only within defined working hours, with a mandatory lunch break.",
    "SC-5: Input data (faculty details, room capacities, course hours, etc.) must be accurate; invalid or inconsistent data may lead to unschedulable scenarios.",
    "SC-6: The system currently assumes a weekly timetable structure and does not handle exam timetabling or ad-hoc event scheduling."
  ];

  for (var c = 0; c < consList.length; c++) {
    body.appendListItem(consList[c])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }
}





/********************************************
 * PART 4: CHAPTER 4 – SYSTEM DESIGN
 ********************************************/

// Part 4 function removed - integrated into generateCompleteReport



/**
 * CHAPTER 4 – SYSTEM DESIGN
 */
function writeChapter4_SystemDesign(body) {

  // CHAPTER HEADING (Centered, bold, TNR)
  var p = body.appendParagraph("CHAPTER 4");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING1);
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(16);
  p.setBold(true);

  p = body.appendParagraph("SYSTEM DESIGN");
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(14);
  p.setBold(true);

  /*************** 4.1 SYSTEM ARCHITECTURE ***************/
  p = body.appendParagraph("4.1 System Architecture");
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true)
    .setHeading(DocumentApp.ParagraphHeading.HEADING2);

  var text =
    "The system architecture of the Automatic Timetable Generator follows a modular, layered design. It is " +
    "structured into three primary layers: the Presentation Layer, the Application Layer, and the Data Layer. " +
    "This separation of concerns improves scalability, maintainability, and flexibility in the overall system.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  /*************** 4.1.1 Presentation Layer ***************/
  p = body.appendParagraph("4.1.1 Presentation Layer");
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true)
    .setHeading(DocumentApp.ParagraphHeading.HEADING3);

  var text1 =
    "This layer represents the client-side interface used by the timetable coordinator. It includes web pages " +
    "developed using HTML5, CSS, Bootstrap, and JavaScript. Users interact with this layer to perform operations " +
    "such as adding faculty, rooms, sections, and generating timetables.";
  body.appendParagraph(text1)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  /*************** 4.1.2 Application Layer ***************/
  p = body.appendParagraph("4.1.2 Application Layer");
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true)
    .setHeading(DocumentApp.ParagraphHeading.HEADING3);

  var text2 =
    "The Application Layer contains the core business logic and scheduling algorithms. It is implemented using " +
    "Python (Flask) and handles requests from the frontend. Key components include:\n" +
    "• CSP-based hard constraint solver\n" +
    "• GA-based optimization engine\n" +
    "• Timetable generation workflow\n" +
    "• Validation and conflict detection";
  body.appendParagraph(text2)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  /*************** 4.1.3 Data Layer ***************/
  p = body.appendParagraph("4.1.3 Data Layer");
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true)
    .setHeading(DocumentApp.ParagraphHeading.HEADING3);

  var text3 =
    "This layer manages all persistent data required for timetable generation. SQLite is used as the primary " +
    "database. SQLAlchemy ORM simplifies interaction with database tables such as Faculty, Rooms, Courses, " +
    "Sections, and Timetable Entries.";
  body.appendParagraph(text3)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  /*************** 4.2 DATA FLOW DIAGRAMS ***************/
  p = body.appendParagraph("4.2 Data Flow Diagrams");
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true)
    .setHeading(DocumentApp.ParagraphHeading.HEADING2);

  var text4 =
    "Data Flow Diagrams (DFDs) describe how data moves inside the system. They capture the logical flow between " +
    "processes, data stores, and external entities.";
  body.appendParagraph(text4)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  /*************** 4.2.1 Level 0 DFD ***************/
  p = body.appendParagraph("4.2.1 Level 0 DFD");
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true)
    .setHeading(DocumentApp.ParagraphHeading.HEADING3);

  body.appendParagraph(
    "The Level 0 DFD represents the entire system as a single process. It shows interactions between users " +
    "and primary system functions such as course management, faculty management, and timetable generation.")
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  /*************** 4.2.2 Level 1 DFD ***************/
  p = body.appendParagraph("4.2.2 Level 1 DFD");
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true)
    .setHeading(DocumentApp.ParagraphHeading.HEADING3);

  var text5 =
    "The Level 1 DFD expands the main system into smaller processes such as:\n" +
    "• Faculty Management\n" +
    "• Room/Lab Management\n" +
    "• Course Mapping\n" +
    "• Hard Constraint Validation\n" +
    "• GA-based Optimization\n" +
    "• Timetable Export Engine";
  body.appendParagraph(text5)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  /*************** 4.3 ER DIAGRAM ***************/
  p = body.appendParagraph("4.3 ER Diagram");
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true)
    .setHeading(DocumentApp.ParagraphHeading.HEADING2);

  var text6 =
    "The Entity–Relationship (ER) diagram outlines the logical structure of the database used by the system. " +
    "Major entities include Faculty, Rooms, Sections, Courses, and Timetable Entries. Each entity maintains key " +
    "attributes such as faculty ID, room capacity, section code, and course L-T-P structure.";
  body.appendParagraph(text6)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  /*************** 4.4 MODULE DESIGN ***************/
  p = body.appendParagraph("4.4 Module Design");
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true)
    .setHeading(DocumentApp.ParagraphHeading.HEADING2);

  var text7 =
    "The system is divided into multiple functional modules. Each module focuses on a specific responsibility " +
    "and communicates with others through well-defined interfaces. Major modules include:\n" +
    "• Faculty Management Module\n" +
    "• Room and Lab Management Module\n" +
    "• Course Management Module\n" +
    "• Section & Batch Module\n" +
    "• CSP Constraint Validation Module\n" +
    "• Genetic Algorithm Optimization Module\n" +
    "• Timetable Export Module\n";
  body.appendParagraph(text7)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);
}





/********************************************
 * PART 5: CHAPTER 5 – MODULE DESIGN & DATABASE TABLES
 ********************************************/

// Part 5 function removed - integrated into generateCompleteReport



/**
 * CHAPTER 5 – MODULE DESIGN AND DATABASE TABLES
 */
function writeChapter5_ModulesAndDB(body) {
  // CHAPTER HEADING
  var p = body.appendParagraph("CHAPTER 5");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING1);
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(16);
  p.setBold(true);

  p = body.appendParagraph("MODULE DESIGN AND DATABASE TABLES");
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(14);
  p.setBold(true);

  addEmptyLine(body, 1);

  /*************** 5.1 MODULE OVERVIEW ***************/
  p = body.appendParagraph("5.1 Module Overview");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  var text =
    "The Automatic Timetable Generator is decomposed into multiple software modules, each responsible for a " +
    "specific part of the overall functionality. This modular design simplifies development, testing, and " +
    "maintenance. Modules communicate through well-defined interfaces and operate on shared database entities.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  /*************** 5.2 MODULE DESCRIPTIONS ***************/
  p = body.appendParagraph("5.2 Module Descriptions");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  addEmptyLine(body, 1);

  // 5.2.1 Faculty Management Module
  p = body.appendParagraph("5.2.1 Faculty Management Module");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  text =
    "The Faculty Management Module is responsible for handling all operations related to faculty members. " +
    "It allows the administrator to add new faculty, update existing details, and remove faculty records. " +
    "Key attributes managed include faculty name, unique code, department, maximum workload per week, and " +
    "specific time preferences (unavailable slots).";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);
  // 5.2.2 Room and Lab Management Module
  p = body.appendParagraph("5.2.2 Room and Lab Management Module");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  text =
    "This module manages information about all available classrooms and laboratories. It stores attributes such as " +
    "room code, room type (theory or lab), and capacity. The scheduler uses this data to allocate suitable rooms " +
    "for each class while respecting capacity constraints and ensuring that multiple classes are not scheduled in " +
    "the same room at the same time.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);
  // 5.2.3 Course Management Module
  p = body.appendParagraph("5.2.3 Course Management Module");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  text =
    "The Course Management Module handles creation and maintenance of course-related information. It stores for " +
    "each course the course code, course name, L-T-P structure (Lecture–Tutorial–Practical hours), semester, and " +
    "whether the course is a theory or laboratory course. This information is vital in deciding the number of " +
    "periods to be scheduled per week for each course and whether it must be mapped to lab rooms.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  // 5.2.4 Section and Batch Management Module
  p = body.appendParagraph("5.2.4 Section and Batch Management Module");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  text =
    "This module maintains section-wise information including section name, semester, and student strength. " +
    "It also handles batch-level information for laboratory sessions (for example, G1 and G2 batches). The " +
    "scheduler uses this data to correctly allocate lab batches to consecutive slots in appropriate lab rooms " +
    "and to ensure that batch-wise constraints are respected.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  // 5.2.5 Mapping Module
  p = body.appendParagraph("5.2.5 Faculty–Course–Section Mapping Module");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  text =
    "The Mapping Module connects faculty, courses, and sections by defining who teaches what and to which section. " +
    "Each mapping record indicates the faculty member, the course assigned, the target section or batch, and the " +
    "number of weekly periods required. These mappings form the foundation for generating the timetable, as each " +
    "mapping corresponds to one or more class events that must be scheduled.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  // 5.2.6 Hybrid Scheduler Module
  p = body.appendParagraph("5.2.6 Hybrid Scheduler (CSP + GA) Module");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  text =
    "This is the core computational module of the system. It uses a two-phase Hybrid Artificial Intelligence " +
    "approach. In the first phase, a Constraint Satisfaction Problem (CSP) solver generates an initial feasible " +
    "timetable that satisfies all hard constraints such as faculty clash, room clash, section clash, lab continuity, " +
    "and room capacity. In the second phase, a Genetic Algorithm (GA) operates on this feasible solution to " +
    "optimize soft constraints like minimizing gaps, satisfying faculty time preferences, and balancing workloads " +
    "across the week.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  // 5.2.7 Timetable View and Export Module
  p = body.appendParagraph("5.2.7 Timetable View and Export Module");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  text =
    "Once a timetable is generated, this module is responsible for presenting the data in a user-friendly form and " +
    "exporting it. It provides section-wise and faculty-wise views using HTML tables. It also supports conversion " +
    "of timetables into PDF and Excel formats so that they can be printed or shared via email and official notices.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  /*************** 5.3 DATABASE TABLES DESIGN ***************/
  p = body.appendParagraph("5.3 Database Tables Design");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "The database schema has been designed to store all the entities required for timetable generation in a " +
    "normalized form. Major tables and their key fields are summarized below.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  // Table 5.1: Database Tables Description
  p = body.appendParagraph("Table 5.1: Database Tables Description");
  p.setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(true);

  var table = body.appendTable();
  table.setBorderWidth(1);

  // Header row
  var headerRow = table.appendTableRow();
  var headerCells = ["Table Name", "Key Fields", "Description"];
  for (var h = 0; h < headerCells.length; h++) {
    headerRow.appendTableCell(headerCells[h]);
  }

  // Row data
  var dbRows = [
    [
      "Faculty",
      "faculty_id, name, code, max_load, unavailable_slots",
      "Stores information about each faculty member including availability and maximum workload."
       ],
    [
      "Room",
      "room_id, code, capacity, type",
      "Stores details of classrooms and laboratories including capacity and room type."
    ],
    [
      "Course",
      "course_id, code, name, ltp, semester, is_lab",
      "Stores course-related data such as code, name, L-T-P structure, semester, and whether it is a lab."
    ],
    [
      "Section",
      "section_id, name, semester, strength",
      "Stores information about each section, its semester, and number of students."
    ],
    [
      "Batch",
      "batch_id, section_id, name",
      "Represents lab batches (e.g., G1, G2) linked to a particular section."
    ],
    [
      "FacultyCourse",
      "mapping_id, faculty_id, course_id, section_id, batch_id, hours_per_week",
      "Mapping table that associates faculty with courses, sections/batches, and weekly hours."
    ],
    [
      "Timeslot",
      "timeslot_id, day, period_no, start_time, end_time",
      "Defines available time slots in the timetable grid for each day and period."
    ],
    [
      "Timetable",
      "entry_id, timeslot_id, room_id, mapping_id",
      "Stores the final generated timetable entries linking time slots, rooms, and course mappings."
    ]
  ];

  for (var r = 0; r < dbRows.length; r++) {
    var row = table.appendTableRow();
    row.appendTableCell(dbRows[r][0]);
    row.appendTableCell(dbRows[r][1]);
    row.appendTableCell(dbRows[r][2]);
  }

  // Format table cells
  var numRows = table.getNumRows();
  for (var i = 0; i < numRows; i++) {
    var row = table.getRow(i);
    var numCells = row.getNumCells();
    for (var j = 0; j < numCells; j++) {
      var cell = row.getCell(j);
      var cellText = cell.getChild(0).asParagraph();
      cellText.setFontFamily("Times New Roman");
      cellText.setFontSize(12);
      cellText.setLineSpacing(1.5);
      
      if (i === 0) {
        cellText.setBold(true);
        cell.setBackgroundColor("#E0E0E0");
      } else {
        cellText.setBold(false);
      }
    }
  }
}


/********************* CHAPTER 6 – PROJECT SNAPSHOTS *********************/

function writeChapter6_Snapshots(body) {
  // Chapter heading
  var p = body.appendParagraph("CHAPTER 6");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING1);
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(16);
  p.setBold(true);

  p = body.appendParagraph("PROJECT SNAPSHOTS");
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(14);
  p.setBold(true);

  addEmptyLine(body, 1);

  // 6.1 Dashboard Screen
  p = body.appendParagraph("6.1 Dashboard Screen");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  var text =
    "The dashboard is the landing page of the Automatic Timetable Generator. It provides a quick overview of " +
    "the system status, including the number of faculty members, rooms, courses, sections, and generated timetables. " +
    "It also provides navigation links to master data modules and the timetable generation module.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  var cap = body.appendParagraph("Figure 6.1: Dashboard Screen of Automatic Timetable Generator");
  cap.setFontFamily("Times New Roman")
     .setFontSize(11)
     .setBold(true)
     .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 1);

  // 6.2 Data Management Screens
  p = body.appendParagraph("6.2 Data Management Screens");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "Data management screens are used to create and maintain the master data of the system. These include " +
    "screens for Faculty Management, Room and Lab Management, Course Management, and Section/Batch Management. " +
    "Each screen typically contains tabular listings of existing records along with forms for adding or updating entries.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  cap = body.appendParagraph("Figure 6.2: Faculty Management Screen");
  cap.setFontFamily("Times New Roman")
     .setFontSize(11)
     .setBold(true)
     .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 1);

  cap = body.appendParagraph("Figure 6.3: Room and Lab Management Screen");
  cap.setFontFamily("Times New Roman")
     .setFontSize(11)
     .setBold(true)
     .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 1);

  // 6.3 Timetable Generation Screen
  p = body.appendParagraph("6.3 Timetable Generation Screen");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "The timetable generation screen allows the user to select the target semester or department configuration " +
    "and trigger the Hybrid AI scheduler. It typically displays status messages indicating progress of CSP-based " +
    "validation and GA-based optimization. Once the process completes, a success message is shown and the generated " +
    "timetables become available for viewing.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  cap = body.appendParagraph("Figure 6.4: Timetable Generation Screen");
  cap.setFontFamily("Times New Roman")
     .setFontSize(11)
     .setBold(true)
     .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 1);

  // 6.4 Timetable View and Export Screens
  p = body.appendParagraph("6.4 Timetable View and Export Screens");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "Once a timetable is generated, the system provides user interfaces for viewing and exporting the final schedule. " +
    "Section-wise timetables are displayed in grid form where days are shown row-wise and periods column-wise. " +
    "Similarly, faculty-wise timetables show the teaching load of each faculty member in a familiar timetable layout. " +
    "From these screens, users can export the timetables in PDF or Excel format for printing and distribution.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 1);

  cap = body.appendParagraph("Figure 6.5: Section-wise Timetable View");
  cap.setFontFamily("Times New Roman")
     .setFontSize(11)
     .setBold(true)
     .setAlignment(DocumentApp.HorizontalAlignment.CENTER);

  addEmptyLine(body, 1);

  cap = body.appendParagraph("Figure 6.6: Faculty-wise Timetable View and Export Options");
  cap.setFontFamily("Times New Roman")
     .setFontSize(11)
     .setBold(true)
     .setAlignment(DocumentApp.HorizontalAlignment.CENTER);
}


/********************* CHAPTER 7 – LIMITATIONS *********************/

function writeChapter7_Limitations(body) {
  // Chapter heading
  var p = body.appendParagraph("CHAPTER 7");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING1);
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(16);
  p.setBold(true);

  p = body.appendParagraph("LIMITATIONS");
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(14);
  p.setBold(true);

  addEmptyLine(body, 1);

  // 7.1 Current Limitations
  p = body.appendParagraph("7.1 Current Limitations");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  var text =
    "Although the Automatic Timetable Generator successfully addresses many of the challenges involved in manual " +
    "timetable preparation, the current implementation has certain limitations that can be considered for future improvements.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  var limList = [
    "The system is designed and tested for a single department (Computer Science & Engineering) and may require additional configuration for multi-department, institute-wide deployment.",
    "The time slot and working day structure are assumed to be fixed. Any change in the daily schedule (such as adding extra periods or half-days) requires configuration changes.",
    "The scheduler handles regular theory and lab classes only. Exam timetabling and invigilation duties are not included in the current scope.",
    "The system assumes that all input data (faculty details, course loads, room capacities, etc.) are accurate. Inconsistent or incomplete input can cause the scheduler to fail in generating a feasible timetable.",
    "The Genetic Algorithm parameters (population size, mutation rate, number of generations) are chosen empirically and may need tuning for very large problem sizes."
  ];

  for (var i = 0; i < limList.length; i++) {
    body.appendListItem(limList[i])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }

  // 7.2 Challenges Faced
  p = body.appendParagraph("7.2 Challenges Faced During Development");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "During the design and implementation of the Automatic Timetable Generator, several challenges were encountered, " +
    "especially in mapping real-world academic constraints into algorithmic form. Some of the major challenges are listed below.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  var challList = [
    "Modeling all hard and soft constraints in a way that the CSP solver and GA could handle efficiently.",
    "Ensuring that the CSP-generated initial solution was always feasible without causing excessive backtracking and timeouts.",
    "Balancing the trade-off between timetable quality and computation time while tuning Genetic Algorithm parameters.",
    "Designing a user interface that is simple for academic staff yet sufficiently expressive to capture complex mappings.",
    "Testing the system with different datasets to ensure that the scheduler works reliably for different semester configurations."
  ];

  for (var j = 0; j < challList.length; j++) {
    body.appendListItem(challList[j])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }
}


/********************* CHAPTER 8 – FUTURE SCOPE *********************/

function writeChapter8_FutureScope(body) {
  // Chapter heading
  var p = body.appendParagraph("CHAPTER 8");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING1);
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(16);
  p.setBold(true);

  p = body.appendParagraph("FUTURE SCOPE");
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(14);
  p.setBold(true);

  addEmptyLine(body, 1);

  // 8.1 Technical Enhancements
  p = body.appendParagraph("8.1 Technical Enhancements");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  var text =
    "The current implementation opens up several directions for technical improvements and extensions. Some " +
    "possible enhancements are given below:";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  var techList = [
    "Deployment of the application on cloud platforms such as AWS, Azure, or Google Cloud to support multi-user access from different locations.",
    "Migration from SQLite to a more scalable relational database system like MySQL or PostgreSQL for large-scale institute deployments.",
    "Integration of advanced optimization techniques (e.g., Simulated Annealing, Tabu Search, or Hybrid Metaheuristics) along with the existing GA.",
    "Implementation of role-based access control (RBAC) with different privilege levels for administrators, faculty members, and students.",
    "Addition of logging and analytics dashboards to monitor usage statistics and performance of the scheduling engine."
  ];

  for (var i = 0; i < techList.length; i++) {
    body.appendListItem(techList[i])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }

  // 8.2 Functional Enhancements
  p = body.appendParagraph("8.2 Functional Enhancements");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setFontFamily("Times New Roman")
    .setFontSize(14)
    .setBold(true);

  text =
    "In addition to technical improvements, the system can be extended functionally to cover other important " +
    "academic processes and user needs.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  var funcList = [
    "Extension of the scheduling engine to support exam timetables, including seating arrangements and invigilation duty assignment.",
    "Support for elective course selection at the student level, with automatic conflict detection and resolution.",
    "Development of a mobile application for students and faculty members to view their timetables and receive notifications.",
    "Implementation of a request/approval workflow where faculty members can request swaps or changes in specific periods.",
    "Integration with Learning Management Systems (LMS) to synchronize timetable data with online teaching platforms."
  ];

  for (var j = 0; j < funcList.length; j++) {
    body.appendListItem(funcList[j])
      .setGlyphType(DocumentApp.GlyphType.BULLET)
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5);
  }
}

function writeConclusionAndReferences(body) {
  /********************* CONCLUSION + REFERENCES *********************/
  var text =
    "The Automatic Timetable Generator using Hybrid AI (CSP + Genetic Algorithm) successfully demonstrates the " +
    "application of Artificial Intelligence techniques to a complex real-world scheduling problem. Manual " +
    "timetable preparation is a tedious and error-prone task, especially under modern curricula where the number " +
    "of courses, lab sessions, and elective options is high. By combining a CSP-based hard constraint solver with " +
    "a Genetic Algorithm for soft constraint optimization, the system is able to generate conflict-free and " +
    "reasonably optimized timetables within an acceptable time frame.\n\n" +
    "The project covers the complete lifecycle of software development, including requirements analysis, system " +
    "design, module decomposition, database design, implementation, and testing. The resulting web-based tool " +
    "provides an intuitive interface for academic staff to manage master data and generate timetables on demand. " +
    "Although the current version is focused on a single department, the underlying design can be extended to " +
    "support institute-wide scheduling with further enhancements.\n\n" +
    "Overall, this mini project not only addresses a practical need in academic administration but also provides " +
    "valuable hands-on experience in applying computational intelligence to a challenging optimization problem.";
  body.appendParagraph(text)
    .setFontFamily("Times New Roman")
    .setFontSize(12)
    .setBold(false)
    .setLineSpacing(1.5)
    .setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);

  addEmptyLine(body, 2);

  // REFERENCES
  p = body.appendParagraph("REFERENCES");
  p.setHeading(DocumentApp.ParagraphHeading.HEADING1);
  p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  p.setFontFamily("Times New Roman");
  p.setFontSize(16);
  p.setBold(true);

  addEmptyLine(body, 1);

  var refList = [
    "1. S. Russell and P. Norvig, \"Artificial Intelligence: A Modern Approach\", 3rd Edition, Pearson.",
    "2. E. K. Burke and S. Petrovic, \"Recent research directions in automated timetabling\", European Journal of Operational Research.",
    "3. D. E. Goldberg, \"Genetic Algorithms in Search, Optimization, and Machine Learning\", Addison-Wesley.",
    "4. Flask Web Framework Documentation, https://flask.palletsprojects.com/",
    "5. SQLAlchemy ORM Documentation, https://www.sqlalchemy.org/",
    "6. AKTU B.Tech CSE NEP 2020 Curriculum and Timetable Guidelines.",
    "7. Research articles and online resources related to University Course Timetabling Problem (UCTP) and hybrid metaheuristics."
  ];

  for (var i = 0; i < refList.length; i++) {
    body.appendParagraph(refList[i])
      .setFontFamily("Times New Roman")
      .setFontSize(12)
      .setBold(false)
      .setLineSpacing(1.5)
      .setAlignment(DocumentApp.HorizontalAlignment.LEFT);
  }
}