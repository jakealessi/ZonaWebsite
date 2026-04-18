#!/usr/bin/env python3
"""Generate js/menu-data.js from structured line blocks (name|description)."""
import json
import os
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def items_from_block(block):
    out = []
    for raw in block.strip().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            name, desc = line.split("|", 1)
            out.append({"name": name.strip(), "desc": desc.strip()})
        else:
            out.append({"name": line, "desc": ""})
    return out


def section(title, intro=None, block=None, groups=None):
    s = {"title": title}
    if intro:
        s["intro"] = intro
    if block:
        s["items"] = items_from_block(block)
    if groups:
        s["groups"] = groups
    return s


def grp(title, block, note=None):
    g = {"groupTitle": title, "items": items_from_block(block)}
    if note:
        g["note"] = note
    return g


DINING = [
    section(
        "Starters — Appetizers",
        block=textwrap.dedent(
            """
            Baked Clams Oreganata|
            Fried or Grilled Calamari|Served with marinara sauce.
            Mozzarella Sticks|Served with marinara sauce.
            Sicilian Rice Balls|Served with marinara sauce.
            Buffalo Wings|
            Hot Antipasto|Baked clams, shrimp oreganata & eggplant rollatini.
            Mussels|Served in marinara or white garlic sauce.
            Spinach & Artichoke Bruschetta|
            """
        ),
    ),
    section(
        "Bruschetta Crostini",
        block=textwrap.dedent(
            """
            Classica|Fresh tomatoes, garlic & basil.
            Pomodorino|Roasted cherry tomatoes & fresh mozzarella.
            Shrimp|Fresh tomatoes, garlic & basil topped with grilled shrimp.
            Eggplant|Fresh tomatoes, garlic & basil topped with grilled eggplant.
            Roasted Peppers|Fresh tomatoes, garlic & basil topped with sliced roasted peppers.
            """
        ),
    ),
    section(
        "Soups",
        block=textwrap.dedent(
            """
            Butternut Squash|
            Chicken Pastina|
            Pasta Fagioli|
            Tortellini|
            Cavatelli with Chicken & Spinach|
            Lentil|
            Stracciatella Romana|
            """
        ),
    ),
    section(
        "Panini & Sandwiches",
        intro="Semolina loaves, ciabatta, rustic bread, krispina, and whole wheat as listed.",
        groups=[
            grp(
                "Old Fashioned Italian Sandwiches",
                textwrap.dedent(
                    """
                    Potatoes & Eggs|Scrambled eggs, potatoes, grilled onion & fresh mozzarella on semolina loaf.
                    Sausage & Peppers|Sweet Italian sausage, Italian peppers & onions on semolina loaf.
                    Peppers & Eggs|Scrambled eggs, Italian peppers & onions on semolina loaf.
                    """
                ),
                note="Served on semolina loaves.",
            ),
            grp(
                "Beef Panini or Wrap",
                textwrap.dedent(
                    """
                    Bistecca|Pan seared filet mignon, sautéed Spanish onions & smoked mozzarella on ciabatta.
                    Bistecca Mozzarella|Pan seared filet mignon, fresh mozzarella & roasted peppers on ciabatta.
                    Hamburger Classica|Homemade burger with spicy mayo, red onions, fresh mozzarella, tomato & arugula on round rustic bread.
                    Meatball Parmigiana|Homemade meatballs, fresh mozzarella & marinara sauce on ciabatta.
                    Bistecca Funghi|Pan seared filet mignon, fontina cheese & sautéed mushrooms on ciabatta.
                    Philly Cheese Steak|Pan seared filet mignon, sautéed mushrooms, roasted red onions & cheddar cheese on ciabatta.
                    Hamburger Moderna|Homemade burger with sautéed onions, mushrooms, fresh mozzarella, mixed greens, bacon, fresh tomatoes & spicy artichoke sauce on round rustic bread.
                    """
                ),
            ),
            grp(
                "Chicken Cutlet Panini or Wrap",
                textwrap.dedent(
                    """
                    Ancona|Chicken cutlet, fresh mozzarella, spicy peppers, mixed greens & tomato on ciabatta.
                    Chicken Parmigiana|Chicken cutlet, fresh mozzarella & marinara sauce on ciabatta.
                    Pepperoni|Chicken cutlet, red onions, fresh mozzarella & roasted peppers on ciabatta.
                    Prato|Chicken cutlet, pepper jack cheese, roasted red onions, sweet peppers & artichoke sauce on ciabatta.
                    Buffalo Chicken|Chicken cutlet, crumbled gorgonzola cheese, fresh mozzarella & buffalo sauce on ciabatta.
                    Cotoletta|Chicken cutlet, fresh mozzarella, tomatoes, red onion & herb mayo on ciabatta.
                    Piccante|Chicken cutlet, fresh mozzarella, spicy mayo & mixed greens on ciabatta.
                    Nova|Chicken cutlet, herb mayo, roasted peppers, mixed greens & fresh mozzarella on ciabatta.
                    """
                ),
            ),
            grp(
                "Grilled Chicken Panini or Wrap",
                textwrap.dedent(
                    """
                    Cuneo|Grilled chicken, fresh mozzarella, grilled zucchini & roasted peppers on ciabatta.
                    Perugia|Grilled chicken, guacamole, chopped iceberg lettuce & fresh mozzarella on a rustic hero.
                    The Ryan|Grilled chicken, fresh mozzarella, baby arugula & balsamic on krispina.
                    UConn|Grilled chicken, ham, fresh mozzarella & baby arugula on krispina.
                    Trieste|Grilled chicken, black olive paste, grilled zucchini & fresh mozzarella on ciabatta.
                    Grilled Chicken BLT|Grilled chicken, bacon, herb mayo, iceberg lettuce, tomatoes & fontina cheese on ciabatta.
                    Pollo|Grilled chicken, broccoli rabe & smoked mozzarella on ciabatta.
                    Savona|Grilled chicken, fresh mozzarella, tomatoes & roasted garlic aioli on ciabatta.
                    Viola|Grilled chicken, sun dried tomatoes, artichokes, basil pesto & fresh mozzarella on ciabatta.
                    Udine|Grilled chicken, roasted red onions, fresh mozzarella & tomatoes on ciabatta.
                    """
                ),
            ),
            grp(
                "Cured Meat Panini or Wrap",
                textwrap.dedent(
                    """
                    Caltanissetta|Sopressata, fontina cheese, hot peppers, tomatoes & baby arugula on ciabatta.
                    Greg|Prosciutto, mozzarella, onion, olives, hot peppers, sun dried tomatoes & salsa cocktail on ciabatta.
                    Prosciutto|Prosciutto, fresh mozzarella & tomatoes on ciabatta.
                    Crudo|Prosciutto, fresh mozzarella & baby arugula on ciabatta.
                    Nuzzi|Ham, fresh mozzarella, tomatoes, herb mayo, romaine lettuce, sweet peppers & balsamic on ciabatta.
                    """
                ),
            ),
            grp(
                "Pork Panini or Wrap",
                textwrap.dedent(
                    """
                    Ascoli|Roasted pork tenderloin, fresh mozzarella, broccoli rabe & spicy peppers on round rustic bread.
                    Gela|Roasted pork tenderloin, provolone cheese, roasted peppers & baby arugula on round rustic bread.
                    Torino|Sweet Italian pork sausage, fresh mozzarella, roasted tomatoes & arugula on round rustic bread.
                    Cuban|Roasted pork tenderloin, salsa cocktail, ham & provolone on ciabatta.
                    Sardegna|Sweet Italian pork sausage, fresh mozzarella & roasted hot peppers on round rustic bread.
                    Trentino|Roasted pork tenderloin, sautéed mushrooms & smoked mozzarella on round rustic bread.
                    """
                ),
            ),
            grp(
                "Roasted Turkey Panini or Wrap",
                textwrap.dedent(
                    """
                    Crotone|Fresh roasted turkey, sautéed mushrooms, roasted red onions & fontina on a rustic hero.
                    Salerno|Fresh roasted turkey, chopped iceberg, tomato, fontina cheese & guacamole on a rustic hero.
                    Sophia Loren|Fresh roasted turkey, spicy-honey pepper sauce, caramelized onions & cheddar cheese on krispina.
                    Frosinone|Fresh roasted turkey, crispy bacon, smoked mozzarella, sautéed onion & herb mayo on krispina.
                    San Remo|Fresh roasted turkey, fresh mozzarella, roasted hot peppers & guacamole on ciabatta.
                    """
                ),
            ),
            grp(
                "Shrimp Panini or Wrap",
                textwrap.dedent(
                    """
                    Alex|Fried shrimp, fresh mozzarella, tomatoes & romaine lettuce on ciabatta.
                    Augusta|Grilled shrimp, black olive paste, fontina cheese & sliced tomato on ciabatta.
                    Asti|Grilled jumbo shrimp, broccoli rabe, fresh mozzarella & hot peppers on ciabatta.
                    Shrimp Parmigiana|Fried shrimp, fresh mozzarella & marinara on ciabatta.
                    """
                ),
            ),
            grp(
                "Vegetarian Panini or Wrap",
                textwrap.dedent(
                    """
                    Eggplant Parmigiana|Fried eggplant, fresh mozzarella & marinara sauce on ciabatta.
                    Portobello|Oven roasted portobello, fresh mozzarella & tomatoes on whole wheat.
                    Quattro Formaggi|Brie, fontina, fresh mozzarella & asiago, grilled zucchini & roasted spicy peppers on round rustic bread.
                    Sierra|Fresh mozzarella, tomato, fresh basil, extra virgin olive oil & balsamic on krispina.
                    Foggia|Fried eggplant, smoked mozzarella, sun dried tomatoes & olive paste on krispina.
                    Potenza|Fried eggplant, fresh mozzarella, tomato & fresh basil on krispina.
                    Sicilia|Fried eggplant, fresh mozzarella & roasted peppers on krispina.
                    Terra|Roasted portobello, broccoli rabe, roasted peppers, grilled vegetables & asiago on whole wheat.
                    """
                ),
            ),
        ],
    ),
]

