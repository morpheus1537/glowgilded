# Each post: slug, title, desc, image (in assets/), date, body(aff, btn) -> HTML string.
# aff(key, text) makes a sponsored affiliate link; btn(key) makes a button. Keys are in build.py (P dict).

def cozy(aff, btn): return f"""
<p>Some gifts get opened, admired, and tucked in a drawer. Cozy gifts are different: they get used every single evening. A soft throw on the couch, a candle that smells like the season, a string of warm lights in a dark corner. None of them cost much, and all of them change how a room feels after sunset.</p>
<p>This list is for the people on your list who love being home: your mom, your sister, the coworker who always has a blanket on her chair, the friend who just moved into her first apartment. Every pick here is <strong>under $30</strong> at the time of writing (prices on Amazon move around, especially in November, so check before you buy), and every one has thousands of reviews behind it.</p>

<h2>1. A sherpa throw that feels far more expensive than it is</h2>
<p>If you only buy one thing from this list, make it the {aff('sherpa','Bedsure Sherpa Throw')}. It's flannel on one side and fluffy sherpa on the other, so it's warm without being heavy, and it comes in dozens of colors. Cream, oatmeal, and sage are the easiest to match with almost any couch.</p>
<p>Why it works as a gift: everyone has a spot where they curl up, and almost nobody buys themselves a nice throw. Reviewers say it holds up well in the wash. Use cold water and a low dryer setting to keep the sherpa side soft.</p>
{btn('sherpa')}

<h2>2. The candle that smells exactly like Christmas</h2>
<p>The {aff('yankee','Yankee Candle Balsam &amp; Cedar')} is the scent of a real tree in a warm living room: fir, cedar, and a little juniper, without the sugary edge some holiday candles have. Yankee's jars throw scent across a whole room, so it's a good pick for someone with an artificial tree who misses the smell.</p>
<p class="tip"><strong>Gift tip:</strong> tie a sprig of real rosemary or a cinnamon stick to the lid with twine. It costs nothing and makes the gift look hand-picked.</p>
{btn('yankee')}

<h2>3. Fairy lights for any dark corner</h2>
<p>A set of {aff('lights','Minetom Fairy Lights')} is the cheapest way we know to make a room feel cozy. Wrap them around a mirror, drape them over a bookshelf, or stuff them into a big glass jar for an instant lantern. The warm white color is the one to get; cool white looks clinical.</p>
<p>These are an easy add-on gift, or pair two sets with the throw for a "cozy night in" bundle that still comes in close to the budget.</p>
{btn('lights')}

<h2>4. Flameless candles for homes with kids or pets</h2>
<p>Real candles aren't for everyone. If your recipient has a toddler, a curious cat, or a landlord with strict rules, {aff('flameless','Homemory Flameless Candles')} give the same flicker with no flame. They come with a remote and a timer, so they can switch on every evening without anyone remembering to do it. That's the feature reviewers love most.</p>
<p>They look most convincing grouped in threes at different heights, on a tray or inside a fireplace that doesn't get used.</p>
{btn('flameless')}

<h2>5. A small diffuser for a calmer room</h2>
<p>The {aff('diffuser','InnoGear Diffuser')} is a simple, quiet essential oil diffuser with a soft color light. It's a great desk or bedside gift, especially for someone who works from home or has trouble winding down. It shuts off automatically when the water runs out, which matters if it's running overnight.</p>
<p>Add a small bottle of lavender or eucalyptus oil and you've got a complete gift.</p>
{btn('diffuser')}

<h2>How to put together a cozy gift basket</h2>
<p>Any two or three items from this list make a lovely basket. Here are combinations that work well:</p>
<ul>
<li><strong>The movie night:</strong> sherpa throw + fairy lights + a bag of their favorite popcorn.</li>
<li><strong>The calm evening:</strong> diffuser + flameless candles + a herbal tea sampler.</li>
<li><strong>The Christmas smell:</strong> balsam candle + a pine cone or two from outside + a handwritten tag.</li>
</ul>
<p>Use a simple woven basket or a cardboard box lined with tissue paper. Roll the throw instead of folding it so it stands up in the back, then put the smaller items in front. A little twine and a paper tag finish it off without needing any wrapping paper.</p>

<h2>A few honest notes before you order</h2>
<p>Holiday shipping gets slow in December, so order by early in the month if you're mailing gifts on. Candle scents are personal: if you're not sure, the flameless set is the safer choice. And colors on screens vary, so neutral throws are less risky than bright ones for someone whose home you haven't seen.</p>
<p>Cozy gifts don't need to be big. They just need to be something your person will reach for on a cold night and think of you.</p>
"""

