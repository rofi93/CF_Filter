from django import template

register = template.Library()


@register.filter(name='check_division', is_safe=True)
def check_division(contest_info, selected_div):
    divisions = []
    div_number = contest_info.contest.kind.division.number

    if selected_div is None or selected_div == '':
        return True
    if selected_div == 0:
        divisions.append(0)
    else:
        divisions.append(3)
    if selected_div == 1 or selected_div == 3:
        divisions.append(1)
    if selected_div == 2 or selected_div == 3:
        divisions.append(2)

    return div_number in divisions
