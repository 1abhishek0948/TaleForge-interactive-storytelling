# from django.contrib.auth import get_user_model
# from django.core.management.base import BaseCommand
# from stories.models import Choice, Story, StoryNode

# class Command(BaseCommand):
#     help = "Seed example interactive stories"

#     def handle(self, *args, **options):
#         user_model = get_user_model()
#         author, created = user_model.objects.get_or_create(
#             username="demo_author",
#             defaults={"email": "author@example.com"},
#         )
#         if created or not author.check_password("demoxyz12@"):
#             author.set_password("demoxyz12@")
#             author.save(update_fields=["password"])

#         seeded_count = 0

#         # Register your stories here
#         story_seeders = [
#             ("The Neon Vault", self._create_neon_vault),
#             ("Forest of Echoes", self._create_forest_echo),
#             ("The Clockwork Lighthouse", self._create_clockwork_lighthouse),
#             ("The Sunken Relay", self._create_sunken_relay),
#             ("The Last Monsoon Train", self._create_last_monsoon_train),
#         ]

#         for story_title, seeder in story_seeders:
#             if Story.objects.filter(title=story_title).exists():
#                 self.stdout.write(self.style.WARNING(f"Story already exists: {story_title}. Skipping."))
#                 continue
            
#             seeder(author)
#             seeded_count += 1
#             self.stdout.write(self.style.SUCCESS(f"Seeded story: {story_title}."))

#         if seeded_count == 0:
#             self.stdout.write(self.style.WARNING("No new stories were seeded."))
#         else:
#             story_word = "story" if seeded_count == 1 else "stories"
#             self.stdout.write(self.style.SUCCESS(f"Seeding complete. Added {seeded_count} new {story_word}."))

#     # --- STORY 1: NEON VAULT ---
#     def _create_neon_vault(self, author):
#         story = Story.objects.create(
#             creator=author,
#             title="The Neon Vault",
#             description="A cyberpunk heist where every choice shifts your fate.",
#             is_published=True,
#         )

#         n1 = StoryNode.objects.create(story=story, node_key="start", title="Rooftop Arrival", content="Rain hammers the skyline as you crouch above the Neon Vault. A maintenance hatch glows below.")
#         n2 = StoryNode.objects.create(story=story, node_key="hatch", title="Quiet Entry", content="You slip into a dim service corridor. Security drones hum in the distance.")
#         n3 = StoryNode.objects.create(story=story, node_key="front", title="Bold Entrance", content="You walk through the front gate with forged credentials. A guard scans your face.")
#         n4 = StoryNode.objects.create(story=story, node_key="vault", title="The Core Vault", content="The data core floats behind laser grids. You have one shot.", is_ending=True)
#         n5 = StoryNode.objects.create(story=story, node_key="caught", title="Mission Failed", content="The alarm detonates in your ears. Floodlights trap you in white fire.", is_ending=True)

#         Choice.objects.bulk_create([
#             Choice(node=n1, text="Drop through the maintenance hatch", next_node=n2, order=1),
#             Choice(node=n1, text="Approach the front gate in disguise", next_node=n3, order=2),
#             Choice(node=n2, text="Bypass drones and push for the vault", next_node=n4, order=1),
#             Choice(node=n2, text="Trigger a decoy explosion", next_node=n5, order=2),
#             Choice(node=n3, text="Bluff the guard with confidence", next_node=n4, order=1),
#             Choice(node=n3, text="Run before the scanner completes", next_node=n5, order=2),
#         ])

#         story.starting_node = n1
#         story.save(update_fields=["starting_node"])

#     # --- STORY 2: FOREST OF ECHOES ---
#     def _create_forest_echo(self, author):
#         story = Story.objects.create(
#             creator=author,
#             title="Forest of Echoes",
#             description="An ancient forest remembers every traveler.",
#             is_published=True,
#         )

#         s1 = StoryNode.objects.create(story=story, node_key="start", title="Crossroads", content="A fork divides the misty trail: one path lined with lanterns, the other swallowed by roots.")
#         s2 = StoryNode.objects.create(story=story, node_key="lanterns", title="Lantern Path", content="Whispering lights guide you to a stone mirror reflecting a sky you do not know.", is_ending=True)
#         s3 = StoryNode.objects.create(story=story, node_key="roots", title="Root Path", content="The roots twist into an archway. Beyond it, your own voice asks if you wish to return.", is_ending=True)

