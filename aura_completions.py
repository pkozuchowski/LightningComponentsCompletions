import sublime, sublime_plugin
import re
from LightningComponentsCompletions.aura_tags import tag_dict as aura_tags

def match(rex, str):
    m = rex.match(str)
    if m:
        return m.group(0)
    else:
        return None

def make_completion(tag, attributes):
    def inc():
        for i in range(1,100):
            yield i

    i = inc()
    required_attributes = [
        '{}="${{{}:{}}}"'.format(attribute, next(i), traits.get("type")) 
        for (attribute, traits) in attributes.items() 
        if traits.get('required', False) == True];

    return (tag + '\tTag', tag +' ' + ' '.join(required_attributes)+ ' ${} >${}</'.format(next(i), next(i)) + tag + '>')

class AuraTagCompletions(sublime_plugin.EventListener):

    # Constructor
    # Generates list of aura tags and tag to attributes dictionary
    def __init__(self):  
        self.prefix_completion_dict = self.default_completion_list()
        self.tag_to_attributes = aura_tags

    def default_completion_list(self):
        default_list = []

        for tag, attributes in aura_tags.items():
            default_list.append(make_completion(tag, attributes))

        prefix_completion_dict = {}

        for s in default_list:
            prefix = s[0][0]
            prefix_completion_dict.setdefault(prefix, []).append(s)

        return prefix_completion_dict

    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "text.html - source - string.quoted"):
            return []

        # check if we are inside a tag
        is_inside_tag = view.match_selector(locations[0],
                "text.html meta.tag - text.html punctuation.definition.tag.begin")

        return self.get_completions(view, prefix, locations, is_inside_tag)

    def get_completions(self, view, prefix, locations, is_inside_tag):
        prefix = self.expand_prefix(view, locations)
        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))


        completion_list = []
        flags = sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS

        if is_inside_tag and ch in [' ', '\t', '\n']:
            completion_list = self.get_attribute_completions(view, locations[0], prefix)
            return (completion_list, flags)

        if prefix == []:
            return ([], flags)

        # match completion list using prefix
        completion_list = self.prefix_completion_dict.get(prefix[0], [])
        # if the opening < is not here insert that
        if ch != '<':
            completion_list = [(pair[0], '<' + pair[1]) for pair in completion_list]

        return (completion_list, flags)


    def expand_prefix(self, view, locations):
        # Get the contents of each line, from the beginning of the line to
        # each point
        lines = [view.substr(sublime.Region(view.line(l).a, l))
            for l in locations]

        # print("lines:", lines)
        # Reverse the contents of each line, to simulate having the regex
        # match backwards
        lines = [l[::-1] for l in lines]

        # Check the first location looks like an expression
        # print('line:', lines[0])
        rex = re.compile("([\w:]+)")
        expr = match(rex, lines[0])

        if not expr:
            return []

        # Ensure that all other lines have identical expressions
        for i in range(1, len(lines)):
            ex = match(rex, lines[i])
            if ex != expr:
                return []

        # Return the completions
        tag = rex.match(expr).groups()[0][::-1]
        return tag

    def get_attribute_completions(self, view, pt, prefix):
        print('get_attribute_completions')
        SEARCH_LIMIT = 500
        search_start = max(0, pt - SEARCH_LIMIT - len(prefix))
        line = view.substr(sublime.Region(search_start, pt + SEARCH_LIMIT))

        line_head = line[0:pt - search_start]
        line_tail = line[pt - search_start:]

        # find the tag from end of line_head
        i = len(line_head) - 1
        tag = None
        space_index = len(line_head)
        while i >= 0:
            c = line_head[i]
            if c == '<':
                # found the open tag
                tag = line_head[i + 1:space_index]
                break
            elif c == ' ':
                space_index = i
            i -= 1

        # check that this tag looks valid
        # 
        if not tag:
            return []

        # determines whether we need to close the tag
        # default to closing the tag
        suffix = '>'

        for c in line_tail:
            if c == '>':
                # found end tag
                suffix = ''
                break
            elif c == '<':
                # found another open tag, need to close this one
                break

        if suffix == '' and not line_tail.startswith(' ') and not line_tail.startswith('>'):
            # add a space if not there
            suffix = ' '

        # got the tag, now find all attributes that match
        attributes = self.tag_to_attributes.get(tag, [])
        # ("class\tAttr", "class="$1">"),
        attri_completions = [ (name + '\t' + type, name + '="${0:'+ type +'}"' + suffix) for name,type in attributes.items()]
        return attri_completions