"""General Awareness banks: History, Geography, Polity, Economy, Current Affairs, Science."""
from __future__ import annotations

from app.seed.gov_reasoning import Bank
from app.seed.util import QuestionDict

HISTORY: Bank = {
    "beginner": [
        ("The Quit India Movement was launched in which year?", ["1920", "1930", "1942", "1947"], 2, "Gandhi gave the 'Do or Die' call in August 1942."),
        ("Who was the first President of India?", ["Jawaharlal Nehru", "Dr. Rajendra Prasad", "Sardar Patel", "Dr. Radhakrishnan"], 1, "Dr. Rajendra Prasad was the first President (1950-1962)."),
        ("The Battle of Plassey was fought in which year?", ["1757", "1764", "1857", "1942"], 0, "Battle of Plassey, 1757 — Clive defeated Siraj-ud-Daulah."),
        ("Who founded the Mughal Empire in India?", ["Akbar", "Babur", "Shah Jahan", "Humayun"], 1, "Babur founded the Mughal Empire after the Battle of Panipat (1526)."),
        ("The Dandi March (1930) was part of which movement?", ["Non-Cooperation Movement", "Quit India Movement", "Civil Disobedience Movement", "Khilafat Movement"], 2, "The Salt March launched the Civil Disobedience Movement."),
        ("Who wrote the book 'The Discovery of India'?", ["Mahatma Gandhi", "Jawaharlal Nehru", "Rabindranath Tagore", "Sardar Patel"], 1, "Nehru wrote it during imprisonment at Ahmednagar Fort (1942-1946)."),
    ],
    "intermediate": [
        ("The Constitution of India was adopted on which date?", ["26 January 1950", "26 November 1949", "15 August 1947", "26 January 1949"], 1, "Adopted on 26 Nov 1949; it came into force on 26 Jan 1950."),
        ("The Non-Cooperation Movement was launched by Gandhi in which year?", ["1919", "1920", "1930", "1942"], 1, "The Non-Cooperation Movement began in 1920 under the Khilafat backdrop."),
        ("The Jallianwala Bagh massacre took place in which year?", ["1905", "1919", "1922", "1930"], 1, "The massacre occurred on 13 April 1919 in Amritsar."),
        ("Who was the Viceroy of India at the time of independence?", ["Lord Linlithgow", "Lord Wavell", "Lord Mountbatten", "Lord Irwin"], 2, "Lord Mountbatten was Viceroy when India became independent in 1947."),
        ("The Second Battle of Panipat (1556) was fought between Akbar and:", ["Rana Sanga", "Hemu", "Sher Shah", "Bahadur Shah"], 1, "Akbar defeated Hemu in the Second Battle of Panipat (1556)."),
        ("Who founded the Brahmo Samaj in 1828?", ["Dayananda Saraswati", "Raja Ram Mohan Roy", "Vivekananda", "Ishwar Chandra Vidyasagar"], 1, "Raja Ram Mohan Roy founded the Brahmo Samaj in 1828."),
    ],
    "advanced": [
        ("The Permanent Settlement of Bengal (1793) was introduced by:", ["Lord Clive", "Lord Cornwallis", "Lord Wellesley", "Lord Dalhousie"], 1, "Lord Cornwallis introduced the Permanent Settlement in 1793."),
        ("The Congress split into Moderates and Extremists at which session?", ["Calcutta 1906", "Surat 1907", "Lahore 1929", "Lucknow 1916"], 1, "The Surat Split of 1907 divided the Congress into Moderates and Extremists."),
        ("The Rowlatt Act was passed in which year?", ["1909", "1919", "1922", "1935"], 1, "The Rowlatt Act (1919) allowed detention without trial and led to protests."),
        ("Who founded the Home Rule League in 1916 along with Bal Gangadhar Tilak?", ["Sarojini Naidu", "Annie Besant", "Madan Mohan Malaviya", "C. R. Das"], 1, "Annie Besant and Tilak founded Home Rule Leagues in 1916."),
        ("The Delhi Sultanate was founded by:", ["Alauddin Khalji", "Qutb-ud-din Aibak", "Iltutmish", "Balban"], 1, "Qutb-ud-din Aibak founded the Delhi Sultanate in 1206."),
        ("The Vijayanagara Empire was founded by:", ["Krishnadevaraya", "Harihara and Bukka", "Saluva Narasimha", "Rama Raya"], 1, "Harihara I and Bukka Raya I founded Vijayanagara in 1336."),
    ],
}

