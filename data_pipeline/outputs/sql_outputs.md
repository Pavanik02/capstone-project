# SQL Query Log

## 01_select_where
```sql
SELECT title, price_gbp, rating
        FROM books
        WHERE rating >= 4
        ORDER BY rating DESC, price_gbp DESC
        LIMIT 10;
```

| title                                                                    |   price_gbp |   rating |
|:-------------------------------------------------------------------------|------------:|---------:|
| A Flight of Arrows (The Pathfinders #2)                                  |       55.53 |        5 |
| The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1) |       52.3  |        5 |
| A Time of Torment (Charlie Parker #14)                                   |       48.35 |        5 |
| While You Were Mine                                                      |       41.32 |        5 |
| The Red Tent                                                             |       35.66 |        5 |
| Mrs. Houdini                                                             |       30.25 |        5 |
| The Passion of Dolssa                                                    |       28.32 |        5 |
| 1,000 Places to See Before You Die                                       |       26.08 |        5 |
| What Happened on Beale Street (Secrets of the South Mysteries #2)        |       25.37 |        5 |
| The Silkworm (Cormoran Strike #2)                                        |       23.05 |        5 |

## 02_order_by_limit
```sql
SELECT title, price_gbp
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 10;
```

| title                                                                  |   price_gbp |
|:-----------------------------------------------------------------------|------------:|
| Boar Island (Anna Pigeon #19)                                          |       59.48 |
| The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1) |       57.7  |
| A Year in Provence (Provence #1)                                       |       56.88 |
| The Past Never Ends                                                    |       56.5  |
| The Last Painting of Sara de Vos                                       |       55.55 |
| A Flight of Arrows (The Pathfinders #2)                                |       55.53 |
| Murder at the 42nd Street Library (Raymond Ambler #1)                  |       54.36 |
| The Last Mile (Amos Decker #2)                                         |       54.21 |
| 1st to Die (Women's Murder Club #1)                                    |       53.98 |
| Tipping the Velvet                                                     |       53.74 |

## 03_distinct_categories
```sql
SELECT DISTINCT category_name
        FROM categories
        ORDER BY category_name;
```

| category_name      |
|:-------------------|
| Historical Fiction |
| Mystery            |
| Travel             |

## 04_between_prices
```sql
SELECT title, price_gbp, price_inr
        FROM books
        WHERE price_gbp BETWEEN 10 AND 30
        ORDER BY price_gbp;
```

| title                                                                                             |   price_gbp |   price_inr |
|:--------------------------------------------------------------------------------------------------|------------:|------------:|
| Tastes Like Fear (DI Marnie Rome #3)                                                              |       10.69 |     1127.79 |
| Hide Away (Eve Duncan #20)                                                                        |       11.84 |     1249.12 |
| The Girl You Lost                                                                                 |       12.29 |     1296.59 |
| Playing with Fire                                                                                 |       13.71 |     1446.41 |
| That Darkness (Gardiner and Renner #1)                                                            |       13.92 |     1468.56 |
| The Girl In The Ice (DCI Erika Foster #1)                                                         |       15.85 |     1672.17 |
| The Constant Princess (The Tudor Court #1)                                                        |       16.62 |     1753.41 |
| A Murder in Time                                                                                  |       16.64 |     1755.52 |
| A Study in Scarlet (Sherlock Holmes #1)                                                           |       16.73 |     1765.02 |
| A Spy's Devotion (The Regency Spies of London #1)                                                 |       16.97 |     1790.33 |
| Lilac Girls                                                                                       |       17.28 |     1823.04 |
| The Cuckoo's Calling (Cormoran Strike #1)                                                         |       19.21 |     2026.66 |
| In a Dark, Dark Wood                                                                              |       19.63 |     2070.96 |
| Blood Defense (Samantha Brinkman #1)                                                              |       20.3  |     2141.65 |
| Love, Lies and Spies                                                                              |       20.55 |     2168.03 |
| Between Shades of Gray                                                                            |       20.79 |     2193.34 |
| Delivering the Truth (Quaker Midwife Mystery #1)                                                  |       20.89 |     2203.89 |
| Voyager (Outlander #3)                                                                            |       21.07 |     2222.89 |
| The Silkworm (Cormoran Strike #2)                                                                 |       23.05 |     2431.78 |
| The Road to Little Dribbling: Adventures of an American in Britain (Notes From a Small Island #2) |       23.21 |     2448.66 |
| Career of Evil (Cormoran Strike #3)                                                               |       24.72 |     2607.96 |
| The Mysterious Affair at Styles (Hercule Poirot #1)                                               |       24.8  |     2616.4  |
| What Happened on Beale Street (Secrets of the South Mysteries #2)                                 |       25.37 |     2676.54 |
| Extreme Prey (Lucas Davenport #26)                                                                |       25.4  |     2679.7  |
| Starlark                                                                                          |       25.83 |     2725.06 |
| 1,000 Places to See Before You Die                                                                |       26.08 |     2751.44 |
| Girl With a Pearl Earring                                                                         |       26.77 |     2824.24 |
| Poisonous (Max Revere Novels #3)                                                                  |       26.8  |     2827.4  |
| The Widow                                                                                         |       27.26 |     2875.93 |
| Lost Among the Living                                                                             |       27.7  |     2922.35 |
| The Marriage of Opposites                                                                         |       28.08 |     2962.44 |
| The Passion of Dolssa                                                                             |       28.32 |     2987.76 |
| Forever and Forever: The Courtship of Henry Longfellow and Fanny Appleton                         |       29.69 |     3132.3  |

## 05_in_ratings
```sql
SELECT title, rating, in_stock
        FROM books
        WHERE rating IN (4, 5)
        ORDER BY rating DESC, title
        LIMIT 15;
```

| title                                                                    |   rating |   in_stock |
|:-------------------------------------------------------------------------|---------:|-----------:|
| 1,000 Places to See Before You Die                                       |        5 |          1 |
| A Flight of Arrows (The Pathfinders #2)                                  |        5 |          1 |
| A Spy's Devotion (The Regency Spies of London #1)                        |        5 |          1 |
| A Time of Torment (Charlie Parker #14)                                   |        5 |          1 |
| Between Shades of Gray                                                   |        5 |          1 |
| Mrs. Houdini                                                             |        5 |          1 |
| The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1) |        5 |          1 |
| The Girl You Lost                                                        |        5 |          1 |
| The Passion of Dolssa                                                    |        5 |          1 |
| The Red Tent                                                             |        5 |          1 |
| The Silkworm (Cormoran Strike #2)                                        |        5 |          1 |
| Voyager (Outlander #3)                                                   |        5 |          1 |
| What Happened on Beale Street (Secrets of the South Mysteries #2)        |        5 |          1 |
| While You Were Mine                                                      |        5 |          1 |
| A Paris Apartment                                                        |        4 |          1 |

## 06_join_category
```sql
SELECT c.category_name, b.title, b.rating, b.price_gbp, b.in_stock
        FROM books AS b
        JOIN categories AS c
          ON b.category_id = c.category_id
        WHERE b.rating >= 4
        ORDER BY c.category_name, b.rating DESC, b.title
        LIMIT 20;
```

| category_name      | title                                                                    |   rating |   price_gbp |   in_stock |
|:-------------------|:-------------------------------------------------------------------------|---------:|------------:|-----------:|
| Historical Fiction | A Flight of Arrows (The Pathfinders #2)                                  |        5 |       55.53 |          1 |
| Historical Fiction | A Spy's Devotion (The Regency Spies of London #1)                        |        5 |       16.97 |          1 |
| Historical Fiction | Between Shades of Gray                                                   |        5 |       20.79 |          1 |
| Historical Fiction | Mrs. Houdini                                                             |        5 |       30.25 |          1 |
| Historical Fiction | The Passion of Dolssa                                                    |        5 |       28.32 |          1 |
| Historical Fiction | The Red Tent                                                             |        5 |       35.66 |          1 |
| Historical Fiction | Voyager (Outlander #3)                                                   |        5 |       21.07 |          1 |
| Historical Fiction | While You Were Mine                                                      |        5 |       41.32 |          1 |
| Historical Fiction | A Paris Apartment                                                        |        4 |       39.01 |          1 |
| Historical Fiction | Lost Among the Living                                                    |        4 |       27.7  |          1 |
| Historical Fiction | The Marriage of Opposites                                                |        4 |       28.08 |          1 |
| Historical Fiction | World Without End (The Pillars of the Earth #2)                          |        4 |       32.97 |          1 |
| Mystery            | A Time of Torment (Charlie Parker #14)                                   |        5 |       48.35 |          1 |
| Mystery            | The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1) |        5 |       52.3  |          1 |
| Mystery            | The Girl You Lost                                                        |        5 |       12.29 |          1 |
| Mystery            | The Silkworm (Cormoran Strike #2)                                        |        5 |       23.05 |          1 |
| Mystery            | What Happened on Beale Street (Secrets of the South Mysteries #2)        |        5 |       25.37 |          1 |
| Mystery            | Delivering the Truth (Quaker Midwife Mystery #1)                         |        4 |       20.89 |          1 |
| Mystery            | Murder at the 42nd Street Library (Raymond Ambler #1)                    |        4 |       54.36 |          1 |
| Mystery            | Sharp Objects                                                            |        4 |       47.82 |          1 |

## 07_stock_filter
```sql
SELECT title, price_gbp, in_stock
        FROM books
        WHERE in_stock = 1
        ORDER BY price_gbp ASC
        LIMIT 15;
```

| title                                             |   price_gbp |   in_stock |
|:--------------------------------------------------|------------:|-----------:|
| Tastes Like Fear (DI Marnie Rome #3)              |       10.69 |          1 |
| Hide Away (Eve Duncan #20)                        |       11.84 |          1 |
| The Girl You Lost                                 |       12.29 |          1 |
| Playing with Fire                                 |       13.71 |          1 |
| That Darkness (Gardiner and Renner #1)            |       13.92 |          1 |
| The Girl In The Ice (DCI Erika Foster #1)         |       15.85 |          1 |
| The Constant Princess (The Tudor Court #1)        |       16.62 |          1 |
| A Murder in Time                                  |       16.64 |          1 |
| A Study in Scarlet (Sherlock Holmes #1)           |       16.73 |          1 |
| A Spy's Devotion (The Regency Spies of London #1) |       16.97 |          1 |
| Lilac Girls                                       |       17.28 |          1 |
| The Cuckoo's Calling (Cormoran Strike #1)         |       19.21 |          1 |
| In a Dark, Dark Wood                              |       19.63 |          1 |
| Blood Defense (Samantha Brinkman #1)              |       20.3  |          1 |
| Love, Lies and Spies                              |       20.55 |          1 |

## 08_category_counts
```sql
SELECT c.category_name, COUNT(*) AS book_count
        FROM categories AS c
        JOIN books AS b ON b.category_id = c.category_id
        GROUP BY c.category_id, c.category_name
        ORDER BY book_count DESC, c.category_name;
```

| category_name      |   book_count |
|:-------------------|-------------:|
| Mystery            |           32 |
| Historical Fiction |           26 |
| Travel             |           11 |

## Acceptance summary

- Book count: `69`
- Category count: `3`

## SQL JOIN vs pandas merge

### `pd.read_sql` result
| category_name      | title                                                                    |   rating |   price_gbp | in_stock   |
|:-------------------|:-------------------------------------------------------------------------|---------:|------------:|:-----------|
| Historical Fiction | A Flight of Arrows (The Pathfinders #2)                                  |        5 |       55.53 | True       |
| Historical Fiction | A Spy's Devotion (The Regency Spies of London #1)                        |        5 |       16.97 | True       |
| Historical Fiction | Between Shades of Gray                                                   |        5 |       20.79 | True       |
| Historical Fiction | Mrs. Houdini                                                             |        5 |       30.25 | True       |
| Historical Fiction | The Passion of Dolssa                                                    |        5 |       28.32 | True       |
| Historical Fiction | The Red Tent                                                             |        5 |       35.66 | True       |
| Historical Fiction | Voyager (Outlander #3)                                                   |        5 |       21.07 | True       |
| Historical Fiction | While You Were Mine                                                      |        5 |       41.32 | True       |
| Historical Fiction | A Paris Apartment                                                        |        4 |       39.01 | True       |
| Historical Fiction | Lost Among the Living                                                    |        4 |       27.7  | True       |
| Historical Fiction | The Marriage of Opposites                                                |        4 |       28.08 | True       |
| Historical Fiction | World Without End (The Pillars of the Earth #2)                          |        4 |       32.97 | True       |
| Mystery            | A Time of Torment (Charlie Parker #14)                                   |        5 |       48.35 | True       |
| Mystery            | The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1) |        5 |       52.3  | True       |
| Mystery            | The Girl You Lost                                                        |        5 |       12.29 | True       |
| Mystery            | The Silkworm (Cormoran Strike #2)                                        |        5 |       23.05 | True       |
| Mystery            | What Happened on Beale Street (Secrets of the South Mysteries #2)        |        5 |       25.37 | True       |
| Mystery            | Delivering the Truth (Quaker Midwife Mystery #1)                         |        4 |       20.89 | True       |
| Mystery            | Murder at the 42nd Street Library (Raymond Ambler #1)                    |        4 |       54.36 | True       |
| Mystery            | Sharp Objects                                                            |        4 |       47.82 | True       |

### `pd.merge` result
| category_name      | title                                                                    |   rating |   price_gbp | in_stock   |
|:-------------------|:-------------------------------------------------------------------------|---------:|------------:|:-----------|
| Historical Fiction | A Flight of Arrows (The Pathfinders #2)                                  |        5 |       55.53 | True       |
| Historical Fiction | A Spy's Devotion (The Regency Spies of London #1)                        |        5 |       16.97 | True       |
| Historical Fiction | Between Shades of Gray                                                   |        5 |       20.79 | True       |
| Historical Fiction | Mrs. Houdini                                                             |        5 |       30.25 | True       |
| Historical Fiction | The Passion of Dolssa                                                    |        5 |       28.32 | True       |
| Historical Fiction | The Red Tent                                                             |        5 |       35.66 | True       |
| Historical Fiction | Voyager (Outlander #3)                                                   |        5 |       21.07 | True       |
| Historical Fiction | While You Were Mine                                                      |        5 |       41.32 | True       |
| Historical Fiction | A Paris Apartment                                                        |        4 |       39.01 | True       |
| Historical Fiction | Lost Among the Living                                                    |        4 |       27.7  | True       |
| Historical Fiction | The Marriage of Opposites                                                |        4 |       28.08 | True       |
| Historical Fiction | World Without End (The Pillars of the Earth #2)                          |        4 |       32.97 | True       |
| Mystery            | A Time of Torment (Charlie Parker #14)                                   |        5 |       48.35 | True       |
| Mystery            | The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1) |        5 |       52.3  | True       |
| Mystery            | The Girl You Lost                                                        |        5 |       12.29 | True       |
| Mystery            | The Silkworm (Cormoran Strike #2)                                        |        5 |       23.05 | True       |
| Mystery            | What Happened on Beale Street (Secrets of the South Mysteries #2)        |        5 |       25.37 | True       |
| Mystery            | Delivering the Truth (Quaker Midwife Mystery #1)                         |        4 |       20.89 | True       |
| Mystery            | Murder at the 42nd Street Library (Raymond Ambler #1)                    |        4 |       54.36 | True       |
| Mystery            | Sharp Objects                                                            |        4 |       47.82 | True       |

**Equivalent after column/type normalization:** `True`