#         Choice.objects.bulk_create([
#             Choice(node=s1, text="Take the lantern-lit path", next_node=s2, order=1),
#             Choice(node=s1, text="Enter the roots and shadows", next_node=s3, order=2),
#         ])

#         story.starting_node = s1
#         story.save(update_fields=["starting_node"])

#     # --- STORY 3: CLOCKWORK LIGHTHOUSE ---
#     def _create_clockwork_lighthouse(self, author):
#         story = Story.objects.create(
#             creator=author,
#             title="The Clockwork Lighthouse",
#             description="A storm-battered lighthouse hides a machine that can rewrite tides and time.",
#             is_published=True,
#         )

#         c1 = StoryNode.objects.create(story=story, node_key="start", title="Shoreline Arrival", content="Thunder rolls above black waves. The lighthouse door hangs open.")
#         c2 = StoryNode.objects.create(story=story, node_key="workshop", title="Keeper's Workshop", content="Dusty blueprints reveal a tidal engine. A brass key rests here.")
#         c3 = StoryNode.objects.create(story=story, node_key="stairwell", title="Spiral Stairwell", content="You climb toward the lantern room while the stairs shudder.")
#         c4 = StoryNode.objects.create(story=story, node_key="engine", title="Tidal Engine Chamber", content="The engine pulses with cold light. You control the tides.", is_ending=True)
#         c5 = StoryNode.objects.create(story=story, node_key="beacon", title="Lantern of Dawn", content="You reignite the beacon, and the storm breaks into silver rain.", is_ending=True)
#         c6 = StoryNode.objects.create(story=story, node_key="maelstrom", title="The Maelstrom", content="A wrong sequence jolts the machine. The tower vanishes into spray.", is_ending=True)

#         Choice.objects.bulk_create([
#             Choice(node=c1, text="Enter the keeper's workshop", next_node=c2, order=1),
#             Choice(node=c1, text="Climb the spiral stairwell", next_node=c3, order=2),
#             Choice(node=c2, text="Use the brass key on the hatch", next_node=c4, order=1),
#             Choice(node=c2, text="Ignore the key and head to the beacon", next_node=c5, order=2),
#             Choice(node=c3, text="Force the hatch open", next_node=c4, order=1),
#             Choice(node=c3, text="Rush straight to the lantern room", next_node=c6, order=2),
#         ])

#         story.starting_node = c1
#         story.save(update_fields=["starting_node"])

#     # --- NEW STORY 4: THE SUNKEN RELAY ---
#     def _create_sunken_relay(self, author):
#         story = Story.objects.create(
#             creator=author,
#             title="The Sunken Relay",
#             description="A ghost signal leads you to a derelict research station orbiting a dying star.",
#             is_published=True,
#         )

#         r1 = StoryNode.objects.create(
#             story=story,
#             node_key="start",
#             title="Airlock Alpha",
#             content="Frost patterns crawl across your visor. The station is silent, save for the hum of failing life support."
#         )
#         r2 = StoryNode.objects.create(
#             story=story,
#             node_key="bridge",
#             title="The Command Bridge",
#             content="The viewports show a collapsing star. The Captain’s terminal is blinking with an unsent SOS."
#         )
#         r3 = StoryNode.objects.create(
#             story=story,
#             node_key="labs",
#             title="Xenobiology Lab",
#             content="Glass canisters lie shattered. Something is breathing behind the specimen freezer."
#         )
#         r4 = StoryNode.objects.create(
#             story=story,
#             node_key="escape",
#             title="The Last Pod",
#             content="You punch the launch sequence as the station buckles. You escape into the void.",
#             is_ending=True
#         )
#         r5 = StoryNode.objects.create(
#             story=story,
#             node_key="consumed",
#             title="The Singularity",
#             content="The signal was a lure. You and the station are pulled into the heart of the star.",
#             is_ending=True
#         )