# PYQ-paper expansion (2020-2026 sets): extra practice depth per level.
HISTORY["beginner"] += [
    ("The Battle of Buxar was fought in which year?", ["1764", "1757", "1772", "1782"], 0, "The Battle of Buxar (1764) gave the British the Diwani of Bengal."),
    ("Who was the founder of the Maurya Empire?", ["Ashoka", "Chandragupta Maurya", "Bindusara", "Kanishka"], 1, "Chandragupta Maurya founded the Maurya Empire around 321 BCE."),
    ("The First War of Independence (1857) started from which city?", ["Delhi", "Kanpur", "Meerut", "Lucknow"], 2, "The 1857 revolt began at Meerut on 10 May 1857."),
    ("Who gave the slogan 'Inquilab Zindabad'?", ["Bhagat Singh", "Hasrat Mohani", "Subhas Bose", "Lala Lajpat Rai"], 1, "Hasrat Mohani coined it; Bhagat Singh popularised it."),
    ("The Indus Valley site of Lothal is located in which present-day state?", ["Rajasthan", "Gujarat", "Punjab", "Haryana"], 1, "Lothal, the famous dockyard site, is in Gujarat."),
    ("Who was the last Mughal emperor?", ["Aurangzeb", "Shah Alam II", "Bahadur Shah Zafar", "Akbar II"], 2, "Bahadur Shah Zafar was exiled to Rangoon after 1857."),
]
HISTORY["intermediate"] += [
    ("The Treaty of Allahabad (1765) was signed after which battle?", ["Plassey", "Buxar", "Wandiwash", "Panipat"], 1, "Clive secured the Diwani through the Treaty of Allahabad after Buxar."),
    ("Who presided over the first session of the Indian National Congress (1885)?", ["A. O. Hume", "W. C. Bonnerjee", "Dadabhai Naoroji", "Surendranath Banerjee"], 1, "W. C. Bonnerjee presided at Bombay in December 1885."),
    ("The Chauri Chaura incident (1922) led Gandhi to:", ["Launch Quit India", "Suspend Non-Cooperation", "Start Dandi March", "Fast unto death"], 1, "Gandhi suspended the Non-Cooperation Movement after Chauri Chaura."),
    ("Ashoka's Dhamma policy is best described as:", ["Forced Buddhism", "Moral and ethical code for all", "Ban on rituals", "Tax reform"], 1, "Dhamma was a moral code of tolerance and non-violence for everyone."),
    ("The Cabinet Mission arrived in India in which year?", ["1942", "1945", "1946", "1947"], 2, "The Cabinet Mission came in March 1946 to discuss transfer of power."),
    ("Who was known as the 'Grand Old Man of India'?", ["Gopal Krishna Gokhale", "Dadabhai Naoroji", "Bal Gangadhar Tilak", "Ferozeshah Mehta"], 1, "Dadabhai Naoroji earned that title for his decades of service."),
]
HISTORY["advanced"] += [
    ("The Battle of Talikota (1565), which broke Vijayanagara power, was fought between:", ["Rama Raya and the Deccan Sultanates", "Krishnadevaraya and Babur", "Harihara and Alauddin Khalji", "Bukka and Muhammad Tughlaq"], 0, "An alliance of Deccan Sultanates defeated Rama Raya at Talikota in 1565."),
    ("The Ilbert Bill controversy (1883-84) concerned:", ["Arms licences", "Indian judges trying Europeans", "Salt tax", "Forest rights"], 1, "The Bill let Indian judges try European offenders, sparking white opposition."),
    ("The 'Drain of Wealth' theory was first systematically presented by:", ["R. C. Dutt in 1901", "Dadabhai Naoroji in 1867", "M. G. Ranade in 1872", "G. V. Joshi in 1888"], 1, "Naoroji presented the drain theory in 1867."),
    ("The Theosophical Society's headquarters in India was established at:", ["Adyar, Madras", "Varanasi", "Pune", "Calcutta"], 0, "Blavatsky and Olcott set up the Adyar headquarters in 1882."),
    ("The Pitt's India Act (1784) set up which body to control the Company?", ["Board of Control", "Court of Directors", "Council of India", "Imperial Council"], 0, "Pitt's Act created a six-member Board of Control in London."),
    ("The Simon Commission arrived in India in 1928. How many Indian members did it have?", ["Two", "One", "Zero", "Seven"], 2, "The all-white Simon Commission had zero Indian members, sparking boycotts."),
]

GEOGRAPHY: Bank = {
    "beginner": [
        ("The Tropic of Cancer passes through how many Indian states?", ["6", "7", "8", "9"], 2, "It passes through 8 states: Gujarat, Rajasthan, MP, Chhattisgarh, Jharkhand, WB, Tripura, Mizoram."),
        ("Which is the longest river in India?", ["Godavari", "Ganga", "Yamuna", "Brahmaputra"], 1, "The Ganga (about 2,525 km within India) is the longest river."),
        ("The capital of Australia is:", ["Sydney", "Melbourne", "Canberra", "Perth"], 2, "Canberra is the capital of Australia."),
        ("Which is the largest ocean on Earth?", ["Atlantic", "Indian", "Arctic", "Pacific"], 3, "The Pacific Ocean is the largest and deepest ocean."),
        ("The Sahara Desert is located in which continent?", ["Asia", "Africa", "Australia", "South America"], 1, "The Sahara is the world's largest hot desert, in North Africa."),
        ("Which mountain range forms the traditional boundary between Europe and Asia?", ["Urals", "Alps", "Andes", "Himalayas"], 0, "The Ural Mountains are the conventional Europe-Asia boundary."),
    ],
    "intermediate": [
        ("Which Indian state has the longest coastline?", ["Tamil Nadu", "Andhra Pradesh", "Gujarat", "Maharashtra"], 2, "Gujarat has the longest coastline among Indian states."),
        ("The Sundarbans delta is formed by which rivers?", ["Ganga and Brahmaputra", "Godavari and Krishna", "Narmada and Tapti", "Mahanadi and Brahmani"], 0, "The Sundarbans is formed by the Ganga-Brahmaputra delta system."),
        ("Which imaginary line divides the Earth into Northern and Southern hemispheres?", ["Tropic of Cancer", "Equator", "Prime Meridian", "Arctic Circle"], 1, "The Equator (0° latitude) divides the two hemispheres."),
        ("The Antarctic Circle lies at approximately which latitude?", ["23.5°S", "45°S", "66.5°S", "80°S"], 2, "The Antarctic Circle is at about 66.5° South."),
        ("Which is the largest Indian state by area?", ["Madhya Pradesh", "Maharashtra", "Rajasthan", "Uttar Pradesh"], 2, "Rajasthan is the largest state by area."),
        ("Mount Everest lies on the border of Nepal and:", ["India", "China", "Bhutan", "Pakistan"], 1, "Everest sits on the Nepal-China (Tibet) border."),
    ],
    "advanced": [
        ("Which soil is most suitable for cotton cultivation in India?", ["Alluvial", "Black (Regur)", "Laterite", "Red"], 1, "Black soil retains moisture and is ideal for cotton — hence 'black cotton soil'."),
        ("Which is the largest freshwater lake in the world by surface area?", ["Lake Baikal", "Lake Victoria", "Lake Superior", "Lake Michigan"], 2, "Lake Superior has the largest surface area; Baikal is the deepest by volume."),
        ("Which ocean current is known as the 'Gulf Stream of the Pacific'?", ["Humboldt Current", "Kuroshio Current", "Labrador Current", "Benguela Current"], 1, "The Kuroshio Current is the warm western boundary current of the North Pacific."),
        ("Wular Lake, often called Asia's largest freshwater lake, is located in:", ["Himachal Pradesh", "Uttarakhand", "Jammu and Kashmir", "Sikkim"], 2, "Wular Lake lies in Jammu and Kashmir, fed by the Jhelum."),
        ("Isohyets are lines on a map joining places with:", ["Equal rainfall", "Equal temperature", "Equal sunshine", "Equal elevation"], 0, "Iso-hyet comes from Greek 'isos' (equal) + 'hyetos' (rain)."),
        ("Which Indian river forms the Dhuandhar Falls at Jabalpur?", ["Narmada", "Tapti", "Chambal", "Son"], 0, "The Narmada forms Dhuandhar Falls near the Marble Rocks at Bhedaghat."),
    ],
}

