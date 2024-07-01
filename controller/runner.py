from config import *

def record_console_errors(data: dict):
    try:
        logging.error(f"""[PAGE ERROR]: {data.name} - {data.message}.\n""")
    except:
        logging.error(f"""Error while recording console errors testing for: {TEST_ID} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))

def prepare_page(page):
    try:
        for module in CAPTURE_MODULES:
            page.add_init_script(path=f"./modules/{module}.js")

        for exposed_function in EXPOSED_MODULES:
            page.expose_function(exposed_function, exposed_function)
    except:
        logging.error(f""" Error while getting preparing page handle with modules - {TEST_ID} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))

def get_page_handle(context: BrowserContext):
    page = None
    try:
        if not context: return
        page = context.new_page()
        page.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
        page.on("pageerror", lambda exception: record_console_errors(exception))
        prepare_page(page)
    except:
        if page: page.close()
        logging.error(f""" Error while getting fresh page handle - {TEST_ID} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))
    return page

def browse(context: BrowserContext, url: str):
    page = None
    try:
        page = get_page_handle(context)
        if not page: raise Exception("Page could not be created!")
        page.goto("https://" + url, **{
            "wait_until": 'load',
            "timeout": CRAWL_TIMEOUT,
        })
        print(f"{page.url}")
        time.sleep(WAIT_TIMEOUT)
        page.close()
    except:
        raise Exception(f"""Couldn't successfully visit - {url} - {'; '.join(str(traceback.format_exc()).split(NEWLINE))}.""")

def get_browser_context(playwright: Playwright):
    context = None
    try:
        if BROWSER == "chrome":
            context = playwright.chromium.launch_persistent_context(f"{TMP_PATH}{TEST_ID}", **CHROMIUM_LAUNCH_ARGS)
        elif BROWSER == "firefox":
            context = playwright.firefox.launch_persistent_context(f"{TMP_PATH}{TEST_ID}", **FIREFOX_LAUNCH_ARGS)
        elif BROWSER == "webkit":
            context = playwright.webkit.launch_persistent_context(f"{TMP_PATH}{TEST_ID}", **CHROMIUM_LAUNCH_ARGS)
        if not context: return None
    except:
        logging.error(f""" Error while instantiating browser context - {TARGET_URL} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))
    return context

def execute_crawl(playwright: Playwright):
    retrial = 0
    try:
        while True:
            try:
                context = get_browser_context(playwright)
                if not context: raise Exception(f"Context could not be created successfuly - {TEST_ID}")
                context.tracing.start(screenshots=True, snapshots=True, sources=True)
                browse(context, TARGET_URL)
                context.tracing.stop(path = f"{TRACE_PATH}/{TEST_ID}.zip")
                context.close()
                break
            except:
                if context: context.close()
                if retrial < ALLOWED_RETRIALS: retrial += 1
                else:
                    logging.error(f"""Couldn't succesfully visit - {TARGET_URL}: %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))
                    break
        if context: context.close()
    except: logging.error(f""" Error while executing crawl - {TARGET_URL} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))

def validate_arguments():
    try:
        if DATASET is None or TEST_ID is None or TARGET_URL is None:
            raise Exception("")
    except:
        logging.error(f""" Invalid arguments passed! : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))
        sys.exit(1)

def init(playwright: Playwright):
    try:
        validate_arguments()
        execute_crawl(playwright)
        playwright.stop()
    except: logging.error(f""" Error in init() - {TEST_ID} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))

with sync_playwright() as playwright:
    init(playwright)
