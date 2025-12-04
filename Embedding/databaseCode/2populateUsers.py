from connection import connectToMongoDB, closeConnection
from bson import ObjectId, Decimal128
from datetime import datetime
import random
from faker import Faker

mongoClient, db = connectToMongoDB()

usersCollection = db['users']
productsCollection = db['products']

usernames = [
    "James Smith", "John Johnson", "Robert Williams", "Michael Brown", "William Jones", "David Garcia", "Richard Miller", "Joseph Davis", "Thomas Rodriguez", "Charles Martinez",
    "Christopher Hernandez", "Daniel Lopez", "Matthew Gonzales", "Anthony Wilson", "Mark Anderson", "Donald Thomas", "Steven Taylor", "Paul Moore", "Andrew Jackson", "Joshua Martin",
    "Kenneth Lee", "Kevin Perez", "Brian Thompson", "George White", "Edward Harris", "Ronald Sanchez", "Timothy Clark", "Jason Ramirez", "Jeffrey Lewis", "Ryan Robinson",
    "Jacob Walker", "Gary Young", "Nicholas Allen", "Eric King", "Jonathan Wright", "Stephen Scott", "Larry Torres", "Justin Nguyen", "Scott Hill", "Brandon Flores",
    "Benjamin Green", "Samuel Adams", "Gregory Nelson", "Frank Baker", "Alexander Hall", "Raymond Campbell", "Patrick Mitchell", "Jack Carter", "Dennis Roberts", "Jerry Gomez",
    "Tyler Phillips", "Aaron Evans", "Jose Turner", "Adam Diaz", "Henry Parker", "Nathan Cruz", "Douglas Edwards", "Zachary Collins", "Peter Reyes", "Kyle Stewart",
    "Walter Morris", "Ethan Morales", "Jeremy Murphy", "Harold Cook", "Keith Rogers", "Christian Gutierrez", "Roger Ortiz", "Noah Morgan", "Gerald Cooper", "Carl Peterson",
    "Terry Bailey", "Sean Reed", "Arthur Kelly", "Austin Howard", "Noah Ramos", "Lawrence Kim", "Jesse Cox", "Joe Ward", "Bryan Richardson", "Billy Watson",
    "Jordan Brooks", "Albert Chavez", "Dylan Wood", "Bruce James", "Willie Bennett", "Gabriel Gray", "Alan Mendoza", "Juan Ruiz", "Logan Hughes", "Wayne Price",
    "Ralph Alvarez", "Roy Castillo", "Eugene Sanders", "Randy Patel", "Vincent Myers", "Russell Long", "Elijah Ross", "Louis Foster", "Bobby Jimenez", "Philip Smith",
    "Johnny Johnson", "Mary Williams", "Patricia Brown", "Jennifer Jones", "Linda Garcia", "Elizabeth Miller", "Barbara Davis", "Susan Rodriguez", "Jessica Martinez", "Sarah Hernandez",
    "Karen Lopez", "Nancy Gonzales", "Lisa Wilson", "Betty Anderson", "Margaret Thomas", "Sandra Taylor", "Ashley Moore", "Kimberly Jackson", "Emily Martin", "Donna Lee",
    "Michelle Perez", "Dorothy Thompson", "Carol White", "Amanda Harris", "Melissa Sanchez", "Deborah Clark", "Stephanie Ramirez", "Rebecca Lewis", "Sharon Robinson", "Laura Walker",
    "Cynthia Young", "Kathleen Allen", "Amy King", "Shirley Wright", "Angela Scott", "Helen Torres", "Anna Nguyen", "Brenda Hill", "Pamela Flores", "Nicole Green",
    "Emma Adams", "Samantha Nelson", "Katherine Baker", "Christine Hall", "Debra Campbell", "Rachel Mitchell", "Catherine Carter", "Carolyn Roberts", "Janet Gomez", "Ruth Phillips",
    "Maria Evans", "Heather Turner", "Diane Diaz", "Virginia Parker", "Julie Cruz", "Joyce Edwards", "Victoria Collins", "Olivia Reyes", "Kelly Stewart", "Christina Morris",
    "Lauren Morales", "Joan Murphy", "Evelyn Cook", "Judith Rogers", "Megan Gutierrez", "Cheryl Ortiz", "Andrea Morgan", "Hannah Cooper", "Martha Peterson", "Jacqueline Bailey",
    "Frances Reed", "Gloria Kelly", "Ann Howard", "Teresa Ramos", "Kathryn Kim", "Sara Cox", "Janice Ward", "Jean Richardson", "Alice Watson", "Madison Brooks",
    "Doris Chavez", "Rose Wood", "Julie James", "Judy Bennett", "Grace Gray", "Denise Mendoza", "Beverly Ruiz", "Marilyn Hughes", "Amber Price", "Danielle Alvarez",
    "Brittany Castillo", "Diana Sanders", "Jane Patel", "Lori Myers", "Olivia Long", "Tiffany Ross", "Kathy Foster", "Tammy Jimenez", "Crystal Smith", "Tina Johnson", "Sophia Williams",
    "James Brown", "John Jones", "Robert Garcia", "Michael Miller", "William Davis", "David Rodriguez", "Richard Martinez", "Joseph Hernandez", "Thomas Lopez", "Charles Gonzales",
    "Christopher Wilson", "Daniel Anderson", "Matthew Thomas", "Anthony Taylor", "Mark Moore", "Donald Jackson", "Steven Martin", "Paul Lee", "Andrew Perez", "Joshua Thompson",
    "Kenneth White", "Kevin Harris", "Brian Sanchez", "George Clark", "Edward Ramirez", "Ronald Lewis", "Timothy Robinson", "Jason Walker", "Jeffrey Young", "Ryan Allen",
    "Jacob King", "Gary Wright", "Nicholas Scott", "Eric Torres", "Jonathan Nguyen", "Stephen Hill", "Larry Flores", "Justin Green", "Scott Adams", "Brandon Nelson",
    "Benjamin Baker", "Samuel Hall", "Gregory Campbell", "Frank Mitchell", "Alexander Carter", "Raymond Roberts", "Patrick Gomez", "Jack Phillips", "Dennis Evans", "Jerry Turner",
    "Tyler Diaz", "Aaron Parker", "Jose Cruz", "Adam Edwards", "Henry Collins", "Nathan Reyes", "Douglas Stewart", "Zachary Morris", "Peter Morales", "Kyle Murphy",
    "Walter Cook", "Ethan Rogers", "Jeremy Gutierrez", "Harold Ortiz", "Keith Morgan", "Christian Cooper", "Roger Peterson", "Noah Bailey", "Gerald Reed", "Carl Kelly",
    "Terry Howard", "Sean Ramos", "Arthur Kim", "Austin Cox", "Noah Ward", "Lawrence Richardson", "Jesse Watson", "Joe Brooks", "Bryan Chavez", "Billy Wood",
    "Jordan James", "Albert Bennett", "Dylan Gray", "Bruce Mendoza", "Willie Ruiz", "Gabriel Hughes", "Alan Price", "Juan Alvarez", "Logan Castillo", "Wayne Sanders",
    "Ralph Patel", "Roy Myers", "Eugene Long", "Randy Ross", "Vincent Foster", "Russell Jimenez", "Elijah Smith", "Louis Johnson", "Bobby Williams", "Philip Brown", "Johnny Jones",
    "Mary Garcia", "Patricia Miller", "Jennifer Davis", "Linda Rodriguez", "Elizabeth Martinez", "Barbara Hernandez", "Susan Lopez", "Jessica Gonzales", "Sarah Wilson", "Karen Anderson",
    "Nancy Thomas", "Lisa Taylor", "Betty Moore", "Margaret Jackson", "Sandra Martin", "Ashley Lee", "Kimberly Perez", "Emily Thompson", "Donna White", "Michelle Harris",
    "Dorothy Sanchez", "Carol Clark", "Amanda Ramirez", "Melissa Lewis", "Deborah Robinson", "Stephanie Walker", "Rebecca Young", "Sharon Allen", "Laura King", "Cynthia Wright",
    "Kathleen Scott", "Amy Torres", "Shirley Nguyen", "Angela Hill", "Helen Flores", "Anna Green", "Brenda Adams", "Pamela Nelson", "Nicole Baker", "Emma Hall",
    "Samantha Campbell", "Katherine Mitchell", "Christine Carter", "Debra Roberts", "Rachel Gomez", "Catherine Phillips", "Carolyn Evans", "Janet Turner", "Ruth Diaz", "Maria Parker",
    "Heather Cruz", "Diane Edwards", "Virginia Collins", "Julie Reyes", "Joyce Stewart", "Victoria Morris", "Olivia Morales", "Kelly Murphy", "Christina Cook", "Lauren Rogers",
    "Joan Gutierrez", "Evelyn Ortiz", "Judith Morgan", "Megan Cooper", "Cheryl Peterson", "Andrea Bailey", "Hannah Reed", "Martha Kelly", "Jacqueline Howard", "Frances Ramos",
    "Gloria Kim", "Ann Cox", "Teresa Ward", "Kathryn Richardson", "Sara Watson", "Janice Brooks", "Jean Chavez", "Alice Wood", "Madison James", "Doris Bennett",
    "Rose Gray", "Julie Mendoza", "Judy Ruiz", "Grace Hughes", "Denise Price", "Beverly Alvarez", "Marilyn Castillo", "Amber Sanders", "Danielle Patel", "Brittany Myers",
    "Diana Long", "Jane Ross", "Lori Foster", "Olivia Jimenez", "Tiffany Smith", "Kathy Johnson", "Tammy Williams", "Crystal Brown", "Tina Jones", "Sophia Garcia",
    "James Miller", "John Davis", "Robert Rodriguez", "Michael Martinez", "William Hernandez", "David Lopez", "Richard Gonzales", "Joseph Wilson", "Thomas Anderson", "Charles Thomas",
    "Christopher Taylor", "Daniel Moore", "Matthew Jackson", "Anthony Martin", "Mark Lee", "Donald Perez", "Steven Thompson", "Paul White", "Andrew Harris", "Joshua Sanchez",
    "Kenneth Clark", "Kevin Ramirez", "Brian Lewis", "George Robinson", "Edward Walker", "Ronald Young", "Timothy Allen", "Jason King", "Jeffrey Wright", "Ryan Scott",
    "Jacob Torres", "Gary Nguyen", "Nicholas Hill", "Eric Flores", "Jonathan Green", "Stephen Adams", "Larry Nelson", "Justin Baker", "Scott Hall", "Brandon Campbell",
    "Benjamin Mitchell", "Samuel Carter", "Gregory Roberts", "Frank Gomez", "Alexander Phillips", "Raymond Evans", "Patrick Turner", "Jack Diaz", "Dennis Parker", "Jerry Cruz",
    "Tyler Edwards", "Aaron Collins", "Jose Reyes", "Adam Stewart", "Henry Morris", "Nathan Morales", "Douglas Murphy", "Zachary Cook", "Peter Rogers", "Kyle Gutierrez",
    "Walter Ortiz", "Ethan Morgan", "Jeremy Cooper", "Harold Peterson", "Keith Bailey", "Christian Reed", "Roger Kelly", "Noah Howard", "Gerald Ramos", "Carl Kim",
    "Terry Cox", "Sean Ward", "Arthur Richardson", "Austin Watson", "Noah Brooks", "Lawrence Chavez", "Jesse Wood", "Joe James", "Bryan Bennett", "Billy Gray",
    "Jordan Mendoza", "Albert Ruiz", "Dylan Hughes", "Bruce Price", "Willie Alvarez", "Gabriel Castillo", "Alan Sanders", "Juan Patel", "Logan Myers", "Wayne Long",
    "Ralph Ross", "Roy Foster", "Eugene Jimenez", "Randy Smith", "Vincent Johnson", "Russell Williams", "Elijah Brown", "Louis Jones", "Bobby Garcia", "Philip Miller", "Johnny Davis",
    "Mary Rodriguez", "Patricia Martinez", "Jennifer Hernandez", "Linda Lopez", "Elizabeth Gonzales", "Barbara Wilson", "Susan Anderson", "Jessica Thomas", "Sarah Taylor", "Karen Moore",
    "Nancy Jackson", "Lisa Martin", "Betty Lee", "Margaret Perez", "Sandra Thompson", "Ashley White", "Kimberly Harris", "Emily Sanchez", "Donna Clark", "Michelle Ramirez",
    "Dorothy Lewis", "Carol Robinson", "Amanda Walker", "Melissa Young", "Deborah Allen", "Stephanie King", "Rebecca Wright", "Sharon Scott", "Laura Torres", "Cynthia Nguyen",
    "Kathleen Hill", "Amy Flores", "Shirley Green", "Angela Adams", "Helen Nelson", "Anna Baker", "Brenda Hall", "Pamela Campbell", "Nicole Mitchell", "Emma Carter",
    "Samantha Roberts", "Katherine Gomez", "Christine Phillips", "Debra Evans", "Rachel Turner", "Catherine Diaz", "Carolyn Parker", "Janet Cruz", "Ruth Edwards", "Maria Collins",
    "Heather Reyes", "Diane Stewart", "Virginia Morris", "Julie Morales", "Joyce Murphy", "Victoria Cook", "Olivia Rogers", "Kelly Gutierrez", "Christina Ortiz", "Lauren Morgan",
    "Joan Cooper", "Evelyn Peterson", "Judith Bailey", "Megan Reed", "Cheryl Kelly", "Andrea Howard", "Hannah Ramos", "Martha Kim", "Jacqueline Cox", "Frances Ward",
    "Gloria Richardson", "Ann Watson", "Teresa Brooks", "Kathryn Chavez", "Sara Wood", "Janice James", "Jean Bennett", "Alice Gray", "Madison Mendoza", "Doris Ruiz",
    "Rose Hughes", "Julie Price", "Judy Alvarez", "Grace Castillo", "Denise Sanders", "Beverly Patel", "Marilyn Myers", "Amber Long", "Danielle Ross", "Brittany Foster",
    "Diana Jimenez", "Jane Smith", "Lori Johnson", "Olivia Williams", "Tiffany Brown", "Kathy Jones", "Tammy Garcia", "Crystal Miller", "Tina Davis", "Sophia Rodriguez",
    "James Martinez", "John Hernandez", "Robert Lopez", "Michael Gonzales", "William Wilson", "David Anderson", "Richard Thomas", "Joseph Taylor", "Thomas Moore", "Charles Jackson",
    "Christopher Martin", "Daniel Lee", "Matthew Perez", "Anthony Thompson", "Mark White", "Donald Harris", "Steven Sanchez", "Paul Clark", "Andrew Ramirez", "Joshua Lewis",
    "Kenneth Robinson", "Kevin Walker", "Brian Young", "George Allen", "Edward King", "Ronald Wright", "Timothy Scott", "Jason Torres", "Jeffrey Nguyen", "Ryan Hill",
    "Jacob Flores", "Gary Green", "Nicholas Adams", "Eric Nelson", "Jonathan Baker", "Stephen Hall", "Larry Campbell", "Justin Mitchell", "Scott Carter", "Brandon Roberts",
    "Benjamin Gomez", "Samuel Phillips", "Gregory Evans", "Frank Turner", "Alexander Diaz", "Raymond Parker", "Patrick Cruz", "Jack Edwards", "Dennis Collins", "Jerry Reyes",
    "Tyler Stewart", "Aaron Morris", "Jose Morales", "Adam Murphy", "Henry Cook", "Nathan Rogers", "Douglas Gutierrez", "Zachary Ortiz", "Peter Morgan", "Kyle Cooper",
    "Walter Peterson", "Ethan Bailey", "Jeremy Reed", "Harold Kelly", "Keith Howard", "Christian Ramos", "Roger Kim", "Noah Cox", "Gerald Ward", "Carl Richardson",
    "Terry Watson", "Sean Brooks", "Arthur Chavez", "Austin Wood", "Noah James", "Lawrence Bennett", "Jesse Gray", "Joe Mendoza", "Bryan Ruiz", "Billy Hughes",
    "Jordan Price", "Albert Alvarez", "Dylan Castillo", "Bruce Sanders", "Willie Patel", "Gabriel Myers", "Alan Long", "Juan Ross", "Logan Foster", "Wayne Jimenez",
    "Ralph Smith", "Roy Johnson", "Eugene Williams", "Randy Brown", "Vincent Jones", "Russell Garcia", "Elijah Miller", "Louis Davis", "Bobby Rodriguez", "Philip Martinez", "Johnny Hernandez",
    "Mary Lopez", "Patricia Gonzales", "Jennifer Wilson", "Linda Anderson", "Elizabeth Thomas", "Barbara Taylor", "Susan Moore", "Jessica Jackson", "Sarah Martin", "Karen Lee",
    "Nancy Perez", "Lisa Thompson", "Betty White", "Margaret Harris", "Sandra Sanchez", "Ashley Clark", "Kimberly Ramirez", "Emily Lewis", "Donna Robinson", "Michelle Walker",
    "Dorothy Young", "Carol Allen", "Amanda King", "Melissa Wright", "Deborah Scott", "Stephanie Torres", "Rebecca Nguyen", "Sharon Hill", "Laura Flores", "Cynthia Green",
    "Kathleen Adams", "Amy Nelson", "Shirley Baker", "Angela Hall", "Helen Campbell", "Anna Mitchell", "Brenda Carter", "Pamela Roberts", "Nicole Gomez", "Emma Phillips",
    "Samantha Evans", "Katherine Turner", "Christine Diaz", "Debra Parker", "Rachel Cruz", "Catherine Edwards", "Carolyn Collins", "Janet Reyes", "Ruth Stewart", "Maria Morris",
    "Heather Morales", "Diane Murphy", "Virginia Cook", "Julie Rogers", "Joyce Gutierrez", "Victoria Ortiz", "Olivia Morgan", "Kelly Cooper", "Christina Peterson", "Lauren Bailey",
    "Joan Reed", "Evelyn Kelly", "Judith Howard", "Megan Ramos", "Cheryl Kim", "Andrea Cox", "Hannah Ward", "Martha Richardson", "Jacqueline Watson", "Frances Brooks",
    "Gloria Chavez", "Ann Wood", "Teresa James", "Kathryn Bennett", "Sara Gray", "Janice Mendoza", "Jean Ruiz", "Alice Hughes", "Madison Price", "Doris Alvarez",
    "Rose Castillo", "Julie Sanders", "Judy Patel", "Grace Myers", "Denise Long", "Beverly Ross", "Marilyn Foster", "Amber Jimenez", "Danielle Smith", "Brittany Johnson",
    "Diana Williams", "Jane Brown", "Lori Jones", "Olivia Garcia", "Tiffany Miller", "Kathy Davis", "Tammy Rodriguez", "Crystal Martinez", "Tina Hernandez", "Sophia Lopez",
    "James Gonzales", "John Wilson", "Robert Anderson", "Michael Thomas", "William Taylor", "David Moore", "Richard Jackson", "Joseph Martin", "Thomas Lee", "Charles Perez",
    "Christopher Thompson", "Daniel White", "Matthew Harris", "Anthony Sanchez", "Mark Clark", "Donald Ramirez", "Steven Lewis", "Paul Robinson", "Andrew Walker", "Joshua Young",
    "Kenneth Allen", "Kevin King", "Brian Wright", "George Scott", "Edward Torres", "Ronald Nguyen", "Timothy Hill", "Jason Flores", "Jeffrey Green", "Ryan Adams",
    "Jacob Nelson", "Gary Baker", "Nicholas Hall", "Eric Campbell", "Jonathan Mitchell", "Stephen Carter", "Larry Roberts", "Justin Gomez", "Scott Phillips", "Brandon Evans",
    "Benjamin Turner", "Samuel Diaz", "Gregory Parker", "Frank Cruz", "Alexander Edwards", "Raymond Collins", "Patrick Reyes", "Jack Stewart", "Dennis Morris", "Jerry Morales",
    "Tyler Murphy", "Aaron Cook", "Jose Rogers", "Adam Gutierrez", "Henry Ortiz", "Nathan Morgan", "Douglas Cooper", "Zachary Peterson", "Peter Bailey", "Kyle Reed",
    "Walter Kelly", "Ethan Howard", "Jeremy Ramos", "Harold Kim", "Keith Cox", "Christian Ward", "Roger Richardson", "Noah Watson", "Gerald Brooks", "Carl Chavez",
    "Terry Wood", "Sean James", "Arthur Bennett", "Austin Gray", "Noah Mendoza", "Lawrence Ruiz", "Jesse Hughes", "Joe Price", "Bryan Alvarez", "Billy Castillo",
    "Jordan Sanders", "Albert Patel", "Dylan Myers", "Bruce Long", "Willie Ross", "Gabriel Foster", "Alan Jimenez", "Juan Smith", "Logan Johnson", "Wayne Williams",
    "Ralph Brown", "Roy Jones", "Eugene Garcia", "Randy Miller", "Vincent Davis", "Russell Rodriguez", "Elijah Martinez", "Louis Hernandez", "Bobby Lopez", "Philip Gonzales", "Johnny Wilson",
    "Caleb Reynolds", "Ryan Ellis", "Luke Harrison", "Isaac Gibson", "Nathaniel McDonald", "Hunter Marshall", "Seth Gentry", "Garrett Burns", "Connor Gordon", "Evan Shaw", "Ian Holmes",
    "Cole Rice", "Julian Robertson", "Adrian Hunt", "Jeremiah Black", "Jordan Daniels", "Preston Palmer", "Marcus Mills", "Dominic Nichols", "Micah Grant", "Blake Knight", "Tristan Ferguson",
    "Xavier Rose", "Harrison Stone", "Sebastian Hawkins", "Damian Dunn", "Axel Perkins", "Carson Hudson", "Brody Spencer", "Chase Gardner", "Bentley Stephens", "Sawyer Payne", "Jason Pierce",
    "Ryder Berry", "Gavin Matthews", "Leo Arnold", "Diego Wagner", "Parker Willis", "Hayden Ray", "Asher Watkins", "Hudson Olson", "Ezra Carroll", "Easton Duncan", "Nolan Snyder", 
    "Colton Hart", "Luca Cunningham", "Austin Bradley", "Jack Lane", "Kevin Andrews", "Zachary Fox", "Riley Webb", "Mason Chapman", "Elias Wheeler", "Oliver Lynch", "Daniel Murray", 
    "Liam Wallace", "William Hopkins", "James Day", "Benjamin Cole", "Samuel Hayes", "Owen Graham", "Henry West", "Gabriel Jordan", "Jackson Hamilton", "Matthew Woods", "Aiden Ford",
    "Lucas Porter", "Logan Bowman", "David Malone", "Carter Hicks", "Wyatt Crawford", "Jayden Mason", "Dylan Boyd", "Grayson Kennedy", "Levi Warren", "Michael Dixon", "Lincoln Freeman",
    "Mateo Simpson", "Julian Tucker", "Jaxon Henry", "Levi Stevens", "Christopher Meyer", "Joshua Hanson", "Andrew Montgomery", "Theodore Harvey", "Ryan Little", "Nathan Burton",
    "Aaron Stanley", "Christian George", "Hunter Jacobs", "Thomas Reid", "Charles Fuller", "Connor Fields", "Eli Bishop", "Landon Franklin"
]