# PYQ-paper expansion (2020-2026 sets): extra practice depth per level.
GEOGRAPHY["beginner"] += [
    ("Which is the smallest state of India by area?", ["Sikkim", "Goa", "Tripura", "Manipur"], 1, "Goa is the smallest state by area."),
    ("The Deccan Plateau is primarily made of which rock?", ["Granite", "Basalt", "Sandstone", "Marble"], 1, "The Deccan Traps are vast basalt lava flows."),
    ("Which river is called the 'Sorrow of Bengal'?", ["Hooghly", "Damodar", "Mahanadi", "Subarnarekha"], 1, "The Damodar's floods earned it that name before the DVC dams."),
    ("The Konkan coast lies between:", ["The Western Ghats and the Arabian Sea", "The Eastern Ghats and the Bay of Bengal", "The Aravallis and the Thar", "The Shivaliks and the plains"], 0, "Konkan is the coastal strip of Maharashtra between the Western Ghats and the Arabian Sea."),
    ("Which country is called the 'Land of the Rising Sun'?", ["China", "Japan", "Thailand", "Korea"], 1, "Japan lies east of Asia, where the sun rises first."),
    ("The Prime Meridian passes through which city?", ["Paris", "Greenwich", "Rome", "Madrid"], 1, "Zero longitude runs through Greenwich, London."),
]
GEOGRAPHY["intermediate"] += [
    ("Which of these rivers flows westwards into the Arabian Sea?", ["Mahanadi", "Godavari", "Narmada", "Krishna"], 2, "The Narmada flows west through a rift valley into the Arabian Sea."),
    ("The 'karewas' of Kashmir are best described as:", ["Glacial lakes", "Oxbow lakes", "Ancient lake deposits", "Crater lakes"], 2, "Karewas are ancient lacustrine deposits, ideal for saffron and horticulture."),
    ("Which pass connects Srinagar to Leh?", ["Rohtang", "Zoji La", "Banihal", "Shipki La"], 1, "Zoji La on the Great Himalayan Range links Srinagar and Leh."),
    ("The Chota Nagpur Plateau is rich in which resource?", ["Petroleum", "Minerals and coal", "Tea", "Cotton"], 1, "Chota Nagpur holds India's major coal and mineral belts."),
    ("Which current flows along the west coast of South America?", ["Gulf Stream", "Humboldt (Peru) Current", "Agulhas Current", "Kuroshio Current"], 1, "The cold Humboldt Current flows north along Peru and Chile."),
    ("The 82.5 degrees East longitude is significant for India because:", ["It marks the Tropic of Cancer", "Indian Standard Time is based on it", "It is the easternmost point", "It divides two zones"], 1, "IST (GMT + 5:30) is based on 82.5E passing near Mirzapur."),
]
GEOGRAPHY["advanced"] += [
    ("The Grand Canyon has been carved by which river?", ["Missouri", "Colorado", "Columbia", "Rio Grande"], 1, "The Colorado River carved the Grand Canyon over millions of years."),
    ("Which of these is a cold desert in India?", ["Thar", "Ladakh", "Rann of Kutch", "Deccan"], 1, "Ladakh's high altitude makes it a cold desert."),
    ("The doldrums refer to:", ["Horse latitudes", "Equatorial low-pressure calm belt", "Polar highs", "Trade wind deserts"], 1, "The doldrums are the calm equatorial belt where trade winds converge."),
    ("Which strait separates Sri Lanka from India?", ["Malacca Strait", "Palk Strait", "Sunda Strait", "Bering Strait"], 1, "The Palk Strait (with Adam's Bridge) separates Tamil Nadu and Sri Lanka."),
    ("Laterite soils develop mainly under conditions of:", ["Low rainfall", "High temperature and heavy rainfall with leaching", "Permafrost", "Volcanic ash"], 1, "Intense leaching in hot, wet climates produces laterite."),
    ("The Rhine river empties into which sea?", ["Mediterranean Sea", "North Sea", "Baltic Sea", "Black Sea"], 1, "The Rhine flows through Rotterdam into the North Sea."),
]

