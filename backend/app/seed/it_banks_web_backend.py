"""IT question banks + lessons: Frontend and Backend learning paths."""
from __future__ import annotations

IT_BANKS: dict[str, list[tuple]] = {
    "frontend-html": [
        ("Which element should wrap the primary, unique content of a page, excluding content repeated on every page such as headers and footers?",
         ["<div>", "<main>", "<section>", "<article>"], 1,
         "<main> marks the dominant content of the document and should appear at most once per page."),
        ("Which attribute on an <input> makes the browser refuse to submit the form until a value is supplied?",
         ["validate", "required", "mandatory", "novalidate"], 1,
         "required enables native validation, while novalidate actually disables it."),
        ("Which line correctly links an external stylesheet named style.css inside the document head?",
         ["<link rel=\"stylesheet\" href=\"style.css\">", "<stylesheet src=\"style.css\">",
          "<link type=\"style\" url=\"style.css\">", "<css file=\"style.css\"></css>"], 0,
         "A stylesheet is referenced with a <link> element using rel=\"stylesheet\" and an href."),
        ("Which element renders a list whose items are meaningfully ordered or numbered?",
         ["<ul>", "<ol>", "<dl>", "<li>"], 1,
         "<ol> is the ordered list; <ul> is unordered and <li> only holds a single item."),
        ("What does the for attribute of a <label> element point to?",
         ["The id of the associated form control", "The name attribute of the input",
          "The CSS selector used to style the input", "The position of the input in the form"], 0,
         "for must match the id of the control so clicking the label focuses that field."),
        ("Which of these is NOT a sectioning content element in HTML?",
         ["<article>", "<aside>", "<nav>", "<span>"], 3,
         "Sectioning content is article, aside, nav and section; span is a generic phrasing element."),
        ("What is the main purpose of the <!DOCTYPE html> declaration?",
         ["It switches the browser into standards mode and declares HTML5",
          "It downloads the HTML5 schema from w3.org",
          "It must be written as the first attribute of the <html> tag",
          "It enables JavaScript execution"], 0,
         "The doctype is a short trigger that puts the browser into standards, not quirks, mode."),
        ("Inside a well-formed <table>, which element groups the column header cells?",
         ["<thead>", "<tfoot>", "<tbody>", "<caption>"], 0,
         "<thead> holds the header rows containing <th> cells; <caption> only names the table."),
        ("Which element represents a self-contained composition that still makes sense on its own, such as a blog post or a product card?",
         ["<div>", "<section>", "<article>", "<footer>"], 2,
         "<article> is for independently meaningful content; section is a thematic grouping that normally needs a heading."),
        ("Which img tag marks a purely decorative image so screen readers skip it?",
         ["<img src=\"hero.jpg\">", "<img src=\"hero.jpg\" alt=\"decorative\">",
          "<img src=\"hero.jpg\" alt=\"hero.jpg\">", "<img src=\"hero.jpg\" alt=\"\">"], 3,
         "An empty alt attribute is the accessibility convention for decorative images; omitting alt entirely is invalid HTML."),
        ("Which value added to a target=\"_blank\" link suppresses the referrer and blocks the new page from scripting this one through window.opener?",
         ["rel=\"noopener noreferrer\"", "download", "hreflang", "referrerpolicy"], 0,
         "noopener removes the window.opener reference and noreferrer also drops the Referer header, protecting the original tab."),
        ("What does the controls attribute on a <video> element do?",
         ["Plays the video automatically on load", "Shows the browser's play, pause, volume and timeline UI",
          "Turns the element into a download link", "Enables captions by default"], 1,
         "controls reveals the native media controls; autoplay and <track> captions are separate concerns."),
    ],
    "frontend-css": [
        ("With p { color: black }, .note { color: green } and #intro { color: blue }, what color renders for <p id=\"intro\" class=\"note\">?",
         ["black", "green", "blue", "The last rule in source order always wins"], 2,
         "Specificity is written as (ID, class, type): the ID selector 1,0,0 beats class 0,1,0 and type 0,0,1."),
        ("Which layout system is designed for two-dimensional work, controlling rows and columns at the same time?",
         ["Flexbox", "CSS Grid", "Floats", "Table layout"], 1,
         "Grid manages rows and columns together; Flexbox is one-dimensional and works along a single axis."),
        ("With the default box-sizing: content-box, an element with width: 100px, padding: 10px and a 2px border occupies how much horizontal space?",
         ["100px", "120px", "124px", "140px"], 2,
         "content-box keeps padding and border outside the declared width: 100 + 10*2 + 2*2 = 124px."),
        ("What does position: absolute do to an element?",
         ["It takes the element out of flow and anchors it to its nearest positioned ancestor, or the initial containing block",
          "It always positions the element relative to the viewport",
          "It keeps the element in the normal document flow",
          "It removes the element from the accessibility tree"], 0,
         "Absolute positioning looks for the closest ancestor whose position is other than static."),
        ("Adjacent vertical margins of two block-level siblings collapse into:",
         ["The sum of both margins", "The larger of the two margins", "Zero", "The smaller of the two margins"], 1,
         "For positive margins the browser keeps the larger value instead of adding them together."),
        ("Which declaration clips content that overflows a box?",
         ["overflow: hidden", "visibility: hidden", "clip-path: none", "white-space: nowrap"], 0,
         "overflow: hidden clips the overflow and also makes the box scrollable; visibility only hides painting."),
        ("Two selectors of equal specificity target the same element. Which rule applies?",
         ["The one declared later in the stylesheet", "The one declared earlier",
          "The one with the shorter selector", "The one in the stylesheet loaded first"], 0,
         "When specificity ties, source order decides: the last declaration wins."),
        ("Given #box { color: blue } and p { color: red !important }, what color is <p id=\"box\">?",
         ["blue", "red", "They alternate by source order", "The page fails to render"], 1,
         "An !important declaration beats every normal declaration regardless of specificity."),
        ("Which declaration centers a flex item along the cross axis of a row flex container?",
         ["text-align: center", "justify-content: center", "align-items: center", "margin: 0 auto"], 2,
         "align-items works across the cross axis; justify-content distributes items along the main axis."),
        ("When does z-index actually take effect on an element?",
         ["The element is positioned or is a flex/grid item, so it takes part in stacking",
          "The element has a non-zero width", "The element is a direct child of the body",
          "The element uses display: inline"], 0,
         "z-index is ignored on statically positioned in-flow boxes because they never take part in stacking contexts."),
        ("Given @media (max-width: 640px) { .grid { grid-template-columns: 1fr; } }, when does the single column apply?",
         ["Only on viewports wider than 640px", "Only when the viewport is exactly 640px",
          "Only on touch devices", "On viewports 640px wide or narrower"], 3,
         "max-width is inclusive, so the block matches any viewport at or below 640px."),
        ("Which of these is a pseudo-element rather than a pseudo-class?",
         [":hover", "::before", ":focus", ":nth-child(2)"], 1,
         "Pseudo-elements use a double colon and style a part of an element, while single-colon selectors match states or positions."),
    ],
    "frontend-javascript": [
        ("What is the result of 0 === \"\"?",
         ["true", "false", "0", "A TypeError is thrown"], 1,
         "Strict equality skips coercion, and the number 0 is never identical to the string \"\" (0 == \"\" would be true)."),
        ("What does this print?\nfunction makeCounter() {\n  let n = 0;\n  return function () {\n    n = n + 1;\n    return n;\n  };\n}\nconst next = makeCounter();\nnext();\nnext();\nconsole.log(next());",
         ["0", "1", "2", "3"], 3,
         "The inner function closes over n, so each call increments the same captured value: 1, then 2, then 3."),
        ("What is the console output order?\nconsole.log(\"1\");\nsetTimeout(() => console.log(\"2\"), 0);\nPromise.resolve().then(() => console.log(\"3\"));\nconsole.log(\"4\");",
         ["1 2 3 4", "1 4 3 2", "1 3 4 2", "1 4 2 3"], 1,
         "Synchronous logs run first, then the promise microtask, then the setTimeout macrotask."),
        ("What happens when code reads a let variable before its declaration in the same scope?",
         ["It is hoisted and equals undefined", "It throws a ReferenceError (temporal dead zone)",
          "It is created as a global variable", "It equals null"], 1,
         "let and const are hoisted but left uninitialized, so reading them early hits the temporal dead zone."),
        ("What does an async function always return?",
         ["A plain value or undefined", "A Promise", "A generator object", "Nothing; it runs synchronously"], 1,
         "async is sugar over Promise, so awaiting it is how you read the resolved value."),
        ("Which statement about const is correct?",
         ["The variable cannot be reassigned, but object and array contents can still be mutated",
          "The bound value is deeply immutable", "It is function-scoped like var",
          "It cannot be used with destructuring"], 0,
         "const blocks rebinding only; mutation of the referenced object is allowed."),
        ("What does typeof null return?",
         ["\"null\"", "\"object\"", "\"undefined\"", "\"number\""], 1,
         "A legacy bug from the first implementation has never been removed for compatibility."),
        ("What does arr.map(fn) return?",
         ["The original array after mutating it", "A new array containing the callback results",
          "undefined", "The first truthy element"], 1,
         "map always returns a new array; forEach is the variant that returns undefined."),
        ("What does [1, 2, 3, 4].filter((n) => n % 2 === 0) return?",
         ["[2, 4]", "[1, 3]", "[6]", "4"], 0,
         "filter keeps the elements whose callback returns true, so the even numbers survive in a new array."),
        ("What is the console output?\nasync function run() {\n  console.log(\"a\");\n  await null;\n  console.log(\"b\");\n}\nrun();\nconsole.log(\"c\");",
         ["a b c", "c a b", "a c b", "c b a"], 2,
         "run() logs a then yields at await, the caller logs c synchronously, and the continuation b runs as a microtask."),
        ("What does JSON.stringify(undefined) return?",
         ["\"undefined\"", "null", "0", "undefined"], 3,
         "undefined is not JSON-serializable, so stringify returns the value undefined instead of a string."),
        ("What does Promise.all([first, second]) do when first rejects?",
         ["It resolves as soon as the first promise settles, whatever the outcome",
          "It rejects with the first rejection reason while the other promises keep running",
          "It waits for every promise and resolves with an array of errors",
          "It cancels the remaining promises"], 1,
         "Promise.all is fail-fast: the first rejection rejects the aggregate, but promises already started are not aborted."),
    ],
    "frontend-react": [
        ("Which of these violates the Rules of Hooks?",
         ["Calling useState() inside an if statement", "Calling useState() at the top level of the component",
          "Calling useEffect() with a dependency array", "Calling a setter inside an event handler"], 0,
         "Hooks must run unconditionally in the same order on every render, so a conditional call breaks the hook list."),
        ("After setCount(count + 1) inside an event handler, what is the value of count in that same handler?",
         ["The incremented value", "The old value, because updates are queued and applied on the next render",
          "undefined", "It throws an error"], 1,
         "State updates are scheduled rather than immediate; the new value is only visible on the next render."),
        ("Why does React need a stable key for each item in a list?",
         ["To style the row", "To give items a stable identity so React can match old and new elements during reconciliation",
          "To make the list keyboard accessible", "To sort the list automatically"], 1,
         "Keys identify elements across renders; index keys break when items are inserted, removed or reordered."),
        ("In a controlled input, where does the displayed value come from?",
         ["The DOM after the user types", "React state synced through the value prop plus onChange",
          "The defaultValue prop only", "The browser autocomplete cache"], 1,
         "value is driven by state and onChange updates that state, so React owns the input."),
        ("What does useEffect(() => { ... }, []) do?",
         ["Runs after every render", "Runs once after the initial mount", "Runs only when props change",
          "Never runs"], 1,
         "An empty dependency array runs the effect once on mount, and twice in development under StrictMode."),
        ("With const [n, setN] = useState(0), calling setN(n + 1) twice in the same handler gives which final n?",
         ["1", "2", "0", "3"], 0,
         "Both updates compute from the same captured n (0), so the result is 1; use setN(prev => prev + 1) twice to reach 2."),
        ("What is the correct way to update state that depends on the previous value?",
         ["setCount(count + 1) inside a setTimeout", "setCount(prev => prev + 1)",
          "this.state.count += 1", "count++"], 1,
         "The functional updater receives the latest queued value, so it is safe inside callbacks and timeouts."),
        ("When does a useEffect cleanup function run?",
         ["Before the effect body on every render", "Before the effect re-runs with new dependencies and on unmount",
          "While the component is rendering", "Only when the component errors"], 1,
         "Cleanup tears down the previous effect, such as timers and subscriptions, before the next run and on unmount."),
        ("What is the recommended way to keep a value that is always derived from other state or props?",
         ["Mirror it in useState and sync it with an effect", "Compute it during render instead of duplicating it in state",
          "Update it inside useLayoutEffect", "Store it in a ref and force a re-render"], 1,
         "Extra state that mirrors other state invites sync bugs, so derive the value in the render body instead."),
        ("What does useRef(initialValue) return?",
         ["A stringified version of the DOM node", "A state variable that re-renders when it changes",
          "A memoized callback that only changes with its dependencies",
          "A mutable object whose current property keeps the same reference across renders without causing re-renders"], 3,
         "Mutating ref.current is invisible to React, which is why refs hold timers and DOM nodes rather than render-driven data."),
        ("How does React 18 batch state updates that happen inside setTimeout, promises or native event handlers?",
         ["It merges every update scheduled in the same tick into a single re-render, even outside React events",
          "It only batches updates that occur inside React event handlers",
          "It applies each update with its own immediate re-render", "Batching was removed in React 18"], 0,
         "Automatic batching in React 18 also covers promises, timeouts and native handlers, not just React event handlers."),
        ("Which statement about useContext(SomeContext) is correct?",
         ["It only works in class components", "It reads the provider's value once and never re-renders",
          "It subscribes the component to the context, so it re-renders when the provided value changes",
          "It creates a new context object"], 2,
         "A component using useContext re-renders whenever the nearest provider's value changes."),
    ],
    "frontend-tailwind": [
        ("In Tailwind's default spacing scale, which class applies 8px (0.5rem) of top margin?",
         ["mt-1", "mt-2", "mt-4", "m-8"], 1,
         "The scale multiplies 4px by the number: mt-1 is 4px, mt-2 is 8px and mt-4 is 16px."),
        ("Which variant prefix applies a style only on screens 768px and wider?",
         ["sm:", "md:", "lg:", "tablet:"], 1,
         "The default breakpoints are sm 640px, md 768px and lg 1024px."),
        ("Which of these is a valid Tailwind utility class?",
         ["padding-10px", "p-10", "p[10]", "pad-10"], 1,
         "Utilities follow a property-value shorthand; off-scale values need arbitrary syntax such as p-[10px]."),
        ("Why must the content array in tailwind.config.js list your source files?",
         ["To import them as modules", "So Tailwind can scan them for class names and emit only the CSS actually used",
          "To enable CSS minification", "To configure the dev server port"], 1,
         "Without those globs Tailwind never sees classes like md:flex and will not generate them."),
        ("What does the class hover:bg-blue-600 do?",
         ["Applies the background on mouse down", "Applies the background while the element is hovered",
          "Applies the background on keyboard focus", "Always applies the background"], 1,
         "hover: is a state variant that wraps the utility inside a :hover rule."),
        ("Which set of classes builds a three-column grid with spacing between cells?",
         ["flex flex-3 gap-4", "grid grid-cols-3 gap-4", "grid col-3 space-4", "display-grid columns-3"], 1,
         "grid sets display, grid-cols-3 sets grid-template-columns and gap sets the gutter."),
        ("What does the arbitrary value syntax w-[137px] do?",
         ["It is invalid and gets ignored", "It generates a one-off width that is not on the default scale",
          "It registers a Tailwind plugin", "It defines a CSS custom property"], 1,
         "Bracket values let you use any raw CSS value while the rest of the class naming stays the same."),
        ("How do you hide an element with Tailwind and show it again from the md breakpoint upward?",
         ["hidden plus md:block", "hidden plus md:visible", "opacity-0 plus md:opacity-100",
          "display-none plus md:flex"], 0,
         "hidden sets display: none and md:block restores display: block at 768px and wider."),
        ("What does the class mx-auto do?",
         ["Centers a block-level box horizontally by setting its left and right margins to auto",
          "Applies the same margin to all four sides", "Sets the maximum width of the element",
          "Centers the text inside the element"], 0,
         "mx targets the horizontal margins, and auto splits the free space, which needs a definite width to work."),
        ("Which class adds 1rem of padding on the left and right sides only?",
         ["p-4", "pt-4", "px-4", "pr-4"], 2,
         "px is the horizontal axis so it pads both sides, while p-4 would also change the top and bottom."),
        ("How do you style a child only while its PARENT is hovered?",
         ["hover:opacity-50 on the parent", "parent-hover:opacity-50 on the child",
          "focus-within:opacity-50 on the child", "group-hover:opacity-50 on the child together with group on the parent"], 3,
         "hover: matches only the hovered element itself, so group plus group-hover extends the state to descendants."),
        ("What is the difference between space-x-4 and gap-4 on a flex container?",
         ["They generate exactly the same CSS", "space-x-4 adds horizontal margins between the children, while gap-4 reserves a gutter in the container's layout",
          "gap-4 applies only to block containers", "space-x-4 sets padding on the container"], 1,
         "gap is laid out by the container for flex and grid tracks, whereas the space utilities put margins on the children."),
    ],
    "backend-fastapi": [
        ("In @app.get(\"/items/{item_id}\") with a handler parameter item_id: int, what is item_id?",
         ["A query parameter", "A path parameter", "A request header", "A body field"], 1,
         "Parameters declared inside the path template are path parameters and are required by definition."),
        ("How do you declare an optional query parameter in FastAPI?",
         ["Give the function parameter a default, for example q: str | None = None",
          "Add a ? suffix to the path template", "Use an @app.query decorator",
          "Declare it inside the Pydantic response model"], 0,
         "A parameter with a default becomes an optional query parameter; Path and Query add constraints."),
        ("Which mechanism injects shared logic such as the current user into a route?",
         ["Depends() used as a parameter default", "@app.inject", "Provide() from a DI container",
          "The sub= argument"], 0,
         "Dependencies are callables resolved once per request and may themselves depend on other dependencies."),
        ("In Pydantic v2, which method replaces the old model.dict()?",
         [".to_dict()", ".model_dump()", ".serialize()", ".as_json()"], 1,
         "v2 renamed the API: model_dump() and model_validate() replace dict() and parse_obj()."),
        ("What status code does FastAPI return when a request body fails validation?",
         ["400 Bad Request", "422 Unprocessable Entity", "500 Internal Server Error", "401 Unauthorized"], 1,
         "Pydantic validation errors are reported as 422 with a detailed list of the offending fields."),
        ("How do you run a task such as sending an email after the response has been sent?",
         ["Accept background_tasks: BackgroundTasks and call background_tasks.add_task(fn, *args)",
          "Wrap the call in a threading.Thread inside the handler", "Call asyncio.sleep before returning",
          "Handle it in custom middleware"], 0,
         "BackgroundTasks runs after the response is returned without holding the client connection open."),
        ("GET /users/42 hits def read(user_id: int): return {\"user_id\": user_id}. What is returned?",
         ["422, because the path value is a string", "JSON {\"user_id\": 42} with a number",
          "JSON {\"user_id\": \"42\"} with a string", "404 Not Found"], 1,
         "FastAPI converts and validates the path segment to int, then serializes it back to JSON."),
        ("Why declare an endpoint def instead of async def when it calls a blocking driver like psycopg2?",
         ["FastAPI runs sync handlers in a threadpool so the event loop is not blocked",
          "Sync handlers automatically retry on failure", "async handlers cannot return JSON",
          "There is no practical difference"], 0,
         "Blocking work inside async def stalls every concurrent request; def handlers get their own thread."),
        ("How does a handler stop processing and return 404 to the client?",
         ["raise HTTPException(status_code=404, detail=\"Item not found\")",
          "return {\"error\": \"not found\"}", "@app.on_error(404)", "yield 404"], 0,
         "Raising HTTPException short-circuits the request and FastAPI turns it into the chosen status code and JSON body."),
        ("What does @app.get(\"/users\", response_model=list[UserOut]) guarantee?",
         ["The request body is validated as list[UserOut]", "The status code is forced to 201",
          "Returned objects are filtered to UserOut's fields and the shape is documented in OpenAPI",
          "The response is cached until it expires"], 2,
         "response_model serializes and strips extra fields on output while driving the documented response schema."),
        ("Why must @app.get(\"/items/new\") be registered before @app.get(\"/items/{item_id}\")?",
         ["FastAPI refuses paths that contain a literal segment after a slash",
          "Routes are matched in registration order, so the path template would otherwise capture \"new\"",
          "FastAPI sorts routes alphabetically at startup", "\"new\" is a reserved word in the router"], 1,
         "The first matching route wins, and item_id would accept the string \"new\" if the literal route came later."),
        ("Which declaration reads repeated query strings such as ?tags=python&tags=fastapi into a list?",
         ["tags: str = Query(default=\"\")", "tags: list[str] = Path(default=[])",
          "tags: list[str] = Query(default=\"python\")", "tags: list[str] = Query(default=[])"], 3,
         "A list annotation collects every occurrence of the parameter, and Query supplies a default so it stays optional."),
    ],
    "backend-rest-apis": [
        ("Which statement about PUT and PATCH is correct?",
         ["PUT replaces the whole resource; PATCH applies a partial update",
          "PATCH replaces the whole resource; PUT applies a partial update",
          "They are interchangeable", "PUT may only be used to create resources"], 0,
         "PUT expects a full representation, while PATCH applies a delta such as {\"status\": \"shipped\"}."),
        ("Which HTTP method is NOT idempotent by specification?",
         ["PUT", "DELETE", "GET", "POST"], 3,
         "Repeating POST creates another resource; repeating PUT or DELETE leaves the server in the same state."),
        ("Which status code means a resource was created, often with a representation in the body?",
         ["200 OK", "201 Created", "204 No Content", "302 Found"], 1,
         "201 Created usually accompanies a Location header pointing at the new resource."),
        ("What is the difference between 401 and 403?",
         ["401 means not authenticated; 403 means authenticated but not permitted",
          "403 means not authenticated; 401 means not permitted", "They mean the same thing",
          "401 is used for missing resources"], 0,
         "401 says identify yourself, with a WWW-Authenticate challenge; 403 says the identity is known but access is denied."),
        ("Which pair consists entirely of safe methods, meaning no intended side effects on the server?",
         ["GET and HEAD", "POST and PUT", "DELETE and PATCH", "CONNECT and TRACE"], 0,
         "GET and HEAD are safe, so caches and crawlers may call them freely."),
        ("What does stateless mean in a REST API?",
         ["The server keeps a session object for every client",
          "Each request carries all the information the server needs, and no client session state is stored between requests",
          "Responses must have an empty body", "The API is not allowed to use a database"], 1,
         "Statelessness is what lets you add servers horizontally without sticky sessions."),
        ("Which URI is the most RESTful way to fetch the orders of user 12?",
         ["/users/12/orders", "/getUserOrders?userId=12", "/user_orders_12",
          "/api/v1/order_list?id=12"], 0,
         "Resources are plural nouns in a hierarchy; verbs belong to HTTP methods, not to URLs."),
        ("Which status tells a client its cached copy is still fresh so no body needs to be sent?",
         ["204 No Content", "304 Not Modified", "200 OK", "412 Precondition Failed"], 1,
         "304 answers a conditional request such as If-None-Match with an ETag the client already holds."),
        ("A client posts a JSON document but sets Content-Type: application/xml to an API that only accepts JSON. Which status fits best?",
         ["400 Bad Request", "406 Not Acceptable", "415 Unsupported Media Type", "413 Payload Too Large"], 2,
         "415 rejects the media type of the request body, whereas 406 concerns the Accept header and the response."),
        ("What is the difference between Cache-Control: no-cache and Cache-Control: no-store?",
         ["no-store forbids storing the response, while no-cache forbids reusing it without checking",
          "no-cache allows the response to be stored but requires revalidation before reuse, while no-store forbids storing it",
          "They are identical spellings of the same rule", "no-cache applies only to POST requests"], 1,
         "no-cache still keeps a copy that must be revalidated, whereas no-store means nothing is written to any cache."),
        ("When should an API respond with 409 Conflict?",
         ["The request path does not match any resource", "The caller sent no credentials",
          "The body failed schema validation", "The request clashes with the resource's current state, such as a duplicate unique key"], 3,
         "409 reports a state conflict; missing credentials are 401 and schema failures are 422."),
        ("What is the OPTIONS method for?",
         ["It describes the communication options for the target resource, which is how browsers send the CORS preflight",
          "It permanently deletes a resource", "It fetches only the response headers",
          "It returns a partial representation of the resource"], 0,
         "CORS preflights use OPTIONS to ask which methods and headers are allowed before the real request is sent."),
    ],
    "backend-postgresql": [
        ("Which index type is best for jsonb containment (@>), array containment and full-text search?",
         ["B-tree", "Hash", "GIN", "BRIN"], 2,
         "GIN indexes composite values such as jsonb, arrays and tsvector; B-tree stays the default for scalars."),
        ("What does Atomicity in ACID guarantee?",
         ["A transaction either fully completes or has no effect at all",
          "Data is stored redundantly on disk", "Concurrent transactions behave like a serial run",
          "Committed data survives a crash"], 0,
         "Atomicity is the A of ACID; durability covers surviving crashes and isolation covers serial behaviour."),
        ("Under MVCC, what does a reader see while another transaction updates the same row?",
         ["It blocks until the writer commits", "The previous row version from its snapshot, without blocking the writer",
          "An error immediately", "The uncommitted new version"], 1,
         "Multi-Version Concurrency Control keeps old row versions, so readers and writers never block each other."),
        ("What is the correct role of the HAVING clause?",
         ["Filter rows before grouping", "Filter the groups produced by GROUP BY, typically with aggregate conditions",
          "Sort the result set", "Join two tables together"], 1,
         "WHERE runs before aggregation on individual rows; HAVING runs after aggregation on the groups."),
        ("What does this query return?\nSELECT dept, COUNT(*) FROM employees GROUP BY dept HAVING COUNT(*) > 5;",
         ["Every department together with its employee count", "Only departments that have more than 5 employees",
          "All employees who work in departments with more than 5 people", "Nothing, because HAVING cannot use COUNT"], 1,
         "HAVING keeps only groups whose aggregate exceeds 5, and the count column is not in the select list."),
        ("Which statement about PRIMARY KEY and UNIQUE is true?",
         ["A PRIMARY KEY implies NOT NULL, while a UNIQUE constraint allows multiple NULLs",
          "Both allow multiple NULLs", "A table may have several primary keys",
          "UNIQUE columns cannot be indexed"], 0,
         "PostgreSQL treats NULLs as distinct, so a unique column can hold many NULL values."),
        ("What does ON DELETE CASCADE do on a foreign key?",
         ["Rejects deletion of the referenced parent row",
          "Deletes the child rows when the referenced parent row is deleted",
          "Sets the foreign key to NULL", "Copies the parent row into the child table"], 1,
         "Without a cascade action, deleting a referenced parent raises a foreign key violation."),
        ("An index on (last_name, first_name) can efficiently serve which query?",
         ["WHERE first_name = 'Ann'", "WHERE last_name = 'Smith'", "ORDER BY department",
          "WHERE salary > 100000"], 1,
         "A composite B-tree index is traversed left to right, so the query must use the leading column first."),
        ("What does EXPLAIN (ANALYZE) show that plain EXPLAIN does not?",
         ["The actual rows, time and loop counts measured during a real execution",
          "The names of every index on the table", "The number of dead tuples in the table",
          "A graphical chart of the query plan"], 0,
         "EXPLAIN only prints the planner's estimate, while ANALYZE runs the query and reports what actually happened."),
        ("What is the balance after this runs?\nBEGIN;\nUPDATE accounts SET balance = balance - 100 WHERE id = 1;\nROLLBACK;",
         ["Lower by 100 until the next vacuum", "Higher by 100", "The row is deleted",
          "Unchanged, because ROLLBACK discards the transaction"], 3,
         "Nothing is durable until COMMIT, so ROLLBACK leaves the row exactly as it was."),
        ("What is a partial index, as in CREATE INDEX ... WHERE status = 'active'?",
         ["An index on every row but only a few columns", "An index covering only the rows that match the predicate, so it stays smaller and faster",
          "An index rebuilt automatically every night", "An index usable only by temporary tables"], 1,
         "Queries whose WHERE clause implies the predicate can use it, and the index occupies far less space."),
        ("Why must PostgreSQL run VACUUM?",
         ["To recluster rows physically on disk", "To refresh the planner's statistics only",
          "To reclaim dead row versions and prevent transaction ID wraparound", "To encrypt newly written pages"], 2,
         "Superseded MVCC row versions stay visible until VACUUM removes them; skipping it bloats tables and can stop writes at wraparound."),
    ],
    "backend-sqlalchemy": [
        ("What does a SQLAlchemy Engine represent?",
         ["A pooled set of DBAPI connections plus connection configuration",
          "An open transaction", "The unit of work and identity map", "A single cursor"], 0,
         "The Engine is configuration plus a connection pool; a Session is the unit of work that borrows from it."),
        ("With the default expire_on_commit=True, what happens to ORM objects after session.commit()?",
         ["They stay fully loaded in memory", "Their attributes are expired and refreshed with a SELECT on next access",
          "They are deleted from the database", "They become permanently detached"], 1,
         "Reading an expired attribute issues a fresh query; pass expire_on_commit=False or copy values before committing."),
        ("By default, what happens the first time you access a relationship() attribute on a loaded object?",
         ["It returns None", "It emits a SELECT and lazy-loads the related rows",
          "Everything was already fetched in the initial query", "It raises an error"], 1,
         "Lazy loading is the default strategy, which is convenient but easy to overuse inside loops."),
        ("What is the N+1 query problem and its usual fix?",
         ["One query for the list plus one per row; fix it with joinedload or selectinload",
          "Too many JOINs; fix it by selecting fewer columns", "An infinite recursion in Python",
          "It is solved by adding more indexes"], 0,
         "Eager loading strategies fetch the related rows in the same round trip instead of one at a time."),
        ("Which cascade setting deletes children when the parent is deleted and when they are removed from the parent collection?",
         ["cascade=\"save-update\"", "cascade=\"merge\"", "cascade=\"all, delete-orphan\"",
          "cascade=\"refresh\""], 2,
         "all includes delete, and delete-orphan additionally deletes objects removed from the parent collection."),
        ("Which description matches SQLAlchemy Core?",
         ["Declarative Python classes mapped to tables",
          "Table metadata plus Connection and executable SQL expressions, with no identity map",
          "A database migration tool", "Only the connection pool"], 1,
         "Core is the lower layer the ORM is built on; use it for high-volume reads and ETL-style work."),
        ("What does session.rollback() do?",
         ["Persists every pending change", "Cancels the current transaction and discards unflushed changes",
          "Closes the Session permanently", "Drops the mapped tables"], 1,
         "rollback undoes the transaction, while commit is the call that persists changes."),
        ("What does the Session identity map guarantee?",
         ["All queries are served from memory without touching the database",
          "Within one session, rows with the same primary key map to the same Python object",
          "Objects are shared between separate sessions", "Query results are cached forever"], 1,
         "Identity is per session, which keeps object graphs consistent while avoiding duplicate copies of a row."),
        ("After session.add(user) and before any commit, when does the INSERT reach the database?",
         ["Immediately when add() is called", "Only when session.close() is called",
          "When the session flushes, which happens automatically before commit and before queries that need the pending row",
          "Never, because add() only caches the object in memory"], 2,
         "add() registers the instance in the identity map; the SQL is emitted at flush time, explicitly or implicitly."),
        ("How should Sessions be scoped in a web application?",
         ["One Session per request, created when the request starts and closed when it finishes",
          "A single global Session shared by every request", "A brand new Session for every SELECT",
          "One Session per mapped model class"], 0,
         "Sharing one Session across requests leaks state between them, while a per-query Session loses the identity map entirely."),
        ("After session.close(), what happens when you read an expired attribute on an object returned earlier?",
         ["It returns the value cached in the identity map", "It raises sqlalchemy.exc.OperationalError",
          "It silently returns None", "It raises sqlalchemy.orm.exc.DetachedInstanceError"], 3,
         "A detached instance has no session left to refresh from, so an expired attribute cannot issue the SELECT it needs."),
        ("What does session.scalars(select(User)).all() return in SQLAlchemy 2.x?",
         ["A list of Row objects", "A list of User instances", "A list of dictionaries",
          "The first column of the first row only"], 1,
         "scalars() extracts the first column of each Row, which for an ORM select is the mapped object itself."),
    ],
    "backend-authentication": [
        ("Which parts make up a JSON Web Token?",
         ["header.payload.signature", "header.body", "payload plus a shared secret",
          "username.signature"], 0,
         "The three base64url segments are joined by dots, and the signature proves the token was not tampered with."),
        ("Which statement about HS256 and RS256 is correct?",
         ["HS256 signs and verifies with one shared secret; RS256 signs with a private key and verifies with a public key",
          "RS256 uses a shared secret", "HS256 uses a public and private key pair",
          "Both encrypt the payload"], 0,
         "Signing is not encryption: anyone holding the HS256 secret can forge tokens, while RS256 verifiers cannot."),
        ("Why is bcrypt recommended for storing passwords?",
         ["It is fast and produces deterministic output",
          "It is deliberately slow and uses a per-password salt, resisting rainbow tables and brute force",
          "It is reversible with a key", "It encrypts the password for transport"], 1,
         "bcrypt also truncates its input at 72 bytes, so very long passphrases gain nothing."),
        ("In the OAuth2 password grant used by FastAPI, where does the client send credentials?",
         ["As JSON in the request body", "As form data (application/x-www-form-urlencoded) to the token endpoint",
          "In the URL query string", "As an already-signed JWT"], 1,
         "OAuth2PasswordRequestForm expects username and password fields and returns access_token plus token_type."),
        ("What is the main benefit of refresh tokens?",
         ["They remove the need for HTTPS",
          "The access token can stay short-lived, so a stolen one expires quickly while the refresh token can be rotated and revoked",
          "They replace CORS", "They allow plaintext passwords to be stored"], 1,
         "Short access tokens limit the damage of theft; long-lived refresh tokens should be stored hashed and rotated."),
        ("Why can allow_origins=[\"*\"] not be combined with allow_credentials=True?",
         ["FastAPI forbids it at startup",
          "Browsers reject a wildcard origin for credentialed requests, so the exact origin must be echoed in Access-Control-Allow-Origin",
          "It produces a 500 error", "It is only a linter warning"], 1,
         "The CORS preflight checks that header, and a wildcard never satisfies a credentialed request."),
        ("What does OAuth2PasswordBearer(tokenUrl=\"/token\") hand to the dependency that uses it?",
         ["The decoded username", "The decoded payload", "The raw bearer token string, or a 401 if it is missing",
          "The request body"], 2,
         "It extracts Authorization: Bearer <token> and passes the token on to your get_current_user dependency."),
        ("Where should the JWT signing secret and database credentials live?",
         ["Hardcoded in settings.py for reproducibility",
          "In environment variables or a secret manager, never committed to the repository",
          "In the frontend bundle", "Inside the JWT payload"], 1,
         "Anything in the payload is readable by whoever holds the token, and anything in git is readable forever."),
        ("Which JWT claim holds the expiry time as seconds since the Unix epoch?",
         ["iss", "iat", "exp", "aud"], 2,
         "exp is a NumericDate claim, and the server must reject any token whose exp is already in the past."),
        ("Why is a unique random salt stored with every password hash?",
         ["It makes the hash fast enough for login", "It encrypts the password so support can recover it",
          "It lets the same password produce the same hash for easier lookups",
          "It makes identical passwords hash differently and defeats precomputed rainbow tables"], 3,
         "Without a salt, identical passwords share a hash and attackers reuse tables computed once and kept forever."),
        ("Why does keeping session state in a cookie create a CSRF risk that a Bearer token in the Authorization header avoids?",
         ["The browser attaches cookies to cross-site requests automatically, but never adds an Authorization header on its own",
          "Cookies are stored in plaintext while headers are encrypted", "CSRF only affects GET requests, which tokens disable",
          "Authorization headers are also sent cross-site but with a signature"], 0,
         "A forged form post carries the victim's cookies for free, and the attacker cannot produce a valid bearer header."),
        ("Which OAuth2 flow should a browser-based SPA use against an authorization server?",
         ["Client credentials grant", "Authorization Code flow with PKCE",
          "Resource owner password credentials grant", "Implicit flow"], 1,
         "PKCE binds the code to the client that requested it, while the password grant is deprecated and the implicit flow leaks tokens in the URL."),
    ],
    "backend-deployment": [
        ("What does EXPOSE 8000 in a Dockerfile do?",
         ["Publishes port 8000 to the host", "Documents that the image listens on 8000; the port is still published with -p 8000:8000",
          "Starts the web server", "Configures nginx"], 1,
         "EXPOSE is metadata for humans and tooling; publishing still requires a port mapping at run time."),
        ("What is the relationship between an image and a container?",
         ["A container is a running instance of an image", "An image is a running container",
          "They are the same thing", "An image only contains the operating system"], 0,
         "The image is an immutable template; containers are writable instances of it, and you may run many."),
        ("Why put nginx in front of Uvicorn?",
         ["Because FastAPI cannot speak HTTP", "To terminate TLS, serve static files and proxy requests to application workers",
          "To replace the database", "To compile Python bytecode"], 1,
         "proxy_pass forwards to 127.0.0.1:8000 while nginx handles compression, caching and certificates."),
        ("How should production secrets such as the database URL be provided?",
         ["Baked into the image so every environment matches",
          "At runtime through environment variables from a secret manager, with .env kept out of git",
          "Hardcoded in settings.py", "Bundled into the frontend"], 1,
         "12-factor configuration keeps one image deployable to staging and production without a rebuild."),
        ("Which is a sensible order for a CI pipeline?",
         ["Deploy, commit, test", "Checkout, install dependencies, lint, test, build image, deploy",
          "Test, deploy, build", "Build, deploy, test"], 1,
         "Fail fast on lint and tests before an image is built, and deploy only from a green pipeline."),
        ("Why expose a /health endpoint?",
         ["So orchestrators and load balancers can probe liveness and readiness",
          "To serve the single-page application", "To log user activity", "To bypass authentication"], 0,
         "A failing liveness probe triggers a restart while readiness keeps traffic away from an instance that is not ready."),
        ("How do you run FastAPI in production with several supervised workers?",
         ["python -m http.server", "gunicorn -k uvicorn.workers.UvicornWorker app:app",
          "python app.py", "npm start"], 1,
         "Gunicorn supervises several Uvicorn workers, so crashed workers restart and all CPU cores are used."),
        ("Why start Uvicorn with --proxy-headers behind nginx?",
         ["It compresses responses", "It makes Uvicorn trust X-Forwarded-For and X-Forwarded-Proto so request.client and the scheme reflect the real client",
          "It enables HTTPS termination", "It caches static files"], 1,
         "Without trusted proxy headers every request appears to arrive from 127.0.0.1 over http."),
        ("In a Dockerfile, why COPY requirements.txt . and RUN pip install before COPY . .?",
         ["It removes the need for a .dockerignore", "It keeps secrets out of the final image",
          "It lets the dependency install layer be cached and re-run only when requirements.txt changes",
          "It reduces the image to a single layer"], 2,
         "Layers are reused while their inputs are unchanged, so copying source later does not invalidate the slow install step."),
        ("What does docker compose down -v do?",
         ["Stops the containers and leaves every volume untouched",
          "Stops and removes the containers and networks along with the named volumes declared in the compose file",
          "Deletes only dangling images", "Pauses the services without removing them"], 1,
         "The -v flag is what removes the declared named volumes; without it the data outlives the containers."),
        ("What is a Dockerfile HEALTHCHECK for?",
         ["Letting the runtime poll the container so it can report unhealthy when the probe fails",
          "Scanning the image for known CVEs", "Restarting the container on a fixed schedule",
          "Compiling the application before startup"], 0,
         "The probe runs on an interval and a non-zero exit flips the status to unhealthy, which Compose and orchestrators act on."),
        ("What is blue-green deployment?",
         ["Running the test suite in a green pipeline before merging", "Scaling the application across two regions",
          "Deploying one container per CPU core",
          "Keeping two identical production environments and flipping traffic between them so a bad release rolls back instantly"], 3,
         "Traffic switches from the old environment to the new one atomically, and rollback means switching back."),
    ],
}