def homeowner(aff, btn): return f"""
<p>Housewarming gifts have a reputation problem. Most of them are decorative signs that say "Home Sweet Home" and end up in a closet. New homeowners have just spent more money than they've ever spent at once, and their new place is full of boxes. What they need are things that make the first few months easier and help the space feel like theirs.</p>
<p>This guide is for anyone who just bought or moved: your friend with the new keys, the couple in their first apartment together, your kid who finally has a lease in their own name. Each pick is practical, well reviewed, and nice enough to give.</p>

<h2>1. A two-tier lazy Susan for the pantry or under the sink</h2>
<p>This is the gift people don't know they want until they have it. The {aff('lazy','Amazon Basics 2-Tier Lazy Susan')} turns a deep cabinet, where things disappear into the back, into storage they can actually use. Spin it, and the spices, oils, or cleaning sprays are right there.</p>
<p>It works in the pantry, under the bathroom sink, on a fridge shelf, or on a desk for craft supplies. New homes almost always come with awkward corner cabinets, and this is the easiest fix. It's a modest gift, so it pairs well with something more personal.</p>
{btn('lazy')}

<h2>2. A charcuterie board set for their first time hosting</h2>
<p>New homeowners host. It might be a housewarming, a first Thanksgiving, or friends dropping by to see the place. The {aff('board','Shanik Charcuterie Board Set')} is the splurge pick on this list and it's worth it. It's a bamboo board with a slide-out drawer of cheese knives and small serving pieces, so it's a whole hosting kit in one box.</p>
<p>It looks good left out on a kitchen counter, which matters in a new place that still feels a little empty. If you're going in on a gift with a few friends, this is the one to choose.</p>
{btn('board')}

<h2>3. A reed diffuser so the house smells like home</h2>
<p>Every house has a smell when you first move in: fresh paint, old carpet, the previous owners' cooking. A {aff('reed','Cocorrína Reed Diffuser')} quietly takes care of that with no flame, no plug, and nothing to remember. The bottle is pretty enough for a bathroom counter or an entryway table, so it doubles as decor.</p>
<p>It's one of the best-looking gifts under $20 we've found, and it's an easy choice when you don't know someone's style well.</p>
{btn('reed')}

<h2>4. Flameless candles for the first cozy nights</h2>
<p>The first weeks in a new place can feel bare, with too much overhead light and not enough warmth. {aff('flameless','Homemory Flameless Candles')} fix that right away. They have a timer and a remote, they're safe around moving boxes and pets, and they make an empty fireplace or windowsill look intentional.</p>
<p>They're especially good for renters, since many leases ban open flames.</p>
{btn('flameless')}

<h2>5. A throw for the couch they just hauled up the stairs</h2>
<p>A new couch, or an old couch in a new room, looks better with a throw over the arm. The {aff('sherpa','Bedsure Sherpa Throw')} comes in plenty of neutral shades and is the softest thing in its price range. It's also good for the first nights in a house where the heating hasn't been figured out yet.</p>
{btn('sherpa')}

<h2>How to choose for your new homeowner</h2>
<ul>
<li><strong>For the organizer:</strong> the lazy Susan, plus a label maker if you want to go further.</li>
<li><strong>For the host:</strong> the charcuterie set with a nice bottle of wine or a wedge of good cheese.</li>
<li><strong>For the first-time renter:</strong> the reed diffuser and flameless candles, both lease-friendly.</li>
<li><strong>For the couple:</strong> the throw and the board together, one cozy gift and one for hosting.</li>
</ul>

<h2>What to skip</h2>
<p>Hold off on big decor like art, rugs, and wall shelves unless you know their taste really well. People need time in a space before they know what it needs. Skip anything that has to be mounted to a wall, too, since renters often can't drill. Useful, good-looking, easy-to-keep gifts are always welcome.</p>
<p>Finally, include a card with something practical: your number for when they need help moving a dresser, or a list of the best takeout near their new place. That's often the part they remember.</p>
"""