POLITY: Bank = {
    "beginner": [
        ("Who is the constitutional head of the Indian State?", ["Prime Minister", "President", "Chief Justice", "Speaker"], 1, "Article 52 — the President is the head of the Indian State."),
        ("How many Fundamental Rights are currently guaranteed by the Constitution?", ["5", "6", "7", "8"], 1, "There are 6 Fundamental Rights after the Right to Property was removed (1978)."),
        ("The Constitution of India came into force on:", ["15 August 1947", "26 January 1950", "26 November 1949", "2 October 1950"], 1, "It came into force on 26 January 1950 — celebrated as Republic Day."),
        ("Who is the head of the government of India?", ["President", "Prime Minister", "Chief Justice", "Vice President"], 1, "The Prime Minister is the head of the government."),
        ("The Parliament of India consists of:", ["Lok Sabha only", "Rajya Sabha only", "Lok Sabha and Rajya Sabha", "Lok Sabha and Vidhan Sabhas"], 2, "Parliament = President + Lok Sabha + Rajya Sabha."),
        ("Which article provides the Right to Education?", ["Article 19", "Article 21", "Article 21A", "Article 32"], 2, "Article 21A (inserted by the 86th Amendment) guarantees education for 6-14 year olds."),
    ],
    "intermediate": [
        ("The concept of Fundamental Duties in the Indian Constitution is borrowed from:", ["USA", "USSR", "UK", "Ireland"], 1, "Fundamental Duties were borrowed from the Soviet Union (added by 42nd Amendment)."),
        ("Who appoints the Chief Election Commissioner of India?", ["Prime Minister", "President", "Chief Justice", "Parliament"], 1, "The President appoints the CEC (Article 324)."),
        ("A Money Bill can be introduced only in:", ["Rajya Sabha", "Lok Sabha", "Either House", "Joint sitting"], 1, "Under Article 110, a Money Bill can be introduced only in the Lok Sabha."),
        ("The maximum permitted strength of the Rajya Sabha is:", ["238", "245", "250", "252"], 2, "Article 80 caps the Rajya Sabha at 250 members (238 elected + 12 nominated)."),
        ("Which writ is issued to release a person from unlawful detention?", ["Mandamus", "Certiorari", "Habeas Corpus", "Quo Warranto"], 2, "Habeas Corpus literally means 'to have the body' — it challenges illegal detention."),
        ("The Preamble declares India to be a:", ["Sovereign Socialist Secular Democratic Republic", "Federal Socialist Democratic Union", "Sovereign Democratic Federal Republic", "Secular Federal Socialist Republic"], 0, "The Preamble: 'Sovereign Socialist Secular Democratic Republic'."),
    ],
    "advanced": [
        ("Which Constitutional Amendment added the word 'Secular' to the Preamble?", ["42nd Amendment", "44th Amendment", "52nd Amendment", "73rd Amendment"], 0, "The 42nd Amendment (1976) added 'Socialist', 'Secular' and 'Integrity'."),
        ("The doctrine of 'Basic Structure' of the Constitution was propounded in:", ["Minerva Mills case", "Kesavananda Bharati case", "Golaknath case", "Maneka Gandhi case"], 1, "The Supreme Court laid down the basic structure doctrine in Kesavananda Bharati (1973)."),
        ("Article 356 of the Constitution deals with:", ["National Emergency", "President's Rule in a State", "Financial Emergency", "Amendment procedure"], 1, "Article 356 provides for President's Rule in a state on failure of constitutional machinery."),
        ("The Finance Commission is constituted under which Article of the Constitution?", ["Article 280", "Article 312", "Article 320", "Article 360"], 0, "Article 280 provides for the Finance Commission."),
        ("The 73rd Constitutional Amendment (1992) relates to:", ["Municipalities", "Panchayati Raj", "Cooperative Societies", "Right to Education"], 1, "The 73rd Amendment gave constitutional status to Panchayati Raj institutions."),
        ("Which Amendment gave constitutional status to the National Commission for Backward Classes?", ["100th Amendment", "101st Amendment", "102nd Amendment", "103rd Amendment"], 2, "The 102nd Amendment (2018) gave NCBC constitutional status."),
    ],
}

