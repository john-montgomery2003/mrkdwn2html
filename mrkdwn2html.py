"""
Code to convert between markdown and html.
This uses re (regex) to find the non printing characters used to denote titles etc in markdown
The program supports:
    - Headers (with #, ##, etc)
    - Bold text
    - Unordered lists
    - Links
    - Paragraphs
"""

import re

def mrkdwnEval(stringValue):
    if re.search("^#.*", stringValue):
        #The # is used to denote a header
        return "Head"
    elif re.search("^\* ", stringValue):
        #The *  is used to denote a UL - note that * character has to be escaped with / as it is a regex expression
        return "List"
    elif re.search(".*\[.*\]\(.*\).*", stringValue):
        #The []() is used to denote a link - note that this can be inside of another Paragraph or other item
        #The functions only goal is to identify the pressence in the string
        return "Link"
    elif re.search(".*\\*\\*.*\\*\\*.*", stringValue) or re.search(".*__.*__.*", stringValue):
        #The ** or __ is used to denote bold - note that this can be inside of another Paragraph
        #The functions only goal is to identify the pressence in the string
        return "Bold"
    else:
        #If none of these exist in the string, we can reasonably assume that it is a simple Paragraph
        return "Para"

def mrkdwnTitle2html(stringValue):
    #Due to the complexity with 6 possible heading sizes, Title conversion has a dedicated function
    #Use a descending list
    for i in range(6,0,-1):
        if re.search( (f"\A{i*'#'}" ), stringValue):
            return f"<h{i}> {mrkdwn2html(stringValue.replace('#',''))} </h{i}>"

def mrkdwnLink2html(stringValue):
    #First test to see if the entire string is a link
    if re.search("^[.*](.*)$", stringValue):
        text,link = [string.replace("[","").replace(")","") for string in stringValue.split("](")]
        return f"<a href={link}>{text}</a>"
    #In this case we can assume that the link is embeded in some other text
    else:
        #Work out the string before the link
        before = stringValue.split("[")
        #Work out href and link text
        text,link = before[1].split(")")[0].split("](")
        #Work out the string after the link
        after = stringValue.replace(f"{before[0]}[{text}]({link})","")
        #Check for additional formatting
        if mrkdwnEval(before[0]) != "Para":
            before[0] = mrkdwn2html(before[0])
        if mrkdwnEval(after) != "Para":
            after = mrkdwn2html(after)
        if mrkdwnEval(text) != "Para":
            text = mrkdwn2html(text)
        #Return final string
        return f"{before[0]} <a href={link}>{text}</a> {after}"

def mrkdwnBold2html(stringValue):
    #Similar to the link function
    #First test to see if the entire string is in bold
    if re.search("^\\*\\*.*\\*\\*$", stringValue) or re.search("^__.*__$", stringValue):
        return f"<b>{stringValue.replace('*','').replace('__','')}</b>"
    #In this case we can assume that the bold is embeded in some other text
    marker = "**" if "*" in stringValue else "__"
    #Due to 2 possible markers for bold
    #Work out before, bold and after text
    before, text, after = stringValue.split(marker,2)
    #Check the new strings for more makers and convert
    if mrkdwnEval(before) != "Para":
        before = mrkdwn2html(before)
    if mrkdwnEval(after) != "Para":
        after = mrkdwn2html(after)
    if mrkdwnEval(after) != "Para":
        after = mrkdwn2html(after)
    return f"{before}<b>{text}</b>{after}"

def mrkdwn2html(mrkdwn):
    #Generate an empty string
    html = ""
    #Loop every line in the string
    for string in mrkdwn.splitlines():
        #Ensure line is not blank, an empty line can be passed
        if string:
            #Evaluate the strings type
            type = mrkdwnEval(string)
            #Perform the conversion
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
    #Return final html
    #NOTE - This does not include headers adn other html formatting
    return html
