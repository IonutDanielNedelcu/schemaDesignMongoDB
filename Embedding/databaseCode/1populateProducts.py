from connection import connectToMongoDB, closeConnection
from bson import ObjectId, Decimal128
from datetime import datetime
import random

mongoClient, db = connectToMongoDB()

productsCollection = db['products']

vendors = [
    {"companyName": "Innovatech Solutions", "contactEmail": "sales@innovatech.com", "supportPhone": "+1-888-123-4567"},
    {"companyName": "Apex Gadgetry", "contactEmail": "support@apexgadgetry.com", "supportPhone": "+1-888-234-5678"},
    {"companyName": "Quantum Devices", "contactEmail": "info@quantumdev.com", "supportPhone": "+1-888-345-6789"},
    {"companyName": "Stellar Goods", "contactEmail": "contact@stellargoods.net", "supportPhone": "+1-888-456-7890"},
    {"companyName": "Fusion Homewares", "contactEmail": "support@fusionhome.com", "supportPhone": "+1-888-567-8901"},
    {"companyName": "Ember Kitchen", "contactEmail": "sales@emberkitchen.io", "supportPhone": "+1-888-678-9012"},
    {"companyName": "Velocity Sports Gear", "contactEmail": "info@velocitysports.com", "supportPhone": "+1-888-789-0123"},
    {"companyName": "Zenith Athletics", "contactEmail": "contact@zenithathletics.com", "supportPhone": "+1-888-890-1234"},
    {"companyName": "Bibliophile's Corner", "contactEmail": "orders@bibliophilescorner.com", "supportPhone": "+1-888-901-2345"},
    {"companyName": "The Story Weaver", "contactEmail": "support@storyweaver.pub", "supportPhone": "+1-888-012-3456"},
    {"companyName": "Chic Threads Apparel", "contactEmail": "sales@chicthreads.com", "supportPhone": "+1-888-112-2334"},
    {"companyName": "Urban Vogue Outfitters", "contactEmail": "info@urbanvogue.com", "supportPhone": "+1-888-223-3445"},
    {"companyName": "Digital Horizon", "contactEmail": "contact@digitalhorizon.tech", "supportPhone": "+1-888-334-4556"},
    {"companyName": "Pinnacle Performance", "contactEmail": "info@pinnacleperf.com", "supportPhone": "+1-888-445-5667"},
    {"companyName": "Evergreen Books", "contactEmail": "support@evergreenbooks.com", "supportPhone": "+1-888-556-6778"},
    {"companyName": "StyleSphere", "contactEmail": "contact@stylesphere.co", "supportPhone": "+1-888-667-7889"},
    {"companyName": "Gourmet Gadgets", "contactEmail": "sales@gourmetgadgets.com", "supportPhone": "+1-888-778-8990"},
    {"companyName": "Celestial Tech", "contactEmail": "support@celestial.tech", "supportPhone": "+1-888-111-2222"},
    {"companyName": "TerraFirm Gear", "contactEmail": "info@terrafirm.gear", "supportPhone": "+1-888-333-4444"},
    {"companyName": "AquaLuxe Kitchenware", "contactEmail": "sales@aqualuxe.kitchen", "supportPhone": "+1-888-555-6666"},
    {"companyName": "Momentum Active", "contactEmail": "contact@momentumactive.com", "supportPhone": "+1-888-777-8888"},
    {"companyName": "The Scholar's Press", "contactEmail": "publishing@scholarspress.com", "supportPhone": "+1-888-999-0000"},
    {"companyName": "Atelier Apparel", "contactEmail": "cs@atelierapparel.com", "supportPhone": "+1-888-212-3232"},
    {"companyName": "Zenith Sports Dynamics", "contactEmail": "relations@zenithdynamics.sport", "supportPhone": "+1-888-434-5454"},
    {"companyName": "The Culinary Edge", "contactEmail": "help@culinaryedge.co", "supportPhone": "+1-888-656-7676"},
    {"companyName": "Nexus Innovations", "contactEmail": "contact@nexusinnov.com", "supportPhone": "+1-888-121-2121"},
    {"companyName": "Horizon Dynamics", "contactEmail": "support@horizondynamics.com", "supportPhone": "+1-888-343-4343"},
    {"companyName": "Aurora Tech", "contactEmail": "info@auroratech.io", "supportPhone": "+1-888-565-6565"},
    {"companyName": "Silverline Goods", "contactEmail": "sales@silverlinegoods.com", "supportPhone": "+1-888-787-8787"},
    {"companyName": "Phoenix United", "contactEmail": "contact@phoenixunited.com", "supportPhone": "+1-888-909-0909"},
    {"companyName": "Summit Supply Co.", "contactEmail": "support@summitsupply.co", "supportPhone": "+1-888-112-3456"},
    {"companyName": "Keystone Merchants", "contactEmail": "info@keystonemerchants.com", "supportPhone": "+1-888-223-4567"},
    {"companyName": "Redwood & Oak", "contactEmail": "sales@redwoodandoak.com", "supportPhone": "+1-888-334-5678"},
    {"companyName": "Northstar Provisions", "contactEmail": "contact@northstarprovisions.com", "supportPhone": "+1-888-445-6789"},
    {"companyName": "Tidal Wave Inc.", "contactEmail": "support@tidalwaveinc.com", "supportPhone": "+1-888-556-7890"},
    {"companyName": "Ironclad Systems", "contactEmail": "info@ironcladsys.com", "supportPhone": "+1-888-667-8901"},
    {"companyName": "Crimson Arrow", "contactEmail": "sales@crimsonarrow.com", "supportPhone": "+1-888-778-9012"},
    {"companyName": "Blue Jay Books", "contactEmail": "orders@bluejaybooks.com", "supportPhone": "+1-888-889-0123"},
    {"companyName": "Golden Grain Foods", "contactEmail": "support@goldengrain.com", "supportPhone": "+1-888-990-1234"},
    {"companyName": "Emerald City Goods", "contactEmail": "contact@emeraldcitygoods.com", "supportPhone": "+1-888-001-2345"},
    {"companyName": "Black Diamond Gear", "contactEmail": "info@blackdiamondgear.com", "supportPhone": "+1-888-111-3456"},
    {"companyName": "White Wolf Wares", "contactEmail": "sales@whitewolfwares.com", "supportPhone": "+1-888-222-4567"},
    {"companyName": "Purple Finch Publishing", "contactEmail": "contact@purplefinch.pub", "supportPhone": "+1-888-333-5678"},
    {"companyName": "Gray Fox Tech", "contactEmail": "support@grayfoxtech.com", "supportPhone": "+1-888-444-6789"},
    {"companyName": "Green Turtle Gaming", "contactEmail": "info@greenturtlegaming.com", "supportPhone": "+1-888-555-7890"},
    {"companyName": "Brown Bear Bistro", "contactEmail": "contact@brownbearbistro.com", "supportPhone": "+1-888-666-8901"},
    {"companyName": "Orange Octopus Optics", "contactEmail": "sales@orangeoctopus.com", "supportPhone": "+1-888-777-9012"},
    {"companyName": "Yellow Jacket Sports", "contactEmail": "info@yellowjacketsports.com", "supportPhone": "+1-888-888-0123"},
    {"companyName": "Violet Vixen Vogue", "contactEmail": "support@violetvixenvogue.com", "supportPhone": "+1-888-999-1234"},
    {"companyName": "Ivory Elephant Imports", "contactEmail": "contact@ivoryelephant.com", "supportPhone": "+1-888-101-2345"},
    {"companyName": "Scarlet Sparrow Styles", "contactEmail": "sales@scarletsparrow.com", "supportPhone": "+1-888-212-3456"},
    {"companyName": "Azure Turtle Toys", "contactEmail": "info@azureturtle.com", "supportPhone": "+1-888-323-4567"},
    {"companyName": "Cerulean Swan Solutions", "contactEmail": "support@ceruleanswan.com", "supportPhone": "+1-888-434-5678"},
    {"companyName": "Saffron Stallion Sports", "contactEmail": "contact@saffronstallion.com", "supportPhone": "+1-888-545-6789"},
    {"companyName": "Veridian Valley Ventures", "contactEmail": "info@veridianvalley.com", "supportPhone": "+1-888-656-7890"},
    {"companyName": "Magenta Moose Media", "contactEmail": "sales@magentamoose.com", "supportPhone": "+1-888-767-8901"},
    {"companyName": "Teal Tiger Tech", "contactEmail": "contact@tealtiger.tech", "supportPhone": "+1-888-878-9012"},
    {"companyName": "Lavender Lion Linens", "contactEmail": "support@lavenderlion.com", "supportPhone": "+1-888-989-0123"},
    {"companyName": "Crimson Cobra Creations", "contactEmail": "info@crimsoncobra.com", "supportPhone": "+1-888-090-1234"},
    {"companyName": "Onyx Otter Outfitters", "contactEmail": "sales@onyxotter.com", "supportPhone": "+1-888-101-1234"},
    {"companyName": "Jade Jaguar Jewelers", "contactEmail": "contact@jadejaguar.com", "supportPhone": "+1-888-212-2345"},
    {"companyName": "Topaz Toucan Travel", "contactEmail": "support@topaztoucan.com", "supportPhone": "+1-888-323-3456"},
    {"companyName": "Ruby Rooster Restaurant", "contactEmail": "info@rubyrooster.com", "supportPhone": "+1-888-434-4567"},
    {"companyName": "Sapphire Shark Supplies", "contactEmail": "sales@sapphireshark.com", "supportPhone": "+1-888-545-5678"},
    {"companyName": "Garnet Griffin Gear", "contactEmail": "contact@garnetgriffin.com", "supportPhone": "+1-888-656-6789"},
    {"companyName": "Amethyst Antelope Apparel", "contactEmail": "support@amethystantelope.com", "supportPhone": "+1-888-767-7890"},
    {"companyName": "Aquamarine Alligator Art", "contactEmail": "info@aquamarinealligator.com", "supportPhone": "+1-888-878-8901"},
    {"companyName": "Diamond Dolphin Designs", "contactEmail": "sales@diamonddolphin.com", "supportPhone": "+1-888-989-9012"},
    {"companyName": "Pearl Peacock Products", "contactEmail": "contact@pearlpeacock.com", "supportPhone": "+1-888-090-0123"},
    {"companyName": "Peridot Panther Publishing", "contactEmail": "support@peridotpanther.com", "supportPhone": "+1-888-101-1122"},
    {"companyName": "Spinel Sparrow Sports", "contactEmail": "info@spinelsparrow.com", "supportPhone": "+1-888-212-2233"},
    {"companyName": "Tourmaline Tiger Toys", "contactEmail": "sales@tourmalinetiger.com", "supportPhone": "+1-888-323-3344"},
    {"companyName": "Zircon Zebra Zenith", "contactEmail": "contact@zirconzebra.com", "supportPhone": "+1-888-434-4455"},
    {"companyName": "Amber Ape Adventures", "contactEmail": "support@amberape.com", "supportPhone": "+1-888-545-5566"}
]

userNames = [
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
    "Ralph Brown", "Roy Jones", "Eugene Garcia", "Randy Miller", "Vincent Davis", "Russell Rodriguez", "Elijah Martinez", "Louis Hernandez", "Bobby Lopez", "Philip Gonzales", "Johnny Wilson"
]


comments = [
    "Excellent product, highly recommended! A true game changer.",
    "Good value for money. Does exactly what it promises.",
    "Not as expected, a bit disappointed with the build quality.",
    "Amazing quality and lightning-fast shipping! Will buy again.",
    "Works perfectly, very satisfied with this purchase.",
    "Could be better for the price. The features are a bit lacking.",
    "Outstanding performance! It exceeded all my expectations.",
    "Decent product but feels overpriced for what it is.",
    "Best purchase I've made this year. Absolutely fantastic!",
    "Average quality, nothing special to write home about.",
    "Fantastic! I'm blown away by how good this is.",
    "Poor quality, returning it immediately. Avoid this product.",
    "Great features but the battery life is a major letdown.",
    "Love it! It has become an essential part of my daily routine.",
    "Not worth the money. You can find better alternatives.",
    "The design is sleek and modern. Looks great on my desk.",
    "Customer support was incredibly helpful with my issue.",
    "The instructions were confusing, took a while to set up.",
    "Five stars! Does the job flawlessly.",
    "I've been using this for a month now and it's still going strong.",
    "It broke after just a week of use. Very fragile.",
    "A solid product that delivers on its promises.",
    "The color is much nicer in person than in the pictures.",
    "Slightly smaller than I anticipated, but still works well.",
    "A must-have for anyone serious about quality.",
    "The packaging was damaged on arrival, but the product was fine.",
    "It's okay. Not great, not terrible. Just okay.",
    "I bought this as a gift and they absolutely loved it!",
    "The software is a bit buggy, hoping for an update soon.",
    "Incredible value. Feels much more expensive than it is.",
    "This is a revolutionary product. Can't imagine my life without it.",
    "The setup was a breeze, up and running in minutes.",
    "It's a bit noisy during operation, which is a downside.",
    "I had high hopes, but it didn't live up to the hype.",
    "Impressive battery life, lasts for days on a single charge.",
    "The user interface is intuitive and easy to navigate.",
    "Aesthetically pleasing, but the performance is just average.",
    "It feels very durable and well-made. Should last a long time.",
    "The warranty process was a nightmare. Terrible customer service.",
    "Perfect for my needs. Exactly what I was looking for.",
    "The app that comes with it is surprisingly polished and useful.",
    "It gets the job done, but I wish it had more features.",
    "There's a steep learning curve, but it's worth it in the end.",
    "This was an impulse buy, and I have zero regrets.",
    "The product arrived earlier than expected, which was a nice surprise.",
    "I'm on the fence about this one. It has its pros and cons.",
    "The build quality is top-notch. Feels very premium.",
    "It's a good entry-level option for beginners.",
    "I would recommend this to a friend without hesitation.",
    "The performance is inconsistent. Sometimes it's great, sometimes it's not.",
    "The materials used feel cheap and flimsy. I expected more.",
    "It's a bit bulky, but the performance makes up for it.",
    "The price is a bit high, but you get what you pay for.",
    "I've had this for over a year, and it's still working like new.",
    "The feature set is impressive for this price point.",
    "It's a decent product, but the competition offers more.",
    "The instructions were clear and easy to follow.",
    "I had to return the first one due to a defect, but the replacement works fine.",
    "This product has completely streamlined my workflow.",
    "It's a simple, no-frills product that does its job well.",
    "The product looks exactly like the photos online.",
    "I'm very impressed with the attention to detail.",
    "It's a bit of a gimmick, but a fun one at that.",
    "The product has a weird smell that won't go away.",
    "I wish I had bought this sooner. It's been a great help.",
    "The customer reviews were spot on. This is a great product.",
    "It's not compatible with my other devices, which is a shame.",
    "The product is very easy to clean and maintain.",
    "I'm giving it four stars because there's always room for improvement.",
    "The product is a bit heavy, making it less portable.",
    "I'm not sure I would buy this again, but it's been okay.",
    "The product is very versatile and can be used for many things.",
    "I'm a loyal customer of this brand, and they never disappoint.",
    "The product is a bit of a letdown. I expected more from this brand.",
    "I'm very happy with my purchase. It's been a great investment.",
    "The product is a bit flimsy. I'm worried it won't last long.",
    "I've recommended this to all my friends and family.",
    "The product is a bit of a novelty, but I enjoy using it.",
    "I'm very impressed with the quality of this product.",
    "The product is a bit of a disappointment. I wouldn't recommend it.",
    "I'm very satisfied with this product. It's been a great addition to my home.",
    "The product is a bit of a letdown. I expected more for the price.",
    "I'm very happy with my purchase. It's been a great value.",
    "The product is a bit of a novelty, but it's a fun one.",
    "I'm very impressed with the performance of this product.",
    "The product is a bit of a disappointment. I wouldn't buy it again.",
    "I'm very satisfied with this product. It's been a great experience.",
    "The product is a bit of a letdown. I expected better quality.",
    "I'm very happy with my purchase. It's been a great product.",
    "The product is a bit of a novelty, but it's a cool one.",
    "I'm very impressed with the design of this product.",
    "The product is a bit of a disappointment. I wouldn't recommend it to others.",
    "I'm very satisfied with this product. It's been a great tool.",
    "The product is a bit of a letdown. I expected more from the description.",
    "I'm very happy with my purchase. It's been a great addition to my collection.",
    "The product is a bit of a novelty, but it's a unique one."
]

def createReviews(minReviews, maxReviews):
    numReviews = random.randint(minReviews, maxReviews)
    reviews = []
    for _ in range(numReviews):
        year = random.randint(2018, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28) # To avoid month length issues
        reviews.append({
            "userDisplayName": random.choice(userNames),
            "rating": random.randint(1, 5),
            "comment": random.choice(comments),
            "date": datetime(year, month, day)
        })
    return reviews