# PYQ-paper expansion (2020-2026 sets): extra practice depth per level.
POLITY["beginner"] += [
    ("The Preamble declares India to be which kind of republic?", ["Democratic", "Sovereign Socialist Secular Democratic", "Federal", "Presidential"], 1, "The Preamble (after the 42nd Amendment) reads Sovereign Socialist Secular Democratic Republic."),
    ("Who appoints the Chief Minister of a state?", ["President", "Governor", "Chief Justice", "Prime Minister"], 1, "The Governor appoints the Chief Minister (Article 164)."),
    ("The minimum age to become President of India is:", ["25 years", "30 years", "35 years", "21 years"], 2, "Article 58 requires 35 years for the presidency."),
    ("Which house of Parliament is permanent and never dissolved?", ["Lok Sabha", "Rajya Sabha", "Both", "Neither"], 1, "Rajya Sabha is a continuing body; one-third retires every two years."),
    ("Fundamental Duties were added by which amendment?", ["42nd Amendment", "44th Amendment", "52nd Amendment", "61st Amendment"], 0, "The 42nd Amendment (1976) added Part IVA with 10 duties."),
    ("The Election Commission is mentioned in which article?", ["Article 320", "Article 324", "Article 326", "Article 330"], 1, "Article 324 vests superintendence of elections in the Election Commission."),
]
POLITY["intermediate"] += [
    ("Which writ is issued to produce a detained person before the court?", ["Mandamus", "Habeas Corpus", "Certiorari", "Quo Warranto"], 1, "Habeas Corpus ('to have the body') tests the legality of detention."),
    ("The Sarkaria Commission (1983) dealt with:", ["Centre-State relations", "Electoral reforms", "Police reforms", "Banking supervision"], 0, "Sarkaria reviewed Centre-State relations and Article 356 misuse."),
    ("A money bill can be introduced only in:", ["Rajya Sabha", "Lok Sabha", "Either house", "Joint sitting"], 1, "Article 109: money bills originate only in the Lok Sabha."),
    ("The 73rd Amendment is associated with:", ["Municipalities", "Panchayati Raj", "Cooperatives", "Tribunals"], 1, "The 73rd Amendment (1992) gave constitutional status to panchayats."),
    ("Who administers the oath of office to the President?", ["Prime Minister", "Chief Justice of India", "Vice President", "Speaker"], 1, "The CJI administers the presidential oath (Article 60)."),
    ("The 'doctrine of basic structure' was laid down in which case?", ["Golaknath case", "Kesavananda Bharati case", "Minerva Mills case", "Maneka Gandhi case"], 1, "Kesavananda Bharati (1973) held Parliament cannot alter the basic structure."),
]
POLITY["advanced"] += [
    ("The Ninth Schedule was added by which amendment, and why is it famous?", ["1st Amendment; it shields land-reform laws from judicial review", "24th Amendment; it curtails property rights", "42nd Amendment; it adds duties", "44th Amendment; it restores rights"], 0, "The 1st Amendment (1951) created the Ninth Schedule to protect agrarian reform laws."),
    ("Under Article 360, a Financial Emergency has been proclaimed in India:", ["Once, in 1991", "Twice, in 1975 and 1991", "Never", "Thrice"], 2, "Article 360 has never been invoked."),
    ("The Punchhi Commission submitted its report in which year?", ["2005", "2010", "2015", "2020"], 1, "The Punchhi Commission on Centre-State relations reported in 2010."),
    ("Which amendment lowered the voting age from 21 to 18?", ["42nd", "44th", "61st", "73rd"], 2, "The 61st Amendment (1988) lowered the voting age to 18."),
    ("The office of the Leader of the Opposition was given statutory recognition in:", ["1977", "1985", "1993", "2004"], 0, "The Salary and Allowances of Leaders of Opposition Act, 1977 recognised the post."),
    ("A proclamation of National Emergency under Article 352 requires approval within:", ["14 days", "One month", "Two months", "Six months"], 1, "After the 44th Amendment, Parliament must approve it within one month."),
]

ECONOMY: Bank = {
    "beginner": [
        ("Which institution regulates monetary policy in India?", ["SEBI", "RBI", "NITI Aayog", "Ministry of Finance"], 1, "The Reserve Bank of India formulates monetary policy."),
        ("GST stands for:", ["Gross Sales Tax", "Goods and Services Tax", "General Statutory Tax", "Government Service Tax"], 1, "GST — Goods and Services Tax — came into force on 1 July 2017."),
        ("Inflation means:", ["A general rise in the price level", "A fall in GDP", "Rise in exports only", "Fall in population"], 0, "Inflation is a sustained increase in the general price level."),
        ("NITI Aayog replaced which body?", ["Finance Commission", "Planning Commission", "Law Commission", "Election Commission"], 1, "NITI Aayog replaced the Planning Commission on 1 January 2015."),
        ("The Indian rupee symbol (₹) was adopted in which year?", ["2008", "2010", "2014", "2016"], 1, "The ₹ symbol was adopted in 2010 (designed by D. Kumar)."),
        ("Which sector includes agriculture and mining?", ["Primary sector", "Secondary sector", "Tertiary sector", "Quaternary sector"], 0, "Primary sector = extraction of natural resources (agriculture, mining)."),
    ],
    "intermediate": [
        ("The repo rate is the rate at which:", ["Banks lend to customers", "RBI lends to commercial banks", "Banks lend to each other", "Government borrows from RBI"], 1, "Repo rate is RBI's lending rate to commercial banks against securities."),
        ("Which body compiles the Consumer Price Index (CPI) in India?", ["RBI", "SEBI", "National Statistical Office", "NITI Aayog"], 2, "The CPI is compiled by the NSO under the Ministry of Statistics and Programme Implementation."),
        ("Deficit financing means:", ["Financing by printing money and borrowing", "Financing through exports", "Financing through disinvestment only", "Financing by foreign aid"], 0, "Deficit financing covers the gap between revenue and expenditure through borrowing or money creation."),
        ("The First Five Year Plan (1951-56) gave priority to:", ["Heavy industry", "Agriculture", "Services", "Exports"], 1, "The First Plan focused on agriculture and irrigation (Harrod-Domar model)."),
        ("Which committee is associated with banking sector reforms in India?", ["Kelkar Committee", "Narasimham Committee", "Rangarajan Committee", "Dhananjay Ghosh Committee"], 1, "The Narasimham Committees (1991, 1998) recommended banking reforms."),
        ("Fiscal deficit is:", ["Revenue minus expenditure", "Total expenditure minus total receipts excluding borrowings", "Imports minus exports", "Interest payments minus receipts"], 1, "Fiscal deficit = total expenditure − total receipts excluding borrowings."),
    ],
    "advanced": [
        ("The Phillips Curve shows the relationship between:", ["Tax rate and tax revenue", "Inflation and unemployment", "Savings and investment", "Exports and imports"], 1, "The Phillips Curve posits an inverse short-run trade-off between inflation and unemployment."),
        ("Under India's inflation targeting framework, the RBI targets CPI inflation at:", ["2% ± 1%", "4% ± 2%", "6% ± 3%", "3% ± 1%"], 1, "The RBI must keep CPI inflation at 4% with a tolerance band of 2%-6% (2016 framework)."),
        ("Special Drawing Rights (SDR) are created by:", ["World Bank", "WTO", "IMF", "UNCTAD"], 2, "The IMF issues SDRs as a supplementary international reserve asset."),
        ("The Laffer Curve describes the relationship between:", ["Money supply and inflation", "Tax rate and tax revenue", "Interest rate and investment", "Wage rate and labour supply"], 1, "The Laffer Curve shows how tax revenue changes as tax rates rise and fall."),
        ("Which of the following is a direct tax?", ["GST", "Customs duty", "Income tax", "Excise duty"], 2, "Income tax is borne by the payer and cannot be shifted — a direct tax."),
        ("Stagflation refers to a situation of:", ["High growth with low inflation", "High inflation with stagnant output and high unemployment", "Low inflation with high growth", "Falling prices with rising output"], 1, "Stagflation = the rare combination of economic stagnation, high unemployment and high inflation."),
    ],
}