mailExtensions = [
    '@gmail.com',
    '@yahoo.com',
    '@hotmail.com',
    '@outlook.com',
    '@icloud.com'
]


fake = Faker('en_GB')

def createAddresses(min, max):
    addresses = []
    
    for i in range(random.randint(min, max)):
        addresses.append({
            "street": fake.street_address(),
            "city": fake.city(),
            "county": fake.county(), # "judet"
            "zipcode": fake.postcode(), 
            "country": "United Kingdom", 
            "fullAddress": fake.address().replace('\n', ', ')
        })
        
    return addresses


def getRandomProducts(sampleSize=1):
    pipeline = [
        { "$sample": { "size": sampleSize } }
    ]
    
    cursor = productsCollection.aggregate(pipeline)
    
    return list(cursor)


def createShoppingCart(minVal, maxVal):
    shoppingCart = []
    
    itemsCount = random.randint(minVal, maxVal)
    products = getRandomProducts(itemsCount)
    
    for product in products:
        stock = product['stock']
        
        limit = max(1, stock//2)
        
        quantity = random.randint(1, limit)
        
        shoppingCart.append({
            'productName': product['name'],
            'sku': product['sku'],
            'price': product['price'],
            'quantity': quantity
        })
        
    return shoppingCart


def createUser(username):
    
    email = username.replace(" ", "").lower() + random.choice(mailExtensions)
    
    addresses = createAddresses(1,4)
    shoppingCart = createShoppingCart(1,10)
    
    user = {
        'username': username,
        'email': email,
        'addresses': addresses,
        'shoppingCart': shoppingCart
    }
    
    return user

users = [createUser(name) for name in usernames]

result = usersCollection.insert_many(users)
print(f"✓ {len(result.inserted_ids)} unique users added successfully")

closeConnection(mongoClient)

# print(users)
# print(len(users))

