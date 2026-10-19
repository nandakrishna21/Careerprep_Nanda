// Curated YouTube channels + playlists for government-exam preparation.
// URLs verified against live YouTube search results — keep them real; never
// hand-guess a channel/playlist link here.

export type TutorialLanguage = 'telugu' | 'english' | 'both';

export type GovtTutorial = {
  id: string;
  title: string;
  channel: string;
  url: string;
  kind: 'channel' | 'playlist';
  language: TutorialLanguage;
  tags: string[];
  description: string;
};

export const GOVT_TUTORIALS: GovtTutorial[] = [
  // ── Telugu ───────────────────────────────────────────────────────────────
  {
    id: 'tg-adda247',
    title: 'Adda247 Telugu',
    channel: 'Adda247',
    url: 'https://www.youtube.com/channel/UCqqDD-1K6WTjS16Y8pdY1_Q',
    kind: 'channel',
    language: 'telugu',
    tags: ['TSPSC', 'TGPSC', 'APPSC', 'SSC', 'Banking'],
    description:
      'Daily current affairs, Groups, SI & Constable classes plus SSC and banking shortcut tricks — taught fully in Telugu.',
  },
  {
    id: 'tg-testbook',
    title: 'Testbook Telugu',
    channel: 'Testbook',
    url: 'https://www.youtube.com/channel/UC08MiG8-bjllfy94OeY5zWw',
    kind: 'channel',
    language: 'telugu',
    tags: ['TGPSC', 'APPSC', 'SSC', 'Railway', 'Banking', 'High Court'],
    description:
      'AP & TS focused classes: Groups 1-4, High Court, SSC, Railway and banking with daily current affairs and PYQ analysis in Telugu.',
  },
  {
    id: 'tg-ssc',
    title: 'SSC Telugu — Telugu Exams Prep',
    channel: 'SSC Telugu',
    url: 'https://www.youtube.com/@ssctelugu',
    kind: 'channel',
    language: 'telugu',
    tags: ['SSC', 'Railway', 'RRB'],
    description:
      'SSC CGL, CHSL, MTS and RRB exam explanations in simple Telugu — concept classes plus practice sessions.',
  },
  {
    id: 'tg-competitive',
    title: 'Telugu Competitive Exams',
    channel: 'Telugu Competitive Exams',
    url: 'https://www.youtube.com/c/Telugucompetitiveexams',
    kind: 'channel',
    language: 'telugu',
    tags: ['TSPSC', 'APPSC', 'Police', 'SI/Constable'],
    description:
      'Topic-wise GS, history, polity and fast revision videos in Telugu for TSPSC, APPSC and police exams.',
  },
  {
    id: 'tg-sakshi',
    title: 'Sakshi Education',
    channel: 'Sakshi Education',
    url: 'https://www.youtube.com/sakshibhavita',
    kind: 'channel',
    language: 'telugu',
    tags: ['TSPSC', 'APPSC', 'DSC', 'Current Affairs'],
    description:
      'Daily current affairs, job notifications and exam guidance videos in Telugu for TSPSC, APPSC and DSC aspirants.',
  },
  {
    id: 'tg-kiran',
    title: 'Kiran Studies for Competitive Exams',
    channel: 'Kiran Studies',
    url: 'https://www.youtube.com/channel/UC-NzxiLMRY99WT5hTuwoRLA',
    kind: 'channel',
    language: 'both',
    tags: ['SSC', 'Banking', 'SI/Constable', 'Groups', 'NCERT'],
    description:
      'Bilingual Telugu + English classes: aptitude, reasoning, GS (History, Polity, Telangana Movement) and NCERT science from 6th to degree level.',
  },
  {
    id: 'tg-group2',
    title: 'Group 2 Preparation (50-video playlist)',
    channel: 'P Krishna Pradeep',
    url: 'https://www.youtube.com/playlist?list=PLTLlgwpX6dw3k0CYQuuukCro87W7cF50t',
    kind: 'playlist',
    language: 'telugu',
    tags: ['TSPSC', 'APPSC', 'Group 2'],
    description:
      'Complete Group 2 playlist: syllabus walkthroughs, topper strategies, free tests and subject-wise tips from faculty and rankers.',
  },

  // ── English ──────────────────────────────────────────────────────────────
  {
    id: 'en-adda247',
    title: 'Adda247',
    channel: 'Adda247',
    url: 'https://www.youtube.com/channel/UC1L2JoMpcY6MRLhFd3gg5Xg',
    kind: 'channel',
    language: 'english',
    tags: ['Banking', 'SSC', 'Railway'],
    description:
      'Banking, SSC and railway marathons — quant, reasoning, English and banking awareness with daily live practice sets.',
  },
  {
    id: 'en-adda247-ssc',
    title: 'Adda247 SSC Exams',
    channel: 'Adda247',
    url: 'https://www.youtube.com/channel/UCAyYBPzFioHUxvVZEn4rMJA',
    kind: 'channel',
    language: 'english',
    tags: ['SSC', 'CGL', 'CHSL', 'CPO'],
    description:
      'Complete SSC CGL/CHSL/CPO preparation: previous-year solutions, vocabulary series, English rules and GS capsules.',
  },
  {
    id: 'en-testbook',
    title: 'Testbook',
    channel: 'Testbook',
    url: 'https://www.youtube.com/@Testbook',
    kind: 'channel',
    language: 'english',
    tags: ['SSC', 'Banking', 'Railway', 'UPSC'],
    description:
      'SSC, banking and railway crash courses, mock-test analysis and current-affairs shows with top educators.',
  },
  {
    id: 'en-studyiq',
    title: 'StudyIQ IAS',
    channel: 'StudyIQ',
    url: 'https://www.youtube.com/channel/UCrC8mOqJQpoB7NuIMKIS6rQ',
    kind: 'channel',
    language: 'english',
    tags: ['UPSC', 'State PSC', 'Current Affairs'],
    description:
      'Crisp editorial analysis plus polity, economy and history lectures for UPSC and state PSC exams — in English.',
  },
  {
    id: 'en-drishti',
    title: 'Drishti IAS (English)',
    channel: 'Drishti IAS',
    url: 'https://www.youtube.com/@DrishtiIASEnglish',
    kind: 'channel',
    language: 'english',
    tags: ['UPSC', 'State PSC', 'Current Affairs'],
    description:
      'UPSC current affairs, The Hindu analysis and GS concept classes in English, plus mains answer-writing guidance.',
  },
  {
    id: 'en-oliveboard',
    title: 'Oliveboard',
    channel: 'Oliveboard',
    url: 'https://www.youtube.com/@OliveboardApp',
    kind: 'channel',
    language: 'english',
    tags: ['Banking', 'RBI', 'Insurance'],
    description:
      'Banking and RBI Grade B sessions — mock-test walkthroughs, banking awareness and mains/ interview strategy.',
  },
  {
    id: 'en-wifistudy',
    title: 'wifistudy by Unacademy',
    channel: 'wifistudy',
    url: 'https://www.youtube.com/channel/UCuWuAvEnKWez5BUr29VpwqA',
    kind: 'channel',
    language: 'english',
    tags: ['SSC', 'Railway', 'Foundation'],
    description:
      'Foundation-to-advance SSC and railway series with daily current affairs, speed quizzes and revision marathons.',
  },
  {
    id: 'en-unacademy',
    title: 'Unacademy India',
    channel: 'Unacademy',
    url: 'https://www.youtube.com/@unacademy',
    kind: 'channel',
    language: 'english',
    tags: ['SSC', 'Banking', 'UPSC', 'Railway'],
    description:
      'Free flagship classes and exam-strategy sessions covering SSC, banking, UPSC and railway exams.',
  },
];