# Salads — dining (full list from user)
DINING.append(
    section(
        "Salad Creations — Salads",
        groups=[
            grp(
                "Salads",
                textwrap.dedent(
                    """
                    Bacon|Baby spinach, gorgonzola, red onion, red pears, candied walnuts & crispy bacon with honey dijon dressing.
                    Brooklyn|Iceberg lettuce, tomatoes, cucumber, black olives & red onions with oil and white vinegar.
                    Chef Classic|Mixed greens, gorgonzola, dried cranberries, red pears & candied walnuts with balsamic dressing.
                    Greek|Baby greens, grape tomatoes, cucumbers, kalamata olives, feta, red peppers & onions with oil and vinegar.
                    Insalata Di Stagione|Mixed greens, tomatoes, carrots & cucumbers with balsamic vinaigrette.
                    Insalata Con Funghi|Mixed greens, roasted portobello, roasted peppers, sunflower seeds & fresh mozzarella with balsamic vinaigrette.
                    Spinach|Baby spinach, croutons, black olives, candied walnuts, white mushrooms & goat cheese with balsamic vinaigrette.
                    Bietole|Mixed greens, roasted beets, goat cheese, candied walnuts, roasted corn & tomatoes with honey dijon dressing.
                    Caesar|Romaine hearts, croutons, shaved parmigiano & caesar dressing. Also available with grilled chicken, chicken cutlet, roasted turkey, grilled shrimp, and filet mignon.
                    Frutta Secca|Mixed field greens, goat cheese, mixed dried fruit & candied walnuts with honey mustard dressing.
                    Insalata Di Pere|Mixed greens, red pears, gorgonzola & candied walnuts with lime dressing.
                    Insalata Tricolore|Radicchio, arugula, endive, olives & shaved parmesan with balsamic vinaigrette.
                    Rushetta e Gorgonzola|Baby arugula, endive, candied walnuts & gorgonzola with balsamic vinaigrette.
                    """
                ),
            ),
            grp(
                "Grilled Chicken Salads",
                textwrap.dedent(
                    """
                    Avocado|Grilled chicken, iceberg lettuce, shredded mozzarella, avocado, almonds & cherry tomatoes with balsamic dressing.
                    Insalata Di Pollo|Grilled chicken, mixed greens, olives, carrots, almonds & onions with balsamic dressing.
                    Rucola Caprino e Pollo|Grilled chicken, arugula, goat cheese, sun dried tomatoes & candied walnuts with balsamic dressing.
                    Cobb Salad|Grilled chicken, iceberg lettuce, black olives, tomatoes, avocado, gorgonzola, hard boiled eggs & bacon with bleu cheese dressing.
                    Pollo e Guacamole|Grilled chicken, iceberg lettuce, guacamole, roasted hot peppers, shredded mozzarella & cherry tomatoes with lime dressing.
                    Rucola E Farro|Grilled chicken, arugula, Tuscan barley, cherry tomatoes, hot peppers, hearts of palm & gorgonzola with honey dressing.
                    """
                ),
            ),
            grp(
                "Chicken Cutlet Salads",
                textwrap.dedent(
                    """
                    DiPrisco Salad|Chicken cutlet, mixed greens, tomatoes & goat cheese with balsamic vinaigrette.
                    Sarah Salad|Chicken cutlet, mixed greens, onions, hot peppers, corn, gorgonzola & tomatoes with balsamic dressing.
                    Parma Salad|Chicken cutlet, romaine lettuce, tomatoes, black olives, roasted peppers, red onions & parmesan with balsamic dressing.
                    Zona Salad|Chicken cutlet, mixed greens, red onions & tomatoes with garlic-balsamic dressing.
                    """
                ),
            ),
            grp(
                "Roasted Turkey Salads",
                textwrap.dedent(
                    """
                    Iceberg e Tacchino|Fresh roasted turkey, iceberg lettuce, sun dried tomatoes, marinated red onions, crumbled gorgonzola, roasted peppers & roasted corn with roasted garlic vinaigrette.
                    Spinaci e Tacchino|Fresh roasted turkey, baby spinach, goat cheese, sautéed mushrooms, roasted corn & crispy bacon with raspberry dressing.
                    Ruchetta Con Zona e Tacchino|Fresh roasted turkey, baby arugula, endive, candied walnuts & gorgonzola with roasted garlic vinaigrette.
                    Tacchino e Avocado|Fresh roasted turkey, mixed greens, shredded mozzarella, tomatoes, avocado, sautéed mushrooms & roasted hot peppers with balsamic dressing.
                    """
                ),
            ),
            grp(
                "Steak Salads",
                textwrap.dedent(
                    """
                    Bistecca e Farro|Grilled filet mignon, baby spinach, crispy bacon, barley, tomatoes & marinated artichokes with roasted garlic vinaigrette.
                    Bistecca e Zona|Grilled filet mignon, mixed greens, cherry tomatoes, black olives, marinated red onions & crumbled gorgonzola with balsamic vinaigrette.
                    Bistecca e Rucola|Grilled filet mignon, baby arugula, radicchio, artichokes, barley, roasted hot peppers & tomatoes with balsamic dressing.
                    """
                ),
            ),
            grp(
                "Salmon Salads",
                textwrap.dedent(
                    """
                    Salmone e Guacamole|Roasted salmon, mixed greens, guacamole, hearts of palm & sunflower seeds with honey dijon dressing.
                    Roasted Salmon|Roasted salmon, mixed greens, butternut squash & wasabi peas with orange dressing.
                    Salmone e Pere|Roasted salmon, baby spinach, endive, red pears, candied walnuts, roasted beets & cherry tomatoes with raspberry vinaigrette.
                    """
                ),
            ),
            grp(
                "Grilled Shrimp Salads",
                textwrap.dedent(
                    """
                    Gamberoni e Guacamole|Grilled shrimp, iceberg lettuce, guacamole, toasted almonds, cherry tomatoes & roasted hot peppers with lime dressing.
                    Romana Con Gamberoni|Grilled shrimp, romaine lettuce, tomatoes, fresh mozzarella, raisins & candied walnuts with balsamic vinaigrette.
                    Gamberoni con Wasabi|Grilled shrimp, mixed greens, spicy wasabi peas, cherry tomatoes & shredded mozzarella with orange dressing.
                    """
                ),
            ),
        ],
    )
)