# PYQ-paper expansion (2020-2026 sets): extra practice depth per level.
ECONOMY["beginner"] += [
    ("The financial year in India runs from:", ["January to December", "April to March", "July to June", "October to September"], 1, "India's financial year runs 1 April to 31 March."),
    ("Which tax replaced most indirect taxes in 2017?", ["VAT", "GST", "Service tax", "Octroi"], 1, "GST subsumed excise, VAT, service tax and octroi from 1 July 2017."),
    ("Bank rate, CRR and SLR are instruments of:", ["Fiscal policy", "Monetary policy", "Trade policy", "Industrial policy"], 1, "RBI uses them under monetary policy to control liquidity."),
    ("Disguised unemployment is most visible in which sector?", ["Industry", "Agriculture", "Services", "Construction"], 1, "Extra hands on family farms add nothing to output - classic disguised unemployment."),
    ("The headquarters of the RBI is located in:", ["New Delhi", "Mumbai", "Kolkata", "Chennai"], 1, "RBI headquarters moved from Kolkata to Mumbai in 1937."),
    ("A rise in the repo rate generally makes loans:", ["Cheaper", "Costlier", "Free", "Unchanged"], 1, "Higher repo raises banks' borrowing costs, passed on as costlier loans."),
]
ECONOMY["intermediate"] += [
    ("The base year for the current CPI (Combined) series in India is:", ["2004-05", "2011-12", "2012", "2015"], 2, "CPI-Combined uses 2012 as the base year."),
    ("Fiscal deficit equals:", ["Total expenditure minus total receipts excluding borrowings", "Revenue deficit minus grants", "Primary deficit minus subsidies", "Budget deficit plus disinvestment"], 0, "Fiscal deficit = total expenditure - (revenue receipts + non-debt capital receipts)."),
    ("NABARD is primarily concerned with:", ["Industrial finance", "Agricultural and rural finance", "Housing finance", "Export finance"], 1, "NABARD (1982) refinances agriculture and rural development."),
    ("The SDR is the reserve asset of which institution?", ["World Bank", "IMF", "WTO", "ADB"], 1, "Special Drawing Rights are the IMF's supplementary reserve asset."),
    ("In India, devaluation of the rupee was first carried out in:", ["1947", "1949", "1966", "1991"], 1, "The rupee was devalued in September 1949 after sterling's devaluation."),
    ("The 'Laffer Curve' shows the relationship between:", ["Inflation and unemployment", "Tax rates and tax revenue", "Money supply and prices", "Wages and productivity"], 1, "The Laffer curve plots tax revenue against tax rates."),
]
ECONOMY["advanced"] += [
    ("The FRBM Act was enacted in which year, and what does it target?", ["2000; zero revenue deficit", "2003; containing fiscal deficit", "2005; bank recapitalisation", "1999; disinvestment"], 1, "FRBM (2003) mandates phased reduction of fiscal and revenue deficits."),
    ("Core inflation in India excludes which two volatile groups?", ["Food and fuel", "Housing and clothing", "Transport and health", "Education and recreation"], 0, "Core inflation = headline minus food and fuel."),
    ("The 'impossible trinity' says a country cannot simultaneously have:", ["Growth, equity and stability", "Fixed exchange rate, free capital flow and independent monetary policy", "Low inflation, low unemployment and high growth", "Surplus budget, low debt and high spending"], 1, "Mundell's trilemma: pick any two of the three."),
    ("Sterilisation by a central bank refers to:", ["Destroying soiled notes", "Offsetting forex intervention with domestic operations", "Closing weak banks", "Banning cash deals"], 1, "Sterilisation neutralises the money-supply impact of forex purchases and sales."),
    ("The Phillips Curve in its original form relates:", ["Wage growth and unemployment", "Money supply and inflation", "Interest rates and investment", "Deficits and interest rates"], 0, "Phillips (1958) linked wage inflation inversely to unemployment."),
    ("India's first Economic Survey was presented in which year?", ["1947-48", "1950-51", "1952-53", "1960-61"], 1, "The first Survey covered 1950-51, presented in 1951."),
]