products = [
    {
        "_id": ObjectId(),
        "name": "Dell XPS 15 9530",
        "sku": "ELE-LAP-0001",
        "price": Decimal128("1799.99"),
        "details": {
            "description": "Premium 15-inch laptop with stunning 4K OLED display and powerful Intel Core i7 processor",
            "specs": {
                "processor": "Intel Core i7-13700H",
                "ram": "32GB DDR5",
                "storage": "1TB NVMe SSD",
                "display": "15.6 inch 4K OLED",
                "graphics": "NVIDIA RTX 4050"
            }
        },
        "stock": 45,
        "category": {"main": "Electronics", "sub": "Laptops"},
        "vendor": {
            "companyName": vendors[0]["companyName"],
            "contactEmail": vendors[0]["contactEmail"],
            "supportPhone": vendors[0]["supportPhone"]
        },
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "MacBook Pro 16-inch M3 Pro",
        "sku": "ELE-LAP-0002",
        "price": Decimal128("2499.99"),
        "details": {
            "description": "Apple's most powerful laptop with M3 Pro chip and Liquid Retina XDR display",
            "specs": {
                "processor": "Apple M3 Pro 12-core",
                "ram": "36GB Unified Memory",
                "storage": "512GB SSD",
                "display": "16.2 inch Liquid Retina XDR",
                "graphics": "18-core GPU"
            }
        },
        "stock": 32,
        "category": {"main": "Electronics", "sub": "Laptops"},
        "vendor": {
            "companyName": vendors[1]["companyName"],
            "contactEmail": vendors[1]["contactEmail"],
            "supportPhone": vendors[1]["supportPhone"]
        },
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "ASUS ROG Strix G16",
        "sku": "ELE-LAP-0003",
        "price": Decimal128("1599.99"),
        "details": {
            "description": "Gaming laptop with high refresh rate display and RGB lighting",
            "specs": {
                "processor": "Intel Core i9-13980HX",
                "ram": "16GB DDR5",
                "storage": "1TB NVMe SSD",
                "display": "16 inch QHD 240Hz",
                "graphics": "NVIDIA RTX 4070"
            }
        },
        "stock": 28,
        "category": {"main": "Electronics", "sub": "Laptops"},
        "vendor": {
            "companyName": vendors[0]["companyName"],
            "contactEmail": vendors[0]["contactEmail"],
            "supportPhone": vendors[0]["supportPhone"]
        },
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "iPhone 15 Pro Max",
        "sku": "ELE-SMR-0001",
        "price": Decimal128("1199.99"),
        "details": {
            "description": "Apple's flagship smartphone with titanium design and A17 Pro chip",
            "specs": {
                "processor": "A17 Pro",
                "storage": "256GB",
                "display": "6.7 inch Super Retina XDR",
                "camera": "48MP Main + 12MP Ultra Wide + 12MP Telephoto",
                "connectivity": "5G"
            }
        },
        "stock": 67,
        "category": {"main": "Electronics", "sub": "Smartphones"},
        "vendor": {
            "companyName": vendors[1]["companyName"],
            "contactEmail": vendors[1]["contactEmail"],
            "supportPhone": vendors[1]["supportPhone"]
        },
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Samsung Galaxy S24 Ultra",
        "sku": "ELE-SMR-0002",
        "price": Decimal128("1299.99"),
        "details": {
            "description": "Samsung's premium smartphone with S Pen and 200MP camera",
            "specs": {
                "processor": "Snapdragon 8 Gen 3",
                "storage": "512GB",
                "display": "6.8 inch Dynamic AMOLED 2X",
                "camera": "200MP Main + 50MP Telephoto + 12MP Ultra Wide",
                "connectivity": "5G"
            }
        },
        "stock": 53,
        "category": {"main": "Electronics", "sub": "Smartphones"},
        "vendor": {
            "companyName": vendors[2]["companyName"],
            "contactEmail": vendors[2]["contactEmail"],
            "supportPhone": vendors[2]["supportPhone"]
        },
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Google Pixel 8 Pro",
        "sku": "ELE-SMR-0003",
        "price": Decimal128("999.99"),
        "details": {
            "description": "Google's flagship with advanced AI features and incredible camera",
            "specs": {
                "processor": "Google Tensor G3",
                "storage": "256GB",
                "display": "6.7 inch LTPO OLED",
                "camera": "50MP Main + 48MP Telephoto + 48MP Ultra Wide",
                "connectivity": "5G"
            }
        },
        "stock": 41,
        "category": {"main": "Electronics", "sub": "Smartphones"},
        "vendor": {
            "companyName": vendors[12]["companyName"],
            "contactEmail": vendors[12]["contactEmail"],
            "supportPhone": vendors[12]["supportPhone"]
        },
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Samsung Galaxy Tab S9 Ultra",
        "sku": "ELE-TAB-0001",
        "price": Decimal128("1199.99"),
        "details": {
            "description": "Massive 14.6-inch AMOLED tablet perfect for productivity and entertainment",
            "specs": {
                "processor": "Snapdragon 8 Gen 2",
                "ram": "12GB",
                "storage": "256GB",
                "display": "14.6 inch Dynamic AMOLED 2X",
                "battery": "11200mAh"
            }
        },
        "stock": 35,
        "category": {"main": "Electronics", "sub": "Tablets"},
        "vendor": {
            "companyName": vendors[2]["companyName"],
            "contactEmail": vendors[2]["contactEmail"],
            "supportPhone": vendors[2]["supportPhone"]
        },
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "iPad Pro 12.9-inch M2",
        "sku": "ELE-TAB-0002",
        "price": Decimal128("1099.99"),
        "details": {
            "description": "Apple's most powerful tablet with M2 chip and Liquid Retina XDR display",
            "specs": {
                "processor": "Apple M2",
                "ram": "8GB",
                "storage": "128GB",
                "display": "12.9 inch Liquid Retina XDR",
                "battery": "10758mAh"
            }
        },
        "stock": 48,
        "category": {"main": "Electronics", "sub": "Tablets"},
        "vendor": {
            "companyName": vendors[1]["companyName"],
            "contactEmail": vendors[1]["contactEmail"],
            "supportPhone": vendors[1]["supportPhone"]
        },
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "LG UltraWide 34WP65C-B",
        "sku": "ELE-MON-0001",
        "price": Decimal128("399.99"),
        "details": {
            "description": "34-inch curved ultrawide monitor perfect for multitasking",
            "specs": {
                "size": "34 inch",
                "resolution": "3440x1440",
                "refresh_rate": "75Hz",
                "panel_type": "IPS",
                "response_time": "5ms"
            }
        },
        "stock": 62,
        "category": {"main": "Electronics", "sub": "Monitors"},
        "vendor": {
            "companyName": vendors[3]["companyName"],
            "contactEmail": vendors[3]["contactEmail"],
            "supportPhone": vendors[3]["supportPhone"]
        },
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Dell UltraSharp U2723DE",
        "sku": "ELE-MON-0002",
        "price": Decimal128("549.99"),
        "details": {
            "description": "27-inch QHD monitor with USB-C connectivity and excellent color accuracy",
            "specs": {
                "size": "27 inch",
                "resolution": "2560x1440",
                "refresh_rate": "60Hz",
                "panel_type": "IPS Black",
                "response_time": "5ms"
            }
        },
        "stock": 71,
        "category": {"main": "Electronics", "sub": "Monitors"},
        "vendor": {
            "companyName": vendors[0]["companyName"],
            "contactEmail": vendors[0]["contactEmail"],
            "supportPhone": vendors[0]["supportPhone"]
        },
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Logitech MX Keys S",
        "sku": "ELE-KEY-0001",
        "price": Decimal128("119.99"),
        "details": {
            "description": "Premium wireless keyboard with smart illumination and comfortable typing",
            "specs": {
                "type": "Membrane",
                "connectivity": "Bluetooth + USB Receiver",
                "layout": "Full Size",
                "backlight": "Smart White",
                "switches": "Low-profile"
            }
        },
        "stock": 89,
        "category": {"main": "Electronics", "sub": "Keyboards"},
        "vendor": {
            "companyName": vendors[4]["companyName"],
            "contactEmail": vendors[4]["contactEmail"],
            "supportPhone": vendors[4]["supportPhone"]
        },
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Keychron K8 Pro",
        "sku": "ELE-KEY-0002",
        "price": Decimal128("109.99"),
        "details": {
            "description": "Hot-swappable mechanical keyboard with wireless connectivity",
            "specs": {
                "type": "Mechanical",
                "connectivity": "Bluetooth + Wired",
                "layout": "TKL",
                "backlight": "RGB",
                "switches": "Gateron G Pro Brown"
            }
        },
        "stock": 54,
        "category": {"main": "Electronics", "sub": "Keyboards"},
        "vendor": {
            "companyName": vendors[4]["companyName"],
            "contactEmail": vendors[4]["contactEmail"],
            "supportPhone": vendors[4]["supportPhone"]
        },
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Logitech MX Master 3S",
        "sku": "ELE-MOU-0001",
        "price": Decimal128("99.99"),
        "details": {
            "description": "Advanced wireless mouse with ultra-precise scrolling and customizable buttons",
            "specs": {
                "sensor": "Optical",
                "dpi": "8000 DPI",
                "connectivity": "Bluetooth + USB Receiver",
                "buttons": "8 buttons",
                "battery": "Rechargeable"
            }
        },
        "stock": 97,
        "category": {"main": "Electronics", "sub": "Mice"},
        "vendor": {
            "companyName": vendors[4]["companyName"],
            "contactEmail": vendors[4]["contactEmail"],
            "supportPhone": vendors[4]["supportPhone"]
        },
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Razer DeathAdder V3 Pro",
        "sku": "ELE-MOU-0002",
        "price": Decimal128("149.99"),
        "details": {
            "description": "Lightweight wireless gaming mouse with Focus Pro 30K sensor",
            "specs": {
                "sensor": "Optical",
                "dpi": "30000 DPI",
                "connectivity": "Wireless USB",
                "buttons": "8 buttons",
                "battery": "Rechargeable"
            }
        },
        "stock": 63,
        "category": {"main": "Electronics", "sub": "Mice"},
        "vendor": {
            "companyName": vendors[13]["companyName"],
            "contactEmail": vendors[13]["contactEmail"],
            "supportPhone": vendors[13]["supportPhone"]
        },
        "reviews": createReviews(4, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Breville Barista Express",
        "sku": "HOM-COF-0001",
        "price": Decimal128("699.99"),
        "details": {
            "description": "All-in-one espresso machine with built-in grinder",
            "specs": {
                "type": "Espresso",
                "capacity": "67oz water tank",
                "features": "Built-in Grinder, Milk Frother",
                "power": "1850W",
                "material": "Stainless Steel"
            }
        },
        "stock": 38,
        "category": {"main": "Home & Kitchen", "sub": "Coffee Makers"},
        "vendor": {
            "companyName": vendors[5]["companyName"],
            "contactEmail": vendors[5]["contactEmail"],
            "supportPhone": vendors[5]["supportPhone"]
        },
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Ninja Specialty Coffee Maker",
        "sku": "HOM-COF-0002",
        "price": Decimal128("179.99"),
        "details": {
            "description": "Versatile coffee maker with fold-away frother for specialty drinks",
            "specs": {
                "type": "Drip + Specialty",
                "capacity": "10 cups",
                "features": "Programmable, Thermal Carafe, Frother",
                "power": "1450W",
                "material": "Stainless Steel"
            }
        },
        "stock": 56,
        "category": {"main": "Home & Kitchen", "sub": "Coffee Makers"},
        "vendor": {
            "companyName": vendors[6]["companyName"],
            "contactEmail": vendors[6]["contactEmail"],
            "supportPhone": vendors[6]["supportPhone"]
        },
        "reviews": createReviews(4, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Ninja BN701 Professional Plus",
        "sku": "HOM-BLE-0001",
        "price": Decimal128("99.99"),
        "details": {
            "description": "Powerful blender with Auto-iQ programs and Total Crushing Technology",
            "specs": {
                "power": "1400W",
                "capacity": "72oz",
                "speeds": "3 speeds + Pulse",
                "features": "Auto-iQ, Total Crushing",
                "material": "Tritan"
            }
        },
        "stock": 73,
        "category": {"main": "Home & Kitchen", "sub": "Blenders"},
        "vendor": {
            "companyName": vendors[6]["companyName"],
            "contactEmail": vendors[6]["contactEmail"],
            "supportPhone": vendors[6]["supportPhone"]
        },
        "reviews": createReviews(5, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Vitamix E310 Explorian",
        "sku": "HOM-BLE-0002",
        "price": Decimal128("349.99"),
        "details": {
            "description": "Professional-grade blender with variable speed control and hardened blades",
            "specs": {
                "power": "1380W",
                "capacity": "48oz",
                "speeds": "Variable + Pulse",
                "features": "Self-Cleaning, Hardened Blades",
                "material": "Tritan"
            }
        },
        "stock": 42,
        "category": {"main": "Home & Kitchen", "sub": "Blenders"},
        "vendor": {
            "companyName": vendors[16]["companyName"],
            "contactEmail": vendors[16]["contactEmail"],
            "supportPhone": vendors[16]["supportPhone"]
        },
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Panasonic NN-SN966S",
        "sku": "HOM-MIC-0001",
        "price": Decimal128("249.99"),
        "details": {
            "description": "Countertop microwave with Inverter Technology for even cooking",
            "specs": {
                "capacity": "2.2 cu ft",
                "power": "1250W",
                "type": "Countertop",
                "features": "Inverter, Sensor Cook, Turbo Defrost",
                "control": "Digital Touch"
            }
        },
        "stock": 51,
        "category": {"main": "Home & Kitchen", "sub": "Microwaves"},
        "vendor": {
            "companyName": vendors[7]["companyName"],
            "contactEmail": vendors[7]["contactEmail"],
            "supportPhone": vendors[7]["supportPhone"]
        },
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Toshiba EM925A5A-BS",
        "sku": "HOM-MIC-0002",
        "price": Decimal128("89.99"),
        "details": {
            "description": "Compact microwave with sound on/off option and eco mode",
            "specs": {
                "capacity": "0.9 cu ft",
                "power": "900W",
                "type": "Countertop",
                "features": "Sound On/Off, Eco Mode, Position Memory",
                "control": "Digital"
            }
        },
        "stock": 84,
        "category": {"main": "Home & Kitchen", "sub": "Microwaves"},
        "vendor": {
            "companyName": vendors[7]["companyName"],
            "contactEmail": vendors[7]["contactEmail"],
            "supportPhone": vendors[7]["supportPhone"]
        },
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Nike Air Zoom Pegasus 40",
        "sku": "SPO-RUN-0001",
        "price": Decimal128("139.99"),
        "details": {
            "description": "Versatile running shoe with responsive cushioning for daily training",
            "specs": {
                "size": "10",
                "gender": "Men",
                "type": "Road",
                "cushioning": "Neutral",
                "drop": "10mm"
            }
        },
        "stock": 68,
        "category": {"main": "Sports", "sub": "Running Shoes"},
        "vendor": {
            "companyName": vendors[8]["companyName"],
            "contactEmail": vendors[8]["contactEmail"],
            "supportPhone": vendors[8]["supportPhone"]
        },
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Brooks Ghost 15",
        "sku": "SPO-RUN-0002",
        "price": Decimal128("149.99"),
        "details": {
            "description": "Smooth-riding running shoe with soft cushioning and smooth transitions",
            "specs": {
                "size": "9",
                "gender": "Women",
                "type": "Road",
                "cushioning": "Neutral",
                "drop": "12mm"
            }
        },
        "stock": 55,
        "category": {"main": "Sports", "sub": "Running Shoes"},
        "vendor": {
            "companyName": vendors[13]["companyName"],
            "contactEmail": vendors[13]["contactEmail"],
            "supportPhone": vendors[13]["supportPhone"]
        },
        "reviews": createReviews(5, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Gaiam Premium Yoga Mat",
        "sku": "SPO-YOG-0001",
        "price": Decimal128("29.99"),
        "details": {
            "description": "Eco-friendly yoga mat with excellent grip and cushioning",
            "specs": {
                "thickness": "6mm",
                "material": "TPE",
                "size": "72 inch",
                "texture": "Extra Grip",
                "eco_friendly": "Yes"
            }
        },
        "stock": 112,
        "category": {"main": "Sports", "sub": "Yoga Mats"},
        "vendor": {
            "companyName": vendors[9]["companyName"],
            "contactEmail": vendors[9]["contactEmail"],
            "supportPhone": vendors[9]["supportPhone"]
        },
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Manduka PRO Yoga Mat",
        "sku": "SPO-YOG-0002",
        "price": Decimal128("89.99"),
        "details": {
            "description": "Ultra-dense cushioning yoga mat with lifetime guarantee",
            "specs": {
                "thickness": "6mm",
                "material": "PVC",
                "size": "71 inch",
                "texture": "Textured",
                "eco_friendly": "No"
            }
        },
        "stock": 47,
        "category": {"main": "Sports", "sub": "Yoga Mats"},
        "vendor": {
            "companyName": vendors[9]["companyName"],
            "contactEmail": vendors[9]["contactEmail"],
            "supportPhone": vendors[9]["supportPhone"]
        },
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "CAP Barbell Adjustable Dumbbell Set",
        "sku": "SPO-DUM-0001",
        "price": Decimal128("199.99"),
        "details": {
            "description": "Space-saving adjustable dumbbell set with multiple weight options",
            "specs": {
                "weight": "50 lbs per dumbbell",
                "type": "Adjustable",
                "material": "Cast Iron",
                "grip": "Contoured",
                "set": "Pair"
            }
        },
        "stock": 33,
        "category": {"main": "Sports", "sub": "Dumbbells"},
        "vendor": {
            "companyName": vendors[10]["companyName"],
            "contactEmail": vendors[10]["contactEmail"],
            "supportPhone": vendors[10]["supportPhone"]
        },
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Bowflex SelectTech 552",
        "sku": "SPO-DUM-0002",
        "price": Decimal128("349.99"),
        "details": {
            "description": "Premium adjustable dumbbells with easy weight selection dial",
            "specs": {
                "weight": "5-52.5 lbs per dumbbell",
                "type": "Adjustable",
                "material": "Rubber Coated",
                "grip": "Contoured",
                "set": "Pair"
            }
        },
        "stock": 27,
        "category": {"main": "Sports", "sub": "Dumbbells"},
        "vendor": {
            "companyName": vendors[13]["companyName"],
            "contactEmail": vendors[13]["contactEmail"],
            "supportPhone": vendors[13]["supportPhone"]
        },
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "The Great Gatsby by F. Scott Fitzgerald",
        "sku": "BOO-FIC-0001",
        "price": Decimal128("14.99"),
        "details": {
            "description": "Classic American novel about the Jazz Age and the American Dream",
            "specs": {
                "format": "Paperback",
                "pages": "180",
                "language": "English",
                "publisher": "Scribner",
                "edition": "Reprint"
            }
        },
        "stock": 156,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {
            "companyName": vendors[11]["companyName"],
            "contactEmail": vendors[11]["contactEmail"],
            "supportPhone": vendors[11]["supportPhone"]
        },
        "reviews": createReviews(6, 12)
    },
    {
        "_id": ObjectId(),
        "name": "1984 by George Orwell",
        "sku": "BOO-FIC-0002",
        "price": Decimal128("16.99"),
        "details": {
            "description": "Dystopian novel about totalitarianism and government surveillance",
            "specs": {
                "format": "Paperback",
                "pages": "328",
                "language": "English",
                "publisher": "Signet Classic",
                "edition": "75th Anniversary Edition"
            }
        },
        "stock": 143,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {
            "companyName": vendors[14]["companyName"],
            "contactEmail": vendors[14]["contactEmail"],
            "supportPhone": vendors[14]["supportPhone"]
        },
        "reviews": createReviews(7, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Atomic Habits by James Clear",
        "sku": "BOO-NON-0001",
        "price": Decimal128("27.99"),
        "details": {
            "description": "Proven framework for improving every day with tiny changes",
            "specs": {
                "format": "Hardcover",
                "pages": "320",
                "language": "English",
                "publisher": "Avery",
                "edition": "1st Edition"
            }
        },
        "stock": 91,
        "category": {"main": "Books", "sub": "Non-Fiction"},
        "vendor": {
            "companyName": vendors[12]["companyName"],
            "contactEmail": vendors[12]["contactEmail"],
            "supportPhone": vendors[12]["supportPhone"]
        },
        "reviews": createReviews(8, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Thinking, Fast and Slow by Daniel Kahneman",
        "sku": "BOO-NON-0002",
        "price": Decimal128("19.99"),
        "details": {
            "description": "Groundbreaking exploration of the two systems that drive how we think",
            "specs": {
                "format": "Paperback",
                "pages": "499",
                "language": "English",
                "publisher": "Farrar, Straus and Giroux",
                "edition": "Reprint"
            }
        },
        "stock": 78,
        "category": {"main": "Books", "sub": "Non-Fiction"},
        "vendor": {
            "companyName": vendors[14]["companyName"],
            "contactEmail": vendors[14]["contactEmail"],
            "supportPhone": vendors[14]["supportPhone"]
        },
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Clean Code by Robert C. Martin",
        "sku": "BOO-TEC-0001",
        "price": Decimal128("44.99"),
        "details": {
            "description": "Handbook of agile software craftsmanship and best practices",
            "specs": {
                "format": "Paperback",
                "pages": "464",
                "language": "English",
                "publisher": "Prentice Hall",
                "topics": "Software Engineering, Best Practices, Refactoring"
            }
        },
        "stock": 64,
        "category": {"main": "Books", "sub": "Technical"},
        "vendor": {
            "companyName": vendors[13]["companyName"],
            "contactEmail": vendors[13]["contactEmail"],
            "supportPhone": vendors[13]["supportPhone"]
        },
        "reviews": createReviews(6, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Design Patterns by Gang of Four",
        "sku": "BOO-TEC-0002",
        "price": Decimal128("54.99"),
        "details": {
            "description": "Elements of reusable object-oriented software design",
            "specs": {
                "format": "Hardcover",
                "pages": "416",
                "language": "English",
                "publisher": "Addison-Wesley",
                "topics": "Design Patterns, OOP, Software Architecture"
            }
        },
        "stock": 52,
        "category": {"main": "Books", "sub": "Technical"},
        "vendor": {
            "companyName": vendors[13]["companyName"],
            "contactEmail": vendors[13]["contactEmail"],
            "supportPhone": vendors[13]["supportPhone"]
        },
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Uniqlo Supima Cotton T-Shirt",
        "sku": "CLO-TSH-0001",
        "price": Decimal128("19.99"),
        "details": {
            "description": "Premium cotton t-shirt with smooth texture and excellent durability",
            "specs": {
                "size": "M",
                "color": "White",
                "material": "100% Supima Cotton",
                "fit": "Regular",
                "sleeve": "Short Sleeve"
            }
        },
        "stock": 124,
        "category": {"main": "Clothing", "sub": "T-Shirts"},
        "vendor": {
            "companyName": vendors[14]["companyName"],
            "contactEmail": vendors[14]["contactEmail"],
            "supportPhone": vendors[14]["supportPhone"]
        },
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Hanes ComfortSoft T-Shirt Pack",
        "sku": "CLO-TSH-0002",
        "price": Decimal128("24.99"),
        "details": {
            "description": "Value pack of comfortable everyday t-shirts",
            "specs": {
                "size": "L",
                "color": "Black",
                "material": "Cotton Blend",
                "fit": "Relaxed",
                "sleeve": "Short Sleeve"
            }
        },
        "stock": 156,
        "category": {"main": "Clothing", "sub": "T-Shirts"},
        "vendor": {
            "companyName": vendors[15]["companyName"],
            "contactEmail": vendors[15]["contactEmail"],
            "supportPhone": vendors[15]["supportPhone"]
        },
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Levi's 501 Original Fit Jeans",
        "sku": "CLO-JEA-0001",
        "price": Decimal128("69.99"),
        "details": {
            "description": "Iconic straight-leg jeans with button fly and classic styling",
            "specs": {
                "size": "32x32",
                "fit": "Regular",
                "wash": "Dark Blue",
                "rise": "Mid Rise",
                "stretch": "Non-Stretch"
            }
        },
        "stock": 87,
        "category": {"main": "Clothing", "sub": "Jeans"},
        "vendor": {
            "companyName": vendors[15]["companyName"],
            "contactEmail": vendors[15]["contactEmail"],
            "supportPhone": vendors[15]["supportPhone"]
        },
        "reviews": createReviews(6, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Levi's 511 Slim Fit Jeans",
        "sku": "CLO-JEA-0002",
        "price": Decimal128("79.99"),
        "details": {
            "description": "Modern slim fit jeans with slight stretch for comfort",
            "specs": {
                "size": "32x34",
                "fit": "Slim",
                "wash": "Light Blue",
                "rise": "Mid Rise",
                "stretch": "Stretch"
            }
        },
        "stock": 94,
        "category": {"main": "Clothing", "sub": "Jeans"},
        "vendor": {
            "companyName": vendors[15]["companyName"],
            "contactEmail": vendors[15]["contactEmail"],
            "supportPhone": vendors[15]["supportPhone"]
        },
        "reviews": createReviews(5, 9)
    },
    {
        "_id": ObjectId(),
        "name": "The North Face ThermoBall Eco Jacket",
        "sku": "CLO-JAC-0001",
        "price": Decimal128("199.99"),
        "details": {
            "description": "Eco-friendly insulated jacket for lightweight warmth",
            "specs": {
                "size": "L",
                "color": "Black",
                "insulation": "ThermoBall Eco",
                "water_resistant": "Yes",
                "pockets": "3"
            }
        },
        "stock": 76,
        "category": {"main": "Clothing", "sub": "Jackets"},
        "vendor": {
            "companyName": vendors[16]["companyName"],
            "contactEmail": vendors[16]["contactEmail"],
            "supportPhone": vendors[16]["supportPhone"]
        },
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Patagonia Nano Puff Jacket",
        "sku": "CLO-JAC-0002",
        "price": Decimal128("229.99"),
        "details": {
            "description": "Windproof and water-resistant jacket with PrimaLoft Gold insulation",
            "specs": {
                "size": "M",
                "color": "Navy Blue",
                "insulation": "PrimaLoft Gold",
                "water_resistant": "Yes",
                "pockets": "3"
            }
        },
        "stock": 65,
        "category": {"main": "Clothing", "sub": "Jackets"},
        "vendor": {
            "companyName": vendors[16]["companyName"],
            "contactEmail": vendors[16]["contactEmail"],
            "supportPhone": vendors[16]["supportPhone"]
        },
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Sony WH-1000XM5",
        "sku": "ELE-HDP-0001",
        "price": Decimal128("399.99"),
        "details": {
            "description": "Industry-leading noise-canceling headphones with exceptional sound quality",
            "specs": {
                "type": "Over-Ear",
                "connectivity": "Bluetooth",
                "noise_canceling": "Yes",
                "battery_life": "30 hours",
                "driver_size": "30mm"
            }
        },
        "stock": 81,
        "category": {"main": "Electronics", "sub": "Headphones"},
        "vendor": {
            "companyName": vendors[17]["companyName"],
            "contactEmail": vendors[17]["contactEmail"],
            "supportPhone": vendors[17]["supportPhone"]
        },
        "reviews": createReviews(6, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Bose QuietComfort Ultra",
        "sku": "ELE-HDP-0002",
        "price": Decimal128("429.99"),
        "details": {
            "description": "Premium noise-canceling headphones with immersive audio and custom tuning",
            "specs": {
                "type": "Over-Ear",
                "connectivity": "Bluetooth",
                "noise_canceling": "Yes",
                "battery_life": "24 hours",
                "driver_size": "40mm"
            }
        },
        "stock": 73,
        "category": {"main": "Electronics", "sub": "Headphones"},
        "vendor": {
            "companyName": vendors[17]["companyName"],
            "contactEmail": vendors[17]["contactEmail"],
            "supportPhone": vendors[17]["supportPhone"]
        },
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Instant Pot Duo 7-in-1",
        "sku": "HOM-CKW-0001",
        "price": Decimal128("99.99"),
        "details": {
            "description": "Multi-functional pressure cooker, slow cooker, rice cooker, and more",
            "specs": {
                "capacity": "6 quarts",
                "functions": "7",
                "power": "1000W",
                "material": "Stainless Steel",
                "programs": "13"
            }
        },
        "stock": 102,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {
            "companyName": vendors[18]["companyName"],
            "contactEmail": vendors[18]["contactEmail"],
            "supportPhone": vendors[18]["supportPhone"]
        },
        "reviews": createReviews(7, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Lodge Cast Iron Skillet 12-inch",
        "sku": "HOM-CKW-0002",
        "price": Decimal128("29.99"),
        "details": {
            "description": "Pre-seasoned cast iron skillet for versatile cooking",
            "specs": {
                "size": "12 inch",
                "material": "Cast Iron",
                "pre_seasoned": "Yes",
                "heat_source": "All",
                "handle": "Integrated"
            }
        },
        "stock": 134,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {
            "companyName": vendors[18]["companyName"],
            "contactEmail": vendors[18]["contactEmail"],
            "supportPhone": vendors[18]["supportPhone"]
        },
        "reviews": createReviews(6, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Osprey Atmos AG 65",
        "sku": "OUT-BCK-0001",
        "price": Decimal128("270.00"),
        "details": {
            "description": "Award-winning backpacking pack with anti-gravity suspension",
            "specs": {
                "capacity": "65 liters",
                "suspension": "Anti-Gravity",
                "torso_size": "M",
                "pockets": "9",
                "raincover_included": "Yes"
            }
        },
        "stock": 49,
        "category": {"main": "Outdoor", "sub": "Backpacks"},
        "vendor": {
            "companyName": vendors[19]["companyName"],
            "contactEmail": vendors[19]["contactEmail"],
            "supportPhone": vendors[19]["supportPhone"]
        },
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Marmot Tungsten 2P Tent",
        "sku": "OUT-TNT-0001",
        "price": Decimal128("219.99"),
        "details": {
            "description": "Durable and spacious 2-person tent for backpacking and camping",
            "specs": {
                "capacity": "2 person",
                "season": "3-Season",
                "weight": "5 lbs 4 oz",
                "doors": "2",
                "floor_area": "32 sq ft"
            }
        },
        "stock": 41,
        "category": {"main": "Outdoor", "sub": "Tents"},
        "vendor": {
            "companyName": vendors[19]["companyName"],
            "contactEmail": vendors[19]["contactEmail"],
            "supportPhone": vendors[19]["supportPhone"]
        },
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Canon EOS R6 Mark II",
        "sku": "ELE-CAM-0001",
        "price": Decimal128("2499.00"),
        "details": {
            "description": "Full-frame mirrorless camera with advanced autofocus and video capabilities",
            "specs": {
                "sensor": "24.2MP Full-Frame CMOS",
                "autofocus": "Dual Pixel CMOS AF II",
                "video": "4K 60p",
                "stabilization": "5-axis IBIS",
                "viewfinder": "3.69m-dot OLED EVF"
            }
        },
        "stock": 29,
        "category": {"main": "Electronics", "sub": "Cameras"},
        "vendor": {
            "companyName": vendors[20]["companyName"],
            "contactEmail": vendors[20]["contactEmail"],
            "supportPhone": vendors[20]["supportPhone"]
        },
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Sony a7 IV",
        "sku": "ELE-CAM-0002",
        "price": Decimal128("2499.99"),
        "details": {
            "description": "Hybrid mirrorless camera with 33MP sensor and real-time tracking AF",
            "specs": {
                "sensor": "33MP Full-Frame Exmor R CMOS",
                "autofocus": "Real-time Tracking AF",
                "video": "4K 60p",
                "stabilization": "5-axis SteadyShot",
                "viewfinder": "3.68m-dot OLED EVF"
            }
        },
        "stock": 34,
        "category": {"main": "Electronics", "sub": "Cameras"},
        "vendor": {
            "companyName": vendors[20]["companyName"],
            "contactEmail": vendors[20]["contactEmail"],
            "supportPhone": vendors[20]["supportPhone"]
        },
        "reviews": createReviews(6, 11)
    },
    {
        "_id": ObjectId(),
        "name": "DJI Mini 4 Pro",
        "sku": "ELE-DRN-0001",
        "price": Decimal128("759.00"),
        "details": {
            "description": "Compact and lightweight drone with 4K HDR video and obstacle sensing",
            "specs": {
                "weight": "Under 249g",
                "video": "4K/60fps HDR",
                "flight_time": "34 mins",
                "obstacle_sensing": "Omnidirectional",
                "transmission": "OcuSync 4"
            }
        },
        "stock": 58,
        "category": {"main": "Electronics", "sub": "Drones"},
        "vendor": {
            "companyName": vendors[21]["companyName"],
            "contactEmail": vendors[21]["contactEmail"],
            "supportPhone": vendors[21]["supportPhone"]
        },
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Autel Robotics EVO Lite+",
        "sku": "ELE-DRN-0002",
        "price": Decimal128("1549.00"),
        "details": {
            "description": "Powerful drone with 1-inch CMOS sensor and 6K video resolution",
            "specs": {
                "weight": "835g",
                "video": "6K/30fps",
                "flight_time": "40 mins",
                "obstacle_sensing": "3-way",
                "transmission": "SkyLink"
            }
        },
        "stock": 37,
        "category": {"main": "Electronics", "sub": "Drones"},
        "vendor": {
            "companyName": vendors[21]["companyName"],
            "contactEmail": vendors[21]["contactEmail"],
            "supportPhone": vendors[21]["supportPhone"]
        },
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Herman Miller Aeron Chair",
        "sku": "OFF-CHR-0001",
        "price": Decimal128("1645.00"),
        "details": {
            "description": "Ergonomic office chair with advanced posture support",
            "specs": {
                "size": "B",
                "material": "Pellicle Mesh",
                "adjustments": "8",
                "lumbar_support": "Adjustable PostureFit SL",
                "armrests": "Fully Adjustable"
            }
        },
        "stock": 22,
        "category": {"main": "Office", "sub": "Chairs"},
        "vendor": {
            "companyName": vendors[22]["companyName"],
            "contactEmail": vendors[22]["contactEmail"],
            "supportPhone": vendors[22]["supportPhone"]
        },
        "reviews": createReviews(7, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Steelcase Gesture Chair",
        "sku": "OFF-CHR-0002",
        "price": Decimal128("1350.00"),
        "details": {
            "description": "Office chair designed to support a wide range of postures and technologies",
            "specs": {
                "size": "Standard",
                "material": "Fabric",
                "adjustments": "Multiple",
                "lumbar_support": "Adjustable",
                "armrests": "360-degree"
            }
        },
        "stock": 31,
        "category": {"main": "Office", "sub": "Chairs"},
        "vendor": {
            "companyName": vendors[22]["companyName"],
            "contactEmail": vendors[22]["contactEmail"],
            "supportPhone": vendors[22]["supportPhone"]
        },
        "reviews": createReviews(6, 13)
    },
    {
        "_id": ObjectId(),
        "name": "LEGO Icons Concorde",
        "sku": "TOY-LEG-0001",
        "price": Decimal128("199.99"),
        "details": {
            "description": "Detailed replica model of the iconic supersonic passenger jet",
            "specs": {
                "pieces": "2083",
                "age": "18+",
                "dimensions": "41.5\" long, 17\" wide",
                "features": "Tiltable nose, functional landing gear",
                "series": "Icons"
            }
        },
        "stock": 45,
        "category": {"main": "Toys", "sub": "LEGO"},
        "vendor": {
            "companyName": vendors[23]["companyName"],
            "contactEmail": vendors[23]["contactEmail"],
            "supportPhone": vendors[23]["supportPhone"]
        },
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Settlers of Catan",
        "sku": "TOY-BRD-0001",
        "price": Decimal128("49.99"),
        "details": {
            "description": "Classic board game of trading, building, and settling",
            "specs": {
                "players": "3-4",
                "play_time": "60-90 mins",
                "age": "10+",
                "genre": "Strategy",
                "expansion_available": "Yes"
            }
        },
        "stock": 88,
        "category": {"main": "Toys", "sub": "Board Games"},
        "vendor": {
            "companyName": vendors[24]["companyName"],
            "contactEmail": vendors[24]["contactEmail"],
            "supportPhone": vendors[24]["supportPhone"]
        },
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "GoPro HERO12 Black",
        "sku": "ELE-ACT-0001",
        "price": Decimal128("399.99"),
        "details": {
            "description": "Waterproof action camera with 5.3K video and HyperSmooth 6.0 stabilization",
            "specs": {
                "video": "5.3K60, 4K120",
                "photo": "27MP",
                "waterproof": "33ft",
                "stabilization": "HyperSmooth 6.0",
                "battery": "Enduro"
            }
        },
        "stock": 67,
        "category": {"main": "Electronics", "sub": "Action Cameras"},
        "vendor": {
            "companyName": vendors[21]["companyName"],
            "contactEmail": vendors[21]["contactEmail"],
            "supportPhone": vendors[21]["supportPhone"]
        },
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Nintendo Switch OLED",
        "sku": "ELE-CON-0001",
        "price": Decimal128("349.99"),
        "details": {
            "description": "Handheld-home console hybrid with a vibrant 7-inch OLED screen",
            "specs": {
                "storage": "64GB",
                "display": "7-inch OLED",
                "connectivity": "Wi-Fi, Bluetooth",
                "modes": "TV, Tabletop, Handheld",
                "controllers": "Joy-Con"
            }
        },
        "stock": 95,
        "category": {"main": "Electronics", "sub": "Gaming Consoles"},
        "vendor": {
            "companyName": vendors[20]["companyName"],
            "contactEmail": vendors[20]["contactEmail"],
            "supportPhone": vendors[20]["supportPhone"]
        },
        "reviews": createReviews(6, 13)
    },
    {
        "_id": ObjectId(),
        "name": "PlayStation 5 Slim",
        "sku": "ELE-CON-0002",
        "price": Decimal128("499.99"),
        "details": {
            "description": "Next-gen gaming console with ultra-high-speed SSD and haptic feedback",
            "specs": {
                "storage": "1TB SSD",
                "cpu": "AMD Zen 2",
                "gpu": "AMD RDNA 2",
                "resolution": "Up to 8K",
                "features": "Ray Tracing, 3D Audio"
            }
        },
        "stock": 72,
        "category": {"main": "Electronics", "sub": "Gaming Consoles"},
        "vendor": {
            "companyName": vendors[17]["companyName"],
            "contactEmail": vendors[17]["contactEmail"],
            "supportPhone": vendors[17]["supportPhone"]
        },
        "reviews": createReviews(7, 15)
    },
    {
        "_id": ObjectId(),
        "name": "The North Face ThermoBall Eco Jacket",
        "sku": "CLO-JAC-0001",
        "price": Decimal128("199.99"),
        "details": {
            "description": "Eco-friendly insulated jacket for lightweight warmth",
            "specs": {
                "size": "L",
                "color": "Black",
                "insulation": "ThermoBall Eco",
                "water_resistant": "Yes",
                "pockets": "3"
            }
        },
        "stock": 76,
        "category": {"main": "Clothing", "sub": "Jackets"},
        "vendor": {
            "companyName": vendors[16]["companyName"],
            "contactEmail": vendors[16]["contactEmail"],
            "supportPhone": vendors[16]["supportPhone"]
        },
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Patagonia Nano Puff Jacket",
        "sku": "CLO-JAC-0002",
        "price": Decimal128("229.99"),
        "details": {
            "description": "Windproof and water-resistant jacket with PrimaLoft Gold insulation",
            "specs": {
                "size": "M",
                "color": "Navy Blue",
                "insulation": "PrimaLoft Gold",
                "water_resistant": "Yes",
                "pockets": "3"
            }
        },
        "stock": 65,
        "category": {"main": "Clothing", "sub": "Jackets"},
        "vendor": {
            "companyName": vendors[16]["companyName"],
            "contactEmail": vendors[16]["contactEmail"],
            "supportPhone": vendors[16]["supportPhone"]
        },
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Sony WH-1000XM5",
        "sku": "ELE-HDP-0001",
        "price": Decimal128("399.99"),
        "details": {
            "description": "Industry-leading noise-canceling headphones with exceptional sound quality",
            "specs": {
                "type": "Over-Ear",
                "connectivity": "Bluetooth",
                "noise_canceling": "Yes",
                "battery_life": "30 hours",
                "driver_size": "30mm"
            }
        },
        "stock": 81,
        "category": {"main": "Electronics", "sub": "Headphones"},
        "vendor": {
            "companyName": vendors[17]["companyName"],
            "contactEmail": vendors[17]["contactEmail"],
            "supportPhone": vendors[17]["supportPhone"]
        },
        "reviews": createReviews(6, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Bose QuietComfort Ultra",
        "sku": "ELE-HDP-0002",
        "price": Decimal128("429.99"),
        "details": {
            "description": "Premium noise-canceling headphones with immersive audio and custom tuning",
            "specs": {
                "type": "Over-Ear",
                "connectivity": "Bluetooth",
                "noise_canceling": "Yes",
                "battery_life": "24 hours",
                "driver_size": "40mm"
            }
        },
        "stock": 73,
        "category": {"main": "Electronics", "sub": "Headphones"},
        "vendor": {
            "companyName": vendors[17]["companyName"],
            "contactEmail": vendors[17]["contactEmail"],
            "supportPhone": vendors[17]["supportPhone"]
        },
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Instant Pot Duo 7-in-1",
        "sku": "HOM-CKW-0001",
        "price": Decimal128("99.99"),
        "details": {
            "description": "Multi-functional pressure cooker, slow cooker, rice cooker, and more",
            "specs": {
                "capacity": "6 quarts",
                "functions": "7",
                "power": "1000W",
                "material": "Stainless Steel",
                "programs": "13"
            }
        },
        "stock": 102,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {
            "companyName": vendors[18]["companyName"],
            "contactEmail": vendors[18]["contactEmail"],
            "supportPhone": vendors[18]["supportPhone"]
        },
        "reviews": createReviews(7, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Lodge Cast Iron Skillet 12-inch",
        "sku": "HOM-CKW-0002",
        "price": Decimal128("29.99"),
        "details": {
            "description": "Pre-seasoned cast iron skillet for versatile cooking",
            "specs": {
                "size": "12 inch",
                "material": "Cast Iron",
                "pre_seasoned": "Yes",
                "heat_source": "All",
                "handle": "Integrated"
            }
        },
        "stock": 134,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {
            "companyName": vendors[18]["companyName"],
            "contactEmail": vendors[18]["contactEmail"],
            "supportPhone": vendors[18]["supportPhone"]
        },
        "reviews": createReviews(6, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Osprey Atmos AG 65",
        "sku": "OUT-BCK-0001",
        "price": Decimal128("270.00"),
        "details": {
            "description": "Award-winning backpacking pack with anti-gravity suspension",
            "specs": {
                "capacity": "65 liters",
                "suspension": "Anti-Gravity",
                "torso_size": "M",
                "pockets": "9",
                "raincover_included": "Yes"
            }
        },
        "stock": 49,
        "category": {"main": "Outdoor", "sub": "Backpacks"},
        "vendor": {
            "companyName": vendors[19]["companyName"],
            "contactEmail": vendors[19]["contactEmail"],
            "supportPhone": vendors[19]["supportPhone"]
        },
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Marmot Tungsten 2P Tent",
        "sku": "OUT-TNT-0001",
        "price": Decimal128("219.99"),
        "details": {
            "description": "Durable and spacious 2-person tent for backpacking and camping",
            "specs": {
                "capacity": "2 person",
                "season": "3-Season",
                "weight": "5 lbs 4 oz",
                "doors": "2",
                "floor_area": "32 sq ft"
            }
        },
        "stock": 41,
        "category": {"main": "Outdoor", "sub": "Tents"},
        "vendor": {
            "companyName": vendors[19]["companyName"],
            "contactEmail": vendors[19]["contactEmail"],
            "supportPhone": vendors[19]["supportPhone"]
        },
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Canon EOS R6 Mark II",
        "sku": "ELE-CAM-0001",
        "price": Decimal128("2499.00"),
        "details": {
            "description": "Full-frame mirrorless camera with advanced autofocus and video capabilities",
            "specs": {
                "sensor": "24.2MP Full-Frame CMOS",
                "autofocus": "Dual Pixel CMOS AF II",
                "video": "4K 60p",
                "stabilization": "5-axis IBIS",
                "viewfinder": "3.69m-dot OLED EVF"
            }
        },
        "stock": 29,
        "category": {"main": "Electronics", "sub": "Cameras"},
        "vendor": {
            "companyName": vendors[20]["companyName"],
            "contactEmail": vendors[20]["contactEmail"],
            "supportPhone": vendors[20]["supportPhone"]
        },
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Sony a7 IV",
        "sku": "ELE-CAM-0002",
        "price": Decimal128("2499.99"),
        "details": {
            "description": "Hybrid mirrorless camera with 33MP sensor and real-time tracking AF",
            "specs": {
                "sensor": "33MP Full-Frame Exmor R CMOS",
                "autofocus": "Real-time Tracking AF",
                "video": "4K 60p",
                "stabilization": "5-axis SteadyShot",
                "viewfinder": "3.68m-dot OLED EVF"
            }
        },
        "stock": 34,
        "category": {"main": "Electronics", "sub": "Cameras"},
        "vendor": {
            "companyName": vendors[20]["companyName"],
            "contactEmail": vendors[20]["contactEmail"],
            "supportPhone": vendors[20]["supportPhone"]
        },
        "reviews": createReviews(6, 11)
    },
    {
        "_id": ObjectId(),
        "name": "DJI Mini 4 Pro",
        "sku": "ELE-DRN-0001",
        "price": Decimal128("759.00"),
        "details": {
            "description": "Compact and lightweight drone with 4K HDR video and obstacle sensing",
            "specs": {
                "weight": "Under 249g",
                "video": "4K/60fps HDR",
                "flight_time": "34 mins",
                "obstacle_sensing": "Omnidirectional",
                "transmission": "OcuSync 4"
            }
        },
        "stock": 58,
        "category": {"main": "Electronics", "sub": "Drones"},
        "vendor": {
            "companyName": vendors[21]["companyName"],
            "contactEmail": vendors[21]["contactEmail"],
            "supportPhone": vendors[21]["supportPhone"]
        },
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Autel Robotics EVO Lite+",
        "sku": "ELE-DRN-0002",
        "price": Decimal128("1549.00"),
        "details": {
            "description": "Powerful drone with 1-inch CMOS sensor and 6K video resolution",
            "specs": {
                "weight": "835g",
                "video": "6K/30fps",
                "flight_time": "40 mins",
                "obstacle_sensing": "3-way",
                "transmission": "SkyLink"
            }
        },
        "stock": 37,
        "category": {"main": "Electronics", "sub": "Drones"},
        "vendor": {
            "companyName": vendors[21]["companyName"],
            "contactEmail": vendors[21]["contactEmail"],
            "supportPhone": vendors[21]["supportPhone"]
        },
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Herman Miller Aeron Chair",
        "sku": "OFF-CHR-0001",
        "price": Decimal128("1645.00"),
        "details": {
            "description": "Ergonomic office chair with advanced posture support",
            "specs": {
                "size": "B",
                "material": "Pellicle Mesh",
                "adjustments": "8",
                "lumbar_support": "Adjustable PostureFit SL",
                "armrests": "Fully Adjustable"
            }
        },
        "stock": 22,
        "category": {"main": "Office", "sub": "Chairs"},
        "vendor": {
            "companyName": vendors[22]["companyName"],
            "contactEmail": vendors[22]["contactEmail"],
            "supportPhone": vendors[22]["supportPhone"]
        },
        "reviews": createReviews(7, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Steelcase Gesture Chair",
        "sku": "OFF-CHR-0002",
        "price": Decimal128("1350.00"),
        "details": {
            "description": "Office chair designed to support a wide range of postures and technologies",
            "specs": {
                "size": "Standard",
                "material": "Fabric",
                "adjustments": "Multiple",
                "lumbar_support": "Adjustable",
                "armrests": "360-degree"
            }
        },
        "stock": 31,
        "category": {"main": "Office", "sub": "Chairs"},
        "vendor": {
            "companyName": vendors[22]["companyName"],
            "contactEmail": vendors[22]["contactEmail"],
            "supportPhone": vendors[22]["supportPhone"]
        },
        "reviews": createReviews(6, 13)
    },
    {
        "_id": ObjectId(),
        "name": "LEGO Icons Concorde",
        "sku": "TOY-LEG-0001",
        "price": Decimal128("199.99"),
        "details": {
            "description": "Detailed replica model of the iconic supersonic passenger jet",
            "specs": {
                "pieces": "2083",
                "age": "18+",
                "dimensions": "41.5\" long, 17\" wide",
                "features": "Tiltable nose, functional landing gear",
                "series": "Icons"
            }
        },
        "stock": 45,
        "category": {"main": "Toys", "sub": "LEGO"},
        "vendor": {
            "companyName": vendors[23]["companyName"],
            "contactEmail": vendors[23]["contactEmail"],
            "supportPhone": vendors[23]["supportPhone"]
        },
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Settlers of Catan",
        "sku": "TOY-BRD-0001",
        "price": Decimal128("49.99"),
        "details": {
            "description": "Classic board game of trading, building, and settling",
            "specs": {
                "players": "3-4",
                "play_time": "60-90 mins",
                "age": "10+",
                "genre": "Strategy",
                "expansion_available": "Yes"
            }
        },
        "stock": 88,
        "category": {"main": "Toys", "sub": "Board Games"},
        "vendor": {
            "companyName": vendors[24]["companyName"],
            "contactEmail": vendors[24]["contactEmail"],
            "supportPhone": vendors[24]["supportPhone"]
        },
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "GoPro HERO12 Black",
        "sku": "ELE-ACT-0001",
        "price": Decimal128("399.99"),
        "details": {
            "description": "Waterproof action camera with 5.3K video and HyperSmooth 6.0 stabilization",
            "specs": {
                "video": "5.3K60, 4K120",
                "photo": "27MP",
                "waterproof": "33ft",
                "stabilization": "HyperSmooth 6.0",
                "battery": "Enduro"
            }
        },
        "stock": 67,
        "category": {"main": "Electronics", "sub": "Action Cameras"},
        "vendor": {
            "companyName": vendors[21]["companyName"],
            "contactEmail": vendors[21]["contactEmail"],
            "supportPhone": vendors[21]["supportPhone"]
        },
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Nintendo Switch OLED",
        "sku": "ELE-CON-0001",
        "price": Decimal128("349.99"),
        "details": {
            "description": "Handheld-home console hybrid with a vibrant 7-inch OLED screen",
            "specs": {
                "storage": "64GB",
                "display": "7-inch OLED",
                "connectivity": "Wi-Fi, Bluetooth",
                "modes": "TV, Tabletop, Handheld",
                "controllers": "Joy-Con"
            }
        },
        "stock": 95,
        "category": {"main": "Electronics", "sub": "Gaming Consoles"},
        "vendor": {
            "companyName": vendors[20]["companyName"],
            "contactEmail": vendors[20]["contactEmail"],
            "supportPhone": vendors[20]["supportPhone"]
        },
        "reviews": createReviews(6, 13)
    },
    {
        "_id": ObjectId(),
        "name": "PlayStation 5 Slim",
        "sku": "ELE-CON-0002",
        "price": Decimal128("499.99"),
        "details": {
            "description": "Next-gen gaming console with ultra-high-speed SSD and haptic feedback",
            "specs": {
                "storage": "1TB SSD",
                "cpu": "AMD Zen 2",
                "gpu": "AMD RDNA 2",
                "resolution": "Up to 8K",
                "features": "Ray Tracing, 3D Audio"
            }
        },
        "stock": 72,
        "category": {"main": "Electronics", "sub": "Gaming Consoles"},
        "vendor": {
            "companyName": vendors[17]["companyName"],
            "contactEmail": vendors[17]["contactEmail"],
            "supportPhone": vendors[17]["supportPhone"]
        },
        "reviews": createReviews(7, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Nebula X1 Smartwatch",
        "sku": "ELE-WEA-1001",
        "price": Decimal128("149.99"),
        "details": {"description": "Waterproof smartwatch with AMOLED display.", "specs": {"battery": "5 days", "color": "Black"}},
        "stock": 120,
        "category": {"main": "Electronics", "sub": "Wearables"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "CyberBass 300 Headphones",
        "sku": "ELE-AUD-1002",
        "price": Decimal128("89.99"),
        "details": {"description": "Deep bass wireless headphones.", "specs": {"driver": "40mm", "type": "Over-ear"}},
        "stock": 85,
        "category": {"main": "Electronics", "sub": "Audio"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "VisionPro 4K Webcam",
        "sku": "ELE-CAM-1003",
        "price": Decimal128("129.50"),
        "details": {"description": "Streaming webcam with ring light.", "specs": {"resolution": "4K", "connection": "USB-C"}},
        "stock": 45,
        "category": {"main": "Electronics", "sub": "Cameras"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "ChefMaster Steel Knife Set",
        "sku": "HOM-KIT-1004",
        "price": Decimal128("79.99"),
        "details": {"description": "Professional 5-piece knife set.", "specs": {"material": "Stainless Steel", "pieces": "5"}},
        "stock": 60,
        "category": {"main": "Home & Kitchen", "sub": "Cutlery"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "CozyCloud Pillow",
        "sku": "HOM-BED-1005",
        "price": Decimal128("35.00"),
        "details": {"description": "Memory foam pillow for neck support.", "specs": {"firmness": "Medium", "size": "Standard"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Bedding"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(6, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Sprint Elite Running Shoes",
        "sku": "SPO-RUN-1006",
        "price": Decimal128("110.00"),
        "details": {"description": "Lightweight shoes for marathon runners.", "specs": {"size": "42", "gender": "Men"}},
        "stock": 30,
        "category": {"main": "Sports", "sub": "Running"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "FlexGrip Yoga Mat",
        "sku": "SPO-YOG-1007",
        "price": Decimal128("25.99"),
        "details": {"description": "Non-slip yoga mat with carrying strap.", "specs": {"thickness": "6mm", "material": "TPE"}},
        "stock": 150,
        "category": {"main": "Sports", "sub": "Yoga"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "The Future of AI",
        "sku": "BOO-TEC-1008",
        "price": Decimal128("29.95"),
        "details": {"description": "Comprehensive guide to artificial intelligence.", "specs": {"pages": "320", "format": "Hardcover"}},
        "stock": 90,
        "category": {"main": "Books", "sub": "Technical"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Denim Jacket",
        "sku": "CLO-JAC-1009",
        "price": Decimal128("65.00"),
        "details": {"description": "Vintage style denim jacket.", "specs": {"color": "Blue", "size": "L"}},
        "stock": 75,
        "category": {"main": "Clothing", "sub": "Jackets"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Urban Cotton Hoodie",
        "sku": "CLO-TOP-1010",
        "price": Decimal128("45.00"),
        "details": {"description": "Soft fleece hoodie for daily wear.", "specs": {"color": "Grey", "size": "M"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "GamerStrike Mechanical Keyboard",
        "sku": "ELE-KEY-1011",
        "price": Decimal128("129.99"),
        "details": {"description": "RGB mechanical keyboard with blue switches.", "specs": {"switch": "Blue", "layout": "Full"}},
        "stock": 55,
        "category": {"main": "Electronics", "sub": "Peripherals"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "SilentClick Wireless Mouse",
        "sku": "ELE-MOU-1012",
        "price": Decimal128("39.99"),
        "details": {"description": "Ergonomic silent mouse for office use.", "specs": {"dpi": "1600", "battery": "AA"}},
        "stock": 130,
        "category": {"main": "Electronics", "sub": "Peripherals"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "PureAir Room Purifier",
        "sku": "HOM-APP-1013",
        "price": Decimal128("199.00"),
        "details": {"description": "HEPA filter air purifier for allergies.", "specs": {"coverage": "300 sq ft", "noise": "24dB"}},
        "stock": 40,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Bamboo Cutting Board",
        "sku": "HOM-KIT-1014",
        "price": Decimal128("22.50"),
        "details": {"description": "Eco-friendly bamboo cutting board.", "specs": {"size": "Large", "material": "Bamboo"}},
        "stock": 95,
        "category": {"main": "Home & Kitchen", "sub": "Kitchenware"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "PowerLift Dumbbell Set",
        "sku": "SPO-GYM-1015",
        "price": Decimal128("85.00"),
        "details": {"description": "Pair of 10kg rubber coated dumbbells.", "specs": {"weight": "2x10kg", "material": "Rubber"}},
        "stock": 25,
        "category": {"main": "Sports", "sub": "Weights"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(6, 12)
    },
    {
        "_id": ObjectId(),
        "name": "TrailBlazer Hiking Boots",
        "sku": "SPO-OUT-1016",
        "price": Decimal128("145.00"),
        "details": {"description": "Waterproof boots for rough terrain.", "specs": {"size": "43", "waterproof": "Yes"}},
        "stock": 35,
        "category": {"main": "Sports", "sub": "Outdoor"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Mystery of the Old Manor",
        "sku": "BOO-FIC-1017",
        "price": Decimal128("14.99"),
        "details": {"description": "A thrilling mystery novel set in 1920s.", "specs": {"author": "A. Christie", "pages": "280"}},
        "stock": 150,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Silk Touch Scarf",
        "sku": "CLO-ACC-1018",
        "price": Decimal128("29.99"),
        "details": {"description": "Elegant silk scarf for formal occasions.", "specs": {"material": "Silk", "pattern": "Floral"}},
        "stock": 80,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "RapidCharge 20000mAh",
        "sku": "ELE-ACC-1019",
        "price": Decimal128("49.99"),
        "details": {"description": "High capacity power bank with fast charging.", "specs": {"capacity": "20000mAh", "ports": "3"}},
        "stock": 200,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Crystal Clear 27 Monitor",
        "sku": "ELE-MON-1020",
        "price": Decimal128("220.00"),
        "details": {"description": "27 inch IPS monitor for graphic design.", "specs": {"refresh": "75Hz", "panel": "IPS"}},
        "stock": 45,
        "category": {"main": "Electronics", "sub": "Monitors"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Ceramic Flower Vase",
        "sku": "HOM-DEC-1021",
        "price": Decimal128("32.00"),
        "details": {"description": "Minimalist white ceramic vase.", "specs": {"height": "25cm", "style": "Modern"}},
        "stock": 60,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Velvet Throw Blanket",
        "sku": "HOM-DEC-1022",
        "price": Decimal128("55.00"),
        "details": {"description": "Luxurious velvet throw for sofa.", "specs": {"color": "Emerald", "size": "150x200cm"}},
        "stock": 90,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "ProForm Resistance Bands",
        "sku": "SPO-FIT-1023",
        "price": Decimal128("19.99"),
        "details": {"description": "Set of 5 resistance bands for home workout.", "specs": {"material": "Latex", "levels": "5"}},
        "stock": 300,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(7, 18)
    },
    {
        "_id": ObjectId(),
        "name": "HydroMate Water Bottle",
        "sku": "SPO-ACC-1024",
        "price": Decimal128("15.99"),
        "details": {"description": "Insulated stainless steel water bottle.", "specs": {"capacity": "1L", "insulation": "24h Cold"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Learn Python in 30 Days",
        "sku": "BOO-TEC-1025",
        "price": Decimal128("34.99"),
        "details": {"description": "Beginner friendly guide to Python programming.", "specs": {"pages": "400", "language": "English"}},
        "stock": 100,
        "category": {"main": "Books", "sub": "Education"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Summer Floral Dress",
        "sku": "CLO-DRE-1026",
        "price": Decimal128("59.99"),
        "details": {"description": "Lightweight cotton dress for summer.", "specs": {"pattern": "Floral", "length": "Midi"}},
        "stock": 70,
        "category": {"main": "Clothing", "sub": "Dresses"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Leather Slim Wallet",
        "sku": "CLO-ACC-1027",
        "price": Decimal128("39.99"),
        "details": {"description": "Genuine leather minimalist wallet.", "specs": {"material": "Leather", "color": "Brown"}},
        "stock": 140,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "SonicBlast Bluetooth Speaker",
        "sku": "ELE-AUD-1028",
        "price": Decimal128("75.00"),
        "details": {"description": "Portable speaker with 360 degree sound.", "specs": {"waterproof": "IPX7", "battery": "12h"}},
        "stock": 65,
        "category": {"main": "Electronics", "sub": "Audio"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(6, 14)
    },
    {
        "_id": ObjectId(),
        "name": "UltraDrive 1TB SSD",
        "sku": "ELE-STO-1029",
        "price": Decimal128("99.99"),
        "details": {"description": "Fast external SSD for data backup.", "specs": {"capacity": "1TB", "interface": "USB 3.2"}},
        "stock": 180,
        "category": {"main": "Electronics", "sub": "Storage"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Morning Brew Coffee Maker",
        "sku": "HOM-APP-1030",
        "price": Decimal128("49.99"),
        "details": {"description": "Programmable drip coffee maker.", "specs": {"capacity": "12 cups", "filter": "Reusable"}},
        "stock": 85,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Non-Slip Bath Mat",
        "sku": "HOM-BAT-1031",
        "price": Decimal128("18.00"),
        "details": {"description": "Absorbent microfiber bath mat.", "specs": {"color": "Grey", "size": "50x80cm"}},
        "stock": 120,
        "category": {"main": "Home & Kitchen", "sub": "Bath"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "CourtMaster Tennis Racket",
        "sku": "SPO-TEN-1032",
        "price": Decimal128("135.00"),
        "details": {"description": "Graphite composite racket for control.", "specs": {"weight": "290g", "head_size": "100sq in"}},
        "stock": 40,
        "category": {"main": "Sports", "sub": "Tennis"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "GoalKeeper Pro Gloves",
        "sku": "SPO-SOC-1033",
        "price": Decimal128("45.00"),
        "details": {"description": "Professional soccer goalie gloves.", "specs": {"size": "10", "grip": "Latex"}},
        "stock": 55,
        "category": {"main": "Sports", "sub": "Soccer"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "History of the Renaissance",
        "sku": "BOO-HIS-1034",
        "price": Decimal128("32.00"),
        "details": {"description": "Detailed history of art and culture.", "specs": {"pages": "550", "cover": "Hardcover"}},
        "stock": 60,
        "category": {"main": "Books", "sub": "History"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "SlimFit Chino Pants",
        "sku": "CLO-PAN-1035",
        "price": Decimal128("55.00"),
        "details": {"description": "Stretch cotton chinos for office.", "specs": {"color": "Beige", "fit": "Slim"}},
        "stock": 95,
        "category": {"main": "Clothing", "sub": "Pants"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Retro Polarized Sunglasses",
        "sku": "CLO-ACC-1036",
        "price": Decimal128("89.99"),
        "details": {"description": "Classic wayfarer style sunglasses.", "specs": {"lens": "Polarized", "protection": "UV400"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "SmartHome Hub Mini",
        "sku": "ELE-SMA-1037",
        "price": Decimal128("39.99"),
        "details": {"description": "Control your home devices with voice.", "specs": {"wifi": "Yes", "voice_assistant": "Included"}},
        "stock": 160,
        "category": {"main": "Electronics", "sub": "Smart Home"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(6, 15)
    },
    {
        "_id": ObjectId(),
        "name": "ErgoLift Laptop Stand",
        "sku": "ELE-ACC-1038",
        "price": Decimal128("42.00"),
        "details": {"description": "Aluminum adjustable laptop stand.", "specs": {"material": "Aluminum", "adjustable": "Yes"}},
        "stock": 75,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "TurboBlend 500 Mixer",
        "sku": "HOM-APP-1039",
        "price": Decimal128("65.00"),
        "details": {"description": "High speed hand mixer for baking.", "specs": {"power": "500W", "speeds": "5"}},
        "stock": 50,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Luxury Cotton Towel Set",
        "sku": "HOM-BAT-1040",
        "price": Decimal128("45.99"),
        "details": {"description": "Set of 4 egyptian cotton towels.", "specs": {"color": "White", "gsm": "600"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Bath"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "IronCore Kettlebell 16kg",
        "sku": "SPO-GYM-1041",
        "price": Decimal128("55.00"),
        "details": {"description": "Cast iron kettlebell for strength training.", "specs": {"weight": "16kg", "finish": "Powder Coat"}},
        "stock": 40,
        "category": {"main": "Sports", "sub": "Weights"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "SpeedRope Pro",
        "sku": "SPO-FIT-1042",
        "price": Decimal128("19.99"),
        "details": {"description": "Adjustable speed jump rope for cardio.", "specs": {"cable": "Steel", "bearing": "Ball"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "The Art of War",
        "sku": "BOO-PHI-1043",
        "price": Decimal128("12.99"),
        "details": {"description": "Classic treatise on military strategy.", "specs": {"author": "Sun Tzu", "pages": "100"}},
        "stock": 300,
        "category": {"main": "Books", "sub": "Philosophy"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Winter Wool Scarf",
        "sku": "CLO-ACC-1044",
        "price": Decimal128("35.00"),
        "details": {"description": "Thick wool scarf for cold weather.", "specs": {"material": "Wool", "pattern": "Plaid"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Canvas Messenger Bag",
        "sku": "CLO-BAG-1045",
        "price": Decimal128("65.00"),
        "details": {"description": "Durable canvas bag for laptops.", "specs": {"size": "15 inch", "color": "Khaki"}},
        "stock": 60,
        "category": {"main": "Clothing", "sub": "Bags"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "ActionCam Mount Kit",
        "sku": "ELE-ACC-1046",
        "price": Decimal128("29.99"),
        "details": {"description": "Universal mounting kit for action cameras.", "specs": {"pieces": "20", "compatible": "GoPro"}},
        "stock": 150,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Digital Photo Frame 10",
        "sku": "ELE-HOM-1047",
        "price": Decimal128("99.00"),
        "details": {"description": "WiFi enabled digital photo frame.", "specs": {"screen": "10 inch", "resolution": "HD"}},
        "stock": 55,
        "category": {"main": "Electronics", "sub": "Decor"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Cast Iron Skillet 10",
        "sku": "HOM-CKW-1048",
        "price": Decimal128("29.99"),
        "details": {"description": "Pre-seasoned cast iron skillet.", "specs": {"diameter": "10 inch", "weight": "2kg"}},
        "stock": 130,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Glass Food Containers",
        "sku": "HOM-KIT-1049",
        "price": Decimal128("39.99"),
        "details": {"description": "Set of 5 glass meal prep containers.", "specs": {"lids": "BPA Free", "oven_safe": "Yes"}},
        "stock": 85,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Camping Tent 4-Person",
        "sku": "SPO-OUT-1050",
        "price": Decimal128("129.99"),
        "details": {"description": "Spacious family camping tent.", "specs": {"capacity": "4 Person", "waterproof": "Yes"}},
        "stock": 30,
        "category": {"main": "Sports", "sub": "Outdoor"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Thermal Sleeping Bag",
        "sku": "SPO-OUT-1051",
        "price": Decimal128("59.99"),
        "details": {"description": "3-season sleeping bag for camping.", "specs": {"temp_rating": "0C", "shape": "Mummy"}},
        "stock": 60,
        "category": {"main": "Sports", "sub": "Outdoor"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Modern Physics Guide",
        "sku": "BOO-SCI-1052",
        "price": Decimal128("45.00"),
        "details": {"description": "Introduction to quantum mechanics.", "specs": {"pages": "450", "level": "University"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Science"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Athletic Ankle Socks",
        "sku": "CLO-ACC-1053",
        "price": Decimal128("15.00"),
        "details": {"description": "Pack of 6 cotton running socks.", "specs": {"color": "White", "size": "One Size"}},
        "stock": 300,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(5, 20)
    },
    {
        "_id": ObjectId(),
        "name": "Formal Leather Belt",
        "sku": "CLO-ACC-1054",
        "price": Decimal128("29.99"),
        "details": {"description": "Classic black leather belt for suits.", "specs": {"material": "Leather", "buckle": "Silver"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "DroneX Pro 4K",
        "sku": "ELE-DRO-1055",
        "price": Decimal128("499.00"),
        "details": {"description": "Foldable camera drone with GPS.", "specs": {"range": "2km", "camera": "4K"}},
        "stock": 25,
        "category": {"main": "Electronics", "sub": "Drones"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Studio Microphone Kit",
        "sku": "ELE-AUD-1056",
        "price": Decimal128("89.99"),
        "details": {"description": "Condenser microphone with boom arm.", "specs": {"pattern": "Cardioid", "connection": "XLR"}},
        "stock": 50,
        "category": {"main": "Electronics", "sub": "Audio"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Electric Kettle 1.7L",
        "sku": "HOM-APP-1057",
        "price": Decimal128("34.99"),
        "details": {"description": "Stainless steel fast boil kettle.", "specs": {"capacity": "1.7L", "auto_off": "Yes"}},
        "stock": 90,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Wall Mirror Circle",
        "sku": "HOM-DEC-1058",
        "price": Decimal128("59.00"),
        "details": {"description": "Gold frame round wall mirror.", "specs": {"diameter": "60cm", "frame": "Metal"}},
        "stock": 45,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Table Tennis Set",
        "sku": "SPO-GAM-1059",
        "price": Decimal128("24.99"),
        "details": {"description": "2 paddles and 3 balls set.", "specs": {"rubber": "Pips-in", "balls": "3 Star"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Compression Leggings",
        "sku": "SPO-APP-1060",
        "price": Decimal128("39.99"),
        "details": {"description": "High performance compression pants.", "specs": {"material": "Spandex", "size": "M"}},
        "stock": 80,
        "category": {"main": "Sports", "sub": "Apparel"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Mastering French Cooking",
        "sku": "BOO-COO-1061",
        "price": Decimal128("49.99"),
        "details": {"description": "Classic cookbook for french cuisine.", "specs": {"recipes": "500+", "author": "J. Child"}},
        "stock": 60,
        "category": {"main": "Books", "sub": "Cooking"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Graphic Tee Vintage",
        "sku": "CLO-TOP-1062",
        "price": Decimal128("24.99"),
        "details": {"description": "Retro rock band t-shirt.", "specs": {"material": "Cotton", "print": "Screen"}},
        "stock": 120,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Running Armband",
        "sku": "ELE-ACC-1063",
        "price": Decimal128("12.99"),
        "details": {"description": "Phone holder for running.", "specs": {"size": "Universal", "sweatproof": "Yes"}},
        "stock": 200,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Gaming Mouse Pad XL",
        "sku": "ELE-ACC-1064",
        "price": Decimal128("19.99"),
        "details": {"description": "Extended mouse pad for desk.", "specs": {"size": "90x40cm", "surface": "Speed"}},
        "stock": 150,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(4, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Silicone Spatula Set",
        "sku": "HOM-KIT-1065",
        "price": Decimal128("14.99"),
        "details": {"description": "Heat resistant baking spatulas.", "specs": {"pieces": "4", "color": "Red"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Espresso Cups Set",
        "sku": "HOM-KIT-1066",
        "price": Decimal128("24.00"),
        "details": {"description": "Set of 6 double wall glass cups.", "specs": {"capacity": "80ml", "material": "Glass"}},
        "stock": 75,
        "category": {"main": "Home & Kitchen", "sub": "Glassware"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Cycling Helmet",
        "sku": "SPO-CYC-1067",
        "price": Decimal128("45.00"),
        "details": {"description": "Lightweight road bike helmet.", "specs": {"size": "M/L", "vents": "18"}},
        "stock": 55,
        "category": {"main": "Sports", "sub": "Cycling"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Swimming Goggles",
        "sku": "SPO-SWI-1068",
        "price": Decimal128("19.99"),
        "details": {"description": "Anti-fog swimming goggles.", "specs": {"lens": "Mirrored", "strap": "Silicone"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Swimming"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Business Strategy 101",
        "sku": "BOO-BUS-1069",
        "price": Decimal128("25.00"),
        "details": {"description": "Fundamentals of corporate strategy.", "specs": {"pages": "300", "edition": "2nd"}},
        "stock": 85,
        "category": {"main": "Books", "sub": "Business"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Wool Fedora Hat",
        "sku": "CLO-ACC-1070",
        "price": Decimal128("45.00"),
        "details": {"description": "Classic wide brim fedora.", "specs": {"material": "Wool Felt", "color": "Black"}},
        "stock": 40,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "USB-C Hub 7-in-1",
        "sku": "ELE-ACC-1071",
        "price": Decimal128("59.99"),
        "details": {"description": "Multiport adapter for laptops.", "specs": {"ports": "HDMI, USB, SD", "pd": "100W"}},
        "stock": 140,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Smart LED Bulb Color",
        "sku": "ELE-SMA-1072",
        "price": Decimal128("15.99"),
        "details": {"description": "WiFi RGB smart light bulb.", "specs": {"socket": "E26", "colors": "16M"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Smart Home"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(3, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Luxury Scented Candle",
        "sku": "HOM-DEC-1073",
        "price": Decimal128("28.00"),
        "details": {"description": "Soy wax candle with lavender scent.", "specs": {"burn_time": "40h", "scent": "Lavender"}},
        "stock": 110,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(6, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Stainless Trash Can",
        "sku": "HOM-KIT-1074",
        "price": Decimal128("75.00"),
        "details": {"description": "Step trash can with soft close lid.", "specs": {"capacity": "50L", "material": "Steel"}},
        "stock": 35,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Basketball Indoor",
        "sku": "SPO-BAS-1075",
        "price": Decimal128("35.00"),
        "details": {"description": "Official size 7 composite leather ball.", "specs": {"size": "7", "use": "Indoor"}},
        "stock": 90,
        "category": {"main": "Sports", "sub": "Basketball"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Pilates Ring",
        "sku": "SPO-FIT-1076",
        "price": Decimal128("22.00"),
        "details": {"description": "Magic circle ring for toning.", "specs": {"diameter": "14 inch", "handles": "Foam"}},
        "stock": 80,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Sci-Fi Short Stories",
        "sku": "BOO-FIC-1077",
        "price": Decimal128("18.99"),
        "details": {"description": "Anthology of future worlds.", "specs": {"pages": "350", "format": "Paperback"}},
        "stock": 65,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Travel Backpack 40L",
        "sku": "CLO-BAG-1078",
        "price": Decimal128("89.99"),
        "details": {"description": "Carry-on travel backpack.", "specs": {"capacity": "40L", "laptop_sleeve": "Yes"}},
        "stock": 50,
        "category": {"main": "Clothing", "sub": "Bags"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Bluetooth Tracker",
        "sku": "ELE-ACC-1079",
        "price": Decimal128("24.99"),
        "details": {"description": "Key finder tag with app.", "specs": {"battery": "1 Year", "range": "200ft"}},
        "stock": 180,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(2, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Portable Projector",
        "sku": "ELE-HOM-1080",
        "price": Decimal128("150.00"),
        "details": {"description": "Mini LED projector for movies.", "specs": {"lumens": "2000", "resolution": "720p"}},
        "stock": 30,
        "category": {"main": "Electronics", "sub": "Video"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Toaster 2-Slice",
        "sku": "HOM-APP-1081",
        "price": Decimal128("29.99"),
        "details": {"description": "Wide slot toaster with bagel setting.", "specs": {"power": "800W", "color": "Silver"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Wine Decanter",
        "sku": "HOM-KIT-1082",
        "price": Decimal128("45.00"),
        "details": {"description": "Crystal glass wine aerator.", "specs": {"capacity": "1.5L", "material": "Lead-free Crystal"}},
        "stock": 55,
        "category": {"main": "Home & Kitchen", "sub": "Glassware"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Boxing Gloves 14oz",
        "sku": "SPO-BOX-1083",
        "price": Decimal128("59.99"),
        "details": {"description": "Training boxing gloves.", "specs": {"weight": "14oz", "material": "Synthetic Leather"}},
        "stock": 45,
        "category": {"main": "Sports", "sub": "Boxing"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Foam Roller",
        "sku": "SPO-FIT-1084",
        "price": Decimal128("19.99"),
        "details": {"description": "High density foam roller for massage.", "specs": {"length": "18 inch", "texture": "Smooth"}},
        "stock": 120,
        "category": {"main": "Sports", "sub": "Recovery"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Graphic Design Basics",
        "sku": "BOO-DES-1085",
        "price": Decimal128("39.99"),
        "details": {"description": "Guide to typography and layout.", "specs": {"pages": "250", "images": "Full Color"}},
        "stock": 70,
        "category": {"main": "Books", "sub": "Design"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Puffer Vest",
        "sku": "CLO-JAC-1086",
        "price": Decimal128("55.00"),
        "details": {"description": "Insulated winter vest.", "specs": {"insulation": "Synthetic", "color": "Navy"}},
        "stock": 85,
        "category": {"main": "Clothing", "sub": "Jackets"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Tablet Stand Adjustable",
        "sku": "ELE-ACC-1087",
        "price": Decimal128("25.00"),
        "details": {"description": "Desktop stand for tablets.", "specs": {"material": "Metal", "rotation": "360"}},
        "stock": 95,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "SoundBar with Subwoofer",
        "sku": "ELE-AUD-1088",
        "price": Decimal128("199.99"),
        "details": {"description": "2.1 Channel soundbar system.", "specs": {"power": "120W", "connectivity": "Bluetooth, Optical"}},
        "stock": 40,
        "category": {"main": "Electronics", "sub": "Audio"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Electric Blanket",
        "sku": "HOM-BED-1089",
        "price": Decimal128("65.00"),
        "details": {"description": "Heated throw blanket with timer.", "specs": {"size": "Twin", "settings": "3"}},
        "stock": 60,
        "category": {"main": "Home & Kitchen", "sub": "Bedding"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Spice Rack Organizer",
        "sku": "HOM-KIT-1090",
        "price": Decimal128("32.00"),
        "details": {"description": "Revolving countertop spice rack.", "specs": {"jars": "16", "material": "Stainless Steel"}},
        "stock": 110,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Golf Balls Pack",
        "sku": "SPO-GOL-1091",
        "price": Decimal128("29.99"),
        "details": {"description": "Dozen soft feel golf balls.", "specs": {"count": "12", "color": "White"}},
        "stock": 150,
        "category": {"main": "Sports", "sub": "Golf"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Ab Roller Wheel",
        "sku": "SPO-FIT-1092",
        "price": Decimal128("18.50"),
        "details": {"description": "Core workout abdominal wheel.", "specs": {"wheel": "Dual", "mat": "Included"}},
        "stock": 90,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Psychology of Success",
        "sku": "BOO-SEL-1093",
        "price": Decimal128("19.99"),
        "details": {"description": "Self-help guide to mindset.", "specs": {"pages": "280", "cover": "Softcover"}},
        "stock": 80,
        "category": {"main": "Books", "sub": "Self-Help"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Gym Duffel Bag",
        "sku": "CLO-BAG-1094",
        "price": Decimal128("45.00"),
        "details": {"description": "Sports bag with shoe compartment.", "specs": {"capacity": "30L", "color": "Black"}},
        "stock": 70,
        "category": {"main": "Clothing", "sub": "Bags"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Gaming Headset 7.1",
        "sku": "ELE-GAM-1095",
        "price": Decimal128("79.99"),
        "details": {"description": "Surround sound gaming headset.", "specs": {"connection": "USB", "mic": "Retractable"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Gaming"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "External Hard Drive 2TB",
        "sku": "ELE-STO-1096",
        "price": Decimal128("85.00"),
        "details": {"description": "Portable HDD for storage.", "specs": {"capacity": "2TB", "type": "HDD"}},
        "stock": 130,
        "category": {"main": "Electronics", "sub": "Storage"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Waffle Maker",
        "sku": "HOM-APP-1097",
        "price": Decimal128("35.00"),
        "details": {"description": "Belgian waffle maker non-stick.", "specs": {"shape": "Round", "indicator": "LED"}},
        "stock": 65,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Desk Organizer Set",
        "sku": "HOM-OFF-1098",
        "price": Decimal128("22.00"),
        "details": {"description": "Metal mesh desk organizer.", "specs": {"pieces": "5", "color": "Black"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Office"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Yoga Ball 65cm",
        "sku": "SPO-YOG-1099",
        "price": Decimal128("19.99"),
        "details": {"description": "Anti-burst exercise ball.", "specs": {"size": "65cm", "pump": "Included"}},
        "stock": 110,
        "category": {"main": "Sports", "sub": "Yoga"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(2, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Ski Goggles Pro",
        "sku": "SPO-WIN-1100",
        "price": Decimal128("75.00"),
        "details": {"description": "Frameless ski goggles UV protection.", "specs": {"lens": "Dual", "strap": "Adjustable"}},
        "stock": 50,
        "category": {"main": "Sports", "sub": "Winter"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Titan Gaming Chair",
        "sku": "HOM-FUR-2001",
        "price": Decimal128("249.99"),
        "details": {"description": "Ergonomic chair with lumbar support.", "specs": {"material": "PU Leather", "max_weight": "150kg"}},
        "stock": 35,
        "category": {"main": "Home & Kitchen", "sub": "Furniture"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Vortex Air Fryer 5L",
        "sku": "HOM-APP-2002",
        "price": Decimal128("89.50"),
        "details": {"description": "Oil-free digital air fryer.", "specs": {"capacity": "5L", "programs": "8"}},
        "stock": 110,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(6, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Echo Noise Cancel Headphones",
        "sku": "ELE-AUD-2003",
        "price": Decimal128("199.00"),
        "details": {"description": "Premium ANC over-ear headphones.", "specs": {"battery": "30h", "driver": "45mm"}},
        "stock": 70,
        "category": {"main": "Electronics", "sub": "Audio"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Carbon Fiber Trekking Poles",
        "sku": "SPO-OUT-2004",
        "price": Decimal128("55.00"),
        "details": {"description": "Ultra-light poles for hiking.", "specs": {"material": "Carbon", "adjustable": "Yes"}},
        "stock": 85,
        "category": {"main": "Sports", "sub": "Hiking"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Introduction to Algorithms",
        "sku": "BOO-TEC-2005",
        "price": Decimal128("65.00"),
        "details": {"description": "Standard textbook for CS students.", "specs": {"pages": "1000", "cover": "Hardcover"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Technical"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Slim Fit Blazer",
        "sku": "CLO-FOR-2006",
        "price": Decimal128("120.00"),
        "details": {"description": "Navy blue formal blazer.", "specs": {"material": "Wool Blend", "size": "42R"}},
        "stock": 50,
        "category": {"main": "Clothing", "sub": "Formal"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Smart Garden Indoor",
        "sku": "HOM-GAR-2007",
        "price": Decimal128("99.99"),
        "details": {"description": "Hydroponic herb garden kit.", "specs": {"pods": "3", "light": "LED"}},
        "stock": 65,
        "category": {"main": "Home & Kitchen", "sub": "Garden"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Wireless Charging Pad",
        "sku": "ELE-ACC-2008",
        "price": Decimal128("24.99"),
        "details": {"description": "Fast Qi wireless charger.", "specs": {"output": "15W", "connector": "USB-C"}},
        "stock": 200,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Marathon Hydration Vest",
        "sku": "SPO-RUN-2009",
        "price": Decimal128("45.00"),
        "details": {"description": "Lightweight vest with water bladder.", "specs": {"capacity": "1.5L", "size": "M/L"}},
        "stock": 90,
        "category": {"main": "Sports", "sub": "Running"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Modern Art History",
        "sku": "BOO-ART-2010",
        "price": Decimal128("50.00"),
        "details": {"description": "Evolution of modern art movements.", "specs": {"pages": "400", "images": "Color"}},
        "stock": 30,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Thermal Winter Gloves",
        "sku": "CLO-ACC-2011",
        "price": Decimal128("19.99"),
        "details": {"description": "Touchscreen compatible warm gloves.", "specs": {"material": "Fleece", "color": "Black"}},
        "stock": 150,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 9)
    },
    {
        "_id": ObjectId(),
        "name": "VR Headset Quest",
        "sku": "ELE-GAM-2012",
        "price": Decimal128("349.00"),
        "details": {"description": "Standalone virtual reality system.", "specs": {"storage": "128GB", "controllers": "2"}},
        "stock": 45,
        "category": {"main": "Electronics", "sub": "Gaming"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Robot Vacuum Cleaner",
        "sku": "HOM-APP-2013",
        "price": Decimal128("299.99"),
        "details": {"description": "Smart robot vacuum with mapping.", "specs": {"runtime": "90min", "suction": "2000Pa"}},
        "stock": 60,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(4, 12)
    },
    {
        "_id": ObjectId(),
        "name": " Badminton Racket Set",
        "sku": "SPO-BAD-2014",
        "price": Decimal128("35.00"),
        "details": {"description": "2 rackets and shuttlecocks set.", "specs": {"material": "Alloy", "case": "Included"}},
        "stock": 120,
        "category": {"main": "Sports", "sub": "Badminton"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Leather Watch",
        "sku": "CLO-ACC-2015",
        "price": Decimal128("89.00"),
        "details": {"description": "Minimalist quartz watch.", "specs": {"strap": "Leather", "resistance": "30m"}},
        "stock": 80,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Portable SSD 500GB",
        "sku": "ELE-STO-2016",
        "price": Decimal128("65.00"),
        "details": {"description": "Rugged external solid state drive.", "specs": {"speed": "1050MB/s", "port": "USB-C"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Storage"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Cast Iron Dutch Oven",
        "sku": "HOM-CKW-2017",
        "price": Decimal128("59.99"),
        "details": {"description": "Enameled 6-quart dutch oven.", "specs": {"color": "Red", "oven_safe": "500F"}},
        "stock": 55,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(6, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Protein Shaker Bottle",
        "sku": "SPO-NUT-2018",
        "price": Decimal128("9.99"),
        "details": {"description": "Leak-proof shaker with mixing ball.", "specs": {"capacity": "700ml", "bpa_free": "Yes"}},
        "stock": 300,
        "category": {"main": "Sports", "sub": "Nutrition"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Biography of Einstein",
        "sku": "BOO-BIO-2019",
        "price": Decimal128("22.00"),
        "details": {"description": "Life and times of the genius.", "specs": {"pages": "600", "author": "W. Isaacson"}},
        "stock": 75,
        "category": {"main": "Books", "sub": "Biography"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Cargo Shorts",
        "sku": "CLO-BOT-2020",
        "price": Decimal128("35.00"),
        "details": {"description": "Durable cotton cargo shorts.", "specs": {"pockets": "6", "color": "Khaki"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Bottoms"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "WiFi Range Extender",
        "sku": "ELE-NET-2021",
        "price": Decimal128("29.99"),
        "details": {"description": "Boosts wireless signal coverage.", "specs": {"speed": "1200Mbps", "band": "Dual"}},
        "stock": 95,
        "category": {"main": "Electronics", "sub": "Networking"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(2, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Memory Foam Mattress Topper",
        "sku": "HOM-BED-2022",
        "price": Decimal128("120.00"),
        "details": {"description": "3-inch gel infused topper.", "specs": {"size": "Queen", "cooling": "Yes"}},
        "stock": 40,
        "category": {"main": "Home & Kitchen", "sub": "Bedding"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Inflatable Kayak",
        "sku": "SPO-WAT-2023",
        "price": Decimal128("180.00"),
        "details": {"description": "2-person durable inflatable kayak.", "specs": {"pump": "Included", "weight_cap": "180kg"}},
        "stock": 25,
        "category": {"main": "Sports", "sub": "Water Sports"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Vegetarian Cookbook",
        "sku": "BOO-COO-2024",
        "price": Decimal128("25.00"),
        "details": {"description": "Healthy plant-based recipes.", "specs": {"recipes": "100", "photos": "Full Color"}},
        "stock": 85,
        "category": {"main": "Books", "sub": "Cooking"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Running Cap",
        "sku": "CLO-ACC-2025",
        "price": Decimal128("18.00"),
        "details": {"description": "Breathable lightweight cap.", "specs": {"material": "Polyester", "size": "Adjustable"}},
        "stock": 130,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Action Camera 4K",
        "sku": "ELE-CAM-2026",
        "price": Decimal128("89.99"),
        "details": {"description": "Waterproof sports action cam.", "specs": {"fps": "60", "wifi": "Yes"}},
        "stock": 60,
        "category": {"main": "Electronics", "sub": "Cameras"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Bamboo Drawer Organizer",
        "sku": "HOM-STO-2027",
        "price": Decimal128("22.00"),
        "details": {"description": "Expandable cutlery tray.", "specs": {"material": "Bamboo", "compartments": "7"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Spin Bike Indoor",
        "sku": "SPO-CYC-2028",
        "price": Decimal128("299.00"),
        "details": {"description": "Stationary bike with flywheel.", "specs": {"monitor": "Digital", "resistance": "Friction"}},
        "stock": 20,
        "category": {"main": "Sports", "sub": "Cycling"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Thriller Novel",
        "sku": "BOO-FIC-2029",
        "price": Decimal128("14.99"),
        "details": {"description": "Page-turning psychological thriller.", "specs": {"author": "S. King", "format": "Paperback"}},
        "stock": 140,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Thermal Underwear Set",
        "sku": "CLO-UND-2030",
        "price": Decimal128("40.00"),
        "details": {"description": "Base layer top and bottom.", "specs": {"material": "Merino Wool", "warmth": "High"}},
        "stock": 75,
        "category": {"main": "Clothing", "sub": "Underwear"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "USB Microphone",
        "sku": "ELE-AUD-2031",
        "price": Decimal128("55.00"),
        "details": {"description": "Plug and play podcast mic.", "specs": {"stand": "Tripod", "pattern": "Cardioid"}},
        "stock": 80,
        "category": {"main": "Electronics", "sub": "Audio"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Shower Curtain Geometric",
        "sku": "HOM-BAT-2032",
        "price": Decimal128("18.00"),
        "details": {"description": "Waterproof fabric curtain.", "specs": {"hooks": "12", "design": "Modern"}},
        "stock": 110,
        "category": {"main": "Home & Kitchen", "sub": "Bath"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Boxing Hand Wraps",
        "sku": "SPO-BOX-2033",
        "price": Decimal128("9.50"),
        "details": {"description": "Elastic cotton hand wraps.", "specs": {"length": "180 inch", "color": "Red"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Boxing"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Financial Freedom Guide",
        "sku": "BOO-BUS-2034",
        "price": Decimal128("19.99"),
        "details": {"description": "Investing basics for beginners.", "specs": {"pages": "220", "topic": "Finance"}},
        "stock": 90,
        "category": {"main": "Books", "sub": "Business"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Leather Gloves",
        "sku": "CLO-ACC-2035",
        "price": Decimal128("49.99"),
        "details": {"description": "Lined genuine leather gloves.", "specs": {"lining": "Cashmere", "color": "Brown"}},
        "stock": 60,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Smart Doorbell",
        "sku": "ELE-SMA-2036",
        "price": Decimal128("110.00"),
        "details": {"description": "Video doorbell with app.", "specs": {"res": "1080p", "night_vision": "Yes"}},
        "stock": 45,
        "category": {"main": "Electronics", "sub": "Smart Home"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Ceramic Baking Dish",
        "sku": "HOM-CKW-2037",
        "price": Decimal128("28.00"),
        "details": {"description": "Rectangular lasagna pan.", "specs": {"size": "9x13", "color": "Blue"}},
        "stock": 85,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Soccer Ball Size 5",
        "sku": "SPO-SOC-2038",
        "price": Decimal128("25.00"),
        "details": {"description": "Training soccer ball.", "specs": {"material": "PU", "stitch": "Machine"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Soccer"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Astronomy for Kids",
        "sku": "BOO-KID-2039",
        "price": Decimal128("15.00"),
        "details": {"description": "Illustrated guide to the stars.", "specs": {"age": "8-12", "cover": "Hardcover"}},
        "stock": 120,
        "category": {"main": "Books", "sub": "Children"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Raincoat Transparent",
        "sku": "CLO-JAC-2040",
        "price": Decimal128("35.00"),
        "details": {"description": "Waterproof hooded raincoat.", "specs": {"material": "EVA", "style": "Poncho"}},
        "stock": 200,
        "category": {"main": "Clothing", "sub": "Jackets"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Bluetooth Car Adapter",
        "sku": "ELE-CAR-2041",
        "price": Decimal128("18.00"),
        "details": {"description": "FM transmitter for car audio.", "specs": {"ports": "2 USB", "display": "LED"}},
        "stock": 150,
        "category": {"main": "Electronics", "sub": "Car Electronics"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Fleece Throw Blanket",
        "sku": "HOM-DEC-2042",
        "price": Decimal128("12.99"),
        "details": {"description": "Soft microplush blanket.", "specs": {"size": "50x60", "color": "Grey"}},
        "stock": 300,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Volleyball Soft Touch",
        "sku": "SPO-VOL-2043",
        "price": Decimal128("22.00"),
        "details": {"description": "Indoor/Outdoor volleyball.", "specs": {"touch": "Soft", "size": "Official"}},
        "stock": 70,
        "category": {"main": "Sports", "sub": "Volleyball"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Learn Spanish Book",
        "sku": "BOO-EDU-2044",
        "price": Decimal128("28.00"),
        "details": {"description": "Language learning course.", "specs": {"level": "Beginner", "audio": "Online"}},
        "stock": 65,
        "category": {"main": "Books", "sub": "Education"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Silk Tie Red",
        "sku": "CLO-FOR-2045",
        "price": Decimal128("25.00"),
        "details": {"description": "Formal silk necktie.", "specs": {"width": "3 inch", "pattern": "Solid"}},
        "stock": 100,
        "category": {"main": "Clothing", "sub": "Formal"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Game Capture Card",
        "sku": "ELE-GAM-2046",
        "price": Decimal128("99.00"),
        "details": {"description": "1080p 60fps streaming card.", "specs": {"interface": "USB 3.0", "passthrough": "4K"}},
        "stock": 35,
        "category": {"main": "Electronics", "sub": "Gaming"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Juicer Machine",
        "sku": "HOM-APP-2047",
        "price": Decimal128("65.00"),
        "details": {"description": "Centrifugal fruit juicer.", "specs": {"power": "600W", "speed": "2"}},
        "stock": 50,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Dart Board Set",
        "sku": "SPO-GAM-2048",
        "price": Decimal128("35.00"),
        "details": {"description": "Bristle dartboard with darts.", "specs": {"size": "18 inch", "darts": "6"}},
        "stock": 80,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Graphic Novel Fantasy",
        "sku": "BOO-COM-2049",
        "price": Decimal128("19.99"),
        "details": {"description": "Epic fantasy comic compilation.", "specs": {"pages": "180", "art": "Color"}},
        "stock": 90,
        "category": {"main": "Books", "sub": "Comics"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Wool Socks Pack",
        "sku": "CLO-ACC-2050",
        "price": Decimal128("22.00"),
        "details": {"description": "Warm merino wool hiking socks.", "specs": {"pairs": "3", "thickness": "Heavy"}},
        "stock": 140,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "4K Projector Screen",
        "sku": "ELE-HOM-2051",
        "price": Decimal128("85.00"),
        "details": {"description": "100-inch pull down screen.", "specs": {"ratio": "16:9", "mount": "Wall"}},
        "stock": 40,
        "category": {"main": "Electronics", "sub": "Video"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Espresso Tamper",
        "sku": "HOM-COF-2052",
        "price": Decimal128("18.00"),
        "details": {"description": "Stainless steel coffee tamper.", "specs": {"size": "58mm", "weight": "Heavy"}},
        "stock": 95,
        "category": {"main": "Home & Kitchen", "sub": "Coffee"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Ski Helmet",
        "sku": "SPO-WIN-2053",
        "price": Decimal128("65.00"),
        "details": {"description": "Safety certified snow helmet.", "specs": {"vents": "Adjustable", "liner": "Fleece"}},
        "stock": 35,
        "category": {"main": "Sports", "sub": "Winter"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Marketing 101",
        "sku": "BOO-BUS-2054",
        "price": Decimal128("32.00"),
        "details": {"description": "Digital marketing fundamentals.", "specs": {"pages": "300", "edition": "2024"}},
        "stock": 60,
        "category": {"main": "Books", "sub": "Business"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(1, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Yoga Leggings",
        "sku": "CLO-BOT-2055",
        "price": Decimal128("28.00"),
        "details": {"description": "High waisted stretch leggings.", "specs": {"material": "Nylon", "pocket": "Hidden"}},
        "stock": 180,
        "category": {"main": "Clothing", "sub": "Bottoms"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Sound Card External",
        "sku": "ELE-AUD-2056",
        "price": Decimal128("25.00"),
        "details": {"description": "USB audio adapter.", "specs": {"channels": "7.1", "input": "Mic/Headphone"}},
        "stock": 110,
        "category": {"main": "Electronics", "sub": "Audio"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Wall Clock Modern",
        "sku": "HOM-DEC-2057",
        "price": Decimal128("22.00"),
        "details": {"description": "Silent non-ticking clock.", "specs": {"size": "12 inch", "color": "Black"}},
        "stock": 130,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Jump Rope Weighted",
        "sku": "SPO-FIT-2058",
        "price": Decimal128("15.00"),
        "details": {"description": "Heavy rope for calorie burn.", "specs": {"weight": "1lb", "grip": "Foam"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Travel Guide Japan",
        "sku": "BOO-TRA-2059",
        "price": Decimal128("18.00"),
        "details": {"description": "Complete guide to Tokyo & Kyoto.", "specs": {"maps": "Included", "pages": "250"}},
        "stock": 80,
        "category": {"main": "Books", "sub": "Travel"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Polo Shirt Classic",
        "sku": "CLO-TOP-2060",
        "price": Decimal128("35.00"),
        "details": {"description": "Cotton pique polo shirt.", "specs": {"fit": "Regular", "color": "Navy"}},
        "stock": 100,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Smart Plug Mini",
        "sku": "ELE-SMA-2061",
        "price": Decimal128("12.99"),
        "details": {"description": "Voice control smart socket.", "specs": {"app": "Yes", "rating": "15A"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Smart Home"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(3, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Table Runner",
        "sku": "HOM-DEC-2062",
        "price": Decimal128("16.00"),
        "details": {"description": "Linen dining table runner.", "specs": {"size": "72 inch", "pattern": "Striped"}},
        "stock": 90,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Boxing Headgear",
        "sku": "SPO-BOX-2063",
        "price": Decimal128("45.00"),
        "details": {"description": "Protective sparring headguard.", "specs": {"padding": "Thick", "size": "L"}},
        "stock": 30,
        "category": {"main": "Sports", "sub": "Boxing"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Mystery Novel",
        "sku": "BOO-FIC-2064",
        "price": Decimal128("12.00"),
        "details": {"description": "Sherlock Holmes collection.", "specs": {"author": "AC Doyle", "cover": "Hardcover"}},
        "stock": 110,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Denim Skirt",
        "sku": "CLO-BOT-2065",
        "price": Decimal128("30.00"),
        "details": {"description": "A-line denim mini skirt.", "specs": {"wash": "Light", "buttons": "Front"}},
        "stock": 75,
        "category": {"main": "Clothing", "sub": "Bottoms"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Webcam Cover Slide",
        "sku": "ELE-ACC-2066",
        "price": Decimal128("5.99"),
        "details": {"description": "Privacy cover for laptop cams.", "specs": {"pack": "3", "material": "Plastic"}},
        "stock": 500,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Hand Blender Stick",
        "sku": "HOM-APP-2067",
        "price": Decimal128("35.00"),
        "details": {"description": "Immersion blender for soups.", "specs": {"power": "300W", "blade": "Steel"}},
        "stock": 65,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Swimming Cap",
        "sku": "SPO-SWI-2068",
        "price": Decimal128("8.00"),
        "details": {"description": "Silicone waterproof swim cap.", "specs": {"size": "One size", "color": "Blue"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Swimming"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Poetry Collection",
        "sku": "BOO-POE-2069",
        "price": Decimal128("16.00"),
        "details": {"description": "Modern poetry anthology.", "specs": {"pages": "120", "author": "Various"}},
        "stock": 55,
        "category": {"main": "Books", "sub": "Poetry"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Crossbody Bag",
        "sku": "CLO-BAG-2070",
        "price": Decimal128("40.00"),
        "details": {"description": "Small leather crossbody purse.", "specs": {"strap": "Chain", "color": "Black"}},
        "stock": 85,
        "category": {"main": "Clothing", "sub": "Bags"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Stylus Pen Tablet",
        "sku": "ELE-ACC-2071",
        "price": Decimal128("29.99"),
        "details": {"description": "Active stylus for touchscreens.", "specs": {"battery": "10h", "tip": "Fine"}},
        "stock": 95,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Wine Glasses Set",
        "sku": "HOM-KIT-2072",
        "price": Decimal128("35.00"),
        "details": {"description": "Set of 4 red wine glasses.", "specs": {"capacity": "500ml", "material": "Crystal"}},
        "stock": 70,
        "category": {"main": "Home & Kitchen", "sub": "Glassware"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Agility Ladder",
        "sku": "SPO-TRA-2073",
        "price": Decimal128("20.00"),
        "details": {"description": "Speed training ladder equipment.", "specs": {"length": "6m", "rungs": "12"}},
        "stock": 50,
        "category": {"main": "Sports", "sub": "Training"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Philosophy 101",
        "sku": "BOO-PHI-2074",
        "price": Decimal128("24.00"),
        "details": {"description": "Introduction to western philosophy.", "specs": {"pages": "350", "cover": "Paperback"}},
        "stock": 65,
        "category": {"main": "Books", "sub": "Philosophy"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Beanie Hat",
        "sku": "CLO-ACC-2075",
        "price": Decimal128("15.00"),
        "details": {"description": "Knit beanie for winter.", "specs": {"material": "Acrylic", "color": "Grey"}},
        "stock": 160,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(3, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Ring Light 10 inch",
        "sku": "ELE-CAM-2076",
        "price": Decimal128("35.00"),
        "details": {"description": "LED ring light with tripod.", "specs": {"modes": "3", "power": "USB"}},
        "stock": 80,
        "category": {"main": "Electronics", "sub": "Cameras"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Mop and Bucket Set",
        "sku": "HOM-CLE-2077",
        "price": Decimal128("45.00"),
        "details": {"description": "Spin mop with wringer bucket.", "specs": {"heads": "2 Microfiber", "handle": "Telescopic"}},
        "stock": 90,
        "category": {"main": "Home & Kitchen", "sub": "Cleaning"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Shin Guards Soccer",
        "sku": "SPO-SOC-2078",
        "price": Decimal128("12.00"),
        "details": {"description": "Hard shell protective guards.", "specs": {"size": "M", "strap": "Velcro"}},
        "stock": 110,
        "category": {"main": "Sports", "sub": "Soccer"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Self-Help Journal",
        "sku": "BOO-SEL-2079",
        "price": Decimal128("18.00"),
        "details": {"description": "Daily gratitude and goal journal.", "specs": {"pages": "180", "cover": "Leather"}},
        "stock": 130,
        "category": {"main": "Books", "sub": "Self-Help"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Tote Bag Canvas",
        "sku": "CLO-BAG-2080",
        "price": Decimal128("15.00"),
        "details": {"description": "Eco-friendly shopping tote.", "specs": {"print": "Graphic", "material": "Cotton"}},
        "stock": 250,
        "category": {"main": "Clothing", "sub": "Bags"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "HDMI Cable 4K",
        "sku": "ELE-ACC-2081",
        "price": Decimal128("12.00"),
        "details": {"description": "High speed HDMI 2.0 cable.", "specs": {"length": "2m", "braided": "Yes"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(5, 20)
    },
    {
        "_id": ObjectId(),
        "name": "Oven Mitts Pair",
        "sku": "HOM-KIT-2082",
        "price": Decimal128("14.00"),
        "details": {"description": "Heat resistant silicone mitts.", "specs": {"temp": "500F", "color": "Red"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Kitchenware"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Basebal Bat Aluminum",
        "sku": "SPO-BAS-2083",
        "price": Decimal128("45.00"),
        "details": {"description": "Lightweight alloy baseball bat.", "specs": {"length": "30 inch", "weight": "20oz"}},
        "stock": 40,
        "category": {"main": "Sports", "sub": "Baseball"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Thriller Paperback",
        "sku": "BOO-FIC-2084",
        "price": Decimal128("10.00"),
        "details": {"description": "Best-selling crime thriller.", "specs": {"pages": "400", "author": "J. Grisham"}},
        "stock": 120,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Track Jacket",
        "sku": "CLO-JAC-2085",
        "price": Decimal128("50.00"),
        "details": {"description": "Retro style athletic jacket.", "specs": {"material": "Polyester", "zip": "Full"}},
        "stock": 65,
        "category": {"main": "Clothing", "sub": "Jackets"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Laptop Cooling Pad",
        "sku": "ELE-ACC-2086",
        "price": Decimal128("25.00"),
        "details": {"description": "Cooler with 4 quiet fans.", "specs": {"size": "17 inch", "usb": "Powered"}},
        "stock": 75,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Food Storage Bags",
        "sku": "HOM-STO-2087",
        "price": Decimal128("15.00"),
        "details": {"description": "Reusable silicone zip bags.", "specs": {"pack": "6", "freezer_safe": "Yes"}},
        "stock": 150,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Knee Support Brace",
        "sku": "SPO-HEA-2088",
        "price": Decimal128("18.00"),
        "details": {"description": "Compression sleeve for running.", "specs": {"size": "L", "material": "Neoprene"}},
        "stock": 90,
        "category": {"main": "Sports", "sub": "Health"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Economics Textbook",
        "sku": "BOO-EDU-2089",
        "price": Decimal128("85.00"),
        "details": {"description": "Principles of microeconomics.", "specs": {"edition": "5th", "pages": "600"}},
        "stock": 30,
        "category": {"main": "Books", "sub": "Education"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Slippers Memory Foam",
        "sku": "CLO-SHO-2090",
        "price": Decimal128("20.00"),
        "details": {"description": "Indoor warm house slippers.", "specs": {"sole": "Rubber", "color": "Grey"}},
        "stock": 100,
        "category": {"main": "Clothing", "sub": "Shoes"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Screen Cleaning Kit",
        "sku": "ELE-ACC-2091",
        "price": Decimal128("10.00"),
        "details": {"description": "Spray and cloth for screens.", "specs": {"volume": "100ml", "cloth": "Microfiber"}},
        "stock": 220,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Pizza Cutter Wheel",
        "sku": "HOM-KIT-2092",
        "price": Decimal128("9.99"),
        "details": {"description": "Stainless steel sharp slicer.", "specs": {"blade": "3 inch", "handle": "Grip"}},
        "stock": 130,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Wrist Wraps Lifting",
        "sku": "SPO-GYM-2093",
        "price": Decimal128("12.00"),
        "details": {"description": "Support wraps for weightlifting.", "specs": {"length": "18 inch", "closure": "Velcro"}},
        "stock": 85,
        "category": {"main": "Sports", "sub": "Weights"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Architecture Book",
        "sku": "BOO-ART-2094",
        "price": Decimal128("45.00"),
        "details": {"description": "World's greatest buildings.", "specs": {"format": "Hardcover", "photos": "Color"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Belt Leather Brown",
        "sku": "CLO-ACC-2095",
        "price": Decimal128("30.00"),
        "details": {"description": "Casual brown leather belt.", "specs": {"width": "1.5 inch", "buckle": "Brass"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Micro SD Card 128GB",
        "sku": "ELE-STO-2096",
        "price": Decimal128("20.00"),
        "details": {"description": "Class 10 memory card.", "specs": {"speed": "100MB/s", "adapter": "Included"}},
        "stock": 180,
        "category": {"main": "Electronics", "sub": "Storage"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Laundry Hamper",
        "sku": "HOM-STO-2097",
        "price": Decimal128("18.00"),
        "details": {"description": "Foldable canvas laundry basket.", "specs": {"capacity": "60L", "handles": "Rope"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Stopwatch Digital",
        "sku": "SPO-ACC-2098",
        "price": Decimal128("10.00"),
        "details": {"description": "Sports timer with lanyard.", "specs": {"features": "Lap, Alarm", "water_resist": "Yes"}},
        "stock": 70,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Novels Set",
        "sku": "BOO-FIC-2099",
        "price": Decimal128("35.00"),
        "details": {"description": "Box set of 3 classic novels.", "specs": {"titles": "Austen, Bronte", "cover": "Paperback"}},
        "stock": 50,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Ankle Boots",
        "sku": "CLO-SHO-2100",
        "price": Decimal128("65.00"),
        "details": {"description": "Faux leather heeled boots.", "specs": {"heel": "2 inch", "color": "Black"}},
        "stock": 60,
        "category": {"main": "Clothing", "sub": "Shoes"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Smart Thermostat",
        "sku": "ELE-SMA-3001",
        "price": Decimal128("129.99"),
        "details": {"description": "WiFi programmable thermostat.", "specs": {"compatibility": "Alexa/Google", "color": "White"}},
        "stock": 45,
        "category": {"main": "Electronics", "sub": "Smart Home"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(4, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Duvet Cover Queen",
        "sku": "HOM-BED-3002",
        "price": Decimal128("45.00"),
        "details": {"description": "Soft cotton duvet cover set.", "specs": {"size": "Queen", "thread_count": "400"}},
        "stock": 80,
        "category": {"main": "Home & Kitchen", "sub": "Bedding"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Trekking Poles Pair",
        "sku": "SPO-HIK-3003",
        "price": Decimal128("35.00"),
        "details": {"description": "Adjustable aluminum hiking poles.", "specs": {"grip": "Cork", "tip": "Carbide"}},
        "stock": 60,
        "category": {"main": "Sports", "sub": "Hiking"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Java Programming Guide",
        "sku": "BOO-TEC-3004",
        "price": Decimal128("55.00"),
        "details": {"description": "Comprehensive Java reference.", "specs": {"pages": "800", "edition": "11th"}},
        "stock": 30,
        "category": {"main": "Books", "sub": "Technical"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Linen Shirt",
        "sku": "CLO-TOP-3005",
        "price": Decimal128("40.00"),
        "details": {"description": "Breathable summer linen shirt.", "specs": {"fit": "Relaxed", "color": "Beige"}},
        "stock": 100,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Dash Cam 1080p",
        "sku": "ELE-CAR-3006",
        "price": Decimal128("65.00"),
        "details": {"description": "Car camera with night vision.", "specs": {"view": "170 degree", "storage": "SD Card"}},
        "stock": 50,
        "category": {"main": "Electronics", "sub": "Car Electronics"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Milk Frother Handheld",
        "sku": "HOM-KIT-3007",
        "price": Decimal128("15.99"),
        "details": {"description": "Battery operated foam maker.", "specs": {"rpm": "19000", "material": "Steel"}},
        "stock": 150,
        "category": {"main": "Home & Kitchen", "sub": "Coffee"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 20)
    },
    {
        "_id": ObjectId(),
        "name": "Camping Stove",
        "sku": "SPO-OUT-3008",
        "price": Decimal128("25.00"),
        "details": {"description": "Portable gas camping burner.", "specs": {"ignition": "Piezo", "case": "Included"}},
        "stock": 75,
        "category": {"main": "Sports", "sub": "Camping"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Graphic Novel Horror",
        "sku": "BOO-COM-3009",
        "price": Decimal128("22.00"),
        "details": {"description": "Scary comic book collection.", "specs": {"pages": "200", "artist": "Various"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Comics"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Leather Wallet Bifold",
        "sku": "CLO-ACC-3010",
        "price": Decimal128("35.00"),
        "details": {"description": "Classic leather wallet.", "specs": {"slots": "8", "rfid": "Blocking"}},
        "stock": 120,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Vertical Ergonomic Mouse",
        "sku": "ELE-MOU-3011",
        "price": Decimal128("29.99"),
        "details": {"description": "Reduces wrist strain.", "specs": {"connection": "Wireless", "dpi": "Adjustable"}},
        "stock": 90,
        "category": {"main": "Electronics", "sub": "Peripherals"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Teapot Ceramic",
        "sku": "HOM-KIT-3012",
        "price": Decimal128("24.00"),
        "details": {"description": "Classic white ceramic teapot.", "specs": {"capacity": "1L", "filter": "Stainless"}},
        "stock": 65,
        "category": {"main": "Home & Kitchen", "sub": "Tea"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Golf Glove",
        "sku": "SPO-GOL-3013",
        "price": Decimal128("12.00"),
        "details": {"description": "Leather grip golf glove.", "specs": {"hand": "Left", "size": "M"}},
        "stock": 110,
        "category": {"main": "Sports", "sub": "Golf"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "History of Rome",
        "sku": "BOO-HIS-3014",
        "price": Decimal128("30.00"),
        "details": {"description": "Rise and fall of the empire.", "specs": {"pages": "500", "author": "M. Beard"}},
        "stock": 55,
        "category": {"main": "Books", "sub": "History"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Swimming Trunks",
        "sku": "CLO-SWI-3015",
        "price": Decimal128("25.00"),
        "details": {"description": "Quick dry swim shorts.", "specs": {"pattern": "Striped", "lining": "Mesh"}},
        "stock": 85,
        "category": {"main": "Clothing", "sub": "Swimwear"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Power Strip Surge",
        "sku": "ELE-ACC-3016",
        "price": Decimal128("18.00"),
        "details": {"description": "6-outlet power strip.", "specs": {"cord": "6ft", "protection": "Yes"}},
        "stock": 200,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Shoe Rack 3-Tier",
        "sku": "HOM-STO-3017",
        "price": Decimal128("29.99"),
        "details": {"description": "Metal shoe organizer.", "specs": {"capacity": "12 pairs", "color": "Black"}},
        "stock": 70,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Fishing Rod",
        "sku": "SPO-FIS-3018",
        "price": Decimal128("50.00"),
        "details": {"description": "Spinning fishing rod.", "specs": {"length": "7ft", "action": "Medium"}},
        "stock": 40,
        "category": {"main": "Sports", "sub": "Fishing"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Dictionary English",
        "sku": "BOO-EDU-3019",
        "price": Decimal128("20.00"),
        "details": {"description": "Oxford English dictionary.", "specs": {"format": "Hardcover", "pages": "1000"}},
        "stock": 95,
        "category": {"main": "Books", "sub": "Reference"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Bucket Hat",
        "sku": "CLO-HAT-3020",
        "price": Decimal128("15.00"),
        "details": {"description": "Cotton reversible bucket hat.", "specs": {"color": "White/Black", "size": "One Size"}},
        "stock": 130,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(2, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Ethernet Cable 10m",
        "sku": "ELE-NET-3021",
        "price": Decimal128("12.00"),
        "details": {"description": "Cat6 high speed internet cable.", "specs": {"length": "10m", "shielding": "UTP"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Networking"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(4, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Kitchen Apron",
        "sku": "HOM-KIT-3022",
        "price": Decimal128("14.00"),
        "details": {"description": "Cotton chef apron with pockets.", "specs": {"color": "Grey", "adjustable": "Yes"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Linens"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Yoga Towel Non-Slip",
        "sku": "SPO-YOG-3023",
        "price": Decimal128("18.00"),
        "details": {"description": "Microfiber towel for hot yoga.", "specs": {"size": "Mat size", "dots": "Silicone"}},
        "stock": 80,
        "category": {"main": "Sports", "sub": "Yoga"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Kids Fairytales",
        "sku": "BOO-KID-3024",
        "price": Decimal128("12.99"),
        "details": {"description": "Classic bedtime stories.", "specs": {"age": "3-6", "illustrations": "Color"}},
        "stock": 60,
        "category": {"main": "Books", "sub": "Children"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Running Socks Pack",
        "sku": "CLO-ACC-3025",
        "price": Decimal128("14.00"),
        "details": {"description": "3-pack anti-blister socks.", "specs": {"material": "Synthetic", "cut": "Low"}},
        "stock": 250,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Memory Card Reader",
        "sku": "ELE-ACC-3026",
        "price": Decimal128("10.00"),
        "details": {"description": "USB 3.0 multi-card reader.", "specs": {"slots": "SD/MicroSD", "speed": "Fast"}},
        "stock": 140,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Mixing Bowls Set",
        "sku": "HOM-KIT-3027",
        "price": Decimal128("28.00"),
        "details": {"description": "Set of 3 stainless steel bowls.", "specs": {"sizes": "S/M/L", "base": "Non-slip"}},
        "stock": 90,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Tennis Balls Can",
        "sku": "SPO-TEN-3028",
        "price": Decimal128("8.00"),
        "details": {"description": "Pressureless tennis balls.", "specs": {"count": "3", "type": "All Court"}},
        "stock": 300,
        "category": {"main": "Sports", "sub": "Tennis"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Science Fiction Anthology",
        "sku": "BOO-FIC-3029",
        "price": Decimal128("18.00"),
        "details": {"description": "Best stories of the decade.", "specs": {"pages": "400", "editor": "Various"}},
        "stock": 70,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Silk Pajamas",
        "sku": "CLO-SLP-3030",
        "price": Decimal128("85.00"),
        "details": {"description": "Luxury silk sleepwear set.", "specs": {"color": "Pink", "size": "S"}},
        "stock": 40,
        "category": {"main": "Clothing", "sub": "Sleepwear"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(5, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Phone Stand Desk",
        "sku": "ELE-ACC-3031",
        "price": Decimal128("12.00"),
        "details": {"description": "Aluminum adjustable holder.", "specs": {"compatible": "Universal", "color": "Silver"}},
        "stock": 180,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Measuring Cups",
        "sku": "HOM-KIT-3032",
        "price": Decimal128("9.00"),
        "details": {"description": "Plastic measuring cups set.", "specs": {"pieces": "4", "color": "Colorful"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Cycling Gloves",
        "sku": "SPO-CYC-3033",
        "price": Decimal128("15.00"),
        "details": {"description": "Padded fingerless gloves.", "specs": {"padding": "Gel", "size": "L"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Cycling"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Atlas of the World",
        "sku": "BOO-REF-3034",
        "price": Decimal128("40.00"),
        "details": {"description": "Detailed geographical atlas.", "specs": {"format": "Large", "maps": "Updated"}},
        "stock": 35,
        "category": {"main": "Books", "sub": "Reference"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Gym Tank Top",
        "sku": "CLO-TOP-3035",
        "price": Decimal128("18.00"),
        "details": {"description": "Muscle fit workout tank.", "specs": {"material": "Cotton", "color": "Black"}},
        "stock": 150,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Battery Charger AA",
        "sku": "ELE-ACC-3036",
        "price": Decimal128("20.00"),
        "details": {"description": "Rechargeable battery charger.", "specs": {"slots": "4", "compatibility": "AA/AAA"}},
        "stock": 90,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Pillow Cases Set",
        "sku": "HOM-BED-3037",
        "price": Decimal128("12.00"),
        "details": {"description": "Satin pillowcases pair.", "specs": {"size": "Standard", "color": "Ivory"}},
        "stock": 160,
        "category": {"main": "Home & Kitchen", "sub": "Bedding"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Snorkel Set",
        "sku": "SPO-WAT-3038",
        "price": Decimal128("35.00"),
        "details": {"description": "Mask and snorkel combo.", "specs": {"lens": "Tempered", "strap": "Silicone"}},
        "stock": 55,
        "category": {"main": "Sports", "sub": "Water Sports"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Business Biography",
        "sku": "BOO-BIO-3039",
        "price": Decimal128("22.00"),
        "details": {"description": "Shoe Dog by Phil Knight.", "specs": {"pages": "380", "cover": "Paperback"}},
        "stock": 80,
        "category": {"main": "Books", "sub": "Biography"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Oversized Hoodie",
        "sku": "CLO-TOP-3040",
        "price": Decimal128("45.00"),
        "details": {"description": "Comfy thick fleece hoodie.", "specs": {"fit": "Oversized", "color": "Grey"}},
        "stock": 100,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "HDMI Switch 3-Port",
        "sku": "ELE-ACC-3041",
        "price": Decimal128("15.00"),
        "details": {"description": "Connect 3 devices to 1 TV.", "specs": {"resolution": "4K", "remote": "Included"}},
        "stock": 130,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Dish Drying Rack",
        "sku": "HOM-KIT-3042",
        "price": Decimal128("30.00"),
        "details": {"description": "Stainless steel dish drainer.", "specs": {"tray": "Plastic", "tiers": "2"}},
        "stock": 75,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Wrist Sweatbands",
        "sku": "SPO-ACC-3043",
        "price": Decimal128("8.00"),
        "details": {"description": "Cotton terry cloth bands.", "specs": {"pair": "Yes", "color": "White"}},
        "stock": 220,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Vegan Diet Guide",
        "sku": "BOO-COO-3044",
        "price": Decimal128("18.00"),
        "details": {"description": "Plant based meal planning.", "specs": {"pages": "150", "author": "Dr. Greger"}},
        "stock": 65,
        "category": {"main": "Books", "sub": "Cooking"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Denim Shirt",
        "sku": "CLO-TOP-3045",
        "price": Decimal128("35.00"),
        "details": {"description": "Casual western denim shirt.", "specs": {"buttons": "Snap", "wash": "Dark"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "AUX Cable 3.5mm",
        "sku": "ELE-ACC-3046",
        "price": Decimal128("8.00"),
        "details": {"description": "Audio cable for car/headphones.", "specs": {"length": "1m", "jack": "Gold plated"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(4, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Coasters Set",
        "sku": "HOM-DEC-3047",
        "price": Decimal128("10.00"),
        "details": {"description": "Cork drink coasters.", "specs": {"count": "6", "shape": "Round"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Hiking Socks Wool",
        "sku": "CLO-ACC-3048",
        "price": Decimal128("16.00"),
        "details": {"description": "Merino wool trail socks.", "specs": {"cushion": "Medium", "size": "L"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(2, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Sketchbook Art",
        "sku": "BOO-ART-3049",
        "price": Decimal128("14.00"),
        "details": {"description": "Blank paper sketchbook.", "specs": {"paper": "100gsm", "binding": "Spiral"}},
        "stock": 140,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Jump Rope Speed",
        "sku": "SPO-FIT-3050",
        "price": Decimal128("12.00"),
        "details": {"description": "PVC cable speed rope.", "specs": {"handles": "Plastic", "color": "Black"}},
        "stock": 160,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Digital Alarm Clock",
        "sku": "ELE-HOM-3051",
        "price": Decimal128("18.00"),
        "details": {"description": "Large display LED clock.", "specs": {"power": "USB", "backup": "Battery"}},
        "stock": 120,
        "category": {"main": "Electronics", "sub": "Home"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Salad Spinner",
        "sku": "HOM-KIT-3052",
        "price": Decimal128("22.00"),
        "details": {"description": "Vegetable dryer and washer.", "specs": {"capacity": "4L", "mechanism": "Pump"}},
        "stock": 80,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Camping Lantern",
        "sku": "SPO-OUT-3053",
        "price": Decimal128("19.99"),
        "details": {"description": "LED rechargeable lantern.", "specs": {"lumens": "500", "mode": "SOS"}},
        "stock": 65,
        "category": {"main": "Sports", "sub": "Camping"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Horror Novel",
        "sku": "BOO-FIC-3054",
        "price": Decimal128("15.00"),
        "details": {"description": "Dracula by Bram Stoker.", "specs": {"cover": "Paperback", "pages": "350"}},
        "stock": 95,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Leather Belt Black",
        "sku": "CLO-ACC-3055",
        "price": Decimal128("25.00"),
        "details": {"description": "Formal black leather belt.", "specs": {"width": "1.2 inch", "buckle": "Silver"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Wireless Keypad",
        "sku": "ELE-KEY-3056",
        "price": Decimal128("20.00"),
        "details": {"description": "Numeric keypad for laptops.", "specs": {"keys": "22", "connection": "Bluetooth"}},
        "stock": 75,
        "category": {"main": "Electronics", "sub": "Peripherals"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Bath Towel Set",
        "sku": "HOM-BAT-3057",
        "price": Decimal128("35.00"),
        "details": {"description": "2 bath towels 2 hand towels.", "specs": {"color": "Blue", "material": "Cotton"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Bath"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Dumbbell 5kg",
        "sku": "SPO-GYM-3058",
        "price": Decimal128("15.00"),
        "details": {"description": "Hex rubber dumbbell single.", "specs": {"weight": "5kg", "handle": "Chrome"}},
        "stock": 140,
        "category": {"main": "Sports", "sub": "Weights"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "French Dictionary",
        "sku": "BOO-REF-3059",
        "price": Decimal128("12.00"),
        "details": {"description": "French-English pocket dict.", "specs": {"words": "40000", "size": "Small"}},
        "stock": 85,
        "category": {"main": "Books", "sub": "Reference"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Winter Scarf Knit",
        "sku": "CLO-ACC-3060",
        "price": Decimal128("18.00"),
        "details": {"description": "Chunky knit infinity scarf.", "specs": {"material": "Acrylic", "color": "Cream"}},
        "stock": 130,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Portable Fan",
        "sku": "ELE-ACC-3061",
        "price": Decimal128("12.99"),
        "details": {"description": "Rechargeable handheld fan.", "specs": {"speed": "3", "battery": "2000mAh"}},
        "stock": 200,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Muffin Pan",
        "sku": "HOM-CKW-3062",
        "price": Decimal128("14.00"),
        "details": {"description": "Non-stick 12 cup pan.", "specs": {"material": "Steel", "safe": "Dishwasher"}},
        "stock": 90,
        "category": {"main": "Home & Kitchen", "sub": "Bakeware"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Balance Board",
        "sku": "SPO-FIT-3063",
        "price": Decimal128("25.00"),
        "details": {"description": "Wobble board for stability.", "specs": {"diameter": "40cm", "surface": "Grip"}},
        "stock": 50,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Travel Journal",
        "sku": "BOO-TRA-3064",
        "price": Decimal128("16.00"),
        "details": {"description": "Notebook for trip memories.", "specs": {"pages": "120", "pocket": "Back"}},
        "stock": 110,
        "category": {"main": "Books", "sub": "Travel"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Sport Sunglasses",
        "sku": "CLO-ACC-3065",
        "price": Decimal128("22.00"),
        "details": {"description": "Polarized cycling glasses.", "specs": {"uv": "400", "frame": "Lightweight"}},
        "stock": 150,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Car Phone Mount",
        "sku": "ELE-CAR-3066",
        "price": Decimal128("14.00"),
        "details": {"description": "Dashboard magnetic holder.", "specs": {"rotation": "360", "magnet": "Strong"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Car Electronics"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Can Opener",
        "sku": "HOM-KIT-3067",
        "price": Decimal128("10.00"),
        "details": {"description": "Manual smooth edge opener.", "specs": {"handle": "Ergonomic", "material": "Steel"}},
        "stock": 120,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Badminton Shuttlecocks",
        "sku": "SPO-BAD-3068",
        "price": Decimal128("8.00"),
        "details": {"description": "Tube of 6 nylon birdies.", "specs": {"speed": "Medium", "color": "Yellow"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Badminton"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Gardening Guide",
        "sku": "BOO-HOB-3069",
        "price": Decimal128("20.00"),
        "details": {"description": "Grow your own vegetables.", "specs": {"season": "All", "cover": "Paperback"}},
        "stock": 60,
        "category": {"main": "Books", "sub": "Hobbies"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Ankle Socks Pack",
        "sku": "CLO-ACC-3070",
        "price": Decimal128("12.00"),
        "details": {"description": "6 pairs white cotton socks.", "specs": {"size": "One Size", "breathable": "Yes"}},
        "stock": 300,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Extension Cord 5m",
        "sku": "ELE-ACC-3071",
        "price": Decimal128("15.00"),
        "details": {"description": "Heavy duty power extension.", "specs": {"length": "5m", "color": "Orange"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Ice Cream Scoop",
        "sku": "HOM-KIT-3072",
        "price": Decimal128("8.00"),
        "details": {"description": "Stainless steel scooper.", "specs": {"trigger": "Lever", "handle": "Rubber"}},
        "stock": 130,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Resistance Loop Bands",
        "sku": "SPO-FIT-3073",
        "price": Decimal128("10.00"),
        "details": {"description": "Set of 4 mini bands.", "specs": {"material": "Latex", "levels": "Mixed"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "World History",
        "sku": "BOO-HIS-3074",
        "price": Decimal128("35.00"),
        "details": {"description": "A global perspective.", "specs": {"pages": "700", "author": "Ponting"}},
        "stock": 45,
        "category": {"main": "Books", "sub": "History"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Flip Flops",
        "sku": "CLO-SHO-3075",
        "price": Decimal128("15.00"),
        "details": {"description": "Rubber beach sandals.", "specs": {"color": "Blue", "size": "42"}},
        "stock": 180,
        "category": {"main": "Clothing", "sub": "Shoes"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "VGA Cable",
        "sku": "ELE-ACC-3076",
        "price": Decimal128("8.00"),
        "details": {"description": "Video cable for older monitors.", "specs": {"length": "1.5m", "pins": "15"}},
        "stock": 60,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Placemats Set",
        "sku": "HOM-DEC-3077",
        "price": Decimal128("18.00"),
        "details": {"description": "PVC woven placemats.", "specs": {"count": "4", "heat_resistant": "Yes"}},
        "stock": 90,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Hand Grip Strengthener",
        "sku": "SPO-FIT-3078",
        "price": Decimal128("9.00"),
        "details": {"description": "Adjustable resistance gripper.", "specs": {"range": "10-40kg", "color": "Black"}},
        "stock": 150,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Economics for Dummies",
        "sku": "BOO-EDU-3079",
        "price": Decimal128("20.00"),
        "details": {"description": "Simple guide to economics.", "specs": {"series": "Dummies", "pages": "300"}},
        "stock": 70,
        "category": {"main": "Books", "sub": "Education"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Baseball Cap",
        "sku": "CLO-HAT-3080",
        "price": Decimal128("15.00"),
        "details": {"description": "Cotton cap with logo.", "specs": {"adjust": "Strap", "color": "Red"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Surge Protector 8",
        "sku": "ELE-ACC-3081",
        "price": Decimal128("25.00"),
        "details": {"description": "8 outlet power strip.", "specs": {"usb": "2 ports", "rating": "1800J"}},
        "stock": 80,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Whisk Stainless",
        "sku": "HOM-KIT-3082",
        "price": Decimal128("7.00"),
        "details": {"description": "Balloon whisk for eggs.", "specs": {"size": "10 inch", "handle": "Loop"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Mouthguard Sports",
        "sku": "SPO-PRO-3083",
        "price": Decimal128("8.00"),
        "details": {"description": "Boil and bite gum shield.", "specs": {"size": "Adult", "case": "Yes"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Protection"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Plays",
        "sku": "BOO-FIC-3084",
        "price": Decimal128("18.00"),
        "details": {"description": "Shakespeare selected works.", "specs": {"plays": "4", "notes": "Included"}},
        "stock": 55,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Cardigan Sweater",
        "sku": "CLO-TOP-3085",
        "price": Decimal128("40.00"),
        "details": {"description": "Button up knit cardigan.", "specs": {"material": "Cotton Blend", "color": "Grey"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "USB C Cable 2m",
        "sku": "ELE-ACC-3086",
        "price": Decimal128("12.00"),
        "details": {"description": "Fast charging data cable.", "specs": {"braid": "Nylon", "pd": "60W"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(4, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Garlic Press",
        "sku": "HOM-KIT-3087",
        "price": Decimal128("11.00"),
        "details": {"description": "Heavy duty garlic crusher.", "specs": {"material": "Zinc Alloy", "clean": "Easy"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Ping Pong Balls",
        "sku": "SPO-GAM-3088",
        "price": Decimal128("6.00"),
        "details": {"description": "Pack of 6 table tennis balls.", "specs": {"stars": "3", "color": "Orange"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Yoga Sutras",
        "sku": "BOO-PHI-3089",
        "price": Decimal128("14.00"),
        "details": {"description": "Ancient yoga philosophy.", "specs": {"translation": "English", "pages": "200"}},
        "stock": 65,
        "category": {"main": "Books", "sub": "Philosophy"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Windbreaker Jacket",
        "sku": "CLO-JAC-3090",
        "price": Decimal128("35.00"),
        "details": {"description": "Lightweight rain jacket.", "specs": {"hood": "Yes", "water_resist": "Yes"}},
        "stock": 85,
        "category": {"main": "Clothing", "sub": "Jackets"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Battery Pack AA",
        "sku": "ELE-ACC-3091",
        "price": Decimal128("8.00"),
        "details": {"description": "Pack of 4 alkaline batteries.", "specs": {"voltage": "1.5V", "life": "Long"}},
        "stock": 400,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Oven Thermometer",
        "sku": "HOM-KIT-3092",
        "price": Decimal128("9.00"),
        "details": {"description": "Analog dial temperature gauge.", "specs": {"range": "50-300C", "hang": "Hook"}},
        "stock": 70,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Sweatband Head",
        "sku": "SPO-ACC-3093",
        "price": Decimal128("7.00"),
        "details": {"description": "Terry cloth headband.", "specs": {"absorbent": "High", "color": "Blue"}},
        "stock": 160,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(5, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Short Story Collection",
        "sku": "BOO-FIC-3094",
        "price": Decimal128("16.00"),
        "details": {"description": "Contemporary short fiction.", "specs": {"authors": "Various", "pages": "300"}},
        "stock": 50,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Fleece Gloves",
        "sku": "CLO-ACC-3095",
        "price": Decimal128("12.00"),
        "details": {"description": "Warm winter liner gloves.", "specs": {"material": "Polyester", "color": "Black"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Phone Case Clear",
        "sku": "ELE-ACC-3096",
        "price": Decimal128("10.00"),
        "details": {"description": "Transparent silicone case.", "specs": {"shockproof": "Yes", "model": "Universal 6in"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Tea Infuser",
        "sku": "HOM-KIT-3097",
        "price": Decimal128("6.00"),
        "details": {"description": "Stainless steel mesh ball.", "specs": {"chain": "Hook", "size": "Standard"}},
        "stock": 130,
        "category": {"main": "Home & Kitchen", "sub": "Tea"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Whistle Sports",
        "sku": "SPO-ACC-3098",
        "price": Decimal128("5.00"),
        "details": {"description": "Metal coach whistle with lanyard.", "specs": {"sound": "Loud", "material": "Steel"}},
        "stock": 180,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Minimalist Poetry",
        "sku": "BOO-POE-3099",
        "price": Decimal128("14.00"),
        "details": {"description": "Haiku collection.", "specs": {"pages": "100", "binding": "Hardcover"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Poetry"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Canvas Belt",
        "sku": "CLO-ACC-3100",
        "price": Decimal128("15.00"),
        "details": {"description": "Webbing belt with flip buckle.", "specs": {"width": "1.5 inch", "color": "Green"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Noise Canceling Earplugs",
        "sku": "ELE-AUD-4001",
        "price": Decimal128("19.99"),
        "details": {"description": "Reusable silicone earplugs for sleep.", "specs": {"noise_reduction": "25dB", "material": "Silicone"}},
        "stock": 150,
        "category": {"main": "Electronics", "sub": "Audio Accessories"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Ceramic Knife Set",
        "sku": "HOM-KIT-4002",
        "price": Decimal128("45.00"),
        "details": {"description": "Sharp ceramic kitchen knives.", "specs": {"pieces": "3", "handle": "Soft Grip"}},
        "stock": 80,
        "category": {"main": "Home & Kitchen", "sub": "Cutlery"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Snowboard Bindings",
        "sku": "SPO-WIN-4003",
        "price": Decimal128("120.00"),
        "details": {"description": "Adjustable snowboard bindings.", "specs": {"size": "M", "flex": "Medium"}},
        "stock": 40,
        "category": {"main": "Sports", "sub": "Winter Sports"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Urban Fantasy Novel",
        "sku": "BOO-FIC-4004",
        "price": Decimal128("16.50"),
        "details": {"description": "Magic in a modern city setting.", "specs": {"pages": "320", "author": "N. Gaiman"}},
        "stock": 65,
        "category": {"main": "Books", "sub": "Fantasy"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Plaid Flannel Shirt",
        "sku": "CLO-TOP-4005",
        "price": Decimal128("38.00"),
        "details": {"description": "Warm cotton flannel shirt.", "specs": {"pattern": "Plaid", "fit": "Regular"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Wireless Presenter",
        "sku": "ELE-ACC-4006",
        "price": Decimal128("22.00"),
        "details": {"description": "Laser pointer presentation remote.", "specs": {"range": "50ft", "battery": "AAA"}},
        "stock": 90,
        "category": {"main": "Electronics", "sub": "Office Electronics"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Glass Teapot",
        "sku": "HOM-KIT-4007",
        "price": Decimal128("28.00"),
        "details": {"description": "Heat resistant glass tea maker.", "specs": {"capacity": "800ml", "infuser": "Glass"}},
        "stock": 70,
        "category": {"main": "Home & Kitchen", "sub": "Tea & Coffee"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Soccer Shin Guards",
        "sku": "SPO-SOC-4008",
        "price": Decimal128("14.00"),
        "details": {"description": "Protective gear for football.", "specs": {"size": "L", "protection": "Hard Shell"}},
        "stock": 130,
        "category": {"main": "Sports", "sub": "Soccer"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Historical Romance",
        "sku": "BOO-FIC-4009",
        "price": Decimal128("12.99"),
        "details": {"description": "Love story set in the 19th century.", "specs": {"pages": "380", "cover": "Paperback"}},
        "stock": 100,
        "category": {"main": "Books", "sub": "Romance"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Leather Card Holder",
        "sku": "CLO-ACC-4010",
        "price": Decimal128("25.00"),
        "details": {"description": "Slim minimalist wallet.", "specs": {"material": "Genuine Leather", "slots": "4"}},
        "stock": 120,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "USB Desk Fan",
        "sku": "ELE-HOM-4011",
        "price": Decimal128("15.00"),
        "details": {"description": "Compact cooling fan for desk.", "specs": {"power": "USB", "speed": "2"}},
        "stock": 200,
        "category": {"main": "Electronics", "sub": "Home Appliances"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Silicone Baking Mats",
        "sku": "HOM-KIT-4012",
        "price": Decimal128("18.00"),
        "details": {"description": "Reusable non-stick oven mats.", "specs": {"pack": "2", "temp": "480F"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Bakeware"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Boxing Speed Bag",
        "sku": "SPO-BOX-4013",
        "price": Decimal128("35.00"),
        "details": {"description": "Leather speed ball for training.", "specs": {"material": "Leather", "size": "M"}},
        "stock": 50,
        "category": {"main": "Sports", "sub": "Boxing"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Philosophy of Mind",
        "sku": "BOO-PHI-4014",
        "price": Decimal128("28.00"),
        "details": {"description": "Exploring consciousness and thought.", "specs": {"pages": "250", "level": "Academic"}},
        "stock": 35,
        "category": {"main": "Books", "sub": "Philosophy"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Cotton T-Shirt Pack",
        "sku": "CLO-TOP-4015",
        "price": Decimal128("30.00"),
        "details": {"description": "Pack of 3 basic tees.", "specs": {"color": "White/Black/Grey", "material": "Cotton"}},
        "stock": 150,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Ethernet Switch 5-Port",
        "sku": "ELE-NET-4016",
        "price": Decimal128("20.00"),
        "details": {"description": "Gigabit network switch.", "specs": {"ports": "5", "speed": "10/100/1000"}},
        "stock": 85,
        "category": {"main": "Electronics", "sub": "Networking"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Laundry Bag Mesh",
        "sku": "HOM-BAT-4017",
        "price": Decimal128("8.00"),
        "details": {"description": "Protective wash bags for delicates.", "specs": {"pack": "3", "zipper": "Yes"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Laundry"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Hand Wraps Boxing",
        "sku": "SPO-BOX-4018",
        "price": Decimal128("10.00"),
        "details": {"description": "Cotton hand protection straps.", "specs": {"length": "180in", "color": "Blue"}},
        "stock": 120,
        "category": {"main": "Sports", "sub": "Boxing"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Cooking for Beginners",
        "sku": "BOO-COO-4019",
        "price": Decimal128("20.00"),
        "details": {"description": "Easy recipes for new cooks.", "specs": {"recipes": "50", "photos": "Yes"}},
        "stock": 95,
        "category": {"main": "Books", "sub": "Cooking"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Beanie with Pom Pom",
        "sku": "CLO-HAT-4020",
        "price": Decimal128("18.00"),
        "details": {"description": "Winter knit hat with faux fur.", "specs": {"material": "Acrylic", "color": "Red"}},
        "stock": 75,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Webcam Privacy Cover",
        "sku": "ELE-ACC-4021",
        "price": Decimal128("6.00"),
        "details": {"description": "Slide cover for laptop camera.", "specs": {"pack": "3", "adhesive": "Strong"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Bamboo Dish Rack",
        "sku": "HOM-KIT-4022",
        "price": Decimal128("25.00"),
        "details": {"description": "Foldable wooden plate drying rack.", "specs": {"material": "Bamboo", "levels": "2"}},
        "stock": 60,
        "category": {"main": "Home & Kitchen", "sub": "Kitchen Storage"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Knee Pads Volleyball",
        "sku": "SPO-VOL-4023",
        "price": Decimal128("22.00"),
        "details": {"description": "Cushioned knee protection.", "specs": {"size": "M", "padding": "Thick"}},
        "stock": 80,
        "category": {"main": "Sports", "sub": "Volleyball"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Modern Art Book",
        "sku": "BOO-ART-4024",
        "price": Decimal128("40.00"),
        "details": {"description": "Coffee table book on modernism.", "specs": {"format": "Hardcover", "pages": "200"}},
        "stock": 45,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Infinity Scarf",
        "sku": "CLO-ACC-4025",
        "price": Decimal128("20.00"),
        "details": {"description": "Loop scarf for cold weather.", "specs": {"material": "Knit", "color": "Grey"}},
        "stock": 100,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Micro USB Cable",
        "sku": "ELE-ACC-4026",
        "price": Decimal128("8.00"),
        "details": {"description": "Charging cable for older devices.", "specs": {"length": "1m", "pack": "2"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Cables"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(4, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Toilet Brush Set",
        "sku": "HOM-BAT-4027",
        "price": Decimal128("15.00"),
        "details": {"description": "Brush with holder for bathroom.", "specs": {"material": "Plastic", "color": "White"}},
        "stock": 110,
        "category": {"main": "Home & Kitchen", "sub": "Bathroom"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Swimming Goggles Pro",
        "sku": "SPO-SWI-4028",
        "price": Decimal128("25.00"),
        "details": {"description": "Anti-fog racing goggles.", "specs": {"lens": "Mirrored", "strap": "Double"}},
        "stock": 70,
        "category": {"main": "Sports", "sub": "Swimming"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Travel Guide Italy",
        "sku": "BOO-TRA-4029",
        "price": Decimal128("22.00"),
        "details": {"description": "Complete guide to Italian cities.", "specs": {"pages": "400", "maps": "Included"}},
        "stock": 90,
        "category": {"main": "Books", "sub": "Travel"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Cargo Pants",
        "sku": "CLO-BOT-4030",
        "price": Decimal128("45.00"),
        "details": {"description": "Utility pants with many pockets.", "specs": {"material": "Cotton", "color": "Green"}},
        "stock": 85,
        "category": {"main": "Clothing", "sub": "Bottoms"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Stylus Pen",
        "sku": "ELE-ACC-4031",
        "price": Decimal128("15.00"),
        "details": {"description": "Touch pen for tablets.", "specs": {"compatibility": "Universal", "tip": "Rubber"}},
        "stock": 130,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Ice Cube Trays",
        "sku": "HOM-KIT-4032",
        "price": Decimal128("10.00"),
        "details": {"description": "Silicone flexible ice molds.", "specs": {"pack": "2", "shape": "Square"}},
        "stock": 160,
        "category": {"main": "Home & Kitchen", "sub": "Kitchenware"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Foam Yoga Block",
        "sku": "SPO-YOG-4033",
        "price": Decimal128("12.00"),
        "details": {"description": "Support block for yoga poses.", "specs": {"material": "EVA Foam", "color": "Purple"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Yoga"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Poetry",
        "sku": "BOO-POE-4034",
        "price": Decimal128("14.00"),
        "details": {"description": "Selected poems of Robert Frost.", "specs": {"pages": "150", "cover": "Paperback"}},
        "stock": 55,
        "category": {"main": "Books", "sub": "Poetry"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Wool Socks",
        "sku": "CLO-ACC-4035",
        "price": Decimal128("18.00"),
        "details": {"description": "Warm hiking socks pair.", "specs": {"material": "Merino Blend", "size": "One Size"}},
        "stock": 120,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Cable Management Box",
        "sku": "ELE-ORG-4036",
        "price": Decimal128("20.00"),
        "details": {"description": "Organizer to hide power strips.", "specs": {"color": "White", "size": "Large"}},
        "stock": 75,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Pizza Stone",
        "sku": "HOM-KIT-4037",
        "price": Decimal128("35.00"),
        "details": {"description": "Ceramic stone for crispy crust.", "specs": {"diameter": "15 inch", "shape": "Round"}},
        "stock": 45,
        "category": {"main": "Home & Kitchen", "sub": "Bakeware"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Badminton Racket",
        "sku": "SPO-BAD-4038",
        "price": Decimal128("40.00"),
        "details": {"description": "Lightweight carbon racket.", "specs": {"weight": "85g", "string": "Tension 24"}},
        "stock": 60,
        "category": {"main": "Sports", "sub": "Badminton"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Memoir Bestseller",
        "sku": "BOO-BIO-4039",
        "price": Decimal128("24.00"),
        "details": {"description": "Inspiring life story.", "specs": {"pages": "350", "cover": "Hardcover"}},
        "stock": 80,
        "category": {"main": "Books", "sub": "Biography"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Running Shorts",
        "sku": "CLO-BOT-4040",
        "price": Decimal128("28.00"),
        "details": {"description": "Breathable athletic shorts.", "specs": {"liner": "Yes", "length": "5 inch"}},
        "stock": 95,
        "category": {"main": "Clothing", "sub": "Bottoms"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Tripod for Phone",
        "sku": "ELE-ACC-4041",
        "price": Decimal128("25.00"),
        "details": {"description": "Flexible mini tripod stand.", "specs": {"height": "12 inch", "mount": "Universal"}},
        "stock": 110,
        "category": {"main": "Electronics", "sub": "Camera Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Jar Opener Gripper",
        "sku": "HOM-KIT-4042",
        "price": Decimal128("8.00"),
        "details": {"description": "Rubber pad for opening jars.", "specs": {"material": "Silicone", "pack": "3"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Agility Cones",
        "sku": "SPO-TRA-4043",
        "price": Decimal128("15.00"),
        "details": {"description": "Training marker cones set.", "specs": {"count": "20", "color": "Orange"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Training"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Self-Help Bestseller",
        "sku": "BOO-SEL-4044",
        "price": Decimal128("18.00"),
        "details": {"description": "Guide to personal growth.", "specs": {"pages": "280", "cover": "Paperback"}},
        "stock": 120,
        "category": {"main": "Books", "sub": "Self-Help"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Denim Jacket",
        "sku": "CLO-OUT-4045",
        "price": Decimal128("60.00"),
        "details": {"description": "Classic blue jean jacket.", "specs": {"fit": "Trucker", "wash": "Medium"}},
        "stock": 55,
        "category": {"main": "Clothing", "sub": "Outerwear"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Monitor Stand Riser",
        "sku": "ELE-OFF-4046",
        "price": Decimal128("30.00"),
        "details": {"description": "Desktop monitor elevator.", "specs": {"material": "Wood", "storage": "Underneath"}},
        "stock": 70,
        "category": {"main": "Electronics", "sub": "Office Electronics"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Paper Towel Holder",
        "sku": "HOM-KIT-4047",
        "price": Decimal128("15.00"),
        "details": {"description": "Countertop roll dispenser.", "specs": {"material": "Stainless Steel", "base": "Weighted"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Kitchen Storage"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Resistance Bands Set",
        "sku": "SPO-FIT-4048",
        "price": Decimal128("20.00"),
        "details": {"description": "Exercise bands with handles.", "specs": {"levels": "5", "bag": "Included"}},
        "stock": 160,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(4, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Children's Picture Book",
        "sku": "BOO-KID-4049",
        "price": Decimal128("12.00"),
        "details": {"description": "Illustrated animal story.", "specs": {"age": "3-5", "pages": "32"}},
        "stock": 90,
        "category": {"main": "Books", "sub": "Children"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Canvas Belt",
        "sku": "CLO-ACC-4050",
        "price": Decimal128("15.00"),
        "details": {"description": "Webbing belt with D-ring.", "specs": {"color": "Beige", "width": "1.5in"}},
        "stock": 115,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Laptop Sleeve 15",
        "sku": "ELE-ACC-4051",
        "price": Decimal128("20.00"),
        "details": {"description": "Protective case for laptop.", "specs": {"size": "15.6 inch", "padding": "Foam"}},
        "stock": 130,
        "category": {"main": "Electronics", "sub": "Computer Accessories"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Soap Dispenser",
        "sku": "HOM-BAT-4052",
        "price": Decimal128("12.00"),
        "details": {"description": "Glass liquid soap bottle.", "specs": {"pump": "Metal", "capacity": "500ml"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Bathroom"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Jump Rope",
        "sku": "SPO-FIT-4053",
        "price": Decimal128("8.00"),
        "details": {"description": "PVC skipping rope for cardio.", "specs": {"length": "Adjustable", "color": "Black"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Business Strategy Book",
        "sku": "BOO-BUS-4054",
        "price": Decimal128("26.00"),
        "details": {"description": "Modern management techniques.", "specs": {"pages": "300", "edition": "Revised"}},
        "stock": 50,
        "category": {"main": "Books", "sub": "Business"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Silk Scarf Floral",
        "sku": "CLO-ACC-4055",
        "price": Decimal128("35.00"),
        "details": {"description": "Elegant printed silk scarf.", "specs": {"size": "Square", "pattern": "Flowers"}},
        "stock": 70,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "HDMI Adapter USB-C",
        "sku": "ELE-ACC-4056",
        "price": Decimal128("25.00"),
        "details": {"description": "Connect laptop to TV.", "specs": {"resolution": "4K@60Hz", "port": "USB-C"}},
        "stock": 80,
        "category": {"main": "Electronics", "sub": "Adapters"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(3, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Wine Opener Electric",
        "sku": "HOM-KIT-4057",
        "price": Decimal128("30.00"),
        "details": {"description": "Cordless corkscrew remover.", "specs": {"battery": "Rechargeable", "cutter": "Included"}},
        "stock": 60,
        "category": {"main": "Home & Kitchen", "sub": "Wine Accessories"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Ankle Weights 2lb",
        "sku": "SPO-FIT-4058",
        "price": Decimal128("18.00"),
        "details": {"description": "Wearable weights for walking.", "specs": {"weight": "2 lbs per leg", "strap": "Velcro"}},
        "stock": 90,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Travel Phrasebook",
        "sku": "BOO-REF-4059",
        "price": Decimal128("10.00"),
        "details": {"description": "Essential Spanish phrases.", "specs": {"size": "Pocket", "pages": "120"}},
        "stock": 110,
        "category": {"main": "Books", "sub": "Travel"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Crew Neck Sweatshirt",
        "sku": "CLO-TOP-4060",
        "price": Decimal128("32.00"),
        "details": {"description": "Classic casual pullover.", "specs": {"material": "Cotton Fleece", "color": "Navy"}},
        "stock": 100,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Bluetooth Audio Receiver",
        "sku": "ELE-AUD-4061",
        "price": Decimal128("18.00"),
        "details": {"description": "Add wireless to old speakers.", "specs": {"version": "5.0", "range": "30ft"}},
        "stock": 140,
        "category": {"main": "Electronics", "sub": "Audio Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Drawer Dividers",
        "sku": "HOM-ORG-4062",
        "price": Decimal128("15.00"),
        "details": {"description": "Adjustable organizers for clothes.", "specs": {"pack": "4", "material": "Plastic"}},
        "stock": 120,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Stopwatch",
        "sku": "SPO-ACC-4063",
        "price": Decimal128("12.00"),
        "details": {"description": "Digital timer for sports.", "specs": {"display": "LCD", "lanyard": "Yes"}},
        "stock": 160,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Biography of an Artist",
        "sku": "BOO-BIO-4064",
        "price": Decimal128("28.00"),
        "details": {"description": "Life of Frida Kahlo.", "specs": {"pages": "400", "photos": "Included"}},
        "stock": 35,
        "category": {"main": "Books", "sub": "Biography"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Athletic Headband",
        "sku": "CLO-ACC-4065",
        "price": Decimal128("8.00"),
        "details": {"description": "Moisture wicking sweatband.", "specs": {"width": "Wide", "color": "Black"}},
        "stock": 250,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "USB Hub 4-Port",
        "sku": "ELE-ACC-4066",
        "price": Decimal128("12.00"),
        "details": {"description": "Expand laptop USB ports.", "specs": {"speed": "3.0", "cable": "Short"}},
        "stock": 180,
        "category": {"main": "Electronics", "sub": "Computer Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Salt and Pepper Grinders",
        "sku": "HOM-KIT-4067",
        "price": Decimal128("25.00"),
        "details": {"description": "Wooden spice mills set.", "specs": {"mechanism": "Ceramic", "height": "8 inch"}},
        "stock": 70,
        "category": {"main": "Home & Kitchen", "sub": "Kitchenware"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Gym Bag Small",
        "sku": "SPO-ACC-4068",
        "price": Decimal128("30.00"),
        "details": {"description": "Compact duffel for workout gear.", "specs": {"capacity": "25L", "shoe_pocket": "Yes"}},
        "stock": 90,
        "category": {"main": "Sports", "sub": "Bags"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Literature",
        "sku": "BOO-FIC-4069",
        "price": Decimal128("14.00"),
        "details": {"description": "Pride and Prejudice.", "specs": {"author": "Jane Austen", "edition": "Penguin"}},
        "stock": 120,
        "category": {"main": "Books", "sub": "Classics"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Wool Socks",
        "sku": "CLO-ACC-4070",
        "price": Decimal128("16.00"),
        "details": {"description": "Warm winter hiking socks.", "specs": {"material": "Wool Blend", "pair": "1"}},
        "stock": 150,
        "category": {"main": "Clothing", "sub": "Socks"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Phone Charging Stand",
        "sku": "ELE-ACC-4071",
        "price": Decimal128("20.00"),
        "details": {"description": "Aluminum dock for desk.", "specs": {"cable_mgmt": "Yes", "color": "Black"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Phone Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Cookie Cutters Set",
        "sku": "HOM-KIT-4072",
        "price": Decimal128("12.00"),
        "details": {"description": "Various shapes for baking.", "specs": {"material": "Metal", "count": "10"}},
        "stock": 130,
        "category": {"main": "Home & Kitchen", "sub": "Bakeware"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Tennis Overgrips",
        "sku": "SPO-TEN-4073",
        "price": Decimal128("8.00"),
        "details": {"description": "Pack of 3 racket grips.", "specs": {"color": "White", "feel": "Tacky"}},
        "stock": 220,
        "category": {"main": "Sports", "sub": "Tennis"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Science Textbook",
        "sku": "BOO-EDU-4074",
        "price": Decimal128("60.00"),
        "details": {"description": "High school biology book.", "specs": {"pages": "500", "cover": "Hardcover"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Education"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Bucket Hat",
        "sku": "CLO-HAT-4075",
        "price": Decimal128("18.00"),
        "details": {"description": "Casual cotton sun hat.", "specs": {"color": "Khaki", "size": "One Size"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Screen Cleaner Kit",
        "sku": "ELE-ACC-4076",
        "price": Decimal128("10.00"),
        "details": {"description": "Spray and microfiber cloth.", "specs": {"safe_for": "All Screens", "vol": "100ml"}},
        "stock": 190,
        "category": {"main": "Electronics", "sub": "Cleaning"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Vegetable Peeler",
        "sku": "HOM-KIT-4077",
        "price": Decimal128("8.00"),
        "details": {"description": "Swivel blade peeler.", "specs": {"handle": "Grip", "blade": "Steel"}},
        "stock": 160,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Golf Tees Pack",
        "sku": "SPO-GOL-4078",
        "price": Decimal128("6.00"),
        "details": {"description": "Wooden tees bag.", "specs": {"count": "50", "length": "2.75 inch"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Golf"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Poetry Anthology",
        "sku": "BOO-POE-4079",
        "price": Decimal128("20.00"),
        "details": {"description": "Modern poems collection.", "specs": {"editor": "Various", "pages": "250"}},
        "stock": 55,
        "category": {"main": "Books", "sub": "Poetry"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Running Belt",
        "sku": "CLO-ACC-4080",
        "price": Decimal128("15.00"),
        "details": {"description": "Waist pouch for phone/keys.", "specs": {"adjustable": "Yes", "reflective": "Yes"}},
        "stock": 140,
        "category": {"main": "Clothing", "sub": "Sportswear"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Mouse Pad",
        "sku": "ELE-ACC-4081",
        "price": Decimal128("8.00"),
        "details": {"description": "Standard cloth mouse mat.", "specs": {"base": "Rubber", "color": "Black"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Peripherals"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Measuring Spoons",
        "sku": "HOM-KIT-4082",
        "price": Decimal128("7.00"),
        "details": {"description": "Stainless steel spoons set.", "specs": {"count": "5", "ring": "Included"}},
        "stock": 170,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Whistle Lanyard",
        "sku": "SPO-ACC-4083",
        "price": Decimal128("5.00"),
        "details": {"description": "Coach whistle.", "specs": {"material": "Plastic", "sound": "Loud"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Short Story Book",
        "sku": "BOO-FIC-4084",
        "price": Decimal128("14.00"),
        "details": {"description": "Collection of short fiction.", "specs": {"author": "A. Chekhov", "pages": "200"}},
        "stock": 65,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Cotton Bandana",
        "sku": "CLO-ACC-4085",
        "price": Decimal128("5.00"),
        "details": {"description": "Square paisley scarf.", "specs": {"size": "22x22", "color": "Red"}},
        "stock": 250,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Stylus Tips Replacement",
        "sku": "ELE-ACC-4086",
        "price": Decimal128("10.00"),
        "details": {"description": "Nibs for digital pen.", "specs": {"pack": "4", "compatibility": "Specific"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Sink Strainer",
        "sku": "HOM-KIT-4087",
        "price": Decimal128("6.00"),
        "details": {"description": "Stainless steel mesh drain.", "specs": {"size": "Standard", "rim": "Wide"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Sink Accessories"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Ping Pong Paddles",
        "sku": "SPO-GAM-4088",
        "price": Decimal128("30.00"),
        "details": {"description": "Table tennis racket set.", "specs": {"count": "2", "case": "Yes"}},
        "stock": 75,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Art History Book",
        "sku": "BOO-ART-4089",
        "price": Decimal128("45.00"),
        "details": {"description": "Renaissance to Modern.", "specs": {"images": "Full Color", "pages": "500"}},
        "stock": 30,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Shoelaces Pack",
        "sku": "CLO-ACC-4090",
        "price": Decimal128("8.00"),
        "details": {"description": "Flat athletic laces.", "specs": {"length": "45 inch", "colors": "Mixed"}},
        "stock": 200,
        "category": {"main": "Clothing", "sub": "Shoe Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Cable Ties",
        "sku": "ELE-ORG-4091",
        "price": Decimal128("5.00"),
        "details": {"description": "Velcro reusable straps.", "specs": {"pack": "20", "color": "Black"}},
        "stock": 350,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Pot Holder",
        "sku": "HOM-KIT-4092",
        "price": Decimal128("7.00"),
        "details": {"description": "Cotton heat pad.", "specs": {"size": "8x8", "loop": "Hanging"}},
        "stock": 150,
        "category": {"main": "Home & Kitchen", "sub": "Linens"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Mouthguard Case",
        "sku": "SPO-PRO-4093",
        "price": Decimal128("5.00"),
        "details": {"description": "Hygienic storage box.", "specs": {"vented": "Yes", "color": "Clear"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Dictionary Pocket",
        "sku": "BOO-REF-4094",
        "price": Decimal128("8.00"),
        "details": {"description": "Small English dictionary.", "specs": {"size": "Mini", "paperback": "Yes"}},
        "stock": 120,
        "category": {"main": "Books", "sub": "Reference"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "No-Show Socks",
        "sku": "CLO-ACC-4095",
        "price": Decimal128("12.00"),
        "details": {"description": "Invisible liner socks.", "specs": {"grip": "Heel", "pack": "3"}},
        "stock": 180,
        "category": {"main": "Clothing", "sub": "Socks"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Microfiber Cloth",
        "sku": "ELE-CLN-4096",
        "price": Decimal128("15.00"),
        "details": {"description": "Large cleaning cloth pack.", "specs": {"count": "6", "size": "12x12"}},
        "stock": 220,
        "category": {"main": "Electronics", "sub": "Cleaning"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Bottle Opener",
        "sku": "HOM-KIT-4097",
        "price": Decimal128("6.00"),
        "details": {"description": "Stainless steel flat opener.", "specs": {"heavy_duty": "Yes", "slim": "Yes"}},
        "stock": 190,
        "category": {"main": "Home & Kitchen", "sub": "Barware"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Ball Pump Needle",
        "sku": "SPO-ACC-4098",
        "price": Decimal128("4.00"),
        "details": {"description": "Inflation needles pack.", "specs": {"count": "5", "thread": "Standard"}},
        "stock": 300,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Notebook Ruled",
        "sku": "BOO-STA-4099",
        "price": Decimal128("5.00"),
        "details": {"description": "Standard lined notebook.", "specs": {"pages": "100", "size": "A5"}},
        "stock": 250,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Tote Bag Plain",
        "sku": "CLO-ACC-4100",
        "price": Decimal128("8.00"),
        "details": {"description": "Canvas bag for painting.", "specs": {"color": "Natural", "handles": "Long"}},
        "stock": 160,
        "category": {"main": "Clothing", "sub": "Bags"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Solar Power Bank 20000mAh",
        "sku": "ELE-ACC-5001",
        "price": Decimal128("45.99"),
        "details": {"description": "Portable solar charger for outdoors.", "specs": {"capacity": "20000mAh", "panel": "Solar"}},
        "stock": 85,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Lemon Zester",
        "sku": "HOM-KIT-5002",
        "price": Decimal128("9.00"),
        "details": {"description": "Stainless steel citrus grater.", "specs": {"handle": "Non-slip", "blade": "Fine"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Running Visor",
        "sku": "SPO-RUN-5003",
        "price": Decimal128("15.00"),
        "details": {"description": "Lightweight sun visor for running.", "specs": {"material": "Polyester", "adjust": "Velcro"}},
        "stock": 110,
        "category": {"main": "Sports", "sub": "Running"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Keto Diet Cookbook",
        "sku": "BOO-COO-5004",
        "price": Decimal128("22.00"),
        "details": {"description": "Low carb recipes for beginners.", "specs": {"recipes": "100+", "cover": "Paperback"}},
        "stock": 60,
        "category": {"main": "Books", "sub": "Cooking"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "V-Neck T-Shirt",
        "sku": "CLO-TOP-5005",
        "price": Decimal128("25.00"),
        "details": {"description": "Soft cotton V-neck tee.", "specs": {"fit": "Slim", "color": "Navy"}},
        "stock": 150,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(2, 8)
    },
    {
        "_id": ObjectId(),
        "name": "DisplayPort Cable",
        "sku": "ELE-ACC-5006",
        "price": Decimal128("14.00"),
        "details": {"description": "4K video cable for monitors.", "specs": {"version": "1.4", "length": "2m"}},
        "stock": 200,
        "category": {"main": "Electronics", "sub": "Cables"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Soap Dish Ceramic",
        "sku": "HOM-BAT-5007",
        "price": Decimal128("12.00"),
        "details": {"description": "White ceramic bar soap holder.", "specs": {"design": "Modern", "drainage": "Yes"}},
        "stock": 90,
        "category": {"main": "Home & Kitchen", "sub": "Bathroom"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Golf Towel",
        "sku": "SPO-GOL-5008",
        "price": Decimal128("10.00"),
        "details": {"description": "Microfiber towel with clip.", "specs": {"size": "16x24", "color": "Black"}},
        "stock": 120,
        "category": {"main": "Sports", "sub": "Golf"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Historical Fiction",
        "sku": "BOO-FIC-5009",
        "price": Decimal128("18.00"),
        "details": {"description": "Novel set in WWII era.", "specs": {"pages": "450", "author": "K. Hannah"}},
        "stock": 75,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Pajama Bottoms",
        "sku": "CLO-SLP-5010",
        "price": Decimal128("28.00"),
        "details": {"description": "Cotton flannel sleep pants.", "specs": {"pattern": "Check", "waist": "Elastic"}},
        "stock": 100,
        "category": {"main": "Clothing", "sub": "Sleepwear"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Smart Light Strip",
        "sku": "ELE-SMA-5011",
        "price": Decimal128("35.00"),
        "details": {"description": "RGB LED strip with app control.", "specs": {"length": "5m", "adhesive": "Back"}},
        "stock": 180,
        "category": {"main": "Electronics", "sub": "Smart Home"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Silicone Tongs",
        "sku": "HOM-KIT-5012",
        "price": Decimal128("11.00"),
        "details": {"description": "Kitchen tongs for cooking.", "specs": {"tips": "Silicone", "lock": "Ring"}},
        "stock": 130,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Pilates Ball Mini",
        "sku": "SPO-FIT-5013",
        "price": Decimal128("14.00"),
        "details": {"description": "Small exercise ball for core.", "specs": {"size": "9 inch", "texture": "Grip"}},
        "stock": 95,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Graphic Design Annual",
        "sku": "BOO-DES-5014",
        "price": Decimal128("50.00"),
        "details": {"description": "Best designs of the year.", "specs": {"format": "Hardcover", "pages": "300"}},
        "stock": 30,
        "category": {"main": "Books", "sub": "Design"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Suspenders",
        "sku": "CLO-ACC-5015",
        "price": Decimal128("18.00"),
        "details": {"description": "Adjustable elastic suspenders.", "specs": {"style": "Y-Back", "clips": "Metal"}},
        "stock": 70,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(2, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Trackball Mouse",
        "sku": "ELE-MOU-5016",
        "price": Decimal128("40.00"),
        "details": {"description": "Ergonomic thumb control mouse.", "specs": {"wireless": "Yes", "buttons": "5"}},
        "stock": 60,
        "category": {"main": "Electronics", "sub": "Peripherals"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Wine Stoppers",
        "sku": "HOM-KIT-5017",
        "price": Decimal128("8.00"),
        "details": {"description": "Silicone reusable bottle sealers.", "specs": {"pack": "4", "colors": "Mixed"}},
        "stock": 220,
        "category": {"main": "Home & Kitchen", "sub": "Barware"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Shin Guard Sleeves",
        "sku": "SPO-SOC-5018",
        "price": Decimal128("12.00"),
        "details": {"description": "Compression sleeves for guards.", "specs": {"material": "Nylon", "size": "M"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Soccer"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Crossword Puzzles",
        "sku": "BOO-GAM-5019",
        "price": Decimal128("10.00"),
        "details": {"description": "Brain teaser puzzle book.", "specs": {"level": "Hard", "pages": "200"}},
        "stock": 130,
        "category": {"main": "Books", "sub": "Games"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Sports Bra High Impact",
        "sku": "CLO-ACT-5020",
        "price": Decimal128("35.00"),
        "details": {"description": "Supportive running bra.", "specs": {"padding": "Removable", "back": "Racer"}},
        "stock": 80,
        "category": {"main": "Clothing", "sub": "Activewear"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "USB C Adapter",
        "sku": "ELE-ACC-5021",
        "price": Decimal128("10.00"),
        "details": {"description": "USB-C to USB-A adapter.", "specs": {"pack": "2", "body": "Aluminum"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Adapters"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Meat Thermometer",
        "sku": "HOM-KIT-5022",
        "price": Decimal128("15.00"),
        "details": {"description": "Instant read digital probe.", "specs": {"waterproof": "Yes", "magnetic": "Yes"}},
        "stock": 110,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Yoga Strap",
        "sku": "SPO-YOG-5023",
        "price": Decimal128("9.00"),
        "details": {"description": "Cotton belt for stretching.", "specs": {"length": "8ft", "buckle": "D-Ring"}},
        "stock": 160,
        "category": {"main": "Sports", "sub": "Yoga"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Political Science",
        "sku": "BOO-POL-5024",
        "price": Decimal128("28.00"),
        "details": {"description": "Introduction to global politics.", "specs": {"pages": "400", "edition": "3rd"}},
        "stock": 45,
        "category": {"main": "Books", "sub": "Education"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Running Gloves",
        "sku": "CLO-ACC-5025",
        "price": Decimal128("18.00"),
        "details": {"description": "Lightweight touchscreen gloves.", "specs": {"reflective": "Yes", "color": "Neon"}},
        "stock": 95,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "E-Reader Cover",
        "sku": "ELE-ACC-5026",
        "price": Decimal128("15.00"),
        "details": {"description": "Smart wake/sleep case.", "specs": {"fit": "6 inch", "material": "PU Leather"}},
        "stock": 120,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Bagel Slicer",
        "sku": "HOM-KIT-5027",
        "price": Decimal128("20.00"),
        "details": {"description": "Safety guillotine cutter.", "specs": {"blade": "Steel", "shield": "Plastic"}},
        "stock": 70,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Bike Lock Cable",
        "sku": "SPO-CYC-5028",
        "price": Decimal128("15.00"),
        "details": {"description": "Coiled security cable lock.", "specs": {"keys": "2", "length": "4ft"}},
        "stock": 140,
        "category": {"main": "Sports", "sub": "Cycling"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Architecture Annual",
        "sku": "BOO-ART-5029",
        "price": Decimal128("45.00"),
        "details": {"description": "Year's best buildings.", "specs": {"photos": "Color", "format": "Large"}},
        "stock": 35,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Polo Shirt Striped",
        "sku": "CLO-TOP-5030",
        "price": Decimal128("32.00"),
        "details": {"description": "Casual striped polo.", "specs": {"material": "Cotton", "fit": "Slim"}},
        "stock": 105,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Webcam Stand",
        "sku": "ELE-ACC-5031",
        "price": Decimal128("18.00"),
        "details": {"description": "Adjustable desk arm mount.", "specs": {"clamp": "C-Clamp", "thread": "1/4"}},
        "stock": 85,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Nutcracker Tool",
        "sku": "HOM-KIT-5032",
        "price": Decimal128("12.00"),
        "details": {"description": "Heavy duty nut cracker.", "specs": {"grip": "Rubber", "material": "Zinc"}},
        "stock": 110,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Resistance Tubes",
        "sku": "SPO-FIT-5033",
        "price": Decimal128("22.00"),
        "details": {"description": "Workout tubes with handles.", "specs": {"count": "5", "anchor": "Door"}},
        "stock": 130,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Garden Encyclopedia",
        "sku": "BOO-HOB-5034",
        "price": Decimal128("35.00"),
        "details": {"description": "A-Z of plants and flowers.", "specs": {"pages": "600", "images": "Yes"}},
        "stock": 50,
        "category": {"main": "Books", "sub": "Hobbies"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Waist Trimmer Belt",
        "sku": "CLO-ACC-5035",
        "price": Decimal128("15.00"),
        "details": {"description": "Neoprene workout belt.", "specs": {"closure": "Velcro", "width": "8 inch"}},
        "stock": 160,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Phone Ring Holder",
        "sku": "ELE-ACC-5036",
        "price": Decimal128("8.00"),
        "details": {"description": "Finger grip stand.", "specs": {"rotate": "360", "adhesive": "3M"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Tea Towels Pack",
        "sku": "HOM-KIT-5037",
        "price": Decimal128("14.00"),
        "details": {"description": "Cotton absorbent kitchen towels.", "specs": {"count": "4", "pattern": "Check"}},
        "stock": 190,
        "category": {"main": "Home & Kitchen", "sub": "Linens"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Ski Goggles Kids",
        "sku": "SPO-WIN-5038",
        "price": Decimal128("30.00"),
        "details": {"description": "Junior size snow goggles.", "specs": {"uv": "400", "anti-fog": "Yes"}},
        "stock": 65,
        "category": {"main": "Sports", "sub": "Winter"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Mythology Book",
        "sku": "BOO-HIS-5039",
        "price": Decimal128("20.00"),
        "details": {"description": "Stories of Greek gods.", "specs": {"author": "Hamilton", "cover": "Paperback"}},
        "stock": 80,
        "category": {"main": "Books", "sub": "History"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Thermal Socks",
        "sku": "CLO-ACC-5040",
        "price": Decimal128("16.00"),
        "details": {"description": "Heavy duty cold weather socks.", "specs": {"rating": "Sub-zero", "pair": "1"}},
        "stock": 140,
        "category": {"main": "Clothing", "sub": "Socks"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Microphone Stand",
        "sku": "ELE-AUD-5041",
        "price": Decimal128("25.00"),
        "details": {"description": "Desktop tripod mic stand.", "specs": {"foldable": "Yes", "clip": "Included"}},
        "stock": 70,
        "category": {"main": "Electronics", "sub": "Audio"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Butter Dish",
        "sku": "HOM-KIT-5042",
        "price": Decimal128("15.00"),
        "details": {"description": "Ceramic dish with wooden lid.", "specs": {"color": "White", "size": "Large"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Tableware"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Tennis Racket Dampener",
        "sku": "SPO-TEN-5043",
        "price": Decimal128("5.00"),
        "details": {"description": "Vibration absorber set.", "specs": {"pack": "2", "design": "Logo"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Tennis"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "DIY Home Repair",
        "sku": "BOO-HOB-5044",
        "price": Decimal128("24.00"),
        "details": {"description": "Manual for home maintenance.", "specs": {"pages": "350", "diagrams": "Yes"}},
        "stock": 55,
        "category": {"main": "Books", "sub": "Hobbies"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Woven Belt",
        "sku": "CLO-ACC-5045",
        "price": Decimal128("20.00"),
        "details": {"description": "Elastic braided stretch belt.", "specs": {"color": "Brown", "buckle": "Zinc"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(3, 10)
    },
    {
        "_id": ObjectId(),
        "name": "VR Controller Cover",
        "sku": "ELE-GAM-5046",
        "price": Decimal128("12.00"),
        "details": {"description": "Silicone grip skin.", "specs": {"anti-slip": "Yes", "color": "Black"}},
        "stock": 90,
        "category": {"main": "Electronics", "sub": "Gaming"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Pastry Brush",
        "sku": "HOM-KIT-5047",
        "price": Decimal128("6.00"),
        "details": {"description": "Silicone basting brush.", "specs": {"heat_resist": "Yes", "clean": "Easy"}},
        "stock": 160,
        "category": {"main": "Home & Kitchen", "sub": "Bakeware"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Kickboard Swimming",
        "sku": "SPO-SWI-5048",
        "price": Decimal128("15.00"),
        "details": {"description": "EVA foam training board.", "specs": {"buoyancy": "High", "grip": "Cutout"}},
        "stock": 70,
        "category": {"main": "Sports", "sub": "Swimming"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Espresso Guide",
        "sku": "BOO-COO-5049",
        "price": Decimal128("16.00"),
        "details": {"description": "Barista techniques book.", "specs": {"pages": "120", "topic": "Coffee"}},
        "stock": 85,
        "category": {"main": "Books", "sub": "Cooking"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Fingerless Gloves",
        "sku": "CLO-ACC-5050",
        "price": Decimal128("12.00"),
        "details": {"description": "Knit typing gloves.", "specs": {"material": "Acrylic", "color": "Grey"}},
        "stock": 130,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Cable Clips",
        "sku": "ELE-ORG-5051",
        "price": Decimal128("7.00"),
        "details": {"description": "Adhesive desktop wire holders.", "specs": {"pack": "10", "slots": "Single"}},
        "stock": 350,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(4, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Baking Spatula Offset",
        "sku": "HOM-KIT-5052",
        "price": Decimal128("9.00"),
        "details": {"description": "Icing spatula for cakes.", "specs": {"blade": "Steel", "length": "8 inch"}},
        "stock": 120,
        "category": {"main": "Home & Kitchen", "sub": "Bakeware"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Sport Cones Set",
        "sku": "SPO-TRA-5053",
        "price": Decimal128("18.00"),
        "details": {"description": "Disc cones for agility.", "specs": {"count": "20", "holder": "Yes"}},
        "stock": 80,
        "category": {"main": "Sports", "sub": "Training"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Modern Fiction",
        "sku": "BOO-FIC-5054",
        "price": Decimal128("15.00"),
        "details": {"description": "Contemporary novel bestseller.", "specs": {"author": "S. Rooney", "format": "Paperback"}},
        "stock": 100,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Wool Beanie",
        "sku": "CLO-HAT-5055",
        "price": Decimal128("20.00"),
        "details": {"description": "Merino wool knit hat.", "specs": {"warmth": "High", "color": "Green"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Headphone Stand",
        "sku": "ELE-ACC-5056",
        "price": Decimal128("15.00"),
        "details": {"description": "Aluminum headset holder.", "specs": {"base": "Anti-slip", "color": "Silver"}},
        "stock": 70,
        "category": {"main": "Electronics", "sub": "Audio Accessories"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Cutting Board Oil",
        "sku": "HOM-KIT-5057",
        "price": Decimal128("10.00"),
        "details": {"description": "Food grade mineral oil.", "specs": {"volume": "250ml", "safe": "Yes"}},
        "stock": 150,
        "category": {"main": "Home & Kitchen", "sub": "Maintenance"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Archery Glove",
        "sku": "SPO-ARC-5058",
        "price": Decimal128("14.00"),
        "details": {"description": "3-finger leather glove.", "specs": {"size": "M", "hand": "Right"}},
        "stock": 40,
        "category": {"main": "Sports", "sub": "Archery"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Travel Guide Spain",
        "sku": "BOO-TRA-5059",
        "price": Decimal128("20.00"),
        "details": {"description": "Insider tips for Barcelona.", "specs": {"pages": "300", "maps": "City"}},
        "stock": 65,
        "category": {"main": "Books", "sub": "Travel"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Gym Towel",
        "sku": "CLO-ACC-5060",
        "price": Decimal128("12.00"),
        "details": {"description": "Quick dry microfiber towel.", "specs": {"size": "Small", "zip": "Pocket"}},
        "stock": 130,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Wireless Earbud Case",
        "sku": "ELE-ACC-5061",
        "price": Decimal128("8.00"),
        "details": {"description": "Silicone protective cover.", "specs": {"clip": "Carabiner", "color": "Blue"}},
        "stock": 200,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(1, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Shower Squeegee",
        "sku": "HOM-BAT-5062",
        "price": Decimal128("12.00"),
        "details": {"description": "Glass wiper with hook.", "specs": {"blade": "Silicone", "handle": "Steel"}},
        "stock": 110,
        "category": {"main": "Home & Kitchen", "sub": "Bathroom"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Baseball Glove",
        "sku": "SPO-BAS-5063",
        "price": Decimal128("45.00"),
        "details": {"description": "Synthetic leather mitt.", "specs": {"size": "12 inch", "hand": "Left throw"}},
        "stock": 50,
        "category": {"main": "Sports", "sub": "Baseball"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Psychology Textbook",
        "sku": "BOO-EDU-5064",
        "price": Decimal128("65.00"),
        "details": {"description": "Introduction to psychology.", "specs": {"edition": "10th", "pages": "700"}},
        "stock": 35,
        "category": {"main": "Books", "sub": "Education"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Thermal Leggings",
        "sku": "CLO-BOT-5065",
        "price": Decimal128("30.00"),
        "details": {"description": "Fleece lined leggings.", "specs": {"color": "Black", "stretch": "High"}},
        "stock": 85,
        "category": {"main": "Clothing", "sub": "Bottoms"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "SATA Cable",
        "sku": "ELE-ACC-5066",
        "price": Decimal128("5.00"),
        "details": {"description": "Hard drive data cable.", "specs": {"speed": "6Gbps", "connector": "Locking"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Computer Parts"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Chopsticks Set",
        "sku": "HOM-KIT-5067",
        "price": Decimal128("10.00"),
        "details": {"description": "Reusable wooden chopsticks.", "specs": {"pairs": "5", "design": "Printed"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Hiking Gaiters",
        "sku": "SPO-HIK-5068",
        "price": Decimal128("20.00"),
        "details": {"description": "Leg protection for trails.", "specs": {"waterproof": "Yes", "size": "Adjustable"}},
        "stock": 60,
        "category": {"main": "Sports", "sub": "Hiking"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "True Crime Book",
        "sku": "BOO-NON-5069",
        "price": Decimal128("16.00"),
        "details": {"description": "Investigative journalism.", "specs": {"author": "T. Capote", "pages": "300"}},
        "stock": 95,
        "category": {"main": "Books", "sub": "Non-Fiction"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Leather Gloves Men",
        "sku": "CLO-ACC-5070",
        "price": Decimal128("45.00"),
        "details": {"description": "Driving gloves leather.", "specs": {"color": "Black", "lining": "Unlined"}},
        "stock": 50,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "USB Fan Mini",
        "sku": "ELE-ACC-5071",
        "price": Decimal128("8.00"),
        "details": {"description": "Flexible USB fan.", "specs": {"blades": "Soft", "power": "Laptop"}},
        "stock": 180,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Cocktail Shaker",
        "sku": "HOM-KIT-5072",
        "price": Decimal128("18.00"),
        "details": {"description": "Stainless steel mixer.", "specs": {"capacity": "750ml", "strainer": "Built-in"}},
        "stock": 80,
        "category": {"main": "Home & Kitchen", "sub": "Barware"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Bike Pump Mini",
        "sku": "SPO-CYC-5073",
        "price": Decimal128("15.00"),
        "details": {"description": "Frame mounted pump.", "specs": {"valve": "Presta/Schrader", "psi": "100"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Cycling"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Self-Help Finance",
        "sku": "BOO-SEL-5074",
        "price": Decimal128("20.00"),
        "details": {"description": "Rich Dad Poor Dad.", "specs": {"author": "Kiyosaki", "topic": "Money"}},
        "stock": 110,
        "category": {"main": "Books", "sub": "Self-Help"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Visor Hat",
        "sku": "CLO-HAT-5075",
        "price": Decimal128("12.00"),
        "details": {"description": "Open top sun visor.", "specs": {"material": "Straw", "brim": "Wide"}},
        "stock": 75,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Ethernet Adapter USB",
        "sku": "ELE-NET-5076",
        "price": Decimal128("15.00"),
        "details": {"description": "USB 3.0 to RJ45 dongle.", "specs": {"speed": "Gigabit", "plug": "Play"}},
        "stock": 120,
        "category": {"main": "Electronics", "sub": "Adapters"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Placemats Cork",
        "sku": "HOM-DEC-5077",
        "price": Decimal128("14.00"),
        "details": {"description": "Eco friendly cork mats.", "specs": {"pack": "4", "shape": "Rectangular"}},
        "stock": 90,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Dumbbell Rack",
        "sku": "SPO-GYM-5078",
        "price": Decimal128("60.00"),
        "details": {"description": "A-frame weight stand.", "specs": {"capacity": "5 pairs", "material": "Steel"}},
        "stock": 25,
        "category": {"main": "Sports", "sub": "Equipment"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Spanish Novel",
        "sku": "BOO-FIC-5079",
        "price": Decimal128("16.00"),
        "details": {"description": "Don Quixote.", "specs": {"language": "Spanish", "pages": "800"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Foreign"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Suspenders Kids",
        "sku": "CLO-ACC-5080",
        "price": Decimal128("10.00"),
        "details": {"description": "Adjustable braces for children.", "specs": {"color": "Red", "clip": "Strong"}},
        "stock": 60,
        "category": {"main": "Clothing", "sub": "Kids"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Keyboard Wrist Rest",
        "sku": "ELE-ACC-5081",
        "price": Decimal128("15.00"),
        "details": {"description": "Gel pad for typing comfort.", "specs": {"base": "Rubber", "cover": "Fabric"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Milk Pitcher",
        "sku": "HOM-KIT-5082",
        "price": Decimal128("12.00"),
        "details": {"description": "Stainless steel frothing jug.", "specs": {"capacity": "350ml", "spout": "Pour"}},
        "stock": 85,
        "category": {"main": "Home & Kitchen", "sub": "Coffee"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Soccer Socks",
        "sku": "SPO-SOC-5083",
        "price": Decimal128("10.00"),
        "details": {"description": "Knee high sports socks.", "specs": {"cushion": "Foot", "color": "White"}},
        "stock": 150,
        "category": {"main": "Sports", "sub": "Apparel"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Fantasy Series Set",
        "sku": "BOO-FIC-5084",
        "price": Decimal128("40.00"),
        "details": {"description": "Box set of 3 books.", "specs": {"genre": "Fantasy", "cover": "Box"}},
        "stock": 30,
        "category": {"main": "Books", "sub": "Fantasy"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Bow Tie Silk",
        "sku": "CLO-ACC-5085",
        "price": Decimal128("20.00"),
        "details": {"description": "Pre-tied formal bow tie.", "specs": {"material": "Silk", "color": "Black"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "VGA Adapter HDMI",
        "sku": "ELE-ACC-5086",
        "price": Decimal128("12.00"),
        "details": {"description": "Convert VGA PC to HDMI TV.", "specs": {"audio": "Yes", "power": "USB"}},
        "stock": 110,
        "category": {"main": "Electronics", "sub": "Adapters"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Sink Caddy",
        "sku": "HOM-ORG-5087",
        "price": Decimal128("10.00"),
        "details": {"description": "Sponge holder for faucet.", "specs": {"drain": "Holes", "material": "Plastic"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Organization"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Billiard Chalk",
        "sku": "SPO-GAM-5088",
        "price": Decimal128("5.00"),
        "details": {"description": "Box of pool cue chalk.", "specs": {"count": "12", "color": "Blue"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Philosophy Essays",
        "sku": "BOO-PHI-5089",
        "price": Decimal128("18.00"),
        "details": {"description": "Collected works of Nietzsche.", "specs": {"pages": "300", "translator": "Various"}},
        "stock": 55,
        "category": {"main": "Books", "sub": "Philosophy"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Rain Poncho",
        "sku": "CLO-OUT-5090",
        "price": Decimal128("10.00"),
        "details": {"description": "Reusable emergency rain gear.", "specs": {"size": "One Size", "color": "Yellow"}},
        "stock": 250,
        "category": {"main": "Clothing", "sub": "Outerwear"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Coaxial Cable",
        "sku": "ELE-ACC-5091",
        "price": Decimal128("8.00"),
        "details": {"description": "RG6 cable for TV antenna.", "specs": {"length": "10ft", "connector": "F-Type"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Cables"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Fondue Set",
        "sku": "HOM-KIT-5092",
        "price": Decimal128("35.00"),
        "details": {"description": "Chocolate or cheese warmer.", "specs": {"pot": "Ceramic", "forks": "4"}},
        "stock": 40,
        "category": {"main": "Home & Kitchen", "sub": "Appliances"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Karate Belt",
        "sku": "SPO-MAR-5093",
        "price": Decimal128("8.00"),
        "details": {"description": "Cotton martial arts belt.", "specs": {"color": "White", "length": "280cm"}},
        "stock": 120,
        "category": {"main": "Sports", "sub": "Martial Arts"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Short Stories Horror",
        "sku": "BOO-FIC-5094",
        "price": Decimal128("14.00"),
        "details": {"description": "Lovecraft collection.", "specs": {"pages": "250", "cover": "Paperback"}},
        "stock": 80,
        "category": {"main": "Books", "sub": "Horror"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Thermal Vest",
        "sku": "CLO-UND-5095",
        "price": Decimal128("18.00"),
        "details": {"description": "Base layer sleeveless top.", "specs": {"material": "Cotton", "warmth": "Medium"}},
        "stock": 95,
        "category": {"main": "Clothing", "sub": "Underwear"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Optical Audio Cable",
        "sku": "ELE-AUD-5096",
        "price": Decimal128("10.00"),
        "details": {"description": "Toslink digital sound cable.", "specs": {"length": "1.5m", "tips": "Gold"}},
        "stock": 130,
        "category": {"main": "Electronics", "sub": "Cables"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Cheese Slicer",
        "sku": "HOM-KIT-5097",
        "price": Decimal128("12.00"),
        "details": {"description": "Wire cutter for cheese.", "specs": {"board": "Marble", "wire": "Steel"}},
        "stock": 70,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Medal Hanger",
        "sku": "SPO-ACC-5098",
        "price": Decimal128("20.00"),
        "details": {"description": "Wall display for awards.", "specs": {"material": "Steel", "bars": "3"}},
        "stock": 50,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Daily Planner",
        "sku": "BOO-STA-5099",
        "price": Decimal128("15.00"),
        "details": {"description": "Undated productivity journal.", "specs": {"layout": "Daily", "cover": "Hard"}},
        "stock": 110,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Shoe Horn",
        "sku": "CLO-ACC-5100",
        "price": Decimal128("5.00"),
        "details": {"description": "Long handled shoe helper.", "specs": {"length": "18 inch", "material": "Plastic"}},
        "stock": 200,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Smart Water Leak Sensor",
        "sku": "ELE-SMA-6001",
        "price": Decimal128("39.99"),
        "details": {"description": "WiFi detector for floods and leaks.", "specs": {"battery": "1 Year", "alert": "App"}},
        "stock": 80,
        "category": {"main": "Electronics", "sub": "Smart Home"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(2, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Ceramic Plant Pot",
        "sku": "HOM-GAR-6002",
        "price": Decimal128("18.00"),
        "details": {"description": "Minimalist white planter.", "specs": {"diameter": "8 inch", "drainage": "Yes"}},
        "stock": 120,
        "category": {"main": "Home & Kitchen", "sub": "Garden"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Pickleball Paddle Set",
        "sku": "SPO-GAM-6003",
        "price": Decimal128("55.00"),
        "details": {"description": "2 paddles and 4 balls.", "specs": {"core": "Honeycomb", "surface": "Graphite"}},
        "stock": 60,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Graphic Novel Noir",
        "sku": "BOO-COM-6004",
        "price": Decimal128("22.00"),
        "details": {"description": "Detective mystery comic.", "specs": {"pages": "180", "style": "B&W"}},
        "stock": 45,
        "category": {"main": "Books", "sub": "Comics"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(1, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Thermal Neck Gaiter",
        "sku": "CLO-ACC-6005",
        "price": Decimal128("12.00"),
        "details": {"description": "Fleece neck warmer.", "specs": {"material": "Polyester", "color": "Black"}},
        "stock": 150,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "USB Fingerprint Reader",
        "sku": "ELE-ACC-6006",
        "price": Decimal128("25.00"),
        "details": {"description": "Biometric scanner for PC.", "specs": {"speed": "0.15s", "os": "Windows"}},
        "stock": 90,
        "category": {"main": "Electronics", "sub": "Security"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Silicone Muffin Pan",
        "sku": "HOM-KIT-6007",
        "price": Decimal128("14.00"),
        "details": {"description": "Flexible non-stick baking mold.", "specs": {"cups": "12", "color": "Red"}},
        "stock": 110,
        "category": {"main": "Home & Kitchen", "sub": "Bakeware"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Agility Hurdles",
        "sku": "SPO-TRA-6008",
        "price": Decimal128("35.00"),
        "details": {"description": "Speed training hurdle set.", "specs": {"height": "6 inch", "count": "5"}},
        "stock": 40,
        "category": {"main": "Sports", "sub": "Training"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Investing for Beginners",
        "sku": "BOO-BUS-6009",
        "price": Decimal128("19.99"),
        "details": {"description": "Stock market basics.", "specs": {"pages": "250", "edition": "2024"}},
        "stock": 100,
        "category": {"main": "Books", "sub": "Business"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Canvas Tote Bag",
        "sku": "CLO-BAG-6010",
        "price": Decimal128("15.00"),
        "details": {"description": "Eco-friendly shopper.", "specs": {"print": "Botanical", "handles": "Cotton"}},
        "stock": 200,
        "category": {"main": "Clothing", "sub": "Bags"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Digital Voice Recorder",
        "sku": "ELE-AUD-6011",
        "price": Decimal128("40.00"),
        "details": {"description": "Portable audio recording device.", "specs": {"storage": "8GB", "mic": "Stereo"}},
        "stock": 55,
        "category": {"main": "Electronics", "sub": "Audio"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Bamboo Utensil Set",
        "sku": "HOM-KIT-6012",
        "price": Decimal128("12.00"),
        "details": {"description": "Eco cooking spoons.", "specs": {"pieces": "5", "holder": "Included"}},
        "stock": 130,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Cycling Shorts Padded",
        "sku": "SPO-CYC-6013",
        "price": Decimal128("30.00"),
        "details": {"description": "Bike shorts with gel cushion.", "specs": {"material": "Lycra", "padding": "3D Gel"}},
        "stock": 75,
        "category": {"main": "Sports", "sub": "Cycling"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Literature Set",
        "sku": "BOO-FIC-6014",
        "price": Decimal128("45.00"),
        "details": {"description": "Box set of Dickens novels.", "specs": {"books": "3", "cover": "Hardcover"}},
        "stock": 35,
        "category": {"main": "Books", "sub": "Classics"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Leather Dress Belt",
        "sku": "CLO-ACC-6015",
        "price": Decimal128("35.00"),
        "details": {"description": "Formal brown leather belt.", "specs": {"width": "1 inch", "buckle": "Gold"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Laptop Privacy Screen",
        "sku": "ELE-ACC-6016",
        "price": Decimal128("28.00"),
        "details": {"description": "Anti-glare privacy filter.", "specs": {"size": "14 inch", "finish": "Matte"}},
        "stock": 65,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Shower Curtain Liner",
        "sku": "HOM-BAT-6017",
        "price": Decimal128("8.00"),
        "details": {"description": "Mildew resistant liner.", "specs": {"material": "PEVA", "magnets": "3"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Bathroom"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Dumbbell Neoprene 3kg",
        "sku": "SPO-GYM-6018",
        "price": Decimal128("12.00"),
        "details": {"description": "Coated hand weight.", "specs": {"weight": "3kg", "color": "Blue"}},
        "stock": 140,
        "category": {"main": "Sports", "sub": "Weights"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Travel Guide France",
        "sku": "BOO-TRA-6019",
        "price": Decimal128("24.00"),
        "details": {"description": "Paris and Provence guide.", "specs": {"pages": "350", "maps": "Fold-out"}},
        "stock": 70,
        "category": {"main": "Books", "sub": "Travel"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Sun Hat Wide Brim",
        "sku": "CLO-HAT-6020",
        "price": Decimal128("18.00"),
        "details": {"description": "UV protection beach hat.", "specs": {"material": "Straw", "upf": "50+"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "USB C Hub 5-in-1",
        "sku": "ELE-ACC-6021",
        "price": Decimal128("35.00"),
        "details": {"description": "Multiport adapter.", "specs": {"ports": "HDMI, USB, SD", "material": "Alloy"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(4, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Pillow Protectors",
        "sku": "HOM-BED-6022",
        "price": Decimal128("15.00"),
        "details": {"description": "Zippered pillow covers.", "specs": {"pack": "2", "fabric": "Cotton"}},
        "stock": 160,
        "category": {"main": "Home & Kitchen", "sub": "Bedding"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Yoga Mat Strap",
        "sku": "SPO-YOG-6023",
        "price": Decimal128("8.00"),
        "details": {"description": "Carrying sling for mats.", "specs": {"material": "Cotton", "adjustable": "Yes"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Yoga"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Biology Textbook",
        "sku": "BOO-SCI-6024",
        "price": Decimal128("75.00"),
        "details": {"description": "Molecular biology basics.", "specs": {"pages": "800", "edition": "5th"}},
        "stock": 25,
        "category": {"main": "Books", "sub": "Education"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Running Socks No-Show",
        "sku": "CLO-ACC-6025",
        "price": Decimal128("14.00"),
        "details": {"description": "Anti-blister athletic socks.", "specs": {"pack": "3", "material": "Synthetic"}},
        "stock": 180,
        "category": {"main": "Clothing", "sub": "Socks"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Bluetooth Mouse",
        "sku": "ELE-MOU-6026",
        "price": Decimal128("20.00"),
        "details": {"description": "Silent click wireless mouse.", "specs": {"dpi": "1600", "battery": "AA"}},
        "stock": 130,
        "category": {"main": "Electronics", "sub": "Peripherals"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(2, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Closet Organizer",
        "sku": "HOM-STO-6027",
        "price": Decimal128("18.00"),
        "details": {"description": "Hanging shelves for clothes.", "specs": {"shelves": "5", "material": "Fabric"}},
        "stock": 95,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Resistance Loop Set",
        "sku": "SPO-FIT-6028",
        "price": Decimal128("12.00"),
        "details": {"description": "Latex mini bands.", "specs": {"levels": "Light-Heavy", "count": "4"}},
        "stock": 220,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Poetry Collection",
        "sku": "BOO-POE-6029",
        "price": Decimal128("16.00"),
        "details": {"description": "Nature poems anthology.", "specs": {"author": "Mary Oliver", "pages": "150"}},
        "stock": 50,
        "category": {"main": "Books", "sub": "Poetry"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Denim Shorts",
        "sku": "CLO-BOT-6030",
        "price": Decimal128("28.00"),
        "details": {"description": "High waisted jean shorts.", "specs": {"wash": "Vintage", "hem": "Frayed"}},
        "stock": 85,
        "category": {"main": "Clothing", "sub": "Bottoms"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Cable Organizer Box",
        "sku": "ELE-ORG-6031",
        "price": Decimal128("18.00"),
        "details": {"description": "Hide power strips and cords.", "specs": {"size": "Large", "color": "Black"}},
        "stock": 110,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Ice Cream Scoop",
        "sku": "HOM-KIT-6032",
        "price": Decimal128("10.00"),
        "details": {"description": "Trigger release scooper.", "specs": {"material": "Steel", "handle": "Rubber"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Swimming Caps Pack",
        "sku": "SPO-SWI-6033",
        "price": Decimal128("15.00"),
        "details": {"description": "Silicone swim caps.", "specs": {"count": "2", "colors": "Blue/Black"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Swimming"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Sci-Fi Short Stories",
        "sku": "BOO-FIC-6034",
        "price": Decimal128("14.00"),
        "details": {"description": "Future dystopia tales.", "specs": {"editor": "Various", "pages": "280"}},
        "stock": 65,
        "category": {"main": "Books", "sub": "Sci-Fi"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Gym Tank Top",
        "sku": "CLO-TOP-6035",
        "price": Decimal128("20.00"),
        "details": {"description": "Racerback workout tank.", "specs": {"material": "Moisture Wick", "color": "Pink"}},
        "stock": 120,
        "category": {"main": "Clothing", "sub": "Activewear"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Screen Cleaning Spray",
        "sku": "ELE-CLN-6036",
        "price": Decimal128("8.00"),
        "details": {"description": "Monitor and phone cleaner.", "specs": {"volume": "250ml", "cloth": "Included"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Cleaning"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Cork Coasters",
        "sku": "HOM-DEC-6037",
        "price": Decimal128("9.00"),
        "details": {"description": "Round cork drink mats.", "specs": {"pack": "6", "absorbent": "Yes"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Wrist Sweatbands",
        "sku": "SPO-ACC-6038",
        "price": Decimal128("6.00"),
        "details": {"description": "Cotton terry wristbands.", "specs": {"pair": "1", "color": "White"}},
        "stock": 300,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "World Atlas",
        "sku": "BOO-REF-6039",
        "price": Decimal128("30.00"),
        "details": {"description": "Illustrated geographical maps.", "specs": {"format": "Hardcover", "size": "Large"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Reference"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Beanie Hat",
        "sku": "CLO-HAT-6040",
        "price": Decimal128("16.00"),
        "details": {"description": "Slouchy knit winter hat.", "specs": {"material": "Acrylic", "color": "Grey"}},
        "stock": 130,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Phone Stand Adjustable",
        "sku": "ELE-ACC-6041",
        "price": Decimal128("12.00"),
        "details": {"description": "Foldable desktop holder.", "specs": {"material": "Plastic", "color": "White"}},
        "stock": 160,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Vegetable Steamer",
        "sku": "HOM-KIT-6042",
        "price": Decimal128("14.00"),
        "details": {"description": "Stainless steel basket.", "specs": {"expandable": "Yes", "feet": "Silicone"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Jump Rope Speed",
        "sku": "SPO-FIT-6043",
        "price": Decimal128("10.00"),
        "details": {"description": "Wire cable skipping rope.", "specs": {"bearing": "Ball", "adjust": "Screw"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Self-Help Journal",
        "sku": "BOO-SEL-6044",
        "price": Decimal128("18.00"),
        "details": {"description": "Daily mindfulness planner.", "specs": {"pages": "180", "cover": "Fabric"}},
        "stock": 90,
        "category": {"main": "Books", "sub": "Self-Help"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Polo Shirt",
        "sku": "CLO-TOP-6045",
        "price": Decimal128("30.00"),
        "details": {"description": "Cotton pique polo.", "specs": {"color": "Red", "fit": "Regular"}},
        "stock": 115,
        "category": {"main": "Clothing", "sub": "Tops"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Extension Cord",
        "sku": "ELE-ACC-6046",
        "price": Decimal128("15.00"),
        "details": {"description": "Power strip 3 outlets.", "specs": {"length": "3m", "switch": "Yes"}},
        "stock": 140,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Jar Opener",
        "sku": "HOM-KIT-6047",
        "price": Decimal128("8.00"),
        "details": {"description": "Rubber grip pad.", "specs": {"pack": "3", "colors": "Mixed"}},
        "stock": 190,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Hand Grip",
        "sku": "SPO-FIT-6048",
        "price": Decimal128("9.00"),
        "details": {"description": "Forearm strengthener.", "specs": {"resistance": "Adjustable", "color": "Black"}},
        "stock": 150,
        "category": {"main": "Sports", "sub": "Training"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Plays",
        "sku": "BOO-FIC-6049",
        "price": Decimal128("16.00"),
        "details": {"description": "Shakespeare tragedies.", "specs": {"plays": "Hamlet, Macbeth", "cover": "Paperback"}},
        "stock": 55,
        "category": {"main": "Books", "sub": "Classics"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Leather Wallet",
        "sku": "CLO-ACC-6050",
        "price": Decimal128("32.00"),
        "details": {"description": "Bifold men's wallet.", "specs": {"slots": "6", "color": "Black"}},
        "stock": 80,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "HDMI Switch 3-Port",
        "sku": "ELE-ACC-6051",
        "price": Decimal128("18.00"),
        "details": {"description": "4K video switcher.", "specs": {"remote": "IR", "ports": "3 In 1 Out"}},
        "stock": 95,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Butter Dish Glass",
        "sku": "HOM-KIT-6052",
        "price": Decimal128("15.00"),
        "details": {"description": "Clear glass butter keeper.", "specs": {"lid": "Included", "size": "Stick"}},
        "stock": 70,
        "category": {"main": "Home & Kitchen", "sub": "Tableware"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Reflective Vest",
        "sku": "SPO-RUN-6053",
        "price": Decimal128("12.00"),
        "details": {"description": "Safety gear for night running.", "specs": {"size": "Adjustable", "color": "Yellow"}},
        "stock": 130,
        "category": {"main": "Sports", "sub": "Running"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "French Dictionary",
        "sku": "BOO-REF-6054",
        "price": Decimal128("12.00"),
        "details": {"description": "Pocket language guide.", "specs": {"words": "30000", "binding": "Flexi"}},
        "stock": 105,
        "category": {"main": "Books", "sub": "Reference"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Bucket Hat Denim",
        "sku": "CLO-HAT-6055",
        "price": Decimal128("18.00"),
        "details": {"description": "Casual jean sun hat.", "specs": {"wash": "Light", "brim": "Short"}},
        "stock": 60,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Laptop Cooling Pad",
        "sku": "ELE-ACC-6056",
        "price": Decimal128("22.00"),
        "details": {"description": "Dual fan cooler stand.", "specs": {"usb": "Powered", "led": "Blue"}},
        "stock": 85,
        "category": {"main": "Electronics", "sub": "Computer Accessories"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Can Opener Manual",
        "sku": "HOM-KIT-6057",
        "price": Decimal128("10.00"),
        "details": {"description": "Smooth edge safety opener.", "specs": {"handle": "Ergonomic", "blade": "Steel"}},
        "stock": 150,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Mouthguard Case",
        "sku": "SPO-ACC-6058",
        "price": Decimal128("5.00"),
        "details": {"description": "Vented storage box.", "specs": {"color": "Clear", "material": "Plastic"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Art History Basics",
        "sku": "BOO-ART-6059",
        "price": Decimal128("25.00"),
        "details": {"description": "Guide to major movements.", "specs": {"pages": "300", "images": "Color"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Silk Tie",
        "sku": "CLO-ACC-6060",
        "price": Decimal128("25.00"),
        "details": {"description": "Formal business necktie.", "specs": {"pattern": "Striped", "width": "3 inch"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Micro USB Cable",
        "sku": "ELE-ACC-6061",
        "price": Decimal128("8.00"),
        "details": {"description": "Charging cord 6ft.", "specs": {"pack": "2", "jacket": "Nylon"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Cables"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Tea Infuser Ball",
        "sku": "HOM-KIT-6062",
        "price": Decimal128("6.00"),
        "details": {"description": "Mesh strainer for loose leaf.", "specs": {"material": "Steel", "chain": "Yes"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Tea"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Whistle Lanyard",
        "sku": "SPO-TRA-6063",
        "price": Decimal128("5.00"),
        "details": {"description": "Coach sports whistle.", "specs": {"sound": "Crisp", "material": "Metal"}},
        "stock": 220,
        "category": {"main": "Sports", "sub": "Training"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Philosophy 101",
        "sku": "BOO-PHI-6064",
        "price": Decimal128("18.00"),
        "details": {"description": "Intro to western thought.", "specs": {"author": "Various", "pages": "250"}},
        "stock": 75,
        "category": {"main": "Books", "sub": "Philosophy"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Crew Socks Pack",
        "sku": "CLO-ACC-6065",
        "price": Decimal128("15.00"),
        "details": {"description": "Cotton everyday socks.", "specs": {"count": "5", "color": "White"}},
        "stock": 160,
        "category": {"main": "Clothing", "sub": "Socks"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "VGA Cable",
        "sku": "ELE-ACC-6066",
        "price": Decimal128("10.00"),
        "details": {"description": "Video cable for monitors.", "specs": {"length": "1.8m", "pins": "15"}},
        "stock": 110,
        "category": {"main": "Electronics", "sub": "Cables"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Sink Strainer",
        "sku": "HOM-KIT-6067",
        "price": Decimal128("7.00"),
        "details": {"description": "Mesh drain filter.", "specs": {"pack": "2", "rim": "Wide"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Sink"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Ball Pump Needle",
        "sku": "SPO-ACC-6068",
        "price": Decimal128("4.00"),
        "details": {"description": "Inflation pins set.", "specs": {"count": "5", "fit": "Universal"}},
        "stock": 350,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Short Stories Collection",
        "sku": "BOO-FIC-6069",
        "price": Decimal128("14.00"),
        "details": {"description": "Modern literary fiction.", "specs": {"editor": "Best American", "pages": "300"}},
        "stock": 50,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Fingerless Gloves",
        "sku": "CLO-ACC-6070",
        "price": Decimal128("10.00"),
        "details": {"description": "Knit gloves for typing.", "specs": {"material": "Acrylic", "color": "Grey"}},
        "stock": 130,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Mouse Pad Basic",
        "sku": "ELE-ACC-6071",
        "price": Decimal128("6.00"),
        "details": {"description": "Cloth surface mouse mat.", "specs": {"base": "Rubber", "color": "Blue"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Peripherals"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Pizza Cutter",
        "sku": "HOM-KIT-6072",
        "price": Decimal128("9.00"),
        "details": {"description": "Stainless steel wheel slicer.", "specs": {"guard": "Finger", "handle": "Plastic"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Tennis Balls",
        "sku": "SPO-TEN-6073",
        "price": Decimal128("8.00"),
        "details": {"description": "Pressureless practice balls.", "specs": {"pack": "3", "bag": "Mesh"}},
        "stock": 220,
        "category": {"main": "Sports", "sub": "Tennis"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Pocket Dictionary",
        "sku": "BOO-REF-6074",
        "price": Decimal128("7.00"),
        "details": {"description": "English definitions.", "specs": {"size": "Small", "pages": "400"}},
        "stock": 170,
        "category": {"main": "Books", "sub": "Reference"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Shoe Horn",
        "sku": "CLO-ACC-6075",
        "price": Decimal128("5.00"),
        "details": {"description": "Plastic long handle helper.", "specs": {"length": "15 inch", "color": "Black"}},
        "stock": 250,
        "category": {"main": "Clothing", "sub": "Shoe Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "USB Fan",
        "sku": "ELE-ACC-6076",
        "price": Decimal128("9.00"),
        "details": {"description": "Flexible neck mini fan.", "specs": {"power": "USB A", "blades": "Soft"}},
        "stock": 190,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Bottle Brush",
        "sku": "HOM-CLN-6077",
        "price": Decimal128("6.00"),
        "details": {"description": "Long handle cleaning brush.", "specs": {"bristles": "Nylon", "neck": "Flexible"}},
        "stock": 160,
        "category": {"main": "Home & Kitchen", "sub": "Cleaning"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Ping Pong Balls",
        "sku": "SPO-GAM-6078",
        "price": Decimal128("5.00"),
        "details": {"description": "Table tennis training balls.", "specs": {"pack": "6", "color": "Orange"}},
        "stock": 300,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Notebook Spiral",
        "sku": "BOO-STA-6079",
        "price": Decimal128("4.00"),
        "details": {"description": "College ruled paper.", "specs": {"pages": "70", "size": "A4"}},
        "stock": 400,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Bandana Red",
        "sku": "CLO-ACC-6080",
        "price": Decimal128("4.00"),
        "details": {"description": "Cotton paisley square.", "specs": {"size": "22x22", "hem": "Stitched"}},
        "stock": 350,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Phone Charging Cable",
        "sku": "ELE-ACC-6081",
        "price": Decimal128("7.00"),
        "details": {"description": "Lightning connector cord.", "specs": {"length": "1m", "mfi": "Certified"}},
        "stock": 220,
        "category": {"main": "Electronics", "sub": "Cables"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Vegetable Peeler",
        "sku": "HOM-KIT-6082",
        "price": Decimal128("6.00"),
        "details": {"description": "Swivel blade potato peeler.", "specs": {"blade": "Carbon Steel", "tip": "Point"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Mouthguard",
        "sku": "SPO-PRO-6083",
        "price": Decimal128("5.00"),
        "details": {"description": "Boil and bite gum shield.", "specs": {"size": "Adult", "case": "No"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Protection"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Sketchpad",
        "sku": "BOO-ART-6084",
        "price": Decimal128("8.00"),
        "details": {"description": "Blank drawing paper.", "specs": {"sheets": "50", "weight": "90gsm"}},
        "stock": 120,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Shoelaces White",
        "sku": "CLO-ACC-6085",
        "price": Decimal128("3.00"),
        "details": {"description": "Flat athletic laces.", "specs": {"length": "45 inch", "pair": "1"}},
        "stock": 500,
        "category": {"main": "Clothing", "sub": "Shoe Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Cable Ties Velcro",
        "sku": "ELE-ORG-6086",
        "price": Decimal128("5.00"),
        "details": {"description": "Reusable wire straps.", "specs": {"pack": "10", "color": "Multi"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Measuring Spoons",
        "sku": "HOM-KIT-6087",
        "price": Decimal128("5.00"),
        "details": {"description": "Plastic spoon set.", "specs": {"count": "5", "ring": "Yes"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Golf Tees",
        "sku": "SPO-GOL-6088",
        "price": Decimal128("4.00"),
        "details": {"description": "Wooden tees pack.", "specs": {"count": "20", "length": "2 inch"}},
        "stock": 400,
        "category": {"main": "Sports", "sub": "Golf"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Crossword Book",
        "sku": "BOO-GAM-6089",
        "price": Decimal128("6.00"),
        "details": {"description": "Easy puzzle collection.", "specs": {"pages": "100", "paper": "Newsprint"}},
        "stock": 150,
        "category": {"main": "Books", "sub": "Games"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Hair Ties",
        "sku": "CLO-ACC-6090",
        "price": Decimal128("3.00"),
        "details": {"description": "Elastic ponytail holders.", "specs": {"pack": "10", "metal_free": "Yes"}},
        "stock": 600,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Stylus Nibs",
        "sku": "ELE-ACC-6091",
        "price": Decimal128("8.00"),
        "details": {"description": "Replacement tips.", "specs": {"pack": "3", "soft": "Yes"}},
        "stock": 120,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Pot Scraper",
        "sku": "HOM-CLN-6092",
        "price": Decimal128("3.00"),
        "details": {"description": "Plastic food remover.", "specs": {"corners": "Different", "safe": "Non-stick"}},
        "stock": 250,
        "category": {"main": "Home & Kitchen", "sub": "Cleaning"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Ball Needle",
        "sku": "SPO-ACC-6093",
        "price": Decimal128("2.00"),
        "details": {"description": "Pump inflation pin.", "specs": {"pack": "2", "metal": "Steel"}},
        "stock": 500,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Coloring Book",
        "sku": "BOO-KID-6094",
        "price": Decimal128("5.00"),
        "details": {"description": "Animals to color.", "specs": {"pages": "40", "age": "4+"}},
        "stock": 180,
        "category": {"main": "Books", "sub": "Children"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "No-Show Socks",
        "sku": "CLO-ACC-6095",
        "price": Decimal128("5.00"),
        "details": {"description": "Single pair liner socks.", "specs": {"color": "Black", "silicone": "Grip"}},
        "stock": 300,
        "category": {"main": "Clothing", "sub": "Socks"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Webcam Cover",
        "sku": "ELE-ACC-6096",
        "price": Decimal128("4.00"),
        "details": {"description": "Privacy slider.", "specs": {"pack": "1", "adhesive": "Yes"}},
        "stock": 400,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Bag Clip",
        "sku": "HOM-STO-6097",
        "price": Decimal128("3.00"),
        "details": {"description": "Food freshness sealer.", "specs": {"size": "Large", "spring": "Strong"}},
        "stock": 350,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Whistle",
        "sku": "SPO-ACC-6098",
        "price": Decimal128("3.00"),
        "details": {"description": "Basic plastic whistle.", "specs": {"color": "Red", "pea": "Cork"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Mini Notebook",
        "sku": "BOO-STA-6099",
        "price": Decimal128("2.00"),
        "details": {"description": "Pocket size jotter.", "specs": {"pages": "48", "ruled": "Yes"}},
        "stock": 500,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(5, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Fabric Patch",
        "sku": "CLO-ACC-6100",
        "price": Decimal128("2.00"),
        "details": {"description": "Iron-on repair patch.", "specs": {"color": "Denim", "size": "3x4"}},
        "stock": 450,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(1, 2)
    },
    {
        "_id": ObjectId(),
        "name": "Smart Door Lock",
        "sku": "ELE-SMA-7001",
        "price": Decimal128("150.00"),
        "details": {"description": "Keyless entry deadbolt.", "specs": {"access": "Code/App", "finish": "Nickel"}},
        "stock": 40,
        "category": {"main": "Electronics", "sub": "Smart Home"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Wok Pan Carbon Steel",
        "sku": "HOM-CKW-7002",
        "price": Decimal128("35.00"),
        "details": {"description": "Traditional stir fry pan.", "specs": {"diameter": "14 inch", "handle": "Wood"}},
        "stock": 85,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Medicine Ball 5kg",
        "sku": "SPO-FIT-7003",
        "price": Decimal128("40.00"),
        "details": {"description": "Weighted ball for training.", "specs": {"weight": "5kg", "grip": "Texture"}},
        "stock": 60,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Satire Book",
        "sku": "BOO-FIC-7004",
        "price": Decimal128("14.00"),
        "details": {"description": "Animal Farm by Orwell.", "specs": {"pages": "120", "cover": "Paperback"}},
        "stock": 150,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(5, 20)
    },
    {
        "_id": ObjectId(),
        "name": "Linen Trousers",
        "sku": "CLO-BOT-7005",
        "price": Decimal128("45.00"),
        "details": {"description": "Lightweight summer pants.", "specs": {"material": "Linen", "color": "Beige"}},
        "stock": 70,
        "category": {"main": "Clothing", "sub": "Bottoms"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "USB C Docking Station",
        "sku": "ELE-ACC-7006",
        "price": Decimal128("80.00"),
        "details": {"description": "Laptop dual monitor dock.", "specs": {"ports": "10", "power": "100W"}},
        "stock": 55,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Dish Scrub Brush",
        "sku": "HOM-CLN-7007",
        "price": Decimal128("6.00"),
        "details": {"description": "Bamboo handle brush.", "specs": {"bristles": "Natural", "head": "Replaceable"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Cleaning"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Hiking Backpack 40L",
        "sku": "SPO-HIK-7008",
        "price": Decimal128("75.00"),
        "details": {"description": "Daypack with rain cover.", "specs": {"capacity": "40L", "frame": "Internal"}},
        "stock": 45,
        "category": {"main": "Sports", "sub": "Hiking"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Cybersecurity Handbook",
        "sku": "BOO-TEC-7009",
        "price": Decimal128("50.00"),
        "details": {"description": "Network security basics.", "specs": {"pages": "450", "edition": "2nd"}},
        "stock": 35,
        "category": {"main": "Books", "sub": "Technical"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Compression Shirt",
        "sku": "CLO-ACT-7010",
        "price": Decimal128("25.00"),
        "details": {"description": "Tight fit base layer.", "specs": {"sleeve": "Long", "color": "Black"}},
        "stock": 120,
        "category": {"main": "Clothing", "sub": "Activewear"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Gaming Mouse White",
        "sku": "ELE-GAM-7011",
        "price": Decimal128("45.00"),
        "details": {"description": "RGB lightweight mouse.", "specs": {"dpi": "12000", "buttons": "6"}},
        "stock": 90,
        "category": {"main": "Electronics", "sub": "Gaming"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Paper Napkins Pack",
        "sku": "HOM-KIT-7012",
        "price": Decimal128("5.00"),
        "details": {"description": "3-ply dinner napkins.", "specs": {"count": "50", "color": "White"}},
        "stock": 300,
        "category": {"main": "Home & Kitchen", "sub": "Tableware"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Yoga Wheel",
        "sku": "SPO-YOG-7013",
        "price": Decimal128("22.00"),
        "details": {"description": "Back pain relief wheel.", "specs": {"diameter": "12 inch", "padding": "Foam"}},
        "stock": 75,
        "category": {"main": "Sports", "sub": "Yoga"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Cookbook Baking",
        "sku": "BOO-COO-7014",
        "price": Decimal128("28.00"),
        "details": {"description": "The art of pastry.", "specs": {"recipes": "80", "photos": "Color"}},
        "stock": 65,
        "category": {"main": "Books", "sub": "Cooking"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Baseball Cap Mesh",
        "sku": "CLO-HAT-7015",
        "price": Decimal128("15.00"),
        "details": {"description": "Trucker style summer hat.", "specs": {"back": "Snap", "color": "Blue"}},
        "stock": 130,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Monitor Arm Single",
        "sku": "ELE-ACC-7016",
        "price": Decimal128("35.00"),
        "details": {"description": "Gas spring desk mount.", "specs": {"vesa": "100x100", "size": "17-32"}},
        "stock": 80,
        "category": {"main": "Electronics", "sub": "Office Electronics"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Ice Cream Molds",
        "sku": "HOM-KIT-7017",
        "price": Decimal128("12.00"),
        "details": {"description": "Silicone popsicle maker.", "specs": {"count": "6", "sticks": "Reusable"}},
        "stock": 110,
        "category": {"main": "Home & Kitchen", "sub": "Kitchenware"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Golf Glove Left",
        "sku": "SPO-GOL-7018",
        "price": Decimal128("12.00"),
        "details": {"description": "Synthetic grip glove.", "specs": {"hand": "Left", "size": "L"}},
        "stock": 95,
        "category": {"main": "Sports", "sub": "Golf"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Travel Guide USA",
        "sku": "BOO-TRA-7019",
        "price": Decimal128("25.00"),
        "details": {"description": "National Parks guide.", "specs": {"pages": "500", "maps": "Trail"}},
        "stock": 50,
        "category": {"main": "Books", "sub": "Travel"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(3, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Wrap Dress",
        "sku": "CLO-DRE-7020",
        "price": Decimal128("55.00"),
        "details": {"description": "Floral midi wrap dress.", "specs": {"material": "Viscose", "sleeve": "Short"}},
        "stock": 60,
        "category": {"main": "Clothing", "sub": "Dresses"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(4, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Bluetooth Adapter PC",
        "sku": "ELE-ACC-7021",
        "price": Decimal128("10.00"),
        "details": {"description": "USB Bluetooth 5.0 dongle.", "specs": {"range": "20m", "os": "Windows"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Adapters"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Bed Sheets Twin",
        "sku": "HOM-BED-7022",
        "price": Decimal128("25.00"),
        "details": {"description": "Microfiber sheet set.", "specs": {"size": "Twin", "color": "Grey"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Bedding"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Swim Goggles Kids",
        "sku": "SPO-SWI-7023",
        "price": Decimal128("15.00"),
        "details": {"description": "Colorful anti-fog goggles.", "specs": {"age": "6-12", "strap": "Silicone"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Swimming"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Philosophy Ethics",
        "sku": "BOO-PHI-7024",
        "price": Decimal128("22.00"),
        "details": {"description": "Moral philosophy intro.", "specs": {"pages": "280", "cover": "Soft"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Philosophy"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Hair Clips",
        "sku": "CLO-ACC-7025",
        "price": Decimal128("5.00"),
        "details": {"description": "Metal snap hair clips.", "specs": {"pack": "12", "color": "Black"}},
        "stock": 400,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Ethernet Cable 5m",
        "sku": "ELE-NET-7026",
        "price": Decimal128("8.00"),
        "details": {"description": "Cat6 internet patch cord.", "specs": {"length": "5m", "color": "Blue"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Cables"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Fridge Organizer",
        "sku": "HOM-STO-7027",
        "price": Decimal128("15.00"),
        "details": {"description": "Clear plastic bin.", "specs": {"handle": "Cutout", "size": "Medium"}},
        "stock": 160,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Tennis Balls Pressureless",
        "sku": "SPO-TEN-7028",
        "price": Decimal128("15.00"),
        "details": {"description": "Bucket of practice balls.", "specs": {"count": "12", "bag": "Yes"}},
        "stock": 80,
        "category": {"main": "Sports", "sub": "Tennis"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Journal Dotted",
        "sku": "BOO-STA-7029",
        "price": Decimal128("12.00"),
        "details": {"description": "Bullet journal notebook.", "specs": {"dots": "Grid", "paper": "Cream"}},
        "stock": 200,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Cotton Briefs",
        "sku": "CLO-UND-7030",
        "price": Decimal128("18.00"),
        "details": {"description": "Men's underwear pack.", "specs": {"count": "3", "waist": "Elastic"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Underwear"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Phone Tripod Mount",
        "sku": "ELE-ACC-7031",
        "price": Decimal128("8.00"),
        "details": {"description": "Smartphone clamp for tripods.", "specs": {"thread": "1/4", "width": "Adjustable"}},
        "stock": 180,
        "category": {"main": "Electronics", "sub": "Camera Accessories"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Dish Drying Mat",
        "sku": "HOM-KIT-7032",
        "price": Decimal128("10.00"),
        "details": {"description": "Microfiber absorbent mat.", "specs": {"size": "18x24", "color": "Grey"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Kitchenware"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Bike Water Bottle Cage",
        "sku": "SPO-CYC-7033",
        "price": Decimal128("8.00"),
        "details": {"description": "Aluminum bottle holder.", "specs": {"weight": "Light", "screws": "Included"}},
        "stock": 220,
        "category": {"main": "Sports", "sub": "Cycling"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Mystery",
        "sku": "BOO-FIC-7034",
        "price": Decimal128("12.00"),
        "details": {"description": "Agatha Christie novel.", "specs": {"title": "Orient Express", "cover": "Paperback"}},
        "stock": 95,
        "category": {"main": "Books", "sub": "Fiction"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Leather Keychain",
        "sku": "CLO-ACC-7035",
        "price": Decimal128("10.00"),
        "details": {"description": "Key fob loop.", "specs": {"material": "Leather", "ring": "Steel"}},
        "stock": 170,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Car Charger USB-C",
        "sku": "ELE-CAR-7036",
        "price": Decimal128("15.00"),
        "details": {"description": "Fast charging car plug.", "specs": {"ports": "2", "output": "30W"}},
        "stock": 130,
        "category": {"main": "Electronics", "sub": "Car Electronics"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Reusable Straws",
        "sku": "HOM-KIT-7037",
        "price": Decimal128("8.00"),
        "details": {"description": "Stainless steel straws set.", "specs": {"count": "4", "brush": "Yes"}},
        "stock": 350,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Stopwatch Mechanical",
        "sku": "SPO-ACC-7038",
        "price": Decimal128("35.00"),
        "details": {"description": "Analog track timer.", "specs": {"wind": "Manual", "case": "Metal"}},
        "stock": 30,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Poetry Modern",
        "sku": "BOO-POE-7039",
        "price": Decimal128("16.00"),
        "details": {"description": "Milk and Honey.", "specs": {"author": "Rupi Kaur", "pages": "200"}},
        "stock": 120,
        "category": {"main": "Books", "sub": "Poetry"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Sports Headband",
        "sku": "CLO-ACC-7040",
        "price": Decimal128("8.00"),
        "details": {"description": "Non-slip hair band.", "specs": {"silicone": "Grip", "color": "Pink"}},
        "stock": 250,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Hard Drive Case",
        "sku": "ELE-ACC-7041",
        "price": Decimal128("10.00"),
        "details": {"description": "Protective bag for HDD.", "specs": {"size": "2.5 inch", "shell": "Hard"}},
        "stock": 160,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Measuring Cups Metal",
        "sku": "HOM-KIT-7042",
        "price": Decimal128("18.00"),
        "details": {"description": "Heavy duty cups set.", "specs": {"material": "Steel", "count": "4"}},
        "stock": 90,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Whistle Plastic",
        "sku": "SPO-ACC-7043",
        "price": Decimal128("3.00"),
        "details": {"description": "Referee whistle.", "specs": {"color": "Black", "lanyard": "No"}},
        "stock": 500,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Chess Strategy Book",
        "sku": "BOO-GAM-7044",
        "price": Decimal128("20.00"),
        "details": {"description": "Mastering the middlegame.", "specs": {"level": "Intermediate", "pages": "300"}},
        "stock": 50,
        "category": {"main": "Books", "sub": "Games"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Canvas Belt",
        "sku": "CLO-ACC-7045",
        "price": Decimal128("12.00"),
        "details": {"description": "Military style web belt.", "specs": {"buckle": "Slide", "color": "Olive"}},
        "stock": 140,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Cable Sleeves",
        "sku": "ELE-ORG-7046",
        "price": Decimal128("12.00"),
        "details": {"description": "Zippered cord covers.", "specs": {"length": "50cm", "pack": "4"}},
        "stock": 110,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Oven Mitt Single",
        "sku": "HOM-KIT-7047",
        "price": Decimal128("8.00"),
        "details": {"description": "Quilted cotton mitt.", "specs": {"color": "Black", "heat": "400F"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Linens"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Soccer Ball Size 4",
        "sku": "SPO-SOC-7048",
        "price": Decimal128("20.00"),
        "details": {"description": "Youth training ball.", "specs": {"stitch": "Machine", "color": "White/Red"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Soccer"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Sketchbook A5",
        "sku": "BOO-ART-7049",
        "price": Decimal128("10.00"),
        "details": {"description": "Small drawing pad.", "specs": {"cover": "Hard", "sheets": "80"}},
        "stock": 130,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Shoe Laces Flat",
        "sku": "CLO-ACC-7050",
        "price": Decimal128("4.00"),
        "details": {"description": "Replacement sneaker laces.", "specs": {"color": "Blue", "length": "54 inch"}},
        "stock": 300,
        "category": {"main": "Clothing", "sub": "Shoe Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(2, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Cable Clips Desk",
        "sku": "ELE-ORG-7051",
        "price": Decimal128("6.00"),
        "details": {"description": "Adhesive wire drops.", "specs": {"pack": "6", "color": "White"}},
        "stock": 400,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Spatula Silicone",
        "sku": "HOM-KIT-7052",
        "price": Decimal128("7.00"),
        "details": {"description": "Heat resistant scraper.", "specs": {"core": "Steel", "color": "Green"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Badminton Shuttle",
        "sku": "SPO-BAD-7053",
        "price": Decimal128("2.00"),
        "details": {"description": "Single nylon birdie.", "specs": {"speed": "Slow", "color": "White"}},
        "stock": 600,
        "category": {"main": "Sports", "sub": "Badminton"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Notebook Pocket",
        "sku": "BOO-STA-7054",
        "price": Decimal128("3.00"),
        "details": {"description": "Mini jotter pad.", "specs": {"size": "A6", "pages": "48"}},
        "stock": 350,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Hair Pins",
        "sku": "CLO-ACC-7055",
        "price": Decimal128("2.00"),
        "details": {"description": "Bobby pins pack.", "specs": {"count": "50", "color": "Black"}},
        "stock": 800,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "USB Dust Plugs",
        "sku": "ELE-ACC-7056",
        "price": Decimal128("4.00"),
        "details": {"description": "Port covers for laptop.", "specs": {"pack": "10", "material": "Silicone"}},
        "stock": 500,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Bag Clip Large",
        "sku": "HOM-STO-7057",
        "price": Decimal128("3.00"),
        "details": {"description": "Chip bag sealer.", "specs": {"width": "4 inch", "spring": "Steel"}},
        "stock": 250,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Ball Pump Hose",
        "sku": "SPO-ACC-7058",
        "price": Decimal128("3.00"),
        "details": {"description": "Extension tube for pump.", "specs": {"length": "10cm", "flexible": "Yes"}},
        "stock": 300,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Bookmark Metal",
        "sku": "BOO-ACC-7059",
        "price": Decimal128("5.00"),
        "details": {"description": "Engraved page marker.", "specs": {"material": "Brass", "tassel": "Red"}},
        "stock": 150,
        "category": {"main": "Books", "sub": "Accessories"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Patch Iron-On",
        "sku": "CLO-ACC-7060",
        "price": Decimal128("3.00"),
        "details": {"description": "Embroidered star patch.", "specs": {"size": "2 inch", "adhesive": "Heat"}},
        "stock": 400,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Webcam Cover Slide",
        "sku": "ELE-ACC-7061",
        "price": Decimal128("3.00"),
        "details": {"description": "Privacy shutter.", "specs": {"thin": "Yes", "pack": "1"}},
        "stock": 600,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Funnel Small",
        "sku": "HOM-KIT-7062",
        "price": Decimal128("2.00"),
        "details": {"description": "Plastic kitchen funnel.", "specs": {"diameter": "3 inch", "color": "Clear"}},
        "stock": 350,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Ping Pong Ball",
        "sku": "SPO-GAM-7063",
        "price": Decimal128("1.00"),
        "details": {"description": "Single training ball.", "specs": {"color": "White", "star": "1"}},
        "stock": 1000,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Eraser White",
        "sku": "BOO-STA-7064",
        "price": Decimal128("1.00"),
        "details": {"description": "Vinyl pencil eraser.", "specs": {"dust": "Free", "wrap": "Paper"}},
        "stock": 800,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Safety Pin Pack",
        "sku": "CLO-ACC-7065",
        "price": Decimal128("2.00"),
        "details": {"description": "Assorted size pins.", "specs": {"count": "20", "material": "Steel"}},
        "stock": 500,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Stylus Tether",
        "sku": "ELE-ACC-7066",
        "price": Decimal128("3.00"),
        "details": {"description": "String for stylus pen.", "specs": {"length": "10 inch", "jack": "3.5mm"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Sponge Holder Suction",
        "sku": "HOM-ORG-7067",
        "price": Decimal128("4.00"),
        "details": {"description": "Sink suction hook.", "specs": {"material": "Plastic", "color": "Clear"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Organization"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Whistle Ring",
        "sku": "SPO-ACC-7068",
        "price": Decimal128("2.00"),
        "details": {"description": "Finger grip whistle.", "specs": {"color": "Black", "sound": "Medium"}},
        "stock": 400,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Pencil Sharpener",
        "sku": "BOO-STA-7069",
        "price": Decimal128("2.00"),
        "details": {"description": "Manual plastic sharpener.", "specs": {"blade": "Single", "color": "Assorted"}},
        "stock": 300,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Collar Stays",
        "sku": "CLO-ACC-7070",
        "price": Decimal128("5.00"),
        "details": {"description": "Plastic shirt stiffeners.", "specs": {"count": "20", "size": "Mixed"}},
        "stock": 150,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Mouse Feet Glides",
        "sku": "ELE-ACC-7071",
        "price": Decimal128("6.00"),
        "details": {"description": "Replacement skates.", "specs": {"material": "PTFE", "fit": "Universal"}},
        "stock": 120,
        "category": {"main": "Electronics", "sub": "Maintenance"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Egg Cup",
        "sku": "HOM-KIT-7072",
        "price": Decimal128("3.00"),
        "details": {"description": "Ceramic boiled egg holder.", "specs": {"color": "White", "shape": "Round"}},
        "stock": 220,
        "category": {"main": "Home & Kitchen", "sub": "Tableware"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Golf Tee",
        "sku": "SPO-GOL-7073",
        "price": Decimal128("0.50"),
        "details": {"description": "Single plastic tee.", "specs": {"color": "Red", "length": "3 inch"}},
        "stock": 1000,
        "category": {"main": "Sports", "sub": "Golf"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(2, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Bookmark Paper",
        "sku": "BOO-ACC-7074",
        "price": Decimal128("1.00"),
        "details": {"description": "Cardstock bookmark.", "specs": {"design": "Quote", "laminated": "No"}},
        "stock": 500,
        "category": {"main": "Books", "sub": "Accessories"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Button Extender",
        "sku": "CLO-ACC-7075",
        "price": Decimal128("3.00"),
        "details": {"description": "Waistband expander.", "specs": {"material": "Metal", "spring": "Yes"}},
        "stock": 250,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Sim Eject Tool",
        "sku": "ELE-ACC-7076",
        "price": Decimal128("1.00"),
        "details": {"description": "Phone tray opener pin.", "specs": {"material": "Steel", "pack": "5"}},
        "stock": 800,
        "category": {"main": "Electronics", "sub": "Tools"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Tea Bag Rest",
        "sku": "HOM-KIT-7077",
        "price": Decimal128("4.00"),
        "details": {"description": "Small ceramic dish.", "specs": {"shape": "Teapot", "color": "White"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Tea"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Dart Flight",
        "sku": "SPO-GAM-7078",
        "price": Decimal128("1.00"),
        "details": {"description": "Replacement dart tail.", "specs": {"shape": "Standard", "color": "Flag"}},
        "stock": 400,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Ruler Plastic",
        "sku": "BOO-STA-7079",
        "price": Decimal128("2.00"),
        "details": {"description": "30cm clear ruler.", "specs": {"units": "cm/inch", "flexible": "No"}},
        "stock": 300,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Sewing Needle Set",
        "sku": "CLO-ACC-7080",
        "price": Decimal128("4.00"),
        "details": {"description": "Hand sewing needles.", "specs": {"count": "10", "eye": "Large"}},
        "stock": 200,
        "category": {"main": "Clothing", "sub": "Tools"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Battery Case AA",
        "sku": "ELE-ACC-7081",
        "price": Decimal128("2.00"),
        "details": {"description": "Storage box for batteries.", "specs": {"holds": "4", "color": "Clear"}},
        "stock": 350,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Corn Holder",
        "sku": "HOM-KIT-7082",
        "price": Decimal128("3.00"),
        "details": {"description": "Cob skewer prongs.", "specs": {"pack": "2", "handle": "Yellow"}},
        "stock": 190,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Nose Clip Swim",
        "sku": "SPO-SWI-7083",
        "price": Decimal128("3.00"),
        "details": {"description": "Water block nose plug.", "specs": {"material": "Silicone", "color": "Skin"}},
        "stock": 220,
        "category": {"main": "Sports", "sub": "Swimming"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Sticky Notes",
        "sku": "BOO-STA-7084",
        "price": Decimal128("3.00"),
        "details": {"description": "Yellow memo pads.", "specs": {"size": "3x3", "sheets": "100"}},
        "stock": 450,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Bra Extender",
        "sku": "CLO-ACC-7085",
        "price": Decimal128("4.00"),
        "details": {"description": "Band extension hooks.", "specs": {"rows": "2", "colors": "Nude/Blk"}},
        "stock": 150,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Thermal Paste",
        "sku": "ELE-ACC-7086",
        "price": Decimal128("8.00"),
        "details": {"description": "CPU cooling compound.", "specs": {"weight": "4g", "conductivity": "High"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Maintenance"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Toothpick Dispenser",
        "sku": "HOM-KIT-7087",
        "price": Decimal128("5.00"),
        "details": {"description": "Pop-up stick holder.", "specs": {"material": "Plastic", "color": "Red"}},
        "stock": 120,
        "category": {"main": "Home & Kitchen", "sub": "Tableware"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Hockey Puck",
        "sku": "SPO-WIN-7088",
        "price": Decimal128("4.00"),
        "details": {"description": "Regulation rubber puck.", "specs": {"weight": "6oz", "color": "Black"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Hockey"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Protractor",
        "sku": "BOO-STA-7089",
        "price": Decimal128("1.00"),
        "details": {"description": "Half circle angle measurer.", "specs": {"degrees": "180", "clear": "Yes"}},
        "stock": 300,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Shirt Stays",
        "sku": "CLO-ACC-7090",
        "price": Decimal128("10.00"),
        "details": {"description": "Elastic garters for shirts.", "specs": {"style": "Y", "clip": "Metal"}},
        "stock": 80,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Microphone Windscreen",
        "sku": "ELE-AUD-7091",
        "price": Decimal128("3.00"),
        "details": {"description": "Foam cover for mic.", "specs": {"color": "Black", "fit": "Universal"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Audio"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Chopstick Rest",
        "sku": "HOM-KIT-7092",
        "price": Decimal128("2.00"),
        "details": {"description": "Ceramic utensil holder.", "specs": {"shape": "Leaf", "color": "Green"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Tableware"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Carabiner Clip",
        "sku": "SPO-OUT-7093",
        "price": Decimal128("3.00"),
        "details": {"description": "Aluminum D-ring hook.", "specs": {"load": "Light", "color": "Silver"}},
        "stock": 400,
        "category": {"main": "Sports", "sub": "Camping"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Highlighter Pen",
        "sku": "BOO-STA-7094",
        "price": Decimal128("1.00"),
        "details": {"description": "Fluorescent marker.", "specs": {"color": "Yellow", "tip": "Chisel"}},
        "stock": 600,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Collar Pin",
        "sku": "CLO-ACC-7095",
        "price": Decimal128("8.00"),
        "details": {"description": "Metal shirt bar.", "specs": {"finish": "Gold", "style": "Classic"}},
        "stock": 70,
        "category": {"main": "Clothing", "sub": "Jewelry"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Dust Blower Bulb",
        "sku": "ELE-CLN-7096",
        "price": Decimal128("5.00"),
        "details": {"description": "Rubber air pump cleaner.", "specs": {"nozzle": "Plastic", "color": "Blue"}},
        "stock": 150,
        "category": {"main": "Electronics", "sub": "Cleaning"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Napkin Ring",
        "sku": "HOM-DEC-7097",
        "price": Decimal128("3.00"),
        "details": {"description": "Wooden ring holder.", "specs": {"finish": "Natural", "pack": "1"}},
        "stock": 250,
        "category": {"main": "Home & Kitchen", "sub": "Decor"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Skate Laces",
        "sku": "SPO-WIN-7098",
        "price": Decimal128("6.00"),
        "details": {"description": "Waxed hockey laces.", "specs": {"length": "72 inch", "color": "White"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Hockey"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(5, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Index Cards",
        "sku": "BOO-STA-7099",
        "price": Decimal128("2.00"),
        "details": {"description": "Ruled flashcards pack.", "specs": {"size": "3x5", "count": "100"}},
        "stock": 300,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Zipper Pull",
        "sku": "CLO-ACC-7100",
        "price": Decimal128("1.00"),
        "details": {"description": "Replacement tag cord.", "specs": {"color": "Black", "material": "Nylon"}},
        "stock": 600,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Smart Garden 9",
        "sku": "HOM-GAR-8001",
        "price": Decimal128("199.99"),
        "details": {"description": "Self-watering indoor garden.", "specs": {"pods": "9", "light": "LED Grow"}},
        "stock": 45,
        "category": {"main": "Home & Kitchen", "sub": "Garden"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(4, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Noise White Machine",
        "sku": "ELE-HOM-8002",
        "price": Decimal128("35.00"),
        "details": {"description": "Sound machine for sleep.", "specs": {"sounds": "20", "timer": "Yes"}},
        "stock": 120,
        "category": {"main": "Electronics", "sub": "Home Appliances"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Trail Running Shoes",
        "sku": "SPO-RUN-8003",
        "price": Decimal128("110.00"),
        "details": {"description": "Rugged terrain sneakers.", "specs": {"grip": "High", "waterproof": "GoreTex"}},
        "stock": 60,
        "category": {"main": "Sports", "sub": "Running"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "History of Science",
        "sku": "BOO-SCI-8004",
        "price": Decimal128("28.00"),
        "details": {"description": "Discoveries that changed the world.", "specs": {"pages": "500", "cover": "Hardcover"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Science"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Leather Messenger Bag",
        "sku": "CLO-BAG-8005",
        "price": Decimal128("150.00"),
        "details": {"description": "Premium leather laptop bag.", "specs": {"color": "Tan", "size": "15 inch"}},
        "stock": 30,
        "category": {"main": "Clothing", "sub": "Bags"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "USB C Hub 8-in-1",
        "sku": "ELE-ACC-8006",
        "price": Decimal128("60.00"),
        "details": {"description": "Massive connectivity adapter.", "specs": {"ports": "Ethernet, HDMI, SD", "pd": "100W"}},
        "stock": 90,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Electric Pepper Grinder",
        "sku": "HOM-KIT-8007",
        "price": Decimal128("25.00"),
        "details": {"description": "Gravity operated mill.", "specs": {"light": "LED", "battery": "AA"}},
        "stock": 150,
        "category": {"main": "Home & Kitchen", "sub": "Kitchenware"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(3, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Kayak Paddle",
        "sku": "SPO-WAT-8008",
        "price": Decimal128("45.00"),
        "details": {"description": "Lightweight aluminum paddle.", "specs": {"length": "230cm", "blades": "Plastic"}},
        "stock": 55,
        "category": {"main": "Sports", "sub": "Water Sports"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Gardening Gloves",
        "sku": "HOM-GAR-8009",
        "price": Decimal128("12.00"),
        "details": {"description": "Thorn proof work gloves.", "specs": {"material": "Leather", "size": "M"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Garden"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Wireless Charger Stand",
        "sku": "ELE-ACC-8010",
        "price": Decimal128("30.00"),
        "details": {"description": "Fast charging phone dock.", "specs": {"power": "15W", "angle": "Vertical"}},
        "stock": 130,
        "category": {"main": "Electronics", "sub": "Phone Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Cycling Jersey",
        "sku": "SPO-CYC-8011",
        "price": Decimal128("40.00"),
        "details": {"description": "Breathable bike shirt.", "specs": {"zipper": "Full", "pockets": "3 Rear"}},
        "stock": 85,
        "category": {"main": "Sports", "sub": "Cycling"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Novels Box",
        "sku": "BOO-FIC-8012",
        "price": Decimal128("50.00"),
        "details": {"description": "Bronte Sisters collection.", "specs": {"books": "3", "binding": "Cloth"}},
        "stock": 35,
        "category": {"main": "Books", "sub": "Classics"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Denim Overalls",
        "sku": "CLO-BOT-8013",
        "price": Decimal128("65.00"),
        "details": {"description": "Vintage style dungarees.", "specs": {"fit": "Relaxed", "wash": "Dark"}},
        "stock": 70,
        "category": {"main": "Clothing", "sub": "Bottoms"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Smart Plug Outdoor",
        "sku": "ELE-SMA-8014",
        "price": Decimal128("25.00"),
        "details": {"description": "Weatherproof WiFi socket.", "specs": {"outlets": "2", "rating": "IP44"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Smart Home"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Bamboo Bath Mat",
        "sku": "HOM-BAT-8015",
        "price": Decimal128("30.00"),
        "details": {"description": "Water resistant wood mat.", "specs": {"size": "24x16", "grip": "Rubber"}},
        "stock": 95,
        "category": {"main": "Home & Kitchen", "sub": "Bathroom"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Ski Gloves",
        "sku": "SPO-WIN-8016",
        "price": Decimal128("45.00"),
        "details": {"description": "Insulated snow gloves.", "specs": {"waterproof": "Yes", "warmth": "-10C"}},
        "stock": 60,
        "category": {"main": "Sports", "sub": "Winter"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Architecture Modern",
        "sku": "BOO-ART-8017",
        "price": Decimal128("55.00"),
        "details": {"description": "Bauhaus design history.", "specs": {"pages": "400", "images": "B&W"}},
        "stock": 25,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Bucket Hat Camo",
        "sku": "CLO-HAT-8018",
        "price": Decimal128("18.00"),
        "details": {"description": "Camouflage print hat.", "specs": {"material": "Cotton", "size": "L"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Gaming Headset Stand",
        "sku": "ELE-GAM-8019",
        "price": Decimal128("35.00"),
        "details": {"description": "RGB headphone holder.", "specs": {"ports": "2 USB", "lights": "Chroma"}},
        "stock": 75,
        "category": {"main": "Electronics", "sub": "Gaming"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Silicone Ice Trays",
        "sku": "HOM-KIT-8020",
        "price": Decimal128("14.00"),
        "details": {"description": "Sphere and cube molds.", "specs": {"pack": "2", "lid": "Yes"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Kitchenware"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Dumbbell Set 10kg",
        "sku": "SPO-GYM-8021",
        "price": Decimal128("90.00"),
        "details": {"description": "Adjustable chrome weights.", "specs": {"case": "Included", "plates": "8"}},
        "stock": 20,
        "category": {"main": "Sports", "sub": "Weights"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Philosophy Logic",
        "sku": "BOO-PHI-8022",
        "price": Decimal128("22.00"),
        "details": {"description": "Introduction to logic.", "specs": {"author": "Copi", "edition": "14th"}},
        "stock": 50,
        "category": {"main": "Books", "sub": "Philosophy"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Silk Scarf Square",
        "sku": "CLO-ACC-8023",
        "price": Decimal128("30.00"),
        "details": {"description": "Small neck scarf.", "specs": {"size": "50cm", "print": "Dots"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Car Phone Mount Mag",
        "sku": "ELE-CAR-8024",
        "price": Decimal128("20.00"),
        "details": {"description": "Magnetic vent holder.", "specs": {"magnet": "N52", "rotation": "360"}},
        "stock": 180,
        "category": {"main": "Electronics", "sub": "Car Electronics"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Mixing Bowls Glass",
        "sku": "HOM-KIT-8025",
        "price": Decimal128("35.00"),
        "details": {"description": "Nesting glass bowls.", "specs": {"count": "3", "microwave": "Safe"}},
        "stock": 65,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Tennis Racket Pro",
        "sku": "SPO-TEN-8026",
        "price": Decimal128("180.00"),
        "details": {"description": "Graphite tournament racket.", "specs": {"weight": "300g", "head": "Midplus"}},
        "stock": 15,
        "category": {"main": "Sports", "sub": "Tennis"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Travel Journal Leather",
        "sku": "BOO-STA-8027",
        "price": Decimal128("25.00"),
        "details": {"description": "Refillable travel notebook.", "specs": {"cover": "Genuine Leather", "inserts": "3"}},
        "stock": 80,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Beanie Slouchy",
        "sku": "CLO-HAT-8028",
        "price": Decimal128("15.00"),
        "details": {"description": "Oversized knit hat.", "specs": {"material": "Acrylic", "color": "Maroon"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "HDMI Cable 8K",
        "sku": "ELE-ACC-8029",
        "price": Decimal128("25.00"),
        "details": {"description": "Ultra high speed cable.", "specs": {"version": "2.1", "length": "2m"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Cables"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Drawer Dividers Bamboo",
        "sku": "HOM-ORG-8030",
        "price": Decimal128("30.00"),
        "details": {"description": "Expandable drawer organizers.", "specs": {"pack": "4", "material": "Bamboo"}},
        "stock": 75,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Golf Balls Distance",
        "sku": "SPO-GOL-8031",
        "price": Decimal128("25.00"),
        "details": {"description": "Long drive golf balls.", "specs": {"pack": "12", "color": "White"}},
        "stock": 120,
        "category": {"main": "Sports", "sub": "Golf"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Poetry Classic",
        "sku": "BOO-POE-8032",
        "price": Decimal128("15.00"),
        "details": {"description": "Poems of Emily Dickinson.", "specs": {"edition": "Complete", "pages": "400"}},
        "stock": 60,
        "category": {"main": "Books", "sub": "Poetry"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Running Socks Pack",
        "sku": "CLO-ACC-8033",
        "price": Decimal128("18.00"),
        "details": {"description": "Compression fit socks.", "specs": {"count": "3", "cushion": "Heel"}},
        "stock": 140,
        "category": {"main": "Clothing", "sub": "Socks"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Webcam Cover Slider",
        "sku": "ELE-ACC-8034",
        "price": Decimal128("5.00"),
        "details": {"description": "Ultra thin privacy shield.", "specs": {"pack": "3", "color": "Black"}},
        "stock": 400,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Garlic Press Steel",
        "sku": "HOM-KIT-8035",
        "price": Decimal128("15.00"),
        "details": {"description": "Professional garlic crusher.", "specs": {"cleaner": "Included", "rust": "Proof"}},
        "stock": 90,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Soccer Shin Guards",
        "sku": "SPO-SOC-8036",
        "price": Decimal128("15.00"),
        "details": {"description": "Ankle protection guards.", "specs": {"size": "S", "strap": "Velcro"}},
        "stock": 110,
        "category": {"main": "Sports", "sub": "Soccer"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Biography Musician",
        "sku": "BOO-BIO-8037",
        "price": Decimal128("26.00"),
        "details": {"description": "Life of David Bowie.", "specs": {"pages": "450", "photos": "Rare"}},
        "stock": 45,
        "category": {"main": "Books", "sub": "Biography"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Gloves Touchscreen",
        "sku": "CLO-ACC-8038",
        "price": Decimal128("12.00"),
        "details": {"description": "Knit smartphone gloves.", "specs": {"tips": "Conductive", "color": "Grey"}},
        "stock": 200,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Battery Organizer",
        "sku": "ELE-ORG-8039",
        "price": Decimal128("20.00"),
        "details": {"description": "Case with tester.", "specs": {"holds": "90", "mount": "Wall"}},
        "stock": 70,
        "category": {"main": "Electronics", "sub": "Storage"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Oven Thermometer",
        "sku": "HOM-KIT-8040",
        "price": Decimal128("8.00"),
        "details": {"description": "Monitoring gauge for baking.", "specs": {"dial": "Large", "hook": "Hang"}},
        "stock": 130,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Ball Pump Electric",
        "sku": "SPO-ACC-8041",
        "price": Decimal128("25.00"),
        "details": {"description": "Automatic sports ball pump.", "specs": {"psi": "Digital", "battery": "Recharge"}},
        "stock": 60,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Language Flashcards",
        "sku": "BOO-EDU-8042",
        "price": Decimal128("15.00"),
        "details": {"description": "Learn Japanese Hiragana.", "specs": {"count": "100", "ring": "Binder"}},
        "stock": 90,
        "category": {"main": "Books", "sub": "Education"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Belt Braided",
        "sku": "CLO-ACC-8043",
        "price": Decimal128("18.00"),
        "details": {"description": "Stretchy woven belt.", "specs": {"color": "Blue", "leather": "Trim"}},
        "stock": 110,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Cable Management Ties",
        "sku": "ELE-ORG-8044",
        "price": Decimal128("6.00"),
        "details": {"description": "Hook and loop straps.", "specs": {"roll": "3m", "cut": "Custom"}},
        "stock": 300,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Pizza Peel",
        "sku": "HOM-KIT-8045",
        "price": Decimal128("28.00"),
        "details": {"description": "Aluminum pizza paddle.", "specs": {"handle": "Folding", "size": "12 inch"}},
        "stock": 50,
        "category": {"main": "Home & Kitchen", "sub": "Bakeware"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Volleyball Knee Pads",
        "sku": "SPO-VOL-8046",
        "price": Decimal128("20.00"),
        "details": {"description": "Impact protection pads.", "specs": {"pair": "1", "color": "White"}},
        "stock": 85,
        "category": {"main": "Sports", "sub": "Volleyball"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(3, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Science Fiction Novel",
        "sku": "BOO-FIC-8047",
        "price": Decimal128("16.00"),
        "details": {"description": "Dune by Frank Herbert.", "specs": {"pages": "600", "cover": "Paperback"}},
        "stock": 100,
        "category": {"main": "Books", "sub": "Sci-Fi"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Scarf Plaid",
        "sku": "CLO-ACC-8048",
        "price": Decimal128("22.00"),
        "details": {"description": "Soft tartan winter scarf.", "specs": {"pattern": "Red Check", "fringe": "Yes"}},
        "stock": 70,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Mouse Wrist Rest",
        "sku": "ELE-ACC-8049",
        "price": Decimal128("10.00"),
        "details": {"description": "Memory foam pad.", "specs": {"shape": "Ergonomic", "base": "Rubber"}},
        "stock": 140,
        "category": {"main": "Electronics", "sub": "Peripherals"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Whisk Set",
        "sku": "HOM-KIT-8050",
        "price": Decimal128("12.00"),
        "details": {"description": "3 sizes wire whisks.", "specs": {"material": "Stainless", "loop": "Hang"}},
        "stock": 160,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Resistance Band Heavy",
        "sku": "SPO-FIT-8051",
        "price": Decimal128("15.00"),
        "details": {"description": "Thick powerlifting band.", "specs": {"tension": "50-125lbs", "color": "Green"}},
        "stock": 60,
        "category": {"main": "Sports", "sub": "Fitness"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Cookbook Vegan",
        "sku": "BOO-COO-8052",
        "price": Decimal128("24.00"),
        "details": {"description": "Easy plant meals.", "specs": {"recipes": "150", "author": "Bosh"}},
        "stock": 85,
        "category": {"main": "Books", "sub": "Cooking"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Sun Hat Floppy",
        "sku": "CLO-HAT-8053",
        "price": Decimal128("20.00"),
        "details": {"description": "Large brim straw hat.", "specs": {"ribbon": "Black", "size": "One Size"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Hats"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Headphone Case",
        "sku": "ELE-AUD-8054",
        "price": Decimal128("15.00"),
        "details": {"description": "Hard shell travel bag.", "specs": {"fit": "Universal Fold", "pocket": "Mesh"}},
        "stock": 110,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Tea Strainer",
        "sku": "HOM-KIT-8055",
        "price": Decimal128("5.00"),
        "details": {"description": "Over cup fine mesh.", "specs": {"material": "Steel", "handle": "Long"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Tea"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Badminton Net",
        "sku": "SPO-BAD-8056",
        "price": Decimal128("40.00"),
        "details": {"description": "Portable sports net.", "specs": {"width": "Standard", "setup": "Easy"}},
        "stock": 35,
        "category": {"main": "Sports", "sub": "Badminton"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Dictionary Thesaurus",
        "sku": "BOO-REF-8057",
        "price": Decimal128("20.00"),
        "details": {"description": "2-in-1 reference book.", "specs": {"pages": "800", "binding": "Soft"}},
        "stock": 75,
        "category": {"main": "Books", "sub": "Reference"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Fingerless Mittens",
        "sku": "CLO-ACC-8058",
        "price": Decimal128("14.00"),
        "details": {"description": "Convertible wool gloves.", "specs": {"cap": "Flip-top", "color": "Beige"}},
        "stock": 100,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Micro SD Adapter",
        "sku": "ELE-ACC-8059",
        "price": Decimal128("3.00"),
        "details": {"description": "Card to SD converter.", "specs": {"lock": "Switch", "pack": "2"}},
        "stock": 400,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Sponge Holder",
        "sku": "HOM-ORG-8060",
        "price": Decimal128("8.00"),
        "details": {"description": "Sink saddle caddy.", "specs": {"material": "Silicone", "drain": "Holes"}},
        "stock": 150,
        "category": {"main": "Home & Kitchen", "sub": "Organization"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Golf Divot Tool",
        "sku": "SPO-GOL-8061",
        "price": Decimal128("8.00"),
        "details": {"description": "Pitch mark repairer.", "specs": {"material": "Metal", "marker": "Magnetic"}},
        "stock": 120,
        "category": {"main": "Sports", "sub": "Golf"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Art Sketchbook",
        "sku": "BOO-ART-8062",
        "price": Decimal128("12.00"),
        "details": {"description": "Spiral bound drawing pad.", "specs": {"size": "A4", "paper": "White"}},
        "stock": 140,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Shoe Insoles",
        "sku": "CLO-ACC-8063",
        "price": Decimal128("15.00"),
        "details": {"description": "Gel comfort inserts.", "specs": {"size": "Trim to fit", "arch": "Support"}},
        "stock": 180,
        "category": {"main": "Clothing", "sub": "Shoe Accessories"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "DisplayPort Adapter",
        "sku": "ELE-ACC-8064",
        "price": Decimal128("12.00"),
        "details": {"description": "DP to HDMI converter.", "specs": {"res": "1080p", "audio": "Yes"}},
        "stock": 90,
        "category": {"main": "Electronics", "sub": "Adapters"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Chopsticks Reusable",
        "sku": "HOM-KIT-8065",
        "price": Decimal128("8.00"),
        "details": {"description": "Fiberglass alloy sticks.", "specs": {"pack": "5 pairs", "color": "Black"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Whistle Metal",
        "sku": "SPO-ACC-8066",
        "price": Decimal128("4.00"),
        "details": {"description": "Stainless steel referee whistle.", "specs": {"lanyard": "Yellow", "cork": "Pea"}},
        "stock": 300,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Sudoku Puzzle Book",
        "sku": "BOO-GAM-8067",
        "price": Decimal128("8.00"),
        "details": {"description": "Logic number games.", "specs": {"level": "Expert", "puzzles": "200"}},
        "stock": 160,
        "category": {"main": "Books", "sub": "Games"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Necktie Clip",
        "sku": "CLO-ACC-8068",
        "price": Decimal128("10.00"),
        "details": {"description": "Silver tie bar.", "specs": {"finish": "Matte", "width": "Short"}},
        "stock": 85,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Thermal Paste 1g",
        "sku": "ELE-ACC-8069",
        "price": Decimal128("5.00"),
        "details": {"description": "Processor cooling grease.", "specs": {"syringe": "1", "type": "Silver"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Maintenance"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Corn Stripper",
        "sku": "HOM-KIT-8070",
        "price": Decimal128("7.00"),
        "details": {"description": "Cob kernel remover.", "specs": {"blade": "Stainless", "grip": "Plastic"}},
        "stock": 110,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Swimming Nose Clip",
        "sku": "SPO-SWI-8071",
        "price": Decimal128("3.00"),
        "details": {"description": "Comfort nose plug.", "specs": {"frame": "Wire", "pads": "Latex"}},
        "stock": 220,
        "category": {"main": "Sports", "sub": "Swimming"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Journal Lined",
        "sku": "BOO-STA-8072",
        "price": Decimal128("10.00"),
        "details": {"description": "Writing notebook hardbound.", "specs": {"color": "Blue", "marker": "Ribbon"}},
        "stock": 130,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "No-Tie Laces",
        "sku": "CLO-ACC-8073",
        "price": Decimal128("6.00"),
        "details": {"description": "Elastic lock shoelaces.", "specs": {"system": "Lock", "color": "Black"}},
        "stock": 300,
        "category": {"main": "Clothing", "sub": "Shoe Accessories"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Phone Dust Plugs",
        "sku": "ELE-ACC-8074",
        "price": Decimal128("3.00"),
        "details": {"description": "Charging port protection.", "specs": {"type": "USB-C", "pack": "5"}},
        "stock": 500,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Pot Handle Holder",
        "sku": "HOM-KIT-8075",
        "price": Decimal128("5.00"),
        "details": {"description": "Silicone hot handle cover.", "specs": {"fit": "Universal", "heat": "High"}},
        "stock": 190,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Ball Pump Needle Set",
        "sku": "SPO-ACC-8076",
        "price": Decimal128("2.00"),
        "details": {"description": "Standard inflating pins.", "specs": {"count": "3", "metal": "Brass"}},
        "stock": 600,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Pocket Notebook",
        "sku": "BOO-STA-8077",
        "price": Decimal128("3.00"),
        "details": {"description": "Small memo pad.", "specs": {"binding": "Staple", "pages": "32"}},
        "stock": 400,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Bra Strap Clips",
        "sku": "CLO-ACC-8078",
        "price": Decimal128("3.00"),
        "details": {"description": "Racerback converter clips.", "specs": {"pack": "4", "shape": "Round"}},
        "stock": 250,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "SIM Card Adapter",
        "sku": "ELE-ACC-8079",
        "price": Decimal128("2.00"),
        "details": {"description": "Nano to micro converter.", "specs": {"kit": "3-piece", "tool": "Yes"}},
        "stock": 700,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Bag Sealer Clip",
        "sku": "HOM-STO-8080",
        "price": Decimal128("2.00"),
        "details": {"description": "Plastic food clamp.", "specs": {"size": "Medium", "color": "Assorted"}},
        "stock": 450,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Dart Shafts",
        "sku": "SPO-GAM-8081",
        "price": Decimal128("3.00"),
        "details": {"description": "Replacement dart stems.", "specs": {"material": "Nylon", "pack": "3"}},
        "stock": 300,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Pencil Grip",
        "sku": "BOO-STA-8082",
        "price": Decimal128("1.00"),
        "details": {"description": "Ergonomic writing aid.", "specs": {"material": "Foam", "color": "Mixed"}},
        "stock": 500,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Shoe Heal Pad",
        "sku": "CLO-ACC-8083",
        "price": Decimal128("4.00"),
        "details": {"description": "Anti-slip heel liner.", "specs": {"adhesive": "Back", "material": "Fabric"}},
        "stock": 200,
        "category": {"main": "Clothing", "sub": "Shoe Accessories"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Keycap Puller",
        "sku": "ELE-ACC-8084",
        "price": Decimal128("3.00"),
        "details": {"description": "Mechanical keyboard tool.", "specs": {"material": "Plastic", "ring": "Finger"}},
        "stock": 350,
        "category": {"main": "Electronics", "sub": "Maintenance"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Egg Separator",
        "sku": "HOM-KIT-8085",
        "price": Decimal128("3.00"),
        "details": {"description": "Yolk white splitter.", "specs": {"material": "Plastic", "clip": "Bowl"}},
        "stock": 220,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Whistle Cord",
        "sku": "SPO-ACC-8086",
        "price": Decimal128("1.00"),
        "details": {"description": "Nylon lanyard for whistle.", "specs": {"color": "Black", "hook": "Metal"}},
        "stock": 600,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Eraser Cap",
        "sku": "BOO-STA-8087",
        "price": Decimal128("1.00"),
        "details": {"description": "Pencil top erasers.", "specs": {"pack": "10", "shape": "Chisel"}},
        "stock": 800,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Collar Stiffeners",
        "sku": "CLO-ACC-8088",
        "price": Decimal128("3.00"),
        "details": {"description": "Plastic shirt stays.", "specs": {"pack": "10", "clear": "Yes"}},
        "stock": 300,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Cable Winder",
        "sku": "ELE-ORG-8089",
        "price": Decimal128("2.00"),
        "details": {"description": "Earphone cord keeper.", "specs": {"shape": "Turtle", "silicone": "Yes"}},
        "stock": 400,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Citrus Peeler",
        "sku": "HOM-KIT-8090",
        "price": Decimal128("1.00"),
        "details": {"description": "Orange skin cutter.", "specs": {"material": "Plastic", "ring": "Finger"}},
        "stock": 500,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Air Pump Nozzle",
        "sku": "SPO-ACC-8091",
        "price": Decimal128("1.00"),
        "details": {"description": "Plastic inflation tip.", "specs": {"use": "Inflatables", "fit": "Standard"}},
        "stock": 700,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Protractor Plastic",
        "sku": "BOO-STA-8092",
        "price": Decimal128("1.00"),
        "details": {"description": "Clear 180 degree tool.", "specs": {"size": "4 inch", "markings": "Black"}},
        "stock": 450,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Safety Pins",
        "sku": "CLO-ACC-8093",
        "price": Decimal128("1.00"),
        "details": {"description": "Small steel pins.", "specs": {"pack": "20", "size": "1 inch"}},
        "stock": 900,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Dust Plug 3.5mm",
        "sku": "ELE-ACC-8094",
        "price": Decimal128("1.00"),
        "details": {"description": "Headphone jack cover.", "specs": {"material": "Rubber", "pack": "5"}},
        "stock": 600,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(2, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Bag Tie",
        "sku": "HOM-STO-8095",
        "price": Decimal128("1.00"),
        "details": {"description": "Twist tie for bags.", "specs": {"length": "Roll", "cutter": "Yes"}},
        "stock": 350,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Dart Point Guard",
        "sku": "SPO-GAM-8096",
        "price": Decimal128("1.00"),
        "details": {"description": "Tip protector for darts.", "specs": {"material": "Rubber", "holds": "3"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Paper Clips",
        "sku": "BOO-STA-8097",
        "price": Decimal128("1.00"),
        "details": {"description": "Standard wire clips.", "specs": {"box": "100", "finish": "Silver"}},
        "stock": 800,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Button White",
        "sku": "CLO-ACC-8098",
        "price": Decimal128("0.50"),
        "details": {"description": "Replacement shirt button.", "specs": {"size": "10mm", "holes": "4"}},
        "stock": 1000,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(1, 2)
    },
    {
        "_id": ObjectId(),
        "name": "Zip Tie",
        "sku": "ELE-ORG-8099",
        "price": Decimal128("0.50"),
        "details": {"description": "Nylon cable tie.", "specs": {"length": "6 inch", "color": "White"}},
        "stock": 1500,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Bottle Cap",
        "sku": "HOM-STO-8100",
        "price": Decimal128("0.50"),
        "details": {"description": "Spare cap for glass bottle.", "specs": {"thread": "Standard", "seal": "Foam"}},
        "stock": 600,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Smart Scale Body Fat",
        "sku": "ELE-HEA-9001",
        "price": Decimal128("35.00"),
        "details": {"description": "Bluetooth bathroom scale.", "specs": {"metrics": "BMI/Fat", "app": "Yes"}},
        "stock": 60,
        "category": {"main": "Electronics", "sub": "Health"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Cast Iron Griddle",
        "sku": "HOM-CKW-9002",
        "price": Decimal128("40.00"),
        "details": {"description": "Reversible grill/griddle pan.", "specs": {"size": "20 inch", "material": "Iron"}},
        "stock": 45,
        "category": {"main": "Home & Kitchen", "sub": "Cookware"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Resistance Parachute",
        "sku": "SPO-TRA-9003",
        "price": Decimal128("15.00"),
        "details": {"description": "Speed training drag chute.", "specs": {"belt": "Adjustable", "size": "56 inch"}},
        "stock": 90,
        "category": {"main": "Sports", "sub": "Training"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Sci-Fi Book",
        "sku": "BOO-FIC-9004",
        "price": Decimal128("14.00"),
        "details": {"description": "Foundation by Asimov.", "specs": {"pages": "250", "cover": "Paperback"}},
        "stock": 110,
        "category": {"main": "Books", "sub": "Sci-Fi"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(5, 15)
    },
    {
        "_id": ObjectId(),
        "name": "Linen Shorts",
        "sku": "CLO-BOT-9005",
        "price": Decimal128("30.00"),
        "details": {"description": "Summer casual shorts.", "specs": {"material": "Linen Blend", "color": "White"}},
        "stock": 80,
        "category": {"main": "Clothing", "sub": "Bottoms"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "USB Desk Lamp",
        "sku": "ELE-HOM-9006",
        "price": Decimal128("20.00"),
        "details": {"description": "Flexible neck LED light.", "specs": {"dimmable": "Yes", "power": "USB"}},
        "stock": 150,
        "category": {"main": "Electronics", "sub": "Home"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Ravioli Stamp Set",
        "sku": "HOM-KIT-9007",
        "price": Decimal128("18.00"),
        "details": {"description": "Pasta maker press.", "specs": {"shapes": "Square/Round", "handle": "Wood"}},
        "stock": 70,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Lacrosse Ball",
        "sku": "SPO-TRA-9008",
        "price": Decimal128("5.00"),
        "details": {"description": "Massage trigger point ball.", "specs": {"material": "Rubber", "color": "Orange"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Recovery"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(5, 14)
    },
    {
        "_id": ObjectId(),
        "name": "Garden Journal",
        "sku": "BOO-HOB-9009",
        "price": Decimal128("16.00"),
        "details": {"description": "Plant tracking logbook.", "specs": {"pages": "120", "cover": "Waterproof"}},
        "stock": 55,
        "category": {"main": "Books", "sub": "Hobbies"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Tuxedo Shirt",
        "sku": "CLO-FOR-9010",
        "price": Decimal128("55.00"),
        "details": {"description": "Formal pleated shirt.", "specs": {"fit": "Slim", "cuff": "French"}},
        "stock": 40,
        "category": {"main": "Clothing", "sub": "Formal"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Drawing Tablet Glove",
        "sku": "ELE-ACC-9011",
        "price": Decimal128("8.00"),
        "details": {"description": "Anti-fouling artist glove.", "specs": {"fingers": "2", "hand": "Universal"}},
        "stock": 180,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Fermenting Lids",
        "sku": "HOM-KIT-9012",
        "price": Decimal128("15.00"),
        "details": {"description": "Airpock lids for jars.", "specs": {"pack": "4", "fit": "Wide Mouth"}},
        "stock": 100,
        "category": {"main": "Home & Kitchen", "sub": "Kitchenware"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Rugby Kicking Tee",
        "sku": "SPO-RUG-9013",
        "price": Decimal128("10.00"),
        "details": {"description": "Adjustable height tee.", "specs": {"material": "Rubber", "color": "Green"}},
        "stock": 130,
        "category": {"main": "Sports", "sub": "Rugby"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Economics History",
        "sku": "BOO-HIS-9014",
        "price": Decimal128("32.00"),
        "details": {"description": "Evolution of markets.", "specs": {"pages": "400", "author": "Ferguson"}},
        "stock": 35,
        "category": {"main": "Books", "sub": "History"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Cummerbund",
        "sku": "CLO-ACC-9015",
        "price": Decimal128("20.00"),
        "details": {"description": "Formal waist sash.", "specs": {"material": "Satin", "color": "Black"}},
        "stock": 60,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Server Rack Screws",
        "sku": "ELE-NET-9016",
        "price": Decimal128("12.00"),
        "details": {"description": "M6 mounting screws.", "specs": {"count": "50", "cage_nuts": "Yes"}},
        "stock": 200,
        "category": {"main": "Electronics", "sub": "Networking"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Basting Brush",
        "sku": "HOM-KIT-9017",
        "price": Decimal128("6.00"),
        "details": {"description": "BBQ marinade brush.", "specs": {"bristles": "Silicone", "handle": "Long"}},
        "stock": 160,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Cricket Ball",
        "sku": "SPO-CRI-9018",
        "price": Decimal128("15.00"),
        "details": {"description": "Leather match ball.", "specs": {"weight": "156g", "color": "Red"}},
        "stock": 85,
        "category": {"main": "Sports", "sub": "Cricket"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Sudoku Advanced",
        "sku": "BOO-GAM-9019",
        "price": Decimal128("9.00"),
        "details": {"description": "Hard puzzle collection.", "specs": {"puzzles": "300", "paper": "Standard"}},
        "stock": 140,
        "category": {"main": "Books", "sub": "Games"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Velvet Hangers",
        "sku": "HOM-STO-9020",
        "price": Decimal128("25.00"),
        "details": {"description": "Non-slip clothes hangers.", "specs": {"pack": "50", "color": "Black"}},
        "stock": 95,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(4, 11)
    },
    {
        "_id": ObjectId(),
        "name": "HDMI Extension",
        "sku": "ELE-ACC-9021",
        "price": Decimal128("10.00"),
        "details": {"description": "Male to female adapter.", "specs": {"length": "1m", "4k": "Supported"}},
        "stock": 170,
        "category": {"main": "Electronics", "sub": "Cables"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Oven Liner",
        "sku": "HOM-KIT-9022",
        "price": Decimal128("12.00"),
        "details": {"description": "Non-stick drip mat.", "specs": {"pack": "2", "clean": "Wipe"}},
        "stock": 120,
        "category": {"main": "Home & Kitchen", "sub": "Kitchenware"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(2, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Stopwatch Metal",
        "sku": "SPO-ACC-9023",
        "price": Decimal128("25.00"),
        "details": {"description": "Heavy duty digital timer.", "specs": {"accuracy": "0.01s", "case": "Metal"}},
        "stock": 50,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Art Anatomy Book",
        "sku": "BOO-ART-9024",
        "price": Decimal128("35.00"),
        "details": {"description": "Drawing the human figure.", "specs": {"pages": "200", "diagrams": "Detailed"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Art"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Apron Canvas",
        "sku": "CLO-ACC-9025",
        "price": Decimal128("28.00"),
        "details": {"description": "Heavy duty work apron.", "specs": {"pockets": "Multiple", "straps": "Leather"}},
        "stock": 65,
        "category": {"main": "Clothing", "sub": "Workwear"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Microphone Pop Filter",
        "sku": "ELE-AUD-9026",
        "price": Decimal128("15.00"),
        "details": {"description": "Mesh screen for recording.", "specs": {"layers": "Double", "neck": "Goose"}},
        "stock": 110,
        "category": {"main": "Electronics", "sub": "Audio"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Cheese Knives Set",
        "sku": "HOM-KIT-9027",
        "price": Decimal128("20.00"),
        "details": {"description": "Serving blades for cheese.", "specs": {"count": "4", "handle": "Wood"}},
        "stock": 80,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(4, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Hand Wraps MMA",
        "sku": "SPO-MAR-9028",
        "price": Decimal128("10.00"),
        "details": {"description": "Protective hand bandages.", "specs": {"length": "120 inch", "stretch": "Yes"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Martial Arts"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Coding for Kids",
        "sku": "BOO-KID-9029",
        "price": Decimal128("18.00"),
        "details": {"description": "Python basics for children.", "specs": {"age": "10+", "pages": "150"}},
        "stock": 90,
        "category": {"main": "Books", "sub": "Education"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Bow Tie Pre-tied",
        "sku": "CLO-ACC-9030",
        "price": Decimal128("15.00"),
        "details": {"description": "Adjustable strap bow tie.", "specs": {"color": "Red", "material": "Polyester"}},
        "stock": 130,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(1, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Keyboard Switch Puller",
        "sku": "ELE-ACC-9031",
        "price": Decimal128("6.00"),
        "details": {"description": "Tool for mechanical keys.", "specs": {"material": "Steel", "grip": "Rubber"}},
        "stock": 220,
        "category": {"main": "Electronics", "sub": "Tools"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Jar Gripper Pads",
        "sku": "HOM-KIT-9032",
        "price": Decimal128("5.00"),
        "details": {"description": "Rubber jar opener sheets.", "specs": {"pack": "3", "shape": "Round"}},
        "stock": 300,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Ski Wax",
        "sku": "SPO-WIN-9033",
        "price": Decimal128("15.00"),
        "details": {"description": "Universal glide wax.", "specs": {"temp": "All", "weight": "60g"}},
        "stock": 70,
        "category": {"main": "Sports", "sub": "Winter"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Classic Drama",
        "sku": "BOO-FIC-9034",
        "price": Decimal128("12.00"),
        "details": {"description": "Death of a Salesman.", "specs": {"author": "Miller", "format": "Play"}},
        "stock": 50,
        "category": {"main": "Books", "sub": "Plays"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Lace Locks",
        "sku": "CLO-ACC-9035",
        "price": Decimal128("5.00"),
        "details": {"description": "Toggles for shoelaces.", "specs": {"pair": "2", "color": "Black"}},
        "stock": 400,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "PC Dust Filter",
        "sku": "ELE-ACC-9036",
        "price": Decimal128("10.00"),
        "details": {"description": "Magnetic fan mesh.", "specs": {"size": "120mm", "pack": "2"}},
        "stock": 150,
        "category": {"main": "Electronics", "sub": "Computer Parts"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Sushi Mat",
        "sku": "HOM-KIT-9037",
        "price": Decimal128("5.00"),
        "details": {"description": "Bamboo rolling mat.", "specs": {"size": "9.5 inch", "natural": "Yes"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 13)
    },
    {
        "_id": ObjectId(),
        "name": "Billiard Glove",
        "sku": "SPO-GAM-9038",
        "price": Decimal128("12.00"),
        "details": {"description": "3-finger pool glove.", "specs": {"hand": "Left", "material": "Spandex"}},
        "stock": 100,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Thesaurus Pocket",
        "sku": "BOO-REF-9039",
        "price": Decimal128("9.00"),
        "details": {"description": "Synonyms and antonyms.", "specs": {"size": "Small", "entries": "100k"}},
        "stock": 120,
        "category": {"main": "Books", "sub": "Reference"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Bandana Blue",
        "sku": "CLO-ACC-9040",
        "price": Decimal128("4.00"),
        "details": {"description": "Cotton head scarf.", "specs": {"pattern": "Paisley", "color": "Navy"}},
        "stock": 300,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "RJ45 Coupler",
        "sku": "ELE-NET-9041",
        "price": Decimal128("5.00"),
        "details": {"description": "Ethernet cable joiner.", "specs": {"type": "Female-Female", "shielded": "Yes"}},
        "stock": 250,
        "category": {"main": "Electronics", "sub": "Networking"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Tea Infuser Tongs",
        "sku": "HOM-KIT-9042",
        "price": Decimal128("8.00"),
        "details": {"description": "Mesh tea ball handle.", "specs": {"mechanism": "Squeeze", "steel": "Stainless"}},
        "stock": 140,
        "category": {"main": "Home & Kitchen", "sub": "Tea"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Reflective Armband",
        "sku": "SPO-RUN-9043",
        "price": Decimal128("8.00"),
        "details": {"description": "High vis safety strap.", "specs": {"closure": "Velcro", "color": "Neon"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Running"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "French Phrasebook",
        "sku": "BOO-TRA-9044",
        "price": Decimal128("10.00"),
        "details": {"description": "Travel language guide.", "specs": {"language": "French", "size": "Pocket"}},
        "stock": 80,
        "category": {"main": "Books", "sub": "Travel"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Braided Belt",
        "sku": "CLO-ACC-9045",
        "price": Decimal128("18.00"),
        "details": {"description": "Stretch woven belt.", "specs": {"color": "Brown", "buckle": "Silver"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "DVI Cable",
        "sku": "ELE-ACC-9046",
        "price": Decimal128("10.00"),
        "details": {"description": "Digital video cord.", "specs": {"length": "1.8m", "dual_link": "Yes"}},
        "stock": 60,
        "category": {"main": "Electronics", "sub": "Cables"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Grapefruit Spoon",
        "sku": "HOM-KIT-9047",
        "price": Decimal128("6.00"),
        "details": {"description": "Serrated edge spoon.", "specs": {"pack": "2", "material": "Steel"}},
        "stock": 150,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Squash Ball",
        "sku": "SPO-GAM-9048",
        "price": Decimal128("5.00"),
        "details": {"description": "Double yellow dot ball.", "specs": {"speed": "Slow", "bounce": "Low"}},
        "stock": 110,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Comics Anthology",
        "sku": "BOO-COM-9049",
        "price": Decimal128("25.00"),
        "details": {"description": "Best indie comics.", "specs": {"pages": "300", "color": "Mixed"}},
        "stock": 40,
        "category": {"main": "Books", "sub": "Comics"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Cufflinks Knot",
        "sku": "CLO-ACC-9050",
        "price": Decimal128("8.00"),
        "details": {"description": "Silk knot cuff links.", "specs": {"pair": "1", "color": "Navy"}},
        "stock": 130,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Audio Splitter",
        "sku": "ELE-AUD-9051",
        "price": Decimal128("7.00"),
        "details": {"description": "3.5mm Y adapter.", "specs": {"ports": "2 Female", "plug": "1 Male"}},
        "stock": 350,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(3, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Funnel Set",
        "sku": "HOM-KIT-9052",
        "price": Decimal128("8.00"),
        "details": {"description": "3 nesting funnels.", "specs": {"material": "Plastic", "color": "Red"}},
        "stock": 190,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Pedometer",
        "sku": "SPO-ACC-9053",
        "price": Decimal128("10.00"),
        "details": {"description": "Simple step counter.", "specs": {"clip": "Waist", "battery": "Included"}},
        "stock": 140,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Graph Paper Pad",
        "sku": "BOO-STA-9054",
        "price": Decimal128("6.00"),
        "details": {"description": "Squared grid notebook.", "specs": {"size": "A4", "sheets": "50"}},
        "stock": 250,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Suspenders Black",
        "sku": "CLO-ACC-9055",
        "price": Decimal128("15.00"),
        "details": {"description": "X-back adjustable braces.", "specs": {"clips": "4", "width": "1 inch"}},
        "stock": 90,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Cable Labels",
        "sku": "ELE-ORG-9056",
        "price": Decimal128("5.00"),
        "details": {"description": "Write-on cord tags.", "specs": {"pack": "20", "color": "Multi"}},
        "stock": 400,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Egg Timer",
        "sku": "HOM-KIT-9057",
        "price": Decimal128("6.00"),
        "details": {"description": "Color changing boil timer.", "specs": {"placed": "In pot", "indicator": "Soft/Hard"}},
        "stock": 220,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Helmet Chin Strap",
        "sku": "SPO-ACC-9058",
        "price": Decimal128("8.00"),
        "details": {"description": "Replacement buckle strap.", "specs": {"fit": "Universal", "color": "Black"}},
        "stock": 160,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Binder Clips",
        "sku": "BOO-STA-9059",
        "price": Decimal128("4.00"),
        "details": {"description": "Assorted size clips.", "specs": {"box": "20", "color": "Black"}},
        "stock": 500,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Money Clip",
        "sku": "CLO-ACC-9060",
        "price": Decimal128("12.00"),
        "details": {"description": "Slim cash holder.", "specs": {"material": "Steel", "finish": "Matte"}},
        "stock": 130,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Solder Wire",
        "sku": "ELE-ACC-9061",
        "price": Decimal128("8.00"),
        "details": {"description": "Lead-free soldering tin.", "specs": {"diameter": "0.8mm", "weight": "50g"}},
        "stock": 100,
        "category": {"main": "Electronics", "sub": "Tools"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Ice Tongs",
        "sku": "HOM-KIT-9062",
        "price": Decimal128("7.00"),
        "details": {"description": "Stainless steel grippers.", "specs": {"teeth": "Serrated", "length": "6 inch"}},
        "stock": 150,
        "category": {"main": "Home & Kitchen", "sub": "Barware"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Gym Chalk Block",
        "sku": "SPO-GYM-9063",
        "price": Decimal128("5.00"),
        "details": {"description": "Magnesium carbonate block.", "specs": {"weight": "2oz", "grip": "Dry"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Weights"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Sheet Music Notebook",
        "sku": "BOO-MUS-9064",
        "price": Decimal128("10.00"),
        "details": {"description": "Blank staff paper.", "specs": {"staves": "12", "pages": "100"}},
        "stock": 75,
        "category": {"main": "Books", "sub": "Music"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Sewing Kit Mini",
        "sku": "CLO-ACC-9065",
        "price": Decimal128("6.00"),
        "details": {"description": "Travel repair set.", "specs": {"threads": "6 colors", "needles": "Included"}},
        "stock": 300,
        "category": {"main": "Clothing", "sub": "Tools"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Phone Stand Ring",
        "sku": "ELE-ACC-9066",
        "price": Decimal128("5.00"),
        "details": {"description": "Adhesive finger holder.", "specs": {"metal": "Zinc", "rotate": "360"}},
        "stock": 450,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Sink Stopper",
        "sku": "HOM-KIT-9067",
        "price": Decimal128("4.00"),
        "details": {"description": "Rubber drain plug.", "specs": {"size": "Universal", "chain": "Yes"}},
        "stock": 200,
        "category": {"main": "Home & Kitchen", "sub": "Sink"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 12)
    },
    {
        "_id": ObjectId(),
        "name": "Referee Card Set",
        "sku": "SPO-SOC-9068",
        "price": Decimal128("5.00"),
        "details": {"description": "Red and yellow cards.", "specs": {"wallet": "Vinyl", "pencil": "Yes"}},
        "stock": 110,
        "category": {"main": "Sports", "sub": "Soccer"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Correction Tape",
        "sku": "BOO-STA-9069",
        "price": Decimal128("3.00"),
        "details": {"description": "White out roller.", "specs": {"length": "8m", "dry": "Instant"}},
        "stock": 600,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Shirt Buttons",
        "sku": "CLO-ACC-9070",
        "price": Decimal128("2.00"),
        "details": {"description": "Spare sewing buttons.", "specs": {"pack": "20", "color": "Clear"}},
        "stock": 800,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(2, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Battery CR2032",
        "sku": "ELE-ACC-9071",
        "price": Decimal128("5.00"),
        "details": {"description": "Coin cell lithium battery.", "specs": {"pack": "5", "volts": "3V"}},
        "stock": 500,
        "category": {"main": "Electronics", "sub": "Accessories"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Cupcake Liners",
        "sku": "HOM-KIT-9072",
        "price": Decimal128("4.00"),
        "details": {"description": "Paper baking cups.", "specs": {"count": "100", "color": "White"}},
        "stock": 350,
        "category": {"main": "Home & Kitchen", "sub": "Bakeware"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 11)
    },
    {
        "_id": ObjectId(),
        "name": "Whistle Guard",
        "sku": "SPO-PRO-9073",
        "price": Decimal128("2.00"),
        "details": {"description": "Hygiene cover for whistle.", "specs": {"material": "Rubber", "color": "Black"}},
        "stock": 400,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(1, 2)
    },
    {
        "_id": ObjectId(),
        "name": "Staples Box",
        "sku": "BOO-STA-9074",
        "price": Decimal128("3.00"),
        "details": {"description": "Standard size staples.", "specs": {"count": "1000", "size": "26/6"}},
        "stock": 700,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(4, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Boot Laces",
        "sku": "CLO-ACC-9075",
        "price": Decimal128("6.00"),
        "details": {"description": "Heavy duty round laces.", "specs": {"length": "60 inch", "color": "Brown"}},
        "stock": 250,
        "category": {"main": "Clothing", "sub": "Shoe Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Dust Blower",
        "sku": "ELE-CLN-9076",
        "price": Decimal128("7.00"),
        "details": {"description": "Manual air cleaner bulb.", "specs": {"tip": "Metal", "body": "Rubber"}},
        "stock": 120,
        "category": {"main": "Electronics", "sub": "Cleaning"},
        "vendor": {"companyName": vendors[0]["companyName"], "contactEmail": vendors[0]["contactEmail"], "supportPhone": vendors[0]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Melon Baller",
        "sku": "HOM-KIT-9077",
        "price": Decimal128("6.00"),
        "details": {"description": "Fruit scooping tool.", "specs": {"ends": "Dual", "material": "Steel"}},
        "stock": 160,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[1]["companyName"], "contactEmail": vendors[1]["contactEmail"], "supportPhone": vendors[1]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Score Counter",
        "sku": "SPO-GOL-9078",
        "price": Decimal128("5.00"),
        "details": {"description": "Handheld clicker counter.", "specs": {"digits": "4", "reset": "Knob"}},
        "stock": 200,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[2]["companyName"], "contactEmail": vendors[2]["contactEmail"], "supportPhone": vendors[2]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Envelope Pack",
        "sku": "BOO-STA-9079",
        "price": Decimal128("4.00"),
        "details": {"description": "White mailing envelopes.", "specs": {"count": "50", "size": "DL"}},
        "stock": 450,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[3]["companyName"], "contactEmail": vendors[3]["contactEmail"], "supportPhone": vendors[3]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Collar Extender",
        "sku": "CLO-ACC-9080",
        "price": Decimal128("3.00"),
        "details": {"description": "Elastic neck button loop.", "specs": {"pack": "5", "metal": "Zinc"}},
        "stock": 300,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[4]["companyName"], "contactEmail": vendors[4]["contactEmail"], "supportPhone": vendors[4]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Keycap Removal Tool",
        "sku": "ELE-ACC-9081",
        "price": Decimal128("2.00"),
        "details": {"description": "Simple plastic puller.", "specs": {"color": "Red", "fit": "Cherry"}},
        "stock": 600,
        "category": {"main": "Electronics", "sub": "Tools"},
        "vendor": {"companyName": vendors[5]["companyName"], "contactEmail": vendors[5]["contactEmail"], "supportPhone": vendors[5]["supportPhone"]},
        "reviews": createReviews(3, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Toothpick Holder",
        "sku": "HOM-KIT-9082",
        "price": Decimal128("4.00"),
        "details": {"description": "Pocket travel case.", "specs": {"material": "Wood", "capacity": "20"}},
        "stock": 250,
        "category": {"main": "Home & Kitchen", "sub": "Tableware"},
        "vendor": {"companyName": vendors[6]["companyName"], "contactEmail": vendors[6]["contactEmail"], "supportPhone": vendors[6]["supportPhone"]},
        "reviews": createReviews(5, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Shoe Spike Key",
        "sku": "SPO-ACC-9083",
        "price": Decimal128("3.00"),
        "details": {"description": "Wrench for track spikes.", "specs": {"handle": "T-Shape", "metal": "Steel"}},
        "stock": 150,
        "category": {"main": "Sports", "sub": "Accessories"},
        "vendor": {"companyName": vendors[7]["companyName"], "contactEmail": vendors[7]["contactEmail"], "supportPhone": vendors[7]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Push Pins",
        "sku": "BOO-STA-9084",
        "price": Decimal128("2.00"),
        "details": {"description": "Clear board tacks.", "specs": {"box": "100", "head": "Plastic"}},
        "stock": 550,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[8]["companyName"], "contactEmail": vendors[8]["contactEmail"], "supportPhone": vendors[8]["supportPhone"]},
        "reviews": createReviews(2, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Bra Strap Holder",
        "sku": "CLO-ACC-9085",
        "price": Decimal128("2.00"),
        "details": {"description": "Clip to hide straps.", "specs": {"shape": "Oval", "color": "Clear"}},
        "stock": 400,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[9]["companyName"], "contactEmail": vendors[9]["contactEmail"], "supportPhone": vendors[9]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Audio Jack Adapter",
        "sku": "ELE-AUD-9086",
        "price": Decimal128("3.00"),
        "details": {"description": "6.35mm to 3.5mm plug.", "specs": {"plated": "Gold", "stereo": "Yes"}},
        "stock": 350,
        "category": {"main": "Electronics", "sub": "Adapters"},
        "vendor": {"companyName": vendors[10]["companyName"], "contactEmail": vendors[10]["contactEmail"], "supportPhone": vendors[10]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Corn Skewers",
        "sku": "HOM-KIT-9087",
        "price": Decimal128("3.00"),
        "details": {"description": "Holders for corn on cob.", "specs": {"pack": "8", "pins": "Interlock"}},
        "stock": 180,
        "category": {"main": "Home & Kitchen", "sub": "Utensils"},
        "vendor": {"companyName": vendors[11]["companyName"], "contactEmail": vendors[11]["contactEmail"], "supportPhone": vendors[11]["supportPhone"]},
        "reviews": createReviews(5, 10)
    },
    {
        "_id": ObjectId(),
        "name": "Nose Plugs",
        "sku": "SPO-SWI-9088",
        "price": Decimal128("2.00"),
        "details": {"description": "Swimming nose clip.", "specs": {"strap": "No", "color": "Beige"}},
        "stock": 250,
        "category": {"main": "Sports", "sub": "Swimming"},
        "vendor": {"companyName": vendors[12]["companyName"], "contactEmail": vendors[12]["contactEmail"], "supportPhone": vendors[12]["supportPhone"]},
        "reviews": createReviews(1, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Rubber Bands",
        "sku": "BOO-STA-9089",
        "price": Decimal128("2.00"),
        "details": {"description": "Assorted elastic bands.", "specs": {"weight": "100g", "color": "Tan"}},
        "stock": 600,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[13]["companyName"], "contactEmail": vendors[13]["contactEmail"], "supportPhone": vendors[13]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Zipper Pull Tab",
        "sku": "CLO-ACC-9090",
        "price": Decimal128("1.00"),
        "details": {"description": "Replacement zipper head.", "specs": {"material": "Metal", "color": "Silver"}},
        "stock": 500,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[14]["companyName"], "contactEmail": vendors[14]["contactEmail"], "supportPhone": vendors[14]["supportPhone"]},
        "reviews": createReviews(3, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Cable Spiral Wrap",
        "sku": "ELE-ORG-9091",
        "price": Decimal128("4.00"),
        "details": {"description": "Cord bundling tube.", "specs": {"length": "2m", "diameter": "10mm"}},
        "stock": 220,
        "category": {"main": "Electronics", "sub": "Organization"},
        "vendor": {"companyName": vendors[15]["companyName"], "contactEmail": vendors[15]["contactEmail"], "supportPhone": vendors[15]["supportPhone"]},
        "reviews": createReviews(4, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Bag Tie Twist",
        "sku": "HOM-STO-9092",
        "price": Decimal128("1.00"),
        "details": {"description": "Paper wire ties.", "specs": {"count": "100", "length": "4 inch"}},
        "stock": 800,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[16]["companyName"], "contactEmail": vendors[16]["contactEmail"], "supportPhone": vendors[16]["supportPhone"]},
        "reviews": createReviews(5, 9)
    },
    {
        "_id": ObjectId(),
        "name": "Dart Sharpener",
        "sku": "SPO-GAM-9093",
        "price": Decimal128("3.00"),
        "details": {"description": "Round stone for tips.", "specs": {"shape": "Cylinder", "case": "Keyring"}},
        "stock": 150,
        "category": {"main": "Sports", "sub": "Games"},
        "vendor": {"companyName": vendors[17]["companyName"], "contactEmail": vendors[17]["contactEmail"], "supportPhone": vendors[17]["supportPhone"]},
        "reviews": createReviews(1, 3)
    },
    {
        "_id": ObjectId(),
        "name": "Chalk White",
        "sku": "BOO-EDU-9094",
        "price": Decimal128("2.00"),
        "details": {"description": "Blackboard chalk sticks.", "specs": {"box": "12", "dustless": "Yes"}},
        "stock": 400,
        "category": {"main": "Books", "sub": "Education"},
        "vendor": {"companyName": vendors[18]["companyName"], "contactEmail": vendors[18]["contactEmail"], "supportPhone": vendors[18]["supportPhone"]},
        "reviews": createReviews(2, 5)
    },
    {
        "_id": ObjectId(),
        "name": "Shirt Pin",
        "sku": "CLO-ACC-9095",
        "price": Decimal128("1.00"),
        "details": {"description": "Straight pins for sewing.", "specs": {"head": "Pearl", "count": "40"}},
        "stock": 600,
        "category": {"main": "Clothing", "sub": "Tools"},
        "vendor": {"companyName": vendors[19]["companyName"], "contactEmail": vendors[19]["contactEmail"], "supportPhone": vendors[19]["supportPhone"]},
        "reviews": createReviews(3, 7)
    },
    {
        "_id": ObjectId(),
        "name": "Phone Sim Pin",
        "sku": "ELE-ACC-9096",
        "price": Decimal128("0.50"),
        "details": {"description": "Ejector tool key.", "specs": {"material": "Metal", "pack": "2"}},
        "stock": 1000,
        "category": {"main": "Electronics", "sub": "Tools"},
        "vendor": {"companyName": vendors[20]["companyName"], "contactEmail": vendors[20]["contactEmail"], "supportPhone": vendors[20]["supportPhone"]},
        "reviews": createReviews(4, 6)
    },
    {
        "_id": ObjectId(),
        "name": "Bottle Cap Spare",
        "sku": "HOM-STO-9097",
        "price": Decimal128("0.50"),
        "details": {"description": "Replacement screw lid.", "specs": {"size": "28mm", "color": "White"}},
        "stock": 500,
        "category": {"main": "Home & Kitchen", "sub": "Storage"},
        "vendor": {"companyName": vendors[21]["companyName"], "contactEmail": vendors[21]["contactEmail"], "supportPhone": vendors[21]["supportPhone"]},
        "reviews": createReviews(5, 8)
    },
    {
        "_id": ObjectId(),
        "name": "Valve Cap Bike",
        "sku": "SPO-CYC-9098",
        "price": Decimal128("0.50"),
        "details": {"description": "Plastic tire dust cover.", "specs": {"type": "Schrader", "color": "Black"}},
        "stock": 800,
        "category": {"main": "Sports", "sub": "Cycling"},
        "vendor": {"companyName": vendors[22]["companyName"], "contactEmail": vendors[22]["contactEmail"], "supportPhone": vendors[22]["supportPhone"]},
        "reviews": createReviews(1, 2)
    },
    {
        "_id": ObjectId(),
        "name": "Paper Clip Jumbo",
        "sku": "BOO-STA-9099",
        "price": Decimal128("1.00"),
        "details": {"description": "Large wire clips.", "specs": {"size": "50mm", "count": "20"}},
        "stock": 450,
        "category": {"main": "Books", "sub": "Stationery"},
        "vendor": {"companyName": vendors[23]["companyName"], "contactEmail": vendors[23]["contactEmail"], "supportPhone": vendors[23]["supportPhone"]},
        "reviews": createReviews(2, 4)
    },
    {
        "_id": ObjectId(),
        "name": "Safety Pin Small",
        "sku": "CLO-ACC-9100",
        "price": Decimal128("0.50"),
        "details": {"description": "Mini steel pins.", "specs": {"size": "19mm", "pack": "10"}},
        "stock": 900,
        "category": {"main": "Clothing", "sub": "Accessories"},
        "vendor": {"companyName": vendors[24]["companyName"], "contactEmail": vendors[24]["contactEmail"], "supportPhone": vendors[24]["supportPhone"]},
        "reviews": createReviews(3, 5)
    },
    
]

# ramas la 900 din Gemini + inca vreo 200 din copilot = 1100

result = productsCollection.insert_many(products)
print(f"✓ {len(result.inserted_ids)} unique products added successfully")

closeConnection(mongoClient)