#         Choice.objects.bulk_create([
#             Choice(node=r1, text="Head to the Command Bridge", next_node=r2, order=1),
#             Choice(node=r1, text="Investigate the Bio-Labs", next_node=r3, order=2),
#             Choice(node=r2, text="Download data and run for the pods", next_node=r4, order=1),
#             Choice(node=r2, text="Try to stabilize the star's core", next_node=r5, order=2),
#             Choice(node=r3, text="Hide and wait for the creature", next_node=r5, order=1),
#             Choice(node=r3, text="Flush the lab and sprint to the exit", next_node=r4, order=2),
#         ])

#         story.starting_node = r1
#         story.save(update_fields=["starting_node"])

#     # --- NEW STORY 5: THE LAST MONSOON TRAIN ---
#     def _create_last_monsoon_train(self, author):
#         story = Story.objects.create(
#             creator=author,
#             title="The Last Monsoon Train",
#             description="A rain-soaked midnight train carries secrets, smugglers, and one missing child.",
#             is_published=True,
#         )

#         t1 = StoryNode.objects.create(
#             story=story,
#             node_key="platform",
#             title="Platform 9, Midnight",
#             content=(
#                 "Monsoon rain drums on the iron roof as the last train to Ketu Valley exhales steam. "
#                 "A mother grabs your sleeve and whispers that her son vanished after boarding coach C."
#             ),
#         )
#         t2 = StoryNode.objects.create(
#             story=story,
#             node_key="coach_c",
#             title="Coach C",
#             content=(
#                 "Lantern lights flicker over wet footprints. A ticket inspector avoids your eyes while "
#                 "a violin case lies open with no instrument inside."
#             ),
#         )
#         t3 = StoryNode.objects.create(
#             story=story,
#             node_key="roof",
#             title="The Train Roof",
#             content=(
#                 "You climb onto the roof. Wind lashes your face and lightning reveals silhouettes moving "
#                 "between carriages with practiced speed."
#             ),
#         )
#         t4 = StoryNode.objects.create(
#             story=story,
#             node_key="dining_car",
#             title="Dining Car",
#             content=(
#                 "A silent card game pauses when you enter. Under the table, you spot a toy compass "
#                 "with the missing boy's initials carved into it."
#             ),
#         )
#         t5 = StoryNode.objects.create(
#             story=story,
#             node_key="engine",
#             title="Engine Cabin",
#             content=(
#                 "The driver swears he saw someone uncouple the rear wagons. Ahead, the mountain tunnel "
#                 "narrows and flooding has already begun."
#             ),
#         )
#         t6 = StoryNode.objects.create(
#             story=story,
#             node_key="cargo_hold",
#             title="Sealed Cargo Hold",
#             content=(
#                 "You break the seal and find crates of medicine, forged manifests, and a hidden compartment "
#                 "where the child is tied but conscious."
#             ),
#         )
#         t7 = StoryNode.objects.create(
#             story=story,
#             node_key="rescue",
#             title="Bridge Before Dawn",
#             content=(
#                 "You pull the emergency brake, evacuate the rear coaches, and carry the child across the bridge "
#                 "as rain thins into morning mist. The smuggling ring is exposed.",
#             ),
#             is_ending=True,
#         )
#         t8 = StoryNode.objects.create(
#             story=story,
#             node_key="washout",
#             title="River Washout",
#             content=(
#                 "You hesitate too long. The rear wagons hit a washed-out section and vanish into the river "
#                 "below. The truth is buried with them.",
#             ),
#             is_ending=True,
#         )
#         t9 = StoryNode.objects.create(
#             story=story,
#             node_key="deal",
#             title="An Offer in the Dark",
#             content=(
#                 "The ring leader offers money and silence. You accept, step off at the next stop, and "
#                 "live with the weight of that night forever.",
#             ),
#             is_ending=True,
#         )

#         Choice.objects.bulk_create([
#             Choice(node=t1, text="Search coach C immediately", next_node=t2, order=1),
#             Choice(node=t1, text="Climb to the roof and track movement", next_node=t3, order=2),
#             Choice(node=t1, text="Interview passengers in the dining car", next_node=t4, order=3),
#             Choice(node=t2, text="Confront the ticket inspector", next_node=t4, order=1),
#             Choice(node=t2, text="Push forward to the engine cabin", next_node=t5, order=2),
#             Choice(node=t3, text="Drop into the cargo section", next_node=t6, order=1),
#             Choice(node=t3, text="Follow silhouettes toward the engine", next_node=t5, order=2),
#             Choice(node=t4, text="Use the toy compass clue to locate hidden cargo", next_node=t6, order=1),
#             Choice(node=t4, text="Take the ring leader's offered deal", next_node=t9, order=2),
#             Choice(node=t5, text="Force an emergency stop before the bridge", next_node=t7, order=1),
#             Choice(node=t5, text="Keep speed and hope to outrun the flood", next_node=t8, order=2),
#             Choice(node=t6, text="Free the child and signal the engine crew", next_node=t7, order=1),
#             Choice(node=t6, text="Wait for backup and stay hidden", next_node=t8, order=2),
#         ])

