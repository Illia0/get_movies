import argparse
import csv
import operator


def get_sort_table_int(table_name, num):
    sort_table = []
    with open(table_name, encoding='utf-8') as r_file:
        table_data = csv.reader(r_file, delimiter=',')
        for row in table_data:
            if str.isdigit(row[num]):
                sort_table.append([int(row[num]), float(row[num+1])])
    sort_table.sort()
    return sort_table


def get_rating(movieid, movie_rating):
    movieid = int(movieid)
    end = len(movie_rating)-1
    end2 = end
    start = 0
    median = 0
    while end >= start:
        median = (end+start)//2
        if movie_rating[median][0] == movieid:
            break
        elif movie_rating[median][0] > movieid:
            end = median-1
        else:
            start = median+1
    all_rating = 0
    count = 0
    while movie_rating[median][0] == movie_rating[median-1][0]:
        median -= 1
    while median+1 <= end2 and movie_rating[median][0] == movie_rating[median+1][0]:
        all_rating += movie_rating[median][1]
        count += 1
        median += 1
    else:
        all_rating += movie_rating[median][1]
        count += 1
    if count == 0 and movie_rating[median][0] == movieid:
        return movie_rating[median][1]
    elif count == 0:
        return 0
    else:
        return all_rating / count


def get_full_table(movies_file, sort_table):
    with open(movies_file, encoding='utf-8') as r_file:
        rating_data = csv.reader(r_file, delimiter=',')
        data_movies = []
        count = 0
        for row in rating_data:
            if count == 0:
                count += 1
            else:
                row[2] = row[2].split('|')
                row.append(get_rating(row[0], sort_table))
                data_movies.append(row)
    data_movies = sorted(data_movies, key=operator.itemgetter(3, 2), reverse=True)
    return data_movies


def get_genres(data_movies):
    all_genre = []
    for i in range(len(data_movies)):
        for j in range(len(data_movies[i][2])):
            if data_movies[i][2][j].lower() not in all_genre:
                all_genre.append(data_movies[i][2][j].lower()  )
    all_genre.sort()
    return all_genre


def only_n_movies(n_movies, data_movies):
    all_genres = get_genres(data_movies)
    for i in range(len(all_genres)):
        count = 0
        print(all_genres[i])
        for j in range(len(data_movies)):
            if count == n_movies:
                break
            for k in range(len(data_movies[j][2])):
                if all_genres[i].lower() == data_movies[j][2][k].lower():
                    print(data_movies[j])
                    count += 1


def n_movies_genre_from_to(n_movies, genre, year_from, year_to, data_movies):
    if n_movies != None and genre == None and year_from == None and year_to == None:
        only_n_movies(n_movies, data_movies)
    if genre == None:
        all_genres = get_genres(data_movies)
    else:
        all_genres = genre.lower().split('|')
    if year_from == None:
        year_from=0
    if year_to == None:
        year_to = 3000
    if n_movies == None :
        n_movies = len(data_movies)
    genre_count = len(all_genres)
    count = 0
    print(genre)
    check_ganre = False
    max_count_genre = 0
    for  i in range(len(data_movies)):
        if len(data_movies[i][2]) > max_count_genre:
            max_count_genre = len(data_movies[i][2])
    if max_count_genre < len(all_genres):
        check_ganre = True
    for j in range(len(data_movies)):
        if count == n_movies:
            break
        lenght = 0
        for k in range(genre_count):
            for l in range(len(data_movies[j][2])):
                if all_genres[k].lower() == data_movies[j][2][l].lower():
                    lenght += 1

        if (check_ganre or lenght == genre_count) and int(data_movies[j][1][-5:-1]) >= year_from and int(
                data_movies[j][1][-5:-1]) <= year_to:
            print(data_movies[j])
            count += 1


def show_table(n_movies=None, genre = None, year_from=None, year_to=None, regexp = None):
    sort_table = get_sort_table_int("ratings.csv", 1)
    pre_data_movies = get_full_table("movies.csv", sort_table)
    data_movies = []
    if regexp != None:
        for row in pre_data_movies:
            caunt = 0
            for i in range(len(regexp)):
                r=regexp[i].lower()
                y=row[1].lower()
                if regexp[i].lower() in row[1].lower():
                    caunt += 1
                if caunt == len(regexp):
                    data_movies.append(row)
    else:
        data_movies = pre_data_movies
    if n_movies == None and genre == None and year_from == None and year_to == None :
        for row in data_movies:
            print(row)
    else:
        n_movies_genre_from_to(n_movies, genre, year_from, year_to, data_movies)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest='n_movies', type=int, help="Number of movies")
    parser.add_argument("-genre", dest='genre', nargs='*', help="Genre of movies")
    parser.add_argument("-year_from", dest='year_from', type=int, help="Schema of parquet file.")
    parser.add_argument("-year_to", dest='year_to', type=int, help="Schema of parquet file.")
    parser.add_argument("-regexp", dest='regexp', nargs='*', help="Name of movie")
    args = parser.parse_args()
    if args.genre != None:
        genre = ''
        for i in range(len(args.genre)):
            genre = genre + args.genre[i] + '|'
        args.genre = genre[:-1]
    show_table(args.n_movies, genre=args.genre, year_to=args.year_to, year_from=args.year_from, regexp=args.regexp)


#py get-movies.py -n 5 -genre Western Horror -year_from 1990 -year_to 2010
#py get-movies.py -regexp love -year_from 2000
