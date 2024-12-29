import sqlite3
from jinja2 import Environment, FileSystemLoader
import os

def render_html(template_name, **context):
    # Load the template from the 'templates' directory
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    return template.render(context)

def make_html(r1, c1, t_name):
    return render_html(
        "base_templates.html",
        title=f"SQLite Table: {t_name}",
        columns=c1,
        rows=r1,
    )

def main():
    # Database and table details
    db_path = '/Users/netrajoshi/Documents/netra_contacts.db'  # Path to your SQLite database
    table_name = 'contacts'  # Name of the table to export

    # HTML output file
    output_file = 'contacts_main.html'

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query the table
    query = f"SELECT first_name, last_name, phone_num, whatsapp_num, insta_handle, circle_tag_list FROM {table_name} ORDER BY first_name"
    cursor.execute(query)
    columns = [description[0] for description in cursor.description]  # Get column names
    rows = cursor.fetchall()

    # Generate HTML using the base template
    html_content = make_html(rows, columns, table_name)

    # Write to an HTML file
    with open(output_file, 'w') as file:
        file.write(html_content)
    conn.close()
    print(f"HTML file generated: {output_file}")

    # Process tags and generate additional files
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    list_query = f"SELECT circle_tag_list FROM contacts"
    cursor.execute(list_query)
    new_list = cursor.fetchall()
    tag_list = list()

    for i in new_list:
        tag_list.extend(list(i))
    str_list = list(set(','.join(tag_list).split(',')))

    for tag in str_list:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = f"SELECT first_name, last_name, phone_num, whatsapp_num, insta_handle, circle_tag_list FROM {table_name} WHERE circle_tag_list like '%{tag}%' ORDER BY first_name"
        cursor.execute(query)
        cursor_columns = [description[0] for description in cursor.description]  # Get column names
        cursor_rows = cursor.fetchall()
        tag_file = tag + ".html"
        html_content = make_html(cursor_rows, cursor_columns, tag + " " + table_name)
        with open(tag_file, 'w') as new_file:
            new_file.write(html_content)
        cursor.close()

if __name__ == "__main__":
    main()
