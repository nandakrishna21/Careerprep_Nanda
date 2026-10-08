"""Career path course definitions: 9 role-based paths x 4 topics x 1 lesson each."""
from __future__ import annotations

CAREER_PATHS: list[dict] = [
    {
        "title": "Python Developer",
        "slug": "python-developer",
        "icon": "code",
        "level": "Beginner",
        "description": "Build real Python programs from core syntax to packaged, tested applications. You finish able to write clean scripts, talk to databases, and defend your code in a technical interview.",
        "topics": [
            {
                "title": "Python Core",
                "slug": "path-python-core",
                "description": "Master the data structures, functions and idioms that make Python code readable and efficient.",
                "lesson": {
                    "title": "Python Core — Lesson",
                    "notes": "Python's power comes from a small set of core data structures and the habits that keep them readable. Start with the distinction between mutable and immutable types: lists and dicts change in place, while strings, tuples and integers do not. Use a tuple for a fixed collection and a list when you need to append, sort or reorder.\n\n- Prefer list comprehensions for simple transformations, but fall back to a plain loop when a condition is combined with nesting — clarity beats cleverness.\n- Dictionaries preserve insertion order from Python 3.7 onwards. Use dict.get(key, default) instead of catching KeyError.\n- Unpack with * and ** when forwarding arguments: def wrapper(*args, **kwargs).\n- Naming: snake_case for functions and variables, UPPER_CASE for module-level constants, PascalCase for classes.\n\nThree bugs cause most beginner pain: a mutable default argument such as def add(item, bucket=[]), which shares one list across every call; mutating a list while iterating over it, which silently skips elements; and using is for value comparison instead of ==.\n\nBuild muscle memory by rewriting one small script twice — once with comprehensions and once with explicit loops — then run python -m trace --count script.py to see exactly which lines executed and how often.",
                    "examples": [
                        "Shared mutable default argument — use bucket=None inside the function and create a fresh list",
                        "Skipping list items while deleting — iterate over a reversed copy or build a new filtered list",
                    ],
                    "practice": [
                        "Write a function that groups a list of words by their first letter and returns a dict of sorted lists.",
                        "Explain the difference between == and is, then give one case where they give different results.",
                        "Rewrite a nested for-loop filter as a single list comprehension with one condition.",
                    ],
                },
            },
            {
                "title": "Python and Databases",
                "slug": "path-python-databases",
                "description": "Connect Python to SQL databases safely with drivers, parameterised queries and simple data layers.",
                "lesson": {
                    "title": "Python and Databases — Lesson",
                    "notes": "Almost every backend role expects you to read and write rows from Python. The standard library ships sqlite3, which is perfect for learning; production code usually swaps in psycopg2 for PostgreSQL or pymysql for MySQL. The API is nearly identical: open a connection, create a cursor, execute SQL, fetch results, commit, close.\n\n- Never build SQL with f-strings. Always parameterise: cursor.execute('SELECT * FROM users WHERE email = %s', (email,)). Placeholders differ by driver: ? for sqlite3, %s for psycopg2.\n- Use a context manager or try/finally so connections close even on error. Forgetting to commit is the classic lost-write bug.\n- Keep SQL out of view functions. Wrap it in a small data layer so queries are testable in isolation.\n- Choose consciously between raw SQL and an ORM: SQL teaches you indexes and joins, an ORM saves time on CRUD-heavy apps.\n\nKnow the four transaction properties (ACID) and when to set isolation level. For long-running read work, use a read-only connection or a replica so you do not hold locks.\n\nWatch for the N+1 pattern: a loop that issues one query per iteration. Replace it with a single query using WHERE id = ANY(%s) or a JOIN, then measure with logging before and after.",
                    "examples": [
                        "SQL injection via string formatting — switch to parameterised execute so the driver escapes input",
                        "N+1 queries in a loop — fetch all related rows in one query and group them in Python",
                    ],
                    "practice": [
                        "Write a function that upserts a user row using INSERT ... ON CONFLICT for SQLite.",
                        "Add connection pooling to a small Flask or FastAPI app and explain why pooling helps.",
                        "Refactor a loop of single-row SELECTs into one query plus a dict grouping step.",
                    ],
                },
            },
            {
                "title": "Testing and Packaging",
                "slug": "path-testing-packaging",
                "description": "Write pytest suites that catch regressions and ship your code as an installable package.",
                "lesson": {
                    "title": "Testing and Packaging — Lesson",
                    "notes": "Employers trust code that proves itself. Pytest is the default: discoverable test functions, expressive asserts, and fixtures that remove setup duplication. Name tests test_behaviour_when_condition so a failure message reads like a bug report.\n\n- Cover the happy path, one boundary (empty input, zero, maximum) and one error path per function.\n- Use fixtures for databases or HTTP clients, and monkeypatch to replace network calls — tests must never hit the internet.\n- Parameterise repeated cases with @pytest.mark.parametrize instead of copying test bodies.\n- Assert on behaviour, not on implementation details; tests coupled to internals break on every refactor.\n\nAim for fast, deterministic suites: every test should run in milliseconds and produce the same result twice. Add coverage reporting to see untested branches, but treat the percentage as a map, not a scoreboard.\n\nPackaging turns your script into something others can install. Define metadata and dependencies in pyproject.toml, keep a src/ layout so tests import the packaged version, and build with python -m build to produce a wheel. Use semantic versioning, tag releases in git, and publish with twine. Run the suite in CI on every push so a broken main branch is impossible to ignore.",
                    "examples": [
                        "Slow tests that call a paid API — inject a fake client fixture and monkeypatch the request function",
                        "Works on my machine only — declare dependencies in pyproject.toml and install the built wheel in a clean venv",
                    ],
                    "practice": [
                        "Add parametrised tests for a parse_date function covering valid, leap-day and invalid inputs.",
                        "Convert a plain script into a package with pyproject.toml and a src layout, then build a wheel.",
                        "Write a test that forces a function to raise and assert the exact exception type and message.",
                    ],
                },
            },
            {
                "title": "Python Interview Prep",
                "slug": "path-python-interview",
                "description": "Practise the coding questions, complexity talk and language deep-dives that Python interviews actually ask.",
                "lesson": {
                    "title": "Python Interview Prep — Lesson",
                    "notes": "Python interviews test reasoning more than memorisation. Approach each problem the same way: restate it, ask about constraints and edge cases, propose a naive solution, analyse its complexity, then optimise. Say your thinking out loud — an interviewer can only grade what they hear.\n\n- Memorise the cost of core operations: list append is O(1), insert or pop at index 0 is O(n), dict lookup is O(1) average, sorting is O(n log n).\n- Know the two-pointer pattern for pair sums and palindromes, sliding window for subarrays, and a hash map for frequency counting.\n- Generators with yield keep memory flat on large inputs; itertools.chain and collections.Counter are rarely penalised, but explain what you use.\n- Be ready for language questions: name versus reference semantics, how MRO works, what a decorator does, GIL implications, and the difference between a list and a generator.\n\nPractise writing on a shared editor without running code. Common follow-ups are: can you do it in one pass, can you reduce space to O(1), what happens if the input is a stream. Close by testing your solution with an empty input, duplicates and a sorted-versus-unsorted case, then state the time and space complexity of the final version.",
                    "examples": [
                        "Two-sum runs in O(n squared) with nested loops — a dict of seen values gives O(n) in one pass",
                        "Loading a huge file into a list exhausts memory — yield lines from a generator and stream instead",
                    ],
                    "practice": [
                        "Solve group anagrams and narrate the complexity out loud as you code it.",
                        "Explain the GIL in two sentences and give one workload where multiprocessing beats threading.",
                        "Write a decorator that retries a function three times on exception and add two tests for it.",
                    ],
                },
            },
        ],
    },
    {
        "title": "Backend Developer",
        "slug": "backend-developer",
        "icon": "server",
        "level": "Intermediate",
        "description": "Design and ship production HTTP APIs with FastAPI, well-modelled databases and sane security. You finish able to take an endpoint from openapi sketch to a measured, hardened service.",
        "topics": [
            {
                "title": "REST API Design",
                "slug": "path-rest-api-design",
                "description": "Model resources, verbs, status codes and pagination so your API is predictable for any client.",
                "lesson": {
                    "title": "REST API Design — Lesson",
                    "notes": "A good REST API looks boring: nouns in the path, verbs in the HTTP method, and status codes that tell the truth. Model resources, not actions. /orders/42 is a resource; /getOrder is a procedure wearing a REST costume.\n\n- Use GET for reads, POST for creation, PUT for full replacement, PATCH for partial update, DELETE for removal. GET, PUT and DELETE must be idempotent so a retried request is harmless.\n- Status codes are an API contract: 200 OK, 201 Created with a Location header, 204 No Content, 400 malformed input, 401 unauthenticated, 403 unauthorised, 404 missing, 409 conflict, 422 validation failure, 429 rate limited, 500 unexpected.\n- Return a consistent error body such as {code, message, details} so clients can branch without parsing prose.\n- Always paginate list endpoints with cursor or keyset pagination; offset pagination drifts when rows are inserted.\n- Version in the path (/v1/...) and document every change. Support filtering, sorting and field selection with query parameters.\n\nDesign the contract first: write the openapi spec or examples, review them with the consumer team, then implement. An API is easy to add to and painful to remove from, so avoid leaking database columns directly in responses.",
                    "examples": [
                        "POST /deleteOrder for an action — move to DELETE /orders/{id} so caching and retries behave",
                        "Endpoint returns 200 with an error string — return 422 with a structured validation payload",
                    ],
                    "practice": [
                        "Design endpoints and status codes for a library system with borrowing and returning books.",
                        "Specify a cursor pagination response shape including next_cursor and has_more fields.",
                        "List five rules you would check in an API design review and justify each one.",
                    ],
                },
            },
            {
                "title": "FastAPI Mastery",
                "slug": "path-fastapi-mastery",
                "description": "Use Pydantic validation, dependency injection and async handlers to build typed, testable services.",
                "lesson": {
                    "title": "FastAPI Mastery — Lesson",
                    "notes": "FastAPI's leverage comes from types. Declare a Pydantic model for every request body and response, and the framework validates input, generates documentation and produces typed client SDKs for free. Keep domain models and API schemas separate: an internal User row and a public UserOut rarely share every field.\n\n- Path and query parameters are typed the same way: def read(user_id: int, limit: int = 20).\n- Dependency injection with Depends() is where FastAPI shines. Put database sessions, current-user checks and feature flags in dependencies so handlers stay thin and tests can override them with app.dependency_overrides.\n- Use APIRouter to split large apps into modules, and include_router with a prefix and tags.\n- Async handlers help when awaiting I/O, but never call blocking libraries inside them — that stalls the whole event loop. Run CPU-bound work in a thread pool or a background queue.\n- Add lifespan handlers for startup and shutdown to open pools and warm caches. Use BackgroundTasks for fire-and-forget work such as sending email.\n\nGenerate pydantic v2 validators for cross-field rules, raise HTTPException with precise status codes, and let the auto-generated /docs page become your living contract. Version your models with model_config = ConfigDict(extra='forbid') to reject unknown fields early.",
                    "examples": [
                        "Handler repeats auth and DB setup — extract a get_current_user dependency and reuse it with Depends",
                        "Blocking PDF generation freezes the loop — move it to run_in_threadpool or a worker queue",
                    ],
                    "practice": [
                        "Build a /items router with GET, POST and PATCH and override its DB dependency in tests.",
                        "Add a Pydantic validator that rejects a date_to earlier than date_from.",
                        "Write an async endpoint that fetches two URLs concurrently and compare it with a sequential version.",
                    ],
                },
            },
            {
                "title": "Data Modelling and SQL",
                "slug": "path-data-modelling-sql",
                "description": "Design normalised schemas, choose keys and indexes, and write joins that stay fast as data grows.",
                "lesson": {
                    "title": "Data Modelling and SQL — Lesson",
                    "notes": "Schema design decides how painful your API feels in year two. Start from the questions the product asks, not from the tables. Identify entities, relationships and cardinality: one user has many orders, one order has many line items. Then normalise — remove repeating groups and transitive dependencies until each fact lives in one place — usually to third normal form for transactional systems.\n\n- Choose primary keys deliberately: a monotonic bigint for joins, plus a public UUID if you expose identifiers to clients.\n- Foreign keys are not optional. Without them, orphan rows accumulate and joins silently drop data.\n- Index the columns used in WHERE, JOIN and ORDER BY. An index that is never used still costs writes, so verify with EXPLAIN ANALYZE.\n- Model many-to-many with a junction table that carries its own attributes, such as membership date.\n- Prefer explicit migrations (Alembic or similar) over auto-created tables so schema changes are reviewable and reversible.\n\nDenormalise only when measurement demands it, and keep a single source of truth. Understand isolation levels enough to explain dirty reads and lost updates, and wrap multi-statement changes in a transaction. Practise joins daily: INNER for overlap, LEFT for optional children, and aggregations with GROUP BY and HAVING for reports.",
                    "examples": [
                        "Store tags as a comma string — split into a tags table plus a post_tags junction table",
                        "Slow LIKE '%term%' search — add an index or use a trigram/FTS index for substring queries",
                    ],
                    "practice": [
                        "Draw an ERD for a course platform with users, courses, enrollments and lessons, then write the DDL.",
                        "Write a query returning each student's enrolment count using LEFT JOIN so zero-count students appear.",
                        "Run EXPLAIN on a slow query and identify one missing index to add.",
                    ],
                },
            },
            {
                "title": "API Security and Performance",
                "slug": "path-api-security-performance",
                "description": "Authenticate callers correctly, defend against common attacks, and make endpoints fast under load.",
                "lesson": {
                    "title": "API Security and Performance — Lesson",
                    "notes": "Security is a checklist you must pass, not a feature you bolt on. Authenticate with short-lived access tokens (JWT or opaque) plus refresh tokens stored httpOnly and Secure; authorise every request against the resource owner, not just the route. Hash passwords with bcrypt or argon2 — never MD5 or SHA-256 alone.\n\n- Parameterise all SQL, escape output to stop XSS, and use CSRF tokens for cookie-authenticated state changes.\n- Validate and cap request body size, add per-user rate limiting, and log auth failures without recording secrets.\n- Keep secrets in environment variables or a vault, rotate them, and never commit .env files.\n- Ship TLS only, set HSTS, and restrict CORS to explicit origins.\n\nPerformance work starts with measurement. Capture a baseline with a load tool, find the slowest endpoint, and look for the usual suspects: N+1 queries, missing indexes, unbounded result sets, and repeated serialization of large payloads. Add caching at the right layer — in-process for rarely changing data, Redis for shared hot keys — and set explicit TTLs plus invalidation on writes. Batch work into bulk inserts, paginate aggressively, add timeouts and circuit breakers so one slow dependency cannot exhaust your worker pool, and monitor p95 latency rather than averages.",
                    "examples": [
                        "Plaintext password column — rehash with bcrypt and add a one-time migration that upgrades on next login",
                        "Endpoint p95 of two seconds due to N+1 — batch fetch with one IN query and cut it to 120 ms",
                    ],
                    "practice": [
                        "Implement JWT access plus refresh token flow and explain why refresh tokens need rotation.",
                        "Find and fix an IDOR bug where /orders/{id} returns other users' rows.",
                        "Profile a slow endpoint, name the bottleneck, and write down the fix with its expected gain.",
                    ],
                },
            },
        ],
    },
    {
        "title": "Frontend Developer",
        "slug": "frontend-developer",
        "icon": "layout",
        "level": "Beginner",
        "description": "Turn designs into fast, accessible interfaces with semantic markup, modern JavaScript and React. You finish able to build responsive pages that work on real devices for real users.",
        "topics": [
            {
                "title": "Semantic HTML and CSS",
                "slug": "path-semantic-html-css",
                "description": "Structure pages with meaningful elements and lay them out with modern, resilient CSS.",
                "lesson": {
                    "title": "Semantic HTML and CSS — Lesson",
                    "notes": "Browsers, screen readers and search engines all read your HTML before any framework does. Choose elements for meaning: header, nav, main, article, section, footer, plus button for actions and a for-linked label for inputs. A div soup page can look perfect and still fail accessibility audits.\n\n- One h1 per page, then h2 and h3 without skipping levels — heading order is how assistive tech builds an outline.\n- Link real navigation with a href; use button for JavaScript actions. Always give img an alt, or alt=\"\" when purely decorative.\n- CSS layout today is flexbox for one-dimensional rows and grid for two-dimensional pages. Learn minmax(), auto-fit and the fr unit before reaching for a framework.\n- Style with a small token set: custom properties for colour, spacing and radius, then compose them.\n- Mobile first: base styles for small screens, then min-width media queries to enhance. Use clamp() for fluid type.\n- Focus states must be visible. Remove outline only if you replace it with a clearly stronger indicator.\n\nMeasure with Lighthouse: aim for a good CLS by reserving space for images and fonts, and avoid layout that shifts when web fonts swap. Validate structure with the WAVE extension and test keyboard-only navigation — if you cannot reach a control with Tab, neither can your users.",
                    "examples": [
                        "Click handler on a clickable div — replace with a button so keyboard and screen reader users can activate it",
                        "Centering fights with floats — rewrite the section with CSS grid and gap instead",
                    ],
                    "practice": [
                        "Rebuild a blog page using only semantic elements and verify its outline in a screen reader.",
                        "Create a responsive card grid that goes from one to three columns without media queries using auto-fit.",
                        "Audit a page with WAVE and fix every contrast and missing-label issue you find.",
                    ],
                },
            },
            {
                "title": "Modern JavaScript",
                "slug": "path-modern-javascript",
                "description": "Use ES6+ syntax, async control flow and browser APIs to write concise, correct client-side code.",
                "lesson": {
                    "title": "Modern JavaScript — Lesson",
                    "notes": "Modern JavaScript is small, expressive and asynchronous at its core. Comfort with a handful of features separates a productive frontend developer from someone copying snippets.\n\n- Declare with const by default and let for rebinding; never var. Block scope prevents a whole class of leaks.\n- Destructure and spread for clean data handling: const {name, age} = user; const next = {...old, age: 1}.\n- Arrow functions inherit this, which is why they shine inside classes and callbacks, but avoid them for object methods that need their own this.\n- Promises: async/await with try/catch reads like synchronous code. Always await inside loops when order matters, and use Promise.all for independent parallel requests.\n- fetch does not reject on 404 or 500 — check response.ok yourself before reading the body.\n- Closures power data privacy and factory functions; remember a closure captures variables, not values.\n\nModules via import and export keep code split by responsibility. On the DOM, use querySelector, addEventListener and event delegation for lists. Handle errors deliberately: wrap network calls, show a retry affordance, and never leave a floating unhandled rejection. Build a habit of testing in dev tools with throttled 3G and offline mode — most real bugs are network and timing bugs, not syntax errors.",
                    "examples": [
                        "Loop variable shared with a delayed callback — wrap the body in a function or use let to capture per iteration",
                        "fetch returns 500 but code continues — guard with if (!response.ok) and throw a typed error",
                    ],
                    "practice": [
                        "Fetch a JSON API, handle loading, error and empty states, and render the results.",
                        "Explain closures with a counter factory and then rewrite it using module scope instead.",
                        "Use event delegation to handle clicks on a list of 1 000 rows with one listener.",
                    ],
                },
            },
            {
                "title": "React Patterns",
                "slug": "path-react-patterns",
                "description": "Compose components, manage state and reuse logic with hooks without creating unnecessary re-renders.",
                "lesson": {
                    "title": "React Patterns — Lesson",
                    "notes": "React rewards a simple model: state is the source of truth, props flow down, events flow up. Keep components small and derive values during render instead of mirroring the same data into another state variable.\n\n- Lift state up to the nearest common ancestor when two siblings need it, or reach for a shared context for truly global data.\n- Keys in lists must be stable and unique — array indexes break reconciliation when items reorder.\n- Custom hooks are the unit of reuse: extract useFetch(url) or useDebounced(value) rather than copying effects.\n- Effects are for synchronising with systems outside React (subscriptions, timers, DOM). For derived data, compute it in the component body.\n- Avoid premature optimisation; measure with the React DevTools Profiler before adding memo or useMemo.\n- Uncontrolled inputs with refs are fine for forms; controlled components win when you need instant validation.\n\nKeep data flow debuggable: one-way updates, a single place where mutations happen, and early returns for loading and error states. Prefer composition over configuration — children and render props beat a component with twenty boolean props. Co-locate styles with the component, keep business logic out of JSX, and write at least one test per component with React Testing Library that queries by role and text, never by internal implementation.",
                    "examples": [
                        "List reorders badly because keys are indexes — key by the record id instead",
                        "Duplicate state mirrors a prop — delete the copy and derive the value during render",
                    ],
                    "practice": [
                        "Build an autocomplete with a debounced custom hook and full keyboard navigation.",
                        "Refactor two sibling components to share filter state by lifting it to their parent.",
                        "Profile a slow list render and justify, with numbers, whether memo is worth keeping.",
                    ],
                },
            },
            {
                "title": "UI Engineering with Tailwind",
                "slug": "path-tailwind-ui",
                "description": "Build consistent, responsive and accessible interfaces quickly with a utility-first design system.",
                "lesson": {
                    "title": "UI Engineering with Tailwind — Lesson",
                    "notes": "Tailwind's value is not that utilities are fashionable; it is that design decisions become visible in the markup and consistent across the team. Treat your config as a design system: define brand colours, a spacing scale, font sizes and radii once, then compose with the same handful of tokens everywhere.\n\n- Mobile first, then sm:, md:, lg: for larger screens. Prefer grid-cols-1 md:grid-cols-3 over custom CSS for layout shifts.\n- Use the design scale for spacing (p-4, gap-6) rather than magic pixel values; visual rhythm comes from restraint.\n- Extract repeated clusters with @apply sparingly or, better, with a small React component like Card or Button. Utilities in JSX are fine; forty classes in one className are not.\n- Build states deliberately: hover, focus-visible, disabled, loading and error. Never ship hover-only interactions on touch devices.\n- Handle dark mode with a class strategy and semantic colour names such as bg-surface and text-muted so themes swap cleanly.\n- Accessibility is part of the UI: contrast ratios, focus rings, aria-labels on icon-only buttons, and a logical tab order.\n\nWork from a reference screen at 1440, 768 and 375 pixels, and check long text wrapping, empty states and loading skeletons. Keep the bundle honest by scanning for unused utilities in the content configuration.",
                    "examples": [
                        "Buttons drift across pages because each dev picked hex codes — centralise brand colours in the Tailwind theme",
                        "Icon button is unlabelled — add aria-label and a visible focus ring with focus-visible:ring-2",
                    ],
                    "practice": [
                        "Implement a responsive navbar that collapses to a menu at the md breakpoint.",
                        "Create a reusable Card component with default, hover and loading states.",
                        "Run a contrast check on your palette and replace every pair below 4.5:1 for body text.",
                    ],
                },
            },
        ],
    },
    {
        "title": "Full Stack Developer",
        "slug": "fullstack-developer",
        "icon": "layers",
        "level": "Intermediate",
        "description": "Own a feature end to end: interface, API, database and deployment. You finish able to ship a small product yourself, from first commit to a live URL.",
        "topics": [
            {
                "title": "Frontend Foundations",
                "slug": "path-frontend-foundations",
                "description": "Build accessible, responsive interfaces and connect them to real APIs with clean state handling.",
                "lesson": {
                    "title": "Frontend Foundations — Lesson",
                    "notes": "A full stack developer's frontend work must be dependable rather than flashy. Start with structure: semantic HTML, a small CSS system built on custom properties, and layout with flexbox and grid. Design mobile first so the base experience is the constrained one, then enhance upward.\n\n- Componentise by responsibility. A page composes Header, Form and List; each owns one concern and receives data via props.\n- Model every remote interaction as three states: loading, success and error. Render skeletons for loading, a retry button for errors, and an explicit empty state when the list is legitimately blank.\n- Keep a single place where server state lives — a fetch layer or a library such as React Query — rather than scattering fetch calls through components.\n- Handle forms with client-side validation for speed and server-side validation for truth; show field-level errors next to inputs.\n- Optimise images with modern formats and explicit dimensions, lazy-load below-the-fold content, and code-split routes so the first paint stays small.\n\nAccessibility and performance are the same conversation: fewer elements, clear focus order, and alt text. Test on a slow device and a real keyboard. Finally, instrument what users feel — track interaction latency and error rates — because a feature nobody can use on 3G is not finished.",
                    "examples": [
                        "Button stays enabled during submit and creates duplicates — disable it and show an inline spinner state",
                        "Page flashes empty on load — render a skeleton until data resolves instead of an empty list",
                    ],
                    "practice": [
                        "Build a paginated list page with loading, error, empty and retry states wired to a real API.",
                        "Convert a pixel-perfect desktop layout into a responsive one using grid and clamp for type.",
                        "Audit a route bundle and split it so the initial download drops by at least a third.",
                    ],
                },
            },
            {
                "title": "Backend Foundations",
                "slug": "path-backend-foundations",
                "description": "Serve typed HTTP APIs with authentication, validation and a clean layering of routes, services and storage.",
                "lesson": {
                    "title": "Backend Foundations — Lesson",
                    "notes": "The backend is a contract plus the machinery behind it. Layer the code so each part can change independently: routes parse and validate input, services hold business rules, and repositories touch the database. Handlers that do all three become impossible to test.\n\n- Validate everything at the boundary with typed schemas — reject unknown fields and return structured 422 errors.\n- Authenticate with tokens, then authorise per resource: checking that a route requires login is not enough, you must check the row belongs to the caller.\n- Make writes idempotent where possible by accepting an idempotency key, so network retries do not duplicate orders.\n- Standardise cross-cutting concerns with middleware: request ids, structured logs, timeouts, and consistent error envelopes.\n- Return pagination by default. Unbounded queries become outages.\n- Keep configuration in the environment and read it once at startup; fail fast if a required variable is missing.\n\nDesign the happy path first, then the failure paths: not found, conflict, unauthorized, downstream timeout. Write an integration test that boots the app against a real database in a container and exercises the full flow. Observability is part of the foundation — log the request id, the duration and the outcome so an on-call engineer can reconstruct a request without guessing.",
                    "examples": [
                        "One 400-line route function — split into validate, service call and repository call layers",
                        "Auth check only on the route, not the row — add an ownership test that must fail before the fix",
                    ],
                    "practice": [
                        "Build a CRUD API with layered code, structured error handling and a request-id middleware.",
                        "Add an integration test that runs against a throwaway Postgres container.",
                        "Write a small design note for how you would version and deprecate an existing endpoint.",
                    ],
                },
            },
            {
                "title": "Database Design",
                "slug": "path-database-design",
                "description": "Model entities and relationships, migrate safely, and keep queries fast with the right indexes.",
                "lesson": {
                    "title": "Database Design — Lesson",
                    "notes": "Good schema design is the cheapest performance win available. Begin with a domain sketch: nouns become tables, verbs become relationships, and cardinality decides where foreign keys live. Normalise transactional data so each fact has one home, then denormalise only where measurements justify it.\n\n- Pick a boring, stable primary key and expose a public identifier separately if needed.\n- Add foreign keys and let the database enforce them; application-level checks drift over time.\n- Junction tables for many-to-many, with their own columns for attributes like joined_at.\n- Index what you filter, join and sort. Verify with EXPLAIN ANALYZE rather than intuition, and drop indexes that never appear.\n- Timestamps for created_at and updated_at on nearly every table make debugging and audits far easier.\n- Evolve the schema with versioned, reversible migrations reviewed like code. Never let an ORM auto-mutate production.\n\nUnderstand transactions well enough to reason about concurrency: choose isolation levels deliberately, keep transactions short, and know that long transactions block vacuuming and replication. Watch for the N+1 query in application code, which no index will fix. Practise with realistic data volumes — generate a million rows and repeat your queries, because behaviour at ten rows and behaviour at ten million are different problems.",
                    "examples": [
                        "Storing comma-separated tags — replace with a tags table and a junction table for clean filtering",
                        "Sequential scan on a huge table — add a composite index matching the WHERE and ORDER BY columns",
                    ],
                    "practice": [
                        "Design and migrate a schema for a marketplace with users, products, orders and line items.",
                        "Write a migration that adds a non-null column with a backfill without locking the table for long.",
                        "Take a slow query, capture its plan before and after indexing, and record the timing change.",
                    ],
                },
            },
            {
                "title": "Ship and Deploy",
                "slug": "path-ship-deploy",
                "description": "Take code from commit to production with CI, container builds, environments and safe releases.",
                "lesson": {
                    "title": "Ship and Deploy — Lesson",
                    "notes": "Shipping is a skill separate from coding. A deployment pipeline turns releases into routine events instead of ceremonies. Start with CI: install dependencies, lint, type-check and run tests on every push, and block merges when any step fails.\n\n- Keep environments consistent: the same container image runs in staging and production, differing only by configuration.\n- Build a multi-stage Dockerfile so the runtime image contains the app, not compilers and caches. Run as a non-root user.\n- Store secrets in your platform's secret manager, inject them at runtime, and never bake them into images.\n- Prefer migrations that run as a separate, ordered step before the new code starts, and make them backwards compatible so old and new versions can coexist during a rollout.\n- Release with zero downtime: rolling or blue-green deploys, a health check endpoint, and automatic rollback when error rates spike.\n- Use preview environments per pull request so reviewers can click the change instead of imagining it.\n\nMeasure what you ship. Track deploy frequency, lead time, change failure rate and time to restore. Keep a rollback rehearsed and cheap, log with request ids across services, and write the release note before merging — if you cannot describe the change and its risk, you are not ready to deploy it.",
                    "examples": [
                        "Image is two gigabytes because dev dependencies are bundled — multi-stage build cuts it to 90 MB",
                        "Migration drops a column and breaks the running app — expand, migrate, then contract across releases",
                    ],
                    "practice": [
                        "Write a CI workflow that lints, tests and builds a Docker image on every pull request.",
                        "Add a health check endpoint and configure a deploy to roll back when it fails.",
                        "Draft a release checklist covering migrations, secrets, monitoring and rollback.",
                    ],
                },
            },
        ],
    },
    {
        "title": "Data Analyst",
        "slug": "data-analyst",
        "icon": "bar-chart-2",
        "level": "Beginner",
        "description": "Answer business questions with SQL, clean Python datasets and visuals that stakeholders trust. You finish able to take a vague request and deliver a defensible number with a chart.",
        "topics": [
            {
                "title": "SQL for Analysis",
                "slug": "path-sql-analysis",
                "description": "Use joins, window functions and CTEs to turn raw tables into metrics leadership can act on.",
                "lesson": {
                    "title": "SQL for Analysis — Lesson",
                    "notes": "SQL is the analyst's primary tool because the data already lives in the database and moving it elsewhere loses fidelity. Move beyond WHERE and GROUP BY into the structures real reporting needs.\n\n- Chain logic with CTEs (WITH) so each step of a calculation is named and readable instead of nested subqueries.\n- Join deliberately: INNER for intersection, LEFT to keep unmatched rows, and always check join cardinality — a fan-out join silently inflates revenue totals.\n- Window functions answer ranking and trend questions: ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at), running totals with SUM() OVER (...), and lag for period-over-period deltas.\n- Aggregate correctly with COUNT(*), COUNT(DISTINCT id), and NULL-safe handling via COALESCE.\n- Filter groups with HAVING, not WHERE, and format dates with the dialect's functions for weekly bucketing.\n\nAccuracy matters more than cleverness. Define each metric precisely — does revenue include refunds, is a active user daily or monthly — and write the definition next to the query. Handle late-arriving data and time zones explicitly, always filtering on a timestamp range in UTC. Save queries as version-controlled views so colleagues reuse the same definition rather than forking slightly different numbers. Validate a result with a second, simpler query before you present it.",
                    "examples": [
                        "Totals double after a join to a one-to-many table — aggregate the child side first or use DISTINCT",
                        "Month-over-month growth — use lag(revenue) OVER (ORDER BY month) in a CTE and compute the delta",
                    ],
                    "practice": [
                        "Write a CTE-based query for monthly revenue by product category with MoM percentage change.",
                        "Rank the top 3 products per category using a window function.",
                        "Explain, with an example, how a many-to-many join can silently duplicate rows.",
                    ],
                },
            },
            {
                "title": "Data Cleaning in Python",
                "slug": "path-data-cleaning-python",
                "description": "Profile, fix and document messy datasets with pandas so downstream analysis is trustworthy.",
                "lesson": {
                    "title": "Data Cleaning in Python — Lesson",
                    "notes": "Real datasets arrive with missing values, duplicate rows, inconsistent labels and columns typed as text. Cleaning is where analysis credibility is won or lost, and it should be reproducible rather than a series of manual edits.\n\n- Profile first: shape, dtypes, head, describe, and value_counts for object columns. Count nulls per column and duplicates on a natural key.\n- Standardise text with str.strip(), str.lower() and a replacement map so Mumbai and mumbai are not two categories.\n- Parse dates explicitly with a format or utc=True, then derive features like weekday rather than re-parsing later.\n- Handle missing data deliberately: drop only when the row is truly unusable, otherwise impute with a documented rule (median for skewed numerics, a labelled Unknown for categoricals) and flag that imputation happened.\n- Convert categories to the efficient dtype and use nullable integer types so NaNs do not force floats.\n- Keep a clean-data script under version control; never edit a spreadsheet by hand as the source of truth.\n\nWatch for subtle corruption: numbers stored as strings with currency symbols, percentages as 0-100 versus 0-1, and leading zeros stripped from identifiers. After cleaning, assert invariants — row counts, key uniqueness, value ranges — so a changed upstream file fails loudly instead of quietly changing your conclusions.",
                    "examples": [
                        "Revenue column parsed as text with $ and commas — strip symbols and cast to float in one step",
                        "Duplicates inflate a conversion rate — deduplicate on order_id keeping the latest updated_at",
                    ],
                    "practice": [
                        "Write a cleaning script that reports null counts, fixes date parsing and asserts row-count invariants.",
                        "Standardise five spellings of the same city and show the value_counts before and after.",
                        "Decide, with justification, how you would handle 40 percent nulls in an optional survey column.",
                    ],
                },
            },
            {
                "title": "Visualisation and Dashboards",
                "slug": "path-visualisation-dashboards",
                "description": "Choose the right chart, design clear dashboards and tell a story that drives decisions.",
                "lesson": {
                    "title": "Visualisation and Dashboards — Lesson",
                    "notes": "A chart is an argument. Pick the form that matches the question: bars for comparison, lines for change over time, scatter for relationship, histogram for distribution, and a table when readers need exact values. Pie charts work only for two or three parts of a clear whole.\n\n- Remove clutter. Delete gridlines that add nothing, drop the legend when direct labels fit, and truncate nothing — a y-axis that does not start at zero exaggerates bar differences.\n- Use colour with intent: highlight the one series that matters and grey the rest. Never encode meaning by colour alone for accessibility.\n- Give every visual a title phrased as an insight, not a label: Revenue grew 18 percent in Q3 beats Q3 Revenue.\n- Order dashboards by decision: headline KPIs first, then trends, then detail. One screen, one purpose.\n- Show context — targets, prior period, or benchmark — so a number is interpretable without explanation.\n\nBuild dashboards with filters that match how stakeholders actually ask questions (date range, segment, region) and make defaults the most common view. Performance is a feature: pre-aggregate where possible so the page loads in under two seconds. Finally, review every dashboard after launch — if nobody opens it after a month, a scheduled report or an alert probably serves them better.",
                    "examples": [
                        "Twelve-series line chart nobody can read — highlight one series and use direct annotation for the rest",
                        "Bar chart with a truncated axis implying 10x growth — start at zero and let the real change show",
                    ],
                    "practice": [
                        "Turn a monthly table into three charts and write insight-first titles for each.",
                        "Redesign a cluttered dashboard to fit a single screen with a clear top-to-bottom order.",
                        "Choose the correct chart type for six different questions and defend each choice in one sentence.",
                    ],
                },
            },
            {
                "title": "Statistics for Analysts",
                "slug": "path-statistics-analysts",
                "description": "Use distributions, sampling, confidence intervals and hypothesis tests to avoid misleading conclusions.",
                "lesson": {
                    "title": "Statistics for Analysts — Lesson",
                    "notes": "Statistics protects you from believing noise. Start with distributions and summary statistics: mean and median tell different stories when data is skewed, and the standard deviation describes spread that a single average hides.\n\n- Know sampling. Convenience samples rarely represent the population, and small samples carry wide uncertainty — always ask how the data was collected.\n- A confidence interval communicates the range a parameter plausibly falls in; a p-value answers only whether an observed difference would be surprising if no real difference existed. Neither measures effect size, so always report the absolute and relative difference as well.\n- Choose tests by question: t-test for a mean difference, chi-square for categorical association, and a non-parametric alternative when assumptions clearly fail.\n- Watch for base rates — a test with 99 percent specificity still produces many false positives when the event is rare.\n- Correlation is not causation; confounders and Simpson's paradox both break naive readings.\n\nPractise framing: state the hypothesis before looking, define the metric and window in advance, and beware peeking at results repeatedly, which inflates false positives. When running experiments, check sample size, guardrail metrics and novelty effects. Communicate uncertainty visually with intervals rather than error-free single numbers, and translate everything back into plain language for stakeholders.",
                    "examples": [
                        "Revenue is heavily skewed — report the median alongside the mean so a few large orders do not mislead",
                        "Conversion dipped 0.2 percent — a confidence interval spanning zero says the change may be noise",
                    ],
                    "practice": [
                        "Compute mean, median, spread and a histogram for a skewed metric and explain the difference.",
                        "Run an A/B test analysis and report lift, interval and practical significance together.",
                        "Give a real example of Simpson's paradox and how you would investigate it.",
                    ],
                },
            },
        ],
    },
    {
        "title": "Data Scientist",
        "slug": "data-scientist",
        "icon": "activity",
        "level": "Intermediate",
        "description": "Move from data to validated predictive models with sound statistics and honest evaluation. You finish able to build, evaluate and explain a model that a stakeholder can trust.",
        "topics": [
            {
                "title": "Python for Data Science",
                "slug": "path-python-data-science",
                "description": "Use NumPy, pandas and scikit-learn fluently to explore data and build reproducible modelling pipelines.",
                "lesson": {
                    "title": "Python for Data Science — Lesson",
                    "notes": "The data science stack is built on NumPy arrays and pandas DataFrames. Work vectorised: operating on whole arrays is orders of magnitude faster than Python loops, and it reads better.\n\n- Select with df.loc[row_index, col] for label-based access and df.iloc for integer positions; mixing them is a classic off-by-one source.\n- Group with df.groupby(col).agg(...) and reshape with pivot_table when a report needs columns as categories.\n- Handle missing values early with isna().sum(), then choose a strategy per column and record it.\n- Use .pipe to chain steps so a pipeline reads top to bottom and can be tested piecewise.\n- Scikit-learn estimators follow fit, predict, score. Put preprocessing and the model in a Pipeline so cross-validation cannot leak information from the test set.\n\nReproducibility is non-negotiable: set random seeds, pin package versions, and keep the whole workflow in a notebook that restarts cleanly or a script orchestrated by a scheduler. Avoid leakage — target-derived features, future data, or scaling fit on the full dataset — because leakage produces excellent offline scores and useless production results. Save trained artefacts with joblib or ONNX, log the data snapshot and parameters, and write a short model card describing intended use, features and known limitations.",
                    "examples": [
                        "Scaling fit on the entire dataset inflated CV scores — move scaling inside the Pipeline so it fits on training folds only",
                        "Row-wise Python loop takes minutes — rewrite as a NumPy vectorised operation that finishes in seconds",
                    ],
                    "practice": [
                        "Build a preprocessing-plus-model Pipeline with cross-validation and compare it with a manual approach.",
                        "Take a messy dataset and produce a groupby report of means, counts and medians in one chained expression.",
                        "Write a small model card covering data, features, metrics and known limitations.",
                    ],
                },
            },
            {
                "title": "Statistics and Probability",
                "slug": "path-statistics-probability",
                "description": "Reason about uncertainty with distributions, estimation, Bayes and the tests you will actually use.",
                "lesson": {
                    "title": "Statistics and Probability — Lesson",
                    "notes": "Probability is the language of uncertainty, and statistics is how you estimate under it. Build from the ground up: a random variable, its distribution, and the summary properties you can derive or estimate.\n\n- Know the workhorses: normal for measurement, binomial for counts of success, Poisson for events in a window, and the central limit theorem that makes sample means approximately normal.\n- Estimation beats dichotomous testing. Report point estimate plus interval, and use bootstrap resampling when the maths has no closed form.\n- Bayes' rule updates belief with evidence and is the cleanest way to think about rare events and diagnostic accuracy — combine base rate with likelihood, not the likelihood alone.\n- Hypothesis tests: state null and alternative, check assumptions, choose the test, then interpret the p-value with effect size and power. A non-significant result is not proof of no effect; it may simply be underpowered.\n- Understand Type I and Type II errors and pick which is costlier for your decision.\n\nApply this to real problems: estimating conversion with few conversions, choosing sample size for an experiment with a minimum detectable effect, and correcting for multiple comparisons when you run many tests. Communicate with simulation — a short Monte Carlo script often teaches a concept faster than a formula and gives you intuition you keep.",
                    "examples": [
                        "Rare conversion at 0.5 percent — use a Wilson interval instead of a naive normal approximation",
                        "Underpowered test shows no effect — compute required sample size from MDE before concluding nothing happened",
                    ],
                    "practice": [
                        "Simulate 10 000 sample means and show the central limit theorem emerging.",
                        "Compute power for a proposed A/B test and state the minimum detectable effect.",
                        "Solve a base-rate problem with Bayes and explain the result to a non-technical reader.",
                    ],
                },
            },
            {
                "title": "Machine Learning Basics",
                "slug": "path-ml-basics",
                "description": "Frame problems, choose algorithms and train your first supervised and unsupervised models responsibly.",
                "lesson": {
                    "title": "Machine Learning Basics — Lesson",
                    "notes": "Start by framing the problem, not by picking an algorithm. Is it classification or regression, are classes balanced, how much data do you have, and what decision will the output drive? The answer determines whether you need gradient boosting or a logistic regression.\n\n- Linear and logistic regression are strong baselines and are interpretable; always fit them first and record their score.\n- Tree ensembles — random forest and gradient boosting — handle mixed features and non-linearities well but need careful regularisation to avoid overfitting.\n- k-NN and Naive Bayes are cheap and useful for baselines and text.\n- For unsupervised work, use k-means or PCA for structure discovery, but remember clusters are hypotheses to validate, not facts.\n\nThe workflow matters more than the model: split data into train, validation and test once; fit preprocessing on training only; tune with cross-validation; and hold the test set untouched until the final report. Regularise with depth limits, learning rate, and early stopping. Encode categoricals thoughtfully and scale features for distance-based methods. Learn to read a learning curve — high bias means more data will not help, high variance means regularise or collect more. Document features, hyperparameters and metrics so a colleague can reproduce the run and you can defend it later.",
                    "examples": [
                        "Boosted model scores 0.99 offline and 0.61 in production — leakage plus overfitting; recheck features and regularise",
                        "Class imbalance makes accuracy meaningless — switch to precision, recall and AUC, and try class weights",
                    ],
                    "practice": [
                        "Train baseline logistic regression and a tree model on the same split and compare honestly.",
                        "Plot a learning curve and decide whether to gather more data or regularise.",
                        "Apply k-means to customer data and design a business check for whether the segments are real.",
                    ],
                },
            },
            {
                "title": "Model Evaluation",
                "slug": "path-model-evaluation",
                "description": "Select the right metrics, avoid leakage and communicate model performance with honesty.",
                "lesson": {
                    "title": "Model Evaluation — Lesson",
                    "notes": "Choosing a metric is choosing what mistakes you are willing to make. Accuracy is misleading under imbalance; for a fraud model, precision and recall express the trade-off between annoying good customers and missing thieves. Use ROC-AUC for ranking quality and precision-recall curves when positives are rare.\n\n- Never evaluate on data used for training or tuning. Keep a held-out test set, and use stratified k-fold when classes are small.\n- Build a confusion matrix and read it cell by cell — it tells you exactly which errors the model makes.\n- For regression report MAE for typical error, RMSE for penalising large misses, and R-squared only as context. Check residuals for patterns, which reveal a misspecified model.\n- Use proper baselines: the current rule-based system, a naive predictor, and human performance. Beating nothing is not an achievement.\n- Watch for leakage, distribution shift between train and serving, and metric drift over time.\n\nCalibration matters if probabilities drive actions: a well-calibrated 0.8 should be right 80 percent of the time, so use reliability diagrams and consider Platt scaling. Evaluate slices — performance by region, device or cohort — because a good average can hide a failing segment. Finally, present results with uncertainty, state what the model is for and not for, and define the monitoring and retraining triggers before deployment.",
                    "examples": [
                        "99 percent accuracy on a 1 percent fraud rate predicts all-zeros — report recall and PR-AUC instead",
                        "Test set used for early stopping gave optimistic scores — move early stopping to a validation fold",
                    ],
                    "practice": [
                        "Compare two models using a confusion matrix and argue which threshold the business should use.",
                        "Produce a calibration curve and describe whether probabilities can be trusted.",
                        "Write a one-page evaluation summary with baselines, slice metrics and monitoring triggers.",
                    ],
                },
            },
        ],
    },
    {
        "title": "Technical Support Engineer",
        "slug": "technical-support-engineer",
        "icon": "headphones",
        "level": "Beginner",
        "description": "Diagnose and resolve customer issues quickly while keeping users informed and confident. You finish able to isolate a fault across network, server and application layers and communicate the fix clearly.",
        "topics": [
            {
                "title": "Networking Fundamentals",
                "slug": "path-networking-fundamentals",
                "description": "Understand the layered network model, DNS, HTTP and the commands that locate faults fast.",
                "lesson": {
                    "title": "Networking Fundamentals — Lesson",
                    "notes": "Most cannot-reach-it tickets are network problems, so learn the stack as a series of layers and test each one in order. The OSI model gives you that order: physical, data link, network, transport, session, presentation, application. Practically you work from the bottom up — link light and Wi-Fi first, then IP, then port, then application response.\n\n- ping tests reachability at layer 3; a reply with high latency or loss points to congestion or a flaky path.\n- traceroute or tracert shows where the path breaks or detours, hop by hop.\n- nslookup or dig checks DNS: does the name resolve, and to the expected address? DNS is the most common cause of works-for-my-coworker issues.\n- curl with -v reveals the HTTP conversation: TLS handshake, status code and headers. Telnet or Test-NetConnection confirms a specific port is open.\n- Understand TCP versus UDP, why HTTPS needs port 443 plus a valid certificate, and how proxies and VPNs change the route.\n\nWork methodically: reproduce, note exact error text, then isolate layer by layer until you find the first thing that fails. Everything after that failure is a symptom. Record each command and its output in the ticket so the next engineer does not repeat your work, and so escalations arrive with evidence attached.",
                    "examples": [
                        "Site fails for one user only — dig shows a stale DNS entry while others resolve the new IP",
                        "Connection times out — Test-NetConnection to port 443 fails, so the firewall, not the app, is blocking",
                    ],
                    "practice": [
                        "Walk a colleague through ping, dig, traceroute and curl -v to locate a simulated outage.",
                        "Explain in two sentences why a valid certificate can still fail if the system clock is wrong.",
                        "Map five real symptoms to the OSI layer you would investigate first.",
                    ],
                },
            },
            {
                "title": "Linux Fundamentals",
                "slug": "path-linux-fundamentals",
                "description": "Navigate shells, inspect processes, read logs and manage files and permissions on Linux servers.",
                "lesson": {
                    "title": "Linux Fundamentals — Lesson",
                    "notes": "Support engineers live in the shell. Get fluent with navigation and files first: pwd, ls -lah, cd, and understanding that everything is a file, including devices under /dev and services under /proc.\n\n- Text tools are your microscope: cat, less, head, tail -f, grep -n with context flags, and pipes to chain them. tail -f on a log during a live issue is the fastest way to watch behaviour.\n- Process control: ps aux, top or htop for CPU and memory, kill for a graceful stop, kill -9 only as a last resort, and systemctl status or restart for services.\n- Diagnose resources with df -h for disk space, du -sh for directory size, free -h for memory, and uptime or load averages. Filling a disk is the most common outage cause you can prevent.\n- Permissions: read, write, execute for owner, group and others; sudo for elevation; chmod and chown to fix access errors. Read ls -l output until it is second nature.\n- Understand redirection and globbing: > to overwrite, >> to append, 2>&1 to merge errors, and wildcards to match files.\n\nAlways confirm the change before making it and prefer config checks (nginx -t, configtest) before restarts. Capture commands and output in the ticket so the incident record is complete.",
                    "examples": [
                        "Service will not start — df -h shows 100 percent on /var, clearing logs restores it",
                        "Permission denied on upload — ls -l reveals the file owner is root and the app user lacks write",
                    ],
                    "practice": [
                        "Use ps, top and journalctl to identify what is consuming CPU on a slow server.",
                        "Write a one-line grep that finds error patterns in a log with three lines of context.",
                        "Explain chmod 640 and chown in terms of who can read, write and execute a file.",
                    ],
                },
            },
            {
                "title": "Troubleshooting Method",
                "slug": "path-troubleshooting-method",
                "description": "Apply a repeatable diagnostic process that isolates root cause instead of guessing at fixes.",
                "lesson": {
                    "title": "Troubleshooting Method — Lesson",
                    "notes": "Method beats intuition. A repeatable process makes you faster and stops you from changing five things at once and learning nothing.\n\n- Reproduce and document: exact steps, expected result, actual result, error text, timestamps, account, environment and whether it affects one user or everyone. Cannot reproduce means not yet diagnosed.\n- Establish a baseline: what does the same check return on a working system or at a working time?\n- Isolate with a divide-and-conquer sweep across layers — client, network, load balancer, service, database, third party — and test one variable at a time.\n- Form a hypothesis, make one change, then verify. Change nothing else, or you lose causality.\n- Confirm the fix by reproducing the original scenario and watching monitoring, then check for regressions.\n- Write the post-mortem: timeline, root cause, contributing factors, what we will change. Blameless, specific, actionable.\n\nResist the reboot reflex. A restart hides the evidence and the problem usually returns. Keep a personal runbook of symptom-to-check pairs and update it after every novel issue. Know when to escalate: when you have evidence at each layer, a clear impact statement and the exact point of failure, engineering can act immediately. Escalating a wall of screenshots wastes everyone's time; escalating a bisected log with timestamps does not.",
                    "examples": [
                        "Five config changes made at once — revert all, then apply one at a time with a test after each",
                        "Bug vanishes after restart — grab core dumps and logs first so the crash cause survives the restart",
                    ],
                    "practice": [
                        "Write an incident ticket for a login failure including reproduction steps and evidence.",
                        "Bisect a simulated regression from release 41 by checking one layer at a time.",
                        "Draft a blameless post-mortem for a 30-minute outage with a real root cause.",
                    ],
                },
            },
            {
                "title": "Customer Communication",
                "slug": "path-customer-communication",
                "description": "Set expectations, explain technical issues plainly and de-escalate difficult conversations.",
                "lesson": {
                    "title": "Customer Communication — Lesson",
                    "notes": "Technical accuracy without clear communication still feels like a bad experience. Support writing should reduce the customer's uncertainty at every message.\n\n- Open by confirming you understood the problem in their words, then state what you will do next and when you will update them.\n- Use plain language. Translate the technical cause into effect: your DNS record was pointing at an old server, which is why the site would not load. Avoid blame and internal jargon.\n- Give timeframes you can keep, and if the estimate slips, update before the deadline passes. Silence after a promise is what destroys trust.\n- When you do not know, say so and give the next step plus a time. Never speculate about causes you have not verified.\n- For difficult conversations, de-escalate: acknowledge impact, take ownership of the next action, and avoid defensive phrasing. Apologise for the impact, not by admitting fault you cannot verify.\n- Close the loop: explain the fix, how to prevent it, and any action the customer must take.\n\nStructure long replies with a short summary first and detail after, so a skimming reader still gets the point. Confirm understanding by asking a question at the end. Every ticket should leave the customer knowing the state, the owner and the next update time — that certainty is the product you are really delivering.",
                    "examples": [
                        "Engineer-speak baffles the customer — rewrite as cause, impact, fix and next step in plain words",
                        "Promised update missed — send a brief interim note before the deadline to preserve trust",
                    ],
                    "practice": [
                        "Rewrite a defensive ticket reply into an owner-first, plain-language response.",
                        "Draft an outage update email with impact, workaround, ETA and next-update time.",
                        "Role-play a de-escalation for a customer whose report was closed prematurely.",
                    ],
                },
            },
        ],
    },
    {
        "title": "KPO Analyst",
        "slug": "kpo-analyst",
        "icon": "book-open",
        "level": "Beginner",
        "description": "Deliver research-backed insights and immaculate reports under tight deadlines. You finish able to source credible data, build error-free spreadsheets and write conclusions executives act on.",
        "topics": [
            {
                "title": "Research and Secondary Data",
                "slug": "path-research-secondary-data",
                "description": "Find, vet and cite credible sources so every claim in your deliverable stands up to scrutiny.",
                "lesson": {
                    "title": "Research and Secondary Data — Lesson",
                    "notes": "KPO work rests on evidence quality. Secondary data is information collected by someone else — government statistics, industry reports, filings, surveys — and your first job is judging whether it is fit for the question.\n\n- Prefer primary sources: a regulator's filing beats a news summary of it; the central bank's series beats a blog's chart of it.\n- Check four things on every source: who published it, when, what methodology and sample underlie it, and whether they have a commercial interest in the conclusion.\n- Capture metadata as you go — publisher, publication date, URL, access date, table number — so citation is a two-minute job instead of an afternoon of archaeology.\n- Normalise comparability: definitions differ between sources (unemployment rate, TAM, revenue recognition), so note the definition before you combine series.\n- Triangulate important claims across at least two independent sources; agreement raises confidence, disagreement demands explanation.\n\nBuild a working evidence table with claim, value, source, date and confidence. Watch for survivorship bias, outdated pre-pandemic baselines, and vendor reports whose methodology is a black box. Store everything in a folder structure per project with a naming convention so a teammate can find files. When a figure cannot be verified, label it as an estimate with its assumption stated openly rather than presenting it as fact — the credibility you protect is your own.",
                    "examples": [
                        "Blog cites market size with no source — trace to the original research and record its methodology",
                        "Two reports disagree on growth — compare definitions and dates before choosing which to present",
                    ],
                    "practice": [
                        "Build a source evaluation matrix for five candidate sources on one topic.",
                        "Create an evidence table with claim, value, publisher, date and confidence for a short brief.",
                        "Find the primary source behind a secondary statistic and write two lines on its methodology.",
                    ],
                },
            },
            {
                "title": "Advanced MS Excel",
                "slug": "path-advanced-ms-excel",
                "description": "Build error-free models with lookups, pivot tables, conditional logic and disciplined formatting.",
                "lesson": {
                    "title": "Advanced MS Excel — Lesson",
                    "notes": "Excel is where most KPO deliverables are actually built, and mastery shows up as speed plus zero errors.\n\n- Lookups: XLOOKUP handles reverse and missing-value cases cleanly; INDEX-MATCH remains essential for legacy files. Always key on a unique, stable identifier and handle not-found values explicitly.\n- Logical structure: IFS for multi-condition classification, SUMIFS and COUNTIFS for metrics by segment, and IFERROR to keep the sheet readable.\n- Pivot tables are your first tool for any cut of a dataset — rows, values, filters, and show values as percent of total. Refresh rather than rebuild.\n- Data integrity: turn on data validation lists for inputs, use named ranges, and freeze panes on headers. Format dates as real dates and keep numbers as numbers, not text.\n- Model hygiene: separate inputs, calculations and outputs with colour conventions (blue for inputs, black for formulas), never hard-code inside a formula, and document assumptions in a notes block.\n\nAudit with formula tracing, precedent and dependent arrows, and a quick check for error cells. Use Ctrl to select visible cells only before copying filters. Keyboard shortcuts multiply your throughput: F4 to lock references, Ctrl+Shift+L to toggle filters. Save versions with dates so an overwritten file never ends the day badly.",
                    "examples": [
                        "VLOOKUP breaks when a column is inserted — switch to INDEX-MATCH or XLOOKUP for stable references",
                        "Text-formatted dates fail to sort — convert with DATEVALUE and reformat the column as dates",
                    ],
                    "practice": [
                        "Build a SUMIFS dashboard summarising revenue by region and product with a pivot backing it.",
                        "Model a scenario table with data validation inputs and clearly separated assumptions.",
                        "Audit a broken workbook by tracing precedents and fixing every error cell you find.",
                    ],
                },
            },
            {
                "title": "Business Communication",
                "slug": "path-business-communication",
                "description": "Write executive-ready emails, memos and slide narratives that make the recommendation obvious.",
                "lesson": {
                    "title": "Business Communication — Lesson",
                    "notes": "Executives read for decisions, not for detail. Structure every deliverable so the answer arrives first and the evidence follows for anyone who wants it.\n\n- Lead with the recommendation or key finding in one sentence. Add a two-line context only if it is genuinely needed.\n- Support with three or four proof points, each with the number and the source. Then detail, method and caveats in an appendix.\n- Emails: put the ask and the deadline in the first two lines, use short paragraphs and bullets, and end with a clear next action and owner.\n- Slides: one message per slide, title written as a full conclusion, and a speaker note carrying the detail. Delete any slide you would not defend aloud.\n- Match tone to audience — clients get polished prose, engineers get crisp specifics — while staying neutral, precise and free of hedging words like basically or kind of.\n\nEdit ruthlessly. Read aloud to catch clunky sentences, cut every sentence that does not change a decision, and verify all numbers against your source before sending. Define acronyms on first use and never let the reader discover ambiguity — specify the time window, currency and segment for every figure. Finish with proofreading: consistent dates, units and product names. Precision is the credibility signal in knowledge work.",
                    "examples": [
                        "Memo buries the recommendation on page three — rewrite so the first line states the decision requested",
                        "Slide title reads Q3 Overview — rewrite as Revenue grew 18 percent in Q3, led by enterprise",
                    ],
                    "practice": [
                        "Write a one-page memo with headline, three proof points and an appendix reference.",
                        "Turn a dense analysis deck into five slides with conclusion-style titles.",
                        "Edit a rambling email to under 150 words while keeping the ask and deadline clear.",
                    ],
                },
            },
            {
                "title": "Analytical Reasoning",
                "slug": "path-analytical-reasoning",
                "description": "Break down unstructured problems, sanity-check numbers and turn analysis into a defensible conclusion.",
                "lesson": {
                    "title": "Analytical Reasoning — Lesson",
                    "notes": "Analytical reasoning is structured thinking under time pressure. The method is always the same: define the question, break it into parts, estimate, then verify.\n\n- Clarify the actual question and its constraints — units, time horizon, audience — before calculating anything. Most errors are framing errors.\n- Decompose with a framework: market sizing by population times penetration times price, profitability into revenue minus cost, or a tree of drivers you can quantify one by one.\n- Estimate with round numbers and stated assumptions, then check the result against common sense. If a market sizing answer implies every person buys ten units a year, the assumption is wrong, not the arithmetic.\n- Sanity-check constantly: does the total tie to the source, do the parts sum to the whole, is the growth rate plausible against history?\n- Separate fact, inference and assumption in your write-up, so a reader can challenge precisely the part they doubt.\n- Consider alternatives and base rates before concluding; ask what else would explain the same pattern.\n\nPractise with Fermi questions daily — how many petrol stations are in a country, how much a coffee shop sells per day — and record your assumption chain. In reports, show the calculation compactly, flag sensitivity to the two inputs that matter most, and state what evidence would change your mind. That honesty is what makes analysis decision-grade.",
                    "examples": [
                        "Profit drop blamed on price — decomposition shows volume fell in one channel, so price is not the driver",
                        "Revenue forecast of a billion with no basis — rebuild from customer count times average contract value",
                    ],
                    "practice": [
                        "Size a national market top-down and bottom-up and reconcile the difference.",
                        "Decompose a 10 percent profit decline into drivers and identify the dominant one.",
                        "List the assumptions in a given forecast and rank them by sensitivity.",
                    ],
                },
            },
        ],
    },
    {
        "title": "DevOps Engineer",
        "slug": "devops-engineer",
        "icon": "cloud",
        "level": "Intermediate",
        "description": "Automate delivery from shell scripts to containers, pipelines and observable cloud systems. You finish able to take code from a commit to a monitored production deployment.",
        "topics": [
            {
                "title": "Linux and Shell Scripting",
                "slug": "path-linux-shell-scripting",
                "description": "Write robust bash scripts with proper quoting, error handling and idempotent system operations.",
                "lesson": {
                    "title": "Linux and Shell Scripting — Lesson",
                    "notes": "Shell is the automation glue of infrastructure. A reliable script starts with discipline at the top: #!/usr/bin/env bash, set -euo pipefail so the script exits on errors, undefined variables and failed pipelines, and IFS to avoid word-splitting surprises.\n\n- Quote every variable expansion: \"$file\" not $file. Unquoted paths with spaces are the single most common shell bug.\n- Prefer [[ ]] over [ ] for conditionals, and use local for function variables.\n- Loop over files with for f in *.log; do ... done rather than ls parsing; use while read -r line for streaming input.\n- Handle arguments with shift and a usage function; validate inputs before touching anything.\n- Capture output deliberately: $(cmd) for stdout, 2>/dev/null only when you truly intend to discard errors, and check $? or rely on set -e.\n- Make operations idempotent — mkdir -p, apt-get install -y only when absent, and guard destructive rm with explicit paths.\n\nUse shellcheck on every script; it catches the majority of quoting and portability mistakes before they cause an outage at 3 a.m. Add traps to clean up temporary files on exit, log with timestamps to a file, and keep scripts small with one responsibility. Know when bash is wrong: complex data handling belongs in Python, where types and error handling exist.",
                    "examples": [
                        "Unquoted $path splits on spaces — quote it as \"$path\" and add shellcheck to CI",
                        "Script half-applies on failure — add set -euo pipefail and a trap so changes are all-or-nothing",
                    ],
                    "practice": [
                        "Write a rotation script that compresses logs older than seven days and is safe to rerun.",
                        "Refactor a legacy script to pass shellcheck with set -euo pipefail and quoted expansions.",
                        "Build a small CLI with flags, validation and a usage message using getopts.",
                    ],
                },
            },
            {
                "title": "CI/CD Pipelines",
                "slug": "path-cicd-pipelines",
                "description": "Automate build, test, security checks and deployment so every commit ships the same reliable way.",
                "lesson": {
                    "title": "CI/CD Pipelines — Lesson",
                    "notes": "A pipeline is a contract: every change passes the same gates, and any engineer can ship without tribal knowledge. Build it in stages that fail fast.\n\n- Stage 1 fast checks — lint, format, type-check and unit tests — in minutes, so feedback lands while context is fresh.\n- Stage 2 build a versioned artefact once and promote that exact artefact through environments. Rebuilding for production introduces drift.\n- Stage 3 integration and security: dependency and image scanning, secret detection, and container tests against a real database.\n- Stage 4 deploy with a strategy — blue-green or canary — behind a health check, with automatic rollback when error rates or latency spike.\n\nKeep pipelines deterministic: pin dependency versions, cache wisely (key the cache on the lock file), and never let tests depend on execution order or external networks. Use environment protection rules and required reviewers for production. Make every build reproducible from a commit hash, and embed that hash in the image tag and the runtime health endpoint for instant traceability. Track lead time, deploy frequency, change failure rate and time to restore as your scoreboard. Finally, treat pipeline code as production code — review it, test it, and keep it under version control next to the app.",
                    "examples": [
                        "Different binary in staging and production — build once, store the artefact, promote it unchanged",
                        "Flaky test blocks every merge intermittently — quarantine it with a ticket and fix or delete it",
                    ],
                    "practice": [
                        "Create a three-stage pipeline: lint and test, build image with a scan, deploy with health check.",
                        "Add automatic rollback triggered by a 5xx threshold after deployment.",
                        "Write a caching strategy for a pip-based pipeline keyed on the lock file.",
                    ],
                },
            },
            {
                "title": "Containers with Docker",
                "slug": "path-containers-docker",
                "description": "Build small, secure, reproducible images and run multi-service applications with compose.",
                "lesson": {
                    "title": "Containers with Docker — Lesson",
                    "notes": "Containers package the app with its dependencies so every environment behaves the same. Getting images right is most of the battle.\n\n- Use a multi-stage build: compile or install in a builder stage, then copy only the artefacts into a slim runtime image. This cuts size and attack surface dramatically.\n- Order layers for cache efficiency — copy lock files and install dependencies before copying source, so dependency layers are reused.\n- Add a .dockerignore for .git, virtualenvs and local secrets. Never bake credentials into an image; inject them at runtime.\n- Run as a non-root user, pin base image versions, and set a specific ENTRYPOINT with an exec form so signals reach your process and shutdown is clean.\n- One concern per container. Compose wires services together with a default network, environment variables, healthchecks and named volumes for state.\n- Containers are ephemeral: keep state in databases or volumes, and make the app tolerate restarts at any moment.\n\nDebug with docker logs, docker exec for a shell, and docker inspect for configuration. Understand namespaces and cgroups enough to explain isolation, and recognise that containers share the host kernel. Scan images in CI, keep them updated, and measure the result — a well-built image starts in seconds and scales by starting more copies, which is exactly what you want in production.",
                    "examples": [
                        "Image is 1.8 GB with compilers in it — multi-stage build produces a 95 MB runtime image",
                        "Container exits immediately because PID 1 ignores signals — switch to exec-form ENTRYPOINT or use tini",
                    ],
                    "practice": [
                        "Write a multi-stage Dockerfile for a Python app with a non-root user and pinned base image.",
                        "Compose a stack of app, Postgres and Redis with healthchecks and a named volume.",
                        "Compare image size and build time before and after layer-order optimisation.",
                    ],
                },
            },
            {
                "title": "Cloud and Monitoring",
                "slug": "path-cloud-monitoring",
                "description": "Deploy resilient cloud infrastructure and instrument systems so you detect problems before users do.",
                "lesson": {
                    "title": "Cloud and Monitoring — Lesson",
                    "notes": "Cloud work is managed trade-offs: cost, resilience and operational complexity. Design for failure — assume any single component can die at any time.\n\n- Run at least two instances across availability zones behind a load balancer, with auto-scaling policies tied to real signals like requests per second or queue depth.\n- Manage infrastructure as code so environments are reviewable, reproducible and disposable. Never click changes into a production console.\n- Separate config from code, store state safely, and make changes apply cleanly without downtime.\n- Observability has three pillars: metrics, logs and traces. Export the four golden signals — latency, traffic, errors and saturation — and attach a request id so logs correlate across services.\n- Alert on symptoms users feel, not on raw internals: page on error rate and latency SLO burn, and route noisy non-urgent warnings to a ticket channel.\n- Define SLOs with error budgets so the team can reason about how much change is safe, and practise rollback until it is boring.\n\nSet budgets with tagging and cost alerts, right-size instances before buying more, and use reserved or spot pricing where appropriate. Keep dashboards that answer one question each: is the system healthy, where is the bottleneck, what changed. Every alert must link to a runbook, otherwise it is just noise at 3 a.m.",
                    "examples": [
                        "Instance dies and the site goes down — add a second AZ behind a load balancer with health checks",
                        "Alert fatigue from CPU warnings — alert on latency and error-rate SLO burn instead",
                    ],
                    "practice": [
                        "Define infrastructure as code for a two-zone deployment with autoscaling and an RDS instance.",
                        "Build a dashboard showing the four golden signals plus a deployment marker.",
                        "Write an SLO, its error budget, and the alert thresholds that should page on-call.",
                    ],
                },
            },
        ],
    },
]
