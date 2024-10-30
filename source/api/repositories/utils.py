def get_or_create_menu(row, menu_map, res_menu):
    menu_id = row['menu_id']
    if menu_id not in menu_map:
        menu = {
            'id': str(menu_id),
            'title': row['menu_title'],
            'description': row['menu_description'],
            'submenus': []
        }
        menu_map[menu_id] = menu
        res_menu.append(menu)
    return menu_map[menu_id]


def get_or_create_submenu(row, menu):
    submenu_map = {submenu['id']: submenu for submenu in menu['submenus']}
    submenu_id = row['submenu_id']
    if submenu_id and submenu_id not in submenu_map:
        submenu = {
            'id': str(submenu_id),
            'title': row['submenu_title'],
            'description': row['submenu_description'],
            'dishes': []
        }
        menu['submenus'].append(submenu)
        submenu_map[submenu_id] = submenu
    return submenu_map.get(submenu_id)


def add_dish_if_unique(row, submenu):
    dish_map = {dish['id'] for dish in submenu['dishes']}
    dish_id = row['dish_id']
    if dish_id and dish_id not in dish_map:
        dish = {
            'id': str(dish_id),
            'title': row['dish_title'],
            'price': str(row['dish_price']),
            'description': row['dish_description']
        }
        submenu['dishes'].append(dish)