DINING.append(
    section(
        "Pasta Creations",
        block=textwrap.dedent(
            """
            Cavatelli Carbonara|Cavatelli pasta, pancetta & scallions.
            Penne alla Vodka|Pink sauce with a splash of vodka.
            Penne alla Vodka & Sautéed Shrimp|
            Lobster Ravioli|
            Linguini Pescatore|Shrimp, calamari & mussels in a red sauce.
            Penne alla Vodka & Chicken|
            Rigatoni Veneziani|Rigatoni with sliced sausage & broccoli rabe in olive oil & garlic.
            Old Fashioned Spaghetti with Meatballs|
            """
        ),
    )
)

DINING.append(
    section(
        "Entrées",
        intro="Please be advised that consuming raw or undercooked meats, poultry, seafood, shellfish, or eggs may increase your risk of food-borne illness.",
        block=textwrap.dedent(
            """
            Grilled Salmon|
            Eggplant Parmigiana|
            Shrimp Parmigiana|
            Parmesan Crusted Tilapia|Pan seared tilapia baked with a parmesan crust.
            Chicken Sorrentino|Batter dipped chicken cutlet topped with prosciutto, eggplant & fresh mozzarella.
            Chicken Francaise|
            Four Cheese Ravioli|
            Shrimp Scampi|Shrimp in lemon, garlic, butter & white wine sauce, served over rice.
            Shrimp & Flounder Oreganata|Baked shrimp & flounder topped with oreganata bread crumbs.
            Chicken Parmigiana|
            Veal Parmigiana|
            Chicken Perugina|Chicken breast with cherry peppers, artichokes & mushrooms.
            Bistecca Romana|Pan seared filet mignon medallions topped with portobello.
            Grilled Rack of Lamb|
            Eggplant Rollatini|Served with linguini or penne.
            """
        ),
    )
)