CURRENT: Bank = {
    "beginner": [
        ("India's Chandrayaan-3 mission landed on the Moon in which year?", ["2019", "2021", "2023", "2024"], 2, "Chandrayaan-3 soft-landed on 23 August 2023."),
        ("The Chandrayaan-3 landing site near the lunar south pole is named:", ["Vikram Point", "Shiv Shakti Point", "Bharat Point", "Apex Point"], 1, "The site was named 'Shiv Shakti Point' (Statio Shiv Shakti)."),
        ("Which country hosted the G20 Leaders' Summit in 2023?", ["Indonesia", "Brazil", "India", "Italy"], 2, "India hosted the G20 summit in New Delhi in September 2023."),
        ("Who was the Chairman of ISRO during the Chandrayaan-3 mission?", ["K. Sivan", "S. Somanath", "R. Chidambaram", "U. R. Rao"], 1, "S. Somanath was ISRO Chairman when Chandrayaan-3 was launched and landed."),
        ("The Paris Agreement (2015) is primarily concerned with:", ["Trade tariffs", "Climate change", "Nuclear disarmament", "Maritime law"], 1, "The Paris Agreement is the global framework to limit global warming."),
        ("Which stadium hosted the 2023 Cricket World Cup final?", ["Eden Gardens", "Wankhede Stadium", "Narendra Modi Stadium, Ahmedabad", "Chepauk"], 2, "The final (19 Nov 2023) was played at the Narendra Modi Stadium in Ahmedabad."),
    ],
    "intermediate": [
        ("The G20 Leaders' Summit 2023 was held in which city?", ["Mumbai", "New Delhi", "Bengaluru", "Hyderabad"], 1, "The summit was held at Bharat Mandapam, New Delhi (9-10 September 2023)."),
        ("Which NASA mission returned samples from the asteroid Bennu in 2023?", ["OSIRIS-REx", "Hayabusa2", "DART", "Lucy"], 0, "OSIRIS-REx delivered Bennu samples to Earth in September 2023."),
        ("India's first indigenously built aircraft carrier is:", ["INS Viraat", "INS Vikramaditya", "INS Vikrant", "INS Delhi"], 2, "INS Vikrant (IAC-1) was commissioned in September 2022."),
        ("'Mission Divyastra', tested in March 2024, refers to the first test of:", ["BrahMos-II", "Agni-5 with MIRV technology", "K-4 submarine missile", "Prithvi-3"], 1, "Mission Divyastra was the first flight test of Agni-5 with Multiple Independently Targetable Re-entry Vehicles."),
        ("Which state became the first in independent India to implement a Uniform Civil Code?", ["Uttar Pradesh", "Himachal Pradesh", "Goa", "Uttarakhand"], 3, "Uttarakhand implemented the UCC in 2024 — Goa has had a common civil code since 1961."),
        ("Who won the men's singles title at Wimbledon 2023?", ["Novak Djokovic", "Daniil Medvedev", "Carlos Alcaraz", "Jannik Sinner"], 2, "Carlos Alcaraz defeated Djokovic in the 2023 Wimbledon final."),
    ],
    "advanced": [
        ("Under India's 'Panchamrit' commitments announced at COP26, the country aims for 500 GW of non-fossil energy capacity by:", ["2025", "2030", "2040", "2070"], 1, "The five pledges included 500 GW non-fossil capacity by 2030 and net zero by 2070."),
        ("ESA's JUICE mission, launched in 2023, is designed to study which planet?", ["Mars", "Jupiter", "Saturn", "Venus"], 1, "JUICE (Jupiter Icy Moons Explorer) launched in April 2023 to study Jupiter and its moons."),
        ("India's Aditya-L1 solar observatory orbits around which point?", ["Earth-Moon L2", "Sun-Earth Lagrange point L1", "Sun-Earth L4", "Mars orbit"], 1, "Aditya-L1 was placed in a halo orbit around the Sun-Earth L1 point in January 2024."),
        ("AUKUS is a security partnership between Australia, the United Kingdom and:", ["Japan", "United States", "France", "Canada"], 1, "AUKUS (2021) is a trilateral security pact between Australia, the UK and the US."),
        ("Hindenburg Research's January 2023 report targeted which Indian group?", ["Tata Group", "Reliance", "Adani Group", "Wipro"], 2, "The Hindenburg report alleged accounting fraud and stock manipulation at Adani Group companies."),
        ("Who was awarded the Nobel Peace Prize 2023?", ["Narges Mohammadi", "Volodymyr Zelensky", "UNHCR", "Ales Bialiatski"], 0, "Iranian human rights activist Narges Mohammadi won the 2023 Nobel Peace Prize."),
    ],
}

SCIENCE: Bank = {
    "beginner": [
        ("Which part of the cell is called the 'powerhouse of the cell'?", ["Nucleus", "Mitochondria", "Ribosome", "Vacuole"], 1, "Mitochondria produce ATP through cellular respiration."),
        ("Which gas is most abundant in the Earth's atmosphere?", ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], 2, "Nitrogen makes up about 78% of the atmosphere."),
        ("Which deficiency disease is caused by lack of Vitamin C?", ["Scurvy", "Rickets", "Beriberi", "Night blindness"], 0, "Vitamin C (ascorbic acid) deficiency causes scurvy."),
        ("What is the boiling point of water at sea level on the Celsius scale?", ["90°C", "100°C", "110°C", "120°C"], 1, "Water boils at 100°C at sea level."),
        ("The nearest star to the Earth is:", ["Proxima Centauri", "The Sun", "Sirius", "Alpha Centauri A"], 1, "The Sun is about 150 million km away — the nearest star."),
        ("Which instrument is used to measure atmospheric pressure?", ["Barometer", "Thermometer", "Hygrometer", "Anemometer"], 0, "A barometer measures atmospheric pressure."),
    ],
    "intermediate": [
        ("The pH value of pure water at 25°C is:", ["0", "7", "10", "14"], 1, "Pure water is neutral with pH 7."),
        ("Which blood group is called the universal donor?", ["AB positive", "A positive", "O negative", "B negative"], 2, "O negative red cells lack A, B and Rh antigens, so they can be given to anyone."),
        ("Photosynthesis in plant cells takes place in the:", ["Mitochondria", "Chloroplast", "Nucleus", "Golgi body"], 1, "Chloroplasts contain chlorophyll, which captures light energy."),
        ("The approximate speed of light in vacuum is:", ["3 × 10^6 m/s", "3 × 10^8 m/s", "3 × 10^10 m/s", "3 × 10^5 m/s"], 1, "Light travels at about 300,000 km/s = 3 × 10^8 m/s."),
        ("Which hormone regulates blood glucose levels?", ["Insulin", "Adrenaline", "Thyroxine", "Testosterone"], 0, "Insulin, secreted by the pancreas, lowers blood glucose."),
        ("The chemical formula of common salt is:", ["KCl", "NaCl", "CaCO3", "NaOH"], 1, "Common salt is sodium chloride (NaCl)."),
    ],
    "advanced": [
        ("The approximate half-life of Carbon-14 is:", ["5,730 years", "4.5 billion years", "365 days", "100 years"], 0, "Carbon-14's half-life is about 5,730 years — the basis of radiocarbon dating."),
        ("Which of the following vitamins is fat-soluble?", ["Vitamin C", "Vitamin D", "Vitamin B12", "Vitamin B6"], 1, "Vitamins A, D, E and K are fat-soluble."),
        ("The chemical name of Vitamin C is:", ["Retinol", "Ascorbic acid", "Folic acid", "Thiamine"], 1, "Vitamin C is ascorbic acid; retinol is Vitamin A and thiamine is B1."),
        ("A dynamo converts:", ["Electrical energy into mechanical energy", "Mechanical energy into electrical energy", "Heat energy into chemical energy", "Chemical energy into heat energy"], 1, "A dynamo/generator converts mechanical energy into electrical energy."),
        ("Newton's first law of motion is also called the:", ["Law of acceleration", "Law of inertia", "Law of action-reaction", "Law of gravitation"], 1, "The first law — a body stays at rest or in uniform motion unless acted on by an external force — is the law of inertia."),
        ("Which type of radiation has the highest penetrating power?", ["Alpha rays", "Beta rays", "X-rays", "Gamma rays"], 3, "Gamma rays penetrate the deepest because they have the shortest wavelength and no charge."),
    ],
}

