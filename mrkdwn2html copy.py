
import re

def mrkdwnEval(stringValue):
    if re.search("^#.*", stringValue):
        return "Head"
    elif re.search("^\* ", stringValue):
        return "List"
    elif re.search(".*\[.*\]\(.*\).*", stringValue):
        return "Link"
    elif re.search(".*\\*\\*.*\\*\\*.*", stringValue) or re.search(".*__.*__.*", stringValue):
        return "Bold"
    else:
        return "Para"

def mrkdwnTitle2html(stringValue):
    for i in range(6,0,-1):
        if re.search( (f"\A{i*'#'}" ), stringValue):
            return f"<h{i}> {mrkdwn2html(stringValue.replace('#',''))} </h{i}>"

def mrkdwnLink2html(stringValue):
    if re.search("^[.*](.*)$", stringValue):
        text,link = [string.replace("[","").replace(")","") for string in stringValue.split("](")]
        return f"<a href={link}>{text}</a>"
    else:
        before = stringValue.split("[")
        text,link = before[1].split(")")[0].split("](")
        after = stringValue.replace(f"{before[0]}[{text}]({link})","")
        if mrkdwnEval(before[0]) != "Para":
            before[0] = mrkdwn2html(before[0])
        if mrkdwnEval(after) != "Para":
            after = mrkdwn2html(after)
        if mrkdwnEval(text) != "Para":
            text = mrkdwn2html(text)
        return f"{before[0]} <a href={link}>{text}</a> {after}"

def mrkdwnBold2html(stringValue):
    if re.search("^\\*\\*.*\\*\\*$", stringValue) or re.search("^__.*__$", stringValue):
        return f"<b>{stringValue.replace('*','').replace('__','')}</b>"
    marker = "**" if "*" in stringValue else "__"
    before, text, after = stringValue.split(marker,2)
    if mrkdwnEval(before) != "Para":
        before = mrkdwn2html(before)
    if mrkdwnEval(after) != "Para":
        after = mrkdwn2html(after)
    if mrkdwnEval(after) != "Para":
        after = mrkdwn2html(after)
    return f"{before}<b>{text}</b>{after}"

def mrkdwn2html(mrkdwn):
    html = ""
    for string in mrkdwn.splitlines():
        if string:
            type = mrkdwnEval(string)
            if type == "Para":
                html = html + f"<p>{string}</p>"
            elif type == "Link":
                html = html + mrkdwnLink2html(string)
            elif type == "Head":
                html = html + mrkdwnTitle2html(string)
            elif type == "Bold":
                html = html + mrkdwnBold2html(string)
            else:
                html = html + f"<li>{string.replace('* ','')}</li>"
    return html