#         story.starting_node = t1
#         story.save(update_fields=["starting_node"])

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from stories.models import Choice, Story, StoryNode

class Command(BaseCommand):
    help = "Seed real-world historical and fictional interactive stories"

    def handle(self, *args, **options):
        user_model = get_user_model()
        author = self._ensure_default_users(user_model)

        seeded_count = 0

        # Story Registry
        story_seeders = [
            ("The Neon Vault", self._create_neon_vault),
            ("Forest of Echoes", self._create_forest_echo),
            ("The Clockwork Lighthouse", self._create_clockwork_lighthouse),
            ("The Sunken Relay", self._create_sunken_relay),
            ("The Last Monsoon Train", self._create_last_monsoon_train),
            ("The Endurance Expedition", self._create_shackleton_expedition),
            ("The Ghost of the Mary Celeste", self._create_mary_celeste),
        ]

        for story_title, seeder in story_seeders:
            if Story.objects.filter(title=story_title).exists():
                self.stdout.write(self.style.WARNING(f"Story already exists: {story_title}. Skipping."))
                continue
            
            seeder(author)
            seeded_count += 1
            self.stdout.write(self.style.SUCCESS(f"Seeded story: {story_title}."))

        if seeded_count == 0:
            self.stdout.write(self.style.WARNING("No new stories were seeded."))
        else:
            story_word = "story" if seeded_count == 1 else "stories"
            self.stdout.write(self.style.SUCCESS(f"Seeding complete. Added {seeded_count} new {story_word}."))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Demo login accounts are ready:"))
        self.stdout.write("  demo_user / demoxyz12@")
        self.stdout.write("  moderator_user / moderatorxyz34@")
        self.stdout.write("  admin_user / adminxyz56@")

    def _create_or_update_user(
        self,
        user_model,
        *,
        username: str,
        email: str,
        password: str,
        is_staff: bool = False,
        is_superuser: bool = False,
    ):
        user, _ = user_model.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": is_staff,
                "is_superuser": is_superuser,
            },
        )

        changed = False
        if user.email != email:
            user.email = email
            changed = True
        if user.is_staff != is_staff:
            user.is_staff = is_staff
            changed = True
        if user.is_superuser != is_superuser:
            user.is_superuser = is_superuser
            changed = True
        if not user.check_password(password):
            user.set_password(password)
            changed = True

        if changed:
            user.save()

        return user

    def _ensure_default_users(self, user_model):
        self._create_or_update_user(
            user_model,
            username="demo_user",
            email="demo@example.com",
            password="demoxyz12@",
        )

        moderator_user = self._create_or_update_user(
            user_model,
            username="moderator_user",
            email="moderator@example.com",
            password="moderatorxyz34@",
            is_staff=True,
        )

        admin_user = self._create_or_update_user(
            user_model,
            username="admin_user",
            email="admin@example.com",
            password="adminxyz56@",
            is_staff=True,
            is_superuser=True,
        )

        moderators_group, _ = Group.objects.get_or_create(name="Moderators")
        moderator_user.groups.add(moderators_group)

        admins_group, _ = Group.objects.get_or_create(name="Admins")
        admin_user.groups.add(admins_group)

        return self._create_or_update_user(
            user_model,
            username="demo_author",
            email="author@example.com",
            password="demoxyz12@",
        )

    # --- 1: NEON VAULT (Original) ---
    def _create_neon_vault(self, author):
        story = Story.objects.create(
            creator=author, title="The Neon Vault", is_published=True,
            description="A cyberpunk heist where every choice shifts your fate."
        )
        n1 = StoryNode.objects.create(story=story, node_key="start", title="Rooftop Arrival", content="Rain hammers the skyline as you crouch above the Neon Vault.")
        n2 = StoryNode.objects.create(story=story, node_key="hatch", title="Quiet Entry", content="You slip into a dim service corridor.")
        n3 = StoryNode.objects.create(story=story, node_key="front", title="Bold Entrance", content="You walk through the front gate with forged credentials.")
        n4 = StoryNode.objects.create(story=story, node_key="vault", title="The Core Vault", content="The data core floats behind laser grids.", is_ending=True)
        n5 = StoryNode.objects.create(story=story, node_key="caught", title="Mission Failed", content="Floodlights trap you in white fire.", is_ending=True)

        Choice.objects.bulk_create([
            Choice(node=n1, text="Drop through the maintenance hatch", next_node=n2, order=1),
            Choice(node=n1, text="Approach the front gate in disguise", next_node=n3, order=2),
            Choice(node=n2, text="Bypass drones and push for the vault", next_node=n4, order=1),
            Choice(node=n2, text="Trigger a decoy explosion", next_node=n5, order=2),
            Choice(node=n3, text="Bluff the guard", next_node=n4, order=1),
            Choice(node=n3, text="Run from the scanner", next_node=n5, order=2),
        ])
        story.starting_node = n1
        story.save(update_fields=["starting_node"])

    # --- 2: FOREST OF ECHOES (Original) ---
    def _create_forest_echo(self, author):
        story = Story.objects.create(
            creator=author, title="Forest of Echoes", is_published=True,
            description="An ancient forest remembers every traveler."
        )
        s1 = StoryNode.objects.create(story=story, node_key="start", title="Crossroads", content="A fork divides the misty trail: lanterns or roots?")
        s2 = StoryNode.objects.create(story=story, node_key="lanterns", title="Lantern Path", content="Whispering lights guide you to a stone mirror.", is_ending=True)
        s3 = StoryNode.objects.create(story=story, node_key="roots", title="Root Path", content="Your own voice asks if you wish to return.", is_ending=True)

        Choice.objects.bulk_create([
            Choice(node=s1, text="Take the lantern-lit path", next_node=s2, order=1),
            Choice(node=s1, text="Enter the roots and shadows", next_node=s3, order=2),
        ])
        story.starting_node = s1
        story.save(update_fields=["starting_node"])

    # --- 3: CLOCKWORK LIGHTHOUSE (Original) ---
    def _create_clockwork_lighthouse(self, author):
        story = Story.objects.create(
            creator=author, title="The Clockwork Lighthouse", is_published=True,
            description="A lighthouse that can rewrite tides and time."
        )
        c1 = StoryNode.objects.create(story=story, node_key="start", title="Shoreline Arrival", content="Thunder rolls. The lighthouse door hangs open.")
        c2 = StoryNode.objects.create(story=story, node_key="workshop", title="Keeper's Workshop", content="Blueprints reveal a tidal engine. A brass key rests here.")
        c3 = StoryNode.objects.create(story=story, node_key="stairwell", title="Spiral Stairwell", content="You climb toward the lantern room.")
        c4 = StoryNode.objects.create(story=story, node_key="engine", title="Tidal Engine Chamber", content="The engine pulses. You control the tides.", is_ending=True)
        c5 = StoryNode.objects.create(story=story, node_key="beacon", title="Lantern of Dawn", content="The storm breaks into silver rain.", is_ending=True)
        c6 = StoryNode.objects.create(story=story, node_key="maelstrom", title="The Maelstrom", content="The tower vanishes into spray.", is_ending=True)

        Choice.objects.bulk_create([
            Choice(node=c1, text="Enter the workshop", next_node=c2, order=1),
            Choice(node=c1, text="Climb the stairwell", next_node=c3, order=2),
            Choice(node=c2, text="Use key on hatch", next_node=c4, order=1),
            Choice(node=c2, text="Head to the beacon", next_node=c5, order=2),
            Choice(node=c3, text="Force the hatch", next_node=c4, order=1),
            Choice(node=c3, text="Rush to the lantern room", next_node=c6, order=2),
        ])
        story.starting_node = c1
        story.save(update_fields=["starting_node"])

    # --- 4: THE SUNKEN RELAY (Original) ---
    def _create_sunken_relay(self, author):
        story = Story.objects.create(creator=author, title="The Sunken Relay", is_published=True, description="A ghost signal in deep space.")
        r1 = StoryNode.objects.create(story=story, node_key="start", title="Airlock Alpha", content="Frost patterns crawl across your visor.")
        r2 = StoryNode.objects.create(story=story, node_key="bridge", title="The Bridge", content="Viewports show a collapsing star.")
        r3 = StoryNode.objects.create(story=story, node_key="labs", title="Xenobiology Lab", content="Glass canisters lie shattered.")
        r4 = StoryNode.objects.create(story=story, node_key="escape", title="The Last Pod", content="You escape into the void.", is_ending=True)
        r5 = StoryNode.objects.create(story=story, node_key="consumed", title="The Singularity", content="You are pulled into the star.", is_ending=True)

        Choice.objects.bulk_create([
            Choice(node=r1, text="Head to the Bridge", next_node=r2, order=1),
            Choice(node=r1, text="Investigate Bio-Labs", next_node=r3, order=2),
            Choice(node=r2, text="Run for pods", next_node=r4, order=1),
            Choice(node=r2, text="Stabilize core", next_node=r5, order=2),
            Choice(node=r3, text="Hide", next_node=r5, order=1),
            Choice(node=r3, text="Sprint to exit", next_node=r4, order=2),
        ])
        story.starting_node = r1
        story.save(update_fields=["starting_node"])

    # --- 5: THE LAST MONSOON TRAIN (Original) ---
    def _create_last_monsoon_train(self, author):
        story = Story.objects.create(creator=author, title="The Last Monsoon Train", is_published=True, description="A rain-soaked mystery.")
        t1 = StoryNode.objects.create(story=story, node_key="start", title="Platform 9", content="A mother whispers her son vanished on coach C.")
        t2 = StoryNode.objects.create(story=story, node_key="coach_c", title="Coach C", content="Lantern lights flicker over wet footprints.")
        t3 = StoryNode.objects.create(story=story, node_key="roof", title="The Train Roof", content="Wind lashes your face. Silhouettes move ahead.")
        t4 = StoryNode.objects.create(story=story, node_key="dining_car", title="Dining Car", content="A card game pauses. You spot a toy compass.")
        t5 = StoryNode.objects.create(story=story, node_key="engine", title="Engine Cabin", content="The driver swears someone uncoupled the rear wagons.")
        t6 = StoryNode.objects.create(story=story, node_key="cargo_hold", title="Sealed Cargo Hold", content="You find the missing child tied up.")
        t7 = StoryNode.objects.create(story=story, node_key="rescue", title="Rescue", content="You carry the child across the bridge. The ring is exposed.", is_ending=True)
        t8 = StoryNode.objects.create(story=story, node_key="washout", title="River Washout", content="The wagons vanish into the river. The truth is buried.", is_ending=True)
        t9 = StoryNode.objects.create(story=story, node_key="deal", title="The Deal", content="You take the money and step off at the next stop.", is_ending=True)

        Choice.objects.bulk_create([
            Choice(node=t1, text="Search coach C", next_node=t2, order=1),
            Choice(node=t1, text="Climb to the roof", next_node=t3, order=2),
            Choice(node=t1, text="Go to dining car", next_node=t4, order=3),
            Choice(node=t2, text="Confront inspector", next_node=t4, order=1),
            Choice(node=t2, text="Go to engine", next_node=t5, order=2),
            Choice(node=t3, text="Drop to cargo", next_node=t6, order=1),
            Choice(node=t4, text="Locate hidden cargo", next_node=t6, order=1),
            Choice(node=t4, text="Take the deal", next_node=t9, order=2),
            Choice(node=t5, text="Emergency stop", next_node=t7, order=1),
            Choice(node=t5, text="Outrun flood", next_node=t8, order=2),
            Choice(node=t6, text="Free the child", next_node=t7, order=1),
            Choice(node=t6, text="Wait for backup", next_node=t8, order=2),
        ])
        story.starting_node = t1
        story.save(update_fields=["starting_node"])

    # --- 6: THE ENDURANCE EXPEDITION (New - Real History) ---
    def _create_shackleton_expedition(self, author):
        story = Story.objects.create(
            creator=author, title="The Endurance Expedition", is_published=True,
            description="Lead Shackleton's crew to survival in the frozen Antarctic. Based on a true story."
        )
        n1 = StoryNode.objects.create(story=story, node_key="start", title="The Ice Trap", content="January 1915. Your ship, the Endurance, is locked in pack ice. The hull groans under pressure.")
        n2 = StoryNode.objects.create(story=story, node_key="stay", title="The Ship's Death", content="You stay until the hull snaps. You salvage what you can, but the loss of the galley is a heavy blow.")
        n3 = StoryNode.objects.create(story=story, node_key="abandon", title="Ocean Camp", content="You set up camp on a moving ice floe. Supplies are thin. To the west: open water; east: ice mountains.")
        n4 = StoryNode.objects.create(story=story, node_key="elephant_island", title="Elephant Island", content="Desolate rock. The men are exhausted. Your only hope is an 800-mile journey in a small lifeboat.")
        n5 = StoryNode.objects.create(story=story, node_key="boat_journey", title="The James Caird", content="You sail through hurricane winds. One wrong turn and you are lost in the Southern Ocean.")
        n6 = StoryNode.objects.create(story=story, node_key="rescue", title="The Miracle", content="You reach South Georgia and find help. Every single man is saved. You are a hero.", is_ending=True)
        n7 = StoryNode.objects.create(story=story, node_key="lost", title="Swallowed by the Deep", content="The Southern Ocean is unforgiving. Your boat capsizes. The expedition ends in silence.", is_ending=True)

        Choice.objects.bulk_create([
            Choice(node=n1, text="Stay on the ship to keep morale high", next_node=n2, order=1),
            Choice(node=n1, text="Order immediate evacuation to the ice", next_node=n3, order=2),
            Choice(node=n2, text="Move salvage to the nearest floe", next_node=n3, order=1),
            Choice(node=n3, text="Wait for the ice to drift north", next_node=n4, order=1),
            Choice(node=n4, text="Launch the lifeboat for South Georgia", next_node=n5, order=1),
            Choice(node=n5, text="Navigate by the stars", next_node=n6, order=1),
            Choice(node=n5, text="Try to wait out the storm", next_node=n7, order=2),
        ])
        story.starting_node = n1
        story.save(update_fields=["starting_node"])

    # --- 7: THE GHOST OF THE MARY CELESTE (New - Real History) ---
    def _create_mary_celeste(self, author):
        story = Story.objects.create(
            creator=author, title="The Ghost of the Mary Celeste", is_published=True,
            description="Investigate the 1872 mystery of the ship found adrift with its crew missing."
        )
        m1 = StoryNode.objects.create(story=story, node_key="start", title="Discovery at Sea", content="The Dei Gratia spots a merchant ship drifting. You board the Mary Celeste. The sails are torn, but the log is open.")
        m2 = StoryNode.objects.create(story=story, node_key="logbook", title="The Captain's Table", content="The last entry was 10 days ago. A half-eaten meal sits on the table.")
        m3 = StoryNode.objects.create(story=story, node_key="hold", title="The Cargo Hold", content="You find 1,701 barrels of alcohol. Nine are empty. Fumes linger in the air.")
        m4 = StoryNode.objects.create(story=story, node_key="the_theory", title="The Lifeboat", content="The lifeboat is missing. A frayed rope trails in the water.")
        m5 = StoryNode.objects.create(story=story, node_key="fumes_ending", title="The Panic Theory", content="The alcohol leaked. Fearing an explosion, the crew fled and were lost at sea.", is_ending=True)
        m6 = StoryNode.objects.create(story=story, node_key="mutiny_ending", title="The Darker Path", content="You find bloodstains hidden under a rug. This was a mutiny. You've changed history.", is_ending=True)

        Choice.objects.bulk_create([
            Choice(node=m1, text="Examine the Captain's cabin", next_node=m2, order=1),
            Choice(node=m1, text="Check the main cargo hold", next_node=m3, order=2),
            Choice(node=m2, text="Look for the ship's lifeboat", next_node=m4, order=1),
            Choice(node=m3, text="Inspect the empty barrels", next_node=m4, order=1),
            Choice(node=m4, text="The crew fled due to fumes", next_node=m5, order=1),
            Choice(node=m4, text="Look for signs of a struggle", next_node=m6, order=2),
        ])
        story.starting_node = m1
        story.save(update_fields=["starting_node"])