DINING.append(
    section(
        "Kids Menu",
        block=textwrap.dedent(
            """
            Penne or Ravioli|Served with marinara, butter or oil & garlic.
            Doug Panini|Kids size panini with chicken cutlet & fresh mozzarella.
            Aria Panini|Kids size panini with ham & fresh mozzarella.
            Italian Grilled Cheese Panini|Double mozzarella.
            Chicken Strips & Fries|Fried chicken strips over french fries.
            Bella Panini|Kids size panini with fresh mozzarella, tomato & basil.
            Hamburger Panini|Hamburger, fresh mozzarella, tomatoes & ketchup.
            Nutella Panini|Kids size panini with Nutella.
            """
        ),
    )
)

DINING.append(
    section(
        "Sides",
        block=textwrap.dedent(
            """
            Broccoli Rabe|
            Sautéed Broccoli|
            Tuscan Fries|
            Italian Fries|
            Spinach with Oil and Garlic|
            Vegetable Du Jour|
            """
        ),
    )
)

# Catering menu (structure mirrors dine-in where repeated; catering-specific entrées/pastas included)
CATERING = [
    section(
        "Catering — Antipasti",
        block=textwrap.dedent(
            """
            Baked Clams|
            Cold Antipasto Platter|
            Fresh Vegetable Display|25–30 people.
            Hot Antipasto|Baked clams, eggplant rollatini, stuffed mushrooms & shrimp oreganata.
            Mixed Platter|Fresh fruit, garden vegetables & assorted cheeses (25–30 people).
            Mussels Portofino|Farm raised mussels in Portofino or fra diavolo.
            Sicilian Rice Balls|Crispy risotto bites with meat ragù, peas & fresh mozzarella; marinara on the side.
            Stuffed Mushrooms|
            Cheese Platter|25–30 people.
            Eggplant Rollatini|Rolled eggplant with ricotta; marinara on top.
            Fried Calamari|With marinara.
            Mini Meatballs|
            Mozzarella Caprese|Homemade mozzarella, tomatoes & basil with balsamic glaze.
            Shrimp Cocktail|
            Spinach And Artichoke Dip|
            """
        ),
    ),
]