IT_LESSONS: dict[str, dict] = {
    "frontend-html": {
        "title": "HTML Foundations",
        "notes": """HTML describes structure and meaning; CSS handles presentation and JavaScript handles behavior. Keep those layers separate and the page stays easy to maintain.

Begin with the skeleton: <!DOCTYPE html> puts the browser into standards mode, then the html element with a lang attribute wraps a head for metadata such as charset, viewport, title and stylesheet links, and a body for visible content. The lang attribute and a viewport meta tag are required for screen readers and for a sane mobile layout.

Choose semantic elements over generic divs: header, nav, main, article, section, aside and footer tell assistive technology and search engines how the page is organized. Use exactly one main per page, article for content that stands alone such as a post or a card, and section for a thematic grouping that normally carries a heading.

- Give every img meaningful alt text, or an empty alt when it is purely decorative.
- Open external links in a new tab with rel="noopener noreferrer".
- Keep heading levels in order: one h1 for the page title, then h2, then h3.

Forms need the most care: pair each control with a label whose for value matches the input id, mark required fields with the required attribute, choose the right type such as email, number or date so native validation and the correct mobile keyboard kick in, and group related controls in a fieldset with a legend. Tables are for tabular data only, using a caption, thead and th scope for headers.

Rule of thumb: reach for native HTML first and add ARIA only when no existing element fits the job.""",
        "examples": [
            "Clicking the label does not focus the input — add a for attribute on the label matching the input id, or wrap the input inside the label.",
            "Screen readers announce every image generically — add descriptive alt text, or an empty alt for purely decorative images so they are skipped.",
            "The form submits empty or malformed values — mark controls with required and the correct type, for example type=\"email\", so native validation blocks bad input.",
        ],
        "practice": [
            "Write the minimal semantic skeleton of an HTML5 page including lang, viewport meta, one main element and correct heading order.",
            "Mark up a login form with a label, a required email input and a submit button, then explain what each attribute contributes.",
            "Take a div-based layout and say which semantic tag should replace each of header, nav, article and footer, and why.",
        ],
        "code": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Profile</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <nav aria-label="Main">
      <ul>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <h1>Jane Doe</h1>
    <form action="/subscribe" method="post">
      <label for="email">Email</label>
      <input id="email" name="email" type="email" required>
      <button type="submit">Subscribe</button>
    </form>
  </main>
</body>
</html>""",
    },
    "frontend-css": {
        "title": "CSS Styling Essentials",
        "notes": """CSS decides how elements look. Three ideas explain most of the language: the cascade, the box model and layout modes.

The cascade resolves conflicts in steps: origin and importance first, then specificity, then source order. Specificity is written as (ID, class, type), so an ID selector beats a class selector, which beats a type selector. When specificity ties, the last rule in the stylesheet wins. A declaration marked !important beats normal declarations regardless of specificity, so use it sparingly and fix the selector instead.

Every element is a box made of content, padding, border and margin. The default box-sizing is content-box, so a declared width of 100px with 10px padding and a 2px border renders 124px wide. Adding a global border-box rule makes width include padding and border, which is what most layouts expect. Adjacent vertical margins collapse to the larger value, while horizontal margins never collapse.

For layout, Flexbox is one-dimensional: display: flex with justify-content along the main axis and align-items across it. CSS Grid is two-dimensional: grid-template-columns with repeat(3, 1fr) plus gap builds rows and columns together. Position absolute removes an element from flow and anchors it to the nearest positioned ancestor, and z-index only reorders elements that create a stacking context.

- Learn the cascade before memorizing utilities.
- Prefer class selectors over IDs so styles stay reusable.
- overflow: hidden clips content and also makes the box scrollable.
- Inspect the box model in dev tools before guessing at widths.""",
        "examples": [
            "A width:100% box overflows its parent — set box-sizing: border-box so padding and border are counted inside the declared width.",
            "A child margin bleeds outside the parent — add overflow: hidden or padding on the parent to contain the collapsed margin.",
            "A row of items wraps unpredictably — use display: flex with gap instead of manual margins, or grid when both rows and columns matter.",
        ],
        "practice": [
            "Calculate the rendered width of a box with box-sizing: content-box, width 200px, padding 15px and a 5px border, and show your working.",
            "Explain in one sentence each when you would reach for Flexbox and when for CSS Grid.",
            "Given #a.b { color: red } and .c { color: blue }, what color renders on <div id=\"a\" class=\"b c\">? Justify with specificity values.",
        ],
        "code": """* { box-sizing: border-box; }

.nav {
  display: flex;
  gap: 16px;
  justify-content: space-between;
  align-items: center;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.card {
  padding: 24px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

@media (max-width: 640px) {
  .grid { grid-template-columns: 1fr; }
}""",
    },
    "frontend-javascript": {
        "title": "JavaScript Core Concepts",
        "notes": """JavaScript is single threaded and driven by an event loop. The mental model is: run the current synchronous code to completion, drain the microtask queue, then take exactly one macrotask.

Values and equality: the triple equals operator compares value and type without coercion, so comparing 0 with an empty string is false, while the loose operator would be true. typeof null returns "object", a legacy quirk. const blocks rebinding, not mutation: you cannot reassign the variable, but you can push into the array it holds.

Scoping and hoisting: var is function-scoped and initialized to undefined when its declaration is hoisted; let and const are block-scoped and stay in the temporal dead zone until the declaration executes, so touching them early throws a ReferenceError. Function declarations are hoisted entirely and can be called before their line runs.

Closures are a function bundled with the lexical environment where it was created. That is why a counter factory can keep a private variable alive between calls, and it is the foundation of module patterns and of React hooks.

Async work: setTimeout is a macrotask, while promise callbacks and await continuations are microtasks, so they always run before a zero-delay timeout. An async function always returns a Promise, and await pauses that function rather than the whole thread until the Promise settles.

- map returns a new array; forEach returns undefined.
- Prefer const by default and let when reassignment is needed.
- Ask for strict equality explicitly instead of relying on implicit coercion.""",
        "examples": [
            "Two setCount(count + 1) calls only add one — use the functional form setCount(prev => prev + 1) so each update reads the latest queued value.",
            "A timeout logs the final value instead of the value at click time — create the timer inside the loop with let so each iteration closes over its own variable.",
            "undefined is not a function on a fetch call — return the promise or await it, since async functions always resolve to a Promise.",
        ],
        "practice": [
            "Predict the console output order for a snippet mixing setTimeout, promise .then and plain logs, then explain microtasks versus macrotasks.",
            "Rewrite a counter that stops incrementing correctly after two rapid updates so that it reaches the expected value.",
            "Explain what a closure is by rewriting a forEach loop so each callback logs its own index without relying on var.",
        ],
        "code": """function createCounter() {
  let count = 0;
  return () => ++count;
}

const next = createCounter();
console.log(next()); // 1
console.log(next()); // 2

console.log(0 === ""); // false
console.log(typeof null); // "object"

async function loadUser(id) {
  const res = await fetch("/api/users/" + id);
  return res.json();
}

console.log("sync");
setTimeout(() => console.log("timeout"), 0);
Promise.resolve().then(() => console.log("microtask"));
// output: sync, microtask, timeout""",
    },
    "frontend-react": {
        "title": "React Fundamentals",
        "notes": """React builds UIs as a function of state: state changes, the component re-renders, and React diffs its virtual tree to apply the smallest possible DOM updates.

Components are plain functions that return JSX. JSX compiles to element creation calls, so expressions live inside braces, and lists need a stable key so React can match old and new items during reconciliation. Index keys break as soon as items are reordered, inserted or removed.

State comes from useState. Updates are queued and applied on the next render, so reading the variable right after calling the setter still gives the old value, and two calls that both add one to the same captured value will not add two. When new state depends on old state, use the functional updater form instead.

Effects live in useEffect with a dependency array: an empty array runs once after mount, a filled array runs whenever a listed value changes, and omitting the array runs after every render, which is usually a bug. The cleanup function returned from the effect runs before the effect re-runs and on unmount, which is where you cancel subscriptions and clear timers.

Rules of Hooks matter: call them at the top level, never inside conditionals, loops or nested functions, and only from function components or custom hooks.

Lifting state up means moving shared state to the closest common ancestor so siblings stay in sync. Prop drilling is fine for a level or two; context or a reducer suits deeper trees. Controlled inputs tie their value to state through onChange, which makes validation and formatting free.""",
        "examples": [
            "List items jump or duplicate after sorting — pass a stable id as key instead of the array index.",
            "State read straight after the setter shows the old value — derive it on the next render or use the functional updater.",
            "A subscription still fires after the component unmounts — return a cleanup function from useEffect to cancel it.",
        ],
        "practice": [
            "List three Rules of Hooks and describe what breaks when one of them is violated.",
            "Write a controlled input that uppercases whatever the user types while they type.",
            "Given useEffect(() => { fetchUser(id) }, []), explain why the effect should depend on [id] instead.",
        ],
        "code": """function SearchBox() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (!query) return;
    const ctrl = new AbortController();
    fetch("/api/search?q=" + query, { signal: ctrl.signal })
      .then((res) => res.json())
      .then(setResults)
      .catch(() => {});
    return () => ctrl.abort();
  }, [query]);

  return (
    <input
      value={query}
      onChange={(event) => setQuery(event.target.value)}
      placeholder="Search"
    />
  );
}""",
    },
    "frontend-tailwind": {
        "title": "Tailwind CSS Utility Styling",
        "notes": """Tailwind is a utility-first CSS framework: you compose styles directly in markup from a fixed set of single-purpose classes, and a build step scans your files to emit only the CSS you actually used.

The spacing scale is the core vocabulary. It runs in quarter-rem steps, so 4px is the unit: m-1 is 4px, m-2 is 8px, m-4 is 16px, and p-4 adds one rem of padding. Anything off the scale is written as an arbitrary value such as w-[137px], which compiles to that exact width. Naming follows a property-value pattern: text-center sets text-align, bg-red-500 sets the background color and font-bold sets font weight.

Variants extend a utility with a state or breakpoint and are written as prefix utility. The default breakpoints are sm at 640px, md at 768px and lg at 1024px, so md:flex applies flex only from 768px upward. hover: applies on pointer hover, focus: on keyboard focus, and dark: requires configuring the dark mode strategy first. Variants stack, for example md:hover:underline.

Layout utilities map straight to CSS: grid plus grid-cols-3 builds a three-column grid, flex items-center justify-between is the classic navigation row, space-x-4 puts margin between sibling children, and hidden paired with md:block shows an element only on larger screens. Because these are ordinary classes, their order in the class attribute does not change the result.

In the Tailwind config file, the content array tells Tailwind which files to scan; forget it and your classes silently vanish from the generated stylesheet.""",
        "examples": [
            "Custom classes produce no CSS — add the source files to the content array in tailwind.config.js so they can be scanned.",
            "A responsive class such as md:flex never appears — check the breakpoint prefix spelling and confirm the file is covered by content.",
            "An element stays hidden on mobile and desktop — pair hidden with md:block instead of relying on display rules elsewhere.",
        ],
        "practice": [
            "Build a responsive card that is stacked on mobile and two columns from the md breakpoint upward, with a hover shadow — write the class list.",
            "Explain what Tailwind's content configuration does and what happens when it is missing.",
            "Convert an arbitrary width like w-[137px] to a scale class and explain the difference between arbitrary and scale values.",
        ],
        "code": """<div class="mx-auto max-w-3xl p-4 md:p-8">
  <header class="flex items-center justify-between gap-4">
    <h1 class="text-2xl font-bold">Dashboard</h1>
    <button class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:ring-2">
      New
    </button>
  </header>
  <div class="mt-6 grid grid-cols-1 gap-4 md:grid-cols-3">
    <div class="hidden rounded border p-4 md:block">Only shown from md upward</div>
  </div>
</div>""",
    },
    "backend-fastapi": {
        "title": "FastAPI Web Framework",
        "notes": """FastAPI is a Python web framework built on Starlette and Pydantic and designed around type hints. Declare the shape of your request and FastAPI validates it, serializes the response and generates OpenAPI documentation for free.

Routes come from decorators. A parameter written inside the path template, such as item_id in /items/{item_id}, is a required path parameter, while a parameter with a default like q: str | None = None becomes an optional query parameter. Import Path and Query from fastapi to add constraints such as ge=1 or min_length=3, and use Header or Cookie for the other locations.

Request bodies are Pydantic models. In Pydantic v2 the API changed: model_validate replaces parse_obj, model_dump replaces dict, and the field_validator decorator replaces the old validator. Validation failures come back as a 422 Unprocessable Entity with a list of the offending fields.

Shared logic such as the current user, a database session or a permission check is injected with Depends as a parameter default. Dependencies are resolved once per request, may cache their result for that request, and may themselves depend on other dependencies, which builds a clean tree of cross-cutting concerns.

async def handlers are awaited on the event loop, so never call blocking libraries such as psycopg2 or requests inside them; a plain def handler runs in a threadpool instead, which is the right home for blocking work. For jobs that should run after the response is sent, accept background_tasks: BackgroundTasks and call add_task. Raise HTTPException to signal errors and set response_model to control and document the output shape.""",
        "examples": [
            "A blocking database call freezes every request — change the endpoint from async def to def so FastAPI runs it in the threadpool.",
            "An optional query parameter returns 422 — give it a default such as q: str | None = None so it becomes optional.",
            "Sending an email delays the response — add a BackgroundTasks parameter and call background_tasks.add_task with your function.",
        ],
        "practice": [
            "Write a GET /items/{item_id} route with an optional q query parameter whose length is at least 2.",
            "Show how to inject a get_current_user dependency into a protected route and where the 401 would be raised.",
            "Explain the difference between async def and def handlers in FastAPI and when each one is correct.",
        ],
        "code": """from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ItemIn(BaseModel):
    name: str
    price: float

def fake_user(x_api_key: str = Header(...)):
    if x_api_key != "secret":
        raise HTTPException(status_code=401, detail="Bad key")
    return {"id": 1}

@app.post("/items", status_code=201)
def create_item(item: ItemIn, user: dict = Depends(fake_user)):
    return {"saved": item.model_dump(), "by": user["id"]}""",
    },
    "backend-rest-apis": {
        "title": "REST API Design",
        "notes": """REST, or Representational State Transfer, is an architectural style rather than a protocol. Its constraints are a uniform interface, stateless communication, cacheable responses, a client-server split and a layered system.

Resources are nouns, so URLs look like /users/12/orders: plural, hierarchical and free of verbs. Verbs belong to HTTP methods. GET reads, POST creates and is not idempotent, PUT replaces a resource and is idempotent, PATCH applies a partial update, and DELETE removes and is idempotent. Repeating a GET, PUT or DELETE leaves the server in the same state; repeating POST creates a second resource, which is why retries need care.

Status codes are a contract with the client. 200 OK for success, 201 Created with a Location header for a new resource, 204 No Content when there is nothing to return, 400 Bad Request for malformed input, 401 Unauthorized when the caller is not authenticated, 403 Forbidden when an authenticated caller lacks permission, 404 Not Found, 409 Conflict for clashing state, 422 for semantic validation failures and 500 for an unhandled server error.

Stateless means every request carries everything the server needs, such as tokens and version information, and the server keeps no session memory between requests. That property is what allows you to add servers horizontally without sticky sessions.

Version the contract when a breaking change arrives, use ETags so clients can send If-None-Match and receive 304 Not Modified, paginate every list endpoint, and return a consistent machine-readable error body. Design for failure too: rate limits, sensible timeouts, and never a stack trace leaking to the client.""",
        "examples": [
            "A retry after a timeout creates duplicate orders — make creation idempotent with an Idempotency-Key header, or retry with PUT instead of POST.",
            "Clients receive 401 where 403 was meant — return 401 when no valid token is present and 403 when the token is valid but lacks permission.",
            "A PATCH wipes fields the client did not send — apply only the provided fields instead of replacing the whole resource.",
        ],
        "practice": [
            "Design the endpoints for creating and listing orders under a user, choosing verbs, paths and status codes for each.",
            "State which HTTP methods are idempotent and explain how a client retry policy depends on that.",
            "Explain the difference between 401 and 403 with a concrete example of each from an API you have used.",
        ],
        "code": """POST   /users/12/orders  -> 201 Created  Location: /orders/981
GET    /orders/981      -> 200 OK
PATCH  /orders/981      -> 200 OK       body: {"status": "shipped"}
PUT    /orders/981      -> 200 OK       full replacement, idempotent
DELETE /orders/981      -> 204 No Content   idempotent
GET    /orders?page=2&page_size=20  -> 200 OK

if-match: "v3"  with  If-None-Match  -> 304 Not Modified
invalid body                              -> 422 Unprocessable Entity
missing token                             -> 401 Unauthorized
valid token, wrong role                   -> 403 Forbidden""",
    },
    "backend-postgresql": {
        "title": "PostgreSQL for Developers",
        "notes": """PostgreSQL is an open source, ACID-compliant relational database with a rich type system and a modern MVCC engine.

ACID means Atomicity, where a transaction either fully commits or fully rolls back, Consistency, where constraints and rules hold after every transaction, Isolation, where concurrent transactions do not corrupt one another, and Durability, where committed data survives a crash. The default isolation level is READ COMMITTED, where each statement sees only rows committed before it started; REPEATABLE READ and SERIALIZABLE are stricter.

MVCC, Multi-Version Concurrency Control, keeps old row versions, so a reader never blocks a writer and a writer never blocks a reader. A reader sees the snapshot taken when its transaction began. Superseded versions become dead rows and are reclaimed by VACUUM, so skipping autovacuum leads to table bloat and slow queries.

Query structure: WHERE filters rows before grouping, aggregate functions run, GROUP BY forms groups, and HAVING filters those groups. That is why HAVING COUNT(*) > 5 returns only departments with more than five employees, while WHERE cannot reference an aggregate at all.

Indexing choices matter. B-tree is the default and suits equality, range and ORDER BY, but a composite index on (last_name, first_name) only helps when the query uses the leftmost column first. GIN indexes jsonb, arrays and full-text search with the containment operator. Hash handles equality on a single column, BRIN suits naturally ordered large tables, and GiST covers geometry and range types.

Constraints are the safety net: a primary key implies NOT NULL and uniqueness, UNIQUE allows multiple NULLs, and a foreign key with ON DELETE CASCADE removes children when the parent goes.""",
        "examples": [
            "A jsonb containment query is slow — create a GIN index on the column instead of a B-tree.",
            "An aggregate query returns the wrong rows — move the condition from WHERE to HAVING when it filters on GROUP BY results.",
            "A delete fails on a foreign key — add ON DELETE CASCADE, or delete the children explicitly in one transaction.",
        ],
        "practice": [
            "Write a query that returns departments with more than 10 employees, then label which clause filters rows and which filters groups.",
            "Choose an index type for a jsonb @> query and justify the choice against the B-tree default.",
            "Explain MVCC in two sentences, including why readers do not block writers and what VACUUM is for.",
        ],
        "code": """CREATE TABLE authors (
  id    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name  text NOT NULL
);

CREATE TABLE books (
  id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  author_id  bigint NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
  title      text NOT NULL,
  tags       text[] NOT NULL DEFAULT '{}'
);

CREATE INDEX books_tags_gin ON books USING gin (tags);

SELECT a.name, COUNT(b.id) AS books
FROM authors a
JOIN books b ON b.author_id = a.id
GROUP BY a.name
HAVING COUNT(b.id) > 3
ORDER BY books DESC;""",
    },
    "backend-sqlalchemy": {
        "title": "SQLAlchemy ORM and Core",
        "notes": """SQLAlchemy offers two layers. Core exposes Table metadata, a Connection and executable expressions such as select, giving you SQL without an object model. The ORM maps declarative classes to tables and manages objects through a Session. Use Core for high-volume reads and ETL-style work, and the ORM for application code that thinks in objects.

The Engine is configuration plus a connection pool, not a connection itself. A Session is a unit of work: it owns a transactional boundary, an identity map and change tracking for the objects it loaded, and it borrows pooled connections as needed.

The usual flow is to create a Session, query, mutate objects, then commit to persist or rollback to discard. With expire_on_commit enabled, which is the default, committing expires the loaded attributes, so the next attribute access issues a fresh SELECT. Move the data you still need before committing, or disable expiry for that session.

Relationships lazy-load by default: touching author.posts emits a SELECT the first time. That scales badly, because you get one query for the list plus one per row, the classic N+1 problem. Fix it with joined loading or selectin loading, either through the relationship's lazy option or options such as selectinload in the query.

Cascade settings on relationship control what propagates. all includes delete, and delete-orphan also removes children that leave the parent collection; otherwise only save-update and merge apply, so deleting a parent with children raises a foreign key violation.

Finally, close releases the connection back to the pool and detaches instances, and the identity map guarantees that within one session a given primary key always maps to the same Python object.""",
        "examples": [
            "Viewing fifty posts fires one hundred and one queries — eager load with selectinload or joinedload to fetch relationships in one round trip.",
            "Attribute access after commit triggers a surprise SELECT — pass expire_on_commit=False, or read the values you need before committing.",
            "Deleting a parent raises a foreign key violation — set cascade to all, delete-orphan on the relationship and consider database-level ON DELETE CASCADE.",
        ],
        "practice": [
            "Describe what happens step by step from Session creation to commit when expire_on_commit is enabled.",
            "Diagnose an N+1 query in a loop over authors and write the eager-loading fix for it.",
            "Explain when you would choose SQLAlchemy Core over the ORM, with one concrete reason.",
        ],
        "code": """from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, Session, mapped_column,
    relationship, selectinload,
)

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    books: Mapped[list["Book"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")

with Session(engine) as session:
    stmt = select(Author).options(selectinload(Author.books))
    authors = session.scalars(stmt).all()
    session.commit()""",
    },
    "backend-authentication": {
        "title": "Authentication and Security",
        "notes": """Authentication answers who are you, while authorization answers what may you do. Keep those two concerns separate in code, because they fail differently.

The usual API flow is: the client posts credentials to a token endpoint, receives a short-lived JWT access token plus a longer-lived refresh token, then sends the access token as an Authorization Bearer header on every request. A JWT is three base64url parts, header, payload and signature, joined by dots. The signature proves integrity but is not encryption, so never put secrets in the payload. HS256 signs and verifies with one shared secret; RS256 signs with a private key and verifies with a public key, which is safer when several services must validate tokens.

Password storage is a different problem and needs hashes, not tokens. bcrypt is deliberately slow, applies a per-password salt and truncates input at 72 bytes, so it resists rainbow tables and brute force far better than a bare SHA-256. Never store, log or return a plaintext password.

Refresh tokens exist because long-lived access tokens are dangerous: a stolen one is usable for hours, whereas a short access token limits the damage and the refresh token can be rotated and revoked server side. Store refresh tokens hashed and rotate them whenever they are used.

CORS is enforced by the browser: a preflight OPTIONS request checks the allowed origin header, and a wildcard origin is rejected whenever credentials are allowed, so echo the exact origin instead. Put signing keys and database URLs in environment variables or a secret manager, and return 401 for missing credentials versus 403 for insufficient permission.""",
        "examples": [
            "Login succeeds but every request returns 401 — send the header exactly as Authorization: Bearer <token> and check the expiry claim.",
            "CORS fails only when credentials are included — replace the wildcard origin with the exact origin the browser sends.",
            "Passwords look weak in the database — hash them with bcrypt and a cost factor, and never log the plaintext.",
        ],
        "practice": [
            "Walk through the OAuth2 password grant from form submission to a bearer token being used on a protected route.",
            "Explain why access tokens should be short-lived and how refresh tokens reduce the risk of a stolen token.",
            "Why is a wildcard origin incompatible with credentialed CORS requests, and what should you send instead?",
        ],
        "code": """from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    if not verify_password(form.username, form.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_jwt(sub=form.username, expires_minutes=15)
    return {"access_token": access, "token_type": "bearer"}

@app.get("/me")
async def me(token: str = Depends(oauth2_scheme)):
    payload = decode_and_check(token)
    return {"username": payload["sub"]}""",
    },
    "backend-deployment": {
        "title": "Deployment and DevOps Basics",
        "notes": """Deployment turns source code into a running service. The modern baseline is: containerize the app, configure it with environment variables, put a reverse proxy in front, and automate the path to production with CI/CD.

A Dockerfile declares how to build an image, an immutable layered snapshot of your app and its dependencies, while a container is a running instance of that image. Order layers from least to most frequently changed, installing dependencies before copying source so caching works, add a .dockerignore, and keep secrets out of the image. EXPOSE only documents the port; you still need a -p mapping to publish it to the host. Multi-stage builds keep the final image small by discarding compilers and build tools.

Configuration belongs in environment variables read at runtime, never hard-coded: one image then runs identically in staging and production, and .env files stay out of git.

In production, run the app behind nginx. It terminates TLS, serves static assets, compresses responses and proxies to application workers with proxy_pass. Run Uvicorn behind Gunicorn using the UvicornWorker worker class so crashed workers restart and every CPU core is used, and enable proxy headers so the application trusts the forwarded client IP and scheme.

Expose a health endpoint so an orchestrator or load balancer can probe liveness and readiness. A basic CI pipeline runs checkout, dependency install, lint, tests and image build, and only then deploys, with secrets taken from the CI secret store and rollbacks kept to a single command.""",
        "examples": [
            "The app works locally but not inside Docker — move configuration to environment variables instead of reading a file baked into the image.",
            "The app sees the proxy IP and an http scheme — start Uvicorn with proxy headers so the forwarded headers from nginx are trusted.",
            "Image rebuilds take minutes — order Dockerfile layers so dependency installation comes before copying source, and add a .dockerignore.",
        ],
        "practice": [
            "Write a two-stage Dockerfile for a FastAPI application and explain what each stage contributes.",
            "Explain what EXPOSE does compared with a -p port mapping, and why both appear in docs and run commands.",
            "Name the steps of a minimal CI pipeline that safely takes a commit all the way into production.",
        ],
        "code": """FROM python:3.11-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=build /usr/local/lib/python3.11/site-packages \\
                   /usr/local/lib/python3.11/site-packages
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", \\
     "-w", "4", "-b", "0.0.0.0:8000", "app.main:app"]

# nginx location block
# location / {
#   proxy_pass http://127.0.0.1:8000;
#   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#   proxy_set_header X-Forwarded-Proto $scheme;
# }""",
    },
}


def get_it(slug: str) -> list[dict]:
    return [
        {"question_text": q, "options": list(opts), "correct_index": idx, "explanation": expl, "difficulty": "beginner"}
        for q, opts, idx, expl in IT_BANKS[slug]
    ]
