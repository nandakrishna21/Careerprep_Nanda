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
  },
  {
    name: 'UPSC',
    url: 'https://upsc.gov.in',
    description:
      'Civil Services (IAS/IPS/IFS) notifications, syllabus, previous year question papers and interview schedules.',
    category: 'government',
    tags: ['UPSC', 'IAS', 'Civil Services'],
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
    name: 'IndiaBIX',
    url: 'https://www.indiabix.com',
    description:
      'Aptitude, reasoning, verbal ability and programming questions with worked explanations — no sign-up needed.',
    category: 'practice',
    tags: ['Aptitude', 'Reasoning', 'English'],
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
    name: 'Tech Interview Handbook',
    url: 'https://www.techinterviewhandbook.org',
    description:
      'Free guides on resumes, coding interviews, behavioural rounds and salary negotiation for tech roles.',
    category: 'interview',
    tags: ['Resume', 'Behavioural', 'Negotiation'],
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
    name: 'NCERT Textbooks',
    url: 'https://ncert.nic.in',
    description:
      'Official free PDF textbooks for classes 6–12 — the base for UPSC, state PSC and government exam basics.',
    category: 'books',
    tags: ['PDF', 'UPSC', 'School'],
  },
  {
    name: 'OpenStax',
    url: 'https://openstax.org',
    description:
      'Peer-reviewed, free university textbooks for maths, science, economics and business — no paywall.',
    category: 'books',
    tags: ['Textbooks', 'Free', 'University'],
  },
];