# Catering paninis — same names as dine-in; condensed into groups
CATERING.append(
    section(
        "Catering — Paninis",
        intro="Panini selections for catering mirror our dine-in sandwiches; ask us to customize for your event.",
        groups=DINING[3]["groups"],  # reuse panini groups from dining
    )
)

CATERING.append(
    section(
        "Catering — Salads",
        groups=[
            grp(
                "Salads",
                textwrap.dedent(
                    """
                    Avocado|Iceberg lettuce, avocado, grilled chicken, shredded mozzarella, cherry tomatoes & almonds with balsamic dressing.
                    Brooklyn|Iceberg lettuce, tomatoes, cucumber, black olives & red onions with oil and white vinegar.
                    Chef Classic|Mixed greens, gorgonzola, dried cranberries, red pears & candied walnuts with balsamic dressing.
                    Greek|Baby greens, grape tomatoes, cucumbers, kalamata olives, feta, red peppers & onions with oil and vinegar.
                    Insalata Di Stagione|Mixed greens, tomatoes, carrots & cucumbers with balsamic vinaigrette.
                    Insalata Con Funghi|Mixed greens, roasted portobello, roasted peppers, sunflower seeds & fresh mozzarella with balsamic vinaigrette.
                    Spinach|Baby spinach, croutons, black olives, candied walnuts, white mushrooms & goat cheese with balsamic vinaigrette.
                    Bacon|Baby spinach, bacon, gorgonzola, dried apples, red onions & candied walnuts with honey mustard dressing.
                    Bietole|Mixed greens, roasted beets, goat cheese, candied walnuts, roasted corn & tomatoes with honey dijon dressing.
                    Caesar|Romaine hearts, croutons, shaved parmigiano & caesar dressing. Also available with grilled chicken, chicken cutlet, roasted turkey, grilled shrimp, and filet mignon.
                    Frutta Secca|Mixed field greens, goat cheese, mixed dried fruit & candied walnuts with honey mustard dressing.
                    Insalata Di Pere|Mixed greens, red pears, gorgonzola & candied walnuts with lime dressing.
                    Insalata Tricolore|Radicchio, arugula, endive, olives & shaved parmesan with balsamic vinaigrette.
                    Rushetta e Gorgonzola|Baby arugula, endive, candied walnuts & gorgonzola with balsamic vinaigrette.
                    """
                ),
            ),
        ],
    )
)

