import urllib2, base64, json
import codecs, os, sys

if len(sys.argv) != 5:
    print "Usage: python confluence-deveo.py [CONFLUENCE_URL] [CONFLUENCE SPACE KEY] [CONFLUENCE USER] [CONFLUENCE PASSWORD]"
    exit()
CONFLUENCE_URL = sys.argv[1].strip('/')
CONFLUENCE_SPACE = sys.argv[2]
CONFLUENCE_USER = sys.argv[3]
CONFLUENCE_PASSWORD = sys.argv[4]
AUTH_STR = base64.encodestring('%s:%s' % (CONFLUENCE_USER, CONFLUENCE_PASSWORD)).replace('\n', '')


def write_home_page(page_names):
    if not os.path.isfile("./markdown/pages/Home.md"):
        with codecs.open("./markdown/pages/Home.md", "w+") as f:
            f.write("# Imported pages\n\n")
            for page in page_names:
                f.write("* [" + page.replace("%20", " ") + "](wiki-page:" + page.replace("%20", " ") + ")\n")

def request_page(url):
    request = urllib2.Request(url)
    request.add_header("Authorization", "Basic %s" % AUTH_STR)
    return json.load(urllib2.urlopen(request))

def store_attachment(title, link):
    os.system("curl -s -S -o markdown/attachments/" + title.replace(" ", "\ ") + " -u " + CONFLUENCE_USER + ":" + CONFLUENCE_PASSWORD + " " + CONFLUENCE_URL + link)

def get_attachments(id):
    result = request_page(CONFLUENCE_URL + "/rest/api/content/" + id["id"] + "/child/attachment")
    for attachment in result["results"]:
        store_attachment(attachment["title"], attachment["_links"]["download"])

def get_page_content_from_result(id):
    result = request_page(CONFLUENCE_URL + "/rest/api/content/" + id["id"] + "?expand=body.storage")
    write_file(str(result["title"]), result)
    get_attachments(id)

def write_file(file_name, result):
    with codecs.open("./confluence/" + file_name + ".txt", "w+", "utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<!DOCTYPE ac:confluence SYSTEM "../confluence-to-markdown-converter/dtd/confluence-all.dtd" [')
        f.write('<!ENTITY clubs    "&#9827;">')
        f.write('<!ENTITY nbsp   "&#160;">')
        f.write('<!ENTITY ndash   "&#8211;">')
        f.write('<!ENTITY mdash   "&#8212;">')
        f.write(']>')
        f.write('<ac:confluence xmlns:ac="http://www.atlassian.com/schema/confluence/4/ac/" xmlns:ri="http://www.atlassian.com/schema/confluence/4/ri/" xmlns="http://www.atlassian.com/schema/confluence/4/">')
        f.write(result["body"]["storage"]["value"])
        f.write("</ac:confluence>")
    os.system("java -jar confluence-to-markdown-converter/lib/saxon9he.jar -s:./confluence/" + file_name.replace(" ", r"\ ") + ".txt -xsl:confluence-to-markdown-converter/xslt/c2deveo.xsl -o:./markdown/pages/" + file_name.replace(" ", r"\ ") + ".md")

def create_directories():
    os.system("mkdir -p ./confluence")
    os.system("mkdir ./markdown")
    os.system("mkdir ./markdown/pages")
    os.system("mkdir ./markdown/attachments")

if __name__ == '__main__':
    create_directories()
    page_names = []
    for result in request_page(CONFLUENCE_URL + "/rest/api/content?spaceKey=" + CONFLUENCE_SPACE)["results"]:
        get_page_content_from_result(result)
        page_names.append(result["title"])
    write_home_page(page_names)
