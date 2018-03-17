#!/usr/bin/env python3
# encoding: utf-8

"""TODO: add docstring"""

# TODO: describe usage

import parser


def generate_activity(template_fn, activity):
    with open(template_fn, 'r') as inp:
        lines = inp.read()

    lines.replace('{{name}}', activity.short_name)
    lines.replace('{{duration}}', activity.date)
    lines.replace('{{logo}}', 'static/ksi.svg')
    lines.replace('{{image}}', 'static/ksi.svg')
    lines.replace('{{gridder-div-id}}', activity.id)
    lines.replace('{{annotation}}', activity.annotation)
    lines.replace('{{link}}', activity.link)

    return lines


def generate_activities(template_fn, output_fn, navbar_fn, page_id,
                        seminars, activities):
    with open(template_fn, 'r') as inp, open(navbar_fn, 'r') as nb, open(output_fn, 'w') as out:
        for line in inp:
            if '{{navbar-fields}}' in line:
                for line in nb:
                    if page_id in line:
                        out.write()
                    else:
                        out.write(line)

            elif '{{seminars}}' in line:
                for activity in seminars:
                    out.write(generate_activity(activity) + '\n')

            elif '{{events}}' in line:
                for activity in events:
                    out.write(generate_activity(activity) + '\n')

            else:
                out.write(line)

if __name__ == '__main__':
    pass