def stocking(aff, btn): return f"""
<p>Stocking stuffers are harder than big gifts. They have to be small, cheap, and still feel like a treat, not just filler. The best ones are little upgrades to everyday life that people rarely buy for themselves.</p>
<p>These picks are all <strong>under $20</strong> at the time of writing and work for anyone who loves their home: parents, roommates, in-laws, the friend who already has everything. They also double as Secret Santa and white elephant gifts that people will actually fight over.</p>

<h2>1. Fairy lights, the stocking stuffer everyone uses</h2>
<p>A set of {aff('lights','Minetom Fairy Lights')} folds down small enough to fit in a stocking, and it's useful all year. Most people put them up for Christmas and then keep them on a headboard, a bookshelf, or a balcony railing long after the tree comes down.</p>
<p class="tip"><strong>Idea:</strong> tuck the lights into a small mason jar with a ribbon around the lid. That's a lantern and a gift in one.</p>
{btn('lights')}

<h2>2. A mini diffuser for the desk</h2>
<p>The {aff('diffuser','InnoGear Diffuser')} is small, quiet, and simple to use. Fill it with water and a few drops of oil, then press one button. It's perfect for a home office, dorm room, or nightstand. The soft color-changing light makes it a gentle nightlight for kids' rooms, too.</p>
<p>It's slightly bigger than a typical stocking stuffer, so set it at the front of the stocking or under the tree with the rest of the stocking gifts.</p>
{btn('diffuser')}

<h2>3. A reed diffuser that looks like a little luxury</h2>
<p>A {aff('reed','Cocorrína Reed Diffuser')} feels like something from a boutique. The bottle is pretty, the reeds come in a neat bundle, and it scents a bathroom or small room for weeks with no effort. It's an especially good gift for someone who likes candles but doesn't like keeping an eye on a flame.</p>
{btn('reed')}

<h2>4. A two-tier lazy Susan for the practical one</h2>
<p>Every family has the person who'd rather get something useful. For them, the {aff('lazy','Amazon Basics 2-Tier Lazy Susan')} is a surprisingly satisfying gift. It organizes spices, skincare, or cleaning supplies and fits into a cabinet in seconds. It won't fit inside a stocking, but it's a perfect "and one more thing" gift beside it.</p>
{btn('lazy')}

<h2>5. A classic holiday candle</h2>
<p>Candles are classic stocking stuffers for good reason. A {aff('yankee','Yankee Candle Balsam &amp; Cedar')} brings the smell of a real Christmas tree into the room, and it's one of the most popular holiday scents for good reason. If the large jar is outside your budget, look for the smaller sizes on the same listing.</p>
{btn('yankee')}

<h2>How to fill a stocking without overspending</h2>
<p>A good stocking has a rhythm: one "main" item, two or three small useful things, and something to eat. Try this formula:</p>
<ul>
<li><strong>Main item:</strong> fairy lights or a reed diffuser.</li>
<li><strong>Useful extras:</strong> fuzzy socks, a nice pen, lip balm, a small notebook.</li>
<li><strong>Treat:</strong> a chocolate orange, hot cocoa packets, or their favorite candy.</li>
</ul>
<p>Put the main item in first so it sits at the bottom and becomes the last surprise. Put candy at the top, because people always reach in for that first.</p>

<h2>Stocking stuffers for specific people</h2>
<ul>
<li><strong>For the college student:</strong> the mini diffuser. It's dorm-safe, unlike real candles.</li>
<li><strong>For Mom:</strong> the reed diffuser and a handwritten note.</li>
<li><strong>For the roommate:</strong> fairy lights for their room.</li>
<li><strong>For Dad, or the hard-to-shop-for:</strong> the lazy Susan. Practical people love practical gifts.</li>
</ul>

<h2>Order early</h2>
<p>Small, cheap items tend to sell out or get slow shipping close to Christmas, so it's worth grabbing stocking stuffers in November. Lights and diffusers also make great teacher, neighbor, and mail-carrier gifts, so buy one or two extra to keep on hand for last-minute gifts.</p>
<p>The best stocking stuffers say "I thought about you" in a small way. Each one on this list does that and gets used well past December.</p>
"""

POSTS = [
 dict(slug="cozy-christmas-gifts-under-30", title="Cozy Christmas Gifts Under $30 for the Home",
      desc="Warm, well-reviewed Christmas gifts under $30: a sherpa throw, a Christmas-scented candle, fairy lights, flameless candles and a diffuser.",
      image="assets/home/1-cozy-gifts-under-30.jpg", date="October 28, 2026", body=cozy),
 dict(slug="gifts-for-new-homeowners", title="Gifts for New Homeowners They'll Actually Use",
      desc="Practical, pretty housewarming gifts new homeowners will use: storage, hosting, scent and cozy finds.",
      image="assets/home/2-new-homeowners.jpg", date="October 28, 2026", body=homeowner),
 dict(slug="stocking-stuffers-under-20", title="Stocking Stuffers Under $20 for Home Lovers",
      desc="Small, useful stocking stuffers under $20 for anyone who loves their home: lights, diffusers, candles and clever storage.",
      image="assets/home/3-stocking-stuffers.jpg", date="October 28, 2026", body=stocking),
]
