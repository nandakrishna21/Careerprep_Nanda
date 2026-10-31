export type ResourceCategory =
  | 'government'
  | 'practice'
  | 'courses'
  | 'coding'
  | 'interview'
  | 'books';

export type FreeResource = {
  name: string;
  url: string;
  description: string;
  category: ResourceCategory;
  tags: string[];
  featured?: boolean;
};

export const RESOURCE_CATEGORIES: { key: 'all' | ResourceCategory; label: string }[] = [
  { key: 'all', label: 'All' },
  { key: 'government', label: 'Government Portals' },
  { key: 'practice', label: 'Practice & Mocks' },
  { key: 'courses', label: 'Free Courses' },
  { key: 'coding', label: 'Coding & DSA' },
  { key: 'interview', label: 'Interview Prep' },
  { key: 'books', label: 'Notes & Books' },
];

export const CATEGORY_LABEL: Record<ResourceCategory, string> = {
  government: 'Government',
  practice: 'Practice',
  courses: 'Course',
  coding: 'Coding',
  interview: 'Interview',
  books: 'Notes',
};

export const FREE_RESOURCES: FreeResource[] = [
  {
    name: 'Staff Selection Commission (SSC)',
    url: 'https://ssc.gov.in',
    description:
      'Official SSC portal for CGL, CHSL, MTS and GD notices — syllabus, exam calendar, admit cards and results.',
    category: 'government',
    tags: ['SSC', 'CGL', 'CHSL', 'MTS'],
    featured: true,
  },
  {
    name: 'UPSC',
    url: 'https://upsc.gov.in',
    description:
      'Civil Services (IAS/IPS/IFS) notifications, syllabus, previous year question papers and interview schedules.',
    category: 'government',
    tags: ['UPSC', 'IAS', 'Civil Services'],
    featured: true,
  },
  {
    name: 'IBPS',
    url: 'https://www.ibps.in',
    description:
      'Bank PO, Clerk and SO recruitment calendar, notifications and eligibility details for public sector banks.',
    category: 'government',
    tags: ['Banking', 'PO', 'Clerk'],
  },
  {
    name: 'RRB Apply',
    url: 'https://www.rrbapply.gov.in',
    description:
      'Apply online for Railway NTPC, Group D and ALP posts; check application status and exam city details.',
    category: 'government',
    tags: ['Railways', 'NTPC', 'Group D'],
  },
  {
    name: 'NTA',
    url: 'https://nta.ac.in',
    description:
      'National Testing Agency — UGC NET, CUET, and other national-level entrance and eligibility exams.',
    category: 'government',
    tags: ['UGC NET', 'CUET', 'NTA'],
  },
  {
    name: 'Reserve Bank of India',
    url: 'https://www.rbi.org.in',
    description:
      'RBI Grade B and Assistant notifications, plus official publications useful for banking awareness.',
    category: 'government',
    tags: ['RBI', 'Grade B', 'Banking'],
  },
  {
    name: 'SBI Careers',
    url: 'https://sbi.co.in/web/careers',
    description:
      'State Bank of India PO, Clerk, and Specialist Officer openings with eligibility and application links.',
    category: 'government',
    tags: ['SBI', 'PO', 'Clerk'],
  },
  {
    name: 'National Career Service',
    url: 'https://www.ncs.gov.in',
    description:
      'Government job exchange with verified vacancies, career counselling and skill-based job matching.',
    category: 'government',
    tags: ['Job Search', 'Counselling'],
  },
  {
    name: 'Employment News',
    url: 'https://employmentnews.gov.in',
    description:
      'Weekly government gazette listing central and state vacancies, results and important dates — free to read.',
    category: 'government',
    tags: ['Gazette', 'Vacancies'],
  },
  {
    name: 'Join Indian Army',
    url: 'https://joinindianarmy.nic.in',
    description:
      'Official Indian Army recruitment — officer entries, Agniveer, TES and soldier trades with notification dates.',
    category: 'government',
    tags: ['Defence', 'Army', 'Agniveer'],
  },
  {
    name: 'Join Indian Navy',
    url: 'https://www.joinindiannavy.gov.in',
    description:
      'Indian Navy officer and sailor entries, eligibility, exam centres and online application portal.',
    category: 'government',
    tags: ['Defence', 'Navy', 'Officer'],
  },
  {
    name: 'Indian Air Force (AFCAT)',
    url: 'https://afcat.cdac.in/AFCAT/',
    description:
      'AFCAT and Agniveer Vayu notifications, syllabus, admit cards and results on the official IAF portal.',
    category: 'government',
    tags: ['Defence', 'AFCAT', 'Air Force'],
  },
  {
    name: 'Life Insurance Corporation (LIC)',
    url: 'https://licindia.in',
    description:
      'LIC AAO, ADO and Assistant recruitment notices along with official results and interview updates.',
    category: 'government',
    tags: ['Insurance', 'AAO', 'LIC'],
  },
  {
    name: 'EPFO',
    url: 'https://www.epfindia.gov.in',
    description:
      'Employees’ Provident Fund Organisation — recruitment notices and official circulars for central government posts.',
    category: 'government',
    tags: ['EPFO', 'Central Govt'],
  },
  {
    name: 'TSPSC (Telangana)',
    url: 'https://www.tspsc.gov.in',
    description:
      'Telangana State Public Service Commission notifications, hall tickets, syllabus and results.',
    category: 'government',
    tags: ['Telangana', 'State PSC', 'Group I'],
  },
  {
    name: 'APPSC (Andhra Pradesh)',
    url: 'https://psc.ap.gov.in',
    description:
      'Andhra Pradesh Public Service Commission Group I, II and other state government recruitment updates.',
    category: 'government',
    tags: ['Andhra', 'State PSC', 'Group II'],
  },
  {
    name: 'MPSC (Maharashtra)',
    url: 'https://mpsc.gov.in',
    description:
      'Maharashtra Public Service Commission state services exams, prelims and mains syllabus and results.',
    category: 'government',
    tags: ['Maharashtra', 'State PSC'],
  },
  {
    name: 'UPPSC (Uttar Pradesh)',
    url: 'https://uppsc.up.nic.in',
    description:
      'Uttar Pradesh PSC PCS, RO/ARO and other state-level exam notifications, calendars and answer keys.',
    category: 'government',
    tags: ['Uttar Pradesh', 'PCS', 'State PSC'],
  },
  {
    name: 'IndiaBIX',
    url: 'https://www.indiabix.com',
    description:
      'Aptitude, reasoning, verbal ability and programming questions with worked explanations — no sign-up needed.',
    category: 'practice',
    tags: ['Aptitude', 'Reasoning', 'English'],
    featured: true,
  },
  {
    name: 'PrepInsta',
    url: 'https://prepinsta.com',
    description:
      'Free placement and government exam practice: quant, logical reasoning, coding and company-wise papers.',
    category: 'practice',
    tags: ['Placement', 'Coding', 'Aptitude'],
  },
  {
    name: 'CareerRide',
    url: 'https://www.careerride.com',
    description:
      'Free interview questions, aptitude tests and HR round practice for freshers and experienced candidates.',
    category: 'practice',
    tags: ['Interview', 'Aptitude'],
  },
  {
    name: 'TCS iON NQT',
    url: 'https://learning.tcsionhub.in/hub/national-qualifier-test/',
    description:
      'Official TCS National Qualifier Test — free mock papers, syllabus and score-based hiring details.',
    category: 'practice',
    tags: ['TCS', 'NQT', 'Placement'],
  },
  {
    name: 'TypingClub',
    url: 'https://www.typingclub.com',
    description:
      'Free touch-typing practice with speed and accuracy tracking — essential for government typing tests.',
    category: 'practice',
    tags: ['Typing', 'Speed Test', 'Govt Exams'],
  },
  {
    name: 'SWAYAM',
    url: 'https://swayam.gov.in',
    description:
      'Government MOOC platform with free courses from IITs, NITs and central universities across every subject.',
    category: 'courses',
    tags: ['MOOC', 'Government', 'Certificates'],
  },
  {
    name: 'NPTEL',
    url: 'https://nptel.ac.in',
    description:
      'Free engineering, science and management courses from IITs and IISc with optional paid certification.',
    category: 'courses',
    tags: ['Engineering', 'IIT', 'Certification'],
  },
  {
    name: 'Khan Academy',
    url: 'https://www.khanacademy.org',
    description:
      'Free maths, science and economics lessons with practice sets — great for building exam fundamentals.',
    category: 'courses',
    tags: ['Maths', 'Science', 'Basics'],
  },
  {
    name: 'freeCodeCamp',
    url: 'https://www.freecodecamp.org',
    description:
      'Learn web development, Python and data skills through free interactive lessons and real projects.',
    category: 'courses',
    tags: ['Web Dev', 'Python', 'Projects'],
    featured: true,
  },
  {
    name: 'CS50 by Harvard',
    url: 'https://cs50.harvard.edu/x/',
    description:
      'Harvard’s free introduction to computer science — programming fundamentals, algorithms and problem sets.',
    category: 'courses',
    tags: ['CS', 'Algorithms', 'Harvard'],
  },
  {
    name: 'MIT OpenCourseWare',
    url: 'https://ocw.mit.edu',
    description:
      'Free lecture notes, videos and assignments from thousands of MIT courses, with no registration.',
    category: 'courses',
    tags: ['MIT', 'Lectures', 'Free'],
  },
  {
    name: 'OpenLearn (Open University)',
    url: 'https://www.open.edu/openlearn/',
    description:
      'Hundreds of free short courses with free statements of participation across business, tech and maths.',
    category: 'courses',
    tags: ['Free Courses', 'Statements'],
  },
  {
    name: 'Alison',
    url: 'https://alison.com',
    description:
      'Free online courses with certificates in IT, business, languages and workplace skills.',
    category: 'courses',
    tags: ['Certificates', 'Skills'],
  },
  {
    name: 'Microsoft Learn',
    url: 'https://learn.microsoft.com/training/',
    description:
      'Free hands-on training modules and learning paths for Azure, Power Platform, .NET and Microsoft 365.',
    category: 'courses',
    tags: ['Azure', '.NET', 'Microsoft'],
  },
  {
    name: 'Google Skillshop',
    url: 'https://skillshop.withgoogle.com',
    description:
      'Official free Google courses and certification prep for Analytics, Ads, Cloud and Workspace tools.',
    category: 'courses',
    tags: ['Google', 'Analytics', 'Certification'],
  },
  {
    name: 'Kaggle Learn',
    url: 'https://www.kaggle.com/learn',
    description:
      'Short free micro-courses on Python, pandas, SQL and machine learning with in-browser notebooks.',
    category: 'courses',
    tags: ['Data Science', 'Python', 'ML'],
  },
  {
    name: 'Coursera (Audit)',
    url: 'https://www.coursera.org',
    description:
      'Audit thousands of university courses for free — watch lectures and read material without paying.',
    category: 'courses',
    tags: ['University', 'Audit', 'Free'],
  },
  {
    name: 'edX (Audit)',
    url: 'https://www.edx.org',
    description:
      'Free audit access to courses from MIT, Harvard, IITs and more; pay only if you want a certificate.',
    category: 'courses',
    tags: ['University', 'Audit', 'Free'],
  },
  {
    name: 'GeeksforGeeks',
    url: 'https://www.geeksforgeeks.org',
    description:
      'DSA tutorials, interview experiences, aptitude notes and coding practice across every language.',
    category: 'coding',
    tags: ['DSA', 'Interview', 'Notes'],
  },
  {
    name: 'NeetCode',
    url: 'https://neetcode.io',
    description:
      'Structured DSA roadmap with free problems, video solutions and patterns for coding interviews.',
    category: 'coding',
    tags: ['DSA', 'Roadmap', 'Interviews'],
    featured: true,
  },
  {
    name: 'roadmap.sh',
    url: 'https://roadmap.sh',
    description:
      'Free step-by-step roadmaps for frontend, backend, DevOps, AI and more — know exactly what to learn next.',
    category: 'coding',
    tags: ['Roadmaps', 'Career', 'IT'],
  },
  {
    name: 'W3Schools',
    url: 'https://www.w3schools.com',
    description:
      'Beginner-friendly tutorials and try-it-yourself editors for HTML, CSS, JavaScript, SQL and Python.',
    category: 'coding',
    tags: ['HTML', 'CSS', 'SQL'],
  },
  {
    name: 'MDN Web Docs',
    url: 'https://developer.mozilla.org',
    description:
      'The reference documentation for HTML, CSS and JavaScript — free, accurate and used by professionals.',
    category: 'coding',
    tags: ['Web', 'Reference', 'JavaScript'],
  },
  {
    name: 'SQLBolt',
    url: 'https://sqlbolt.com',
    description:
      'Learn SQL interactively in the browser with short lessons and exercises — ideal for data and analyst roles.',
    category: 'coding',
    tags: ['SQL', 'Database', 'Data'],
  },
  {
    name: 'HackerRank Practice',
    url: 'https://www.hackerrank.com/domains',
    description:
      'Free domain-wise coding challenges in algorithms, SQL, Python and more, with instant judging.',
    category: 'coding',
    tags: ['Problems', 'SQL', 'Algorithms'],
  },
  {
    name: 'Codewars',
    url: 'https://www.codewars.com',
    description:
      'Solve community-made kata ranked by difficulty to sharpen problem solving in 50+ languages.',
    category: 'coding',
    tags: ['Kata', 'Practice', 'Languages'],
  },
  {
    name: 'Exercism',
    url: 'https://exercism.org',
    description:
      'Free coding exercises with human mentoring across 70+ languages — feedback, not just test cases.',
    category: 'coding',
    tags: ['Mentoring', 'Exercises', 'Free'],
  },
  {
    name: 'CSES Problem Set',
    url: 'https://cses.fi/problemset/',
    description:
      'Classic competitive programming tasks covering sorting, graphs, DP and trees — great for depth.',
    category: 'coding',
    tags: ['Competitive', 'DP', 'Graphs'],
  },
  {
    name: 'JavaScript.info',
    url: 'https://javascript.info',
    description:
      'Modern JavaScript tutorial from basics to advanced topics, with runnable examples and tasks.',
    category: 'coding',
    tags: ['JavaScript', 'Tutorial', 'Tasks'],
  },
  {
    name: 'The Odin Project',
    url: 'https://www.theodinproject.com',
    description:
      'Free full-stack curriculum with real projects in HTML, CSS, JavaScript, Node and databases.',
    category: 'coding',
    tags: ['Full Stack', 'Projects', 'Curriculum'],
  },
  {
    name: 'Full Stack Open',
    url: 'https://fullstackopen.com/en/',
    description:
      'University of Helsinki’s free modern web development course — React, Node, GraphQL and testing.',
    category: 'coding',
    tags: ['React', 'Node', 'GraphQL'],
  },
  {
    name: 'GitHub Skills',
    url: 'https://skills.github.com',
    description:
      'Free hands-on labs that teach Git, GitHub Actions and Pages directly inside real repositories.',
    category: 'coding',
    tags: ['Git', 'GitHub', 'CI/CD'],
  },
  {
    name: 'Python Official Tutorial',
    url: 'https://docs.python.org/3/tutorial/',
    description:
      'The official Python tutorial — authoritative, free and the fastest way to learn the language properly.',
    category: 'coding',
    tags: ['Python', 'Official', 'Reference'],
  },
  {
    name: 'Tech Interview Handbook',
    url: 'https://www.techinterviewhandbook.org',
    description:
      'Free guides on resumes, coding interviews, behavioural rounds and salary negotiation for tech roles.',
    category: 'interview',
    tags: ['Resume', 'Behavioural', 'Negotiation'],
    featured: true,
  },
  {
    name: 'Pramp',
    url: 'https://www.pramp.com',
    description:
      'Free peer-to-peer mock interviews — practise coding and system design with other candidates.',
    category: 'interview',
    tags: ['Mock Interview', 'Peer Practice'],
  },
  {
    name: 'InterviewBit',
    url: 'https://www.interviewbit.com',
    description:
      'Practice programming interview questions, take free mock tests and revise CS fundamentals.',
    category: 'interview',
    tags: ['Coding', 'CS Fundamentals'],
  },
  {
    name: 'LeetCode (Free Problems)',
    url: 'https://leetcode.com/problemset/',
    description:
      'Thousands of free coding problems filtered by topic and difficulty — the standard interview practice site.',
    category: 'interview',
    tags: ['Coding', 'Problems'],
  },
  {
    name: 'Canva Resume Templates',
    url: 'https://www.canva.com/resumes/templates/',
    description:
      'Free, recruiter-friendly resume templates you can edit in the browser and export as PDF.',
    category: 'interview',
    tags: ['Resume', 'Templates', 'PDF'],
  },
  {
    name: 'System Design Primer',
    url: 'https://github.com/donnemartin/system-design-primer',
    description:
      'Free open-source guide to designing scalable systems, with diagrams and real interview questions.',
    category: 'interview',
    tags: ['System Design', 'Scalability'],
  },
  {
    name: 'Interview Warmup (Google)',
    url: 'https://grow.google/certificates/interview-warmup/',
    description:
      'Practise answers aloud and get instant AI feedback on your wording, filler words and pacing.',
    category: 'interview',
    tags: ['Mock Interview', 'AI Feedback'],
  },
  {
    name: 'Big-O Cheat Sheet',
    url: 'https://www.bigocheatsheet.com',
    description:
      'Quick reference for time and space complexity of common data structures and sorting algorithms.',
    category: 'interview',
    tags: ['Complexity', 'Reference'],
  },
  {
    name: 'Awesome Interview Questions',
    url: 'https://github.com/DopplerHQ/awesome-interview-questions',
    description:
      'Curated list of interview question banks by language, framework and role — all free on GitHub.',
    category: 'interview',
    tags: ['Questions', 'Curated', 'GitHub'],
  },
  {
    name: 'NCERT Textbooks',
    url: 'https://ncert.nic.in',
    description:
      'Official free PDF textbooks for classes 6–12 — the base for UPSC, state PSC and government exam basics.',
    category: 'books',
    tags: ['PDF', 'UPSC', 'School'],
    featured: true,
  },
  {
    name: 'OpenStax',
    url: 'https://openstax.org',
    description:
      'Peer-reviewed, free university textbooks for maths, science, economics and business — no paywall.',
    category: 'books',
    tags: ['Textbooks', 'Free', 'University'],
  },
  {
    name: 'Project Gutenberg',
    url: 'https://www.gutenberg.org',
    description:
      'Over 70,000 free public-domain ebooks — novels, classics and reference works in every format.',
    category: 'books',
    tags: ['Ebooks', 'Classics', 'Public Domain'],
  },
  {
    name: 'Open Library',
    url: 'https://openlibrary.org',
    description:
      'Borrow digital books for free from the Internet Archive’s lending library with a free account.',
    category: 'books',
    tags: ['Borrow', 'Library', 'Ebooks'],
  },
  {
    name: 'Standard Ebooks',
    url: 'https://standardebooks.org',
    description:
      'Carefully edited, beautifully formatted public-domain ebooks — free EPUB and Kindle downloads.',
    category: 'books',
    tags: ['Ebooks', 'EPUB', 'Classics'],
  },
  {
    name: 'Wikibooks',
    url: 'https://www.wikibooks.org',
    description:
      'Community-written free textbooks and study guides covering science, computing and competitive exams.',
    category: 'books',
    tags: ['Textbooks', 'Wiki', 'Study'],
  },
  {
    name: 'Press Information Bureau (PIB)',
    url: 'https://pib.gov.in',
    description:
      'Official government press releases — the primary source for current affairs in UPSC and state PSC prep.',
    category: 'books',
    tags: ['Current Affairs', 'UPSC', 'Official'],
  },
  {
    name: 'GKToday',
    url: 'https://www.gktoday.in',
    description:
      'Free daily current affairs, static GK notes and quizzes for banking, SSC and civil services exams.',
    category: 'books',
    tags: ['Current Affairs', 'Quiz', 'GK'],
  },
  {
    name: 'Drishti IAS Free Downloads',
    url: 'https://www.drishtiias.com/free-downloads',
    description:
      'Free monthly current affairs magazines and UPSC notes in PDF — widely used for prelims revision.',
    category: 'books',
    tags: ['UPSC', 'PDF', 'Magazine'],
  },
];