CATERING.append(
    section(
        "Catering — Pastas",
        block=textwrap.dedent(
            """
            Al Forno|Baked with fresh mozzarella, ricotta & marinara.
            Pasta Alla Vodka|
            Carbonara|Sautéed pancetta, scallions, parmesan & a splash of cream.
            Primavera|Broccoli, zucchini, carrots, mushrooms & peas in pink sauce or oil & garlic.
            San Remo|Fresh artichoke hearts, sun dried tomatoes & peas in a light cream sauce.
            Alfredo|Classic cream sauce with parmesan.
            Bolognese|Slow cooked beef and pork sauce.
            Lasagna|Layered with fresh mozzarella, ground beef & homemade marinara.
            Puttanesca|Fresh tomato sauce with olives, capers & onions.
            Siciliana|Fresh eggplant with marinara & chunks of fresh mozzarella.
            """
        ),
    )
)

CATERING.append(
    section(
        "Catering — Entrées",
        intro="Please be advised that consuming raw or undercooked meats, poultry, seafood, shellfish, or eggs may increase your risk of food-borne illness.",
        groups=[
            grp(
                "Chicken",
                textwrap.dedent(
                    """
                    Al Forno|Baked with fresh mozzarella, ricotta & marinara.
                    Francese|Batter dipped chicken sautéed in white wine & lemon sauce.
                    Marsala|Sautéed chicken breast with mixed wild mushrooms & marsala wine sauce.
                    Pomodorini|Chicken breast in cherry tomato & white wine sauce.
                    Sorrentino|Breaded chicken layered with prosciutto, fried eggplant & fresh mozzarella.
                    Cordon Bleu|Rolled chicken breasts breaded & stuffed with prosciutto & swiss cheese.
                    Limone|Chicken strips sautéed with garlic & fresh lemon.
                    Parmigiana|
                    Scarpiarello|Chicken with sausage, potatoes, rosemary, garlic & light lemon sauce.
                    Verde|Batter dipped chicken topped with broccoli florets & fresh mozzarella in sherry wine sauce.
                    """
                ),
            ),
            grp(
                "Steak",
                textwrap.dedent(
                    """
                    Filet Romano|Pan seared filet mignon medallions with portobello barolo wine sauce.
                    Grilled Skirt Steak|With portobello mushrooms.
                    """
                ),
            ),
            grp(
                "Veal",
                textwrap.dedent(
                    """
                    Francese|Veal medallions in white wine & lemon sauce.
                    Parmigiana|Breaded veal with fresh mozzarella & marinara.
                    Marsala|Tender veal with wild mushrooms & marsala wine.
                    Romana|Tender veal with baby spinach, asparagus, fresh mozzarella & light demi glaze.
                    """
                ),
            ),
            grp(
                "Pork",
                textwrap.dedent(
                    """
                    Sausage & Peppers|Sweet or hot Italian sausage with peppers & sautéed onions.
                    Porchetta Ripiena|Pounded pork loin stuffed with spinach, fontina & prosciutto.
                    Sausage Marinara|Sweet or hot Italian sausage slow cooked in marinara.
                    """
                ),
            ),
            grp(
                "Seafood",
                textwrap.dedent(
                    """
                    Flounder Oreganata|Broiled flounder with bread crumbs, white wine, garlic & oil.
                    Shrimp Francese|Batter dipped shrimp in white wine & lemon sauce.
                    Shrimp Scampi|Sautéed shrimp in white wine & garlic sauce.
                    Salmon Griglia|Grilled salmon with white wine, lemon & capers.
                    Shrimp Parmigiana|Fried shrimp with fresh mozzarella & marinara.
                    Tilapia Oreganata|Broiled tilapia with bread crumbs, white wine, garlic & oil.
                    """
                ),
            ),
            grp(
                "Vegetarian",
                textwrap.dedent(
                    """
                    Eggplant Parmigiana|Fried eggplant with fresh mozzarella & marinara.
                    """
                ),
            ),
        ],
    )
)

CATERING.append(
    section(
        "Catering — Kids & Sides",
        groups=[
            grp(
                "Kids Menu",
                textwrap.dedent(
                    """
                    Chicken Fingers|With your choice of dressing.
                    Mac & Cheese|
                    Italian Fries|Topped with garlic & parmesan.
                    Tuscan Fries|
                    """
                ),
            ),
            grp(
                "Sides",
                textwrap.dedent(
                    """
                    Broccoli|With oil & garlic.
                    Oven Roasted Potatoes|
                    Vegetable Medley|Seasonal vegetables sautéed with garlic & fresh herbs.
                    Broccoli Rabe|With oil & garlic.
                    String Beans Almondine|
                    """
                ),
            ),
        ],
    )
)


def main():
    out = []
    out.append("/* Generated by scripts/build_menu.py — do not edit by hand */")
    out.append("window.ZONA_DINING = " + json.dumps(DINING, ensure_ascii=False) + ";")
    out.append("window.ZONA_CATERING = " + json.dumps(CATERING, ensure_ascii=False) + ";")
    path = os.path.join(ROOT, "js", "menu-data.js")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Wrote", path)


if __name__ == "__main__":
    main()
