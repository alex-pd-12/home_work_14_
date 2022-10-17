import json
import sqlite3
from flask import Flask, jsonify


def run_sql(sql):
    ''' Запрос '''
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = []
        for item in connection.execute(sql).fetchall():
            result.append(dict(item))

        return result


app = Flask(__name__)


@app.route("/movie/<title>", methods=["Get", "POST"])
def step_1(title):
    sql = f'''select title, country, release_year, listed_in as genre, description 
              from netflix 
              where title='{title}'
              order by date_added desc
              limit 1
              '''
    result = run_sql(sql)
    if result:
        result = result[0]

    return jsonify(result)


@app.route("/movie/<int:year1>/to/<int:year2>")
def step_2(year1, year2):
    sql = f'''select title,  release_year
             from netflix
             where release_year between {year1} and {year2}
             '''
    return jsonify(run_sql(sql))


@app.route("/rating/<rating>")
def ste_3(rating):
    my_dict = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    sql = f'''
                select title, rating, description
                from netflix
                where rating in {my_dict.get(rating, ("PG-13", "NC-17"))}
                '''

    return jsonify(run_sql(sql))


@app.route("/genre/<genre>")
def step_4(genre):
    sql = f'''
            select * 
            from netflix
            where listed_in LIKE '%{genre.title()}%'
            '''
    return jsonify(run_sql(sql))


def step_5(name1='Rose McIver', name2='Ben Lamb'):
    ''' Шаг 5ый по заданию '''
    sql = f'''
            select "cast" 
            from netflix
            where "cast" LIKE '%{name1}%' and "cast" LIKE '%{name2}%'
            '''
    result = run_sql(sql)

    main_name = {}
    for item in result:
        names = item.get('cast').split(', ')
        for name in names:
            if name in main_name.keys():
                main_name[name] += 1
            else:
                main_name[name] = 1

    print(main_name)
    for item in main_name:
        if item not in (name1, name2) and main_name[item] > 2:
            print(item)


def step_6(types='TV Show', release_year=2021, genre='TV'):
    '''Шаг 6'''
    sql = f'''
            select * from netflix
            where type = '{types}'
            and release_year = '{release_year}'
            and listed_in LIKE '%{genre}%'
            '''
    return json.dumps(run_sql(sql), indent=4, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host="localhost", debug=True, port=5432)