# PYQ-paper expansion (2020-2026 sets): extra practice depth per level.
SCIENCE["beginner"] += [
    ("The chemical symbol for gold is:", ["Go", "Gd", "Au", "Ag"], 2, "Gold's symbol Au comes from Latin 'aurum'."),
    ("The hardest natural substance on Earth is:", ["Iron", "Quartz", "Diamond", "Granite"], 2, "Diamond tops the Mohs scale at 10."),
    ("Which gas do plants absorb for photosynthesis?", ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], 2, "Plants take in carbon dioxide and release oxygen."),
    ("The SI unit of electric current is:", ["Volt", "Ampere", "Ohm", "Watt"], 1, "Current is measured in amperes."),
    ("Which part of the human cell contains genetic material?", ["Ribosome", "Nucleus", "Cytoplasm", "Membrane"], 1, "DNA is stored in the nucleus."),
    ("Water boils at 100 degrees Celsius at:", ["Sea level", "Mountain tops", "Deep mines", "High pressure chambers"], 0, "At sea-level pressure, water boils at 100 degrees C."),
]
SCIENCE["intermediate"] += [
    ("The pH of human blood is approximately:", ["6.4", "7.4", "8.4", "5.4"], 1, "Blood is slightly alkaline at about 7.4."),
    ("Which law states that voltage equals current times resistance?", ["Faraday's law", "Ohm's law", "Newton's law", "Boyle's law"], 1, "V = IR is Ohm's law."),
    ("Photosynthesis releases which gas as a byproduct?", ["Carbon dioxide", "Oxygen", "Nitrogen", "Methane"], 1, "Splitting water releases oxygen."),
    ("The functional unit of the kidney is:", ["Neuron", "Nephron", "Alveolus", "Glomerulus alone"], 1, "Each kidney has about a million nephrons that filter blood."),
    ("Which vitamin is synthesised in the skin by sunlight?", ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin K"], 2, "UV-B converts cholesterol in skin to vitamin D."),
    ("An object floats when its density is:", ["Greater than the fluid", "Less than the fluid", "Equal to zero", "Infinite"], 1, "Lower density than the fluid lets buoyancy win."),
]
SCIENCE["advanced"] += [
    ("The particles called mesons are made of:", ["Three quarks", "A quark-antiquark pair", "Two protons", "Gluons only"], 1, "Mesons = quark + antiquark; baryons = three quarks."),
    ("CRISPR-Cas9 is primarily a tool for:", ["Gene editing", "Blood typing", "X-ray imaging", "Vaccine storage"], 0, "CRISPR-Cas9 cuts DNA at targeted spots for editing."),
    ("The Heisenberg uncertainty principle relates:", ["Energy and time only", "Position and momentum", "Mass and charge", "Speed and distance"], 1, "You cannot know both position and momentum exactly at once."),
    ("Superconductivity was first observed in which element?", ["Copper", "Mercury", "Lead", "Aluminium"], 1, "Onnes found mercury loses resistance near absolute zero (1911)."),
    ("The ozone layer absorbs mainly which radiation?", ["Infrared", "Ultraviolet", "X-rays", "Radio waves"], 1, "Ozone absorbs harmful UV-B and UV-C."),
    ("Mitochondrial DNA in humans is inherited:", ["From the father only", "From the mother only", "Equally from both parents", "From neither parent"], 1, "Mitochondria come almost entirely from the egg - maternal inheritance."),
]


def get_ga(topic_slug: str, difficulty: str) -> list[QuestionDict]:
    bank: Bank = {
        "history": HISTORY,
        "geography": GEOGRAPHY,
        "polity": POLITY,
        "economy": ECONOMY,
        "current-affairs": CURRENT,
        "science": SCIENCE,
    }[topic_slug]
    return [
        {"question_text": q, "options": list(opts), "correct_index": idx, "explanation": expl, "difficulty": difficulty}
        for q, opts, idx, expl in bank[difficulty]
    ]
